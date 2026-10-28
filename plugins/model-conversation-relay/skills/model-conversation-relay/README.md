# model-conversation-relay

[简体中文](README.zh-CN.md)

Relay one exact exchange with an already bound ChatGPT advisory conversation.
Preserve the caller's request, the other model's response and their origins,
while leaving interpretation, correctness and task acceptance with the caller.

Read [SKILL.md](SKILL.md) for the complete method. Examples: continue waiting for
an acknowledged request; reconcile an interrupted first submission; submit an
authorized exact follow-up once; retain an immutable receipt for the bound answer.
This relay does not create or select conversations, change models or rewrite
either side of the exchange.

## Install and bind

Install `model-conversation-relay@boluopai` through the collection's
[Codex instructions](https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/docs/codex.md),
or obtain this complete directory through
[GitHub source](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/model-conversation-relay)
and your client's supported Skill mechanism. Installation supplies instructions,
not account access, message authorization, browser control or a running service.

| Capability or companion | Actual requirement |
| --- | --- |
| Caller and private task storage | Required: exact conversation/mode/readiness binding, authorized operation, exact request bytes and SHA-256, prior turn/attempt evidence, and a private location for immutable request, response and receipt files. The caller retains surrounding task/source provenance and answer judgment. |
| Native conversation adapter | Conditional: a currently exposed tool and schema that address the exact target and expose sufficient ordered-turn, running and acknowledgement evidence. The Codex App tool names in the entrypoint are examples, not portable API guarantees. Observe and send are separate capabilities and authorities. |
| [Browser Relay](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/browser-relay) | Required only for the selected Browser Relay route: install `browser-relay@boluopai`, read its complete entrypoint and bind a recipient-configured controlled carrier, intended authenticated account, target custody and lifecycle. It does not install a browser controller or grant login access. |
| Host continuation and credential owners | Supply supported waiting/resumption, actual login/consent boundaries and safe desktop behavior. A note does not schedule a wake-up; without supported continuation report the retained pending exchange. |
| `cloud-local-workflow` | Optional host-specific provenance owner when already present. It is not a public collection member or installation prerequisite. Without it, retain task, source, model-selection and first-submission evidence in the caller's existing records. |

Keep transport receipts, actual conversations, account/profile identifiers and
private requests outside the public package, plugin cache and public repository.
Resolve all bindings from the recipient's current host; no author account,
credential, profile, path or conversation is supplied here.

## Evidence and limits

The method freezes target and request identity, reconciles ordered turns before
mutation, keeps one attempt in flight and treats acknowledged sends as pending
even before a remote turn becomes visible. An idle target or observation lag does
not authorize a resend. Explicit non-acceptance or an observed terminal incomplete
response can justify only the exact retry allowed by the entrypoint. Interruption
recovery retains acknowledgement and retry history instead of resetting them.

A completed transport receipt binds an observed response to its request and
target; it does not certify the answer's correctness, evidence quality or task
completion. Keep the original response intact when evaluating or forwarding it.

Package/discovery checks and offline reconciliation scenarios can establish
delivery and inspect decision boundaries without sending a message. Actual
authenticated transport, provider completeness signals and continuation must be
verified on the recipient's real authorized exchange. Installing, authoring or
testing this Skill supplies no authorization for a test advisory message.

This public adaptation preserves the local exchange, reconciliation, waiting,
retry, provenance and receipt method, with recipient-resolved host bindings and
an optional provenance companion. Original package material is
[MIT licensed](LICENSE), copyright 2026 sun2paramita. Host tools and relayed
material retain their own rights. No third-party runtime is bundled.
