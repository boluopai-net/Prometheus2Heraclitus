#!/usr/bin/env python3
"""Build or check portable Codex plugins from the collection's tracked Skills."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def expected_files(entry):
    name = entry['name']
    source = ROOT / 'skills' / name
    paths = subprocess.check_output(
        ['git', '-C', str(ROOT), 'ls-files', '-z', '--', 'skills/' + name]
    ).decode().split('\0')
    files = {}
    for relative in filter(None, paths):
        path = ROOT / relative
        if path.is_symlink():
            raise ValueError(f'Package source must be a regular file: {relative}')
        destination = 'skills/' + name + '/' + path.relative_to(source).as_posix()
        files[destination] = (path.read_bytes(), path.stat().st_mode & 0o777)
    if 'skills/' + name + '/SKILL.md' not in files:
        raise ValueError(f'Missing tracked Skill: {name}')
    license_name = 'CC-BY-NC-SA-4.0' if name in {'yinyang', 'yinyang-empty'} else 'MIT'
    manifest = {
        '$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
        'name': name,
        'version': entry['version'],
        'description': entry['description'],
        'author': {'name': 'boluopai', 'url': 'https://boluopai.net/'},
        'homepage': 'https://boluopai.net/repositories/',
        'repository': 'https://github.com/boluopai-net/Prometheus2Heraclitus',
        'license': license_name,
        'extensions': {'com.openai': {'interface': entry['interface']}},
    }
    files['plugin.json'] = ((json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode(), 0o644)
    files['LICENSE'] = ((source / 'LICENSE').read_bytes(), 0o644)
    files['assets/logo.svg'] = ((ROOT / 'assets/marketplace-icon.svg').read_bytes(), 0o644)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Regenerate plugin directories')
    args = parser.parse_args()
    subprocess.run([sys.executable, str(ROOT / 'scripts/build-yinyang-empty.py'),
                    *(['--apply'] if args.apply else [])], check=True)
    market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
    entries = market['plugins']
    names = {entry['name'] for entry in entries}
    sources = {p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')} - {'yinyang'}
    if names != sources or len(names) != len(entries):
        raise ValueError('Marketplace must cover each installable Skill exactly once (Full is reference-only)')
    count = 0
    for entry in entries:
        target = ROOT / 'plugins' / entry['name']
        if entry['source'] != {'source': 'local', 'path': './plugins/' + entry['name']}:
            raise ValueError('Unexpected marketplace source')
        files = expected_files(entry)
        if args.apply:
            if target.exists():
                shutil.rmtree(target)
            for name, (data, mode) in files.items():
                destination = target / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                destination.chmod(mode)
        actual = {p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()}
        if actual != set(files):
            raise ValueError(f'Plugin file coverage differs: {entry["name"]}')
        for name, (data, mode) in files.items():
            path = target / name
            if path.is_symlink() or path.read_bytes() != data or path.stat().st_mode & 0o777 != mode:
                raise ValueError(f'Plugin differs from source: {path}')
        count += len(files)
    print(f'Verified {len(entries)} portable plugins, {count} files, exact source bytes and modes.')


if __name__ == '__main__':
    main()
