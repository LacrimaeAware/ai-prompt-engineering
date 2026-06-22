# Roadmap

This repo is now organized around `docs/`, `tools/`, `dropoff/`, and
`private_docs/`. It should become more useful by accumulating examples,
task-specific packs, rewrite tests, and maintenance automation.

## Phase 1: Seed library

Status: done in this pass.

Contents:

- core directives
- recurring failure modes
- use-case tone map
- public/private boundary rules
- showcase/devlog/game-doc rules
- research/technical-doc rules
- code-comment and commit rules
- journal/archive rules
- prompt templates
- public audit-method note

## Phase 2: Example bank

Status: started with `examples/bad-good-examples.md`.

Expand the example bank with:

- bad public-boundary paragraph -> normal public rewrite
- bad AI-disclaimer paragraph -> plain AI-use note
- raw planning scratch -> devlog entry
- living bible excerpt -> public game-bible excerpt
- technical result ramble -> experiment note
- noisy journal transcript -> structured private note
- bad code comments -> maintainer comments

Keep raw private examples in `private_docs/examples/`, which should stay ignored.
Public-safe examples can go in `examples/`.

## Phase 3: Repo-specific packs

Create short files for common repo families:

- `packs/game-showcase.md`
- `packs/research-repo.md`
- `packs/kaggle-writeup.md`
- `packs/master-organizer.md`
- `packs/chat-archive-bot.md`
- `packs/godot-code.md`

Each pack should name the files to include, the tone, and the release gates.
Keep the repo-specific source notes that feed these packs in `private_docs/`.
The public pack should contain reusable rules, not local source maps.

## Phase 4: Lint checklist

Create a checklist or script that flags phrases like:

- public boundary
- safe to publish
- sanitized
- this document records
- the goal is to
- as an AI
- it is important to note
- to be honest
- great question
- powerful
- elegant
- exciting
- genuinely
- Co-Authored-By

The script should report likely issues, not auto-rewrite them.

Also consider research-methodology lint checks:

- single-result conclusion without counterevidence
- local benchmark win treated as target-metric proof
- stale plan referenced without a freshness label
- document claims duplicated across multiple owners
- result table copied manually in several docs
- submission decision missing accepted/rejected status

## Phase 5: Codex skill

Turn this folder into a local Codex skill if it becomes stable.

Possible skill trigger:

Use when writing, rewriting, auditing, or publishing user-facing docs where the
main risk is AI-sounding tone, meta-reference, public/private boundary leakage,
or mismatch between research-report and devlog voice.

## Phase 6: Review queue tool

Status: prototype working.

Build a small human-in-the-loop review tool from
`docs/instructions/12-human-in-loop-label-review.md`.

Implemented:

- read JSONL question items
- present one question at a time
- allow listed choices, a free-answer note box, parking, and direct navigation
- save answers back to JSONL
- write Markdown exports to ignored dropoff files
- combine multiple private queues into one review view
- filter by all, pending, answered, and parked
- accept messy notes and preserve them separately from normalized labels

Still useful later:

- add better tests around navigation and export behavior

Public-safe demo queue:

- `tools/review_queue/samples/demo_queue.jsonl`

## Phase 6b: Review queue v2 result flow

Status: next system upgrade.

The prototype proved the keyboard/card workflow, but future producer repos
should not depend on a manual final export step.

Target behavior:

- accept queue folders from ignored intake locations
- read one JSONL queue file per review batch
- write one result artifact after every answer
- resume cleanly after crashes or browser refreshes
- support hundreds of items with keyboard-first review
- make `skip`, `park`, and `can't tell` first-class labels
- let producer repos poll result folders and consume completed answers

Keep source-specific queue names, raw examples, and evidence payloads out of
public docs.

## Phase 7: Return-state and release hygiene

Status: active.

Keep the repo easy to resume after breaks:

- maintain one public-safe state document at the repo root
- keep private source exports in ignored folders
- update the README when new tool surfaces or core docs are added
- rerun privacy scans before committing public docs
- note whether a remote is configured before promising that changes were pushed
- run `docs/maintenance/freshness-check.md` before larger pushes

## Phase 8: Maintenance automation

Status: active weekly audit.

The automation should periodically:

- pull latest public main when safe
- run the freshness checklist
- verify the review queue server compiles
- scan public docs for privacy and stale-path issues
- update state/roadmap docs if the repo drifted
- refresh the dated handoff even when no tracked repo behavior changed
- commit and push only public-safe changes
