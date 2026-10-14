#!/usr/bin/env python3
"""List/fetch an exact public track with yt-dlp, or read a bounded local chunk."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


def platform(url):
    p = urlsplit(url)
    host = (p.hostname or "").lower()
    if p.scheme != "https" or p.username or p.password:
        raise ValueError("use an HTTPS video URL without credentials")
    if host in ("youtu.be", "youtube.com", "www.youtube.com", "m.youtube.com"):
        return "youtube"
    if host in ("bilibili.com", "www.bilibili.com") and "/video/" in p.path:
        pages = parse_qs(p.query, keep_blank_values=True).get("p", ["1"])
        if len(pages) != 1 or not pages[0].isdigit() or int(pages[0]) < 1:
            raise ValueError("use one positive Bilibili p parameter")
        return "bilibili"
    raise ValueError("supported URLs: YouTube; explicit Bilibili /video/ URL with ?p=N for a part")


def run_ytdlp(arguments):
    binary = shutil.which("yt-dlp")
    if not binary:
        raise ValueError("yt-dlp missing; install it as described in README")
    # Ignore user config and plugins: neither cookies nor media downloads are inherited.
    result = subprocess.run([binary, "--ignore-config", "--no-plugin-dirs",
                             "--no-playlist", "--socket-timeout", "30",
                             "--retries", "1", "--quiet", *arguments],
                            capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise ValueError("yt-dlp failed (access/network/extractor boundary); no transcript established. "
                         "Run yt-dlp --ignore-config --no-plugin-dirs --list-subs URL locally to diagnose.")
    return result.stdout


def extract(url):
    site = platform(url)
    options = ["--skip-download", "--dump-single-json"]
    if site == "youtube":
        options += ["--extractor-args", "youtube:skip=translated_subs"]
    info = json.loads(run_ytdlp([*options, "--", url]))
    if info.get("_type") in ("playlist", "multi_video") or info.get("entries"):
        raise ValueError("multiple entries returned; select an explicit single video/part")
    if not info.get("id"):
        raise ValueError("missing video identity")
    return info


def describe(url, info):
    site = platform(url)
    scope = {"platform": site}
    if site == "bilibili":
        raw_page = parse_qs(urlsplit(url).query).get("p", ["1"])[0]
        if not raw_page.isdigit() or int(raw_page) < 1:
            raise ValueError("invalid Bilibili p parameter")
        scope.update(requested_page=int(raw_page), page_count=None,
                     covers_entire_video=None,
                     coverage_warning="Only this extracted part is established; multipart count is unknown.")
    tracks = []
    for kind, key in (("manual", "subtitles"), ("automatic", "automatic_captions")):
        for code, formats in info.get(key, {}).items():
            if code in ("live_chat", "danmaku") or not formats:
                continue
            tracks.append({"language": code, "kind": kind,
                           "formats": sorted({f.get("ext", "unknown") for f in formats})})
    return {"source_url": url, "video_id": str(info["id"]), "title": info.get("title"),
            "duration": info.get("duration"), "video_scope": scope, "tracks": tracks}


def file_record(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def fetch(url, listing, language, kind, output):
    expected = json.loads(Path(listing).read_text(encoding="utf-8"))
    info = extract(url)
    current = describe(url, info)
    for key in ("source_url", "video_id", "video_scope"):
        if current[key] != expected.get(key):
            raise ValueError(f"list/fetch {key} mismatch; list again and inspect scope")
    selected = {"language": language, "kind": kind}
    if language in ("all", "live_chat", "danmaku") or not any(
            all(track[k] == v for k, v in selected.items()) for track in expected.get("tracks", [])):
        raise ValueError("select one exact listed language and kind")
    key = "subtitles" if kind == "manual" else "automatic_captions"
    formats = info.get(key, {}).get(language)
    if not formats:
        raise ValueError("selected track no longer available")
    # Download only this fresh track. Keep provider URLs in a temporary file,
    # never in the published provenance record. No cookie source is configured.
    info["subtitles"] = {language: formats} if kind == "manual" else {}
    info["automatic_captions"] = {language: formats} if kind == "automatic" else {}
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="subtitle-") as temporary:
        stage = Path(temporary)
        info_path = stage / "input.json"
        info_path.write_text(json.dumps(info), encoding="utf-8")
        run_ytdlp(["--load-info-json", str(info_path), "--skip-download",
                    "--write-subs" if kind == "manual" else "--write-auto-subs",
                    "--sub-langs", "^" + re.escape(language) + "$",
                    "--sub-format", "vtt/srt/json3/json/best",
                    "--output", str(stage / "track.%(ext)s")])
        files = [p for p in stage.iterdir() if p.is_file() and p != info_path]
        if len(files) != 1 or not files[0].stat().st_size:
            raise ValueError("expected one nonempty subtitle file; fetch remains unverified")
        target = output / files[0].name
        # Refuse overwrites, including existing metadata, so provenance stays coherent.
        metadata = output / "metadata.json"
        if target.exists() or metadata.exists():
            raise ValueError("output already contains this artifact; use a fresh directory")
        with target.open("xb") as destination:
            destination.write(files[0].read_bytes())
    current.update(selected_track=selected, file=file_record(target),
                   retrieved_at=datetime.now(timezone.utc).isoformat(),
                   track_completeness="downloaded; read and inspect cues before claiming complete coverage")
    metadata.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**current, "metadata_path": str(metadata)}


def read_chunk(path, start, count):
    if start < 1 or count < 1 or count > 500:
        raise ValueError("start must be >=1; count must be 1..500")
    lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    # JSON tracks can occupy one huge line. Render their cues as separate lines.
    if Path(path).suffix in (".json", ".json3"):
        document = json.loads("\n".join(lines))
        if "body" in document:
            lines = [f"[{cue.get('from')}–{cue.get('to')}] {cue['content']}"
                     for cue in document["body"]]
        elif "events" in document:
            lines = [f"[{cue.get('tStartMs')}ms] " + "".join(s.get("utf8", "") for s in cue.get("segs", []))
                     for cue in document["events"] if cue.get("segs")]
        else:
            raise ValueError("unknown JSON subtitle structure; inspect with a format-aware reader")
    end = min(start - 1 + count, len(lines))
    if start > len(lines):
        raise ValueError(f"start exceeds total lines ({len(lines)})")
    return {"file": file_record(Path(path)), "start_line": start, "end_line": end,
            "total_lines": len(lines), "remaining_lines": len(lines) - end,
            "text": "\n".join(lines[start - 1:end])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("url")
    fetching = sub.add_parser("fetch")
    fetching.add_argument("url")
    fetching.add_argument("--listing", required=True)
    fetching.add_argument("--language", required=True)
    fetching.add_argument("--kind", choices=("manual", "automatic"), required=True)
    fetching.add_argument("--output", required=True)
    reader = sub.add_parser("read")
    reader.add_argument("path")
    reader.add_argument("--start", type=int, default=1)
    reader.add_argument("--count", type=int, default=120)
    args = parser.parse_args()
    try:
        if args.action == "list":
            result = describe(args.url, extract(args.url))
        elif args.action == "fetch":
            result = fetch(args.url, args.listing, args.language, args.kind, args.output)
        else:
            result = read_chunk(args.path, args.start, args.count)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Subtitle operation failed: {exc}\n")


if __name__ == "__main__":
    main()
