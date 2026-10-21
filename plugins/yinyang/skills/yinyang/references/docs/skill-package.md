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
of the actual user. This guide's five-account and common-update contract applies
to full adoption of the maintained Skill. Reading its philosophy or borrowing
a selected method does not by itself adopt that contract or require a personal
philosophy project.

## Common and situated content

Distributed and situated copies share byte-identical common content. Permanent
writing guides live under `references/formation/`, with complete Chinese editions.
A private situated version adds the following fixed five accounts; public
distribution contains neither these files nor placeholder accounts.

| Fixed situated slot | Responsibility |
| --- | --- |
| `references/situated/orientation.md` | Adopted philosophy, values, and direction. |
| `references/situated/person.md` | Grounded understanding of the actual person. |
| `references/situated/counterpart.md` | Actual model and wanted contribution. |
| `references/situated/relationship.md` | Joint activity, correction, and division of work. |
| `references/situated/environment.md` | Realization through the actual environment. |

Person, counterpart, and relationship remain three modeling objects. Orientation
supplies adopted interpretive and evaluative direction; environment explains
realization. The five are not all psychological models. The
[formation method](../design-and-revision.md) routes each account to its
permanent guide, which remains available after adoption.

Adoption requires forming all five accounts from relevant authorized material
and organizing their necessary private support. The model carries this writing;
the user need not maintain files personally. Explicit unknowns can be honest
situated content. Unchanged templates, a copied portrait, or an invented person
do not constitute a formed version. Check coherence, grounding, reachable
evidence, and the conversational model's ability to read and use the accounts
at its actual entrypoint. Later revisions need change only affected content.

`references/personal/sources.md` is the actual private evidence entrance,
supporting all five accounts rather than becoming another core account.
The public [evidence guide](../formation/sources.md) supplies its method.
Further `references/personal/` material retains useful private support and topical
provenance. Filenames follow actual evidence; there is no universal list or
required empty companion for every essay. Originals and extended history can
remain with existing owners, reached through access-bounded references. Keep one
authored philosophy: a private companion links to its common argument and
retains the private evidence, rather than reproducing a second theory.

Everything outside the entire `references/situated/` and `references/personal/`
trees is common:
the entrypoint, reader editions, methods, essays, diagrams, reading map,
administration, scripts, and OpenAI YAML adapter. The shared GitHub package owns
this content. The [entrypoint](../../SKILL.md) owns initial reading; [design and
revision](../design-and-revision.md) owns formation; [harness adaptation](../harness-adaptation.md)
owns environmental realization.

## Project common changes

`scripts/sync-common.py` checks common source projection by default. With
`--apply`, it projects common files into the target, preserving everything under
both private trees, including additional files and links. It does not traverse
or inspect their contents. It does not infer
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

Earlier packages mixed public guidance and private content at
`references/{encounter,models,relationship,usage,sources}.md`. The projector
refuses either package with any of these paths before changing files. Their
owner first redistributes actual meaning into the five new accounts and private
evidence index, preserves unique support, and retires the old paths. The old
encounter can contain orientation and relationship, and the old relationship
both counterpart and joint activity: a mechanical rename cannot complete this
semantic migration. Retain any useful private `references/personal/README.md`
substance at the appropriate private owner; the whole personal tree is protected.

Common parity preserves one recipient-local discovery exception: when the
target's single-line `SKILL.md` description already begins with `用户自制：`,
the projector retains that prefix while replacing its substantive wording from
the common source. An unmarked target stays unmarked. Every other common byte
and file mode remains source-owned; the public package does not assign itself
recipient-relative authorship.

This parity applies to copies choosing continuing common updates. If you
replace the philosophy or organization independently, keep that work at its
own source and maintain its coherent references. Do not project this common
package over it, even if it retains the five-slot format.

Authors of other works can change the number and organization of accounts and
the philosophy. The maintained YinYang implementation keeps this fixed five.

## Personal and public boundaries

Personal accounts remain private even when formalized or written for models.
Private quotations, biography, psychological and health records, relationship
narratives, account information, private paths and conversation identifiers,
and unpublished manuscripts stay with their actual owners. General abstraction
does not authorize public links that reconstruct private sources.

Return only authorized reusable insights to the collection. YinYang original
material uses CC BY-NC-SA 4.0; other independent members retain their own MIT
licenses. Follow the [collection guide](https://github.com/boluopai-net/Prometheus2Heraclitus/blob/main/README.md) and the actual
publication owner for permissions, attribution, and source review. A private
adaptation need not be published.
