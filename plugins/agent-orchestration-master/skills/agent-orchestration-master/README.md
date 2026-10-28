# agent-orchestration-master

**Design agent roles, delegation, handoffs, and shared work around the actual task.**

[简体中文](README.zh-CN.md)

This Skill helps choose whether delegation adds a distinct contribution, map
work to the host's actual roles and carriers, coordinate dependencies and
mutable targets, and preserve accountable handoffs. It treats a single agent
as sufficient by default when no real coordination need exists.

## Use and dependencies

Provide the complete `agent-orchestration-master/` directory through your
assistant's Skill mechanism when designing or operating multi-agent work. The
paired [`prompt-audit-orchestration`](../prompt-audit-orchestration/) package
uses this Skill for its agent roles and handoffs; this Skill does not own that
audit's domain routing or repair authority.

The conditional companion Skills `multi-agent-patterns` (topology design),
`harness-engineering` (durable agent harnesses), and `tool-design` (tool
interfaces) are not included in this collection yet.
`project-development`, `cloud-local-workflow`, and
`model-conversation-relay` may be useful for the specific work they own; they
are not required for ordinary delegation. Follow the current host's model
policy and actual agent catalog; no model version is prescribed here.

Host-native role support, isolation, and delegation interfaces are runtime
capabilities, not Skill dependencies. Inspect them before dispatch and report
unsupported mappings instead of assuming role-name compatibility.

## Independence and license

The package adapts a local method into a host-neutral workflow. It removes
host-specific agent formats and publication commands while retaining role
scope, task ownership, dispatch context, safe parallelism, review selection,
integration, and native-carrier readback.

This package uses the [MIT License](LICENSE). Obtain the complete directory
from [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/agent-orchestration-master).
