"""Resource overview and its dedicated Skills destinations."""
from public_skill_pages import GITHUB, SKILLS, reading_groups
from skill_wheel import badge, wheel, thumbnail
from repository_panel import comments


def render(dist, shell):
    entries = [
        ('getting-started', '工具使用', 'Using the Tools', 'axe.svg',
         '从订阅、全局提示词和搜索起步，接通母语阅读、个人哲学、Web 与本地、云盘和配置仓库。',
         'Begin with a subscription, global instructions, and search. Connect native-language reading, personal philosophy, Web and local work, Drive, and configuration.'),
        ('research-learning', '科研与学习', 'Research and Learning', 'graduation-cap.svg',
         '认识 Scientific Agents、Scientific Agent Skills 等科研仓库，以及两个老师怎样辅助研究与教学。',
         'Explore Scientific Agents, Scientific Agent Skills, further research repositories, and two teachers for research and learning.'),
        ('psychology', '心理', 'Psychology', 'notebook.svg',
         '让模型查找和整理相关材料，协助量表计分与统计，并准备实际支持和专业求助。',
         'Ask models to find and organize relevant materials, check questionnaire scores and statistics, and prepare practical support and access to professional care.'),
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
                artwork = thumbnail(english, SKILLS)
                artwork = f'<a class="skills-wheel-link" href="/skills/{suffix}" aria-label="{t("打开 Skills 页面", "Open the Skills page")}">{artwork}</a>'
            return f'<section class="repository-entry"><div class="section-heading"><h2><a href="/{route}/{suffix}" data-page-title>{t(zh, en)}</a></h2>{artwork}</div><p class="entry-summary">{t(description_zh, description_en)}</p></section>'
        overview = ''.join(render_entry(*entry) for entry in entries)
        overview += f'<section class="repository-entry"><div class="section-heading"><h2><a href="{GITHUB}">GitHub</a></h2></div></section>'
        body = f'<main id="main" class="wrap collection"><div class="collection-heading"><img class="motif collection-motif" src="/motifs/notebook.svg" alt="" aria-hidden="true"><h1>{t("资料与建议", "Resources & Advice")}</h1><p class="collection-intro">{t("思想走向实践，留下可以继续生长的造物。", "Thought becomes practice, leaving creations that can keep growing.")}</p></div>{overview}{comments(english, "Advice")}</main>'
        write('repositories', t('资料与建议', 'Resources & Advice'), body,
              '<link rel="stylesheet" href="/repository.css"><script type="module" src="/giscus-comments.js"></script>')
        back = f'<a class="back" href="/repositories/{suffix}">{t("← 资料与建议", "← Resources and suggestions")}</a>'
        yinyang_source = '/repositories/prometheus/source/skills/yinyang/SKILL' + ('.html' if english else '.zh-CN.html')
        yinyang = f'''<section class="library-section"><h2><a href="{yinyang_source}">{t("阴阳", "Yinyang")}</a></h2><p class="section-note">{t("从理解自己、模型与彼此的关系出发，把个人哲学、协作方式和工具环境连成可以持续修订的实践。", "Begin with understanding yourself, the model, and your relationship. Connect personal philosophy, collaboration, and the tool environment into a practice that can keep evolving.")}</p></section>'''
        wheel_speed = f'''<div class="skills-wheel-speed"><button type="button" class="skills-wheel-motion" data-wheel-motion role="switch" aria-checked="true" aria-label="{t("转盘动态效果", "Wheel motion")}">{t("动态效果：开", "Motion: On")}</button><label for="skills-wheel-speed">{t("转速", "Speed")}</label><output data-wheel-speed-output>{t("10 圈/秒", "10 rotations / sec")}</output><div class="skills-wheel-speed-line"><span aria-hidden="true">{t("慢", "Slow")}</span><input id="skills-wheel-speed" data-wheel-speed type="range" min="0" max="100" step="any" value="100" aria-label="{t("转盘转速", "Wheel speed")}" aria-valuetext="{t("0.1 秒/圈", "0.1 seconds per rotation")}"><span aria-hidden="true">{t("快", "Fast")}</span></div></div>'''
        yinyang = yinyang.replace('<section class="library-section">', '<section class="library-section" data-skill="yinyang">').replace(f'href="{yinyang_source}">', f'href="{yinyang_source}">{badge("yinyang")}')
        draw = f'<button type="button" class="skills-wheel-draw" data-wheel-draw>{t("抽选并打开", "Spin & open a Skill")}</button><p class="skills-wheel-result" data-wheel-result role="status" aria-live="polite">{t("每格对应下方同图标的 Skill，停稳后自动打开。", "Each symbol matches a Skill below. The selected Skill opens after the wheel stops.")}</p>'
        skill_body = f'<main id="main" class="wrap collection"><div class="collection-heading skills-wheel-heading">{wheel(english, SKILLS, yinyang_source)}{wheel_speed}<div class="skills-wheel-intro">{back}<h1>Skills</h1><p class="collection-intro">{t("选择适合当前工作的工具与方法。", "Choose tools and methods for the work at hand.")}</p>{draw}</div></div>{yinyang}{reading_groups(english)}</main>'
        write('skills', 'Skills', skill_body)
