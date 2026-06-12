# Research methodology failure modes

This file covers a different problem than AI-sounding prose. It is about
AI-sounding research behavior: overreacting to one result, forgetting earlier
flip-flops, and turning a local finding into a conclusion before the evidence is
strong enough.

## Main rule

A single result is not a verdict. It is a clue.

Before treating a result as important, ask:

- What exactly did the number measure?
- Is it comparable to the number being discussed?
- Did the result transfer to the target metric?
- Did prior experiments point the other way?
- Did the methodology isolate the changed variable?
- Could the result be a local benchmark artifact, leakage, recentering effect,
  scoring mismatch, or hidden distribution mismatch?
- What would disprove the interpretation?

## Failure mode: holy-grail result

Bad:

```text
Scale helped here, so scale is the main bottleneck.
```

Better:

```text
Scale helped in this run. Before making it the main bottleneck, compare it to
the prior runs where scale changes did not transfer, check whether the metric is
the same, and isolate whether the gain came from scale itself or from a coupled
post-processing change.
```

Rule:
Do not promote one result until it survives comparison against the history and
the target metric.

## Failure mode: forgetting the flip-flop history

Bad:

```text
The latest experiment shows the direction. Continue this path.
```

Better:

```text
The latest experiment points this way, but the project has alternated between
"scale helps" and "scale does not help." That flip-flop is evidence about the
methodology. The next step is to explain why the same claim changes across runs.
```

Rule:
Repeated reversals are not noise to ignore. They are evidence that the validation
surface, scoring scale, or variable isolation may be broken.

## Failure mode: local oracle mistaken for target evidence

Bad:

```text
The local benchmark improved, so submit it.
```

Better:

```text
The local benchmark improved, but it uses true scale and a different comparison
surface. It is a sanity tool, not submission evidence. Submit only if the change
also survives a validation layer that predicts the target metric.
```

Rule:
Name the exam. Do not compare numbers across different exams.

## Failure mode: coupled changes treated as isolated evidence

Bad:

```text
The scale-tail submission failed, so scale-tail is bad.
```

Better:

```text
The scale-tail file changed scale on a small set of rows, but recentering moved
many other FL rows. The failed submission does not isolate whether the problem
was the scale rows, borrowed assumptions, or recenter ripple.
```

Rule:
If multiple mechanisms moved, the result cannot prove which mechanism caused the
score change.

## Failure mode: chasing the satisfying explanation

Bad:

```text
The bend is anatomically real, so modeling the bend should improve the score.
```

Better:

```text
The bend can be anatomically real and still diverge from the scoring convention.
The target is the metric's measurement procedure, not the most satisfying
biological story.
```

Rule:
The best explanation is not always the score-moving explanation.

## Failure mode: leaderboard as the only judge

Bad:

```text
Try another public submission and see if it improves.
```

Better:

```text
Stop isolated submissions until there is a validation signal, a verified bug fix,
or a substantial model branch. A public submission should test a specific
hypothesis, not replace methodology.
```

Rule:
The leaderboard is a scarce, noisy external check. It is not the research loop.

## Failure mode: stale ranking after new evidence

Bad:

```text
The plan still says scale is the next lever, so continue scale work.
```

Better:

```text
The plan predates later failed scale-tail and MT probes. Update the ranking
before continuing. The next lever should reflect the current evidence, not the
old brief.
```

Rule:
Plans have timestamps. A good old plan becomes a bad current plan when new
evidence changes the ranking.

## Failure mode: method beauty over score relevance

Bad:

```text
This is a cleaner and more protocol-aligned method, so it should be preferred.
```

Better:

```text
The method is cleaner and protocol-aligned, but it worsened the target score. It
should stay rejected unless a new audit finds the implementation was wrong or the
validation target changes.
```

Rule:
Elegance is not evidence. A better-looking method can lose.

## Evidence ladder

Use this ladder before claiming a finding matters:

1. Observation: one run changed a number.
2. Isolation: only the intended variable moved.
3. Repeatability: the result survives rerun, seed, fold, or nearby variant.
4. Transfer: the result predicts the target metric or an accepted proxy.
5. Mechanism: the cause is understood well enough to avoid cargo-culting.
6. Decision: the result changes the ranking of next actions.

Most AI research mistakes happen by jumping from step 1 to step 6.

## Required writeup pattern for uncertain findings

Use:

```text
Result:
What changed, with numbers.

Scope:
What data, score scale, and validation surface this measured.

Interpretation:
What the result suggests.

Counterevidence:
Prior runs or facts that point the other way.

Method risk:
What could make the result misleading.

Next proof:
What would confirm or reject the interpretation.
```

## Bad and good examples

Bad:

```text
Scale is the missing piece. The benchmark shows the score can reach 0.33 with
correct scale, so improving scale should close most of the gap.
```

Good:

```text
Correct scale is necessary for real measurement, but the 0.33 benchmark and the
0.62 leaderboard are different score surfaces. The benchmark uses true scale and
does not directly value the target scale router. The scale claim needs an
A-to-A comparison or an isolated target-set validation signal.
```

Bad:

```text
The local FL blend improved, so it is the next submission.
```

Good:

```text
The local FL blend improved on the 35-image harness, but the public submission
regressed. Treat this as evidence that the local FL harness is not a reliable
submission oracle for that change.
```

Bad:

```text
The newest result contradicts the old result, so use the newest result.
```

Good:

```text
The contradiction is now the object of study. First explain why the old and new
results disagree: score scale, data split, recentering, hidden-label convention,
or variable coupling.
```

