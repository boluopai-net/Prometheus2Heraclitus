"""Generate a reversible, non-identifying holding edition of shared readings.

Canonical private and shared sources are never changed. Run after saving the
current generated edition in Git; render-library.py restores reviewed content.
"""
import re
import shutil
from pathlib import Path

from commentaries import ESSAYS

dist = Path(__file__).resolve().parents[1] / 'dist'
library = dist / 'repositories/prometheus'
reader_routes = [path.relative_to(library) for path in library.rglob('*.html')]
license_page = (library / 'license/index.html').read_text()
vendor = library / 'vendor'
temporary_vendor = dist.parent / '.sites-runtime/privacy-hold-vendor'
temporary_vendor.parent.mkdir(parents=True, exist_ok=True)
if temporary_vendor.exists():
    shutil.rmtree(temporary_vendor)
shutil.copytree(vendor, temporary_vendor)
shutil.rmtree(library)


def page(english=False):
    lang = 'en' if english else 'zh-CN'
    title = 'Reading edition being updated' if english else '阅读版本正在更新'
    explanation = 'These readings are temporarily unavailable while identifying information is removed. The anonymous edition will return here.' if english else '这些阅读材料正在移除可识别个人的信息，暂时不提供正文。匿名阅读版将继续在这里呈现。'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow, noimageindex"><title>{title} · boluopai</title><link rel="icon" href="/mark.svg"><link rel="stylesheet" href="/style.css"></head><body><header class="header wrap"><a class="wordmark" href="/">boluopai.</a><nav aria-label="主导航"><a href="/philosophy/">哲学评论</a><a href="/singing/">唱歌</a><a href="/repositories/">作品</a></nav></header><main id="main" class="article wrap"><h1>{title}</h1><p>{explanation}</p><a class="text-link" href="/philosophy/">{'Philosophy commentaries →' if english else '哲学评论 →'}</a></main><footer class="footer wrap"><a class="wordmark" href="/">boluopai.</a><p class="copyright">© 2026 BOBBY · <a href="/rights/">版权与许可</a></p></footer></body></html>'''


for relative in reader_routes:
    target = library / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page('.zh-CN.' not in str(relative) and relative.name != 'index.html'))
(library / 'license/index.html').write_text(license_page)
shutil.copytree(temporary_vendor, library / 'vendor')
shutil.rmtree(temporary_vendor)
for name in ESSAYS:
    for language in ('', 'en'):
        (dist / 'philosophy' / name / language / 'index.html').write_text(page(bool(language)))
(dist / 'repositories/index.html').write_text(page())
for path in dist.rglob('*.html'):
    if path.relative_to(dist).parts[0] in {'client', 'server', '.openai'}:
        continue
    text = path.read_text()
    # Remove links to unreviewed profile, source, commit and history surfaces.
    text = re.sub(r'<a\b[^>]*href=["\']https?://(?:www\.)?github\.com/[^"\']*["\'][^>]*>([\s\S]*?)</a>', r'\1', text)
    path.write_text(text)
print('Published-output preparation: shared readings held; source-derived assets and GitHub links removed. Canonical sources unchanged.')
