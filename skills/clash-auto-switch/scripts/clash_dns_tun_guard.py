#!/usr/bin/env python3
"""One-cycle Clash DNS/TUN guard for macOS.

The guard is intentionally nonresident. Launchd starts it every 15 seconds; each
process performs one locked cycle and exits.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import io
import ipaddress
import json
import os
import re
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from clash_controller import Controller as RuntimeController

APP_BUNDLE_ID = "io.github.clash-verge-rev.clash-verge-rev"
LABEL = os.environ.get("CLASH_GUARD_LABEL", "recipient.clash-dns-tun-guard")
DEFAULT_PROBE_HOSTS = ("chatgpt.com", "github.com", "www.apple.com")
DEFAULT_CODEX_TRANSPORT_URL = "https://chatgpt.com/backend-api/codex/responses"
FAULT_CONFIRM_SECONDS = 15.0


def now() -> float:
    forced = os.environ.get("CLASH_GUARD_NOW")
    if forced:
        return float(forced)
    return time.time()


def sleep_for(seconds: float) -> None:
    scale = float(os.environ.get("CLASH_GUARD_SLEEP_SCALE", "1"))
    if scale <= 0:
        return
    time.sleep(seconds * scale)


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def home() -> Path:
    return Path(os.environ["CLASH_TARGET_HOME"])


def default_runtime_root() -> Path:
    return Path(os.environ["RUNTIME_ROOT"])


def state_dir() -> Path:
    return Path(os.environ["CLASH_GUARD_STATE_DIR"])


def mode_state_dir() -> Path:
    return Path(os.environ["CLASH_GUARD_MODE_STATE_DIR"])


def state_path() -> Path:
    return state_dir() / "state.json"


def desired_mode_path() -> Path:
    return mode_state_dir() / "desired_mode.json"


def log_dir() -> Path:
    return Path(os.environ["CLASH_GUARD_LOG_DIR"])


def event_path() -> Path:
    return log_dir() / "events.jsonl"


def runtime_root() -> Path:
    return Path(
        os.environ.get("CLASH_GUARD_RUNTIME_ROOT", str(default_runtime_root()))
    ).expanduser()


def default_state() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "desired_mode": os.environ["CLASH_GUARD_DEFAULT_MODE"],
        "last_status": "unknown",
        "last_run_at": None,
        "last_fault": None,
        "fault_first_seen_at": None,
        "snapshot": None,
        "incident": None,
    }


def read_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return fallback
    except json.JSONDecodeError:
        return fallback


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        temp = Path(handle.name)
    temp.replace(path)
    if os.environ.get("CLASH_GUARD_STATE_PUBLIC") == "1":
        path.chmod(0o644)


def load_state() -> dict[str, Any]:
    state = default_state()
    loaded = read_json(state_path(), {})
    if isinstance(loaded, dict):
        state.update(loaded)
    mode_state = read_json(desired_mode_path(), {})
    if isinstance(mode_state, dict) and mode_state.get("desired_mode") in {"tun", "system"}:
        state["desired_mode"] = mode_state["desired_mode"]
    return state


def save_state(state: dict[str, Any]) -> None:
    atomic_write_json(state_path(), state)


def append_event(kind: str, **fields: Any) -> None:
    log_dir().mkdir(parents=True, exist_ok=True)
    event = {"ts": now(), "kind": kind, **fields}
    with event_path().open("a", encoding="utf-8") as handle:
        handle.write(json_dumps(event) + "\n")


def send_notification(message: str) -> None:
    if os.environ.get("CLASH_GUARD_DISABLE_NOTIFICATIONS") == "1":
        return
    custom = os.environ.get("CLASH_GUARD_NOTIFICATION_COMMAND")
    if custom:
        command = [custom, "Clash DNS/TUN Guard", message]
    else:
        osascript = "/usr/bin/osascript"
        if not Path(osascript).is_file():
            return
        command = [
            osascript,
            "-e",
            "on run argv",
            "-e",
            "display notification (item 2 of argv) with title (item 1 of argv)",
            "-e",
            "end run",
            "Clash DNS/TUN Guard",
            message,
        ]
    with contextlib.suppress(Exception):
        subprocess.run(command, check=False, capture_output=True, text=True, timeout=5)


def notify_once(incident: dict[str, Any], key: str, message: str) -> None:
    notified = incident.setdefault("notifications", [])
    if not isinstance(notified, list):
        notified = []
        incident["notifications"] = notified
    if key in notified:
        return
    send_notification(message)
    notified.append(key)


@contextlib.contextmanager
def nonblocking_lock() -> Any:
    state_dir().mkdir(parents=True, exist_ok=True)
    lock_file = state_dir() / "lock"
    with lock_file.open("w", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        yield True


def read_scalar_yaml(path: Path, key: str) -> str | None:
    if not path.is_file():
        return None
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped[len(prefix) :].strip().strip("\"'")
            return value or None
    return None


def current_profile_uid() -> str | None:
    return read_scalar_yaml(runtime_root() / "profiles.yaml", "current")


def yaml_mapping_block(path: Path, key: str) -> list[str]:
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line == f"{key}:":
            start = index + 1
            break
    if start is None:
        return []
    block: list[str] = []
    for line in lines[start:]:
        if line and not line[0].isspace() and not line.lstrip().startswith("#"):
            break
        block.append(line)
    return block


def yaml_block_scalar(block: list[str], key: str) -> str | None:
    pattern = re.compile(rf"^\s+{re.escape(key)}:\s*(.*?)\s*$")
    for line in block:
        match = pattern.match(line)
        if not match:
            continue
        value = match.group(1).split(" #", 1)[0].strip().strip("\"'")
        return value or None
    return None


def final_dns_semantics() -> dict[str, Any]:
    # The raw subscription precedes Merge/Script/GUI overrides and is not the
    # configuration that Mihomo uses. /configs does not expose DNS on this core.
    profile = runtime_root() / "clash-verge.yaml"
    if not profile.is_file():
        return {"available": False, "source": "generated_final"}
    block = yaml_mapping_block(profile, "dns")
    if not block:
        return {"available": True, "source": "generated_final", "valid": False}
    enable = yaml_block_scalar(block, "enable")
    enhanced_mode = yaml_block_scalar(block, "enhanced-mode")
    fake_ip_range = yaml_block_scalar(block, "fake-ip-range")
    fake_range_source = "generated_final"
    if fake_ip_range:
        try:
            fake_network = ipaddress.ip_network(fake_ip_range, strict=False)
            fake_range_ok = ipaddress.ip_network("198.18.0.0/16").subnet_of(fake_network)
        except ValueError:
            fake_range_ok = False
    else:
        fake_range_ok = False
    doh = any("https://" in line.split("#", 1)[0] for line in block)
    valid = enable in {"true", "True"} and enhanced_mode == "fake-ip" and fake_range_ok and doh
    return {
        "available": True,
        "source": "generated_final",
        "valid": valid,
        "enable": enable in {"true", "True"},
        "enhanced_mode": enhanced_mode,
        "fake_ip_range": fake_ip_range,
        "fake_ip_range_source": fake_range_source,
        "doh": doh,
    }


def app_exists() -> bool:
    forced = os.environ.get("CLASH_GUARD_ASSUME_APP")
    if forced is not None:
        return forced not in {"0", "false", "False", "no"}
    probe_command = os.environ.get("CLASH_GUARD_PROCESS_PROBE_COMMAND")
    if probe_command:
        try:
            result = subprocess.run(
                probe_command,
                shell=True,
                check=False,
                capture_output=True,
                text=True,
                timeout=2,
            )
            return result.returncode == 0
        except Exception:
            return False
    try:
        result = subprocess.run(
            ["pgrep", "-f", f"Clash Verge|clash-verge|{APP_BUNDLE_ID}"],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return result.returncode == 0
    except Exception:
        return False


class Controller(RuntimeController):
    @classmethod
    def from_runtime(cls) -> Controller:
        explicit = os.environ.get("CLASH_GUARD_SOCK")
        return cls.discover(
            runtime_root(),
            socket_override=Path(explicit) if explicit else None,
            url_override=os.environ.get("CLASH_GUARD_CONTROLLER_URL"),
            secret_override=os.environ.get("CLASH_GUARD_SECRET"),
        )


def controller_snapshot(controller: Controller) -> tuple[dict[str, Any], dict[str, str]]:
    configs = controller.request("GET", "/configs", timeout=3)
    proxies = controller.request("GET", "/proxies", timeout=3)
    selectors: dict[str, str] = {}
    proxy_items = proxies.get("proxies", {}) if isinstance(proxies, dict) else {}
    if isinstance(proxy_items, dict):
        for name, payload in proxy_items.items():
            if isinstance(payload, dict) and isinstance(payload.get("now"), str):
                selectors[str(name)] = str(payload["now"])
    return configs if isinstance(configs, dict) else {}, selectors


def tun_invariants(configs: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    tun = configs.get("tun")
    if not isinstance(tun, dict):
        return False, {"available": False}
    hijack = tun.get("dns-hijack")
    hijack_ok = isinstance(hijack, list) and "any:53" in hijack
    stack = tun.get("stack")
    stack_ok = isinstance(stack, str) and stack.lower() == "gvisor"
    evidence = {
        "available": True,
        "enable": tun.get("enable") is True,
        "auto_route": tun.get("auto-route") is True,
        "stack": stack,
        "dns_hijack": hijack_ok,
    }
    return (
        evidence["enable"] and evidence["auto_route"] and stack_ok and evidence["dns_hijack"],
        evidence,
    )


def dns_invariants(configs: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    profile = final_dns_semantics()
    if profile.get("available") is True:
        return profile.get("valid") is True, profile
    dns = configs.get("dns")
    evidence = {
        "available": isinstance(dns, dict),
        "source": "controller",
        "enhanced_mode": dns.get("enhanced-mode") if isinstance(dns, dict) else None,
    }
    return evidence["enhanced_mode"] == "fake-ip", evidence


def fake_ip_ok() -> tuple[bool, str]:
    forced = os.environ.get("CLASH_GUARD_FAKE_IP")
    address = forced
    if not address:
        addresses = resolve_system_addresses(DEFAULT_PROBE_HOSTS[0], timeout=3)
        address = addresses[0] if addresses else None
    if not address:
        return False, "fake_ip_unavailable"
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        return False, f"fake_ip_invalid:{address}"
    if ip not in ipaddress.ip_network("198.18.0.0/16"):
        return False, f"fake_ip_out_of_range:{address}"
    iface = os.environ.get("CLASH_GUARD_ROUTE_IFACE") or route_iface(address)
    if iface and iface.startswith("utun"):
        return True, f"{address}:{iface}"
    return False, f"route_not_utun:{address}:{iface or 'unknown'}"


def resolve_system_addresses(hostname: str, *, timeout: float) -> list[str]:
    resolver = os.environ.get("CLASH_GUARD_SYSTEM_RESOLVER_BIN", "/usr/bin/dscacheutil")
    if not Path(resolver).is_file() or not os.access(resolver, os.X_OK):
        return []
    try:
        result = subprocess.run(
            [resolver, "-q", "host", "-a", "name", hostname],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except Exception:
        return []
    if result.returncode != 0:
        return []
    addresses: list[str] = []
    for line in result.stdout.splitlines():
        match = re.match(r"^ip_address:\s*(\S+)\s*$", line.strip())
        if match:
            addresses.append(match.group(1))
    return addresses


def route_iface(address: str) -> str | None:
    try:
        result = subprocess.run(
            ["route", "-n", "get", address],
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except Exception:
        return None
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("interface:"):
            return stripped.split(":", 1)[1].strip()
    return None


def probe_hosts() -> tuple[int, dict[str, str]]:
    forced = os.environ.get("CLASH_GUARD_PROBE_RESULTS")
    if forced:
        results = {}
        failures = 0
        for item in forced.split(","):
            host, _, value = item.partition("=")
            ok = value.strip().lower() in {"ok", "true", "1", "pass"}
            results[host.strip()] = "ok" if ok else "failed"
            failures += 0 if ok else 1
        return failures, results

    timeout = float(os.environ.get("CLASH_GUARD_PROBE_TIMEOUT", "4"))
    fake_network = ipaddress.ip_network("198.18.0.0/16")
    results: dict[str, str] = {}
    failures = 0
    for host in DEFAULT_PROBE_HOSTS:
        addresses = resolve_system_addresses(host, timeout=timeout)
        ok = False
        detail = "resolve_failed"
        for address in addresses:
            try:
                parsed = ipaddress.ip_address(address)
            except ValueError:
                detail = "invalid_address"
                continue
            if parsed not in fake_network:
                detail = "outside_fake_ip"
                continue
            iface = os.environ.get("CLASH_GUARD_ROUTE_IFACE") or route_iface(address)
            if not iface or not iface.startswith("utun"):
                detail = "route_not_utun"
                continue
            ok = True
            detail = "ok"
            break
        results[host] = detail
        failures += 0 if ok else 1
    return failures, results


def probe_codex_transport() -> tuple[bool, dict[str, Any]]:
    forced = os.environ.get("CLASH_GUARD_CODEX_TRANSPORT_RESULT")
    if forced:
        ok = forced.strip().lower() in {"ok", "true", "1", "pass"}
        return ok, {"status": "ok" if ok else "connection_failed", "forced": True}

    curl_bin = os.environ.get("CLASH_GUARD_CURL_BIN", "/usr/bin/curl")
    url = os.environ.get("CLASH_GUARD_CODEX_TRANSPORT_URL", DEFAULT_CODEX_TRANSPORT_URL)
    try:
        result = subprocess.run(
            [
                curl_bin,
                "--silent",
                "--show-error",
                "--connect-timeout",
                "4",
                "--max-time",
                "8",
                "--output",
                "/dev/null",
                "--write-out",
                "%{http_code}",
                url,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:
        return False, {
            "status": "connection_failed",
            "error_type": type(exc).__name__,
        }
    if result.returncode != 0:
        return False, {
            "status": "connection_failed",
            "curl_code": result.returncode,
        }
    http_status = result.stdout.strip()
    return True, {
        "status": "ok",
        "http_status": http_status if re.fullmatch(r"\d{3}", http_status) else "received",
    }


def classify_health(controller: Controller) -> dict[str, Any]:
    app_running = app_exists()
    if not app_running:
        return {"status": "inactive_app_absent", "healthy": True}
    state = load_state()
    if state.get("desired_mode") == "system":
        return {"status": "inactive_system_mode", "healthy": True, "app_running": True}
    try:
        configs, selectors = controller_snapshot(controller)
    except Exception as exc:
        return {
            "status": "controller_unavailable",
            "healthy": False,
            "fault": "controller_unavailable",
            "detail": str(exc),
            "app_running": True,
        }
    tun_ok, tun_evidence = tun_invariants(configs)
    dns_ok, dns_evidence = dns_invariants(configs)
    if not tun_ok or not dns_ok:
        return {
            "status": "degraded",
            "healthy": False,
            "fault": "tun_down" if not tun_ok else "dns_configuration_invalid",
            "configs": public_configs(configs, dns_evidence=dns_evidence),
            "invariants": {"tun": tun_evidence, "dns": dns_evidence},
            "selectors": selectors,
            "app_running": True,
        }
    fake_ok, fake_detail = fake_ip_ok()
    if not fake_ok:
        fake_fault = (
            "dns_stalled"
            if fake_detail.split(":", 1)[0]
            in {"fake_ip_unavailable", "fake_ip_invalid", "fake_ip_out_of_range"}
            else "tun_down"
        )
        return {
            "status": "degraded",
            "healthy": False,
            "fault": fake_fault,
            "fault_source": "fake_ip_resolution"
            if fake_fault == "dns_stalled"
            else "fake_ip_route",
            "detail": fake_detail,
            "configs": public_configs(configs, dns_evidence=dns_evidence),
            "selectors": selectors,
            "app_running": True,
        }
    failures, probes = probe_hosts()
    if failures >= 2:
        return {
            "status": "degraded",
            "healthy": False,
            "fault": "dns_stalled",
            "probe_failures": failures,
            "probes": probes,
            "configs": public_configs(configs, dns_evidence=dns_evidence),
            "selectors": selectors,
            "app_running": True,
        }
    transport_ok, transport_probe = probe_codex_transport()
    if not transport_ok:
        return {
            "status": "degraded",
            "healthy": False,
            "fault": "chatgpt_transport_stalled",
            "probes": probes,
            "codex_transport": transport_probe,
            "configs": public_configs(configs, dns_evidence=dns_evidence),
            "selectors": selectors,
            "app_running": True,
        }
    return {
        "status": "healthy",
        "healthy": True,
        "configs": public_configs(configs, dns_evidence=dns_evidence),
        "invariants": {"tun": tun_evidence, "dns": dns_evidence},
        "selectors": selectors,
        "profile": current_profile_uid(),
        "probes": probes,
        "codex_transport": transport_probe,
        "app_running": True,
    }


def public_configs(
    configs: dict[str, Any], *, dns_evidence: dict[str, Any] | None = None
) -> dict[str, Any]:
    return {
        "tun": configs.get("tun"),
        "dns": configs.get("dns"),
        "dns_semantics": dns_evidence,
        "mixed-port": configs.get("mixed-port"),
    }


def health_event_evidence(health: dict[str, Any]) -> dict[str, Any]:
    return {
        key: health[key]
        for key in (
            "fault_source",
            "detail",
            "invariants",
            "probe_failures",
            "probes",
            "codex_transport",
        )
        if key in health
    }


def refresh_healthy_snapshot(state: dict[str, Any], health: dict[str, Any]) -> None:
    state["last_status"] = "healthy"
    state["last_run_at"] = now()
    state["last_fault"] = None
    state["fault_first_seen_at"] = None
    state["incident"] = None
    state["snapshot"] = {
        "updated_at": now(),
        "desired_mode": state.get("desired_mode", "tun"),
        "profile": health.get("profile"),
        "selectors": health.get("selectors", {}),
    }


def mark_inactive(state: dict[str, Any], status: str) -> None:
    state["last_status"] = status
    state["last_run_at"] = now()
    state["last_fault"] = None
    state["fault_first_seen_at"] = None
    state["incident"] = None


def confirmed_fault(state: dict[str, Any], fault: str) -> bool:
    current = now()
    if state.get("last_fault") != fault:
        state["last_fault"] = fault
        state["fault_first_seen_at"] = current
        state["last_status"] = "pending"
        return False
    raw_first_seen = state.get("fault_first_seen_at")
    first_seen = float(raw_first_seen) if raw_first_seen is not None else current
    state["last_status"] = "pending" if current - first_seen < FAULT_CONFIRM_SECONDS else "degraded"
    return current - first_seen >= FAULT_CONFIRM_SECONDS


def incident_state(state: dict[str, Any], fault: str) -> dict[str, Any]:
    incident = state.get("incident")
    if not isinstance(incident, dict) or incident.get("fault") != fault:
        incident = {
            "fault": fault,
            "started_at": now(),
            "notifications": [],
        }
        state["incident"] = incident
    else:
        incident.setdefault("notifications", [])
    return incident


def reset_system_dns_cache() -> tuple[bool, dict[str, Any]]:
    custom = os.environ.get("CLASH_GUARD_SYSTEM_DNS_RESET_COMMAND")
    if custom:
        commands = [[custom]]
    else:
        if os.geteuid() != 0:
            return False, {"reason": "root_required"}
        commands = [
            ["/usr/bin/dscacheutil", "-flushcache"],
            ["/usr/bin/killall", "-HUP", "mDNSResponder"],
        ]

    completed: list[str] = []
    for command in commands:
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except Exception as exc:
            return False, {
                "reason": "command_exception",
                "command": Path(command[0]).name,
                "error_type": type(exc).__name__,
                "completed": completed,
            }
        if result.returncode != 0:
            return False, {
                "reason": "command_failed",
                "command": Path(command[0]).name,
                "returncode": result.returncode,
                "completed": completed,
            }
        completed.append(Path(command[0]).name)
    return True, {"commands": completed}


def recover(
    state: dict[str, Any],
    controller: Controller,
    fault: str,
    evidence: dict[str, Any],
    controller_was_available: bool,
    app_was_running: bool,
) -> str:
    incident = incident_state(state, fault)
    incident["evidence"] = evidence
    del controller_was_available, app_was_running

    if fault not in {"dns_stalled", "chatgpt_transport_stalled"}:
        outcome = f"observed_{fault}"
        state["last_status"] = outcome
        append_event("observed", fault=fault, action="none", **evidence)
        notify_once(
            incident,
            outcome,
            f"Observed {fault}; DNS guard made no Clash runtime change",
        )
        return outcome

    reset_ok, reset_detail = reset_system_dns_cache()
    incident["system_dns_reset"] = reset_detail
    if not reset_ok:
        state["last_status"] = "failed_system_dns_reset"
        append_event(
            "failure",
            reason="system_dns_reset_failed",
            detail=reset_detail,
        )
        notify_once(
            incident,
            "failed_system_dns_reset",
            "System DNS reset failed; root LaunchDaemon installation is required",
        )
        return "failed_system_dns_reset"

    append_event(
        "recovery",
        fault=fault,
        action="system_dns_reset",
        **evidence,
        **reset_detail,
    )
    notify_once(
        incident,
        "system_dns_reset",
        "Reset macOS DNS caches after confirmed Codex transport or DNS stall",
    )
    sleep_for(2)
    if classify_health(controller).get("healthy") is True:
        state["last_status"] = "repaired"
        return "repaired"

    # The request that triggered the reset may already have failed, and the
    # forced test probe can remain stale until the next launchd cycle. Record a
    # successful reset without escalating into Clash config or process changes.
    state["last_status"] = "dns_reset_sent"
    state["last_fault"] = None
    state["fault_first_seen_at"] = None
    state["incident"] = None
    return "dns_reset_sent"


def command_check(args: argparse.Namespace) -> int:
    controller = Controller.from_runtime()
    health = classify_health(controller)
    if args.json:
        print(json_dumps(health))
    else:
        print(health["status"])
    if health.get("healthy") is True:
        return 0
    if health.get("fault") in {
        "dns_stalled",
        "chatgpt_transport_stalled",
        "tun_down",
        "controller_unavailable",
        "dns_configuration_invalid",
    }:
        return 1
    return 2


def command_run(args: argparse.Namespace) -> int:
    with nonblocking_lock() as acquired:
        if not acquired:
            result = {"status": "pending_lock", "healthy": True}
            if args.json:
                print(json_dumps(result))
            else:
                print("pending_lock")
            return 0
        controller = Controller.from_runtime()
        state = load_state()
        health = classify_health(controller)
        status = str(health.get("status"))
        if health.get("healthy") is True:
            if status == "healthy":
                refresh_healthy_snapshot(state, health)
            else:
                mark_inactive(state, status)
            save_state(state)
            if args.json:
                print(json_dumps({"status": status, "state": state}))
            return 0
        fault = str(health.get("fault") or "unknown")
        evidence = health_event_evidence(health)
        if not confirmed_fault(state, fault):
            state["last_run_at"] = now()
            save_state(state)
            append_event("pending", fault=fault, **evidence)
            if args.json:
                print(
                    json_dumps(
                        {
                            "status": "pending",
                            "fault": fault,
                            "evidence": evidence,
                            "state": state,
                        }
                    )
                )
            return 0
        controller_available = fault != "controller_unavailable"
        outcome = recover(
            state,
            controller,
            fault,
            evidence,
            controller_available,
            bool(health.get("app_running")),
        )
        state["last_run_at"] = now()
        save_state(state)
        if args.json:
            print(
                json_dumps(
                    {
                        "status": outcome,
                        "fault": fault,
                        "evidence": evidence,
                        "state": state,
                    }
                )
            )
        else:
            print(outcome)
        return 0 if outcome in {"repaired", "dns_reset_sent"} else 1


def command_status(args: argparse.Namespace) -> int:
    state = load_state()
    if args.json:
        print(json_dumps(state))
    else:
        print(f"status={state.get('last_status')}")
        print(f"desired_mode={state.get('desired_mode')}")
        print(f"last_run_at={state.get('last_run_at')}")
    return 0


def set_desired_mode(mode: str) -> None:
    if mode not in {"tun", "system"}:
        raise SystemExit("desired mode must be tun or system")
    atomic_write_json(desired_mode_path(), {"desired_mode": mode})


class FakeControllerHandler(BaseHTTPRequestHandler):
    configs = {
        "tun": {
            "enable": True,
            "auto-route": True,
            "strict-route": True,
            "stack": "gVisor",
            "dns-hijack": ["any:53"],
        },
        "dns": {"enhanced-mode": "fake-ip"},
        "mixed-port": 7897,
    }
    proxies = {"proxies": {"GLOBAL": {"now": "node-a"}, "Proxies": {"now": "node-a"}}}
    calls: list[str] = []

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _send(self, status: int = 200, payload: Any = None) -> None:
        raw = b"" if payload is None else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        self.calls.append(f"GET {self.path}")
        if self.path == "/configs":
            self._send(payload=self.configs)
        elif self.path == "/proxies":
            self._send(payload=self.proxies)
        else:
            self._send(404, {})


def command_self_test(args: argparse.Namespace) -> int:
    with tempfile.TemporaryDirectory(prefix="clash-guard-self-test-") as temp:
        root = Path(temp)
        runtime = root / "runtime"
        runtime.mkdir()
        (runtime / "config.yaml").write_text(
            "external-controller: 127.0.0.1:1\nsecret: test\n", encoding="utf-8"
        )
        (runtime / "profiles.yaml").write_text("current: profile-a\n", encoding="utf-8")
        (runtime / "profiles").mkdir()
        (runtime / "clash-verge.yaml").write_text(
            "dns:\n"
            "  enable: true\n"
            "  enhanced-mode: fake-ip\n"
            "  fake-ip-range: 198.18.0.0/15\n"
            "  nameserver:\n"
            "    - https://1.1.1.1/dns-query\n",
            encoding="utf-8",
        )
        FakeControllerHandler.calls = []
        FakeControllerHandler.configs["tun"] = {
            "enable": True,
            "auto-route": True,
            "strict-route": True,
            "stack": "gVisor",
            "dns-hijack": ["any:53"],
        }
        server = ThreadingHTTPServer(("127.0.0.1", 0), FakeControllerHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        env_backup = dict(os.environ)
        os.environ["CLASH_GUARD_DEFAULT_MODE"] = "tun"
        os.environ["CLASH_GUARD_MODE_STATE_DIR"] = str(root / "mode-state")
        os.environ["CLASH_GUARD_STATE_DIR"] = str(root / "state")
        os.environ["CLASH_GUARD_LOG_DIR"] = str(root / "logs")
        os.environ["CLASH_GUARD_RUNTIME_ROOT"] = str(runtime)
        os.environ["CLASH_GUARD_CONTROLLER_URL"] = f"http://127.0.0.1:{server.server_port}"
        os.environ["CLASH_GUARD_ASSUME_APP"] = "1"
        os.environ["CLASH_GUARD_FAKE_IP"] = "198.18.0.10"
        os.environ["CLASH_GUARD_ROUTE_IFACE"] = "utun9"
        os.environ["CLASH_GUARD_PROBE_RESULTS"] = "chatgpt.com=ok,github.com=ok,www.apple.com=ok"
        os.environ["CLASH_GUARD_CODEX_TRANSPORT_RESULT"] = "ok"
        reset_marker = root / "system-dns-reset"
        reset_command = root / "reset-system-dns"
        reset_command.write_text(
            f"#!/bin/sh\n/usr/bin/touch {reset_marker}\n",
            encoding="utf-8",
        )
        reset_command.chmod(0o755)
        os.environ["CLASH_GUARD_SYSTEM_DNS_RESET_COMMAND"] = str(reset_command)
        try:
            os.environ["CLASH_GUARD_NOW"] = "100"
            with contextlib.redirect_stdout(io.StringIO()):
                healthy_rc = command_run(argparse.Namespace(json=True))
            os.environ["CLASH_GUARD_PROBE_RESULTS"] = (
                "chatgpt.com=fail,github.com=fail,www.apple.com=ok"
            )
            os.environ["CLASH_GUARD_NOW"] = "115"
            with contextlib.redirect_stdout(io.StringIO()):
                pending_rc = command_run(argparse.Namespace(json=True))
            os.environ["CLASH_GUARD_NOW"] = "130"
            with contextlib.redirect_stdout(io.StringIO()):
                repaired_rc = command_run(argparse.Namespace(json=True))
            state = load_state()
        finally:
            server.shutdown()
            os.environ.clear()
            os.environ.update(env_backup)
        calls = FakeControllerHandler.calls
        result = {
            "ok": (
                healthy_rc == 0
                and pending_rc == 0
                and repaired_rc == 0
                and state.get("last_status") == "dns_reset_sent"
                and reset_marker.is_file()
                and calls.count("POST /restart") == 0
                and not any("/cache/" in call for call in calls)
                and "PUT /restart" not in calls
            ),
            "state": state,
            "calls": calls,
        }
    if args.json:
        print(json_dumps(result))
    else:
        print("ok" if result["ok"] else "failed")
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clash_dns_tun_guard")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "run", "status", "self-test"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--json", action="store_true")
    hidden = sub.add_parser("_set-desired-mode")
    hidden.add_argument("mode", choices=("tun", "system"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        return command_check(args)
    if args.command == "run":
        return command_run(args)
    if args.command == "status":
        return command_status(args)
    if args.command == "self-test":
        return command_self_test(args)
    if args.command == "_set-desired-mode":
        set_desired_mode(args.mode)
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
