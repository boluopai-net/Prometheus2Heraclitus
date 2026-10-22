"""The wheel and its reading-list symbols share one catalog and artwork."""
import html
import math
import re

ORDER = ['yinyang', 'research', 'task-inquiry', 'paper-retrieval', 'local-teacher',
         'web-teacher', 'shopping', 'prompt-and-skill-lifecycle',
         'prompt-audit-orchestration', 'agent-orchestration-master',
         'model-conversation-relay', 'random-wheel', 'personal-environment-design',
         'android-control', 'browser-relay', 'obsidian-sync', 'chezmoi', 'network',
         'clash-auto-switch', 'model-upgrade-check', 'singing', 'video-subtitle']
SYMBOLS = dict(zip(ORDER, ['☯︎', '🔎', '💡', '📜', '📚', '🎓', '🛍️', '✍️', '📋', '🤝', '💬', '🎯', '🛠️', '📱', '🌐', '💎', '🏠', '📡', '🔀', '🚀', '🎤', '🎬']))

DRAWN = {
    'paper-retrieval': '<path d="M3 1h11l4 4v16H3z" fill="#fffefa" stroke="#738594" stroke-width="1"/><path d="M14 1v5h4" fill="#dde7ec" stroke="#738594" stroke-width=".8"/><path d="M6 6h5 M6 9h8 M6 12h5 M6 15h4" stroke="#91a3ad" stroke-width="1.1"/><circle cx="15" cy="15" r="5" fill="#bce9f3" fill-opacity=".85" stroke="#456e88" stroke-width="1.5"/><path d="M18.7 18.7l3.7 3.7" stroke="#3a5261" stroke-width="2.8" stroke-linecap="round"/><path d="M12.5 13.3q1-1.8 3.3-1.3" fill="none" stroke="white" stroke-width="1.2" stroke-linecap="round"/>',
    'local-teacher': '<path d="M2 10L12 2l10 8v12H2z" fill="#fff0ce" stroke="#bf9472" stroke-width=".8"/><path d="M1 10L12 1l11 9" fill="none" stroke="#df9366" stroke-width="2" stroke-linecap="round"/><rect x="9" y="7" width="11" height="7" rx="1" fill="#75ada0" stroke="#a47c53" stroke-width="1"/><path d="M12 9h5 M12 11h3" stroke="#edf7e7" stroke-width=".8"/><circle cx="6" cy="12" r="2" fill="#e8b68d"/><path d="M3.5 19v-3a2.5 2.5 0 0 1 5 0v3" fill="#819fc8"/><circle cx="15" cy="16" r="1.8" fill="#e8b68d"/><path d="M12.5 21v-2a2.5 2.5 0 0 1 5 0v2" fill="#e7ac74"/><path d="M9 19h12 M11 19v4 M19 19v4" stroke="#9b805d" stroke-width="1.3"/><path d="M11 17l3 .5 3-.5v2l-3 .4-3-.4z" fill="#fff"/>',
    'web-teacher': '<rect x="1" y="2" width="22" height="17" rx="2" fill="#e7f4fb" stroke="#5b7b97" stroke-width="1.3"/><path d="M1 6h22" stroke="#8aa9bf" stroke-width="1"/><circle cx="4" cy="4" r=".7" fill="#e98b7d"/><circle cx="6.5" cy="4" r=".7" fill="#e7c46a"/><circle cx="9" cy="4" r=".7" fill="#7cb591"/><circle cx="7" cy="10" r="2" fill="#e9b990"/><path d="M3.5 16v-2a3.5 3.5 0 0 1 7 0v2" fill="#82aac4"/><rect x="13" y="8" width="8" height="7" rx="1" fill="#78b8bc"/><path d="M16 9.5l3 2-3 2z" fill="white"/><path d="M4 17h16 M12 19v3 M8 22h8" stroke="#5b7b97" stroke-width="1.2" stroke-linecap="round"/>',
    'prompt-and-skill-lifecycle': '<path d="M4 9a9 9 0 0 1 15-4" fill="none" stroke="#579fba" stroke-width="2.3" stroke-linecap="round"/><path d="M19 1v5h-5" fill="none" stroke="#579fba" stroke-width="2" stroke-linejoin="round"/><path d="M21 9a9 9 0 0 1-7 12" fill="none" stroke="#dfa260" stroke-width="2.3" stroke-linecap="round"/><path d="M18 23l-5-2 3-4" fill="none" stroke="#dfa260" stroke-width="2" stroke-linejoin="round"/><path d="M9 21a9 9 0 0 1-7-9" fill="none" stroke="#7eaf88" stroke-width="2.3" stroke-linecap="round"/><path d="M0 16l2-5 4 3" fill="none" stroke="#7eaf88" stroke-width="2" stroke-linejoin="round"/><rect x="8" y="7" width="8" height="10" rx="1" fill="#fffdf5" stroke="#8995a0" stroke-width=".8"/><path d="M10 10h4 M10 12h4 M10 14h2" stroke="#8995a0" stroke-width=".8"/>',
    'prompt-audit-orchestration': '<rect x="3" y="3" width="18" height="20" rx="2" fill="#fffdf8" stroke="#93a0ab" stroke-width="1"/><rect x="8" y="1" width="8" height="4" rx="1" fill="#c8d5df" stroke="#8395a4" stroke-width=".8"/><path d="M6 9l1.5 1.5L11 7" fill="none" stroke="#42a46b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.5 14l4 4 M10.5 14l-4 4" stroke="#df6b66" stroke-width="1.8" stroke-linecap="round"/><path d="M14 9h4 M14 16h4 M6 21h12" stroke="#a5b1b9" stroke-width="1" stroke-linecap="round"/>',
    'yinyang': '<circle cx="12" cy="12" r="10" fill="white" stroke="#222" stroke-width=".8"/><path d="M12 2a10 10 0 0 1 0 20 5 5 0 0 1 0-10 5 5 0 0 0 0-10" fill="#222"/><circle cx="12" cy="7" r="1.8" fill="#222"/><circle cx="12" cy="17" r="1.8" fill="white"/>',
    'obsidian-sync': '<path d="M12 4l5 5-1 9-5 3-5-7 2-7z" fill="#7951b3" stroke="#68439a" stroke-width=".6"/><path d="M12 4l-1 10-5 0 2-7z" fill="#b69adf"/><path d="M12 4l5 5-6 5z" fill="#9972cf"/><path d="M11 14l5 4-5 3z" fill="#563482"/><path d="M17 9l-1 9-5-4z" fill="#7044a6"/><path d="M2 10a10 10 0 0 1 17-5 M22 14a10 10 0 0 1-17 5" fill="none" stroke="#689c9a" stroke-width="1.7" stroke-linecap="round"/><path d="M19 1v4h-4 M5 23v-4h4" fill="none" stroke="#689c9a" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
}
_mini_colors = ['#ee8f86', '#f4b46f', '#f2d86f', '#99c990', '#7dcbc7', '#80addd', '#b091d3']
_mini_parts = []
for _i, _color in enumerate(_mini_colors):
    _a, _b = [math.radians(v * 360 / 7) for v in (_i, _i + 1)]
    _mini_parts.append(f'<path d="M12 12L{12+10*math.sin(_a):.2f} {12-10*math.cos(_a):.2f}A10 10 0 0 1 {12+10*math.sin(_b):.2f} {12-10*math.cos(_b):.2f}Z" fill="{_color}" stroke="white" stroke-width=".5"/>')
DRAWN['random-wheel'] = ''.join(_mini_parts) + '<circle cx="12" cy="12" r="3" fill="white" stroke="#aaa" stroke-width=".5"/><path d="M10 0h4l-2 5z" fill="#555"/>'


def graphic(name, x=0, y=0, size=28):
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true">{DRAWN[name]}</svg>'


def thumbnail(english, skills):
    drawing = wheel(english, skills, '#')
    drawing = re.sub(r'<a\b[^>]*>|</a>', '', drawing)
    return drawing.replace('skills-wheel-stage', 'skills-wheel-stage skills-wheel-mini').replace(' data-wheel-disc', '')


def badge(name):
    art = graphic(name) if name in DRAWN else f'<span>{SYMBOLS[name]}</span>'
    return f'<span class="skill-symbol" aria-hidden="true"><small>{ORDER.index(name)+1:02}</small>{art}</span>'


def wheel(english, skills, yinyang_source):
    colors = ['#ef9991', '#f5bd83', '#f5df83', '#a7d49c', '#91d5d2', '#92bae5', '#ba9edb']
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
        art = graphic(name, float(x)-17, float(y)-17, 34) if name in DRAWN else f'<text x="{x}" y="{float(y)+2}" text-anchor="middle" dominant-baseline="central" font-size="32" style="font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif">{SYMBOLS[name]}</text>'
        d = f'M280 280 L{point(264, mid-step/2)} A264 264 0 0 1 {point(264, mid+step/2)} Z'
        segments.append(f'<a href="{route}" data-wheel-option="{name}" data-wheel-label="{html.escape(title, quote=True)}" aria-label="{i+1}. {html.escape(title, quote=True)}"><title>{html.escape(title)}</title><path class="skill-sector" d="{d}" fill="{colors[i % len(colors)]}" stroke="#fff9e9" stroke-width="1.8"/><circle cx="{x}" cy="{y}" r="23" fill="#fff8e7" fill-opacity=".88"/>{art}<text x="{point(246, mid).split()[0]}" y="{point(246, mid).split()[1]}" text-anchor="middle" dominant-baseline="middle" fill="#29404c" font-weight="600" font-size="11">{i+1:02}</text></a>')
    label = '22 Skills · equal chances' if english else '22 个 Skill · 等概率抽选'
    studs = ''.join(f'<circle cx="{point(272, i*360/44).split()[0]}" cy="{point(272, i*360/44).split()[1]}" r="3.7" fill="#e2e0dc" stroke="#fff" stroke-width=".8"/>' for i in range(44))
    return f'<div class="skills-wheel-stage"><span class="skills-wheel-pointer" aria-hidden="true"></span><svg class="skills-picker" viewBox="0 0 560 560" role="group" aria-label="{label}"><defs><linearGradient id="wheel-rim" x2=".8" y2="1"><stop stop-color="#ffffff"/><stop offset=".38" stop-color="#faf9f6"/><stop offset=".7" stop-color="#eeede9"/><stop offset="1" stop-color="#f8f7f3"/></linearGradient><radialGradient id="wheel-hub" cx="35%" cy="25%"><stop stop-color="#ffffff"/><stop offset=".8" stop-color="#faf9f6"/><stop offset="1" stop-color="#e6e4de"/></radialGradient></defs><circle cx="280" cy="280" r="279" fill="url(#wheel-rim)" stroke="#d5d3cf" stroke-width="1"/>{studs}<g data-wheel-disc>{"".join(segments)}</g><circle cx="281" cy="284" r="73" fill="#77766f" opacity=".22"/><circle cx="280" cy="280" r="70" fill="url(#wheel-hub)" stroke="#c9c7c0" stroke-width="3"/><circle cx="280" cy="280" r="62" fill="none" stroke="#ffffff"/><text x="280" y="277" text-anchor="middle" fill="#53616a" font-size="22" font-weight="700" letter-spacing="2">SKILLS</text><text x="280" y="301" text-anchor="middle" fill="#868a88" font-size="11" letter-spacing="1">22 · DISCOVER</text></svg></div>'
