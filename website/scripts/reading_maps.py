"""Embed the canonical responsive maps without creating another prose owner."""
import html

SOURCE = '/repositories/prometheus/source/skills/yinyang/references/diagrams/'


def reading_map(name, chinese):
    suffix = '.zh-CN' if chinese else ''
    title = {
        'formation-path': ('窃火，然后成为火', 'Steal Fire, Then Become Fire'),
        'borrowed-fire': ('参加窃火，用火培养自己', 'Join in stealing fire, and use it to cultivate yourself'),
    }[name][0 if chinese else 1]
    src = SOURCE + name + suffix + '.html'
    return f'''<section class="reading-map-embed"><iframe class="reading-map-frame" data-reading-map title="{html.escape(title, quote=True)}" src="{src}?embed=1" style="width:100%;height:760px;border:0" loading="lazy"></iframe><script defer src="/reading-map-embed.js"></script></section>'''
