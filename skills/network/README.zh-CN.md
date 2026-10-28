# network

沿请求链路诊断网络，通过实际配置负责人修复，并提供可配置的代理检查和配置恢复工具。

[English](README.md) · [模型指令](SKILL.md)

使用控制器、切换或保护方法时，还须下载 **clash-auto-switch**。实际互斥与配置恢复实现已包含。接收者自己的基准配置、Colima 和运行时配置仍需另行提供。

在选定的 Python 环境安装 PyYAML。复制两份 JSON 模板并替换全部路径，先执行 scripts/proxy-purity 的 check-config，以及 scripts/network-repair 的 --files-only status。帮助命令无需配置。

将 colima_profile 设为自己的既有 Colima 虚拟机名称；扫描器不会选择作者的配置或隐式默认配置。模板里的 recipient-profile 是占位值。

从本仓库或 GitHub 原生归档下载**完整目录**，保留脚本与可执行权限。相对资源和配套 Skill 关系也是包的一部分。本包不包含个人账号、订阅、库列表、凭据或主机默认配置。请配置自己的真实目标；下载方法不代表运行时服务已经安装。

原始可复用内容与公开适配采用 MIT 许可证，见 [LICENSE](LICENSE)。第三方应用与服务保留各自权利。
