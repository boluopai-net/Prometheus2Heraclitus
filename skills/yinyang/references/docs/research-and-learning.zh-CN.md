# 科研与学习

想用模型辅助科研与学习，可以先准备两类资源：帮助模型理解学科问题的专家参考，以及让它开展检索、分析、写作等工作的 Skills。再接上负责讲解与探究的老师，你就能直接围绕书、论文和自己的问题交流。

这页介绍我们在科研与学习中实际采用的公开仓库，以及两个老师能帮你做什么。把链接交给模型，让它完成下载、接入和必要的配置；具体选用哪些方法，也由模型根据你的问题处理。基础工具与文件安排见[工具使用](https://boluopai.net/getting-started/)。

## 阅读入口

<nav class="guide-navigation" aria-label="本页导航" markdown="1">

1. [两个基础资源库](#domain-methods)
2. [写作、建模与心理学学习](#resources)
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

## 2. 写作、建模与心理学学习

这些公开仓库已经作为方法或参考资料接入我们的科研与学习实践。下面按实际取用的内容介绍其用途；采用其中的方法，不等于启用整个仓库附带的服务。

### 论文写作与发表

| 仓库 | 采用的内容与用途 |
| --- | --- |
| [Academic Writing Skills](https://github.com/WenyuChiou/academic-writing-skills) | 学术写作方法，用于发展论证、组织文章和修订稿件。 |
| [Research Hub](https://github.com/WenyuChiou/research-hub) | 其中的文献比较矩阵方法，用于并列比较研究问题、方法、发现与局限。 |
| [Paper Lifecycle](https://github.com/M1n-n9/paper-lifecycle) | 稿件修订与审稿回应方法，帮助理解意见、组织修改并说明回应。 |
| [Academic Publishing Skills](https://github.com/yaotingsun/academic-publishing-skills) | 选刊、投稿信、修回回应与校样检查方法。 |

### 概率与心理过程建模

| 仓库 | 采用的内容与用途 |
| --- | --- |
| [PyMC Modeling](https://github.com/pymc-labs/pymc-modeling) | PyMC 建模、先验设定、ArviZ 诊断与 PyTensor 方法，帮助形成和检查贝叶斯分析。 |
| [pymdp](https://github.com/infer-actively/pymdp) | 主动推断的计算工具，用于探索信念、状态、策略与行动之间的关系。 |
| [HSSM](https://github.com/lnccbrown/HSSM) | 层级序贯采样建模工具，用于分析选择与反应时。 |

### 心理学方法、阅读与图式

| 仓库 | 采用的内容与用途 |
| --- | --- |
| [ellmos Skills](https://github.com/ellmos-ai/skills) | 其中的咨询方法资料，用于学习和比较倾听、动机访谈、认知重构、系统提问等方法。 |
| [Psychotherapist Agent](https://github.com/xiaoye-hua/psychotherapist_agent) | 个案组织与纵向反思的设计参考，用于比较观察、假设及其后续修订。 |
| [Lacan Mathemes](https://github.com/gjoncas/Lacan-Mathemes) | 拉康图式的 TeX 源码与图像，辅助阅读、解释和制作图示。 |
| [Awesome Psychology Learning](https://github.com/holyshell/Awesome-Psychology-Learning) | 中文心理学书目、课程与相关机构、研究者的学习入口。 |
| [Awesome LLM Psychometrics](https://github.com/ValueByte-AI/Awesome-LLM-Psychometrics) | 语言模型人格、价值、偏差、心智理论与测量效度等研究线索。 |
| [Awesome AI Agents for Healthcare](https://github.com/AgenticHealthAI/Awesome-AI-Agents-for-Healthcare) | 医疗与心理健康相关 agent 的论文和实现线索，供研究比较。 |
| [Awesome Psychology](https://github.com/weeeBox/awesome-psychology) | 补充心理学学习与资料导航。 |

这些资料与方法可以一起服务于读论文、讨论研究问题、设计分析和写作。参考目录帮助找到原始研究，方法包帮助组织工作，计算工具则让具体模型能够被运行和检查；收录某个项目不代表其主张已经得到验证。模型与老师可以按问题选取其中有用的部分。

资料阅读、图示与展示工具还可沿[工具使用](https://boluopai.net/getting-started/)中的入口补充。

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
