# AI prompt instructions and preferences

This folder is a reusable instruction library for AI-assisted writing, coding,
documentation, and public showcase work.

The central rule:

> Do the requested work. Do not perform the instructions out loud inside the
> artifact.

If a page must avoid private data, keep the private data out. Do not write a
public paragraph about keeping private data out. If a public game page must avoid
copyrighted placeholders, remove or replace them. Do not turn the page into an
audit memo. If the task gives style rules, follow them in the output. Do not
describe the style rules unless the artifact itself is an instruction document.

## How to use this folder

For most future AI work, paste or attach only the files that match the task:

- `00-core-directives.md`: the rules that apply almost everywhere.
- `01-failure-modes.md`: the recurring problems and what to do instead.
- `02-use-cases.md`: which tone to use for each document type.
- `03-public-private-boundaries.md`: privacy, public release, and safety handling.
- `04-showcase-devlog-game-docs.md`: game showcase, devlog, game bible, and
  pipeline notes.
- `05-research-technical-docs.md`: research repos, experiment notes, READMEs, and
  technical reports.
- `06-code-comments-and-commits.md`: code comments, implementation notes, and
  commit messages.
- `07-journal-archive-personal-notes.md`: journal cleanup, archives, personal
  notes, and knowledge-vault work.
- `08-prompt-templates.md`: copy-paste prompt blocks for common tasks.
- `09-research-methodology-failure-modes.md`: single-result overreaction,
  flip-flop handling, validation discipline, and evidence ladders.
- `10-documentation-maintenance.md`: living-doc ownership, freshness labels,
  dependency blocks, and when structured data should render docs.
- `11-privacy-instructions.md`: public/private prompting, silent privacy
  handling, release gates, and dropoff/private-doc handling.
- `12-human-in-loop-label-review.md`: generic tool spec for review queues,
  label questions, messy answers, and producer/consumer schemas.
- `13-review-question-writing.md`: rules and examples for writing concrete,
  implementation-facing review questions instead of vague model summaries.
- `examples/bad-good-examples.md`: direct bad-to-good rewrite examples.
- `ROADMAP.md`: how this folder should grow.
- `audit/audit-method.md`: public-safe summary of how the rules were extracted.

## What this is not

This is not a public-facing style guide for any one project. Public repositories
should absorb these preferences quietly and ship normal project pages.

This is also not a raw archive of private complaints, chats, or logs. It is a
distilled operating manual built from recurring patterns across the local repos.
