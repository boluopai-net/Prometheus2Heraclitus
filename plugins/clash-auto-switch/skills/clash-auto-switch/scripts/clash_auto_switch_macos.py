#!/usr/bin/env python3
"""
macOS 入口：复用 clash_auto_switch.py 的核心逻辑。

能力：
1) 自动从 Clash Verge Rev 运行态 config.yaml 读取 external-controller 与 secret。
2) 自动注入 macOS 默认参数（避免 Windows 进程名判断影响）。
3) 其余参数透传给原脚本（如 --watch / --groups / --dry-run）。
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

from clash_controller import Controller


def _load_mac_runtime_controller_defaults() -> tuple[str, str]:
    """读取 macOS Clash Verge Rev 运行态 controller 与 secret。"""
    cfg_root = pathlib.Path(os.environ["RUNTIME_ROOT"])
    controller = Controller.discover(cfg_root)
    url = "unix://" + str(controller.unix_socket) if controller.unix_socket else controller.base_url
    return (url, controller.secret)


def main() -> int:
    script_dir = pathlib.Path(__file__).resolve().parent
    core_script = script_dir / "clash_auto_switch.py"
    if not core_script.exists():
        print(f"[错误] 找不到核心脚本: {core_script}", file=sys.stderr)
        return 1

    if "--help" in sys.argv or "-h" in sys.argv:
        return subprocess.call([sys.executable, str(core_script), "--help"])
    controller, secret = _load_mac_runtime_controller_defaults()

    user_args = sys.argv[1:]
    cmd = [
        sys.executable,
        str(core_script),
        "--controller",
        controller,
        "--controller-process-name",
        "io.github.clash-verge-rev.clash-verge-rev",
        "--exit-on-controller-down-rounds",
        "0",
    ] + user_args

    env = dict(os.environ)
    env["CLASH_CONTROLLER_SECRET"] = secret
    return subprocess.call(cmd, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
