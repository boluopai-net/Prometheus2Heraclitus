# boluopai public website

Public personal homepage for `boluopai.net`. The independent owner-private
`start.boluopai.net` site is outside this project's scope.

## Design and behavior

White reading companion layout with restrained teal links. The 菠萝派 masthead
places language and theme controls on its first row; philosophy, singing, and
GitHub form horizontal section tabs on the second row. The navigation refinement
pass owns this shared header for static pages and generated readers. Language
controls link only to existing counterpart editions, with an explicit unavailable
state otherwise. `site.js` follows the system theme until a visitor selects light
or dark, then persists that choice locally across pages; `site.css` supplies the
shared masthead and dark reading colors without filtering original artwork.
Essays lead with their title and serif prose;
original illustrations accompany the introduction. Desktop contents stay in a
quiet sticky rail; phones use a disclosure below the title. Fire above river is the main animated composition;
YinYang, sun/moon, and sun/river are small paired motifs elsewhere. Canvas
animation can be paused, respects reduced motion, and stops offscreen or when
the tab is hidden. The singing section accurately states that its first
recording is pending. The GitHub section leads to the selected local reading edition.

`dist/` is the tracked static source projection. Its original URLs, HTML, scripts,
and assets are preserved; generated `dist/client/`, `dist/server/`, and
`dist/.openai/` are ignored and excluded from the content generators.
The public hosted site uses the Sites Vinext build integration and a small
Worker for durable feedback; it is no longer a buildless deployment. Run
`npm run build` after finishing content generation. Native Sites publication
uses the installed plugin's `scripts/build-site.mjs` helper, which invokes that
project build. `scripts/build-preserved-site.mjs` snapshots
the original static files into ignored `.static-assets/`, builds without deleting
the source projection, then restores every original file into `dist/client/`.
The Worker serves these assets with `X-Robots-Tag: noindex, nofollow, noarchive`.
Its robots response permits Google/Bing to observe noindex on public documents,
disallows their API/admin crawling, and disallows other crawlers. These controls
request crawler cooperation; public reading does not prevent copying.

### Publication and interrupted transfers

Keep source preparation, local validation, artifact transfer, and hosted
deployment distinct. Reuse a passed build while its inputs are unchanged, push
the exact source revision with the native source helper, and reconcile saved
versions and deployments before retrying an uncertain native call. Continue an
existing deployment through its terminal state instead of creating another.

For this Site, repeated large-archive transfer failures are established evidence:
eleven distinct uploads timed out at about 300 seconds during 2026-10-12–14,
including repeated transfers of identical archives. The latest archive was
about 95 MB compressed. Other archive uploads succeeded, so the evidence shows
an intermittent transfer failure, not a broken build or a proven network cause.
Rebuilding, renaming the archive, changing its extension, or retrying the same
bytes does not address that failure. Retry only when evidence indicates that
the failed condition changed; a new task or new content revision alone is not
such evidence. Do not remove required assets or change the audience to reduce
the transfer.

Native source-only publication successfully built and deployed version 96 from
`0844f80ba1811d4e05f7249698d71f2805a0ec11` on 2026-10-14, preserving the Worker,
static assets and bindings. When the current native tool contract permits this
route, prefer it for this Site while archive transfer remains unreliable:
save the verified pushed commit without an archive, deploy the returned version,
and inspect its terminal result. Retain local validation; server-side build is
the publication route, not a reason to omit source checks. If the current tool
requires an archive despite the observed transfer limitation, identify that
contract conflict explicitly and resolve the supported route rather than
silently cycling between contradictory instructions and identical retries.

Confirm the changed public content at `https://boluopai.net/` and preserve the
version's exact source identity in the collection snapshot. This project record
owns its observed transport behavior; it does not assert the same limitation
for other Sites or replace their audience, credential, or publication owners.

### Public feedback runtime

The Site and its GitHub source repository are public. New comments and replies
use giscus with GitHub sign-in and are stored in the public
`boluopai-net/Prometheus2Heraclitus` Discussions, under Announcements.
The giscus App has metadata read and discussion read/write access to this
repository only. `dist/giscus-comments.js` owns its public IDs and stable terms:
`boluopai:philosophy`, `boluopai:singing`, and `boluopai:resources`.
Strict specific-term mapping shares each discussion across its Chinese/English
pages and across the custom and native Site domains. The widget supports
in-page login, comments, and replies; its link also opens GitHub directly.
GitHub identity does not depend on the old visitor-supplied names.

The earlier anonymous comment system is retired. All suggestion API methods and
old management pages return 410 before storage access. The old UI, client, and
admin handler are removed; migration 0005 drops the suggestions table and its
records. GitHub Discussions are the only current comment storage. The three
bilingual streams remain Philosophy, Singing, and resources; the documents hub
has no separate comment section.

Dependency review (2026-10-12; revisit by 2026-11-12 or before changing runtime
routes): npm audit against the official registry reports existing advisories
in Next/ImageResponse/cache/image routes, RSC server functions, image/source-map
parsers, and build/dev dependencies (glob/YAML, Undici, Vite, Wrangler, ws).
No dependencies changed for comment deletion. The deployed custom Worker handles
the allowlisted APIs and then ASSETS; it does not dispatch Next image/SSR/RSC
routes, accept uploads, or parse visitor-provided SVG, source maps, YAML, or
glob patterns. Dev services bind loopback. These advisories are deferred for
this bounded release based on that inspected entrypoint; this is not a clean
dependency audit or a claim that these versions are generally safe. Reassess
before enabling framework routes or accepting new external build inputs.

`.openai/hosting.json` declares platform-provisioned D1 `DB` and private R2
`BUCKET` bindings. `db/schema.ts` retains the unrelated historical
`rate_limits`, `download_tokens`, and `access_applications` tables.
Sites applies the schema migrations before uploading the Worker.

The header has one GitHub entrance alongside on-site philosophy, singing, and
resources. The homepage's “Continue the conversation” heading links to the
repository root. The retired Contact pages redirect there too. Full source,
archive downloads, cloning, Issues and pull requests
use GitHub's native public workflow. The website presents articles and four
MIT Skill introductions linking to GitHub; it has no access application or download
code form. Comments and replies use GitHub's native identity and moderation.
The bilingual `comment_section` renderer keeps the giscus widget visible in a
labelled section. The widget initializes eagerly without a disclosure click.

Access applications, owner approvals, notification claims/decisions, release
uploads and code redemption are retired. The Worker returns a generic 410 for
`/api/applications`, `/api/admin/applications`, `/api/hermes/applications/*`,
`/api/releases/*`, `/api/download`, `/api/download-requests` and
`/api/admin/download-tokens`; this happens before any database or bucket access.
Old application/download/release UI paths redirect to the public GitHub repository.
There is no active approval consumer in the Site. Any old private local notification
service must remain disabled; its host configuration belongs to the macOS owner.
Historical `access_applications`, `download_tokens` and private R2 objects are
retained privately; this change neither exports nor deletes historical records,
changes credentials, nor drops tables. They are not public source/download data.
The removed application and release handlers cannot process credentials or grants.

Public AI chat remains retired. `/talk/` redirects to GitHub; `/api/visit/*` and
former public bridge claim/complete routes cannot enqueue model work. The status
route returns `online:false, retired:true`. Hermes remains the owner's private
assistant, with no visitor chatbot or website approval workflow.

Acceptance checks the rendered bilingual pages, new motifs, and retired comment
routes returning 410 without database bindings. Hosted readback verifies that
no earlier-comment section or old API data remains. Never post test comments
into the public GitHub discussions.

The 2026-10-12 native npm audit against npmjs reported 1 critical, 21 high,
7 moderate, and 1 low inherited starter advisories (the configured mirror has
no audit endpoint). They concern Next rendering/image/dev routes, React server
functions, Vinext dependencies, and build/preview tools. The deployed Worker
imports no framework request handler or connector fallback; its compiled entry
contains feedback, retired-service responses,
owner moderation, and ASSETS routing, so those framework
routes are unreachable. Dependency upgrades are deferred rather than force-fixed;
reassess advisories before introducing any framework request path or exposing a
development server. Keep the lockfile and Sites build integration intact.

`scripts/render-article.py` renders a registered canonical article to its
own path below `dist/philosophy/`; pass the owner's original Markdown path.
It requires Python Markdown (`uv run --with markdown python ...`). Do not edit
the generated article instead of its canonical source.

The practical toolkit guide is independently maintained in
`content/guides/getting-started.md` and `getting-started.en.md`, with complete
bilingual prose and the tool-map labels in those sources. Run
`uv run --with markdown python scripts/render-guide.py` to project the native
`/getting-started/` and `/getting-started/en/` pages; `dist/guide.css` owns only
their responsive presentation. This is a practical resource, not an additional
philosophy essay or Skill. `reader-pages.py` maintains its prominent homepage
entrances; `render-library.py` maintains the resources-hub entrances. Generate
the guide after library and reader pages, before the Sites build. Shared chrome
is projected automatically, with the resources tab active. Product facts link
to sources checked on 2026-10-13; update both editions when actual availability
or product conditions change, without turning a subscription list or hardware
purchase into a prerequisite for meaningful practice.

The guide connects subscription and instruction setup, search-first tool
adoption, personal philosophy, translation APIs, Vim-oriented human interfaces,
chezmoi configuration, shared Obsidian settings, Drive/GitHub storage, and Web/local
collaboration. Its recurring-work section distinguishes lightweight observation
of changing Web objects from local preparation of usable materials. Local
configuration and automation sources informed these examples; publishing this
guide does not configure the reader's services or claim that every suggested
collector already runs. Preserve that distinction and keep private setup details
out of this public guide.

Canonical essays live in `content/philosophy/meng.md` and
`content/philosophy/baby-heraclitus.md`, together with
`content/philosophy/why-yinyang.md` and `content/philosophy/literary-programming.md`.
The owner selected this repository
as their maintained source on 2026-10-11. The first two originals were initially
imported from the former personal-web-materials folder; subsequent revisions
and the independent explanations “为什么要写阴阳” and “文学式编程” are maintained here.
Preserve completed prose unless the owner requests revision.
Render each with `uv run --with markdown python scripts/render-article.py content/philosophy/SLUG.md`.
Each independent essay now has a maintained `SLUG.en.md` translation. Render
that source with the same command to produce `/philosophy/SLUG/en/`. Keep the
argument, qualifications, and citations aligned when revising either edition.
The home, singing, and wheel English entrances are maintained sibling pages;
the library renderer generates the English philosophy, sequence, repository,
and library entrances. Run the shared navigation refiner after the complete
edition set exists so its language and section links resolve within that set.
Both article renderers and reference documents use the shared `reading_rail`
markup from `scripts/commentaries.py`, with H2/H3 anchors generated from the
complete Markdown. Prose stays expanded. `article.css` owns the common sticky
desktop rail; `library.js` moves that same visible navigation below the title
on phones and marks the current section. The tool map keeps its separate
navigation layout. Full source prose remains linear Markdown.
Section pages are `/philosophy/`, `/singing/`, and
`/repositories/`; the homepage is their overview and navigation entry.

Each of the 20 essays opens with its own concept-specific, cute editorial
illustration in warm ivory, expressive ink line, and restrained gouache.
The built-in image generator created the 2026-10-15 revision as 20 distinct
1536 × 1024 images in `dist/art/<exact-article-slug>.png`; `content/artwork.md`
records the exact final prompts. `scripts/article_art.py` owns bilingual scene
descriptions and shared figure markup for both renderers. Images retain their
full 3:2 composition. Only “The stream and time” adds a temporal inset: two
currents update at different rates, an earlier trace remains, and the present
account changes. Its animation ends after 4.8 seconds; a bilingual native replay
button restarts it through `dist/article-art.js`, including after scrolling.
Reduced-motion and print show the complete final state and hide replay.
Existing standalone figure URLs show the same
article-specific illustration. Private academic materials
are excluded from the public projection. Withdrawn routes have no replacement
page, redirect, or download; local retained materials stay with their owner.
Website copyright
uses the owner's chosen alias BOBBY.

The site-authored “为什么要写阴阳”, “文学式编程”, and “赫拉克利特宝宝”
participate in the same main argument as the common-source essays. “超萌论证”
and the Deleuze/Guattari comparison are anchored branches. Their source owner
does not determine their reading role. Each article uses its exact slug for
artwork, including separate images for personal philosophy and literary
programming; an article without an illustration has no empty image placeholder.
Use “超萌论证” for the meng title and navigation; the argument remains in its
body. Omit anonymous-edition/private-original maintenance notices from reader
UI; source provenance remains in this repository. User correction: 2026-10-12.

Both renderers run `scripts/refine-navigation.py` to remove decorative arrows
from navigation while preserving article prose and semantic diagram viewers.
Chinese readers use the complete `SKILL.zh-CN.md`, `reading-map.zh-CN.md`,
`design-and-revision.zh-CN.md`, and `harness-adaptation.zh-CN.md` editions.
The library presents methods and reading links directly, with maintenance and
formation sources under a separate disclosure in the selected reading language.
Global language controls resolve to actual bilingual counterparts across reader
and section pages. Six website-only Chinese overlays in
`scripts/reader-translations.zh-CN.json` complete encounter, models, relationship,
usage, sources, and the distributed personal-reference index readers. The
renderer checks each original's SHA-256 before applying its translation; these
overlays do not change executable source-package instructions or private models.
Keep source labels faithful to each file's actual purpose. Decorative borders belong to
their owning CSS rules; prose links use the shared teal color, a subtle hover background, and visible keyboard focus without underlines; disclosures retain native carets.
Run it directly after editing static section pages. `design-qa.md` records the
selected visual reference, browser evidence, and responsive verification.

The generator excludes private academic source paths and removes their former
download asset, even when an older canonical checkout contains those files.
Local complete and anonymous PDFs remain outside this Site checkout.

Category motifs follow the current home and section pages: philosophy uses
the Sun, singing the Moon, and resources a notebook. The homepage hero retains
fire and river imagery with its `sun-river.svg` motif.
The shared footer links the Chinese `/rights/` and English `/rights/en/` pages
without underlines. Keep this single compact link at the bottom of each main
page, including the fire/river homepage. These routes forward readers to the
canonical GitHub `LICENSING.md` scope notice and its complete license texts;
omit repeated article, library, and tool-page permission summaries. The YinYang
package license reader retains its complete package notice with one compact
link to that canonical scope owner. Keep package-distributed license files,
source mirrors, third-party notices, separate rights, and earlier valid grants
intact. Presentation changes do not extend or replace any grant.

The Baby Heraclitus essay develops the user's supplied character and cultivation
proposal. On 2026-10-12 the user corrected the intervention order to society,
software, then the individual: adapt arrangements and tools to the person first;
if this resolves the problem, personal change is unnecessary. Voluntary growth
remains distinct from compulsory accommodation of existing norms. This supersedes
the earlier society/individual/software order. It is not a proposal to
circumvent security controls. User source: this project's Codex conversation,
2026-10-11/12. The later attributable wording is: “应该是优先改变社会，其次改变软件，最后改变个人。”
and “如果可以把社会和软件改得符合个人的话，那么这个社会才是对的。”
Philosophical imagery is distinguished from historical attribution
and the conditional practical argument; source links are kept with the essay.
The subsequent 2026-10-12 clarification distinguishes philosophical ontology
from engineering ontology. Baby retains the character's modest naturalism,
fire/process worldview, and shared participation with a language model, then
links to the next essay, World, process, and expression. That canonical essay
develops computational ontology, representation, simulation, and the shared
modeling chain; Trinity and the formation/adaptation methods develop practical
realization. Keep this technical account with those owners rather than turning
the character introduction into another method lesson. The earlier
attributable formulation is “他在工程上是自顶向下的素因的，或者说又素因又归纳；但在哲学上是朴素自然主义。”
The surrounding explicit “溯因” resolves the dictated “素因” in the maintained
prose. The character's Turing-test joke now gives the requested reason: “因为他这个回得太快了”.

The wheel engine is vendored from the installed random-wheel Skill's wheel and
standalone shell assets. It uses secure browser randomness, equal probabilities,
manual start, and a 3x default speed. Public visitors start with an empty list.
The wrapper saves this browser's list, selection, free-input draft, mode and
speed in localStorage. No account, remote catalog, or API is used. Only an
untouched legacy starter list is cleared during migration; visitor-authored
state remains. The owner's separate local wheel is outside this website's
storage and maintenance scope. The wheel entrance appears on the bilingual
homepages, not repeatedly on philosophy or singing pages.

## Publishing

When maintaining this existing Site, reuse `.openai/hosting.json` and its Site ID. Use Sites' source workflow helper
to push and package this exact checkout; source credentials enter through hidden
stdin and must never be written to disk. The required audience is public.
Custom-domain provisioning is separate from publication and must be verified
before claiming the apex domain is live.

The same GitHub collection now carries the complete website under `website/`.
After committing and pushing the final Site source through the native helper,
run the collection's `scripts/sync-website.py --source SITE_CHECKOUT --revision
FULL_SITE_COMMIT --apply`, then repeat without `--apply`. Publish that verified
collection snapshot and deploy this exact Site version. Keep Site-authored
content here and canonical YinYang prose in `skills/yinyang/`; the snapshot is
a checked distribution copy, not a second authoring location. QA captures,
runtime secrets and applicant records are outside that snapshot. An independent
deployment needs its own Site registration, project ID and runtime credentials.

## Scope and provenance

Owner decisions: Codex chat on 2026-10-10/11 selected `boluopai.net`, warm
editorial styling, public access, horizontal navigation, fire/river hero, and
paired motifs. The owner supplied the personal-web-materials directory and its
article `萌⇒无敌.md`. The website publishes that article without its private
filesystem metadata. The supplied singing recording does not yet exist.
Canonical maintenance repository: `https://github.com/boluopai-net/Prometheus2Heraclitus`.
The public collection and GitHub source repository are publicly accessible at this URL. The previous private history is archived separately; only the reviewed clean public tree belongs at the public repository. Public readers link to the repository for source downloads and collaboration.

## Repository reading projection

The website retains its search-exclusion preference while the GitHub source is public. Every
HTML page, including homepages, redirects, essays, repository readers, and
standalone diagram HTML, carries one robots meta directive requesting
noindex/nofollow/noimageindex. `scripts/refine-navigation.py` owns the final
site-wide normalization so regenerated editions retain that choice. The former
static deployment did not apply `_headers`. The current Worker sets
`X-Robots-Tag` explicitly, verified in hosted responses, alongside page-level
directives. The robots policy lets Google/Bing retrieve public documents to
observe noindex and disallows other crawlers.
This is discoverability control, not access control; verify the live HTML.

The current owner selection licenses YinYang and original philosophical text under CC BY-NC-SA 4.0, permitting sharing and adaptations for noncommercial purposes only, with attribution, a license link, indication of changes, and ShareAlike. The four independent Skills use MIT. Photos, singing recordings, third-party material, and other separately designated material retain their own rights. The YinYang license reader uses the canonical package LICENSE. `dist/licenses/MIT.txt` is a legacy URL serving an accurate website licensing-scope notice, not a universal MIT grant.

`scripts/render-library.py` builds `/repositories/prometheus/` from an explicit
shared GitHub repository checkout. Run:

```sh
uv run --with markdown python scripts/render-library.py --repo /path/to/Prometheus2Heraclitus
```

Only tracked common-package files are eligible. This projection does not read
the situated YinYang package or private sources. It renders the complete
Markdown editions, resolves document and figure links locally, and copies
the original interactive HTML/SVG diagrams without changing their semantics.
Standalone HTML gains only a robots meta directive; SVG assets remain exact.
JSON candidates and validation metadata are not published. Change content at
the shared repository owner, then regenerate; generated reader pages are not
independently maintained copies. Regeneration replaces only the reader subtree
and repositories landing page, leaving the singing section intact.

The same command projects selected common essays into Chinese
`/philosophy/SLUG/` and English `/philosophy/SLUG/en/` editions. The visible
argument is “窃火，然后成为火 / Borrow Fire, Then Become Fire”: five stages
with sixteen main articles and five anchored branch articles. The landing
shows five stage entrances; `/philosophy/yinyang/` retains its URL and shows
the complete order. Branches return to the relevant continuation, and the
getting-started guide supplies a practical entrance without requiring every
article to be read first.
`scripts/commentaries.py` owns this shared route across source owners. Common
prose remains in `skills/yinyang/references/docs/SLUG[.zh-CN].md`; site-authored
prose remains in `content/philosophy/`. Render the common library first, then
both editions of the five site-authored articles with `render-article.py`,
which resolves common navigation titles from their rendered editions. Render
reader-page entrances and the getting-started guide afterward. No prose is
duplicated merely to place an article into the shared argument.

Title-bearing homepage and resource entrances carry `data-page-title` on their
local directory-page links. The existing final navigation projection reads the
destination's rendered H1, so renaming an article or guide updates those labels
without maintaining another title table. `check-repository-entry.py` checks the
result against the actual destination. Series navigation already uses
`commentaries.py`'s title resolver. Contextual prose and section labels remain
authored: when a title changes, inspect its incoming source links in both
languages, correct stale names at their Markdown owner, then regenerate them.

The public common repository carries its license scope and complete package licenses. Source downloads and GitHub collaboration are public. Link the canonical GitHub licensing scope from the rights sources and generated license reader; do not reintroduce access applications or codes.
`dist/rights/{index.html,en/index.html}` are the tracked rights-page sources;
`.static-assets/` and `dist/client/` are build projections. Maintain the
generated license introductions in `scripts/render-library.py` and the concise
access distinction in `scripts/reader-pages.py` alongside those source pages.
The original `meng` and `baby-heraclitus` article pages are never regenerated by
this command. Their index entries live under the independent-essays heading,
without numbering them as part of YinYang. Migrated commentaries
retain the reader's noindex/nofollow/noimageindex directives. Public readers link within the website and to the public GitHub source, including source revision permalinks.
Old source-reading essay URLs are generated redirects that retain URL fragments.
Retired metaphors and Oedipus reading URLs lead to Taiji; the former anthology's
`YM-01` through `YM-08` anchors lead to their corresponding successor essays.
Links between essays, use documents, headings and footnotes resolve
within the website; the same vendored KaTeX renders both reading sections.
Ordinary inline formulas allow visible glyph overhang. `library.js` measures
the rendered KaTeX width after font loading and on reader resize, adding a
horizontal scroll area only for an inline formula wider than its reader.
This avoids small subscript formulas turning into scroll boxes while keeping
the full content of genuinely wide formulas reachable.
For migrated essays, Markdown navigation inside native `<details>` is rendered
with `md_in_html`; the presentation adds its parsing attribute without changing
canonical prose or the existing article render paths.
The library landing lists use documents alongside interactive
maps, with a link to the commentary collection rather than another essay catalog.
Poetic illustrations are taken from `dist/art/SLUG.png` when present; add the
assets before the final render. Image production and source edits are separate
from projection. Rebuild after committing canonical changes, passing the exact
source revision with `--revision` when identifying a reviewed edition.

The default source permalink revision is the supplied repository's HEAD.
The same render builds bilingual introductions at
`/tools/<skill-name>/`
and their `/en/` counterparts. `scripts/public_skill_pages.py` owns these
introductions and collection cards. Each links to its complete package directory
in the public GitHub repository. All source downloads use GitHub (clone or
Code → Download ZIP); the website creates and serves no separate Skill ZIPs.
YinYang uses CC BY-NC-SA 4.0; the other reusable packages retain their MIT licenses.
Each introduction preserves the package's companion-method and host-capability
requirements; collection membership does not imply standalone installation.

`scripts/reader-pages.py` rebuilds the singing station from
`content/singing/recordings.json` through `scripts/singing_pages.py`, then adds
the existing Singing comments for requests and submission proposals. The empty
catalog truthfully shows no published recordings. Accepted entries require
`title`, `performer`, `audio_url`, `source_url`, and `rights`; audio/source URLs
must be HTTPS or site-relative. Native audio controls use no autoplay and no
preload. Keep rights per recording; neither the package MIT license nor YinYang's
CC license grants rights to a recording. This source catalog is the publication
owner; comments are proposals, not uploads or automatic publication.

`scripts/cjk_markdown.py` adds CJK-adjacent strong emphasis to the practical guide.
Code, escapes, and links retain their normal Markdown handling. Recheck visible
text after rendering when changing this boundary.

`--revision FULL_COMMIT_SHA` can identify the reviewed, published source revision;
the checkout must contain that same content before publication. Commit source
changes before the final render so displayed permalinks identify the rendered text.

KaTeX 0.16.22 is vendored in `scripts/vendor/katex/` with its MIT license and
fonts; the renderer copies it into the generated reader subtree. Formula TeX
is protected before Markdown rendering and retained in HTML, including a readable
fallback. Fenced pseudocode remains exact code. No CDN or backend is required.
The pinned npm distribution is `https://registry.npmjs.org/katex/-/katex-0.16.22.tgz`,
with npm integrity `sha512-XCHRdUw4lf3SKBaJe4EvgqIuWwkPSo9XoeO8GjQW94Bp7TWv9hNhzZjZ+OH9yf1UmLygb7DIT5GSFQiyt16zYg==`.
Dependency updates require rechecking formula rendering and retaining licenses.
