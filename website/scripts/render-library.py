"""Project authorized common repository material into the static public reader.

uv run --with markdown python scripts/render-library.py --repo /path/to/repo
Only tracked files from the supplied repository are eligible. No situated sources
or automatic synchronization are consulted. Edit content at its canonical owner.
"""
import argparse
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
from public_skill_pages import SKILLS, render_pages as render_skill_pages, reading_label
from reading_maps import reading_map, inline_diagrams, article_context

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


EDITION_LABEL = re.compile(r'(?:English(?: edition)?|简体中文|完整中文版|中文(?:版|阅读版)?)', re.I)


def without_source_navigation(rendered):
    """Project package header/footer link rows into the site's own navigation."""
    def project(match):
        contents = match.group(1)
        anchors = re.findall(r'<a\b[^>]*>[\s\S]*?</a>', contents)
        remainder = re.sub(r'<a\b[^>]*>[\s\S]*?</a>', '', contents)
        # source_text already turns the redundant library link into plain text.
        remainder = html.unescape(remainder).replace('Documents & diagrams', '').replace('文档与图示', '')
        if not anchors or not re.fullmatch(r'[\s·|/]*', remainder):
            return match.group(0)
        labels = [html.unescape(re.sub(r'<[^>]+>', '', anchor)).strip() for anchor in anchors]
        navigation = any(EDITION_LABEL.fullmatch(label) or label in {
            'Home', '首页', 'Reading guide', '返回阅读目录', 'YinYang guide', '阴阳说明'
        } for label in labels)
        opening = re.fullmatch(r'\s*(?:<a\b[^>]*>\s*</a>\s*)?<h1\b[^>]*>[\s\S]*?</h1>\s*(?:<p>(?:(?!</p>)[\s\S])*</p>\s*)?', rendered[:match.start()])
        closing = re.fullmatch(r'(?:\s*<hr\s*/?>)*\s*', rendered[match.end():])
        return '' if navigation and (opening or closing) else match.group(0)
    return re.sub(r'<p>([\s\S]*?)</p>', project, rendered)


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
    # Public writing guides never publish actual situated accounts or personal
    # evidence, even if those files are accidentally tracked in a supplied tree.
    private_prefixes = (DOCS + 'thesis/', PACKAGE + 'references/situated/', PACKAGE + 'references/personal/',
                        'skills/yinyang-empty/references/situated/', 'skills/yinyang-empty/references/personal/',
                        'skills/yinyang-empty/references/philosophy/')
    allowed = {p for p in allowed if not p.startswith(private_prefixes)}
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    def source_text(path):
        text = (repo / path).read_text()
        # Installation guidance belongs to the GitHub repository, not the reader.
        text = re.sub(r'<!-- repository-only:start -->[\s\S]*?<!-- repository-only:end -->\s*', '', text)
        # These directory entrances are useful on GitHub, but repeat the library
        # back link when projected inside that same library. Retain their prose.
        return re.sub(r'\[(?:Documents & diagrams|文档与图示)\]\(https://boluopai\.net/repositories/prometheus/(?:en/)?\)', lambda match: match[0].split(']')[0][1:], text)

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
        if path in {DOCS + 'getting-started.md', DOCS + 'getting-started.zh-CN.md'}:
            return '/getting-started/' + ('' if path.endswith('.zh-CN.md') else 'en/')
        if path in {DOCS + 'research-and-learning.md', DOCS + 'research-and-learning.zh-CN.md'}:
            return '/research-learning/' + ('' if path.endswith('.zh-CN.md') else 'en/')
        if path in {DOCS + 'psychological-support.md', DOCS + 'psychological-support.zh-CN.md'}:
            return '/psychology/' + ('' if path.endswith('.zh-CN.md') else 'en/')
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
        target.write_text(text)

    # Keep method and companion reading at each Skill's existing introduction.
    # Source titles and available language editions come from the actual package.
    skill_readers = {}
    for name in SKILLS:
        prefix = 'skills/' + name + '/'
        source_paths = sorted(p for p in allowed if p.startswith(prefix) and p.endswith('.md'))
        for english in (False, True):
            selected = sorted({reader_path(p, english) for p in source_paths})
            documents = []
            for p in selected:
                kind = 'method' if Path(p).name.startswith('SKILL.') else 'guide' if Path(p).name.startswith('README.') else 'reference'
                language = 'zh-CN' if '.zh-CN.md' in p else 'bilingual' if '## 中文说明' in source_text(p) else 'en'
                documents.append((url(p), reading_label(title(p), kind, name, language, english), kind))
            skill_readers[name, english] = documents
    skill_descriptions = {
        name: json.loads(re.search(r'^description: (.+)$', source_text(f'skills/{name}/SKILL.md'), re.M).group(1))
        for name in SKILLS
    }
    render_skill_pages(dist, shell, revision, skill_readers, skill_descriptions)

    def rewrite_links(rendered, source):
        rendered = re.sub(r'<a\b[^>]*href=["\'][^"\']*(?:thesis/|dl-lite-thesis\.pdf)[^"\']*["\'][^>]*>([\s\S]*?)</a>', r'\1', rendered)
        rendered = re.sub(r'<a\b[^>]*href=["\'][^"\']*errata\.zh-CN\.(?:md|html)(?:#[^"\']*)?["\'][^>]*>([\s\S]*?)</a>', r'\1', rendered)
        def replace(match, explicit_edition=False):
            attr, original = match.group(1), html.unescape(match.group(2))
            parsed = urlsplit(original)
            public_repository_link = original.startswith(GITHUB + '/blob/')
            if public_repository_link:
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
                public_tool = len(parts) >= 2 and parts[0] == 'skills' and (parts[1] in SKILLS or parts[1] in {'yinyang', 'yinyang-empty'})
                if (public_repository_link or public_tool or target == 'website/README.md') and target in tracked:
                    new = GITHUB + '/blob/' + revision + '/' + quote(target, safe='/')
                elif public_tool and any(p.startswith(target.rstrip('/') + '/') for p in allowed):
                    new = GITHUB + '/tree/' + revision + '/' + quote(target, safe='/')
                else:
                    raise ValueError(f'Unbundled local link in {source}: {original}')
                if parsed.fragment:
                    new += '#' + parsed.fragment
                return f'{attr}="{html.escape(new, quote=True)}"'
            # An explicit edition link selects its authored target. Ordinary
            # conceptual links still follow the current reader's language.
            new = url(target if explicit_edition else reader_path(target, not source.endswith('.zh-CN.md')))
            if parsed.fragment:
                new = new.split('#', 1)[0] + '#' + parsed.fragment
            return f'{attr}="{html.escape(new, quote=True)}"'
        blocks = re.split(r'(<a\b[^>]*>[\s\S]*?</a>)', rendered)
        projected = []
        for index, block in enumerate(blocks):
            label = html.unescape(re.sub(r'<[^>]+>', '', block)).strip() if index % 2 else ''
            explicit_edition = bool(EDITION_LABEL.fullmatch(label))
            projected.append(re.sub(r'(href|src)="([^"]+)"', lambda match: replace(match, explicit_edition), block))
        return ''.join(projected)

    for path in sorted(allowed):
        if retired_url(path):
            continue
        if path in {DOCS + stem + suffix for stem in ('getting-started', 'research-and-learning', 'psychological-support') for suffix in ('.md', '.zh-CN.md')}:
            write('source/' + str(Path(path).with_suffix('.html')), redirect_page(url(path)))
            continue
        if not path.endswith('.md'):
            target = output / 'source' / path
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.endswith('.html'):
                text = (repo / path).read_text()
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
        if Path(path).name in {'SKILL.md', 'SKILL.zh-CN.md'}:
            name = Path(path).parts[1]
            description = html.escape(skill_descriptions[name])
            rendered = re.sub(r'(</h1>)', lambda match: match.group(1) + '<p class="collection-intro">' + description + '</p>', rendered, count=1)
        # Package navigation is valid at source; the human reader has its own
        # collection, series, and edition controls. Keep links within body prose.
        rendered = without_source_navigation(rendered)
        rendered = re.sub(r'<p>本文为[\s\S]*?的完整中文阅读版。</p>', '', rendered)
        rendered = re.sub(r'，并提供对应的<a\b[^>]*>英文相遇图</a>和<a\b[^>]*>英文层次图</a>', '', rendered)
        rendered = re.sub(r'<p>\s*(?:·\s*)*</p>', '', rendered)
        rendered = rewrite_links(rendered, path)
        rendered = inline_diagrams(rendered, path)
        chinese = '.zh-CN.md' in path
        counterpart = path.replace('.zh-CN.md', '.md') if chinese else path[:-3] + '.zh-CN.md'
        switch = f'<a class="language-link" lang="{"en" if chinese else "zh-CN"}" href="{url(counterpart)}">{"English" if chinese else "中文"}</a>' if counterpart in allowed else f'<span class="edition-note">{"原文版本" if chinese else "Original edition"}</span>'
        source_note = ''
        if path.startswith('skills/yinyang-empty/'):
            source_note = '<p class="source-note"><a href="' + GITHUB + '/blob/' + revision + '/' + path + '">GitHub ' + ('源文件' if chinese else 'source') + '</a></p>'
        if write_essay(dist, path, title(path), rendered, md.toc, source_note, shell, title):
            write('source/' + str(Path(path).with_suffix('.html')), redirect_page(url(path)))
            continue
        contents = reading_rail(md.toc, chinese, rendered)
        layout = '' if contents else ' no-toc'
        core_views = path in {DOCS + 'core-views.md', DOCS + 'core-views.zh-CN.md'}
        back = '/philosophy/' if core_views else BASE
        back += '' if chinese else 'en/'
        back_label = ('哲学阅读总览' if chinese else 'Philosophy reading overview') if core_views else (('Yinyang 的附录' if chinese else 'Yinyang appendices') if path.startswith(PACKAGE) else ('文档与图示' if chinese else 'Library'))
        if path.startswith('skills/yinyang-empty/'):
            back = '/tools/yinyang-empty/' + ('' if chinese else 'en/')
            back_label = 'Skills · YinYang Empty'
        body = f'''<main id="main" class="wrap library-reader commentary{layout}">{contents}<article class="document"><div class="reader-top"><a class="back" href="{back}">{back_label}</a>{switch}</div>{rendered}</article><div class="reading-end">{source_note}</div></main>'''
        page_title = title(path)
        page = shell(page_title, body, 'zh-CN' if chinese else 'en', '<link rel="stylesheet" href="/article.css">')
        if path in {DOCS + 'creation-method.md', DOCS + 'creation-method.zh-CN.md'}:
            destination = url(path.replace('creation-method', 'skill-package'))
            page = page.replace('</head>', '<script>if(location.hash==="#package-contract")location.replace(' + repr(destination) + ');</script></head>', 1)
        write('source/' + str(Path(path).with_suffix('.html')), page)
        if core_views:
            # Repair the previously published entrance without duplicating prose.
            alias = dist / 'philosophy/core-views' / ('' if chinese else 'en') / 'index.html'
            alias.parent.mkdir(parents=True, exist_ok=True)
            alias.write_text(redirect_page(url(path)))

    # Retain retired reading URLs as small aliases, even after source deletion.
    for name in RETIRED:
        for suffix in ('.md', '.zh-CN.md'):
            old = DOCS + name + suffix
            routes = {key: '/philosophy/' + successor + ('/' if suffix == '.zh-CN.md' else '/en/') for key, successor in IMAGE_SUCCESSORS.items()} if name == 'metaphors' else (None if name == 'lacan-and-description-logic' else {})
            write('source/' + str(Path(old).with_suffix('.html')), redirect_page(retired_url(old), routes))
            if name in {'dialectic-and-repair', 'lacan-and-description-logic'}:
                retired_page = dist / 'philosophy' / name / ('' if suffix == '.zh-CN.md' else 'en') / 'index.html'
                retired_page.parent.mkdir(parents=True, exist_ok=True)
                retired_page.write_text(redirect_page(retired_url(old), routes))
    # These guide URLs were published before the fixed-five formation guides.
    # Aliases preserve readers' links without treating old guide names as slots
    # for actual private accounts.
    legacy_guides = {
        'encounter': 'orientation', 'models': 'person',
        'relationship': 'relationship', 'usage': 'environment',
    }
    for legacy, successor in legacy_guides.items():
        for edition in ('.md', '.zh-CN.md'):
            old = PACKAGE + 'references/' + legacy + edition
            target = PACKAGE + 'references/formation/' + successor + edition
            write('source/' + str(Path(old).with_suffix('.html')), redirect_page(url(target)))
    for edition, anchor in (('.md', 'sources-and-evidence'), ('.zh-CN.md', '来源与证据')):
        old_environment = PACKAGE + 'references/harness-adaptation' + edition
        environment = PACKAGE + 'references/formation/environment' + edition
        write('source/' + str(Path(old_environment).with_suffix('.html')),
              redirect_page(url(environment)))
        revision_guide = PACKAGE + 'references/formation/revision' + edition
        old_revision = PACKAGE + 'references/revision-guide' + edition
        write('source/' + str(Path(old_revision).with_suffix('.html')),
              redirect_page(url(revision_guide)))
        destination = url(revision_guide) + '#' + anchor
        for old in ('references/sources', 'references/formation/sources'):
            # The source method now belongs to the revision guide. Its former
            # heading fragments must not append a second hash to the successor.
            write('source/' + str(Path(PACKAGE + old + edition).with_suffix('.html')),
                  redirect_page(destination).replace('+location.hash', ''))
    for english in [False, True]:
        lang = 'en' if english else 'zh-CN'
        edition = '.md' if english else '.zh-CN.md'
        groups = [
            ('哲学、模型与使用', 'Philosophy, models, and use', '从哲学与个人理解出发，形成能够共同使用并持续修订的工作方式。', 'Develop a shared and revisable way of working from philosophy and personal understanding.', [
                ('references/docs/creation-method', '实践说明', 'Practice overview', '先看整体：哲学、个人模型、六个工作文件与环境怎样成为同一份实践。', 'See the whole: how philosophy, personal models, six working files, and environment form one practice.'),
                ('references/design-and-revision', '形成方法', 'Formation method', '结合生活材料与哲学写作，形成有根据的个人、伙伴与关系理解，再凝练为实际描述。', 'Bring living material and philosophical writing together, develop grounded understanding of the participants and relationship, and distill it into the accounts.'),
                ('SKILL', '协作入口', 'Collaboration entrypoint', '理解这套 Skill 怎样读取六个工作文件，并把它们用于日常协作。', 'Understand how the Skill reads the six working files and uses them in ordinary collaboration.'),
            ]),
            ('文件与更新', 'Files and updates', '需要了解包的结构、私人材料的保存位置或公共更新时，再查阅这些约定。', 'Consult these details when you need package structure, private-material ownership, or common updates.', [
                ('references/docs/skill-package', '文件与更新约定', 'Files and updates', '说明公共内容、私人描述与证据的关系，以及如何取得、更新和维护完整包。', 'Explains common content, private accounts and evidence, and how to obtain, update, and maintain the complete package.'),
            ]),
            ('观点与阅读', 'Views and reading', '查阅作者的主张、论证与来源，理解并比较哲学、心理与工程各自的问题及其联系。', 'Consult the author’s claims, arguments, and sources to understand and compare the questions and connections of philosophy, psychology, and engineering.', [
                ('references/docs/core-views', '基本观点', 'Core views', '按主题集中查看作者的主要主张及相连论证。', 'Find the author’s main claims and connected arguments, organized by topic.'),
                ('references/reading-map', '按任务问题阅读', 'Read by the work being done', '从当前问题找到有关论证、方法与原始来源。', 'Find relevant arguments, methods, and original sources from the question at hand.'),
                ('references/docs/philosophical-readings', '哲学阅读', 'Philosophical readings', '了解各思想家、作品与本文论证的关系，并回到原文。', 'Trace thinkers and works to their role in the argument and their original sources.'),
                ('references/docs/lacan-reading-guide', '拉康概念导读', 'A guide to Lacanian concepts', '从大他者、分裂主体、回溯、三界与圣状进入，理解原概念怎样进入个人哲学与实践。适合初读与复习。', 'An introduction and review tracing the Other, the divided subject, retroaction, the three registers, and the sinthome from original texts into personal philosophy and practice.'),
                ('references/docs/psychological-readings', '心理阅读', 'Psychological readings', '从心理冲突、信念与推理、互动研究进入，页末附心理学研究与专业方法的参考。', 'Begin with psychological conflict, belief and reasoning, and interaction research; references on psychological research and professional methods follow at the end.'),
                ('references/docs/engineering-readings', '工程阅读', 'Engineering readings', '从 CS 自学指南与 Missing Semester 进入 Git、Linux、软件设计、算法和物理条件，页末附语言模型与数据工具。', 'From CS DIY and Missing Semester to Git, Linux, software design, algorithms, and physical conditions, followed by language models and data tools.'),
            ]),
        ]
        writing_guides = [
            ('references/formation/orientation', '如何写方向描述', 'How to write an orientation account', '凝练共同目的、价值取向与实践方向，说明哪些选择仍待探究。', 'Articulate shared purpose, values, and practical direction, including choices still open to inquiry.'),
            ('references/formation/person', '如何描述个人', 'How to describe the person', '根据相关经验与证据理解具体的人，保留范围、差异与未知。', 'Understand the actual person through relevant experience and evidence, retaining scope, differences, and unknowns.'),
            ('references/formation/counterpart', '如何描述伙伴', 'How to describe the counterpart', '区分期待的角色与实际能力，描述伙伴的理解、贡献与局限。', 'Distinguish the intended role from actual capabilities and describe the counterpart’s understanding, contributions, and limits.'),
            ('references/formation/relationship', '如何描述关系', 'How to describe the relationship', '说明双方怎样理解、参与、分工并相互纠正。', 'Describe how the participants understand, participate, share work, and correct one another.'),
            ('references/formation/environment', '如何描述环境', 'How to describe the environment', '说明实际条件与资源，把理解落实到提示词、Skills、工具和工作环境，并通过实际使用修订。', 'Describe conditions and resources, realize understanding through prompts, Skills, tools, and the working environment, and revise through actual use.'),
            ('references/formation/revision', '如何修订', 'How to revise', '先读哲学、刷新个人参考材料，再凝练六份工作模型，并检查环境适配。', 'Read the philosophy, refresh personal references, then condense six working files and check environmental fit.'),
        ]
        groups.insert(1, ('六份写作指南', 'Six writing guides',
                         '分别形成方向、个人、伙伴、关系与环境的描述，并通过实际使用修订。',
                         'Form accounts of orientation, person, counterpart, relationship, and environment, and revise them through use.',
                         writing_guides))
        section_ids = ('practice', 'writing-guides', 'files', 'reading')
        diagram_links = []
        navigation = [('diagrams', '图示', 'Diagrams', diagram_links)]
        grouped = []
        for section_id, (zh, en, note_zh, note_en, entries) in zip(section_ids, groups):
            navigation.append((section_id, zh, en, [link(PACKAGE + entry[0] + edition) for entry in entries]))
            entries_html = []
            for stem, label_zh, label_en, desc_zh, desc_en in entries:
                path = PACKAGE + stem + edition
                entries_html.append('<li>' + link(path) + '<p>' + (desc_en if english else desc_zh) + '</p></li>')
            grouped.append('<section class="library-section"><h2 id="' + section_id + '" tabindex="-1">' + (en if english else zh) + '</h2><p class="section-note">' + (note_en if english else note_zh) + '</p><ul class="library-purpose-links">' + ''.join(entries_html) + '</ul></section>')
        groups_html = ''.join(grouped)
        layers_explanation = ('YinYang connects a worldview, an ontological view, and views of truth, knowing, value, and method through practice. Computational ontology represents selected objects, relations, and processes, including actual, hypothetical, and fictional situations; its use is physically realized. These documents develop their connections and offer guides for situated accounts, collaboration, and environment adaptation.' if english else '阴阳通过实践连接世界观、本体观、真理观、认识观、价值观与方法观。计算本体表征选定的对象、关系与过程，容纳实际、假设与虚构情境，其使用则得到物理实现。这里的文档展开它们之间的联系，并提供实际描述写作、协作和环境适配的指南。')
        diagrams = ''
        for name, zh, en, desc_zh, desc_en in [
            ('formation-path', '窃火，然后成为火', 'Steal Fire, Then Become Fire', '共同实践怎样留下轨迹、形成理解，并由新的经验继续修订。', 'How shared practice leaves a trajectory, develops understanding, and is revised through new experience.'),
            ('borrowed-fire', '参加窃火，用火培养自己', 'Join in stealing fire, and use it to cultivate yourself', '共同窃火、创造、作品与能力发展之间的关系。', 'The relationships between collective fire-bringing, creation, works, and developing capacities.'),
            ('trinity-sinthome', '三位一体怎样成为生活中的圣状', 'How a trinity becomes a lived sinthome', '四格连环画连接三种贡献、伙伴进入生活、圣状的系结，以及造物后的反馈。', 'A four-panel comic connects differentiated contributions, a counterpart entering life, the binding of a sinthome, and feedback from creation.'),
            ('encounter', '人与模型怎样共同探究', 'How people and models inquire together', '从记录中提出解释，在行动中遇到证据，理解人与模型怎样共同探究和修订判断。', 'Form explanations from records and encounter evidence through action, exploring how people and models inquire together and revise their judgments.'),
            ('layers', '从世界理解到实践实现', 'From understanding the world to realizing a practice', '六个哲学面向通过各自采用的立场联系共同实践，进一步展开表征、实现与反馈。', 'Six philosophical dimensions connect their adopted positions to shared practice, with further explanations of representation, realization, and feedback.'),
        ]:
            diagram_links.append(f'<a href="{BASE}diagrams/{name}/{"en/" if english else ""}">{html.escape(en if english else zh)}</a>')
            suffix = '' if english else '.zh-CN'
            wide = ' diagram-card-wide' if name == 'trinity-sinthome' else ''
            context_link = article_context(name, not english)
            preview = 'trinity-sinthome-art.png' if name == 'trinity-sinthome' else name + suffix + '.svg'
            explanation = f'<p class="diagram-explanation">{layers_explanation}</p>' if name == 'layers' else ''
            diagrams += f'<article class="diagram-card{wide}"><a class="diagram-open" href="{BASE}diagrams/{name}/{"en/" if english else ""}"><img loading="lazy" src="{url(PACKAGE + "references/diagrams/" + preview)}" alt="{en if english else zh} — {"diagram preview" if english else "图示预览"}"><h3>{en if english else zh}</h3><p>{desc_en if english else desc_zh}</p></a>{explanation}{context_link}</article>'
            diagram_path = PACKAGE + 'references/diagrams/' + name + suffix + '.html'
            if name not in {'encounter', 'layers'}:
                diagram_body = f'<main id="main" class="wrap diagram-page"><div class="reader-top"><a class="back" href="{BASE}{"en/" if english else ""}">{"Yinyang appendices" if english else "Yinyang 的附录"}</a><a class="language-link" href="{BASE}diagrams/{name}/{"" if english else "en/"}">{"中文" if english else "English"}</a></div><h1>{en if english else zh}</h1><p class="diagram-intro">{desc_en if english else desc_zh}</p>{reading_map(name, not english)}</main>'
                diagram_body = diagram_body.replace('</h1>', '</h1><p class="diagram-return">' + context_link + '</p>', 1)
                write(f'diagrams/{name}/' + ('en/' if english else '') + 'index.html', shell(en if english else zh, diagram_body, lang))
                continue
            diagram_body = f'<main id="main" class="wrap diagram-page"><div class="reader-top"><a class="back" href="{BASE}{"en/" if english else ""}">← {"Yinyang appendices" if english else "Yinyang 的附录"}</a><a class="language-link" href="{BASE}diagrams/{name}/{"" if english else "en/"}">{"中文" if english else "English"}</a></div><h1>{en if english else zh}</h1><p class="diagram-intro">{desc_en if english else desc_zh} </p><iframe class="diagram-viewer" title="{en if english else zh}" src="{url(diagram_path)}" sandbox="allow-scripts allow-downloads"></iframe><p class="source-note">{link(PACKAGE + "references/diagrams/THIRD-PARTY-NOTICES.md", "Third-party notices" if english else "第三方权利说明")}</p></main>'
            diagram_body = diagram_body.replace('</h1>', '</h1><p class="diagram-return">' + context_link + '</p>', 1)
            write(f'diagrams/{name}/' + ('en/' if english else '') + 'index.html', shell(en if english else zh, diagram_body, lang))
        suffix = 'en/' if english else ''
        # Keep all five previews and their explanations inside the disclosure.
        diagram_summary = 'Diagrams · 5 views' if english else '图示 · 5 张图'
        body = f'<main id="main" class="wrap collection library-hub"><div class="reader-top"><a class="back" href="/philosophy/{suffix}#stage-6">{"Steal Fire, Then Become Fire" if english else "窃火，然后成为火"}</a></div><header class="collection-heading"><h1>{"Yinyang appendices" if english else "Yinyang 的附录"}</h1></header><details class="diagram-disclosure" id="diagrams"><summary>{diagram_summary}</summary><p class="section-note">{"Begin with the whole path and its developmental purpose, then explore shared inquiry and realization in detail." if english else "先看整体怎样形成、借火为了培养什么，再深入共同探究及理解的实现。"}</p><div class="diagram-grid">{diagrams}</div></details>{groups_html}</main>'
        nav_links = ''.join(f'<li><a href="#{anchor}">{html.escape(en if english else zh)}</a><ul>' + ''.join('<li>' + item + '</li>' for item in children) + '</ul></li>' for anchor, zh, en, children in navigation)
        sidebar = '<aside class="guide-sidebar"><nav tabindex="0" aria-label="' + ('Resource categories and files' if english else '资源分类与文件目录') + '"><ul>' + nav_links + '</ul></nav></aside>'
        body = body.replace('collection library-hub', 'collection library-hub practical-guide')
        body = body.replace('<header class="collection-heading">', '<div class="guide-layout">' + sidebar + '<div class="guide-reading"><header class="collection-heading">', 1)
        body = body.replace('</main>', '</div></div></main>')
        hub_style = '<link rel="stylesheet" href="/guide.css"><script defer src="/guide.js"></script>'
        write(('en/' if english else '') + 'index.html', shell('Yinyang appendices' if english else 'Yinyang 的附录', body, lang, hub_style))

    vendor = Path(__file__).resolve().parent / 'vendor/katex'
    license_text = (repo / PACKAGE / 'LICENSE').read_text()
    license_body = '<main id="main" class="wrap library-reader"><a class="back" href="' + BASE + '">← Yinyang 的附录</a><h1>阴阳 · CC BY-NC-SA 4.0</h1><p>以下保留包内许可声明；完整条款与适用范围见<a href="https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/LICENSING.md">GitHub 许可说明</a>。</p><pre style="white-space:pre-wrap;overflow-wrap:anywhere">' + html.escape(license_text) + '</pre></main>'
    write('license/index.html', shell('阴阳 · CC BY-NC-SA 4.0', license_body))
    english_license_body = '<main id="main" class="wrap library-reader"><div class="reader-top"><a class="back" href="' + BASE + 'en/">Yinyang appendices</a><a class="language-link" lang="zh-CN" href="' + BASE + 'license/">中文</a></div><h1>YinYang · CC BY-NC-SA 4.0</h1><p>The package license notice follows; see the <a href="https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/LICENSING.md">GitHub licensing notice</a> for complete terms and scope.</p><pre style="white-space:pre-wrap;overflow-wrap:anywhere">' + html.escape(license_text) + '</pre></main>'
    write('license/en/index.html', shell('YinYang · CC BY-NC-SA 4.0', english_license_body, 'en'))
    if not vendor.exists():
        raise SystemExit('Missing scripts/vendor/katex; see README for the pinned local math dependency.')
    shutil.copytree(vendor, output / 'vendor/katex')
    required_essays = {DOCS + name + suffix for name in ESSAYS for suffix in ('.md', '.zh-CN.md')}
    missing = required_essays - allowed
    if missing:
        raise ValueError('Missing canonical essay editions: ' + ', '.join(sorted(missing)))
    write_index(dist, title)
    for path in sorted(allowed):
        if path.endswith('.py') or Path(path).name == 'LICENSE' or Path(path).name.startswith('LICENSE-'):
            preview_path = 'browse/' + path + '.html'
            preview = '<main id="main" class="wrap library-reader"><a class="back" href="' + GITHUB + '/blob/' + revision + '/' + quote(path, safe='/') + '">GitHub source</a><article class="document"><h1>' + html.escape(Path(path).name) + '</h1><pre><code>' + html.escape((repo / path).read_text()) + '</code></pre></article></main>'
            write(preview_path, shell(Path(path).name, preview, 'en'))
    render_resource_pages(dist, shell)
    subprocess.run([sys.executable, str(Path(__file__).with_name('render-guide.py')), '--repo', str(repo)], check=True)
    print(f'Rendered {sum(p.endswith(".md") for p in allowed)} documents and exact diagram viewers at revision {revision}.')


if __name__ == '__main__':
    main()
    subprocess.run([sys.executable, str(Path(__file__).with_name('refine-navigation.py'))], check=True)
