---
name: model-upgrade-check
description: "<用户自制> 模型升级检查：按实际用途核对模型、推理档位与消费者。 Model upgrade check: reconcile model and reasoning choices with actual purposes and consumers."
user-invocable: true
---

# model-upgrade-check

Maintain model choices by purpose as providers and catalogs change. A model
announcement, a similar-looking version label, or a successful configuration
write does not establish that a choice fits its intended work or that a
consumer is using it.

## Discover the actual system

Start from the user's request and the affected work. Establish which purpose,
role, account, provider, and consumer are in scope. Respect explicit current
task choices and preserve running sessions and their account/provider identity.
Do not infer that all consumers share one provider, catalog, policy file, or
fallback.

Inspect the recipient's actual configuration and supported interfaces to find:

- the policy or source that owns purpose-to-model choices;
- the executable settings, generators, and runtime consumers that realize it;
- the active provider and account for each affected consumer;
- the provider's current model catalog and supported reasoning effort, mode,
  or capability tier;
- any established fallback and the conditions under which it is supported.

Use authenticated or account-specific catalogs through an authorized session
or the recipient's existing credential owner, without exposing credential
values. Prefer provider documentation for unsettled behavior. If a consumer or
mapping cannot be inspected, retain it as unknown instead of assuming a name
or capability correspondence. Preserve provider/account identity; do not
switch them as a shortcut.

## Select by purpose

For each affected role or consumer, derive the capability it needs from its
actual work, latency and quality needs, and consequences of error. Compare
currently available candidates by demonstrated or documented capability,
supported effort/mode, and operational fit. Match local IDs and hosted labels
by task capability and purpose, never by spelling or version-number similarity.
Select effort separately from model choice. Preserve explicit user selections
and any still-supported specialized choice; do not migrate unrelated consumers
because a new model exists.

Record the current choice, proposed choice, reason, source of current
availability evidence, supported fallback, and affected consumers. A fallback
is valid only when that same consumer can use it under its actual provider and
account configuration. If no fallback is verified, say so. Keep historical
notes, examples, announcements, and prompting guides separate from active
policy.

## Change the owning policy and consumers

Use [prompt-and-skill-lifecycle](../prompt-and-skill-lifecycle/SKILL.md) when
changing instruction or Skill assembly. For durable host configuration, use
[chezmoi](../chezmoi/SKILL.md) with the recipient's configured publication owner;
the local source calls that owner `macos-publish`, which is not bundled here.
For unsettled OpenAI product behavior, use the host's available `openai-docs`
alongside relevant independent evidence through [research](../research/SKILL.md).
These are conditional method relationships, not mandatory provider integrations
for a read-only catalog check. Actual tools and authority remain host-supplied.

Find the actual owner of each policy and configuration field before editing.
Update the authoritative purpose-to-model rule and remove displaced active
instructions that would conflict with it. Change only the affected executable
consumer settings through their existing configuration owner. Provider-required
identifiers may remain in executable configuration as realizations of the
policy. Keep provider-specific syntax and version IDs out of reusable role
guidance unless that guidance itself owns a verified specialized selection.

Preserve account and provider identity, credentials, schedules, enabled state,
task identity, and running sessions. Do not restart an active conversation to
force a new default. Treat ordinary updates according to the recipient's real
authorization and publication boundaries; this Skill adds no approval gate or
deployment process.

## Verify through the real consumer

For every affected consumer, keep these observations distinct:

1. **Policy source:** the maintained instruction or setting names the intended
   purpose-based choice and fallback.
2. **Runtime readback:** the assembled instructions or effective configuration
   actually exposes the intended model, effort/mode, provider, and account.
3. **Successful use:** the real consumer completes a small, meaningful,
   authorized request using that selection.

One observation does not prove the next. Verify at the consumer's public
entrypoint where possible; a rendered prompt does not prove a saved model field,
and a configuration readback does not prove the consumer can run. Use a safe
public probe only when it provides useful evidence without changing unrelated
state. For an account-specific hosted selector, read back the selected model
and mode before any in-scope use. Do not launch unrelated jobs or submit a
consultation just to validate policy prose.

If context-window settings are part of the requested change, inspect effective
window and compaction behavior, including inherited settings, separately from
conversation-history isolation. A short request can verify effective
configuration, not long-context quality.

Report the policy source changed, each consumer's runtime readback, successful
use evidence, and any unavailable or unverified mappings separately. State
what remains unknown and the concrete next check. Do not claim a complete
migration from source edits alone.
