"""One argument-driven reading route through the public YinYang essays."""
import html
import json
import re
from pathlib import Path
from repository_panel import with_comments
from article_art import article_figure

ROOT = Path(__file__).resolve().parents[1]
DOCS = 'skills/yinyang/references/docs/'
SERIES = '/philosophy/'
STAGE_SLUGS = ('starting-point', 'understanding', 'encounter', 'formation', 'practice')
SERIES_NAMES = ('窃火，然后成为火', 'Steal Fire, Then Become Fire')
GROUPS = [
    ('起点：参加窃火，然后拿火培养自己', 'Starting point: join in stealing fire, then use it to cultivate yourself', [
        ('stealing-fire', '从共同的窃火出发：有限的人怎样参与其中，再用火培养自己的理解、创造与行动？'),
        ('personal-first-humanism', '把个人优先的价值前提说清楚：工具与合作应当支持具体人的生活，而不以输出数量代替发展。'),
        ('why-yinyang', '先说明 agent 是什么，再问分散能力为什么需要共同方向：把实际的人、对方与关系写进安排。'),
        ('meng', '先论证开放、共同学习与引导在什么条件下形成适应优势，为“宝宝”的培养方向提供理由。'),
        ('baby-heraclitus', '接着用赫拉克利特的火与河流塑造这个宝宝：保持开放，能够判断、创造并被相遇改变。'),
    ]),
    ('理解：生活轨迹的保留与探究', 'Understanding: retaining and exploring life trajectories', [
        ('world-and-expression', '从共同活动到可以返回的表达：区分过程、模型与记录，说明生活轨迹保留的是什么。'),
        ('flow-and-time', '以共同改善阅读环境为例，通过 Git/GitHub 版本历史与 Computer History 汇集各类历史，形成可接续的生活轨迹。'),
        ('reasoning', '从轨迹中提出问题、比较候选解释，让检查、行动、结果与判断的修订继续留下根据。'),
        ('preference-harness', '在轨迹中保留选择与证据各自的贡献：采用一个工作视图，同时让其他材料与分岔仍能返回。'),
        ('finite-inquiry-and-abstraction', '在有限条件下保留和取用足够的轨迹，把可探索的生活材料带入下一部分的共同反思。'),
    ]),
    ('相遇：共同反思与相互培育', 'Encounter: shared reflection and mutual cultivation', [
        ('yinyang-and-taiji', '从阴阳、相互为根的双鱼进入太极的场，再借弓琴与日月大地理解差别、造物及其返回。'),
        ('participation-and-support', '从对轨迹的共同反思中调整参与和支持，在实际尝试中培育关系，并为个人哲学准备具体理解。'),
    ]),
    ('形成：从个人哲学到实践形式', 'Formation: from personal philosophy to a form of practice', [
        ('literary-programming', '承接共同做事留下的轨迹与对协作的反思，通过文学式编程、隐喻和类比写出自己的哲学。'),
        ('speech-opposition-and-self-formation', '写出的哲学遇到回应，回溯改变理解；辨认对立、重构前提与关系，为个人模型准备内容。'),
        ('metaphor-and-self-revision', '将写出的哲学与生活材料一起凝练为个人、伙伴及双方关系的模型，让理解能够进入持续协作。'),
        ('writing-a-sinthome', '让哲学与个人模型进入实际环境，经由使用与修订，使哲学、心理与工程共同形成具体的圣状。'),
    ]),
    ('实践：持续检验与共同创造', 'Practice: continued testing and shared creation', [
        ('local-source-and-website', '承接已形成的个人安排，说明哲学、心理与工程怎样在本地使用、源内容和作品之间继续维系与修订。'),
        ('embodied-experimental-philosophy', '考察持续使用的后果：修订实现、个人理解或哲学，并区分安排改善与人的能力发展。'),
        ('example-and-commons', '让实践留下的作品与方法成为他人的资源，接续新的创造，也把新的相遇带回自己的生活。'),
    ]),
]
STAGE_REASONS = [
    ('先总览窃火的论证，再说明价值与行动者；超萌论证给出培养的条件性理由，赫拉克利特宝宝继而使培养方向取得人物形象。', 'Preview the argument, establish value and agency, give cultivation its conditional rationale through super-cuteness, then embody that direction in Baby Heraclitus.'),
    ('共同做事留下版本、操作、对话与反馈；把这些材料连成可返回的生活轨迹，保留其中的问题、选择、根据和修订，为下一部分的共同反思准备材料。', 'Shared work leaves versions, operations, conversations, and feedback. Connect them into a revisitable life trajectory, retaining questions, choices, grounds, and revisions as material for the next part’s shared reflection.'),
    ('双方已经共同做事并留下轨迹；现在一起探索和反思这些生活材料，认识彼此怎样参与，在这种相遇中继续培育关系与能力。', 'Having worked together and left a trajectory, explore and reflect on this living material together, recognize each participant’s contribution, and cultivate relationships and capabilities through that encounter.'),
    ('从轨迹与共同反思写出个人哲学，让言说与对立推动理解的形成；再结合生活材料凝练个人模型，落实为能够维系和修订的实践。', 'Write philosophy from trajectories and shared reflection; let speech and opposition develop understanding, distill personal models with living material, then realize a practice that can be sustained and revised.'),
    ('让已经形成的安排继续工作，检验它怎样改变生活与能力；把有用的作品和方法交给新的相遇，使新的轨迹能够回到反思、哲学与模型的修订。', 'Sustain the formed arrangement and examine its effects on life and capabilities. Offer useful works and methods to new encounters, whose trajectories can return to reflection and revisions of philosophy and models.'),
]
MAINLINE = [n for _, _, entries in GROUPS for n, _ in entries]
SUMMARIES = {n: s for _, _, entries in GROUPS for n, s in entries}
EN_SUMMARIES = {
    'stealing-fire': 'Join in the collective work of stealing fire, then use it to cultivate understanding, creation, and action.',
    'personal-first-humanism': 'Make the ethical premise explicit: tools and cooperation support concrete lives; output volume does not substitute for development.',
    'world-and-expression': 'Move from shared activity to revisitable expression: distinguish processes, models, and records to explain what a life trajectory retains.',
    'flow-and-time': 'Use a jointly improved reading environment to gather histories through Git/GitHub version history and Computer History, forming a life trajectory that can be continued.',
    'reasoning': 'Pose questions and compare candidate explanations from the trajectory, retaining grounds for checks, actions, outcomes, and revised judgments.',
    'preference-harness': 'Retain the distinct contributions of choices and evidence: adopt a working view while keeping other materials and branches revisitable.',
    'finite-inquiry-and-abstraction': 'Retain and retrieve enough of the trajectory under finite conditions, carrying explorable living material into the next part’s shared reflection.',
    'yinyang-and-taiji': 'Move from YinYang and mutually grounding paired fish to Taiji’s field, then through bow, lyre, Sun, Moon, and Earth to difference, creations, and their return.',
    'participation-and-support': 'Revise participation and support through shared reflection on the trajectory, cultivate the relationship through actual trials, and prepare concrete understanding for personal philosophy.',
    'why-yinyang': 'First define an agent, then ask why scattered capacities need shared direction: write the actual participants and relationship into the arrangement.',
    'literary-programming': 'Carry jointly produced trajectories and reflection on cooperation into a philosophy of your own through literary programming, metaphor, and analogy.',
    'speech-opposition-and-self-formation': 'Encounter responses to the written philosophy, reinterpret earlier meaning, and reconstruct premises and relationships through opposition, preparing content for personal models.',
    'metaphor-and-self-revision': 'Distill the authored philosophy together with living material into models of the person, counterpart, and relationship for continuing cooperation.',
    'writing-a-sinthome': 'Bring philosophy and personal models into the actual environment; through use and revision, philosophy, psychology, and engineering jointly form a concrete sinthome.',
    'baby-heraclitus': 'Then give this baby a Heraclitean character: remain open, judge, create, and change through encounters.',
    'meng': 'First establish when openness, shared learning, and guidance support adaptation, giving the baby’s cultivation a rationale.',
    'local-source-and-website': 'Receive the formed personal arrangement and explain how philosophy, psychology, and engineering sustain and revise it across local use, source, and works.',
    'embodied-experimental-philosophy': 'Examine continued use: revise realization, personal understanding, or philosophy, distinguishing improvements to arrangements from development of human capabilities.',
    'example-and-commons': 'Let works and methods from the practice become resources for others, continuing creation and bringing new encounters back into one’s own life.',
}
EXTENSIONS = [
    ('deleuze-and-becoming', '机器与生成', '从已经形成的个人实践安排，进入连接、组装与生成的哲学比较。', 'writing-a-sinthome'),
]
EN_EXTENSIONS = {
    'deleuze-and-becoming': ('Machines and becoming', 'From an established personal practice arrangement, compare connections, assemblages, and becoming.'),
}
BRANCHES = [
    ('writing-a-sinthome', ['deleuze-and-becoming'], 'local-source-and-website'),
]
ESSAYS = set(MAINLINE) | {x[0] for x in EXTENSIONS}
RETIRED = {'metaphors', 'oedipus-and-thirdness', 'dialectic-and-repair', 'lacan-and-description-logic'}
IMAGE_SUCCESSORS = {'01': 'yinyang-and-taiji', '02': 'stealing-fire', '03': 'yinyang-and-taiji', '04': 'world-and-expression', '05': 'preference-harness', '06': 'speech-opposition-and-self-formation', '07': 'writing-a-sinthome', '08': 'stealing-fire'}


def article_url(name, chinese):
    return f'/philosophy/{name}/' + ('' if chinese else 'en/')


def stage_url(index, chinese):
    return f'/philosophy/stages/{STAGE_SLUGS[index]}/' + ('' if chinese else 'en/')


def stage_entry(index, chinese):
    return article_url(GROUPS[index][2][0][0], chinese)


def stage_for(name):
    parent = next((parent for parent, branches, _ in BRANCHES if name in branches), name)
    return next((i for i, (_, _, entries) in enumerate(GROUPS) if any(slug == parent for slug, _ in entries)), None)


def book_navigation(current, chinese, title=None):
    """Cross-page book structure, separate from each page's own contents."""
    active = stage_for(current)
    current_title = '' if current == 'overview' else essay_title(current, chinese, title)
    context = current_title
    if active is not None:
        context = GROUPS[active][0 if chinese else 1].split('：' if chinese else ':')[0] + ' · ' + current_title
    def link(url, label, selected=False):
        return f'<a href="{url}"' + (' aria-current="page"' if selected else '') + f'>{html.escape(label)}</a>'
    groups = []
    for index, (zh, en, entries) in enumerate(GROUPS):
        label = zh if chinese else en
        items = []
        for slug, _ in entries:
            branches = [n for parent, names, _ in BRANCHES if parent == slug for n in names]
            nested = '<ul class="book-branches">' + ''.join('<li>' + link(article_url(n, chinese), essay_title(n, chinese, title), current == n) + '</li>' for n in branches) + '</ul>' if branches else ''
            items.append('<li>' + link(article_url(slug, chinese), essay_title(slug, chinese, title), current == slug) + nested + '</li>')
        groups.append(f'<section class="book-stage"><h2>{link(stage_entry(index, chinese), label)}</h2><ol>{"".join(items)}</ol></section>')
    label = '目录' if chinese else 'Contents'
    nav = f'<nav aria-label="{label}" tabindex="0">{"".join(groups)}</nav>'
    status = f'<span class="book-current-context">{html.escape(context)}</span>' if context else ''
    return f'<aside class="book-navigation">{nav}</aside><details class="book-mobile-menu"><summary><span class="book-menu-label">{label}{toggle_text(chinese)}</span>{status}</summary>{nav}</details>'


def toggle_text(chinese):
    return '<span class="contents-toggle"><span class="when-closed">' + ('展开' if chinese else 'Expand') + '</span><span class="when-open">' + ('收起' if chinese else 'Collapse') + '</span></span>'


def useful_contents(toc, rendered):
    """Contents help with substantial, sectioned reading, not short notes."""
    if len(re.findall(r'<a\b[^>]*href=[\"\']#[^\"\']+[\"\']', toc)) < 2:
        return False
    text = html.unescape(re.sub(r'<[^>]+>', ' ', rendered))
    # Approximate reading length across the two editions: two CJK characters
    # count as one word. A short reference should not acquire a navigation rail
    # merely because it has a couple of headings.
    words = len(re.findall(r'[A-Za-z0-9]+', text))
    cjk = len(re.findall(r'[\u3400-\u9fff]', text))
    return words + cjk / 2 >= 600


def book_contents(toc, chinese, rendered):
    if not useful_contents(toc, rendered):
        return ''
    label = '本文目录' if chinese else 'On this page'
    return f'<aside class="reading-rail book-contents-rail"><details class="reader-toc book-contents" open><summary><span>{label}</span>{toggle_text(chinese)}</summary><nav aria-label="{label}">{toc}</nav></details></aside>'


def essay_title(name, chinese, title=None):
    """Resolve headings at their owner, without importing executable renderers."""
    if title is not None:
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
    if name == 'lacan-and-description-logic':
        return article_url('speech-opposition-and-self-formation', chinese)
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
    series_label = '窃火' if chinese else 'Stealing Fire'
    home = f'<a class="series-home" href="{sequence_url}">{"回到窃火" if chinese else "Back to Stealing Fire"}</a>'
    nav_label = '文章导航' if chinese else 'Article navigation'
    if name in MAINLINE:
        i = MAINLINE.index(name)
        stage = next(zh if chinese else en for zh, en, entries in GROUPS if any(n == name for n, _ in entries)).split('：' if chinese else ':', 1)[0]
        intro = SUMMARIES[name] if chinese else EN_SUMMARIES[name]
        label = '主线' if chinese else 'Main'
        guide = f'<aside class="series-context"><p class="eyebrow">{series_label} · {html.escape(stage)} · {label} {i + 1:02d} / {len(MAINLINE):02d}</p><p>{intro}</p></aside>'
        links = []
        if i:
            links.append(article_link(MAINLINE[i - 1], chinese, '上一篇' if chinese else 'Previous', title, 'prev'))
        if i + 1 < len(MAINLINE):
            links.append(article_link(MAINLINE[i + 1], chinese, '下一篇' if chinese else 'Next', title, 'next'))
        else:
            links.append(f'<a rel="next" href="/getting-started/{"" if chinese else "en/"}"><span class="navigation-label">{"接下来" if chinese else "Continue"}</span><span class="navigation-title">{"在实践之前，先学习工具" if chinese else "Before practice, learn to use the tools"}</span></a>')
        nav = f'<nav class="series-navigation" aria-label="{nav_label}">' + ''.join(links) + home + '</nav>' + branch_panel(name, chinese, title)
    else:
        parent, items, return_to = next(b for b in BRANCHES if name in b[1])
        i = items.index(name)
        intro = next(x[2] for x in EXTENSIONS if x[0] == name) if chinese else EN_EXTENSIONS[name][1]
        label = '专题路径' if chinese else 'Focused branch'
        stage = GROUPS[stage_for(name)][0 if chinese else 1].split('：' if chinese else ':', 1)[0]
        guide = f'<aside class="series-context"><p class="eyebrow">{series_label} · {html.escape(stage)} · {label}</p><p>{intro}</p></aside>'
        previous = items[i - 1] if i else parent
        following = items[i + 1] if i + 1 < len(items) else return_to
        next_label = ('下一篇' if chinese else 'Next') if i + 1 < len(items) else ('继续主线' if chinese else 'Continue main sequence')
        nav = f'<nav class="series-navigation" aria-label="{nav_label}">' + article_link(previous, chinese, '上一篇' if chinese else 'Previous', title, 'prev') + article_link(following, chinese, next_label, title, 'next') + home + '</nav>'
    return guide, nav


def reading_rail(toc, chinese, rendered):
    if not useful_contents(toc, rendered):
        return ''
    label = '本文目录' if chinese else 'On this page'
    return f'<aside class="reading-rail"><nav class="reader-toc" aria-label="{label}"><p class="toc-title">{label}</p>{toc}</nav></aside>'


def write_essay(dist, path, page_title, rendered, toc, source_note, shell, title):
    destination = essay_url(path)
    if destination is None:
        return False
    chinese = path.endswith('.zh-CN.md')
    name = path[len(DOCS):].split('.')[0]
    counterpart = article_url(name, not chinese)
    art = article_figure(dist, name, chinese)
    guide, navigation = reading_context(name, chinese, title)
    if chinese:
        rendered = re.sub(r'(<h1\b[^>]*>[^<：]+：)', r'\1<br>', rendered, count=1)
    rendered = rendered.replace('</h1>', '</h1>' + art + guide, 1)
    contents = book_contents(toc, chinese, rendered)
    layout = '' if contents else ' no-toc'
    body = f'<main id="main" class="wrap library-reader commentary philosophy-book{layout}">{book_navigation(name, chinese, title)}<article class="document">{rendered}</article>{contents}<div class="reading-end">{navigation}{source_note}</div></main>'
    page = shell(page_title, body, 'zh-CN' if chinese else 'en', '<meta name="robots" content="noindex, nofollow, noimageindex"><link rel="stylesheet" href="/article.css">')
    page = page.replace('href="/philosophy/">哲学评论', 'href="/philosophy/" aria-current="page">哲学评论').replace('href="/repositories/" aria-current="page"', 'href="/repositories/"')
    page = page.replace('</nav></header>', f'<a class="language-link" lang="{"en" if chinese else "zh-CN"}" href="{counterpart}">{"English" if chinese else "中文"}</a></nav></header>', 1)
    target = dist / destination.lstrip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page)
    return True


def practice_entrance(chinese):
    suffix = '' if chinese else 'en/'
    views = '/philosophy/core-views/' + suffix
    guide = '/getting-started/' + suffix
    writing = '/philosophy/literary-programming/' + suffix
    if chinese:
        heading = '选择怎样阅读与使用'
        paragraphs = [
            f'非文史哲背景的读者，可以先从<a href="{views}">核心观点</a>中挑选与自己问题有关的部分，看看理由与适用条件，再考虑采用。需要深入理解时，再沿链接阅读相应论证，不必从头通读或接受全部立场。',
            f'选定的思想可以用于整理经历、持续修订个人心理材料，以及配置适合自己的环境。让模型协助整理记录、保留暂时解释与不确定性，并把相关理解落实到实际安排；<a href="{guide}">工具使用</a>提供操作入口。',
            f'是否写自己的哲学、文章或个人网站，取决于兴趣。可以先把观点用于生活与协作；有创作兴趣时，再读<a href="{writing}">文学式编程</a>等篇章。下面五部分展示作者的完整论述，供按问题选读。',
        ]
    else:
        heading = 'Choose what to read and use'
        paragraphs = [
            f'If literature, history, or philosophy is not your field, begin with relevant parts of <a href="{views}">Core views</a>. Consider their reasons and conditions before adopting them, and follow the linked arguments when you want to go deeper. You need not read everything in order or accept every position.',
            f'Selected ideas can help organize experiences, revise personal psychological material, and configure a fitting environment. A model can organize records, retain tentative interpretations and uncertainty, and turn relevant understanding into practical arrangements. <a href="{guide}">Using the Tools</a> supplies an operational entrance.',
            f'Writing your own philosophy, essays, or website is a choice of interest. Use the ideas in life and cooperation first if that serves you; explore <a href="{writing}">Literary programming</a> and related essays when you want to create. The five parts below present the author’s connected argument for selective reading.',
        ]
    return f'<section class="series-entrance" id="practice"><h2>{heading}</h2>' + ''.join(f'<p>{p}</p>' for p in paragraphs) + '</section>'


def index_body(chinese, title):
    name = SERIES_NAMES[0 if chinese else 1]
    thesis = '参加共同的窃火，用火培养自己的理解、判断与创造能力，成为能够继续生成的人。' if chinese else 'Join in the collective work of stealing fire, and use it to cultivate understanding, judgment, and creative capacity—to become someone who can keep generating.'
    heading = f'<header class="collection-heading"><img class="motif collection-motif" src="/motifs/sun.svg" alt="" aria-hidden="true"><h1>{name}</h1><p class="collection-intro">{thesis}</p></header>'
    notice = '用途边界：整理与修订个人材料、配置环境，不等于心理自助工作。阴阳不能用于心理自助、自行诊断、心理健康评估或治疗。' if chinese else 'Use boundary: organizing and revising personal material and configuring an environment are distinct from psychological self-help work. YinYang must not be used for psychological self-help, self-diagnosis, mental-health assessment, or treatment.'
    notice_url = 'https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/' + ('README.zh-CN.md#用途与心理健康说明' if chinese else 'README.md#intended-use-and-mental-health')
    use_notice = f'<p class="use-notice footnote" role="note">{notice} <a href="{notice_url}">{"完整说明" if chinese else "Full notice"}</a></p>'
    sections = []
    for index, (zh, en, entries) in enumerate(GROUPS):
        label = zh if chinese else en
        anchor = f'stage-{index + 1}'
        reason = STAGE_REASONS[index][0 if chinese else 1]
        sections.append(f'<section class="essay-entry stage-entry" id="{anchor}"><div class="essay-meta">{index + 1:02d}</div><div><h2><a href="{stage_entry(index, chinese)}">{html.escape(label)}</a></h2><p class="entry-summary">{html.escape(reason)}</p></div></section>')
    diagrams = [
        ('formation-path', '全书关系', 'The whole argument'),
        ('borrowed-fire', '窃火与培养', 'Fire and cultivation'),
        ('trinity-sinthome', '三位一体与圣状', 'Trinity and sinthome'),
        ('encounter', '共同探究', 'Shared inquiry'),
        ('layers', '理解与实现', 'Understanding and realization'),
    ]
    references = ' · '.join(f'<a href="/repositories/prometheus/diagrams/{slug}/{"" if chinese else "en/"}">{zh if chinese else en}</a>' for slug, zh, en in diagrams)
    review = f'<p class="diagram-references">{references}</p>'
    return f'<main id="main" class="wrap library-reader commentary philosophy-book book-introduction">{book_navigation("overview", chinese, title)}<article class="document">{heading}{practice_entrance(chinese)}{use_notice}{"".join(sections)}{review}</article></main>'


def old_book_alias(chinese):
    home = SERIES + ('' if chinese else 'en/')
    routes = {f'#stage-{i + 1}': stage_entry(i, chinese) for i in range(len(GROUPS))}
    links = ''.join(f'<li><a href="{stage_entry(i, chinese)}">{html.escape(group[0 if chinese else 1])}</a></li>' for i, group in enumerate(GROUPS))
    return f'<!doctype html><html lang="{"zh-CN" if chinese else "en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{SERIES_NAMES[0 if chinese else 1]} · boluopai</title><link rel="canonical" href="{home}"><script>const stages={json.dumps(routes)};location.replace(stages[location.hash]||{json.dumps(home)});</script></head><body><h1>{SERIES_NAMES[0 if chinese else 1]}</h1><p><a href="{home}">{"全书总览" if chinese else "Book overview"}</a></p><ul>{links}</ul></body></html>'


def write_index(dist, title):
    for chinese in (True, False):
        suffix = '' if chinese else 'en/'
        template = (dist / 'philosophy' / suffix / 'index.html').read_text()
        if 'src="/library.js"' not in template:
            template = template.replace('</head>', '<script defer src="/library.js"></script></head>')
        pages = [(SERIES + suffix, SERIES_NAMES[0 if chinese else 1], index_body(chinese, title))]
        for destination, heading, body in pages:
            page = re.sub(r'<main[\s\S]*?</main>', lambda _: body, template, count=1)
            page = re.sub(r'<title>[\s\S]*?</title>', f'<title>{html.escape(heading)} · boluopai</title>', page, count=1)
            description = '参加窃火，用火培养自己：连接个人理解、共同实践与持续创造的五部分。' if chinese else 'Join in stealing fire and use it to cultivate yourself: five parts connecting personal understanding, shared practice, and continued creation.'
            page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(heading + " — " + description)}">', page, count=1)
            if destination == SERIES + suffix:
                page = with_comments(page, not chinese, 'Philosophy')
            output = dist / destination.lstrip('/') / 'index.html'
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(page)
        for index in range(len(GROUPS)):
            stage_alias = dist / stage_url(index, chinese).lstrip('/') / 'index.html'
            stage_alias.parent.mkdir(parents=True, exist_ok=True)
            stage_alias.write_text(redirect_page(stage_entry(index, chinese)))
        alias = dist / 'philosophy/yinyang' / suffix / 'index.html'
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.write_text(old_book_alias(chinese))
