# Recipient configuration and record ownership

The public Teacher pair supplies reusable methods. It does not contain the
recipient's corpus, learner model, research direction, paths, State or work plan.
Resolve these objects from the recipient's existing project instructions and
accessible records. Record bindings in the existing corpus/project resolver,
not by filling this installed package with private data. No extra configuration
service, shared memory namespace or coordination layer is needed.

## Bind only the objects the task needs

| Binding | Semantic owner and expected content |
| --- | --- |
| `course_root` | Recipient's course/source collection; its `AGENTS.md` maps layout, actual sources and course-local resolvers. A named course can use another existing layout. |
| `global_learning_path` | Maintained target selection and course-mapping hypotheses; resolved by [learning-path.md](learning-path.md). |
| `local_learning_path` | Current attention/execution selection and useful return conditions; resolved by [local-learning-path.md](local-learning-path.md). |
| `work_plan` | Recipient's single maintained work/priorities record; [work-plan.md](work-plan.md) owns only its reference slot. It is not another learning-progress store. |
| `global_state` | Compact cross-course recovery with links to course records; an existing `GLOBAL_STATE.md` is a conventional name, not a supplied learner history. |
| `course_state` | Current course's source scope, observed exposure/contributions, unresolved questions and next entry; default `<course>/_master/COURSE_STATE.md`, or the collection's existing owner. |
| `research_context` | Actual research question/manuscript owner when a substantive research connection is requested. Missing context limits that connection; it does not make a source unusable. |
| `teaching_language` | Recipient's selected language and bilingual terminology convention; preserve original text/notation and use the recipient language first in bilingual labels. Chinese examples in the materials branch illustrate the source profile. |
| `reading_surface` | Actual Markdown/source reader and supported links, math and diagrams. Obsidian is the source method's documented profile. |

For an established collection, inspect the current instructions and records
before making a new binding or file. Resolve collisions by actual path/edition
and source role. Keep private values with that owner; do not publish them in
this package, a download example or a public dependency table. The source's
three personal path documents have intentionally been replaced by slots without
reading or publishing their bodies.

For a new course mapping, use [course workspace](course-workspace.md) to inspect
sources and compile only necessary facts. Do not initialize a curriculum,
Global State or per-book progress merely to answer an isolated known-source
question. A missing binding is an explicit scope/access limit, not evidence
that the learner has no prior exposure or must reconstruct every prior session.

## Required capabilities and optional reading support

Textual teaching needs access to the selected source and current conversation.
Fresh external investigation needs an actually available search/retrieval route;
[research](../../research/SKILL.md) supplies the method, not a provider account.
Saved material/State maintenance additionally needs authorized record access,
read-before-write and saved-result readback. A host without file writes can
complete an explanation or supply an exact unsaved proposal; it cannot claim
persisted materials or progress. Local execution needs the project's actual
tools and authority. Neither Teacher commands another conversation to obtain it.

The materials branch documents Obsidian Markdown, one-based PDF pages, concept
passage links, math and diagrams. Use built-in ordinary links/math and verify
the actual reader. [PDF++](https://github.com/RyotaUshio/obsidian-pdf-plus) is an
optional external dependency for selection/rectangle highlighting and backlinks;
its coordinates must come from the exact source text layer or verified UI. Without
it, retain exact page/section and searchable passage locators and state that
highlight/backlink verification remains unavailable. Do not invent coordinates.
Academic callout styling and Linter are optional; neither certifies correctness.
If another reader is selected, preserve source identity, concept-to-passage
navigation, math meaning and return routes using its real supported interface.
Report unavailable rendering/navigation checks instead of claiming success.

## Verify a usable entry

For the selected activity, resolve its source/edition, the relevant glossary and
guide (plus applicable technical training), and any records needed for recovery
or path judgment. Read actual source passages and inspect the named artifacts.
Keep preparation, source exposure, teacher demonstration, learner contribution
and untested understanding distinct. After a permitted write, reread the owner
record and follow the changed reading path; preserve unrelated entries. An
unresolved path slot never turns an imagined learner/corpus into fact.
