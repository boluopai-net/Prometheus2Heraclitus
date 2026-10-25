"""Check generated entrance destinations and Core views' linked arguments."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'dist'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])


def check(href, current):
    link = urlsplit(href)
    if link.scheme or link.netloc:
        return
    target = ROOT / link.path.lstrip('/') if link.path else current
    if target.is_dir():
        target /= 'index.html'
    assert target.is_file(), f'Missing destination: {href}'
    if link.fragment:
        assert unquote(link.fragment) in Page(target).ids, f'Missing section: {href}'


for suffix in ('', 'en/'):
    entrance = ROOT / 'philosophy' / suffix / 'index.html'
    for href in Page(entrance).links:
        check(href, entrance)
    core = ROOT / ('repositories/prometheus/source/skills/yinyang/references/docs/'
                   + ('core-views.html' if suffix else 'core-views.zh-CN.html'))
    page = Page(core)
    assert any('/philosophy/stealing-fire/' in href for href in page.links)
    for href in page.links:
        if href.startswith('/philosophy/'):
            check(href, core)
print('Both reading entrances and Core views argument links resolve.')
