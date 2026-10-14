#!/usr/bin/env python3
"""Discover this user's live Mihomo controller, shared by the local Clash tools."""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def runtime_root() -> Path:
    return Path(os.environ["RUNTIME_ROOT"])


def scalar(path: Path, key: str) -> str:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\r\n]*)", raw)
    value = match.group(1).strip().strip("\"'") if match else ""
    return "" if value in {"null", "~"} else value


def runtime_sockets(root: Path) -> list[Path]:
    # The daemon runs as root with the user's HOME. Do not select root's socket
    # or a core belonging to a different logged-in user.
    owner_uid = Path(os.environ["CLASH_TARGET_HOME"]).stat().st_uid
    candidates = []
    process = subprocess.run(
        ["/bin/ps", "-axo", "command="], capture_output=True, text=True, timeout=3, check=False
    )
    for line in process.stdout.splitlines():
        if not re.search(r"(?:^|/)verge-mihomo(?:\s|$)", line):
            continue
        match = re.search(r"(?:^|\s)-ext-ctl-unix(?:=|\s+)(\S+)", line)
        if match:
            candidates.append(Path(match.group(1)))
    candidates.append(Path(f"/var/run/clash-verge-service/users/{owner_uid}/verge-mihomo.sock"))
    for name in ("clash-verge.yaml", "config.yaml"):
        configured = scalar(root / name, "external-controller-unix")
        if configured:
            candidates.append(Path(configured))
    result = []
    for path in candidates:
        try:
            if (
                path.is_absolute()
                and path.is_socket()
                and path.stat().st_uid == owner_uid
                and path not in result
            ):
                result.append(path)
        except OSError:
            continue
    return result


class UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, path: Path, timeout: float):
        super().__init__("localhost", timeout=timeout)
        self.path = path

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(str(self.path))


@dataclass(frozen=True)
class Controller:
    base_url: str
    secret: str = field(default="", repr=False)
    unix_socket: Path | None = None

    @classmethod
    def discover(
        cls,
        root: Path | None = None,
        *,
        socket_override: Path | None = None,
        url_override: str | None = None,
        secret_override: str | None = None,
    ) -> Controller:
        root = root or runtime_root()
        secret = (
            scalar(root / "config.yaml", "secret") if secret_override is None else secret_override
        )
        if url_override:
            parsed = urllib.parse.urlsplit(url_override)
            if parsed.scheme == "unix":
                return cls("http://localhost", secret, Path(urllib.parse.unquote(parsed.path)))
            return cls(url_override.rstrip("/"), secret)
        if socket_override:
            return cls("http://localhost", secret, socket_override)
        for path in runtime_sockets(root):
            candidate = cls("http://localhost", secret, path)
            try:
                version = candidate.request("GET", "/version", timeout=1)
                if isinstance(version, dict) and version.get("version"):
                    return candidate
            except (OSError, RuntimeError, ValueError, http.client.HTTPException):
                continue
        address = scalar(root / "config.yaml", "external-controller") or os.environ.get("CLASH_CONTROLLER_URL", "")
        if not address:
            raise ValueError("No configured controller endpoint")
        return cls(address if "://" in address else "http://" + address, secret)

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Any = None,
        timeout: float = 3,
        allow_empty: bool = False,
    ) -> Any:
        if self.unix_socket:
            connection = UnixHTTPConnection(self.unix_socket, timeout)
        else:
            url = urllib.parse.urlsplit(self.base_url)
            if url.scheme not in {"http", "https"} or not url.hostname:
                raise ValueError("Invalid controller URL")
            connection_type = (
                http.client.HTTPSConnection if url.scheme == "https" else http.client.HTTPConnection
            )
            connection = connection_type(url.hostname, url.port, timeout=timeout)
            path = url.path.rstrip("/") + path
        headers = {"Content-Type": "application/json"}
        if self.secret:
            headers["Authorization"] = "Bearer " + self.secret
        try:
            connection.request(
                method, path, body=None if body is None else json.dumps(body), headers=headers
            )
            response = connection.getresponse()
            raw = response.read()
            if response.status >= 400:
                raise RuntimeError(f"Mihomo {method} {path}: HTTP {response.status}")
            return json.loads(raw) if raw else (None if allow_empty else {})
        finally:
            connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("request", "socket", "bridge", "relay"))
    parser.add_argument("method", nargs="?", default="GET")
    parser.add_argument("path", nargs="?", default="/version")
    parser.add_argument("--body")
    args = parser.parse_args()
    if args.command == "bridge":
        # Each accepted connection resolves the current socket anew; existing
        # streams survive as long as their core does. Bind only to loopback.
        relay = shlex.join([sys.executable, str(Path(__file__).resolve()), "relay"])
        os.execv(
            os.environ["CLASH_SOCAT_BIN"],
            ["socat", "TCP-LISTEN:19090,bind=127.0.0.1,reuseaddr,fork", "EXEC:" + relay],
        )
    explicit = os.environ.get("CLASH_SOCK")
    controller = Controller.discover(
        socket_override=Path(explicit) if explicit else None,
        url_override=os.environ.get("CLASH_CONTROLLER_URL"),
    )
    if args.command in {"socket", "relay"}:
        if controller.unix_socket is None:
            raise RuntimeError("No live Unix controller for this user")
        if args.command == "relay":
            os.execv(
                os.environ["CLASH_SOCAT_BIN"],
                ["socat", "STDIO", "UNIX-CONNECT:" + str(controller.unix_socket)],
            )
        print(controller.unix_socket)
    else:
        print(
            json.dumps(
                controller.request(
                    args.method, args.path, body=json.loads(args.body) if args.body else None
                )
            )
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, http.client.HTTPException) as error:
        print(f"clash-controller: {error}", file=sys.stderr)
        raise SystemExit(1) from error
