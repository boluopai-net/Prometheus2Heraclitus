"""Public reading edition and comments; source collaboration lives on GitHub."""


def comment_section(english=False, kind='YinYang'):
    def t(zh, en):
        return en if english else zh
    subject = {'YinYang': t('阴阳方法与阅读', 'YinYang method and reading'),
               'Philosophy': t('哲学', 'Philosophy'),
               'Advice': t('资料', 'Resources'),
               'Singing': t('唱歌', 'Singing')}[kind]
    heading = t('点歌与投稿', 'Song requests and submissions') if kind == 'Singing' else t('评论', 'Comments')
    return f'''<details id="{'advice' if kind == 'Advice' else 'comments'}" class="repository-tool comment-section">
<summary>{heading}</summary>
<div class="comment-content">
<p class="section-note">{t('在这里交流「' + subject + '」的内容。评论会公开显示。', 'Discuss ' + subject + ' here. Comments are public.')}</p>
<p class="repo-status" role="status" data-suggestion-list-status></p><div data-suggestion-list></div><button type="button" data-more-suggestions hidden>{t('更多评论', 'More comments')}</button>
<h3>{t('写评论', 'Write a comment')}</h3>
<form data-suggestion-form class="repo-form">
<label>{t('标题', 'Title')}<input name="title" maxlength="200" required></label>
<label>{t('内容', 'Comment')}<textarea name="body" rows="5" maxlength="10000" required></textarea></label>
<label>{t('署名（可选）', 'Name (optional)')}<input name="author" maxlength="100" autocomplete="nickname"></label>
<label class="repo-honeypot" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
<p class="section-note">{t('请勿填写私人信息。提交后可以删除自己的评论，并保存私人删除链接，换设备也能使用。', 'Please leave out private information. After submitting, you can delete your comment and save a private deletion link for use on another device.')}</p>
<button type="submit">{t('提交评论', 'Submit comment')}</button><p class="repo-status" role="status" data-form-status></p>
</form></div></details>'''


def comments(english=False, kind='YinYang'):
    return f'''<!-- COMMENTS START --><div class="repository-tools" data-repository-tools data-feedback-kind="{kind}" data-language="{'en' if english else 'zh-CN'}">{comment_section(english, kind)}</div><!-- COMMENTS END -->'''


def with_comments(page, english=False, kind='YinYang'):
    import re
    page = re.sub(r'<!-- COMMENTS START -->[\s\S]*?<!-- COMMENTS END -->', '', page)
    page = page.replace('<script defer src="/repository.js"></script>', '<script type="module" src="/repository.js"></script>')
    for asset in ('<link rel="stylesheet" href="/repository.css">', '<script type="module" src="/repository.js"></script>'):
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
