"""Support paired bold delimiters beside CJK text without changing code spans."""
import re
from xml.etree import ElementTree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

CJK = re.compile(r'[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]')


class CjkStrong(InlineProcessor):
    def handleMatch(self, match, data):
        neighborhood = data[max(0, match.start() - 1):match.end() + 1]
        if not CJK.search(neighborhood):
            return None, None, None
        element = ElementTree.Element('strong')
        element.text = match.group(2)
        return element, match.start(), match.end()


class CjkBoldExtension(Extension):
    def extendMarkdown(self, md):
        # Links, escapes and code spans are processed before this rule.
        md.inlinePatterns.register(CjkStrong(
            r'(?<!\*)(\*\*)(?!\*)(?=\S)(.+?\S|\S)\1(?!\*)', md),
            'cjk_strong', 65)
