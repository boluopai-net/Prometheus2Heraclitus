# 购物与比价 · shopping

[English guide](README.md)

比较中国电商平台的商品、优惠和二手报价。推荐前，方法会匹配型号、版本、卖家、
成色、保修、价格类型、日期与购买条件，并区分候选发现、已核实详情和接收方
实际结算价。

## 使用与配套 Skill

下载[完整 shopping 目录](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/shopping)，
或从[集合压缩包](https://github.com/boluopai-net/Prometheus2Heraclitus/archive/refs/heads/main.zip)
取得本目录，将其放到智能体宿主支持的 Skill 位置。

没有始终必需的配套 Skill。[YinYang](../yinyang/README.zh-CN.md) 在接收方采用其
情境账户时负责上下文关系；Shopping 使用有依据的接收方信息，不包含私人画像。
[Research](../research/README.zh-CN.md) 在需要调查规格、兼容性或来源陈述时提供
证据方法。二者是同一公开压缩包中的独立完整包。未安装时，仍可使用当前对话和
合适的现有研究能力。

请求示例：“比较新的 16 GB/512 GB 笔记本与闲鱼同型号二手商品，列出卖家成色
陈述、剩余保修、运费、优惠券资格和最终价格依据。我会在两处工作地点间携带它。”
结果应解释可比候选与使用取舍，提供直接链接、日期、缺失事实和未核实陈述；
不能保证找到了全市场最低价。

## 按需工具依赖

本包提供方法和智能体元数据，不包含购物客户端或脚本。只使用问题所需且已有
访问范围内可用的来源。

| 路线 | 获取与设置 | 选择该路线时需要 |
| --- | --- | --- |
| 海纳 | [官方平台](https://ai.zhidemai.com/haina-platform) | 接收方自己的密钥、商品与优惠权限，以及依据当前官方文档配置的客户端 |
| 买手妈妈 | [完整上游 Skill](https://github.com/aahl/skills/tree/main/skills/maishou) | Python 3.11+、uv 和其脚本，在上游包目录运行 |
| 直接平台 | [cn-scraper-mcp](https://github.com/goesByhc/cn-scraper-mcp) | Python 3.11+、上游包和支持 MCP 的宿主；有效平台会话，浏览器路线还需受支持的浏览器 |
| 闲鱼 | [goofish-cli](https://github.com/fancyboi999/goofish-cli) | Python 3.11+、上游包和已授权会话；搜索与浏览器详情需 Playwright 和受支持的 Chrome，uvx 启动 MCP 还需 uv |

Maishou 文档命令包括 `uv run scripts/main.py search --source=0 --keyword='MODEL'`
和 `uv run scripts/main.py detail --source=SOURCE --id=GOODS_ID`。
cn-scraper 安装为 `cn-scraper-mcp`，通过宿主实际 MCP 配置连接。
goofish 提供 CLI `goofish` 和 MCP `uvx goofish-cli`。
执行前检查当前上游设置、帮助和参数结构；这些示例不执行安装或登录。
当前 cn-scraper 文档不推荐 PDD 搜索。服务宣称的平台支持不代表你的环境已有有效
访问。调整时海纳入口可访问，但未核实其 API 参数结构。

安装、账户访问、购买、付款、卖家消息与商品写入保留已有授权边界。不随包提供
凭据。部分上游工具提供写入能力；此比较方法不授权使用它们。

## 调整与权利

公开版保留原本地 Skill 的比较、条件、价格、来源、适配和访问区别，把私人云端
封装、已停用注册、宿主路径、已观察账户历史和私人画像引用，替换为公开依赖与
有依据的接收方上下文。`SKILL.md` 是英文模型指令，中英文指南含义一致。

本包原创内容采用 [MIT 许可](LICENSE)。外部包是独立依赖，保留各自许可和声明；
本包不包含其源码、二进制、凭据或私人会话。公开文档核对日期为 2026-10-14；
没有安装依赖或查询电商账户。
