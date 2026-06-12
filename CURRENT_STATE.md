# Current State

Date: 2026-06-12

This repo is a public-facing prompt engineering library. Its job is to capture
the recurring AI failure modes, tone preferences, privacy rules, review
workflows, and reusable prompt blocks that should guide future AI-assisted work.

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

The newest docs added in this pass are:

- `11-privacy-instructions.md`
- `12-human-in-loop-label-review.md`
- `13-review-question-writing.md`
- `audit/audit-method.md`

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

The current interaction model:

- `1` through `9`: choose visible answer options.
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

Current private queue status at handoff:

- Total review items: 22
- Answered: 22
- Pending: 0
- Parked: 0

The latest private export is intentionally ignored by git:

```text
dropoff/review_exports/latest_all_review_queues.md
```

That export contains source-specific answers and should be consumed only by the
matching source repos or chats. Do not publish it as part of this prompt
engineering repo.

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
2. `AI-PROMPT-INSTRUCTIONS-AND-PREFERENCES/README.md`
3. `CURRENT_STATE.md`
4. `AI-PROMPT-INSTRUCTIONS-AND-PREFERENCES/12-human-in-loop-label-review.md`
5. `AI-PROMPT-INSTRUCTIONS-AND-PREFERENCES/13-review-question-writing.md`

If resuming private source work, read the ignored export:

```text
dropoff/review_exports/latest_all_review_queues.md
```

Only use the entries relevant to the repo currently being worked on. Do not
copy unrelated repo details across project boundaries.

## Next Work

Highest-value next steps:

1. Add reusable repo-family prompt packs under `AI-PROMPT-INSTRUCTIONS-AND-PREFERENCES/packs/`.
2. Build a lint checklist or script for AI-tone and privacy failure phrases.
3. Convert this folder into a local Codex skill once the rules stabilize.
4. Improve the review queue import/export loop so producer repos can consume
   answered queues more directly.
5. Add a small public-safe sample queue so the review tool can be demonstrated
   without exposing private material.
6. Decide whether this repo needs a GitHub Pages site or whether the README is
   enough for now.

## Git And Publish Notes

If a checkout has no remote, configure `origin` before pushing.

For a public push, make sure the pushed history does not include deleted private
handoffs, source maps, or review exports. Deleting a file from the current tree
is not enough if the old commit history still contains it.
