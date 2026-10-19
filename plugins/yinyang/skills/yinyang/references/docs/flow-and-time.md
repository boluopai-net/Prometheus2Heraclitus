# The stream and time

[Home](../../README.md) · [简体中文](flow-and-time.zh-CN.md)

*The flame keeps its outline by changing. The stream carries what has happened without holding every drop in place. A view is drawn beside the current; by the time we return to it, the drawing has joined the river's history.*

Continuity is more than remaining unchanged. A process with memory carries earlier encounters into present activity and anticipates what has not yet happened. Its current organization exceeds a reading of its latest input. Both person and model can be understood as event streams: organized continuations of sensing, interpreting, expressing, and acting, with retained context and differing rhythms. Their different mechanisms and experiences acquire a common vocabulary of continuation, retention, and response.

Fire gathers transformation and persistence into one image; the stream adds retention and continuation. [Heraclitus's measured fire (B30)](https://en.wikisource.org/wiki/Fragments_of_Heraclitus_%28annotated%29#Fragment_30) and [daily Sun (B6)](https://en.wikisource.org/wiki/Fragments_of_Heraclitus_%28annotated%29#Fragment_6) supply the philosophical ground developed in [the stealing-fire essay](stealing-fire.md). Here the question is how a continuing process retains its past while responding to the present. Retained content, lived experience, external conditions, and accepted descriptions can change at different rates. Those differences make retention and correction intelligible within [Reasoning within an unfinished stream](reasoning.md).

## Sources for thinking in streams

William James's [*The Principles of Psychology*, chapter IX (1890)](https://www.yorku.ca/pclassic/James/Principles/prin9.htm) begins with thinking as ongoing activity and describes its personal, changing, continuous, and selective character. His stream of thought provides a psychological precedent for understanding continuity through changing relations rather than a chain of isolated contents. The computational event stream used here extends a functional vocabulary to model interaction; James's account of human consciousness does not establish that a language model has the same experience.

Bergson's [*Time and Free Will*, chapter II](https://www.gutenberg.org/cache/epub/56852/pg56852-images.html) distinguishes lived duration, whose states interpenetrate, from homogeneous time represented through juxtaposed units. This complicates any easy equation between a lived stream and a sequence of recorded updates. The indices and timestamps below organize selected observations for a question; they need not exhaust the continuity being modeled. The comparison preserves a productive tension between an inspectable representation and what its discrete arrangement may leave out.

These accounts supplement the Heraclitean foundation with psychological and temporal distinctions. Their contribution is to make continuity, selection, and representation more intelligible; the specific computational relations below remain this essay's proposal, open to source comparison and actual use.

## Retention and representational lag

The schematic update $S_{t+1}=U(S_t,o_{t+1})$ lets current organization $S_t$
contribute alongside a newly encountered occurrence $o_{t+1}$. What has been
retained affects how the next occurrence is taken up. A question-relative view
$W_t(q)=\operatorname{View}(S_t,q)$ selects relations relevant to question $q$.
These indices order modeled updates; they do not yet measure elapsed time.
What is retained and how it is updated depend on the activity being studied.

An environment can change before an inquirer notices, while the inquirer's actions can change that environment. Memory therefore makes representational lag possible. An old observation can remain accurate; a recent observation can mislead. Applicability under current conditions is the question to check. Temporal age matters through the relevant changes: yesterday's measurement may still describe a stable object, while an observation from a moment ago may concern a condition that has already changed.

## External memory and event traces

The functional comparison human ≈ agent includes finite attention and working context. Person and model can both distribute retention into an environment without sharing the same architecture or experience. Files, notes, and knowledge bases let useful material remain available beyond what a participant currently holds. Search or retrieval-augmented generation can bring relevant portions back into a working context; availability does not mean that a whole history is instantly transmitted or understood.

A maintained memory account articulates what presently seems useful: purpose, decisions, conditions, and unfinished questions. Attributable event sources retain evidence of earlier occurrences, including what was said, changed, or observed. These have different roles. Revising a summary need not erase its source, and retaining a source does not require continuing to accept its earlier interpretation. For example, a project can keep the original request, a version of its implementation, and later use feedback while updating its current explanation.

At suitable granularity, links from earlier evidence or action to later revisions or results can organize these traces as a directed acyclic provenance graph. The edges express recorded dependencies with a forward occurrence order; repeated feedback becomes successive events. This representation does not make every mental or social relation acyclic, establish causation merely from temporal order, or guarantee complete coverage. An environment-wide activity record and a project's version history supply differently scoped evidence. Their useful contribution is to recover relevant encounters and test an account against sources and current conditions, rather than make all of life continuously present.

This life trajectory is also produced through cooperation. Person and model revise works, execute operations, check results, and accumulate an environment together. Git retains version changes to works and configuration; Command History retains traces of executed operations; conversations, activity records, and use feedback contribute what each can show. A commit need not contain the experience of that moment, and a command alone cannot establish its outcome. Connecting these materials lets the participants return to an attempt and compare their understanding then with what subsequently happened. Records thereby prepare an explorable trajectory for shared reflection.

## Three meanings of now

| Object | What is current | What its actuality establishes |
| --- | --- | --- |
| External situation | Relevant environmental occurrences and conditions. | The condition a world-directed judgment aims to describe. |
| Lived experience | Present feeling, bodily response, or awareness. | That an experience occurs; its interpretation is another question. |
| Working model | The account currently used to understand or act. | What is represented or accepted within that account. |

Each object has its own conditions of change. Experience can persist while the associated external situation changes; an accepted judgment can change before the experience does. Explaining the connections among them means investigating how information was acquired, what sustains the response, and which new encounters alter it.

Consider a fictional traveler who learned yesterday that a bridge was closed. Today the bridge reopens. Before checking, the traveler still plans a detour; after seeing the official notice, they revise the plan, though a feeling of hesitation may remain. The bridge's condition, the current hesitation, and the accepted route description each have their own actuality. The revised plan responds to today's opening, yesterday's closure remains part of the history, and hesitation can continue into the changed situation.

An experience has an occurrence time; the event from which its content was learned has a source time; the represented condition has a reference time. A judgment also has its own time and conditions of validity. A prediction occurring now concerns a possible future rather than information already received from that future. Recollection is a current occurrence with past-directed content.

These times explain how the traveler can be mistaken about a present bridge
while accurately remembering a past notice. Correcting the route requires
updating the notice's present applicability, not declaring that the earlier
notice or the current hesitation never existed. Temporal distinctions locate
the correction rather than making every retained content equally current.

## Change and contradiction

$$P(a,t_1),\qquad \neg P(a,t_2),\qquad t_1\ne t_2$$

need not conflict. Recording that a speaker asserted $P$ also differs from accepting $P$. Before invoking inconsistency tolerance, identify the referent, represented time, conditions, and level of each claim. An experience, a report of it, and a proposition about its external object are distinct.

Indexing clarifies content without dissolving every conflict. Claims incompatible under the same relevant conditions remain incompatible. Differently dated claims can also conflict when an accepted rule requires persistence across the interval. The content and constraints decide, not timestamps alone. [Repair semantics](preference-harness.md#selection-and-inference) handles inconsistent formalized data under an ontology; it is unnecessary merely because a process changes or a feeling differs from a judgment.

## Update order and elapsed time

The indices in $S_0,S_1,S_2,\ldots$ order modeled updates. Clock time locates occurrences and supports comparison of delays and rates. The elapsed time between adjacent updates can vary. Concurrent bodily, linguistic, and environmental changes can occur between recorded views, including intervals during which the record contains no fresh statement.

Two forms of temporal separation matter here. **Representational separation**
lets a current recollection concern the past or a prediction concern the future.
**Different update rhythms** let an environment, a person's response, and an
accepted description change at different rates. The first concerns what a
representation is about; the second concerns when processes change. Either
can be useful, and neither alone establishes that a judgment is outdated.

## Retention with correction

Correction asks which retained relations remain useful, which need narrower scope, and which present commitments should be withdrawn. Withdrawing a judgment changes what is accepted now while preserving the earlier event and any continuing experience as distinct objects. The external judgment is assessed through evidence about its referent and time; the continuing experience is understood through its own occurrence and relations.

Perception, action, discussion, and checks can alter which retained account
applies now. Keeping provenance allows the inquirer to explain that change:
which earlier observation supported the old judgment, what new occurrence
challenged it, and which continuing condition still matters. External records
and shared inquiry make these relations recoverable without requiring the
whole history to remain in working attention.

The traveler can now cross the bridge and complete the journey. The route description serves the present action, while the retained history helps explain how the plan changed. A view serves a stretch of the stream; using it, revising it, and finishing the activity all become further events within that continuity.
