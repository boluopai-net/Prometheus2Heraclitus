# browser-relay

Hold exact target custody for a bounded browser operation: verify ownership,
destination, effects and cleanup while preserving surrounding sessions and work.
The exact Skill identifier is `browser-relay`. The caller owns task purpose and
semantic completion; Relay owns the physical target operation. A matching URL,
successful click or authenticated browser alone does not establish that chain.

Examples: “Use an owned page to download this available paper and identify the
returned file”; “Inspect this exact authorized conversation without submitting”;
“Submit these exact bytes once and report uncertain delivery”; “Reuse the
dedicated authorized session, release the task page and verify retention.”

## Dependencies and configuration

Copy the complete directory to your host's supported Skill location and read
[SKILL.md](SKILL.md). Bind actual tools through
[carrier configuration](references/carriers.md). Downloading this Skill does not
install a browser controller or grant access to an existing account/profile.

| Dependency or companion | Requirement and relationship |
| --- | --- |
| Host browser/tab API or configured controller | Required execution capability: exact create/attach handle, current inspection/actions and readback, close/release and lifecycle inventory. Use current tool documentation; no private wrapper command is assumed. |
| Dedicated authenticated carrier | Conditional on signed-in work: recipient-configured isolated profile/context, observed intended account and real lifecycle owner. The package contains no profile, credentials or login adapter. |
| Host desktop/credential owner | Actual placement, focus, account and personal-authentication boundaries; supply safe background/headless or permitted window placement. Profile paths alone do not establish these capabilities. |
| `chrome-configuration` | Local source's conditional method owner for browser settings/extensions. No public copy is bundled or required for normal Relay work; use an installed counterpart or recipient configuration owner for that separate task. |
| `jev-browser-use` | Local source's optional delegated-loop method. Use only when actually available and selected by the host; Relay retains target ownership and cleanup. |
| [paper-retrieval](../paper-retrieval/README.md) | Example downloadable caller that composes custody with scholarly identity/version/full-text checks; [public package](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/paper-retrieval). It is not a Relay execution dependency. |

The complete method supports in-app owned tabs, retained authenticated pages and
ephemeral headless contexts as distinct carriers. Release retaining a page differs
from page closure and whole-owner shutdown. Model-message exchanges preserve the
caller’s `observe`/`submit` and single-attempt reconciliation boundary. Downloads
preserve initiation-to-file attribution; domain verification stays with the caller.
Failures prompt exact-target recovery/readback within actual authority, with
human participation reserved for actual personal authentication/consent boundaries.

## Optional harmless headless check

If a host already exposes a suitable browser API, no Python/Playwright installation
is required. The bundled example separately demonstrates one ephemeral route with
local fixture content and no network, existing browser/profile or authentication.
It is not the retained/authenticated controller described by the method.

```sh
python3 -m venv .venv
# POSIX; Windows uses .venv\Scripts\activate
. .venv/bin/activate
python -m pip install playwright
python -m playwright install chromium
python scripts/smoke_headless.py --help
python scripts/smoke_headless.py
```

The smoke example prints JSON for task-created ownership, changed text readback,
page closure and browser disconnection. It explicitly leaves authentication,
shared-owner retention and desktop placement unestablished. Python 3.10+,
[Playwright](https://playwright.dev/python/docs/intro) and its
[browser runtime](https://playwright.dev/python/docs/browsers) are optional external
dependencies; use supported platform/dependency setup. The script creates and
closes only its own headless browser. It saves no profile or fixture artifacts.

This original public adaptation preserves the local custody, session, placement,
message and lifecycle method while removing private host integrations, profile
paths, account/service targets and incident-specific configuration. Carrier
bindings remain explicit external prerequisites. The private runtime scripts
are not bundled or presented as standard APIs. Original package material is
[MIT licensed](LICENSE). Playwright/browser implementations and visited material
retain their own rights; no third-party code is bundled.

## 中文说明

本 Skill 负责有界浏览器操作的准确目标：确认所有权、目的地、操作效果和清理，
同时保留周围会话与工作。准确标识为 `browser-relay`。调用方拥有任务目的与
语义完成判断，Relay 拥有物理目标操作。URL 相同、点击成功或浏览器已登录，
都不能单独证明这条关系链。

示例：“在自己拥有的页面下载这篇可获取论文，标识返回文件”；
“只观察这段准确的已授权会话，不发送”；“准确发送这些字节一次，报告投递不确定性”；
“复用专用授权会话，释放任务页面并确认保留”。

将完整目录安装到宿主支持的位置，读取 [SKILL.md](SKILL.md)，按
[载体配置](references/carriers.md) 绑定真实工具。下载 Skill 不等于安装浏览器
控制器，也不授予已有账号或 Profile 的访问权。

| 依赖或配套方法 | 要求与关系 |
| --- | --- |
| 宿主浏览器／标签页 API 或已配置控制器 | 必需执行能力：准确创建／附加句柄、当前检查和操作、结果确认、关闭／释放及生命周期清单。使用当前工具文档，不假定私人包装器命令存在。 |
| 专用登录载体 | 登录任务才需要：接收方配置的隔离 Profile／context、已观察的目标账号和真实生命周期负责人。本包不含 Profile、凭据或登录适配器。 |
| 宿主桌面／凭据负责人 | 保留真实的窗口放置、焦点、账号和个人认证边界；提供安全后台／无头或已允许的窗口放置。仅有 Profile 路径不足以证明这些能力。 |
| `chrome-configuration` | 本地源中浏览器设置／扩展的条件方法负责人；本包不附公开副本，普通 Relay 工作不需要。该独立任务使用已安装对应方法或接收方设置负责人。 |
| `jev-browser-use` | 本地源中的可选委派循环方法；宿主选择且真实可用时才使用，Relay 仍负责准确目标和清理。 |
| [paper-retrieval](../paper-retrieval/README.md) | 可下载调用方示例，将目标管理与学术身份、版本和全文检查组合；[公开包](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/paper-retrieval)。不是 Relay 的执行依赖。 |

完整方法区分应用内标签页、保留的登录页面与临时无头 context。保留页面的释放、
页面关闭和整个负责人退出不同。模型消息操作保留调用方的观察／提交及一次尝试后
确认边界；下载保留发起操作到文件的归属，领域验证归调用方。故障在真实权限内
恢复准确目标并确认效果，仅在实际个人认证或同意边界需要本人参与。

宿主已有合适 API 时无需安装 Python／Playwright。上方可选无头检查命令使用
本地 fixture，不访问网络、已有浏览器／Profile 或账号，也不是保留／登录控制器。
Windows 激活虚拟环境使用 `.venv\Scripts\activate`。脚本输出自己创建的目标、
文字变更确认、页面关闭和浏览器断开的 JSON；不会证明登录、共享负责人保留或桌面
放置。依赖 Python 3.10+、[Playwright](https://playwright.dev/python/docs/intro) 及
其 [浏览器运行时](https://playwright.dev/python/docs/browsers)。它仅创建和关闭自己
的无头浏览器，不保存 Profile 或 fixture 文件。

此原创公开改写保留本地目标、会话、放置、消息和生命周期方法，移除私人主机集成、
Profile 路径、账号／服务目标及事故特定配置。载体仍明确由外部提供；私人脚本不附带，
也不冒充标准 API。原创内容采用 [MIT 许可](LICENSE)，Playwright／浏览器和访问材料
保留各自权利，本包不附第三方代码。
