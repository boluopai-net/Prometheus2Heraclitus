"""Maintain the bilingual contact and picker shells; shared chrome is projected last."""
from pathlib import Path
import re
from repository_panel import panel, with_comments
from singing_pages import render as render_singing
render_singing()
root = Path(__file__).resolve().parents[1] / 'dist'
for route, kind in [('philosophy', 'Philosophy'), ('singing', 'Singing')]:
    for english in (False, True):
        target = root / route / ('en/index.html' if english else 'index.html')
        target.write_text(with_comments(target.read_text(), english, kind))
        if route == 'singing':
            target.write_text(target.read_text().replace('/motifs/sun-moon.svg', '/motifs/microphone-tilted.svg').replace('/motifs/microphone.svg', '/motifs/microphone-tilted.svg'))
for route, english in [('repositories/index.html', False), ('repositories/en/index.html', True)]:
    target = root / route
    text = target.read_text()
    text = text.replace('<script defer src="/repository.js"></script>', '<script type="module" src="/repository.js"></script>')
    if '<script type="module" src="/giscus-comments.js"></script>' not in text:
        text = text.replace('</head>', '<script type="module" src="/giscus-comments.js"></script></head>')
    text = re.sub(r'<div class="repository-tools"[\s\S]*?(?=</main>)', lambda _: panel(english), text)
    target.write_text(text)
for en in (False, True):
    def tr(zh, english): return english if en else zh
    lang = 'en' if en else 'zh-CN'
    suffix = 'en/' if en else ''
    def page(route, title, body, extra=''):
        target = root / route / suffix / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · boluopai.</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="/mark.svg">{extra}</head><body><header class="header wrap"></header><main class="wrap">{body}</main><footer class="footer wrap"><a class="wordmark" href="/">boluopai.</a><p class="copyright"></p></footer></body></html>')
    page('comment/manage', tr('管理我的评论','Manage my comment'), f'''<section class="comment-management repository-tool"><h1>{tr('管理我的评论','Manage my comment')}</h1><p>{tr('这里是这条评论的私人管理入口。打开链接不会删除评论；只有点击删除并确认后才会删除。','This is the private management page for your comment. Opening it does not delete anything; deletion requires your confirmation.')}</p><p>{tr('保存私人删除链接可以换设备管理，请勿公开分享。','Save the private deletion link to manage your comment on another device. Do not share it publicly.')}</p><p id="manage-status" class="repo-status" role="status">{tr('正在读取…','Loading…')}</p><article id="managed-comment" class="suggestion-entry" hidden><p class="suggestion-meta"><strong id="managed-author" class="suggestion-author"></strong><time id="managed-time"></time></p><h2 id="managed-title"></h2><p id="managed-body" class="suggestion-body"></p></article><div id="manage-actions" class="suggestion-actions" hidden><button id="copy-deletion-link" type="button">{tr('复制私人删除链接','Copy private deletion link')}</button><button id="delete-comment" type="button">{tr('删除这条评论','Delete this comment')}</button><input id="deletion-link" aria-label="{tr('私人删除链接','Private deletion link')}" readonly hidden></div><p><a id="back-to-comments" href="/repositories/{suffix}#advice">{tr('返回评论区','Back to comments')}</a></p><p>{tr('如果私人链接和原浏览器记录都丢失，可以','If you lose both the private link and the original browser data, you can')} <a href="https://github.com/boluopai-net/Prometheus2Heraclitus">{tr('在 GitHub 联系我','contact me on GitHub')}</a>。</p></section>''', '<meta name="robots" content="noindex,nofollow,noarchive"><meta name="referrer" content="no-referrer"><link rel="stylesheet" href="/repository.css"><script type="module" src="/manage-comment.js"></script>')
    page('wheel',tr('抽卡转盘','Draw wheel'),f'''<div class="picker"><section class="selection-panel"><h1>{tr('今天选什么？','What will it be?')}</h1><div class="mode-switch"><button id="catalog-mode" aria-pressed="true">{tr('现有清单','Saved list')}</button><button id="free-mode" aria-pressed="false">{tr('自由输入','Free input')}</button></div><div id="free-input" hidden><label for="options">{tr('一行一个选项','One option per line')}</label><textarea id="options" maxlength="20100"></textarea></div><div class="actions"><button id="all">{tr('全选','Select all')}</button><button id="none">{tr('清空','Clear selection')}</button></div><p id="message" role="status"></p><div id="choices"></div><form id="add-option"><label for="new-option">{tr('添加选项','Add an option')}</label><div class="add-row"><input id="new-option" maxlength="200" required><button type="submit">{tr('添加','Add')}</button></div></form><p class="hint">{tr('每项机会相同。清单和选择只保存在当前浏览器，不影响其他人；清理网站数据后会丢失。','Every option has an equal chance. Your list and selection stay only in this browser and do not affect anyone else. Clearing site data removes them.')}</p></section><section class="wheel-panel"><p id="empty">{tr('先添加几个选项，再转。','Add a few options to start.')}</p><iframe id="wheel" title="{tr('抽卡转盘','Draw wheel')}" sandbox="allow-scripts" hidden></iframe></section></div>''','<link rel="stylesheet" href="/wheel/picker.css"><script src="/wheel/picker.js" defer></script>')
    home = root / suffix / 'index.html'
    guide_entry = f'''<!-- GETTING STARTED START --><section class="section wrap" aria-labelledby="getting-started-title"><p class="eyebrow">{tr('开始使用','GETTING STARTED')}</p><div class="section-heading"><h2 id="getting-started-title"><a href="/getting-started/{suffix}" data-page-title>{tr('工具使用','Using the Tools')}</a></h2><img class="motif" src="/motifs/axe.svg" alt="" aria-hidden="true"></div><p>{tr('具身全模态学习、具身全模态理解、具身全模态工作，把协作投入自己的生活。让模型协助形成个人哲学、控制工具与环境的复杂性，在实际任务中培养整体感、直觉与创造。','Embodied, full-modal learning, understanding, and work: bring collaboration into your life. Let models help form a personal philosophy and control environmental complexity, cultivating intuition, a sense of the whole, and creation through actual tasks.')}</p></section><!-- GETTING STARTED END -->'''
    home_source = re.sub(r'<!-- GETTING STARTED START -->[\s\S]*?<!-- GETTING STARTED END -->(?:\r?\n)?', '', home.read_text())
    home_source = home_source.replace('/motifs/yinyang.svg', '/motifs/notebook.svg')
    home.write_text(home_source.replace('  <section id="philosophy"', guide_entry + '\n  <section id="philosophy"', 1))
    home_text = re.sub(r'<!-- READER PATHS START -->[\s\S]*?<!-- READER PATHS END -->', '', home.read_text())
    if 'href="/reader-paths.css"' not in home_text:
        home_text = home_text.replace('</head>', '<link rel="stylesheet" href="/reader-paths.css"></head>')
    paths = f'''<!-- READER PATHS START --><section class="section wrap reader-paths"><div class="section-heading"><h2><a href="https://github.com/boluopai-net/Prometheus2Heraclitus">{tr('继续交流与创作','Continue the conversation')}</a></h2></div><p>{tr('Skills 和工具欢迎直接改进并提交 PR，也可以先用 Issue 讨论问题。哲学鼓励你从自己的经验与思想出发创作；对这份文集的纠正、异议和改进，同样欢迎 Issue 与 PR。想法也可以留在哲学、唱歌和资料页面的评论区。','Improve reusable Skills and tools and submit a pull request, or open an Issue to discuss a problem. For philosophy, develop your own work from your experience and ideas; corrections, objections, and improvements to this collection are also welcome through Issues and pull requests. Thoughts can also be shared in the page comments.')}</p></section><!-- READER PATHS END -->'''
    home.write_text(home_text.replace('<aside class="playground wrap">', paths+'<aside class="playground wrap">'))
