"""The wheel and its reading-list symbols share one catalog and artwork."""
import html
import math

ORDER = ['yinyang', 'research', 'task-inquiry', 'paper-retrieval', 'local-teacher',
         'web-teacher', 'shopping', 'prompt-and-skill-lifecycle',
         'prompt-audit-orchestration', 'agent-orchestration-master',
         'model-conversation-relay', 'random-wheel', 'personal-environment-design',
         'android-control', 'browser-relay', 'obsidian-sync', 'chezmoi', 'network',
         'clash-auto-switch', 'model-upgrade-check', 'singing', 'video-subtitle']
SYMBOLS = dict(zip(ORDER, ['☯', '🔎', '💡', '📜', '📚', '🎓', '🛍️', '✍️', '📋', '🤝', '💬', '🎯', '🛠️', '📱', '🌐', '💎', '🏠', '📡', '🔀', '🚀', '🎤', '🎬']))


def badge(name):
    return f'<span class="skill-symbol" aria-hidden="true"><span>{SYMBOLS[name]}</span><small>{ORDER.index(name)+1:02}</small></span>'


def wheel(english, skills, yinyang_source):
    colors = ['#ffd3b5', '#bce8d8', '#c7e2fa', '#d9ccf4', '#f6c6db', '#fae4a6', '#cce7bc', '#bfe8ed', '#e8cdec', '#ffdfbf', '#d0ddef']
    segments = []
    step = 360 / len(ORDER)
    def point(radius, degrees):
        a = math.radians(degrees)
        return f'{280 + radius * math.sin(a):.3f} {280 - radius * math.cos(a):.3f}'
    for i, name in enumerate(ORDER):
        title = ('YinYang' if english else '阴阳') if name == 'yinyang' else skills[name][1 if english else 0]
        route = yinyang_source if name == 'yinyang' else '/tools/' + name + ('/en/' if english else '/')
        mid = i * step
        x, y = point(211, mid).split()
        d = f'M280 280 L{point(264, mid-step/2)} A264 264 0 0 1 {point(264, mid+step/2)} Z'
        segments.append(f'<a href="{route}" data-wheel-option="{name}" data-wheel-label="{html.escape(title, quote=True)}" aria-label="{i+1}. {html.escape(title, quote=True)}"><title>{html.escape(title)}</title><path class="skill-sector" d="{d}" fill="{colors[i % len(colors)]}" stroke="#fff9e9" stroke-width="1.8"/><circle cx="{x}" cy="{y}" r="23" fill="#fff8e7" fill-opacity=".88"/><text x="{x}" y="{float(y)+2}" text-anchor="middle" dominant-baseline="central" font-size="32" fill="#243b50" style="font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif">{SYMBOLS[name]}</text><text x="{point(246, mid).split()[0]}" y="{point(246, mid).split()[1]}" text-anchor="middle" dominant-baseline="middle" fill="#29404c" font-weight="600" font-size="11">{i+1:02}</text></a>')
    label = '22 Skills · equal chances' if english else '22 个 Skill · 等概率抽选'
    studs = ''.join(f'<circle cx="{point(272, i*360/44).split()[0]}" cy="{point(272, i*360/44).split()[1]}" r="3.7" fill="#d6c8ed"/>' for i in range(44))
    return f'<div class="skills-wheel-stage"><span class="skills-wheel-pointer" aria-hidden="true"></span><svg class="skills-picker" viewBox="0 0 560 560" role="group" aria-label="{label}"><defs><linearGradient id="wheel-rim" x2=".8" y2="1"><stop stop-color="#b9d8f3"/><stop offset=".38" stop-color="#b9a5df"/><stop offset=".7" stop-color="#e8b6d2"/><stop offset="1" stop-color="#aadbcf"/></linearGradient><radialGradient id="wheel-hub" cx="35%" cy="25%"><stop stop-color="#ffffff"/><stop offset=".8" stop-color="#fff9fb"/><stop offset="1" stop-color="#e8dff4"/></radialGradient></defs><circle cx="280" cy="280" r="279" fill="#fff"/>{studs}<g data-wheel-disc>{"".join(segments)}</g><circle cx="281" cy="284" r="73" fill="#8873ac" opacity=".22"/><circle cx="280" cy="280" r="70" fill="url(#wheel-hub)" stroke="#c9b9e5" stroke-width="3"/><circle cx="280" cy="280" r="62" fill="none" stroke="#ffffff"/><text x="280" y="277" text-anchor="middle" fill="#7c69a0" font-size="22" font-weight="700" letter-spacing="2">SKILLS</text><text x="280" y="301" text-anchor="middle" fill="#9b7b9d" font-size="11" letter-spacing="1">22 · DISCOVER</text></svg></div>'
