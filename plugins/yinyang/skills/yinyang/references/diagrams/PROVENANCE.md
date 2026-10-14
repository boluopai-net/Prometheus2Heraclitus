# Diagram maintenance

These concept diagrams interpret the English public claims in `docs/core-views.md`
and the corresponding complete Chinese edition: `encounter` covers YY-05,
YY-10 and YY-11, with the ongoing-process distinction developed in YY-09;
`layers` covers YY-09. English is primary; the complete matching Chinese versions
use the `.zh-CN` filename suffix. The candidate JSON files are the editable source.
HTML is the self-contained interactive viewer;
SVG is a canonical static export made through the viewer's native export menu.
The SVG contains the graph and legend; explanatory cards and guided views remain
in the HTML and the public claim text.

Generated with Archify 3.0.1. From the YinYang references directory (`skills/yinyang/references/` in the collection), with `ARCHIFY_CLI` pointing
to the installed `bin/archify.mjs`, regeneration uses:

```sh
node "$ARCHIFY_CLI" finalize architecture diagrams/encounter.candidate.json diagrams/encounter.html --quality showcase --out-dir "$CHECK_DIR/encounter" --json
node "$ARCHIFY_CLI" finalize architecture diagrams/layers.candidate.json diagrams/layers.html --quality showcase --out-dir "$CHECK_DIR/layers" --json
node "$ARCHIFY_CLI" finalize architecture diagrams/encounter.zh-CN.candidate.json diagrams/encounter.zh-CN.html --quality showcase --out-dir "$CHECK_DIR/encounter-zh" --json
node "$ARCHIFY_CLI" finalize architecture diagrams/layers.zh-CN.candidate.json diagrams/layers.zh-CN.html --quality showcase --out-dir "$CHECK_DIR/layers-zh" --json
```

Choose a new temporary `CHECK_DIR` for a changed candidate. After successful
finalization, the viewer's **Export → SVG · Auto** action (or **导出 → SVG · 自动**)
produces the dual-theme
static preview. Use headless browser controls for this operation when preserving
desktop focus. No server or package installation is required to read the HTML.

Candidates carry their complete resolved language catalogs because Archify 3.0.1
uses English defaults for missing keys in a custom catalog. The small semantic
overrides describe modeled relations and questions instead of software components.
Preserve those overrides when updating the catalog with a future tool version.

`validation.json` records portable byte hashes and completed checks. Its
`pathBase` is relative to that file: `..` is the YinYang references directory. Source,
candidate output, and recorded file paths resolve from that root. Native
delivery and browser receipts contain machine-local absolute paths; they are
temporary execution evidence and are deliberately excluded from this repository.
Do not treat this portable summary as a native delivery sidecar. A future strict
provenance check requires a fresh finalize run in its own checkout.

Trace motion shows authored relationship directions. It does not establish
temporal order, causal strength, update frequency, or demonstrated human growth.
These are conceptual maps, not executable workflows or authority hierarchies.
The displayed relations illustrate one local path through revisitable source
occurrences, conditional candidate models, adopted views, outputs and evidence.
The ongoing process exceeds any selected view; its input need not be an explicit
query. Both the human and model are modeled as interacting event streams;
local working models are revisable formations within that process. Candidate
coexistence does not itself jointly accept incompatible premises. The selected
analogy favors a coherent working ontology while accommodating conflicting
data and interpretations, supporting stability without freezing the ontology.
The preference-harness analogy informs informal natural-language reasoning;
it does not require formal modeling or select a calculus. Human/model contributions
are permeable positions of generation and judgment. Computational ontology
provides their shared event-based foundation; physical reduction is neither
established nor required here.

Retain [third-party notices](THIRD-PARTY-NOTICES.md) with redistributed generated
viewers and exports. This notice does not assign a license to the original claims.
