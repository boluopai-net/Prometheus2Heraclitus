# 模型升级检查 · model-upgrade-check

**Maintain model choices by actual purpose, then verify the consumers that use them.**

[简体中文](README.zh-CN.md)

This Skill helps an assistant update model and reasoning choices as provider
catalogs change. It starts by discovering the recipient's real providers,
accounts, role policy, configuration owners, and consumers. It then matches
supported choices to actual work and checks policy, runtime readback, and
successful use as separate evidence.

## Use this Skill

Make the complete `model-upgrade-check/` directory available through the Skill
mechanism supported by your assistant, then invoke **模型升级检查 ·
model-upgrade-check** when you need to reconcile model choices with current
availability or update affected consumers. The method is in
[`SKILL.md`](SKILL.md). It requires no private context, scripts, or specific
provider integration; use the interfaces and authority available in your own
environment.

## What it checks

Companion methods preserve the source workflow: download
[prompt-and-skill-lifecycle](../prompt-and-skill-lifecycle/) for instruction/Skill
changes, and [chezmoi](../chezmoi/) when persisting host configuration through your
configured publication owner. The original `macos-publish` service is not included;
the chezmoi package explains the recipient publication contract. For unsettled
OpenAI behavior, the host's external `openai-docs` Skill can supplement
[research](../research/). These are conditional relationships; reading a model
catalog does not require installing an entire configuration system.

The method establishes the affected purpose and consumer, inspects the
authoritative policy and real provider/account catalog, and chooses a supported
model and effort by capability and task fit. It preserves explicit choices,
account boundaries, and active sessions. After an authorized change, it
distinguishes the maintained policy from runtime configuration readback and
evidence that the actual consumer works.

For example, a role instruction may name a new model while an automation still
has its old saved model field. Reading the instruction verifies the policy;
reading the automation verifies its setting; a small run verifies use. Each
answers a different question.

## Independence and license

This package adapts the local `model-upgrade-check` Skill into a reusable
provider-neutral method. It replaces host-specific paths and synchronization
steps with discovery through the recipient's actual configuration owners and
consumer interfaces. Optional consumer examples from the source environment
are not prerequisites.

This independent package uses the [MIT License](LICENSE). You may obtain the
complete directory from [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/model-upgrade-check)
and use, modify, and redistribute it, including commercially, with the
required MIT notices. The [public collection](https://github.com/boluopai-net/Prometheus2Heraclitus)
provides downloads and Issue discussion; this collection does not accept pull requests.
