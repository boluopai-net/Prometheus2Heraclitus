# prompt-audit-orchestration

**按用途、所有权、消费者和可观察结果审计相互连接的指引系统。**

[English](README.md)

本 Skill 协调四个相关领域的按需审计：学习、工作流、托管助手与已保存任务。它保留各领域
独立的判断和来源归属，同时协调共享依赖、每个可变来源的单一写入者，以及受影响消费者的证据。

## 使用与配套 Skill

通过助手支持的 Skill 机制提供完整的 `prompt-audit-orchestration/` 目录。必要配套 Skill 是
[`prompt-and-skill-lifecycle`](../prompt-and-skill-lifecycle/)，负责来源编写、整合与发布；以及
[`agent-orchestration-master`](../agent-orchestration-master/)，负责智能体角色、派发、协调和交接。
它们各自拥有其方法；本 Skill 保留审计路由、领域权限和完成判断。

需要外部证据时可使用 [`research`](../research/)；需要澄清未决的用户选择时可使用
[`task-inquiry`](../task-inquiry/)。学习审计可按需使用 [local-teacher](../local-teacher/) 或
[web-teacher](../web-teacher/) 来理解相应教学方法；浏览器操作可按需使用
[browser-relay](../browser-relay/)配合宿主实际的受控浏览器能力。下载需要的配套目录，
并按各包说明配置自己的环境。宿主原生的智能体委派支持属于运行时能力，
不是需要下载的 Skill。

## 内容与边界

[`SKILL.md`](SKILL.md) 定义单领域与联合审计路由、协调、用户判断转达、覆盖范围、按来源所有权执行修复，
以及证据要求。[`references/`](references/) 中的四个适配器保留了不同领域范围及跨领域来源责任。本方法
不绑定服务商：应在接收环境中查明实际来源所有者、消费者、模型策略、工具和发布接口。它不固定模型版本、
账户、项目身份，也不添加强制审批步骤。

本包改编自本地编排方法，移除了专用宿主路径和具名受保护项目例外；保留了通用规则：所有者明确保护的
目标只能作为证据读取。配套的 [`agent-orchestration-master`](../agent-orchestration-master/) 是独立 Skill，
不会嵌入本包。

本包采用 [MIT 许可](LICENSE)。可从 [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/prompt-audit-orchestration)
获取完整目录。
