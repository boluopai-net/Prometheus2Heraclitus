# Engineering readings

[中文](engineering-readings.zh-CN.md) · [Philosophical readings](philosophical-readings.md) · [Psychological readings](psychological-readings.md)

Engineering gives an understanding a form that can run, be observed, and be
changed. Use this guide for the concepts and sources needed by that realization:
learning maps, command lines, version history, software design, algorithms,
systems, data tools, and physical conditions. Choose the part that helps the
actual work; [harness adaptation](../harness-adaptation.md) explains how its
result connects to the intended collaboration. Courses, documentation, and
source repositories are accompanied by useful textbooks and papers.

Tool pages locate usable tools and Skills; this reading map explains their concepts, methods, and implementation. Documentation can support both learning and reference during actual work.

**Choose a main thread that connects with your starting point.** Suggested
entrances are CS 61A and Composing Programs for programming, Princeton's courses
and Algorithms for algorithms, CS:APP for systems, and MIT and Sipser for
computation theory, with Arora–Barak for further depth. Choose among them according to current interests and questions. Courses offer
teaching, assignments, and projects; books develop connected concepts;
documentation references particular interfaces. Links include course notes, open textbooks, and publisher records.

## Find the map and build a usable environment

| Material | Where to begin |
| --- | --- |
| [CS DIY](https://csdiy.wiki/) · [source repository](https://github.com/PKUFlyingPig/cs-self-learning) | An open self-study map initiated by PKUFlyingPig. Read its usage guide, then select programming, mathematics, algorithms, or systems courses from your existing foundation. |
| Tsinghua's computer-science student association: [SAST skill docs](https://docs.net9.org/) | Chinese introductory skill documentation. Follow the immediate need into problem solving, Git, Linux, editors, languages, and development frameworks, connecting foundational courses with actual work. |
| [MIT Missing Semester 2026](https://missing.csail.mit.edu/) | Begin with the shell, command-line environment, and development workflows, using the current course's notes and small exercises. Earlier offerings remain available through the site's archive; keep each year's lesson sequence distinct. |
| William Shotts, [The Linux Command Line](https://linuxcommand.org/tlcl.php) | The author's open books introduce files, permissions, processes, pipes, redirection, and scripts. macOS and Linux share some Unix concepts, but command options and system administration require the target system's documentation. |
| [Official Vim documentation](https://www.vim.org/docs.php) · [Vim user manual](https://vimhelp.org/usr_toc.txt.html) | Begin with `vimtutor` for modes, movement, and editing, then use the manual for command composition, searching, and substitution; consult `:help` for particular options. This learning entrance can coexist with your own editor choice. |

A useful beginning is a small project built with model assistance whose inputs, outputs, files, and results you can understand. Follow these entrances when a concept becomes unclear. Engineering reading can interleave with the work already underway.

## Git and GitHub: continuing a work through its changes

| Material | What it addresses |
| --- | --- |
| Chacon and Straub, [Pro Git, second edition](https://git-scm.com/book/en/v2) | Chapters 1–3 introduce repositories, commits, branches, and merges; chapter 10 explains the structure beneath history. Git is the version-control system. |
| [GitHub getting-started documentation](https://docs.github.com/en/get-started) | An entrance to repository pages, collaboration, and hosting. GitHub is a platform built around Git; the two have distinct responsibilities. |
| [GitHub Pull Requests documentation](https://docs.github.com/en/pull-requests) | Compare changes, request reviews, and handle branches and merges. Read the reasons and outcomes of a change, as well as the interface operations. |

## Software design and computer systems

### Programming and abstraction: CS 61A and SICP

**CS 61A is the foundational entrance here.** It develops an understanding of programs through functions, data, and interpretation. Software construction then organizes existing programming ability into reliable software.

| Course and book | Content and purpose |
| --- | --- |
| Berkeley [CS 61A](https://cs61a.org/) · John DeNero, [Composing Programs](https://www.composingprograms.com/) | A course paired with its online text. From functions, higher-order functions, recursion, and data abstraction, proceed to objects, interpreters, and different programming approaches. Small exercises and projects make behavior and abstraction boundaries concrete. |
| Abelson and Sussman, [SICP, second edition](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) · [full PDF hosted by MIT](https://web.mit.edu/6.001/6.037/sicp.pdf) | Develop procedural and data abstraction, state, interpreters, and evaluation through Scheme. This original work is an important intellectual background for CS 61A and a deeper reading beyond Composing Programs. |
| [SICP JavaScript adaptation / Comparison Edition](https://sicp.sourceacademy.org/) | Compare the Scheme original with its JavaScript adaptation; the site also links to Interactive SICP JS for reading and evaluation. Choose according to existing language experience and the question; the versions correspond while differing in implementation. |

### Software construction and design

| Courses, notes, and reference books | Content and purpose |
| --- | --- |
| John Ousterhout, [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) | Author's book and course resources. Study complexity, modules, interfaces, and information hiding. “Philosophy” names design thinking in the title; this map locates the book by its software-engineering purpose. |
| [MIT 6.031 Software Construction (2021)](https://web.mit.edu/6.031/www/sp21/) · readings listed on the course page | After programming foundations, study specifications, testing, abstract data types, and concurrency to develop working code into software with explicit behavioral contracts. Its own notes are the paired reading; Ousterhout is adjacent design reading. |

### From programs to machines, operating systems, and networks

| Course and book | Content and purpose |
| --- | --- |
| CMU [15-213 Introduction to Computer Systems](https://www.cs.cmu.edu/~213/) · Bryant and O’Hallaron, [Computer Systems: A Programmer’s Perspective, 3rd edition](https://csapp.cs.cmu.edu/3e/home.html) | CS:APP introduces data representations, machine code, the memory hierarchy, linking, processes, virtual memory, and system I/O from a programmer's perspective. The authors' site also provides labs and student resources. |
| Arpaci-Dusseau and Arpaci-Dusseau, [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) | The authors' open textbook and projects. Understand operating systems through virtualization, concurrency, and persistence, selecting chapters alongside a systems course. |
| MIT [6.1810 Operating System Engineering (2025)](https://pdos.csail.mit.edu/6.1810/2025/) · [the same year's xv6 text and source entrance](https://pdos.csail.mit.edu/6.828/2025/xv6.html) | Connect text, implementation, and labs through a small RISC-V operating system. Match the text and labs to the course year and source version. |

## Algorithms, computation, and complexity

### Algorithms: begin with Princeton's courses and textbook

| Course and book | Content and purpose |
| --- | --- |
| Princeton [Algorithms, Part I](https://www.coursera.org/learn/algorithms-part1) and [Part II](https://www.coursera.org/learn/algorithms-part2) · Sedgewick and Wayne, [Algorithms, 4th edition](https://algs4.cs.princeton.edu/home/) | The principal entrance. Courses and book develop sorting, searching, graphs, strings, and their data structures. The companion site supplies code, exercises, notes, and course links. The courses primarily use Java. |
| Berkeley [CS170](https://cs170.org/) · Dasgupta, Papadimitriou, and Vazirani, [Algorithms (DPV), author resources](https://cseweb.ucsd.edu/~dasgupta/book/index.html) | Deepen algorithm design, correctness, and complexity arguments through divide-and-conquer, greedy methods, dynamic programming, linear programming, and reductions. This is a different Algorithms from the Princeton textbook. |
| MIT [6.006 Introduction to Algorithms (2020)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) · CLRS, [Introduction to Algorithms, 3rd edition](https://mitpress.mit.edu/9780262033848/introduction-to-algorithms/) | The course supplies its own notes and lists CLRS's third edition as supplementary reading. Use it to strengthen mathematical modeling, data structures, correctness, and asymptotic analysis. A [4th edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) is also available; match chapter and exercise numbers when using it. |
| Jeff Erickson, [Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/) | Author's open textbook, notes, and exercises. Study recursion, dynamic programming, greedy methods, and graph algorithms, including correctness and cost. |

### Computation theory: MIT and Sipser, then Arora–Barak

| Course and book | Content and purpose |
| --- | --- |
| MIT [18.404J Theory of Computation (2020)](https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/) · Michael Sipser, [Introduction to the Theory of Computation, 3rd edition](https://math.mit.edu/~sipser/book.html) | The foundational thread. The course offers lectures and exercises; the book moves from automata and computability into complexity. The author's book page provides edition information and errata. Match exercise numbers to the edition used by the course. |
| MIT [6.045J Automata, Computability, and Complexity (2011)](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/) · course notes and textbook information | Another organization of the foundational field, useful for supplementary topic reading. |
| Sanjeev Arora and Boaz Barak, [Computational Complexity: A Modern Approach](https://theory.cs.princeton.edu/complexity/) | The advanced thread. With a foundation in computational models, reductions, and basic complexity classes, investigate classes, randomness, interactive proofs, and lower bounds. The authors provide a public draft and companion resources; distinguish the draft from the published edition. |
| Boaz Barak, [Introduction to Theoretical Computer Science](https://introtcs.org/public/index.html) | Open textbook connecting models of computation, computability, and efficiency to complexity. Distinguish impossibility, high computational cost, and something not yet implemented by the current program. |

Algorithms and complexity analysis establish properties under formal conditions; real systems also depend on data, implementation, and machine resources. Speed measurements and asymptotic analysis offer two scales of observation.

### Original sources behind this collection's comparisons

| Source | Connection to the essays |
| --- | --- |
| A. M. Turing (1936), [On Computable Numbers, with an Application to the Entscheidungsproblem](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf), especially §6 | The universal machine supplies the formal reference for the interpreter analogy in [Metaphor and personal modeling](metaphor-and-self-revision.md). |
| Thomas R. Gruber (1993), [A Translation Approach to Portable Ontology Specifications](https://tomgruber.org/writing/ontolingua-kaj-1993.pdf), §§1–2 | Objects, relations, and shared conceptualization in knowledge representation. Read alongside the engineering ontology developed in [Stealing fire and cultivating creative capacity](stealing-fire.md); that essay extends the source into its own account. |
| Donald E. Knuth, [Literate Programming](https://www-cs-faculty.stanford.edu/~knuth/lp.html) | The established practice of organizing explanation and program code together. Compare its technical purpose with this collection's broader literary natural-language programming. |

## Self-improvement research

| Documentation or paper | Content |
| --- | --- |
| [Gödel Machine](https://people.idsia.ch/~juergen/goedelmachine.html) and [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954v3) | Two entrances to technical self-improvement research: proof-guided work and empirical evaluation, respectively. Compare their objectives, assumptions, and verification before reading this collection's analogies. |

## Physical conditions, measurement, and feedback

Engineering realization happens in the material world. Programs run on machines, measurement requires devices and time, and interfaces enter human perception and action. Energy, latency, error, and bodily conditions shape actual use.

[The Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/) provide open online reading: volume I mainly covers mechanics, radiation, and heat; volume II electromagnetism and matter; volume III quantum mechanics. Each volume develops its topics through concepts, derivations, and examples.

Physics investigates regularities; engineering designs and realizes under those
conditions. [The trinity of philosophy, psychology, and engineering](local-source-and-website.md) develops their connection
with philosophy and psychology.

## Language models, retrieval, and data tools

Books, courses, and official tool references for language models, databases, and retrieval systems.

| Book or course | Content |
| --- | --- |
| Jurafsky and Martin, [Speech and Language Processing, third-edition online draft](https://web.stanford.edu/~jurafsky/slp3/) | A natural-language-processing and language-model textbook covering tokens, embeddings, context, information extraction, time, discourse, and retrieval. The official site provides the text and slides; the Agents chapter remains unwritten in the August 19, 2026 release. |
| [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) | An online course introducing models, messages, tools, and observations following actions. |
| [Agent Skills overview](https://agentskills.io/home) · [Specification](https://agentskills.io/specification) | An open format for organizing instructions, scripts, and reference resources. |

| Tool or project | General purpose and official source |
| --- | --- |
| [SQLite](https://www.sqlite.org/docs.html) | An embedded relational database supporting SQL queries and transactions. |
| [sqlite-utils](https://sqlite-utils.datasette.io/) · [Datasette](https://datasette.io/) | The former supplies command-line and Python interfaces for importing and manipulating SQLite data; the latter provides database browsing, queries, and JSON interfaces. |
| [PostgreSQL](https://www.postgresql.org/docs/) · [pgvector](https://github.com/pgvector/pgvector) | A relational database and its vector-similarity-search extension. |
| [Hindsight](https://github.com/vectorize-io/hindsight) | An agent memory and retrieval system with retain, recall, and reflect capabilities. |
| [Graphiti](https://github.com/getzep/graphiti) | Temporal knowledge graphs for agents. |
| [Mem0](https://github.com/mem0ai/mem0) | Persistent-memory components for agents and applications. |
| [Letta](https://github.com/letta-ai/letta) | A platform for agents with persistent state and memory management. |

See each project’s documentation for its capabilities and operating requirements.
