# 工程阅读

[English](engineering-readings.md) · [哲学阅读](philosophical-readings.zh-CN.md) · [心理阅读](psychological-readings.zh-CN.md)

工程让一个理解取得可运行、可观察、可修改的形式。这里从学习地图进入命令行、版本历史和软件设计，再按问题深入算法、系统、实验与物理条件。以课程、文档和源仓库为主要入口，并保留有助于理解的教材与论文。

工具页帮助找到可用的工具和 Skills；这张阅读地图解释它们背后的概念、方法与实现。工具能够调用，不表示使用者已经理解它；一份文档既可以支持学习，也可以在实际工作中按需查阅。

## 先找到地图，再做出一个可用环境

| 材料 | 从哪里开始 |
| --- | --- |
| [CS 自学指南](https://csdiy.wiki/) · [源仓库](https://github.com/PKUFlyingPig/cs-self-learning) | PKUFlyingPig 发起的开放自学地图。先读使用指南，再按已有基础选程序设计、数学、算法、系统等课程；它不是北大统一规定的课程表，也不必整站修完。 |
| [MIT Missing Semester 2026](https://missing.csail.mit.edu/) | 从 shell、命令行环境和开发工作流进入，跟随课程当期讲义做小练习。已有版本通过网站的历年入口查阅，避免混用不同年份的课次。 |
| William Shotts，[The Linux Command Line](https://linuxcommand.org/tlcl.php) | 作者提供的开放书籍。学习文件、权限、进程、管道、重定向与脚本。macOS 和 Linux 共享部分 Unix 概念，具体命令选项与系统管理仍要查看目标系统文档。 |

一个合适的起点是让模型协助建立小项目，自己看懂它的输入、输出、文件和运行结果；遇到不理解的概念，沿这些入口补读。工程阅读可以与正在做的事交错发生。

## Git 与 GitHub：让作品和修改能够接续

| 材料 | 解决的问题 |
| --- | --- |
| Chacon 与 Straub，[Pro Git，第二版](https://git-scm.com/book/zh/v2) | 第 1–3 章理解仓库、提交、分支与合并；需要解释历史结构时读第 10 章。Git 是版本控制系统。 |
| [GitHub 入门文档](https://docs.github.com/en/get-started) | 仓库页面、协作和托管的入口；GitHub 是围绕 Git 的平台，两者各有职责。 |
| [GitHub Pull Requests 文档](https://docs.github.com/en/pull-requests) | 比较修改、提出评审、处理分支与合并。阅读变更的理由和结果，不仅是按钮操作。 |

## 软件设计与计算机系统

| 材料 | 阅读用途 |
| --- | --- |
| John Ousterhout，[A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) | 作者书目与课程材料。围绕复杂性、模块、接口和信息隐藏理解软件设计。「哲学」在书名中指设计思想，这里按软件工程用途收录。 |
| [MIT 6.031 Software Construction](https://web.mit.edu/6.031/www/sp21/) | 规格、测试、抽象数据类型与并发等课程材料；把「代码能运行」进一步发展为有明确行为契约的软件。 |
| Arpaci-Dusseau 与 Arpaci-Dusseau，[Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) | 作者开放教材。从虚拟化、并发与持久化理解进程、内存和存储；Linux 命令的表面操作可以在这里找到系统背景。 |

## 算法、计算与复杂性

| 材料 | 阅读用途 |
| --- | --- |
| Jeff Erickson，[Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/) | 作者开放教材、讲义与习题。理解递归、动态规划、贪心与图算法，练习说明正确性和成本。 |
| Boaz Barak，[Introduction to Theoretical Computer Science](https://introtcs.org/public/index.html) | 开放教材。从计算模型、可计算性和效率进入复杂性问题。区分做不到、计算代价高和现有程序尚未实现。 |

算法和复杂性分析回答形式条件下的性质；实际系统还受数据、实现和机器资源影响。实验测得的速度与渐近复杂度可以互相解释，但不是同一项证据。

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
