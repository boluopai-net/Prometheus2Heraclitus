"""Render bilingual general and research guides, with existing legacy aliases.

uv run --with markdown python scripts/render-guide.py --repo /path/to/Prometheus2Heraclitus
Shared site chrome is projected by refine-navigation.py after both editions exist.
"""
import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import markdown
from cjk_markdown import CjkBoldExtension

root = Path(__file__).resolve().parents[1]
SECTION_IDS = (
    'foundation', 'subscription', 'reading', 'information', 'environment',
    'continuity', 'first-loop', 'ways-of-practice', 'automation',
)
LEGACY_TOPICS = {
    'start': 'foundation',
    'reading': 'reading',
    'tools': 'environment',
    'continuity': 'continuity',
    'practice': 'ways-of-practice',
    'automation': 'automation',
}
GUIDES = (
    ('getting-started', 'getting-started', SECTION_IDS, 'axe.svg',
     '从实际任务开始，了解工具、协作、学习与持续维护。',
     'A practical guide to tools, collaboration, learning, and maintenance.'),
    ('research-and-learning', 'research-learning',
     ('domain-methods', 'resources', 'learning'),
     'notebook.svg', '了解实际采用的科研与学习仓库，以及本地老师和云端老师的用途。',
     'Explore the research and learning repositories used in this practice and what Local Teacher and Web Teacher can offer.'),
)


def route(english, slug='getting-started'):
    return '/' + slug + '/' + ('en/' if english else '')


def render(text, section_ids):
    md = markdown.Markdown(extensions=['md_in_html', 'sane_lists', 'tables', CjkBoldExtension()])
    rendered = md.convert(text)
    for anchor in section_ids:
        rendered, count = re.subn(
            rf'(?:<p>)?<a id="{anchor}"></a>(?:</p>)?\s*<h2>',
            f'<h2 id="{anchor}" tabindex="-1">', rendered,
        )
        if count != 1:
            raise ValueError(f'Expected one guide heading for {anchor}, found {count}')
    return rendered.replace('<table>', '<div class="guide-table"><table>').replace('</table>', '</table></div>')


def navigation(headings, english):
    label = 'Guide sections' if english else '本文章节'
    items = ''.join(
        f'<li><a href="#{anchor}"' + (' aria-current="location"' if index == 0 else '')
        + f'>{html.escape(title)}</a></li>'
        for index, (anchor, title) in enumerate(headings)
    )
    return f'<aside class="guide-sidebar"><nav aria-label="{label}"><ul>{items}</ul></nav></aside>'


def legacy_alias(slug, english):
    base = route(english)
    fallback = base + '#' + LEGACY_TOPICS[slug]
    label = 'Continue reading the guide' if english else '继续阅读工具使用'
    script = (
        f'const anchors={json.dumps(SECTION_IDS)};let fragment;'
        'try{fragment=decodeURIComponent(location.hash.slice(1));}catch{fragment="";}'
        f'location.replace({json.dumps(base)}+"#"+'
        f'(anchors.includes(fragment)?fragment:{json.dumps(LEGACY_TOPICS[slug])}));'
    )
    return f'''<!doctype html>
<html lang="{'en' if english else 'zh-CN'}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow, noimageindex">
<title>{label} · boluopai</title><link rel="canonical" href="{base}">
<script>{script}</script></head><body><p><a href="{fallback}">{label}</a></p></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    for guide, english in ((guide, english) for guide in GUIDES for english in (False, True)):
        stem, slug, section_ids, motif, description_zh, description_en = guide
        source = args.repo / 'skills/yinyang/references/docs' / (stem + ('.md' if english else '.zh-CN.md'))
        text = source.read_text().replace('https://boluopai.net/', '/')
        title = text.splitlines()[0].removeprefix('# ')
        headings = re.findall(r'<a id="([^"]+)"></a>\s*## (.+)', text)
        if tuple(anchor for anchor, _ in headings) != section_ids:
            raise ValueError(f'{source}: expected its ordered guide anchors')
        # The flat reading navigation replaces only the source's duplicated tool map.
        text, count = re.subn(
            r'(?ms)^## [^\n]+\n\s*<nav class="guide-navigation".*?</nav>\s*', '', text,
        )
        if count != 1:
            raise ValueError(f'{source}: expected one source tool map')
        rendered = render(text, section_ids).replace('<p>', '<p class="guide-lead">', 1)
        note_start = rendered.rfind('<p>')
        rendered = rendered[:note_start] + rendered[note_start:].replace('<p>', '<p class="guide-note">', 1)
        rendered = f'<img class="motif guide-motif" src="/motifs/{motif}" alt="" aria-hidden="true">' + rendered
        lang, suffix = ('en', 'en/') if english else ('zh-CN', '')
        back = 'Resources &amp; Advice' if english else '资料与建议'
        skip = 'Skip to content' if english else '跳至正文'
        description = description_en if english else description_zh
        page = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · boluopai</title><meta name="description" content="{html.escape(title + ' — ' + description)}"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/guide.css"><link rel="icon" href="/mark.svg"><script defer src="/guide.js"></script></head>
<body><a class="skip" href="#main">{skip}</a><header class="header wrap"></header>
<main id="main" class="wrap practical-guide"><a class="back" href="/repositories/{suffix}">{back}</a><div class="guide-layout">{navigation(headings, english)}<div class="guide-reading"><article>{rendered}</article></div></div></main>
<footer class="footer wrap"><p class="copyright"></p><a href="#main">{'Back to top' if english else '回到顶部'}</a></footer></body></html>'''
        target = root / 'dist' / route(english, slug).lstrip('/') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)
        if stem == 'getting-started':
            for old_slug in LEGACY_TOPICS:
                alias = root / 'dist/getting-started' / old_slug / suffix / 'index.html'
                alias.parent.mkdir(parents=True, exist_ok=True)
                alias.write_text(legacy_alias(old_slug, english))
        print(f'Rendered {target.relative_to(root)} from {source.name}')
    subprocess.run([sys.executable, str(root / 'scripts/refine-navigation.py')], check=True)


if __name__ == '__main__':
    main()
