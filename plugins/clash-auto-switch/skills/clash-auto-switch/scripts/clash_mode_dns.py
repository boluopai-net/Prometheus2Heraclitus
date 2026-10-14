#!/usr/bin/env python3
"""Manage the primary macOS network service DNS around Clash TUN mode.

This helper deliberately separates the reversible network-service mutation from
Clash controller changes. It snapshots the exact pre-TUN DNS configuration,
changes only the network service backing the physical default route, and keeps
the snapshot until system-mode convergence has completed.
"""

from __future__ import annotations

import argparse
import contextlib
import ipaddress
import json
import os
import re
import subprocess
import tempfile
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class DnsModeError(RuntimeError):
    """Raised when a safe DNS transition cannot be proven."""


@dataclass(frozen=True)
class DnsConfig:
    mode: str
    servers: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {"mode": self.mode, "servers": list(self.servers)}


@dataclass(frozen=True)
class RestoreState:
    network_service: str
    config: DnsConfig
    tun_dns_server: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "network_service": self.network_service,
            "mode": self.config.mode,
            "servers": list(self.config.servers),
            "tun_dns_server": self.tun_dns_server,
        }


class Runner:
    def __init__(self) -> None:
        self.networksetup = os.environ.get("NETWORKSETUP_BIN", "/usr/sbin/networksetup")
        self.route = os.environ.get("ROUTE_BIN", "/sbin/route")
        self.dig = os.environ.get("DIG_BIN", "/usr/bin/dig")
        self.dscacheutil = os.environ.get("DSCACHEUTIL_BIN", "/usr/bin/dscacheutil")
        self.killall = os.environ.get("KILLALL_BIN", "/usr/bin/killall")
        self.sudo = os.environ.get("SUDO_BIN", "/usr/bin/sudo")
        self.direct_privilege = os.environ.get("CLASH_MODE_DNS_TEST_DIRECT") == "1"

    def run(
        self,
        args: Sequence[str],
        *,
        check: bool = True,
        capture_output: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            list(args),
            check=False,
            text=True,
            capture_output=capture_output,
        )
        if check and result.returncode != 0:
            detail = (result.stderr or result.stdout or "command failed").strip()
            raise DnsModeError(f"{args[0]} failed ({result.returncode}): {detail}")
        return result

    def authorize(self) -> None:
        # Test the permitted command, not sudo -v: this Mac grants specific
        # noninteractive commands without granting an unrestricted sudo ticket.
        service = discover_network_service(self)
        self.privileged([self.networksetup, "-getdnsservers", service])

    def privileged(self, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
        if os.geteuid() == 0 or self.direct_privilege:
            return self.run(args)
        return self.run([self.sudo, "-n", *args])


def state_path() -> Path:
    return Path(os.environ["CLASH_GUARD_MODE_STATE_DIR"]) / "network_dns_restore.json"


def tun_dns_server() -> str:
    value = os.environ.get("CLASH_TUN_DNS_SERVER", "198.18.0.1")
    try:
        ipaddress.ip_address(value)
    except ValueError as exc:
        raise DnsModeError(f"invalid CLASH_TUN_DNS_SERVER: {value}") from exc
    return value


def fake_ip_network() -> ipaddress._BaseNetwork:
    value = os.environ.get("CLASH_TUN_FAKE_IP_CIDR", "198.18.0.0/15")
    try:
        return ipaddress.ip_network(value, strict=False)
    except ValueError as exc:
        raise DnsModeError(f"invalid CLASH_TUN_FAKE_IP_CIDR: {value}") from exc


def parse_default_interface(raw: str) -> str:
    match = re.search(r"(?m)^\s*interface:\s*(\S+)\s*$", raw)
    if not match:
        raise DnsModeError("could not determine the physical default-route interface")
    return match.group(1)


def parse_network_service_order(raw: str, interface: str) -> str:
    current_service: str | None = None
    current_disabled = False
    for line in raw.splitlines():
        service_match = re.match(r"^\(\d+\)\s+(.+?)\s*$", line)
        if service_match:
            current_service = service_match.group(1)
            current_disabled = current_service.startswith("*")
            current_service = current_service.lstrip("*")
            continue
        device_match = re.search(r"Device:\s*([^)]*)\)", line)
        if (
            device_match
            and current_service
            and not current_disabled
            and device_match.group(1).strip() == interface
        ):
            return current_service
    raise DnsModeError(f"no enabled network service owns interface {interface}")


def discover_network_service(runner: Runner) -> str:
    explicit = os.environ.get("CLASH_DNS_NETWORK_SERVICE", "").strip()
    if explicit:
        return explicit
    route = runner.run([runner.route, "-n", "get", "default"])
    interface = parse_default_interface(route.stdout)
    services = runner.run([runner.networksetup, "-listnetworkserviceorder"])
    return parse_network_service_order(services.stdout, interface)


def parse_dns_config(raw: str, service: str) -> DnsConfig:
    text = raw.strip()
    if text.startswith("There aren't any DNS Servers set on "):
        return DnsConfig("automatic", ())
    servers = tuple(line.strip() for line in text.splitlines() if line.strip())
    if not servers:
        raise DnsModeError(f"networksetup returned no DNS state for {service}")
    for server in servers:
        try:
            ipaddress.ip_address(server)
        except ValueError as exc:
            raise DnsModeError(
                f"networksetup returned an invalid DNS server for {service}: {server}"
            ) from exc
    return DnsConfig("manual", servers)


def read_dns_config(runner: Runner, service: str) -> DnsConfig:
    result = runner.run([runner.networksetup, "-getdnsservers", service])
    return parse_dns_config(result.stdout, service)


def write_dns_config(runner: Runner, service: str, config: DnsConfig) -> None:
    if config.mode == "automatic":
        args = [runner.networksetup, "-setdnsservers", service, "Empty"]
    elif config.mode == "manual" and config.servers:
        args = [runner.networksetup, "-setdnsservers", service, *config.servers]
    else:
        raise DnsModeError(f"invalid DNS restore config for {service}: {config}")
    runner.privileged(args)


def flush_dns_cache(runner: Runner) -> None:
    runner.run([runner.dscacheutil, "-flushcache"])
    runner.privileged([runner.killall, "-HUP", "mDNSResponder"])


def load_restore_state(*, required: bool = False) -> RestoreState | None:
    path = state_path()
    if not path.is_file():
        if required:
            raise DnsModeError(f"DNS restore state is missing: {path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DnsModeError(f"DNS restore state is unreadable: {path}: {exc}") from exc
    if payload.get("schema_version") != 1:
        raise DnsModeError(f"unsupported DNS restore state schema: {path}")
    service = payload.get("network_service")
    mode = payload.get("mode")
    servers = payload.get("servers")
    stored_tun_dns = payload.get("tun_dns_server")
    if not isinstance(service, str) or not service:
        raise DnsModeError(f"invalid network service in DNS restore state: {path}")
    if mode not in {"automatic", "manual"}:
        raise DnsModeError(f"invalid DNS mode in restore state: {path}")
    if not isinstance(servers, list) or not all(isinstance(item, str) for item in servers):
        raise DnsModeError(f"invalid DNS servers in restore state: {path}")
    if mode == "automatic" and servers:
        raise DnsModeError(f"automatic DNS restore state contains servers: {path}")
    if mode == "manual" and not servers:
        raise DnsModeError(f"manual DNS restore state has no servers: {path}")
    if not isinstance(stored_tun_dns, str) or not stored_tun_dns:
        raise DnsModeError(f"invalid managed DNS server in restore state: {path}")
    return RestoreState(service, DnsConfig(mode, tuple(servers)), stored_tun_dns)


def atomic_write_restore_state(state: RestoreState) -> None:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(state.as_dict(), stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.close(descriptor)
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)
        raise


def capture_restore_state(runner: Runner, service: str, managed_dns: str) -> RestoreState:
    existing = load_restore_state()
    if existing is not None:
        if existing.network_service != service:
            raise DnsModeError(
                "DNS restore state belongs to "
                f"{existing.network_service}, but the current service is {service}; "
                "switch to system mode before changing the primary network service"
            )
        if existing.tun_dns_server != managed_dns:
            raise DnsModeError(
                "managed DNS server changed while a restore state is active; "
                "restore system mode before changing CLASH_TUN_DNS_SERVER"
            )
        return existing
    current = read_dns_config(runner, service)
    if current == DnsConfig("manual", (managed_dns,)):
        raise DnsModeError(
            f"{service} already uses {managed_dns}, but no restore state exists; "
            "refusing to guess the previous DNS configuration"
        )
    state = RestoreState(service, current, managed_dns)
    atomic_write_restore_state(state)
    return state


def verify_dns_config(runner: Runner, service: str, expected: DnsConfig) -> None:
    observed = read_dns_config(runner, service)
    if observed != expected:
        raise DnsModeError(
            f"DNS verification failed for {service}: expected {expected.as_dict()}, "
            f"observed {observed.as_dict()}"
        )


def verify_tun_dns_target(runner: Runner, managed_dns: str) -> None:
    route = runner.run([runner.route, "-n", "get", managed_dns])
    interface = parse_default_interface(route.stdout)
    if not interface.startswith("utun"):
        raise DnsModeError(
            f"managed DNS target {managed_dns} is routed through {interface}, not a utun interface"
        )
    probe_name = os.environ.get("CLASH_DNS_PROBE_NAME", "steamcommunity.com")
    attempts = max(1, int(os.environ.get("CLASH_DNS_PROBE_ATTEMPTS", "8")))
    delay = max(0.0, float(os.environ.get("CLASH_DNS_PROBE_DELAY_SEC", "0.25")))
    expected_network = fake_ip_network()
    last_detail = "no answer"
    for attempt in range(attempts):
        result = runner.run(
            [
                runner.dig,
                "+time=2",
                "+tries=1",
                "+short",
                f"@{managed_dns}",
                "-p",
                "53",
                "A",
                probe_name,
            ],
            check=False,
        )
        answers: list[ipaddress._BaseAddress] = []
        for line in result.stdout.splitlines():
            try:
                answers.append(ipaddress.ip_address(line.strip()))
            except ValueError:
                continue
        if result.returncode == 0 and any(answer in expected_network for answer in answers):
            return
        last_detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
        if attempt + 1 < attempts:
            time.sleep(delay)
    raise DnsModeError(
        f"Mihomo DNS probe through {managed_dns} did not return a fake IP for "
        f"{probe_name}: {last_detail}"
    )


def apply_tun_dns(runner: Runner) -> dict[str, Any]:
    managed_dns = tun_dns_server()
    service = discover_network_service(runner)
    verify_tun_dns_target(runner, managed_dns)
    runner.authorize()
    state = capture_restore_state(runner, service, managed_dns)
    target = DnsConfig("manual", (managed_dns,))
    write_dns_config(runner, service, target)
    flush_dns_cache(runner)
    verify_dns_config(runner, service, target)
    verify_tun_dns_target(runner, managed_dns)
    return {
        "action": "apply-tun",
        "changed": True,
        "network_service": service,
        "dns": target.as_dict(),
        "restore": state.config.as_dict(),
        "state_file": str(state_path()),
    }


def prepare_system_dns(runner: Runner) -> dict[str, Any]:
    state = load_restore_state()
    if state is None:
        service = discover_network_service(runner)
        current = read_dns_config(runner, service)
        managed = DnsConfig("manual", (tun_dns_server(),))
        if current == managed:
            raise DnsModeError(
                f"{service} still uses managed DNS {managed.servers[0]}, but the restore "
                "state is missing; refusing to clear an unknown previous configuration"
            )
        return {
            "action": "prepare-system",
            "changed": False,
            "network_service": service,
            "dns": current.as_dict(),
            "state_file": str(state_path()),
        }
    runner.authorize()
    write_dns_config(runner, state.network_service, state.config)
    flush_dns_cache(runner)
    verify_dns_config(runner, state.network_service, state.config)
    return {
        "action": "prepare-system",
        "changed": True,
        "network_service": state.network_service,
        "dns": state.config.as_dict(),
        "state_file": str(state_path()),
    }


def rollback_system_dns(runner: Runner) -> dict[str, Any]:
    state = load_restore_state()
    if state is None:
        return {"action": "rollback-system", "changed": False, "state_file": str(state_path())}
    verify_tun_dns_target(runner, state.tun_dns_server)
    runner.authorize()
    target = DnsConfig("manual", (state.tun_dns_server,))
    write_dns_config(runner, state.network_service, target)
    flush_dns_cache(runner)
    verify_dns_config(runner, state.network_service, target)
    return {
        "action": "rollback-system",
        "changed": True,
        "network_service": state.network_service,
        "dns": target.as_dict(),
        "state_file": str(state_path()),
    }


def commit_system_dns() -> dict[str, Any]:
    path = state_path()
    existed = path.is_file()
    if existed:
        path.unlink()
    return {"action": "commit-system", "changed": existed, "state_file": str(path)}


def dns_status(runner: Runner) -> dict[str, Any]:
    service = discover_network_service(runner)
    current = read_dns_config(runner, service)
    state = load_restore_state()
    return {
        "network_service": service,
        "current": current.as_dict(),
        "managed_dns_server": tun_dns_server(),
        "managed": current == DnsConfig("manual", (tun_dns_server(),)),
        "restore_state": state.as_dict() if state else None,
        "system_proxies": read_proxies(runner, service),
        "state_file": str(state_path()),
    }


PROXY_TYPES = ("webproxy", "securewebproxy", "socksfirewallproxy")


def read_proxies(runner: Runner, service: str) -> dict:
    proxies = {}
    for kind in PROXY_TYPES:
        raw = runner.run([runner.networksetup, "-get" + kind, service]).stdout
        values = dict(line.split(": ", 1) for line in raw.splitlines() if ": " in line)
        if values.get("Authenticated Proxy Enabled", "0") != "0":
            raise DnsModeError(
                "authenticated system proxy cannot be restored without its credentials"
            )
        proxies[kind] = {
            "enabled": values.get("Enabled") == "Yes",
            "server": values.get("Server", ""),
            "port": int(values.get("Port", "0")),
        }
    return proxies


def write_proxies(runner: Runner, service: str, proxies: dict) -> None:
    for kind, value in proxies.items():
        if value["server"] and value["port"]:
            runner.privileged(
                [
                    runner.networksetup,
                    "-set" + kind,
                    service,
                    value["server"],
                    str(value["port"]),
                    "off",
                ]
            )
        runner.privileged(
            [
                runner.networksetup,
                "-set" + kind + "state",
                service,
                "on" if value["enabled"] else "off",
            ]
        )
    actual = read_proxies(runner, service)
    for kind, expected in proxies.items():
        # Disabled empty proxy slots have no meaningful server/port identity.
        if actual[kind]["enabled"] != expected["enabled"] or (
            expected["server"] and actual[kind] != expected
        ):
            raise DnsModeError(f"system proxy readback failed: {service}/{kind}")


def transition_checkpoint(runner: Runner, path: Path) -> dict:
    service = discover_network_service(runner)
    runner.authorize()
    # Preserve both the immediate DNS and the original pre-TUN restore record.
    # A failed repeated `tun` must not replace the user's original snapshot.
    files = [state_path()]
    for variable in ("CLASH_MODE_VERGE_FILE", "CLASH_MODE_GUARD_FILE"):
        if os.environ.get(variable):
            files.append(Path(os.environ[variable]))
    saved = {
        "network_service": service,
        "dns": read_dns_config(runner, service).as_dict(),
        "proxies": read_proxies(runner, service),
        "files": {str(p): p.read_text() if p.exists() else None for p in files},
    }
    path.write_text(json.dumps(saved))
    path.chmod(0o600)
    return {"action": "checkpoint", "network_service": service}


def restore_transition(runner: Runner, path: Path) -> dict:
    saved = json.loads(path.read_text())
    service = saved["network_service"]
    config = DnsConfig(saved["dns"]["mode"], tuple(saved["dns"]["servers"]))
    errors = []
    # Attempt all independent restoration steps, retaining the checkpoint on
    # any error rather than stopping after one failed cache or proxy command.
    for operation in (
        lambda: write_dns_config(runner, service, config),
        lambda: write_proxies(runner, service, saved["proxies"]),
        lambda: flush_dns_cache(runner),
        lambda: verify_dns_config(runner, service, config),
    ):
        try:
            operation()
        except DnsModeError as exc:
            errors.append(str(exc))
    for name, content in saved["files"].items():
        destination = Path(name)
        if content is None:
            destination.unlink(missing_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content)
    if errors:
        raise DnsModeError("; ".join(errors))
    return {"action": "restore-transition", "network_service": service}


def set_system_proxy(runner: Runner, path: Path, enabled: bool, port: int) -> dict:
    saved = json.loads(path.read_text())
    service = saved["network_service"]
    proxies = saved["proxies"]
    for value in proxies.values():
        value["enabled"] = enabled
        if enabled:
            value.update(server="127.0.0.1", port=port)
    write_proxies(runner, service, proxies)
    return {"action": "set-proxy", "network_service": service, "enabled": enabled}


def emit(payload: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    action = payload.get("action", "status")
    service = payload.get("network_service", "unknown")
    dns = payload.get("dns") or payload.get("current") or {}
    print(f"system-dns.action={action}")
    print(f"system-dns.service={service}")
    print(f"system-dns.mode={dns.get('mode', 'unknown')}")
    print(f"system-dns.servers={','.join(dns.get('servers', [])) or 'automatic'}")
    if "managed" in payload:
        print(f"system-dns.managed={str(bool(payload['managed'])).lower()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clash_mode_dns")
    parser.add_argument(
        "command",
        choices=(
            "apply-tun",
            "prepare-system",
            "rollback-system",
            "commit-system",
            "status",
            "checkpoint",
            "restore-transition",
            "set-proxy",
        ),
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--enabled", choices=("true", "false"))
    parser.add_argument("--port", type=int, default=7897)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    runner = Runner()
    try:
        if args.command in ("checkpoint", "restore-transition", "set-proxy"):
            if args.checkpoint is None:
                raise DnsModeError("transition operation requires --checkpoint")
            if args.command == "checkpoint":
                payload = transition_checkpoint(runner, args.checkpoint)
            elif args.command == "restore-transition":
                payload = restore_transition(runner, args.checkpoint)
            else:
                if args.enabled is None or not 1 <= args.port <= 65535:
                    raise DnsModeError("set-proxy requires --enabled and a valid port")
                payload = set_system_proxy(
                    runner, args.checkpoint, args.enabled == "true", args.port
                )
        elif args.command == "apply-tun":
            payload = apply_tun_dns(runner)
        elif args.command == "prepare-system":
            payload = prepare_system_dns(runner)
        elif args.command == "rollback-system":
            payload = rollback_system_dns(runner)
        elif args.command == "commit-system":
            payload = commit_system_dns()
        elif args.command == "status":
            payload = dns_status(runner)
        else:
            raise AssertionError(args.command)
    except DnsModeError as exc:
        print(f"[error] {exc}", file=os.sys.stderr)
        return 1
    emit(payload, as_json=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
