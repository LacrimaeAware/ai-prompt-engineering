# Human-in-the-loop label review

This is a generic tool spec for AI-assisted review queues.

The purpose is to let producer projects ask the user small classification
questions, preserve messy answers, and write the answers back in a consistent
format that the producer can consume.

## Use cases

- classify project ideas from messy docs
- confirm whether two records refer to the same entity
- review ambiguous extracted claims
- triage public/private document status
- label research findings as accepted, rejected, uncertain, or stale
- resolve conflicts between old notes and current plans
- build small user-reviewed datasets for later automation

## Product shape

Start simple:

- JSONL input
- one question per item
- CLI or local-only page
- answers written back to JSONL
- no external service required

The clever part is the queue and answer model, not the UI.

The preferred v2 shape is folder-based:

```text
dropoff/<queue-name>/queue.jsonl
dropoff/<queue-name>/results/
```

The tool reads unanswered items from `queue.jsonl` and writes a result artifact
after every answer. There should not be a required "done" step before producer
repos can consume progress.

## Required behavior

Every question must offer:

- the listed choices
- one free-answer note box for messy or non-listed answers
- `Skip`
- `Ask later`

In a fast review UI, `Skip` and `Ask later` may be the same parked state. If
the reviewer leaves a card without a final answer, preserve the note and mark
the item for later instead of treating it as untouched.

The tool must preserve:

- normalized answer
- messy answer text
- refusal or skip state
- timestamp
- reviewer id or mode
- source item id

Skipped or refused items stay in the queue and can be asked later with different
wording or a conversational free-answer mode.

## Minimal JSONL schema

One item per line:

```json
{
  "id": "example-0001",
  "source_project": "example-project",
  "kind": "classification",
  "question": "Which status best describes this extracted idea?",
  "subject": {
    "title": "Route telegraph icons",
    "summary": "Routes should reveal risk and reward before commitment."
  },
  "context": [
    "The current docs mention route risk icons as planned.",
    "The unresolved decision is what the player can preview before committing."
  ],
  "options": ["live", "planned", "parked", "discarded", "needs clarification"],
  "allow_other": true,
  "answer": null,
  "answer_note": null,
  "answer_status": "pending",
  "answered_at": null,
  "reviewer": null
}
```

## Answer fields

Use:

- `answer`: one normalized option or free text from the note box
- `answer_note`: messy elaboration or rationale
- `answer_status`: `pending`, `answered`, `skipped`, `ask_later`, `refused`
- `answered_at`: ISO timestamp
- `reviewer`: human, model, or workflow id

Do not overwrite messy notes when normalizing the answer.

## Producer contract

Producer projects should:

1. Emit JSONL items in the shared schema.
2. Write concrete questions using `13-review-question-writing.md`.
3. Avoid copying raw private logs into the item.
4. Re-read the answered JSONL after review.
5. Treat free-answer notes, `Skip`, and `Ask later` as real outcomes.
6. Preserve stable IDs across wording changes.
7. Prefer incremental result folders when queues may contain many items.

## Result flow

For small local queues, updating the JSONL file in place is acceptable.

For larger queues, prefer append-only or per-item result files:

```text
dropoff/<queue-name>/results/<item-id>.json
```

Each result should include:

- queue name
- item id
- answer
- answer note
- answer status
- answered timestamp
- reviewer mode

This makes the review loop resilient. Browser refreshes, crashes, or stopping
mid-session should not lose completed labels or require a manual export before
another repo can continue.

## Reviewer UX

Each question should show:

- title or subject
- why the item is being asked
- short context
- current model guess, if any
- choices
- a free-answer note box
- `Skip`
- `Ask later`

The UI should not force a false binary. Ambiguity is a valid result.

For keyboard-heavy review, prefer:

- `A`: previous item
- `S`: park current item
- `D`: next item
- `1` through `9`: choose visible answer options

Do not map `A` to ask-later when the reviewer is moving through a card stack.
If the reviewer typed a free answer and presses `D`/Next, treat the typed text
as the answer. If they press `D`/Next on a blank unanswered item, park it for
later.

## Messy answer mode

For skipped or unclear items, the tool can later ask:

```text
What should happen with this item? Answer however you want.
```

Then an AI or parser can convert the messy answer into:

- normalized label
- rationale
- uncertainty
- follow-up question

The raw answer stays in `answer_note`.

## Public/private handling

This tool may process private source material, but public outputs should use
clean summaries.

Rules:

- Do not publish raw review queues by default.
- Keep source excerpts short.
- Prefer source refs and paraphrases over copied private text.
- Mark items with `public_surface` only when they are safe to reuse.
- Keep handoff files and raw queues in ignored folders unless deliberately
  publishing a clean sample.

## Optional fields

Useful later:

```json
{
  "model_guess": "planned",
  "model_confidence": 0.72,
  "needs_user_answer": true,
  "priority": 2,
  "domain": "routes",
  "public_surface": "devlog",
  "freshness": "current",
  "source_rank": "current-doc",
  "conflicts": [
    "Older roadmap says parked; current design note says planned."
  ],
  "next_review_after": "2026-06-20"
}
```

## First implementation

Build the smallest useful version:

1. Read a JSONL file.
2. Select the first `pending` or due `ask_later` item.
3. Print question, subject, context, and choices.
4. Accept one of the choices, a typed free answer, `Skip`, or `Ask later`.
5. Save a new JSONL file or update in place after a backup.
6. Repeat until the user exits.

Avoid building a large app before the schema and review loop feel right.

After the loop feels right, improve the result flow before adding fancy UI:

1. Read queue folders from ignored dropoff paths.
2. Save one result file after every answer.
3. Resume by merging queue items with existing results.
4. Keep manual Markdown export as a convenience, not the only handoff path.
