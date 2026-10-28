# Install in Codex

[简体中文](codex.zh-CN.md)

The **boluopai** marketplace offers all 22 collection Skills as individually
installable plugins. Choose one from the repository catalog and give Codex the
commands below to perform the native installation. No ZIP extraction or manual
directory repair is required.

## Native installation

For YinYang:

```bash
codex plugin marketplace add boluopai-net/Prometheus2Heraclitus
codex plugin add yinyang@boluopai
```

Replace `yinyang` with any name in the [catalog](../README.md#skills-in-the-collection).
For example, `codex plugin add research@boluopai` installs Research.
Add the marketplace once; later plugins need only the second command.
The desktop plugin browser can also browse the configured marketplace.
Use a new chat after installation so the installed Skills can be discovered.

The package includes the complete Skill, references, scripts, assets, and its
license. Installing it does not provision external tools, authentication,
devices, or services. Read the package README for those requirements. For local
teaching, install both `local-teacher@boluopai` and `web-teacher@boluopai`.
For model conversation relay, install `model-conversation-relay@boluopai`; add
`browser-relay@boluopai` only when using its controlled browser route. Native
conversation operations depend on the tools actually exposed by your host.

If your Codex version lacks `codex plugin`, update Codex or use its built-in
Skill installer with the selected GitHub `skills/<name>` directory. Do not
install both a standalone copy and the same plugin unintentionally.

## YinYang: install first, personalize in your own private source

The installed plugin contains public formation guidance, not the author's
private portrait. Ask it to form situated working accounts from the goals,
selected views, and material you choose to share. A separate philosophical
writing project is optional.

Plugin cache files are replaceable. Keep your personal version in your own
private Skill source, outside the plugin cache and marketplace checkout.
Have Codex copy the complete YinYang package there, preserve an existing
personal version, form six accounts of orientation, person, counterpart, relationship,
environment, and revision under `references/situated/` and the evidence entrance at
`references/personal/sources.md`,
and register that private Skill through your client's actual discovery mechanism.
Once that personal Skill is active, disable the distribution plugin to avoid
two competing YinYang entrypoints. Verify the private entrypoint in a new chat.
Common updates can use the included `scripts/sync-common.py`; it preserves the
entire `references/situated/` and `references/personal/` trees. Public writing
guides remain under `references/formation/` after formation. Legacy mixed-path
packages require owner migration under the [package guide](../skills/yinyang/references/docs/skill-package.md#project-common-changes)
before projection; the command refuses them without changing files.

## Updates and removal

```bash
codex plugin marketplace upgrade boluopai
codex plugin add research@boluopai
codex plugin remove research@boluopai
```

Refresh the marketplace and install the selected current plugin version, then
start a new chat. Never store personal modifications in the managed cache.

## Source and licenses

[Browse source](https://github.com/boluopai-net/Prometheus2Heraclitus) or
[download the repository ZIP](https://github.com/boluopai-net/Prometheus2Heraclitus/archive/refs/heads/main.zip)
when you want to inspect, adapt, or use another client. ZIP is an optional source
route, not the normal Codex installation step.

YinYang retains CC BY-NC-SA 4.0; the other Skills retain their package-local MIT
licenses. The GitHub marketplace is independently distributed and is not a claim
of inclusion in OpenAI's public plugin directory.

References: [Official plugin packaging](https://developers.openai.com/plugins/build/plugins)
and [public directory submission](https://developers.openai.com/plugins/deploy/submission).
