# Course materials

Use this branch when preparing, revising or validating saved Course material.
The root Skill owns teaching, evidence, actor and State boundaries.

When a course combines several source formats, apply
[Course sources and entry](course-sources-and-entry.md) to their selection and
integration. The documents below serve the learning object across its sources;
they are not repeated once per medium or incidental reference.

Choose and combine three writing approaches: mathematics, technical study,
and philosophy. Here technical study is a broad material-organizing category
that includes scientific investigation, methods and tools, and engineering
realization; it does not assert that these disciplines are identical. All three
share source grounding, an independent glossary and relevant learner/research
connections. Preparation supplies support; learning evidence stays with State.

## Select the writing approach

Judge the actual source and current question rather than its folder, title or
department. For substantial saved material, briefly state the primary approach
and any supporting emphasis that materially changes the explanation. A sentence
such as “Mathematics-led, with computational experiments” or “Technical study,
emphasizing empirical modeling and engineering implementation” is enough.
Use the learner's language in the saved material. This is an explanation of
how to read the material, not a score, permanent discipline assignment or new
metadata registry. A clear single approach needs no elaborate classification.

| Approach | What the main guide develops | What supports its conclusions |
| --- | --- | --- |
| Mathematics | Objects, definitions, notation, assumptions, statements and their formal relationships; develop needed derivations, proofs, examples and counterexamples in the guide. Distinguish a definition, a result under conditions and an application. | Valid reasoning under explicit assumptions; computations and examples illuminate or test candidates but do not replace a general proof. |
| Technical study | Connect the problem, representation, model or method, operations and observable consequences. Combine the scientific, methodological and engineering emphases below as the selected work needs. | Evidence appropriate to the claim: empirical comparison, formal properties, computational behavior or actual system performance. A successful run establishes only what it checks. |
| Philosophy | Develop situated concepts, problems, theses, reasons, distinctions, objections, responses and interpretive alternatives under the philosophy branch. | Source interpretation and argument, with factual or formal claims checked on their own grounds. Preserve the source's ambiguity and historical differences where material. |

In mathematics, make domains, quantifiers, dimensions and assumptions explicit
where they determine meaning. Explain which objects a statement connects, what
its conditions permit, and how changing a condition changes the conclusion.
Distinguish necessary from sufficient conditions and an equivalence from a
one-way implication. Develop the proof or derivation needed for understanding
in the main guide, with counterexamples at the relevant boundary; retain only
the precise statement and conditions in the glossary. Applied interpretation
belongs beside the formal result, with the additional modeling assumptions
visible. This supports mathematical understanding without making unaided
proof production or memorization a prerequisite.

Within technical study, distinguish these contributions without creating three
more compulsory document sets:

- **Scientific investigation:** phenomena, measurement and operationalization,
  hypotheses or explanatory models, observations and experimental design,
  uncertainty, competing explanations and limits of generalization. State what
  evidence would distinguish the accounts; a simulation alone does not establish
  a claim about the observed world.
- **Methods and tools:** representations, algorithms, procedures, inputs and
  outputs, applicability conditions, mechanisms, comparisons and failure modes.
  Explain how a method works and what its result means rather than only listing
  commands or interfaces.
- **Engineering realization:** the intended function, requirements, constraints,
  architecture and interfaces, implementation choices, tradeoffs, verification
  and operation of an actual artifact or system. Connect success to the intended
  use and observable acceptance, not merely construction or execution.

These emphases can recur within one unit. An empirical model may need software,
but scientific modeling does not automatically make engineering the main study
object. Using a technique does not require a separate technique course.
Conversely, calling an implemented model “research” does not remove its
implementation and validation needs. Mathematics can supply a formal component
of either work without making its empirical claims mathematical theorems.

For mixed sources, choose the main explanatory progression and bring in the
other approach where it contributes. Philosophy of science can be philosophy-led
with a scientific case; a computational psychology study can be technical,
emphasizing scientific evidence with mathematical and engineering support.
Ontology work may be philosophical clarification, formal semantics, or
engineering a usable schema and reasoner: inspect the actual task. The words
“conceptual engineering” alone do not establish an artifact-building task.
Do not force all material into three repeated sections, split one connected
explanation into competing guides, or relocate corpus folders to enact this
writing distinction. Language learning keeps its own applicable method.

## Required independent glossary

For substantial saved study material, prepare the relevant glossary scope first.
Keep it as a separate file regardless of length: the user needs it to recognize
and recover concepts, not as an optional appendix after memorization. Begin with
a concept map rendered as a diagram, followed by detailed entries and
verified source associations. The map uses visible concept nodes and connections
with meaningful relations: for example dependency, distinction, representation,
explanation, evidence or transformation. Link its concepts to the maintained
entries where the reading surface supports that navigation. Use Mermaid or
another supported diagram/image format and check its rendered legibility.
A prose outline, bullet list, table of contents or collection of linked names
does not substitute for the diagram. Do not add a separate “conceptual
throughline” section; put needed connected explanation in the main guide.
A short diagram legend may explain a symbol or relation without becoming a
second exposition. The detailed glossary also needs a fitting amount of
explanatory visuals beside the terms whose meaning, conditions or distinctions
they clarify; the opening map does not replace these local visual explanations.
Preserve useful depth and source order. Philosophy
uses its branch's contextual depth; technical material retains the definitions,
symbols, conditions and mathematical statements needed to recognize its objects.

Connect the guide's named concepts directly to their glossary headings or blocks,
and give reciprocal unit/return navigation. Ground a needed term briefly at its
point of use so reading does not require memorization or constant switching;
retain the detailed maintained definition in the glossary. Neither one giant
file nor a page of links substitutes for this relationship. An isolated question
does not require producing a whole book's materials first.

## Mathematics and technical study: three connected documents

Mathematical and technical sources use their actual knowledge and training
structure, with the distinct writing approaches above. Maintain:

1. **Glossary** — the independent recognition support above.
2. **Study and research guide** — integrate the former learning plan and reading
   reference with the learner connections described below in one main document, such as
   `<course-or-source>学习与研究指南.md`. It explains what to understand, the
   useful source order and depth, exact original-reading selections when that
   mode is intended, and relevant connections to the learner's environment,
   interests, prior understanding, and research. Develop the actual
   mathematical relationships, empirical models, procedures, code behavior or
   engineering decisions needed for understanding, according to the selected
   approach. Do not require an author-objection-response structure merely
   because philosophy uses one. Overall personal priorities and scheduling keep
   their existing learning-path owner.
3. **Exercises and experiments** — one training document, such as
   `<course-or-source>习题与实验.md`, with clearly distinct written-exercise and
   experiment/project parts. Integrate the former plan's written-exercise pool
   and local-practice reference here, preserving their different purposes and
   real sources. The guide links each knowledge unit to its corresponding
   training, and training links back to that unit and its glossary entries.

Prepare reusable testing and evaluation material across the overall knowledge
structure of the agreed book, course, or topic. When the learner's level and
specific needs are not yet known, retain broad coverage rather than guessing
which few points will matter. This is preparation for later selection, not an
assignment to complete every item. A bounded request still bounds the source
scope; broad preparation does not expand one question into an entire curriculum.

Keep both forms of technical training explicit. For written exercises, provide
usable questions and separately readable answers, necessary reasoning, relevant
definitions or source locators, and grounds for evaluation. Inspect and adapt
suitable source questions or author source-grounded questions and variations;
label teacher-authored material and verify its premises and solutions. An answer
availability flag or a list of source ranges alone does not complete this
material. Open problems can use reasoned alternatives and comparison criteria
rather than a fabricated unique answer. For experiments/projects, identify the
actual runnable source/workspace, question, useful scope, operations, observations
and expected interpretation, with the model's implementation work and the learner's
supported judgments distinguished. A generic list of possible activities or
links without purpose and use is not prepared training.

Keep the broad prepared material recoverable in this training document. During
practice, remove most of that coverage from the active working set and retain
only the very small subset substantively necessary for the current question and
observed needs. This reduction is required, not merely an option to shorten an
otherwise comprehensive assignment. Strengthen the retained points with diagrams,
worked examples, counterexamples, and smaller supporting exercises for the
remaining difficulties. Preserve links from this adapted selection to the base
material, guide, glossary, and sources; selection need not duplicate the whole
document or delete material useful for a later need. Repair errors in the owning
question or answer. These saved materials should support repeating an item,
changing conditions for another check, or returning after forgetting. Record
actual attempts under the existing Course State contract, without treating an
earlier success as permanent mastery. The teaching-method branch owns how to
use this preparation in the encounter.

For mathematics or technical study with exercises or labs, retain and prepare the applicable
training for the selected study scope even if the learner is not doing it this
turn. Select actual items adaptively during teaching; enough practice to address
an observed gap need not mean completing every available item. Preserve explicit
course exceptions and a deliberate no-practice scope. A source with only one
training form needs only that form, not invented experiments or empty sections.
The learner's choice not to attempt an activity now does not erase the training
design; readiness does not compel immediate execution or gate explanation.
Actual problem wording, solution checks, presentation, attempts and feedback
follow the teaching-method branch. Code, data, notebooks and execution records
stay in their real workspaces; link them rather than rewriting those artifacts.

## Philosophical study: two connected documents

Use the same required independent glossary plus one main document developing
the selected book's arguments, discussions and grounded connections to the
learner, including current research where applicable.
The [philosophy branch](philosophy.md#book-materials-and-research-connection)
owns contextual depth and question-led explanation. Do not create a separate
research-relationship file, per-book plan or progress file, or automatically
apply technical exercise/lab preparation to philosophical text study.
Keep each book's account distinct; a cross-book synthesis does not substitute
for it. A genuinely selected technical activity has its own technical training,
without turning the whole philosophical book into a technical course.

## Relate material to the actual learner

For either kind of main guide, use relevant known purposes, current questions,
interests, existing understanding, and actual environment to decide what needs
explanation and how to make its relations intelligible. Inspect the accessible
source, project, workspace, or current research material when a proposed
connection depends on it. Reuse context already supplied; a complete personal
profile, research plan, or new interview is not a prerequisite. Missing context
limits the personal connection, not the explanation of the subject.

Develop these relations where their concepts and reasons become intelligible.
The environment can supply a real tool, arrangement, activity, or lived problem
that the material helps interpret or change, and whose behavior tests an analogy.
Interests and prior understanding can motivate an entry, suggest a comparison,
or expose a consequential disagreement. Research can give a question to which
the source contributes a method, argument, criticism, or limit. Let these
connections affect the selected scope, examples, depth, and applicable training;
do not append the same relevance statement to every unit or create another
mandatory document. The glossary still grounds terms in their sources.

Preserve the object's independent content and the distinction between the
author's claim, a proposed transfer or analogy, and the learner's experience.
A source can change how the learner understands a purpose, interest, or
environment; it need not merely justify an existing project. Philosophical
understanding can revise a way of seeing oneself or the world without immediate
instrumental use. A concept without a supported personal application remains
worth explaining; do not invent one or infer personal facts from a tool setup.

Use the learner's actual questions, objections, intuitions, and responses to
revise the explanation and its material. When a useful connection becomes
clearer or fails, update its affected passage and examples rather than treating
the initial guide as fixed. This is ordinary situated teaching and material
maintenance; it does not create a separate learner profile or authorize changes
to the environment, research manuscript, or psychological model.

## Research relationships across disciplines

Technical books and courses receive the same attention to research connections
as philosophical sources. Where current research is relevant to a substantial
main guide, inspect the recipient-owned direction and pertinent manuscript,
then explain the meaningful
relationship inside its main flow. An overall orientation can state why the
source matters; develop specific connections after the concepts or content on
which they depend. Research relevance remains substantive rather than a fifth
file, a detached list, or a sentence saying that the source is useful.

Compare the source's actual content and conditions with the current research
question: what corresponds, what differs, what can transfer or must change, and
what proof or evidence remains missing. Distinguish established results,
attributable user judgments and model proposals. A methodological contribution,
criticism or absence of a direct connection is a valid result. Missing research
context limits the claimed connection; do not invent applications or repeat the
same relevance label after every section. An isolated question does not require
a fresh whole-research review.

A source-led learning guide, including its research-relevance account, stays in
course. A report primarily developing the user's research belongs with its
existing manuscript project and may integrate its needed source explanation
there. Choose one owner for the complete main document; a research-relevance
section alone does not require splitting it across vaults. Reuse independent
research comparisons at their existing owners: explain the connection needed
here and link deeper work without maintaining a competing copy.

## Connected presentation and economical maintenance

### Explanatory visuals within the existing documents

The two/three-document arrangement includes explanatory visuals inside both the
glossary's detailed entries and the main guide, beyond the opening concept map.
Neither a substantial glossary nor a substantial guide should become only
prose and formulas after treating that map as sufficient visual support.
Add a fitting amount of source-grounded diagrams,
figures, plots or visual comparisons at the places whose relationships they
clarify. Select their number and form from the material, without a per-section
quota or decorative illustrations.

For example, mathematics can use geometry or a changed-condition comparison;
scientific inquiry can show a model, measurement or evidence relationship;
methods can show data transformations or an algorithm's behavior; engineering
can show components, interfaces or feedback; philosophy can show a consequential
distinction, dependency or competing argument. These are possibilities to
adapt, not mandatory illustration templates. A table of contents in boxes or
another copy of the glossary map does not fulfill a different explanatory need.

Place each visual near the passage it supports, explain its meaningful marks,
relations, assumptions and omissions, and keep the prose connected. Reuse a
verified source figure with attribution and appropriate rights, or create a
faithful explanatory diagram; distinguish a schematic from observed data.
Preserve figures and tables needed to understand actual exercise questions and
to interpret experimental results. Preparing visuals does not authorize running
learner experiments or inventing measurements. Embed the visuals and ordinary
assets in the existing documents/corpus; no additional required reading file or
separate visual guide is created. Verify the actual reading-mode result.

In glossary entries, use visuals to recover the object, defining relationship,
essential condition or contrast, such as a projection, a distribution's shape
or an interface relationship. A concise visual explanation and its necessary
caption can accompany a definition without turning it into a worked exercise.
Keep proofs, extended derivations and long case discussions in the main guide.
Choose the location by the visual's actual contribution, not a blanket rule
that all figures belong only in the guide.

### Connected explanation and maintenance

Use coherent problem/section order and transitions in the main document, not
repeated mandatory slots for every unit. Keep the explanation self-contained
at its intended depth; links support checking and deeper lookup rather than
sending the reader away for every central connection. Align named units across
glossary, guide and, for technical study, training. Use a shallow contents list
and direct section/block links instead of forcing the user through indexes.
The guide's progression identifies the relevant training entry and return point
without repeating the training specification.

Reduce duplicated introductions, source routes, generic instructions, unused
templates and repeated research summaries. Preserve load-bearing definitions,
conditions, source evidence, conceptual depth and the two distinct training
forms. Prepare the actual requested scope rather than a full-library curriculum;
do not interpret concision as omitting requested book coverage or necessary
practice. Reuse verified source pools and update materially changed sections
instead of regenerating all documents after a lesson.

During the next substantive revision, integrate existing plans and reading
references into the main guide and written/lab preparation into the technical
training document, preserving the independent glossary. Repair incoming and
internal links and retain unique content, learner notes, original sources and
existing State. Retire superseded duplicate bodies through their existing
history/ownership route after integration is verified. Do not bulk rewrite the
library merely because this default changed or maintain old and new files as
competing authorities. Existing filenames remain valid locators until integrated.
Existing Course State owns evidenced exposure, attempts, unresolved questions
and resumption; do not create per-book progress files or duplicate State.

## Authoring and readback

When preparing or revising a main guide, make the root teaching contract's
two commitments concrete for that course: the learner develops modeling through
selected worthwhile intuitive attempts and feedback, with model support
throughout inquiry, and enters concepts through relevant conflicts or explanatory
tensions. Name useful source-grounded comparisons, counterexamples or prediction
gaps and the intuitive contribution they can develop. Apply the root's recurring
question, candidate, distinguishing-check, and revision relation within the subject;
the teacher may supply candidates and formalize fragmentary intuitions without
requiring a complete construction before help. A learner's chosen formal
contribution can also develop and evidence that modeling; the model continues
to carry needed detail.
Keep these as adaptable entries within the selected progression, not mandatory
paradoxes, a fixed lesson script, or additional reading/exercise obligations.
Retain the general cognitive account with YinYang; the guide owns its subject-specific
application rather than another psychological portrait. Glossaries continue to
state objective source-grounded meanings. A modeling goal also applies when the
current course deliberately limits practice to concept recognition and reading.

Before materially creating or revising a guide, read the affected material with
the applicable path, existing Global/Course State, resolver and source evidence.
Ordinary explanatory prose does not require the Prompt/Skill authoring lifecycle;
use that owner when actually changing controlling instructions. Read
before and after a permitted write; otherwise retain the exact proposal as
unsaved. Read the actual source edition and chapter structure before glossary
work. Incomplete sources limit coverage rather than licensing invented content.
The final rendering checks below belong to the teacher's own document maintenance
under actual host and Course permissions; they do not authorize learner labs.

## Philosophical book materials

For philosophical text study, [the philosophy branch](philosophy.md#book-materials-and-research-connection)
supplies contextual concept depth and the connected argument/discussion method.
Use the same independent glossary plus main-guide arrangement above. The main
guide develops the book's arguments and current-research connections together;
the glossary restores its conceptual structure and detailed meanings. Apply this
branch's source association, Markdown and saved-result checks to both documents.

## Learner glossary

Prepare and maintain the independent glossary in the recipient's chosen teaching language for substantive study as specified above, repairing gaps in the selected scope before using it. An isolated question can receive definitions directly; this does not waive the glossary for sustained study or requested material preparation. Respect
scope, edition, depth, skips and access. In Web, proactively map terms to
verified passages under the rendering section below, preferring corresponding sources in the recipient's teaching language and
honoring explicit learner exceptions. Verify mappings as
part of authoring rather than deferring them to local repair.

Glossaries support recognition and recovery, teaching connected modeling, and
sources full detail. The model retrieves the needed entry and source connection
when recall is costly; difficulty recalling a name does not establish a gap in
understanding its object. The root teaching contract owns the current example
or visual entry and State owns resumption; neither requires another saved
artifact or an expanded glossary. Each entry conveys defining meaning in
the chosen teaching language, with essential qualifications, original terms, abbreviations
and notation.
Formulas and selected explanatory visuals support meaning rather than replace
it. The visual-support section applies inside detailed entries as well as to
the opening map. Ordinary recall glossaries omit extended worked examples,
assigned exercises, proofs and expanded exposition; teaching
may use them. Philosophy concept tables use the contextual explanation required
by [the philosophy branch](philosophy.md), including a bounded example or contrast
when it is needed to preserve a concept's meaning. Proofs, proof sketches and
assigned exercises still belong outside the glossary. Use enough prose for
recognition and recovery, without a fixed template or length ceiling.

Put an explicit teaching-language role label before each entry's term so the reader can
recognize what kind of thing it is. The following Chinese profile illustrates the roles: 【定义】, 【概念】,
【记号】, 【方法】 and 【算法】. Mathematics retains 【公理】, 【定理】,
【引理】 and 【推论】, with exact definitions, notation, statement conditions and
conclusions. Within mathematics, group other established formal results as
【定理】 rather than 命题/性质, without inventing source numbers; distinguish
definitions from results and keep proofs in the guide.

For other material, choose a meaningful role from the actual entry, such as
【模型】, 【理论】, 【假说】, 【定律】, 【经验结果】, 【机制】, 【指标】, 【工具】, 【协议】,
【组件】, 【接口】, 【设计约束】, 【论点】 or 【区分】. These are examples,
not a required taxonomy or quota. An empirical regularity is not a mathematical
theorem; an author's claim is not an established fact merely because it has a
label. The role states what the entry contributes, while its explanation
preserves evidential status and qualifications. Mixed subjects can use different
roles entry by entry without assigning every term the subject's name.
Use the optional important-entry callouts supported by the rendering section;
ordinary bold labels need no plugin or new callout type.

Select mathematics from the learner's purpose, prior exposure, paths and
inspected sources, including useful applied objects rigorous texts leave
peripheral. Do not copy a proof syllabus or take a mechanical source intersection
or union. Follow verified chapter and section order; when combining sources,
explain a coherent spine and preserve provenance. Keep visible chapter and
section names and shallow organization; label authorized cross-course bridges.

Use actual folders and resolvers; preserve learner content and useful
explanations unless removal is requested. Keep one discoverable glossary entrypoint
(`术语表` in the Chinese profile);
it may link named unit tables grouped under a collapsible folder or headings.
The philosophy branch owns their chronological ordering and complementary maps.
Repair links after renames or removals. Retained handbooks are concept expositions
(`概念详解` in the Chinese profile); essential meanings
and conditions belong in the glossary itself. Update for scope or meaning
changes, errors or recall gaps, not ordinary progress.

## Reading-language companions

When preparing or revising skimming materials, proactively translate selected
passages not readable in the recipient's selected language into that language
through the active teacher; reuse adequate editions or translations. Do not defer this preparation to learner reminders or local models.
Save each language companion beside the relevant source under the
collection's configured source category (`书/` in the Chinese examples), using a recognizable source name and selected range.
Keep the original material unchanged and the skimming reference's reading links
pointing only to that original, with its existing page or section coordinates;
do not add a parallel set of translation links.

The companion identifies its source edition and original page or section
boundaries. Put each original-source link in its corresponding translated
section's heading or immediately beside that section, with the actual page or
section destination. Do not collect these links in a separate top-of-file
source-location index that forces the reader to scroll back and match ranges.
It faithfully translates the selected passages, preserving formulas,
code, examples and necessary figure context, rather than replacing them with a
summary or a new lecture. Check coverage and source correspondence, then follow
the rendering section below for saved-result validation. Report any inaccessible or
unfinished portion. Preparing translations does not establish reading progress
or mastery and does not change Course State.

## Markdown format and rendering

This section owns Markdown form and saved Course materials' Obsidian compatibility. The glossary section above owns pedagogy; the course source and plan own content and progression. Formatting checks do not judge teaching quality, impose entry lengths, remove necessary conditions, or reorganize a book. Its formatting rules do not change the shared ownership, permissions, State, Memory, or route boundaries in the root Skill.

### Language and structure

Write model-facing rules, contracts, `AGENTS.md`, schemas, State, and structured interpretations in English. Write direct learner-facing material and Route prose in the recipient's selected language; the Chinese examples below illustrate one supported profile. Preserve exact quotations, user-authored artifacts, source text, source titles, filenames, and identity-bearing paths. Do not rewrite historical or create-only evidence merely to normalize language.

Use UTF-8 Markdown, one `#` title, and `##` / `###` headings according to real containment without skipped levels. Separate blocks with one blank line; do not use repeated blank lines, manual line breaks, or horizontal rules to simulate structure. Keep terminology, field names, IDs, and owner names stable. Use `-` for unordered lists and numbered lists for real order, dependency, or procedure. Keep one primary proposition per list item and avoid deep nesting. Use tables for compact comparisons across the same dimensions and blockquotes for exact source text or direct quotation.

Use inline code for literal paths, filenames, commands, IDs, schema fields, status values, and exact tokens; use actual links when navigation is intended. Use fenced blocks for multiline code, configuration, protocol examples, literal paths, or diagrams, with the actual language or `text` as appropriate. Keep `AGENTS.md` as a navigable entrypoint rather than copying downstream instructions. Preserve producer-defined machine schemas; apply formatting rules only where the schema leaves form unspecified. Consistent form must not remove distinctions required by an existing contract.

### Write for the actual reader

Put the material itself in learner-facing documents. A preface is useful only for document-specific facts such as actual source editions, selected coverage, or the relationship between primary and supplemental books. Do not copy shared authoring rules into a “purpose”, “usage”, or scope preface: glossary purpose, progress/mastery boundaries, entry-type rules, formula policy, PDF numbering conventions, CSS/plugin names and validation duties belong in their existing instruction owners. Follow them while writing instead of explaining them again to the reader. Do not invent an eligibility condition such as “use only after finishing the course”, or embed changing learner progress and route state in a glossary. Retain useful source information and navigation; omit a preface when it adds no distinct information. The same non-duplication principle applies to model-facing records: retain task-specific facts and references rather than restating shared prompts.

Use ordinary Obsidian Markdown. Inline mathematics uses `$...$`; displayed mathematics uses `$$` on separate lines. Keep a display block out of code fences and separate it from prose with blank lines. In a list, maintain the indentation required by the list. Do not surround intended mathematics with backticks or use `\(...\)` / `\[...\]` as saved Markdown delimiters; these forms need not be recognized as mathematics by the Markdown parser. Keep valid TeX inside recognized math boundaries. A MathJax extension can support extra commands after Markdown recognizes the formula; its presence does not prove that the formula was recognized.

Use headings and normal lists for readable organization. The required concept map is a rendered diagram under the independent-glossary contract, not a text-layout substitute. Choose supported Mermaid, an embedded image or another working graphical format. Check the resulting diagram in the current vault, including its labels and any intended links. A LaTeX environment or plugin installed elsewhere is not evidence of local support.

Resolve links against the actual vault and source file. Wikilinks can address a file, heading, block, or PDF page; Markdown links need correctly encoded destinations. Prefer a sufficiently specific existing path when names collide. In a Markdown table, escape a wikilink's alias separator as `\|`; outside a table use `|`. Verify heading text and physical PDF page positions rather than guessing anchors or printed-to-physical offsets. The PDF++ profile uses one-based physical PDF pages. Verify that `#page=40` reaches page 40 in the recipient's actual reader rather than applying an assumed offset. Verify the displayed destination when the reader or source changes. Code-formatted paths are labels, not clickable links. Escape characters only when their literal display is intended.

### Maintain source-linked reading notes

For a recipient who configures academic callout styling, the optional profile uses `[!definition]`, `[!axiom]`, `[!theorem]`, `[!lemma]`, `[!corollary]`, `[!concept]`, `[!notation]`, `[!algorithm]` and `[!method]`. Use them to emphasize especially important entries; ordinary entries use compact bold teaching-language type labels. Definitions default to plain labels; emphasizing an important definition is optional. Keep the explicit type in callout titles, with color auxiliary. The glossary section above owns selection, meaning and the selected classification; its Chinese profile simplifies proposition/property labels without changing the source's actual statement. No custom headings plugin is required for this presentation.

Apply the glossary contract's exclusion of proofs by substance, regardless of formatting. Relabeling a proof as `【方法】`, `【概念】`, a proof idea, or a sequence of separate entries does not make it glossary content. Keep a result's statement, essential assumptions and defining meaning; omit the argument establishing it, including an expanded proof outline. A clearly identifiable, reusable method may have its own entry explaining its purpose, applicability and central operation, without developing a proof of a particular result. Review adjacent entries together: a derivation split across labels is still a derivation. Do not remove an independently useful concept merely because it is also used in proofs, and do not replace a meaningful entry name with a generic label such as “概念” or “方法”.

When creating or substantively updating a glossary entry or a source-specific explanation, put the source link on the concept name the learner reads. For a distinct mathematical term or result, link that term itself. For dispersed programming practices or several concepts explained together, a concise linked concept-cluster name at the start of the paragraph, followed by a colon and the explanation, is appropriate. Choose a passage that meaningfully supports the explanation; an exact wording match or separate anchor for every incidental sub-concept is unnecessary. A chapter entrance alone does not replace these explanation-level associations. For a local PDF with the configured [PDF++](https://github.com/RyotaUshio/obsidian-pdf-plus)
capability, use a text-selection link: `[[vault/path/source.pdf#page=N&selection=beginItem,beginOffset,endItem,endOffset|concept name]]`. Obtain item indexes and UTF-16 offsets from that exact PDF's current text layer or the reader's copied selection link; never invent coordinates or accept a lexical match without checking its meaning. Use a verified rectangle for a figure or passage whose text layer cannot support a useful selection. Preserve the vault's configured default highlight style; ordinary source association does not modify the PDF file. Do not append separate locator labels or repeatedly display the source filename, book title or same association when the linked concept already carries it.

Write bilingual concept labels in the recipient-language-first order. In the Chinese profile use `中文名（English name）`, not `English name（中文名）`. Link only the main concept name and keep the other-language parenthetical outside the link as ordinary text: `[[source#anchor|计算机科学]]（computer science）`. Preserve the gloss, mathematical notation and surrounding emphasis. Retain an established acronym, code or symbolic name where no useful counterpart is supplied; do not invent an unnatural translation merely to satisfy this display rule.

An English parenthetical must also remain unlinked when it previously had its own separate source link; moving it outside the Chinese link alone is insufficient. Consolidate redundant bilingual links. If an English link carried a genuinely distinct supporting passage, attach that association to an appropriate concise Chinese concept already in the explanation, without appending a new locator label or linking the entire explanatory sentence.

Keep TeX mathematics out of wikilink aliases, where the reader may display literal delimiters. Use a meaningful plain concept name as the link and place its mathematical notation beside it in ordinary Markdown math, for example `[[source#anchor|根号尺度]]（$\sqrt{n}$）`. A readable conventional symbol may be used as plain label text when it preserves the meaning. Do not strip TeX delimiters while leaving commands or changing the mathematics. Check both the link label and adjacent formula in actual reading mode; inspect separately linked English glosses and symbolic labels as well as ordinary bilingual aliases.

Rendering failure patterns and repairs (the placeholder `source#anchor` describes form only and must be replaced by a verified destination):

- A linked bilingual alias such as `[[source#anchor|正则语言的泵引理（pumping lemma）]]` colors the English gloss too. Write `[[source#anchor|正则语言的泵引理]]（pumping lemma）`; a separate linked English parenthetical has the same defect.
- An alias such as `[[source#anchor|根号 $n$ 尺度]]` can display raw dollar signs. Write `[[source#anchor|根号尺度]]（$\sqrt{n}$）`, preserving the intended mathematics in ordinary Markdown outside the link.
- Linking an entire explanatory sentence makes the explanation a large navigation label. Link its meaningful concise Chinese concept and leave the explanatory prose ordinary text.
- A label such as `PDF 物理页 64–67` repeats implementation wording. After verifying the actual destination, display `64–67 页` for a reading range; a glossary entry instead uses its concept-name passage link.

Keep the learner-facing note and its explanation as the destination of the PDF backlink, so hovering or opening the highlight can recover the relevant note context. Link a meaningful introduction or explanation, not every occurrence of a word. Prefer one stable primary book for an entry's mapping; identify a supplemental source when the primary book does not support its content. When corresponding Chinese and English sources are available, map and highlight the actual Chinese passage after verifying the edition and meaning; do not transfer English page numbers or selection coordinates. Use the available source honestly when no corresponding Chinese passage exists. This glossary association does not create a translation companion; the existing skimming-companion contract owns selected-reading translation. A compound or multi-page explanation may need additional passage links with its actual range visible; do not collapse it into a misleading single-page locator. If a concept is a course bridge rather than a claim made by that source, keep that distinction visible and use an existing appropriate supporting passage when available; do not manufacture a source anchor to make coverage look complete. Name genuinely unmapped entries as unfinished instead of treating a page-only
fallback as completed passage mapping. If PDF++ is unavailable, use a verified
page link plus a searchable passage locator and explicitly retain the
selection/highlight limitation; ordinary teaching remains possible.

All page references in model-authored learner materials, including skimming references, learning plans, practice references, glossaries and reading companions, use the actual one-based PDF page position. Display only ordinary page wording such as `第 25 页` or `25–28 页`; do not add `物理页` or `印刷页` labels, printed-page alternatives, or parallel numbering. Match visible page numbers and ranges to the exact PDF and its navigation targets. When revising a printed-page reference, inspect the source and verify the corresponding PDF positions before changing the numbers; removing a label alone is not a conversion. Apply this rule when first producing the material, not as a later manual cleanup. Preserve exact quotations and original source content.

Use page links for reading-window starts and show the verified PDF range in the label under the page convention above; do not highlight entire assigned ranges. For local Markdown sources, use an existing semantic heading or block link. For Web sources, use a stable source URL and an available section anchor. Maintain these associations as part of the existing notes, without asking the learner to perform annotation work or creating another index to maintain. Updating links does not establish reading progress or mastery.

On the changed reading path, verify note-to-source navigation and, for PDF selection links, the actual highlight and its backlink context in Obsidian reading mode. Exercise hover preview or note opening through the current PDF++ interaction. Respect the learner's occupied views; use a task-owned view for validation. If a source changes, repair the affected anchors against the new source rather than retaining stale coordinates.

### Verify changed materials

After saving a glossary, main guide, training document or an existing material being integrated, reread the final bytes and check affected content in its actual vault's **reading mode**. Inspect changed formulas and diagrams for visible mathematics and legibility, including explanatory visuals inside glossary entries and the main guide beyond the opening map. Follow the real study path: guide to the named glossary entry and back, guide to applicable written/external training and back, and source passages/page jumps. Check that the main explanation remains connected without mandatory hopping. Fix observed defects and check the repaired portion. Validate the actual visuals rather than adding unrelated test specimens.

During authoring, use the valid forms above directly. Before delivering a glossary, inspect bilingual and symbolic link labels, separately linked English glosses, surrounding formulas and page labels in the saved result; also read related entries together for proofs disguised by classification. The teacher who writes the material repairs these defects before delivery rather than deferring them to the learner or a later local cleanup. A source-text scan can locate candidates but does not establish rendered correctness or decide whether prose is a proof.

Use available mechanical checks for the mechanically decidable portion: delimiter/fence balance, accidental escaping, existing target files and headings, and resolved links. When the recipient's available Obsidian CLI exposes `links`, `outline`, and
`unresolved`, target the configured vault and changed files. Inspect the current
CLI/tool schema before use; an absent CLI does not establish successful rendering. Existing Linter rules may help formatting, but a clean lint result does not establish MathJax rendering, diagram layout, accurate page destinations, or pedagogical usefulness. Prefer existing Obsidian rendering and link resolution over a second Markdown parser with different semantics. Keep any diagnostic read-only unless the repair is understood; do not automatically rewrite formulas or teaching prose from pattern matches.

Inspect the current display layout and preserve the learner's work when UI access is needed. Available app-native inspection may support the check; an actual reading-mode view remains the reference. If access is unavailable, state precisely which rendering or navigation remains unverified, complete the available checks, and do not report visual success. A teacher with tools may verify its teaching documents; this does not authorize learner lab execution or a new cross-agent coordination system.

### References

- [Obsidian advanced formatting, mathematics and diagrams](https://obsidian.md/help/advanced-syntax)
- [Obsidian internal links](https://obsidian.md/help/links)
- [Obsidian Linter rules](https://github.com/platers/obsidian-linter/blob/master/docs/rules.md)
