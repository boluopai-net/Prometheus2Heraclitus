import functools
import http.server
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "subtitles.py"
spec = importlib.util.spec_from_file_location("subtitles", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
URL = "https://www.youtube.com/watch?v=fixture"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class SubtitleTests(unittest.TestCase):
    def test_scope_and_exactness(self):
        info = {"id": "part2", "title": "Part two", "subtitles": {
            "en.US": [{"ext": "vtt"}], "danmaku": [{"ext": "xml"}], "live_chat": [{"ext": "json"}]}}
        result = helper.describe("https://www.bilibili.com/video/BVfixture?p=2", info)
        self.assertEqual(result["video_scope"]["requested_page"], 2)
        self.assertIsNone(result["video_scope"]["covers_entire_video"])
        self.assertEqual(result["tracks"][0]["language"], "en.US")
        self.assertEqual(len(result["tracks"]), 1)
        with self.assertRaises(ValueError):
            helper.platform("https://www.youtube.com.evil.example/video")
        with self.assertRaises(ValueError):
            helper.platform("https://user:secret@youtube.com/watch?v=fixture")
        with self.assertRaises(ValueError):
            helper.platform("https://www.bilibili.com/video/BVfixture?p=1&p=2")

    def test_chunk_cli_and_json_cue_lines(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "captions.json"
            path.write_text(json.dumps({"body": [{"from": i, "to": i + 1, "content": f"cue {i}"}
                                                  for i in range(5)]}))
            result = subprocess.run([sys.executable, str(SCRIPT), "read", str(path),
                                     "--start", "2", "--count", "2"],
                                    check=True, capture_output=True, text=True)
            chunk = json.loads(result.stdout)
            self.assertEqual((chunk["start_line"], chunk["end_line"], chunk["remaining_lines"]), (2, 3, 2))
            self.assertIn("cue 1", chunk["text"])
            self.assertNotIn("cue 3", chunk["text"])
            self.assertEqual(helper.read_chunk(path, 4, 2)["remaining_lines"], 0)

    @unittest.skipUnless(shutil.which("yt-dlp"), "yt-dlp unavailable")
    def test_actual_ytdlp_download_and_refusal_boundaries(self):
        # Mock only remote extraction. The installed yt-dlp CLI downloads real
        # local HTTP bytes through the helper's load-info-json route.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            content = "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nHello fixture\n"
            (root / "source.vtt").write_text(content)
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
                       functools.partial(QuietHandler, directory=temporary))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                info = {"id": "fixture", "title": "Fixture", "extractor": "generic",
                        "extractor_key": "Generic", "webpage_url": URL,
                        "url": "http://127.0.0.1/unused.mp4", "ext": "mp4",
                        "subtitles": {"en.US": [{"ext": "vtt", "url":
                            f"http://127.0.0.1:{server.server_port}/source.vtt"}]}}
                listing = root / "listing.json"
                listing.write_text(json.dumps(helper.describe(URL, info)))
                with patch.object(helper, "extract", return_value=info):
                    with self.assertRaisesRegex(ValueError, "exact listed"):
                        helper.fetch(URL, listing, "en", "manual", root / "wrong")
                    result = helper.fetch(URL, listing, "en.US", "manual", root / "out")
                    self.assertEqual(Path(result["file"]["path"]).read_text(), content)
                    self.assertEqual(helper.read_chunk(result["file"]["path"], 1, 120)["file"]["sha256"],
                                     result["file"]["sha256"])
                    self.assertNotIn("127.0.0.1", Path(result["metadata_path"]).read_text())
                    with self.assertRaisesRegex(ValueError, "already contains"):
                        helper.fetch(URL, listing, "en.US", "manual", root / "out")
                with patch.object(helper, "extract", return_value={**info, "id": "other"}):
                    with self.assertRaisesRegex(ValueError, "video_id mismatch"):
                        helper.fetch(URL, listing, "en.US", "manual", root / "other")
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


if __name__ == "__main__":
    unittest.main()
