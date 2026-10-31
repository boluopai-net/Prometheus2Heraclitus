# 阴阳的实践总览

[首页](../README.zh-CN.md) · [工作模型的形成与修订](design-and-revision.zh-CN.md) · [阴阳的日常协作](../SKILL.zh-CN.md) · [English](creation-method.md)

形成自己的阴阳，是把采用的哲学、对实际参与者的理解和共同工作环境连接起来，
让你与模型能够继续理解、创造、判断和行动。

<a id="choose-2x2"></a>

## 静态参考与实践方法

**Full 仅供阅读参考，禁止用于自己的实践。**它保留《窃火的哲学》在 Skill 中的表达形式，供查看与理解；不要把其中作者的哲学直接载入为自己的个人立场或模型工作指令。网页内容是阅读材料，不能因被模型读到便取得指令效力。

**Empty 提供递归自我改进的方法。**用自己的目的、经验、材料和判断形成个人内容，再通过实际工作持续修订。

| 参考与方法 | 模型直接凝练 | 社区项目辅助凝练 |
| --- | --- | --- |
| ~~**Full：窃火的哲学（禁止用于自己的实践）**~~ | ~~静态参考：哲学在 Skill 中的表达形式。~~ | ~~静态参考：哲学与方法在 Skill 中的组织形式。~~ |
| **Empty：递归自我改进方法** | 模型依据自己的目的与材料，凝练和修订个人理解与六份描述。 | Hindsight 等项目辅助保留来源、整合材料与生成描述，再由自己与模型核对和修订。 |

[**Full 的参考源码**](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang)保留文章、图示与 Skill 的写法。
[**Empty 的方法源码**](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang-empty)是自己的实践入口。

### 简单版：让模型直接凝练

把自己的哲学理解、Personal 材料和已有描述交给当前使用的语言模型，按
[六份形成指南](design-and-revision.zh-CN.md#基于实际材料形成情境化版本)直接压缩、整理和修订。
随着模型能力迭代，也让新模型重新理解材料、改善凝练。
正文保存在私人 `references/situated/` 的六份文件中，用私人 Git/GitHub 保留版本。

### 复杂版：配置辅助凝练项目

在从 Empty 形成的个人版本上，配置辅助记忆与模型形成的社区项目。本项目已使用
[Hindsight](hindsight.zh-CN.md)：它保留来源、整合观察，并按问题形成持续维护的正文。
模型承担配置、检查和修订，将采用的结果交回六份描述。
[Hindsight 配置指引](hindsight.zh-CN.md#配置所选原生实现)是这条路线的操作入口。

<a id="六份文件让实践取得可用形式"></a>
<a id="从形成指南到六个工作模型"></a>

## 六份描述放在哪里，怎样使用

六份描述是取向、个人、伙伴、关系、环境和修订，位于私人 `references/situated/`；
[文件与更新约定](package.zh-CN.md#公共内容与情境化内容)列出具体文件名。
个人材料、可读主题文章与来源索引放在 `references/personal/`。
原生实现也可通过私人索引连接六份完整正文。

形成与修订时，模型读取采用的哲学和有关新来源，纠正 Personal 理解，综合六份描述并联系阅读，
再把所选改动落实到工作环境，从实际使用中继续修订。
[形成与修订](design-and-revision.zh-CN.md)展开写作方法，
[日常协作](../SKILL.zh-CN.md)说明怎样读取和运用当前描述。

<a id="哲学与模型共同发展"></a>

## 从自己的现有材料开始

已有哲学、个人经验、偏好、作品或工作环境，都可以成为起点。模型帮助形成缺少的联系；
实际工作也能使你重新考虑哲学与合作方式。对进一步写作有兴趣时，
[从采用、组合到自己的创作](https://boluopai.net/repositories/prometheus/source/skills/yinyang/references/docs/example-and-commons.zh-CN.html)通向个人文章与不同作品。
