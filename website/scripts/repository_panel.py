"""Public reading edition and comments; source collaboration lives on GitHub."""


def comment_section(english=False, kind='YinYang'):
    def t(zh, en):
        return en if english else zh
    heading = t('点歌与投稿', 'Song requests and submissions') if kind == 'Singing' else t('评论', 'Comments')
    section_id = 'advice' if kind == 'Advice' else 'comments'
    return f'''<section id="{section_id}" class="repository-tool comment-section" aria-labelledby="{section_id}-title">
<h2 id="{section_id}-title">{heading}</h2>
<div class="comment-content">
<div class="giscus" data-giscus-kind="{kind}" data-giscus-language="{'en' if english else 'zh-CN'}"></div>
</div></section>'''


def comments(english=False, kind='YinYang'):
    return f'''<!-- COMMENTS START --><div class="repository-tools" data-repository-tools data-feedback-kind="{kind}" data-language="{'en' if english else 'zh-CN'}">{comment_section(english, kind)}</div><!-- COMMENTS END -->'''


def with_comments(page, english=False, kind='YinYang'):
    import re
    page = re.sub(r'<!-- COMMENTS START -->[\s\S]*?<!-- COMMENTS END -->', '', page)
    page = re.sub(r'<script\b[^>]*src="/repository\.js"[^>]*></script>', '', page)
    for asset in ('<link rel="stylesheet" href="/repository.css">', '<script type="module" src="/giscus-comments.js"></script>'):
        if asset not in page:
            page = page.replace('</head>', asset + '</head>')
    # The philosophy overview keeps discussion in its reading column. Every
    # renderer uses this placement so a later refresh cannot undo it.
    if kind == 'Philosophy' and re.search(r'<main\b[^>]*\bbook-introduction\b', page):
        return page.replace('</article>', comments(english, kind) + '</article>', 1)
    return page.replace('</main>', comments(english, kind) + '</main>', 1)
