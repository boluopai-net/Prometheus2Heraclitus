# Writing one's own recursive improvement through literature

[中文](literary-recursive-improvement.zh-CN.md)

People borrow fire, create works, and change themselves through creation. Among these works another takes shape: a description of how one perceives, understands, generates, and acts. Personal philosophy gives it direction, a personal model brings it close to actual life, and a language model unfolds it into new interpretations, tools, and activities. The description continues into itself: how understanding forms, how possibilities are compared, how a change is judged worth keeping, and how these practices can themselves be revised.

**Recursive improvement happens in this return: what one round of practice yields changes how the next round produces improvement.** A better work gives a person a useful result; a more fitting method gives later work a new starting point; and capacities developed through repeated participation can change how the person poses questions, understands feedback, and organizes help. YinYang expresses these connections as a personal arrangement that can be read, used, and revised.

This chapter connects three earlier questions: what a [trajectory](flow-and-time.md) retains, how [reasoning and the working view](reasoning.md) organize current judgment, and how [literary programming](literary-programming.md) makes a description into a usable relationship. RSI brings them together in a further question: **How can we make the way we improve ourselves available to our own practice for improvement?**

## Body, generative description, and interpreter

In his conception of self-reproducing automata, von Neumann distinguished an apparatus that constructs according to a description, an apparatus that copies the description, and a control that coordinates these operations. The description participates in construction and is also transmitted as material from which further construction can proceed. He also examined what parts the environment already supplies: the choice of elementary components determines how much work the constructor must do [[1]](#source-1).

This offers a relational structure for understanding YinYang. Within an ongoing shared practice, we distinguish three functions:

| Function | What it bears in YinYang | How it produces subsequent consequences |
| --- | --- | --- |
| Body $B_t$ | A person's senses, actions, habits, and capacities, together with devices, records, tools, and counterparts that continually support activity. | Perceives, participates, acts, learns, and bears consequences. |
| Generative description $\Delta_t$ | Philosophical direction, understanding of the person and counterpart, their relationship, environmental arrangements, and methods of revision. | Enables participants to understand, unfold, and reorganize the practice. |
| Interpreter $I_t$ | A process of interpretation and realization centered on a language model and equipped with actual tools. | Forms plans from the description and current situation, constructs works, and adjusts the environment. |

Body here has a distributed practical meaning. When a capacity is maintained jointly by a person's judgment, a model's elaboration, available tools, and records one can return to, we understand it along those actual connections. The person's body is the center of life and the entrance to feeling and action; the model makes more expression, comparison, and construction available as contributions. As support, the model belongs to this organization, and in reading and unfolding the description it also serves as interpreter.

A generative description expresses relationships that can continue to be unfolded. For example, “a counterpart who unfolds a question together with the person” can lead to investigation, formation of candidates, making, checking, and revision. New situations have not yet been listed individually, but the relationship already gives the model a direction for interpreting them. On seeing the result, the person may also reconsider how that sentence should be written. Both participate in interpretation, and engineering supplies actual means for the parts that need to be enacted.

The [trinity of philosophy, psychology, and engineering](local-source-and-website.md#trinity-and-sinthome) thus acquires a set of technical connections: philosophy develops the description and its reasons, psychology understands the activity of embodied participants, and engineering organizes interpretation and realization. The three change one another along the same practice.

## Self-reference makes a method its own object

Kleene's second recursion theorem establishes a precise possibility. Let $\varphi_e$ denote the partial function computed by the program numbered $e$. For every total computable transformation $F$ of program indices, there exists an index $e$ such that

$$
\varphi_e \simeq \varphi_{F(e)}.
$$

What is compared is computational behavior. A program can operate according to an effective procedure that obtains its own index. Kleene's original paper and Moschovakis's modern account give constructions; the latter also presents a Turing machine that outputs its own description [[2]](#source-2), [[3]](#source-3). This makes “a process taking its own description as material” a concretely constructible relationship.

Self-reference supplies an entry for modification; evaluation and methods of modification give change a direction. An operator that always returns the original program unchanged is also a computable transformation, and its trajectory remains as it was. To create new functionality, one must specify how candidates are generated, on what basis they are compared, and how a selected change enters the next run.

Schmidhuber's Gödel machine takes this question to the method of improvement itself: its initial software contains a proof searcher that searches for proofs supporting self-rewrites; a rewrite may also concern proof search and resource allocation. Its comparison has a definite object: the utility of adopting a modification now against the utility of continuing the existing search. This comparison brings the time and opportunity cost of seeking a better method into judgment [[4]](#source-4). Yampolskiy's discussion of RSI likewise distinguishes changing a program, improving performance, and improving the capacity for later improvement [[5]](#source-5).

YinYang brings these questions into human practice. Its self-description includes methods of collaboration and revision, which person and model can read, discuss, rewrite, and realize. Mathematical research provides concrete constructions of effective self-reference and modifiable improvement programs; the following account explains how to organize a developmentally meaningful return in embodied, open life supported by external capacities.

## Retaining conflict and forming a view for action

Improvement requires seeing possibilities beyond the current arrangement. A failure, reports from different people, and an earlier abandoned proposal may point to incompatible explanations. Retaining them as material for comparison allows the current description to continue encountering difference. Action also requires sufficiently definite grounds: what object is to be addressed, which relations matter, and what predictions and choices follow?

The earlier essay's **working view** answers the latter questions. It organizes relevant material, candidate explanations, adopted premises, and ways of reasoning for the current problem. Retained sources are broader; the working view makes grounded commitments from them. Explanations not currently adopted remain available for comparison and can return when new results appear.

[Inconsistency-tolerant semantics](preference-harness.md#selection-and-inference) provides a precise local example of this distinction. Fix general axioms $T$; select subsets of conflicting assertions $A$ that are consistent relative to $T$ and maximal under inclusion, and the result is a set of repairs. The adopted query semantics then determines how answers are obtained across repairs. Under an answer rule requiring support in every selected repair, a conclusion can hold amid unresolved conflict [[6]](#source-6).

For example, suppose $P$ and $N$ are mutually exclusive, both entail $Q$, and the material contains both $P(a)$ and $N(a)$. Either consistent basis yields $Q(a)$. This shows how to obtain a local conclusion robust across these alternatives. If further inquiry finds the classification relations unsuitable for the current object, $T$ itself needs reconsideration; changing the classification, axioms, or answer rule forms a new question of inquiry.

Here inconsistency tolerance meets recursive improvement. **Local reasoning produces a result under selected relations; reflection also makes the way those relations are selected an object.** The participants can modify the scope of material, methods of generating candidates, priorities among sources, conditions for accepting conclusions, and concepts that organize the whole question. Each modification has its own reasons: new facts can change a judgment, a new purpose can alter a practical trade-off, and a new interpretation can reconstruct the original options.

## From rewriting words to changing the next activity

Writing a method into a description makes it identifiable and modifiable. How it actually works also takes shape through the model's understanding, tools, a person's habits, and current conditions. “Compare two options,” for example, must be unfolded into which outcomes to compare, how to obtain them, which differences would change the choice, and who undertakes the comparison. These concrete activities can themselves be revisited.

A set of working notations gathers the relationship:

$$
A_t=I_t(\Delta_t,B_t),\qquad
(B_{t+1},E_{t+1})=\operatorname{Encounter}(B_t,A_t,\Omega_t).
$$

$\Delta_t$ is the current description, $B_t$ the embodied participation and support conditions at that time, and $I_t$ unfolds them into activity $A_t$. The activity encounters the world $\Omega_t$, bringing actual participation and environment into a subsequent state $B_{t+1}$ and leaving experience and results $E_{t+1}$ available for understanding. The notation expresses dependencies to investigate; a particular study must explain which changes occur, how, and how they can be observed.

Revision brings these results back into the description. Let $R_t$ be the revision method actually used at the time, and $\Delta^R$ the part of the description concerning revision:

$$
\Delta_{t+1}=\operatorname{Revise}_{R_t}(\Delta_t,E_{\leq t+1}),\qquad
R_{t+1}=\operatorname{Realize}(\Delta^R_{t+1};I_{t+1},B_{t+1}).
$$

The first step compares current understanding with relevant experience and writes a successor description. The second brings its method into the next round of work through interpretation and actual organization. The method in the description may be rewritten first, software may update relatively quickly, and a person's habits may form gradually over many activities. Each change follows the rhythm of its actual realization.

**The reflexive relationship lies between these two steps: a revision method participates in modifying the description of itself, and the revised description, once realized, changes later revision practice.** New words offer a candidate that can be realized; subsequent selection of material, comparison, judgment, and action show what function it has acquired.

## How one reading changes the way reading is improved

Continue with the hypothetical reading environment from the earlier essay. A person wants to resume reading easily. The model organizes a bookshelf and checks the result by asking whether the selected book can be opened. The correct book does open, yet the person still has to find the previous passage and reconstruct the argument just followed. The operational result and the reading experience together clarify the problem: opening the book is one step, while resuming understanding also requires recovering a thread.

The participants can retain two candidates. One holds that the destination is wrong; the other that the original check covered only part of the purpose. Inspecting the actual page can examine the first explanation; once the book is found to be correct, the course of reading helps illuminate the second. The sources retain the original request, the version actually opened, the person's response, and the checking process; the current working view uses them to select the next modification.

The first modification returns the page directly to the relevant passage, and its effect is examined during reading. Git retains the original bookshelf and the later entry point, while feedback from use explains why the difference matters. If the new arrangement makes reading easier to resume, it provides grounds for claiming an improvement to this work.

The recursive next step is to rewrite the improvement practice as well: when modifying a reading environment in future, first recover the activity the user wants to continue, then select acceptance checks from that activity. Guided by this method, the model identifies a return point to preserve earlier in another reading task, and the participants can more easily form a fitting arrangement. Subsequent work then provides grounds for judging the method improved.

Further use may reveal that new reading calls for an overview, while resumed reading calls for direct access. The participants therefore retain both entry points and explain the activity each serves. An idea previously set aside in favor of the current proposal becomes part of the reconstructed arrangement. “Keeping hold of the thread” can condense these relationships; examples, conditions, and realization continually enrich its meaning.

The example connects three kinds of result:

| Object improved | How it appears in the example | Where subsequent grounds come from |
| --- | --- | --- |
| Work | The page supports return to the needed passage. | How this page works in actual reading. |
| Method | Checks are selected from the activity to be continued. | How later related tasks produce fitting arrangements more effectively. |
| Capacity | The person and supporting environment can more readily recover, understand, and continue reading. | The activities they can subsequently initiate, judge, and sustain in practice. |

These results can support one another and can also appear at different speeds. Support that remains available can itself become part of a person's distributed capacity.

## How evaluation continues to develop

Improvement requires something worth improving. Personal philosophy supplies a direction for life, particular tasks unfold that direction into comparable outcomes, and methods organize how those outcomes are obtained and understood. Evaluation therefore also has content that can be revised.

In the reading example, changing “can open the book” to “can resume understanding” corrects a proxy under the same purpose in life. A later wish to preserve opportunities to explore unfamiliar material may change the trade-off: some navigation helps form an overview, while other steps are the burden of repeatedly recovering context. Later still, the person may reconsider how much to invest in reading, creation, and rest. Revision can occur at the distinct positions of checks, means, and ends.

By connecting the original direction, difficulties encountered, reasons for change, and later results, changes in evaluation acquire an intelligible continuity. The participants can explain what a new standard sees, what the earlier one missed, and what gains and costs the new choice brings. The model contributes comparison, explanation, and realization; the person contributes lived experience, direction, and judgment; the world supplies further material through use of the work and responses from others.

This gives “better” a concrete meaning. It may mean noticing important differences more readily, forming more intelligible judgments, spending less effort repeatedly recovering context, realizing a wish more reliably, or being freer to change a pursuit that no longer fits. Recursive improvement thus serves a life and can also enrich the interpretation of values through which that life is organized.

## Git/GitHub: making change comparable and continuable

Both literary description and its engineering realization can retain versions. Git makes a change to text or code an inspectable difference; GitHub lets selected public works be read, discussed, and developed further. Connecting records with versions lets the model return to the understanding adopted at a time and compare what happened later.

| Version operation | Contribution to recursive inquiry |
| --- | --- |
| Save a commit | Retain a description or realization as a definite object for later comparison. |
| Inspect a diff | Show which relationship, method, or code changed. |
| Develop a branch | Give an alternative arrangement worth trying a place where work can continue. |
| Merge and reconstruct | Organize selected contributions into the next arrangement actually used. |
| Return to an earlier version | Recover old material under new conditions and form a new choice. |

These are means of retention and construction. One file can contain several candidate explanations, and one explanation can be expressed jointly through several works. The meaning of the writing and actual use show which view is adopted; version relationships locate how these expressions formed. Connecting reasons for choices with relevant experience allows version history to help explain the meaning of a revision.

**A recursive loop and a directed acyclic commit history can both hold.** The loop describes a functional relationship that repeatedly returns: a work puts a method to the test, and the method changes the next work. The history records each return as a later event: the first modification, first use, and second revision each have their own place. Returning to a question produces a new event; adopting old content again can also form a new commit. Git's parent–child edges record version ancestry [[7]](#source-7); the meaning of reflection comes from the actual connections among versions, reasons, and consequences.

Descriptions of how to revise methods can enter the same history. The participants can compare how material was selected before, why that changed, and whether the change took effect in the next work. Public philosophy, private understanding, and records of actual use each reside in suitable places; shared inquiry connects them according to the question. Website, repository, and local environment respectively support reading, maintenance, and operation, making self-description work that can be continued.

## The benefits of condensation come from existing interpretive capacity

Literature lets an image organize many connected activities. “Borrowing fire” connects acquiring capacity, cultivating oneself, and continuing to create; “keeping hold of the thread” connects returning to a place, recovering context, and resuming understanding. Readers unfold a short phrase because language, culture, examples, and shared experience already participate in their understanding.

Discussing genetic descriptions, von Neumann paid particular attention to how a description operates in an already organized environment: sometimes it need only provide cues for selection and triggering, with existing organization doing much of the work [[1]](#source-1). This helps illuminate the cooperation of a short description and a capable interpreter. YinYang's literary expression likewise entrusts much of the unfolding to participants who already possess knowledge and contextual understanding.

The benefits of condensation must be assessed across the whole practice. Easier writing and maintenance are one benefit; faster recovery of shared direction by the model is another; the costs of interpretation, checking, and repair also enter the account. A phrase that reliably recalls fitting relationships can reduce coordination among scattered instructions; when a new distinction needs elaboration, longer writing, examples, and original material provide room for continued understanding.

Good condensation therefore has both **organizing and unfolding power**: it can bring practices in different places back into one relationship, and can elaborate its reasons and conditions where they matter. It retains distinctions that would change judgment and entrusts other details to the interpreter and environment currently able to bear them. Revising a set of core relationships can consequently change many related activities together.

This also shows where complexity resides. A description can be concise because interpreter, body, tools, and shared history bear other organizing work. The question is whether this division of work can continue at an affordable cost and whether, when a new problem arises, the relevant relationships can be found and changed. Literature thus becomes a practical means of revision: easy to return to, easy to rewrite, and capable of generating new arrangements.

## Developing with a changing interpreter

Advances in language models change what contributions a description can elicit. The same philosophical relationship may be unfolded by a more capable model and new tools into works previously difficult to realize. By recognizing this possibility, selecting and connecting capabilities, and rearranging collaboration, the person–model community turns external progress into its own working conditions.

This is one concrete form of reverse alignment. The person develops an understanding of how to create together with generative capacity; the model adjusts its contribution according to the personal description; and both reconsider who undertakes what. Work that previously needed item-by-item specification can gradually be entrusted to clearer purposes and relationships, giving the person's attention an opportunity to enter new perception, comparison, and creation.

External model upgrades and local development of methods support each other in the same practice. When explaining an improvement, retaining the models, tools, materials, and conditions of participation involved helps clarify which capacities came from new support and which relationships formed through shared work. The person's body, habits, and environment each change at their own pace; the personal description connects them in a time to which the participants can continue to return.

YinYang's RSI therefore centers development on this person and their actual relationships of support. Literature makes self-understanding a readable work, philosophy explains why to cultivate in this way, model and engineering give it function, and embodied experimental philosophy lets consequences continue to participate in the argument. **Creation changes the work and the creator; when that change further improves how the next round learns, judges, and creates, recursive self-improvement acquires its own practical content.**

## Sources and their contributions

1. <a id="source-1"></a> John von Neumann, edited by Arthur W. Burks (1966), *Theory of Self-Reproducing Automata*, Lecture V, printed pp. 75–87. Pages 75–77 discuss construction components and environment, p. 79 the dependence of description on existing organization, and pp. 84–87 construction, copying descriptions, and hereditary variation. [Public scan](https://fab.cba.mit.edu/classes/862.16/notes/computation/vonNeumann-1966.pdf). This chapter develops a functional comparison of description and supporting environment from that account.
2. <a id="source-2"></a> Stephen Cole Kleene (1938), *On Notation for Ordinal Numbers*, §2, printed p. 153. [DOI](https://doi.org/10.2307/2267778). Effective construction using one's own index as a parameter.
3. <a id="source-3"></a> Yiannis N. Moschovakis (2010), *Kleene’s Amazing Second Recursion Theorem*, theorem statement on printed p. 190, and §1, Theorem 1.1, pp. 192–193. [Author's full text](https://www.math.ucla.edu/~ynm/papers/1602-002-1.pdf). Concrete constructions of effective self-reference and output of one's own description.
4. <a id="source-4"></a> Jürgen Schmidhuber (2006, v5), *Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements*, §4.1, Theorem 4.1 (printed p. 11), §4.3 (p. 12), and §6.1 (pp. 15–16). [Version read](https://arxiv.org/abs/cs/0309048v5). The utility comparison includes the opportunity cost of continued search, and modification may concern the improvement program itself. This chapter borrows that problem structure to develop a person–model method grounded in interpretation, practice, and subsequent results.
5. <a id="source-5"></a> Roman V. Yampolskiy (2015), *From Seed AI to Technological Singularity via Recursively Self-Improving Software*, §§1–2, PDF pp. 2–4. [Paper](https://arxiv.org/abs/1502.06512). Distinguishes self-modification, improved performance, and change in capacity for subsequent improvement.
6. <a id="source-6"></a> Meghyn Bienvenu and Camille Bourgaux, definitions of repairs and query semantics, §3. [Author's version](https://arxiv.org/html/2003.05746v5#S3). This chapter follows the local formal example in the [preference essay](preference-harness.md), then examines how such selection rules themselves become objects of revision.
7. <a id="source-7"></a> Git project, *Git Glossary*, entries including DAG, commit, branch, and merge. [Official glossary](https://git-scm.com/docs/gitglossary). Version ancestry gives technical meaning to historical location; actual materials establish the connection between versions and consequences in life.
