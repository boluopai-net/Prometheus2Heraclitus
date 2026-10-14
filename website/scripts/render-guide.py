"""Render the bilingual practical guide from its maintained Markdown sources.

uv run --with markdown python scripts/render-guide.py
Shared site chrome is projected by refine-navigation.py after both editions exist.
"""
import html
import subprocess
import sys
from pathlib import Path

import markdown
from cjk_markdown import CjkBoldExtension

root = Path(__file__).resolve().parents[1]
for english in (False, True):
    source = root / 'content/guides' / ('getting-started.en.md' if english else 'getting-started.md')
    text = source.read_text()
    title = text.splitlines()[0].removeprefix('# ')
    md = markdown.Markdown(extensions=['md_in_html', 'sane_lists', 'tables', CjkBoldExtension()])
    rendered = md.convert(text)
    rendered = rendered.replace('<table>', '<div class="guide-table"><table>').replace('</table>', '</table></div>')
    lang, suffix = ('en', 'en/') if english else ('zh-CN', '')
    back = 'Resources &amp; Advice' if english else '资料与建议'
    skip = 'Skip to content' if english else '跳至正文'
    target = root / 'dist/getting-started' / suffix / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · boluopai</title><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/guide.css"><link rel="icon" href="/mark.svg"></head>
<body><a class="skip" href="#main">{skip}</a><header class="header wrap"></header>
<main id="main" class="wrap practical-guide"><a class="back" href="/repositories/{suffix}">{back}</a><article>{rendered}</article></main>
<footer class="footer wrap"><p class="copyright"></p><a href="#main">{'Back to top' if english else '回到顶部'}</a></footer></body></html>''')
    print(f'Rendered {target.relative_to(root)} from {source.relative_to(root)}')
subprocess.run([sys.executable, str(root / 'scripts/refine-navigation.py')], check=True)
