#!/usr/bin/env python3
"""
Clash Verge Rev 自动切换守护脚本。

设计目标：
1. 当前策略组节点不可用时自动切换。
2. 按地区健康度优先切换，并支持排除指定地区（默认排除 HK/TW）。
3. 支持按策略组约束候选（如 1x 过滤）并跨订阅容灾。
4. 支持 TUN/非TUN 感知测速与可选 TUN 自动切换。

说明：
- 脚本依赖 Clash/Mihomo External Controller API（默认 http://127.0.0.1:9090）。
- TUN 与非TUN使用不同优先探测 URL，并带有多地址回退与缓存回退。
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import heapq
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from datetime import datetime

# =========================
# 1) 基础工具
# =========================

REGION_PATTERNS: dict[str, tuple[str, ...]] = {
    "TW": ("台湾", "台灣", "tw", "taiwan"),
    "HK": ("香港", "hk", "hongkong", "hong kong"),
    "JP": ("日本", "jp", "japan", "tokyo", "osaka"),
    "SG": ("新加坡", "sg", "singapore"),
    "US": ("美国", "美國", "us", "usa", "united states"),
    "KR": ("韩国", "韓國", "kr", "korea", "seoul"),
}

NON_PROXY_NAMES = {
    "DIRECT",
    "REJECT",
    "PASS",
    "GLOBAL",
    "MATCH",
}

# 默认控制器密钥（可被命令行 --secret 覆盖）
DEFAULT_CONTROLLER_SECRET = ""
DEFAULT_CONTROLLER_URL = os.environ.get("CLASH_CONTROLLER_URL", "")
DEFAULT_EXCLUDED_REGIONS = tuple(os.environ.get("CLASH_EXCLUDED_REGIONS", "").split(","))
DEFAULT_PROBE_URL_TUN = "https://www.gstatic.com/generate_204"
DEFAULT_PROBE_URL_NON_TUN = "https://cp.cloudflare.com/generate_204"
DEFAULT_DOMESTIC_GROUPS = tuple(filter(None, os.environ.get("CLASH_DIRECT_GROUPS", "").split(",")))


def load_runtime_controller_defaults() -> tuple[str, str]:
    """从 Clash Verge 运行态 config.yaml 读取 controller 与 secret。

    仅用于默认值兜底：命令行显式传参优先级更高。
    """
    configured = os.environ.get("RUNTIME_ROOT")
    if not configured:
        raise ValueError("Use clash-tool --config; RUNTIME_ROOT is required")
    cfg_path = pathlib.Path(configured) / "config.yaml"
    raw = cfg_path.read_text(encoding="utf-8", errors="ignore") if cfg_path.exists() else ""

    controller = DEFAULT_CONTROLLER_URL
    secret = DEFAULT_CONTROLLER_SECRET

    controller_match = re.search(r"(?m)^external-controller:\s*([^\r\n#]+)", raw)
    if controller_match:
        value = controller_match.group(1).strip().strip("\"'")
        if value:
            controller = value if value.startswith(("http://", "https://")) else f"http://{value}"

    secret_match = re.search(r"(?m)^secret:\s*([^\r\n#]+)", raw)
    if secret_match:
        value = secret_match.group(1).strip().strip("\"'")
        if value:
            secret = value

    return (controller, secret)


def probe_controller(base_url: str, secret: str, timeout_sec: float) -> bool:
    """探测控制器是否可访问。"""
    if base_url.startswith("unix://"):
        from clash_controller import Controller

        try:
            Controller.discover(url_override=base_url, secret_override=secret).request(
                "GET", "/version", timeout=timeout_sec
            )
            return True
        except (OSError, RuntimeError, ValueError):
            return False
    headers = {}
    if secret:
        headers["Authorization"] = f"Bearer {secret}"
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/version",
        headers=headers,
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec):
            return True
    except Exception:
        return False


def discover_controller_endpoint(
    preferred_url: str,
    preferred_secret: str,
    timeout_sec: float,
) -> tuple[str, str, bool]:
    """自动发现可用 controller URL + secret 组合。"""
    if preferred_url.startswith("unix://"):
        return (
            preferred_url,
            preferred_secret,
            probe_controller(preferred_url, preferred_secret, timeout_sec),
        )
    runtime_url, runtime_secret = load_runtime_controller_defaults()

    url_candidates: list[str] = []
    for item in (preferred_url, runtime_url):
        if not item:
            continue
        if item not in url_candidates:
            url_candidates.append(item)

    secret_candidates: list[str] = []
    for item in (
        preferred_secret,
        runtime_secret,
        DEFAULT_CONTROLLER_SECRET,
        "",
    ):
        if item is None:
            continue
        if item not in secret_candidates:
            secret_candidates.append(item)

    if not url_candidates:
        url_candidates = [DEFAULT_CONTROLLER_URL]
    if not secret_candidates:
        secret_candidates = [""]

    for url in url_candidates:
        for secret in secret_candidates:
            if probe_controller(url, secret, timeout_sec=timeout_sec):
                return (url, secret, True)

    return (url_candidates[0], secret_candidates[0], False)


def now_ts() -> str:
    """返回当前时间字符串，便于日志阅读。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str) -> None:
    """统一日志输出格式。"""
    text = f"[{now_ts()}] {message}"
    safe_text = text.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    print(safe_text)


def normalize_text(text: str) -> str:
    """统一小写并去除多余空白，提升关键词匹配稳定性。"""
    return re.sub(r"\s+", " ", text.strip().lower())


def normalize_group_name(name: str) -> str:
    """归一化策略组名，便于兼容 emoji/符号前缀。"""
    lowered = normalize_text(name)
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", "", lowered)
    return cleaned


def detect_region(node_name: str) -> str | None:
    """根据节点名推断地区代号，无法识别时返回 None。"""
    lowered = normalize_text(node_name)
    for region, keywords in REGION_PATTERNS.items():
        for keyword in keywords:
            if keyword in lowered:
                return region
    return None


def detect_provider(node_name: str) -> str:
    """从节点名中提取“订阅/提供方”标签（启发式）。"""
    # 优先识别“1x/5x/10x”这类订阅标签（你的订阅节点常见命名形态）。
    match = re.search(r"(\d+)\s*[xX]\b", node_name)
    if match:
        return f"{match.group(1)}x"

    # 其次按分隔符提取（兼容中文竖线“丨”）。
    chunks = re.split(r"\s*[|｜丨/\\\-_:]\s*", node_name)
    if chunks:
        head = chunks[0].strip()
        if head:
            return head[:24]
    return "UNKNOWN"


def detect_station_signature(node_name: str) -> str:
    """提取线路签名，用于“同名站点”匹配（跨订阅场景）。"""
    # 常见形态："🇹🇼 台湾 02丨1x TW" / "台湾高级 IEPL 专线 1"
    base = re.split(r"\s*[|｜丨]\s*", node_name, maxsplit=1)[0]
    normalized = normalize_text(base)
    # 去掉 emoji/标点，仅保留中英文与数字，提升跨订阅同名匹配稳定性。
    signature = re.sub(r"[^\w\u4e00-\u9fff]+", "", normalized)
    return signature or normalized


def is_selectable_proxy(node_name: str) -> bool:
    """过滤掉非实际代理节点名称。"""
    if not node_name:
        return False
    return node_name.upper() not in NON_PROXY_NAMES


def is_process_running(process_name: str) -> bool:
    """检查 Windows 进程是否存在。"""
    if not process_name:
        return True
    if sys.platform != "win32":
        return True

    try:
        result = subprocess.run(
            [
                "tasklist",
                "/FI",
                f"IMAGENAME eq {process_name}",
                "/FO",
                "CSV",
                "/NH",
            ],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="ignore",
        )
        output = f"{result.stdout}\n{result.stderr}".lower()
        return process_name.lower() in output
    except Exception:
        return True


# =========================
# 2) 节点状态追踪器（记忆模块）
# =========================


class NodeStateTracker:
    """节点历史状态追踪器。

    使用环形缓冲区记录每个节点在最近 N 次测速中的延迟，
    为评分函数和区域健康度提供数据支撑。
    """

    def __init__(self, max_history: int = 10) -> None:
        # { node_name: deque([delay_or_None, ...], maxlen=max_history) }
        self.history: dict[str, deque] = {}
        self.max_history = max_history

    def record(self, node_name: str, delay: int | None) -> None:
        """记录一次测速结果（delay=None 表示超时/失败）。"""
        if node_name not in self.history:
            self.history[node_name] = deque(maxlen=self.max_history)
        self.history[node_name].append(delay)

    def get_node_stats(self, node_name: str) -> tuple[float, float]:
        """返回 (超时率 T(i), 有效平均延迟 D(i))。

        无历史数据时返回 (1.0, 9999.0)，视为最差。
        """
        records = self.history.get(node_name)
        if not records:
            return (1.0, 9999.0)

        timeouts = sum(1 for r in records if r is None)
        valid = [r for r in records if r is not None]

        timeout_rate = timeouts / len(records)
        avg_delay = sum(valid) / len(valid) if valid else 9999.0
        return (timeout_rate, avg_delay)

    def get_region_stats(
        self, region_nodes: list[str], max_green_ms: int = 200
    ) -> tuple[float, float]:
        """返回区域的 (超时率 T(R), 优良率 G(R))。

        - T(R): 区域内所有历史记录中超时的占比。
        - G(R): 区域内平均延迟 <= max_green_ms 的节点比例。
        """
        total_records = 0
        total_timeouts = 0
        green_count = 0

        for node in region_nodes:
            records = self.history.get(node)
            if not records:
                continue
            total_records += len(records)
            total_timeouts += sum(1 for r in records if r is None)
            valid = [r for r in records if r is not None]
            if valid and (sum(valid) / len(valid)) <= max_green_ms:
                green_count += 1

        if total_records == 0:
            return (1.0, 0.0)

        timeout_rate = total_timeouts / total_records
        green_rate = green_count / len(region_nodes) if region_nodes else 0.0
        return (timeout_rate, green_rate)


# =========================
# 3) Clash API 封装
# =========================


class ClashAPI:
    """最小可用的 Clash/Mihomo External Controller API 客户端。"""

    def __init__(self, base_url: str, secret: str, timeout_sec: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.secret = secret
        self.timeout_sec = timeout_sec

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        """发送 HTTP 请求并返回 JSON。"""
        if self.base_url.startswith("unix://"):
            from clash_controller import Controller

            return Controller.discover(
                url_override=self.base_url, secret_override=self.secret
            ).request(method, path, body=payload, timeout=self.timeout_sec)
        url = f"{self.base_url}{path}"
        body = None
        headers = {"Content-Type": "application/json"}

        if self.secret:
            headers["Authorization"] = f"Bearer {self.secret}"

        if payload is not None:
            body = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(url=url, data=body, method=method, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data) if data else {}
        except urllib.error.HTTPError as err:
            error_body = ""
            with contextlib.suppress(Exception):
                error_body = err.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"HTTP {err.code} {url} {error_body}") from err
        except urllib.error.URLError as err:
            raise RuntimeError(f"连接失败 {url}: {err}") from err

    def get_all_proxies(self) -> dict:
        """获取所有代理与策略组数据。"""
        return self._request("GET", "/proxies")

    def get_configs(self) -> dict:
        """获取当前 Clash 运行配置。"""
        return self._request("GET", "/configs")

    def patch_configs(self, payload: dict) -> None:
        """更新 Clash 运行配置。"""
        self._request("PATCH", "/configs", payload)

    def test_delay(self, proxy_name: str, url: str, timeout_ms: int) -> int | None:
        """测速某个节点（单次）；失败返回 None。"""
        encoded_name = urllib.parse.quote(proxy_name, safe="")
        encoded_url = urllib.parse.quote(url, safe="")
        path = f"/proxies/{encoded_name}/delay?url={encoded_url}&timeout={timeout_ms}"

        try:
            result = self._request("GET", path)
            delay = result.get("delay")
            if isinstance(delay, int) and delay > 0:
                return delay
            return None
        except Exception:
            return None

    def test_delay_reliable(
        self,
        proxy_name: str,
        url: str,
        timeout_ms: int,
        rounds: int = 3,
    ) -> int | None:
        """多轮测速取最小值，过滤偶发抖动峰值。

        至少有 1 次成功才返回结果；全部失败返回 None。
        """
        results: list[int] = []
        for _ in range(rounds):
            d = self.test_delay(proxy_name, url, timeout_ms)
            if d is not None:
                results.append(d)
        if not results:
            return None
        return min(results)  # 取最小值，过滤偶发抖动峰值

    def get_cached_delay(self, proxy_name: str) -> int | None:
        """读取 Clash 内部缓存的最近一次延迟（不发新测速请求）。

        Mihomo /proxies/{name} 返回 history:[{time, delay}, ...]，
        取最后一条作为缓存值；节点从未测速过则返回 None。
        """
        try:
            encoded = urllib.parse.quote(proxy_name, safe="")
            data = self._request("GET", f"/proxies/{encoded}")
            history = data.get("history", [])
            if history:
                last = history[-1]
                delay = last.get("delay", 0)
                if isinstance(delay, int) and delay > 0:
                    return delay
        except Exception:
            pass
        return None

    def switch_group(self, group_name: str, proxy_name: str) -> None:
        """切换策略组到指定节点。"""
        encoded_group = urllib.parse.quote(group_name, safe="")
        self._request("PUT", f"/proxies/{encoded_group}", {"name": proxy_name})


# =========================
# 4) 自动切换核心逻辑
# =========================


class AutoSwitcher:
    """有状态两级调度自动切换器（宏观区域熔断 + 微观节点评分）。"""

    def __init__(
        self,
        api: ClashAPI,
        groups: list[str],
        probe_url: str,
        probe_url_non_tun: str,
        probe_timeout_ms: int,
        max_delay_ms: int,
        interval_sec: int,
        fallback_regions: list[str],
        excluded_regions: list[str],
        tun_mode: str,
        max_probe_per_round: int,
        dry_run: bool,
        allow_auto_discover: bool,
        lock_domestic_direct: bool,
        exit_on_controller_down_rounds: int,
        controller_process_name: str,
    ) -> None:
        self.api = api
        self.groups = groups
        self.probe_url = probe_url
        self.probe_url_non_tun = probe_url_non_tun
        self.probe_timeout_ms = probe_timeout_ms
        self.max_delay_ms = max_delay_ms
        self.interval_sec = interval_sec
        self.fallback_regions = fallback_regions
        self.excluded_regions = {item.upper() for item in excluded_regions}
        self.tun_mode = tun_mode
        self.max_probe_per_round = max_probe_per_round
        self.dry_run = dry_run
        self.allow_auto_discover = allow_auto_discover
        self.lock_domestic_direct = lock_domestic_direct
        self.exit_on_controller_down_rounds = max(0, exit_on_controller_down_rounds)
        self.controller_process_name = controller_process_name.strip()
        self.tracker = NodeStateTracker(max_history=5)
        self.active_probe_urls: list[str] = [self.probe_url]
        self._controller_down_rounds = 0

    def _is_region_excluded(self, node_name: str) -> bool:
        """判断节点所属地区是否被排除。"""
        region = detect_region(node_name)
        if not region:
            return False
        return region.upper() in self.excluded_regions

    def _prepare_runtime_mode(self) -> None:
        """处理 TUN 开关与测速 URL 选择。"""
        tun_enabled: bool | None = None

        if self.tun_mode in {"on", "off"}:
            desired = self.tun_mode == "on"
            if not self.dry_run:
                try:
                    self.api.patch_configs({"tun": {"enable": desired}})
                    log(f"[模式] 已请求切换 TUN -> {'ON' if desired else 'OFF'}")
                except Exception as err:
                    log(f"[警告] 设置 TUN 失败: {err}")

        try:
            cfg = self.api.get_configs()
            tun_cfg = cfg.get("tun")
            if isinstance(tun_cfg, dict):
                tun_enabled = bool(tun_cfg.get("enable", False))
            elif isinstance(tun_cfg, bool):
                tun_enabled = tun_cfg
        except Exception as err:
            log(f"[警告] 读取运行配置失败: {err}")

        probe_urls: list[str] = []
        if tun_enabled is False and self.probe_url_non_tun:
            probe_urls.append(self.probe_url_non_tun)
        if self.probe_url:
            probe_urls.append(self.probe_url)

        probe_urls.extend(
            [
                "https://cp.cloudflare.com/generate_204",
                "https://www.gstatic.com/generate_204",
                "https://www.google.com/generate_204",
            ]
        )

        deduped: list[str] = []
        for item in probe_urls:
            if item and item not in deduped:
                deduped.append(item)

        self.active_probe_urls = deduped
        tun_text = "UNKNOWN" if tun_enabled is None else ("ON" if tun_enabled else "OFF")
        log(
            f"[模式] TUN={tun_text} | 排除地区={','.join(sorted(self.excluded_regions)) or '无'} | "
            f"测速URL={self.active_probe_urls[0]}"
        )

    def _probe_node(self, node_name: str) -> int | None:
        """对单节点做稳健测速：多 URL 探测 + 缓存回退。"""
        for url in self.active_probe_urls:
            delay = self.api.test_delay_reliable(
                node_name,
                url,
                self.probe_timeout_ms,
                rounds=1,
            )
            if delay is not None:
                return delay

        return self.api.get_cached_delay(node_name)

    def _resolve_effective_groups(self, all_proxies: dict) -> list[str]:
        """解析本轮生效的策略组。

        规则：
        1) 优先使用用户显式传入且存在的组名；
        2) 若显式组名全部不存在且禁用了自动发现，则直接失败；
        3) 仅在允许自动发现时，才回退到自动发现可切换组。
        """
        proxies = all_proxies.get("proxies", {})
        proxy_names = list(proxies.keys())

        explicit_groups: list[str] = []
        for group in self.groups:
            if group in proxies:
                explicit_groups.append(group)
                continue

            normalized_target = normalize_group_name(group)
            matched = [
                name for name in proxy_names if normalize_group_name(name) == normalized_target
            ]
            if len(matched) == 1:
                explicit_groups.append(matched[0])
                log(f"[提示] 策略组别名匹配: {group} -> {matched[0]}")
            elif len(matched) > 1:
                log(f"[警告] 策略组 {group} 匹配到多个候选: {', '.join(matched)}，请使用更精确组名")

        # 去重并保持顺序
        deduped_explicit_groups: list[str] = []
        seen = set()
        for group in explicit_groups:
            if group in seen:
                continue
            seen.add(group)
            deduped_explicit_groups.append(group)
        explicit_groups = deduped_explicit_groups

        if explicit_groups:
            return explicit_groups

        if self.groups and not self.allow_auto_discover:
            log("[失败] 显式策略组均未匹配，且已禁用自动发现")
            return []

        auto_groups: list[str] = []
        for name, data in proxies.items():
            if not isinstance(data, dict):
                continue
            if not data.get("now"):
                continue
            all_nodes = data.get("all")
            if not isinstance(all_nodes, list) or not all_nodes:
                continue
            if name.upper() in NON_PROXY_NAMES:
                continue
            auto_groups.append(name)

        auto_groups.sort()
        if auto_groups:
            log(f"[提示] 未匹配到显式策略组，自动发现并启用: {', '.join(auto_groups)}")
        return auto_groups

    def _enforce_domestic_direct(self, all_proxies: dict) -> None:
        """只锁定国内两组到 DIRECT，不改其它组。"""
        proxies = all_proxies.get("proxies", {})
        changed: list[tuple[str, str, str]] = []

        for group_name in DEFAULT_DOMESTIC_GROUPS:
            group = proxies.get(group_name)
            if not isinstance(group, dict):
                continue

            group_type = str(group.get("type", "")).lower()
            if group_type and group_type != "selector":
                continue

            choices = group.get("all")
            if not isinstance(choices, list) or "DIRECT" not in choices:
                continue

            current = str(group.get("now", ""))
            if current == "DIRECT":
                continue

            if self.dry_run:
                changed.append((group_name, current, "DIRECT"))
                continue

            try:
                self.api.switch_group(group_name, "DIRECT")
                changed.append((group_name, current, "DIRECT"))
            except Exception as err:
                log(f"[警告] 国内组锁定失败: {group_name}: {current} -> DIRECT, err={err}")

        if changed:
            action = "[演练]" if self.dry_run else "[锁定]"
            preview = ", ".join([f"{name}: {src}->{dst}" for name, src, dst in changed])
            log(f"{action} 国内组: {preview}")

    def _ensure_global_egress(self, all_proxies: dict) -> None:
        """确保 GLOBAL 不落在 DIRECT。

        现象：当 GLOBAL= DIRECT 时，规则命中的外网流量会全部直连并超时。
        处理：若当前为 DIRECT，优先切到 Proxies；否则尝试手动切换组。
        """
        proxies = all_proxies.get("proxies", {})
        global_group = proxies.get("GLOBAL")
        if not isinstance(global_group, dict):
            return

        current = global_group.get("now")
        if not isinstance(current, str):
            return
        if current.upper() != "DIRECT":
            return

        candidates = global_group.get("all", [])
        if not isinstance(candidates, list):
            candidates = []

        preferred = ["Proxies", "♻️ 手动切换", "手动切换"]
        target = next((name for name in preferred if name in candidates), None)
        if target is None:
            target = next((name for name in candidates if name.upper() != "DIRECT"), None)

        if not target:
            log("[警告] GLOBAL 当前为 DIRECT，且未找到可用代理组进行纠偏")
            return

        if self.dry_run:
            log(f"[演练] GLOBAL: 当前为 DIRECT，将纠偏切换到 {target}")
            return

        try:
            self.api.switch_group("GLOBAL", target)
            log(f"[纠偏] GLOBAL: DIRECT -> {target}")
        except Exception as err:
            log(f"[警告] GLOBAL 纠偏失败: {err}")

    def _update_memory_concurrently(self, nodes: list[str]) -> None:
        """并发测速并更新状态追踪器（代替原来的无记忆测速）。

        每个节点只做 1 轮测速，依靠多次 run_once 周期积累的
        历史数据做平滑，大幅提升探测速度。
        """
        if not nodes:
            return
        max_workers = min(20, len(nodes))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_node = {executor.submit(self._probe_node, node): node for node in nodes}
            for future in concurrent.futures.as_completed(future_to_node):
                node = future_to_node[future]
                try:
                    delay = future.result()
                except Exception:
                    delay = None
                self.tracker.record(node, delay)

    def _pick_best_available(
        self,
        current_node: str,
        all_nodes: list[str],
    ) -> tuple[str | None, int | None, bool]:
        """基于历史记忆与区域健康度的两级调度算法。

        宏观层：评估区域健康度，超时率 T(R) > 50% 时触发区域熔断。
        同时跳过被排除地区（--exclude-regions）。
        微观层：在目标区域内按 S(i) = <T(i), D(i)> 字典序选取最优节点。

        返回值：
        - 节点名（或 None）
        - 延迟（或 None）
        - 是否满足 max_delay_ms 阈值
        """
        # 排除当前节点
        candidates = [n for n in all_nodes if n != current_node and not self._is_region_excluded(n)]
        if not candidates:
            return None, None, False

        # 1. 并发测速，更新短期记忆
        probe_batch = candidates[: self.max_probe_per_round]
        self._update_memory_concurrently(probe_batch)

        # 2. 按地区分组
        nodes_by_region: dict[str, list[str]] = {}
        for node in probe_batch:
            reg = detect_region(node) or "UNKNOWN"
            nodes_by_region.setdefault(reg, []).append(node)

        current_reg = detect_region(current_node) or "UNKNOWN"

        # 3. 评估当前地区健康度
        curr_region_nodes = nodes_by_region.get(current_reg, [])
        curr_timeout_rate, _ = self.tracker.get_region_stats(curr_region_nodes, self.max_delay_ms)

        target_region: str | None = current_reg

        # 4. 宏观决策：超时率 > 50% 或当前地区无节点 -> 区域熔断
        if curr_timeout_rate > 0.5 or not curr_region_nodes:
            log(
                f"[宏观调度] 当前地区 {current_reg} "
                f"超时率({curr_timeout_rate:.0%}) > 50%，触发区域切换"
            )

            region_scores: list[tuple[str, float, float]] = []
            for reg in self.fallback_regions:
                if reg.upper() in self.excluded_regions:
                    continue
                reg_nodes = nodes_by_region.get(reg, [])
                if not reg_nodes:
                    continue
                t_rate, g_rate = self.tracker.get_region_stats(reg_nodes, self.max_delay_ms)
                # 过滤掉同样处于瘫痪状态的区域
                if t_rate <= 0.5:
                    region_scores.append((reg, g_rate, t_rate))

            if region_scores:
                # 按优良率降序、超时率升序排列
                region_scores.sort(key=lambda x: (-x[1], x[2]))
                target_region = region_scores[0][0]
                log(
                    f"[宏观调度] 决胜地区: {target_region} "
                    f"(优良率: {region_scores[0][1]:.0%}, "
                    f"超时率: {region_scores[0][2]:.0%})"
                )
            else:
                log("[警告] 所有回退地区均处于瘫痪状态，降级为全局搜索")
                target_region = None  # 全局混战

        # 5. 微观调度：构建优先队列 S(i) = <T(i), D(i)>
        search_space = (
            nodes_by_region.get(target_region, probe_batch) if target_region else probe_batch
        )

        pq: list[tuple[float, float, str]] = []
        for node in search_space:
            t_rate, avg_delay = self.tracker.get_node_stats(node)
            heapq.heappush(pq, (t_rate, avg_delay, node))

        # 6. 弹出最优节点
        while pq:
            t_rate, avg_delay, best_node = heapq.heappop(pq)
            if t_rate >= 1.0:
                continue  # 100% 超时节点，跳过
            meets_threshold = avg_delay <= self.max_delay_ms
            return best_node, int(avg_delay), meets_threshold

        return None, None, False

    def _collect_global_1x_candidates(self, proxies: dict) -> list[str]:
        """从全量代理树收集 1x 候选节点（用于组内候选为空时兜底）。

        规则：
        1) 优先收集“真实节点”条目（通常不含 all 字段）；
        2) 额外补充各策略组当前 now 为 1x 的节点名；
        3) 去重后按名称排序。
        """
        collected: list[str] = []

        for name, data in proxies.items():
            if not isinstance(data, dict):
                continue

            # 真实节点（非策略组）
            if "all" not in data and is_selectable_proxy(name) and detect_provider(name) == "1x":
                if self._is_region_excluded(name):
                    continue
                collected.append(name)

            # 策略组当前节点（用于兜底）
            now = data.get("now")
            if isinstance(now, str) and is_selectable_proxy(now) and detect_provider(now) == "1x":
                if self._is_region_excluded(now):
                    continue
                collected.append(now)

        deduped = sorted(set(collected))
        return deduped

    def _collect_global_candidates(self, proxies: dict) -> list[str]:
        """从全量代理树收集可选候选节点（不限制 1x）。"""
        collected: list[str] = []
        for name, data in proxies.items():
            if not isinstance(data, dict):
                continue
            if "all" not in data and is_selectable_proxy(name):
                if self._is_region_excluded(name):
                    continue
                collected.append(name)
            now = data.get("now")
            if isinstance(now, str) and is_selectable_proxy(now):
                if self._is_region_excluded(now):
                    continue
                collected.append(now)
        return sorted(set(collected))

    def _requires_1x(self, group_name: str) -> bool:
        """按策略组名决定是否强制 1x。

        规则：
        - Proxies: 不限制 1x
        - 手动切换（含 emoji 别名）: 强制 1x
        - 其他组：默认强制 1x（保守策略）
        """
        normalized = normalize_group_name(group_name)
        if normalized == normalize_group_name("Proxies"):
            return False
        if "手动切换" in group_name:
            return True
        return True

    def _is_sunday_1230(self) -> bool:
        """是否命中周日 12:30 的定时调度时间。"""
        now = datetime.now()
        return now.weekday() == 6 and now.hour == 12 and now.minute == 30

    def _pick_best_by_memory(self, candidates: list[str]) -> tuple[str | None, int | None]:
        """仅基于已记录的历史统计选择最优节点。"""
        pq: list[tuple[float, float, str]] = []
        for node in candidates:
            t_rate, avg_delay = self.tracker.get_node_stats(node)
            heapq.heappush(pq, (t_rate, avg_delay, node))

        while pq:
            t_rate, avg_delay, node = heapq.heappop(pq)
            if t_rate >= 1.0:
                continue
            return node, int(avg_delay)
        return None, None

    def _apply_sunday_japan_switch(
        self,
        group_name: str,
        current: str,
        node_list: list[str],
    ) -> bool:
        """周日 12:30 兜底：将策略组切到日本节点。"""
        if not self._is_sunday_1230():
            return False

        jp_candidates = [name for name in node_list if detect_region(name) == "JP"]
        if not jp_candidates:
            log(f"[周日12:30] {group_name}: 未找到日本节点，跳过定时切换")
            return False

        if detect_region(current) == "JP":
            log(f"[周日12:30] {group_name}: 当前已是日本节点 {current}，保持不变")
            return True

        probe_batch = jp_candidates[: self.max_probe_per_round]
        self._update_memory_concurrently(probe_batch)
        target, target_delay = self._pick_best_by_memory(probe_batch)
        if not target:
            target = jp_candidates[0]
            target_delay = self.api.get_cached_delay(target)

        delay_text = f"{target_delay}ms" if isinstance(target_delay, int) else "unknown"
        if self.dry_run:
            log(f"[周日12:30][演练] {group_name}: 将切换到日本节点 {target} ({delay_text})")
            return True

        self.api.switch_group(group_name, target)
        log(f"[周日12:30][切换] {group_name}: {current} -> {target} ({delay_text})")
        return True

    def _check_and_switch_group(self, all_proxies: dict, group_name: str) -> None:
        """检查单个策略组，必要时执行切换。"""
        proxies = all_proxies.get("proxies", {})
        group = proxies.get(group_name)
        switched_to_direct = False

        if not group:
            log(f"[跳过] 策略组不存在: {group_name}")
            return

        current = group.get("now")
        requires_1x = self._requires_1x(group_name)

        if requires_1x:
            node_list = [
                name
                for name in group.get("all", [])
                if is_selectable_proxy(name)
                and detect_provider(name) == "1x"
                and not self._is_region_excluded(name)
            ]
        else:
            node_list = [
                name
                for name in group.get("all", [])
                if is_selectable_proxy(name) and not self._is_region_excluded(name)
            ]

        if not node_list:
            fallback_nodes = (
                self._collect_global_1x_candidates(proxies)
                if requires_1x
                else self._collect_global_candidates(proxies)
            )
            if fallback_nodes:
                node_list = fallback_nodes
                if requires_1x:
                    log(f"[提示] {group_name}: 组内无1x候选，启用全局1x候选池({len(node_list)}个)")
                else:
                    log(f"[提示] {group_name}: 组内无候选，启用全局候选池({len(node_list)}个)")

        if not current:
            log(f"[跳过] 策略组 {group_name} 无当前节点")
            return

        if self._apply_sunday_japan_switch(group_name, current, node_list):
            return

        # 仅当 current 符合本组限制时才补入候选池
        if (
            current not in node_list
            and (not requires_1x or detect_provider(current) == "1x")
            and not self._is_region_excluded(current)
        ):
            node_list.insert(0, current)

        current_is_allowed = not self._is_region_excluded(current) and (
            (not requires_1x) or (detect_provider(current) == "1x")
        )

        if current_is_allowed:
            current_delay = self._probe_node(current)
            self.tracker.record(current, current_delay)

            if current_delay is not None and current_delay <= self.max_delay_ms:
                log(f"[健康] {group_name}: {current} ({current_delay}ms)")
                return

            reason = "测速失败" if current_delay is None else f"延迟过高({current_delay}ms)"
        else:
            # 非 1x 或命中排除地区，视为故障
            current_delay = None
            region_text = detect_region(current) or "UNKNOWN"
            if self._is_region_excluded(current):
                reason = f"当前节点地区被排除({region_text})"
            else:
                reason = f"当前节点非1x({current})"

        log(f"[故障] {group_name}: {current} -> {reason}，开始切换")

        # 【防 DNS 死锁】当节点完全失联时，Clash 的 DNS 出口也可能瘫痪，
        # 导致后续对备选节点的测速全部在 DNS 阶段超时（全红现象）。
        # 解决方案：先临时切换到一个备用代理节点（起搏器）唤醒 DNS，再测速备选节点。
        if current_is_allowed and current_delay is None and not self.dry_run:
            pacemaker_node = next((name for name in node_list if name != current), None)
            if pacemaker_node:
                try:
                    log(
                        f"[防死锁] {group_name}: 临时切换到备用节点 [{pacemaker_node}]，尝试唤醒 DNS..."
                    )
                    self.api.switch_group(group_name, pacemaker_node)
                    switched_to_direct = True
                    time.sleep(2)  # 等待 2s 让系统 DNS 请求刷新路由
                except Exception as e:
                    log(f"[警告] 切换起搏器节点失败: {e}")

        target, target_delay, meets_threshold = self._pick_best_available(current, node_list)
        if not target:
            if switched_to_direct and current and not self.dry_run:
                try:
                    self.api.switch_group(group_name, current)
                    log(f"[回滚] {group_name}: 未找到备选，恢复到原节点 {current}")
                except Exception as e:
                    log(f"[警告] {group_name}: 回滚原节点失败: {e}")
            log(f"[失败] {group_name}: 未找到可用备选节点")
            return

        if not meets_threshold:
            log(
                f"[降级] {group_name}: 未找到延迟 <= {self.max_delay_ms}ms 的节点，"
                f"改用可达节点 {target} ({target_delay}ms)"
            )

        if self.dry_run:
            log(f"[演练] {group_name}: 将切换到 {target} ({target_delay}ms)")
            return

        # 最终守卫：仅对强制 1x 的组禁止切到非 1x 节点
        if requires_1x and detect_provider(target) != "1x":
            if switched_to_direct and current and not self.dry_run:
                try:
                    self.api.switch_group(group_name, current)
                    log(f"[回滚] {group_name}: 目标非 1x，恢复到原节点 {current}")
                except Exception as e:
                    log(f"[警告] {group_name}: 回滚原节点失败: {e}")
            log(f"[拒绝] {group_name}: 目标节点 {target} 非 1x，跳过切换")
            return

        self.api.switch_group(group_name, target)
        log(f"[切换] {group_name}: {current} -> {target} ({target_delay}ms)")

    def run_once(self) -> None:
        """执行一次全量检查。"""
        self._prepare_runtime_mode()
        all_proxies = self.api.get_all_proxies()
        if self.lock_domestic_direct:
            self._enforce_domestic_direct(all_proxies)
        effective_groups = self._resolve_effective_groups(all_proxies)
        if not effective_groups:
            log("[失败] 未发现可切换的策略组，请检查 --groups 或 Clash 配置")
            return
        if "GLOBAL" in effective_groups:
            self._ensure_global_egress(all_proxies)

        for group in effective_groups:
            try:
                self._check_and_switch_group(all_proxies, group)
            except Exception as err:
                log(f"[异常] 策略组 {group} 检查失败: {err}")

    def run_forever(self) -> None:
        """持续运行守护循环。"""
        log("自动切换守护已启动")
        while True:
            try:
                self.run_once()
                self._controller_down_rounds = 0
            except Exception as err:
                log(f"[异常] 本轮检查失败: {err}")
                error_text = str(err)
                controller_unreachable = (
                    "连接失败" in error_text
                    or "WinError 10061" in error_text
                    or "Connection refused" in error_text
                )

                if controller_unreachable and self.exit_on_controller_down_rounds > 0:
                    self._controller_down_rounds += 1
                    if (
                        self._controller_down_rounds >= self.exit_on_controller_down_rounds
                        and not is_process_running(self.controller_process_name)
                    ):
                        log(
                            f"[退出] 控制器连续失败 {self._controller_down_rounds} 轮，"
                            f"且进程 {self.controller_process_name} 不存在，守护退出"
                        )
                        break
                else:
                    self._controller_down_rounds = 0
            time.sleep(self.interval_sec)


# =========================
# 5) CLI 入口
# =========================


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="Clash Verge Rev 自动切换脚本（同地区优先 + 跨订阅优先）",
    )
    runtime_controller, runtime_secret = load_runtime_controller_defaults()
    parser.add_argument(
        "--controller",
        default=runtime_controller,
        help="External Controller 地址（默认自动读取运行态 config.yaml，兜底 http://127.0.0.1:9090）",
    )
    parser.add_argument(
        "--secret",
        default=os.environ.get("CLASH_CONTROLLER_SECRET", runtime_secret),
        help="External Controller 密钥（默认自动读取运行态 config.yaml）",
    )
    parser.add_argument(
        "--groups",
        default="",
        help="要监控的策略组，英文逗号分隔；留空时自动发现可切换策略组",
    )
    parser.add_argument(
        "--probe-url",
        default=DEFAULT_PROBE_URL_TUN,
        help="TUN 模式优先测速 URL",
    )
    parser.add_argument(
        "--probe-url-non-tun",
        default=DEFAULT_PROBE_URL_NON_TUN,
        help="非 TUN 模式优先测速 URL",
    )
    parser.add_argument(
        "--probe-timeout-ms",
        type=int,
        default=2500,
        help="单次测速超时（毫秒）",
    )
    parser.add_argument(
        "--max-delay-ms",
        type=int,
        default=300,
        help="判定可用的最大延迟（毫秒）",
    )
    parser.add_argument(
        "--interval-sec",
        type=int,
        default=20,
        help="watch 模式下轮询间隔（秒）",
    )
    parser.add_argument(
        "--fallback-regions",
        default="TW,HK,JP,SG,US,KR",
        help="地区回退顺序（英文逗号分隔），例如 TW,HK,JP",
    )
    parser.add_argument(
        "--exclude-regions",
        default=",".join(DEFAULT_EXCLUDED_REGIONS),
        help="切换时排除的地区（英文逗号分隔），默认 HK",
    )
    parser.add_argument(
        "--tun-mode",
        choices=["auto", "on", "off"],
        default="auto",
        help="TUN 模式控制：auto(不改配置)/on/off",
    )
    parser.add_argument(
        "--max-probe-per-round",
        type=int,
        default=40,
        help="每轮每个策略组最多测速多少个候选",
    )
    parser.add_argument(
        "--exit-on-controller-down-rounds",
        type=int,
        default=6,
        help="watch 模式下控制器连续失败多少轮后尝试自退；设为 0 表示禁用",
    )
    parser.add_argument(
        "--controller-process-name",
        default="clash-verge.exe",
        help="用于判断是否应自退的进程名（Windows）",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--once",
        action="store_true",
        help="只执行一轮检查后退出（默认行为）",
    )
    mode_group.add_argument(
        "--watch",
        action="store_true",
        help="持续守护运行（不会自动退出）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="演练模式：只打印将要切换到的节点，不实际切换",
    )
    parser.add_argument(
        "--lock-domestic-direct",
        action="store_true",
        help="每轮执行前仅锁定国内两组(🌏 国内网站/🌏 国内流媒体)为 DIRECT",
    )
    parser.add_argument(
        "--disable-auto-discover",
        action="store_true",
        help="显式组全部失配时不自动发现，直接失败返回",
    )

    return parser.parse_args()


def main() -> int:
    """程序主入口。"""
    # 计划任务/无控制台场景：sys.stdout 可能为 None 或句柄无效（写入即崩）。
    # Installed Skills have no repository-relative root; use user runtime state.
    # 有控制台时强制 UTF-8，防止 emoji/中文在 Windows GBK 终端崩溃。
    if "--help" in sys.argv or "-h" in sys.argv:
        parse_args()
    _log_dir = pathlib.Path(os.environ["CLASH_SWITCH_LOG_DIR"])
    _log_dir.mkdir(parents=True, exist_ok=True)
    _log_path = _log_dir / "clash_auto_switch.log"

    def _stdout_ok() -> bool:
        """探测 stdout 是否可正常写入（计划任务下句柄可能无效）。"""
        try:
            sys.stdout.write("")
            sys.stdout.flush()
            return True
        except Exception:
            return False

    # 始终写入日志文件，同时尝试保留控制台输出（tee 模式）。
    # 计划任务下 stdout 句柄虽然存在但无控制台窗口，若不主动写文件则输出全部丢失。
    _log_file = open(_log_path, "a", encoding="utf-8", errors="replace", buffering=1)  # noqa: SIM115

    class _Tee:
        """同时写入文件和原始 stdout（若 stdout 不可用则仅写文件）。"""

        def __init__(self, file, console):
            self._file = file
            self._console = console

        def write(self, s: str) -> int:
            self._file.write(s)
            if self._console is not None:
                with contextlib.suppress(Exception):
                    self._console.write(s)
            return len(s)

        def flush(self) -> None:
            self._file.flush()
            if self._console is not None:
                with contextlib.suppress(Exception):
                    self._console.flush()

        def fileno(self):
            return self._file.fileno()

    _orig_stdout = sys.stdout if _stdout_ok() else None
    _orig_stderr = sys.stderr

    if _orig_stdout is not None and hasattr(_orig_stdout, "reconfigure"):
        with contextlib.suppress(Exception):
            _orig_stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(_orig_stderr, "reconfigure"):
        with contextlib.suppress(Exception):
            _orig_stderr.reconfigure(encoding="utf-8", errors="replace")

    sys.stdout = _Tee(_log_file, _orig_stdout)
    sys.stderr = _Tee(_log_file, _orig_stderr)

    args = parse_args()

    groups = [item.strip() for item in args.groups.split(",") if item.strip()]
    fallback_regions = [
        item.strip().upper() for item in args.fallback_regions.split(",") if item.strip()
    ]
    excluded_regions = [
        item.strip().upper() for item in args.exclude_regions.split(",") if item.strip()
    ]

    if excluded_regions:
        fallback_regions = [item for item in fallback_regions if item not in excluded_regions]

    timeout_sec = max(1.0, args.probe_timeout_ms / 1000.0 + 1.0)
    resolved_controller, resolved_secret, controller_ok = discover_controller_endpoint(
        preferred_url=args.controller,
        preferred_secret=args.secret,
        timeout_sec=timeout_sec,
    )
    if (resolved_controller != args.controller) or (resolved_secret != args.secret):
        redacted = "<empty>" if not resolved_secret else ("*" * min(len(resolved_secret), 8))
        log(f"[Controller] auto-discovered endpoint={resolved_controller}, secret={redacted}")
    if not controller_ok:
        log(f"[Controller] warning: endpoint unreachable now, fallback={resolved_controller}")

    api = ClashAPI(
        base_url=resolved_controller,
        secret=resolved_secret,
        timeout_sec=timeout_sec,
    )

    switcher = AutoSwitcher(
        api=api,
        groups=groups,
        probe_url=args.probe_url,
        probe_url_non_tun=args.probe_url_non_tun,
        probe_timeout_ms=args.probe_timeout_ms,
        max_delay_ms=args.max_delay_ms,
        interval_sec=max(5, args.interval_sec),
        fallback_regions=fallback_regions,
        excluded_regions=excluded_regions,
        tun_mode=args.tun_mode,
        max_probe_per_round=max(1, args.max_probe_per_round),
        dry_run=args.dry_run,
        allow_auto_discover=not args.disable_auto_discover,
        lock_domestic_direct=args.lock_domestic_direct,
        exit_on_controller_down_rounds=args.exit_on_controller_down_rounds,
        controller_process_name=args.controller_process_name,
    )

    if args.watch:
        switcher.run_forever()
        return 0

    switcher.run_once()
    return 0


if __name__ == "__main__":
    sys.exit(main())
