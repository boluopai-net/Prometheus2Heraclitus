# Diagram maintenance

The article-local `taiji.svg` is a conventional black-and-white symbol authored
directly as accessible SVG. Its two opposite-color dots illustrate the
body/role and eye/actual-participant reading developed in
`../docs/yinyang-and-taiji.md`; the geometric symbol does not establish that
interpretation. Both reader editions embed the same language-neutral figure.
The native Site separately owns the paired-fish opening illustration.

These four conceptual maps connect the reading path, its developmental aim,
and selected [core views](../docs/core-views.md), with complete Chinese counterparts:

- **Steal Fire, Then Become Fire** (`formation-path`) places ongoing
  human–model practice at the center of trajectories, reflection, personal
  philosophy and models, and environments and works. The developmental aim
  gives the whole a direction; reflection clarifies the pictures organizing
  experience, and new experience can revise that direction through the relationships.
  It condenses the five-part argument without reproducing the article directory.
- **Join in stealing fire, and use it to cultivate yourself** (`borrowed-fire`)
  develops the stealing-fire essay's practical argument under a chosen
  developmental purpose. It separates accumulated works from demonstrated
  changes in the person's capacities, desires, and aims, including reliably
  supported capacities. Shared practice and the living environment connect
  those changes to further activity; cultivation can revise what is worth creating.
  The person participates in the collective work rather than appearing only
  as a recipient of its results; the diagram does not require each participant
  to reproduce industrial model production.

- **How people and models inquire together** (`encounter`) connects records, candidate models,
  an adopted view, generated work, and returning evidence within human–model
  activity. Activity and interaction histories are event streams; records
  preserve selected parts, while conceptual participant models are inferred
  from histories and other material. The participants themselves are not
  identified with those streams. Its vocabulary connects the essays on process,
  inquiry, participants, and revisable understanding; the map is not restricted
  to a numbered core view.
- **Six philosophical dimensions and shared practice** (`layers`) develops
  the philosophical account through seven visible subjects. Worldview, ontology, theory of truth,
  epistemology, axiology, and methodology each state an adopted position and
  connect their contribution to shared human–model practice. Supporting cards
  unfold computational ontology, conceptual models, expression, realization,
  and feedback within practice. They explain representation and physical
  realization as distinct relations and connect personal-first humanism with
  concrete criteria. The viewer retains node inspection, relationship
  exploration, and guided views.

For the two detailed maps, the candidate JSON files own the authored labels, relationships, guided views,
and explanatory cards. HTML is the standalone interactive viewer. SVG is the
viewer's native static export of the graph and legend; the HTML cards and guided
views remain available in the viewer.

## Regeneration

The two responsive concept maps use `reading-maps.json` for their bilingual
concepts, relationship labels, and accessible descriptions. Run
`python3 skills/yinyang/scripts/render-reading-maps.py` from the collection.
The renderer owns two explicit SVG compositions, with separate desktop and
mobile geometry. It generates self-contained HTML and full SVG diagrams. It uses the
Site's existing color and system-font vocabulary without external dependencies.
Nodes and directed connections carry the meaning; there are no article lists,
disclosure cards, cross-diagram links, or standalone-view buttons inside them.
The complete graph remains visible without JavaScript. The Site adapts frame
height and theme only. Inspect label readability, node and edge relationships,
and both viewport compositions. The philosophy directory retains four compact
review links after its five chapter entries; it embeds no diagram.

The detailed viewers are generated with Archify 3.2.0. Their titles describe
their subject without limiting their scope to selected numbered core views.
The Site places graph-only figures in the first relevant article discussion;
standalone viewers retain their explanatory cards and inspection controls.
From the YinYang references directory,
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
