"""Bilingual public Skill introductions with GitHub source/download links."""
import html
from skill_wheel import badge

GITHUB = "https://github.com/boluopai-net/Prometheus2Heraclitus"

SKILLS = {
    'yinyang': (
        '阴阳 Full', 'YinYang Full',
        '静态参考：查看网页哲学在 Skill 中的表达与组织形式。',
        'Static reference: inspect how the website’s philosophy is expressed and organized in a Skill.',
        '✗ 禁止用于他人的实践。Full 仅供静态参考；自己的实践从 Empty 开始。',
        '✗ Not for another person’s practice. Full is a static reference; start your own practice from Empty.',
        '包含日常协作入口、六份 formation 指南、参考文章、图示和更新脚本。',
        'Includes daily collaboration, six formation guides, reference essays, diagrams, and the common-update script.'),
    'yinyang-empty': (
        '阴阳 Empty', 'YinYang Empty',
        '保留反向对齐、阴阳辩证法与形成方法，留出自己的哲学、个人材料和实际工作模型。',
        'Keep reverse alignment, YinYang dialectics, and formation methods, with room for your own philosophy, personal material, and working accounts.',
        '想从共同核心、方法与空白结构出发，和模型形成自己的阴阳时选择。',
        'Choose Empty to develop your own YinYang with a model from shared core methods and an unfilled structure.',
        '六份 formation 指南、基本观点建议、实践总览、形成与修订、日常协作；另有四个空 Personal 分区和六份未填写的 Situated 文件。不含 docs、diagrams。',
        'Six formation guides, Core views as suggestions, practice overview, formation and revision, and daily collaboration; four empty Personal areas and six unfilled Situated files. No docs or diagrams.'),
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
        '包含完整方法入口与中英文使用说明。可调查提供的本地材料；外部事实需要客户端实际可用的搜索或浏览工具。',
        'Includes the complete method and bilingual guides. It can investigate supplied local material; external claims require search or browser tools available in your client.'),
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
        '包含方法入口、中英文说明与完整参考资源。按当前动作选择资源。',
        'Includes the entrypoint, bilingual guides, and complete reference resources. Select resources for the current action.'),
}

ADDITIONAL_SKILLS = [
    ('android-control', '安卓手机控制', 'Android control',
     '通过 ADB 与原生界面操作自己的安卓设备，并核实实际效果。', 'Operate your Android device through ADB and native interfaces, verifying actual effects.',
     '手机应用操作、文件管理和连接排查。需要已授权连接的设备。', 'App operation, file management, and connection diagnosis. Requires an authorized connected device.'),
    ('personal-environment-design', '个人环境设计', 'Personal environment design',
     '统筹提示词、Skills、MCP、插件、应用、自动化、服务与使用体验的配置。', 'Configure prompts, Skills, MCP, plugins, applications, automation, services, and human-facing use as a connected environment.',
     '安装、连接、替换或重组环境时使用；按需读取人的使用与 MCP 服务资源，验证从能力发现、连接到执行和实际结果的路径。', 'Use when installing, connecting, replacing, or reorganizing the environment; select human-use or MCP/service resources as needed and verify discovery, connection, execution, and actual results.'),
    ('model-upgrade-check', '模型升级检查', 'Model upgrade checks',
     '核对可用模型、用途分配与实际消费者，让升级保持一致。', 'Reconcile available models, purpose-specific selections, and actual consumers.',
     '模型或应用更新时使用。先核对实际账号、提供者与消费者。', 'Use when models or applications change. Inspect the account, provider, and consumer.'),
    ('paper-retrieval', '论文与学术书籍检索', 'Paper and book retrieval',
     '核对题录、版本与全文，把搜索结果交付为可验证的学术材料。', 'Reconcile bibliography, editions, and full text to deliver verifiable scholarly material.',
     '找论文、作者文献或学术书籍。配合 research；认证浏览与连接诊断按需使用 browser-relay、network。', 'Find papers, author bibliographies, or scholarly books. Use research, with browser-relay and network when authenticated browsing or connection diagnosis is needed.'),
    ('video-subtitle', '视频字幕提取', 'Video subtitles',
     '取得带来源与时间线的视频讲话文本，再回到原视频核对。', 'Retrieve source-linked, timed spoken text and check it against the original video.',
     '分析 YouTube、Bilibili 视频的讲话内容。实际抓取需要 yt-dlp。', 'Analyze speech in YouTube or Bilibili videos. Retrieval needs yt-dlp.'),
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
     '国内电商与闲鱼调查；按需要配置包中声明的搜索或购物工具。', 'Research Chinese marketplaces and secondhand listings; configure the declared search or shopping tools as needed.'),
    ('prompt-audit-orchestration', '提示词审计', 'Prompt audit orchestration',
     '按实际范围审查学习、工作、Web 与自动化的指令和执行关系。', 'Audit instructions and execution relationships across learning, work, Web, and automation within the requested scope.',
     '与生命周期、研究、任务探究等方法协同；检查受影响的执行链。', 'Combine lifecycle, research, and task-inquiry methods; examine affected execution chains.'),
    ('agent-orchestration-master', '多智能体协作', 'Agent orchestration',
     '按实际工作拆分贡献、交接和依赖，并由任务所有者整合结果。', 'Organize contributions, handoffs, and dependencies around actual work, with the task owner integrating results.',
     '独立贡献确实有帮助时使用。宿主提供模型、调度与权限。', 'Use when independent contributions help. The host supplies models, dispatch, and authority.'),
    ('browser-relay', '浏览器会话', 'Browser sessions',
     '管理任务专用浏览器、认证会话、目标归属与清理。', 'Manage task-owned browsers, authenticated sessions, target ownership, and cleanup.',
     '需要持续登录或隔离浏览时使用。使用者配置自己的浏览器载体。', 'Use for retained login or isolated browsing. Recipients configure their own browser carrier.'),
    ('obsidian-sync', '笔记同步', 'Obsidian synchronization',
     '维护多个 Obsidian 库的共同配置、云端复制与同步。', 'Maintain shared configuration, cloud copies, and synchronization across Obsidian vaults.',
     '先绑定自己的库、共享配置与同步方向，再预览并验证。', 'Bind your vaults, shared configuration, and synchronization directions, then preview and verify.'),
    ('chezmoi', '系统配置持久化', 'Configuration persistence',
     '把授权的本机配置变更保存到源码，并通过实际发布机制接回环境。', 'Persist authorized host configuration changes in source and converge them through the actual publication mechanism.',
     '需要自己的 chezmoi 源仓库与发布责任方；先配置这些关系，再持久化和核对。', 'Requires your own chezmoi source repository and publication owner. Configure those relationships before persistence and readback.'),
    ('network', '网络诊断', 'Network diagnosis',
     '通过本机证据排查 DNS、代理、网站连接和路由问题。', 'Diagnose DNS, proxies, website connectivity, and routing from host evidence.',
     '使用自己的探测目标与网络配置；涉及节点切换时配合 clash-auto-switch，改变后核对真实连接。', 'Use your own probe targets and network configuration; combine clash-auto-switch when node switching is needed and verify connectivity after changes.'),
    ('clash-auto-switch', '节点自动切换', 'Proxy node switching',
     '维护 Clash 节点选择、地区回退与 DNS/TUN 保护。', 'Maintain Clash node selection, regional fallback, and DNS/TUN protection.',
     '需要自己配置的 Clash 控制器、组名、凭据引用与运行目录。', 'Requires your configured Clash controller, groups, credential references, and runtime paths.'),
]
for name, zh, en, description_zh, description_en, use_zh, use_en in ADDITIONAL_SKILLS:
    SKILLS[name] = (zh, en, description_zh, description_en, use_zh, use_en,
                   '包含完整方法及配置说明；具体资源、脚本、配套 Skill 与外部工具见包内 README。保留配套关系，按需安装相关包，并绑定自己的环境。',
                   'Includes the method and configuration guidance. The package README specifies resources, scripts, companion Skills, and external tools. Install relevant companions and bind your own environment.')

SKILLS['model-conversation-relay'] = (
    '模型对话接续', 'Model Conversation Relay',
    '接续已绑定的 ChatGPT 咨询会话，核对、等待或提交准确的已授权请求，并保留原始回复与传输回执。',
    'Continue an already bound ChatGPT advisory conversation: inspect, wait, or submit an exact authorized request, retaining the original response and transport receipt.',
    '已有准确的会话与模式绑定，需要核对先前提交、等待回复、恢复被打断的接续，或发送一次已授权的后续请求时使用。调用方解释回复，并判断其对任务的贡献。',
    'Use it with an exact conversation and mode binding to reconcile a prior submission, wait for a response, recover an interrupted exchange, or send one authorized follow-up. The caller interprets the response and judges its contribution to the task.',
    '包含完整方法、中英文使用说明、MIT 许可与客户端发现元数据，覆盖提交核对、中断恢复、自适应等待和不可改写的回执。使用者提供准确的目标、请求、先前回合证据与私有任务存放位置，并绑定实际可用的原生会话适配器或受控浏览器；只有选用浏览器路线时才需要配套的 Browser Relay。',
    'Includes the complete method, bilingual guides, MIT license, and client discovery metadata, covering submission reconciliation, interruption recovery, adaptive waiting, and immutable receipts. Supply the exact target, request, prior-turn evidence, and private task storage, together with an available native conversation adapter or controlled browser. Browser Relay is required only for the browser route.')


def reading_label(title, kind, name, language, english):
    """Display the actual selected edition's title without a language placeholder."""
    return title


def reading_groups(english):
    """Place existing Skills and their substantive reading in practical contexts."""
    families = [
        ('学习与研究', 'Learning and research',
         '围绕问题寻找证据，准备阅读材料，组织学习与实践。', 'Find evidence, prepare reading material, and connect learning with practice.',
         ['research', 'task-inquiry', 'paper-retrieval', 'local-teacher', 'web-teacher', 'shopping']),
        ('创作与协作', 'Authoring and collaboration',
         '写作和维护指令，组织协作，接续模型对话，或用转盘进行选择。', 'Write and maintain instructions, organize collaboration, continue model conversations, or make a random selection.',
         ['prompt-and-skill-lifecycle', 'prompt-audit-orchestration', 'agent-orchestration-master', 'model-conversation-relay', 'random-wheel']),
        ('设备与环境', 'Devices and environments',
         '让手机、浏览器、笔记、配置与网络支持实际工作。', 'Make devices, browsers, notes, configuration, and networks support actual work.',
         ['personal-environment-design', 'android-control', 'browser-relay', 'obsidian-sync', 'chezmoi', 'network', 'clash-auto-switch', 'model-upgrade-check']),
        ('练唱与视频', 'Singing and video',
         '准备录音与伴奏，比较演唱片段，取得视频讲话文本。', 'Prepare recordings and accompaniment, compare performances, and retrieve video speech.',
         ['singing', 'video-subtitle']),
    ]
    sections = []
    for zh, en, note_zh, note_en, names in families:
        entries = []
        for name in names:
            info = SKILLS[name]
            route = '/tools/' + name + ('/en/' if english else '/')
            entries.append(f'<li data-skill="{name}"><a href="{route}">{badge(name)}{name}</a><p>{html.escape(info[3 if english else 2])}</p></li>')
        sections.append('<section class="library-section"><h2>' + (en if english else zh) + '</h2><p class="section-note">' + (note_en if english else note_zh) + '</p><ul class="library-purpose-links">' + ''.join(entries) + '</ul></section>')
    return ''.join(sections)


def render_pages(dist, shell, revision, readers, descriptions):
    for name, info in SKILLS.items():
        for english in (False, True):
            i = 1 if english else 0
            def t(zh, en):
                return en if english else zh
            route = '/tools/' + name + ('/' if english else '/en/')
            title = name
            license_label = 'CC BY-NC-SA 4.0' if name in {'yinyang', 'yinyang-empty'} else 'MIT'
            example = {
                'yinyang': t('“说明网页中的哲学在这个 Skill 参考中怎样表达和组织。”', '“Explain how the website’s philosophy is expressed and organized in this Skill reference.”'),
                'yinyang-empty': t('“从这些空文件开始，结合我的目的与材料，和我一起形成自己的阴阳。”', '“Start from these unfilled files and help me develop my own YinYang from my purposes and material.”'),
                'random-wheel': t('“从这些选项中随机抽一个，用转盘展示。”', '“Randomly pick one of these options and show a wheel.”'),
                'research': t('“调查这个产品今天是否支持我的工作流程，并比较可用方案与证据。”', '“Investigate whether this product supports my workflow today, comparing available approaches and evidence.”'),
                'task-inquiry': t('“这份报告和仪表盘结果不同，找出能解释差异的证据。”', '“This report differs from the dashboard; find evidence that can explain the discrepancy.”'),
                'prompt-and-skill-lifecycle': t('“审查这套 Skill 的指令、维护责任与交付，确认消费者能发现并使用它。”', '“Audit this Skill’s instructions, ownership, and delivery, and verify its consumer can discover and use it.”'),
                'model-conversation-relay': t('“继续这个已经绑定的咨询会话：先核对最新回合与先前提交，再按已授权的请求接续，并保存原始回复与回执。”', '“Continue this already bound advisory conversation: reconcile the latest turns and prior submission, proceed with the authorized request, and retain the original response and receipt.”'),
            }.get(name, t('“请按这个 Skill 帮我处理当前任务，先核对需要的配套方法与实际工具。”', '“Use this Skill for my task, first checking the companion methods and actual tools it needs.”'))
            body = f'<main id="main" class="wrap library-reader"><div class="reader-top"><a class="back" href="/skills/{"en/" if english else ""}">← Skills</a><a class="language-link" href="{route}">{t("English", "中文")}</a></div><article class="document"><p class="eyebrow">SKILL · MIT</p><h1>{html.escape(title)}</h1><p class="collection-intro">{html.escape(descriptions[name])}</p><p><a class="outline-button" href="{GITHUB}/tree/main/skills/{name}">{t("GitHub 源码", "GitHub source")}</a></p><h2>{t("何时使用", "When to use it")}</h2><p>{html.escape(info[4 + i])}</p><blockquote><p>{html.escape(example)}</p></blockquote><h2>{t("包里有什么", "What is included")}</h2><p>{html.escape(info[6 + i])}</p><p>{t("按自然语言提出任务；客户端支持显式调用时，也可以指定", "Ask naturally; if the client supports explicit invocation, select")} <code>{name}</code>。{t("客户端已有的权限、认证和工具边界继续适用。", "The client’s existing authority, authentication, and tool boundaries remain in force.")}</p></article></main>'
            if name == 'yinyang':
                start = body.index('<p>', body.index(t('包里有什么', 'What is included')))
                end = body.index('</article>', start)
                body = body[:start] + '<p>' + html.escape(info[6 + i]) + '</p><p><a href="/tools/yinyang-empty/">' + t('自己的实践使用 Empty', 'Use Empty for your own practice') + '</a></p>' + body[end:]
            readings = []
            body = body.replace('SKILL · MIT', 'SKILL · ' + license_label)
            for kind, zh, en in [('method', '方法', 'Method'), ('guide', '使用说明', 'User guide')]:
                links = ''.join(f'<li><a href="{href}">{html.escape(label)}</a></li>' for href, label, role in readers[name, english] if role == kind)
                if links:
                    readings.append('<h3>' + t(zh, en) + '</h3><ul>' + links + '</ul>')
            reading_body = '<section><h2>' + t('阅读方法与说明', 'Read the method and guide') + '</h2>' + ''.join(readings) + '</section>'
            body = body.replace('</article></main>', reading_body + '</article></main>')
            target = dist / 'tools' / name / ('en' if english else '') / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(shell(title, body, 'en' if english else 'zh-CN'))
