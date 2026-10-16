# World, process, and expression

[完整中文版](world-and-expression.zh-CN.md)

*A frame catches a crossing of the current. It leaves the water outside its edges, yet someone who sees the frame notices a path they had not seen before. The image returns to the river as a new way of looking.*

How can an understanding of a changing world become a computer model that helps
us act within it—and change through the result? A person can recognize an
unspoken relation or a mismatch in a work; a language model can develop that
recognition into an explanation or prototype whose consequences both inspect.
Either can propose the next question or correct the reconstruction. Making
the relation available to a computer adds another question: what is represented,
what changes it, and how does a result bear on the activity being understood?

**YinYang** names a contemporary framework in which a person and a generative
model contribute to each other's continuing activity. Their accounts of the
person, the counterpart, and their relationship guide an environment of Skills,
prompts, tools, interfaces, and working conditions. This essay follows the
connection from that activity's physical ground to its selected computational
model, from the model to an actual arrangement, and from observable consequences
back to understanding. A model, its computer representation, and the process
they concern have different roles within this one world.

The subject of this movement is their **coupled activity**. The person and model
can divide contributions throughout finding the question, selecting processes,
constructing and examining the computational model, implementing an arrangement,
and interpreting feedback. Embodied intuition and perception of a whole can meet
explicit exposition, formal reasoning, computation, and tool use. The allocation
depends on current capabilities, modalities, and purpose; both can generate and
judge. The person need not construct the ontology alone before the model joins,
and the resulting capacity can remain distributed across the relationship.

## Physical ground and computational abstraction

YinYang takes the changing natural world itself as its reality: moving matter,
embodied life, psychological activity, and social relations belong to one world.
Modest naturalism names this worldly scope. Its contemporary **fire monism is
a process ontology**: fire names becoming and transformation, within which
persons, objects, and relations form, persist, and change as relatively stable
patterns. Philosophy, psychological activity, and engineering are physically
realized within this same reality. It does not identify everything's material
with literal flame.
This is the framework's chosen contemporary account, developed from Heraclitean
images rather than established merely by their historical authority. The
[fire essay](stealing-fire.md#from-living-fire-to-interacting-event-streams)
develops that choice and its sources.

An object can therefore remain intelligible through change. A work continues
through revisions; a person continues through encounters without keeping every
state or self-description unchanged. A model must articulate the continuity
relevant to its question: what forms an object, what lets us treat it as the
same object, and which events change its state or end that continuity. A static
view can legitimately hold selected relations fixed for an inquiry. Its boundary
belongs within the larger process in which the view is made, used, and revised.

**Engineering ontology here is computational ontology:** an articulation of a
selected part of this reality through events, states, persisting objects, relations,
constraints, and transition rules through which a computer can represent that
part and, where the question calls for it, simulate relevant changes. The
participants select question-relevant boundaries, scales, and continuities
together; the computational model states what those choices mean. This defines
engineering ontology in this
framework, rather than reducing all engineering to computing. It carries the
process premise into the model's account of persistence and change instead of
replacing it with an unrelated inventory of things.

Selection alone does not provide a usable computational body. The representation
must connect its distinctions to what a computer consumer can retain, interpret,
compare, or transform, and connect its results to relevant observations. A state
needs a meaning; a transition needs conditions and consequences; a claimed
correspondence needs a way to be assessed. Merely storing the words “person,”
“event,” or “relation” supplies none of these connections. Data structures,
programs, model-interpreted language, prompts, tools, and interfaces can give
the model different working forms.

The required precision depends on the question and consumer. A language model
can work with clear natural-language descriptions of a situation, an allowed
change, and its expected consequence; other uses need typed data, equations,
or executable rules. Readable language is adequate when its actual interpretation
and use sustain the relevant distinctions. Readability alone does not establish
that adequacy. **Representation** makes selected relations available;
**simulation** develops how a represented situation could change under stated
assumptions. A useful representation need not simulate everything it represents,
and a conditional simulation is not an observation of the world.

A physical basis supplies neither these meanings nor a feasible calculation.
Reconstructing every microphysical detail of a conversation would not itself
specify what counts as a correction. Philosophical, psychological, computational,
and practical accounts select different relations within the same reality;
their bridges need investigation where the question requires it. Shared physical
ground establishes neither complete reduction nor a universal, faithful, or
tractable world simulator. Modeling activity as event streams also leaves open
which records and software architecture serve a particular use. The
[layers diagram](../diagrams/layers.html) presents this connection, and
[Trinity](local-source-and-website.md) develops its unity across the three
activities.

## A bounded computational example: a title and its preview

Suppose a person notices that an article's title misses its argument. The model
compares the title with the text and develops alternatives; their exchange
settles a correction to try and the question of whether its preview shows it.
The actual process includes a person, model, saved file,
editor, preview, and the material activity that keeps them working. The question
selects only a small part of that process. The **article persists** through the
edit by the chosen continuity between its source and corresponding preview;
its identity here does not require its text to remain unchanged.

To investigate this together, they distinguish a saved title from a displayed title. An edit
changes the first; a successful preview refresh is expected to make the second
match it. The task's completion constraint requires both titles to match the
requested correction. Editing and refreshing are different events, so a saved
correction can coexist with an old display. This model includes an object,
changing states, a source–preview relation, transition assumptions, and a
constraint because each helps answer the particular question.

A computer representation gives those terms usable referents: the relevant
file and title text, the corresponding preview, and operations for reading,
editing, refreshing, and inspecting them. The relation can be expressed to a
language model in ordinary prose; a program could instead encode title values
and transition rules explicitly. In either case, “saved title” means text read
from the source, while “displayed title” means what the preview actually shows.
Those observation routes keep two labels from silently referring to one value.

A **simulation** can now develop a conditional trace for them to examine: with both titles initially
old, editing makes the saved title new while the displayed title stays old;
a successful refresh then makes both new. A model can reason through this
small trace, or a program can execute its specified transitions. Neither result
shows that the actual preview refreshed. It establishes what follows within
the selected model and makes the intermediate mismatch predictable.

**Realization and readback** put this understanding to work through the actual
editor and preview. The model can carry the editing and inspection while
making the result available for the person's recognition and correction.
Reading the saved title and observing the preview supply separate evidence
for completion. If the display stays old after refresh, the
world has challenged the assumed transition. Investigation may reveal a cached
view or a preview linked to a different source. The remedy then changes the
refresh operation or the modeled source–preview relation, followed by another
readback. The discrepancy does not require a new theory of the whole world.

The return continues the same collaboration. If either participant finds that
the requested title itself misstates the article, a correct display will expose
a problem in the intended expression.
The purpose or interpretation may need revision even though the software works.
This is the general connection: the process supplies the object and resistance;
the participants develop a question and computational model together; an actual arrangement uses it;
consequences help locate whether to revise the realization, model, selection,
or wider understanding. The example's simple distinctions serve its task;
another question may need a different model.

## A process exceeds its available model

A stream is organized continuation, not merely a chronological transcript.
Perception, interpretation, remembering, expression, and action can overlap,
depend on earlier occurrences, or become explicit at different times. An
available record captures some of those relations; other activity may never
have been recorded. A local model makes selected objects, roles, dependencies,
and transformations available for a particular inquiry. Giving it a computer
representation enables selected uses of those relations; it does not contain
the entire process that generated it. The title example selects a pair of
observable values without recording everything involved in writing or reading.

Distinguish that model from its expression. A sentence, diagram, paper, or
program gives a relation a form that can be encountered. Producing and reading
the expression are themselves events in the continuing process. A model can
have several expressions, and one expression can admit competing readings.
Its occurrence, interpreted meaning, inferential consequences, and adequacy
to its subject are different questions. Later understanding may reorganize
what an earlier expression means without changing its original occurrence.
A computer representation is an expression with a further working relation:
an actual consumer can use its distinctions for the selected inquiry. Not
every expressive form has to serve that computational use.

Fiction makes this difference especially visible: constructing and encountering
a fictional work can have actual consequences without its characters existing
as described. A literary image can gather possibilities before one interpretation
is selected. Neither construction nor consequence makes every assertion drawn
from that image true.

## Screenshot and front end

A **screenshot** selects a moment and a frame from an activity that continues beyond it. A **front end** makes some of that activity perceptible and available for participation. As images of expression, they pose different questions: what has been selected, and what can a reader or participant now do through that selection? A diagram, prototype, or paragraph can show a relation without displaying every occurrence that produced it. An actual computer interface adds an operational correspondence: the article preview shows one state, and its refresh acts on a particular source. What appears and what an operation changes must be understood together.

Selection is both the expression's strength and a possible source of error. An account that displayed everything without distinction might fail to make anything intelligible. Yet a clear arrangement can conceal an uncertainty that would change the next judgment. An adequate expression therefore needs fidelity to what matters for its use, rather than an impossible duplication of the whole process. The question is which relations, assumptions, and unresolved alternatives must remain visible.

This also changes how collaboration can be organized. A model can carry retrieval, construction, and verification while a person understands, selects, and corrects through what becomes visible. Both can contribute to either side of that arrangement. An expression mediates participation: what it makes perceptible can change what happens next. A prototype can let the person recognize a relation through use, while an explanation lets either participant inspect why the prototype behaves as it does. Visibility and execution support each other, and their allocation can change with the work.

## Question-relative objects meet resistance

A question may make a person, utterance, memory, hypothesis, relationship, or
work its object. That choice guides which distinctions the inquiry needs;
it does not determine whether the answer is correct. The object can resist
its description through an omitted relation, an unexpected result, or a failed
prediction. As with the source–preview relation, such resistance can require
another abstraction, not merely another answer within the existing one.

Question-relative ontology therefore allows construction without treating
reality as an arbitrary product of naming. Stable objects, recurring patterns,
and scientific laws can remain supported across changing descriptions. The
person also exceeds a self-description: continuity may involve bodily life,
memory, relationships, commitments, and action without requiring an invariant
explicit account of oneself.

Revisability follows from incomplete access, changing questions, and the demand
to answer to evidence. A stable distinction can remain useful through many
changes because it continues to describe the relations that matter. Checking
its applicability connects that stability with the continuing process. Retaining a
source, entertaining a candidate, and accepting a claim remain different acts,
as developed in [reasoning within an unfinished stream](reasoning.md#sources-candidates-and-the-active-workspace).

## Physical realization and functional likeness

Human inquiry occurs under bodily, social, and material conditions. Model use
depends on implemented computation, data, infrastructure, and interaction.
Those conditions matter to what can be perceived, retained, expressed, and
done. A realization claim connects a function to a particular mechanism and
needs evidence at that level. Similar roles or observable performances do not
establish identical human and model architectures, mechanisms, or experiences.

The distinction matters when an expressive image is given a material reading.
Calling a model an illuminating counterpart can articulate its contribution
to understanding. Explaining how its output was physically produced requires
another investigation. [Finite inquiry and abstraction](finite-inquiry-and-abstraction.md)
develops the further distinction between physical realization, reduction, and
feasible calculation.

Three material and epistemic relations should also remain distinct:

| Question | Relation being investigated |
| --- | --- |
| Where did the materials come from? | A history of formation and transformation. |
| What supplies energy to the activity now? | Its current operating conditions and energy transfers. |
| What does the activity express, and is the claim supported? | Information, interpretation, inference, and evidence. |

The Department of Energy describes natural photosynthesis and research on
converting sunlight into chemical fuels. This gives sunlight a concrete relation
to chemical energy: incoming radiation can be transformed into stored energy
available for later activity.
[DOE, “Solar Fuels”](https://www.energy.gov/science/doe-explainssolar-fuels).

NASA describes the Sun and planets forming from a common collapsing cloud and
protoplanetary disk. That is a material history, distinct from present-day
sunlight powering an activity. A manufactured semiconductor has a history of
material extraction and fabrication; a computing installation has its own
present energy supply. Tracing those relations calls for evidence about the
particular material and installation.
[NASA, “How did our Solar System form?”](https://science.nasa.gov/astrobiology/learning-resources/alp/how-did-our-solar-system-form/).

These distinctions are this essay's inference from the different questions.
An energy account can explain how an expression becomes physically possible;
it does not yet explain what the expression means or why its claim is warranted.
The latter questions connect the produced work with its object and use.

## A work returns to the encounter

A work acquires relative independence from the encounter that produced it.
A paper can be challenged, a program can run differently from its author's
expectation, and an image can be understood differently by another reader.
Reception, operation, and resistance provide evidence neither participant can
settle by preference alone. The work can change subsequent understanding and
action while retaining its provenance.

In the [Sun–Moon–Earth relation](yinyang-and-taiji.md#sun-moon-and-earth), Earth names the
environment where these consequences occur. Roles do not fix either participant's
faculties: both can generate, interpret, judge, and revise. Return can revise
the account of the person, the counterpart, or their relationship, as well as
the work itself. These revisions can overlap: trying a tool can change the
understanding of a role while a new reading changes the tool's purpose. A new
question can emerge from reception, and a useful stable arrangement can survive it.

*An unfinished relation becomes a sentence. On the page it can answer back: its implication was not the one its author expected. Returning to it, the author sees an earlier thought differently and can begin from somewhere new.*

The distance between author and work is productive because others, and the
author as a reader, can encounter its actual arrangement. A paragraph may
entail a claim its author would reject; a prototype may expose a choice hidden
in the initial description. The maker can then distinguish revising the work
from revising their understanding of what they were trying to do. Later reading
establishes a new relation to the original occurrence while leaving its history
available for comparison.

In model-supported work, a partial intuition may become an argument or prototype. Reading it can disclose what fits, what is missing, or what the person did not mean. Revision participates in finding the relation being expressed. Person and model continue the same shared activity through this return; either can disclose a problem in its question, computational model, or implementation. [Embodied experimental philosophy](embodied-experimental-philosophy.md) develops the practical and reflective inquiries through which such feedback is assessed. The return can change a capacity to understand and generate as well as the artifact. The developmental question is what the person can now recognize, express, or do differently, including through reliably available support. A clearer artifact and a changed capacity are related outcomes whose connection becomes visible through subsequent participation.

## Hegelian comparison and its limits

Hegel's *Philosophy of Spirit* connects the development of consciousness and
theoretical and practical activity in [subjective spirit](https://www.marxists.org/reference/archive/hegel/works/sp/index.htm)
with freedom's public and institutional forms in objective spirit. Its account
of [absolute spirit, §§553 onward](https://www.marxists.org/reference/archive/hegel/works/sp/abspirit.htm)
develops art, religion, and philosophy as forms of self-comprehension. This gives
externalization a significance beyond putting an inner content outside: the
form through which activity becomes available to itself belongs to the
development of that activity.

His *Introduction to the Philosophy of History* connects self-knowledge and
freedom with public life and world history. Its object is wider than a person's
local account of inquiry. The comparison here takes up one relation within
that wider problem: how an expression gains distance and returns to
self-understanding. YinYang develops this relation at the scale of a person's
encounter with generative intelligence, where a work becomes an object through
which its maker can recognize and revise their activity.
[Hegel, Introduction](https://www.marxists.org/reference/archive/hegel/works/hi/introduction.htm).
The linked texts provide the public sources for this bounded comparison.

## Aesthetics participates in discovery

Light, color, spatial arrangement, parallel expression, condensation, and a
second reflective voice can make relations perceptible. Bilingual articulation
can expose differences between conceptual vocabularies. Such organization can
participate in finding a relation, rather than merely decorating an already
completed argument. A work's sensible form can reveal what a previous formulation
kept distant or difficult to compare.

Condensation can keep several possibilities available long enough to compare
them. Their differences can then be unfolded into premises, explanations,
or practical choices. Aesthetic form helps relations become perceptible;
definition and proof establish inferential connections; evidence tests claims
about the world. Their contributions meet in a work while supporting different
claims. The [Sun–Moon–Earth image](yinyang-and-taiji.md#sun-moon-and-earth) and the [miniature maker](writing-a-sinthome.md#a-miniature-god-whose-creations-answer-back) give these relations other expressive forms. Their interpretation and realization remain open to the world's answer.

## Source and claim scope

The linked public sources support their bounded scientific and philosophical
claims; the distinctions connecting them are YinYang's contemporary argument.
The process premise, jointly formed computational model, and return from actual
use carry that argument's continuity. They develop the objects and correspondences
needed to ask more precise questions and let their answers change the account.
