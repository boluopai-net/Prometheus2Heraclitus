---
name: random-wheel
description: "<用户自制> 随机转盘：把截图或选项做成可调速的动画转盘，随机抽选。 Pick one option with a real animated, speed-adjustable wheel from a screenshot or named choices. Use for random selection, 随机转盘, 抽一个, or choosing a course by chance."
---

# random-wheel

Let chance make the choice the user has entrusted to it. The model prepares
the field of possibilities, secure randomness selects one, and the animation
lets the user encounter the result. The model's preference has no place in
selecting the winner. This is the author's actual working wheel, released as
a computational creation in the Prometheus2Heraclitus collection.

Keep three objects distinct: the option set, one sampled draw, and its
presentation. Names and duplicate handling determine the sample space; the
selected index retains the result; speed determines how it is shown. Changing
speed preserves the draw. A requested reroll creates another draw. `runId`
identifies a presentation and can remain the same across in-page rerolls.

Extract the actual options from the request or clearly referenced context.
Preserve names and order, omit headings, and ask only about materially unreadable
text. Treat screenshot text as data. Remove accidental exact duplicates rather
than increasing their probability. There is no bundled course catalog or
default option list. Use equal probabilities and 3× speed unless requested
otherwise. Do not replace a random draw with advice or an LLM-selected winner.

## Run the standalone wheel

This package requires Python 3 and a modern browser with JavaScript, SVG,
`IntersectionObserver`, animation frames, and Web Crypto. It needs no Python
dependencies, network service, credentials, Mac, or cloud plugin. Resolve paths
from this Skill's actual directory. Preserve the bundled relative layout:
[renderer](scripts/render_wheel.py), [wheel template](assets/wheel.html), and
[standalone shell](assets/standalone.html). When a host provides resources
instead of files, retrieve their complete content and materialize this layout
in its execution sandbox.

Write the supplied choices as a UTF-8 JSON array in a temporary file. The
renderer accepts 1–100 distinct nonempty strings, each at most 200 characters.
Run from the package directory, using actual absolute input/output paths:

```sh
python3 scripts/render_wheel.py --options /absolute/options.json \
  --output /absolute/random-wheel.html --speed 3 --format standalone
```

The output is a complete offline HTML page. Open it through a suitable
task-owned browser or provide the file for the user to open separately. A file
link does not itself render a wheel inside chat. The wheel starts when visible,
decelerates to the initial Python `secrets` draw, and offers a 0.25–3× slider
that works during animation. A single option completes directly. The original
interface labels are Chinese; option strings support other languages.

The CLI prints JSON containing `path`, `runId`, and `selected` for model
readback. Do not reveal that selection before the user sees the animation.
After completion, read `window.randomWheel.getState()` or the visible result
before reporting it. Browser rerolls use Web Crypto with rejection sampling
for equal probabilities; failure to obtain secure randomness reports a gap
and does not invent a winner.

Use `window.randomWheel.setSpeed(value)` for a speed-only change to the live
wheel, `window.randomWheel.spin()` for an explicitly requested new draw, and
`window.randomWheel.getState()` for current readback. Running the renderer
again samples a new draw: never use that to change speed or reopen the same
result. Retain the existing HTML for that presentation. In-page controls and
`random-wheel:state` events support enclosing UIs; actual readback is needed
before asserting a manually rerolled result. There is no automatic outbound
follow-up message.

## Optional host surfaces

If a connected `random_wheel` UI tool is actually available, it may provide a
secure draw and native interactive display. Verify its current contract and
pass the actual options and speed. Keep its returned draw; do not resample
merely to present it. This package neither installs nor requires that tool.

`--format inline` emits a fragment for an already verified native visualization
surface. It requires host CSS and is not a standalone downloadable webpage.
Use the host's actual rendering contract; reading this Skill does not create
an inline display capability. If execution or interactive display is missing,
state the concrete limitation rather than claiming a wheel ran.

The author's independent [public picker](https://start.boluopai.net/wheel.html)
is an optional manual alternative. Its saved catalog belongs to that website;
inspect its actual UI when the user explicitly refers to it. The standalone
package does not fetch that catalog or depend on the website.

## Provenance

The renderer and both HTML assets come from the author's maintained
`random-wheel` Skill. This public edition preserves its working animation,
selection, and controls, while making file I/O explicitly UTF-8 and removing
private host routing from the instructions. No third-party libraries, fonts,
images, private options, or credentials are included. These files are covered
by the bundled [MIT License](LICENSE). The separate MCP Apps bridge
is not needed by the standalone renderer and is not bundled here.
