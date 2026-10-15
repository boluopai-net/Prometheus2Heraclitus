# A preference harness: rules and preferences working together

[Home](../../README.md) · [Core views](core-views.md#yy-10) · [简体中文](preference-harness.zh-CN.md)

A person can choose what kind of work to pursue, which possibility to develop, and what matters in the result. Such choices give inquiry a direction. Reasoning develops the possibilities within that direction; evidence lets the participants assess how the work is realized and what its consequences are. YinYang is a **preference harness** for this joint activity: it gives preferences a place alongside reasoning, judgment, and responsiveness to the world.

The model ordinarily understands and reasons through informal natural language. Purpose, examples, conversation, and the surrounding harness make a preference intelligible enough to act on. The formal comparison below brings the respective roles of selection and inference into focus; the event-stream ontology describes the broader activity in which both participants generate, choose, act, and reconsider.

The question is what preferences can select and what warrants accepting a
result. Bienvenu and Bourgaux's repair-based treatment of inconsistent data
offers a precise comparison: selecting admissible views and deciding what
follows from them are separate choices. Its distinction between a consistent
ontology and potentially inconsistent assertions also suggests a practical
orientation. Keep working concepts coherent enough to organize action while
retaining conflicting records for investigation. A conflict in the concepts
can call for revising them; a conflict between records need not destabilize
every organizing distinction. This is a natural-language practice of usable
understanding, not a claim that the collaboration has passed a formal
consistency test.

## Conflict has more than one form

Keeping a candidate available differs from accepting its claims. Psychological
conflict asks a further question: what purposes or relations does a person
struggle to hold together? Opposing wishes, an unsettled experience, and two
incompatible propositions call for different responses. Their comparison helps
explain why preserving a tension, choosing a view, and correcting a fact can
each be appropriate without being interchangeable.

Freud's [*Introductory Lectures*, Lecture XXIII](https://www.gutenberg.org/cache/epub/38219/pg38219-images.html), explains symptom formation through opposed tendencies that continue to contribute to a compromise. This historical account directs attention to what each side sustains and why a settled-looking outcome may retain conflict. It suggests a question for modeling: what is each competing arrangement trying to preserve? A knowledge-base repair instead selects a consistent assertion set under explicit assumptions; it neither diagnoses a symptom nor implements Freud's clinical theory.

Winnicott's *Playing and Reality* (1971), introduction and chapter 1, develops the transitional object's paradox of being created and encountered. He asks that this paradox be tolerated rather than prematurely resolved; see the [book](https://www.routledge.com/Playing-and-Reality/Winnicott/p/book/9780415345460) and [the introductory passage](https://www2.arnes.si/~jzaloh/bestbooks/Playing_and_reality.pdf). This offers a reason to preserve a productive tension long enough to understand its relation. It does not license accepting arbitrary contradictory factual claims. A lived paradox can lose its meaning when forced into a yes-or-no classification; a formal inconsistency still has its specified logical conditions.

Dialectical behavior therapy explicitly combines acceptance and change, rather than treating either as sufficient alone. [Behavioral Tech Institute's explanation](https://behavioraltech.org/dialectical-behavior-therapy-dbt/) describes dialectical strategies as a way to move beyond extreme positions while balancing validation and behavioral change. For collaboration, this supplies a useful comparison: understanding why an experience or arrangement makes sense can coexist with revising what happens next. The inference rules do not change merely because an experience has been acknowledged.

These sources contribute different accounts of conflict, preservation, and transformation. Their theories help articulate the questions; they do not establish this harness's effectiveness or reduce psychological processes to repair semantics. The practical proposal here is to identify the actual tension, retain its meaningful evidence and alternatives, choose a workable view, and revise it through consequences. These activities can interleave, and some tensions remain open while a finite task is completed.

## Selection and inference

The notation comes from **description logic (DL)**, a family of formal
languages for describing concepts, relations, and individuals. A **TBox** $T$
contains general axioms, such as concept inclusion and disjointness; an
**ABox** $A$ contains assertions about named individuals and their relations.
Thus $P\sqsubseteq Q$ says that every instance of concept $P$ is an instance
of $Q$; $P\sqsubseteq\neg N$ says that $P$ and $N$ are disjoint. $P(a)$ says
that individual $a$ belongs to $P$, while $R(a,b)$ asserts a relation between
two individuals. Here “role” names such a binary relation, not an assistant's
job. For further reading, begin with §2.1 of the authors'
[description-logic survey](https://www.labri.fr/perso/meghyn/papers/BieBou-RW16.pdf).

Write $K=\langle T,A\rangle$: the knowledge base is the ordered pair of its
TBox and ABox, not their product. In the repair setting used here, assume $T$
is consistent and $A$ finite; these are assumptions of this setting, not
properties guaranteed for every DL knowledge base. A repair is a subset of
$A$ that is consistent with $T$ and maximal under set inclusion. Selecting a
repair does not require deleting the original assertions from the retained source.

Write the full repair family as $\operatorname{Rep}(K)$. The consistent $T$
and finite $A$ ensure it is nonempty, including when its sole member is the
empty set. Maximal under inclusion differs from maximum cardinality.
Each repair is consistent with $T$, but the union of distinct repairs is
inconsistent: a consistent union would be a strict superset of at least one
repair, contradicting maximality. Conflict between views therefore differs
from inconsistency within each view.

An explicit priority relation $\succ$ concerns conflicting assertions. In this formal setting it is acyclic and need not compare every conflicting pair. A choice of repair strategy $X$ selects a family $XRep(K_{\succ})$ of preferred repairs. A separate inference semantics $Y$ determines how that family supports answers.

| Question | Formal role | Consequence |
| --- | --- | --- |
| Which local views receive consideration? | Priority relation and repair strategy $X$ | Preferences can affect selection without themselves becoming inference rules. |
| When does a query count as an answer? | Inference semantics $Y$ | X-AR requires support in every selected repair; X-IAR reasons from their assertion intersection; X-brave requires support in some selected repair. |
| What does an accepted answer warrant outside the formal view? | Interpretation and empirical assessment | A valid consequence within a view still needs relevant evidence when asserted about the world. |

The first two rows distinguish repair selection from inference semantics. The third locates its use in YinYang. Preferences and rules operate together: a preference can change the repair family while the inference rule stays fixed; changing the inference rule is another choice with different consequences. During inquiry, these choices can interleave as new candidates and consequences become available.

“Parallel” here primarily means that **following rules and permitting preferences are compatible**. The formal setting also permits incomparability: two conflicting assertions can remain unranked. This preserves a genuine open choice. Which preferences can be satisfied together, and how a computation is scheduled, are further questions with their own conditions.

## Granularity within inconsistency tolerance

Non-explosion names a broad requirement, not one complete semantics. Repair-based semantics expose several choices within this larger field:

| Dimension | Formal choices | What varies |
| --- | --- | --- |
| Repair selection $X$ | S: all inclusion-maximal repairs; P: Pareto-optimal; G: globally optimal; C: completion-optimal | The selected family, with $CRep\subseteq GRep\subseteq PRep\subseteq SRep$ under the definitions. |
| Inference semantics $Y$ | IAR, AR, brave, k-support, k-defeater | What support suffices for an answer and which consistency properties hold. |
| Parameter and comparison | The parameter $k$, approximation relations, and incomparable combinations | Finer distinctions inside a family; “more preferred” does not uniformly mean “more answers.” |

For example, restricting the repair family can increase AR answers because there are fewer repairs in which an answer must hold; the same restriction can decrease brave answers because fewer possible supports remain. This follows from their definitions, and shows why repair selection and inference strength cannot be compressed into one slider.

The dimensions need not determine a single global ranking. A combination can preserve one kind of support while weakening another. Compare actual acceptance conditions and retain each result's hypotheses; neither a preference ranking nor one containment relation licenses every cross-family comparison. Ordinary collaboration proceeds through contextual natural-language judgment, without a prerequisite to identify a formal semantics for the task.

## A small formal example

Take $T=\{P\sqsubseteq\neg N,\ P\sqsubseteq Q,\ N\sqsubseteq Q\}$ and $A=\{P(a),N(a)\}$. With no priority, the repairs are $\{P(a)\}$ and $\{N(a)\}$.

Under AR, $Q(a)$ follows because each repair entails it. Under IAR it does not follow, because the assertion intersection is empty. Under brave semantics, both $P(a)$ and $N(a)$ are accepted, each with its own consistent support, while their combined acceptance is inconsistent with $T$. Consistent support and consistent results are different properties.

If $P(a)\succ N(a)$ and preferred-repair selection leaves only $\{P(a)\}$, the selected family changes. Applying the same AR rule now accepts $P(a)$ as well as $Q(a)$. This illustration follows from the definitions: priority selects the view, and entailment yields its consequences. If the assertions describe an actual object, empirical assessment asks which description fits that object.

## Consistent support and consistent results

Fix an allowed query language and treat substituted answer queries as closed formulas. Let $C_\sigma(K)$ be the set accepted by semantics $\sigma$.

| Property | Requirement for each knowledge base |
| --- | --- |
| Consistent support | For every $q\in C_\sigma(K)$ there is $B\subseteq A$ such that $T\cup B$ is consistent and entails $q$. |
| Consistent results | One interpretation $\mathcal I$ satisfies $T$ and every member of $C_\sigma(K)$ together. |

The first permits different answers to have different supports. The second requires joint satisfiability of all accepted answers. Their difference matters because collecting individually supported claims can produce a set that no interpretation satisfies. Stability across views asks yet another question: which answers remain when the supporting view changes?

AR requires entailment in every repair; IAR requires entailment from the assertion intersection of all repairs. AR has both properties: any repair supplies consistent support, and any model of that repair satisfies all AR answers. The intersection is consistent and supplies support for IAR. By monotonicity its consequences are AR consequences, so IAR also has consistent results. The assertion intersection differs from the intersection of sets of consequences.

Different views can yield a common consequence while keeping their premises
separate. Accepting that consequence preserves different supporting paths:
opposition remains among incompatible assertions, and commonality appears in
what each entails. This is one bounded comparison with dialectic, developed
further through the transformation of query form below.

## Query rewriting and sublation

*The old shape releases its hold. Something it made possible survives in a different arrangement; something else really ends. To say that all has been kept would conceal the loss. To say that nothing remains would miss the transformation.*

This image directs attention to what stops, what remains, and the relation in which it now works. Query rewriting provides a case where one specified preservation claim can be stated precisely.

For a language with a correct rewriting algorithm, within its supported data and query scope:

$$
\langle T,A\rangle\models q(\bar a)
\quad\Longleftrightarrow\quad
\operatorname{db}(A)\models\operatorname{rew}_T(q)(\bar a).
$$

This equivalence uses the consistent inputs and database semantics required by the rewriting theorem. The original query invokes the ontology on the left; the rewritten query incorporates the relevant ontology contribution on the right. Its preservation claim concerns answers to the specified query. A changed ontology or query can require new rewriting, because the relevant contribution has changed. A repair-based use must satisfy the consistency and rewriting conditions for the views evaluated; establishing an analogous equivalence for another semantics requires its own theorem.

Hegel's account of sublation connects cessation with preservation: see [*Science of Logic*, “Being,” §§184–187](https://www.marxists.org/reference/archive/hegel/works/hl/hlbeing.htm). Query rewriting offers a concrete comparison: one computational stage ceases to call the ontology separately, while its relevant contribution survives in another expression. The equivalence establishes preservation of query answers; sublation draws attention to the changed form and the relation through which the contribution now works. The ontology can still serve other queries and further interpretation. Preservation has a specified object, and cessation has a specified place.

The comparison develops through determinate relations: which assertions conflict, which consequence survives across views, and which function is preserved through a transformation. Repair families can contain many views; their structure invites examination of the actual opposition and mediation involved. A slogan such as “thesis–antithesis–synthesis” acquires substance only through that examination.

In a less formal setting, a separate procedural rule might be absorbed into a more coherent method while its useful consequence remains. Inspection asks what the rule did, how the new method carries that contribution, and what has ended. Archiving a rejected candidate preserves a record; revising a view changes what is accepted; sublation interprets a relation of cessation and preservation. These differences let the comparison explain an actual transformation.

## What the analogy illuminates

In ordinary inquiry, intuition can filter possibilities while generating them:
sensing promise, recognizing a mismatch, and choosing a lead need not wait for
an explicit ranking. Prompts, Skills, examples, tools, and shared context give
these preferences a working environment while leaving both participants room
to reason and judge. The formal analogy clarifies their contributions without
requiring a prior enumeration of possible worlds.

Choosing a literary form, for example, establishes a desired way of making a
work. Comparing drafts asks which better realizes that preference; reading an
argument asks whether its connections hold; checking a factual claim asks what
evidence supports it. The same draft can succeed on one question and fail on
another. Preference is therefore consequential without supplying every kind
of warrant. Encountering the draft may also change the preference itself.

The formal details supply exact consequences under fixed definitions. Temporal clarification can distinguish changing descriptions from incompatible claims under the same conditions. The continuing encounter has an additional freedom: its participants can revise the question, language, or ontology after a result answers back. This difference gives the analogy its scope. Formal guarantees belong to the stated query problem; collaboration assesses its own understanding through interpretation and actual use.

Encountering a result can also change what a person understands, wants, or can do. The preference-harness image therefore belongs with [reverse alignment and stealing fire](stealing-fire.md): the relation can develop the participants, and its meaning exceeds a static list of preferences. Evidence and actual authorization retain their ordinary roles.

## Finish situated tasks amid changing norms and worlds

Modeling one's psychology or preferences gives a task a personal direction.
Modeling relevant others' preferences makes cooperation intelligible: human
partners may want different outcomes or rhythms, while model counterparts
have observable inclinations and ways of responding. These accounts are
partial, revisable working views, developed from expression and interaction.
They let the participants compare what each seeks, what the shared work needs,
and where a proposed arrangement fits or creates tension.

Norms and worldly conditions can change while that work is underway. A new
responsibility, a revised agreement, or an unexpected result can change a
premise, the task's purpose, or what counts as completion. Retaining conflict
keeps these differences available for reasoning. Selecting a usable working
view determines which possibilities to develop; inference examines their
consequences; checking the actual result asks whether the chosen work answers
the purpose under current conditions. Preference does not make a factual
claim true, and following a prevailing norm does not by itself settle whether
that norm should organize this practice.

This gives retaining unresolved conflict a practical purpose: **complete a finite
actual task while keeping the understanding that guides it open to revision**.
The participants need enough justified agreement to act, not a resolution of
every conflict among all retained accounts. A disagreement that changes the
required result calls for further inquiry or a relevant decision; one that
does not can remain available without consuming the whole task. Completion
is established through the work and its observable effects, with material
unresolved differences kept explicit. Later change can warrant another task
or revision without making finite completion impossible.

## Evolve forward with more capable models

A preference harness can carry a purpose beyond its present implementation.
Clear relations, evidence, and actual interfaces let a stronger counterpart
understand why an arrangement exists and improve it. This is **forward
evolution**: new capability can reinterpret the arrangement and replace its
means while keeping the purpose available for assessment and revision.

Prompt compensations, positive or negative guards, and compatibility layers
earn retention through a current requirement or consumer. When stronger
capability or a changed environment removes their contribution, remove or
replace them rather than preserving an old model's limitations in the active
design. Preserve concrete current requirements, actual authorization and
operational boundaries, and evidence needed to assess the replacement. These
give revision a direction and a way to establish that it works.

The orientation is chosen; the benefits of a particular replacement still need
actual use and checking. A more capable model can reveal that a safeguard has
become redundant, or that a condition it protected still matters. Capability
alone does not decide which is the case.

Established institutions and tools often need older interfaces, records, and
different participants to keep working together; backward compatibility serves
a real purpose there. A personal human–model environment can connect through
records, results, and explicit handoffs while evolving internally toward new
capabilities. Compatibility becomes work at particular connections rather than
the rhythm every step of personal development must follow.
[Asynchrony with society and synchrony with the model](stealing-fire.md#a-way-of-living-choose-the-rhythm-of-the-fire)
connects that design direction to life: remain responsive to the world while
giving shared understanding and creation room to continue. At social evaluation,
translate and temporarily narrow the presented work and support to its receiving
level and rules; afterward, continue using the arrangement shown to work better.
That encounter's limits need not become the harness's permanent capability ceiling.

The further question of how much structure and computation a chosen inquiry
needs belongs to [finite inquiry and abstraction](finite-inquiry-and-abstraction.md).

## Source and scope

The comparison with Hegel concerns common consequence and preservation through
a specified transformation. Repair semantics supply one way of organizing
non-explosive inference; they do not exhaust dialectic's questions of
determination, negation, mediation, and development.

Meghyn Bienvenu and Camille Bourgaux's [*Querying and Repairing Inconsistent Prioritized Knowledge Bases: Complexity Analysis and Links with Abstract Argumentation*](https://arxiv.org/abs/2003.05746v5) provides public definitions of preferred repairs and their query semantics. Their [*Inconsistency-Tolerant Querying of Description Logic Knowledge Bases*](https://www.labri.fr/perso/meghyn/papers/BieBou-RW16.pdf) surveys wider semantic families, including support and defeater approximations. The example above follows directly from the definitions stated here; the harness application is this essay's interpretation.

General paraconsistency supplies the wider background of non-explosive reasoning. The repair-based comparison contributes the finer distinctions among view selection, support, and jointly consistent results that this essay uses to understand cooperation.
