"""Build bilingual reading books from exact public source, preserving section links.

Requires Pandoc, Typst and macOS sips. Intermediate files stay outside the repo.
The Site owns this reading projection; canonical philosophical prose stays in
the public YinYang package. Run --help for the source and output contract.
"""
import argparse
import copy
from datetime import datetime
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit
from zoneinfo import ZoneInfo

from commentaries import GROUPS, BRANCHES
from article_art import SCENES, CAPTIONS
from pdf_diagrams import DiagramRenderer

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'skills/yinyang/'
GITHUB = 'https://github.com/boluopai-net/Prometheus2Heraclitus'
SITE = 'https://boluopai.net'
READER = 'markdown-smart+pipe_tables+tex_math_dollars+autolink_bare_uris'
APPENDICES = [
    ('references/design-and-revision',),
    tuple('references/formation/' + name for name in
          ('orientation', 'person', 'counterpart', 'relationship', 'environment', 'revision')),
    tuple('references/docs/' + name for name in
          ('philosophical-readings', 'psychological-readings', 'engineering-readings', 'lacan-reading-guide')),
    ('references/docs/skill-package',),
]
DIAGRAMS = {
    'core-views': [('layers', '六个哲学面向与共同实践', 'Six philosophical dimensions and shared practice')],
    'stealing-fire': [('borrowed-fire', '窃火与培养', 'Fire and cultivation')],
    'yinyang-and-taiji': [('encounter', '共同探究', 'Shared inquiry')],
    'local-source-and-website': [('trinity-sinthome', '三位一体与圣状', 'Trinity and sinthome')],
}


def run(command, **kwargs):
    return subprocess.check_output(command, **kwargs)


def raw_typst(text):
    return {'t': 'RawBlock', 'c': ['typst', text]}


def plain(node):
    if isinstance(node, list):
        return ''.join(plain(item) for item in node)
    if not isinstance(node, dict):
        return ''
    kind, content = node.get('t'), node.get('c')
    if kind in ('Str', 'Code', 'Math'):
        return content if isinstance(content, str) else content[-1]
    if kind in ('Space', 'SoftBreak', 'LineBreak'):
        return ' '
    if kind in ('Link', 'Image', 'Span'):
        return plain(content[1])
    return plain(content)


def slug(text):
    # Same heading rule as the HTML reader. Incoming source fragments are stable.
    return re.sub(r'\s', '-', re.sub(r'[^\w\- ]', '', text.lower())).strip('-')


def walk(node, fn):
    if isinstance(node, dict):
        node = fn(node)
        for key, value in list(node.items()):
            if isinstance(value, (dict, list)):
                node[key] = walk(value, fn)
    elif isinstance(node, list):
        node = [walk(item, fn) for item in node]
    return node


def book_paths(english):
    edition = '.md' if english else '.zh-CN.md'
    sections = [('开始阅读' if not english else 'Begin reading', ['references/docs/core-views'])]
    for zh, en, essays in GROUPS:
        members = []
        for name, _ in essays:
            members.append('references/docs/' + name)
            for parent, branches, _ in BRANCHES:
                if parent == name:
                    members.extend('references/docs/' + branch for branch in branches)
        sections.append((en if english else zh, members))
    appendix_titles = [('附录一 · 哲学与模型', 'Appendix I · Philosophy and models'),
                       ('附录二 · 六份写作指南', 'Appendix II · Six writing guides'),
                       ('附录三 · 参考阅读', 'Appendix III · Further reading'),
                       ('附录四 · 阴阳 Skill 的形式', 'Appendix IV · The YinYang Skill')]
    sections.extend((titles[english], list(paths)) for titles, paths in zip(appendix_titles, APPENDICES))
    return [(title, [PACKAGE + name + edition for name in members]) for title, members in sections]


def read_source(repo, revision, path):
    if not path.startswith(PACKAGE) or '/personal/' in path or '/situated/' in path:
        raise ValueError('Only the public package may be read: ' + path)
    return run(['git', '-C', str(repo), 'show', revision + ':' + path])


def prepare_markdown(text):
    text = re.sub(r'^---\n[\s\S]*?\n---\n', '', text)
    text = re.sub(r'<!-- repository-only:start -->[\s\S]*?<!-- repository-only:end -->', '', text)
    text = re.sub(r'<details>\s*<summary>(?:本篇导航|On this page)</summary>[\s\S]*?</details>', '', text)
    text = re.sub(r'<a\s+id="([^"]+)"\s*></a>', r'[]{#\1}', text)
    text = re.sub(r'<summary>(.*?)</summary>', r'\n\n**\1**\n\n', text, flags=re.S)
    text = re.sub(r'</?details[^>]*>', '', text)
    text = re.sub(r'<!--[\s\S]*?-->', '', text)
    # Standalone package navigation repeats the book's contents and bookmarks.
    rows = []
    for row in text.splitlines():
        if re.match(r'^\[(?:Home|首页|English edition|English|中文|简体中文|Documents & diagrams|文档与图示)\]', row):
            remainder = re.sub(r'\[[^\]]*\]\([^)]*\)', '', row)
            if re.fullmatch(r'[\s·|/]*', remainder):
                continue
        rows.append(row)
    return '\n'.join(rows)


def intro(english, revision, stamp):
    if english:
        return f'''# Reading this edition

This book brings together YinYang's public philosophical essays and writing
guides. Begin with relevant Core views, examine their reasons and conditions,
then follow the linked sections when you want to go deeper. You need not accept
every view or read every chapter in order.

The five parts follow the website's connected argument. The appendices contain
the guide to philosophy and models, six public writing guides, further reading,
and the Skill's package guide. Writing a personal philosophy or other essays is
optional and follows your interests. The practical [tool guide]({SITE}/getting-started/en/)
and [research and learning guide]({SITE}/research-learning/en/) remain available online.

Selected ideas can support organizing experiences, revising personal
psychological material, and configuring a fitting environment. YinYang must not
be used for psychological self-help, self-diagnosis, mental-health assessment,
or treatment. See the [full use statement]({GITHUB}/blob/{revision}/README.md#intended-use-and-mental-health).

The contents, PDF bookmarks and in-text references link to chapters and specific
sections. Clickable links are teal. Uncollected sources open online. Interactive
diagrams are represented by static figures with links to their online versions;
private situated files and personal material are not included.

The original prose is preserved; navigation, pagination and figures are adapted
for this reading edition. Generated {stamp} (Asia/Shanghai), from public source
[{revision[:12]}]({GITHUB}/tree/{revision}/skills/yinyang).
'''
    return f'''# 怎样读这本书

本书汇集阴阳的公开哲学论述与写作指南。可以先从核心观点中挑选与自己问题有关的部分，
看看理由与适用条件，再沿链接进入相应论证。不必接受全部立场，也不必从头通读。

五部分正文沿用网站的论述顺序。附录集中收录哲学与模型的连接、六份公开写作指南、
参考阅读及 Skill 的形式说明。是否写自己的哲学或其他文章，取决于兴趣。
[工具使用]({SITE}/getting-started/)和[研究与学习建议]({SITE}/research-learning/)保留在线阅读入口。

选定的思想可以用于整理经历、持续修订个人心理材料，以及配置适合自己的环境。
阴阳不能用于心理自助、自行诊断、心理健康评估或治疗。完整的用途与评价边界见
[仓库说明]({GITHUB}/blob/{revision}/README.zh-CN.md#用途与心理健康说明)。

目录、PDF 书签与正文中的引用，可以跳转到相应文章和具体章节。青色文字是可点击链接；
未收录的资料连向在线来源。交互图以静态图呈现，并保留在线版本入口。
本书不包含私人实际文件与个人材料。

本版保留原文，为连续阅读调整了导航、分页和图示呈现。生成日期：{stamp}（北京时间）。
公开内容版本：[{revision[:12]}]({GITHUB}/tree/{revision}/skills/yinyang)。
'''


def parse(text):
    return json.loads(run(['pandoc', '--from=' + READER, '--to=json'], input=text.encode()))


def build(repo, revision, english, output, work, sample, diagrams):
    lang = 'en' if english else 'zh-CN'
    stamp = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d')
    sections = book_paths(english)
    paths = [path for _, members in sections for path in members]
    if sample:
        paths = paths[:3]  # Core views and two essays; the full build is authoritative.
        sections = [(title, [p for p in members if p in paths]) for title, members in sections]
    assert len(paths) == len(set(paths))
    documents, anchors, ids = {}, {}, {}
    serial = 0
    for path in paths:
        doc = parse(prepare_markdown(read_source(repo, revision, path).decode()))
        ids[path] = f'doc-{len(documents) + 1}'
        anchors[(path, '')] = ids[path]
        used = {}

        def identify(node):
            nonlocal serial
            if node.get('t') == 'Header':
                level, attr, content = node['c']
                fragment = slug(plain(content))
                count = used.get(fragment, 0)
                used[fragment] = count + 1
                if count:
                    fragment += '_' + str(count)
                serial += 1
                label = ids[path] if level == 1 else f'section-{serial}'
                anchors[(path, fragment)] = label
                anchors.setdefault((path, attr[0]), label)
                attr[0] = label
                node['c'][0] += 1  # Parts own level 1; chapters own level 2.
            elif node.get('t') in ('Span', 'Div') and node['c'][0][0]:
                serial += 1
                fragment = node['c'][0][0]
                node['c'][0][0] = f'anchor-{serial}'
                anchors[(path, fragment)] = node['c'][0][0]
            return node
        documents[path] = walk(doc, identify)

    media = work / 'media'
    media.mkdir(exist_ok=True)
    copied = {}

    def asset(path, source=False):
        key = str(path)
        if key in copied:
            return copied[key]
        target = media / (hashlib.sha256(key.encode()).hexdigest()[:12] + Path(path).suffix)
        target.write_bytes(read_source(repo, revision, str(path)) if source else Path(path).read_bytes())
        if target.suffix == '.svg' and 'var(--' in target.read_text():
            target = diagrams.render(target)
        if target.suffix == '.png':
            jpg = target.with_suffix('.jpg')
            # Diagrams retain their 2x text resolution; artwork needs less space.
            size = '2100' if source else '1200'
            quality = '88' if source else '76'
            subprocess.run(['sips', '-Z', size, '-s', 'format', 'jpeg', '-s', 'formatOptions', quality, str(target), '--out', str(jpg)], check=True, stdout=subprocess.DEVNULL)
            target = jpg
        copied[key] = target
        return target

    internal, external, missing = 0, 0, []

    def resolve_link(href, source):
        nonlocal internal, external
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc:
            external += 1
            return href
        path = PurePosixPath(source).parent / unquote(parsed.path) if parsed.path else PurePosixPath(source)
        parts = []
        for piece in path.parts:
            if piece == '..':
                parts.pop()
            elif piece != '.':
                parts.append(piece)
        target = '/'.join(parts)
        fragment = unquote(parsed.fragment)
        if target in documents:
            label = anchors.get((target, fragment))
            if not label:
                missing.append((source, href))
                return href
            internal += 1
            return '#' + label
        external += 1
        return GITHUB + '/blob/' + revision + '/' + quote(target, safe='/') + ('#' + quote(fragment) if fragment else '')

    def transform(node, source):
        if node.get('t') == 'Span' and node['c'][0][0] and not node['c'][1]:
            # Separate location-bearing elements keep consecutive source aliases.
            return {'t': 'RawInline', 'c': ['typst', '#metadata(none) <' + node['c'][0][0] + '>']}
        if node.get('t') == 'Link':
            node['c'][2][0] = resolve_link(node['c'][2][0], source)
        elif node.get('t') == 'Image':
            target = str(PurePosixPath(source).parent / node['c'][2][0])
            # resolve lexical parent segments without reading another tree.
            target = str((repo / target).resolve().relative_to(repo))
            node['c'][2][0] = str(asset(target, True))
            node['c'][0][2].append(['width', '32%'])
        elif node.get('t') in ('RawInline', 'RawBlock') and node['c'][0] == 'html':
            if node['c'][1].strip() in ('<br>', '<br/>', '<br />'):
                return {'t': 'LineBreak'}
            if node['c'][1].strip():
                raise ValueError('Unconverted HTML in ' + source + ': ' + node['c'][1][:120])
        return node

    book = parse(intro(english, revision, stamp))
    for block in book['blocks']:
        if block.get('t') == 'Header':
            block['c'][1][0] = 'reading-introduction'
    overview = asset(PACKAGE + 'references/diagrams/formation-path' + ('.svg' if english else '.zh-CN.svg'), True)
    book['blocks'].append(raw_typst('#diagram-page(' + ', '.join(json.dumps(s, ensure_ascii=False) for s in (
        str(overview), 'The whole argument' if english else '全书关系', SITE + '/repositories/prometheus/diagrams/formation-path/' + ('en/' if english else ''))) + ')'))
    for section_title, members in sections:
        if not members:
            continue
        book['blocks'].append(raw_typst('#part(' + json.dumps(section_title, ensure_ascii=False) + ')'))
        for path in members:
            doc = walk(copy.deepcopy(documents[path]), lambda node: transform(node, path))
            name = Path(path).name.split('.')[0]
            blocks = doc['blocks']
            art = ROOT / 'dist/art' / (name + ('.svg' if name == 'writing-a-sinthome' else '.png'))
            if name in SCENES and art.is_file():
                image_path = asset(art)
                caption = CAPTIONS.get(name, SCENES[name])[english]
                blocks.insert(1, raw_typst('#chapter-art(' + json.dumps(str(image_path)) + ', ' + json.dumps(caption, ensure_ascii=False) + ')'))
            book['blocks'].extend(blocks)
            for diagram, zh, en in DIAGRAMS.get(name, []):
                source = PACKAGE + 'references/diagrams/' + diagram + ('.svg' if english else '.zh-CN.svg')
                image_path = asset(source, True)
                online = SITE + '/repositories/prometheus/diagrams/' + diagram + ('/en/' if english else '/')
                wide = diagram in {'layers', 'encounter'}
                book['blocks'].append(raw_typst('#diagram-page(' + ', '.join(json.dumps(s, ensure_ascii=False) for s in (str(image_path), en if english else zh, online)) + ', wide: ' + str(wide).lower() + ')'))
    # Readable rights and public source provenance travel with the exported book.
    rights = ('# Edition and rights\n\nOriginal author: boluopai. This reading edition is generated from the public YinYang package. '
              'Original prose is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). '
              'Images and third-party material retain their separate rights. See the [package license](' + GITHUB + '/blob/' + revision + '/skills/yinyang/LICENSE) '
              'and [image notices](' + SITE + '/rights/).\n\nThe layout and static rendering are adapted for PDF; they do not replace the maintained online sources.' if english else
              '# 版本与权利\n\n原作者：boluopai。本阅读版由公开阴阳包生成。原创文字采用 '
              '[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)；图像与第三方材料保留各自的权利范围。'
              '详见[包内许可](' + GITHUB + '/blob/' + revision + '/skills/yinyang/LICENSE)与[图像及其他权利说明](' + SITE + '/rights/)。'
              '\n\n本版为 PDF 调整了版面与静态呈现；持续维护的在线来源仍可由书内链接访问。')
    rights_blocks = parse(rights)['blocks']
    rights_blocks[0]['c'][1][0] = 'edition-and-rights'
    book['blocks'].extend(rights_blocks)
    if missing:
        raise ValueError('Unresolved internal links: ' + json.dumps(missing, ensure_ascii=False))
    ast = work / (lang + '.json')
    ast.write_text(json.dumps(book, ensure_ascii=False))
    body = run(['pandoc', '--from=json', '--to=typst', '--wrap=none', str(ast)]).decode()
    header = (ROOT / 'scripts/pdf/reading.typ').read_text()
    header = header.replace('"LANGUAGE"', json.dumps('en' if english else 'zh'))
    header = header.replace('"BOOKTITLE"', json.dumps('YinYang' if english else '阴阳', ensure_ascii=False))
    header = header.replace('"BOOKSUBTITLE"', json.dumps('Steal Fire, Then Become Fire' if english else '窃火，然后成为火', ensure_ascii=False))
    header = header.replace('"EDITION"', json.dumps('English reading edition' if english else '中文阅读版', ensure_ascii=False))
    header = header.replace('"BUILDSTAMP"', json.dumps(stamp + ' · ' + revision[:12], ensure_ascii=False))
    typ = work / (lang + '.typ')
    typ.write_text(header + '\n' + body)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['typst', 'compile', str(typ), str(output), '--root', '/'], check=True)
    if output.stat().st_size > 16 * 1024 * 1024:
        raise ValueError('PDF exceeds the content release 16 MiB object limit: ' + str(output))
    report = {'language': lang, 'source': revision, 'chapters': len(paths), 'internal_links': internal,
              'external_links': external, 'sources': paths, 'output': str(output), 'bytes': output.stat().st_size}
    (work / (lang + '-report.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--revision', help='Exact public Git revision; defaults to source HEAD')
    parser.add_argument('--language', choices=['zh-CN', 'en', 'both'], default='both')
    parser.add_argument('--out', type=Path, default=ROOT / 'dist/downloads')
    parser.add_argument('--work', type=Path, help='Temporary build directory; never a public output')
    parser.add_argument('--sample', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve()
    revision = run(['git', '-C', str(repo), 'rev-parse', args.revision or 'HEAD']).decode().strip()
    if not re.fullmatch('[0-9a-f]{40}', revision):
        parser.error('Source must resolve to an exact Git commit')
    work = args.work or Path(tempfile.mkdtemp(prefix='yinyang-pdf-'))
    work.mkdir(parents=True, exist_ok=True)
    diagrams = DiagramRenderer(work)
    try:
        for english in (False, True):
            lang = 'en' if english else 'zh-CN'
            if args.language not in ('both', lang):
                continue
            build(repo, revision, english, args.out / ('yinyang.' + lang + '.pdf'), work, args.sample, diagrams)
    finally:
        diagrams.close()


if __name__ == '__main__':
    main()
