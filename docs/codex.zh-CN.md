# 安装到 Codex

[English](codex.md)

**boluopai 插件市场**把集合中的 22 个 Skill 分别做成了可安装插件。从仓库目录选择需要的
Skill，把下面的命令交给 Codex，由它完成原生安装。不需要下载 ZIP、解压或手工修目录。

## 原生安装

安装阴阳：

```bash
codex plugin marketplace add boluopai-net/Prometheus2Heraclitus
codex plugin add yinyang@boluopai
```

将 `yinyang` 换成[目录](../README.zh-CN.md#集合里的-skill)中的其他包名即可。
例如，`codex plugin add research@boluopai` 安装搜索与研究。
市场只需添加一次；以后安装其他插件只需第二条命令。桌面端插件浏览器也可以浏览
已配置的市场。安装后在新对话里使用，让 Codex 发现新装的 Skill。

插件包含完整 Skill、参考文档、脚本、资源及许可。安装不会自动配置外部工具、认证、
设备或服务，具体要求见各包 README。本地教学需要同时安装
`local-teacher@boluopai` 与 `web-teacher@boluopai`。
模型对话接续安装 `model-conversation-relay@boluopai`；仅在选择受控浏览器路线时
另装 `browser-relay@boluopai`。原生会话操作取决于宿主当前真实暴露的工具。

如果你的 Codex 版本没有 `codex plugin` 命令，先更新 Codex，或让内置 Skill 安装工具
从 GitHub 的 `skills/<包名>` 目录安装。避免无意中同时启用同一个 Skill 的独立副本和插件。

## 阴阳：先安装，再形成自己的私人版本

插件提供公开的形成指引，不包含作者的私人模型。你可以让它根据自己选择提供的目标与
材料，协助形成自己的哲学和具体模型。

插件缓存会被更新替换。个人版应保存在自己的私人 Skill 源目录里，放在插件缓存和市场
检出目录之外。让 Codex 将完整阴阳包复制到那里，保留已经存在的个人版，在
`references/situated/` 形成取向、人、伙伴、关系、环境五份描述，在
`references/personal/sources.md` 形成私人证据入口，再通过客户端实际的发现机制启用。
个人版启用后，停用分发插件，
避免两个阴阳入口相互竞争，并在新对话中核实私人入口。
共同内容更新可使用包内 `scripts/sync-common.py`；它会保留整个 `references/situated/`
与 `references/personal/`。形成后，公开写作指引仍保留在 `references/formation/`。
旧混合路径包先按[包结构说明](../skills/yinyang/references/docs/skill-package.zh-CN.md#投影公共变更)
由维护者迁移；迁移前，命令拒绝操作且不改变文件。

## 更新与卸载

```bash
codex plugin marketplace upgrade boluopai
codex plugin add research@boluopai
codex plugin remove research@boluopai
```

先刷新市场，再安装所选插件的当前版本，然后开启新对话。个人修改不要保存在托管缓存中。

## 源码与许可

需要检查、改编源码或使用其他客户端时，可以[浏览源码](https://github.com/boluopai-net/Prometheus2Heraclitus)
或[下载仓库 ZIP](https://github.com/boluopai-net/Prometheus2Heraclitus/archive/refs/heads/main.zip)。
ZIP 是可选的源码入口，不再是 Codex 常规安装步骤。

阴阳保留 CC BY-NC-SA 4.0，其他 Skills 保留各自的 MIT 许可。
这个 GitHub 市场独立分发，不表示已经进入 OpenAI 官方公共插件目录。

参考：[官方插件打包说明](https://developers.openai.com/plugins/build/plugins)
与[公共目录提交流程](https://developers.openai.com/plugins/deploy/submission)。
