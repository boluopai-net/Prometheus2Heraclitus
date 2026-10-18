# Design basis

## Reusable design distinctions

This method treats a personal environment as the connected instructions,
capabilities, services, and surfaces through which a person and model work.
Prompts, Skills, MCP connections, plugins, applications, automation, and local or
cloud services can all affect that work. Trace their contribution from discovery
and configuration to execution and observable result. Their labels alone do not
establish which capabilities are installed, connected, or actually usable.

Human-facing design remains one contribution to this broader configuration
method. A website, desktop, application, document, launcher, and automation can
participate in one journey without becoming one application. Its design follows
the person's use rather than the inventory of tools or repositories.

Cognitive effort and physical interaction both matter. Parallel software work
can help while competing requests for the person's attention make coordination
harder. This is a design consideration about actual participation, not a measured
claim about every person's abilities or a ban on parallel activity.

Simplification should preserve distinctions needed for judgment. Fewer clicks,
fewer visible elements, and attractive screens are observations; they cannot
by themselves establish a better journey. Compare what the person must find,
remember, understand, enter, switch, wait for, and recover. An extra explanation
or deliberate step can reduce uncertainty and later rework.

Implementation information belongs with maintenance when the person does not
need it to choose or act. Quiet automation still needs visible outcomes,
recoverable errors, and inspectable consequential state. Existing permission
and consent boundaries remain unchanged by design convenience.

These generalized distinctions replace private originating conversation evidence
in this public adaptation. They are working hypotheses to test against actual
use, not a portrait of an originating user.

## Configuration and service rationale

The public adaptation retains the original human-use method in
[Human use](human-use.md) and expands the entrypoint to overall environment
configuration. A separate prompt-and-skill authoring method can own its detailed
lifecycle, while this method connects it with tools, services, and human use.
Specialists and native configuration owners are selected from the recipient's
actual environment.

[MCP and services](mcp-and-services.md) distinguishes connection transport,
backend execution location, and safe process sharing. Native compatible
connections can remove unnecessary bridges; suitable hosted execution or shared
local work can reduce duplication. These are design options whose contribution
depends on actual implementation, state isolation, resource costs, and client
readback. They are not universal memory thresholds or a requirement to migrate
every service.

The public references below support human-use design. They do not establish MCP
compatibility, authentication support, service isolation, or resource savings.
Those judgments require the affected implementation's current documentation
and runtime evidence. This package supplies a reusable method, not a copy of a
particular host's configuration or authority.

## Selected external evidence

Public references retained from the originating method's 2026-10-12 source
review. Their supporting roles are summarized here; current interface choices
should be checked against current documentation and actual behavior.

- [Nielsen Norman Group: Interaction Cost](https://www.nngroup.com/articles/interaction-cost-definition/)
  treats cognitive and physical effort as parts of completing a task. This
  supports assessing a journey beyond its number of clicks.
- [Nielsen Norman Group: Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
  includes recognition, visible state, user control, and error recovery as
  separate usability concerns. Quiet automation therefore needs feedback and
  recovery as well as fewer manual steps.
- [GitHub Primer: Progressive Disclosure](https://github.com/primer/design/blob/main/content/ui-patterns/progressive-disclosure.mdx)
  is an archived design-system reference for selectively revealing detail
  while preserving the user's focus. It does not establish that all dense
  interfaces should be collapsed or that this environment should adopt Primer.

These references support design judgments; they are not dependencies, imported
instructions, fixed numerical thresholds, or evidence of this person's measured
performance. Preserve the actual task's needed concepts and compare proposed
simplification against its navigation and recovery costs.
