# Diagram maintenance

These conceptual maps explain selected [core views](../docs/core-views.md),
with complete Chinese counterparts:

- **Encounter** connects YY-05, YY-10, and YY-11: records, candidate models,
  an adopted view, generated work, and returning evidence within human–model
  activity. YY-09 supplies its event-based vocabulary.
- **Layers** develops YY-09: physical grounding, computational abstraction,
  and the relations among ontology, epistemology, value, methods, and practice.

The candidate JSON files own the authored labels, relationships, guided views,
and explanatory cards. HTML is the standalone interactive viewer. SVG is the
viewer's native static export of the graph and legend; the HTML cards and guided
views remain available in the viewer.

## Regeneration

The current viewers use Archify 3.1.0. From the YinYang references directory,
set `ARCHIFY_CLI` to the installed `bin/archify.mjs` and choose a temporary
`CHECK_DIR` for the run:

```sh
node "$ARCHIFY_CLI" finalize architecture diagrams/encounter.candidate.json diagrams/encounter.html --quality showcase --out-dir "$CHECK_DIR/encounter" --json
node "$ARCHIFY_CLI" finalize architecture diagrams/layers.candidate.json diagrams/layers.html --quality showcase --out-dir "$CHECK_DIR/layers" --json
node "$ARCHIFY_CLI" finalize architecture diagrams/encounter.zh-CN.candidate.json diagrams/encounter.zh-CN.html --quality showcase --out-dir "$CHECK_DIR/encounter-zh" --json
node "$ARCHIFY_CLI" finalize architecture diagrams/layers.zh-CN.candidate.json diagrams/layers.zh-CN.html --quality showcase --out-dir "$CHECK_DIR/layers-zh" --json
```

Regenerate only changed candidates or artifacts requiring repair. After successful
finalization, use **Export → SVG · Auto** (or **导出 → SVG · 自动**) for the
matching static export. Headless browser controls preserve desktop focus.
Retain the semantic translation overrides when updating the tool: they describe
questions and modeled relationships rather than software services.

Check meaningful labels, directions, and readability against the owning text.
Native delivery and browser receipts are execution evidence and contain local
paths; keep them with that execution rather than distributing a second hash
registry. A future checkout can run its own checks on its actual artifacts.

Trace motion follows authored arrows. It illustrates local relationships, not
a mandatory sequence, causal strength, or measured rate of development.
Both maps leave activity outside their selected questions unrepresented.

Retain [third-party notices](THIRD-PARTY-NOTICES.md) with viewers and exports;
the original claims keep their own license.
