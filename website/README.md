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
Worker for routing and immutable public content snapshots. Runtime changes use
`npm run build`; ordinary content generation uses the content release route
below without a Worker build or deployment. Native Sites runtime publication
uses the installed plugin's `scripts/build-site.mjs` helper, which invokes that
project build. `scripts/build-preserved-site.mjs` preserves the tracked root
projection, builds the Worker with the existing Vinext/Sites integration, then
removes generated `dist/client/` and the emitted Wrangler asset configuration.
Vite public-directory copying and the `ASSETS` binding/fallback are disabled.
Public documents and resources come only from the selected R2 snapshot, with
`X-Robots-Tag: noindex, nofollow, noarchive`.
Its robots response permits Google/Bing to observe noindex on public documents,
disallows their API/admin crawling, and disallows other crawlers. These controls
request crawler cooperation; public reading does not prevent copying.

### Publication and interrupted transfers

Select the route from the changed object before building or calling native Sites:

- For ordinary content changes—canonical prose, rendered pages, illustrations,
  source views, browser scripts, CSS, fonts or other files in the public
  projection—follow [content releases without runtime deployment](#content-releases-without-runtime-deployment).
  Render and commit the complete projection, prepare the exact Git revision,
  then delta publish and verify the reader. This route performs no framework
  build, library packaging, native Sites save or service deployment.
- For runtime source changes—Worker handlers, release protocol, binding declarations
  or build/deployment configuration—use the native Git-first route below.
  A change that needs both routes deploys its compatible runtime first, then
  publishes content through the content route.

For runtime changes only, publish from Git first: validate the changed source,
commit and push it to the selected Site repository, and verify the exact remote
SHA. Call
`save_site_version` with that `project_id` and `commit_sha`, omitting `archive`,
then deploy the returned saved version and follow its remote build to a terminal
result. Reuse a passed local build while its inputs are unchanged. This route
order is the owner's explicit instruction of 2026-10-16 and takes precedence
over the Sites plugin's general preference for an archive when local packaging
is possible. Preserve the existing Site identity, audience and runtime bindings.

The native `site-workflow.mjs` helper does not choose between content and runtime
routes. For runtime publication, omitting `archivePath` in the current helper
opens and reconciles source only; it does not
commit or push edits. Use that opening operation when needed, then commit and
push the exact source with Git using the short-lived credential for the same
Site. Keep the credential in memory or hidden stdin and an ephemeral Git header
environment; never put it in command arguments, files, persistent Git config
or logs. Supplying `archivePath` makes the helper run the requested checks,
commit, push and package; reserve that operation for the archive fallback.

Consider a locally built archive only when the direct Git/source build route
is unavailable or fails and the observed failure makes an archive a suitable
recovery. Defer both archive generation and upload until that fallback is
selected; a successful Git-first run prepares no archive. Retain the same exact
source revision and Site identity. An uncertain
save must first be reconciled against saved versions by source SHA; an existing
deployment must be continued through its terminal state. Neither a timeout nor
a missing response authorizes a duplicate save or deployment. Retain the raw
native error and retry only when evidence supports the recovery.

Repeated archive transfers have timed out at approximately 300 seconds,
including eleven distinct uploads on 2026-10-12–14 and two uploads of the same
approximately 133 MB archive on 2026-10-16. Other uploads succeeded, so this is
an intermittent transfer failure with no established network cause. Rebuilding,
renaming, changing the extension or retrying identical bytes does not address
it. Keep required assets and the audience intact. Source-only publication
successfully built and deployed version 96 on 2026-10-14 and version 124 from
`9409ae0e11ef7b74387a69cca6ed35a865884ea8` on 2026-10-16, preserving the Worker,
static assets and bindings. Reuse that real route evidence; documentation-only
publication changes do not require redeploying unchanged public content.

Confirm the changed runtime at `https://boluopai.net/` and preserve the
version's exact source identity in the collection snapshot. This project record
owns its observed transport behavior; it does not assert the same limitation
for other Sites or replace their audience, credential, or publication owners.

### Content releases without runtime deployment

`lib/content-release.js` owns the content protocol and read boundary;
`scripts/content-release.mjs` is its local publisher. Author canonical sources
and run the existing renderers into tracked `dist/`, preserving source views,
rights, canonical URLs, giscus and the bilingual editions. Commit the complete
source and projection through the repository owner. Then prepare an immutable
candidate from that exact Git commit; this reads committed blobs rather than
the working directory and checks the complete resource dependency closure:

```sh
node scripts/content-release.mjs prepare --commit COMMIT --out /tmp/NEW-CANDIDATE
```

The candidate includes every tracked public `dist/` file, including images,
scripts, CSS, sibling fonts, JSON and source-view assets. It excludes generated
`dist/client/`, `dist/server/` and `dist/.openai/`. It does not run the framework
build, package a library archive, save a Sites version or deploy the service.
`prepare` requires a new output directory and reports manifest digest, source
commit, file/object counts, bytes and validation partition count. A candidate
is disposable local evidence, not another maintained authoring source.

For remote commands, pipe one JSON object `{"key":"…"}` from runtime Bitwarden
retrieval into stdin. The separate hosted secret is `CONTENT_PUBLISH_KEY`; the
owner/publisher maintains its vault entry and sets it using native Sites secret
tools. Never use the Hermes bridge key, historical release credentials, source
repository credentials or a private Site service token for this public write
authority. Do not place the key in command arguments, environment variables,
files, shell history, source or output. With that pipe prepared, the receiving
command is:

```sh
node scripts/content-release.mjs publish --site https://boluopai.net --candidate /tmp/NEW-CANDIDATE
```

`publish` reads active state before upload, reuses digests in its already
validated manifest, uploads only new objects, stages the exact manifest bytes,
validates every partition and conditionally promotes against the initially read
pointer ETag. It then checks status and the actual homepage version headers.
Object sizes/digests and closure are validated server-side before promotion;
R2 checks SHA-256 during immutable object PUT. Validation uses that checksum
metadata for unchanged binaries and reads HTML/CSS/JS to verify dependencies.
There are at most 32 objects per validation request. All immutable receipts
must name the exact manifest digest and complete partition before promotion.
The 451-file initial projection has 410 distinct objects and 15 partitions.

Individual `upload`, `stage`, `validate` and `promote` commands accept the same
Site and candidate arguments. `promote` additionally requires `--expected ETAG`,
or `--expected null` for an empty store. `upload` explicitly checks object
existence even for currently active digests, allowing repair of observed object
loss. These commands preserve the same candidate identity across retries.
`status --site ORIGIN` reads the active manifest, source commit, ETag and
bootstrap-retirement state. `reconcile --site ORIGIN --candidate DIRECTORY`
adds `matches` for that exact candidate. A timeout is an unknown outcome: read
status/reconcile before retrying the affected operation. The CLI never retries
an uncertain mutation automatically; an identical completed promotion is
idempotent, while an old ETag cannot overwrite a newer publication.

The API is `/api/content-release`: authenticated `GET /status`, `HEAD|PUT
/objects/<sha256>`, `GET|PUT /manifests/<digest>`, `POST
/validate/<digest>/<zero-based-part>`, `POST /promote` with
`{"manifest":"<digest>","expected":"<ETag>"}` (or null), and `POST
/retire-bootstrap`. All use `Authorization: Bearer <CONTENT_PUBLISH_KEY>`.
Manifests are exact UTF-8 JSON bytes, identified by their SHA-256, with this
schema and strictly sorted unique file paths:

```json
{"schema":1,"source":{"commit":"<40 lowercase hex>"},"files":[{"path":"/index.html","sha256":"<64 lowercase hex>","size":123,"contentType":"text/html; charset=utf-8"}]}
```

Paths must be unambiguous ASCII public paths, with no traversal, dot segments,
percent encoding, service/auth routes or snapshot prefix. The runtime accepts
at most 1024 files, 16 MiB per object and 2 MiB per manifest. MIME types have an
explicit allowlist. This is one complete snapshot, not a partial patch.

Only `public-content/v1/` in the existing logical `BUCKET` binding belongs to
this feature. It stores immutable objects, manifests and validation receipts,
plus a CAS active pointer and irreversible bootstrap-retirement marker. There
is no bucket listing, raw-key endpoint, remote URL import, anonymous write,
database migration, queue or new CMS. Historical private bucket objects remain
private and untouched. The updater route is deliberately before the generic
API handler; old API retirement, redirects and robots retain precedence over
document reads.

The initial transition runtime (v127) retained bundled assets while seeding R2.
Hosted readback showed that matching static assets could bypass the Worker despite
the emitted `run_worker_first: true`; existing-page responses lacked all Worker
headers while API and missing-path requests reached it. The following runtime
removes deployed client assets and the ASSETS fallback. Deploy that runtime only
after the publisher verifies the complete R2 seed, active pointer and snapshot
reader. Tracked root `dist/` remains the Git authoring/export projection.

Promotion writes the active pointer before the permanent bootstrap-retirement
marker. An uncertain marker outcome can still be reconciled with status plus
`retire-bootstrap` (or identical promotion), without interrupting active reads.
There is no bundled fallback in the current runtime: missing paths return 404,
missing selected objects return 503, and an absent active pointer or storage
binding returns 503 regardless of the marker. No request can mix stale bundled
assets into the selected snapshot.

Canonical requests select one complete active manifest. Responses identify
`X-Content-Manifest` and `X-Content-Source` without private metadata. The runtime
pins HTML resource attributes (including iframe, srcset, object and embed),
CSS URLs and the current repository/wheel data fetches to
`/_content/<manifest>/<public-path>`. Each pinned request must belong to that
manifest; old snapshot resources remain readable after promotion. Navigation,
canonical/alternate URLs and external giscus retain their existing behavior.
The digests describe original source bytes; HTML/CSS/JS responses may contain
the snapshot URL projection. `npm run test:content` exercises the actual Worker
in Miniflare, including private-object isolation, authorization, closure,
partition completeness, simultaneous CAS and bootstrap retirement/recovery.

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
No dependencies changed for comment deletion or the content runtime. The custom
Worker handles the authenticated content publisher, retired APIs and snapshot
reader; it does not dispatch Next image/SSR/RSC routes, accept anonymous uploads,
or parse visitor-provided SVG, source maps, YAML, or
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
archive downloads, cloning and Issues use GitHub's native public workflow.
The collection does not accept pull requests. Readers publish independent works
in their own spaces and mention or link the collection, or use Issues for questions
and song requests to boluopai. The website presents articles and reusable
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
contains retired-service responses, authenticated content publication and
snapshot reads, so those framework
routes are unreachable. Dependency upgrades are deferred rather than force-fixed;
reassess advisories before introducing any framework request path or exposing a
development server. Keep the lockfile and Sites build integration intact.

`scripts/render-library.py --repo /path/to/Prometheus2Heraclitus` renders every
philosophical essay and both book menus from the public package in one pass.
It requires Python Markdown (`uv run --with markdown python ...`). Edit the
canonical package source rather than generated articles.

The practical toolkit guide is maintained in the public package at
`skills/yinyang/references/docs/getting-started.md` and `getting-started.zh-CN.md`.
The library renderer also invokes `render-guide.py --repo /path/to/Prometheus2Heraclitus`
to render the native
`/getting-started/` and `/getting-started/en/` as two continuous articles,
retaining every section and the ending from their respective source. Only the
duplicated source tool-map navigation is removed from the projection. A flat
nine-section navigation uses the actual source H2 labels and stable fragment IDs:
a sticky, independently scrolling desktop rail and an expanded vertical list
above the article in normal flow on narrow screens. There is no nested menu or
horizontal navigation. Native anchors own clicks, keyboard navigation, deep links,
and history; `dist/guide.js` follows reading progress, reveals the active link
inside the desktop rail only, and retains valid fragments in the language
control. Updating the current section never pulls a narrow-screen reader back
to the contents.
`dist/guide.css` owns responsive presentation. The six old topic routes
(`start/`, `reading/`, `tools/`, `continuity/`, `practice/`, `automation/`)
in both languages are small direct aliases to the article: a valid source
fragment is retained, otherwise the topic's first section is selected. Each alias
also provides an ordinary no-JavaScript fallback link. Generated pages are not
independent prose sources. The content-release owner pins the ordinary
`/guide.js` script resource along with the existing styles, without a runtime
protocol change.
This is a practical resource, not an additional philosophy essay or Skill.
The separate research and learning guide is authored at
`skills/yinyang/references/docs/research-and-learning{,.zh-CN}.md` and rendered
by the same script at `/research-learning/` and `/research-learning/en/`.
Its three source anchors drive the existing reading navigation. It has its own
resources-hub entrance and reciprocal links with the general guide; specialist
repository recommendations and the two teachers' purposes stay there, with
operational procedures and private environment inventories excluded. Library source
views redirect to these reading routes, and both guides remain complete bilingual
projections of the public package.
`reader-pages.py` maintains its prominent homepage entrances;
`resource_pages.py`, called by library generation, maintains the resources-hub entrances. Generate the guide
after library and reader pages, before preparing a content release. Shared
chrome is projected automatically, with the resources tab active. The earlier
product-source review was dated 2026-10-13. A focused 2026-10-17 revision reviews
global setup, shared sources, plugin connections, and compatible API gateways
against linked primary sources; it does not refresh every unchanged product fact.
Update both editions when actual availability
or product conditions change, without turning a subscription list or hardware
purchase into a prerequisite for meaningful practice.

The guide connects subscription and instruction setup with an author-recommended
default of simple globally shared Skills, plugins, and MCP configuration and
Full Access for ordinary global work locally, retaining local exceptions for
concrete needs. This recommendation is not an official product default or a
grant of service access. Optional CC Switch manages client configuration;
Sub2API and CLIProxyAPI illustrate compatible-API translation routes. Native
plugin installation, service connection, and actual tool availability remain
distinct. Section 6 owns the relationship among general Web cloud work, Dot's
cloud and connected repository environments, and local execution: Drive holds
materials and documents, GitHub holds versioned code, configuration, and Skills,
and results return to their existing maintained owners. Shared sources reduce
machine-specific friction without mirroring local sessions or granting access.
Section 9 applies that distinction to recurring work and result writeback,
alongside lightweight Web observation and local material preparation. Chinese
Skill discovery, search-first adoption, Vim-oriented human interfaces, chezmoi,
and shared Obsidian settings retain their practical roles. Local configuration
and automation sources informed these examples; publishing the guide does not
configure the reader's services or claim that every suggested collector runs.
Keep private setup details out of this public guide.

All philosophical essays, including Super-Cuteness, Baby Heraclitus, personal
philosophy, literary programming, and Machines and becoming, are authored in
the public collection's `skills/yinyang/references/docs/`. English uses
`SLUG.md` and Chinese uses `SLUG.zh-CN.md`. The owner unified these sources on
2026-10-22; Git retains the former Site-authored editions. The library renderer
preserves `/philosophy/SLUG/` and `/philosophy/SLUG/en/`. Keep arguments,
qualifications, citations, and existing heading anchors aligned when revising.
The home, singing, and wheel English entrances are maintained sibling pages;
the library renderer generates the English philosophy, sequence, repository,
and library entrances. Run the shared navigation refiner after the complete
edition set exists so its language and section links resolve within that set.
Both article renderers generate H2/H3 anchors from the complete Markdown.
The philosophy overview uses cross-page book navigation on the left; essays
also have current-page contents on the right at wide desktop widths. At
narrower widths, essay contents and the book-menu control appear together
before the title, using native disclosures with the book menu closed by
default. Reference documents retain their shared left `reading_rail` and
existing mobile placement. `scripts/commentaries.py`
owns these navigation structures, `article.css` owns their responsive layout,
and `library.js` moves the contents and marks the current section. Prose stays
expanded. The tool map keeps its separate navigation layout. Full source prose
remains linear Markdown.
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
`design-and-revision.zh-CN.md`, the formation guides, and
`formation/revision.zh-CN.md` edition. The library presents three shared entrances:
practice overview, philosophy and models, and using YinYang. Environment
realization belongs in the environment writing guide, alongside the revision
writing guide. The overview no longer concatenates the package contract, which
has its own file/update page; the old overview `#package-contract` link forwards
there. Six public writing guides sit together under the philosophy/models
disclosure. Each guides one actual private account, including the adopted
revision method: six guides and six actual accounts, with only the guides public.
Global language controls resolve to actual bilingual counterparts across reader
and section pages. Human projections omit the package's opening and closing
navigation rows in favor of their own collection, series, and edition controls;
body links and arguments remain. Explicit edition links retain their authored
language target, while ordinary conceptual links select the current reader's
available counterpart. The five core writing guides use the canonical bilingual
`references/formation/{orientation,person,counterpart,relationship,environment,revision}`
editions. Source/evidence guidance is part of `formation/revision`;
former `formation/sources` URLs redirect to that section, and `revision-guide`
URLs redirect to the revision writing guide. The actual accounts
and private evidence remain outside the public reader. Earlier encounter,
models, relationship, usage, and sources guide URLs redirect to their public
successors. The former website-only Chinese overlays are retired now that their
successors have complete canonical editions.
Keep source labels faithful to each file's actual purpose. Decorative borders belong to
their owning CSS rules; prose links use the shared teal color, a subtle hover background, and visible keyboard focus without underlines; disclosures retain native carets.
Run it directly after editing static section pages. `design-qa.md` records the
selected visual reference, browser evidence, and responsive verification.

The generator excludes `references/situated/`, `references/personal/`, and
private academic source paths, even when a supplied canonical checkout tracks
those files. It also removes the former private academic download asset.
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

### YinYang PDF reading editions

The Site also publishes two reading editions at `/reading/yinyang.zh-CN.pdf`
and `/reading/yinyang.en.pdf`, linked from the philosophy entrance. These are
reading projections, not Skill packages or replacements for the public source.
The canonical prose remains in the public YinYang package. The PDF builder
reads an exact committed source revision; the main sequence comes from
`commentaries.py` and its one branch, followed by public writing guides and
reading references. Private actual files and personal evidence are excluded.
“Steal Fire, Then Become Fire” names the complete nineteen-essay main sequence,
not just its opening essay. Core views follows that whole sequence and its
existing focused extension. Figures use `reading_maps.diagram_placements`,
the same article and paragraph locations as the website reader. Gallery order
does not determine their first introduction in the book. No PDF-only bridge
paragraphs or alternate philosophical ordering are maintained.

On this Mac, regenerate both editions with installed Pandoc, Typst, `sips`,
and the managed headless `browser-relay` carrier:

```sh
python3 scripts/build-reading-pdf.py --repo /path/to/Prometheus2Heraclitus --revision FULL_PUBLIC_SHA --work /tmp/NEW-PDF-BUILD
```

`--sample --language zh-CN --out /tmp/PDF-SAMPLE` makes a disposable short
sample. Default output is tracked `dist/reading/`; do not publish sample
output. The builder retains specific section/alias targets, namespaces internal
links, produces PDF bookmarks, and unwraps content disclosures. Original public
SVG figures are scaled proportionally to the text width and flow with prose on
ordinary portrait pages. Each part starts on a fresh page with its first chapter,
using a black part heading and generous whitespace; subsequent articles start on fresh pages.
The opening reading note stays separate, and part titles never receive a title-only
page. Browser-only CSS and embedded artwork are resolved in a task-owned
loopback browser; that exact target and server
are closed after generation. Temporary ASTs, media, and coverage reports stay
in the selected temporary build directory.

The reading body is self-contained: references to included own material become
book-internal destinations, and uncollected own references keep their descriptive
text without outbound links. External authors' and research sources' links are
retained. Own repository/site provenance and rights locators belong only in the
opening reading note, not repeated under figures or at the end of the book.

The website and PDF share reader-facing Chinese-concept labels through
`scripts/reader_names.py`. PDF naming runs after source anchors and figure
placement are resolved; quotations, code, URLs and identifiers retain their
original values. Philosopher names remain authored judgments under the public
YinYang `MODEL.md`, not name-frequency classifications in the renderer.

The print template is `scripts/pdf/reading.typ`. Its current font set is
Libertinus Serif, Songti SC, PingFang SC, Helvetica Neue and STIX Two Math.
Validate both editions' text coverage, internal destinations, tables, formulas
and rendered pages after a material source/template change; generation alone
does not establish readable output. Each PDF must remain under the content
release's 16 MiB object ceiling, enforced by the builder. Commit regenerated
PDFs with their source changes, publish through the ordinary content release,
and read back the actual downloaded files. No separate release/tag or scheduler
is introduced by this reading feature.

The `/downloads/` prefix belongs to the retired package-access service and is
redirected before static content lookup. Reading editions use `/reading/`;
validate their actual hosted responses, not only manifest membership.

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

The current owner selection licenses YinYang and original philosophical text under CC BY-NC-SA 4.0, permitting sharing and adaptations for noncommercial purposes only, with attribution, a license link, indication of changes, and ShareAlike. The other reusable Skill packages use their package-local MIT licenses. Photos, singing recordings, third-party material, and other separately designated material retain their own rights. The YinYang license reader uses the canonical package LICENSE. `dist/licenses/MIT.txt` is a legacy URL serving an accurate website licensing-scope notice, not a universal MIT grant.

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
argument is “窃火，然后成为火 / Borrow Fire, Then Become Fire”: five structural
chapters with nineteen main articles and one focused branch article. Its 42
canonical pages are two overview editions and forty essay editions. Chapter
headings link directly to their first essay; child links open the selected
essay. There are no separate chapter introductions or introduction JSON source.
`scripts/commentaries.py` owns the chapter map and article order. Twelve
compatibility aliases retain the ten former `/philosophy/stages/SLUG/{en/}`
URLs and two `/philosophy/yinyang/{en/}` URLs. Former stage URLs and exact
`#stage-1` through `#stage-5` YinYang links resolve directly to the corresponding
first essay, with ordinary links also available without JavaScript. Branches
return to the relevant continuation, and the
getting-started guide supplies a practical entrance without requiring every
article to be read first.
`scripts/commentaries.py` owns the shared route. Every essay's prose lives in
`skills/yinyang/references/docs/SLUG[.zh-CN].md` in the public collection.
Render the library once to refresh all forty essay editions, both book
overviews, the twelve legacy aliases, reader entrances, and the practical guide.
Run `python scripts/check-repository-entry.py`
after generation; it compares every desktop/mobile book menu with the current
route and destination titles, catching incomplete regeneration.

The shared essay renderer uses the opening order: H1, artwork with any muted
figure caption, series position marker, one reading-route lead, then the
canonical body. The shared `reading_context` supplies the marker and lead.
Before the position marker, only the title, artwork, and muted figure material
belong; ordinary body-style prose begins below it. The current layout omits a
standalone subtitle and duplicate visible overview; the native article overview
remains the document's metadata description only. This applies to main and branch
essays in both languages.

Title-bearing homepage and resource entrances carry `data-page-title` on their
local directory-page links. The existing final navigation projection reads the
destination's rendered H1, so renaming an article or guide updates those labels
without maintaining another title table. `check-repository-entry.py` checks the
result against the actual destination. Series navigation already uses
`commentaries.py`'s title resolver. Contextual prose and section labels remain
authored: when a title changes, inspect its incoming source links in both
languages, correct stale names at their Markdown owner, then regenerate them.

The philosophy overview keeps its five chapter entries followed by five compact
diagram references for review. The library keeps all five diagram entrances in
a native disclosure, initially closed and placed before the document groups.
Review entrances place the two fire illustrations first, the Trinity-and-sinthome
comic next on its own row, then shared inquiry and world-to-practice relations.
Each library figure and standalone reader has one “查看正文” / “Read in context”
link to its first embedded article location. These links use the same stable
figure anchors as the article renderer and do not depend on browser history.
`reading_maps.inline_diagrams` embeds the canonical bilingual diagrams where
their arguments first develop: borrowed fire after the stealing-fire opening,
six dimensions in personal-first humanism, and shared inquiry and formation
in the corresponding why-YinYang sections. The four-panel `trinity-sinthome`
comic stays together beside the Trinity-and-sinthome discussion in
`local-source-and-website`; it is not split between articles. Its responsive
viewer uses a two-by-two composition on wide screens and a continuous vertical
composition on narrow screens. Later references retain the standalone
diagram readers; no duplicate philosophical prose or diagram source is created.
The article uses only graph surfaces: responsive SVG compositions for the three
reading maps and native SVG exports for the detailed maps. Toolbars, explanatory
cards, and node indexes remain in the standalone readers. The `layers` graph
connects six adopted philosophical views to shared practice through seven nodes;
its explanatory cards distinguish physical grounding, computational
representation, truth and inference, and guidance by value and method. Activity
histories can be organized as event streams; conceptual participant models are
inferred from histories and other material. The computational ontology represents
actual, hypothetical, and fictional domains while its use is physically realized.
Its canonical Archify candidates retain click/focus, relationship inspection,
guided views, and SVG exports in both reading languages. The `formation-path` and `borrowed-fire`
views are actual SVG relationship diagrams, without article indexes, disclosure
cards, cross-diagram links, or separate-open buttons. Canonical
`reading-maps.json` and `render-reading-maps.py` own their bilingual labels,
accessible descriptions, and desktop/mobile compositions.
`scripts/reading_maps.py` supplies the standalone and in-article embeds.
`dist/reading-map-embed.js` accepts height messages solely from a matching
same-origin frame and propagates the reader's current theme.

The public common repository carries its license scope and complete package licenses. Source downloads and GitHub collaboration are public. Link the canonical GitHub licensing scope from the rights sources and generated license reader; do not reintroduce access applications or codes.
`dist/rights/{index.html,en/index.html}` are the tracked rights-page sources;
Legacy `.static-assets/` and generated `dist/client/` are disposable build
projections excluded from the runtime. Maintain the
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
`content/singing/recordings.json` through `scripts/singing_pages.py`. The station
links to GitHub Issues for song requests to boluopai only; it has no recording
submission or Singing comment widget. Existing discussion history is retained
at its GitHub owner. The empty catalog truthfully shows no published recordings.
Owner-published entries require
`title`, `performer`, `audio_url`, `source_url`, and `rights`; audio/source URLs
must be HTTPS or site-relative. Native audio controls use no autoplay and no
preload. Keep rights per recording; neither the package MIT license nor YinYang's
CC license grants rights to a recording. This source catalog is the publication
owner; requests do not upload recordings or publish content automatically.

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
