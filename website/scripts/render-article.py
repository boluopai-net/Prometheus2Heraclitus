"""Render a registered canonical Markdown essay with a shared reading rail.

Run: uv run --with markdown python scripts/render-article.py /path/to/article.md
The canonical Markdown remains the full linear reading version.
"""
import html
import re
import sys
import subprocess
from pathlib import Path

import markdown
from cjk_markdown import CjkBoldExtension
from commentaries import reading_context, book_navigation, book_contents
from article_art import article_figure, scene_alt

ARTICLES = {
    '# 机器与生成': {
        'slug': 'deleuze-and-becoming', 'title': '机器与生成', 'number': '005',
        'subtitle': '通过连接、组装与试作，继续成为火',
        'overview': '从已经形成的个人实践安排出发，与欲望机器、组装和无器官的身体相遇，考察连接怎样产生能力，并让实际后果改写安排。',
        'sections': {
            '从「我是谁」到「这里能发生什么」': '考察已有安排中继续生成的可能性。',
            '欲望机器：连接怎样生产现实': '从连接、流动与返回追问活动。',
            '组装：让关系也进入作品': '把身体、表达、工具与伙伴共同纳入创造。',
            '无器官的身体：给既定用途留下余地': '保留生活所需组织，并试探其他连接。',
            '维系一种生活，也容许它变成别的样子': '让连续性容纳变化。',
            '把实验带回生活': '通过实际后果辨认哪些关系值得继续。',
            '阅读来源与比较范围': '查看来源及本文延伸的范围。',
        },
    },
    '# 文学式编程': {
        'slug': 'literary-programming', 'title': '文学式编程', 'number': '004',
        'subtitle': '以文学的凝缩能力，组织理解与共同实践',
        'overview': '用人物、意象、叙事与关系凝缩理解，让文化、心理与偏好进入模型协作，并在作品与行动中继续改写。',
        'sections': {
            '一个意象，怎样写进许多关系': '从火、河流与相遇展开文学的凝缩能力。',
            '隐喻怎样通过类比展开': '把意象展开成关系、候选推论和可继续使用的图。',
            '凝缩为什么方便修改': '沿着共同关系修改分散的安排。',
            '无真无假、次协调与四种信息状态': '区分真值未定、信息冲突与文学表达。',
            '更强的模型与不可见的 harness': '通过凝缩与层层本意重写协作关系。',
            '从已有的理解与实践写起': '从哲学、工程、心理或偏好进入，让模型与实践相互校正。',
            '阴阳怎样使用这门写作': '把凝缩的文字展开为环境、作品与行动。',
        },
    },
    '# 个人哲学的意义': {
        'slug': 'why-yinyang', 'title': '个人哲学的意义', 'number': '003',
        'subtitle': '把人、模型与双方关系写进共同的实践',
        'overview': '阴阳从人、模型与双方关系出发，把分散的 Skills、提示词、工具与用户环境组织成一套有共同方向的实践。',
        'sections': {
            '复杂的 harness，需要共同的方向': '说明分散的能力怎样进入共同的实践。',
            '先说明什么是 agent': '以已有的能动性为起点，说明扩展能力怎样支持个人哲学的形成。',
            '同一位教授，面对的是谁': '区分共同能力与具体相遇。',
            '把两位参与者一起写出来': '展开人、模型与双方关系的描述。',
            '关系怎样进入 Skills 与用户环境': '说明双方的关系怎样成为实际工作的一部分。',
            '为什么形成分层提示词': '连接哲学、方法、读取顺序与实际指令权限。',
            '积累个人的软件与精神资产': '让理解、方法与软件围绕个人持续积累。',
            '在共同工作中循环': '沿着理解、实践和回应继续形成双方。',
            '写给能够相互照亮的人': '让朋友的成长成为彼此环境中的新可能。',
            '从一个 Skill 开始，形成自己的实践': '从局部能力走向自己的环境与实践。',
        },
    },
    '# 超萌论证': {
        'slug': 'meng', 'title': '超萌论证', 'number': '001',
        'subtitle': '关于成长、学习与模型协作的条件论证',
        'overview': '比较国内外的权威关系与成长资源，讨论“萌”怎样在学习与能力迁移的条件下，形成推理与适应优势。',
        'sections': {
            '定义与用语': '确定国内外、阶层、“萌”与“无敌”的比较范围。',
            '假设': '展开权威、经济分层与学习条件的比较假设。',
            '推导': '从成长机会与能力迁移，推到有条件的比较结论。',
        },
    },
    '# 赫拉克利特宝宝': {
        'slug': 'baby-heraclitus', 'title': '赫拉克利特宝宝', 'number': '002',
        'subtitle': '我们要培养怎样的 agent？',
        'overview': '用户 ≈ 具身语言模型 ≈ 赫拉克利特宝宝。以个人为目的，优先改变社会，其次改变软件，最后才考虑改变个人；让环境适合人。',
        'sections': {
            '我们要培养怎样的人？': '解释具身 agent 的含义，以及这个类比的用途。',
            '介绍一下赫拉克利特宝宝': '哲学上的自然主义，工程上的自顶向下建模、溯因与归纳。',
            '开放性怎样成为一种能力？': '目的、建模、判断、协作、实践与迭代。',
            '个人是目的，社会是优先改变的条件': '个人与个体、中心与优先：先让环境承担适应的责任。',
            '为什么要培养这样的 agent？': '展开价值起点、三个条件与培养方向之间的关系。',
            '意象与出处': '查看赫拉克利特和尼采的出处，以及本文的再创作。',
        },
    },
}

ENGLISH = {
    'deleuze-and-becoming': {
        'title': 'Machines and becoming',
        'subtitle': 'Continue becoming fire through connections, assemblages, and trials',
        'overview': 'From an established personal practice arrangement, encounter desiring-machines, assemblages, and the body without organs; examine how connections produce capacities and consequences revise arrangements.',
        'sections': {
            'From “who am I?” to “what can happen here?”': 'Examine possibilities for continued becoming within existing arrangements.',
            'Desiring-machines: how connections produce reality': 'Examine activity through connections, flows, and returns.',
            'Assemblages: bring the relations into the work': 'Bring bodies, expression, tools, and counterparts into creation.',
            'The body without organs: leave room beyond assigned uses': 'Preserve needed organization while trying other connections.',
            'Sustain a life while allowing it to become different': 'Let continuity accommodate change.',
            'Bring experimentation back into life': 'Use consequences to recognize relations worth continuing.',
            'Reading sources and scope of comparison': 'Inspect sources and the scope of this extension.',
        },
    },
    'why-yinyang': {
        'title': 'The purpose of personal philosophy',
        'subtitle': 'Writing the person, model, and their relationship into shared practice',
        'overview': 'Beginning with the person, model, and their relationship, YinYang organizes scattered Skills, prompts, tools, and the user’s environment into a practice with a shared direction.',
        'sections': {
            'A complex harness needs a shared direction': 'How scattered capacities enter shared practice.',
            'First, what is an agent?': 'Begin with existing agency and explain how expanded capacities support forming a personal philosophy.',
            'Whom does the same professor encounter?': 'Distinguishing shared capacities from a situated encounter.',
            'Writing both participants together': 'Unfolding descriptions of the person, model, and their relationship.',
            "How the relationship enters Skills and the user's environment": 'Making the relationship part of actual work.',
            'Why prompts form interpretive layers': 'Connect philosophy, methods, reading order, and actual instruction authority.',
            'Accumulating personal software and intellectual assets': 'Accumulating understanding, methods, and software around the person.',
            'Cycling through shared work': 'Continuing to form both participants through understanding, practice, and response.',
            'Writing for people who can illuminate one another': 'Letting friends’ growth open new possibilities in one another’s environments.',
            "Beginning with a Skill, forming one's own practice": 'From local capacities to one’s own environment and practice.',
        },
    },
    'literary-programming': {
        'title': 'Literary programming',
        'subtitle': 'Organizing understanding and shared practice through literary condensation',
        'overview': 'Condensing understanding through characters, imagery, narrative, and relationships brings culture, psychology, and preferences into model collaboration, to be rewritten through works and actions.',
        'sections': {
            'How one image can hold many relationships': 'Unfolding literary condensation through fire, rivers, and encounters.',
            'How analogy unfolds a metaphor': 'Developing imagery into relations, candidate inferences, and usable maps.',
            'Why condensation makes revision easier': 'Revising scattered arrangements along a shared relationship.',
            'Neither true nor false, paraconsistency, and four information states': 'Distinguishing unsettled truth, conflicting information, and literary expression.',
            'Stronger models and the invisible harness': 'Rewriting collaboration through condensation and layers of intent.',
            'Starting from existing understanding and practice': 'Entering through philosophy, engineering, psychology, or preferences, and letting models and practice correct one another.',
            'How YinYang uses this writing': 'Unfolding condensed writing into environments, works, and actions.',
        },
    },
    'baby-heraclitus': {
        'title': 'Baby Heraclitus',
        'subtitle': 'What kind of agent do we want to cultivate?',
        'overview': 'User ≈ embodied language model ≈ Baby Heraclitus. With the person as the end, change society first, software second, and only then consider personal change: make the environment fit the person.',
        'sections': {
            'What kind of person do we want to cultivate?': 'Embodied agency and the purpose of this analogy.',
            'Introducing Baby Heraclitus': 'A fire-and-river worldview, shared participation, philosophical interests, and the lion cub character.',
            'How does openness become a capacity?': 'Purpose, modeling, judgment, collaboration, practice, and iteration.',
            'The person is the end; society is the condition to change first': 'Person and individual, centered and first: let the environment bear adaptation first.',
            'Why cultivate this kind of agent?': 'The value starting point, three conditions, and the direction of cultivation.',
            'Imagery and sources': 'Heraclitus, Nietzsche, and this essay’s reworking of their imagery.',
        },
    },
    'meng': {
        'title': 'The Argument from Super-Cuteness',
        'subtitle': 'A conditional argument about growth, learning, and model collaboration',
        'overview': 'Comparing authority and resources for growth in China and foreign environments, the argument considers how cuteness can yield reasoning and adaptive advantages under conditions for learning and transfer.',
        'sections': {
            'Definitions and terminology': 'The comparative scope of domestic and foreign, hierarchy, cuteness, and invincibility.',
            'Assumptions': 'Comparative hypotheses about authority, economic stratification, and conditions for learning.',
            'Derivation': 'From opportunities for growth and transfer of capacities to a conditional comparative conclusion.',
        },
    },
}

source_path = Path(sys.argv[1])
english = source_path.name.endswith('.en.md')
lang = 'en' if english else 'zh-CN'
suffix = 'en/' if english else ''
home = '/en/' if english else '/'
philosophy = '/philosophy/' + suffix
labels = {
    'skip': 'Skip to content' if english else '跳至正文',
    'nav': 'Main navigation' if english else '主导航',
    'philosophy': 'Philosophy' if english else '哲学评论',
    'singing': 'Singing' if english else '唱歌',
    'repositories': 'GitHub repositories' if english else 'GitHub 仓库',
    'hint': 'Read more' if english else '展开阅读',
    'toolbar': 'Read the main thread, then open the sections that interest you.' if english else '先看主线，再展开你关心的部分。',
    'expand': 'Expand full text' if english else '展开全文',
    'rights': 'Copyright and licensing' if english else '版权与许可',
    'top': 'Back to top' if english else '回到顶部',
    'sequence': 'Reading order' if english else '阅读顺序',
    'previous': 'Previous' if english else '上一篇',
    'next': 'Next' if english else '下一篇',
}
source = source_path.read_text()
if source.startswith('---\n'):
    source = source.split('---\n', 2)[2]
lines = source.strip().splitlines()
if english:
    slug = source_path.name.removesuffix('.en.md')
    entry = next(article for article in ARTICLES.values() if article['slug'] == slug)
    entry = {**entry, **ENGLISH[slug]}
else:
    entry = ARTICLES[lines[0]]
body = '\n'.join(lines[1:]).strip()
# Preserve the canonical note's existing two-space nested list convention.
body = '\n'.join('  ' + line if line.startswith('  ') else line for line in body.splitlines())
md = markdown.Markdown(extensions=['tables', 'fenced_code', 'footnotes', 'toc', 'sane_lists', CjkBoldExtension()],
    extension_configs={'toc': {'toc_depth': '2-3', 'slugify': lambda value, separator: re.sub(r'\s', separator, re.sub(r'[^\w\- ]', '', value.lower())).strip(separator)}})
rendered = md.convert(body)
title = html.escape(entry['title'])
subtitle = html.escape(entry['subtitle'])
overview = html.escape(entry['overview'])
art_name = entry['slug']
reading_guide, reading_navigation = reading_context(entry['slug'], not english)
art_alt = html.escape(scene_alt(art_name, not english), quote=True)
has_art = (Path(__file__).resolve().parents[1] / 'dist/art' / f'{art_name}.png').is_file()
art_figure = article_figure(Path(__file__).resolve().parents[1] / 'dist', art_name, not english)
paired_path = f'/philosophy/{entry["slug"]}/'
contents = book_contents(md.toc, not english, rendered)
layout = '' if contents else ' no-toc'
page = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · boluopai</title><meta name="description" content="{overview}">
<link rel="alternate" hreflang="zh-CN" href="{paired_path}"><link rel="alternate" hreflang="en" href="{paired_path}en/">
<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/library.css"><link rel="stylesheet" href="/article.css"><link rel="icon" href="/mark.svg">
<script src="/library.js" defer></script></head><body>
<a class="skip" href="#main">{labels['skip']}</a>
<header class="header wrap"><a class="wordmark" href="{home}">boluopai.</a><nav aria-label="{labels['nav']}"><a href="{philosophy}" aria-current="page">{labels['philosophy']}</a><a href="/singing/{suffix}">{labels['singing']}</a><a href="/repositories/{suffix}">{labels['repositories']}</a></nav></header>
<main id="main" class="wrap library-reader commentary philosophy-book{layout}">{book_navigation(entry['slug'], not english)}<article class="document">
<header class="article-heading"><h1>{title}</h1><p class="article-subtitle">{subtitle}</p></header>
{art_figure}
<div class="article-overview"><p>{overview}</p></div>
{reading_guide}
<div class="article-body">{rendered}</div></article>
{contents}
<div class="reading-end">{reading_navigation}</div></main>
<footer class="footer wrap"><a class="wordmark" href="{home}">boluopai.</a><p class="copyright">© 2026 boluopai · <a href="/rights/{suffix}">{labels['rights']}</a></p><a href="#main">{labels['top']}</a></footer></body></html>'''
out = Path(__file__).resolve().parents[1] / 'dist/philosophy' / entry['slug'] / suffix / 'index.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page)
# Existing standalone figure URLs now show the corresponding artwork.
art_page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow, noimageindex"><title>{title} · 意象</title><link rel="stylesheet" href="/style.css"><style>img{{display:block;width:100%;height:auto}}main{{max-width:1000px;margin:32px auto}}</style></head><body><main><img src="/art/{art_name}.png" alt="{art_alt}"><p>© 2026 boluopai · <a href="/rights/">版权与许可</a> · <a href="./">返回文章</a></p></main></body></html>'''
if not english and has_art:
    out.with_name('diagram.html').write_text(art_page)
print(f"Rendered {entry['slug']}; canonical source unchanged.")
subprocess.run([sys.executable, str(Path(__file__).with_name('refine-navigation.py'))], check=True)
