"""Shared reader-facing concept labels for HTML and PDF projections.

Philosopher names are authored from their actual use in the essays. This module
only realizes the established Chinese-concept spelling and brand labels.
"""
import re


CONCEPT_LABELS = {
    '阴阳': 'Yinyang', '太极': 'Taiji',
    '无极': 'Wuji', '无为': 'Wuwei', '两仪': 'Liangyi', '四象': 'Sixiang',
    '八卦': 'Bagua', '五行': 'Wuxing', '双鱼': 'Shuang yu', '生生': 'Shengsheng',
}
# These are the concept-bearing quotations and original title in the current
# classical-source passages. Quotation marks around an authored label alone
# do not turn that display label into an immutable source quotation.
QUOTATION = (r'((?:「|“)(?:一动一静，互为其根|万物生生，而变化无穷焉|'
             r'生生之谓易|阴阳之义配日月|日月相推而明生焉)(?:」|”)|太极图说|太極圖說)')


def reader_text(value):
    """Change display labels while leaving quoted wording intact."""
    pieces = re.split(QUOTATION, value)
    for index in range(0, len(pieces), 2):
        text = pieces[index].replace('菠萝派', 'boluopai')
        text = text.replace('生生不息的转化', 'Shengsheng 与持续转化')
        text = text.replace('将易与生生相连', '将 Yi 与 Shengsheng 相连')
        for original, label in CONCEPT_LABELS.items():
            text = text.replace(original, label)
        text = re.sub(r'(?<![A-Za-z])(?:yinyang|YinYang)(?![A-Za-z])', 'Yinyang', text)
        pieces[index] = text.replace('Yinyang · Yinyang', 'Yinyang')
    return ''.join(pieces)


def reader_names(text):
    """Apply display names to HTML text and accessible labels, not link targets."""
    protected = (r'(<(?P<verbatim>pre|code|script|style|textarea|blockquote)\b[^>]*>'
                 r'[\s\S]*?</(?P=verbatim)\s*>|<!--[\s\S]*?-->|<[^>]+>|'
                 + QUOTATION + ')')
    chunks, start = [], 0
    for match in re.finditer(protected, text, re.I):
        chunks.append(reader_text(text[start:match.start()]))
        token = match[0]
        if token.startswith('<') and not match.group('verbatim') and not token.startswith('<!--'):
            token = re.sub(r'((?<![\w:-])(?:title|alt|aria-label)=["\'])(.*?)(["\'])',
                           lambda m: m[1] + reader_text(m[2]) + m[3], token)
            if re.match(r'<meta\b', token, re.I) and re.search(
                    r'\b(?:name|property)=["\'](?:description|og:title|og:description|twitter:title|twitter:description|application-name)["\']',
                    token, re.I):
                token = re.sub(r'(\bcontent=["\'])(.*?)(["\'])',
                               lambda m: m[1] + reader_text(m[2]) + m[3], token)
        chunks.append(token)
        start = match.end()
    chunks.append(reader_text(text[start:]))
    return ''.join(chunks)


def reader_document(node):
    """Name Pandoc reader text after source anchors and figure positions resolve."""
    if isinstance(node, list):
        return [reader_document(item) for item in node]
    if not isinstance(node, dict):
        return node
    kind = node.get('t')
    if kind in {'Code', 'CodeBlock', 'Math', 'RawInline', 'RawBlock', 'BlockQuote', 'Quoted'}:
        return node
    if kind == 'Str':
        return {**node, 'c': reader_text(node['c'])}
    return {key: reader_document(value) for key, value in node.items()}
