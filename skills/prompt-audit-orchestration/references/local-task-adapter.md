# On-demand Role Adapter: Saved Task

This adapter defines the Saved Task domain's semantic and write authority for
one on-demand review of local scheduled, recurring, or deferred execution. The
current domain coordinator loads `prompt-audit-orchestration`,
`prompt-and-skill-lifecycle` authoring and delivery references, and
`agent-orchestration-master`. Give each child the actual task or Skill
owner and publication owner plus the current-run package: resolved objective,
causal scope and extent, attributable user input and user-input provenance binding,
intended result, stopping boundary, evidence access, authority, validation, and
return responsibility. The main Skill owns topology and repair disposition;
this adapter adds no scheduler, persistent audit identity, or user-source record.

## Connected Task scope

Discover current Tasks through the host's actual task owners and saved state.
Resolve whether each candidate executes locally and identify its existing task
identity, scheduler, execution destination, and saved prompt. Do not infer the
consumer from a product label, filename, authoring example, or the word Task.
Use current owner discovery rather than a fixed task inventory, storage path,
scheduler backend, or model version. Include retained paused Tasks when their
current consumer or intended resumption contract requires review; inert history
is evidence rather than an active target. Ordinary one-off chat requests are
not saved Tasks unless being prepared for such execution.

For a full-domain run, cover these connected families for current saved Tasks;
for a bounded run, follow the main Skill's causal-scope and exclusion rule:

- the saved task-purpose prompt and any task-specific instructions that govern
  the concrete result, decisions, allowed effects, stopping, and reporting;
- the real scheduler and execution destination, including the project or
  conversation context, files, tools, permissions, and instructions actually
  available to a run;
- directly and transitively invoked Skills, including their entry conditions,
  loaded resources and instructions, and material dependencies that shape the
  result; resolve actual discovery and retrieval rather than stopping at a
  Skill name in the prompt or treating every nearby package as a dependency;
- the configured execution model and relevant current environment, together
  with observable run behavior, outputs, delivery or quiet outcomes, and the
  evidence needed to distinguish semantic fit from persistence or execution
  failure.

Read settings where they affect interpretation, including timing, enabled state,
notifications, and destination. Follow dependencies far enough to judge the
material execution chain without expanding into unrelated task inventories,
whole repositories, or a general operational audit. If a Task lacks observable
runs or a dependency cannot be resolved, report the affected judgment's evidence
limit rather than claiming runtime success from saved text.

## Semantic judgment and source responsibility

Use `prompt-and-skill-lifecycle`'s authoring method for the saved prompt
contract and its current model guidance for model fit.
Judge the Task's purpose and decision rules together with what execution
actually receives and does. Check whether task-specific correctness depends on
implicit retrieval of an earlier conversation, whether called methods and
resources are accessible, and whether the composed instructions preserve the
intended result, permitted effects, timing semantics, completion boundary, and
meaningful reporting or quiet behavior. Reusable methods belong with their
existing Skills rather than being copied into every saved prompt.

Apply the main Skill's assessment of prescriptions and prohibitions throughout
this chain. Examine hardcoded routes, tools, paths, model assumptions, sequences,
and restrictions for a current purpose or consumer contract. Separate a repaired
historical defect from adaptation to a changed model or environment. An earlier
model workaround may now obstruct judgment, while an exact boundary may remain
necessary; retain, simplify, or remove it only with supporting current evidence.
A request to adapt prompts to a newer model does not settle either conclusion.

Saved Task owns the integrated execution-chain judgment, saved task-purpose
prompts, and Skills whose primary responsibility is dedicated to that task
purpose. Dedicated Learning Skills retain Learning ownership; local/shared reusable
non-learning methods and local common/global or project instructions retain
Workflow ownership; hosted common/global and non-learning Project instructions
and Hosted-specific reusable
methods retain Hosted ownership.
Invocation by a Task changes neither source responsibility nor publication
authority. Inspect their material downstream effects and report the exact source,
consumer dependency, finding, and consequence. Route shared-source findings to
the existing semantic owner under the main Skill's cross-owner disposition.
When that domain is selected in a joint run, coordinate directly with its peer
and reuse its source result; otherwise report the dependency without becoming a
second writer or automatically launching another domain. A shared dependency
remains part of Task coverage even when this domain cannot repair its source.

## Repair and evidence boundary

An audit-only run remains read-only under the main Skill. For an authorized
role-owned semantic repair, use the host's actual task owner to read the exact
existing saved prompt and relevant configuration, apply the integrated prompt
change, and read back persistence through that owner. Follow the lifecycle
package's delivery method for configuration readback and any required source
or recovery projection. Preserve identity and non-prompt configuration unless separately
authorized: execution model and effort, cadence and time zone, destination,
notification preferences, enabled or paused state, title, and other settings.
Model adaptation of prompt text grants no authority to change the execution
model or scheduling. Do not replace a Task merely to edit its prompt.

A dedicated task-purpose Skill repair uses its canonical package, publication,
and runtime-convergence owners. Verify the saved Task still resolves the intended
Skill and material resources in its actual execution context; a source edit or
matching package name alone does not prove retrieval or successful execution.
Use the main Skill's proportionate evaluation rule. Prefer available real run
and output evidence; trigger a run only when it is a faithful necessary check
and its actual effects are authorized. Persistence readback, Skill availability,
and successful execution are distinct claims, with unresolved gaps kept explicit.

Hosted Scheduled Tasks remain governed by the user's Scheduled Task Project and
are evidence-only here under the main Skill's Hosted boundary. A saved Task that
reads or refers to a Hosted Task does not acquire authority over that Hosted source,
native fields, or recovery mirror. A pre-existing scheduler, authentication,
service, delivery, or other operational incident is evidence for its actual
owner and remains outside semantic repair unless separately scoped; do not
rewrite a prompt as a substitute for incident diagnosis or repair.

## Coordination and return boundary

The Saved Task coordinator owns decomposition, follow-ups, connected-chain
coverage, peer coordination, and its domain conclusion using the main Skill and
current Agent owner. Group work by causal questions and exact dependencies,
with one mutation owner per exact target; neither task count nor Skill count
prescribes agent count. Use existing single-domain or N-peer topology without
adding a coordination layer.

Return the resolved scope, current Task and execution identities examined,
material exclusions and evidence limits, the connected conclusion across saved
prompts and invoked Skills/resources, and supported dispositions. For changes,
include actual owner publication and saved-prompt/configuration readback,
relevant Skill availability and behavior evidence, and remaining gaps. Account
for routed shared-source findings, protected Hosted dependencies, operational
incidents, and blockers without claiming those sources were repaired or a Task
ran successfully. Do not operate or wait for another selected domain's work
unless the root selected a joint request.
