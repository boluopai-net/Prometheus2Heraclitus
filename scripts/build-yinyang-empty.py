#!/usr/bin/env python3
"""Refresh/check the shared method selection for YinYang Empty, without essays or diagrams."""
import argparse
import os
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / 'skills/yinyang'
EMPTY = ROOT / 'skills/yinyang-empty'
WEB = 'https://boluopai.net/repositories/prometheus/source/skills/yinyang/'
GUIDES = ('orientation', 'person', 'counterpart', 'relationship', 'environment', 'revision')
SELECTION = {'LICENSE': 'LICENSE'}
for edition in ('.md', '.zh-CN.md'):
    SELECTION.update({f'references/formation/{name}{edition}': f'references/formation/{name}{edition}' for name in GUIDES})
    SELECTION.update({
        f'references/formation/personal-material{edition}': f'references/personal-material{edition}',
        f'references/design-and-revision{edition}': f'references/design-and-revision{edition}',
        f'references/docs/core-views{edition}': f'references/core-views{edition}',
        f'references/docs/creation-method{edition}': f'references/creation-method{edition}',
    })
LINKS = {**SELECTION}
for edition in ('.md', '.zh-CN.md'):
    LINKS.update({f'SKILL{edition}': f'SKILL{edition}', f'README{edition}': f'README{edition}',
                  f'references/docs/skill-package{edition}': f'references/package{edition}'})
AUTHORED = {'SKILL.md', 'SKILL.zh-CN.md', 'README.md', 'README.zh-CN.md',
            'references/package.md', 'references/package.zh-CN.md'}
AUTHORED.update(f'references/situated/{name}.md' for name in GUIDES)
AUTHORED.update({'references/personal/README.md', 'references/personal/sources.md'})
AUTHORED.update(f'references/personal/{name}/.gitkeep' for name in
                ('preferences', 'psychology', 'life', 'self-expression'))


def project(source, destination):
    text = (FULL / source).read_text()
    # Only this package fact differs: Full omits starters; Empty deliberately
    # supplies blank ones. Formation methods and philosophical content are shared.
    distribution = {
        'references/design-and-revision.md': (
            'Public distribution ships the common guides, with no filled or\nplaceholder private accounts.',
            'Empty ships the common guides, four empty Personal areas, and six\nSituated starters marked `status: unfilled`. These starters are not actual\naccounts; form their content from this person’s material.'),
        'references/design-and-revision.zh-CN.md': (
            '公开分发提供\n共同指引，不附带已填或占位的私人描述。',
            'Empty 提供共同指引、四个空 Personal 分区与六份标为 `status: unfilled` 的 Situated\n起始文件。起始文件不是实际描述，仍需结合本人的材料形成内容。'),
    }
    if source in distribution:
        old, new = distribution[source]
        if text.count(old) != 1:
            raise ValueError('Review the changed Full distribution statement: ' + source)
        text = text.replace(old, new)

    def link(match):
        href = match.group(1)
        parsed = urlsplit(href)
        if parsed.scheme or href.startswith(('#', '/', '//')):
            return match[0]
        target = (FULL / source).parent.joinpath(unquote(parsed.path)).resolve()
        relative = target.relative_to(FULL).as_posix()
        if not target.is_file():
            raise ValueError(f'Missing source reference in {source}: {href}')
        if relative in LINKS:
            new = os.path.relpath(EMPTY / LINKS[relative], (EMPTY / destination).parent)
        else:
            new = WEB + (relative[:-3] + '.html' if relative.endswith('.md') else relative)
        if parsed.query:
            new += '?' + parsed.query
        if parsed.fragment:
            new += '#' + parsed.fragment
        return '](' + new + ')'

    return re.sub(r'\]\(([^\s)]+)\)', link, text).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    expected = set(SELECTION.values()) | AUTHORED
    actual = {p.relative_to(EMPTY).as_posix() for p in EMPTY.rglob('*') if p.is_file()}
    unexpected = actual - expected
    if unexpected:
        raise ValueError('Unexpected Empty package files: ' + ', '.join(sorted(unexpected)))
    if not all((EMPTY / p).is_file() for p in AUTHORED):
        raise ValueError('Missing authored Empty entrypoint or package guide')
    changed = []
    for source, destination in SELECTION.items():
        original, target = FULL / source, EMPTY / destination
        content = project(source, destination) if source.endswith('.md') else original.read_bytes()
        if target.is_symlink():
            raise ValueError('Generated target is a symlink: ' + destination)
        if not target.is_file() or target.read_bytes() != content or target.stat().st_mode & 0o777 != original.stat().st_mode & 0o777:
            changed.append(destination)
            if args.apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                shutil.copymode(original, target)
    print(f'YinYang Empty: {len(SELECTION)} shared files, {len(changed)} {"updated" if args.apply else "differ"}; no docs or diagrams.')
    return 0 if args.apply or not changed else 1


if __name__ == '__main__':
    raise SystemExit(main())
