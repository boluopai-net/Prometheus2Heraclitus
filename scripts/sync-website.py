#!/usr/bin/env python3
"""Export/check the complete committed public Site tree, excluding QA probes."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

EXCLUSIONS = [".playwright-cli/", "design-evidence/", "design-qa.md"]
DEFAULT_TARGET = Path(__file__).resolve().parents[1] / "website"


def git(source, *args):
    return subprocess.check_output(["git", "-C", str(source), *args])


def excluded(path):
    return any(path.startswith(item) if item.endswith("/") else path == item
               for item in EXCLUSIONS)


def snapshot(source, revision):
    if not re.fullmatch(r"[0-9a-fA-F]{4,40}", revision):
        raise ValueError("Revision must be a commit SHA, not a mutable branch or tag")
    commit = git(source, "rev-parse", "--verify", revision + "^{commit}").decode().strip()
    entries = []
    for record in git(source, "ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
        if not record:
            continue
        header, raw_path = record.split(b"\t", 1)
        mode, kind, oid = header.decode().split()
        path = raw_path.decode("utf-8")
        if excluded(path):
            continue
        if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
            raise ValueError(f"Unsafe source path: {path}")
        if kind != "blob" or mode not in ("100644", "100755", "120000"):
            raise ValueError(f"Unsupported Git entry: {path} ({mode} {kind})")
        if path == "SOURCE.json":
            raise ValueError("Source SOURCE.json collides with snapshot provenance")
        # Secret contents must never be printed; reject common credential carriers.
        name = PurePosixPath(path).name.lower()
        if (name.startswith(".env") and name != ".env.example") or name.endswith((".pem", ".key")):
            raise ValueError(f"Credential candidate requires source review: {path}")
        entries.append((path, mode, oid))
    request = "".join(oid + "\n" for _, _, oid in entries).encode()
    result = subprocess.run(["git", "-C", str(source), "cat-file", "--batch"],
                            input=request, stdout=subprocess.PIPE, check=True).stdout
    files, offset = {}, 0
    for path, mode, oid in entries:
        end = result.index(b"\n", offset)
        actual_oid, kind, size = result[offset:end].decode().split()
        if actual_oid != oid or kind != "blob":
            raise ValueError(f"Unexpected Git blob: {path}")
        start, length = end + 1, int(size)
        files[path] = (mode, result[start:start + length])
        offset = start + length + 1
    example = files.get(".env.example")
    if example:
        for line in example[1].decode().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and ("=" not in line or line.split("=", 1)[1].strip() not in ("", '""', "''")):
                raise ValueError(".env.example contains a nonempty value; review without printing it")
    provenance = {
        "source_project": "boluopai public website (native Sites Git repository)",
        "source_commit": commit,
        "excluded_paths": EXCLUSIONS,
        "content_owner": "Site owns independent prose, presentation and implementation; skills/yinyang owns canonical YinYang prose",
        "publication": "Native Sites source publication remains separate from collection GitHub publication",
        "reuse": "Preserve existing rights and third-party notices; independent deployment needs its own Site project_id and runtime secrets",
    }
    files["SOURCE.json"] = ("100644", (json.dumps(provenance, ensure_ascii=False, indent=2) + "\n").encode())
    return commit, files


def inventory(target):
    found = set()
    if target.is_symlink():
        raise ValueError("Target directory must not be a symlink")
    if target.exists():
        for parent, dirs, names in os.walk(target, followlinks=False):
            for name in dirs[:]:
                path = Path(parent) / name
                if path.is_symlink():
                    found.add(path.relative_to(target).as_posix())
                    dirs.remove(name)
            found.update((Path(parent) / name).relative_to(target).as_posix() for name in names)
    return found


def check(target, files):
    actual = inventory(target)
    errors = [f"Missing: {p}" for p in sorted(files.keys() - actual)]
    errors += [f"Unexpected: {p}" for p in sorted(actual - files.keys())]
    for name in sorted(actual & files.keys()):
        path, (mode, data) = target / name, files[name]
        if mode == "120000":
            equal = path.is_symlink() and os.fsencode(os.readlink(path)) == data
        else:
            equal = not path.is_symlink() and path.is_file() and path.read_bytes() == data
            equal = equal and bool(path.stat().st_mode & 0o111) == (mode == "100755")
        if not equal:
            errors.append(f"Bytes or mode differ: {name}")
    return errors


def apply(target, files):
    # This directory is wholly generated. Remove stale entries before writing.
    for name in sorted(inventory(target), reverse=True):
        (target / name).unlink()
    if target.exists():
        for parent, dirs, _ in os.walk(target, topdown=False):
            for name in dirs:
                (Path(parent) / name).rmdir()
    target.mkdir(parents=True, exist_ok=True)
    for name, (mode, data) in files.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if mode == "120000":
            path.symlink_to(os.fsdecode(data))
        else:
            path.write_bytes(data)
            path.chmod(0o755 if mode == "100755" else 0o644)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--revision", required=True, help="Exact committed Site revision")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Generated output; default: collection website/")
    parser.add_argument("--apply", action="store_true", help="Replace the generated target; default only checks")
    args = parser.parse_args()
    target = args.target.absolute()
    source = args.source.resolve()
    collection = DEFAULT_TARGET.parent
    if target == source or target in source.parents or target == collection or target in collection.parents:
        parser.error("Target must not contain the source or collection checkout")
    if source in target.parents:
        parser.error("Target must not be inside the source checkout")
    if collection in target.parents and target != DEFAULT_TARGET:
        parser.error("Within the collection, only website/ is a generated target")
    commit, files = snapshot(source, args.revision)
    if args.apply:
        if not check(target, files):
            print(f"Unchanged: {commit} ({len(files) - 1} source files)")
            return 0
        apply(target, files)
    errors = check(target, files)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Verified: {commit} ({len(files) - 1} source files; bytes, modes and coverage)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Snapshot failed: {error}", file=sys.stderr)
        sys.exit(1)
