"""Render the bilingual practical guide from its maintained Markdown sources.

uv run --with markdown python scripts/render-guide.py
Shared site chrome is projected by refine-navigation.py after both editions exist.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

import markdown
from cjk_markdown import CjkBoldExtension

root = Path(__file__).resolve().parents[1]
# The anchors are the stable editorial boundaries in the two canonical sources.
topics = [
    ('start', '开始使用', 'Getting started', ('foundation', 'subscription')),
    ('reading', '阅读与信息', 'Reading and information', ('reading', 'information')),
    ('tools', '工具与界面', 'Tools and interfaces', ('environment',)),
    ('continuity', '协作与接续', 'Collaboration and continuity', ('continuity', 'first-loop')),
    ('practice', '学习工作与生活', 'Learning, working, and living', ('ways-of-practice',)),
    ('automation', '自动化与维护', 'Automation and maintenance', ('automation',)),
]


def route(slug, english):
    return '/getting-started/' + (slug + '/' if slug else '') + ('en/' if english else '')


def render(text, english):
    md = markdown.Markdown(extensions=['md_in_html', 'sane_lists', 'tables', CjkBoldExtension()])
    rendered = md.convert(text)
    for slug, _, _, anchors in topics:
        for anchor in anchors:
            rendered = rendered.replace(f'href="#{anchor}"', f'href="{route(slug, english)}#{anchor}"')
    return rendered.replace('<table>', '<div class="guide-table"><table>').replace('</table>', '</table></div>')


def navigation(current, english):
    label = 'Guide topics' if english else '指南主题'
    links = [(None, 'Overview' if english else '总览')] + [(t[0], t[2] if english else t[1]) for t in topics]
    items = ''.join(f'<li><a href="{route(slug, english)}"' + (' aria-current="page"' if slug == current else '') + f'>{html.escape(title)}</a></li>' for slug, title in links)
    nav = f'<nav aria-label="{label}"><ul>{items}</ul></nav>'
    return f'<aside class="guide-sidebar">{nav}</aside><div class="guide-mobile-menu">{nav}</div>'


for english in (False, True):
    source = root / 'content/guides' / ('getting-started.en.md' if english else 'getting-started.md')
    text = source.read_text()
    title = text.splitlines()[0].removeprefix('# ')
    anchors = [anchor for topic in topics for anchor in topic[3]]
    parts = re.split(r'<a id="(' + '|'.join(anchors) + r')"></a>', text)
    if parts[1::2] != anchors:
        raise ValueError(f'{source}: expected the nine ordered guide anchors')
    sections = dict(zip(parts[1::2], parts[2::2]))
    # The closing invitation and service note belong to the overview, once.
    closing = re.split(r'(?m)(?=^## (?:继续走|Continue)\s*$)', sections['automation'])
    if len(closing) != 2:
        raise ValueError(f'{source}: missing closing invitation')
    sections['automation'], ending = closing
    section_titles = {anchor: re.search(r'(?m)^## \d+\. (.+)$', value)[1] for anchor, value in sections.items()}
    intro = re.sub(r'(?ms)^## [^\n]+\n\s*<nav class="guide-navigation".*?</nav>\s*', '', parts[0])
    entries = []
    for index, (slug, zh, en, group) in enumerate(topics, 1):
        links = ' · '.join(f'<a id="{anchor}" href="{route(slug, english)}#{anchor}">{html.escape(section_titles[anchor])}</a>' for anchor in group)
        entries.append(f'<li><span class="guide-topic-number">{index:02}</span><div><h3><a href="{route(slug, english)}">{html.escape(en if english else zh)}</a></h3><p>{links}</p></div></li>')
    overview = render(intro, english)
    overview = overview.replace('<p>', '<p class="guide-lead">', 1)
    ending_html = render(ending, english)
    # Only the actual source service note receives the quiet footer treatment.
    note_start = ending_html.rfind('<p>')
    ending_html = ending_html[:note_start] + ending_html[note_start:].replace('<p>', '<p class="guide-note">', 1)
    overview += f'<section class="guide-topic-index"><h2>{"Explore the guide" if english else "按主题阅读"}</h2><ol>{"".join(entries)}</ol></section>' + ending_html
    pages = [(None, title, overview)]
    for slug, zh, en, group in topics:
        body = '\n\n'.join(f'<a id="{anchor}"></a>\n' + re.sub(r'(?m)^(##) \d+\. ', r'\1 ', sections[anchor]) for anchor in group)
        pages.append((slug, en if english else zh, f'<h1>{html.escape(en if english else zh)}</h1>' + render(body, english)))
    lang, suffix = ('en', 'en/') if english else ('zh-CN', '')
    back = 'Resources &amp; Advice' if english else '资料与建议'
    skip = 'Skip to content' if english else '跳至正文'
    for slug, page_title, rendered in pages:
        rendered = '<img class="motif guide-motif" src="/motifs/axe.svg" alt="" aria-hidden="true">' + rendered
        pagination = ''
        if slug:
            index = [topic[0] for topic in topics].index(slug)
            neighbors = []
            if index:
                previous = topics[index - 1]
                neighbors.append(f'<a rel="prev" href="{route(previous[0], english)}"><span>{"Previous" if english else "上一篇"}</span>{html.escape(previous[2] if english else previous[1])}</a>')
            neighbors.append(f'<a href="{route(None, english)}">{"Guide overview" if english else "指南总览"}</a>')
            if index + 1 < len(topics):
                following = topics[index + 1]
                neighbors.append(f'<a rel="next" href="{route(following[0], english)}"><span>{"Next" if english else "下一篇"}</span>{html.escape(following[2] if english else following[1])}</a>')
            pagination = f'<nav class="guide-pagination" aria-label="{"Continue reading" if english else "继续阅读"}">{"".join(neighbors)}</nav>'
        target = root / 'dist' / route(slug, english).lstrip('/') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        description = ('A practical guide to tools, collaboration, learning, and maintenance.' if english else '从实际任务开始，按主题了解工具、协作、学习与持续维护。')
        target.write_text(f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page_title)} · {html.escape(title) + ' · ' if slug else ''}boluopai</title><meta name="description" content="{html.escape(page_title + ' — ' + description)}"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/guide.css"><link rel="icon" href="/mark.svg"></head>
<body><a class="skip" href="#main">{skip}</a><header class="header wrap"></header>
<main id="main" class="wrap practical-guide"><a class="back" href="/repositories/{suffix}">{back}</a><div class="guide-layout">{navigation(slug, english)}<div class="guide-reading"><article>{rendered}</article>{pagination}</div></div></main>
<footer class="footer wrap"><p class="copyright"></p><a href="#main">{'Back to top' if english else '回到顶部'}</a></footer></body></html>''')
        print(f'Rendered {target.relative_to(root)} from {source.relative_to(root)}')
subprocess.run([sys.executable, str(root / 'scripts/refine-navigation.py')], check=True)
