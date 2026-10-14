#!/usr/bin/env python3
"""Render a portable wheel with an independently sampled initial result."""

import argparse
import json
import math
import secrets
import uuid
from pathlib import Path


def render(options, speed=3, output_format="standalone"):
    if (
        not isinstance(options, list)
        or not 1 <= len(options) <= 100
        or any(not isinstance(x, str) or not x.strip() or len(x) > 200 for x in options)
        or len(set(options)) != len(options)
    ):
        raise ValueError(
            "Expected 1–100 distinct nonempty option strings, at most 200 characters each"
        )
    if not math.isfinite(speed) or not 0.25 <= speed <= 3:
        raise ValueError("Speed must be between 0.25 and 3")
    config = {
        "options": options,
        "speed": speed,
        "runId": str(uuid.uuid4()),
        "drawIndex": secrets.randbelow(len(options)),
    }
    template = (Path(__file__).resolve().parents[1] / "assets/wheel.html").read_text(encoding="utf-8")
    payload = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
    fragment = template.replace("__WHEEL_ID__", "wheel-" + config["runId"]).replace(
        "__WHEEL_CONFIG__", payload
    )
    if output_format == "standalone":
        shell = (Path(__file__).resolve().parents[1] / "assets/standalone.html").read_text(encoding="utf-8")
        return shell.replace("__WHEEL_FRAGMENT__", fragment), config
    if output_format != "inline":
        raise ValueError("Format must be standalone or inline")
    return fragment, config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--options", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--speed", type=float, default=3)
    parser.add_argument("--format", choices=["standalone", "inline"], default="standalone")
    args = parser.parse_args()
    fragment, config = render(json.loads(args.options.read_text(encoding="utf-8")), args.speed, args.format)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(fragment, encoding="utf-8")
    print(
        json.dumps(
            {
                "path": str(args.output.resolve()),
                "runId": config["runId"],
                "selected": config["options"][config["drawIndex"]],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
