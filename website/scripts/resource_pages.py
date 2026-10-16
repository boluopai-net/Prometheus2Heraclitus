"""Resource overview and its dedicated Skills and file-browser destinations."""
from public_skill_pages import GITHUB, cards
from repository_panel import comments, file_browser


def render(dist, shell):
    entries = [
        ('getting-started', '工具使用', 'Using the Tools', 'axe.svg',
         '从订阅、全局提示词和搜索起步，接通母语阅读、个人哲学、Web 与本地、云盘和配置仓库。',
         'Begin with a subscription, global instructions, and search. Connect native-language reading, personal philosophy, Web and local work, Drive, and configuration.'),
        ('repositories/prometheus', '文档与图示', 'Documents & diagrams', 'document-diagram.svg',
         '按问题查阅哲学文档与来源，通过交互图示理解其中的关系。',
         'Consult philosophical documents and sources by question, and explore their relationships through interactive diagrams.'),
        ('skills', 'Skills', 'Skills', 'skills-wheel.svg',
         '浏览研究、教学、创作和环境维护等方法，了解各自用途与配套资源。',
         'Explore methods for research, teaching, creation, and environment maintenance, with their purposes and supporting resources.'),
        ('repositories/files', '浏览文件', 'Browse files', 'folder.svg',
         '按文件夹查看公开阅读版，搜索文件名或路径，打开需要的文档。',
         'Explore the public reading edition by folder, search filenames or paths, and open the documents you need.'),
    ]
    for english in (False, True):
        def t(zh, en): return en if english else zh
        suffix = 'en/' if english else ''
        lang = 'en' if english else 'zh-CN'
        def write(route, title, body, extra=''):
            target = dist / route / suffix / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(shell(title, body, lang, extra=extra))
        overview = ''.join(
            f'<section class="repository-entry"><div class="section-heading"><h2><a href="/{route}/{suffix}" data-page-title>{t(zh, en)}</a></h2><img class="motif" src="/motifs/{motif}" alt="" aria-hidden="true"></div><p class="entry-summary">{t(description_zh, description_en)}</p></section>'
            for route, zh, en, motif, description_zh, description_en in entries
        )
        overview += f'<section class="repository-entry"><div class="section-heading"><h2><a href="{GITHUB}">GitHub</a></h2></div></section>'
        body = f'<main id="main" class="wrap collection"><div class="collection-heading"><img class="motif collection-motif" src="/motifs/notebook.svg" alt="" aria-hidden="true"><h1>{t("资料与建议", "Resources & Advice")}</h1><p class="collection-intro">{t("思想走向实践，留下可以继续生长的造物。", "Thought becomes practice, leaving creations that can keep growing.")}</p></div>{overview}{comments(english, "Advice")}</main>'
        write('repositories', t('资料与建议', 'Resources & Advice'), body,
              '<link rel="stylesheet" href="/repository.css"><script type="module" src="/giscus-comments.js"></script>')
        back = f'<a class="back" href="/repositories/{suffix}">{t("← 资料与建议", "← Resources and suggestions")}</a>'
        skill_body = f'<main id="main" class="wrap collection"><div class="collection-heading"><img class="motif collection-motif" src="/motifs/skills-wheel.svg" alt="" aria-hidden="true">{back}<h1>Skills</h1><p class="collection-intro">{t("选择适合当前工作的工具与方法。", "Choose tools and methods for the work at hand.")}</p></div>{cards(english)}</main>'
        write('skills', 'Skills', skill_body)
        file_body = f'<main id="main" class="wrap collection"><div class="collection-heading"><img class="motif collection-motif" src="/motifs/folder.svg" alt="" aria-hidden="true">{back}<h1 id="files-title">{t("浏览文件", "Browse files")}</h1></div>{file_browser(english)}</main>'
        write('repositories/files', t('浏览文件', 'Browse files'), file_body,
              '<link rel="stylesheet" href="/repository.css"><script type="module" src="/repository.js"></script>')
