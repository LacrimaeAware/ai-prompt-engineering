# Current State

Date: 2026-06-15

This repo is a public-facing prompt engineering library. Its job is to capture
the recurring AI failure modes, tone preferences, privacy rules, review
workflows, and reusable prompt blocks that should guide future AI-assisted work.

Treat `docs/README.md` and the linked docs tree as the durable public source of
truth. This file is the dated re-entry handoff for the latest verified repo
state.

The central rule remains:

> Do the requested work. Do not perform the instructions out loud inside the
> artifact.

## What We Were Doing

The recent work turned a loose collection of preferences into a structured
instruction library:

- Core directives and failure modes for avoiding AI-sounding artifacts.
- Use-case tone rules for public docs, research notes, code work, journals, and
  project archives.
- Public/private boundary rules that keep private material out of public output
  without narrating the privacy work.
- Research-methodology rules for avoiding single-result overreaction and
  flip-flopping conclusions without checking method quality.
- Documentation-maintenance rules for living docs, stale claims, ownership, and
  dependency between documents.
- Prompt templates that can be pasted into future chats.
- A local review queue tool for answering many small classification questions
  quickly.

Recent docs added or reorganized:

- `docs/instructions/11-privacy-instructions.md`
- `docs/instructions/12-human-in-loop-label-review.md`
- `docs/instructions/13-review-question-writing.md`
- `docs/audit/audit-method.md`
- `docs/maintenance/freshness-check.md`

The public documentation now lives under:

```text
docs/
```

Root files are limited to the README, license, and the current-state handoff.

Freshness audit verified on 2026-06-15:

- `git pull --ff-only`: already up to date on `main`
- ignored private folders still contain queues, exports, and handoffs
- `python -m py_compile tools/review_queue/server.py`: passed
- public-safe demo queue smoke test passed on `/api/queues` and `/api/items`

## Review Queue Tool

The review queue prototype lives in:

```text
tools/review_queue/
```

Run it with:

```powershell
python tools/review_queue/server.py
```

Then open:

```text
http://127.0.0.1:8991
```

The tool reads private ignored JSONL queues from:

```text
private_docs/review_queues/
```

It also has a public-safe demo queue:

```text
tools/review_queue/samples/demo_queue.jsonl
```

The current interaction model:

- `Q` through `O`, or configured option keys: choose visible answer options.
- `1` through `9`: fallback choice shortcuts.
- `A`: previous card.
- `S`: park the current card and move next.
- `D`: next card.
- If the note box has text and the user presses `D`/Next, that text becomes the
  answer.
- If the note box is blank and the user presses `D`/Next, the card is parked for
  later.
- `All`, `Pending`, `Answered`, and `Parked` filter the visible stack.
- The question dropdown jumps directly to a card in the current filter.
- `Send everything so far` writes a Markdown export into ignored dropoff files.

Current ignored private queue status at this freshness pass:

- Total review items: 127
- Answered: 89
- Pending: 35
- Parked: 3

Private exports are intentionally ignored by git:

```text
dropoff/review_exports/
```

Those exports contain source-specific answers and should be consumed only by the
matching source repos or chats. Do not publish them as part of this prompt
engineering repo. If the active queue changes, click `Send everything so far` in
the tool before expecting the latest export to reflect the current private
queue.

The next review-tool agenda is v2 result flow:

- accept producer queues from ignored queue folders
- save an incremental result after every answer
- avoid any required final export/copy step
- support hundreds of items without losing progress
- keep source-specific queue names and payloads private

## Public/Private State

This repo is intended to be public-safe.

Public tracked material should contain:

- reusable rules
- reusable examples
- generic schemas
- tool specs
- sanitized workflow descriptions

Ignored private areas contain raw or source-specific material:

```text
dropoff/
private_docs/
```

Raw handoffs and source maps were moved out of the public tree. The old public
source-map file and root handoff file should remain deleted unless they are
rewritten into public-safe summaries.

Before publishing or pushing, run a privacy scan for:

- local paths
- raw usernames or handles
- source repo names that should stay private
- private quotes or logs
- secrets, tokens, `.env` content, and config fragments
- handoff language in public-facing docs

## Where To Resume

Start by reading:

1. `README.md`
2. `docs/README.md`
3. `CURRENT_STATE.md`
4. `docs/instructions/12-human-in-loop-label-review.md`
5. `docs/instructions/13-review-question-writing.md`
6. `docs/maintenance/freshness-check.md`

If resuming private source work, open the review tool and read the ignored
export when it has been refreshed:

```text
dropoff/review_exports/latest_all_review_queues.md
```

Only use the entries relevant to the repo currently being worked on. Do not
copy unrelated repo details across project boundaries.

## Next Work

Highest-value next steps:

1. Add reusable repo-family prompt packs under `docs/packs/`.
2. Build a lint checklist or script for AI-tone and privacy failure phrases.
3. Convert this folder into a local Codex skill once the rules stabilize.
4. Improve the review queue result loop so producer repos can consume answered
   queues incrementally.
5. Decide whether this repo needs a GitHub Pages site or whether the README is
   enough for now.
6. Keep the weekly freshness automation active or update it when the repo's
   maintenance checklist changes.

Active automation:

- `ai-prompt-engineering-weekly-freshness-audit`
- runs a recurring docs freshness, privacy, review-tool, commit, and push check
- uses `docs/maintenance/freshness-check.md` as the durable checklist

## Git And Publish Notes

If a checkout has no remote, configure `origin` before pushing.

For a public push, make sure the pushed history does not include deleted private
handoffs, source maps, or review exports. Deleting a file from the current tree
is not enough if the old commit history still contains it.
