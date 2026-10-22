"""Check local reading and public GitHub source entrances."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

from commentaries import MAINLINE, EXTENSIONS, article_url, book_navigation


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.current_link = None
        self.in_heading = False
        self.heading = ''
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.current_link = dict(attrs, label='')
            self.links.append(self.current_link)
        if tag == 'h1':
            self.in_heading = True

    def handle_data(self, data):
        if self.current_link is not None:
            self.current_link['label'] += data
        if self.in_heading:
            self.heading += data

    def handle_endtag(self, tag):
        if tag == 'a':
            self.current_link = None
        if tag == 'h1':
            self.in_heading = False


dist = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'dist'
for landing_path, reader in (
    ('repositories/index.html', '/repositories/prometheus/'),
    ('repositories/en/index.html', '/repositories/prometheus/en/'),
):
    landing = (dist / landing_path).read_text()
    actions = [a for a in Links(landing).links if a.get('href') == reader]
    assert len(actions) == 1, f'{landing_path}: expected one local reading action'
    assert (dist / reader.lstrip('/') / 'index.html').is_file(), reader
    assert any(a.get('href', '').startswith('https://github.com/boluopai-net/Prometheus2Heraclitus') for a in Links(landing).links), landing_path
    for removed_copy in ('仓库访问说明', '无需 GitHub 登录', 'Repository access', 'without signing in to GitHub'):
        assert removed_copy not in landing, (landing_path, removed_copy)
for page in (dist / 'repositories/prometheus').rglob('*.html'):
    assert not any(a.get('href', '').startswith(('/apply/', '/applications/', '/downloads/')) for a in Links(page.read_text()).links), page
print('Local reading, public GitHub entrances, and retired download-route checks passed.')

for page in dist.rglob('*.html'):
    if page.relative_to(dist).parts[0] in {'client', 'server', '.openai'}:
        continue
    for link in Links(page.read_text()).links:
        if 'data-page-title' not in link:
            continue
        target = dist / link['href'].lstrip('/') / 'index.html'
        title = Links(target.read_text()).heading
        assert title and link['label'].split() == title.split(), (page, link['href'], link['label'], title)
print('Full-title entrances match their destination headings.')


def book_links(text):
    return [
        [(link.get('href'), ' '.join(link['label'].split())) for link in Links(section).links]
        for section in re.findall(r'<section class="book-stage">[\s\S]*?</section>', text)
    ]


for chinese in (True, False):
    for name in ['overview', *MAINLINE, *(entry[0] for entry in EXTENSIONS)]:
        route = ('/philosophy/' + ('' if chinese else 'en/')) if name == 'overview' else article_url(name, chinese)
        page = dist / route.lstrip('/') / 'index.html'
        expected = book_links(book_navigation(name, chinese))
        assert book_links(page.read_text()) == expected, f'{route}: rendered book navigation differs from the current reading route'
print('Every desktop and mobile book menu matches the current route and article titles.')
