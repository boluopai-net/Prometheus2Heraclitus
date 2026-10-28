# YinYang files and shared updates

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
of the actual user. This guide's six-file and common-update contract applies
to full adoption of the maintained Skill. Reading its philosophy or borrowing
a selected method does not by itself adopt that contract or require a personal
philosophy project. Full adoption also leaves original essay-writing optional:
its six actual files state the positions and arrangements adopted for use,
which can draw on selected existing ideas.

## Common and situated content

This implementation distinguishes six public writing guides from six private
actual files, corresponding by object:

| Object | Public guide | Private actual file |
| --- | --- | --- |
| Orientation | `references/formation/orientation.md` | `references/situated/orientation.md` |
| Person | `references/formation/person.md` | `references/situated/person.md` |
| Counterpart | `references/formation/counterpart.md` | `references/situated/counterpart.md` |
| Relationship | `references/formation/relationship.md` | `references/situated/relationship.md` |
| Environment | `references/formation/environment.md` | `references/situated/environment.md` |
| Revision | `references/formation/revision.md` | `references/situated/revision.md` |

The public guides have complete Chinese editions and explain how to form the
corresponding content. The actual files articulate one's own orientation,
the working implications of personal understanding, actual counterpart,
relationship, environment, and revision method. Together they are personal
working models of person–model cooperation, intended to make the actual personal
environment fit the person psychologically and practically. Revision guidance and an actual revision method are distinct
too: the former offers adaptable writing guidance; the latter explains how
revision works with this person's philosophy, material, and actual environment.
Public distribution contains guides, with no actual files or placeholder portraits.
The initial reading uses all six actual files; a common guide cannot substitute
for one of them.

For full adoption, the model forms these six files from relevant authorized
material and organizes their needed private support. Explicit unknowns can be
honest content; copying guidance or someone else's portrait cannot form an actual
version. Person, counterpart, and relationship remain three subjects of understanding;
the other files supply direction, realization, and revision. Later changes follow
affected meanings and dependencies.

`references/personal/` holds preference and selection material, psychological
experience and assessments, personal conditions, and selected self-expression
and works. Its maintained `README.md` classifies the material;
`sources.md` locates provenance. [Organizing Personal material](../formation/personal-material.md)
owns classification, material gaps, and how these grounds inform the six accounts. Extended history, originals, and topical material stay
with existing owners or under that tree, reached through access-bounded locators.
The same guide explains how [personal memory](../formation/personal-material.md#bring-personal-memory-into-the-same-account)
can be maintained within Personal or referenced there from an existing private owner.
The six working files condense adopted philosophy and updated personal material
into the implications needed for cooperation. They are not six psychological
models or the primary self-analysis archive; `person.md` does not hold the whole
psychological portrait. The [maintenance method](../design-and-revision.md#maintain-the-private-material-through-use)
owns each refresh; the [revision writing guide](../formation/revision.md#sources-and-evidence)
supplies evidence guidance. Independently authored philosophy has its own source;
private material links it and retains relevant grounds.

Personal material names use one consistent language: the user's native language.
Apply it to each material's primary title and its name in inventories and reader
navigation, including newly added records. The body may use another language
according to its semantic consumer; an English body does not make the material's
name English. Derive reading-surface names from the maintained primary title
so separate display translations cannot drift. Preserve standard instrument
identifiers where needed within a native-language title.

Both entire trees, `references/situated/` and `references/personal/`, are private.
Everything else is common package content, including the entrypoint, six writing
guides, essays, diagrams, and scripts. Distributed copies and private copies
choosing continued common updates keep common content byte-identical.
[Everyday collaboration with YinYang](../../SKILL.md) owns the actual initial reading;
[Forming and revising working models](../design-and-revision.md) connects the writing objects.

## Questionnaire and assessment material

When a situated version has questionnaire or assessment records, organize this
distinct part of personal evidence under `references/personal/questionnaires/`.
Use its `README.md` as a readable inventory linking dated records and their
original sources. Connect it from `personal/README.md` and `personal/sources.md`.
Group records by occasion or instrument according to what makes them easy to
retrieve; repeated completions remain separate dated observations.

Keep each record's instrument name, language and version when known, completion
date and context, result and score direction, and access to original answers or
the report. Distinguish a questionnaire response, a performance test, a report's
written conclusion, and a later interpretation. Preserve conflicting findings
and missing information explicitly; a report without item answers must not be
expanded into invented responses. Existing private measurement systems and
medical-document collections can retain their originals, with useful results
and working links maintained here instead of duplicate archives. Undated
material remains undated until its source establishes a date.

This organization makes measurements available alongside narrative material
without turning them into a complete personal account or automatically revising
the six working files. The [Psychology guide](psychological-support.md) owns
selection, scoring and interpretation. The directory and all filled records
remain private; the distributed package supplies this organizing method, not
another person's records or placeholder results.

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
owner first redistributes actual meaning into the six actual files and private
evidence index, preserves unique support, and retires the old paths. The old
encounter can contain orientation and relationship, and the old relationship
both counterpart and joint activity: a mechanical rename cannot complete this
semantic migration. Retain any useful private `references/personal/README.md`
substance at the appropriate private owner; the whole personal tree is protected.

Common parity preserves one recipient-local discovery exception: when the
target's single-line `SKILL.md` description already begins with `<用户自制>` and a space,
the projector retains that prefix while replacing its substantive wording from
the common source. An unmarked target stays unmarked. Every other common byte
and file mode remains source-owned; the public package does not assign itself
recipient-relative authorship.

This parity applies to copies choosing continuing common updates. If you
replace the philosophy or organization independently, keep that work at its
own source and maintain its coherent references. Do not project this common
package over it, even if it retains the six-slot format.

Authors of other works can change the number and organization of accounts and
the philosophy. The maintained YinYang implementation keeps these fixed six actual files.

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
