# Shared Skills and personal philosophy

[Home](../../README.md) · [Model entrypoint](../../SKILL.md) · [简体中文](skill-package.zh-CN.md)

This guide owns the file and update contract for the maintained YinYang package.
The collection is **Prometheus2Heraclitus**; this complete member lives under
`skills/yinyang/`. Its `references/docs/` and `references/diagrams/` are
supporting resources, not independent Skills. Obtain the complete directory
from the public repository and expose it through the consumer's actual Skill
mechanism. The website is a reading surface; repository cloning and GitHub's
native ZIP preserve complete source.

YinYang is one developed philosophy and formation method. Readers can adopt
it, combine selected resources, or create a different work. The
[example and commons essay](example-and-commons.md) develops that invitation.
A philosopher's thought may inform a framework; it cannot replace the account
of the actual user.

## Common and situated content

Distributed and situated copies following this implementation share the same
structure and byte-identical common content. The five fixed paths have the
same responsibilities in both. Distributed files contain formation guidance;
situated files contain grounded accounts of the actual person and collaboration.

| Fixed situated slot | Responsibility |
| --- | --- |
| `references/encounter.md` | Condensed usable encounter and purpose. |
| `references/models.md` | Developed user model, with scope and uncertainty. |
| `references/relationship.md` | Counterpart model, relationship, cooperation, and correction. |
| `references/usage.md` | Actual environment use and allocation of work. |
| `references/sources.md` | Source-owner index and private provenance routes. |

Adoption requires forming all five accounts from relevant authorized material
and organizing their necessary private support. The model carries this writing;
the user need not maintain files personally. Explicit unknowns can be honest
situated content. Unchanged templates, a copied portrait, or an invented person
do not constitute a formed version. Check coherence, grounding, reachable
evidence, and the conversational model's ability to read and use the accounts
at its actual entrypoint. Later revisions need change only affected content.

`references/personal/` retains useful private supporting material and topical
provenance. Filenames follow actual evidence; there is no universal list or
required empty companion for every essay. Originals and extended history can
remain with existing owners, reached through access-bounded references. Keep one
authored philosophy: a private companion links to its common argument and
retains the private evidence, rather than reproducing a second theory.

Everything outside those five slots and `references/personal/` is common:
the entrypoint, reader editions, methods, essays, diagrams, reading map,
administration, scripts, and OpenAI YAML adapter. The shared GitHub package owns
this content. The [entrypoint](../../SKILL.md) owns initial reading; [design and
revision](../design-and-revision.md) owns formation; [harness adaptation](../harness-adaptation.md)
owns environmental realization.

## Project common changes

`scripts/sync-common.py` checks common source projection by default. With
`--apply`, it projects common files into the target, preserving all five
situated slots and everything under `references/personal/`. It does not infer
a person, export private files, or publish to a runtime.

Start a new situated version from a complete shared copy, then form its private
accounts. Compare explicit package directories:

```bash
python3 /path/to/shared/yinyang/scripts/sync-common.py \
  --source /path/to/shared/yinyang --target /path/to/situated/yinyang
```

Add `--apply` to copy changes, then run the comparison again. Unmatched target
files and common-path symlinks stop copying; inspect ownership rather than
silently deleting them. Existing local or private Web owners install and
publish the projected source, followed by actual-consumer readback.

Byte parity applies to copies choosing continuing common updates. If you
replace the philosophy or organization independently, keep that work at its
own source and maintain its coherent references. Do not project this common
package over it, even if it retains the five-slot format.

## Personal and public boundaries

Personal accounts remain private even when formalized or written for models.
Private quotations, biography, psychological and health records, relationship
narratives, account information, private paths and conversation identifiers,
and unpublished manuscripts stay with their actual owners. General abstraction
does not authorize public links that reconstruct private sources.

Return only authorized reusable insights to the collection. YinYang original
material uses CC BY-NC-SA 4.0; other independent members retain their own MIT
licenses. Follow the [collection guide](../../../../README.md) and the actual
publication owner for permissions, attribution, and source review. A private
adaptation need not be published.
