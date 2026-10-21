#!/usr/bin/env python3
"""Compare or project YinYang's common files between two source packages.

This is a source maintenance command, not a runtime installer or an exporter.
It never reads or copies either private reference tree. Legacy account layouts
must be migrated by their owner before common projection.
"""

import argparse
import re
import shutil
import stat
import sys
from pathlib import Path

LEGACY_ACCOUNTS = {
    "references/encounter.md",
    "references/models.md",
    "references/relationship.md",
    "references/sources.md",
    "references/usage.md",
}
PRIVATE_TREES = {"references/situated", "references/personal"}
ORIGIN_PREFIX = "用户自制：".encode()


def projected_bytes(relative, original, destination):
    """Retain a situated discovery label while updating all canonical wording."""
    content = original.read_bytes()
    if relative != "SKILL.md" or not destination.is_file():
        return content
    # This package uses a single-line description scalar. Restrict inspection
    # to frontmatter, leaving every method and other metadata byte canonical.
    field = rb"(?m)^description:[ \t]*[\"']?"
    target_sections = destination.read_bytes().split(b"---", 2)
    if len(target_sections) != 3 or target_sections[0].strip():
        raise ValueError("Missing target entrypoint frontmatter")
    target_header = target_sections[1]
    target_field = re.search(field, target_header)
    if not target_field or not target_header[target_field.end() :].startswith(ORIGIN_PREFIX):
        return content
    sections = content.split(b"---", 2)
    if len(sections) != 3 or sections[0].strip():
        raise ValueError("Missing source entrypoint frontmatter")
    source_field = re.search(field, sections[1])
    if not source_field or sections[1][source_field.end() :].startswith(
        (b"|", b">", b"&", b"*", b"\n")
    ):
        raise ValueError("Origin prefix requires a single-line source description")
    start = source_field.end()
    if not sections[1][start:].startswith(ORIGIN_PREFIX):
        sections[1] = sections[1][:start] + ORIGIN_PREFIX + sections[1][start:]
    return b"---".join(sections)


def situated(path):
    return any(path == tree or path.startswith(tree + "/") for tree in PRIVATE_TREES)


def common_files(root):
    """Do not traverse either private directory, including its links."""
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
    legacy = sorted(
        relative for relative in LEGACY_ACCOUNTS
        if (path / relative).exists() or (path / relative).is_symlink()
    )
    if legacy:
        raise ValueError(
            "Legacy accounts require owner migration before common projection: "
            + ", ".join(legacy)
            + ". Form references/situated/{orientation,person,counterpart,relationship,environment}.md "
            "and references/personal/sources.md from their actual meaning; preserve unique "
            "private evidence before retiring the old paths. No files were changed."
        )
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
    changed = {}
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
        expected = projected_bytes(relative, original, destination)
        if (
            relative not in current
            or expected != destination.read_bytes()
            or stat.S_IMODE(original.stat().st_mode) != stat.S_IMODE(destination.stat().st_mode)
        ):
            changed[relative] = expected
    if args.apply:
        for relative, content in changed.items():
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            shutil.copystat(originals[relative], destination)
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
