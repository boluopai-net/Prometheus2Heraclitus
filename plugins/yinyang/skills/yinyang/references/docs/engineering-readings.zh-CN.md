# 工程阅读

[English](engineering-readings.md) · [哲学阅读](philosophical-readings.zh-CN.md) · [心理阅读](psychological-readings.zh-CN.md)

工程让一个理解取得可运行、可观察、可修改的形式。这里从学习地图进入命令行、版本历史和软件设计，再按问题深入算法、系统、实验与物理条件。以课程、文档和源仓库为主要入口，并保留有助于理解的教材与论文。

工具页帮助找到可用的工具和 Skills；这张阅读地图解释它们背后的概念、方法与实现。工具能够调用，不表示使用者已经理解它；一份文档既可以支持学习，也可以在实际工作中按需查阅。

**先选一条能接上自己的主线。**程序设计从 CS 61A 与 Composing Programs 进入；算法从普林斯顿课程与 Algorithms 进入；计算机系统从 CS:APP 进入；计算理论从 MIT 与 Sipser 进入，再按需要深入 Arora–Barak。下面把课程、教材与文档放在一起，说明各自的用途。课程提供讲授、作业与项目，教材展开连贯概念，文档便于查阅具体接口；一本出版社书目也不等于免费全文。

## 先找到地图，再做出一个可用环境

| 材料 | 从哪里开始 |
| --- | --- |
| [CS 自学指南](https://csdiy.wiki/) · [源仓库](https://github.com/PKUFlyingPig/cs-self-learning) | PKUFlyingPig 发起的开放自学地图。先读使用指南，再按已有基础选程序设计、数学、算法、系统等课程；它不是北大统一规定的课程表，也不必整站修完。 |
| 清华大学计算机系学生科协：[SAST skill docs](https://docs.net9.org/) | 中文技能引导文档。按具体需要进入问题解决、Git、Linux、编辑器、编程语言与开发框架；适合连接基础课程和实际工作。 |
| [MIT Missing Semester 2026](https://missing.csail.mit.edu/) | 从 shell、命令行环境和开发工作流进入，跟随课程当期讲义做小练习。已有版本通过网站的历年入口查阅，避免混用不同年份的课次。 |
| William Shotts，[The Linux Command Line](https://linuxcommand.org/tlcl.php) | 作者提供的开放书籍。学习文件、权限、进程、管道、重定向与脚本。macOS 和 Linux 共享部分 Unix 概念，具体命令选项与系统管理仍要查看目标系统文档。 |
| [Vim 官方文档](https://www.vim.org/docs.php) · [Vim 用户手册](https://vimhelp.org/usr_toc.txt.html) | 先用 `vimtutor` 理解模式、移动与编辑，再按用户手册学习组合命令、搜索与替换；具体选项查 `:help`。它是编辑工具的学习入口，可以与自己的编辑器选择并存。 |

一个合适的起点是让模型协助建立小项目，自己看懂它的输入、输出、文件和运行结果；遇到不理解的概念，沿这些入口补读。工程阅读可以与正在做的事交错发生。

## Git 与 GitHub：让作品和修改能够接续

| 材料 | 解决的问题 |
| --- | --- |
| Chacon 与 Straub，[Pro Git，第二版](https://git-scm.com/book/zh/v2) | 第 1–3 章理解仓库、提交、分支与合并；需要解释历史结构时读第 10 章。Git 是版本控制系统。 |
| [GitHub 入门文档](https://docs.github.com/en/get-started) | 仓库页面、协作和托管的入口；GitHub 是围绕 Git 的平台，两者各有职责。 |
| [GitHub Pull Requests 文档](https://docs.github.com/en/pull-requests) | 比较修改、提出评审、处理分支与合并。阅读变更的理由和结果，不仅是按钮操作。 |

## 软件设计与计算机系统

### 程序设计与抽象：CS 61A 和 SICP

**CS 61A 是这里的基础入口。**它帮助理解程序如何由函数、数据与解释过程构成；后面的软件构造关注怎样把已有编程能力组织成可靠的软件，不能替代这层基础。

| 课程与教材 | 内容与用途 |
| --- | --- |
| Berkeley [CS 61A](https://cs61a.org/) · John DeNero，[Composing Programs](https://www.composingprograms.com/) | 课程与在线教材配对。从函数、高阶函数、递归与数据抽象，进入对象、解释器和不同编程方式。配合课程的小练习与项目，看清程序的行为和抽象边界。 |
| Abelson 与 Sussman，[SICP 第二版](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) · [MIT 提供的全文 PDF](https://web.mit.edu/6.001/6.037/sicp.pdf) | 用 Scheme 展开过程与数据抽象、状态、解释器和求值。它是 CS 61A 思想背景的重要原典，可以在 Composing Programs 之外深入阅读，不把两本书当成同一版本。 |
| [SICP JavaScript 改写与 Scheme 对照版](https://sicp.sourceacademy.org/) | 对照 Scheme 原版与 JavaScript 改写版；站点也链接到可交互阅读与求值的 Interactive SICP JS。选择语言时看已有经验和想理解的问题；版本之间有对应关系，也有实现差异。 |

### 软件构造与设计

| 课程、讲义与参考书 | 内容与用途 |
| --- | --- |
| John Ousterhout，[A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) | 作者书目与课程材料。围绕复杂性、模块、接口和信息隐藏理解软件设计。「哲学」在书名中指设计思想，这里按软件工程用途收录。 |
| [MIT 6.031 Software Construction（2021）](https://web.mit.edu/6.031/www/sp21/) · 同页逐讲阅读 | 在编程基础之后学习规格、测试、抽象数据类型与并发，把「代码能运行」发展为有明确行为契约的软件。这里以课程自带讲义配套；Ousterhout 的书是相邻的设计阅读，不冒充该课指定教材。 |

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
| Berkeley [CS170](https://cs170.org/) · Dasgupta、Papadimitriou 与 Vazirani，[Algorithms（DPV）作者材料](https://cseweb.ucsd.edu/~dasgupta/book/index.html) | 进一步学习算法设计、正确性与复杂度论证，按问题进入分治、贪心、动态规划、线性规划和归约。它是另一部 Algorithms，不与普林斯顿教材混称。 |
| MIT [6.006 Introduction to Algorithms（2020）](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) · CLRS，[Introduction to Algorithms，第 3 版](https://mitpress.mit.edu/9780262033848/introduction-to-algorithms/) | 课程有独立讲义，并把 CLRS 第三版列为补充参考；可用于补强数学建模、数据结构、正确性与渐近分析。另有[第 4 版](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)，使用时核对章节和题号。 |
| Jeff Erickson，[Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/) | 作者开放教材、讲义与习题。理解递归、动态规划、贪心与图算法，练习说明正确性和成本。 |

### 计算理论：MIT、Sipser，再到 Arora–Barak

| 课程与教材 | 内容与用途 |
| --- | --- |
| MIT [18.404J Theory of Computation（2020）](https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/) · Michael Sipser，[Introduction to the Theory of Computation，第 3 版](https://math.mit.edu/~sipser/book.html) | 基础主线。课程提供讲授和习题，教材从自动机、可计算性进入复杂性；书的作者页面提供版本说明与勘误。使用习题时按课程所用版本核对题号。 |
| MIT [6.045J Automata, Computability, and Complexity（2011）](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/) · 课程讲义与教材说明 | 同一基础领域的另一套课程组织，适合按主题补读，不要求与 18.404 重复完成。 |
| Sanjeev Arora 与 Boaz Barak，[Computational Complexity: A Modern Approach](https://theory.cs.princeton.edu/complexity/) | 进阶主线。已有计算模型、归约与基本复杂性类基础后，再深入复杂性类、随机性、交互证明与下界等问题。作者页面提供公开草稿和配套材料；草稿与出版版应分别标识。 |
| Boaz Barak，[Introduction to Theoretical Computer Science](https://introtcs.org/public/index.html) | 开放教材。从计算模型、可计算性和效率进入复杂性问题。区分做不到、计算代价高和现有程序尚未实现。 |

算法和复杂性分析回答形式条件下的性质；实际系统还受数据、实现和机器资源影响。实验测得的速度与渐近复杂度可以互相解释，但不是同一项证据。

### 本文集相关比较的原始来源

| 来源 | 与文章的关系 |
| --- | --- |
| A. M. Turing（1936），[On Computable Numbers, with an Application to the Entscheidungsproblem](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf)，尤其第 6 节 | 通用机器为[隐喻、类比与个人的自我改写](metaphor-and-self-revision.zh-CN.md)中的解释器类比提供形式参照，并不证明语言模型能够正确解释所有程序。 |
| Thomas R. Gruber（1993），[A Translation Approach to Portable Ontology Specifications](https://tomgruber.org/writing/ontolingua-kaj-1993.pdf)，第 1–2 节 | 知识表示中的对象、关系与共享概念化。可对照[窃火](stealing-fire.zh-CN.md)发展的工程本体阅读；后者进一步提出自己的解释。 |
| Donald E. Knuth，[Literate Programming](https://www-cs-faculty.stanford.edu/~knuth/lp.html) | 把解释与程序代码组织在一起的既有实践。比较它的技术用途与本文集更广义的文学自然语言编程。 |

## 实验实现、数据与模型检验

| 文档或仓库 | 阅读用途 |
| --- | --- |
| [PsychoPy 文档](https://www.psychopy.org/) | 在实验任务中呈现刺激、记录响应与组织流程。由一个简单实验理解测量怎样进入程序。 |
| [jsPsych 文档](https://www.jspsych.org/latest/) · [源仓库](https://github.com/jspsych/jsPsych) | 浏览器行为实验；从时间线、插件、数据记录和计时精度文档进入。 |
| [Wilson–Collins 配套代码](https://github.com/AnneCollins/TenSimpleRulesModeling) | 把[心理阅读](psychological-readings.zh-CN.md#心理过程建模与经验检验)中的模型检验落到模拟、拟合与恢复检查；代码可运行之后，仍要检查假设和数据是否适合问题。 |
| Schoukens 与 Ljung（2019），[Nonlinear System Identification: A User-Oriented Roadmap](https://arxiv.org/abs/1902.00683) | 从输入输出、噪声、模型结构与验证理解系统辨识。按需要查阅；自然互动能否满足工程辨识的条件，需要另行判断。 |
| [Gödel Machine](https://people.idsia.ch/~juergen/goedelmachine.html) 与 [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954v3) | 两类自改进技术研究入口：前者围绕证明引导，后者围绕经验评估。比较其目标、假设和验证方式，再读本文集中的相关类比。 |

研究设计、构念与效度留在[心理阅读](psychological-readings.zh-CN.md)；这里提供实现和复现的知识。把实现材料接到研究问题，比单独积累工具名称更有用。

## 物理条件、测量与反馈

工程实现发生在物质世界中：程序要在机器上运行，测量需要设备和时间，界面也要进入人的感知与行动。软件的抽象并不消除能量、延迟、误差和身体条件。

[费曼物理学讲义](https://www.feynmanlectures.caltech.edu/)提供物理概念的开放在线阅读：第一卷侧重力学、辐射和热，第二卷侧重电磁与物质，第三卷讨论量子力学。按所需概念进入，不以读完三卷作为写程序的前提。反馈与模型检验则可接回上面的系统辨识材料。

物理学研究规律，工程在这些条件下设计与实现；二者相接而各有任务。心理活动、哲学表达和工程造物可以在同一实际过程中往返，这种[三位一体](local-source-and-website.zh-CN.md)不因一份可运行程序就完成了关于心灵物理实现的全部解释。
