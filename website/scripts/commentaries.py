"""One argument-driven reading route across common and site-owned essays."""
import html
import json
import re
from pathlib import Path
from repository_panel import with_comments

ROOT = Path(__file__).resolve().parents[1]
DOCS = 'skills/yinyang/references/docs/'
SITE_ARTICLES = {'why-yinyang', 'literary-programming', 'baby-heraclitus', 'meng', 'deleuze-and-becoming'}
SERIES = '/philosophy/yinyang/'  # Preserve the existing public URL.
SERIES_NAMES = ('窃火，然后成为火', 'Borrow Fire, Then Become Fire')
GROUPS = [
    ('起点：窃火与行动者的生成', 'Starting point: borrowed fire and the becoming of agents', [
        ('stealing-fire', '从已经可用的智能开始：有限的人怎样借来火，再发展自己的理解、创造与行动？'),
        ('personal-first-humanism', '把个人优先的价值前提说清楚：工具与合作应当支持具体人的生活，而不以输出数量代替发展。'),
        ('why-yinyang', '先说明 agent 是什么，再问分散能力为什么需要共同方向：把实际的人、对方与关系写进安排。'),
        ('meng', '先论证开放、共同学习与引导在什么条件下形成适应优势，为“宝宝”的培养方向提供理由。'),
        ('baby-heraclitus', '接着用赫拉克利特的火与河流塑造这个宝宝：保持开放，能够判断、创造并被相遇改变。'),
    ]),
    ('理解：变化世界中的有限探究', 'Understanding: finite inquiry in a changing world', [
        ('world-and-expression', '区分世界、过程、模型与表达，让图景能够行动，也能够被世界纠正。'),
        ('flow-and-time', '考察变化、记忆与体验的不同节奏：过去怎样进入现在，连续性怎样保留修订空间？'),
        ('reasoning', '从事件流中形成问题、候选解释与可检查的推论，区分保存材料和接受观点。'),
        ('preference-harness', '让偏好、规则与证据相连：选择要展开的可能，检查它们支持什么，并在冲突与后果中修订理解。'),
        ('finite-inquiry-and-abstraction', '在有限信息与时间中选择足够有用的抽象，明确局部形式结果与现实解释的尺度。'),
    ]),
    ('相遇：共同参与怎样成为可能', 'Encounter: making shared participation possible', [
        ('yinyang-and-taiji', '用日月、Shuang yu 与大地表达相互生成：双方可以判断和创造，作品遇到独立后果。'),
        ('participation-and-support', '把关系落到参与，连接理解、表达和可用行动，使支持保留人的主动性。'),
    ]),
    ('形成：从人类 agent 到个人哲学与实践', 'Formation: from human agency to personal philosophy and practice', [
        ('literary-programming', '通过人物、意象与关系凝缩理解，再让具体指令和工具展开它。'),
        ('metaphor-and-self-revision', '把隐喻展开为类比与关系图，组织模型、记录和工具之间的分布式认知，并修订组织本身。'),
        ('writing-a-sinthome', '从已经能够感知、生成与行动的人出发，借助模型拓展能力，形成自己的个人哲学，以及承载它的环境与实践。'),
    ]),
    ('实践：成为火，进入环境与反馈', 'Practice: becoming fire through environment and feedback', [
        ('local-source-and-website', '哲学、心理与工程怎样统一于同一物理现实，并通过不同抽象层次形成实践闭环？'),
        ('embodied-experimental-philosophy', '让作品进入具身生活，以实践和反思的反馈修订解释、系统边界及目的。'),
        ('example-and-commons', '把已形成的实践交给另一位创造者：采用、组合，或写出自己的哲学与形式。'),
    ]),
]
STAGE_REASONS = [
    ('先总览窃火的论证，再说明价值与行动者；超萌论证给出培养的条件性理由，赫拉克利特宝宝继而使培养方向取得人物形象。', 'Preview the argument, establish value and agency, give cultivation its conditional rationale through super-cuteness, then embody that direction in Baby Heraclitus.'),
    ('给实践以可修正的理解：从表示与时间进入推理，以偏好 harness 连接冲突、视图选择和推论支持，再考察有限抽象。', 'Make understanding corrigible: move from representation and time into reasoning, connect conflict, view selection, and support through the preference harness, then examine finite abstraction.'),
    ('把已有的行动者概念落实为相互生成与实际参与，保留人的主动性及模型的贡献。', 'Develop the agent concept into reciprocal generation and actual participation, preserving human initiative and model contributions.'),
    ('人类 agent 是起点：已有的能动者借助生成能力，发展自己的哲学、世界观与可维系的生活形式。', 'Human agency is the starting point: an existing agent draws on generative capabilities to develop a personal philosophy, worldview, and sustainable form of living.'),
    ('从开始自己的实践进入环境的三种形式，再以实验与反馈继续生成，并邀请另一位创造者。', 'Begin your own practice, then enter its three environmental forms, experimental feedback, and further creation with others.'),
]
MAINLINE = [n for _, _, entries in GROUPS for n, _ in entries]
SUMMARIES = {n: s for _, _, entries in GROUPS for n, s in entries}
EN_SUMMARIES = {
    'stealing-fire': 'Begin with available intelligence: borrow fire, then develop understanding, creation, and action.',
    'personal-first-humanism': 'Make the ethical premise explicit: tools and cooperation support concrete lives; output volume does not substitute for development.',
    'world-and-expression': 'Distinguish world, process, model, and expression so representations guide action and meet correction.',
    'flow-and-time': 'Examine different rhythms of change, memory, and experience, preserving continuity and room for revision.',
    'reasoning': 'Form questions, candidate explanations, and checkable inferences; distinguish retaining material from accepting a view.',
    'preference-harness': 'Connect preferences, rules, and evidence: choose possibilities to develop, examine their support, and revise through conflict and consequences.',
    'finite-inquiry-and-abstraction': 'Choose useful abstractions under finite information and time, distinguishing formal results from worldly explanation.',
    'yinyang-and-taiji': 'Use Sun, Moon, paired fish, and Earth to express reciprocal generation and the independent consequences of creations.',
    'participation-and-support': 'Connect understanding, expression, and available action through support that preserves human initiative.',
    'why-yinyang': 'First define an agent, then ask why scattered capacities need shared direction: write the actual participants and relationship into the arrangement.',
    'literary-programming': 'Condense understanding through characters, imagery, and relationships, then unfold it through instructions and tools.',
    'metaphor-and-self-revision': 'Develop metaphor into analogy and relation maps, distribute cognition across models, records, and tools, and revise that organization.',
    'writing-a-sinthome': 'Begin with a person who already perceives, generates, and acts; expand capacities with models and form a personal philosophy and the environment that sustains it.',
    'baby-heraclitus': 'Then give this baby a Heraclitean character: remain open, judge, create, and change through encounters.',
    'meng': 'First establish when openness, shared learning, and guidance support adaptation, giving the baby’s cultivation a rationale.',
    'local-source-and-website': 'Understand philosophy, psychology, and engineering as activities in one physical reality, connected through distinct levels of abstraction and practice.',
    'embodied-experimental-philosophy': 'Bring works into embodied life; use practice and reflection to revise explanations, boundaries, and aims.',
    'example-and-commons': 'Offer the practice to another creator: adopt, combine, or write a philosophy and form of your own.',
}
EXTENSIONS = [
    ('lacan-and-description-logic', '言说与自我表述', '从圣状深入言说事件、自我表述与形式断言。', 'writing-a-sinthome'),
    ('deleuze-and-becoming', '机器与生成', '从圣状的维系形式进入连接、组装与生成的哲学比较。', 'writing-a-sinthome'),
]
EN_EXTENSIONS = {
    'lacan-and-description-logic': ('Speech and self-description', 'From the sinthome, examine speech events, self-description, and formal assertions.'),
    'deleuze-and-becoming': ('Machines and becoming', 'From the sinthome’s sustaining form, compare connections, assemblages, and becoming.'),
}
BRANCHES = [
    ('writing-a-sinthome', ['lacan-and-description-logic'], 'local-source-and-website'),
    ('writing-a-sinthome', ['deleuze-and-becoming'], 'local-source-and-website'),
]
ESSAYS = (set(MAINLINE) | {x[0] for x in EXTENSIONS}) - SITE_ARTICLES
RETIRED = {'metaphors', 'oedipus-and-thirdness', 'dialectic-and-repair'}
IMAGE_SUCCESSORS = {'01': 'yinyang-and-taiji', '02': 'stealing-fire', '03': 'yinyang-and-taiji', '04': 'world-and-expression', '05': 'preference-harness', '06': 'lacan-and-description-logic', '07': 'writing-a-sinthome', '08': 'stealing-fire'}


def article_url(name, chinese):
    return f'/philosophy/{name}/' + ('' if chinese else 'en/')


def essay_title(name, chinese, title=None):
    """Resolve headings at their owner, without importing executable renderers."""
    if name in SITE_ARTICLES:
        path = ROOT / 'content/philosophy' / (name + ('.md' if chinese else '.en.md'))
        match = re.search(r'^#\s+(.+)$', path.read_text(), re.M)
    elif title is not None:
        return title(DOCS + name + ('.zh-CN.md' if chinese else '.md'))
    else:
        # Standalone rendering follows common projection: use its real edition.
        path = ROOT / 'dist' / article_url(name, chinese).lstrip('/') / 'index.html'
        match = re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>', path.read_text())
    if match is None:
        raise ValueError(f'Missing reading title: {name}')
    return html.unescape(re.sub(r'<[^>]+>', '', match.group(1)))


def article_link(name, chinese, label='', title=None, relation=None):
    heading = html.escape(essay_title(name, chinese, title))
    prefix = html.escape(label) + ' · ' if label else ''
    rel = f' rel="{relation}"' if relation else ''
    if relation:
        return f'<a{rel} href="{article_url(name, chinese)}"><span class="navigation-label">{html.escape(label)}</span><span class="navigation-title">{heading}</span></a>'
    return f'<a{rel} href="{article_url(name, chinese)}">{prefix}{heading}</a>'


def retired_url(path, fragment=''):
    if not path.startswith(DOCS):
        return None
    filename = path[len(DOCS):]
    chinese = filename.endswith('.zh-CN.md')
    name = filename.removesuffix('.zh-CN.md') if chinese else filename.removesuffix('.md')
    if name not in RETIRED:
        return None
    if name == 'dialectic-and-repair':
        return article_url('preference-harness', chinese)
    ym = re.match(r'ym-(\d\d)(?:-|$)', fragment.lower())
    successor = IMAGE_SUCCESSORS.get(ym.group(1), 'yinyang-and-taiji') if ym and name == 'metaphors' else 'yinyang-and-taiji'
    return article_url(successor, chinese)


def essay_url(path):
    if not path.startswith(DOCS) or '/' in path[len(DOCS):]:
        return None
    filename = path[len(DOCS):]
    chinese = filename.endswith('.zh-CN.md')
    name = filename.removesuffix('.zh-CN.md') if chinese else filename.removesuffix('.md')
    return article_url(name, chinese) if name in ESSAYS and filename.endswith('.md') else None


def redirect_page(destination, image_successors=None):
    safe = html.escape(destination, quote=True)
    if image_successors is None:
        script = f'location.replace({json.dumps(destination)}+location.hash);'
    else:
        script = 'const routes=' + json.dumps(image_successors) + ';const match=decodeURIComponent(location.hash.slice(1)).toLowerCase().match(/^ym-(\\d{2})(?:-|$)/);location.replace((match&&routes[match[1]])||' + json.dumps(destination) + ');'
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow, noimageindex"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Philosophy · boluopai</title><link rel="canonical" href="{safe}"><script>{script}</script></head><body><a href="{safe}">阅读全文 / Read the essay →</a></body></html>'


def branch_panel(parent, chinese, title=None):
    branches = [b for b in BRANCHES if b[0] == parent]
    if not branches:
        return ''
    panels = []
    for _, items, _ in branches:
        links = ' → '.join(article_link(n, chinese, title=title) for n in items)
        label = '专题路径' if chinese else 'Focused branch'
        panels.append(f'<aside class="series-context"><p>{label}: {links}</p></aside>')
    return ''.join(panels)


def reading_context(name, chinese, title=None):
    sequence_url = SERIES + ('' if chinese else 'en/')
    home = f'<a class="series-home" href="{sequence_url}">{"回到窃火" if chinese else "Back to Borrow Fire"}</a>'
    nav_label = '文章导航' if chinese else 'Article navigation'
    if name in MAINLINE:
        i = MAINLINE.index(name)
        stage = next(zh if chinese else en for zh, en, entries in GROUPS if any(n == name for n, _ in entries))
        intro = SUMMARIES[name] if chinese else EN_SUMMARIES[name]
        label = '主线' if chinese else 'MAIN SEQUENCE'
        guide = f'<aside class="series-context"><p class="eyebrow">{SERIES_NAMES[0 if chinese else 1]} · {label} {i + 1:02d} / {len(MAINLINE):02d}</p><p>{html.escape(stage)}</p><p>{intro}</p></aside>'
        links = []
        if i:
            links.append(article_link(MAINLINE[i - 1], chinese, '上一篇' if chinese else 'Previous', title, 'prev'))
        if i + 1 < len(MAINLINE):
            links.append(article_link(MAINLINE[i + 1], chinese, '下一篇' if chinese else 'Next', title, 'next'))
        else:
            links.append(f'<a rel="next" href="/getting-started/{"" if chinese else "en/"}"><span class="navigation-label">{"接下来" if chinese else "Continue"}</span><span class="navigation-title">{"开始自己的实践" if chinese else "Begin your own practice"}</span></a>')
        nav = f'<nav class="series-navigation" aria-label="{nav_label}">' + ''.join(links) + home + '</nav>' + branch_panel(name, chinese, title)
    else:
        parent, items, return_to = next(b for b in BRANCHES if name in b[1])
        i = items.index(name)
        intro = next(x[2] for x in EXTENSIONS if x[0] == name) if chinese else EN_EXTENSIONS[name][1]
        label = '专题路径' if chinese else 'FOCUSED BRANCH'
        guide = f'<aside class="series-context"><p class="eyebrow">{SERIES_NAMES[0 if chinese else 1]} · {label}</p><p>{intro}</p></aside>'
        previous = items[i - 1] if i else parent
        following = items[i + 1] if i + 1 < len(items) else return_to
        next_label = ('下一篇' if chinese else 'Next') if i + 1 < len(items) else ('继续主线' if chinese else 'Continue main sequence')
        nav = f'<nav class="series-navigation" aria-label="{nav_label}">' + article_link(previous, chinese, '上一篇' if chinese else 'Previous', title, 'prev') + article_link(following, chinese, next_label, title, 'next') + home + '</nav>'
    return guide, nav


def reading_rail(toc, chinese):
    label = '本文目录' if chinese else 'On this page'
    return f'<aside class="reading-rail"><nav class="reader-toc" aria-label="{label}"><p class="toc-title">{label}</p>{toc}</nav></aside>'


def write_essay(dist, path, page_title, rendered, toc, source_note, shell, title):
    destination = essay_url(path)
    if destination is None:
        return False
    chinese = path.endswith('.zh-CN.md')
    name = path[len(DOCS):].split('.')[0]
    counterpart = article_url(name, not chinese)
    art = ''
    if (dist / 'art' / f'{name}.png').is_file():
        alt = page_title + ('的意象插画' if chinese else ' — poetic illustration')
        art = f'<figure class="article-art"><img src="/art/{name}.png" alt="{html.escape(alt, quote=True)}" width="1536" height="1024" fetchpriority="high"></figure>'
    guide, navigation = reading_context(name, chinese, title)
    rendered = re.sub(r'(<h1\b[^>]*>[\s\S]*?</h1>)\s*<p>(?:<a [^>]*>[^<]+</a> · )+<a [^>]*>(?:English|中文)</a></p>', r'\1', rendered, count=1)
    if chinese:
        rendered = re.sub(r'(<h1\b[^>]*>[^<：]+：)', r'\1<br>', rendered, count=1)
    rendered = rendered.replace('</h1>', '</h1>' + art + guide, 1)
    body = f'<main id="main" class="wrap library-reader commentary"><article class="document">{rendered}</article>{reading_rail(toc, chinese)}<div class="reading-end">{navigation}{source_note}</div></main>'
    page = shell(page_title, body, 'zh-CN' if chinese else 'en', '<meta name="robots" content="noindex, nofollow, noimageindex"><link rel="stylesheet" href="/article.css">')
    page = page.replace('href="/philosophy/">哲学评论', 'href="/philosophy/" aria-current="page">哲学评论').replace('href="/repositories/" aria-current="page"', 'href="/repositories/"')
    page = page.replace('</nav></header>', f'<a class="language-link" lang="{"en" if chinese else "zh-CN"}" href="{counterpart}">{"English" if chinese else "中文"}</a></nav></header>', 1)
    target = dist / destination.lstrip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page)
    return True


def practice_entrance(chinese):
    heading = '开始自己的实践' if chinese else 'Begin your own practice'
    text = '从入门指南开始，让模型帮助形成并实现适合自己的安排。概念阅读可以按问题返回，不必先读完整组文章。' if chinese else 'Begin with the getting-started guide and ask a model to help form and realize your arrangement. Return to conceptual reading by question; completing the series is not a prerequisite.'
    guide = '/getting-started/' + ('' if chinese else 'en/')
    method = '/repositories/prometheus/source/' + DOCS + ('creation-method.zh-CN.html' if chinese else 'creation-method.html')
    return f'<section class="series-entrance" id="practice"><h2><a href="{guide}">{heading}</a></h2><p>{text}</p><p><a href="{method}">{"进一步了解创造方法" if chinese else "Explore the creation method"}</a></p></section>'


def index_body(chinese, title, full):
    sequence_url = SERIES + ('' if chinese else 'en/')
    name = SERIES_NAMES[0 if chinese else 1]
    thesis = '借来智能的火，在实践中成为能够理解、判断、创造并继续生成的人。' if chinese else 'Borrow the fire of intelligence; through practice, develop understanding, judgment, creation, and the capacity to keep becoming.'
    intro = '这条论证从能力的取得走向人的培养，展开有限探究、合作关系与实际实现，最后让生活和世界的反馈进入共同创造。能力可以内化，也可以可靠地分布在人、模型与工具之间。阴阳是其中一个已经展开的哲学与工作形式。' if chinese else 'The argument moves from acquiring capability to cultivating a person, through finite inquiry, cooperation, and realization, then into lived feedback and shared creation. Capacities can be internalized or reliably distributed across person, models, and tools. YinYang is one developed philosophical and working form within it.'
    back = '/philosophy/' + ('' if chinese else 'en/') if full else ('/' if chinese else '/en/')
    back_label = '哲学' if full and chinese else 'Philosophy' if full else '火与河流' if chinese else 'Fire and River'
    heading = f'<div class="collection-heading"><img class="motif collection-motif" src="/motifs/sun-river.svg" alt="" aria-hidden="true"><a class="back" href="{back}">← {back_label}</a><h1>{name}</h1><p class="collection-intro">{thesis}</p><p>{intro}</p></div>'
    sections = []
    number = 1
    for index, (zh, en, entries) in enumerate(GROUPS, 1):
        stage = zh if chinese else en
        reason = STAGE_REASONS[index - 1][0 if chinese else 1]
        if not full:
            destination = sequence_url + f'#stage-{index}'
            sections.append(f'<section class="essay-entry stage-entry"><div class="essay-meta">{index:02d}</div><div><h2><a href="{destination}">{stage}</a></h2><p class="entry-summary">{reason}</p></div></section>')
            continue
        if any(slug == 'local-source-and-website' for slug, _ in entries):
            sections.append(practice_entrance(chinese))
        cards = []
        for slug, summary in entries:
            summary = summary if chinese else EN_SUMMARIES[slug]
            cards.append(f'<section class="essay-entry"><div class="essay-meta">{number:02d}</div><div><h3>{article_link(slug, chinese, title=title)}</h3><p class="entry-summary">{summary}</p></div></section>' + branch_panel(slug, chinese, title))
            number += 1
        destination = article_url(entries[0][0], chinese)
        sections.append(f'<section class="commentary-group" id="stage-{index}"><header class="commentary-group-heading"><h2><a href="{destination}">{stage}</a></h2><p>{reason}</p></header>{"".join(cards)}</section>')
    return '<main id="main" class="wrap collection">' + heading + ''.join(sections) + ('' if full else practice_entrance(chinese)) + '</main>'


def write_index(dist, title):
    for chinese in (True, False):
        suffix = '' if chinese else 'en/'
        template = (dist / 'philosophy' / suffix / 'index.html').read_text()
        for full in (False, True):
            page = re.sub(r'<main[\s\S]*?</main>', lambda _: index_body(chinese, title, full), template, count=1)
            heading = SERIES_NAMES[0 if chinese else 1] + ((' · 阅读顺序' if chinese else ' · Reading order') if full else '')
            page = re.sub(r'<title>[\s\S]*?</title>', f'<title>{heading} · boluopai</title>', page, count=1)
            description = '从窃火到成为火，理解、实现并发展个人实践的五段论证。' if chinese else 'From borrowing fire to becoming fire: five stages of understanding, realizing, and developing personal practice.'
            page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', page, count=1)
            output = dist / (SERIES.lstrip('/') if full else 'philosophy/') / suffix / 'index.html'
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(with_comments(page, not chinese, 'Philosophy'))
