"""Project authorized common repository material into the static public reader.

uv run --with markdown python scripts/render-library.py --repo /path/to/repo
Only tracked files from the supplied repository are eligible. No situated sources
or automatic synchronization are consulted. Edit content at its canonical owner.
"""
import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import markdown
from cjk_markdown import CjkBoldExtension
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from commentaries import ESSAYS, RETIRED, IMAGE_SUCCESSORS, essay_url, retired_url, redirect_page, write_essay, write_index, reading_rail
from repository_panel import with_comments
from resource_pages import render as render_resource_pages
from public_skill_pages import SKILLS, render_pages as render_skill_pages

BASE = '/repositories/prometheus/'
GITHUB = 'https://github.com/boluopai-net/Prometheus2Heraclitus'
PACKAGE = 'skills/yinyang/'
DOCS = PACKAGE + 'references/docs/'
METHOD_PACKAGES = {name: (info[0], name) for name, info in SKILLS.items() if name != 'random-wheel'}



class MathPreprocessor(Preprocessor):
    def run(self, lines):
        # Preserve code verbatim; stash TeX before Markdown interprets underscores.
        text = '\n'.join(lines)
        pattern = r'(```[^\n]*\n[\s\S]*?\n```|~~~[^\n]*\n[\s\S]*?\n~~~|`[^`\n]+`)|(\$\$[\s\S]+?\$\$|(?<![\\$])\$(?!\$)[^\n$]+?(?<!\\)\$)'
        def replace(match):
            if match.group(1):
                return match.group(1)
            token = match.group(2)
            display = token.startswith('$$')
            tex = token[2:-2] if display else token[1:-1]
            tag = 'div' if display else 'span'
            element = f'<{tag} class="math-source" data-display="{str(display).lower()}" data-tex="{html.escape(tex, quote=True)}">{html.escape(token)}</{tag}>'
            stored = self.md.htmlStash.store(element)
            return '\n\n' + stored + '\n\n' if display else stored
        return re.sub(pattern, replace, text).splitlines()


class MathExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(MathPreprocessor(md), 'preserved_math', 29)


def slug(value, separator):
    return re.sub(r'\s', separator, re.sub(r'[^\w\- ]', '', value.lower())).strip(separator)


def without_source_toc(source):
    """The website supplies its own responsive rail; retain content disclosures."""
    def project(match):
        disclosure = match.group(0)
        toc = re.fullmatch(
            r'<details\b[^>]*>\s*<summary>\s*(?:本篇导航|On this page)\s*</summary>'
            r'(?P<links>[\s\S]*?)</details>', disclosure, re.I)
        if toc:
            lines = [line.strip() for line in toc['links'].splitlines() if line.strip()]
            if lines and all(re.fullmatch(r'[-*+]\s+\[[^\]\n]+\]\(#[^\s)]+\)', line) for line in lines):
                return ''
        return disclosure
    # A quoted source example must stay verbatim even when it shows a TOC.
    blocks = re.split(r'(^ {0,3}(?:`{3,}|~{3,})[^\n]*\n[\s\S]*?^ {0,3}(?:`{3,}|~{3,})[ \t]*$)', source, flags=re.M)
    return ''.join(block if index % 2 else re.sub(
        r'<details\b[^>]*>[\s\S]*?</details>', project, block, flags=re.I)
        for index, block in enumerate(blocks))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--revision', help='Published source commit; defaults to source HEAD')
    args = parser.parse_args()
    repo = args.repo.resolve()
    tracked = subprocess.check_output(['git', '-C', str(repo), 'ls-files', '-z']).decode().split('\0')
    revision = args.revision or subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip()
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        parser.error('--revision must be a full Git commit SHA')
    dist = Path(__file__).resolve().parents[1] / 'dist'
    output = dist / 'repositories/prometheus'
    allowed = {p for p in tracked if p and (
        (p.startswith(PACKAGE) and (Path(p).suffix in {'.md', '.html', '.svg', '.jpg', '.png'} or Path(p).name == 'LICENSE'))
        or (len(Path(p).parts) >= 3 and Path(p).parts[0] == 'skills' and Path(p).parts[1] in METHOD_PACKAGES and (Path(p).suffix == '.md' or Path(p).name == 'LICENSE'))
        or p in {'README.md', 'README.zh-CN.md', 'CONTRIBUTING.md', 'CONTRIBUTING.zh-CN.md', 'MODEL.md', 'AGENTS.md', 'LICENSING.md', 'LICENSE', 'LICENSE-MIT', 'skills/random-wheel/SKILL.md', 'skills/random-wheel/LICENSE', 'skills/random-wheel/scripts/render_wheel.py', 'skills/random-wheel/assets/wheel.html', 'skills/random-wheel/assets/standalone.html'}
    )}
    # Private academic material is excluded even when an older source contains it.
    allowed = {p for p in allowed if not p.startswith(DOCS + 'thesis/')}
    # Website reader translations do not change executable package contracts.
    # Check the exact public source before replacing any generated pages.
    overlay_data = json.loads(Path(__file__).with_name('reader-translations.zh-CN.json').read_text())
    overlays = {}
    for original, entry in overlay_data['translations'].items():
        if original not in allowed or hashlib.sha256((repo / original).read_bytes()).hexdigest() != entry['source_sha256']:
            raise ValueError(f'Reader translation needs source review: {original}')
        translated = original[:-3] + '.zh-CN.md'
        if translated not in allowed:
            overlays[translated] = entry['markdown']
    allowed.update(overlays)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    def source_text(path):
        text = overlays[path] if path in overlays else (repo / path).read_text()
        # Installation guidance belongs to the GitHub repository, not the reader.
        return re.sub(r'<!-- repository-only:start -->[\s\S]*?<!-- repository-only:end -->\s*', '', text)

    def reader_path(path, english):
        suffix = Path(path).suffix
        if suffix not in {'.md', '.html', '.svg'}:
            return path
        stem = path.replace('.zh-CN' + suffix, suffix)
        preferred = stem if english else stem[:-len(suffix)] + '.zh-CN' + suffix
        return preferred if preferred in allowed else path
    (dist / 'downloads/dl-lite-thesis.pdf').unlink(missing_ok=True)
    # Only this repository's shared formation guide is included, never a private
    # situated package. Candidate/validation JSON and execution metadata are excluded.
    def url(path):
        commentary = essay_url(path) or retired_url(path)
        if commentary:
            return commentary
        target = str(Path(path).with_suffix('.html')) if path.endswith('.md') else path
        return BASE + 'source/' + quote(target, safe='/')

    def title(path):
        text = source_text(path)
        found = re.search(r'^#\s+(.+)$', text, re.M)
        result = found.group(1) if found else Path(path).stem
        return result

    def link(path, label=None):
        return f'<a href="{url(path)}">{html.escape(label or title(path))}</a>'

    def shell(page_title, body, lang='zh-CN', extra=''):
        return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(page_title)} · boluopai</title><link rel="icon" href="/mark.svg"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/library.css"><link rel="stylesheet" href="{BASE}vendor/katex/katex.min.css"><script defer src="{BASE}vendor/katex/katex.min.js"></script><script defer src="/library.js"></script>{extra}</head><body><a class="skip" href="#main">{"跳至正文" if lang == "zh-CN" else "Skip to content"}</a><header class="header wrap"><a class="wordmark" href="/">boluopai.</a><nav aria-label="主导航"><a href="/philosophy/">哲学评论</a><a href="/singing/">唱歌</a><a href="/repositories/" aria-current="page">GitHub 仓库</a></nav></header>{body}<footer class="footer wrap"><a class="wordmark" href="/">boluopai.</a><p class="copyright">© 2026 BOBBY · <a href="/rights/">版权与许可</a></p><a href="#main">回到顶部 ↑</a></footer></body></html>'''

    def write(relative, text):
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if str(relative).endswith('.html'):
            text = text.replace('<head>', '<head><meta name="robots" content="noindex, nofollow, noimageindex">', 1)
        target.write_text(text)

    render_skill_pages(dist, shell, revision)

    def rewrite_links(rendered, source):
        rendered = re.sub(r'<a\b[^>]*href=["\'][^"\']*(?:thesis/|dl-lite-thesis\.pdf)[^"\']*["\'][^>]*>([\s\S]*?)</a>', r'\1', rendered)
        rendered = re.sub(r'<a\b[^>]*href=["\'][^"\']*errata\.zh-CN\.(?:md|html)(?:#[^"\']*)?["\'][^>]*>([\s\S]*?)</a>', r'\1', rendered)
        def replace(match):
            attr, original = match.group(1), html.unescape(match.group(2))
            parsed = urlsplit(original)
            if original.startswith(GITHUB + '/blob/'):
                tail = original[len(GITHUB + '/blob/'):].split('/', 1)
                target = tail[1].split('#')[0] if len(tail) == 2 else ''
            elif parsed.scheme or original.startswith(('#', '//', '/')):
                return match.group(0)
            else:
                target = str((repo / source).parent.joinpath(unquote(parsed.path)).resolve().relative_to(repo))
            retired = retired_url(target, unquote(parsed.fragment))
            if retired:
                return f'{attr}="{html.escape(retired, quote=True)}"'
            if target not in allowed:
                parts = Path(target).parts
                public_tool = len(parts) >= 2 and parts[0] == 'skills' and parts[1] in SKILLS
                if (public_tool or target == 'website/README.md') and target in tracked:
                    new = GITHUB + '/blob/' + revision + '/' + quote(target, safe='/')
                elif public_tool and any(p.startswith(target.rstrip('/') + '/') for p in allowed):
                    new = GITHUB + '/tree/' + revision + '/' + quote(target, safe='/')
                else:
                    raise ValueError(f'Unbundled local link in {source}: {original}')
                if parsed.fragment:
                    new += '#' + parsed.fragment
                return f'{attr}="{html.escape(new, quote=True)}"'
            new = url(reader_path(target, not source.endswith('.zh-CN.md')))
            if parsed.fragment:
                new += '#' + parsed.fragment
            return f'{attr}="{html.escape(new, quote=True)}"'
        return re.sub(r'(href|src)="([^"]+)"', replace, rendered)

    for path in sorted(allowed):
        if retired_url(path):
            continue
        if not path.endswith('.md'):
            target = output / 'source' / path
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.endswith('.html'):
                text = (repo / path).read_text()
                text = re.sub(r'(<head[^>]*>)', r'\1<meta name="robots" content="noindex, nofollow, noimageindex">', text, count=1, flags=re.I)
                target.write_text(text)
            else:
                shutil.copyfile(repo / path, target)
            continue
        source = source_text(path)
        if source.startswith('---\n'):
            source = source.split('---\n', 2)[2]
        source = without_source_toc(source)
        extensions = ['tables', 'fenced_code', 'footnotes', 'toc', 'sane_lists', MathExtension()]
        if essay_url(path):
            # Preserve useful Markdown content inside essay disclosures without
            # changing the maintained source; website navigation is supplied above.
            source = re.sub(r'<details\s*>', '<details markdown="1">', source)
            extensions.append('md_in_html')
        md = markdown.Markdown(extensions=[*extensions, CjkBoldExtension()], extension_configs={'toc': {'slugify': slug, 'toc_depth': '2-3'}})
        rendered = md.convert(source)
        # Edition navigation belongs exclusively to the site masthead. These
        # labels are source navigation, not quotations or bibliography.
        rendered = re.sub(r'<a\b[^>]*>(?:English(?: edition)?|中文(?:版)?)</a>\s*(?:·\s*)?', '', rendered)
        rendered = re.sub(r'<p>本文为[\s\S]*?的完整中文阅读版。</p>', '', rendered)
        rendered = re.sub(r'，并提供对应的<a\b[^>]*>英文相遇图</a>和<a\b[^>]*>英文层次图</a>', '', rendered)
        rendered = re.sub(r'<p>\s*(?:·\s*)*</p>', '', rendered)
        rendered = rewrite_links(rendered, path)
        chinese = '.zh-CN.md' in path
        counterpart = path.replace('.zh-CN.md', '.md') if chinese else path[:-3] + '.zh-CN.md'
        switch = f'<a class="language-link" lang="{"en" if chinese else "zh-CN"}" href="{url(counterpart)}">{"English" if chinese else "中文"}</a>' if counterpart in allowed else f'<span class="edition-note">{"原文版本" if chinese else "Original edition"}</span>'
        source_note = '<p class="reader-provenance">本站中文阅读版</p>' if path in overlays else ''
        if write_essay(dist, path, title(path), rendered, md.toc, source_note, shell, title):
            write('source/' + str(Path(path).with_suffix('.html')), redirect_page(url(path)))
            continue
        body = f'''<main id="main" class="wrap library-reader commentary">{reading_rail(md.toc, chinese)}<article class="document"><div class="reader-top"><a class="back" href="{BASE}{'' if chinese else 'en/'}">{"文档与图示" if chinese else "Library"}</a>{switch}</div>{rendered}</article><div class="reading-end">{source_note}</div></main>'''
        write('source/' + str(Path(path).with_suffix('.html')), shell(title(path), body, 'zh-CN' if chinese else 'en', '<link rel="stylesheet" href="/article.css">'))

    # Retain retired reading URLs as small aliases, even after source deletion.
    for name in RETIRED:
        for suffix in ('.md', '.zh-CN.md'):
            old = DOCS + name + suffix
            routes = {key: '/philosophy/' + successor + ('/' if suffix == '.zh-CN.md' else '/en/') for key, successor in IMAGE_SUCCESSORS.items()} if name == 'metaphors' else {}
            write('source/' + str(Path(old).with_suffix('.html')), redirect_page(retired_url(old), routes))
            if name == 'dialectic-and-repair':
                retired_page = dist / 'philosophy' / name / ('' if suffix == '.zh-CN.md' else 'en') / 'index.html'
                retired_page.parent.mkdir(parents=True, exist_ok=True)
                retired_page.write_text(redirect_page(retired_url(old), routes))
    for english in [False, True]:
        lang = 'en' if english else 'zh-CN'
        edition = '.md' if english else '.zh-CN.md'
        groups = [
            ('观点与三类阅读', 'Views and three reading paths', '哲学展开世界观，心理研究感受与认识，工程连接方法与实现。按问题进入原文，让三方面在实际工作中相互修订；工具入口另行提供可用的 Skills。', 'Philosophy develops worldview, psychology investigates feeling and knowing, and engineering connects method with realization. Enter original sources by question and let these contributions revise one another through work; tool entrances separately provide usable Skills.', [
                ('docs/core-views', '基本观点', 'Core views', '按主题集中查看阴阳的主要主张。', 'Find the main claims together, organized by topic.'),
                ('docs/philosophical-readings', '哲学阅读', 'Philosophical readings', '了解各思想家、作品与本文论证的关系，并回到原文。', 'Trace thinkers and works to their role in the argument and their original sources.'),
                ('docs/psychological-readings', '心理阅读', 'Psychological readings', '心理过程建模与经验检验、心灵与心理理论，以及信念、推理和互动研究的书与论文。', 'Books and papers on psychological process modeling and evidence, mind and psychological theories, belief, reasoning, and interaction.'),
                ('docs/engineering-readings', '工程阅读', 'Engineering readings', '从 CS 自学指南与 Missing Semester 进入 Git、Linux、软件设计、算法、实验实现与物理条件。', 'From CS DIY and Missing Semester to Git, Linux, software design, algorithms, experimental implementation, and physical conditions.'),
            ]),
            ('形成实践', 'Develop a practice', '从自己的问题出发，把理解发展为可使用、可修订的安排。', 'Begin with your own questions and give understanding a usable, revisable form.', [
                ('docs/creation-method', '创制与实现', 'Creation and realization', '理解个人哲学、伙伴关系与实际环境怎样共同形成。', 'See how personal philosophy, the counterpart relation, and an actual environment develop together.'),
                ('docs/skill-package', '共享 Skill 与个人哲学', 'Shared Skills and personal philosophy', '区分可复用的共同材料与自己的个人内容，了解怎样采用和维护。', 'Distinguish reusable shared material from personal content, and understand adoption and maintenance.'),
            ]),
        ]
        grouped = []
        for zh, en, note_zh, note_en, entries in groups:
            entries_html = []
            for stem, label_zh, label_en, desc_zh, desc_en in entries:
                path = PACKAGE + 'references/' + stem + edition
                entries_html.append('<li>' + link(path, label_en if english else label_zh) + '<p>' + (desc_en if english else desc_zh) + '</p></li>')
            grouped.append('<section class="library-section"><h2>' + (en if english else zh) + '</h2><p class="section-note">' + (note_en if english else note_zh) + '</p><ul class="library-purpose-links">' + ''.join(entries_html) + '</ul></section>')
        groups_html = ''.join(grouped)
        diagrams = ''
        for name, zh, en, desc_zh, desc_en in [('encounter', '相遇', 'Encounter', '生成、判断与证据怎样在持续的相遇中形成关系。', 'Generation, judgment and evidence within an ongoing encounter.'), ('layers', '层次', 'Layers', '物理基础、计算抽象，以及认识、价值、方法与实践的联系。', 'Physical grounding, computational abstraction, and their connections with knowing, value, methods, and practice.')]:
            suffix = '' if english else '.zh-CN'
            diagrams += f'<a class="diagram-card" href="{BASE}diagrams/{name}/{"en/" if english else ""}"><img loading="lazy" src="{url(PACKAGE + "references/diagrams/" + name + suffix + ".svg")}" alt="{en if english else zh} — {"concept map preview" if english else "概念图预览"}"><h3>{en if english else zh}</h3><p>{desc_en if english else desc_zh}</p><span class="text-link">{"Explore diagram →" if english else "进入交互图示 →"}</span></a>'
            diagram_path = PACKAGE + 'references/diagrams/' + name + suffix + '.html'
            diagram_body = f'<main id="main" class="wrap diagram-page"><div class="reader-top"><a class="back" href="{BASE}{"en/" if english else ""}">← {"Library" if english else "文档与图示"}</a><a class="language-link" href="{BASE}diagrams/{name}/{"" if english else "en/"}">{"中文" if english else "English"}</a></div><h1>{en if english else zh}</h1><p class="diagram-intro">{desc_en if english else desc_zh} {"Use the viewer’s zoom, guided views and details. Open the full viewer for more space." if english else "可缩放、切换导览并查看关系说明；打开完整图示获得更大阅读空间。"}</p><div class="diagram-actions"><a class="outline-button" href="{url(diagram_path)}">{"Open full viewer ↗" if english else "打开完整图示 ↗"}</a><a class="text-link" href="{url(diagram_path.replace(".html", ".svg"))}">SVG</a>{link(DOCS + "core-views" + edition, "Related claims" if english else "回到核心观点")}</div><iframe class="diagram-viewer" title="{en if english else zh}" src="{url(diagram_path)}" sandbox="allow-scripts allow-downloads"></iframe><p class="source-note">{link(PACKAGE + "references/diagrams/THIRD-PARTY-NOTICES.md", "Third-party notices" if english else "第三方权利说明")}</p></main>'
            write(f'diagrams/{name}/' + ('en/' if english else '') + 'index.html', shell(en if english else zh, diagram_body, lang))
        intro = ('Use this page to consult ideas and sources, develop a practice, or explore relationships through diagrams. The philosophy section already supplies the sequential reading route.' if english else '这里按用途查阅观点与来源、形成自己的实践，或通过图示理解关系。哲学栏目已有完整的顺序阅读，这里提供随问题进入的参考。')
        suffix = 'en/' if english else ''
        body = f'<main id="main" class="wrap collection library-hub"><div class="reader-top"><a class="back" href="/repositories/{suffix}">{"Resources & advice" if english else "资料与建议"}</a></div><header class="collection-heading"><h1>{"Documents & diagrams" if english else "文档与图示"}</h1><p class="collection-intro">{intro}</p></header>{groups_html}<section class="library-section"><h2>{"Explore the relations" if english else "看见关系"}</h2><p class="section-note">{"Two complementary views: the encounter shows reciprocal activity; the layers distinguish the questions different kinds of work address." if english else "两张图从不同角度理解同一实践：相遇图看相互作用，层次图看不同工作各自回答什么问题。"}</p><div class="diagram-grid">{diagrams}</div></section></main>'
        write(('en/' if english else '') + 'index.html', shell('Documents & diagrams' if english else '文档与图示', body, lang))

    vendor = Path(__file__).resolve().parent / 'vendor/katex'
    license_text = (repo / PACKAGE / 'LICENSE').read_text()
    license_body = '<main id="main" class="wrap library-reader"><a class="back" href="' + BASE + '">← 文档与图示</a><h1>阴阳 · CC BY-NC-SA 4.0</h1><p>以下保留包内许可声明；完整条款与适用范围见<a href="https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/LICENSING.md">GitHub 许可说明</a>。</p><pre style="white-space:pre-wrap;overflow-wrap:anywhere">' + html.escape(license_text) + '</pre></main>'
    write('license/index.html', shell('阴阳 · CC BY-NC-SA 4.0', license_body))
    english_license_body = '<main id="main" class="wrap library-reader"><div class="reader-top"><a class="back" href="' + BASE + 'en/">Documents &amp; diagrams</a><a class="language-link" lang="zh-CN" href="' + BASE + 'license/">中文</a></div><h1>YinYang · CC BY-NC-SA 4.0</h1><p>The package license notice follows; see the <a href="https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/LICENSING.md">GitHub licensing notice</a> for complete terms and scope.</p><pre style="white-space:pre-wrap;overflow-wrap:anywhere">' + html.escape(license_text) + '</pre></main>'
    write('license/en/index.html', shell('YinYang · CC BY-NC-SA 4.0', english_license_body, 'en'))
    if not vendor.exists():
        raise SystemExit('Missing scripts/vendor/katex; see README for the pinned local math dependency.')
    shutil.copytree(vendor, output / 'vendor/katex')
    required_essays = {DOCS + name + suffix for name in ESSAYS for suffix in ('.md', '.zh-CN.md')}
    missing = required_essays - allowed
    if missing:
        raise ValueError('Missing canonical essay editions: ' + ', '.join(sorted(missing)))
    write_index(dist, title)
    browser_urls = {}
    for path in sorted(allowed):
        if path.endswith('.py') or Path(path).name == 'LICENSE' or Path(path).name.startswith('LICENSE-'):
            preview_path = 'browse/' + path + '.html'
            browser_urls[path] = BASE + quote(preview_path, safe='/')
            preview = '<main id="main" class="wrap library-reader"><a class="back" href="/repositories/files/en/#files-title">Browse files</a><article class="document"><h1>' + html.escape(Path(path).name) + '</h1><pre><code>' + html.escape((repo / path).read_text()) + '</code></pre></article></main>'
            write(preview_path, shell(Path(path).name, preview, 'en'))
        else:
            browser_urls[path] = url(path)
    (output / 'files.json').write_text(json.dumps({
        'revision': revision,
        'files': [{'path': path, 'url': browser_urls[path], 'urls': {lang: browser_urls[reader_path(path, english)] for lang, english in [('en', True), ('zh-CN', False)]}} for path in sorted(allowed)],
    }, ensure_ascii=False))
    render_resource_pages(dist, shell)
    print(f'Rendered {sum(p.endswith(".md") for p in allowed)} documents and exact diagram viewers at revision {revision}.')


if __name__ == '__main__':
    main()
    subprocess.run([sys.executable, str(Path(__file__).with_name('refine-navigation.py'))], check=True)
