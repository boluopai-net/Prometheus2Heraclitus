# Contributing

[简体中文](CONTRIBUTING.zh-CN.md) · [Collection](README.md)

Corrections, alternative interpretations, additional philosophy, stronger
arguments and rigor, useful technology, and working improvements are welcome.
Agreement with YinYang's philosophy is not a condition of
participation. Explain the relation you want to examine or change so others
can assess and continue the work.

## Create independently, develop your version, or contribute here

You may take inspiration from the form of making philosophy usable and create
entirely different content, organization, and tools in your own repository.
You need not retain YinYang, join this collection, fork this repository, or
open an Issue first. An independent work may express a different or opposing
philosophy; its existence does not depend on this maintainer's agreement.

You may also copy or fork existing material under its applicable license and
add philosophy, arguments, examples, criticism, rigor, or technical realization
in your own version. Whether to submit a PR or keep the versions synchronized
is your choice. The Issue/PR workflow below applies only to questions and
changes you want to bring into **this repository**.

References to relevant material and acknowledgments of inspiration are welcome,
as is returning with a new work for conversation and mutual introductions through
links. Independent works determine licensing from their own sources and rights;
reuse of this repository's material follows that material's attribution and
license requirements. Permission to create or modify, source attribution, and
whether this repository accepts a merge are different questions. [LICENSING.md](LICENSING.md)
describes the licensing scope.

## Contributing here: Issue or pull request?

For a reusable Skill, improving the actual method and sending a PR directly is
welcome: a change that works better in your environment can benefit the original
author and other users too. Explain the use that led to it and the observed
improvement. For philosophy, the main invitation is to write your own work from
your own questions and experience; this example need not become its template.
Corrections, objections, and proposed improvements to this philosophical account
are also welcome through Issues and PRs. These invitations distinguish purposes,
not who is allowed to contribute or which ideas may be questioned.

Contributions can concern **philosophy, psychological or preference-modeling
methods, tools, and singing**. Model-making methods and sanitized examples are
welcome; another person's private portrait is not public contribution material.
The [singing station](https://boluopai.net/singing/en/) welcomes song requests
and proposed recordings through its comments or a GitHub Issue. Include the
song title, performer credit, an accessible recording link, and the permission
that allows publication. Contributors may also propose a PR with a recording
catalog entry; the native website owner integrates accepted entries into
`content/singing/recordings.json` and publishes the player. Each entry supplies
`title`, `performer`, `audio_url`, `source_url`, and `rights`. This is an invitation
to contribute, not an automatic upload or blanket license for recordings.

| What you have | Where to start | What to include |
| --- | --- | --- |
| A question, unclear passage, objection, or missing reference | Open an Issue | Link the page or file, identify the passage, and explain the question or competing interpretation. Include sources when a factual claim depends on them. |
| A broken page, tool, link, or installation | Open an Issue | Describe what you tried, what you expected, and what happened. Add the relevant environment and a minimal example or screenshot when useful. |
| A correction, philosophical addition, stronger argument or rigor, technical contribution, or another concrete change | Open a PR directly | Explain the problem, the resulting change, and how you checked it. A prior Issue is optional. |
| A change to this repository's overall direction, a new collection member, or a broad reorganization proposed for merging | Open an Issue for discussion first | State the purpose, proposed scope, alternatives, and the effect on existing readers or users before investing in a large implementation. This does not restrict your independent version. |

Use Chinese or English for discussion. A short, concrete description is enough;
you do not need a finished theory or implementation specification to ask a question.
Related discussion can continue in one Issue instead of opening a new one for
every reply.

## Preparing a change for this repository

Fork the repository, make a branch for the change, and open a pull request
against `main`. Keep one coherent purpose in a PR. Link an existing Issue when
there is one, but do not create an Issue solely to satisfy a template.

Read the affected package's instructions. [AGENTS.md](AGENTS.md) and
[MODEL.md](MODEL.md) explain source ownership; each Skill may add its own
maintenance guidance. Edit original material at its owner and preserve the
meaning of both English and Chinese reader editions. If you can update only one
language, state the translation gap clearly so it can be resolved during review.

The `website/` directory is a generated snapshot of the native Site source.
For website changes, an Issue can identify the desired result, or a PR can
provide a proposed patch to the snapshot. Mark it as a website proposal: the
maintainer will apply the accepted change at the native source, regenerate the
snapshot, and publish it. Direct edits to generated copies do not become a second
maintenance source. Canonical YinYang writing belongs in `skills/yinyang/`.

## What reviewers need

- The concrete problem or purpose and the behavior or meaning after the change.
- Relevant sources for factual corrections, with interpretation distinguished
  from quotation or established results.
- Appropriate checks: readable links and language parity for text; a useful
  real example for a Skill or script; screenshots for layout changes; relevant
  build or behavior checks for implementation changes.
- Any remaining uncertainty, translation gap, or check you could not perform.

Scale checking to the change. A wording correction does not need a new test
suite. AI assistance is welcome; the submitter remains responsible for reading
the proposed changes, checking their claims, and excluding private material.

## Public material and rights

Issues and PRs are public. Remove credentials, private conversations, personal
portraits, and material you are not authorized to publish. Use a minimal,
sanitized example when reporting a problem. Do not paste a secret into an Issue.

Contributions follow the existing license of the affected material; this does
not relicense unrelated work. YinYang's original material uses CC BY-NC-SA 4.0,
and the other reusable Skill packages use their included MIT licenses. Retain attribution and third-party
notices and identify outside sources. [LICENSING.md](LICENSING.md) records the scope.

Review may request a clarification, revision, or narrower scope. The maintainer
handles merging and publication; opening an Issue or PR does not guarantee
adoption. Discuss arguments and observable effects, leaving room for independent
works and other ways of using the shared material.
