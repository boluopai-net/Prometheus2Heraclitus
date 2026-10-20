#!/usr/bin/env python3
"""Render the two responsive reading maps from their bilingual authored source."""
import html
import json
import re
import argparse
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[1]
SITE_SOURCE = REPO / 'website'
DIAGRAMS = PACKAGE / 'references/diagrams'
SITE_ARTICLES = {'why-yinyang', 'meng', 'baby-heraclitus', 'literary-programming', 'deleuze-and-becoming'}
H = html.escape

CSS = """
:root{color-scheme:light;--paper:#fff;--ink:#292d31;--muted:#626f73;--line:#d8e3e1;--water:#245f64;--surface:#f4f8f7;--fire:#a54827;--warm:#fff6ee;font-family:"Hiragino Sans GB","PingFang SC","Microsoft YaHei",system-ui,sans-serif}
@media(prefers-color-scheme:dark){:root{color-scheme:dark;--paper:#171e20;--ink:#e5eceb;--muted:#abb9b8;--line:#465b5d;--water:#9bd6d0;--surface:#222e30;--fire:#f3ad8a;--warm:#332820}}
:root[data-theme=light]{color-scheme:light;--paper:#fff;--ink:#292d31;--muted:#626f73;--line:#d8e3e1;--water:#245f64;--surface:#f4f8f7;--fire:#a54827;--warm:#fff6ee}
:root[data-theme=dark]{color-scheme:dark;--paper:#171e20;--ink:#e5eceb;--muted:#abb9b8;--line:#465b5d;--water:#9bd6d0;--surface:#222e30;--fire:#f3ad8a;--warm:#332820}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);line-height:1.7}
main{max-width:1280px;margin:auto;padding:32px 24px}h1{font-size:clamp(26px,3.2vw,40px);line-height:1.4;margin:0 0 16px;letter-spacing:.02em}
h2,h3,p{margin:0}a{color:var(--water);text-decoration:none}a:hover{text-decoration:underline;text-underline-offset:4px}
.embedded header{display:none}.embedded main{padding:12px 0}.embedded .premises{margin-top:0}
:is(a,button,summary):focus-visible{outline:2px solid var(--water);outline-offset:4px}header>p{color:var(--muted);max-width:840px}
.eyebrow{font-size:13px;color:var(--fire);margin-bottom:12px;letter-spacing:.08em}
.premises{display:grid;grid-template-columns:1fr 1.25fr;gap:28px;margin:28px 0;padding-block:20px;border-block:1px solid var(--line)}
.premises h2,.outcomes h2{font-size:16px;margin-bottom:8px}.premises p,.outcomes p{font-size:14px;color:var(--muted)}
.flow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:28px 20px;margin-top:24px;align-items:start}
.stage{display:contents}.stage::details-content{display:contents}.stage:not([open])>.stage-detail{display:none}.stage summary{grid-column:var(--column);grid-row:1;list-style:none;cursor:pointer;position:relative;min-height:260px;padding:20px 16px 16px;border:1px solid var(--line);border-top:3px solid var(--water);border-radius:4px;background:var(--surface)}
.stage summary::-webkit-details-marker{display:none}.stage summary:hover,.stage[open] summary{border-color:var(--water)}
.stage summary{align-self:stretch}
.stage[open] summary{background:var(--paper)}.stage-number{display:block;font-size:13px;color:var(--fire);margin-bottom:12px}
.stage-title{display:block;font-size:18px;font-weight:600;line-height:1.5}.question{display:block;font-size:14px;margin-top:12px;color:var(--muted)}
.handoff{display:block;font-size:12px;line-height:1.7;color:var(--water);margin-top:18px}
.disclose{display:block;margin-top:16px;font-size:12px;color:var(--water)}.stage[open] .open-label,.stage:not([open]) .close-label{display:none}
.stage:not(:last-child) summary:after{content:"→";position:absolute;right:-18px;top:45%;color:var(--water);font-size:20px}
.stage-detail{grid-column:1/-1;padding:24px 28px;border-left:3px solid var(--water);background:var(--surface)}
.stage-detail h2{font-size:22px;line-height:1.5;margin-bottom:12px}.stage-detail>p{font-size:16px;max-width:920px}
.reading-list{display:grid;grid-template-columns:1fr 1fr;gap:10px 28px;padding-left:24px;margin:20px 0 0}.reading-list a{font-size:15px;display:inline-block;padding:5px 0}
.related{font-size:14px;margin-top:20px}.return{margin-top:32px;padding:22px 24px;border:1px solid var(--line);border-left:3px solid var(--fire);background:var(--warm)}
.return h2{font-size:16px;color:var(--fire);margin-bottom:8px}.return .route{font-size:18px;line-height:1.8}.return .note{font-size:14px;color:var(--muted);margin-top:12px}
.outcomes{margin-top:28px;display:grid;grid-template-columns:1fr 1.15fr;gap:24px}.outcomes section{padding:20px 24px;border-block:1px solid var(--line)}
.outcomes section:last-child{border-color:var(--fire)}footer{margin-top:28px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted)}
.motif{width:54px;height:34px;vertical-align:middle;margin-right:12px;color:var(--fire)}
@media(max-width:760px){main{padding:24px 16px}.premises{grid-template-columns:1fr;gap:20px}.flow{display:block}.stage{display:block;margin-bottom:28px}.stage summary{min-height:0;padding:16px 18px}.stage-title{font-size:19px}.stage-number{margin-bottom:6px}.question{margin-top:8px}.handoff{margin-top:10px}.disclose{margin-top:10px}.stage:not(:last-child) summary:after{content:"↓";right:22px;top:auto;bottom:-28px}.stage[open]:not(:last-child) summary:after{display:none}.stage-detail{margin-top:12px;padding:20px}.reading-list{grid-template-columns:1fr;gap:6px}.outcomes{grid-template-columns:1fr;gap:12px}.return{padding:20px}.return .route{font-size:16px}}
@media print{.stage{display:contents}.stage-detail{display:block!important}.disclose{display:none}a{color:inherit}main{max-width:none}body{background:white;color:black}}
"""

JS = """
if(new URLSearchParams(location.search).has('embed'))document.documentElement.classList.add('embedded');
const stages=[...document.querySelectorAll('.stage')];
stages.forEach(s=>s.addEventListener('toggle',()=>{if(s.open)stages.forEach(other=>{if(other!==s)other.open=false});}));
const notify=()=>{if(parent!==window)parent.postMessage({type:'reading-map-size',height:Math.ceil(document.documentElement.getBoundingClientRect().height)},'*');};
new ResizeObserver(notify).observe(document.querySelector('main'));
addEventListener('message',e=>{if(e.source!==parent||e.data?.type!=='reading-map-theme')return;if(['light','dark'].includes(e.data.theme))document.documentElement.dataset.theme=e.data.theme;});
addEventListener('load',notify);
"""


def article_title(slug, lang):
    if slug in SITE_ARTICLES:
        path = SITE_SOURCE / 'content/philosophy' / (slug + ('.md' if lang == 0 else '.en.md'))
    else:
        path = PACKAGE / 'references/docs' / (slug + ('.zh-CN.md' if lang == 0 else '.md'))
    return re.search(r'^# (.+)$', path.read_text(), re.M)[1]


def article_url(slug, lang):
    return f'https://boluopai.net/philosophy/{slug}/' + ('en/' if lang else '')


def diagram_url(slug, lang):
    return f'https://boluopai.net/repositories/prometheus/diagrams/{slug}/' + ('en/' if lang else '')


def svg(name, data, lang):
    """A deliberately sparse overview for the library card, not a shrunken screenshot."""
    labels = (['方向', '轨迹', '反思', '形成', '创造'] if lang == 0 else
              ['Purpose', 'Trajectory', 'Reflection', 'Formation', 'Creation']) if name == 'formation-path' else (
              ['共同窃火', '带火入生活', '共同生成', '能力发展', '继续生火'] if lang == 0 else
              ['Join', 'Apply', 'Participate', 'Develop', 'Create'])
    nodes = []
    for i, label in enumerate(labels):
        x = 36 + i * 176
        if i < 4:
            nodes.append(f'<path d="M{x+140} 104h32" stroke="#245f64" stroke-width="2" marker-end="url(#{name}-arrow)" fill="none"/>')
        nodes.append(f'<rect x="{x}" y="60" width="140" height="88" rx="4" fill="#f4f8f7" stroke="#bfd2ce"/><text x="{x+70}" y="88" text-anchor="middle" fill="#a54827" font-size="13">0{i+1}</text><text x="{x+70}" y="121" text-anchor="middle" fill="#245f64" font-size="18">{H(label)}</text>')
    back = '新经验返回理解，继续改变实践' if lang == 0 else 'New experience returns to understanding and practice'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{name}-title {name}-desc" viewBox="0 0 920 244"><title id="{name}-title">{H(data['title'][lang])}</title><desc id="{name}-desc">{H(data['return'][lang])}</desc><defs><marker id="{name}-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#245f64"/></marker></defs><rect width="920" height="244" fill="#fff"/><g font-family="system-ui,sans-serif">{''.join(nodes)}<path d="M810 164v32H284v-32" stroke="#a54827" fill="none" stroke-width="1.5" stroke-dasharray="5 4"/><rect x="320" y="181" width="450" height="29" fill="#fff"/><text x="545" y="202" fill="#a54827" text-anchor="middle" font-size="16">{back}</text></g></svg>'''


def render(name, data, lang):
    suffix = '.zh-CN' if lang == 0 else ''
    title = data['title'][lang]
    premise = ''.join(f'<section><h2>{H(p[lang])}</h2><p>{H(p[lang+2])}</p></section>' for p in data['premises'])
    stages = []
    for i, s in enumerate(data['stages']):
        links = ''.join(f'<li><a target="_top" href="{article_url(n, lang)}">{H(article_title(n, lang))}</a></li>' for n in s['essays'])
        related = ''
        for n in s.get('related', []):
            label = {'encounter': ['人与模型怎样共同探究', 'How people and models inquire together'],
                     'layers': ['从世界理解到实践实现', 'From understanding the world to realizing a practice']}[n][lang]
            related += f'<p class="related"><a target="_top" href="{diagram_url(n, lang)}">{H(label)} ↗</a></p>'
        opening = (f'展开 · {len(s["essays"])} 篇文章' if lang == 0 else f'Explore · {len(s["essays"])} essays')
        close = '收起' if lang == 0 else 'Collapse'
        stages.append(f'''<details class="stage" id="part-{i+1}" style="--column:{i+1}"><summary><span class="stage-number">0{i+1}</span><span class="stage-title">{H(s['title'][lang])}</span><span class="question">{H(s['question'][lang])}</span><span class="handoff">{H(s['handoff'][lang])}</span><span class="disclose"><span class="open-label">{opening} ＋</span><span class="close-label">{close} −</span></span></summary><section class="stage-detail"><h2>{H(s['title'][lang])}</h2><p>{H(s['detail'][lang])}</p><ol class="reading-list">{links}</ol>{related}</section></details>''')
    outcomes = ''
    if 'outcomes' in data:
        outcomes = '<div class="outcomes">' + ''.join(f'<section><h2>{H(p[lang])}</h2><p>{H(p[lang+2])}</p></section>' for p in data['outcomes']) + '</div>'
    companion = 'borrowed-fire' if name == 'formation-path' else 'formation-path'
    companion_label = ['窃火与个人发展的论证', 'The argument for borrowed fire and personal development'] if name == 'formation-path' else ['五部分与十八篇文章的路径', 'Five parts and eighteen essays']
    eyebrow = ['全书路径 · 18 篇', 'READING PATH · 18 ESSAYS'] if name == 'formation-path' else ['窃火 · 培养 · 再创造', 'STEAL FIRE · CULTIVATE · CREATE']
    back_label = (['从新的经验重新出发', 'Return through new experience'] if name == 'formation-path' else ['造物返回，改变造物者', 'Creation changes the creator'])[lang]
    body = f'''<main><header><p class="eyebrow">{eyebrow[lang]}</p><h1>{H(title)}</h1><p>{H(data['intro'][lang])}</p></header><div class="premises">{premise}</div><div class="flow">{''.join(stages)}</div>{outcomes}<aside class="return"><h2>{back_label}</h2><p class="route">{H(data['return'][lang])}</p><p class="note">{H(data['return_note'][lang])}</p></aside><footer><a target="_top" href="{diagram_url(companion,lang)}">{companion_label[lang]} ↗</a><span>YinYang · CC BY-NC-SA 4.0</span></footer></main>'''
    return f'<!doctype html><html lang="{"zh-CN" if lang == 0 else "en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow, noimageindex"><title>{H(title)}</title><style>{CSS}</style></head><body>{body}<script>{JS}</script></body></html>'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-source', type=Path, default=SITE_SOURCE,
                        help='Native Site checkout when editing its article titles before snapshot synchronization.')
    SITE_SOURCE = parser.parse_args().site_source
    data = json.loads((DIAGRAMS / 'reading-maps.json').read_text())
    for name, item in data.items():
        for lang, suffix in [(0, '.zh-CN'), (1, '')]:
            (DIAGRAMS / (name + suffix + '.html')).write_text(render(name, item, lang))
            (DIAGRAMS / (name + suffix + '.svg')).write_text(svg(name, item, lang))
    print('Rendered two bilingual responsive reading maps and their overview previews.')
