# 在 Codex 中使用

[English](codex.md)

这个集合的安装指南目前适用于 **Codex**。从[包目录](../README.zh-CN.md#集合里的-skill)
选择需要的 Skill，再读它的配套方法与配置要求。复制 Skill 不会自动配置外部工具、凭据、
设备或主机服务；有的方法只需已有模型工具，有的还需接入包内说明的实际能力。

本集合为公开 GitHub 仓库，各包都可以直接读取、克隆和下载，无须申请或审批。
全部下载都使用 GitHub；网站提供阅读版与介绍。

- [random-wheel](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/random-wheel)
- [research](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research)
- [task-inquiry](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/task-inquiry)
- [prompt-and-skill-lifecycle](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/prompt-and-skill-lifecycle)

## 让 Codex 安装

公开仓库的安装无需 GitHub 邀请或私有仓库权限。

将想安装的 Skill 对应指令粘贴到 Codex 对话中：

下面示例与其他目录成员使用同一种安装方法。将链接最后的包名换成需要的目录，并安装
当前工作所需的配套包。例如，本地教学方法需要同时取得 `local-teacher` 与 `web-teacher`。

**阴阳**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/yinyang
```

**随机转盘**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/random-wheel
```

**提示词与技能生命周期**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/prompt-and-skill-lifecycle
```

**搜索与研究**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research
```

**任务探究**

```text
$skill-installer install https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/task-inquiry
```

内置安装工具会复制完整的 Skill 目录，包括参考资料和资源文件。安装后在新对话中
使用；如果 Skill 选择器仍未出现它，重启 Codex 后再检查。

## 也可以直接下载

直接[下载仓库 ZIP](https://github.com/boluopai-net/Prometheus2Heraclitus/archive/refs/heads/main.zip)。
GitHub 的 **Code → Download ZIP** 也是同一个入口，不必先学会 Git clone。

解压后，让 Codex 安装其中 `skills/` 下选中的目录。五个包都可公开下载，使用时遵守各自许可。
请保留选中 Skill 的完整目录；只复制 `SKILL.md` 会丢失配套材料。
若手动安装到一个项目，把选中目录复制到该项目的 `.agents/skills/`，使入口位于
`.agents/skills/<skill-name>/SKILL.md`。
随机转盘的渲染脚本还需要 Python 3。研究 Skill 使用接收环境实际可用的搜索、
文件或浏览器能力；安装 Skill 本身不会开通搜索服务。

## 试着使用

在新的 Codex 对话中选择已安装的 Skill，或输入它的名字：

```text
$yinyang 根据我选择提供的目标和材料，帮助我形成自己的阴阳。
```

```text
$random-wheel 把阅读、写作、散步做成转盘，随机选一个。
```

```text
$prompt-and-skill-lifecycle 把这套正在使用的方法写成可复用的 Skill，并检查配套资源是否完整。
$research 结合文档、源代码与独立报告，比较这个项目已有的实现方案。
$task-inquiry 帮我区分这个不合之处的几种解释，核查能够核查的部分，并继续推进任务。
```

阴阳包提供形成指引，不包含作者私人的个人记录。你提供的材料和形成的个人版本
留在你自己那里。已经个性化的版本需要更新时，先让 Codex 比较新旧内容、保留你的
个人成果，再进行更新。使用时遵守各 Skill 的许可。

参考：[Codex 本地 Skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
与[官方 Skill 安装工具](https://github.com/openai/skills/tree/main/skills/.system/skill-installer)。
