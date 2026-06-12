# Bad and good examples

This file is the fast pattern bank. It shows the transformation directly.

## Public constraint leakage

Bad:

```text
Public boundary: this page contains only sanitized visuals and no private logs.
```

Good:

```text
The page shows the current menu flow, early combat clips, and the systems that
are stable enough to explain publicly.
```

## Game showcase

Bad:

```text
This public-facing update documents the sanitized pipeline state while avoiding
private archive details.
```

Good:

```text
The run loop now has towns, routes, shops, trainer fights, and the base combat
flow connected. The rough part is pacing: battles work, but they still need
clearer hit timing and impact.
```

## AI use

Bad:

```text
Although AI-generated assets are used, care has been taken to avoid slop and
maintain transparency.
```

Good:

```text
AI speeds up art and code prototypes. I keep the parts that fit the game and
replace the parts that do not.
```

## Research result

Bad:

```text
This result proves scale is the key.
```

Good:

```text
This result supports scale as a candidate lever on this validation surface. It
does not yet prove scale is the target-score bottleneck, because earlier scale
probes failed to transfer.
```

## Research flip-flop

Bad:

```text
The newest run contradicts the old run, so follow the newest run.
```

Good:

```text
The contradiction is the finding. Before changing direction, explain whether the
disagreement came from score scale, data split, variable coupling, recentering,
or a hidden-label convention mismatch.
```

## Kaggle local benchmark

Bad:

```text
The local score improved, so submit it.
```

Good:

```text
The local score improved, but this benchmark has mispredicted public direction
before. Treat the result as a sanity check until it is isolated and tied to a
validation signal that predicts the public metric.
```

## Technical README

Bad:

```text
This project provides a powerful and elegant framework for robust event mining.
```

Good:

```text
The project mines event rules from time-series features, scores them on
validation windows, and tests whether accepted cases beat zero-return and
momentum baselines.
```

## College class note

Bad:

```text
This note is designed to help the student understand washer-method axis shifts.
```

Good:

```text
Washer method around `x = 1`: radius is horizontal distance to the axis, so use
`|x - 1|`, not just `x`.
```

## Twitch bot/persona

Bad:

```text
This persona feature uses sanitized chat examples while preserving user privacy.
```

Good:

```text
Personas are built from message habits: length, casing, repeated phrases,
emotes, reply targets, and topic context. Public demos use aggregate or
permission-safe examples.
```

## Hobby writeup

Bad:

```text
This writeup honestly documents the limitations of the approach while showing
why the result is still exciting.
```

Good:

```text
Local CV improved from 0.803 to 0.812. Public score stayed at 0.801. The change
is useful as a local feature test, not as evidence of leaderboard improvement.
```

## Documentation maintenance

Bad:

```text
Keep all docs synced and up to date.
```

Good:

```text
`MASTER_REVIEW.md` owns the evidence ranking. The README summarizes it. Older
strategy briefs must link to the current front door when superseded.
```

## Code comment

Bad:

```python
score = compute_score(rows)  # Updated to use the new scoring method
```

Good:

```python
score = compute_score(rows)  # Uses tolerance-normalized MAE for all targets.
```

## Surface AI tell

Bad:

```text
This powerful framework provides a clean, robust, and deeply practical solution
to the problem.
```

Good:

```text
The framework scans source files, creates a manifest, and renders concise notes
with links back to the originals.
```

