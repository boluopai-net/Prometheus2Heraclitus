# Diagram maintenance

These four conceptual maps connect the reading path, its developmental aim,
and selected [core views](../docs/core-views.md), with complete Chinese counterparts:

- **Steal Fire, Then Become Fire** (`formation-path`) connects
  the five parts and eighteen main essays. Its arrows describe what one part
  contributes to the next; the return brings new experience to trajectories,
  reflection, and revised aims and arrangements.
- **Join in stealing fire, and use it to cultivate yourself** (`borrowed-fire`)
  develops the stealing-fire essay's practical argument under a chosen
  developmental purpose. It separates accumulated works from demonstrated
  changes in the person's capacities, including reliably supported capacities.
  The person participates in the collective work rather than appearing only
  as a recipient of its results; the diagram does not require each participant
  to reproduce industrial model production.

- **How people and models inquire together** (`encounter`) connects YY-05, YY-10, and YY-11: records, candidate models,
  an adopted view, generated work, and returning evidence within human–model
  activity. YY-09 supplies its event-based vocabulary.
- **From understanding the world to realizing a practice** (`layers`) develops YY-09: physical grounding, computational abstraction,
  and the relations among ontology, epistemology, value, methods, and practice.

For the two detailed maps, the candidate JSON files own the authored labels, relationships, guided views,
and explanatory cards. HTML is the standalone interactive viewer. SVG is the
viewer's native static export of the graph and legend; the HTML cards and guided
views remain available in the viewer.

## Regeneration

The two responsive overview maps use `reading-maps.json` for bilingual
relationships, explanations, and essay membership. Run
`python3 skills/yinyang/scripts/render-reading-maps.py` from the collection.
The renderer uses current canonical essay headings and, for Site-authored
essays, the committed `website/content/philosophy/` source snapshot. Supply
`--site-source /path/to/site` to read titles from an in-progress native Site
checkout, then synchronize that committed Site afterward. The renderer generates
self-contained HTML and deliberately sparse SVG card previews. It uses the
Site's existing color and system-font vocabulary without external dependencies.
Native disclosure controls expose the essays; all five main relationships
remain visible without JavaScript. Desktop uses a horizontal route, while
phones arrange the same content vertically. The Site embeds these exact files
and adapts frame height and theme; it does not own a second copy of their prose.
Verify links, membership, disclosure behavior, and both viewport arrangements.

The two detailed viewers use Archify 3.1.0. From the YinYang references directory,
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
