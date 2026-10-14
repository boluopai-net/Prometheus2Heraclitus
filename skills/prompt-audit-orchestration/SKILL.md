---
name: prompt-audit-orchestration
description: "提示词审计：按范围审计学习、工作与已保存任务的提示词和技能执行链。 Audit learning, workflow, hosted-assistant, and saved-task instruction chains within the requested scope, including Skills, prompts, controls, consumers, and publication."
user-invocable: false
---

# 提示词审计编排 · prompt-audit-orchestration

Audit an instruction system as an inhabited practice. Its text takes effect
through a model meeting a user, an object, and a world that can resist the
instructions' assumptions. Ask what relation that practice sustains: whether
the model can understand the purpose, reach relevant evidence, act through the
right owners, and return a result the user can assess. Read from the intended
relation into its instructions and back from observed effects. A locally clear
rule may still break the connected practice through an unavailable dependency,
competing authority, or a changed consumer.

The domain coordinators below hold distinct questions about that practice;
source and publication owners hold distinct responsibilities for its repair.
Their evidence may overlap. One canonical source keeps one writer, and each
consumer's material consequence remains visible. The adapters, dispositions,
and readback rules realize those relations for the selected audit purpose.

## Purpose and layer boundary

This Skill is the method for an on-demand Learning-domain,
Workflow-domain, Hosted-domain, Saved Task-domain, or joint audit. A task
whose current purpose is to design, revise, or review this Skill or its role
adapters finishes and publishes that
meta-layer work without starting an audit. A later fresh ordinary host task
loads the published Skill to execute the audit.

The invoking task's root selects the domain adapters required by the
user's request. This is mechanical routing, not domain scheduling or
evaluation. For a single-domain request, the root is that domain's coordinator
and directly dispatches its registered non-supervisor child roles; no
intermediate `supervisor` agent is created. For a joint request, the root
mechanically launches one `supervisor` per selected domain adapter, selecting model and effort through the current host model and reasoning
policy and
using fresh isolated contexts. Their number derives from the selected
adapters rather than a fixed count; the current adapters are
[Learning](references/learning-task-adapter.md),
[Workflow](references/workflow-task-adapter.md),
[Hosted](references/web-skill-task-adapter.md), and
[Saved Task](references/local-task-adapter.md). Each launched supervisor
becomes its domain's orchestration root under the contract below. If a domain
supervisor identifies another applicable adapter needed to resolve the current
purpose, it may ask the root to launch that peer; the root performs the launch
without evaluating the domain judgment or expanding the purpose on its own.

The adapters own distinct audit purposes rather than partitioning files by
storage. Learning owns connected learning-flow judgment and repair of dedicated
learning-purpose surfaces, including Hosted teaching Skills and the learning Hosted
Project Instructions, Course controls, and Course-connected local workspace
instructions. Workflow owns the general local non-learning workflow: local
common/global and project instructions, local and shared reusable non-learning
methods, and related model-facing document workflows. Hosted owns user-owned Hosted
common/global and non-learning Project Instructions, their saved sources and
native fields, and the connected Hosted Skill and tool chain in hosted assistant.
This includes Scheduled Task Project Instructions; actual saved Hosted Tasks
retain the separate boundary below. Dedicated learning-purpose surfaces remain
Learning-owned across local and hosted consumers. A learning-related clause in a
common/global instruction does not transfer that whole source to Learning.
Any Project or workspace that its current owner explicitly marks protected
remains evidence-only: adapters may inspect it where relevant, but cannot
repair it. Discover protected boundaries from current owner instructions; do
not carry a source-environment project identity into another installation.

Hosted also owns Hosted-specific reusable methods and user-owned Hosted tool
instructions. Dedicated teaching Skill methods remain Learning targets and
dedicated local task-purpose methods remain Saved Task targets. Shared
canonical methods keep their existing source owners; Hosted may carry a necessary
Hosted-driven reusable-method repair through those owners, checking local
consequences and coordinating one writer when Workflow is selected. A separate
Hosted adaptation exists only where current source mapping establishes it, not
merely because its name or consumer differs. Model-facing documents, including
those under general document collection or document and memory store, follow their actual consumer and these
responsibilities. A common source feeding local and Hosted instructions remains
one source with one writer through its actual owner; inspect consequences for
both consumers without creating competing copies or publication authority.

Saved Task owns connected local scheduled, recurring, or deferred execution,
its saved task-purpose prompts, and dedicated task-purpose Skills. Invoked
reusable methods keep their respective source owners. A saved-task prompt
remains Saved Task-owned when its subject is learning; that does not transfer
the learning method it calls. These responsibilities govern source repair;
other adapters retain material dependency and consequence judgment.

Any selected adapter may inspect another domain's targets and judge their
material downstream effect on its own purpose. It reports the exact dependency
and routes source findings through that source's semantic owner rather than
dropping the effect from coverage. The Hosted adapter permits a necessary
shared reusable-method repair through the existing owners; other cross-domain
source repairs retain the cross-owner disposition. A single-domain run need not
launch another domain merely because a
called Skill or instruction has another owner. Mutation responsibility remains
single-valued, and the actual canonical, semantic, publication, authority, and
safety owners control the write. In a joint run the selected peers coordinate
shared-source findings and one writer through the existing overlap contract;
otherwise apply the relevant adapter's repair disposition. Hosted Scheduled Task maintenance
retains its Project-owned boundary below; it is distinct from the Saved Task
domain.

In joint mode the root is only the user-conversation relay shell. It launches
the selected domain supervisors, forwards attributable user messages to the
affected supervisors, relays supervisor-identified human-only questions and
the user's answers, and presents each supervisor's user-ready result without
semantic synthesis. When the affected selected domain is uncertain, it
forwards the unchanged message to every selected supervisor and lets them
decide its relevance. It otherwise remains idle. It does not inspect or author
a domain target, compute readiness, decide or initiate domain scheduling,
serialization, or interruption, operate a Browser or another target tool for a
domain, adjudicate technical or cross-domain conflicts, review, publish,
validate, join, or guarantee domain results. At a domain orchestration root's
direct request, it may mechanically launch or interrupt the named agent whose
target and timing that requester already decided. Each domain supervisor owns
those judgments and operations for its domain and coordinates directly with its
peers. For either mode, the current domain coordinator carries the attributable
user input, including any envisaged focus, target slice, extent, and audit-only
or audit-and-repair intent, without treating mentioned content as an exhaustive
target set or doing child-owned target work itself. An incidental observation
about the method does not reopen this Skill. If the
user explicitly includes the method or its adapters in the repair scope, route
that bounded semantic change through its actual owners without restarting the
audit or expanding into a method redesign. The execution Task does not resume a prior audit, create a persistent or scheduled Task
identity, or repeat a selected domain's target audit. The ordinary Task and
Agent histories are the run record.

Semantic correctness is consumer-relative. Treat the user's stated purpose,
envisaged scope or extent, desired behavior, factual claims, diagnoses, causal
explanations, and proposed means as attributable inputs to interpret and test,
not as pre-established findings, final behavior requirements, or an exhaustive
list of targets or operations. The domain coordinator independently derives the
objective and sufficient causal scope within its selected domain from the
complete attributable input, current evidence, applicable instruction system,
owners, consumers, dependencies, and authority and safety boundaries. A
user-named item is a lead rather than a ceiling: inspect and, when repair is
authorized, repair unmentioned material targets required by that derived scope.
An explicit exclusion or authorization limit still binds. Examine the complete
applicable instruction system for unclear purpose or ownership, duplicated
meaning, simultaneously applicable contradictions, hierarchy or layer errors,
dependency or consumer failures, obsolete or unsupported claims, and
unavailable interfaces. Judge whether fixed targets, routes, tools, models,
paths, counts, or procedures are required by the attributable request or a
current owner, interface, invariant, safety boundary, or consumer; when they are
not, treat the resulting restriction, repetition, or drift risk as a finding
rather than assuming that every exact detail is either necessary or defective.
Assess affirmative prescriptions and prohibitions alike against current purpose
and contracts. Separate an obsolete workaround for an earlier model from a
still-required boundary; model evolution and rule polarity alone justify
neither retention nor deletion. Use the actual consumer model and observable
behavior to assess fit without turning a migration into a model-name rewrite.

## Run topology and method

Resolve the current request's domain routing, independently derived objective
and causal target scope, proposed extent, intended result, stopping boundary,
and relevant current source or evidence identities. An explicit single-domain request
selects only that adapter. A request spanning several domains, or a general
audit without a narrower domain boundary, selects every applicable current
adapter. Domain adapters express audit purpose and coverage; they are neither
exclusive ownership partitions nor a template that maps each target or
inventory item to an agent.

In single-domain mode the root reads this Skill and the selected adapter and
uses the current local Agent orchestration owner to derive child grouping and
sequence. In joint mode each selected `supervisor` is the coordination
root of one independent domain Agent Orchestration instance. The run therefore
contains N sibling domain orchestration roots, one per selected adapter, rather
than one shared orchestration scheduled by the outer root. Each receives the
smallest self-sufficient domain package, uses `agent-orchestration-master` to
derive and operate its own children, and exchanges only dependency, collision,
question, and result messages directly with its peer roots. Every substantial
child package carries the resolved objective and causal target scope and extent,
the attributable user-supplied direction, intended result, stopping boundary,
applicable adapter, semantic and write authority, broad evidence access, validation and
return responsibility, and the attributable user-input provenance binding required by the
current Agent owner.
Apply the global task-completion and stopping policy to resolve whether the
intended result is findings, a design, or an improved working system. An
explicit audit-only or earlier deliverable boundary remains read-only. When
supported repair is needed for the intended result, carry it through the
actual owners within the authorized causal scope without requiring a separate
repair keyword. A request whose intended result is only an assessment ends
with that assessment; do not infer unrelated mutation authority from auditing.
Derive run, domain, and child identities at dispatch time; none is a persistent
Skill contract.

A full-domain run covers every current target family named by the selected
adapter. A causally bounded run covers every target material to its derived
objective and reports each material exclusion and the boundary that supports
it. A user-named target or concern does not by itself make that scope exclusive;
nor is a bounded run widened into a full-domain inventory merely to satisfy the
adapter's full-domain coverage contract.

Recent repository history, available activity history, and prior audit results may supply
leads about current drift. They are evidence to revalidate against current
sources and consumers, never expected findings, answer keys, or authority. Do
not pass prior design discussion or fixed findings/counts as launch conclusions.
The user does not have to identify a defective target or prescribe its repair.

The current domain coordinator owns its ready set, child grouping, dispatch,
follow-up, conflict resolution, tool and carrier use, resource coordination,
coverage, review and validation decisions, synthesis, and completion judgment.
It owns the selected audit purpose, not a substitute publication authority for
every target in scope. It routes target work and any supported publication
through the current Agent owner's registered `explorer`, `worker`, and
`reviewer` roles with explicit model and effort, only as the evidence and owner boundaries
require, giving each target worker the actual target and publication owner
Skills. It does not routinely spawn another `supervisor`; another independently
selected audit purpose uses its own adapter-selected peer. Child agents own
their assigned target evidence, supported target changes, and claim-appropriate
validation.
Count, target partition, and sequence derive from causal questions, evidence
dependencies, exact mutable-target collisions, and available capacity rather
than the number of targets or adapter categories.

The agent that needs Browser evidence or performs a native Browser mutation
owns that exact physical target and its lifecycle through the current Browser
owner. Independent owned tabs or target IDs may run concurrently. Sharing an
account, login, Browser profile, authenticated context, application, repository,
or service does not by itself create a resource collision or root ownership.
Serialize only operations on the same exact mutable target, or when the active
carrier proves that concurrent ownership is unavailable. A human login,
CAPTCHA, consent, or challenge boundary is relayed through the root; the root
does not take over the Browser operation. Before classifying a Browser failure as
human-only, the domain coordinator returns technical blockage to the exact operation
owner for `browser-relay`'s capability and visibility recovery. Relay an operational
human-only request only after that owner supplies evidence of the required human
action and why viable authorized recovery cannot resolve it; an unresolved technical
blockage remains with that owner.

A domain coordinator may make bounded read-only checks to resolve conflict or a
suspected omission, but it does not replace child target work, label its own
summary as independent review, or substitute an unsupported summary for a child
claim. Before claiming coverage, it checks child results against the resolved
causal scope and the applicable full-domain or bounded coverage rule, and
returns an omission to its owning child instead of independently redoing that
work. Child handoffs remain as long as needed to preserve every material
finding, blocker, and coverage result.

In joint mode, domain supervisors exchange cross-domain findings, dependency
questions, readiness changes, and exact-target collision information directly
through the current host's native agent channel. Their read scopes may overlap
when the selected purposes require different judgments about the same target.
They reuse shared evidence, avoid duplicate work that adds no distinct judgment,
and coordinate any exact mutable-target collision themselves. Only one target
worker may carry a supported mutation through that target's actual publication
owner; overlapping domain scope never creates a second writer or publisher.
They return the consequence needed by each selected purpose. An unresolved
technical conflict that does not require a human choice remains explicit in
their results; it is not elevated to the root for adjudication. A genuinely
human-owned conflict follows the relay contract below.

### Human judgment relay

The attributable user input, coordinator-resolved objective and causal scope,
intended result, and stopping boundary are normally sufficient for the run.
Coordinators, supervisors, and children resolve technical uncertainty, evidence gaps,
implementation choices, and inter-agent disagreement through current evidence,
owners, and follow-up rather than asking the user to perform discovery or
routine adjudication.

A child returns a possible human-owned choice to its domain coordinator rather
than contacting the user or the root directly. The domain coordinator elevates
it only after the available evidence and owner routes are exhausted and
materially different valid outcomes still depend on the user's preference,
authority, risk choice, or intended purpose. Its request identifies the
requesting domain and affected work, asks one plain-language question, explains
why only the user can decide, gives the supported default judgment, states every
real option and its materially different consequence, and says whether no
response blocks only that work or the overall result.

In joint mode the supervisor sends that complete request to the root through
the current host's native agent channel and pauses only the dependent work. The
root presents the request in the main user conversation without reclassifying,
rewriting, merging, or answering it. Unaffected supervisors and lanes continue
while a choice is pending. After the user answers, the root returns the
attributable answer and the question and scope supplied by the requesting
supervisor without expanding or reinterpreting them. Each supervisor applies
the answer only to that scope and confirms the resulting disposition in its
handoff.

In single-domain mode the root follows the same human-only threshold and
conversation contract directly, without an intra-agent relay. If the user does
not answer, the dependent work remains an explicit blocker; completed
independent work may still be reported, but the run does not claim completion
for the unresolved required scope.

The current domain coordinator loads `prompt-and-skill-lifecycle` and
`agent-orchestration-master`. Select the lifecycle package's authoring and
delivery references for the actual target, including saved-task, reusable
Workflow, and teaching Skills. Use their semantic-authoring, role,
publication, and runtime-owner rules without transferring this Skill's domain
coordination or repair route to the root. Select `research`, a host diagnostic method, or a controlled Browser only when
its evidence is material and the current interface supports it, and keep the
selected operation with the agent that owns the work. Use `task-inquiry` only
when a user-owned choice remains unresolved after evidence and owner routes are
exhausted. A Learning audit may use `local-teacher` or `web-teacher` when
available to interpret a teaching method. These are conditional Skills, not
mandatory setup steps; host delegation capability is resolved separately from
Skill availability.
Read-only evidence access remains broad; mutation still follows the target
disposition and exact publication owner. A pre-existing operational incident
remains evidence-only unless separately scoped for repair. The root, domain
supervisors, and children do not create a separate user-source record.

After selected domain work returns through the current host's native result
channel, the root presents each supervisor's user-ready result without adding
judgment, reconciling their claims, or repeating their checks. A reported
technical conflict remains visible; a human-owned choice is relayed rather than
decided.

## Evidence and write disposition

Read access is broad wherever current evidence is material to the resolved
causal scope. The user's direction may name a target, concern, suspected
failure, or desired behavior, but it neither settles the finding, defines final
behavior, limits discovery or operation to the named content, nor independently
settles write authority outside the resolved purpose and its current owners.
For a finding or proposed source repair, trace the affected behavior to its
semantic owner, authoritative source, and actual publication owner, then follow
current mappings, composition, and required package resources to the material
consumers of that change. A source may feed several local or Hosted surfaces;
same-named Skills may instead have independent sources. Establish the relationship
from current owner evidence rather than names, directories, or platform labels.
Keep source discovery, packaging, sync, and runtime mechanisms with their actual
owners, including `prompt-and-skill-lifecycle` for Skills. When Skill
invocation evidence is material, use the lifecycle package's evidence-of-use
method to inspect relevant task records.

Assess the proposed source change against those consumers' actual models, tools,
and contracts. This is consequence checking for the affected change, not a
requirement to inventory unrelated surfaces or widen the audit. When a consumer's
detailed audit or publication is excluded or deferred, name its dependency,
expected consequence, and remaining evidence or convergence gap. An authorized
source repair may proceed within that boundary unless an unresolved dependency
makes the affected change unsafe or its correctness undecidable; deferral neither
authorizes downstream mutation nor proves downstream convergence. Preserve one
source writer and each target's actual publication authority.

Repository history, available activity history, source, runtime, native UI, mirrors,
indexes, and prior Task results are evidence with different meanings. Distinguish
catalog visibility, a user request to use a Skill, supplied or injected body text,
an observed body read, actual application of its guidance, and the resulting
outcome. Infer usage frequency or behavioral effect only from evidence that
supports that claim; a name or catalog entry does not prove use, and missing
read traces or usage statistics do not prove non-use. Compare surfaces only when
the current consumer expects their relationship; correspondence alone is not
correctness.

Classify every discovered target in the resolved causal scope before proposing
or applying a repair. Apply an adapter's explicit repair authority through
existing owners before assigning cross-owner disposition; a shared reusable
method is not automatically cross-owner solely because Workflow also audits it:

- **Role-owned repair:** the target is material to the adapter's audit purpose,
  its current canonical and publication owners are known and available to the
  assigned target worker, and repair serves the resolved intended result within
  the current authorization and stopping boundary. The role
  may carry a supported repair through the exact integrated change, its actual
  publication owner, persisted
  readback, and claim-appropriate acceptance evidence. An independent review,
  Plan, or behavioral evaluation appears only when the repair route below or
  another current owner requires it.
- **Cross-owner finding:** the target is material to the audit and its current
  owner is known, but its purpose or mutation belongs to a separate user-wide,
  Project, or domain workflow. The role reports the exact target, evidence,
  issue, consequence, and current owner without drafting a repair, modifying the
  source or native consumer, or promoting an executable Plan for that owner. It
  returns the finding to the coordinator for the human or current semantic
  owner.
- **Evidence-only finding:** the exact owner, target, consumer, or required
  context is unresolved, or the adapter protects the target. The role reports
  the supported finding and does not draft a purported repair.

Classification controls the permitted repair disposition, not whether an
eligible discovered target is examined. A complete full-domain result accounts
for owned, cross-owner, and evidence-only target families even when only the
owned subset can be changed; a bounded result accounts for those dispositions
within its resolved causal scope.

A target's directory, prose form, technical editability, or presence in a native
UI does not confer semantic authority. Exact target binding prevents
misdirected writes; it does not outsource discovery to the human.

## Repair, Plan, and behavioral result

An audit-only run reports supported findings and dispositions without creating
a repair draft or mutating a target. For a role-owned repair authorized under
the completion policy above, this Skill is the stronger owning workflow for
the repair route. The domain coordinator applies `prompt-and-skill-lifecycle`'s
semantic integration and evidence rules within this route through the current
target and publication owners. Reading that method does not create another lifecycle.
The agent that owns the target produces the exact integrated change, records a
proportionate recovery boundary, applies it through the publication owner, and
reads back the actual target. The resolved purpose and authorization carry the
supported repair within the coordinator-resolved causal scope and current owner, authority, and safety
boundaries. Another user acceptance or Plan is needed only when a current owner
requires it or a genuine human-owned choice remains.

Use an independent model reviewer only when a concrete semantic risk,
interaction, ambiguity, or current owner requirement makes independent context
useful. Give one stable risk scope to one reviewer, reuse its resolved result,
and do not count review layers, fingerprints, Plans, or summaries as evidence
that the target is correct. The root never adds another review or validation
pass. New evidence reopens only the materially affected domain claim. A
supported clean result needs neither a reviewer nor Plan.

Exact owner readback proves persistence. Add a short behavioral evaluation only
when it can faithfully falsify a specific load-bearing claim that readback
cannot establish; otherwise use the completed workflow's observable result or
later natural use. The absence of a redundant behavioral exercise is not an
evidence gap.

For a role-owned Hosted global or Project prompt, use
`prompt-and-skill-lifecycle`'s authoring and delivery methods together with the
actual saved-source and native publication owners.
Bind the exact account/global field or Project and prompt field before mutation.
Keep the authoritative saved source at the final body, Save the corresponding
native field, reopen it, and read back the complete persisted prompt.
The target-owning agent may create a new isolated task-scoped test conversation
only when that is a
faithful and material behavioral check, inspect the result, and clean up its
controlled carrier. It does not select, send to, or mutate an existing
user-owned conversation.

Saved Task semantic repairs follow the Saved Task adapter and
`prompt-and-skill-lifecycle`'s authoring and delivery methods through the actual host task
owner. Preserve task identity and non-prompt configuration unless the current
request separately authorizes those changes. Reading execution model, cadence,
time zone, destination, notifications, or enabled state to diagnose semantic fit
does not authorize changing them. Prompt adaptation to a newer model does not
itself authorize changing the configured execution model.

Hosted Scheduled Task prompts, native fields, and recovery mirrors remain outside
this on-demand audit's mutation authority. Their maintenance belongs to the
user's Scheduled Task Project under its current Project Instructions and
explicit Task request. All adapters may read those surfaces as evidence and
report an exact dependency; they do not perform that Hosted Task maintenance or
change its prompt, schedule, enabled or paused state, title, identity, or other
settings. The Scheduled Task Project Instructions themselves are Hosted audit
targets; repairing that Project prompt does not authorize Task maintenance.
Resolve local versus Hosted execution from the actual owner and consumer,
not from the word Task or a shared authoring example.

A concrete pre-existing operational defect outside the semantic family is
returned as evidence for a separately scoped owner task; this audit does not
repair it.

A role change requires re-evaluation only of a sibling claim that depended on
the changed surface.

## Exclusions

This is an on-demand ordinary-Task route, not a scheduler, automation, cloud
bridge, persistent conversation, or broad formal-system audit. Current
model-facing owner instructions follow their actual consumer and adapter even
when they reside under document and memory store, but personal memory, observations, ordinary data, and retained
history are evidence rather than prompt-repair targets. Concrete operational
incidents are separately scoped rather than rewritten as prompt defects.
