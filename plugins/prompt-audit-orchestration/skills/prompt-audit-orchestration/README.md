# 提示词审计编排 · prompt-audit-orchestration

**Audit connected instruction systems by purpose, ownership, consumers, and observable effects.**

[简体中文](README.zh-CN.md)

This Skill coordinates on-demand audits across four related domains: Learning,
Workflow, Hosted assistant, and Saved Task. It preserves separate domain
judgment and source ownership while coordinating shared dependencies, one
writer per mutable source, and evidence across each affected consumer.

## Use and companion packages

Provide the complete `prompt-audit-orchestration/` directory through your
assistant's Skill mechanism. Its required companion Skills are
[`prompt-and-skill-lifecycle`](../prompt-and-skill-lifecycle/) for source
authoring, integration, and publication, and
[`agent-orchestration-master`](../agent-orchestration-master/) for agent
roles, dispatch, coordination, and handoffs. They own their methods; this
Skill keeps audit routing, domain authority, and completion judgment.

Use [`research`](../research/) when external evidence is material and
[`task-inquiry`](../task-inquiry/) when an unresolved user-owned choice needs
to be framed. Learning audits may conditionally use
[local-teacher](../local-teacher/) or [web-teacher](../web-teacher/) to understand
the corresponding teaching method. Browser work may use
[browser-relay](../browser-relay/) with the host's actual controlled browser
capability. Download the needed companion directories; each retains its own
configuration requirements. Host-native delegation support is a
runtime capability, not a downloadable Skill dependency.

## Package contents and boundaries

[`SKILL.md`](SKILL.md) defines single-domain and joint audit routing,
coordination, human-judgment relay, coverage, ownership-based repair, and
evidence requirements. The four adapters in [`references/`](references/)
preserve distinct domain scope and cross-domain source responsibility. The
method is provider-neutral: resolve actual source owners, consumers, model
policy, tools, and publication interfaces in the recipient environment. It
adds no fixed model version, account, project identity, or mandatory approval
step.

This package adapts a local orchestration method and removes its private host
routes and named protected-project exception. It retains the general rule that
any owner-declared protected target is evidence-only. Its paired
[`agent-orchestration-master`](../agent-orchestration-master/) package is a
separate companion, not embedded here.

This package uses the [MIT License](LICENSE). Obtain the complete directory
from [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/prompt-audit-orchestration).
