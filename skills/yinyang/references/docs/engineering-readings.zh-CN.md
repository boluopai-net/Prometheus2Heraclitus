# 工程阅读

[English](engineering-readings.md) · [哲学阅读](philosophical-readings.zh-CN.md) · [心理阅读](psychological-readings.zh-CN.md)

工程使理解取得可运行、可观察、可修改的形式。本指引定位实现所需的概念与来源：
学习地图、命令行、版本历史、软件设计、算法、系统、数据工具和物理条件。
选择有助于实际工作的部分；[环境适配](../harness-adaptation.zh-CN.md)说明结果怎样连接
预期协作。课程、文档和源仓库配有有用的教材与论文。

工具页帮助找到可用的工具和 Skills；这张阅读地图解释它们背后的概念、方法与实现。文档既支持学习，也可在实际工作中按需查阅。

**选择能接上自己起点的主线。**建议入口包括：程序设计读 CS 61A 与 Composing Programs，
算法读普林斯顿课程与 Algorithms，系统读 CS:APP，计算理论读 MIT 与 Sipser，
再按需深入 Arora–Barak。可以按当前兴趣与问题选择。
课程提供讲授、作业与项目，教材展开连贯概念，文档说明具体接口。链接包含课程讲义、开放教材和出版社书目。

## 先找到地图，再做出一个可用环境

| 材料 | 从哪里开始 |
| --- | --- |
| [CS 自学指南](https://csdiy.wiki/) · [源仓库](https://github.com/PKUFlyingPig/cs-self-learning) | PKUFlyingPig 发起的开放自学地图。先读使用指南，再按已有基础选程序设计、数学、算法、系统等课程。 |
| 清华大学计算机系学生科协：[SAST skill docs](https://docs.net9.org/) | 中文技能引导文档。按具体需要进入问题解决、Git、Linux、编辑器、编程语言与开发框架；适合连接基础课程和实际工作。 |
| [MIT Missing Semester 2026](https://missing.csail.mit.edu/) | 从 shell、命令行环境和开发工作流进入，跟随课程当期讲义做小练习。已有版本通过网站的历年入口查阅。 |
| William Shotts，[The Linux Command Line](https://linuxcommand.org/tlcl.php) | 作者提供的开放书籍。学习文件、权限、进程、管道、重定向与脚本。macOS 和 Linux 共享部分 Unix 概念，具体命令选项与系统管理仍要查看目标系统文档。 |
| [Vim 官方文档](https://www.vim.org/docs.php) · [Vim 用户手册](https://vimhelp.org/usr_toc.txt.html) | 先用 `vimtutor` 理解模式、移动与编辑，再按用户手册学习组合命令、搜索与替换；具体选项查 `:help`。它是编辑工具的学习入口，可以与自己的编辑器选择并存。 |

一个合适的起点是让模型协助建立小项目，自己看懂它的输入、输出、文件和运行结果；遇到不理解的概念，沿这些入口补读。工程阅读可以与正在做的事交错发生。

## Git 与 GitHub：让作品和修改能够接续

| 材料 | 解决的问题 |
| --- | --- |
| Chacon 与 Straub，[Pro Git，第二版](https://git-scm.com/book/zh/v2) | 第 1–3 章理解仓库、提交、分支与合并；需要解释历史结构时读第 10 章。Git 是版本控制系统。 |
| [GitHub 入门文档](https://docs.github.com/en/get-started) | 仓库页面、协作和托管的入口；GitHub 是围绕 Git 的平台，两者各有职责。 |
| [GitHub Pull Requests 文档](https://docs.github.com/en/pull-requests) | 比较修改、提出评审、处理分支与合并。包含变更的理由、结果与操作说明。 |

## 软件设计与计算机系统

### 程序设计与抽象：CS 61A 和 SICP

**CS 61A 是这里的基础入口。**它帮助理解程序如何由函数、数据与解释过程构成；后面的软件构造关注怎样把已有编程能力组织成可靠的软件。

| 课程与教材 | 内容与用途 |
| --- | --- |
| Berkeley [CS 61A](https://cs61a.org/) · John DeNero，[Composing Programs](https://www.composingprograms.com/) | 课程与在线教材配对。从函数、高阶函数、递归与数据抽象，进入对象、解释器和不同编程方式。配合课程的小练习与项目，看清程序的行为和抽象边界。 |
| Abelson 与 Sussman，[SICP 第二版](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) · [MIT 提供的全文 PDF](https://web.mit.edu/6.001/6.037/sicp.pdf) | 用 Scheme 展开过程与数据抽象、状态、解释器和求值。它是 CS 61A 思想背景的重要原典，可以在 Composing Programs 之外深入阅读。 |
| [SICP JavaScript 改写与 Scheme 对照版](https://sicp.sourceacademy.org/) | 对照 Scheme 原版与 JavaScript 改写版；站点也链接到可交互阅读与求值的 Interactive SICP JS。选择语言时看已有经验和想理解的问题；版本之间有对应关系，也有实现差异。 |

### 软件构造与设计

| 课程、讲义与参考书 | 内容与用途 |
| --- | --- |
| John Ousterhout，[A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) | 作者书目与课程材料。围绕复杂性、模块、接口和信息隐藏理解软件设计。「哲学」在书名中指设计思想，这里按软件工程用途收录。 |
| [MIT 6.031 Software Construction（2021）](https://web.mit.edu/6.031/www/sp21/) · 同页逐讲阅读 | 在编程基础之后学习规格、测试、抽象数据类型与并发，把「代码能运行」发展为有明确行为契约的软件。这里以课程自带讲义配套；Ousterhout 的书是相邻的设计阅读。 |

### 从程序看到机器、操作系统与网络

| 课程与教材 | 内容与用途 |
| --- | --- |
| CMU [15-213 Introduction to Computer Systems](https://www.cs.cmu.edu/~213/) · Bryant 与 O’Hallaron，[Computer Systems: A Programmer’s Perspective，第 3 版](https://csapp.cs.cmu.edu/3e/home.html) | 即 CS:APP／深入理解计算机系统。从程序员的视角理解数据表示、机器代码、内存层次、链接、进程、虚拟内存与系统 I/O。作者站另有实验与学生资源。 |
| Arpaci-Dusseau 与 Arpaci-Dusseau，[Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) | 作者开放教材及项目。从虚拟化、并发与持久化理解操作系统；可以配合系统课程按章节阅读。 |
| MIT [6.1810 Operating System Engineering（2025）](https://pdos.csail.mit.edu/6.1810/2025/) · [同年 xv6 教材与源码入口](https://pdos.csail.mit.edu/6.828/2025/xv6.html) | 通过一个小型 RISC-V 操作系统连接文字、实现与实验。教材和实验需要匹配课程年份与源码版本。 |

## 算法、计算与复杂性

### 算法：从普林斯顿课程与教材开始

| 课程与教材 | 内容与用途 |
| --- | --- |
| Princeton [Algorithms, Part I](https://www.coursera.org/learn/algorithms-part1) 与 [Part II](https://www.coursera.org/learn/algorithms-part2) · Sedgewick 与 Wayne，[Algorithms，第 4 版](https://algs4.cs.princeton.edu/home/) | 主入口。课程与教材围绕排序、查找、图、字符串等数据结构与算法展开；教材配套站提供代码、练习、讲义及课程链接。注意课程主要使用 Java。 |
| Berkeley [CS170](https://cs170.org/) · Dasgupta、Papadimitriou 与 Vazirani，[Algorithms（DPV）作者材料](https://cseweb.ucsd.edu/~dasgupta/book/index.html) | 进一步学习算法设计、正确性与复杂度论证，按问题进入分治、贪心、动态规划、线性规划和归约。这是另一部同名的 Algorithms。 |
| MIT [6.006 Introduction to Algorithms（2020）](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) · CLRS，[Introduction to Algorithms，第 3 版](https://mitpress.mit.edu/9780262033848/introduction-to-algorithms/) | 课程有独立讲义，并把 CLRS 第三版列为补充参考；可用于补强数学建模、数据结构、正确性与渐近分析。另有[第 4 版](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)，使用时核对章节和题号。 |
| Jeff Erickson，[Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/) | 作者开放教材、讲义与习题。理解递归、动态规划、贪心与图算法，练习说明正确性和成本。 |

### 计算理论：MIT、Sipser，再到 Arora–Barak

| 课程与教材 | 内容与用途 |
| --- | --- |
| MIT [18.404J Theory of Computation（2020）](https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/) · Michael Sipser，[Introduction to the Theory of Computation，第 3 版](https://math.mit.edu/~sipser/book.html) | 基础主线。课程提供讲授和习题，教材从自动机、可计算性进入复杂性；书的作者页面提供版本说明与勘误。使用习题时按课程所用版本核对题号。 |
| MIT [6.045J Automata, Computability, and Complexity（2011）](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/) · 课程讲义与教材说明 | 同一基础领域的另一套课程组织，适合按主题补读。 |
| Sanjeev Arora 与 Boaz Barak，[Computational Complexity: A Modern Approach](https://theory.cs.princeton.edu/complexity/) | 进阶主线。已有计算模型、归约与基本复杂性类基础后，再深入复杂性类、随机性、交互证明与下界等问题。作者页面提供公开草稿和配套材料；草稿与出版版应分别标识。 |
| Boaz Barak，[Introduction to Theoretical Computer Science](https://introtcs.org/public/index.html) | 开放教材。从计算模型、可计算性和效率进入复杂性问题。区分做不到、计算代价高和现有程序尚未实现。 |

算法和复杂性分析回答形式条件下的性质；实际系统还受数据、实现和机器资源影响。实际速度测量与渐近复杂度分析提供两种观察尺度。

### 本文集相关比较的原始来源

| 来源 | 与文章的关系 |
| --- | --- |
| A. M. Turing（1936），[On Computable Numbers, with an Application to the Entscheidungsproblem](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf)，尤其第 6 节 | 通用机器为[从个人哲学到个人模型](metaphor-and-self-revision.zh-CN.md)中的解释器类比提供形式参照。 |
| Thomas R. Gruber（1993），[A Translation Approach to Portable Ontology Specifications](https://tomgruber.org/writing/ontolingua-kaj-1993.pdf)，第 1–2 节 | 知识表示中的对象、关系与共享概念化。可对照[窃火与创造能力的培养](stealing-fire.zh-CN.md)发展的工程本体阅读；后者进一步提出自己的解释。 |
| Donald E. Knuth，[Literate Programming](https://www-cs-faculty.stanford.edu/~knuth/lp.html) | 把解释与程序代码组织在一起的既有实践。比较它的技术用途与本文集更广义的文学自然语言编程。 |

## 自改进研究

| 文档或论文 | 内容 |
| --- | --- |
| [Gödel Machine](https://people.idsia.ch/~juergen/goedelmachine.html) 与 [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954v3) | 两类自改进技术研究入口：前者围绕证明引导，后者围绕经验评估。比较其目标、假设和验证方式，再读本文集中的相关类比。 |

## 物理条件、测量与反馈

工程实现发生在物质世界中：程序要在机器上运行，测量需要设备和时间，界面也要进入人的感知与行动。能量、延迟、误差和身体条件共同影响实际使用。

[费曼物理学讲义](https://www.feynmanlectures.caltech.edu/)提供物理概念的开放在线阅读：第一卷侧重力学、辐射和热，第二卷侧重电磁与物质，第三卷讨论量子力学。各卷提供相应主题的概念、推导与例子。

物理学研究规律，工程在这些条件下设计与实现。
[哲学、心理与工程的三位一体](local-source-and-website.zh-CN.md)展开它们与哲学、心理的联系。

## 语言模型、检索与数据工具

这里收录语言模型、数据库与检索系统的教材、课程和官方工具入口。

| 教材或课程 | 内容 |
| --- | --- |
| Jurafsky 与 Martin，[Speech and Language Processing，第 3 版在线草稿](https://web.stanford.edu/~jurafsky/slp3/) | 自然语言处理与语言模型教材，涵盖词元、嵌入、上下文、信息抽取、时间、话语和检索。官网提供全文与课件；2026-08-19 版的 Agents 章仍未完成。 |
| [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) | 在线课程，介绍模型、消息、工具及行动后的观察。 |
| [Agent Skills 概览](https://agentskills.io/home) · [规范](https://agentskills.io/specification) | 用于组织指令、脚本和参考资源的开放格式。 |

| 工具或项目 | 一般用途与官方入口 |
| --- | --- |
| [SQLite](https://www.sqlite.org/docs.html) | 嵌入式关系数据库，提供 SQL 查询与事务。 |
| [sqlite-utils](https://sqlite-utils.datasette.io/) · [Datasette](https://datasette.io/) | 前者提供 SQLite 数据导入与操作的命令行／Python 接口；后者提供数据库浏览、查询与 JSON 接口。 |
| [PostgreSQL](https://www.postgresql.org/docs/) · [pgvector](https://github.com/pgvector/pgvector) | 关系数据库及向量相似度检索扩展。 |
| [Hindsight](https://github.com/vectorize-io/hindsight) | Agent 记忆与检索系统，提供 retain、recall、reflect 等能力。 |
| [Graphiti](https://github.com/getzep/graphiti) | 面向 Agent 的时序知识图谱。 |
| [Mem0](https://github.com/mem0ai/mem0) | 为 Agent 与应用提供持久记忆的组件。 |
| [Letta](https://github.com/letta-ai/letta) | 带有持久状态和记忆管理的 Agent 平台。 |

具体能力和运行条件见各项目文档。
