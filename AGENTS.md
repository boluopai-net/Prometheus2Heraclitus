# Prometheus2Heraclitus collection maintenance

Read [MODEL.md](MODEL.md) before maintaining this repository. It owns collection
scope, independent member ownership, language, source limits, and publication
boundaries. The root README editions introduce the actual collection members.
Keep English and Chinese reader editions semantically aligned.

Each Skill under `skills/` owns its complete package and supporting resources.
For YinYang, read [its MODEL.md](skills/yinyang/MODEL.md) and
[its AGENTS.md](skills/yinyang/AGENTS.md) before editing its philosophical account
or formation method. YinYang's `references/docs/` and `references/diagrams/` are
package accessories, not root collections or independent Skills. Other actual
Skills retain their specialist purpose and methods.

Keep changes within the affected owner. Verify local links and public source
locators after relocation; preserve licenses, separate rights, third-party
notices, executable modes, and assets. Do not invent demonstration members,
copy a private portrait, or retrieve personal material just to maintain this
public repository. Model-facing maintenance prose remains English.

`website/` is a complete generated snapshot of an exact committed native Site
revision, with the QA-only exclusions recorded in `website/SOURCE.json`.
Do not edit its copies directly. Read MODEL.md's website publication workflow;
use `scripts/sync-website.py` to apply and check committed source coverage,
bytes and modes. Preserve tracked `dist/` static sources and all rights notices.
The website presents materials and package introductions; all source downloads
use GitHub directories or its native repository ZIP. Do not add separate
website package ZIP generation or Release/tag maintenance.
