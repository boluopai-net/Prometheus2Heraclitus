#!/usr/bin/env python3
"""Compare or project YinYang's common files between two source packages.

This is a source maintenance command, not a runtime installer or an exporter.
It never reads or copies the situated slots or the personal reference tree.
"""

import argparse
import shutil
import stat
import sys
from pathlib import Path

SITUATED = {
    "references/encounter.md",
    "references/models.md",
    "references/relationship.md",
    "references/sources.md",
    "references/usage.md",
}
PERSONAL = "references/personal"


def situated(path):
    return path in SITUATED or path == PERSONAL or path.startswith(PERSONAL + "/")


def common_files(root):
    """Do not traverse the personal directory, including its links."""
    found = {}

    def visit(directory):
        for path in sorted(directory.iterdir()):
            relative = path.relative_to(root).as_posix()
            if situated(relative):
                continue
            if path.is_symlink():
                raise ValueError(f"Common path is a symlink: {relative}")
            if path.is_dir():
                visit(path)
            elif path.is_file():
                found[relative] = path
            else:
                raise ValueError(f"Unsupported common path: {relative}")

    visit(root)
    return found


def package(value):
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_dir() or not (path / "SKILL.md").is_file():
        raise ValueError(f"Not a Skill package: {path}")
    for relative in SITUATED | {PERSONAL + "/README.md"}:
        if not (path / relative).is_file():
            raise ValueError(f"Missing situated slot: {relative} in {path}")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Canonical shared Skill directory")
    parser.add_argument("--target", required=True, help="Situated source Skill directory")
    parser.add_argument("--apply", action="store_true", help="Copy changed common files")
    args = parser.parse_args()
    source, target = package(args.source), package(args.target)
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("Source and target must be separate, non-nested packages")
    originals, current = common_files(source), common_files(target)
    stale = sorted(current.keys() - originals.keys())
    if stale:
        print("Unmatched target files; inspect and relocate or remove them before syncing:")
        print("\n".join(stale))
        return 2
    changed = []
    for relative, original in originals.items():
        destination = target / relative
        if destination.exists() and not destination.is_file():
            raise ValueError(f"Target file path is occupied by a directory: {relative}")
        # A target file may also occupy an ancestor of a newly added source file.
        for parent in destination.parents:
            if parent == target:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Target parent is not a directory: {parent.relative_to(target)}")
        if (
            relative not in current
            or original.read_bytes() != destination.read_bytes()
            or stat.S_IMODE(original.stat().st_mode) != stat.S_IMODE(destination.stat().st_mode)
        ):
            changed.append(relative)
    if args.apply:
        for relative in changed:
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(originals[relative], destination)
    print(
        f"{len(originals)} common files; {len(changed)} {'copied' if args.apply else 'differ'}; situated content untouched"
    )
    if changed and not args.apply:
        print("\n".join(changed))
    return 0 if args.apply or not changed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)
