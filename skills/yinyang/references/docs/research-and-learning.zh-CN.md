# 科研与学习的建议

想用模型辅助科研与学习，可以先准备两类资源：帮助模型理解学科问题的专家参考，以及让它开展检索、分析、写作等工作的 Skills。再接上负责讲解与探究的老师，你就能直接围绕书、论文和自己的问题交流。

这页介绍值得获取的公开仓库，以及两个老师能帮你做什么。把链接交给模型，让它完成下载、接入和必要的配置；具体选用哪些方法，也由模型根据你的问题处理。基础工具与文件安排见[工具使用](https://boluopai.net/getting-started/)。

## 阅读入口

<nav class="guide-navigation" aria-label="本页导航" markdown="1">

1. [两个基础资源库](#domain-methods)
2. [进一步的科研仓库](#resources)
3. [本地老师与云端老师](#learning)

</nav>

<a id="domain-methods"></a>

## 1. 先准备这两个基础资源库

### Scientific Agents：给模型更丰富的学科参考

[K-Dense Scientific Agents](https://github.com/K-Dense-AI/scientific-agents)收集不同学科与专业的专家思考资料，涉及数学、物理、计算机、统计、生命科学等领域。它的价值，是让模型在理解和解释问题时，有更具体的专业知识与思考方式可以参考。

可以让模型把这套资料库下载好，接到研究与教学环境中。以后你问一个概念、读一篇跨学科论文，或想讨论某个研究方向，模型和老师就可以读取有关专家的 `AGENTS.md` 等资料。你不必自己逐个阅读专家文件，也不必先挑选一个专家角色。

### Scientific Agent Skills：给模型可用的科研方法

[K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)提供文献检索、实验设计、统计分析、机器学习、数据处理、科学绘图、引用管理等方面的能力包。它适合为研究和学习准备一套较广的工具基础，不只服务于某一种学科。

建议把这两个仓库一起交给模型，让它获取完整资料并接通需要的 Skills。前一个丰富学科理解，后一个补充具体工作方法。实际下载、安装与后续使用由模型处理，你只需知道这些能力已经有公开来源可供采用，不必先学会每个包的名字和操作。

<a id="resources"></a>

## 2. 还可以加入哪些科研仓库

下面这些仓库可以补充写作、文献整理、投稿和专业建模。把感兴趣的链接交给模型，说明你想增加什么能力；不确定是否用得上时，也可以让它结合你的学习或研究方向判断。

| 仓库 | 可以提供什么帮助 |
| --- | --- |
| [Academic Writing Skills](https://github.com/WenyuChiou/academic-writing-skills) | 辅助学术论文写作与修订，展开论证、组织文章，并按目标刊物调整稿件。 |
| [Research Hub](https://github.com/WenyuChiou/research-hub) | 连接文献、笔记与来源问答，提供 Zotero、Obsidian、NotebookLM 之间的研究工作空间，也有可单独采用的文献比较方法。 |
| [Paper Lifecycle](https://github.com/M1n-n9/paper-lifecycle) | 围绕论文分析、修改与审稿回应开展工作，适合已有稿件、准备修订或处理审稿意见时使用。 |
| [Academic Publishing Skills](https://github.com/yaotingsun/academic-publishing-skills) | 补充选刊、格式调整、投稿信、修回与校样等发表环节的帮助。 |
| [PyMC Modeling](https://github.com/pymc-labs/pymc-modeling) | 为概率与贝叶斯建模提供 PyMC、PyTensor 等专业方法参考，适合需要这类分析的研究。 |

这些来源可以按需要获取，也可以请模型一起准备好。仓库包含的方法多于你眼下会用到的部分；挑选、组合以及软件依赖的处理属于模型的工作。你不需要为了保存一套资料，就先购买它提到的所有服务或学完所有方法。

资料阅读、图示与展示工具仍可沿[工具使用](https://boluopai.net/getting-started/)中的入口补充。这里保留的是科研资源来源，方便你记起还有哪些能力可以交给模型接入。

<a id="learning"></a>

## 3. 本地老师与云端老师分别做什么

这两个老师是可以交给模型使用的教学与探究方法。它们让模型围绕你的问题持续讲解、讨论和准备材料，而不只是一次性概括一篇文章。

| 老师 | 适合怎样使用 |
| --- | --- |
| [本地老师（Local Teacher）](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/local-teacher) | 在本地 Codex 中持续学习、读教材与论文、复习概念，也可以结合本地文件、代码和实验边学边做。 |
| [云端老师（Web Teacher）](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/web-teacher) | 在 Web 对话中讨论尚未明确的问题、比较不同理解、探索相邻知识，并组织课程材料与学习接续。 |

两者共享教学方法；这些是使用上的侧重，不意味着本地只能实践、Web 只能讲理论。可以从你当前方便使用的入口开始。

**老师可以调用前面那些仓库里的 AGENTS 专家资料与 Skills 方法，同时辅助教学和研究。**例如，讲一个物理概念时借助相关学科参考，读论文时使用文献与统计方法，讨论研究构想时调用专业建模或写作能力。你可以直接提出问题，由老师选择和读取有用的资料，不必另外指挥它选哪个专家、调用哪个 Skill。

准备环境时，把两个老师和前面的仓库一并交给模型，让它建立实际可读取、可调用的连接。完成以后，你就可以说「带我读这篇论文」「解释这个概念和我原来理解的关系」「帮我讨论这个研究想法」。安装和连接的细节交给模型，页面只需要让你知道这些老师和资源可以提供什么帮助。

持续学习时，老师还可以准备术语表、概念图、学习指南，以及适合当前材料的习题或实验，并随讨论更新。你主要通过阅读、观看、提问、异议和尝试参与；需要模型把材料整理好，也可以直接提出，不必先完成一轮课程。

回到[工具使用](https://boluopai.net/getting-started/)了解通用工具，或从本页选择想增加的资源，让模型把它接到你的科研与学习中。
