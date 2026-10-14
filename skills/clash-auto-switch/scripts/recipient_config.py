"""Recipient configuration for the public Clash tools; no host/account defaults."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

PATH_KEYS = {
    "target_home": "CLASH_TARGET_HOME", "runtime_root": "RUNTIME_ROOT",
    "guard_state_dir": "CLASH_GUARD_STATE_DIR", "mode_state_dir": "CLASH_GUARD_MODE_STATE_DIR",
    "log_dir": "CLASH_GUARD_LOG_DIR", "switch_log_dir": "CLASH_SWITCH_LOG_DIR",
    "python_executable": "PY_BIN", "socat_executable": "CLASH_SOCAT_BIN",
    "root_runtime_dir": "CLASH_ROOT_RUNTIME_DIR", "plist_dir": "CLASH_PLIST_DIR",
    "mutex_executable": "CLASH_MUTEX_EXECUTABLE", "mutex_path": "MACOS_HOME_MUTEX_PATH",
}


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Configuration must be a JSON object")
    for key, variable in PATH_KEYS.items():
        value = data.get(key)
        if not isinstance(value, str) or not Path(value).is_absolute():
            raise ValueError(f"{key} must be an explicit absolute path")
        os.environ[variable] = value
    label = data.get("label", "")
    if not isinstance(label, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]+", label):
        raise ValueError("Choose a recipient-owned launchd label")
    os.environ["CLASH_GUARD_LABEL"] = label
    url = data.get("controller_url", "")
    if not isinstance(url, str) or (url and not url.startswith(("http://", "https://", "unix://"))):
        raise ValueError("controller_url must be empty for socket discovery or an explicit endpoint")
    if url:
        os.environ["CLASH_CONTROLLER_URL"] = url
        os.environ["CLASH_GUARD_CONTROLLER_URL"] = url
    else:
        os.environ.pop("CLASH_CONTROLLER_URL", None)
        os.environ.pop("CLASH_GUARD_CONTROLLER_URL", None)
    for key in ("groups", "direct_groups", "fallback_regions", "excluded_regions"):
        values = data.get(key)
        if not isinstance(values, list) or any(not isinstance(v, str) or "," in v for v in values):
            raise ValueError(f"{key} must be a list of names without commas")
    if not data["groups"] or not data["fallback_regions"]:
        raise ValueError("Choose explicit selector groups and fallback regions")
    os.environ["CLASH_DIRECT_GROUPS"] = ",".join(data["direct_groups"])
    os.environ["CLASH_EXCLUDED_REGIONS"] = ",".join(data["excluded_regions"])
    for key in ("tun_dns_server", "fake_ip_cidr", "probe_url"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise ValueError(f"{key} is required")
    if not data["probe_url"].startswith("https://"):
        raise ValueError("probe_url must be HTTPS")
    os.environ["CLASH_TUN_DNS_SERVER"] = data["tun_dns_server"]
    os.environ["CLASH_TUN_FAKE_IP_CIDR"] = data["fake_ip_cidr"]
    os.environ["CLASH_GUARD_CODEX_TRANSPORT_URL"] = data["probe_url"]
    os.environ["CLASH_GUARD_RUNTIME_ROOT"] = data["runtime_root"]
    if data.get("desired_mode") not in ("tun", "system"):
        raise ValueError("desired_mode must explicitly select tun or system")
    os.environ["CLASH_GUARD_DEFAULT_MODE"] = data["desired_mode"]
    os.environ["CLASH_GUARD_DISABLE_NOTIFICATIONS"] = "1"
    os.environ["CLASH_PUBLIC_CONFIG"] = str(path.resolve())
    return data
