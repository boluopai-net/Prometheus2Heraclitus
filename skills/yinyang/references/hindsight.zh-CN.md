# 可选 Hindsight 实现

[English](hindsight.md) · [形成与修订](design-and-revision.zh-CN.md)

Hindsight 是阴阳形成与修订方法的一种可选实现。简单路线可以独立使用，由语言模型直接综合同样的六文件，
并用私人 Git/GitHub 持久保存，不要求安装 Hindsight。Full/Empty 分发选择与工具路线相互独立。
本指南在原生能力适合实际环境时说明配置方法，不引入另一套哲学或复制 Skill。

Hindsight 保留选定的可归属来源，整合为可修订的 Observations，再按六个细致功能问题生成持续维护的
Mental Models 或 Knowledge Pages。任务所有者准备获授权材料、配置操作、检查修复输出并落实采纳的含义。
保留原有修订步骤、完整问题范围和跨描述融贯；换工具不授权把六者缩成较少原型，也不把实际修订方法换成 API 步骤。

## 配置所选原生实现

根据实际主机确认安装或支持的 Hindsight 版本、部署方式、服务地址、认证、私人 bank、存储、推理与嵌入提供方，
以及各阶段模型设置。[上游项目](https://github.com/vectorize-io/hindsight)维护当前安装路线；这些配置因环境而异。
下文原生接口来自已核对的 1.1.0，不假定对所有安装都有效。安装阴阳 Skill 不会配置服务或凭据。

1. 选择实际原生服务或托管部署及私人来源范围，配置持久数据库与存储、推理和嵌入。凭据保留在既有秘密维护者处，
   不放进 Skill 或普通 Git 文件。确认实际访问与提供方、数据边界。
2. 读取有效 bank 配置，再按下文共同目的设置 `retain_mission`、`observations_mission` 与 `reflect_mission`。
   按实际数据与成本设置各阶段提供方、模型、预算和来源保留，不复制他人的运行时设置。
3. 从六份完整指南与实际根据定义六个完整问题，配置原生范围和完整或增量刷新，通过实际支持的 SDK/API 或 MCP
   接入目标调用者。问题相互联系，不是六份孤立语料。记录实际绑定与阅读位置。
4. 检查服务健康与 bank/配置读取，再用可丢弃的非个人记录测试原生保留、抽取、整合、reflect、页面刷新与 Markdown
   导出。检查操作终态并读回实际内容；接口接受不等于完整结果。
5. 按保留的修订依赖处理获授权实际来源，检查六份整体，再为实际读者投影核对后的正文。核验真实消费者与必要环境后果。
   路线失败时明确说明原生集成缺口；简单路线仍是受支持的独立选择，不能据此声称原生操作成功。

适合消费者时，优先投影到熟悉的
`references/situated/{orientation,person,counterpart,relationship,environment,revision}.md` 六路径。
需要其他原生布局时，用 `references/situated/index.md` 明确绑定私人服务、bank、六问题 ID、来源范围与完整正文，
保留六项阅读职责；实际处境中的修订方法放在 `revision.md` 或有明确完整绑定的位置。索引不能替代正文，也不保留
两套竞争的权威模型。需要持久保存的私人源与导出内容通过实际私人 Git/GitHub 维护者保存；原生数据库备份与历史
保有运行时维护者。Hindsight 本身不完成 GitHub 发布。

## 准备来源与处理指令

所选原生路线保留[修订依赖](formation/revision.zh-CN.md#刷新选定的根据)：先读采纳的哲学，检索有关的新可归属来源，
刷新与纠正 Personal 理解并保留冲突和不确定性，再由 Hindsight 综合六份、检查融贯，将必要变化落实到
Skills 与环境并实际回读。原生操作实现这些责任；只要能取得原始来源，并不替代 Personal 纠正步骤。
不要求手工完整重写或强制串联生成摘要，各项产物均保留返回原始根据的路径。

Philosophy 提供论证、区分和选择的承诺；Personal 提供可归属的报告与证据；环境和工作历史提供条件、
事件与实际结果。保留作者、时间、来源定位、语境和不确定性。采纳的哲学与对人的解释假说不同。
原始来源保有作者和证据维护者。Personal 同时保留在既有四个主题分组内、本人可以阅读的实质文章。
Hindsight 可以用细致主题问题维护 Knowledge Pages，把 Markdown 正文投影到已有私人阅读路径。
保持可读目录、文章和来源链接可用；Observations 留在后台，不把文章换成原始数据库清单。
[Personal 指南](formation/personal-material.zh-CN.md#保持-personal-便于本人阅读)维护阅读用途与组织方法。

实际修订需要时再迁移受影响的派生文章，保留独有证据和当前可读性。不要求一次删除或重写全部 Personal，
不另写完整重复摘要，也不强制先手工综合。本人和获授权模型仍可以直接编辑、整理来源与文章。
Personal 主题页面与协作模型从有关原始根据形成不同内容，不要求协作模型再摘要生成的 Personal 页面。
有意使用原生范围和相邻模型排除，避免循环综合或自我佐证。

原生 **World** 与 **Experience** 是并列的原始事实类别。World 包含人的可归属报告、偏好、规则与外部事件；
Experience 记录助手实际做过的行动或观察。人的经验报告通常属于带归属的 World，不能变成助手自己的经历。
**Observations** 是保有来源联系、可修订的整合侧面。**Mental Models** 是另行维护、由问题生成的文档。
这些名称均不证明真实，也不授予权限。

用原生 bank 的 `retain_mission`、`observations_mission` 和 `reflect_mission` 分别说明抽取、整合与综合的共同目的。
保留会影响理解的关系、条件、备选解释和纠正历史，不只抽取特征。抽取阶段丢失的关系可能无法在综合阶段恢复。
Tags、tag groups 与 `fact_types` 限定检索来源，不承载全部哲学关系或指令等级。原生 directives 是用于
reflect/refresh 的明确指令；仅有意加入实际采纳的要求，不把每项推断偏好自动提升为指令。
它们不会自动成为 Codex 指令，也不授权修改主机。

## 把模型问题写成细致的内容规格

保留取向、人、伙伴、关系、环境和修订六个明确的原生模型问题。完整功能范围由
[六问题形成方法](design-and-revision.zh-CN.md#基于实际材料形成情境化版本)与六份完整指南展开。
规定或实质修订每个 `source_query` 时，联系阅读全部指南，使问题范围既保留自己的对象，
也保留与其他五者的联系。标题或缩短的职责清单不能替代指南全文。

问题可以细致说明用途和消费者、对象范围、重要关系、关注重点的优先次序、组织方式、证据区分、
不确定性、反例以及怎样指导工作。行文可以随材料组织，不把人、伙伴和关系缩并为一个不加区分的问题，
也不把环境只写成清单。修订问题需要形成本人在实际处境中重新考虑目的、材料、解释、联动变化与
核验使用的方法；只有原生 API 步骤不能提供这份方法。六个哲学维度仍是理解问题，不是数据库结构。

在有关问题中写明共同采纳的前提与跨问题联系，同时保留各自不同贡献。例如，若采纳自愿参与的目的，
对人的理解、希望伙伴的贡献、共同分工、支持环境与纠正方法都需要使它保持可理解。
这需要相连推理，不是把同一段复制六遍。

## 检查六个问题之间的融贯

形成或重要修订之后，完整联系阅读全部六份描述，对照来源与实际使用，检查共同前提、概念和所指、
条件与时间、责任与实际后果。共同 bank、相同 missions、可检索相同来源或每页各自刷新成功，
都不保证这些关系融贯。保留真实分歧与不确定性，不把它们修饰掉。

相邻描述可以作为需要协调的当前解释阅读，不能互相充当事实主张的独立证据。重要判断返回原始根据，
区分把相邻描述的立场作为背景与把它算作佐证。有意配置原生模型纳入或排除，避免回响旧解释；
不能把排除变成要求各问题孤立理解或孤立修订。

整体显出不合时，修复受影响的原始来源、mission、问题、检索范围或环境实现，刷新有依赖的问题，
再把六者联系起来完整阅读。局部纠正不一定重生无关正文，但必须检查对整体的后果，并明确保留重要未决差异。
实际处境中的修订方法承担这种判断与落实，不强制增加第七份总摘要。

## 使用原生接口

[英文版接口段落](hindsight.md#use-the-native-interfaces)给出从 Hindsight 1.1.0 已安装 Python 客户端与
API 实现核对的完整示例、字段和路由；代码标识保持原文。换主机时重新核对安装版本。
[上游项目](https://github.com/vectorize-io/hindsight)维护安装和变化中的提供方、服务说明。

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")  # actual configured URL
bank = "private-example"
client.retain(
    bank_id=bank,
    content="An attributed, authorized source passage with its context.",
    document_id="source-owner-record-id",
    context="Source identity, date, evidence role and applicable scope",
    tags=["philosophy", "personal"],
)
created = client.create_mental_model(
    bank_id=bank,
    name="The actual model counterpart",
    source_query="""Develop the counterpart question from the six complete
    formation guides and relevant original grounds. Explain actual capabilities
    and conditions, wanted contribution, independent judgment and fallibility.
    Relate them coherently to adopted direction, the actual person, joint work,
    environment and situated revision. Distinguish observed effects, intended
    arrangements and hypotheses; preserve conditions and unknowns.""",
    max_tokens=6000,
    trigger={"mode": "full", "fact_types": ["world", "experience", "observation"],
             "exclude_mental_models": True, "refresh_after_consolidation": True},
)
# Creation schedules work: inspect its operation_id and terminal result,
# then read the resulting ID through client.get_mental_model(bank, model_id).
# Specify the other five full questions and check all six accounts together.
```

上述字段示例不是对任意个人数据执行的授权，也不规定通用的模型、提供方或 token 数量。
SDK 的 `Hindsight(base_url=...)` 提供 `retain(bank_id, content, document_id=..., context=..., tags=...)`、
`create_mental_model(bank_id, name, source_query, ..., trigger=...)`、
`create_knowledge_page(bank_id, name, source_query, ..., trigger=...)`、
`get_mental_model(bank_id, mental_model_id)`、`refresh_mental_model(bank_id, mental_model_id, mode="full")`、
`reflect(bank_id, query, ...)` 与 `export_knowledge_base(bank_id)`。异步调用方使用 `a...` 对应方法；
生成的 API 客户端可通过 `client.banks`、`client.mental_models` 与 `client.knowledge_base` 使用。

REST 前缀为 `/v1/default/banks/{bank_id}`：

| 操作 | 路由 |
| --- | --- |
| 读取、修改处理配置 | `GET` / `PATCH /config` |
| 保留、整合、综合 | `POST /memories`、`POST /consolidate`、`POST /reflect` |
| 创建、读取、刷新模型 | `POST /mental-models`、`GET /mental-models/{id}`、`POST /mental-models/{id}/refresh` |
| 检查异步操作 | `GET /operations/{operation_id}` |
| 导出 Knowledge Pages Markdown | `GET /knowledge-base/export` |

配置前先读取当前值；mission 更新会替换该值。创建返回 `operation_id` 只表示已安排工作，需要确认终态和错误，
再读取实际正文。分别检查来源抽取、整合积压、Observation 来源与模型刷新。改变问题或来源解释后可用完整刷新；
增量和自动刷新按实际维护需要选用。Knowledge Pages 原生默认从 Observations 增量刷新并排除其他 Mental Models；
需要原始事实时有意调整范围。排除相邻模型有助于避免把旧综合当作新的独立支持。
需要文件阅读时导出原生 Markdown bundle，不另造综合引擎。示例不规定通用的模型、提供方或 token 数量。

## 检查形成的理解及其使用

对照有代表性和重要的来源完整读取生成正文，检查采纳的哲学、个人报告、实际关系、冲突与不确定性是否保留，
历史引文是否误变成当前助手的经历。用 recall 与来源检索调查缺口，修正来源语境、missions、范围或模型问题，
重跑原生操作并读取结果。更短正文或更多 Observations 不证明语义保留；来源引用不等于独立佐证，流畅综合不证明因果解释。

核对六问题完整整体后，更新私人索引的实际绑定与必读选择。通过各自维护者迁移物理阅读路径，
先核验继任内容保留所需功能与联系；在此之前，已有实际正文可以继续承担当前阅读，生成本身不自动退役它们。核验实际调用会话能取得所选完整正文。
环境变更通过既有维护者实现，并检查实际使用。执行者保有目的、判断、权限与完成职责，Hindsight 提供形成和修订机制。
来源送达、原生融合、消费者可读、有用协作与人的发展是不同主张，各需相应证据。
