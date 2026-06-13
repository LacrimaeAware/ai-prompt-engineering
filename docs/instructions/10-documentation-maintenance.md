# Documentation maintenance and dependency rules

This file is for living documentation systems: project READMEs, handoffs,
experiment logs, roadmaps, public pages, private notes, and any repo where many
documents can drift apart.

## Main rule

Documentation is a system. Treat it like one.

A document should have:

- a clear owner role
- a freshness status
- a known relationship to other docs
- a defined update trigger
- a reason to exist that is not duplicated elsewhere

## Failure mode: many front doors

Bad:

```text
Read the README, handoff, synthesis, strategy brief, master review, and current
alignment. They all contain the current state.
```

Better:

```text
Current front door: `STATE_RESET_2026-06-10.md`.
`MASTER_REVIEW.md` owns the evidence ranking.
`NEXT_SUBMISSION_REVIEW.md` owns the latest submission decision.
Older strategy briefs are archive/context only.
```

Rule:
There should be one current front door. Other docs should say whether they are
current, specialized, or archived.

## Failure mode: duplicate truths

Bad:

```text
The README says scale is the bottleneck. The synthesis says FL is the bottleneck.
The master review says segmentation is the bottleneck.
```

Better:

```text
The master review owns the current bottleneck ranking. The README summarizes it.
The synthesis keeps historical reasoning and must defer to the master review
when they disagree.
```

Rule:
Do not let several docs independently own the same conclusion.

## Failure mode: stale docs without labels

Bad:

```text
This plan says retraining is lower priority.
```

Better:

```text
Archive note: this plan predates the failed FL blend, MT vertical-3, and
scale-tail probes. Current priority is in `STATE_RESET_2026-06-10.md`.
```

Rule:
If a document remains useful but stale, label it at the top. Do not silently let
old advice compete with current advice.

## Failure mode: no semantic dependencies

Bad:

```text
Update the docs.
```

Better:

```text
This result changes the bottleneck ranking, so update:
- the experiment note that owns the result
- the master review ranking
- the README status line if the public summary changes
- the decisions log if priority changed
- the handoff if it affects the next session
```

Rule:
Know which documents semantically depend on a result.

## Document ownership model

Recommended roles:

- README: public front page and short current status.
- Handoff: fastest re-entry for the next chat or tired future session.
- Master review: current evidence ranking and decisions.
- Experiment note: one experiment, one method, one result, one caveat.
- Decision log: open and settled decisions with dates.
- Source log: where inputs came from.
- Update map: what to touch when a fact changes.
- Public-readiness audit: private release blockers.
- Dev journal: private session history and rough context.
- Archive note: historical document kept for context, not current action.

## Freshness labels

Use one of:

```text
Status: current front door
Status: current specialist doc
Status: historical context
Status: superseded by <file>
Status: private scratch
Status: public summary
```

This prevents future AI from treating every Markdown file as equally current.

## Dependency block

For important living docs, add a small block:

```text
Owns:
- current bottleneck ranking
- accepted/rejected submission list

Depends on:
- experiment notes under `experiments/`
- latest leaderboard submissions
- benchmark lab score tables

Update when:
- a submitted score changes the anchor
- a local validation result changes the ranking
- a method is accepted or rejected
```

## Table of contents

A good table of contents should answer:

- Where is the current state?
- Where are the detailed results?
- Where are the decisions?
- Where are the raw/private notes?
- Which docs are stale?
- Which docs should a new AI read first?

Bad TOC:

```text
Docs:
- notes
- plan
- review
- synthesis
- current alignment
```

Better TOC:

```text
Start here:
- `STATE_RESET_2026-06-10.md`: current state and next action.

Current evidence:
- `MASTER_REVIEW.md`: accepted/rejected claims and score-scale rules.
- `NEXT_SUBMISSION_REVIEW.md`: latest submitted files and decisions.

Historical:
- `strategy_brief.md`: archived original plan, superseded after 2026-06-10.
```

## Database-backed docs

A database-backed documentation layer can help when the same facts need to render
in multiple views.

Use a database or structured source when:

- many docs repeat the same table
- results update often
- status depends on machine-readable experiment metadata
- multiple pages need the same source of truth
- stale duplicated tables have already caused errors

Do not use a database when:

- a short hand-written note is clearer
- the facts are narrative decisions
- the schema would become a second project
- the document is a one-off public page

Good compromise:

- store experiment metadata in structured files or tables
- render summaries from that source
- keep interpretation in authored docs
- include generated timestamp and source file list

## Update checklist

When a result changes:

1. Identify the fact that changed.
2. Identify the owning doc.
3. Update dependent summaries.
4. Mark superseded docs if they disagree.
5. Update the table of contents if the entry point changed.
6. Remove duplicated claims where possible.
7. Add a short dated decision note.

## Bad and good examples

Bad:

```text
The docs should be maintained actively and kept up to date.
```

Good:

```text
`MASTER_REVIEW.md` owns the current evidence ranking. When a submission result is
accepted or rejected, update that ranking and add a dated entry to
`NEXT_SUBMISSION_REVIEW.md`. The README only changes if the public status changes.
```

Bad:

```text
Maybe generate all docs from a database.
```

Good:

```text
Use structured experiment metadata for repeated result tables. Keep narrative
interpretation authored. Render public summaries from the metadata only when
manual duplication has already caused drift.
```

