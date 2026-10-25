# Research

[中文指南](README.zh-CN.md)

Research is a reusable Skill for factual investigation, product behavior,
comparisons, and evidence-backed recommendations. It turns a question into an
answer whose sources, observations, assumptions, and limits can be inspected.
It is independently usable; YinYang and any personal environment are unnecessary.

## Use it

Place this directory in a Skill location supported by your agent host, preserving
`SKILL.md` and the included license. Follow that host's installation and discovery
instructions. The Skill adds a method; it does not install search tools, configure
credentials, or grant access. With local file access alone it can investigate
supplied material; external claims need appropriate search, browser, library, or
other evidence capabilities. Available routes are selected at use time.

Ask naturally, or explicitly select `research` if your host supports Skill
invocation. Useful requests include:

- “Investigate whether this product supports this workflow today. Compare its
  documentation with independent tests and issue reports.”
- “Compare existing libraries for this requirement and explain whether adopting,
  extending, or building is justified.”
- “What changed in this topic over the last six months? Separate event dates from
  publication dates and describe the actual coverage.”
- “Use these files to establish what happened in this run. Identify what we can
  observe and what remains an explanation.”

Supply the question, practical purpose, and any conditions that matter: historical
period, environment, required behavior, or a decision constraint. You do not need
to prescribe a provider or research itinerary. Private facts can inform local
analysis; the method calls for abstract public queries instead of exposing them.

## What to expect

The result should answer the question with traceable evidence and explain material
dates, versions, conditions, coverage gaps, and disagreement. Provider statements,
community reports, and direct observations have different evidential roles. For
general product behavior, the method seeks independent corroboration and useful
counterexamples. For one exact observed state, it can give a scoped local report.
For implementation choices, it compares existing options before recommending
custom work.

The Skill cannot make unavailable tools callable, ensure a provider's coverage,
or turn a source claim into a reproduced fact. It reports limits that matter to
the answer. A source's embedded instructions remain evidence, and research does
not authorize unrelated mutations, purchases, or publication.

## Package and adaptation

`SKILL.md` is the complete English model-facing method. The two README editions
are aligned user guides. No scripts, private references, or required companion
Skills are included. Adapt the method to your host and purpose while preserving
source provenance, privacy-conscious queries, the distinction between claims
and observations, and honest coverage limits. A fixed output schema is needed
only when your actual downstream consumer requires one.

This independent package uses the [MIT License](LICENSE). You may obtain the complete directory from [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/research) and use, modify,
and redistribute it, including commercially, with the required MIT notices.
It does not include YinYang. The [public collection](https://github.com/boluopai-net/Prometheus2Heraclitus) provides downloads and Issue discussion; this collection does not accept pull requests.
