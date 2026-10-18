---
name: personal-environment-design
description: "个人环境设计：统筹提示词、Skill、MCP、插件、应用、自动化、服务与使用体验的配置。 Use when setting up, connecting, extending, or revising a personal working environment and its capabilities."
---

# Personal Environment Design

Make the environment a coherent place for the person and model to work together.
Its visible surfaces should support understanding and action; its instructions,
tools, connections, and services should supply the needed capabilities with
reasonable resource use and maintenance. A convenient interface and a sound
technical arrangement contribute to the same lived environment.

This is the overall design and configuration entrypoint. Read it when installing,
connecting, configuring, replacing, or materially reorganizing the user's
environment, including prompts, Skills, MCP servers, plugins, applications,
automation, and local or cloud services. Ordinary use of an already configured
tool does not require another environment-design exercise. Keep the scope at
the requested change and its necessary dependencies; a small configuration
change does not authorize a whole-environment rebuild.

The person and model both generate, judge, and revise. The model carries the
discovery, integration, implementation, and maintenance it can resolve; the
person's purposes, experience, and consequential choices guide the result.
An available situated philosophy or relationship account can clarify these
purposes and contributions when relevant. This Skill supplies environment
methodology, while specialists retain their own methods, publication boundaries,
and actual access authority.

## Understand the connected environment

Start with what the person or model needs to accomplish and what the current
environment already provides. Trace the relevant path from instruction or user
action through capability discovery, connection, execution, and observable result.
Read the affected configuration and real consumer before choosing a change.
An installed package, a discoverable tool, a working login, and a successful
operation establish different parts of that path.

Consider both human and machine costs where they matter: understanding and
operation, startup and latency, memory and repeated processes, external service
cost, reliability, updates, and recovery. Compare reusing, configuring, replacing,
or building against the actual purpose. Inspect current upstream implementations
when their capabilities affect the choice. A new layer earns its place through
a concrete contribution; remove displaced duplication after successor readback.

For a substantive change, establish the current arrangement, intended result,
affected dependencies, and sufficient acceptance evidence before implementation.
Follow configuration to its maintained source, runtime consumer, and update or
publication owner. Keep credentials and application sessions with their existing
owners. Decide from current evidence rather than treating installed state as the
desired design. A short explanation and coherent patch can be sufficient; this
entrypoint adds no separate Plan, approval gate, registry, or scheduler.

## Compose the needed capabilities

Read only the resources and specialists relevant to the actual change. Discover
what is actually available before selecting a companion method or tool; the
person need not choose internal routing.

| Affected part | Contribution and owner |
| --- | --- |
| Prompts and Skills | Use an available authoring and management method, such as `prompt-and-skill-lifecycle`, for meaning, discovery, packaging, review, delivery, and consumer readback. Its specialist lifecycle remains separate from this overall environment method. |
| MCP and service placement | Read [MCP and services](references/mcp-and-services.md) for transport, process lifetime, sharing, and local/cloud placement. Use available tool-contract or interface-design expertise where needed. |
| Plugins and connectors | Use the current host's native management capability and relevant specialist. Inspect the tools, Skills, connections, background processes, dependencies, authentication, and update behavior the package actually supplies. Compare existing usable routes before installing a duplicate. |
| Applications and host configuration | Use the application's or host's current configuration, persistence, and service-management owners. Trace maintained source to the running consumer rather than assuming one configuration file controls both. |
| Automation and event-driven effects | Use the actual scheduling or lifecycle-event owner. Add background machinery only when its contribution is needed; inspect its trigger, execution environment, state, and result. |
| Human-facing surfaces and workflows | Read [Human use](references/human-use.md). Compose the affected website/content maintainer, design, frontend, or native application capability. |
| Failures and uncertain behavior | Use the affected diagnostic specialist or available native evidence to resolve concrete uncertainty, then return to the intended result. |

A plugin is a delivery unit, an MCP endpoint a connection, and a Skill an
instructional capability; inspect their actual relationships rather than
assuming the labels describe independent installations. Select the actual
account, host, project, and consumer. Preserve deliberate disabled components
and host-specific differences. Installing one component does not authorize
enabling unrelated capabilities or copying private material to another service.

## Realize and verify the whole affected path

Carry the change through the relevant specialists and publication owners to
actual use. For an instruction change, check discovery and readable content;
for a connection, check authentication and a representative operation; for a
shared service, check concurrency boundaries and the claimed resource benefit;
for a visible workflow, exercise its real entrypoint and resulting effect.
Use only the checks needed to settle material uncertainty. A configuration diff,
package installation, or healthy process alone does not prove the intended result.

After replacement works, retire displaced registrations, startup entries,
bridges, or configuration that no current consumer needs. Preserve useful data,
sessions, and recovery evidence under their actual owners. Keep maintenance
knowledge with the affected project; show the user the resulting capability,
meaningful choices, verification, and any remaining required difference.

The overall task owner retains integration and completion while specialists
carry their contributions. A specialist handoff is progress when more work is
needed for the user's outcome. A requested exploration may finish with grounded
options; an implementation request continues through delivery and readback.

This package provides methods, not installed integrations or access. Do not
assume the author's desktop, browser profile, credential store, companion Skills,
private history, or service stack exists in the recipient's environment.

The [design basis](references/design-basis.md) explains the reusable distinctions
and scope of this public adaptation. It is supporting rationale rather than a
second operating procedure.
