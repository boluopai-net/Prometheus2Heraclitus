# Tools and setup

Select capabilities from the recipient's actual environment. Commands below
illustrate local file operations; replace filenames with the selected assets
and inspect outputs. No installation or microphone access occurs by loading
this Skill.

## Supplied files and basic checks

Python 3.9+ runs the bundled read-only PCM WAV checker with no third-party
dependencies:

```sh
python3 scripts/check_wav.py /path/to/take.wav
```

Run from this package directory. It accepts uncompressed integer PCM WAV with
8-, 16-, 24-, or 32-bit samples and prints JSON. It reports duration, channels,
sample rate, per-channel peak/RMS dBFS, full-scale sample fraction, and the
fraction of frames below a chosen amplitude threshold. It is not a pitch
extractor, calibrated loudness meter, listening system, or singing score.
The silence threshold defaults to -60 dBFS and can be changed with
`--silence-db -50`. Recording context determines whether those values are useful.
Unsupported compressed/float WAV or a damaged file produces an error and exit 2.
It reads only the supplied file and never records, uploads, or changes it.

With separately installed [FFmpeg](https://ffmpeg.org/), inspect a video:

```sh
ffprobe -v error -show_format -show_streams -of json karaoke.mp4
```

For a supported stream, remux audio without re-encoding:

```sh
ffmpeg -n -i karaoke.mp4 -map 0:a:0 -vn -c:a copy backing.mka
```

Matroska audio may not import into a particular DAW. Choose a compatible
container for the actual codec, or decode into a derived PCM WAV; keep the
original file and offsets. A PCM derivative for the checker can be made with:

```sh
ffmpeg -n -i input-audio.m4a -map 0:a:0 -c:a pcm_s24le take-check.wav
```

These commands do not validate lyrics, cleanliness, export rights, or perceptual
quality. Use actual frame inspection and listening for those judgments. FFmpeg
options are documented in its [official manual](https://ffmpeg.org/ffmpeg.html).

## Recorder and DAW operation

Use a recorder or DAW already available through the host's supported tools.
Identify the live project, selected track, input/output devices, and current
transport before changing them. Discover the current schema or app controls;
tool names in documentation are not proof of availability. Operate under the
host's focus, desktop, filesystem, and permission boundaries. Preserve other
work, read back uncertain mutations before retrying, and verify stopped
transport plus the new raw audio artifact at completion.

Logic Pro is an optional macOS route. It requires a recipient-owned installation,
an audio device, the required microphone permissions, and a working control
channel. [MongLong0214/logic-pro-mcp](https://github.com/MongLong0214/logic-pro-mcp)
is an independently maintained optional MCP implementation. Follow its current
upstream installation and [setup documentation](https://github.com/MongLong0214/logic-pro-mcp/tree/main/docs)
for the installed version. Discover its exposed schemas and operation-specific
requirements; verify handshake, target application, live project/track reads,
and the intended transport route before recording. Supported app variants and
permission requirements can change. Installing a binary does not prove any
of these operations work on the recipient's host.

An app-bound Accessibility/API route can be used when available and permitted,
with live controls and readback. Neither a stale project snapshot nor synthesized
placeholder track data is a safe live target. Do not assume several server
instances can share MIDI endpoints. Use the upstream ownership requirements.
DAW controls, file diagnostics, audio listening, and pitch analysis are separate
capabilities; report which actually worked. A `logic_audio` file-analysis result,
if exposed, does not by itself establish reference-performance comparison.

## Pitch and listening

Use an existing audio-capable model or player for listening only if it actually
receives the audio. Optional analysis libraries include
[Parselmouth](https://parselmouth.readthedocs.io/en/stable/) for Praat-based
analysis and [librosa](https://librosa.org/doc/) for signal processing. They are
not bundled or required; install through their documented setup only when the
task needs that capability. Consult the installed version's pitch API and
document algorithm, sample rate, hop size, pitch bounds, voicing confidence,
and alignment. A successful import is not accuracy evidence on mixed music.

External tools retain their own licenses. No third-party implementation or
media is copied into this package.
