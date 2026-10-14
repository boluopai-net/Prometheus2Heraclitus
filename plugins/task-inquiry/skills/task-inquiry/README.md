# Task Inquiry

**Clarify consequential uncertainty through evidence, reasoning, and useful questions.**

[简体中文](README.zh-CN.md)

Task Inquiry helps an assistant resolve uncertainty that can change what a task
should do next. It begins with a real mismatch or tension, develops plausible
explanations, and uses evidence or a focused user question to distinguish them.
The assistant carries the investigation and execution forward instead of
requiring the user to formalize the whole problem.

## Use this Skill

Make the complete `task-inquiry/` directory available through the Skill
mechanism supported by your assistant, then invoke **Task Inquiry** when a
material ambiguity, conflicting explanation, or unresolved choice affects the
task. The package contains the standalone instructions in [`SKILL.md`](SKILL.md).
It has no required companion framework, private context, scripts, or provider
integration.

This method is useful when inquiry can improve the result. A clear, settled task
should proceed directly. A question is useful only when its answer can change
the interpretation, evidence, or action.

## Examples

**Investigate an unexpected result.** A report's totals differ from the
dashboard. The assistant checks date ranges, filters, and definitions, identifies
which differences could explain the mismatch, then asks about the intended
reporting period only if the available evidence cannot determine it.

**Resolve a meaningful preference.** Two proposed plans meet the stated goal,
but one saves time while the other preserves flexibility. The assistant
explains that tradeoff and asks which outcome matters more before taking the
dependent step; it continues any independent research meanwhile.

## Method at a glance

The assistant identifies the actual tension, distinguishes facts from
assumptions and unknowns, and proposes explanations worth checking. It derives
what would differ under each explanation, gathers available evidence, and
updates its judgment. In ordinary work, it asks the user for information or a
decision the evidence cannot supply when that answer would change the work.
Teaching may also use questions to reveal or develop understanding, as described
below. The host's own interaction and authorization boundaries remain in force.

## Work and learning

In ordinary work, useful feedback can help the user notice a relationship:
show what the explanation predicted and what the evidence showed. The assistant
still carries the reasoning and execution, without adding lessons or exercises.
In teaching, questions and practice may be chosen to reveal or develop the
learner's understanding even when the answer is known. The teaching role chooses
the method and owns progression; inquiry does not impose a teaching format on
ordinary tasks.

## License

This independent package uses the [MIT License](LICENSE). You may obtain the complete directory from [GitHub](https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/task-inquiry) and use, modify,
and redistribute it, including commercially, with the required MIT notices.
It does not include YinYang. The [public collection](https://github.com/boluopai-net/Prometheus2Heraclitus) supports downloads and Issues/PR collaboration.
