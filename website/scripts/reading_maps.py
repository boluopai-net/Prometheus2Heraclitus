"""Embed the canonical responsive maps without creating another prose owner."""
import html

SOURCE = '/repositories/prometheus/source/skills/yinyang/references/diagrams/'


def reading_map(name, chinese, heading=True):
    suffix = '.zh-CN' if chinese else ''
    title = {
        'formation-path': ('窃火，然后成为火', 'Steal Fire, Then Become Fire'),
        'borrowed-fire': ('参加窃火，用火培养自己', 'Join in stealing fire, and use it to cultivate yourself'),
    }[name][0 if chinese else 1]
    src = SOURCE + name + suffix + '.html'
    label = '单独打开图示' if chinese else 'Open the diagram on its own'
    section_title = ('五部分的展开与回返' if chinese else 'Five parts, unfolding and returning') if name == 'formation-path' else title
    header = f'<h2>{html.escape(section_title)}</h2>' if heading else ''
    return f'''<section class="reading-map-embed">{header}<p><a href="{src}">{label} ↗</a></p><iframe class="reading-map-frame" data-reading-map title="{html.escape(title, quote=True)}" src="{src}?embed=1" style="width:100%;height:1580px;border:0" loading="lazy"></iframe><script defer src="/reading-map-embed.js"></script></section>'''
