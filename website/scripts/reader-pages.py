"""Maintain the bilingual contact and picker shells; shared chrome is projected last."""
from pathlib import Path
import re
from repository_panel import with_comments
from singing_pages import render as render_singing
render_singing()
root = Path(__file__).resolve().parents[1] / 'dist'
for route, kind in [('philosophy', 'Philosophy'), ('singing', 'Singing')]:
    for english in (False, True):
        target = root / route / ('en/index.html' if english else 'index.html')
        target.write_text(with_comments(target.read_text(), english, kind))
for route, english in [('repositories/index.html', False), ('repositories/en/index.html', True)]:
    target = root / route
    target.write_text(with_comments(target.read_text(), english, 'Advice'))
for en in (False, True):
    def tr(zh, english): return english if en else zh
    lang = 'en' if en else 'zh-CN'
    suffix = 'en/' if en else ''
    def page(route, title, body, extra=''):
        target = root / route / suffix / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · boluopai.</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="/mark.svg">{extra}</head><body><header class="header wrap"></header><main class="wrap">{body}</main><footer class="footer wrap"><a class="wordmark" href="/">boluopai.</a><p class="copyright"></p></footer></body></html>')
    page('wheel',tr('抽卡转盘','Draw wheel'),f'''<div class="picker"><section class="selection-panel"><h1>{tr('今天选什么？','What will it be?')}</h1><div class="mode-switch"><button id="catalog-mode" aria-pressed="true">{tr('现有清单','Saved list')}</button><button id="free-mode" aria-pressed="false">{tr('自由输入','Free input')}</button></div><div id="free-input" hidden><label for="options">{tr('一行一个选项','One option per line')}</label><textarea id="options" maxlength="20100"></textarea></div><div class="actions"><button id="all">{tr('全选','Select all')}</button><button id="none">{tr('反选','Invert selection')}</button><button id="delete">{tr('删除','Delete selected')}</button></div><p id="message" role="status"></p><div id="choices"></div><form id="add-option"><label for="new-option">{tr('添加选项','Add an option')}</label><div class="add-row"><input id="new-option" maxlength="200" required><button type="submit">{tr('添加','Add')}</button></div></form><p class="hint">{tr('每项机会相同。清单和选择只保存在当前浏览器，不影响其他人；清理网站数据后会丢失。','Every option has an equal chance. Your list and selection stay only in this browser and do not affect anyone else. Clearing site data removes them.')}</p></section><section class="wheel-panel"><p id="empty">{tr('先添加几个选项，再转。','Add a few options to start.')}</p><iframe id="wheel" title="{tr('抽卡转盘','Draw wheel')}" sandbox="allow-scripts" hidden></iframe></section></div>''','<link rel="stylesheet" href="/wheel/picker.css"><script src="/wheel/picker.js" defer></script>')
    home = root / suffix / 'index.html'
    guide_entry = f'''<!-- GETTING STARTED START --><section class="section wrap" aria-labelledby="getting-started-title"><div class="section-heading"><h2 id="getting-started-title"><a href="/getting-started/{suffix}" data-page-title>{tr('工具使用','Using the Tools')}</a></h2><img class="motif" src="/motifs/axe.svg" alt="" aria-hidden="true"></div><p>{tr('从网络、订阅与客户端开始，用中文表达眼前的需要，让模型选择和组合合适的 Skills、接通工具并完成一件实际任务，再按使用反馈改进环境。','Start with connectivity, a subscription, and a client. Express the need in Chinese, let the model select and combine suitable Skills, connect tools, and complete an actual task, then improve the environment through feedback from use.')}</p></section><!-- GETTING STARTED END -->'''
    home_source = re.sub(r'<!-- GETTING STARTED START -->[\s\S]*?<!-- GETTING STARTED END -->(?:\r?\n)?', '', home.read_text())
    home_source = home_source.replace('/motifs/yinyang.svg', '/motifs/notebook.svg')
    home_source = re.sub(r'(<section id="philosophy"[\s\S]*?<img class="motif" src=")[^"]+', r'\1/motifs/sun.svg', home_source, count=1)
    home_source = re.sub(r'(<section id="singing"[\s\S]*?<img class="motif" src=")[^"]+', r'\1/motifs/moon.svg', home_source, count=1)
    if 'class="hero-title-row"' not in home_source:
        home_source = re.sub(r'(<h1 id="hero-title">[^<]+</h1>)', r'<div class="hero-title-row">\1<img class="motif" src="/motifs/sun-river.svg" alt="" aria-hidden="true"></div>', home_source, count=1)
    home.write_text(home_source.replace('  <section id="philosophy"', guide_entry + '\n  <section id="philosophy"', 1))
    home_text = re.sub(r'<!-- READER PATHS START -->[\s\S]*?<!-- READER PATHS END -->', '', home.read_text())
    if 'href="/reader-paths.css"' not in home_text:
        home_text = home_text.replace('</head>', '<link rel="stylesheet" href="/reader-paths.css"></head>')
    paths = f'''<!-- READER PATHS START --><section class="section wrap reader-paths"><div class="section-heading"><h2><a href="https://github.com/boluopai-net/Prometheus2Heraclitus">{tr('继续交流与创作','Continue the conversation')}</a></h2><img class="motif" src="/motifs/pen.svg" alt="" aria-hidden="true"></div><p>{tr('Skills 和工具欢迎直接改进并提交 PR，也可以先用 Issue 讨论问题。哲学鼓励你从自己的经验与思想出发创作；对这份文集的纠正、异议和改进，同样欢迎 Issue 与 PR。想法也可以留在哲学、唱歌和资料页面的评论区。','Improve reusable Skills and tools and submit a pull request, or open an Issue to discuss a problem. For philosophy, develop your own work from your experience and ideas; corrections, objections, and improvements to this collection are also welcome through Issues and pull requests. Thoughts can also be shared in the page comments.')}</p></section><!-- READER PATHS END -->'''
    home.write_text(home_text.replace('<aside class="playground wrap">', paths+'<aside class="playground wrap">'))
