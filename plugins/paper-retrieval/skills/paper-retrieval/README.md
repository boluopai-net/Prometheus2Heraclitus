# paper-retrieval

Find relevant Chinese/English papers, books and chapters, reconcile citations
and editions, and verify the actual acquired text. The exact Skill identifier is
`paper-retrieval`. Copy this complete directory into your host's Skill directory
and invoke its [SKILL.md](SKILL.md) through that host, or use the helper directly.

Examples: “Find the author's papers since 2020 and separate bibliography coverage
from obtained full texts”; “Obtain the available author manuscript for this DOI”;
“Check whether this PDF is the complete second edition or a preview.”

## Companion methods and execution dependencies

| Dependency | When and why | Obtain or supply |
| --- | --- | --- |
| [research](../research/README.md) | Companion method for evidence selection, current investigation and conflicting sources; use with the scholarly workflow | Download the complete [public research package](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research) beside this package. It is a Skill, not a search engine. |
| [browser-relay](../browser-relay/README.md) | Conditional on controlled/authenticated pages; owns exact targets, session reuse, readback, placement and cleanup | Download the complete sibling browser-relay package and bind the host’s real authorized browser/download API. The Skill does not install a browser carrier or copy authentication. |
| [network](../network/README.md) | Conditional on evidenced connectivity faults; distinguish transport from access/capture failures | Download the network companion when using that method, configure your own targets, and use actual diagnosis capabilities within authorization. It is conditional, not permission to alter routing. |
| Search/HTTP/browser tools, Python, Poppler, optional curl | Actual execution capabilities, not companion Skills | Supply the tools and install the helper dependencies below. Downloading a Skill does not install them or establish library access. |

The local method's division of responsibility is retained: research selects and
assesses evidence; the browser owner controls the exact authorized surface;
paper-retrieval reconciles the scholarly object and acquired bytes. The inspector
can run independently; the complete collection method composes these roles.

The host needs an available search/HTTP/browser tool for discovery and acquisition.
The local helper requires Python 3.10+ and Poppler (`pdfinfo`, `pdftotext` on PATH).
Install Poppler through your platform's package manager, for example
`brew install poppler` on macOS or `sudo apt install poppler-utils` on Debian/Ubuntu.
The public direct-download example also uses `curl`.

```sh
python3 scripts/inspect_pdf.py --help
python3 scripts/inspect_pdf.py /path/to/candidate.pdf
python3 -m unittest discover -s tests -v
```

The helper prints JSON with byte size, SHA-256, page count and endpoint text;
it rejects non-PDF responses and parsing errors. It does not certify identity,
missing middle pages, edition equivalence or completeness. Inspect the printed
work against its source record, and render image-only pages. There is no universal
retrieval promise, credential store, authenticated capture adapter, CAJ converter
or restriction-evasion mechanism. Existing library access must be established
through the recipient's own authorized interface. Record incomplete items and
verified identifiers in the conversation as well as the collection manifest.

See [source and verification guidance](references/sources-and-verification.md).
This original portable adaptation derives its scholarly workflow from the
maintainer's local Skill, removing host paths, personal records and private
browser/library machinery. Original package material is [MIT licensed](LICENSE).
Poppler and retrieved publications retain their own rights; no third-party code
or publication is bundled.

## 中文说明

本 Skill 用于检索相关的中英文论文、学术书籍与章节，核对题录和版本，
并验证实际取得的文本。准确标识为 `paper-retrieval`。将整个目录复制到
宿主的 Skill 目录，通过宿主调用 [SKILL.md](SKILL.md)，也可直接运行脚本。

示例：“收集这位作者 2020 年以来的论文，区分题录覆盖与已取得全文”；
“寻找这个 DOI 可获取的作者稿”；“检查这个 PDF 是完整第二版还是预览”。

| 配套方法或依赖 | 用途与取得方式 |
| --- | --- |
| [research](../research/README.md) | 证据选择、当前调查与冲突来源判断的配套 Skill；将完整的 [公开 research 包](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research) 下载到本包旁边。它不是搜索引擎。 |
| 浏览器／会话负责人（本地源名为 `browser-relay`） | 仅在受控或登录页面需要：负责准确目标、授权会话复用、结果确认、窗口放置与清理。由宿主提供相应方法和真实浏览器／下载 API；本包不附私人适配器或公开 browser-relay 包。 |
| 网络诊断负责人（本地源名为 `network`） | 仅在有证据的连接故障需要：使用接收方已有的授权诊断能力，区分传输与访问／捕获问题。无需强制安装 Mac 网络包，也不由此授权更改路由。 |
| 搜索／HTTP／浏览器工具、Python、Poppler、可选 curl | 是实际执行能力，需自行提供或按下文安装；下载 Skill 不等于安装工具或取得图书馆权限。 |

本地方法的职责关系仍保留：research 选择和判断证据，浏览器负责人管理准确的
授权界面，paper-retrieval 核对学术对象与取得的文件。检查脚本可单独运行；
完整收藏方法组合这些职责。

检索和下载需要宿主已有的搜索、HTTP 或浏览器工具。本地脚本需要 Python
3.10+ 和 PATH 中的 Poppler `pdfinfo`、`pdftotext`。macOS 可用
`brew install poppler`，Debian/Ubuntu 可用 `sudo apt install poppler-utils`；
公开直链下载示例还需 `curl`。上方命令用于帮助、文件检查和本地测试。

脚本输出字节数、SHA-256、页数及首尾页文字，拒绝非 PDF 与解析失败；
不会自动确认作品身份、内部缺页、版本等价或完整性。应核对正文与来源题录，
无文字页需渲染检查。本包不保证任意全文可得，不包含凭据库、登录捕获适配器、
CAJ 转换器或限制规避机制。图书馆权限仍由使用者的授权界面确认。未完成作品
及已验证标识应同时出现在对话交付和收藏清单中。

[来源与验证指南](references/sources-and-verification.md) 保留方法说明。
这是从维护者本地 Skill 独立改写的可移植版本，移除了私人记录、主机路径与
专用浏览器和图书馆机制。原创内容采用 [MIT 许可](LICENSE)；Poppler 和取得
的出版物保留各自权利，本包不附第三方代码或出版物。
