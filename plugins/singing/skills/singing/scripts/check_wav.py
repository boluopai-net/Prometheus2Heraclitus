#!/usr/bin/env python3
"""Read-only signal diagnostics for integer PCM WAV; no singing assessment."""

import argparse
import json
import math
import sys
import wave


def dbfs(amplitude):
    return 20 * math.log10(amplitude) if amplitude > 0 else None


def inspect_wav(path, silence_db):
    threshold = 10 ** (silence_db / 20)
    with wave.open(str(path), "rb") as source:
        channels, width, rate, declared, compression, _ = source.getparams()
        if compression != "NONE" or width not in (1, 2, 3, 4):
            raise ValueError("Requires uncompressed 8/16/24/32-bit integer PCM WAV")
        if channels < 1 or rate < 1:
            raise ValueError("Invalid channel count or sample rate")
        scale = 2 ** (width * 8 - 1)
        peaks = [0.0] * channels
        squares = [0.0] * channels
        full_scale = [0] * channels
        frames = silent = 0
        while True:
            block = source.readframes(4096)
            if not block:
                break
            stride = channels * width
            if len(block) % stride:
                raise ValueError("Truncated PCM frame")
            for offset in range(0, len(block), stride):
                frame_silent = True
                for channel in range(channels):
                    start = offset + channel * width
                    raw = block[start:start + width]
                    value = raw[0] - 128 if width == 1 else int.from_bytes(
                        raw, "little", signed=True
                    )
                    amplitude = abs(value) / scale
                    peaks[channel] = max(peaks[channel], amplitude)
                    squares[channel] += amplitude * amplitude
                    full_scale[channel] += int(value in (-scale, scale - 1))
                    frame_silent = frame_silent and amplitude < threshold
                frames += 1
                silent += int(frame_silent)
        if frames != declared:
            raise ValueError("Truncated audio: frame count differs from WAV header")
        if not frames:
            raise ValueError("WAV contains no audio frames")
    return {
        "frames": frames,
        "duration_seconds": frames / rate,
        "sample_rate_hz": rate,
        "channels": channels,
        "sample_width_bits": width * 8,
        "silence_threshold_dbfs": silence_db,
        "silent_frame_fraction": silent / frames,
        "channel_metrics": [
            {
                "channel": channel + 1,
                "peak_dbfs": dbfs(peaks[channel]),
                "rms_dbfs": dbfs(math.sqrt(squares[channel] / frames)),
                "full_scale_sample_fraction": full_scale[channel] / frames,
            }
            for channel in range(channels)
        ],
        "definitions": {
            "silence": "All channels below amplitude threshold in a frame",
            "full_scale": "Samples equal to minimum or maximum representable integer",
            "null_dbfs": "Zero amplitude; negative infinity represented as null",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Existing integer PCM WAV to read")
    parser.add_argument("--silence-db", type=float, default=-60.0)
    args = parser.parse_args()
    if not math.isfinite(args.silence_db) or args.silence_db > 0:
        parser.error("--silence-db must be a finite number at or below zero")
    try:
        result = inspect_wav(args.path, args.silence_db)
    except (OSError, EOFError, wave.Error, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
