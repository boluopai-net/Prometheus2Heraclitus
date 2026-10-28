# singing

[English](README.md)

这个可复用 Skill 将选定的歌曲变成实际练唱循环：寻找可用伴奏和同步歌词，
单独录下人声，及时返回录音供回听，再依据实际原唱音频比较有意义的乐句。
反馈把音高、节奏、咬字和表达联系到下一次具体尝试，不要求固定课程，也不预设歌者音域。

将完整 `singing/` 目录放入你的智能体宿主支持的 Skill 位置，从
[SKILL.md](SKILL.md) 开始。例如：“用我提供的原唱和麦克风录音帮我练这个副歌，
返回录音，并指出入句时间的差异。”宿主必须实际支持所需的音频读取、媒体播放或
应用操作；安装这个包不会自动提供这些能力。

| 依赖或组合 | 用途与获取方式 |
| --- | --- |
| 必需的支持 Skill | 无；练唱方法完整保存在本包中。 |
| 可选 [research](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research) | 调查伴奏来源；需要时下载完整包。伴奏试听和练唱判断仍由 singing 负责。 |
| 可选 [YinYang](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang) | 支持更广泛的用户与模型关系；需要时下载完整包。本包不含也不要求私人画像。 |
| Python 3.9+ | 仅 WAV 检查脚本需要；从 [Python](https://www.python.org/downloads/) 获取。 |
| 录音工具或 DAW、音频播放及可选分析工具 | 按请求的操作需要，由宿主提供；路线和上游链接见工具说明。 |

通过仓库原生源码归档或克隆获取链接中的 Skill 目录，保留各自的完整包和许可证。

[工具说明](references/tools.md)介绍已有文件的使用方法、可选 FFmpeg、分析库，
以及另行安装的 Logic Pro/MCP 路线。[比较说明](references/audio-evidence.md)
解释证据的适用范围。只读 [WAV 检查脚本](scripts/check_wav.py)仅需 Python 3.9+：

```sh
python3 scripts/check_wav.py /path/to/take.wav
```

它检查整数 PCM WAV 的完整性和信号指标，不负责听音、录音、提取音高或给演唱评分。
使用你自己的录音工具或 DAW 及获准使用的媒体。原始录音、个人偏好、账户资料和
曲库记录留在你自己的会话存储中。可免费观看不代表可以重新分发媒体。

这是作者维护的本地练唱工作流的可移植改编，排除了私人歌者画像、可归属个人记录、
录音、主机路径、凭据和特定机器的集成回执。包内原创文字与代码采用
[MIT 许可证](LICENSE)。未捆绑第三方代码或媒体；链接的工具和获取的音乐保留各自权利。
