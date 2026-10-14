"""Public reading edition and comments; source collaboration lives on GitHub."""


def comment_section(english=False, kind='YinYang'):
    def t(zh, en):
        return en if english else zh
    heading = t('点歌与投稿', 'Song requests and submissions') if kind == 'Singing' else t('评论', 'Comments')
    return f'''<details id="{'advice' if kind == 'Advice' else 'comments'}" class="repository-tool comment-section">
<summary>{heading}</summary>
<div class="comment-content">
<p class="section-note">{t('用 GitHub 登录后，可以在这里留言和回复。讨论公开显示，中英文页面共享。', 'Sign in with GitHub to comment and reply here. Discussions are public and shared across languages.')}</p>
<div class="giscus" data-giscus-kind="{kind}" data-giscus-language="{'en' if english else 'zh-CN'}"></div>
<p class="section-note"><a data-github-discussion href="https://github.com/boluopai-net/Prometheus2Heraclitus/discussions">{t('也可以在 GitHub 讨论区交流', 'You can also join the discussion on GitHub')}</a></p>
</div></details>'''


def comments(english=False, kind='YinYang'):
    return f'''<!-- COMMENTS START --><div class="repository-tools" data-repository-tools data-feedback-kind="{kind}" data-language="{'en' if english else 'zh-CN'}">{comment_section(english, kind)}</div><!-- COMMENTS END -->'''


def with_comments(page, english=False, kind='YinYang'):
    import re
    page = re.sub(r'<!-- COMMENTS START -->[\s\S]*?<!-- COMMENTS END -->', '', page)
    page = page.replace('<script defer src="/repository.js"></script>', '<script type="module" src="/repository.js"></script>')
    for asset in ('<link rel="stylesheet" href="/repository.css">', '<script type="module" src="/repository.js"></script>', '<script type="module" src="/giscus-comments.js"></script>'):
        if asset not in page:
            page = page.replace('</head>', asset + '</head>')
    return page.replace('</main>', comments(english, kind) + '</main>', 1)


def panel(english=False):
    def t(zh, en):
        return en if english else zh

    return f'''<div class="repository-tools" data-repository-tools data-language="{'en' if english else 'zh-CN'}">
<section class="repository-tool" aria-labelledby="files-title">
<h2 id="files-title">{t('浏览文件', 'Browse files')}</h2>
<p class="section-note">{t('按文件夹浏览这份公开阅读版本。', 'Explore folders in this public reading edition.')}</p>
<label for="file-search">{t('查找文件', 'Find a file')}</label><input id="file-search" type="search" placeholder="{t('文件名或路径', 'Filename or path')}" autocomplete="off">
<nav class="file-breadcrumb" aria-label="{t('文件夹路径', 'Folder path')}" data-file-breadcrumb></nav>
<p class="repo-status" role="status" data-file-status></p><ul class="file-list" data-file-list></ul>
<noscript><p>{t('文件浏览需要 JavaScript；也可以使用上方阅读入口。', 'File browsing requires JavaScript; the reading link above remains available.')}</p></noscript>
</section>
{comment_section(english, 'Advice')}
</div>'''
