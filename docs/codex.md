# Use with Codex

[简体中文](codex.zh-CN.md)

This collection's installation guide currently supports **Codex**. Choose from
the [package catalog](../README.md#skills-in-the-collection), then read the selected
package's companion and configuration requirements. Copying a Skill does not
configure its external tools, credentials, devices, or host services. Some methods
need only the model's existing tools; others require the documented integrations.

This is a public GitHub repository. The packages may be read, cloned, and
downloaded without an application or approval. All downloads use GitHub;
the website supplies reading editions and introductions.

- [random-wheel](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/random-wheel)
- [research](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research)
- [task-inquiry](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/task-inquiry)
- [prompt-and-skill-lifecycle](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/prompt-and-skill-lifecycle)

## Install through Codex

Installation from this public repository needs no GitHub invitation or private
repository permission.

Paste the command for the Skill you want into a Codex chat:

The examples below use the same mechanism as the other catalog members. Replace
the final package name with the desired directory, and install the companion
packages required for the chosen workflow. For example, install both
`local-teacher` and `web-teacher` for the shared local teaching method.

**YinYang**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang
```

**Random wheel**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/random-wheel
```

**Prompt and Skill Lifecycle**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/prompt-and-skill-lifecycle
```

**Research**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research
```

**Task Inquiry**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/task-inquiry
```

The built-in installer copies the complete Skill directory, including its
references and assets. Use it in a new chat after installation. If it does not
appear in the Skill selector, restart Codex and check again.

## Download instead

[Download the repository ZIP](https://github.com/boluopai-net/Prometheus2Heraclitus/archive/refs/heads/main.zip)
directly. GitHub's **Code → Download ZIP** provides the same download; no Git
clone is required.

Extract it, then ask Codex to install the selected directories under `skills/`
from the extracted folder. All five packages are public downloads; follow each
package's license. Keep each selected folder complete; copying only
`SKILL.md` loses its supporting material. For a manual project-scoped install,
copy the selected folder into your project's `.agents/skills/`, so the entrypoint
is `.agents/skills/<skill-name>/SKILL.md`.
The random wheel's renderer also needs Python 3. Research uses the search,
file, or browser capabilities actually available in the recipient's environment;
installing the Skill does not itself provision a search service.

## Try it

In a new Codex chat, select the installed Skill or type its name:

```text
$yinyang Help me develop my own YinYang from the goals and material I choose to share.
```

```text
$random-wheel Make a wheel with Reading, Writing, and Walking, then pick one.
```

```text
$prompt-and-skill-lifecycle Turn this working method into a reusable Skill and check that its supporting resources are complete.
$research Compare existing implementations for this project using documentation, source code, and independent reports.
$task-inquiry Help me distinguish the explanations for this mismatch, check what can be checked, and continue the task.
```

YinYang ships formation guidance, not the author's private personal account.
Your own material and resulting personal version stay with you. Before updating
an installation you have personalized, ask Codex to compare the new package
with your copy and preserve your personal work. Follow each Skill's license.

Reference: [Codex local Skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
and the [official Skill installer](https://github.com/openai/skills/tree/main/skills/.system/skill-installer).
