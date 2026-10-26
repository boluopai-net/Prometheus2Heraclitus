"""Keep the public reading projection discoverable at its canonical URLs."""
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

ORIGIN = "https://boluopai.net"


class PageHead(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.redirect = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.redirect = True


def update_search_index(root):
    root = Path(root)
    urls = set()
    pages = 0
    for page in sorted(root.rglob("*.html")):
        relative = page.relative_to(root).as_posix()
        if relative.split("/")[0] in {"client", "server", ".openai"}:
            continue
        text = page.read_text()
        # The current public-site choice supersedes the former site-wide exclusion.
        text = re.sub(r'<meta\b(?=[^>]*\bname\s*=\s*["\'](?:robots|googlebot|bingbot)["\'])[^>]*>', '', text, flags=re.I)
        url = ORIGIN + "/" + relative.removesuffix("index.html")
        head = PageHead()
        head.feed(text)
        if not head.canonical and not head.redirect:
            link = '<link rel="canonical" href="' + escape(url, quote=True) + '">'
            if re.search(r"<head\b", text, re.I):
                text = re.sub(r"(<head\b[^>]*>)", lambda match: match[1] + link, text, count=1, flags=re.I)
            else:
                text = "<head>" + link + "</head>" + text
        if not head.redirect and (not head.canonical or head.canonical == url):
            urls.add(url)
        page.write_text(text)
        pages += 1
    for pdf in (root / "reading").glob("*.pdf"):
        urls.add(ORIGIN + "/" + pdf.relative_to(root).as_posix())
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    sitemap = ET.Element("{" + namespace + "}urlset")
    for url in sorted(urls):
        node = ET.SubElement(sitemap, "{" + namespace + "}url")
        ET.SubElement(node, "{" + namespace + "}loc").text = url
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(root / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    return {"html_pages": pages, "sitemap_urls": len(urls)}


if __name__ == "__main__":
    print(update_search_index(Path(__file__).resolve().parents[1] / "dist"))
