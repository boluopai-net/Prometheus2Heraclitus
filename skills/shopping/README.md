# 购物与比价 · shopping

[中文指南](README.zh-CN.md)

Compare products, discounts, and used listings across Chinese marketplaces.
The method matches model, variant, seller, condition, warranty, price type,
date, and buying conditions before recommending an option. It distinguishes
discovery from verified detail and the recipient's actual checkout price.

## Use and companions

Download the [complete shopping directory](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/shopping)
or obtain it from the [collection archive](https://github.com/boluopai-net/Prometheus2Heraclitus/archive/refs/heads/main.zip).
Place the directory in a Skill location supported by your agent host.

No companion Skill is universally required. [YinYang](../yinyang/README.md)
is the contextual companion when the recipient adopts its situated account;
Shopping uses supported recipient context without bundling a private portrait.
[Research](../research/README.md) is the evidence companion when specifications,
compatibility, or source claims require investigation. Both are separate complete
packages in the same public archive. Current conversation and a fitting available
research capability remain usable when those companions are not installed.

Example: “Compare a new 16 GB/512 GB laptop with the same model used on Xianyu.
Include seller condition claims, remaining warranty, shipping, coupon eligibility,
and evidence for the final price. I will carry it between two work locations.”
The result should explain comparable candidates and fit tradeoffs, with direct
links, dates, missing facts, and unverified claims; it cannot promise an exhaustive
market minimum.

## Conditional tool dependencies

This package contains a method and agent metadata, not shopping clients or scripts.
Use only the sources needed for the question and available within existing access.

| Route | Obtain/setup | Needed when selected |
| --- | --- | --- |
| Haina | [Official platform](https://ai.zhidemai.com/haina-platform) | Recipient's own key, product/deal permissions, and a configured client using current official documentation |
| Maishou | [Complete upstream Skill](https://github.com/aahl/skills/tree/main/skills/maishou) | Python 3.11+, uv, and its scripts; run from its package directory |
| Direct platforms | [cn-scraper-mcp](https://github.com/goesByhc/cn-scraper-mcp) | Python 3.11+, upstream package and MCP-capable host; accepted platform session and supported browser for browser routes |
| Xianyu | [goofish-cli](https://github.com/fancyboi999/goofish-cli) | Python 3.11+, upstream package and authorized session; search/browser detail need Playwright and supported Chrome; MCP startup via uvx also needs uv |

Maishou's documented commands include `uv run scripts/main.py search --source=0
--keyword='MODEL'` and `uv run scripts/main.py detail --source=SOURCE --id=GOODS_ID`.
cn-scraper is installed as `cn-scraper-mcp` and connected through the host's actual
MCP configuration. goofish exposes CLI `goofish` and MCP `uvx goofish-cli`.
Inspect current upstream setup, help, and schemas before executing; these examples
do not install or authenticate anything. Current cn-scraper documentation discourages
PDD search. A service's advertised platform support does not establish useful access
in your environment. Haina's landing page was reachable during adaptation, but
its API schema was not verified.

Installation, account access, purchases, payments, seller messages, and listing
writes keep their existing authorization boundaries. Credentials are not bundled.
Some upstream tools expose writes; this comparison method does not authorize them.

## Adaptation and rights

The public edition preserves the local Skill's comparison, condition, pricing,
provenance, fit, and access distinctions. Private cloud wrappers, retired
registrations, host paths, observed account history, and a private portrait
reference are replaced with public dependencies and supported recipient context.
`SKILL.md` is English model-facing instruction; README editions are aligned guides.

Original package material uses the [MIT License](LICENSE). External packages are
separate dependencies under their own licenses and notices; none of their source,
binaries, credentials, or private sessions is bundled. Public documentation was
checked on 2026-10-14; no dependency was installed or marketplace account queried.
