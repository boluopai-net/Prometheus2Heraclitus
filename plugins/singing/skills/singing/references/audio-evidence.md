# Audio evidence and phrase comparison

## Recording integrity

Confirm identity, start offset, duration, channel layout, and sample rate for
each input. Keep the raw vocal take unchanged and analyze a labelled derivative
if decoding or resampling is needed. Check each channel: averaging stereo can
cancel signal, while selecting an empty channel can create false silence.
Inspect onset and end to catch a missing entrance or premature stop.

Peak/RMS and full-scale samples help diagnose capture. They do not measure
musical quality. Low RMS can reflect quiet singing, distance, gain, or silence;
full-scale samples suggest possible clipping, while prior processing may hide
clipping below full scale. Listen and inspect the signal before attributing a
cause. The bundled checker reports exact metrics under its stated definitions,
not “pass/fail” vocal quality or integrated LUFS.

## Compare a corresponding phrase

Locate the same lyric and musical gesture in both versions. Establish offsets
from a shared entrance or accompaniment cue. Retain original timestamps and
report any trimming, resampling, pitch shift, separation, or alignment used.
Different live/album versions may have different arrangements; identify that
before calling a difference a performance error.

Extract pitch from a sufficiently isolated lead when supported. Inspect voiced
confidence and octave discontinuities against listening or a spectral view.
Background harmony, bleed, consonants, breath, and separation artifacts can
mislead an extractor. Choose bounds from the audible passage rather than a
gender assumption. Compare stable notes and transitions separately.
For reliable corresponding frequencies, cents difference is
$1200\log_2(f_{take}/f_{reference})$. Retain the trajectory for slides and runs;
a phrase-wide median erases musical detail.

Keep entrance, consonant release, vowel onset, and note onset distinctions clear.
Compare timing on the original timeline in milliseconds or beats. Dynamic time
warping may locate corresponding gestures, but its aligned overlay cannot prove
rhythmic agreement. Preserve pre-alignment offsets and durations to expose
rushing, dragging, and drift. Tempo changes or accompaniment latency can affect
the interpretation.

Compare intensity within phrases with consistent processing. Microphone gain,
compression, distance, and accompaniment affect absolute level comparisons.
Describe a relative contour only where supported. Vibrato and ornaments need
enough stable voiced material and temporal resolution; report extraction limits
instead of supplying a precise number from an unsuitable passage.

## Turn evidence into musical feedback

Use three distinct layers, in ordinary language:

- Observation: the take enters about 120 ms after the reference at the selected
  lyric, with the measurement's confidence and offset assumptions stated.
- Interpretation: that entrance may make the phrase feel less urgent; this is a
  listening judgment that depends on the intended style.
- Attempt: listen to the reference pickup, sing through the complete sentence,
  and aim the first vowel at the accompaniment cue; compare the next take.

This is an illustrative feedback shape, not a finding about an actual singer.
Use actual timestamps and audible evidence in a session. Diction feedback should
identify the word or syllable that loses clarity and its effect on the phrase.
Offer an expressive cue or audible model when useful, without claiming that a
specific physical mechanism has been diagnosed. Keep health or clinical claims
outside acoustic coaching. If the singer reports discomfort, do not treat it
as a technique defect established by the waveform.

Return the recording before requesting self-evaluation. Preserve earlier takes
for comparison and check whether the adjustment improved the intended effect.
One take establishes evidence about that take, not a permanent ability, identity,
physiology, or ranking against other singers.
