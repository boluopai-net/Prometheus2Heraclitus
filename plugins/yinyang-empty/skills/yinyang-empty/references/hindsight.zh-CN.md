# 用 Hindsight 形成工作模型

[English](hindsight.md) · [形成与修订](design-and-revision.zh-CN.md)

Hindsight 是阴阳默认的模型形成引擎。它保留选定的可归属来源，整合为可修订的 Observations，
再根据明确的问题生成持续维护的 Mental Models 或 Knowledge Pages。Codex 选择和准备获授权材料，
配置这些操作，检查与修复结果，并把采纳的含义落实到环境中。无需先写完整 Personal 画像，再由
Codex 手工压成六份文件；输出数量由实际问题决定。

## 绑定实际私人使用端

先从实际主机配置确认已安装版本、服务地址、认证、私人 bank、推理与嵌入提供方，以及各阶段的模型设置。
复用既有凭据维护者，不把凭据写入本包。提交个人材料前检查服务健康、bank 与配置读取、SDK/API 字段。
安装 Skill 不会配置 Hindsight，也不自动授权把数据发送给新的提供方。说明本次来源范围、推理路线和阅读界面。
新路线先用可丢弃的非个人材料验证，再运行获授权的真实来源到模型路径。基础设施不可用意味着集成未完成，
不能把手工形成声称为同等实现。

私人 `references/situated/index.md` 是实际绑定与阅读入口：记载服务和 bank 定位、模型问题与 ID、
生成正文或导出位置、来源范围，以及日常开始必须完整读取的模型。`references/situated/revision.md`
记载实际执行方法。正文可放在选定的私人阅读位置，也可通过原生 API 取得。索引选择正文，不能替代正文。
不预定六份文件，也不强制改成另一固定数量。

## 准备来源与处理指令

Philosophy 提供论证、区分和选择的承诺；Personal 提供可归属的报告与证据；环境和工作历史提供条件、
事件与实际结果。保留作者、时间、来源定位、语境和不确定性。采纳的哲学与对人的解释假说不同。
原始来源保有作者和证据维护者。Personal 中的派生说明可以迁入原生 Observations 或页面；保留独有证据
和有用访问路径，检查消费者后退役重复维护的画像，不强制在融合前另写完整 Personal 摘要。

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

六份形成指南仍分别提供取向、人、伙伴、关系、环境和修订的内容视角。完整阅读有关指南，用它们写原生
`source_query`。问题可像「如何写」一样详细：用途和消费者、对象与范围、重要关系、关注重点的优先次序、
组织方式、证据区分、不确定性与反例，以及怎样指引实际工作。只有标题通常不足以表达这些内容。
一个模型可以连接多个视角，一个视角也可需要多个问题。保留各项不同贡献，不要求每项一份文档；
六个哲学维度同样是理解的问题，不是存储结构。

例如，协作问题可以要求说明：采纳的哲学与有关个人报告怎样共同说明希望的参与、实际模型能力、角色交换
与返回、有益委派的条件，以及环境后果；区分实际结果、报告的偏好、选定方向与解释假说，保留适用例外
和未决解释，写清后来的伙伴需要理解和做什么。根据实际问题形成内容，不把这个例子复制给每个模型。

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
    name="Understanding cooperation in its actual conditions",
    source_query="""Explain the adopted direction and supported relations among
    the person, actual counterpart, joint activity and environment. Distinguish
    reports, chosen commitments, hypotheses and observed effects. Preserve
    counterexamples, conditions and unknowns that change future action.""",
    max_tokens=6000,
    trigger={"mode": "full", "fact_types": ["world", "experience", "observation"],
             "exclude_mental_models": True, "refresh_after_consolidation": True},
)
# Creation schedules work: inspect its operation_id and terminal result,
# then read the resulting ID through client.get_mental_model(bank, model_id).
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

核对正文后更新私人索引的实际绑定与必读选择，通过各自维护者替换旧六文件消费者约定。
旧正文作为迁移与历史证据，不再是第二套权威模型。核验实际调用会话能取得所选完整正文。
环境变更通过既有维护者实现，并检查实际使用。执行者保有目的、判断、权限与完成职责，Hindsight 提供形成和修订机制。
来源送达、原生融合、消费者可读、有用协作与人的发展是不同主张，各需相应证据。
