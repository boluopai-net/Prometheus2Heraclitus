# How preference participates in choice and reasoning

[Home](../../README.md) · [Core views](core-views.md#yy-10) · [简体中文](preference-harness.zh-CN.md)

A recoverable trajectory needs to show both what the participants chose and
what they had grounds to conclude. [Reasoning within an unfinished stream](reasoning.md)
followed the reading environment from an initial request through competing
explanations and a revised interface. Here the question is how the choices
within that history relate to evidence: why develop this arrangement, what
supports saying it works, and what remains open after it has been chosen?

The person can prefer continuity of reading and choose direct access to a
passage over a more elaborate shelf. This gives the work a direction. A test
showing that the correct passage opens establishes an operational result;
the person's reading and feedback bear on whether the arrangement supports
continuation. If use still interrupts reading, the chosen design can be
revised. Its having been preferred does not settle these factual questions.
YinYang is a **preference harness** for this joint activity: preferences,
reasoning, judgment, and responsiveness to the world contribute together.

The model ordinarily understands and reasons through informal natural language. Purpose, examples, conversation, and the surrounding harness make a preference intelligible enough to act on. The formal comparison below brings the respective roles of selection and inference into focus. Process ontology represents relevant objects, relations, and changes; event streams organize the history in which both participants generate, choose, act, and reconsider.

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

## Keep choice and support within the trajectory

In the reading example, the relevant history can retain the choice of a
layout, the reason for choosing it, the version tried, and what happened in
use. These connections let later participants distinguish “we wanted fewer
interruptions,” “we tried direct links,” and “this use supported the claim
that the links helped.” A later preference for another layout changes the
active arrangement; it does not make the earlier choice or its grounds cease
to have occurred.

Nor does accepting one explanation require rewriting the source history as
though no alternative existed. If an execution defect was considered and then
ruled out, its retained question and check can explain why the inquiry turned
toward reading continuity. A preferred current account selects what guides
action now. The trajectory preserves enough of the sources and changes to
make that selection understandable and open to criticism.

The formal repair comparison below sharpens this distinction. Selecting a
consistent view from conflicting assertions need not delete the retained
assertions; deriving an answer within that view has further conditions.
The historical record and the currently accepted premises therefore have
different responsibilities. Ordinary cooperation can preserve their relation
in clear language without turning the history into a formal knowledge base.

## Conflict has more than one form

Keeping a candidate available differs from accepting its claims. Psychological
conflict asks a further question: what purposes or relations does a person
struggle to hold together? Opposing wishes, an unsettled experience, and two
incompatible propositions call for different responses. Their comparison helps
explain why preserving a tension, choosing a view, and correcting a fact can
each be appropriate without being interchangeable.

Freud's [*Introductory Lectures*, Lecture XXIII](https://www.gutenberg.org/cache/epub/38219/pg38219-images.html), explains symptom formation through opposed tendencies that continue to contribute to a compromise. This historical account directs attention to what each side sustains and why a settled-looking outcome may retain conflict. It suggests a question for understanding conflict: what is each competing arrangement trying to preserve? A knowledge-base repair instead selects a consistent assertion set under explicit assumptions; it neither diagnoses a symptom nor implements Freud's clinical theory.

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

## From conflicting views to reconstructed premises

Two consistent views can disagree: one entails $p$, another entails $\neg p$.
Each has interpretations satisfying its premises; no single classical
interpretation satisfies both conclusions together. Keeping these views
available therefore does not assert a contradiction within one interpretation.
The disagreement also does not establish that both views are inadequate. Evidence
may support one, distinguish their circumstances, or leave the issue unresolved.
When their shared assumptions prevent a purpose from being adequately understood
or realized, the next contribution can instead be a better account of the problem.

Consider a **propositional teaching example** using the same maximal-consistent-
subset principle. It is an illustration authored here, not another result about
the DL query languages studied by [Bienvenu and Bourgaux](https://arxiv.org/abs/2003.05746v5).
For one specified task and situation, let $h$ mean assistance is used, $p$ mean
the person retains direction and control, and $c$ mean the delegation is
inspectable and changeable by the person. These meanings stay fixed below.
Start with:

$$
T_0=\{h\rightarrow\neg p\},\qquad A_0=\{h,p\}.
$$

$T_0$ is consistent, but $T_0\cup A_0$ is not. Its two repairs are $\{h\}$
and $\{p\}$. The first, together with $T_0$, entails $\neg p$; the second
entails $p$. With both repairs retained, AR accepts neither $p$ nor $\neg p$;
IAR accepts neither from their empty assertion intersection. Brave inference
accepts each separately through a different repair. It does not establish the
conjunction $p\land\neg p$, which neither repair entails.

Choosing a preferred repair changes which assertion set guides inference while
leaving $T_0$ fixed. Yet if the actual task calls for useful help while retaining
the person's direction, and observation shows that both occur together, the
shared rule “assistance entails loss of direction” deserves examination. Merely
choosing between the old repairs cannot express that possibility. A candidate
reconstruction distinguishes the conditions of delegation:

$$
T_1=\{(h\land c)\rightarrow p,\ (h\land\neg c)\rightarrow\neg p\},
\qquad A_1=\{h,c,p\}.
$$

Here $T_1\cup A_1$ is consistent. The old unconditional rule has been
**retracted and replaced**, not supplemented: retaining it would again make
the assertions inconsistent. The new account preserves the concern about lost
direction while making room for help under specified conditions. This is a
change to the theory and available distinctions, beyond repairing assertions
under a fixed theory. Other reconstructions can revise vocabulary or the question
itself; they must explain how old and new meanings relate.

The two rules in $T_1$ are illustrative conditional assumptions, not established
causal laws or an autonomy principle. Inspectability and changeability may be
insufficient in actual use, and their absence need not imply loss of direction.
Evidence, the person's purposes, and observable consequences determine whether
this reconstruction improves on the old account or needs further revision.
Formal coherence makes the candidate intelligible; it does not guarantee fit.
[Conflicting models and reconstructing the question](speech-opposition-and-self-formation.md#conflicting-models-and-reconstructing-the-question)
develops this move in the cooperation example. The dialectical comparison lies
in examining and transforming what generated the opposition, while retaining
the concerns it expressed, rather than always selecting a winner among unchanged
views. Repair semantics specify inference within their given setting; they do
not themselves prescribe this reconstruction.

## Consistent support and consistent results

Fix an allowed query language and treat substituted answer queries as closed formulas. Let $C_\sigma(K)$ be the set accepted by semantics $\sigma$.

| Property | Requirement for each knowledge base |
| --- | --- |
| Consistent support | For every $q\in C_\sigma(K)$ there is $B\subseteq A$ such that $T\cup B$ is consistent and entails $q$. |
| Consistent results | One interpretation $\mathcal I$ satisfies $T$ and every member of $C_\sigma(K)$ together. |

The first permits different answers to have different supports. The second requires joint satisfiability of all accepted answers. Their difference matters because collecting individually supported claims can produce a set that no interpretation satisfies. Stability across views asks yet another question: which answers remain when the supporting view changes?

AR requires entailment in every repair; IAR requires entailment from the assertion intersection of all repairs. AR has both properties: any repair supplies consistent support, and any model of that repair satisfies all AR answers. The intersection is consistent and supplies support for IAR. By monotonicity its consequences are AR consequences, so IAR also has consistent results. The assertion intersection differs from the intersection of sets of consequences.

## Unity within conflict: consistent views and common consequences

Inconsistency-tolerant semantics already organizes opposition. The retained
assertions conflict; repairs organize them into internally consistent views;
query semantics specifies how answers may be accepted across those views.
Unity can occur in a common consequence: premises that cannot be merged may
still support the same conclusion.

In the earlier example, $R_1=\{P(a)\}$ and $R_2=\{N(a)\}$ are each consistent
with $T$, while their union is inconsistent. Because $P\sqsubseteq Q$ and
$N\sqsubseteq Q$, both paths entail $Q(a)$. AR accepts $Q(a)$ without first
choosing between $P(a)$ and $N(a)$. The answer to this query is unified, while
the original conflict and distinct grounds remain visible. This is
**commonality established through difference**.

Two levels of consistency can coexist here: consistency inside each repair,
and joint consistency of the answers accepted by AR or IAR. Cross-view
stability asks another question: does an answer hold in every considered
view? The relations connect but have distinct objects. Brave can give every
answer consistent support while leaving the answer set jointly inconsistent.
IAR starts from the assertion intersection and can lose a consequence that
AR obtains through different paths.
[Definition 7 in the source paper](https://arxiv.org/html/2003.05746v5#S3)
provides these acceptance conditions. Whether unity is possible, and at
which level, depends on the semantics and the actual conflict.

In [the *Encyclopaedia Logic*, §§79–81](https://www.marxists.org/reference/archive/hegel/works/sl/sl_vi.htm),
Hegel distinguishes understanding's fixed determinations, their dialectical
disclosure of limitations, and the speculative apprehension of affirmative
content within opposition. The [development of §82](https://www.marxists.org/reference/archive/hegel/works/sl/sl_divis.htm)
understands unity as a concrete relation among distinct determinations.
Read through this question, the example asks which different grounds the
common answer passes through and which distinctions it preserves.
The commonality of $Q(a)$ does not turn $P$ and $N$ into one concept:
incompatible support paths meet in a specified result.

A further change becomes relevant when the fixed $T$ itself creates an
inadequate exclusion: revise the premises producing the opposition. The
earlier passage from $T_0$ to $T_1$ changes the relation between assistance
and autonomy. Obtaining a common consequence preserves the theory, whereas
premise reconstruction changes it. Both admit a dialectical interpretation
while accomplishing different work. Formal semantics makes the former unity
precise; philosophical inquiry continues to ask why that organization is
appropriate and when it needs to change.

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

Understanding one's own psychology and preferences gives a task a personal direction.
Understanding relevant others' preferences makes cooperation intelligible: human
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

The reading environment can change again while retaining an intelligible
trajectory: which alternatives were preferred, why, what was checked, and what
the checks warranted. Distinguishing these relations gives finite inquiry a
target. Which of them must a representation and method preserve, and what
evidence makes that representation adequate for later use?
[Finite inquiry and abstraction](finite-inquiry-and-abstraction.md) asks how
much structure and computation a usable trajectory needs under limited time
and attention. Choosing an abstraction and checking its consequences can
develop together; preference guides the choice while formal validity depends
on the stated premises and inference rules.

## Source and scope

The comparison with Hegel concerns common consequence, reconstruction of the
premises generating an opposition, and preservation through a specified
transformation. Repair semantics supply one way of organizing
non-explosive inference; they do not exhaust dialectic's questions of
determination, negation, mediation, and development.

Meghyn Bienvenu and Camille Bourgaux's [*Querying and Repairing Inconsistent Prioritized Knowledge Bases: Complexity Analysis and Links with Abstract Argumentation*](https://arxiv.org/abs/2003.05746v5) provides public definitions of preferred repairs and their query semantics. Their [*Inconsistency-Tolerant Querying of Description Logic Knowledge Bases*](https://www.labri.fr/perso/meghyn/papers/BieBou-RW16.pdf) surveys wider semantic families, including support and defeater approximations. The DL example follows directly from the definitions stated here. The propositional teaching example uses the same repair principle; reconstructing its theory and applying these distinctions to the harness are this essay's contributions.

General paraconsistency supplies the wider background of non-explosive reasoning. The repair-based comparison contributes the finer distinctions among view selection, support, and jointly consistent results that this essay uses to understand cooperation.
