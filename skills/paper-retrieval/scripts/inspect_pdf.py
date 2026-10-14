#!/usr/bin/env python3
"""Inspect local PDF bytes; this report never establishes scholarly identity."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


def inspect(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    if not data.startswith(b"%PDF-"):
        raise ValueError("not a PDF signature (HTML/error pages are rejected)")
    for tool in ("pdfinfo", "pdftotext"):
        if not shutil.which(tool):
            raise ValueError(f"missing {tool}; install Poppler")
    result = subprocess.run(["pdfinfo", str(path)], capture_output=True,
                            text=True, timeout=60, check=True)
    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.M)
    if not match or int(match[1]) < 1:
        raise ValueError("PDF page count unavailable")
    pages = int(match[1])
    samples = {}
    for label, page in (("first_page", 1), ("last_page", pages)):
        sample = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page),
                                 str(path), "-"], capture_output=True, text=True,
                                timeout=60, check=True)
        samples[label] = sample.stdout[:12000]
    return {"path": str(path), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "pages": pages,
            "parseable": True, "identity_verified": False,
            "completeness_verified": False, "samples": samples,
            "notice": "Inspect printed title/authors/version and ending; render image-only pages."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.pdf), ensure_ascii=False, indent=2))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Inspection failed: {exc}\n")


if __name__ == "__main__":
    main()
