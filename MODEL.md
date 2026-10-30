# Maintaining the Prometheus2Heraclitus collection

**Prometheus2Heraclitus** develops a philosophy for assisting personal recursive
self-improvement, realized through YinYang and a collection of reusable Skills.
Personal RSI concerns improved understanding, judgment, creation, action, and
the methods producing those improvements within a person's actual support
relations. The essays own its argument; descriptions, collaboration, and tools
give it practical form. Each
member under `skills/` owns its entrypoint, methods, references, documents,
diagrams, scripts, and other supporting resources. Independent members retain
their own purpose and specialist responsibilities. Collection membership does
not make every resource part of YinYang or impose its philosophical account.

The collection offers its working Skills as examples for adoption, combination,
and independent authorship. YinYang's philosophy is this example's developed
account, not a required worldview for recipients. Its literary/philosophical
form can inspire a differently organized work. Preserve the distinction between
maintaining the existing implementation and authoring another one. The website
projects selected source documents and diagrams; maintain their meaning here,
with source revision and rights traceable in that reading surface.

The root README editions are the collection entrance. Keep their descriptions
aligned with the actual members and preserve full semantic parity. English is
the first reading language for English-capable readers and models; model-facing
maintenance prose remains English.

Use the native English Skill identifier for package names, entrypoint headings,
catalog links, and website titles in both reading languages. Put the Chinese
invocation cue and purpose in `description`, prefixed with `<用户自制>` for these
author-created Skills, followed by the accurate English discovery description.
The website renders that source description as readable text, including its
literal angle brackets. Names and descriptions have separate display roles.

## YinYang editions

`skills/yinyang/` is the Full edition, including the author's essays and diagrams.
`skills/yinyang-empty/` is the Empty edition: reverse alignment, crossed roles and
dialectical return, six formation guides, Core views as attributed suggestions,
practice overview, formation/revision, daily collaboration, and Personal guidance.
Empty contains no `docs/` or `diagrams/`. Recipients develop their own philosophy,
Personal material, and six complete working accounts with their model; neither edition
ships private substance. Empty supplies unfilled Personal and Situated starters,
with four empty Personal areas plus six actual starters marked `status: unfilled`;
these are templates rather than actual accounts. The simple route retains the
six original actual files, direct model synthesis and private Git/GitHub
persistence, with no Hindsight installation requirement. Optional native
Hindsight configuration implements the same six full questions, revision steps
and whole-six coherence, projected to those paths or an explicit all-six binding.
Full/Empty distribution is independent of route choice. Keep one shared
philosophy/method source rather than separate full packages for the tool routes.

Shared method content remains authored in Full. `scripts/build-yinyang-empty.py`
projects its declared selection into Empty, relocating the selected guides and
converting links to omitted essays into optional public reading links. It adapts
the shared guide's Full-specific distribution sentence to Empty's unfilled starters.
Empty's
entrypoint, README editions, and package guidance are authored in its own tree.
Do not edit generated Empty references independently. `build-plugins.py` invokes
the selection builder in the same check/apply mode before packaging both editions.
The two plugin identities are `yinyang` (Full) and `yinyang-empty` (Empty), both
under CC BY-NC-SA 4.0. Recipient updates use the chosen edition, preserving their
private philosophy, Personal, Situated, and independently authored additions.

[YinYang's MODEL.md](skills/yinyang/MODEL.md) owns interpretation of that Skill's
philosophical claims, formation method, reader editions, and supporting resources.
Its documents and diagrams live inside `skills/yinyang/references/`. Other
members keep their own instructions and resources. Do not import another
repository's philosophical content merely to follow its directory organization.

## Publication boundary

The owner selected a fresh public history for the noncommercial YinYang edition
on 2026-10-14. Preserve the private recovery archive and build future public
changes on the current public main. Do not merge pre-replacement branches back
into public ancestry; reapply any needed contributions onto the current tree.
Replacing history reduces ordinary access to prior versions but cannot revoke
earlier license grants or erase copies and caches outside this repository.

### Complete website source in the collection

`website/` holds the public website's complete committed material and
implementation: rendered reading pages, static assets, runtime code,
build integration, dependencies and migrations. It is generated from one exact
native Sites Git commit. Only `.playwright-cli/`, `design-evidence/`, and
`design-qa.md` are omitted as QA probes. Tracked `dist/` is public static source
and must remain; ignored client/server build output, caches, local secrets and
live applicant databases are not source material. `website/SOURCE.json` records
the source commit and exclusions. The empty `.env.example` is a template;
`.openai/hosting.json` contains nonsecret project and binding identifiers.
Independent deployment requires its own Site ID and runtime secrets.

The native Site repository owns presentation, implementation, and its
publication helper. Canonical YinYang philosophical prose and the practical guide live at
`skills/yinyang/`; copies and rendered editions inside `website/` are generated
projections, not a second authoring owner. Their displayed canonical revision
can precede the snapshot commit when content is unchanged. Maintain original
content at its owner and regenerate before publishing.

Follow the native Site README's [publication route](website/README.md#publication-and-interrupted-transfers)
when preparing publication; it owns the content/runtime selection and the
Git-first runtime route with archive fallback for this Site. Commit and push
the final Site source. Ordinary content activates its exact immutable snapshot
without a Worker build or native Sites deployment; runtime changes publish
that exact source through the native workflow. Apply its source snapshot with
`python scripts/sync-website.py --source /path/to/site --revision FULL_SHA --apply`,
then run the same command without `--apply` to check path coverage, bytes and
modes. Review and publish the collection change to GitHub separately, then
verify the selected content manifest or native Site version through its owning
route. Skip unchanged snapshots and deployments. This is an explicit publication workflow, not a new
watcher or automatic GitHub push service. Never edit generated snapshot copies.

The collection is published as a clean public GitHub repository. Anyone may
view, clone, and download it without an application, invitation, download code,
or continuing-access grant. Historical private source must stay in its private
archive; never publish excluded manuscripts or private records through history.
GitHub supplies source archives and independent forks. This collection accepts
conversation through Issues and does not accept pull requests of any kind;
the author owns revisions and publication. Song requests are for boluopai only,
not recording submissions. CONTRIBUTING.md owns the reader-facing guidance. The
website presents reading editions and package introductions; all source and
downloads go to GitHub package directories or its native repository ZIP.
Codex recipients normally install selected plugins from the boluopai GitHub
marketplace; archives remain an optional source route. Keep the installation
entrance and commands in the GitHub README and docs/codex editions. The website
is for reading and introductions, with source links to GitHub; do not repeat
installation buttons across its pages or maintain a separate website installer. The catalog at
`.agents/plugins/marketplace.json` owns plugin identity, version and presentation.
`scripts/build-plugins.py --apply` assembles complete portable packages in
`plugins/` from tracked `skills/` sources; its default mode checks byte, mode and
coverage equality. Do not edit generated plugin copies. Increment the affected
plugin version when its shipped content changes, regenerate, check native
installation and discovery, then publish the source and generated packages together.
No separate GitHub Release or tag workflow is required. Official directory
submission uses a ZIP of the same generated plugin; it is a publisher artifact,
not a website download service. Keep private personal adaptations outside plugin
caches and never include them in distribution.

YinYang's original material is licensed under CC BY-NC-SA 4.0, governed by the
official legal code at https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en.
Reproduction, adaptation, and distribution are permitted for noncommercial purposes only.
When sharing, retain required attribution and notices, provide the license
link, and identify changes. Shared adaptations follow the license's ShareAlike
conditions; private adaptations need not be published. Preserve the NonCommercial element; do not add a redistribution ban or
individual download approval.
The reusable method and tool packages other than YinYang retain their
package-local MIT licenses. Their companion relationships do not merge their
ownership or licensing. Root LICENSING.md records
the mixed scope by material, not platform. YinYang projections and original
philosophical text retain CC BY-NC-SA 4.0 on both GitHub and the website; the other
package projections and downloads retain MIT on both surfaces.
Independently authored site code, interface design, photos, and audio keep their
own stated rights; neither grant automatically covers them. Do not invent a new
site-code license. Third-party rights and earlier valid grants remain intact.

Publish only authorized reusable material. Personal accounts, private source
quotations, health or psychological records, relationship narratives, accounts,
private paths, conversation identifiers, and links exposing those materials stay
with their actual private owner. Do not retrieve private personal materials merely
to maintain this collection or create a public index that reconstructs a portrait.

Unpublished manuscripts, their reading editions, PDFs, figures, source files, and
private source records are excluded from public packages. General ideas may be
developed in the existing essays as standalone exposition with independently
public references where relevant. Publication of any original or anonymous
manuscript requires fresh explicit user authorization. Do not reintroduce
excluded source through links, assets, history, or provider previews.

Review the whole public change, including assets, metadata, published Git history,
and link destinations. Reusable packages must remain meaningful without private
sources. Keep conceptual reading links local to their owning complete package;
verify moved references, source locators, and asset paths. Preserve actual
permissions, consent, and publication authority.

Do not maintain a download application, approval service, access-code system,
publication-secret workflow, or separate package ZIP generator for this
collection. Use GitHub's public archive and native collaboration functions.
Website reading editions retain their own source and publication workflow.

Maintain each account at its existing owner rather than duplicating it in the
collection root. Do not add interpretation registries, automatic personal-data
feeds, or synchronization services for this collection.
