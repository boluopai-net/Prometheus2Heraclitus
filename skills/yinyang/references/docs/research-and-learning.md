# Advice for Research and Learning

Begin with a question, paper, set of materials, or research idea. Let the model combine domain knowledge, research methods, and actual tools into work you can read, inspect, and revise. You express purposes, raise objections, and judge meaning; the model finds sources, develops methods, computes, writes, and maintains the working environment. [Using the Tools](https://boluopai.net/getting-started/en/) covers subscriptions, Chinese discovery, files, and connections. This page concentrates on more involved research and learning arrangements.

## Capability map

<nav class="guide-navigation" aria-label="Page navigation" markdown="1">

1. [Choose capabilities from the question](#research-map)
2. [Domain experts and research methods](#domain-methods)
3. [Literature and evidence](#evidence)
4. [Models, computation, and visualization](#models)
5. [Writing and delivery](#writing)
6. [Learning and explanation](#learning)
7. [Workspaces and continued maintenance](#workspace)

</nav>

You need not memorize tool names. Give this page to a model and ask it to choose methods for the question, explain the distinctions you need to understand, and carry out the work. These entrances help you remember possibilities and inspect results; the model selects from current materials and conditions.

<a id="research-map"></a>

## 1. Choose capabilities from the question

| What you want to advance | Capabilities to combine | Results to expect |
| --- | --- | --- |
| Understand a concept, paper, or interdisciplinary problem | Teaching methods, domain profiles, original textbooks and papers, concept maps and demonstrations | Grounded explanations, important distinctions, traceable originals, and further development of your questions. |
| Find and compare research | Search and paper retrieval, literature review, metadata and citation management | Relevant studies, acquired full texts and versions, a comparison, and explicit acquisition or knowledge gaps. |
| Develop an intuition into a research question | Domain references, hypothesis generation, critical thinking, study design and method comparison | A clear question, competing explanations, needed observations, and results that could discriminate between them. |
| Construct or examine a model | Formal methods, symbolic computation, graphs, simulation, statistics, machine learning and visualization | Explicit assumptions, runnable computation, results and scope, with model comparisons where useful. |
| Produce a paper, report, or shareable explanation | Academic writing, citation checking, figures, typesetting, review and revision | Maintained sources, readable deliverables, traceable figures and references, and unresolved questions. |

Work can move back and forth among these activities. New evidence can change a question; computation can expose inadequate assumptions; writing can reveal a confused concept. Address the relationship currently blocking progress and select methods for it, without requiring every task to complete a research pipeline.

<a id="domain-methods"></a>

## 2. Combine Scientific Agents and Scientific Agent Skills

The names are similar, but the projects offer different contributions. [K-Dense Scientific Agents](https://github.com/K-Dense-AI/scientific-agents) organizes expert-thinking references by discipline and profession, helping a model attend to a field's important questions, concepts, assumptions, judgments, and common mistakes. [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) provides more concrete capabilities, such as literature retrieval, experimental design, statistics, machine learning, scientific computing, and figures. Packages may include scripts, examples, and interface documentation.

The former helps ask which disciplinary perspectives clarify a problem; the latter helps develop work through particular methods. This is not a rigid partition: profiles discuss tools, and methods include reasoning. Both remain answerable to current sources and results. A label does not make a model a qualified human expert.

For a process changing over time, relevant domain, dynamical-systems, and statistical references might first clarify states, observations, timescales, and competing explanations. Data and questions then guide graph analysis, state-space models, simulation, or statistical methods. If you only want to understand feedback versus correlation, a teacher can draw on the same resources to explain and demonstrate the distinction without creating a complete experiment.

**This week's practical improvement connected the full domain reference library and selected methods to entrances the model can discover proactively.** As of 2026-10-24, the example environment retains all 503 Scientific Agents profiles and exposes 63 selected research-workspace Skills, including other sources and user-authored methods. The Chinese “domain and research methods library” connects relevant resources to local and Web teachers. Models can find an index, read suitable originals, and combine methods. These counts describe that date's available material; consult the actual catalog for later changes.

Keeping the full reference library supports later retrieval while each task reads useful portions. Expert profiles are resources to borrow, not a requirement to launch hundreds of subagents. An available method package does not mean every software dependency, model weight, GPU environment, or external account is installed. The model checks and prepares the actual project's dependencies when execution needs them.

You can ask:

> Help me understand this question from relevant disciplinary perspectives and compare suitable methods. Explain what each answers, then use the available tools for the needed analysis; do not make me choose Skill names first.

<a id="evidence"></a>

## 3. Make literature usable as evidence

Source work includes discovery, acquisition, checking, comparison, and connection to the question. Search finds leads; paper and metadata tools locate authors, titles, dates, DOIs, and versions; full-text reading enables examination of arguments, methods, and results. Abstracts, reviews, and primary studies can work together while supporting different judgments.

Ask the model for a connected source bundle: search around the question, reuse existing material, deduplicate and check records, obtain available full texts, and prepare a comparison. State each study's object, material, method, main result, limitations, and relevance. Retain specific acquisition gaps. When a preprint differs from the published article, preserve their version relationship. Connect books, papers, supplements, code, and data so revised judgments can return to their sources.

For larger investigations, methods such as `paper-lookup`, `literature-review`, and `citation-management` can complement general search, paper retrieval, and an existing library. Choose services by current coverage and actual accessibility; one successful query establishes that particular route. A reference manager can help, while files and BibTeX may already suffice without adding another service.

For continuing work, distinguish paper and book acquisition, discovery of new tools, and updates to selected methods. They respectively enrich evidence, find capabilities, and maintain adopted sources. Choose a useful cadence, record new material's contribution relative to what is already available, and return useful full texts, code, and methods to their established libraries. A saved schedule and an actual completed run need separate checks.

<a id="models"></a>

## 4. Connect research ideas with computation, data, and visualization

Have the model explain the object being studied, observed material, representation chosen for computation, and intended judgment. Symbolic reasoning, statistical estimation, machine learning, and simulation can cooperate while supporting different conclusions. Derivation establishes consequences under assumptions; statistics describes relationships in material; prediction needs appropriate held-out evaluation; simulation shows how specified rules evolve. Their combination still requires an account of the correspondence between model and real object.

| Needed work | Example methods and tools |
| --- | --- |
| Equations, relations, events, and graphs | SymPy for symbolic computation, NetworkX for graphs, and SimPy for discrete-event simulation; choose the representation by the question. |
| Statistics and uncertainty | Common models in statsmodels; PyMC, PyTensor, and ArviZ for probabilistic modeling, computation, and diagnostics. |
| Change over time and machine learning | Choose time-series methods, scikit-learn, explanation methods, or genuinely needed deep and graph learning from the material. |
| Data preparation and checks | Examine missingness, duplicates, units, time, individuals, and grouping, then choose processing methods suited to scale. |
| Research figures and explanatory visuals | Standard plotting for axes, units, and uncertainty; concept maps, workflows, or interactive demonstrations for structure and conditions. |

These are entrances in the selected library, not a simultaneous installation list. Begin with computation that answers the current question and expand from the result. Synthetic data can check implementation; claims about reality need corresponding observations and research design. A working script does not also validate a scientific explanation.

Give visuals a concrete contribution. Keep assumptions, inputs, and outputs adjacent when comparing methods. Let readers change conditions and inspect trajectories when explaining dynamics. Deliver research results with data, code, and exportable figures rather than replacing quantitative charts with generated illustrations. Interactive tools support intuition and formal figures support inspection and communication; both can come from one analysis.

<a id="writing"></a>

## 5. From maintained sources to readable, revisable delivery

Organize questions, arguments, analyses, and citations in a maintained source, with the model carrying authorship, rewriting, formatting, and technical detail. You can begin with speech, notes, a sensed mismatch, or a draft needing revision rather than supplying a complete first draft. The model explains consequential arguments and changes so you can judge whether the work expresses your purpose.

The example workspace mainly authors in Markdown and LaTeX, with PDF as a common reading and submission output. Use LaTeX when equations, proofs, or a venue template benefit from it. Use document tools when collaborators supply Word or a venue requires it. Software and formats serve the work; an upstream Skill's default output does not determine every project's format.

Combine academic writing, citation management, scientific figures, venue formats, review, and response-to-review methods as needed. Check that cited works exist, sources support the claims, figures correspond to current results, and exported pages are readable. Retain editable sources and versioned deliverables. A changed calculation or definition should lead to its affected figure, prose, and reference.

Submission advice, preparing materials, actual submission, and outbound communication are different actions. The model follows the task's existing authorization to its relevant boundary and explains results, grounds, and remaining judgments. Fluent prose does not establish a sound research conclusion.

<a id="learning"></a>

## 6. A teacher makes specialist methods approachable

Domain references help the teacher see a question's structure, while concrete methods supply examples and runnable demonstrations. The teacher retains the learning purpose, your existing understanding, explanation, and conversational continuity. You can ask why something is defined that way, request a diagram, or compare it with an earlier idea. The model develops an answer from relevant originals and methods. Research resources can support learning without making every lesson a research project.

**Sustained learning needs material that is independently readable and revisable through dialogue.** The example Teacher method distinguishes its objects: philosophy and textual study usually use a glossary plus an argument and research guide; technical courses usually use a glossary, a study and research guide, and exercises and experiments. Glossaries begin with a concept map and throughline. Main texts develop questions, reasons, conditions, and distinctions coherently. Prepare training according to the actual material; availability does not require immediate completion. An isolated question can receive an explanation without generating a full file set first.

Philosophy and intellectual history retain arguments, contexts, objections, and conceptual change. Technical learning connects concepts, mathematics, code behavior, and actual conditions. At relevant arguments, connect the reader's questions, understanding, interests, and lived or research experience, showing what transfers and which conditions differ. An introductory claim of relevance is insufficient, and each connection need not become another document. Keep original claims, model-proposed analogies, and personal experience distinguishable.

**A written explanation and your understanding are two results that need to connect.** Saved guides retain structure and sources. Current teaching adapts depth, examples, and entrances through questions, intuition, objections, and feedback, returning useful understanding to the material. Leave room for your own judgments and corrections when practice is wanted; the model can carry derivation, code, and organization when a finished contribution is wanted. Exhaustive terminology recall or personal execution of every detail is not a prerequisite for understanding.

Reading arrangements can be concrete. In Obsidian, connect original PDFs, glossaries, guides, and applicable exercises with [backlinks](https://obsidian.md/help/plugins/backlinks), [PDF page embeds](https://obsidian.md/help/embeds), and [split tabs](https://obsidian.md/help/tabs). Video material retains timestamps and spoken text, returning to audio when sound matters. For a fixed source set, [NotebookLM / Gemini Notebook](https://support.google.com/gemininotebook/answer/16179559) can support questions and citation checking. Choose images, sound, and interactive demonstrations for their contribution to the current understanding.

First make material readable, comparable, and traceable. Add classification, tags, or a knowledge base when actual retrieval or continuation difficulties justify them. Tools carry memory, retrieval, and layout while readers retain room to read, distinguish, question, try, and respond.

<a id="workspace"></a>

## 7. Keep workspaces and capability explanations usable together

**Tools, research projects, original material, and deliverables have stable homes.** The example environment keeps shared research tools in one workspace, with each study owning its repository, code, dependencies, and experiments. Books and papers remain in the source library; readable deliveries enter the manuscript space with source-version provenance. Existing manuscripts need not all move. Models locate the right owner, maintain connections, and handle versions; people need not memorize every directory.

A readable current account should explain what capabilities exist, when to use them, where to start, what comes back, and which methods remain optional references. The model-facing technical entrance additionally identifies sources, dependencies, and execution. Both connect to the same work. A model's ability to search configuration is no reason to omit the human explanation.

This week's improvements connected domain references, concrete methods, local and Web teaching entrances, and discovery within projects. Selected sources also entered existing weekly maintenance. Compare updated content with local adaptations, verify affected methods, and revise the explanation. Dependencies not needed yet can remain uninstalled; updates do not silently enable intentionally disabled capabilities. A catalog name should lead to an intelligible distinction between a readable reference, an available method, and a tool already exercised.

Ask the model to revisit relevant History, project changes, and actual outputs when useful: has a new capability reached use, has a description become stale, and can an earlier entrance still continue the work? Summaries locate evidence; original files and actual operations verify it. Turn useful improvements into a human-readable account without copying every log into the page.

Return to [Using the Tools](https://boluopai.net/getting-started/en/) for the general arrangement, or bring the current research or learning question to the model and select a useful combination from here.
