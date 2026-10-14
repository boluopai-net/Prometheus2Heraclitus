"""Render the Codex installation chooser from the published marketplace catalog."""
import html
import json


def render(dist, shell, repo):
    market = json.loads((repo / '.agents/plugins/marketplace.json').read_text())
    for english in (False, True):
        def t(zh, en): return en if english else zh
        suffix = 'en/' if english else ''
        options = ''.join('<option value="' + p['name'] + '">' + html.escape(p['interface']['displayName'].split(' · ')[-1 if english else 0]) + '</option>' for p in market['plugins'])
        body = f'''<main id="main" class="wrap library-reader install-page"><a class="back" href="/repositories/{suffix}">{t('← 资料与建议', '← Resources and suggestions')}</a><article class="document">
<p class="eyebrow">CODEX · BOLUOPAI</p><h1>{t('安装到 Codex', 'Install in Codex')}</h1>
<p class="collection-intro">{t('选一个 Skill，把安装指令交给 Codex。它会从 GitHub 市场取得完整插件，无须下载或解压 ZIP。', 'Choose a Skill and give its installation request to Codex. It fetches the complete plugin from the GitHub marketplace, without manual ZIP downloads or extraction.')}</p>
<section class="install-chooser" aria-labelledby="choose-title"><h2 id="choose-title">{t('你想使用什么？', 'What would you like to use?')}</h2>
<label for="install-skill">Skill</label><select id="install-skill">{options}</select>
<p id="install-description"></p><button id="copy-install" type="button">{t('复制给 Codex', 'Copy for Codex')}</button><p id="copy-status" role="status" aria-live="polite"></p>
<label for="install-request">{t('粘贴到 Codex 的内容', 'Paste this into Codex')}</label><textarea id="install-request" readonly rows="7"></textarea>
<p class="section-note">{t('复制后，在 Codex 对话里粘贴并发送。安装完成后开启新对话使用。', 'After copying, paste and send in a Codex chat. Start a new chat after installation.')}</p></section>
<section id="yinyang-install-note"><h2>{t('让阴阳成为自己的', 'Make YinYang your own')}</h2><p>{t('安装得到的是形成方法、哲学文档与图示。让模型根据你愿意提供的目标和材料形成私人版本；个人内容应保存在自己的私人目录中，避免被插件更新覆盖。', 'Installation supplies the formation method, philosophical documents, and diagrams. Ask the model to develop a private version from the goals and material you choose to share. Keep personal content in your own private source, outside replaceable plugin caches.')}</p></section>
<details class="install-details"><summary>{t('直接使用终端命令', 'Use terminal commands')}</summary><pre><code id="install-commands"></code></pre></details>
<p>{t('每个插件包含完整 Skill 和配套资源。外部工具与账号按实际需要配置；安装不会自动开通服务。', 'Each plugin includes the complete Skill and supporting resources. Configure external tools and accounts as needed; installation does not provision services.')}</p>
<p><a id="install-source" href="https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang">{t('查看所选 Skill 源码', 'View the selected Skill source')}</a> · <a href="https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/docs/codex{'.md' if english else '.zh-CN.md'}">{t('安装、更新与私人版本说明', 'Installation, updates, and private versions')}</a></p>
<p class="section-note">{t('这是独立的 GitHub 插件市场。阴阳采用 CC BY-NC-SA 4.0，其他 Skills 采用 MIT；尚未以官方公共目录上架作为安装条件。', 'This is an independent GitHub plugin marketplace. YinYang uses CC BY-NC-SA 4.0; the other Skills use MIT. Installation does not depend on a public directory listing.')}</p>
<noscript><p>{t('请把下面两条命令交给 Codex，或打开安装说明选择其他 Skill。', 'Give the following commands to Codex, or open the installation guide to choose another Skill.')}</p><pre>codex plugin marketplace add boluopai-net/Prometheus2Heraclitus
codex plugin add yinyang@boluopai</pre></noscript>
</article></main>'''
        target = dist / 'install' / ('en' if english else '') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(shell(t('安装到 Codex', 'Install in Codex'), body, 'en' if english else 'zh-CN',
            extra='<link rel="stylesheet" href="/install.css"><script type="module" src="/install.js"></script>'))
