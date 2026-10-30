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
of the actual user. This guide's six-question, dual-route and common-update contract applies
to full adoption of the maintained Skill. Reading its philosophy or borrowing
a selected method does not by itself adopt that contract or require a personal
philosophy project. Full adoption also leaves original essay-writing optional:
its question-defined models state the positions and arrangements adopted for use,
which can draw on selected existing ideas.

## Common and situated content

The six bilingual formation guides define the full questions and reading roles
of orientation, person, counterpart, relationship, environment and revision.
Each synthesis instruction draws on the six complete guides and relevant actual
grounds. [Formation and revision](../design-and-revision.md) owns their distinct
subjects, connected scope and whole-six coherence.

The [2×2 practice selector](creation-method.md#choose-2x2) explains edition and condensation choices;
this page locates the private files and their updates:

| Question | Actual private file |
| --- | --- |
| Orientation | `references/situated/orientation.md` |
| Person | `references/situated/person.md` |
| Counterpart | `references/situated/counterpart.md` |
| Relationship | `references/situated/relationship.md` |
| Environment | `references/situated/environment.md` |
| Actual situated revision method | `references/situated/revision.md` |

Read all six complete actual accounts in ordinary collaboration. Persist intended
private source in Git and a private GitHub repository through the actual account
and publication owner, checking private visibility, committed content and reader
retrieval. Original records retain their owners; secrets stay outside ordinary
repository files. Public Full ships no private accounts or placeholders.

The complex route projects checked bodies to the same six paths, or binds the six questions,
native IDs, and complete bodies through private `references/situated/index.md`.
See [Hindsight configuration](../hindsight.md).
[Formation and revision](../design-and-revision.md) owns their content and whole-account checking.

Philosophy retains its authored source. Personal remains human-readable topic
articles in the existing four subject groups, with usable navigation and original
source links. Direct source/article editing remains available. In the native
route, substantive Knowledge Pages can maintain those articles and project
Markdown into existing private reading paths, with Observations backstage.
Migrate affected derived articles as revision needs, preserving readability and
unique grounds. Corrected Personal understanding must inform later synthesis;
all products can return to originals without requiring chained generated summaries.
The [Personal guide](../formation/personal-material.md#keep-personal-readable-for-the-person)
owns that reading arrangement.

Keep meaningful Personal material names in the person's native language; body
language follows its consumer. Preserve instrument identifiers where useful.
Both `references/personal/` and `references/situated/`, including optional native
bindings and private generated bodies, stay private. Common projection protects
both trees; it does not change bank state, GitHub visibility or runtime consumers.
Independently authored philosophy retains its own source.

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
the working models. The [Psychology guide](psychological-support.md) owns
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
owner first migrates actual meaning into the six actual accounts and private
evidence index, or an explicit all-six native binding, preserves unique support, and retires the old paths. The old
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

The maintained implementation preserves the six full questions and their
coherent relations through either route. Native paths may differ under an explicit
all-six binding; independently authored works can choose another design.

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
