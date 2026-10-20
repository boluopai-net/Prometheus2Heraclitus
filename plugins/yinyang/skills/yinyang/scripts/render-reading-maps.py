#!/usr/bin/env python3
"""Render two concise bilingual concept diagrams, with no article index or controls."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'references/diagrams'
H = html.escape
STYLE = '''
:root{--paper:#fff;--ink:#293537;--muted:#657575;--line:#698b89;--water:#245f64;--pale:#edf5f3;--fire:#a54d2c;--warm:#fff3e8;color-scheme:light}
@media(prefers-color-scheme:dark){:root{--paper:#171e20;--ink:#e5eceb;--muted:#abb9b8;--line:#80a9a3;--water:#a1d8d0;--pale:#233a38;--fire:#edb18e;--warm:#3e2d25;color-scheme:dark}}
:root[data-theme=light]{--paper:#fff;--ink:#293537;--muted:#657575;--line:#698b89;--water:#245f64;--pale:#edf5f3;--fire:#a54d2c;--warm:#fff3e8;color-scheme:light}
:root[data-theme=dark]{--paper:#171e20;--ink:#e5eceb;--muted:#abb9b8;--line:#80a9a3;--water:#a1d8d0;--pale:#233a38;--fire:#edb18e;--warm:#3e2d25;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif}
main{max-width:1100px;margin:auto;padding:24px 12px}h1{font-size:clamp(26px,3.4vw,40px);line-height:1.4;margin:0 0 20px;text-align:center;font-weight:500}
svg{display:block;width:100%;height:auto;overflow:visible;font-family:inherit}svg text{font-family:inherit}.desktop svg{max-height:740px}.mobile{display:none}.embedded h1{display:none}.embedded main{padding:0}
@media(max-width:700px){.desktop{display:none}.mobile{display:block}main{padding:20px 0}h1{padding-inline:16px}}
'''


def text(x, y, lines, size=26, color='ink', weight=400):
    if isinstance(lines, str): lines = [lines]
    start = y - (len(lines)-1)*size*0.68
    spans = ''.join(f'<tspan x="{x}" y="{start+i*size*1.36:.1f}">{H(s)}</tspan>' for i,s in enumerate(lines))
    return f'<text text-anchor="middle" dominant-baseline="middle" fill="var(--{color})" font-size="{size}" font-weight="{weight}">{spans}</text>'


def label(x, y, value, size=20, color='muted'):
    units = sum(1 if ord(c)>255 else .54 for c in value)
    w = max(36, units*size+20)
    return f'<rect x="{x-w/2:.1f}" y="{y-size*.68:.1f}" width="{w:.1f}" height="{size*1.36:.1f}" rx="5" fill="var(--paper)"/>'+text(x,y,value,size,color)


def edge(path, prefix, color='water', dashed=False):
    return f'<path d="{path}" fill="none" stroke="var(--{color})" stroke-width="2.3" '+('stroke-dasharray="6 7" ' if dashed else '')+f'marker-end="url(#{prefix}-{color})"/>'


def circle(x,y,r,fill='pale',stroke='line'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--{fill})" stroke="var(--{stroke})" stroke-width="1.3"/>'


def flame(x,y,scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})"><path d="M0 24C-35 12-32-14-13-34C-9-11 5-17 3-52C42-15 41 15 12 24C20 5 8-2 3-13C2 4-9 7 0 24Z" fill="var(--fire)" opacity=".16"/><path d="M0 24C-35 12-32-14-13-34C-9-11 5-17 3-52C42-15 41 15 12 24" fill="none" stroke="var(--fire)" stroke-width="1.8"/></g>'


def formation(d,lang,mobile,p):
    w,h = (600,880) if mobile else (800,770)
    cx,cy = (300,430) if mobile else (400,390)
    lx,rx,ty,by = (125,475,245,660) if mobile else (165,635,260,575)
    r = 92 if mobile else 106
    cr = 78 if mobile else 92
    nodes=d['nodes']; e={k:v[lang] for k,v in d['edges'].items()}
    paths=[]; labels=[]
    paths.append(edge(f'M{cx-cr*.86} {cy-cr*.48} Q{lx+r+35} {ty+55} {lx+r*.94} {ty+r*.34}',p))
    labels.append(label(270 if mobile else 305,310 if mobile else 295,e['record'],18))
    paths.append(edge(f'M{lx+r} {ty} H{rx-r}',p));labels.append(label(cx,ty-23,e['reflect']))
    paths.append(edge(f'M{rx} {ty+r} V{by-r}',p));labels.append(label(rx+48,(ty+by)/2,e['articulate'],17 if lang else 19))
    paths.append(edge(f'M{rx-r} {by} H{lx+r}',p));labels.append(label(cx,by+27,e['realize']))
    paths.append(edge(f'M{lx+r*.8} {by-r*.6} Q{cx-cr-20} {cy+70} {cx-cr*.85} {cy+cr*.52}',p));labels.append(label((lx+cx)/2+2,(by+cy)/2+12,e['use'],18))
    paths.append(edge(f'M{rx-r*.8} {ty+r*.6} Q{cx+cr+28} {cy-58} {cx+cr*.85} {cy-cr*.52}',p,'fire',True));labels.append(label(440 if mobile else 555,380,e['revise'],17 if lang else 19,'fire'))
    paths.append(edge(f'M{lx} {by-r} V{ty+r}',p,'fire',True));labels.append(label(lx-49,(ty+by)/2,e['experience'],17 if lang else 19,'fire'))
    drawn = ''.join(paths)
    for n,x,y in [('trajectory',lx,ty),('reflection',rx,ty),('formation',rx,by),('practice',lx,by)]:
        drawn+=circle(x,y,r)
        drawn+=text(x,y-r+28,d['tags'][n][lang],14 if lang else 18,'muted')
        size=20 if lang and n in ['formation','practice'] else 24 if mobile else 26
        drawn+=text(x,y+10,nodes[n][lang],size,'water',500)
    drawn+=circle(cx,cy,cr,'paper','water')+text(cx,cy,nodes['center'][lang],22 if lang or mobile else 27,'ink',500)
    drawn+=''.join(labels)
    drawn+=text(w/2,25,'起点' if not lang else 'STARTING POINT',18,'muted')
    drawn+=text(w/2,80 if lang else 72,d['purpose'][lang],24 if mobile else 28,'fire',500)
    note = ['New experience can also change', 'the original developmental aim.'] if mobile and lang else d['note'][lang]
    drawn+=text(w/2,h-36,note,20 if mobile and lang else 17 if lang else 21,'muted')
    return w,h,drawn


def cultivation(d,lang,mobile,p):
    w,h=(600,1010) if mobile else (1000,790)
    e={k:v[lang] for k,v in d['edges'].items()};n=d['nodes']
    if mobile:
        ax,ay,ar=300,150,100; cx,cy=300,425; bx,by,br=450,785,103; wx,wy=150,785
        paths=[edge('M300 250V315',p),edge('M440 485C500 540 500 610 480 687',p,'fire',True),edge('M410 690C365 607 365 590 340 533',p),edge('M225 524C205 585 190 655 175 710',p),edge('M100 717C45 625 65 500 132 467',p),edge('M276 785H347',p,'fire',True)]
        labs=[label(340,281,e['use']),label(501,591,e['cultivate'],18 if lang else 21,'fire'),label(352,622,e['continue'],17 if lang else 20),label(233,650,e['make']),label(102,592,e['response'],16 if lang else 20),label(312,758,e['support'],17 if lang else 20,'fire')]
        worksrx,worksry=126,75
    else:
        ax,ay,ar=150,290,112;cx,cy=500,290;bx,by,br=850,290,112;wx,wy=500,570
        paths=[edge('M262 290H325',p),edge('M675 290H738',p,'fire',True),edge('M850 178C850 85 500 85 500 180',p),edge('M500 400V492',p),edge('M342 550C285 530 280 390 350 346',p),edge('M664 584C850 584 850 500 850 402',p,'fire',True)]
        labs=[label(294,264,e['use']),label(706,264,e['cultivate'],18 if lang else 21,'fire'),label(675,102,e['continue'],20),label(542,447,e['make']),label(287,456,e['response'],18 if lang else 20),label(844,505,e['support'],20,'fire')]
        worksrx,worksry=170,78
    drawn=''.join(paths)
    drawn+=circle(ax,ay,ar,'warm','fire')+flame(ax,ay-35,.9)
    drawn+=text(ax,ay+36,n['collective'][lang],24 if lang else 28,'fire',500)
    drawn+=f'<ellipse cx="{cx}" cy="{cy}" rx="175" ry="110" fill="var(--pale)" stroke="var(--line)" stroke-width="1.3"/>'
    drawn+=circle(cx-65,cy-25,43,'paper')+circle(cx+65,cy-25,43,'paper')
    drawn+=text(cx-65,cy-25,n['person'][lang],19 if lang else 25,'water',500)+text(cx+65,cy-25,n['model'][lang],19 if lang else 25,'water',500)
    drawn+=edge(f'M{cx-20} {cy-41} Q{cx} {cy-59} {cx+20} {cy-41}',p)+edge(f'M{cx+20} {cy-9} Q{cx} {cy+9} {cx-20} {cy-9}',p)
    drawn+=text(cx,cy+56,n['creation'][lang],25,'water',500)
    drawn+=circle(bx,by,br,'warm','fire')+text(bx,by,n['capacity'][lang],20 if lang else 25,'fire',500)
    drawn+=f'<ellipse cx="{wx}" cy="{wy}" rx="{worksrx}" ry="{worksry}" fill="var(--pale)" stroke="var(--line)" stroke-width="1.3"/>'
    drawn+=text(wx,wy,n['works'][lang],20 if lang else 27,'water',500)
    drawn+=''.join(labs)
    note = ['Accumulated works are not the same', 'as personal development.'] if mobile and lang else d['note'][lang]
    drawn+=text(w/2,h-86,note,22 if lang else 25,'ink',500)
    legend = '虚线表示培养或支持的关系，效果由实际参与检验。' if not lang else ['Dashed: cultivation or support;', 'examined through actual participation.'] if mobile else 'Dashed: cultivation or support, examined through actual participation.'
    drawn+=text(w/2,h-30,legend,18 if mobile or not lang else 16,'muted')
    return w,h,drawn


def svg(name,d,lang,mobile=False):
    p=name+('-mobile' if mobile else '-desktop')
    w,h,body=(formation if name=='formation-path' else cultivation)(d,lang,mobile,p)
    markers=''.join(f'<marker id="{p}-{c}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L8 4L0 8" fill="none" stroke="var(--{c})" stroke-width="1.5"/></marker>' for c in ['water','fire'])
    return f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{p}-title {p}-desc" viewBox="0 0 {w} {h}"><title id="{p}-title">{H(d["title"][lang])}</title><desc id="{p}-desc">{H(d["description"][lang])}</desc><style>{STYLE}</style><defs>{markers}</defs><rect width="{w}" height="{h}" fill="var(--paper)"/>{body}</svg>'


SCRIPT = '''if(new URLSearchParams(location.search).has('embed'))document.documentElement.classList.add('embedded');const tell=()=>{if(parent!==window)parent.postMessage({type:'reading-map-size',height:Math.ceil(document.querySelector('main').getBoundingClientRect().height)},'*')};new ResizeObserver(tell).observe(document.querySelector('main'));addEventListener('load',tell);addEventListener('message',e=>{if(e.source===parent&&e.data?.type==='reading-map-theme'&&['light','dark'].includes(e.data.theme))document.documentElement.dataset.theme=e.data.theme});'''


def render(name,d,lang):
    graphic=svg(name,d,lang);small=svg(name,d,lang,True)
    return f'<!doctype html><html lang="{"en" if lang else "zh-CN"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow, noimageindex"><title>{H(d["title"][lang])}</title><style>{STYLE}</style></head><body><main><h1>{H(d["title"][lang])}</h1><div class="desktop">{graphic}</div><div class="mobile">{small}</div></main><script>{SCRIPT}</script></body></html>',graphic


if __name__=='__main__':
    data=json.loads((ROOT/'reading-maps.json').read_text())
    for name,d in data.items():
        for lang,suffix in [(0,'.zh-CN'),(1,'')]:
            page,graphic=render(name,d,lang)
            (ROOT/(name+suffix+'.html')).write_text(page)
            (ROOT/(name+suffix+'.svg')).write_text(graphic)
    print('Rendered two bilingual concept diagrams with desktop and mobile compositions.')
