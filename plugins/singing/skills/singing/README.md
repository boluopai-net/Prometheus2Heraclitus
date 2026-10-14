# 练唱 · singing

[中文](README.zh-CN.md)

A reusable Skill for turning a chosen song into a practical loop: find usable
accompaniment and synchronized lyrics, record a separate vocal take, return it
for listening, and compare a meaningful phrase with the actual reference audio.
Feedback connects pitch, timing, diction, and expression to a concrete next
attempt. It does not require a fixed curriculum or assume a singer's range.

Copy the complete `singing/` directory into the Skill location supported by your
agent host. Start with [SKILL.md](SKILL.md). Example request: “Help me practice
this chorus using my reference and microphone take; return the recording and
show where the entrances differ.” The host must actually support the requested
audio access, media playback, or application operation; installing this package
does not supply those capabilities.

| Dependency or composition | Role and acquisition |
| --- | --- |
| Required supporting Skills | None; the singing method is contained here. |
| Optional [research](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research) | Investigate accompaniment sources; download its complete package if needed. Singing retains audition and practice judgment. |
| Optional [YinYang](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang) | Broader user/model relationship; download its complete package if wanted. No private portrait is included or required. |
| Python 3.9+ | Required only for the bundled WAV checker; obtain from [Python](https://www.python.org/downloads/). |
| Recorder/DAW, audio playback, optional analysis tools | Required according to the requested operation, supplied by your host; routes and upstream links are in the tool guide. |

Download linked Skill directories through the repository's native source archive
or clone, retaining each complete package and its license.

The [tool guide](references/tools.md) describes supplied-file use, optional
FFmpeg, analysis libraries, and a separately installed Logic Pro/MCP route.
The [comparison guide](references/audio-evidence.md) explains evidence limits.
The read-only [WAV checker](scripts/check_wav.py) needs Python 3.9+ only:

```sh
python3 scripts/check_wav.py /path/to/take.wav
```

It checks integer PCM WAV integrity and signal metrics; it does not listen,
record, extract pitch, or score singing. Use your own recorder/DAW and authorized
media. Keep raw takes, personal preferences, account details, and library records
in your own session storage. Free viewing does not grant media redistribution.

This is a portable adaptation of an author-maintained local singing workflow.
Private singer profiles, attributable personal records, recordings, host paths,
credentials, and machine-specific integration receipts are excluded. Original
package prose and code are [MIT licensed](LICENSE). No third-party code or media
is bundled; linked tools and acquired music retain their respective rights.
