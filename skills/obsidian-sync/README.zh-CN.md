# 笔记同步（Obsidian Sync）

用真实云端副本和本地软链接，在明确选择的 Obsidian 库之间共享配置。

[English](README.md) · [模型指令](SKILL.md)

执行资源不要求其他 Skill。外部依赖为 Python 3.12+、macOS 和 Git。需要持久化安装时，可以选用 Chezmoi。

复制 config.example.json，替换所有接收者路径，再通过 scripts/obsidian-sync 的 --config、--print-config 和 --dry-run 检查。检查、补种、备份与监视注册细节见 SKILL.md。

从本仓库或 GitHub 原生归档下载**完整目录**，保留脚本与可执行权限。相对资源和配套 Skill 关系也是包的一部分。本包不包含个人账号、订阅、库列表、凭据或主机默认配置。请配置自己的真实目标；下载方法不代表运行时服务已经安装。

原始可复用内容与公开适配采用 MIT 许可证，见 [LICENSE](LICENSE)。第三方应用与服务保留各自权利。
