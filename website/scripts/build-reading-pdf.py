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
from reading_maps import diagram_placements, TITLES
from article_art import SCENES, CAPTIONS
from pdf_diagrams import DiagramRenderer
from reader_names import reader_text, reader_document

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
    sections = []
    for zh, en, essays in GROUPS:
        members = []
        for name, _ in essays:
            members.append('references/docs/' + name)
            for parent, branches, _ in BRANCHES:
                if parent == name:
                    members.extend('references/docs/' + branch for branch in branches)
        sections.append((f'{len(sections) + 1:02d} · ' + (en if english else zh), members))
    sections.append(('06 · YinYang appendices' if english else '06 · 阴阳的附录',
                     ['references/docs/core-views'] + [path for group in APPENDICES for path in group]))
    sections.append(('07 · Resources and advice' if english else '07 · 资料与建议',
                     ['references/docs/' + name for name in
                      ('getting-started', 'research-and-learning', 'psychological-support')]))
    return [(title, [PACKAGE + name + edition for name in members]) for title, members in sections]


def read_source(repo, revision, path):
    if not path.startswith(PACKAGE) or '/personal/' in path or '/situated/' in path:
        raise ValueError('Only the public package may be read: ' + path)
    return run(['git', '-C', str(repo), 'show', revision + ':' + path])


def prepare_markdown(text):
    text = re.sub(r'^---\n[\s\S]*?\n---\n', '', text)
    text = re.sub(r'<!-- repository-only:start -->[\s\S]*?<!-- repository-only:end -->', '', text)
    text = re.sub(r'<details>\s*<summary>(?:本篇导航|On this page)</summary>[\s\S]*?</details>', '', text)
    text = re.sub(r'(?:^## [^\n]+\n\s*)?<nav class="guide-navigation"[^>]*>[\s\S]*?</nav>', '', text, flags=re.M)
    text = re.sub(r'<a\s+id="([^"]+)"\s*></a>', r'[]{#\1}', text)
    text = re.sub(r'<summary>(.*?)</summary>', r'\n\n**\1**\n\n', text, flags=re.S)
    text = re.sub(r'</?details[^>]*>', '', text)
    text = re.sub(r'<!--[\s\S]*?-->', '', text)
    # Standalone package navigation repeats the book's contents and bookmarks.
    rows = []
    for row in text.splitlines():
        if re.search(r'\[(?:Home|首页|English edition|English|中文|中文版|简体中文|完整中文版|Documents & diagrams|文档与图示)\]\(', row):
            remainder = re.sub(r'\[[^\]]*\]\([^)]*\)', '', row)
            if re.fullmatch(r'[\s·|/]*', remainder):
                continue
        rows.append(row)
    return '\n'.join(rows)


def intro(english, revision, stamp):
    if english:
        return f'''# Reading this edition

This book collects YinYang's public philosophical essays, writing guides, and practical resources.
Its five-part main sequence, Steal Fire, Then Become Fire, contains nineteen
essays and a focused extension, following the website's argument. Core views
comes after that sequence in part 06. These appendices explain the connection between
philosophy and models and provide six public writing guides, further reading,
and the Skill's package guide. Part 07, Resources and advice, collects Tool use,
Research and Learning, and Psychology; it does not include the Skills directory.
Private situated accounts and personal material
are excluded.

You can follow the argument in order or enter through a question of your own.
**If literature, history, or philosophy is not your field, start with relevant
Core views**, then follow their links to examine the reasons and conditions
behind each position. Core views also serves as a reference when revisiting the
book. You need not accept every position or read every chapter; writing your
own philosophy or other essays is a separate choice of interest.

Selected ideas can support organizing experiences, revising personal
psychological material, and configuring a fitting environment. Keep personal
interpretations grounded in sources, retain uncertainty, and revise them through
experience. **YinYang must not be used for psychological self-help work,
self-diagnosis, mental-health assessment, or treatment.** These working accounts
are not clinical assessments, and the project has not been systematically
evaluated for those uses. Personal experience and version history do not establish
general psychological effects. When professional assessment or care is needed,
seek a qualified professional; project texts and model outputs cannot replace
that service. The [source use statement]({GITHUB}/blob/{revision}/README.md#intended-use-and-mental-health)
sets out the same boundary.

Use the contents, PDF bookmarks, and teal links to reach chapters, figures, and
specific sections. The five relational diagrams accompany the same passages as
on the website, scaled proportionally to the portrait page. This edition preserves
the original prose while adapting navigation, pagination, and figure presentation
for continuous reading. External references retain their source links; the
author's repository and website locators are gathered here at the front. The
practical guides are included in full at the end of this edition.

Generated {stamp} (Asia/Shanghai), from public source
[{revision[:12]}]({GITHUB}/tree/{revision}/skills/yinyang).
[Package license]({GITHUB}/blob/{revision}/skills/yinyang/LICENSE) · [Image and other rights]({SITE}/rights/).
'''
    return f'''# 怎样读这本书

本书收录阴阳的公开哲学论述、写作指南与实用资料。正文「窃火，然后成为火」分为 01—05 五部分，包含十九篇
主线文章及一篇专题延伸，沿用网站的论述顺序。06「阴阳的附录」从「基本观点」开始，说明哲学与模型的
连接，并收录六份公开写作指南、参考阅读及 Skill 的形式说明。07「资料与建议」完整收录
「工具使用」「科研与学习」「心理」，不收录 Skills 目录。私人实际文件与个人材料不在
本书收录范围内。

阅读可以沿论证顺序展开，也可以从自己的问题进入。**非文史哲背景的读者，建议先选读相关的
「基本观点」**，再沿链接考察相应立场的理由与适用条件；读过正文后，也可以用它回看整体。
不必接受全部立场或通读每篇文章。是否进一步写自己的哲学或其他文章，由个人兴趣决定。

选定的思想可以用于整理经历、修订个人心理材料，以及配置适合自己的环境。个人解释需要
保留来源与不确定性，并随经验修订。**阴阳不能用于心理自助工作、自行诊断、心理健康评估
或治疗。**这些工作描述不是临床评估，项目也尚未经过针对上述用途的系统性实证评估；
个人经验与版本历史不能确立普遍的心理效果。需要专业评估或照护时，应寻求合格专业人员，
项目文字与模型输出不能替代这种服务。[来源说明]({GITHUB}/blob/{revision}/README.zh-CN.md#用途与心理健康说明)
载有同一用途边界。

目录、PDF 书签与青色链接用于跳转到文章、图示和具体章节。五张关系图放在与网页相同的
正文位置，按纵向书页等比例缩放。本版保留原文，为连续阅读调整导航、分页和图示呈现。
外部文献保留来源链接，作者自己的仓库和网页出处集中列在书首；
三篇实用指南收录于书末，可由目录直接进入。

生成日期：{stamp}（北京时间）。
公开内容版本：[{revision[:12]}]({GITHUB}/tree/{revision}/skills/yinyang)。
[包内许可]({GITHUB}/blob/{revision}/skills/yinyang/LICENSE) · [图像及其他权利说明]({SITE}/rights/)。
'''


def parse(text):
    return json.loads(run(['pandoc', '--from=' + READER, '--to=json'], input=text.encode()))


def build(repo, revision, english, output, work, sample, diagrams):
    lang = 'en' if english else 'zh-CN'
    stamp = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d')
    sections = book_paths(english)
    paths = [path for _, members in sections for path in members]
    if sample:
        paths = paths[:3]  # Opening essays; the full build is authoritative.
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
    figure_names = {name for path in paths for name, _ in
                    diagram_placements(not english).get(Path(path).name.split('.')[0], [])}

    def resolve_link(href, source):
        nonlocal internal, external
        parsed = urlsplit(href)
        absolute_target = None
        if parsed.netloc.lower() in {'boluopai.net', 'www.boluopai.net'}:
            article = re.fullmatch(r'/philosophy/([^/]+)/(?:en/)?', parsed.path)
            document = re.fullmatch(r'/repositories/prometheus/source/(.+)\.html', parsed.path)
            figure = re.fullmatch(r'/repositories/prometheus/diagrams/([^/]+)/(?:en/)?', parsed.path)
            guide = re.fullmatch(r'/(getting-started|research-learning|psychology)/(?:en/)?', parsed.path)
            if figure and figure[1] in figure_names:
                internal += 1
                return '#figure-' + figure[1]
            if article:
                absolute_target = PACKAGE + 'references/docs/' + article[1] + ('.md' if english else '.zh-CN.md')
            elif document:
                absolute_target = document[1] + '.md'
            elif guide:
                name = {'getting-started': 'getting-started', 'research-learning': 'research-and-learning', 'psychology': 'psychological-support'}[guide[1]]
                absolute_target = PACKAGE + 'references/docs/' + name + ('.md' if english else '.zh-CN.md')
            else:
                return None
        elif parsed.netloc.lower() == 'github.com' and parsed.path.lower().startswith(('/boluopai-net/', '/sun2prometheus/')):
            prefix = '/boluopai-net/prometheus2heraclitus/blob/'
            if parsed.path.lower().startswith(prefix):
                absolute_target = parsed.path[len(prefix):].split('/', 1)[-1]
            else:
                return None
        elif parsed.scheme or parsed.netloc:
            external += 1
            return href
        path = PurePosixPath(absolute_target) if absolute_target else (PurePosixPath(source).parent / unquote(parsed.path) if parsed.path else PurePosixPath(source))
        parts = []
        for piece in path.parts:
            if piece == '..':
                parts.pop()
            elif piece != '.':
                parts.append(piece)
        target = '/'.join(parts)
        fragment = unquote(parsed.fragment)
        if '/references/diagrams/' in target:
            name = Path(target).name.split('.')[0]
            if name in figure_names:
                internal += 1
                return '#figure-' + name
        if target not in documents and target.endswith('.md'):
            edition_target = target.removesuffix('.zh-CN.md').removesuffix('.md') + ('.md' if english else '.zh-CN.md')
            if (edition_target, fragment) in anchors:
                target = edition_target
        if target in documents:
            label = anchors.get((target, fragment))
            if not label:
                missing.append((source, href))
                return href
            internal += 1
            return '#' + label
        # Uncollected own material stays readable prose, not an outbound citation.
        return None

    def transform(node, source):
        if node.get('t') == 'Span' and node['c'][0][0] and not node['c'][1]:
            # Separate location-bearing elements keep consecutive source aliases.
            return {'t': 'RawInline', 'c': ['typst', '#metadata(none) <' + node['c'][0][0] + '>']}
        if node.get('t') == 'Link':
            target = resolve_link(node['c'][2][0], source)
            if target is None:
                return {'t': 'Span', 'c': [node['c'][0], node['c'][1]]}
            node['c'][2][0] = target
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
    for section_title, members in sections:
        if not members:
            continue
        book['blocks'].append(raw_typst('#part(' + json.dumps(reader_text(section_title), ensure_ascii=False) + ')'))
        for chapter_index, path in enumerate(members):
            if chapter_index:
                book['blocks'].append(raw_typst('#pagebreak(weak: true)'))
            doc = walk(copy.deepcopy(documents[path]), lambda node: transform(node, path))
            name = Path(path).name.split('.')[0]
            blocks = doc['blocks']
            art = ROOT / 'dist/art' / (name + ('.svg' if name == 'writing-a-sinthome' else '.png'))
            if name in SCENES and art.is_file():
                image_path = asset(art)
                caption = reader_text(CAPTIONS.get(name, SCENES[name])[english])
                blocks.insert(1, raw_typst('#chapter-art(' + json.dumps(str(image_path)) + ', ' + json.dumps(caption, ensure_ascii=False) + ')'))
            additions = {}
            for diagram, heading in diagram_placements(not english).get(name, []):
                if heading is None:
                    boundary = next(i for i, block in enumerate(blocks)
                                    if block.get('t') == 'Header' and block['c'][0] == 3)
                else:
                    section_start = next(i for i, block in enumerate(blocks)
                                         if block.get('t') == 'Header' and plain(block['c'][2]) == heading)
                    boundary = next(i for i in range(section_start + 1, len(blocks))
                                    if blocks[i].get('t') == 'Para') + 1
                # Keep aliases immediately before their original section, rather
                # than moving their link destinations in front of a new figure.
                while boundary and blocks[boundary - 1].get('t') == 'Para' and all(
                    item.get('t') == 'Space' or (item.get('t') == 'RawInline' and
                    item['c'][0] == 'typst' and item['c'][1].startswith('#metadata(none)'))
                    for item in blocks[boundary - 1]['c']):
                    boundary -= 1
                source = PACKAGE + 'references/diagrams/' + diagram + ('.svg' if english else '.zh-CN.svg')
                image_path = asset(source, True)
                additions[boundary] = [raw_typst('#metadata(none) <figure-' + diagram + '>\n#book-figure(' + json.dumps(str(image_path)) + ', ' + json.dumps(reader_text(TITLES[diagram][english]), ensure_ascii=False) + ')')]
            if additions and list(additions) != sorted(additions):
                raise ValueError('PDF figure positions no longer follow the website article order')
            for index, block in enumerate(blocks):
                book['blocks'].extend(additions.get(index, []))
                book['blocks'].append(block)
    # Readable rights and public source provenance travel with the exported book.
    rights = ('# Edition and rights\n\nOriginal author: boluopai. This reading edition is generated from the public YinYang package. '
              'Original prose is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). '
              'Images and third-party material retain their separate rights. Source and edition information is collected at the beginning of the book.\n\nThe layout and figures are adapted for book reading.' if english else
              '# 版本与权利\n\n原作者：boluopai。本阅读版由公开阴阳包生成。原创文字采用 '
              '[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)；图像与第三方材料保留各自的权利范围。'
              '来源与版本信息集中列于书首。'
              '\n\n本版为书籍阅读调整了版面与图示呈现。')
    rights_blocks = parse(rights)['blocks']
    rights_blocks[0]['c'][1][0] = 'edition-and-rights'
    book['blocks'].extend(rights_blocks)
    if missing:
        raise ValueError('Unresolved internal links: ' + json.dumps(missing, ensure_ascii=False))
    ast = work / (lang + '.json')
    ast.write_text(json.dumps(reader_document(book), ensure_ascii=False))
    body = run(['pandoc', '--from=json', '--to=typst', '--wrap=none', str(ast)]).decode()
    header = (ROOT / 'scripts/pdf/reading.typ').read_text()
    header = header.replace('"LANGUAGE"', json.dumps('en' if english else 'zh'))
    header = header.replace('"BOOKTITLE"', json.dumps(reader_text('YinYang'), ensure_ascii=False))
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
    parser.add_argument('--out', type=Path, default=ROOT / 'dist/reading')
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
