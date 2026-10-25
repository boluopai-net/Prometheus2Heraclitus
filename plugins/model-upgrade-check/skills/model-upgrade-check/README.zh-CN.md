# 模型升级检查 · model-upgrade-check

**按实际用途维护模型选择，并核实真正使用这些选择的消费者。**

[English](README.md)

当服务商目录变化时，本 Skill 帮助助手调整模型与推理档位。它先查明接收方实际使用的
服务商、账户、角色策略、配置归属和消费者，再按照工作需要匹配可用选项，并分别核实策略、
运行时读回结果与消费者的成功使用。

## 使用本 Skill

通过助手支持的 Skill 机制提供完整的 `model-upgrade-check/` 目录；当需要依据当前可用性
调整模型选择或更新受影响的消费者时，调用**模型升级检查 · model-upgrade-check**。
方法位于 [`SKILL.md`](SKILL.md)。它不依赖私人上下文、脚本或特定服务商集成；请使用你所在
环境实际提供的接口和权限。

## 检查内容

保留原方法的按需配套关系：修改指令或 Skill 时，下载
[prompt-and-skill-lifecycle](../prompt-and-skill-lifecycle/)；持久化主机配置时，配合
[chezmoi](../chezmoi/)和自己配置的发布责任方。原来的 `macos-publish` 服务没有包含在这里，
chezmoi 包说明了使用者需要提供的发布能力。OpenAI 行为仍不确定时，可由宿主提供的外部
`openai-docs` 配合 [research](../research/)调查。只读模型目录不要求先安装整套配置系统。

这套方法先确定受影响的用途和消费者，检查权威策略、真实服务商与账户目录，再按能力和任务
适配度选择支持的模型与推理档位。它保留明确指定的选择、账户边界和进行中的会话。获得授权
并完成变更后，分别核实维护后的策略、运行时配置读回，以及实际消费者能否工作。

例如，角色指引已经写入新模型，但某个自动化保存的模型字段仍是旧值。读取指引只能核实策略，
读取自动化配置才能核实该项设置；一次小规模运行才能验证消费者确实可以使用。三者回答的是
不同问题。

## 独立性与许可

本包将本地 `model-upgrade-check` Skill 改写为可复用、与服务商无关的方法。它以接收方实际的
配置归属和消费者接口发现流程，替换了原有的宿主专用路径和同步步骤。源环境中可选的消费者
示例不构成本包的前置条件。

本独立软件包采用 [MIT 许可](LICENSE)。你可以从 [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/model-upgrade-check)
获取完整目录，并在保留 MIT 要求声明的前提下使用、修改和再分发，包括商业用途。
[公开集合仓库](https://github.com/boluopai-net/Prometheus2Heraclitus)提供下载与 Issue 交流，本集合不接受 PR。
