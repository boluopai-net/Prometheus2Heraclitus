"""Render the public listening station from an explicitly published catalog."""
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def safe_url(value):
    if any(ord(char) < 33 for char in value) or '\\' in value:
        raise ValueError('Recording URLs cannot contain whitespace, controls, or backslashes')
    parsed = urlsplit(value)
    if not ((parsed.scheme == 'https' and parsed.netloc) or
            (value.startswith('/') and not value.startswith('//') and not parsed.scheme)):
        raise ValueError('Recording URLs must be HTTPS or site-relative')
    return html.escape(value, quote=True)


def recordings_html(recordings, english):
    if not recordings:
        title = 'The first recording is still to come.' if english else '第一首录音，待发布。'
        return f'<section class="voice-empty"><div><h2>{title}</h2></div></section>'
    entries = []
    for item in recordings:
        title, performer, rights = (html.escape(item[key]) for key in ('title', 'performer', 'rights'))
        audio = safe_url(item['audio_url'])
        source = safe_url(item['source_url'])
        label = 'Recording source' if english else '录音来源'
        entries.append(f'<article class="recording"><h2>{title}</h2><p>{performer}</p>'
                       f'<audio controls preload="none" src="{audio}"></audio>'
                       f'<p><a href="{source}">{label}</a> · {rights}</p></article>')
    return '<section class="recordings">' + ''.join(entries) + '</section>'


def render():
    recordings = json.loads((ROOT / 'content/singing/recordings.json').read_text())
    for english in (False, True):
        suffix = 'en/' if english else ''
        title = 'Singing station' if english else '唱歌点播台'
        intro = ('A collection of my singing.' if english else '这里收录我的演唱。')
        contribution = ('Include the song title and preferred artist or version.' if english else
                        '请注明曲名、原唱或想听的版本。')
        target = ROOT / 'dist/singing' / suffix / 'index.html'
        target.write_text(f'''<!doctype html><html lang="{'en' if english else 'zh-CN'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · boluopai</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="/mark.svg"></head>
<body><header class="header wrap"></header><main id="main" class="wrap collection">
<div class="collection-heading"><img class="motif collection-motif" src="/motifs/moon.svg" alt="" aria-hidden="true">
<h1>{title}</h1><p class="collection-intro">{intro}</p>
<a href="https://github.com/boluopai-net/Prometheus2Heraclitus/issues/new">{'Request a song for boluopai' if english else '向 boluopai 点歌'}</a><p>{contribution}</p></div>
{recordings_html(recordings, english)}</main><footer class="footer wrap"><p class="copyright"></p></footer></body></html>''')


if __name__ == '__main__':
    render()
