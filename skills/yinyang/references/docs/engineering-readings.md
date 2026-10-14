# Engineering readings

[中文](engineering-readings.zh-CN.md) · [Philosophical readings](philosophical-readings.md) · [Psychological readings](psychological-readings.md)

Engineering gives an understanding a form that can run, be observed, and be changed. Begin here with a learning map, the command line, version history, and software design, then follow the question into algorithms, systems, experiments, and physical conditions. Courses, documentation, and source repositories are the main entrances, accompanied by useful textbooks and papers.

Tool pages locate usable tools and Skills; this reading map explains their concepts, methods, and implementation. Being able to invoke a tool does not establish understanding. Documentation can support both learning and reference during actual work.

**Choose a main thread that connects with your starting point.** Begin programming with CS 61A and Composing Programs; algorithms with Princeton's courses and Algorithms; computer systems with CS:APP; and computation theory with MIT and Sipser, then deepen through Arora–Barak as needed. The entries pair courses, books, and documentation and explain their roles. Courses offer teaching, assignments, and projects; books develop connected concepts; documentation provides reference for particular interfaces. A publisher's book record does not imply free full text.

## Find the map and build a usable environment

| Material | Where to begin |
| --- | --- |
| [CS DIY](https://csdiy.wiki/) · [source repository](https://github.com/PKUFlyingPig/cs-self-learning) | An open self-study map initiated by PKUFlyingPig. Read its usage guide, then select programming, mathematics, algorithms, or systems courses from your existing foundation. It is not an official university-wide Peking University curriculum or a requirement to complete every course. |
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

**CS 61A is the foundational entrance here.** It develops an understanding of programs through functions, data, and interpretation. Software construction then organizes existing programming ability into reliable software; it does not replace this foundation.

| Course and book | Content and purpose |
| --- | --- |
| Berkeley [CS 61A](https://cs61a.org/) · John DeNero, [Composing Programs](https://www.composingprograms.com/) | A course paired with its online text. From functions, higher-order functions, recursion, and data abstraction, proceed to objects, interpreters, and different programming approaches. Small exercises and projects make behavior and abstraction boundaries concrete. |
| Abelson and Sussman, [SICP, second edition](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) · [full PDF hosted by MIT](https://web.mit.edu/6.001/6.037/sicp.pdf) | Develop procedural and data abstraction, state, interpreters, and evaluation through Scheme. This original work is an important intellectual background for CS 61A and a deeper reading beyond Composing Programs; the two books are not editions of the same text. |
| [SICP JavaScript adaptation / Comparison Edition](https://sicp.sourceacademy.org/) | Compare the Scheme original with its JavaScript adaptation; the site also links to Interactive SICP JS for reading and evaluation. Choose according to existing language experience and the question; the versions correspond while differing in implementation. |

### Software construction and design

| Courses, notes, and reference books | Content and purpose |
| --- | --- |
| John Ousterhout, [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) | Author's book and course resources. Study complexity, modules, interfaces, and information hiding. “Philosophy” names design thinking in the title; this map locates the book by its software-engineering purpose. |
| [MIT 6.031 Software Construction (2021)](https://web.mit.edu/6.031/www/sp21/) · readings listed on the course page | After programming foundations, study specifications, testing, abstract data types, and concurrency to develop working code into software with explicit behavioral contracts. Its own notes are the paired reading; Ousterhout is adjacent design reading, not presented as this course's assigned textbook. |

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
| MIT [6.045J Automata, Computability, and Complexity (2011)](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/) · course notes and textbook information | Another organization of the foundational field, useful for supplementary topic reading rather than compulsory duplication of 18.404. |
| Sanjeev Arora and Boaz Barak, [Computational Complexity: A Modern Approach](https://theory.cs.princeton.edu/complexity/) | The advanced thread. With a foundation in computational models, reductions, and basic complexity classes, investigate classes, randomness, interactive proofs, and lower bounds. The authors provide a public draft and companion resources; distinguish the draft from the published edition. |
| Boaz Barak, [Introduction to Theoretical Computer Science](https://introtcs.org/public/index.html) | Open textbook connecting models of computation, computability, and efficiency to complexity. Distinguish impossibility, high computational cost, and something not yet implemented by the current program. |

Algorithms and complexity analysis establish properties under formal conditions; real systems also depend on data, implementation, and machine resources. Measured speed and asymptotic complexity can inform one another without being the same evidence.

## Experimental implementation, data, and model assessment

| Documentation or repository | Reading purpose |
| --- | --- |
| [PsychoPy documentation](https://www.psychopy.org/) | Present stimuli, record responses, and organize experimental tasks. Use a simple experiment to understand how measurement enters a program. |
| [jsPsych documentation](https://www.jspsych.org/latest/) · [source repository](https://github.com/jspsych/jsPsych) | Browser-based behavioral experiments. Begin with timelines, plugins, data recording, and timing-accuracy documentation. |
| [Wilson–Collins companion code](https://github.com/AnneCollins/TenSimpleRulesModeling) | Realize the model assessment in [psychological readings](psychological-readings.md#psychological-process-modeling-and-empirical-assessment) through simulation, fitting, and recovery checks. After the code runs, its assumptions and data must still fit the question. |
| Schoukens and Ljung (2019), [Nonlinear System Identification: A User-Oriented Roadmap](https://arxiv.org/abs/1902.00683) | Understand system identification through inputs and outputs, noise, model structure, and validation. Consult as needed; whether natural interaction meets engineering identification conditions requires its own assessment. |
| [Gödel Machine](https://people.idsia.ch/~juergen/goedelmachine.html) and [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954v3) | Two entrances to technical self-improvement research: proof-guided work and empirical evaluation, respectively. Compare their objectives, assumptions, and verification before reading this collection's analogies. |

Research design, constructs, and validity remain in [psychological readings](psychological-readings.md); this page supplies implementation and reproduction knowledge. Connecting implementation resources to a research question is more useful than collecting tool names alone.

## Physical conditions, measurement, and feedback

Engineering realization happens in the material world. Programs run on machines, measurement requires devices and time, and interfaces enter human perception and action. Software abstraction does not remove energy, latency, error, or bodily conditions.

[The Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/) provide open online reading: volume I mainly covers mechanics, radiation, and heat; volume II electromagnetism and matter; volume III quantum mechanics. Enter through the needed concept rather than treating all three volumes as a prerequisite for programming. Feedback and model assessment connect back to the system-identification resources above.

Physics investigates regularities; engineering designs and realizes under those conditions. They connect while retaining their tasks. Psychological activity, philosophical expression, and engineered works can participate in one actual process; this [Trinity](local-source-and-website.md) does not make a running program a complete explanation of the mind's physical realization.
