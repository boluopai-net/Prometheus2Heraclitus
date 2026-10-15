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
        text = 'Request a song or offer a recording below.' if english else '可以先在下面点歌，或提出录音投稿。'
        return f'<section class="voice-empty"><div><h2>{title}</h2><p>{text}</p></div></section>'
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
        intro = ('Listen to published recordings, request a song, or contribute your voice. '
                 'Request songs in the comments or contribute a recording directly through a GitHub PR; no prior comment or Issue is required.' if english else
                 '听已经发布的录音，点一首想听的歌，也欢迎把自己的声音带来。可以在评论区点歌，也可以直接通过 GitHub PR 投稿录音，不必先发评论或 Issue。')
        contribution = ('Include the song, performer, a recording link, and permission to publish it. '
                        'A submission becomes playable here after it is accepted and published.' if english else
                        '投稿时请写明曲目、演唱者、录音链接和可公开使用的授权说明；确认收录并发布后，就能在这里播放。')
        target = ROOT / 'dist/singing' / suffix / 'index.html'
        target.write_text(f'''<!doctype html><html lang="{'en' if english else 'zh-CN'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · boluopai</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="/mark.svg"></head>
<body><header class="header wrap"></header><main id="main" class="wrap collection">
<div class="collection-heading"><img class="motif collection-motif" src="/motifs/moon.svg" alt="" aria-hidden="true">
<h1>{title}</h1><p class="collection-intro">{intro}</p><p>{contribution}</p>
<a href="https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/CONTRIBUTING{'.md' if english else '.zh-CN.md'}">{'Contribution guide' if english else '投稿与共同编辑说明'}</a></div>
{recordings_html(recordings, english)}</main><footer class="footer wrap"><p class="copyright"></p></footer></body></html>''')


if __name__ == '__main__':
    render()
