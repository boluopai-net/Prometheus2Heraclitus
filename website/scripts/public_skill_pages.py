"""Bilingual public Skill introductions with GitHub source/download links."""
import html

GITHUB = "https://github.com/boluopai-net/Prometheus2Heraclitus"

SKILLS = {
    'random-wheel': (
        '抽卡转盘', 'random-wheel',
        '把截图或明确给出的选项变成可调速的动画转盘，以等概率随机抽选。',
        'Turn screenshot choices or named options into a speed-adjustable animated wheel with equal-probability random selection.',
        '想从课程、活动或其他备选项中随机抽一个时使用。速度只改变动画；重新抽选才会产生新结果。',
        'Use it to pick a course, activity, or another supplied option by chance. Speed changes the animation; a reroll creates a new draw.',
        '包内包含 Python 渲染脚本与 HTML 模板。需要 Python 3 和现代浏览器，无额外 Python 依赖；可生成离线 HTML。',
        'Includes the Python renderer and HTML templates. Requires Python 3 and a modern browser, with no extra Python dependencies; produces offline HTML.'),
    'research': (
        '搜索与研究', 'Research',
        '调查事实、产品行为与方案，把来源、观察、假设和覆盖限制放在同一个可检查的回答中。',
        'Investigate facts, product behavior, and alternatives with inspectable sources, observations, assumptions, and coverage limits.',
        '需要核实某个功能是否支持、比较现有方案，或理解一段时间内发生了什么变化时使用。',
        'Use it to verify support for a workflow, compare existing approaches, or understand what changed over a period.',
        '包含完整方法入口与中英文使用说明。可调查提供的本地材料；外部事实需要客户端实际可用的搜索或浏览工具。包本身不安装工具或配置凭据。',
        'Includes the complete method and bilingual guides. It can investigate supplied local material; external claims require search or browser tools available in your client. The package installs no tools or credentials.'),
    'task-inquiry': (
        '任务探究', 'Task Inquiry',
        '从实际分歧、证据和有用的问题出发，澄清会改变任务下一步的关键不确定性。',
        'Clarify consequential uncertainty through real tensions, evidence, reasoning, and useful questions.',
        '结果与预期不一致、解释互相冲突，或存在会影响行动的重要选择时使用。清楚且已确定的任务可以直接执行。',
        'Use it when results differ from expectations, explanations conflict, or a meaningful choice changes the next action. Clear, settled work can proceed directly.',
        '包含独立方法入口与中英文使用说明，无脚本、必需的配套框架或服务集成。',
        'Includes the standalone method and bilingual guides, with no scripts, required companion framework, or service integration.'),
    'prompt-and-skill-lifecycle': (
        '提示词与技能生命周期', 'Prompt and Skill Lifecycle',
        '把指令的含义、维护责任、交付方式和实际使用证据连在一起，编写、审查与维护 Prompt 和 Skill。',
        'Connect instruction meaning, ownership, delivery, and evidence of use when authoring, auditing, and maintaining Prompts and Skills.',
        '编写或改写指令、审查职责冲突、调整 Skill 包，或核实发布后的消费者是否能发现并使用它时使用。',
        'Use it to draft or revise instructions, audit conflicting ownership, adapt a Skill package, or verify that its published consumer can discover and use it.',
        '包含方法入口、中英文说明与完整参考资源。按当前动作选择资源，不依赖作者的电脑、私人文档或阴阳包。',
        'Includes the entrypoint, bilingual guides, and complete reference resources. Select resources for the current action; no dependency on the author’s computer, private documents, or YinYang package.'),
}

ADDITIONAL_SKILLS = [
    ('android-control', '安卓手机控制', 'Android control',
     '通过 ADB 与原生界面操作自己的安卓设备，并核实实际效果。', 'Operate your Android device through ADB and native interfaces, verifying actual effects.',
     '手机应用操作、文件管理和连接排查。需要已授权连接的设备；安装 Skill 不会授予设备访问。', 'App operation, file management, and connection diagnosis. Requires an authorized connected device; installing a Skill grants no device access.'),
    ('personal-environment-design', '个人环境设计', 'Personal environment design',
     '从人的理解与操作出发，组织网站、桌面和跨工具工作方式。', 'Organize websites, desktops, and cross-tool work around human understanding and action.',
     '减少来回导航与操作负担；保留整体、重要关系和实际使用反馈。', 'Reduce navigation and operational burden while retaining the whole, important relationships, and feedback from use.'),
    ('model-upgrade-check', '模型升级检查', 'Model upgrade checks',
     '核对可用模型、用途分配与实际消费者，让升级保持一致。', 'Reconcile available models, purpose-specific selections, and actual consumers.',
     '模型或应用更新时使用。先核对实际账号、提供者与消费者；不凭版本名猜测能力。', 'Use when models or applications change. Inspect the account, provider, and consumer rather than guessing capability from version names.'),
    ('paper-retrieval', '论文与学术书籍检索', 'Paper and book retrieval',
     '核对题录、版本与全文，把搜索结果交付为可验证的学术材料。', 'Reconcile bibliography, editions, and full text to deliver verifiable scholarly material.',
     '找论文、作者文献或学术书籍。配合 research；认证浏览与连接诊断按需使用 browser-relay、network。', 'Find papers, author bibliographies, or scholarly books. Use research, with browser-relay and network when authenticated browsing or connection diagnosis is needed.'),
    ('video-subtitle', '视频字幕提取', 'Video subtitles',
     '取得带来源与时间线的视频讲话文本，再回到原视频核对。', 'Retrieve source-linked, timed spoken text and check it against the original video.',
     '分析 YouTube、Bilibili 视频的讲话内容。实际抓取需要 yt-dlp；字幕不替代声音和画面。', 'Analyze speech in YouTube or Bilibili videos. Retrieval needs yt-dlp; subtitles do not replace sound and images.'),
    ('singing', '练唱', 'Singing practice',
     '准备伴奏、录音与参考表演，把听辨和音频证据用于练唱。', 'Prepare accompaniment, recordings, and reference performances for evidence-based singing practice.',
     '准备 KTV、比较演唱或操作录音软件。Logic Pro 与其他音频工具按实际能力接入。', 'Prepare karaoke, compare performances, or operate recording software. Bind Logic Pro or other audio tools only where available.'),
    ('local-teacher', '本地老师', 'Local teacher',
     '在本地环境中讲解、复习、练习，并通过真实工作发展理解。', 'Explain, review, and practice in a local environment, developing understanding through real work.',
     '与 web-teacher 成组使用，保留整体感、直觉、多模态表达与材料和读者的关系。', 'Use with web-teacher, preserving the whole, intuition, multimodal expression, and the relationship between materials and the reader.'),
    ('web-teacher', '云端老师', 'Web teacher',
     '提供课程材料、教学方法、学习路径与学习空间的共同方法。', 'Provide shared methods for course material, teaching, learning paths, and learning spaces.',
     '与 local-teacher 共享教学方法。学习记录与材料由使用者自己的环境提供。', 'Share teaching methods with local-teacher. The recipient supplies their own learning records and materials.'),
    ('shopping', '购物与比价', 'Shopping and comparison',
     '比较商品、价格、优惠与二手选择，保留实际证据与条件。', 'Compare products, prices, offers, and secondhand choices with inspectable evidence and conditions.',
     '国内电商与闲鱼调查；按需要配置包中声明的搜索或购物工具，不随包提供账号。', 'Research Chinese marketplaces and secondhand listings; configure the declared search or shopping tools as needed. Accounts are not included.'),
    ('prompt-audit-orchestration', '提示词审计', 'Prompt audit orchestration',
     '按实际范围审查学习、工作、Web 与自动化的指令和执行关系。', 'Audit instructions and execution relationships across learning, work, Web, and automation within the requested scope.',
     '与生命周期、研究、任务探究等方法协同；检查受影响的执行链，不机械遍历整个环境。', 'Combine lifecycle, research, and task-inquiry methods; examine affected execution chains rather than mechanically scanning an entire environment.'),
    ('agent-orchestration-master', '多智能体协作', 'Agent orchestration',
     '按实际工作拆分贡献、交接和依赖，并由任务所有者整合结果。', 'Organize contributions, handoffs, and dependencies around actual work, with the task owner integrating results.',
     '独立贡献确实有帮助时使用。宿主提供模型、调度与权限，Skill 不自带运行平台。', 'Use when independent contributions help. The host supplies models, dispatch, and authority; the Skill is not a runtime platform.'),
    ('browser-relay', '浏览器会话', 'Browser sessions',
     '管理任务专用浏览器、认证会话、目标归属与清理。', 'Manage task-owned browsers, authenticated sessions, target ownership, and cleanup.',
     '需要持续登录或隔离浏览时使用。使用者配置自己的浏览器载体，私人会话不随包分发。', 'Use for retained login or isolated browsing. Recipients configure their own browser carrier; private sessions are never distributed.'),
    ('obsidian-sync', '笔记同步', 'Obsidian synchronization',
     '维护多个 Obsidian 库的共同配置、云端复制与同步。', 'Maintain shared configuration, cloud copies, and synchronization across Obsidian vaults.',
     '先绑定自己的库、共享配置与同步方向，再预览并验证；不附带作者的笔记或库清单。', 'Bind your vaults, shared configuration, and synchronization directions, then preview and verify. Author notes and vault lists are not included.'),
    ('chezmoi', '系统配置持久化', 'Configuration persistence',
     '把授权的本机配置变更保存到源码，并通过实际发布机制接回环境。', 'Persist authorized host configuration changes in source and converge them through the actual publication mechanism.',
     '需要自己的 chezmoi 源仓库与发布责任方；先配置这些关系，再持久化和核对。', 'Requires your own chezmoi source repository and publication owner. Configure those relationships before persistence and readback.'),
    ('network', '网络诊断', 'Network diagnosis',
     '通过本机证据排查 DNS、代理、网站连接和路由问题。', 'Diagnose DNS, proxies, website connectivity, and routing from host evidence.',
     '使用自己的探测目标与网络配置；涉及节点切换时配合 clash-auto-switch，改变后核对真实连接。', 'Use your own probe targets and network configuration; combine clash-auto-switch when node switching is needed and verify connectivity after changes.'),
    ('clash-auto-switch', '节点自动切换', 'Proxy node switching',
     '维护 Clash 节点选择、地区回退与 DNS/TUN 保护。', 'Maintain Clash node selection, regional fallback, and DNS/TUN protection.',
     '需要自己配置的 Clash 控制器、组名、凭据引用与运行目录。包中没有订阅或作者的节点。', 'Requires your configured Clash controller, groups, credential references, and runtime paths. No subscription or author nodes are included.'),
]
for name, zh, en, description_zh, description_en, use_zh, use_en in ADDITIONAL_SKILLS:
    SKILLS[name] = (zh, en, description_zh, description_en, use_zh, use_en,
                   '包含完整方法及配置说明；具体资源、脚本、配套 Skill 与外部工具见包内 README。保留配套关系，按需安装相关包，并绑定自己的环境。',
                   'Includes the method and configuration guidance. The package README specifies resources, scripts, companion Skills, and external tools. Install relevant companions and bind your own environment.')


def cards(english=False):
    index = 1 if english else 0
    items = []
    for name, info in SKILLS.items():
        route = '/tools/' + name + ('/en/' if english else '/')
        items.append(f'<article class="repository-entry skill-summary"><h3><a href="{route}">{html.escape(info[0])} · {name}</a></h3><p>{html.escape(info[2 + index])}</p><p><a class="text-link" href="/install/{"en/" if english else ""}?skill={name}">{"Install in Codex" if english else "安装到 Codex"} ↗</a></p></article>')
    note = ('These methods retain useful companion relationships. Read each package’s dependencies, install the needed companions, and configure your own environment. Package licenses remain MIT.' if english else '这些方法保留有用的配套关系。先读各包依赖说明，按需安装配套 Skill，再配置自己的环境；包内保留 MIT 许可。')
    return '<section class="library-section"><h2>' + ('Reusable Skills and their companions' if english else '可复用的 Skills 与配套关系') + '</h2><p class="section-note">' + note + '</p>' + ''.join(items) + '</section>'


def render_pages(dist, shell, revision):
    for name, info in SKILLS.items():
        for english in (False, True):
            i = 1 if english else 0
            def t(zh, en):
                return en if english else zh
            route = '/tools/' + name + ('/' if english else '/en/')
            title = info[0] + ' · ' + name
            example = {
                'random-wheel': t('“从这些选项中随机抽一个，用转盘展示。”', '“Randomly pick one of these options and show a wheel.”'),
                'research': t('“调查这个产品今天是否支持我的工作流程，并比较可用方案与证据。”', '“Investigate whether this product supports my workflow today, comparing available approaches and evidence.”'),
                'task-inquiry': t('“这份报告和仪表盘结果不同，找出能解释差异的证据。”', '“This report differs from the dashboard; find evidence that can explain the discrepancy.”'),
                'prompt-and-skill-lifecycle': t('“审查这套 Skill 的指令、维护责任与交付，确认消费者能发现并使用它。”', '“Audit this Skill’s instructions, ownership, and delivery, and verify its consumer can discover and use it.”'),
            }.get(name, t('“请按这个 Skill 帮我处理当前任务，先核对需要的配套方法与实际工具。”', '“Use this Skill for my task, first checking the companion methods and actual tools it needs.”'))
            body = f'<main id="main" class="wrap library-reader"><div class="reader-top"><a class="back" href="/repositories/{"en/" if english else ""}">{t("← 资料与建议", "← Resources and suggestions")}</a><a class="language-link" href="{route}">{t("English", "中文")}</a></div><article class="document"><p class="eyebrow">SKILL · MIT</p><h1>{html.escape(title)}</h1><p class="collection-intro">{html.escape(info[2 + i])}</p><p><a class="outline-button" href="/install/{"en/" if english else ""}?skill={name}">{t("安装到 Codex ↗", "Install in Codex ↗")}</a> <a class="text-link" href="{GITHUB}/tree/main/skills/{name}">{t("GitHub 源码", "GitHub source")}</a></p><h2>{t("何时使用", "When to use it")}</h2><p>{html.escape(info[4 + i])}</p><blockquote><p>{html.escape(example)}</p></blockquote><h2>{t("包里有什么", "What is included")}</h2><p>{html.escape(info[6 + i])}</p><h2>{t("安装到 Codex", "Install in Codex")}</h2><p>{t("打开安装页，把指令复制给 Codex，它会从 boluopai 插件市场安装完整包，无须手工下载 ZIP。", "Open the installation page and copy the request to Codex. It installs the complete package from the boluopai marketplace, without manual ZIP extraction.")}</p><p><a class="outline-button" href="/install/{"en/" if english else ""}?skill={name}">{t("复制安装指令 ↗", "Get installation request ↗")}</a></p><p>{t("按自然语言提出任务；客户端支持显式调用时，也可以指定", "Ask naturally; if the client supports explicit invocation, select")} <code>{name}</code>。{t("客户端已有的权限、认证和工具边界继续适用。", "The client’s existing authority, authentication, and tool boundaries remain in force.")}</p><h2>{t("许可", "License")}</h2><p>{t("本包采用 MIT 许可，允许使用、修改和再分发；请保留包内版权与许可声明。软件按原样提供。阴阳采用单独的 CC BY-NC-SA 4.0 许可；网站其他材料遵循各自说明。", "This package uses the MIT license, permitting use, modification, and redistribution while retaining the included copyright and license notices. It is provided as-is. YinYang has its separate CC BY-NC-SA 4.0 license; other website materials follow their own notices.")}</p></article></main>'
            target = dist / 'tools' / name / ('en' if english else '') / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(shell(title, body, 'en' if english else 'zh-CN').replace('<head>', '<head><meta name="robots" content="noindex, nofollow, noimageindex">', 1))
