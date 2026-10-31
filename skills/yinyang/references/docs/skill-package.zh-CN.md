# 阴阳的文件与更新约定

本页说明作者维护源及私人实例的文件关系。公开 Full 仅供静态参考，禁止用于他人的实践；他人的实际入口是 [Empty](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang-empty)，按其包约定形成和更新自己的版本。

[首页](../../README.zh-CN.md) · [阴阳方法](../../SKILL.zh-CN.md) · [English](skill-package.md)

本说明维护这套阴阳实现的文件与更新约定。集合名为 **Prometheus2Heraclitus**，
其中完整的阴阳成员位于 `skills/yinyang/`。`references/docs/` 与
`references/diagrams/` 是配套资源，不是独立 Skills。
从公开仓库取得完整目录，通过实际使用环境的 Skill 机制提供给模型。
网站提供阅读；克隆仓库和 GitHub 原生 ZIP 保留完整源内容。

阴阳是一项已经展开的哲学与形成方法。读者可以采用、组合选定资源，也可以创作不同作品。
[从采用、组合到自己的创作](example-and-commons.zh-CN.md)展开这份邀请。
哲学家的思想可以支持框架，不能替代实际用户的描述。本说明的六问题、双路线与公共更新约定
适用于完整采用持续维护的 Skill；阅读哲学或取用某项方法，本身不等于采用这份约定，
也不要求开展个人哲学项目。完整采用也不要求另写原创文章：按问题形成的模型说明使用中
采纳的立场与安排，可以选择性借用既有思想。

## 公共内容与情境化内容

六份中英文形成指南规定取向、人、伙伴、关系、环境与修订的完整问题及阅读职责。
每项综合指引从全部六份完整指南与有关实际根据形成。[形成与修订](../design-and-revision.zh-CN.md)
维护不同对象、相连范围与六份整体融贯。

[2×2 实践选择](creation-method.zh-CN.md#choose-2x2)说明版本与凝练方式；本页列出私人文件及更新位置：

| 问题 | 私人实际文件 |
| --- | --- |
| 取向 | `references/situated/orientation.md` |
| 个人 | `references/situated/person.md` |
| 伙伴 | `references/situated/counterpart.md` |
| 关系 | `references/situated/relationship.md` |
| 环境 | `references/situated/environment.md` |
| 实际处境中的修订方法 | `references/situated/revision.md` |

日常完整读取全部六份实际描述。通过实际账号与发布维护者，将需要持久保存的私人源放在 Git 与私人 GitHub 仓库，
核实私有范围、提交内容与读者取得。原件保有维护者，秘密不进入普通仓库文件。公开 Full 不提供私人描述或占位画像。

复杂版将核对后的正文投影到同样六路径，或用私人 `references/situated/index.md`
绑定六个问题、原生 ID 与完整正文。配置见 [Hindsight 指引](../hindsight.zh-CN.md)。
六份的内容形成与整体检查由[形成与修订](../design-and-revision.zh-CN.md)维护。

Philosophy 保有写作来源。Personal 在原有四个主题组内保留可读文章、目录与原始来源链接，仍可直接编辑整理。
原生路线可用实质 Knowledge Pages 维护文章，将 Markdown 投影到已有私人阅读路径，Observations 在后台支持。
按修订需要迁移受影响派生文章，保留可读性与独有根据。已纠正的 Personal 理解须影响后续综合；各产物均能返回
原件，不强制串联生成摘要。[Personal 指南](../formation/personal-material.zh-CN.md#保持-personal-便于本人阅读)维护阅读安排。

材料名称使用本人的母语，正文语言按消费者选择，必要时保留量表标识。
`references/personal/` 与 `references/situated/`，包括可选原生绑定和私人生成正文，均为私有。
公共投影保护两个目录，不修改 bank 状态、GitHub 可见性或运行时消费者。独立哲学保有自己的来源。

## 量表与测评材料

个人版已有量表或测评记录时，把这部分特殊的个人证据整理到
`references/personal/questionnaires/`。用其中的 `README.md` 提供清楚的目录，连接
按日期保留的记录与原始来源，并从 `personal/README.md` 和 `personal/sources.md`
接入。按测量场次或量表组织，以便检索；重复填写仍是彼此独立、有日期的观察。

每条记录保留已知的量表名称、语言与版本、完成日期与情境、结果与分数方向，以及
原始作答或报告的入口。区分问卷作答、表现测验、报告写出的结论与后来的解释。
明确保留不同结论和缺失信息；报告没有逐题答案时，不补造作答。已有私人测量系统
和就医文档集合可以继续保存原件，这里保留有用结果与可用链接，不再复制整套档案。
没有日期的材料保持未定日期，直到来源能确定时间。

这样组织，使测量与叙述材料能够一起被使用，不把量表当作完整个人描述，也不因
增添记录而自动改写工作模型。量表选择、计分与解释由
[心理页](psychological-support.zh-CN.md)说明。这个目录和所有填写后的记录保持私有；
分发包只提供组织方法，不带入别人的记录或占位结果。

## 投影公共变更

`scripts/sync-common.py` 默认检查公共源内容的投影。`--apply` 把公共文件投影到目标，
保留两个私人目录中的一切，包括额外文件与链接，不遍历或检查其内容。它不推断一个人、不导出私人文件，
也不发布到运行环境。

新的个人版从完整共享副本开始，再形成私人描述。用明确包目录比较：

```bash
python3 /path/to/shared/yinyang/scripts/sync-common.py \
  --source /path/to/shared/yinyang --target /path/to/situated/yinyang
```

加上 `--apply` 复制变化，再运行比较。目标中未对应文件和公共路径符号链接会阻止复制；
检查归属，不静默删除。既有本地或私人 Web 维护者安装和发布投影源，再回读实际使用处。

旧包在 `references/{encounter,models,relationship,usage,sources}.md` 混合公开指引与私人
内容。任一包仍有这些路径时，投影器在改变文件前拒绝操作。维护者先按实际含义迁入六份实际描述与私人证据索引，或明确的六问题原生绑定，保存独有支撑，再退役旧路径。旧相遇可能同时包含取向与关系，旧关系
可能同时包含伙伴与共同活动；机械改名不能完成这种语义迁移。私人
`references/personal/README.md` 中有用的内容保留在适当维护者处；整个私人目录受保护。

公共内容的一致性保留一项接收方本地的发现标记例外：若目标 `SKILL.md` 的单行
`description` 已以 `<用户自制>` 和一个空格开头，投影时保留这个前缀，并用公共源替换其余描述；
没有该标记的目标不会被加上。其他公共字节与文件模式仍由源维护；公开包不会把自己
标为接收方自制。

字节一致适用于选择持续采用公共更新的副本。独立替换哲学或组织时，在自己的来源处保留
作品并维护连贯引用；即使仍采用六槽位格式，也不要用本公共包覆盖它。

另行创作可以改变描述的数目、组织与哲学；当前维护的阴阳实现通过两条路线保留六个完整问题与相互融贯；原生路径可在明确六者绑定下变化。

## 私人与公开边界

个人描述即使经过形式化或面向模型书写，也仍属于私人内容。私人引文、传记、心理和
健康记录、关系叙述、账户信息、私人路径、对话标识和未发表手稿留在实际维护位置。
一般化抽象不授权公开能够重建私人来源的链接。

只有获授权的可复用认识回到集合。阴阳原创材料采用 CC BY-NC-SA 4.0，
其他独立成员保留各自 MIT 许可。权限、署名与来源审查遵循
[集合说明](https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/README.zh-CN.md)及实际发布维护者。私人改编不必公开。
