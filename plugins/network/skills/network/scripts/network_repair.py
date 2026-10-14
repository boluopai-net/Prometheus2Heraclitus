#!/usr/bin/env python3
"""Bounded local Clash recovery; also callable through Desktop Commander."""

import argparse
import contextlib
import hashlib
import fcntl
import sys
import json
import os
import re
import signal
import subprocess
import tempfile
import time
import uuid
import zipfile
from pathlib import Path

import yaml

DATA: Path
STORE: Path
BASELINE: Path
APP: str
APP_EXECUTABLE: str
CONTROLLER_COMMAND: str
CONTROLLER_CONFIG: str
PROBE_URL: str
MUTEX_COMMAND: str
MUTEX_PATH: Path
FILES_ONLY = False
GLOBALS = ("profiles/Merge.yaml", "profiles/Script.js")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_current():
    files = {}
    for file in [DATA / "profiles.yaml", *sorted((DATA / "profiles").glob("*"))]:
        if file.is_symlink():
            raise ValueError("Symlink in profile data; recovery requires ordinary files")
        if file.is_file() and (file.suffix in (".yaml", ".yml", ".js")):
            files[str(file.relative_to(DATA))] = file.read_bytes()
    return files


def index_summary(files):
    try:
        index = yaml.safe_load(files.get("profiles.yaml", b""))
        if not isinstance(index, dict) or not isinstance(index.get("items"), list):
            raise ValueError("Profile index is missing or invalid")
        items = index["items"]
        remote = []
        uids = set()
        missing = []
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Invalid profile item")
            name, uid = item.get("file"), item.get("uid")
            if not isinstance(name, str) or Path(name).name != name or name in (".", ".."):
                raise ValueError("Unsafe profile filename")
            if not isinstance(uid, str) or uid in uids:
                raise ValueError("Invalid or duplicate profile UID")
            uids.add(uid)
            if "profiles/" + name not in files:
                missing.append(name)
            if item.get("type") in ("remote", "local"):
                remote.append(item)
        for item in remote:
            for kind in ("merge", "script", "rules", "proxies", "groups"):
                ref = (item.get("option") or {}).get(kind)
                if ref and ref not in uids:
                    missing.append("reference:" + str(ref))
        current = index.get("current")
        if remote and current not in {item["uid"] for item in remote}:
            missing.append("current-profile")
        return {"valid": not missing, "profiles": len(remote), "missing": missing}
    except (ValueError, TypeError, yaml.YAMLError):
        return {"valid": False, "profiles": 0, "error": "Profile index is malformed"}


def reset_globals(files):
    merge = files.get(GLOBALS[0], b"").decode("utf-8", errors="replace")
    script = files.get(GLOBALS[1], b"").decode("utf-8", errors="replace")
    stripped = re.sub(r"//[^\n]*", "", script)
    try:
        merge_default = not merge.strip() or yaml.safe_load(merge) in (
            None,
            {},
            {"profile": {"store-selected": True}},
        )
    except yaml.YAMLError:
        merge_default = False
    # An intentionally empty managed Merge is healthy. Application-owned
    # settings no longer need an extension; do not resurrect an old overlay.
    baseline_merge = BASELINE / "Merge.yaml"
    if merge.strip() and baseline_merge.is_file():
        try:
            if yaml.safe_load(merge) == yaml.safe_load(baseline_merge.read_text()) == {}:
                merge_default = False
        except yaml.YAMLError:
            pass
    script_default = (
        not stripped.strip()
        or re.fullmatch(
            r"\s*function\s+main\s*\([^)]*\)\s*\{\s*return\s+config\s*;?\s*\}\s*", stripped
        )
        is not None
    )
    return [
        name
        for name, is_default in zip(GLOBALS, (merge_default, script_default), strict=True)
        if is_default
    ]


def snapshot(files, kind):
    STORE.mkdir(parents=True, exist_ok=True, mode=0o700)
    identity = time.strftime("%Y%m%d-%H%M%S") + "-" + kind + "-" + uuid.uuid4().hex[:8]
    destination = STORE / (identity + ".zip")
    with destination.open("xb") as stream:
        os.chmod(destination, 0o600)
        with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in files.items():
                archive.writestr(name, data)
    return identity


def load_snapshot(identity):
    if not re.fullmatch(r"[A-Za-z0-9-]+", identity):
        raise ValueError("Use a backup ID returned by this command")
    path = STORE / (identity + ".zip")
    if path.is_symlink():
        raise ValueError("Backup must be an ordinary local file")
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if sum(item.file_size for item in entries) > 64 * 1024 * 1024:
            raise ValueError("Backup exceeds the profile recovery size limit")
        names = [item.filename for item in entries]
        if len(set(names)) != len(names):
            raise ValueError("Duplicate backup entries")
        for name in names:
            parts = Path(name).parts
            if name != "profiles.yaml" and not (
                len(parts) == 2
                and parts[0] == "profiles"
                and parts[1] not in (".", "..")
                and Path(name).suffix in (".yaml", ".yml", ".js")
            ):
                raise ValueError("Backup contains a file outside profile recovery scope")
        return {name: archive.read(name) for name in names}


def app_pids():
    output = subprocess.run(
        ["/bin/ps", "-axo", "pid=,comm="], capture_output=True, text=True, check=True
    ).stdout
    return [
        int(parts[0])
        for line in output.splitlines()
        if len(parts := line.strip().split(None, 1)) == 2 and parts[1] == APP_EXECUTABLE
    ]


def stop_app():
    for pid in app_pids():
        os.kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + 15
    while app_pids():
        if time.monotonic() >= deadline:
            raise RuntimeError("Clash did not exit; no profile files were changed")
        time.sleep(0.2)


def start_app():
    for attempt in range(3):
        result = subprocess.run(
            ["/usr/bin/open", "-g", "-j", "-a", APP], capture_output=True, text=True
        )
        if result.returncode == 0:
            return
        time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(
        "Clash could not reopen; open Clash Verge manually. A rollback backup is retained."
    )


def write_files(files):
    for name, data in files.items():
        destination = DATA / name
        if destination.is_symlink() or destination.parent.is_symlink():
            raise ValueError("Refusing a symlink recovery destination")
        destination.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix=".network-repair-", dir=destination.parent)
        temporary = Path(name)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)


def apply_files(replacement, scope):
    before = read_current()
    changed = {name: data for name, data in replacement.items() if before.get(name) != data}
    if not changed:
        return {"result": "already_current", "scope": scope}
    # Persist recovery before changing app state. Do not remove unreferenced files:
    # orphan deletion is the data-loss pattern this tool exists to recover from.
    recovery = snapshot(before, "rollback")
    started_at = time.time()
    try:
        stop_app()
        if read_current() != before:
            raise RuntimeError(
                "Profile files changed during app shutdown; inspect again before repair"
            )
        try:
            write_files(changed)
        except Exception:
            try:
                write_files({name: before[name] for name in changed if name in before})
            finally:
                for name in changed.keys() - before.keys():
                    created = DATA / name
                    if (
                        created.is_file()
                        and not created.is_symlink()
                        and created.read_bytes() == changed[name]
                    ):
                        created.unlink()
            raise
    except Exception as error:
        with contextlib.suppress(Exception):
            start_app()
        raise RuntimeError(
            f"Repair failed ({type(error).__name__}); rollback backup: {recovery}"
        ) from error
    try:
        start_app()
    except Exception as error:
        raise RuntimeError("Clash failed to reopen; rollback backup: " + recovery) from error
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        generated = DATA / "clash-verge.yaml"
        if app_pids() and generated.exists() and generated.stat().st_mtime >= started_at:
            break
        time.sleep(0.2)
    after = read_current()
    if any(after.get(name) != value for name, value in replacement.items()):
        raise RuntimeError("Profile readback differs; rollback backup: " + recovery)
    if scope == "globals" and any(
        after.get(name) != value for name, value in before.items() if name not in GLOBALS
    ):
        raise RuntimeError("Subscription preservation check failed; rollback backup: " + recovery)
    return {
        "result": "files_restored",
        "scope": scope,
        "rollback": recovery,
        "index": index_summary(after),
        "runtime": status(),
    }


def transport():
    result = subprocess.run(
        [
            "/usr/bin/curl",
            "--silent",
            "--output",
            "/dev/null",
            "--write-out",
            "%{http_code}",
            "--max-time",
            "8",
            PROBE_URL,
        ],
        capture_output=True,
        text=True,
    )
    return {
        "reachable": result.returncode == 0 and result.stdout != "000",
        "http_status": result.stdout.strip(),
        "curl_exit": result.returncode,
    }


def status():
    files = read_current()
    try:
        config = yaml.safe_load((DATA / "clash-verge.yaml").read_bytes()) or {}
    except (OSError, yaml.YAMLError):
        config = {}
    if FILES_ONLY:
        return {"index": index_summary(files), "default_globals": reset_globals(files),
                "backups": [path.stem for path in sorted(STORE.glob("*.zip"), reverse=True)][:12],
                "runtime": "not observed (files-only)"}
    return {
        "index": index_summary(files),
        "default_globals": reset_globals(files),
        "app_running": bool(app_pids()),
        "generated_nodes": len(config.get("proxies") or []),
        "tun": (config.get("tun") or {}).get("enable"),
        "transport": transport(),
        "active_core": core_summary(),
        "backups": [path.stem for path in sorted(STORE.glob("*.zip"), reverse=True)][:12],
    }


def core_summary():
    observed = {}
    for endpoint in ("configs", "rules"):
        result = subprocess.run(
            [
                CONTROLLER_COMMAND,
                "request",
                "GET",
                "/" + endpoint,
            ],
            env={**os.environ, "CLASH_SKILL_CONFIG": CONTROLLER_CONFIG},
            capture_output=True,
            text=True,
        )
        try:
            data = json.loads(result.stdout)
            if endpoint == "configs":
                observed.update(mode=data.get("mode"), tun=(data.get("tun") or {}).get("enable"))
            else:
                rules = data.get("rules", [])
                observed.update(
                    rule_count=len(rules),
                    chatgpt_targets=[
                        r.get("proxy") for r in rules if r.get("payload") == "chatgpt.com"
                    ],
                    steam_download_targets=[
                        r.get("proxy") for r in rules if r.get("payload") == "steamcontent.com"
                    ],
                )
        except (ValueError, TypeError, AttributeError):
            observed[endpoint] = "unavailable"
    return observed


def run(action, identity=None):
    files = read_current()
    if action == "status":
        return status()
    if action == "backup":
        summary = index_summary(files)
        if not summary["valid"] or not summary["profiles"] or reset_globals(files):
            raise ValueError(
                "Current profile set is incomplete or globals are defaults; healthy backup not created"
            )
        return {"backup": snapshot(files, "healthy"), "index": summary}
    if action == "flush-dns":
        for command in (
            ["/usr/bin/dscacheutil", "-flushcache"],
            ["/usr/bin/killall", "-HUP", "mDNSResponder"],
        ):
            subprocess.run(["/usr/bin/sudo", "-n", *command], check=True, capture_output=True)
        return {"result": "dns_cache_reset", "transport": transport()}
    if action == "restore-globals":
        replacement = {name: (BASELINE / Path(name).name).read_bytes() for name in GLOBALS}
        return apply_files(replacement, "globals")
    if action == "repair":
        summary = index_summary(files)
        if summary["profiles"]:
            missing = set(summary.get("missing", []))
            if not summary["valid"] and (
                not missing or missing - {Path(name).name for name in GLOBALS}
            ):
                raise ValueError(
                    "Existing subscriptions have missing dependencies; preserve them and inspect a specific backup"
                )
            reset = reset_globals(files)
            if reset:
                candidates = sorted(STORE.glob("*-healthy-*.zip"), reverse=True)
                source = (
                    load_snapshot(candidates[0].stem)
                    if candidates
                    else {name: (BASELINE / Path(name).name).read_bytes() for name in GLOBALS}
                )
                return apply_files({name: source[name] for name in reset}, "globals")
            return {"result": "no_profile_loss_detected", **status()}
        if not summary["valid"]:
            raise ValueError(
                "Malformed index; preserve existing files and inspect before choosing a snapshot"
            )
        candidates = sorted(STORE.glob("*-healthy-*.zip"), reverse=True)
        if not candidates:
            raise ValueError(
                "No healthy snapshot is available; reimport subscription, then run restore-globals"
            )
        return run("restore-profiles", candidates[0].stem)
    replacement = load_snapshot(identity)
    if action == "restore-profiles":
        current = index_summary(files)
        if current["profiles"] or not current["valid"]:
            raise ValueError(
                "Current subscriptions exist or the index is malformed; refusing replacement"
            )
        summary = index_summary(replacement)
        if not summary["valid"] or not summary["profiles"]:
            raise ValueError("Selected backup has an incomplete profile index")
    return apply_files(replacement, "profiles")


def configure(path):
    global DATA, STORE, BASELINE, APP, APP_EXECUTABLE, CONTROLLER_COMMAND, CONTROLLER_CONFIG
    global PROBE_URL, MUTEX_COMMAND, MUTEX_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("data_root", "backup_root", "baseline_root", "app_path",
                "controller_command", "controller_config", "mutex_command", "mutex_path"):
        if not isinstance(data.get(key), str) or not Path(data[key]).is_absolute():
            raise ValueError(f"{key} must be an explicit absolute path")
    if not isinstance(data.get("probe_url"), str) or not data["probe_url"].startswith("https://"):
        raise ValueError("probe_url must be an explicit HTTPS transport probe")
    DATA, STORE, BASELINE = (Path(data[key]).resolve() for key in
                              ("data_root", "backup_root", "baseline_root"))
    if DATA == STORE or DATA in STORE.parents or STORE in DATA.parents:
        raise ValueError("Recovery archives must be outside app data")
    if BASELINE == DATA or DATA in BASELINE.parents:
        raise ValueError("Baseline must be independent of app data")
    APP = data["app_path"]
    APP_EXECUTABLE = APP + "/Contents/MacOS/clash-verge"
    CONTROLLER_COMMAND = data["controller_command"]
    CONTROLLER_CONFIG = data["controller_config"]
    PROBE_URL = data["probe_url"]
    MUTEX_COMMAND, MUTEX_PATH = data["mutex_command"], Path(data["mutex_path"]).resolve()
    if MUTEX_PATH == DATA or DATA in MUTEX_PATH.parents:
        raise ValueError("Mutex must be outside app data")


def ensure_mutex():
    """Require an inherited lock from the configured executable; never bypass it."""
    raw = os.environ.get("MACOS_HOME_MUTEX_FD", "")
    if raw.isdecimal() and os.environ.get("MACOS_HOME_MUTEX_LOCK_PATH") == str(MUTEX_PATH):
        try:
            descriptor = int(raw)
            held, configured = os.fstat(descriptor), MUTEX_PATH.stat()
            if (held.st_dev, held.st_ino) == (configured.st_dev, configured.st_ino):
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
        except OSError:
            pass
    if not os.path.isfile(MUTEX_COMMAND) or not os.access(MUTEX_COMMAND, os.X_OK):
        raise RuntimeError("Configured mutex executable is missing or not executable")
    env = os.environ.copy()
    env["MACOS_HOME_MUTEX_PATH"] = str(MUTEX_PATH)
    os.execve(MUTEX_COMMAND, [MUTEX_COMMAND, "--", sys.executable, str(Path(__file__).resolve()),
                             *sys.argv[1:]], env)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--files-only", action="store_true", help="Offline status; no app/core/transport access")
    parser.add_argument("--check-config", action="store_true", help="Validate configuration only")
    parser.add_argument(
        "action",
        choices=(
            "status",
            "backup",
            "repair",
            "restore-globals",
            "restore-profiles",
            "rollback",
            "flush-dns",
        ),
    )
    parser.add_argument("backup_id", nargs="?")
    args = parser.parse_args()
    global FILES_ONLY
    try:
        configure(args.config)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    if args.check_config:
        print(json.dumps({"configuration": "valid", "effects": "none"}))
        return
    FILES_ONLY = args.files_only
    if FILES_ONLY and args.action != "status":
        parser.error("--files-only is restricted to status")
    if args.action != "status":
        try:
            ensure_mutex()
        except (OSError, RuntimeError) as error:
            parser.error(str(error))
    if (args.action in ("restore-profiles", "rollback")) != (args.backup_id is not None):
        parser.error(
            "restore-profiles and rollback require one backup ID; other commands take no arguments"
        )
    try:
        print(json.dumps(run(args.action, args.backup_id), ensure_ascii=False))
    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.SubprocessError,
        zipfile.BadZipFile,
    ) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
