---
name: model-conversation-relay
description: "<用户自制> 模型对话接续：继续已绑定的 ChatGPT 咨询会话，读取、等待、发送并留存回执。 Continue one exact ready-bound ChatGPT advisory conversation through serial read, wait, send, retry, and immutable receipt persistence. It never creates or substitutes a conversation, Browser target, or destination."
user-invocable: true
---

# model-conversation-relay

A relay keeps two voices distinct while making their exchange traceable. The
request remains the caller's exact contribution; the response remains the
other model's observed contribution. Carry each across the boundary with its
origin intact, so the caller can judge what the answer means for the task.
Transport establishes that this response belongs to this request at this
conversation; interpretation and acceptance remain further judgments.

Continue one ready-bound request/response exchange. Responsibilities are:

| Owner | Responsibility |
| --- | --- |
| Caller | Destination creation and selection, first-request reconciliation, task and source provenance, model selection, outbound-message authority, semantic follow-up, interpretation, and task completion. |
| Relay | Exact exchange identity, ordered-turn reconciliation, response-turn completeness, wait/retry decisions, immutable evidence, and at most one mutation attempt in flight. |
| Operation adapter | Physical or native observations and, when selected for mutation, submission to the frozen target. An observation adapter never submits or resends. |

Native task/thread and permitted controlled Browser carriers are per-operation
adapters and may differ between observation and mutation. Read the installed
`browser-relay` entrypoint completely when selecting that route; native-only
operations do not need this conditional companion. Reuse actual authorization
for the exchange; installing or testing this package does not authorize a
submission. Runtime owners retain host confirmation, login, credential, consent,
and human-action boundaries. Conversation creation, model changes, and account
settings stay outside the relay's operations. The relay binds a complete response
turn; the caller judges its meaning and adequacy. See [configuration and dependencies](README.md).

An installed host-specific provenance owner, such as `cloud-local-workflow`,
may retain surrounding task evidence. It is optional, is not distributed in this
collection, and is never required to use this relay. Without it, the caller's
existing task records retain that provenance and first-request reconciliation.

## Freeze the ready exchange

This relay never creates or selects a destination. Before outbound mutation,
require and freeze:

- `exchange_id`;
- exact conversation identity plus caller-supplied target mode and readiness
  evidence;
- exact request bytes and SHA-256;
- latest observed remote turn boundary or explicit absence boundary; and
- the current operation constraint, if any.

A caller may attach task, creation, Project-instruction, checkpoint,
model-selection, source, or object provenance as receipt annotations; the relay
parses only the required exchange fields above. Reject an unready, missing,
guessed, substituted, or mode-ambiguous target, a mutable or digest-mismatched
request, and destination discovery. Titles, recency, similar questions, former
Project membership, and a URL without retained binding cannot identify the
target. Creation or first submission before a conversation ID exists belongs
to the caller's binding route.

## Immutable transport evidence

Resolve a task-owned private storage location from the consumer before writing.
Keep requests, responses, receipts, account bindings and continuation notes outside
public packages, plugin caches and public repositories. Store only the evidence
needed for this exchange under the actual data and retention authority. This
package supplies no personal account, conversation, profile or storage binding.

Before any mutation, write the exact frozen request to an immutable file and
verify its SHA-256.

After one exact response is bound, write one immutable JSON receipt containing
exchange ID, conversation identity and target-mode evidence, request and
response paths/digests, remote user/assistant turn identities, operation-adapter
evidence, acknowledgement/in-flight reconciliation evidence, and Browser
cleanup or release evidence when applicable. Verify and return the receipt path
and SHA-256. The caller binds that receipt through its existing task handoff. No
second transport ledger is required.

## ChatGPT operation adapters

For each observation or mutation operation, select the smallest currently
capable adapter that can address the frozen exact target and return evidence
required for that operation. Native task/thread and controlled Browser are both
eligible when their current exact-target evidence and owner constraints permit
the operation. Select the carrier from current host policy, actual capabilities,
and the operation's needs while retaining the frozen target binding.
Both retain the ready-binding requirements above. Browser never bypasses a
missing native authorization or tool boundary.

For an exact ChatGPT advisory conversation, use a native `codex_app` adapter
when the current host actually exposes that callable tool and its exact target
binding is available. Inspect the currently callable schema and its target semantics first. For example,
a host exposing this binding through `functions.exec` can read it with:

```js
const observed = await tools.mcp__codex_app__read_thread({
  threadId: exact_conversation_id,
  turnLimit: 20,
});
```

Use `tools.mcp__codex_app__send_message_to_thread` only for a selected, actually
authorized mutation operation and only with that exact `threadId`. Its current
schema and authorization contract govern whether and how that operation is allowed;
a readable native target does not establish send authority. Resolve deferred tools through
the current host's supported discovery. A name in this example does not establish
availability. Use integrations supported and authorized by the recipient’s current host;
do not infer a usable adapter from a tool name.
If the native operation is unavailable, use an already permitted
controlled carrier or report that operation's concrete capability limit.
For a Browser operation, follow the selected controlled
carrier's owning instructions and pass exact destination, operation (`observe` or `submit`),
frozen payload for `submit`, prior boundary, and lifecycle requirement. Read and
use `browser-relay` only when that is the selected carrier. Browser returns
physical observations and cleanup evidence only. The relay decides semantic
turn binding, completion, waiting, and retry. Never persist a current task's
transient browser/provider ID as general Skill policy.

## First submission and interrupted continuation

Conversation creation and a first request sent by another owner precede this
relay. Require its retained exact conversation binding, frozen request and last
known attempt evidence. Reconcile that first submission before any follow-up or
retry: if accepted, recover its matching user turn and response or continue waiting;
if acceptance is uncertain, retain that uncertainty without sending again. Never
recreate a conversation or repeat a first request to discover what happened.

After interruption, restore the same exchange ID, request bytes and digest, exact
target, prior ordered-turn boundary, acknowledgement and resend history, last
observation, and pending wait decision from the caller's continuity. Observe the
same target before the next mutation. Missing evidence is an unresolved boundary,
not permission to reset attempt counts, adopt a nearby conversation or assume the
request was never sent. Native and Browser observation can reconcile each other
only when both establish that same target and ordered exchange.

## One exact conversation exchange

1. Verify the request digest immediately before a mutation attempt and
   reconcile the latest ordered turn through any capable observation adapter.
   If the request may already exist, bind its latest attempt before deciding
   whether to wait or retry.
2. Retain each operation-adapter identity in `transport_evidence`. Observation
   never submits or resends. Before another mutation after any adapter may have
   changed the target, reconcile ordered turns again.
3. If the target reports running or paused, use the discrete waiting policy
   below before observing again. Otherwise
   submit exact frozen bytes without translation, normalization, summarization,
   wrapping, or explanation. Keep at most one mutation attempt in flight.
4. Any successful return from the selected mutation operation counts as
   submission acknowledgement, even when it contains only target identity and
   no remote turn identity, unless the adapter explicitly reports
   non-acceptance or error. After acknowledgement, keep that attempt in flight
   until the matching request/response turn becomes observable or the adapter
   supplies explicit evidence that no submission was accepted. An idle target or
   temporarily absent matching turn is observation lag, not resend eligibility.
   If acknowledgement cannot be reconciled, return the uncertain transport
   boundary rather than resend.
5. A same-target exact resend is eligible only after explicit non-acceptance
   evidence or after an observable matching request turn is followed, after
   reconciliation, by a terminal or idle non-running target with no complete
   assistant response, including a missing, interrupted, or truncated response.
   Permit at most one exact resend for that observable terminal-response
   boundary. Preserve exchange, target, `chat_creation_id`, and request digest.
   Identity, authentication, challenge, consent, safety, ownership, digest, or
   cleanup failure stops without substitution.
6. Retain the exact response and evidence in the same calling-model turn, write
   and verify the immutable receipt defined above, and return its path and digest.
   Browser cleanup or release readback belongs in `cleanup_evidence`.

## Discrete waiting for Web generation

After submission reconciliation establishes an accepted request still generating,
choose when to check again from the observed progress, elapsed time, expected
remaining work, and the cost of noticing completion later. Estimate when another
observation is likely to be useful, balancing response latency against local
model usage. Reassess after each due observation: evidence of nearing completion
can justify a shorter wait; substantial remaining work or little change can
justify a longer one. Do not prescribe a fixed interval, initial sequence, or
backoff ladder. Treat unavailable progress as uncertainty, not an invented
percentage or a reason for rapid polling. This applies to advisory heavy work
and Web behavior evaluations after Prompt or Skill edits alike. Initial submission
reconciliation and an explicit user request to inspect now are separate from
routine generation checks; an actual completion or error event can be handled
when delivered.

Between checks, let the host's supported passive wait or deferred wake-up carry
the time, or continue independent useful work. Preserve the exact conversation,
request/turn binding, last observation and its time, progress estimate with its
uncertainty, and chosen next check time with a brief reason before yielding.
Use existing task continuity or a small task-owned temporary note; update it
after each check rather than creating a separate durable ledger. This note
retains the waiting decision but does not itself schedule execution.
Use the host's current scheduling and continuation contract; verify any scheduled
wake-up before relying on it. A short tool timeout
does not make another conversation read due. Avoid repeated screenshots, thread
reads, refreshes, short model/tool polling loops, or ongoing reasoning merely to
occupy the interval. Do not introduce a custom watcher or daemon. If no supported
continuation can carry the wait, report that concrete limitation and retained
pending exchange rather than pretending a future check is scheduled.

At the due check, read the smallest evidence needed to distinguish running,
complete, and actionable failure. While still running, retain the same request
and choose the next useful check from the new evidence; elapsed time alone never
justifies resubmission, restart, or a duplicate evaluation. On completion, consume
and bind the response;
on an actionable failure, follow the existing reconciliation and retry boundary.
Retire any task-owned wake-up when its exchange is complete or cancelled.

## Result package

```text
exchange_id
target_identity
target_mode_evidence
request_path
request_sha256
response_path
remote_user_turn_id
remote_assistant_turn_id
remote_assistant_text
remote_assistant_sha256
transport_evidence
cleanup_evidence
receipt_path
receipt_sha256
```

Return the strongest observed transport evidence and exact missing proof. The
caller decides whether to retain, evaluate, forward, reject, or follow up on
the answer; the result package carries no semantic-success or task-completion
judgment.
