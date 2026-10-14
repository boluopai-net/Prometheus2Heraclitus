#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import pathlib
import re
import secrets
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

import yaml

LOG_ROOT: pathlib.Path
DEFAULT_RUNTIME_CONFIG: pathlib.Path
DEFAULT_PROFILES_INDEX: pathlib.Path

DEFAULT_CONTROLLER = "http://127.0.0.1:9090"
DEFAULT_IP_ENDPOINT = "https://api64.ipify.org?format=json"
DEFAULT_CF_TRACE_ENDPOINT = "https://www.cloudflare.com/cdn-cgi/trace"
DEFAULT_PROXYCHECK_URL = "https://proxycheck.io/v3/{ip}?vpn=1&risk=1&days=30{key_param}"
DEFAULT_ISOLATED_PORTS = {"mixed": 17897, "socks": 17898, "controller": 19097}
COLIMA_PROFILE: str
DEFAULT_PROVIDER_SELECTOR = "GLOBAL"
COLIMA_RUNTIME_ROOT = pathlib.Path("/tmp/proxy-purity")
COLIMA_EXECUTABLE_CANDIDATES = ("mihomo", "clash")
PROXYCHECK_API_ENV = "PROXYCHECK_API_KEY"
COLIMA_MIHOMO_IMAGE = "metacubex/mihomo:latest"
COLIMA_CONTAINER_NAME_PREFIX = "proxy-purity"
COLIMA_RUNTIME_CONFIG_DIR = COLIMA_RUNTIME_ROOT / "config"
COLIMA_RUNTIME_LOG_DIR = COLIMA_RUNTIME_ROOT / "logs"
COLIMA_RUNTIME_BIN_DIR = COLIMA_RUNTIME_ROOT / "bin"
COLIMA_MIHOMO_BINARY = COLIMA_RUNTIME_BIN_DIR / "mihomo"
COLIMA_GITHUB_RELEASE_API = "https://api.github.com/repos/MetaCubeX/mihomo/releases/latest"
COLIMA_MIHOMO_ASSET_PATTERN = re.compile(r"mihomo-linux-(?:arm64|aarch64)-.*\.gz$", re.IGNORECASE)
COLIMA_MIHOMO_BINARY_GZ = COLIMA_RUNTIME_BIN_DIR / "mihomo.gz"
COLIMA_MIHOMO_IMAGE_HINT = (
    "If binary bootstrap fails, use a preinstalled mihomo binary or adjust the download URL."
)
COLIMA_START_TIMEOUT_SEC = 20.0
ISOLATED_SCAN_HELP = "scan a live remote profile through isolated Colima Mihomo"
IPQS_BATCH_HEADER = ["ip"]
PROFILE_GROUP_KEY = "proxy-groups"
PROFILE_PROXY_KEY = "proxies"
MULTIPLIER_PATTERN = re.compile(r"丨(\d+)x")

NON_PROXY_NAMES = {
    "DIRECT",
    "REJECT",
    "PASS",
    "GLOBAL",
    "MATCH",
}

REGION_PATTERNS: dict[str, tuple[str, ...]] = {
    "HK": ("香港", "hk", "hongkong", "hong kong"),
    "JP": ("日本", "jp", "japan", "tokyo", "osaka"),
    "SG": ("新加坡", "sg", "singapore"),
    "TW": ("台湾", "台灣", "tw", "taiwan"),
    "US": ("美国", "美國", "us", "usa", "united states"),
    "KR": ("韩国", "韓國", "kr", "korea", "seoul"),
    "GB": ("英国", "英國", "uk", "united kingdom", "london"),
    "DE": ("德国", "德國", "de", "germany", "frankfurt"),
}


class ProxyPurityError(RuntimeError):
    pass


@dataclass(frozen=True)
class RemoteProfile:
    uid: str
    name: str
    path: pathlib.Path

    @property
    def output_key(self) -> str:
        candidate = pathlib.Path(self.name).stem or self.uid
        slug = re.sub(r"[^A-Za-z0-9._-]+", "-", candidate).strip("-.").lower()
        return slug or self.uid.lower()


@dataclass
class RuntimeSettings:
    controller: str
    secret: str


@dataclass
class NodeObservation:
    round_index: int
    exit_ip: str = ""
    latency_ms: int | None = None
    cf_loc: str = ""
    cf_colo: str = ""
    error: str = ""


@dataclass
class PurityResult:
    selector: str
    node: str
    expected_country: str
    exit_ip: str
    unique_exit_ips: list[str]
    avg_latency_ms: float | None
    min_latency_ms: int | None
    max_latency_ms: int | None
    cf_loc: str
    cf_colo: str
    score: int
    grade: str
    notes: list[str] = field(default_factory=list)
    proxycheck: dict[str, Any] = field(default_factory=dict)
    ipqs: dict[str, Any] = field(default_factory=dict)
    rounds: list[NodeObservation] = field(default_factory=list)

    def to_csv_row(self) -> dict[str, Any]:
        proxycheck_network = self.proxycheck.get("network", {})
        proxycheck_location = self.proxycheck.get("location", {})
        proxycheck_detections = self.proxycheck.get("detections", {})
        return {
            "selector": self.selector,
            "node": self.node,
            "expected_country": self.expected_country,
            "exit_ip": self.exit_ip,
            "unique_exit_ip_count": len(self.unique_exit_ips),
            "unique_exit_ips": "|".join(self.unique_exit_ips),
            "avg_latency_ms": "" if self.avg_latency_ms is None else f"{self.avg_latency_ms:.1f}",
            "min_latency_ms": "" if self.min_latency_ms is None else self.min_latency_ms,
            "max_latency_ms": "" if self.max_latency_ms is None else self.max_latency_ms,
            "cf_loc": self.cf_loc,
            "cf_colo": self.cf_colo,
            "proxycheck_country": proxycheck_location.get("country_code", ""),
            "proxycheck_asn": proxycheck_network.get("asn", ""),
            "proxycheck_provider": proxycheck_network.get("provider", ""),
            "proxycheck_type": proxycheck_network.get("type", ""),
            "proxycheck_hosting": truthy_text(proxycheck_detections.get("hosting")),
            "proxycheck_vpn": truthy_text(proxycheck_detections.get("vpn")),
            "proxycheck_proxy": truthy_text(proxycheck_detections.get("proxy")),
            "proxycheck_tor": truthy_text(proxycheck_detections.get("tor")),
            "proxycheck_risk": proxycheck_detections.get("risk", ""),
            "ipqs_fraud_score": self.ipqs.get("fraud_score", ""),
            "ipqs_proxy": truthy_text(self.ipqs.get("proxy")),
            "ipqs_vpn": truthy_text(self.ipqs.get("vpn")),
            "ipqs_tor": truthy_text(self.ipqs.get("tor")),
            "score": self.score,
            "grade": self.grade,
            "notes": " | ".join(self.notes),
        }


def truthy_text(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return ""


def load_runtime_settings(
    config_path: pathlib.Path | None = None,
    controller_override: str | None = None,
    secret_override: str | None = None,
) -> RuntimeSettings:
    config_path = config_path or DEFAULT_RUNTIME_CONFIG
    raw = ""
    if config_path.exists():
        raw = config_path.read_text(encoding="utf-8", errors="ignore")

    controller = controller_override or env_text("PROXY_PURITY_CONTROLLER") or DEFAULT_CONTROLLER
    secret = secret_override or env_text("PROXY_PURITY_SECRET") or ""

    controller_match = re.search(r"(?m)^external-controller:\s*([^\r\n#]+)", raw)
    if controller_match and not controller_override and not env_text("PROXY_PURITY_CONTROLLER"):
        value = controller_match.group(1).strip().strip("\"'")
        if value:
            controller = value if value.startswith(("http://", "https://")) else f"http://{value}"

    secret_match = re.search(r"(?m)^secret:\s*([^\r\n#]+)", raw)
    if secret_match and not secret_override and not env_text("PROXY_PURITY_SECRET"):
        value = secret_match.group(1).strip().strip("\"'")
        if value:
            secret = value

    return RuntimeSettings(controller=controller, secret=secret)


def env_text(name: str) -> str:
    return (os.environ.get(name) or "").strip()


class ClashController:
    def __init__(self, base_url: str, secret: str, timeout_sec: float = 8.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.secret = secret
        self.timeout_sec = timeout_sec

    def _request(
        self, method: str, path: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        body = None
        headers = {"Content-Type": "application/json"}
        if self.secret:
            headers["Authorization"] = f"Bearer {self.secret}"
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                text = resp.read().decode("utf-8")
        except urllib.error.HTTPError as err:
            details = err.read().decode("utf-8", errors="ignore")
            raise ProxyPurityError(f"controller HTTP {err.code}: {details or err.reason}") from err
        except urllib.error.URLError as err:
            raise ProxyPurityError(f"controller request failed: {err}") from err
        return json.loads(text) if text else {}

    def get_proxies(self) -> dict[str, Any]:
        return self._request("GET", "/proxies")

    def get_selector(self, selector: str) -> dict[str, Any]:
        encoded = urllib.parse.quote(selector, safe="")
        return self._request("GET", f"/proxies/{encoded}")


class IsolatedClashController(ClashController):
    def switch_selector(self, selector: str, node: str) -> None:
        encoded = urllib.parse.quote(selector, safe="")
        self._request("PUT", f"/proxies/{encoded}", {"name": node})


class ProxyProbeClient:
    def __init__(self, proxy_url: str, timeout_sec: float) -> None:
        if not proxy_url:
            raise ProxyPurityError(
                "no HTTP proxy URL available; Clash mixed-port or port is required"
            )
        proxy_handler = urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
        self.opener = urllib.request.build_opener(proxy_handler)
        self.timeout_sec = timeout_sec

    def json_get(self, url: str) -> tuple[dict[str, Any], int]:
        started = time.perf_counter()
        with self.opener.open(url, timeout=self.timeout_sec) as resp:
            text = resp.read().decode("utf-8")
        latency_ms = int((time.perf_counter() - started) * 1000)
        return json.loads(text), latency_ms

    def text_get(self, url: str) -> tuple[str, int]:
        started = time.perf_counter()
        with self.opener.open(url, timeout=self.timeout_sec) as resp:
            text = resp.read().decode("utf-8")
        latency_ms = int((time.perf_counter() - started) * 1000)
        return text, latency_ms


def direct_json_get(url: str, timeout_sec: float = 15.0) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "proxy-purity/1.0"})
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_cloudflare_trace(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key] = value
    return result


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def keyword_matches_text(text: str, keyword: str) -> bool:
    normalized_keyword = normalize_text(keyword)
    if not normalized_keyword:
        return False
    if re.fullmatch(r"[a-z ]+", normalized_keyword):
        pattern = rf"(?<![a-z]){re.escape(normalized_keyword)}(?![a-z])"
        return re.search(pattern, text) is not None
    return normalized_keyword in text


def detect_expected_country(node_name: str) -> str:
    lowered = normalize_text(node_name)
    for code, keywords in REGION_PATTERNS.items():
        if any(keyword_matches_text(lowered, keyword) for keyword in keywords):
            return code
    return ""


def multiplier_allowed(node_name: str) -> bool:
    match = MULTIPLIER_PATTERN.search(node_name)
    if not match:
        return True
    return match.group(1) == "1"


def resolve_remote_profile(
    identifier: str,
    profiles_index: pathlib.Path | None = None,
) -> RemoteProfile:
    profiles_index = profiles_index or DEFAULT_PROFILES_INDEX
    if not profiles_index.exists():
        raise ProxyPurityError(f"profiles index not found: {profiles_index}")
    with profiles_index.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        raise ProxyPurityError(f"profiles index has no items list: {profiles_index}")

    exact_uid: list[dict[str, Any]] = []
    matching_name: list[dict[str, Any]] = []
    normalized_identifier = identifier.casefold()
    for item in items:
        if not isinstance(item, dict) or item.get("type") != "remote":
            continue
        uid = item.get("uid")
        name = item.get("name")
        file_name = item.get("file")
        if not all(isinstance(value, str) and value for value in (uid, name, file_name)):
            continue
        if uid == identifier:
            exact_uid.append(item)
        if name.casefold() == normalized_identifier:
            matching_name.append(item)

    matches = exact_uid or matching_name
    if not matches:
        raise ProxyPurityError(f"remote profile not found by name or UID: {identifier}")
    if len(matches) > 1:
        uids = [str(item["uid"]) for item in matches]
        raise ProxyPurityError(
            f"remote profile name is ambiguous: {identifier}; matching UIDs: {uids}"
        )

    item = matches[0]
    filename = str(item["file"])
    if pathlib.Path(filename).name != filename or filename in (".", ".."):
        raise ProxyPurityError("Unsafe profile filename")
    profile_path = profiles_index.parent / "profiles" / filename
    return RemoteProfile(
        uid=str(item["uid"]),
        name=str(item["name"]),
        path=profile_path,
    )


def load_profile(profile_path: pathlib.Path) -> dict[str, Any]:
    actual_path = profile_path
    if not actual_path.exists():
        raise ProxyPurityError(f"profile not found: {profile_path}")
    with actual_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ProxyPurityError(f"profile is not a mapping: {actual_path}")
    return payload


def profile_leaf_nodes(profile: dict[str, Any]) -> list[str]:
    groups = profile.get(PROFILE_GROUP_KEY) or []
    group_names = {
        item.get("name") for item in groups if isinstance(item, dict) and item.get("name")
    }
    proxy_names = {
        item.get("name")
        for item in (profile.get(PROFILE_PROXY_KEY) or [])
        if isinstance(item, dict) and item.get("name")
    }
    nodes: list[str] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        for item in group.get(PROFILE_PROXY_KEY) or []:
            if not isinstance(item, str):
                continue
            if item.upper() in NON_PROXY_NAMES:
                continue
            if item in group_names:
                continue
            if item.startswith("Traffic:") or item.startswith("Expire:"):
                continue
            if item not in proxy_names:
                continue
            if not multiplier_allowed(item):
                continue
            if item not in nodes:
                nodes.append(item)
    return nodes


def filter_profile_nodes(nodes: list[str], requested_nodes: list[str]) -> list[str]:
    requested = {node for node in requested_nodes if node}
    return [node for node in nodes if node in requested]


def profile_leaf_node_objects(profile: dict[str, Any]) -> list[dict[str, Any]]:
    node_names = set(profile_leaf_nodes(profile))
    results: list[dict[str, Any]] = []
    for proxy in profile.get(PROFILE_PROXY_KEY) or []:
        if not isinstance(proxy, dict):
            continue
        name = proxy.get("name")
        if isinstance(name, str) and name in node_names:
            results.append(dict(proxy))
    return results


def render_isolated_config(
    *,
    provider: str,
    nodes: list[dict[str, Any]],
    mixed_port: int,
    socks_port: int,
    controller_port: int,
    secret: str,
) -> str:
    return yaml.safe_dump({
        "mixed-port": mixed_port, "socks-port": socks_port,
        "external-controller": f"0.0.0.0:{controller_port}", "secret": secret,
        "mode": "global", "allow-lan": False, "log-level": "info",
        "proxies": nodes,
        "proxy-groups": [{"name": DEFAULT_PROVIDER_SELECTOR, "type": "select",
                          "proxies": [node["name"] for node in nodes]}],
        "rules": [f"MATCH,{DEFAULT_PROVIDER_SELECTOR}"],
    }, allow_unicode=True, sort_keys=False)


def node_matches(
    node_name: str, contains_all: Iterable[str], pattern: re.Pattern[str] | None
) -> bool:
    lowered = normalize_text(node_name)
    contains_terms = [normalize_text(item) for item in contains_all if item.strip()]
    if any(term not in lowered for term in contains_terms):
        return False
    return not (pattern and not pattern.search(node_name))


def score_grade(score: int) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    if score >= 30:
        return "D"
    return "E"


def calculate_purity_score(
    proxycheck: dict[str, Any],
    ipqs: dict[str, Any],
    *,
    unique_exit_ips: int,
    actual_country: str,
    expected_country: str,
    avg_latency_ms: float | None,
) -> tuple[int, list[str]]:
    score = 100
    notes: list[str] = []

    detections = proxycheck.get("detections", {})
    network = proxycheck.get("network", {})

    if detections.get("hosting"):
        score -= 20
        notes.append("proxycheck=hosting")
    if detections.get("vpn"):
        score -= 25
        notes.append("proxycheck=vpn")
    if detections.get("proxy"):
        score -= 30
        notes.append("proxycheck=proxy")
    if detections.get("tor"):
        score -= 50
        notes.append("proxycheck=tor")
    if detections.get("anonymous"):
        score -= 10
        notes.append("proxycheck=anonymous")
    if detections.get("compromised"):
        score -= 35
        notes.append("proxycheck=compromised")
    if detections.get("scraper"):
        score -= 20
        notes.append("proxycheck=scraper")

    risk = detections.get("risk")
    if isinstance(risk, int):
        if risk >= 80:
            score -= 30
            notes.append(f"proxycheck_risk={risk}")
        elif risk >= 50:
            score -= 18
            notes.append(f"proxycheck_risk={risk}")
        elif risk >= 20:
            score -= 8
            notes.append(f"proxycheck_risk={risk}")

    conn_type = str(network.get("type", "")).strip().lower()
    if conn_type in {"hosting", "datacenter", "data center"}:
        score -= 15
        notes.append(f"network_type={network.get('type')}")

    fraud_score = ipqs.get("fraud_score")
    if isinstance(fraud_score, int):
        if fraud_score >= 75:
            score -= 30
            notes.append(f"ipqs_fraud_score={fraud_score}")
        elif fraud_score >= 50:
            score -= 18
            notes.append(f"ipqs_fraud_score={fraud_score}")
        elif fraud_score >= 25:
            score -= 8
            notes.append(f"ipqs_fraud_score={fraud_score}")

    for flag, penalty in (
        ("proxy", 15),
        ("vpn", 12),
        ("tor", 30),
        ("recent_abuse", 18),
        ("bot_status", 15),
    ):
        if ipqs.get(flag) is True:
            score -= penalty
            notes.append(f"ipqs_{flag}=true")

    if unique_exit_ips > 1:
        score -= min(25, 15 + (unique_exit_ips - 2) * 5)
        notes.append(f"exit_ip_changed={unique_exit_ips}")

    if expected_country and actual_country and actual_country.upper() != expected_country.upper():
        score -= 12
        notes.append(f"geo_mismatch={expected_country}->{actual_country}")

    if isinstance(avg_latency_ms, (int, float)):
        if avg_latency_ms >= 800:
            score -= 10
            notes.append(f"latency_high={avg_latency_ms:.1f}")
        elif avg_latency_ms >= 400:
            score -= 5
            notes.append(f"latency_mid={avg_latency_ms:.1f}")

    return max(0, min(100, int(round(score)))), notes


def proxycheck_lookup(ip: str) -> dict[str, Any]:
    key = env_text(PROXYCHECK_API_ENV)
    key_param = f"&key={urllib.parse.quote(key, safe='')}" if key else ""
    url = DEFAULT_PROXYCHECK_URL.format(ip=urllib.parse.quote(ip, safe=""), key_param=key_param)
    payload = direct_json_get(url)
    if payload.get("status") != "ok":
        raise ProxyPurityError(f"proxycheck lookup failed for {ip}: {payload}")
    return payload.get(ip, {})


def provider_output_paths(output_dir: pathlib.Path, provider: str) -> dict[str, pathlib.Path]:
    return {
        "results_csv": output_dir / f"{provider}_scan_results.csv",
        "results_json": output_dir / f"{provider}_scan_results.json",
        "ipqs_csv": output_dir / f"{provider}_ipqs_batch_input.csv",
        "ranking_csv": output_dir / f"{provider}_node_rankings.csv",
    }


def write_ipqs_batch_csv(path: pathlib.Path, results: list[PurityResult]) -> pathlib.Path:
    ips = sorted({result.exit_ip for result in results if result.exit_ip})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(IPQS_BATCH_HEADER)
        for ip in ips:
            writer.writerow([ip])
    return path


def sorted_results(results: list[PurityResult]) -> list[PurityResult]:
    return sorted(results, key=lambda item: (-item.score, item.node))


def write_provider_outputs(
    provider: str,
    results: list[PurityResult],
    output_dir: pathlib.Path,
    metadata: dict[str, Any],
) -> dict[str, pathlib.Path]:
    paths = provider_output_paths(output_dir, provider)
    ordered_results = sorted_results(results)
    json_payload = {
        "metadata": metadata,
        "provider": provider,
        "results": [
            {
                **asdict(result),
                "rounds": [asdict(item) for item in result.rounds],
            }
            for result in ordered_results
        ],
    }
    paths["results_json"].write_text(
        json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    fieldnames = [
        "provider",
        *(
            list(ordered_results[0].to_csv_row().keys())
            if ordered_results
            else list(
                PurityResult(
                    selector="",
                    node="",
                    expected_country="",
                    exit_ip="",
                    unique_exit_ips=[],
                    avg_latency_ms=None,
                    min_latency_ms=None,
                    max_latency_ms=None,
                    cf_loc="",
                    cf_colo="",
                    score=0,
                    grade="E",
                )
                .to_csv_row()
                .keys()
            )
        ),
    ]
    with paths["results_csv"].open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in ordered_results:
            row = result.to_csv_row()
            row["provider"] = provider
            writer.writerow(row)
    with paths["ranking_csv"].open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["rank", "provider", "node", "score", "grade", "avg_latency_ms", "exit_ip", "notes"]
        )
        for index, result in enumerate(ordered_results, start=1):
            writer.writerow(
                [
                    index,
                    provider,
                    result.node,
                    result.score,
                    result.grade,
                    "" if result.avg_latency_ms is None else f"{result.avg_latency_ms:.1f}",
                    result.exit_ip,
                    " | ".join(result.notes),
                ]
            )
    write_ipqs_batch_csv(paths["ipqs_csv"], ordered_results)
    return paths


def resolve_colima_executable() -> str:
    for candidate in COLIMA_EXECUTABLE_CANDIDATES:
        proc = subprocess.run(
            ["colima", "--profile", COLIMA_PROFILE, "ssh", "--", "/bin/sh", "-lc", f"command -v {candidate}"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    return str(COLIMA_MIHOMO_BINARY)


def resolve_latest_mihomo_download_url() -> str:
    req = urllib.request.Request(
        COLIMA_GITHUB_RELEASE_API,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "proxy-purity"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as err:
        raise ProxyPurityError(f"failed to query Mihomo release metadata: {err}") from err
    assets = payload.get("assets") or []
    for asset in assets:
        name = str(asset.get("name", ""))
        if not COLIMA_MIHOMO_ASSET_PATTERN.search(name):
            continue
        url = str(asset.get("browser_download_url", "")).strip()
        if url:
            return url
    raise ProxyPurityError("failed to find a linux arm64 Mihomo .gz asset in the latest release")


def ensure_colima_mihomo_ready() -> str:
    existing = resolve_colima_executable()
    if existing != str(COLIMA_MIHOMO_BINARY):
        return existing
    check_cached = subprocess.run(
        ["colima", "--profile", COLIMA_PROFILE, "ssh", "--", "/bin/sh", "-lc", f"test -x {COLIMA_MIHOMO_BINARY}"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    if check_cached.returncode == 0:
        return str(COLIMA_MIHOMO_BINARY)
    download_url = resolve_latest_mihomo_download_url()
    bootstrap = " && ".join(
        [
            f"mkdir -p {COLIMA_RUNTIME_BIN_DIR} {COLIMA_RUNTIME_CONFIG_DIR} {COLIMA_RUNTIME_LOG_DIR}",
            f"rm -f {COLIMA_MIHOMO_BINARY} {COLIMA_MIHOMO_BINARY_GZ}",
            f"curl -L {urllib.parse.quote(download_url, safe=':/?&=%.-_')} -o {COLIMA_MIHOMO_BINARY_GZ}",
            f"gunzip -f {COLIMA_MIHOMO_BINARY_GZ}",
            f"chmod +x {COLIMA_MIHOMO_BINARY}",
            f"test -x {COLIMA_MIHOMO_BINARY}",
        ]
    )
    proc = subprocess.run(
        ["colima", "--profile", COLIMA_PROFILE, "ssh", "--", "/bin/sh", "-lc", bootstrap],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise ProxyPurityError(
            f"failed to prepare Colima mihomo: {proc.stderr.strip() or proc.stdout.strip() or COLIMA_MIHOMO_IMAGE_HINT}"
        )
    return str(COLIMA_MIHOMO_BINARY)


def colima_runtime_path(name: str) -> pathlib.Path:
    return COLIMA_RUNTIME_CONFIG_DIR / name


def wait_for_http_ready(
    url: str,
    timeout_sec: float = COLIMA_START_TIMEOUT_SEC,
    headers: dict[str, str] | None = None,
) -> None:
    started = time.time()
    last_error = ""
    while time.time() - started < timeout_sec:
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=2):
                return
        except urllib.error.HTTPError as err:
            if err.code in {200, 204, 401, 403}:
                return
            last_error = f"HTTP {err.code}: {err.reason}"
            time.sleep(0.5)
        except Exception as err:
            last_error = str(err)
            time.sleep(0.5)
    raise ProxyPurityError(f"timed out waiting for isolated controller: {last_error}")


def run_isolated_scan(
    *,
    provider: str,
    repeat: int,
    settle_sec: float,
    pause_sec: float,
    request_timeout_sec: float,
    requested_nodes: list[str],
) -> int:
    remote_profile = resolve_remote_profile(provider)
    profile = load_profile(remote_profile.path)
    nodes = profile_leaf_node_objects(profile)
    if requested_nodes:
        available_names = [str(node.get("name", "")) for node in nodes]
        missing = [node for node in requested_nodes if node not in available_names]
        if missing:
            raise ProxyPurityError(
                f"requested nodes not found in provider {remote_profile.name} "
                f"({remote_profile.uid}): {missing}"
            )
        allowed_names = set(filter_profile_nodes(available_names, requested_nodes))
        nodes = [node for node in nodes if str(node.get("name", "")) in allowed_names]
    if not nodes:
        raise ProxyPurityError(
            f"no leaf nodes found for provider {remote_profile.name} ({remote_profile.uid})"
        )
    output_dir = ensure_output_dir(None)
    provider_key = remote_profile.output_key
    ports = DEFAULT_ISOLATED_PORTS
    isolated_secret = secrets.token_urlsafe(24)
    config_text = render_isolated_config(
        provider=provider_key,
        nodes=nodes,
        mixed_port=ports["mixed"],
        socks_port=ports["socks"],
        controller_port=ports["controller"],
        secret=isolated_secret,
    )
    local_config = output_dir / f"{provider_key}_isolated.yaml"
    local_config.write_text(config_text, encoding="utf-8")
    runtime_config = colima_runtime_path(local_config.name)
    subprocess.run(
        [
            "colima",
            "--profile",
            COLIMA_PROFILE,
            "ssh",
            "--",
            "/bin/sh",
            "-lc",
            f"umask 077; mkdir -p {COLIMA_RUNTIME_CONFIG_DIR} {COLIMA_RUNTIME_LOG_DIR}",
        ],
        check=True,
        timeout=30,
    )
    subprocess.run(
        ["colima", "--profile", COLIMA_PROFILE, "ssh", "--", "/bin/sh", "-lc", f"umask 077; cat > {runtime_config}"],
        input=config_text,
        text=True,
        check=True,
        timeout=30,
    )
    executable = ensure_colima_mihomo_ready()
    log_path = output_dir / f"{provider_key}_isolated.log"
    log_handle = log_path.open("w", encoding="utf-8")
    proc = subprocess.Popen(
        [
            "colima",
            "--profile",
            COLIMA_PROFILE,
            "ssh",
            "--",
            "/bin/sh",
            "-lc",
            f"{executable} -f {runtime_config}",
        ],
        stdout=log_handle,
        stderr=log_handle,
        text=True,
    )
    controller_url = f"http://127.0.0.1:{ports['controller']}"
    proxy_url = f"http://127.0.0.1:{ports['mixed']}"
    results: list[PurityResult] = []
    try:
        wait_for_http_ready(
            f"{controller_url}/version",
            headers={"Authorization": f"Bearer {isolated_secret}"},
        )
        controller = IsolatedClashController(controller_url, isolated_secret)
        probe = ProxyProbeClient(proxy_url, timeout_sec=request_timeout_sec)
        proxycheck_cache: dict[str, dict[str, Any]] = {}
        current = DEFAULT_PROVIDER_SELECTOR
        for node in nodes:
            node_name = str(node["name"])
            controller.switch_selector(DEFAULT_PROVIDER_SELECTOR, node_name)
            time.sleep(settle_sec)
            rounds: list[NodeObservation] = []
            for round_index in range(1, repeat + 1):
                observation = NodeObservation(round_index=round_index)
                try:
                    ip_data, latency_ms = probe.json_get(DEFAULT_IP_ENDPOINT)
                    cf_text, _ = probe.text_get(DEFAULT_CF_TRACE_ENDPOINT)
                    cf_data = parse_cloudflare_trace(cf_text)
                    observation.exit_ip = str(ip_data.get("ip", "")).strip()
                    observation.latency_ms = latency_ms
                    observation.cf_loc = cf_data.get("loc", "")
                    observation.cf_colo = cf_data.get("colo", "")
                except Exception as err:
                    observation.error = str(err)
                rounds.append(observation)
                if round_index < repeat:
                    time.sleep(pause_sec)
            exit_ips = [item.exit_ip for item in rounds if item.exit_ip]
            unique_exit_ips = sorted(set(exit_ips))
            dominant_ip = unique_exit_ips[0] if unique_exit_ips else ""
            latencies = [item.latency_ms for item in rounds if isinstance(item.latency_ms, int)]
            avg_latency_ms = statistics.mean(latencies) if latencies else None
            min_latency_ms = min(latencies) if latencies else None
            max_latency_ms = max(latencies) if latencies else None
            cf_loc = next((item.cf_loc for item in rounds if item.cf_loc), "")
            cf_colo = next((item.cf_colo for item in rounds if item.cf_colo), "")
            proxycheck_payload = {}
            proxycheck_error = ""
            if dominant_ip:
                if dominant_ip not in proxycheck_cache:
                    try:
                        proxycheck_cache[dominant_ip] = proxycheck_lookup(dominant_ip)
                    except Exception as err:
                        proxycheck_cache[dominant_ip] = {"_error": str(err)}
                cached_proxycheck = proxycheck_cache[dominant_ip]
                if isinstance(cached_proxycheck, dict) and cached_proxycheck.get("_error"):
                    proxycheck_error = str(cached_proxycheck.get("_error", "")).strip()
                else:
                    proxycheck_payload = cached_proxycheck
            actual_country = ""
            if isinstance(proxycheck_payload.get("location"), dict):
                actual_country = (
                    str(proxycheck_payload["location"].get("country_code", "")).strip().upper()
                )
            elif cf_loc:
                actual_country = cf_loc.upper()
            expected_country = detect_expected_country(node_name)
            score, notes = calculate_purity_score(
                proxycheck_payload,
                {},
                unique_exit_ips=len(unique_exit_ips),
                actual_country=actual_country,
                expected_country=expected_country,
                avg_latency_ms=avg_latency_ms,
            )
            if any(item.error for item in rounds):
                notes.append("round_errors_present")
            if proxycheck_error:
                notes.append(f"proxycheck_error={proxycheck_error}")
            if not dominant_ip:
                notes.append("no_exit_ip")
                score = max(0, score - 25)
            results.append(
                PurityResult(
                    selector=current,
                    node=node_name,
                    expected_country=expected_country,
                    exit_ip=dominant_ip,
                    unique_exit_ips=unique_exit_ips,
                    avg_latency_ms=avg_latency_ms,
                    min_latency_ms=min_latency_ms,
                    max_latency_ms=max_latency_ms,
                    cf_loc=cf_loc,
                    cf_colo=cf_colo,
                    score=score,
                    grade=score_grade(score),
                    notes=notes,
                    proxycheck=proxycheck_payload,
                    rounds=rounds,
                )
            )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        log_handle.close()
    metadata = {
        "provider": provider_key,
        "profile_uid": remote_profile.uid,
        "profile_name": remote_profile.name,
        "profile_path": str(remote_profile.path),
        "repeat": repeat,
        "candidate_count": len(nodes),
        "controller": controller_url,
        "proxy_url": proxy_url,
        "generated_at": datetime.now().isoformat(),
    }
    written = write_provider_outputs(provider_key, results, output_dir, metadata)
    print_results_table(results)
    print()
    print(f"json={written['results_json']}")
    print(f"csv={written['results_csv']}")
    print(f"ipqs_csv={written['ipqs_csv']}")
    return 0


def run_profile_scan(args: argparse.Namespace) -> int:
    return run_isolated_scan(
        provider=args.provider,
        repeat=args.repeat,
        settle_sec=args.settle_sec,
        pause_sec=args.pause_sec,
        request_timeout_sec=args.request_timeout_sec,
        requested_nodes=args.nodes,
    )


def selector_names(proxies_payload: dict[str, Any]) -> list[str]:
    selectors: list[str] = []
    for name, meta in (proxies_payload.get("proxies") or {}).items():
        if not isinstance(meta, dict):
            continue
        if meta.get("type") != "Selector":
            continue
        selectors.append(name)
    return sorted(selectors)


def selector_state(proxies_payload: dict[str, Any]) -> dict[str, str]:
    states: dict[str, str] = {}
    proxies = proxies_payload.get("proxies") or {}
    for name in selector_names(proxies_payload):
        meta = proxies.get(name, {})
        current = meta.get("now") if isinstance(meta, dict) else ""
        states[name] = current if isinstance(current, str) else ""
    return states


def selectable_nodes(
    selector_payload: dict[str, Any], selector_group_names: Iterable[str] = ()
) -> list[str]:
    selector_name_set = {name for name in selector_group_names}
    nodes = []
    for item in selector_payload.get("all") or []:
        if not isinstance(item, str):
            continue
        if item.upper() in NON_PROXY_NAMES:
            continue
        if item in selector_name_set:
            continue
        if item.startswith("Traffic:") or item.startswith("Expire:"):
            continue
        nodes.append(item)
    return nodes


def ensure_output_dir(base_dir: str | None) -> pathlib.Path:
    if base_dir:
        path = pathlib.Path(base_dir).expanduser()
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = LOG_ROOT / stamp
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)
    return path


def print_results_table(results: list[PurityResult]) -> None:
    print("grade score selector node exit_ip avg_ms risk notes")
    for result in sorted_results(results):
        proxycheck_risk = ""
        if isinstance(result.proxycheck.get("detections"), dict):
            proxycheck_risk = str(result.proxycheck["detections"].get("risk", ""))
        avg_ms = "-" if result.avg_latency_ms is None else f"{result.avg_latency_ms:.1f}"
        notes = ",".join(result.notes[:3])
        print(
            f"{result.grade:>5} {result.score:>5} {result.selector} {result.node} "
            f"{result.exit_ip or '-'} {avg_ms:>6} {proxycheck_risk:>4} {notes}"
        )


def run_selectors(args: argparse.Namespace, controller: ClashController) -> int:
    payload = controller.get_proxies()
    names = selector_names(payload)
    if not names:
        raise ProxyPurityError("no selector groups found")
    if args.state:
        print(json.dumps(selector_state(payload), ensure_ascii=False, sort_keys=True))
        return 0
    for name in names:
        print(name)
    return 0


def run_nodes(args: argparse.Namespace, controller: ClashController) -> int:
    proxies_payload = controller.get_proxies()
    payload = controller.get_selector(args.selector)
    nodes = selectable_nodes(payload, selector_names(proxies_payload))
    pattern = re.compile(args.node_regex) if args.node_regex else None
    filtered = [node for node in nodes if node_matches(node, args.contains or [], pattern)]
    for node in filtered[: args.limit if args.limit > 0 else None]:
        marker = "*" if node == payload.get("now") else " "
        print(f"{marker} {node}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Measure Clash node exit IP purity using repeated exit-IP checks and IP reputation lookups."
    )
    parser.add_argument("--config", required=True, type=pathlib.Path, help="Recipient JSON paths")
    parser.add_argument("--controller", default=None, help="override Clash external controller URL")
    parser.add_argument("--secret", default=None, help="override Clash controller secret")
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check-config", help="Validate configured paths without requests or writes")
    check.set_defaults(func=None)

    selectors = subparsers.add_parser("selectors", help="list selector groups")
    selectors.add_argument(
        "--state",
        action="store_true",
        help="emit stable JSON mapping selector groups to their current targets",
    )
    selectors.set_defaults(func=run_selectors)

    nodes = subparsers.add_parser("nodes", help="list nodes from a selector")
    nodes.add_argument("--selector", required=True, help="selector group name")
    nodes.add_argument(
        "--contains",
        action="append",
        default=[],
        help="case-insensitive substring filter; can repeat",
    )
    nodes.add_argument("--node-regex", default="", help="regex filter for node names")
    nodes.add_argument("--limit", type=int, default=0, help="limit output rows; 0 means no limit")
    nodes.set_defaults(func=run_nodes)

    profile_scan = subparsers.add_parser("profile-scan", help=ISOLATED_SCAN_HELP)
    profile_scan.add_argument(
        "--provider",
        required=True,
        help="remote profile name or UID from the live Clash Verge profiles.yaml",
    )
    profile_scan.add_argument(
        "--nodes",
        nargs="*",
        default=[],
        help="explicit node names to scan inside the provider profile",
    )
    profile_scan.add_argument("--repeat", type=int, default=3)
    profile_scan.add_argument("--settle-sec", type=float, default=2.0)
    profile_scan.add_argument("--pause-sec", type=float, default=1.0)
    profile_scan.add_argument("--request-timeout-sec", type=float, default=12.0)
    profile_scan.set_defaults(func=run_profile_scan)

    return parser


def configure(path: pathlib.Path) -> None:
    global LOG_ROOT, DEFAULT_RUNTIME_CONFIG, DEFAULT_PROFILES_INDEX, DEFAULT_CONTROLLER
    global COLIMA_RUNTIME_ROOT, COLIMA_RUNTIME_CONFIG_DIR, COLIMA_RUNTIME_LOG_DIR
    global COLIMA_RUNTIME_BIN_DIR, COLIMA_MIHOMO_BINARY, COLIMA_MIHOMO_BINARY_GZ
    global COLIMA_PROFILE
    data = json.loads(path.read_text(encoding="utf-8"))
    endpoint = data.get("controller_url")
    if not isinstance(endpoint, str) or not endpoint.startswith(("http://", "https://")):
        raise ValueError("Choose an explicit HTTP(S) controller_url for selector inspection")
    DEFAULT_CONTROLLER = endpoint
    for key in ("runtime_config", "profiles_index", "output_root", "colima_runtime_root"):
        if not isinstance(data.get(key), str) or not pathlib.Path(data[key]).is_absolute():
            raise ValueError(f"{key} must be an explicit absolute path")
    # These VM paths enter shell commands; reject shell metacharacters and whitespace.
    runtime = data["colima_runtime_root"]
    if not re.fullmatch(r"/[A-Za-z0-9/_-]+", runtime) or runtime in ("/", "/tmp", "/var"):
        raise ValueError("Use a dedicated shell-safe absolute colima_runtime_root")
    COLIMA_PROFILE = data.get("colima_profile", "")
    if not isinstance(COLIMA_PROFILE, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", COLIMA_PROFILE):
        raise ValueError("Choose an explicit existing Colima profile")
    DEFAULT_RUNTIME_CONFIG = pathlib.Path(data["runtime_config"])
    DEFAULT_PROFILES_INDEX = pathlib.Path(data["profiles_index"])
    LOG_ROOT = pathlib.Path(data["output_root"])
    COLIMA_RUNTIME_ROOT = pathlib.Path(runtime)
    COLIMA_RUNTIME_CONFIG_DIR = COLIMA_RUNTIME_ROOT / "config"
    COLIMA_RUNTIME_LOG_DIR = COLIMA_RUNTIME_ROOT / "logs"
    COLIMA_RUNTIME_BIN_DIR = COLIMA_RUNTIME_ROOT / "bin"
    COLIMA_MIHOMO_BINARY = COLIMA_RUNTIME_BIN_DIR / "mihomo"
    COLIMA_MIHOMO_BINARY_GZ = COLIMA_RUNTIME_BIN_DIR / "mihomo.gz"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        configure(args.config)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    if args.command == "check-config":
        print("Configuration valid; no controller or network request made")
        return 0
    if args.command == "profile-scan":
        try:
            return args.func(args)
        except ProxyPurityError as err:
            print(f"[error] {err}", file=sys.stderr)
            return 1
    settings = load_runtime_settings(
        controller_override=args.controller,
        secret_override=args.secret,
    )
    controller = ClashController(settings.controller, settings.secret)
    try:
        return args.func(args, controller)
    except ProxyPurityError as err:
        print(f"[error] {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
