"""Keep shared navigation quiet and the public edition discoverable.

Run after either article renderer. Static section pages are maintained in dist.
"""
import re
import hashlib
import html
from pathlib import Path
from urllib.parse import quote
from reader_names import reader_names
from search_index import update_search_index

root = Path(__file__).resolve().parents[1] / 'dist'
style_versions = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()[:12]
                  for name in ('style.css', 'site.css', 'guide.css', 'article.css', 'library.css')}


def page_url(page):
    path = page.relative_to(root).as_posix()
    return '/' + quote(path[:-10] if path.endswith('index.html') else path, safe='/')


def join_chinese_soft_wraps(text):
    """Do not render editorial line wraps inside Chinese prose as word spaces."""
    protected = r'(<(?P<verbatim>pre|code|script|style|textarea)\b[^>]*>[\s\S]*?</(?P=verbatim)\s*>|<!--[\s\S]*?-->|<[^>]+>)'
    chunks = []
    start = 0
    soft_wrap = re.compile(r'(?<=[\u3400-\u9fff，。；：！？、…）》」』】])\r?\n[ \t]*(?=[\u3400-\u9fff（《「『【])')
    for match in re.finditer(protected, text, re.I):
        chunks.append(soft_wrap.sub('', text[start:match.start()]))
        chunks.append(match[0])
        start = match.end()
    chunks.append(soft_wrap.sub('', text[start:]))
    return ''.join(chunks)


def space_chinese_latin(text):
    """Give prose a consistent space across CJK/Latin boundaries, including inline tags."""
    protected = r'(<(?P<verbatim>pre|code|script|style|textarea)\b[^>]*>[\s\S]*?</(?P=verbatim)\s*>|<!--[\s\S]*?-->|<[^>]+>)'
    cjk = r'[\u3400-\u9fff]'
    chinese = r'[\u3400-\u9fff，。；：！？、…（）《》「」『』【】]'
    latin = r'[A-Za-z0-9]'
    boundary = re.compile(f'(?:{cjk}{latin}|{latin}{cjk})')
    inline = {'a', 'abbr', 'b', 'bdi', 'bdo', 'cite', 'del', 'em', 'i', 'ins', 'label', 'mark', 'q', 's', 'small', 'span', 'strong', 'sub', 'sup', 'time', 'u'}
    chunks, start, previous, previous_slot, gap_slots = [], 0, '', None, []

    def prose(value):
        nonlocal previous, previous_slot, gap_slots
        value = re.sub(f'({chinese})[ \t\r\n]+(?={chinese})', r'\1', value)
        value = re.sub(f'({cjk})({latin})', r'\1 \2', value)
        value = re.sub(f'({latin})({cjk})', r'\1 \2', value)
        visible = value.strip()
        if visible and previous:
            mixed = bool(boundary.fullmatch(previous + visible[0]))
            chinese_pair = bool(re.fullmatch(chinese + chinese, previous + visible[0]))
            if mixed or chinese_pair:
                chunks[previous_slot] = chunks[previous_slot].rstrip()
                for slot in gap_slots:
                    chunks[slot] = ''
                value = (' ' if mixed else '') + value.lstrip()
        if visible:
            previous, previous_slot, gap_slots = value.rstrip()[-1], len(chunks), []
        elif value:
            gap_slots.append(len(chunks))
        return value

    for match in re.finditer(protected, text, re.I):
        chunks.append(prose(text[start:match.start()]))
        token = match[0]
        chunks.append(token)
        tag = re.match(r'</?([a-zA-Z0-9]+)\b', token)
        if not token.startswith('<!--') and (match.group('verbatim') or not tag or tag[1].lower() not in inline):
            previous, previous_slot, gap_slots = '', None, []
        start = match.end()
    chunks.append(prose(text[start:]))
    return ''.join(chunks)


def counterpart(page, english):
    """Link to an actual edition, including file-based library source routes."""
    relative = page.relative_to(root)
    if relative.name == 'index.html':
        candidate = page.parent.parent / 'index.html' if english and page.parent.name == 'en' else page.parent / 'en/index.html'
    elif relative.as_posix().startswith('repositories/prometheus/source/'):
        candidate = page.with_name(page.name.replace('.zh-CN.html', '.html')) if not english else page.with_name(page.stem + '.zh-CN.html')
    else:
        return None
    if not candidate.is_file() or candidate == page:
        return None
    edition = candidate.read_text()
    expected = 'zh-CN' if english else 'en'
    if not re.search(r'<html\b[^>]*lang=["\']' + expected + r'["\']', edition):
        return None
    return page_url(candidate)


def header(page, text):
    english = bool(re.search(r'<html\b[^>]*lang=["\']en["\']', text))
    other = counterpart(page, english)
    language = '中文' if english else 'EN'
    if other:
        switch = f'<a class="language-control" href="{other}" lang="{"zh-CN" if english else "en"}" aria-label="{"Read this page in Chinese" if english else "阅读本页英文版"}">{language}</a>'
    else:
        unavailable = 'Chinese edition unavailable' if english else '本页暂无英文版'
        switch = f'<span class="language-control unavailable" aria-disabled="true" title="{unavailable}" aria-label="{unavailable}">{language}<span class="unavailable-note"> · {"unavailable" if english else "暂无"}</span></span>'
    section = page.relative_to(root).parts[0]
    nav = []
    home = '/en/' if english and (root / 'en/index.html').is_file() else '/'
    home_current = ' aria-current="page"' if page.relative_to(root).as_posix() in {'index.html', 'en/index.html'} else ''
    nav.append(f'<a href="{home}"{home_current}>{"Fire and River" if english else "火与河流"}</a>')
    for slug, zh, en in [('philosophy', '哲学', 'Philosophy'), ('repositories', '资料与建议', 'Resources & Advice'), ('singing', '唱歌', 'Singing')]:
        destination = f'/{slug}/'
        if english and (root / slug / 'en/index.html').is_file():
            destination += 'en/'
        current = ' aria-current="page"' if section == slug or (section in {'getting-started', 'research-learning', 'psychology', 'skills', 'tools'} and slug == 'repositories') else ''
        nav.append(f'<a href="{destination}"{current}>{en if english else zh}</a>')
    return f'<header class="header wrap"><div class="header-top"><a class="wordmark" href="{home}" aria-label="{"boluopai home" if english else "boluopai 首页"}"><img class="brand-lion" src="/art/boluopai-lion.jpg" width="48" height="48" alt="">boluopai.</a><div class="header-controls">{switch}<button class="theme-control" type="button" aria-pressed="false" aria-label="{"Dark mode" if english else "深色模式"}" data-theme-control><span aria-hidden="true">◐</span><span data-theme-label>{"Dark" if english else "深色"}</span></button></div></div><nav class="section-tabs" aria-label="{"Sections" if english else "栏目"}">{"".join(nav)}</nav></header>'


def refresh_page_titles(text):
    """Full-title entrances follow their destination; prose labels stay authored."""
    def replace(match):
        href = re.search(r'\bhref="(/[^"]*)"', match[1])
        if href is None:
            raise ValueError('A data-page-title entrance needs a local page URL')
        target = root / href[1].lstrip('/') / 'index.html'
        heading = re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>', target.read_text())
        if heading is None:
            raise ValueError(f'Missing destination heading: {href[1]}')
        title = html.unescape(re.sub(r'<[^>]+>', '', heading[1]))
        return match[1] + html.escape(reader_names(title)) + '</a>'
    return re.sub(r'(<a\b(?=[^>]*\sdata-page-title(?:\s|>))[^>]*>)[\s\S]*?</a>', replace, text)


for page in root.rglob('*.html'):
    if page.relative_to(root).parts[0] in {'client', 'server', '.openai'}:
        continue
    # The website uses the owner's chosen Latin label, including reader editions
    # projected from the separately maintained philosophical source package.
    text = refresh_page_titles(reader_names(page.read_text()))
    text = re.sub(r'<p class="eyebrow">(?:实践指南|Practical guide|等待第一首歌|Waiting for the first song)</p>', '', text)
    # Full semantic diagram viewers have their own interface and retain arrows.
    if 'class="header wrap"' not in text:
        page.write_text(space_chinese_latin(text))
        continue
    if re.search(r'<html\b[^>]*lang=["\']zh-CN["\']', text):
        text = join_chinese_soft_wraps(text)
    fragments = re.split(r'(<article class="document">[\s\S]*?</article>|<div class="article-body">[\s\S]*?</div>\s*(?=<nav class="series-navigation"))', text)
    def quiet(fragment):
        return re.sub(r'(<a\b[^>]*>)([\s\S]*?)(</a>)',
                      lambda m: m[1] + re.sub(r'\s*[←→↗↑]\s*', ' ', m[2]).strip() + m[3], fragment)
    updated = ''.join(fragment if i % 2 else quiet(fragment) for i, fragment in enumerate(fragments))
    # Link captions carry the subject; edition and source-path metadata belong
    # to the language control and file browser, not repeated in reading prose.
    def clean_caption(match):
        label = match[2].replace('（英文形成指引）', '')
        if '/repositories/prometheus/' in match[1]:
            label = re.sub(r'（(?:references/)?[^（）]*\.md）', '', label)
        return match[1] + label + match[3]
    updated = re.sub(r'(<a\b[^>]*>)([\s\S]*?)(</a>)', clean_caption, updated)
    updated = updated.replace('GitHub 仓库</a>', 'GitHub</a>')
    # Navigation links use one textual affordance; actual commands keep buttons.
    updated = updated.replace('class="outline-button"', 'class="text-link"')
    if page.relative_to(root).as_posix() in {'index.html', 'en/index.html', 'repositories/index.html', 'repositories/en/index.html'}:
        # Section labels may change; repository access remains GitHub access.
        updated = re.sub(r'(?<=>)GitHub 仓库(?=<)', '资料与建议', updated)
        updated = re.sub(r'(?<=>)GitHub repositories(?=<)', 'Resources &amp; Advice', updated)
        updated = updated.replace('<title>GitHub 仓库 ·', '<title>资料与建议 ·').replace('<title>GitHub repositories ·', '<title>Resources &amp; Advice ·')
    # Page chrome used to carry an extra edition link above the reading body.
    # Keep a single language control in the masthead, without touching prose.
    updated = re.sub(r'<a\b[^>]*class="language-link"[^>]*>[\s\S]*?</a>', '', updated)
    # Static entrances and Markdown sources also carry plain edition anchors.
    # Remove only navigation labels on local links; preserve external originals.
    updated = re.sub(r'<a\b(?=[^>]*href="/)[^>]*>(?:English(?: edition)?|中文(?:版)?)</a>\s*(?:·\s*)?', '', updated)
    updated = re.sub(r'<p>\s*(?:·\s*)*</p>', '', updated)
    updated = re.sub(r'<p class="language-link">\s*</p>', '', updated)
    updated = re.sub(r'<header class="header wrap">[\s\S]*?</header>', lambda _: header(page, updated), updated, count=1)
    if 'src="/site.js"' not in updated:
        updated = updated.replace('</head>', '<link rel="stylesheet" href="/site.css"><script src="/site.js"></script></head>', 1)
    updated = re.sub(r'href="/((?:style|site|guide|article|library)\.css)(?:\?v=[^" ]*)?"',
                     lambda m: f'href="/{m[1]}?v={style_versions[m[1]]}"', updated)
    english_page = bool(re.search(r'<html\b[^>]*lang=["\']en["\']', updated))
    rights_url = '/rights/en/' if english_page else '/rights/'
    rights_label = 'Copyright &amp; licensing' if english_page else '版权与许可'
    copyright_footer = f'<p class="copyright">© 2026 boluopai · <a href="{rights_url}">{rights_label}</a></p>'
    updated = re.sub(r'<p class="copyright">[\s\S]*?</p>', copyright_footer, updated)
    if re.search(r'<html\b[^>]*lang=["\']en["\']', updated):
        def english_footer(match):
            footer = match[0].replace('回到顶部', 'Back to top').replace('返回首页', 'Home')
            if (root / 'en/index.html').is_file():
                footer = footer.replace('href="/"', 'href="/en/"')
            return footer
        updated = re.sub(r'<footer\b[\s\S]*?</footer>', english_footer, updated)
    if page.relative_to(root).as_posix() not in {'index.html', 'en/index.html'}:
        updated = re.sub(r'<aside class="playground wrap">[\s\S]*?</aside>', '', updated)
    page.write_text(space_chinese_latin(reader_names(updated)))

update_search_index(root)
