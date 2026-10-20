"""Resource overview and its dedicated Skills destinations."""
from public_skill_pages import GITHUB, reading_groups
from repository_panel import comments


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
    ]
    for english in (False, True):
        def t(zh, en): return en if english else zh
        suffix = 'en/' if english else ''
        lang = 'en' if english else 'zh-CN'
        def write(route, title, body, extra=''):
            target = dist / route / suffix / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(shell(title, body, lang, extra=extra))
        def render_entry(route, zh, en, motif, description_zh, description_en):
            artwork = f'<img class="motif" src="/motifs/{motif}" alt="" aria-hidden="true">'
            if route == 'skills':
                artwork = f'<a class="skills-wheel-link" href="/skills/{suffix}" aria-label="{t("打开 Skills 页面", "Open the Skills page")}">{artwork}</a>'
            return f'<section class="repository-entry"><div class="section-heading"><h2><a href="/{route}/{suffix}" data-page-title>{t(zh, en)}</a></h2>{artwork}</div><p class="entry-summary">{t(description_zh, description_en)}</p></section>'
        overview = ''.join(render_entry(*entry) for entry in entries)
        overview += f'<section class="repository-entry"><div class="section-heading"><h2><a href="{GITHUB}">GitHub</a></h2></div></section>'
        body = f'<main id="main" class="wrap collection"><div class="collection-heading"><img class="motif collection-motif" src="/motifs/notebook.svg" alt="" aria-hidden="true"><h1>{t("资料与建议", "Resources & Advice")}</h1><p class="collection-intro">{t("思想走向实践，留下可以继续生长的造物。", "Thought becomes practice, leaving creations that can keep growing.")}</p></div>{overview}{comments(english, "Advice")}</main>'
        write('repositories', t('资料与建议', 'Resources & Advice'), body,
              '<link rel="stylesheet" href="/repository.css"><script type="module" src="/giscus-comments.js"></script>')
        back = f'<a class="back" href="/repositories/{suffix}">{t("← 资料与建议", "← Resources and suggestions")}</a>'
        yinyang_source = '/repositories/prometheus/source/skills/yinyang/SKILL' + ('.html' if english else '.zh-CN.html')
        yinyang = f'''<section class="library-section"><h2><a href="{yinyang_source}">{t("阴阳", "Yinyang")}</a></h2><p class="section-note">{t("从理解自己、模型与彼此的关系出发，把个人哲学、协作方式和工具环境连成可以持续修订的实践。阴阳提供整体方向，下面的专项 Skills 支持具体工作。", "Begin with understanding yourself, the model, and your relationship. Connect personal philosophy, collaboration, and the tool environment into a practice that can keep evolving. Yinyang provides the overall direction; the specialist Skills below support particular work.")}</p><ul class="library-purpose-links"><li><a href="{yinyang_source}">{t("阴阳 Skill", "Yinyang Skill")}</a><p>{t("阅读完整方法入口，理解、采用或形成自己的协作安排。", "Read the complete method to understand, adopt, or form your own collaborative arrangement.")}</p></li><li><a href="/getting-started/{suffix}" data-page-title>{t("工具使用", "Using the Tools")}</a><p>{t("把协作落实到客户端、提示词、Skills 与工具环境。", "Put collaboration into practice through clients, instructions, Skills, and tools.")}</p></li><li><a href="/repositories/prometheus/{suffix}" data-page-title>{t("文档与图示", "Documents & diagrams")}</a><p>{t("继续阅读阴阳的哲学、形成方法与关系图示。", "Explore Yinyang’s philosophy, formation methods, and diagrams of their relationships.")}</p></li></ul></section>'''
        skill_body = f'<main id="main" class="wrap collection"><div class="collection-heading skills-wheel-heading"><img class="motif" src="/motifs/skills-wheel.svg" alt="" aria-hidden="true"><div class="skills-wheel-intro">{back}<h1>Skills</h1><p class="collection-intro">{t("选择适合当前工作的工具与方法。", "Choose tools and methods for the work at hand.")}</p></div></div>{yinyang}{reading_groups(english)}</main>'
        write('skills', 'Skills', skill_body)
