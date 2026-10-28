# agent-orchestration-master

**围绕实际任务设计智能体角色、委派、交接与协作。**

[English](README.md)

本 Skill 帮助判断委派能否带来独立贡献，将工作分配给宿主实际支持的角色与执行载体，协调依赖和可变目标，
并保留可追责的交接。如果没有真实的协调需要，默认由单个智能体完成即可。

## 使用与依赖

在设计或运行多智能体工作时，通过助手支持的 Skill 机制提供完整的 `agent-orchestration-master/` 目录。
配套的 [`prompt-audit-orchestration`](../prompt-audit-orchestration/) 使用本 Skill 处理智能体角色和交接；
本 Skill 不负责该审计的领域路由或修复权限。

进行实质拓扑设计时可使用 `multi-agent-patterns`，设计持久运行框架时可使用 `harness-engineering`，
设计工具接口时可使用 `tool-design`。这些按需配套 Skill 目前尚未收录于本集合。具体工作也可能需要 `project-development`、
`cloud-local-workflow` 或 `model-conversation-relay` 所负责的方法；普通委派不要求这些 Skill。遵循宿主当前的
模型策略和实际智能体目录；本包不指定模型版本。

宿主原生角色、隔离与委派接口属于运行时能力，不是 Skill 依赖。派发前应检查这些能力；角色名称不兼容时，
应报告实际差异，不要自行假定它们等价。

## 独立性与许可

本包将本地方法改写为通用工作流，移除了特定宿主的智能体格式与发布命令，同时保留角色范围、任务所有权、
派发上下文、安全并行、审查选择、整合和原生载体读回方法。

本包采用 [MIT 许可](LICENSE)。可从 [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/agent-orchestration-master)
获取完整目录。
