# video-subtitle

Retrieve one exact YouTube/Bilibili subtitle track and ground answers in the
portion actually read. The exact Skill identifier is `video-subtitle`. Install
this complete directory in your host's Skill directory and load [SKILL.md](SKILL.md),
or run the wrapper from the package directory.

Examples: “Summarize this video's argument from its subtitles”; “Explain the
claim around 12:30”; “Analyze Bilibili part 2 and state the coverage limit.”
A video URL alone does not trigger acquisition when spoken evidence is irrelevant.

| Dependency or owner | Relationship |
| --- | --- |
| Python and yt-dlp | Required execution tools for the bundled route; installed separately below, not Skills. |
| Host execution/file access | Runs the CLI and delivers actual read content; a path or successful connection alone is not evidence read by the model. |
| Enclosing learning/course or analysis owner | Supplies the question, relevant scope and learning/analysis judgment; video-subtitle owns track acquisition and grounding. No named companion Skill is required by the local source. |
| Host credential and authentication owner | Retains actual access/personal-authentication boundaries; the public helper uses no credentials. The private-origin connector is replaced, not an installation dependency. |

Requires Python 3.10+ and a current [yt-dlp](https://github.com/yt-dlp/yt-dlp)
executable on PATH. Install in a virtual environment:

```sh
python3 -m venv .venv
# POSIX shell; Windows: use .venv\Scripts\activate
. .venv/bin/activate
python -m pip install -U yt-dlp
python scripts/subtitles.py --help
python scripts/subtitles.py list 'https://www.youtube.com/watch?v=jNQXAC9IVRw' > listing.json
```

The example is a public video locator, not a promise that it offers a suitable
track. Inspect the returned `tracks`; select the exact language and kind, then:

```sh
python scripts/subtitles.py fetch 'SAME_VIDEO_URL' --listing listing.json --language 'EXACT_RETURNED_CODE' --kind manual --output transcript-run
python scripts/subtitles.py read 'RETURNED_FILE_PATH' --start 1 --count 120
python -m unittest discover -s tests -v
```

Choose `--kind automatic` only for a listed automatic track. Continue reading at
the returned `end_line + 1`; use a fresh output directory per fetch. The CLI
returns JSON, a timed subtitle file and companion metadata with SHA-256, size,
title, video ID, language/kind, source URL and retrieval time. It downloads no
video and uses no user config, external plugins or browser-cookie discovery.
It never saves signed track URLs in provenance. Temporary extraction metadata
is deleted when the operation finishes; outputs remain with the caller.

YouTube generated translation tracks are excluded by the extractor setting.
VTT/SRT read as raw text; JSON3 and Bilibili JSON render as timed cue lines.
Unknown JSON structures fail explicitly. Captions can contain recognition errors,
overlap or missing speech. Reading every cue establishes whole-track reading,
not complete speech coverage. Bilibili supports explicit `/video/` URLs, with
`?p=N` for parts; short links must first be resolved visibly. Multipart count and
whole-video coverage remain unknown, so answers must be scoped to the extracted
part. Private videos, login, CAPTCHA and site restrictions are outside this
wrapper. It does not bypass restrictions or silently substitute speech
recognition, translation, comments or another track. Network/extractor failures
remain failures; update yt-dlp or diagnose with its official tools when useful.

This original adaptation preserves the local Skill's track, scope and reading
method while replacing its private connector resource route and host audit
dependencies. Original package material is [MIT licensed](LICENSE). yt-dlp is a
separate dependency with its own [license and notices](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE);
its code is not bundled. Video/subtitle rights remain with their owners.

## 中文说明

取得 YouTube 或 Bilibili 的一个准确字幕轨道，并依据实际读到的范围作答。
准确标识为 `video-subtitle`。将整个目录复制到宿主 Skill 目录并加载
[SKILL.md](SKILL.md)，或从本目录直接运行脚本。

示例：“依据字幕总结这个视频的论证”；“解释 12:30 附近的主张”；
“分析 Bilibili 第 2 分 P 并说明覆盖范围”。若问题不依赖讲话内容，仅有视频
链接不应触发提取。

| 依赖或负责人 | 职责关系 |
| --- | --- |
| Python 与 yt-dlp | 本包提取路线所需的执行工具，按下文单独安装；不是 Skill。 |
| 宿主执行／文件访问能力 | 运行 CLI 并交付实际读取内容；文件路径或连接成功不等于模型已读到字幕。 |
| 外层课程／学习或分析负责人 | 决定问题、相关范围及学习／分析判断；video-subtitle 负责轨道取得与证据依据。本地源未要求某个具名配套 Skill。 |
| 宿主凭据与认证负责人 | 保留实际访问与个人认证边界；公开脚本不使用凭据。原有私人连接器已替换，不是安装依赖。 |

依赖 Python 3.10+ 和 PATH 中当前版本的 [yt-dlp](https://github.com/yt-dlp/yt-dlp)。
按上方命令创建虚拟环境并安装；Windows 使用 `.venv\Scripts\activate` 激活。
公开示例链接不保证存在合适字幕。先查看 listing.json 的轨道，再以准确代码和
类型提取；自动字幕应使用 `--kind automatic`。按返回的 `end_line + 1` 继续
分块读取，每次提取使用新的输出目录。结果为 JSON、带时间信息的字幕文件和
含 SHA-256、字节数、标题、视频 ID、语言/类型、来源 URL 与提取时间的元数据。

脚本不下载视频，不继承用户配置、外部插件或浏览器 Cookie。签名字幕直链不
写入来源记录，临时提取元数据在操作后删除，输出由调用者保留。YouTube 的
生成翻译轨道由提取器选项排除；VTT/SRT 保留原始文字，JSON3 与 Bilibili JSON
转为带时间的逻辑行，不认识的 JSON 结构明确失败。

字幕可能识别错误、重复或漏掉讲话。读完全部轨道不等于完整讲话覆盖。
Bilibili 使用显式 `/video/` 链接及 `?p=N`，短链接需先明确解析；总分 P 数与
整个视频覆盖未知，回答应限定于提取的分 P。本脚本不处理私有视频、登录、
验证码或站点限制，不规避限制，不暗中改用语音识别、翻译、评论或其他轨道。
网络或提取器失败仍是失败，可依据实际问题更新 yt-dlp 或用其官方工具诊断。

这是保留本地 Skill 的轨道、范围与阅读方法的原创可移植改写，替换了私人连接器
资源路由与主机审计依赖。原创内容采用 [MIT 许可](LICENSE)。yt-dlp 单独安装，
保留其 [许可与声明](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE)，本包
不附其代码。视频及字幕权利仍属于各自权利人。
