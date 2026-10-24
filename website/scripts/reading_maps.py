"""Embed the canonical responsive maps without creating another prose owner."""
import html
import re

SOURCE = '/repositories/prometheus/source/skills/yinyang/references/diagrams/'


def reading_map(name, chinese):
    suffix = '.zh-CN' if chinese else ''
    title = {
        'formation-path': ('窃火，然后成为火', 'Steal Fire, Then Become Fire'),
        'borrowed-fire': ('参加窃火，用火培养自己', 'Join in stealing fire, and use it to cultivate yourself'),
    }[name][0 if chinese else 1]
    src = SOURCE + name + suffix + '.html'
    return f'''<section class="reading-map-embed"><iframe class="reading-map-frame" data-reading-map title="{html.escape(title, quote=True)}" src="{src}?embed=1" style="width:100%;height:760px;border:0" loading="lazy"></iframe><script defer src="/reading-map-embed.js"></script></section>'''


def inline_diagrams(rendered, path):
    """Place canonical diagrams where their argument is first developed."""
    chinese = '.zh-CN.md' in path
    name = path.rsplit('/', 1)[-1].replace('.zh-CN', '').removesuffix('.md')
    placements = {
        'stealing-fire': [('borrowed-fire', None)],
        'personal-first-humanism': [('layers', '六个相连的面向' if chinese else 'Six connected dimensions')],
        'why-yinyang': [
            ('encounter', '把两位参与者一起写出来' if chinese else 'Writing both participants together'),
            ('formation-path', '在共同工作中循环' if chinese else 'Cycling through shared work'),
        ],
    }
    for diagram, heading in placements.get(name, []):
        title = {
            'borrowed-fire': ('参加窃火，用火培养自己', 'Join in stealing fire, and use it to cultivate yourself'),
            'formation-path': ('窃火，然后成为火', 'Steal Fire, Then Become Fire'),
            'encounter': ('人与模型怎样共同探究', 'How people and models inquire together'),
            'layers': ('从世界理解到实践实现', 'From understanding the world to realizing a practice'),
        }[diagram][0 if chinese else 1]
        if diagram in {'borrowed-fire', 'formation-path'}:
            content = reading_map(diagram, chinese)
        else:
            source = SOURCE + diagram + ('.zh-CN' if chinese else '') + '.svg'
            content = f'<img class="inline-diagram-image" src="{source}" alt="{title}" loading="lazy">'
        href = '/repositories/prometheus/diagrams/' + diagram + ('/' if chinese else '/en/')
        figure = f'<figure class="inline-diagram" id="diagram-{diagram}">{content}<figcaption><a href="{href}">{title}</a></figcaption></figure>'
        if heading is None:
            match = re.search(r'<h2\b', rendered)
            if not match:
                raise ValueError(f'Missing first argument section: {path}')
            rendered = rendered[:match.start()] + figure + rendered[match.start():]
        else:
            pattern = r'(<h2\b[^>]*>' + re.escape(heading) + r'</h2>\s*<p>[\s\S]*?</p>)'
            rendered, count = re.subn(pattern, lambda match: match[0] + figure, rendered, count=1)
            if count != 1:
                raise ValueError(f'Missing inline diagram location: {path}: {heading}')
    return rendered
