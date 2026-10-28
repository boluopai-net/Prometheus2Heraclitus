---
name: shopping
description: "<用户自制> 购物与比价：搜索国内电商与闲鱼商品，比较价格、优惠和二手选择。 Find and compare products, prices, deals, and secondhand listings across Chinese shopping platforms using available Haina, Maishou, direct marketplace, and Xianyu tools."
---

# shopping

Bring offers onto a common scale before helping the user choose. A price is
attached to a particular item, seller, moment, and set of conditions; detached
from those relations, the smallest number can describe the wrong purchase.

Develop the use case and tradeoffs from the user's request, current context,
and actual use; the user need not first produce a complete preference model.
Aggregators discover candidates and
reported deals; direct platforms identify their own listings; manufacturers
can establish specifications; checkout establishes this user's payable price.
Accounts and permissions determine which observations are available, while
seller claims and parsed tool fields still need assessment. Matching variants,
condition, warranty, coupons, and dates makes comparison possible without
turning discovery into a promise of an exhaustive market minimum.

Use the four sources below through their available cloud or local tools to
produce comparable, source-backed candidates. Inspect callable schemas and
returned fields, retain direct links and material buying conditions, and explain
the tradeoff supporting a recommendation. Lookup informs the user's purchase;
buying, paying, or contacting a seller retains its separate instruction and
transaction boundary. Installation alone does not establish authentication or
successful search/detail access.

## Fit the purchase to lived use

[YinYang](../yinyang/SKILL.md) owns situated understanding and its uncertainty
when the recipient uses that companion. Use the recipient's supplied context,
current conversation, and authorized supported account to judge fit. Read only
relevant grounded material through the host's actual Skill discovery; the public
YinYang framework does not contain a portrait of this recipient. Keep any maintained
personal account with its existing owner rather than constructing a second
diagnostic profile in Shopping. If YinYang is not adopted, work from the current
conversation and supported context without inventing a substitute biography.

For equipment, furniture, and everyday setups, consider recipient-reported
movement, posture, location, sensory, and setup needs only when supported by the
actual use case. Comfort in one setting does not establish comfort in another.
Compare whether each option supports resuming the same activity with little
setup or lost context. Carry weight, cables, power, input effort, and switching
cost matter when they affect actual use. Balance them against capability, price,
and existing equipment; portability is not an unconditional winner, and a fixed
setup can remain one useful part of a flexible arrangement.

Distinguish observed fit, inferred fit, and what only actual use can establish.
Explain the relevant setting and tradeoff, including trial or return conditions
when comfort remains uncertain. Changing preferences across situations need not
be an error to correct. Do not infer a health condition or promise therapeutic
effects from a shopping request. Keep this context proportionate: a concrete price lookup need not become a
personal assessment, and a purchase is not always required to meet the need.

Make the comparison inspectable through a suitable table, visual, or concrete
use scenario when linear explanation makes the relationships hard to follow.
Keep each recommendation close to its supporting evidence and unresolved fit
questions; the user should not have to infer from the model's tone whether a
price, compatibility claim, or comfort claim was actually verified.

## Host entrypoints and setup

Install this complete Skill through the recipient host's normal Skill discovery.
It is a method package, not a cloud service or a bundled shopping server. Inspect
the actually callable tools or CLI help and their schemas before use. MCP prefixes,
argument names, login storage, and supported platforms depend on the installed
upstream version and host integration; no private wrapper is assumed.

Choose only the dependencies needed for the question:

- [Haina](https://ai.zhidemai.com/haina-platform): configure the recipient's own
  service key and product/deal permissions in an available authorized client or
  integration. Follow its current official service documentation; this package
  provides no key, client, proxy, or promised tool name.
- [Maishou](https://github.com/aahl/skills/tree/main/skills/maishou): obtain the
  complete upstream Skill including its scripts. Its documented CLI uses Python
  3.11+ and `uv run scripts/main.py`, whose script metadata supplies dependencies.
  Run from that package directory. Inspect its current output and supported
  sources rather than assuming a cloud adapter.
- [cn-scraper-mcp](https://github.com/goesByhc/cn-scraper-mcp): install the upstream
  Python 3.11+ package and connect its MCP server through the host's supported
  configuration. Direct platform lookup needs the relevant platform's accepted
  authentication; browser-dependent routes additionally need upstream-supported
  Chrome/browser setup. Current upstream documentation discourages PDD search;
  do not promise usable results for every listed platform.
- [goofish-cli](https://github.com/fancyboi999/goofish-cli): install its Python
  3.11+ package for Xianyu lookup. CLI entrypoint is `goofish`; the upstream MCP
  entrypoint is `uvx goofish-cli` when uv and an MCP-capable host are available.
  Search/browser detail additionally use Playwright and supported Chrome with
  an authorized Xianyu session. Follow current upstream setup and restrictions.

Installation is conditional on the requested task and existing authorization;
this method does not silently install services, enable registrations, or obtain
account access. No dependency is bundled. If a needed capability is unavailable,
state the concrete gap, use suitable available search/browser evidence or another
source, and continue supported work. A named repository is not proof of a
callable tool, working login, or useful search/detail response.

## Choose the source for the question

| Source | Useful for | Available upstream entrypoints and identity |
| --- | --- | --- |
| Haina / 什么值得买海纳 | Cross-store discovery, available history, dated deal reports and conditions | Product/SKU and deal search through the recipient's configured official client; inspect actual schema |
| Maishou / 买手妈妈 | Additional candidates with coupon and commission fields | From upstream package: `uv run scripts/main.py search --source=0 --keyword='MODEL'`; `detail --source=SOURCE --id=GOODS_ID` |
| Direct marketplaces | Platform search and specific listing details | cn-scraper MCP tools such as `taobao_search`, `taobao_product`, `jd_search`, `jd_product`; inspect current platform limits and schemas |
| Xianyu / 闲鱼 | Used asking prices, condition, seller descriptions | goofish CLI `search items`, `item get`, `item view`, `auth status`, or their actually exposed MCP equivalents |

Maishou documents source `0` all, `1` Taobao/Tmall, `2` JD, `3` PDD, plus other
sources in its current upstream method. Use returned `goodsId` and source together
for detail. If Haina exposes mall identifiers, take their values and encoding
from current documented or observed data. Direct detail calls use IDs returned
by that platform's search or an identified native product link. Aggregate IDs
are not necessarily interchangeable with direct-platform IDs.

Choose enough sources to resolve the purchase question. Haina is a useful start
for deals and cross-store discovery; direct lookup can verify a concrete SKU;
Xianyu adds the used-market comparison. Maishou supplies another candidate pool.
There is no need to call every source for every request. If selection depends on
specifications or compatibility that shopping data cannot establish, use current
manufacturer evidence and [research](../research/SKILL.md) as needed. Research
owns evidence gathering and source assessment; Shopping owns purchase fit and
comparable offers. A fitting available research method can serve that contribution
when the companion is not installed.

## Compare like with like

Match exact model, variant, capacity, bundle, condition and store before ranking
prices. Keep listing price, coupon price, reported historical paid price,
affiliate commission and the user's verified checkout price distinct.
Maishou `actualPrice` is an upstream label, not proof of the user's payable
price; commission is not an automatic discount. Inspect whether the installed
Maishou tool returns raw detail, purchase links, or both; keep affiliate provenance explicit rather than treating a link as an
independent price verification.

For useful candidates, retain a direct link, model/variant, store or seller,
price type, observation or report date, and material conditions such as coupons,
membership, region, shipping, warranty and used condition when available.
Label missing information and seller claims. Explain the tradeoff that supports
a recommendation rather than treating the lowest visible number as the winner.
Do not promise an exhaustive market minimum from a few sources.

Judge the returned fields, not only `ok` or `state`. Missing IDs, empty titles,
null prices, or engagement text in a price field can make a nominally successful
response unusable. Keep no matches, authentication failure, platform challenge,
parser failure and timeout distinct. A working search does not prove detail
access works. On an explicit platform challenge, stop repeated requests to that
endpoint; use an available alternative or report the remaining boundary.
A later bounded retry can reassess a transient failure.

## Account and access boundaries

Haina uses the recipient's own key and service permissions. Direct platforms and
Xianyu use their actual accepted account sessions. Cached cookie files and an
authentication-status response do not prove remote search or detail acceptance;
verify a useful scoped query and needed detail. Reuse existing authorized sessions
or saved credentials through the recipient host's credential owner. Carry
available sign-in steps through permitted tools; leave observed personal
verification or consent to its actual owner, then verify useful access. Respect
the host's browser and desktop boundaries and keep secrets out of output and
version control. This package assumes no daily-browser access, credential store,
or privately configured session.

Maishou's upstream access identity is not automatically the recipient's shopping
account. Personal mobile-app authorization, an invite code, or a shared shortlink
does not establish an accepted adapter login or platform grant. Inspect current
upstream behavior before asking for authorization again. The upstream script
reads optional `MAISHOU_INVITE_CODE` for detail; that variable does not itself
implement personal search login. No code or credential is supplied here.

Use upstream tools for lookup within this Skill's comparison scope. Some upstream
packages also expose write or messaging tools; their presence does not authorize
buying, paying, contacting sellers, posting, or deleting listings. Those actions
require their own user instruction and applicable transaction boundaries.

## Refresh support at the actual entrypoint

Record the source, observation time, installed version when material, useful
fields, and access limitations for the present task. Keep successful search,
successful detail, and verified checkout as distinct results. A platform challenge
such as `RGV587_ERROR` or `FAIL_SYS_USER_VALIDATE` is access evidence, not a claim
about price or stock. A response such as `pdd未授权` does not prove that a mobile
authorization reached this integration. Engagement or price-change text in an
`original_price` field is not a numeric historical price.

Upstream support and platform behavior can change. Refresh an affected limitation
when needed, replace old observations with successful new evidence, and retain
the actual scope of each result. Consult the installed upstream documentation
for repair and ownership. Ordinary lookup does not require private host records
or reconstructing another installation's history.
