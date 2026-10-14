# Shared Skills and personal philosophy

[Home](../../README.md) · [Formation Skill](../../SKILL.md) · [简体中文](skill-package.zh-CN.md)

**Prometheus2Heraclitus** is the collection. Its YinYang formation Skill is
[`SKILL.md`](../../SKILL.md), supported by
[`design-and-revision.md`](../design-and-revision.md),
[`harness-adaptation.md`](../harness-adaptation.md),
and [`reading-map.md`](../reading-map.md) under that
Skill's `references/`. The nested `docs/` and `diagrams/` directories are
YinYang accessories in that same complete package. The collection root is not
itself a YinYang Skill.

Shared Skills offer capabilities and materials to adopt and rework. A personal
philosophy develops from one's own experiences, questions, sources, and practice.
YinYang is one developed example: readers may begin with it, combine other ideas,
and create work with different names, concepts, and organization.

**Philosophy is replaceable; personal accounts must be formed anew.** You may retain the
five-file structure while replacing the philosophy with your own thought or an
evidence-grounded model of a philosopher's thought. Philosophy, imagery, and
essays serve the modeling of an actual person and counterpart relationship;
if you retain this structure, all five files must describe the real user and
their collaboration. A philosopher's thought model cannot replace the user's
personal model. Maintain revised philosophy in your own version without
overwriting it with the common-file updater. Byte parity applies to copies
opting into this repository's continuing common-content updates.

The maintained YinYang implementation below illustrates one concrete approach. The
[example and commons essay](example-and-commons.md) explains the broader
invitation to adopt, combine, or independently reauthor its philosophy and
form. Technical paths below support this implementation, not a universal
literary format. A differently authored work maintains its own coherent
source and references; the common-file updater below is not for that work.

The public website provides reading and file browsing; complete Skills are
available from the public GitHub repository. Clone it or download the repository
ZIP and retain the complete directory of the package you need. Original YinYang
material uses CC BY-NC-SA 4.0, while the other independent Skills retain their package-local MIT licenses.
Use and sharing follow each material's existing license and attribution terms;
see the [collection guide](../../../../README.md).

Obtain the complete `skills/yinyang/` directory and make it available through
the consumer's actual Skill mechanism. This supplies a formation method, not
a ready-made personal relationship. The consuming model reads the entrypoint,
inspects authorized actual environment and relevant psychological or preference
material, and helps write the person's philosophy and situated relations at
their private owning location.
It then realizes the supported understanding in the actual environment, within
the task's authority, and verifies the result.

Distributed and situated editions of this maintained implementation have the same structure and byte-identical
common content. The common main `SKILL.md` carries purpose and reading routes;
the main conversational model reads it with the complete
[encounter](../encounter.md), [user model](../models.md), and
[counterpart model](../relationship.md), [situated use](../usage.md), and
[source index](../sources.md) before substantive work, in both Codex
and private Web ChatGPT. Reuse complete current text already in context. The five
fixed situated slots have the same names and roles in both packages:

**Adopting this implementation requires rewriting all five files below from
formation guidance into your own grounded accounts, and organizing the relevant
private material in `references/personal/`.** This is necessary formation work,
not optional cosmetic customization. The model writes from authorized evidence;
the user need not maintain the files personally. Unsettled relations may remain
explicitly unknown; a complete autobiography or psychological theory is not required.

| Slot | Situated content |
| --- | --- |
| `references/encounter.md` | A condensed usable account of the actual encounter. |
| `references/models.md` | The developed user model. |
| `references/relationship.md` | The counterpart model and their relationship. |
| `references/usage.md` | Use in the actual environment and allocation of work. |
| `references/sources.md` | An index of source owners and private provenance. |

In the distributed package these files contain formation instructions. In a
situated package the consuming model writes grounded actual accounts in them.
Formalized user accounts are personal information too; notation does not make
them common content. The [design reference](../design-and-revision.md) explains
formation and revision. Do not copy the author's portrait or invent a substitute.
An existing personal philosophy retains its grounded content when using this
same format; it is not replaced with generic instructions.

[Private supporting materials](../personal/README.md) belong under
`references/personal/`. These pages record provenance and private material omitted from the common
essays. The philosophy remains one authored body even when written by this
person; do not reproduce it as a second personal application. A topic companion
links to its common text and records its actual sources and privacy boundary.
Create one when it carries useful evidence, not an empty copy for every essay.
Their filenames follow the evidence; this does not create a different schema. Private content is
not committed back into the shared collection.

At completion, check that all five files coherently describe the actual person,
counterpart, relationship, and environment; that necessary private materials and
provenance are reachable; and that the conversational model can read and use
them at the actual entrypoint. Merely downloading, retaining generic guidance,
or copying someone else's portrait does not complete a situated version.
After initial formation, revise what actual collaboration changes; each update
need not rewrite every file.

All other material is common: documents, diagrams, `design-and-revision.md`,
`harness-adaptation.md`, `reading-map.md`, package administration, READMEs, and
the OpenAI YAML adapter. The shared GitHub package is the canonical common
owner. `scripts/sync-common.py` checks projection by default; `--apply` projects
common source into the target while preserving all five slots and everything
under `references/personal/`. Native owners realize the projected source in
local and private Web consumers. It never exports personal content and is not
a service or automatic personal upload. Later common edits therefore remain
shared rather than forking into separate local and distributed instructions.

Run the source comparison with explicit package directories:

```bash
python3 /path/to/shared/yinyang/scripts/sync-common.py \
  --source /path/to/shared/yinyang --target /path/to/situated/yinyang
```

Add `--apply` to copy changed common files, then run the comparison again.
Start a new situated package from a complete shared copy before filling its
personal files. Unmatched target files and common-path symlinks stop the command
before copying; inspect their ownership instead of silently deleting them.
The command updates source packages only; use the host's existing owner for
runtime installation and cloud publication.

The essays in `references/docs/` explain the ideas that inform formation. Their relation
is described on the homepage; they are not additional Skills or a linear
installation sequence. No fictional mini package or calculator stands in for
the personal formation and actual environment work.
