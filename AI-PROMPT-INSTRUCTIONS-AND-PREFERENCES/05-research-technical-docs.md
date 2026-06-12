# Research and technical docs

This file is for research repos, experiment notes, technical READMEs, Kaggle
writeups, math notes, finance research, and reproducibility docs.

## Tone

Plain and factual, like a technical report.

Use:

- impersonal constructions
- concrete method names
- exact metrics
- sample sizes
- reproducibility notes
- limitations in their own section

Avoid:

- sales language
- encouragement
- "great question"
- "you are right"
- "honestly"
- "no hype"
- "for the record"
- "the value of this is"
- first-person diary narration
- private context
- prior chats
- other repos unless they are public dependencies

## Claims

Claims should be proportional to evidence.

Good:

```text
The run improves local CV from 0.803 to 0.812. Public leaderboard score remains
0.801, so the change is not yet externally validated.
```

Bad:

```text
This is a strong and exciting improvement that shows the method is working.
```

## Numbers first

Write numbers before interpretation when possible.

Good:

```text
Split-half reproducibility is 0.91. Ground-truth alignment is 0.13. The first
number measures stability, not correctness.
```

Bad:

```text
The method appears robust and accurate.
```

## Experiment-note shape

Use this structure:

```text
# Experiment NN: short name

## Question

One sentence.

## Method

Data, split, computation, model, baseline, and sample size.

## Outputs

Generated tables, figures, and files. Note whether they are tracked or
regenerable.

## Result

Numbers first, then interpretation.

## Caveat

What this does not establish.

## Lesson

The reusable rule or next decision.
```

## Public README shape

Use:

- one-sentence scope
- current status
- key findings table
- how to run
- project layout
- limitations
- links to details

Avoid:

- full project diary
- raw planning notes
- repeated caveats
- long source digests
- copied paper text
- private research archives

## Limitations

Use "Limitations" or "Caveats." Do not write "honest caveats" as a recurring
style marker.

Good:

```text
Limitations: one dataset, no frozen holdout, and no independent replication.
```

Bad:

```text
To be completely honest, this should not be overclaimed.
```

## Public release for research repos

Keep public:

- source code
- tests
- runners
- selected small result tables
- generated figures only if useful and allowed
- verified findings
- documentation conventions
- update maps
- preregistration or experiment notes

Keep private or review first:

- raw data
- source snapshots
- copied paper text
- raw model outputs
- prompt archives
- local paths
- scaffold suggestions
- full private research logs

## Documentation drift

Use an update map when changes affect multiple docs.

Example:

- New result changes interpretation -> update experiment note, summary table,
  README status if the milestone changed, and decisions log if ranking changed.
- New dataset -> update data inventory and source log.
- New public claim -> add the supporting experiment or citation.

## Figures

Figure titles should describe what the chart shows. No slogans.

Use:

- direct title
- readable labels
- legends outside plot area if needed
- no overlapping text
- regeneration script committed with the figure when practical

Avoid:

- editorial captions inside charts
- "breakthrough" or "real signal" titles
- unreadable label piles

