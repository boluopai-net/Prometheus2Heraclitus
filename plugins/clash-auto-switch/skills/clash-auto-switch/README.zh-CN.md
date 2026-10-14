# 节点自动切换（Clash Auto Switch）

配置控制器发现、地区回退、可恢复的模式与 DNS 切换，以及范围受限的 DNS 保护。

[English](README.md) · [模型指令](SKILL.md)

还须下载 **network**，沿用其授权与恢复边界，并安装其中的实际互斥程序或经过验证的兼容实现。Clash Verge Rev、现代 Python、桥接所需的 socat 和特权运行时仍需另行准备。

复制 config.example.json 并替换所有路径和组名，先执行 scripts/clash-tool 的 check-config。controller、nodes、mode、guard、setup 各入口的实际作用见 SKILL.md；改变运行状态之前先阅读授权边界。

从本仓库或 GitHub 原生归档下载**完整目录**，保留脚本与可执行权限。相对资源和配套 Skill 关系也是包的一部分。本包不包含个人账号、订阅、库列表、凭据或主机默认配置。请配置自己的真实目标；下载方法不代表运行时服务已经安装。

原始可复用内容与公开适配采用 MIT 许可证，见 [LICENSE](LICENSE)。第三方应用与服务保留各自权利。

网络恢复可以将 scripts/clash-controller 配置为 controller_command，将本包的接收者 JSON 配置为 controller_config。直接使用时设置 CLASH_SKILL_CONFIG=/absolute/config.json，再执行 scripts/clash-controller request GET /version。包装器会解析安装目录里的实际资源。
