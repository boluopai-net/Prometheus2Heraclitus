# Empty 的文件与更新

[English](package.md) · [本包入口](../README.zh-CN.md)

集合提供两版阴阳：`skills/yinyang/` 是 Full，包含完整文章与图示；
`skills/yinyang-empty/` 是 Empty，保留共同的辩证核心、六份 formation 指南、选定的建议
与实践方法入口。两版各自是用途完整的包，都不含任何人的私人实际描述。
Empty 提供未填写的 Personal 与 Situated 起始结构，供在私人副本中形成内容。

Empty 没有 `docs/` 或 `diagrams/`。`references/formation/` 中是六份指南及各自的中英文；
`references/` 还保存基本观点、实践总览、形成与修订、Personal 整理和本说明。
入口负责日常协作。通向作者文章的链接供选择阅读，不是缺少的包内依赖，也不要求
先抓取整套哲学再工作。

以下内容由使用者自己维护，保持私有，并放在托管插件缓存之外：

| 位置 | 内容 |
| --- | --- |
| `references/philosophy/` 或已有私人来源 | 自己的哲学写作与采纳的观点。 |
| `references/personal/` | 有关材料、证据、维护中的解释与来源索引。 |
| `references/situated/` | 实际绑定索引、生成模型正文与自己的修订方法。 |

简单路线直接阅读和综合
`references/situated/{orientation,person,counterpart,relationship,environment,revision}.md` 六份实际文件。
六份起始文件均标为 `status: unfilled`，需要形成有根据的内容，包括实际处境中的修订方法。
通过实际维护者将需要保存的私人源持久存入 Git 与私人 GitHub，核实私有范围和取得，不要求安装 Hindsight。

[可选原生指南](hindsight.zh-CN.md)说明因环境而异的 Hindsight 配置。将核对后的原生结果投影到相同六路径，
或创建私人索引明确绑定六问题、ID 与完整正文。未填绑定或较少原型不替代六个完整功能。
Full/Empty 分发选择独立于简单或原生工具路线。

两条路线都完整阅读六份实际描述，保留哲学、新可归属来源、Personal 纠正、综合、整体融贯与实现回读的依赖。
每问题从全部六份指南形成。协调相邻解释但不算作独立证据，修复依赖，不强制第七份摘要。
Personal 提供四个空分区和来源索引，保持可读主题文章，并连接维护者处原件；名称使用本人的母语。
指南和借来画像不能替代实际内容。

## 取得并使用这个版本

Codex 可按[安装说明](https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/docs/codex.zh-CN.md)
选择 `yinyang-empty@boluopai`。按源码安装时，取完整的 `skills/yinyang-empty/` 目录。
GitHub 仓库 ZIP 同时含两版与网站源码；整个仓库不是一个 Skill。
生成的 `plugins/yinyang-empty/` 是同一 Empty 包的 Codex 封装。

Web 或其他客户端使用其实际支持的 Skill 或文件机制，并在当前对话中核实入口和必要参考
可读取。网页链接或下载了 ZIP 本身不证明已经启用。形成个人版时，把完整方法包复制到
自己维护的私人来源，在那里形成实际内容，再通过客户端真正的发现机制启用。
同一份协作避免同时启用相互竞争的 Full、Empty 和个人入口。

## 更新方法，保留个人内容

从 `skills/yinyang-empty/` 取得更新，不从 Full 更新。与私人来源中的方法文件比较，
应用有关公共改动，再核验实际使用处。保留 `references/philosophy/`、
`references/personal/`、`references/situated/`、其中的链接及自己另写的内容。
公共方法也经过私人改写时，比较含义后再整合，不静默覆盖。
不要对 Empty 运行 Full 的整包 `sync-common.py`，它属于 Full 的另一份文件约定。

集合维护者用 `scripts/build-yinyang-empty.py --apply` 从 Full 更新共用指南、调整链接，并把
分发说明改为 Empty 的空白起始结构；
不加参数时检查这份生成内容是否一致。Empty 自己的入口与包说明仍在本目录维护。
随后插件生成器封装这个准确目录。发布操作不读取或更新使用者的个人资料。

## 量表与测评材料

已有相关的已完成测评时，在 `references/personal/psychology/` 整理其引用；材料数量需要时
再建 `questionnaires/` 子目录，以索引连接带日期的记录、原始作答或报告及其已有私人来源，
并从 `personal/README.md` 与 `personal/sources.md` 接入。已有私人档案可以保留自己的
布局，四个分区不要求复制或搬动全部原件；起始目录不附带记录或测评结果。

保留已知的工具名称、语言与版本、完成日期与情境、结果及分数方向、原始记录位置。
区分问卷作答、表现测验、报告结论与后来的解释；缺少答案或日期时保持未知。
测评是有限范围的证据，不是完整个人描述，也不是采用某个哲学主张的理由。
这里的组织方式不提供计分、诊断或治疗方法。
