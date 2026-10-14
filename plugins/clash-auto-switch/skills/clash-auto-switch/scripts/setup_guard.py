#!/usr/bin/env python3
"""Install the configured DNS-only guard into root-owned macOS runtime carriers."""
from __future__ import annotations

import argparse
import json
import os
import plistlib
import stat
import subprocess
import tempfile
from pathlib import Path

from recipient_config import load


def trusted(path: Path):
    """Never execute a privileged job from a user-writable or symlink parent."""
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ValueError(f"Privileged path contains symlink: {candidate}")
        if candidate.exists():
            info = candidate.stat()
            if info.st_uid != 0 or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
                raise ValueError(f"Privileged path is not exclusively root writable: {candidate}")


def root_command(*args):
    subprocess.run(["/usr/bin/sudo", "-n", *map(str, args)], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("preview", "enable", "disable", "status"), nargs="?", default="preview")
    args = parser.parse_args()
    config = load(Path(os.environ["CLASH_PUBLIC_CONFIG"]))
    runtime = Path(config["root_runtime_dir"])
    plist = Path(config["plist_dir"]) / (config["label"] + ".plist")
    document = {
        "Label": config["label"], "ProgramArguments": [
            config["python_executable"], str(runtime / "clash-tool"), "--config",
            str(runtime / "recipient.json"), "guard", "run"],
        "EnvironmentVariables": {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        "RunAtLoad": True, "StartInterval": 15, "KeepAlive": False,
        "StandardOutPath": str(Path(config["log_dir"]) / "stdout.log"),
        "StandardErrorPath": str(Path(config["log_dir"]) / "stderr.log"),
    }
    if args.action == "preview":
        print("[PREVIEW] root-owned runtime:", runtime, "\n[PREVIEW] plist:", plist)
        print(plistlib.dumps(document).decode())
        return 0
    if args.action == "status":
        return subprocess.run(["/bin/launchctl", "print", "system/" + config["label"]]).returncode
    for path in (runtime, Path(config["plist_dir"]), Path(config["guard_state_dir"]),
                 Path(config["log_dir"]), Path(config["python_executable"])):
        trusted(path)
    if args.action == "disable":
        # Read first: an absent job needs no mutation, a failed bootout is an error.
        observed = subprocess.run(["/bin/launchctl", "print", "system/" + config["label"]],
                                  capture_output=True)
        if observed.returncode == 0:
            root_command("/bin/launchctl", "bootout", "system/" + config["label"])
        root_command("/bin/launchctl", "disable", "system/" + config["label"])
        return 0
    with tempfile.TemporaryDirectory(prefix="clash-guard-install-") as temporary:
        staging = Path(temporary)
        (staging / "job.plist").write_bytes(plistlib.dumps(document))
        (staging / "recipient.json").write_text(json.dumps(config), encoding="utf-8")
        root_command("/usr/bin/install", "-d", "-m", "0755", runtime, config["plist_dir"])
        root_command("/usr/bin/install", "-d", "-m", "0700", config["log_dir"], config["guard_state_dir"])
        for name in ("clash-tool", "recipient_config.py", "clash_controller.py", "clash_dns_tun_guard.py"):
            root_command("/usr/bin/install", "-m", "0644", Path(__file__).parent / name, runtime / name)
        root_command("/usr/bin/install", "-m", "0600", staging / "recipient.json", runtime / "recipient.json")
        root_command("/usr/bin/install", "-m", "0644", staging / "job.plist", plist)
        # The user's desired-mode state remains explicit and separate; no automatic mode change.
        observed = subprocess.run(["/bin/launchctl", "print", "system/" + config["label"]], capture_output=True)
        if observed.returncode == 0:
            root_command("/bin/launchctl", "bootout", "system/" + config["label"])
        root_command("/bin/launchctl", "enable", "system/" + config["label"])
        root_command("/bin/launchctl", "bootstrap", "system", plist)
    return subprocess.run(["/bin/launchctl", "print", "system/" + config["label"]]).returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"guard setup: {error}", file=__import__("sys").stderr)
        raise SystemExit(1)
