# Prometheus2Heraclitus · 从普罗米修斯到赫拉克利特

**一个让有限生命取得生成能力的 Skill 集。**

[网站首页](https://boluopai.net/) · [文档与图示](https://boluopai.net/repositories/prometheus/) · [English](README.md)

<!-- repository-only:start -->
**[安装到 Codex](docs/codex.zh-CN.md)**
<!-- repository-only:end -->

**从这个例子出发，写自己的哲学，凝练自己的私人模型，并把愿意公开的思想做成自己的作品与网页。**
哲学写作帮助人探索尚不清楚的自我理解；其中清晰、有依据的关系，凝练为五份核心文件，
供模型在实际协作中使用。具体身份、经历与原始材料留在私人来源里。
公开作品可以表达哲学与经过选择的模型理解，同时由本人保留完整的个人模型。
这里示范的是这种创作与建模方式，而不只是让别人替换一份现成配置。

**这个仓库的核心特色是建模，不是提供一个记忆系统。**其中的阴阳从具体的人出发：
以哲学、心理与偏好材料形成动态的用户模型，据此形成对应的 agent 模型与合作关系，
再让双方的工作进入现实，由后果继续修订理解。记忆使材料能够保存和接续；建模则
组织这些材料的意义、关系与变化，并使它们参与判断和行动。

哲学在这里是可继续书写的整体。文学、历史、美学、计算机与工程都可以成为建模材料；
不同观点可以保留、比较或组合，不要求先加入同一学派。容纳冲突仍需区分保留的材料、
当前采用的理解及其后果。具体方法和工具给这份理解以可用形式；另一个人也可以
由此写出完全不同的哲学与环境。

这里提供的是可以实际使用的例子，Skill 本身也在其中。你可以取用、组合或重新
创作，写出与阴阳很不相同的哲学和作品；共享的愿望是创造能力，不是对同一套
信条的认同。[例子与知识共有地](skills/yinyang/references/docs/example-and-commons.zh-CN.md)
展开这个邀请，并区分文学形式与技术格式。
[文档与图示](https://boluopai.net/repositories/prometheus/)直接呈现持续维护的文档与图示，
并保留通往源内容的链接。

## 哲学、心理与工程：从已有能力补齐三位一体

**哲学展开理解与方向，心理理解具体的人，工程让关系成为可用环境。**三方面相互支撑：只熟悉一方面，就从它进入另外两方面；已经熟悉两方面，就重点补第三方面。哲学与心理已有基础时，重点把理解实现为 harness；哲学与工程已有基础时，补充个人经验与偏好依据；心理与工程已有基础时，把实际关系展开为哲学。这是借助模型共同发展实践的方式，不要求先独立修完三门学科。

**不会工程，就先补工程。**先学会借助模型组织文件、工具、harness、运行与核验，使材料整理、模型写作和修订有可用环境，再把已有理解接进来。只有一个主要起点时，通常这样展开：

- **已有心理基础：工程 → 哲学。**先形成可用的工程环境，再整理自己的相关经历、聊天、记忆与偏好材料，在私人 `personal/` 中保留材料或来源；与模型一起形成个人模型，再把其中的关系展开为哲学。
- **已有哲学基础：工程 → 心理。**先形成能够整理材料与持续修订的环境，再把已有哲学与自己的具体经历、偏好和实际使用相互对照，凝练个人模型。
- **已有工程基础：通常心理 → 哲学。**从 harness 的使用、选择、阻力和修改中提出个人模型的候选解释，再结合相关心理与偏好材料修订，把依据留在私人 `personal/`，由此展开哲学。工程已经可用时，也可以按已有思想与材料灵活调整入口。

这三条是可以转入彼此的起步路线，适合哪条由当前对象决定，不按职业把人固定分组。工程配置可能受习惯、限制或默认值影响，不能单凭“装了什么”推断“这个人是谁”；哲学的融贯也需要个人证据与实践回应。模型帮助整理、成文和实现，人通过理解、选择、使用与纠正参与。形成后，哲学、个人模型、材料和环境继续互相修订。[阴阳的具体形成方法](skills/yinyang/README.zh-CN.md#怎样使用并理解阴阳)说明五份核心的职责与使用。

## 集合里的 Skill

每个成员维护自己的入口、方法与配套资源。取得想使用的 Skill 的完整目录，
通过模型实际的 Skill 机制让它读取。

| Skill | 用途 | 包 |
| --- | --- | --- |
| [阴阳 · yinyang](skills/yinyang/SKILL.zh-CN.md) | 建模具体的人，据此形成对应的 agent 与双方关系，再把协作落实到实际环境。 | [使用说明与哲学资源](skills/yinyang/README.zh-CN.md) |
| [抽卡转盘 · random-wheel](skills/random-wheel/SKILL.md) | 把截图或明确给出的选项变成可调速的动画转盘，以等概率随机抽选。 | [完整包](skills/random-wheel/) |
| [搜索与研究 · research](skills/research/SKILL.md) | 调查事实、产品行为与方案，把来源、观察、假设和覆盖限制放在同一个可检查的回答中。 | [完整包](skills/research/) |
| [任务探究 · task-inquiry](skills/task-inquiry/SKILL.md) | 从实际分歧、证据和有用的问题出发，澄清会改变任务下一步的关键不确定性。 | [完整包](skills/task-inquiry/) |
| [提示词与技能生命周期 · prompt-and-skill-lifecycle](skills/prompt-and-skill-lifecycle/SKILL.md) | 把指令的含义、维护责任、交付方式和实际使用证据连在一起，编写、审查与维护 Prompt 和 Skill。 | [完整包](skills/prompt-and-skill-lifecycle/) |
| [安卓手机控制 · android-control](skills/android-control/SKILL.md) | 通过 ADB 与原生界面操作自己的安卓设备，并核实实际效果。 | [完整包](skills/android-control/) |
| [个人环境设计 · personal-environment-design](skills/personal-environment-design/SKILL.md) | 将相连的指令、工具、服务与人的使用流程，配置为共同工作的环境。 | [完整包](skills/personal-environment-design/) |
| [模型升级检查 · model-upgrade-check](skills/model-upgrade-check/SKILL.md) | 核对可用模型、用途分配与实际消费者，让升级保持一致。 | [完整包](skills/model-upgrade-check/) |
| [论文与学术书籍检索 · paper-retrieval](skills/paper-retrieval/SKILL.md) | 核对题录、版本与全文，把搜索结果交付为可验证的学术材料。 | [完整包](skills/paper-retrieval/) |
| [视频字幕提取 · video-subtitle](skills/video-subtitle/SKILL.md) | 取得带来源与时间线的视频讲话文本，再回到原视频核对。 | [完整包](skills/video-subtitle/) |
| [练唱 · singing](skills/singing/SKILL.md) | 准备伴奏、录音与参考表演，把听辨和音频证据用于练唱。 | [完整包](skills/singing/) |
| [本地老师 · local-teacher](skills/local-teacher/SKILL.md) | 在本地环境中讲解、复习、练习，并通过真实工作发展理解。 | [完整包](skills/local-teacher/) |
| [云端老师 · web-teacher](skills/web-teacher/SKILL.md) | 提供课程材料、教学方法、学习路径与学习空间的共同方法。 | [完整包](skills/web-teacher/) |
| [购物与比价 · shopping](skills/shopping/SKILL.md) | 比较商品、价格、优惠与二手选择，保留实际证据与条件。 | [完整包](skills/shopping/) |
| [提示词审计 · prompt-audit-orchestration](skills/prompt-audit-orchestration/SKILL.md) | 按实际范围审查学习、工作、Web 与自动化的指令和执行关系。 | [完整包](skills/prompt-audit-orchestration/) |
| [多智能体协作 · agent-orchestration-master](skills/agent-orchestration-master/SKILL.md) | 按实际工作拆分贡献、交接和依赖，并由任务所有者整合结果。 | [完整包](skills/agent-orchestration-master/) |
| [模型对话接续 · model-conversation-relay](skills/model-conversation-relay/SKILL.md) | 接续准确的咨询交换，确认有序轮次，限定重试并保存不可变回执。 | [完整包](skills/model-conversation-relay/) |
| [浏览器会话 · browser-relay](skills/browser-relay/SKILL.md) | 管理任务专用浏览器、认证会话、目标归属与清理。 | [完整包](skills/browser-relay/) |
| [笔记同步 · obsidian-sync](skills/obsidian-sync/SKILL.md) | 维护多个 Obsidian 库的共同配置、云端复制与同步。 | [完整包](skills/obsidian-sync/) |
| [系统配置持久化 · chezmoi](skills/chezmoi/SKILL.md) | 把授权的本机配置变更保存到源码，并通过实际发布机制接回环境。 | [完整包](skills/chezmoi/) |
| [网络诊断 · network](skills/network/SKILL.md) | 通过本机证据排查 DNS、代理、网站连接和路由问题。 | [完整包](skills/network/) |
| [节点自动切换 · clash-auto-switch](skills/clash-auto-switch/SKILL.md) | 维护 Clash 节点选择、地区回退与 DNS/TUN 保护。 | [完整包](skills/clash-auto-switch/) |

阴阳提供文化、思想与推理形式；个人内容来自获授权的实际材料，以及使用模型与
这个人的协作。直接采用阴阳时，**必须由模型协助改写五份核心关系文档，并整理自己的 `references/personal/`**；
下载或安装并不完成个人版。[上手说明](skills/yinyang/README.zh-CN.md#怎样使用并理解阴阳)逐项说明改什么、由谁完成及怎样确认可用。
论述与图示都属于 `skills/yinyang/references/` 内的阴阳配件。
其他成员保留各自的用途与专业方法；进入这个集合，不会使它们变成阴阳参考，
也不要求使用它们时采用阴阳的哲学。
组合使用时，阴阳是用户哲学的一个例子，其他 Skills 用具体能力补充它。
读者可以选择自己的组合，并围绕它写出另一种哲学。

公开包保留实际本地方法的结构和有用的配套关系。先读各包的依赖与配置说明，按任务下载
需要的配套 Skill，再绑定自己的工具与环境。配套 Skill 提供方法，不会自动授予认证、
设备访问或运行服务。它们不包含私人参与者描述、凭据、个人记录或作者的主机绑定配置。

<!-- repository-only:start -->
## 在 Codex 中使用

[安装与更新说明](docs/codex.zh-CN.md)

22 个 Skill 均可从 **boluopai** 插件市场独立安装。把下面的命令交给 Codex，
即可安装完整阴阳包，无须手工下载或解压 ZIP：

```bash
codex plugin marketplace add boluopai-net/Prometheus2Heraclitus
codex plugin add yinyang@boluopai
```

将 `yinyang` 换成目录中需要的 Skill 名称。市场只需添加一次，之后安装其他插件只需
`codex plugin add <包名>@boluopai`。安装后开启新对话使用。
阴阳个人版应保存在私人源目录中，不能写进会被更新替换的插件缓存。
<!-- repository-only:end -->

## 维护与贡献

[协作与贡献](CONTRIBUTING.zh-CN.md)说明什么时候发 Issue、什么时候提交 PR，
以及怎样准备改动、检查和参与审阅。

<!-- repository-only:start -->
[完整网站源码](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/website)保存在同一个集合中，包含公开文章、页面、资源与实现。
它是原生 Site 某个已提交版本的生成快照，版本记录在
[SOURCE.json](https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/website/SOURCE.json)。阴阳文档仍以 `skills/yinyang/` 为维护源，
网站中的对应副本是阅读投影；独立网站材料在原生 Site 源码处维护。
GitHub 集合 ZIP 包含完整网站；网站负责展示、阅读与包介绍，源码和全部下载都在 GitHub。
可以浏览包目录，或下载仓库 ZIP 后选取完整 Skill 目录。Git 提交保留修改历史，
不需要另设 Release、标签或稳定版本流程。
<!-- repository-only:end -->

[MODEL.md](MODEL.md)维护集合的维护与发布边界，[AGENTS.md](AGENTS.md)为贡献者提供入口。
各 Skill 在自己的目录维护进一步的解释与维护指令。英文为主；提供读者对应版本时，
保留完整的语义对应。

通过 [issues](https://github.com/boluopai-net/Prometheus2Heraclitus/issues)
与 [pull requests](https://github.com/boluopai-net/Prometheus2Heraclitus/pulls)
提出问题和修订。个人理解与私人来源留在其实际维护位置；
只有获授权的可复用材料进入这个集合。

## 许可

阴阳原创材料采用 [CC BY-NC-SA 4.0](LICENSE)，仅限非商业性再利用；其他可复用包保留 [MIT](LICENSE-MIT)。适用范围、署名、单独权利与旧版有效授权见[集合许可说明](LICENSING.md)及各包的 `LICENSE`。
