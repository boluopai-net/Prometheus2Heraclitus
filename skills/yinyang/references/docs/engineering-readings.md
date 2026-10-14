# Engineering readings

[中文](engineering-readings.zh-CN.md) · [Philosophical readings](philosophical-readings.md) · [Psychological readings](psychological-readings.md)

Engineering gives an understanding a form that can run, be observed, and be changed. Begin here with a learning map, the command line, version history, and software design, then follow the question into algorithms, systems, experiments, and physical conditions. Courses, documentation, and source repositories are the main entrances, accompanied by useful textbooks and papers.

Tool pages locate usable tools and Skills; this reading map explains their concepts, methods, and implementation. Being able to invoke a tool does not establish understanding. Documentation can support both learning and reference during actual work.

## Find the map and build a usable environment

| Material | Where to begin |
| --- | --- |
| [CS DIY](https://csdiy.wiki/) · [source repository](https://github.com/PKUFlyingPig/cs-self-learning) | An open self-study map initiated by PKUFlyingPig. Read its usage guide, then select programming, mathematics, algorithms, or systems courses from your existing foundation. It is not an official university-wide Peking University curriculum or a requirement to complete every course. |
| [MIT Missing Semester 2026](https://missing.csail.mit.edu/) | Begin with the shell, command-line environment, and development workflows, using the current course's notes and small exercises. Earlier offerings remain available through the site's archive; keep each year's lesson sequence distinct. |
| William Shotts, [The Linux Command Line](https://linuxcommand.org/tlcl.php) | The author's open books introduce files, permissions, processes, pipes, redirection, and scripts. macOS and Linux share some Unix concepts, but command options and system administration require the target system's documentation. |

A useful beginning is a small project built with model assistance whose inputs, outputs, files, and results you can understand. Follow these entrances when a concept becomes unclear. Engineering reading can interleave with the work already underway.

## Git and GitHub: continuing a work through its changes

| Material | What it addresses |
| --- | --- |
| Chacon and Straub, [Pro Git, second edition](https://git-scm.com/book/en/v2) | Chapters 1–3 introduce repositories, commits, branches, and merges; chapter 10 explains the structure beneath history. Git is the version-control system. |
| [GitHub getting-started documentation](https://docs.github.com/en/get-started) | An entrance to repository pages, collaboration, and hosting. GitHub is a platform built around Git; the two have distinct responsibilities. |
| [GitHub Pull Requests documentation](https://docs.github.com/en/pull-requests) | Compare changes, request reviews, and handle branches and merges. Read the reasons and outcomes of a change, as well as the interface operations. |

## Software design and computer systems

| Material | Reading purpose |
| --- | --- |
| John Ousterhout, [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) | Author's book and course resources. Study complexity, modules, interfaces, and information hiding. “Philosophy” names design thinking in the title; this map locates the book by its software-engineering purpose. |
| [MIT 6.031 Software Construction](https://web.mit.edu/6.031/www/sp21/) | Course materials on specifications, testing, abstract data types, and concurrency, developing working code into software with explicit behavioral contracts. |
| Arpaci-Dusseau and Arpaci-Dusseau, [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) | The authors' open textbook. Virtualization, concurrency, and persistence explain processes, memory, and storage, supplying the systems background behind command-line operations. |

## Algorithms, computation, and complexity

| Material | Reading purpose |
| --- | --- |
| Jeff Erickson, [Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/) | Author's open textbook, notes, and exercises. Study recursion, dynamic programming, greedy methods, and graph algorithms, including correctness and cost. |
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
