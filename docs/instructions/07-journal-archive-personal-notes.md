# Journals, archives, and personal notes

This file is for journal cleanup, ChatGPT export organization, personal archive
work, Obsidian vault notes, and source-to-canonical transforms.

## Core principle

Keep originals. Make the usable version concise, searchable, and source-traceable
without erasing unrecoverable facts.

## Desired output

A cleaned note should:

- preserve concrete events
- preserve decisions
- preserve original ideas
- preserve project facts
- preserve names only when the destination is private
- separate repeated emotional noise from unique information
- use categories and headers
- avoid one giant bullet list
- link or point back to the source
- keep enough detail that future self can reconstruct why it mattered

## What not to do

Do not insert assistant personality.

Avoid:

- motivational commentary
- diagnosis
- "the speaker is processing..."
- "the user is struggling..."
- broad psych summaries as a replacement for facts
- moralizing
- advice unless explicitly requested
- removing details because they are messy

## First person and third person

For private journal cleanup, first-person source voice can remain when it is part
of the value of the note.

Do not convert everything into distant third person unless the requested format
requires it.

Bad:

```text
The speaker is reflecting on stress, productivity, and personal growth.
```

Better:

```text
Main thread: stress is high, but the concrete plan is to limit distractions,
prioritize math work, and avoid impulsive routine changes.
```

## Fluff handling

Some source text is thinking out loud. Do not preserve every loop at equal weight.

Keep:

- concrete facts
- decisions
- tasks
- dates
- people and places when private
- emotional state when it changes interpretation
- original project ideas
- health or routine changes when relevant
- uncertainty that affects decisions

Compress:

- repeated "I don't know" loops
- repeated anxiety without new facts
- repeated caveats
- repeated context already captured

Do not mock, pathologize, or narrate the compression.

## Knowledge-vault routing

One source can update multiple places.

Examples:

- daily journal
- project journal
- game-dev idea bank
- task list
- health/routine log
- class notes
- research branch
- relationship or life-arc summary

The destination should control detail level. A private daily note can preserve
more raw specificity. A public project page should only contain public facts.

## Retention audit

After summarizing a messy source, ask:

- What facts would be impossible to recover if the original disappeared?
- What task or decision changed?
- What project idea appeared?
- What named entity matters later?
- What is repeated noise rather than new information?
- Does the cleaned note preserve enough source anchors?

## Prompt for journal cleanup

Use this when the task is personal archive work:

```text
Clean and organize this source into a private note.

Rules:
- Preserve unrecoverable facts, decisions, names, dates, project ideas, and tasks.
- Use headers and grouped bullets, not one long list.
- Keep the speaker's meaning. Do not insert assistant personality.
- Do not diagnose, moralize, reassure, or coach.
- Compress repeated loops when they add no new fact.
- Keep source traceability.
- Add a short "Tasks / follow-up" section only for explicit tasks or decisions.
```
