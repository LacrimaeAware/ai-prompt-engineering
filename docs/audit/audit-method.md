# Audit Method

This file describes the public-safe method used to build the instruction
library. Source-specific repo names, local paths, raw handoffs, and private
examples belong in `private_docs/`.

## Scope

The audit looked across local documents for recurring patterns in:

- AI-sounding prose
- meta-reference
- public/private boundary mistakes
- research-methodology failures
- documentation drift
- code-comment habits
- journal cleanup preferences
- persona and voice work

The goal was not to preserve a raw archive. The goal was to distill reusable
instructions, examples, and tool specs.

## Process

1. Inventory document-like files.
2. Search for high-signal terms around tone, privacy, public release, AI use,
   research claims, documentation conventions, code comments, and handoffs.
3. Read the high-signal matches closely.
4. Convert repeated problems into public rules.
5. Move source-specific evidence and raw handoffs into ignored private folders.
6. Keep public examples generic enough to reuse without exposing private source
   context.

## Main Findings

1. The strongest recurring writing problem is instruction leakage: the model
   repeats the constraint instead of obeying it.
2. There is no single desired tone. Research docs, devlogs, code comments,
   journals, and persona tools need different voices.
3. Privacy work should usually be operational and silent in public artifacts.
4. AI use can be stated plainly, but it should not become the subject of every
   page.
5. Research mistakes are often methodological, not tonal: one result gets treated
   as a verdict before transfer, isolation, and counterevidence are checked.
6. Living docs need ownership, freshness labels, and dependency rules to avoid
   competing sources of truth.

## Public vs Private Audit Material

Public:

- distilled rules
- bad/good examples
- generic schemas
- reusable prompt templates
- public-safe tool specs

Private:

- source maps naming local repositories
- raw handoffs from other models
- personal examples
- local paths
- repo-specific source excerpts
- private implementation notes
