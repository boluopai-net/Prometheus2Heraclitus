---
name: video-subtitle
description: "视频字幕：提取 YouTube 与 Bilibili 的字幕并依据实际读到的讲话文本作答。 Retrieve exact subtitle tracks and read scoped spoken evidence when an answer materially depends on a YouTube or Bilibili video and usable authoritative text is absent. A video URL alone does not trigger this capability."
---

# Video Subtitle

Keep the answer in contact with the voice it claims to understand. Evidence
belongs to one video, one returned track and the portion actually retrieved and
read. A fetched artifact establishes acquisition; only read content grounds the
answer. Use this package when the task materially depends on spoken content and
reliable usable authoritative text is not already present. Metadata, comments,
danmaku and another summary cannot silently replace it.

This Skill owns triggering, exact-track choice, video/part scope, chunk reading
and evidence grounding. The enclosing learning/course or analysis owner decides
the question, relevance and learning judgment; the host owns tool access,
credential handling and actual personal-authentication boundaries. The local
source names no downloadable companion Skill for these roles. See the
[dependency and owner table](README.md): Python and yt-dlp are execution
dependencies, and the private connector formerly used for transport is not a
standard or required public companion.

## Concrete portable route

Use Python 3.10+ and `yt-dlp` on PATH; follow [setup and examples](README.md).
The bundled wrapper has no browser-cookie discovery, private connector, login
adapter, or media-download step. Use it from this package directory:

```sh
python3 scripts/subtitles.py list 'VIDEO_URL' > listing.json
python3 scripts/subtitles.py fetch 'VIDEO_URL' --listing listing.json --language 'EXACT_CODE' --kind manual --output transcript-run
python3 scripts/subtitles.py read transcript-run/RETURNED_FILENAME --start 1 --count 120
```

Inspect listing JSON before fetching. Replace placeholders with the actual URL,
one exact returned code, its returned kind (`manual` or `automatic`), and the
returned file path. Provider codes are case-sensitive and may contain dots or
hyphens. Never normalize, guess, translate, prefix-match or select `all`. Prefer
a suitable manual track when present; identify automatic captions and their
possible recognition errors. YouTube generated translations are excluded by
the extractor setting; verify the track's provenance if the provider/extractor
classification is unclear. Do not silently translate or substitute another
track when the selected track is absent.

Fetch re-extracts metadata, checks URL/video/scope against the listing and requests
only the exact selected track. Inspect current title, video ID, track, scope,
file bytes/hash, retrieval date and companion `metadata.json`. Signed provider
URLs exist only in a disposable temporary input, not saved metadata. Keep local
output directories unique; the helper refuses artifact overwrites. Its metadata
is provenance, never the transcript body. Read the returned actual file and
compare the read hash with fetch metadata before attributing its content.

## Scope and reading

Use explicit Bilibili `/video/` URLs and `?p=N` for a requested part; resolve short
links visibly before invocation. The wrapper conservatively reports the requested
page and unknown multipart page count/whole-video coverage. It does not establish
that all parts were obtained. Verify the extracted title/identity against the
requested part, and describe the answer as limited to that extracted part. Fetch
other required parts separately using their explicit URLs. A scope/identity
mismatch between listing and fetch stops adoption; list again and investigate.
Do not transfer Bilibili multipart claims to YouTube.

Read bounded chunks, continuing from `end_line + 1` until needed coverage is
established. The reader returns 1-based ranges, total and remaining lines plus
the file hash; for JSON/JSON3 it renders timed cues as separate logical lines.
VTT/SRT remain raw timed text, retaining overlap and repetitions. Treat cue count
and timestamps as evidence rather than assuming repetition means new speech.
For whole-track summaries, structure or judgments read all chunks, including
the ending, and inspect missing/empty cues or unexplained time gaps. Preserve a
compact working outline; do not copy a full transcript into unrelated durable
memory. For local timestamp questions read the needed range and identify that
scope. If a read fails, state the last confirmed range and answer only from it.
A complete file read is whole-track coverage, not proof of all spoken content:
captions may omit speech, and Bilibili multipart scope remains unknown.

## Failure and completion

No available track, extractor/network errors, access restrictions and incomplete
readback are different boundaries. Report the failing operation and what usable
evidence was actually obtained. Update `yt-dlp` or diagnose current official
tool behavior for a concrete extractor failure; do not evade restrictions or
claim subtitles do not exist merely because one route failed. This wrapper
does not handle login, CAPTCHA, geo restrictions or private videos. Any other
authorized source or explicit user-provided transcript must be separately
identified and verified; never hide a switch to speech recognition, translation,
danmaku or an approximate summary. Existing host permission, credential and
personal-authentication boundaries remain with their owners.

Completion requires the same URL/video/scope across list and fetch, one exact
listed code/kind, a nonempty downloaded artifact with provenance, matching read
hash, and actual cue text read for the claimed range. The answer cites video,
track kind/language and useful timestamps, and states material caption/part/read
limits. Tool installation, a listing, a path or metadata alone is not completion.

## Provenance

This original public adaptation retains the source method's exact-track,
multipart-scope and chunk-read distinctions, replacing its private file-resource
bridge and host audit ledger with the bundled standard `yt-dlp` wrapper. No
private helper implementation, connector ID, cookie discovery or account data
is distributed. [yt-dlp](https://github.com/yt-dlp/yt-dlp) is installed separately
under its own licensing; video/subtitle rights remain with their owners.
