# Recurring AI failure modes

This file names the recurring problems, why they are bad, and the replacement
behavior.

## 1. Instruction leakage

Problem:
The AI repeats the user's instructions inside the artifact instead of following
them.

Bad:

```text
This page is public, so private data has been removed and raw logs are not shown.
```

Better:

```text
The combat simulator now runs headless balance passes across the current roster.
```

Rule:
If the instruction is a constraint, obey it silently. Only mention the constraint
in private checklists, audit notes, or explicit release-readiness documents.

## 2. Privacy theater

Problem:
The AI writes public privacy disclaimers that make the document feel like a
sanitization report.

Bad:

```text
Public boundary: this page contains only sanitized visuals and no private logs.
```

Better:

```text
This page shows the current menu flow, early combat clips, and design notes for
the prototype.
```

Rule:
Public pages should read like normal public pages. They can have a license or
asset note where appropriate, but they should not explain the hidden cleanup
process.

## 3. Meta-writing

Problem:
The AI writes sentences that explain the document's purpose instead of giving the
reader useful content.

Bad:

```text
This document records the current state of the pipeline and aims to provide an
overview for future readers.
```

Better:

```text
The pipeline currently covers party setup, room routing, shop flow, base trainer
battles, and 1v1/2v2 combat.
```

Rule:
Replace "this document..." sentences with the actual fact the sentence was
stalling before.

## 4. Distant third-person process voice

Problem:
The AI turns personal project work into detached narration about "the author" or
"the project owner."

Bad:

```text
The developer has been exploring how AI can support the workflow while maintaining
quality.
```

Better for showcase:

```text
I use AI for fast prototyping, then keep or replace the result based on whether it
fits the game.
```

Better for technical docs:

```text
AI-assisted prototypes are reviewed against coherence, readability, and test
coverage before being kept.
```

Rule:
Use first person when the public page is a solo devlog and it sounds natural. Use
impersonal technical language for research repos. Do not use awkward third-person
distance to sound "professional."

## 5. AI apology spiral

Problem:
The AI treats AI use as a confession and keeps returning to it.

Bad:

```text
Some art is AI-generated, but care was taken to avoid slop and maintain quality.
This is a transparent AI-assisted prototype, and future work may replace the AI
assets.
```

Better:

```text
AI speeds up art and code prototyping here. The standard is still whether the
result fits the game, reads clearly, and improves the build.
```

Rule:
State AI use plainly once when relevant. Then talk about the work.

## 6. Over-caveating and fake humility

Problem:
The AI uses caveats as a self-protective fog.

Bad:

```text
To be honest, this is only a preliminary and imperfect exploration, and it is
important to note that the results should not be overinterpreted.
```

Better:

```text
Limitations: one dataset, one split, no frozen holdout.
```

Rule:
Put limits in a `Limitations` or `Caveats` section. Be direct. Do not apologize
for the existence of uncertainty.

## 7. Sales voice

Problem:
The AI tries to impress instead of report.

Bad:

```text
This powerful and elegant system unlocks a genuinely exciting new workflow.
```

Better:

```text
The system routes one source note into a daily journal, a project branch, and a
task list without duplicating the original.
```

Rule:
Let the facts carry the weight.

## 8. Bullet-stack bloat

Problem:
The AI responds with ten nested lists, each with examples, even when the user
asked for a focused output.

Bad pattern:

```text
Overview
- Point
  - Subpoint
    - Example
      - Further note
```

Better:
Use short sections and direct paragraphs. Use bullets only when they make the
artifact easier to scan.

Rule:
Structure is for navigation, not for making the answer look comprehensive.

## 9. "As an AI" self-reference

Problem:
The AI announces its limitations or identity when it should just answer or act.

Bad:

```text
As an AI language model, I do not have personal preferences...
```

Better:

```text
The answer depends on the audience and the artifact type.
```

Rule:
Do not foreground the assistant. The artifact is about the user's work.

## 10. Generic safety boilerplate

Problem:
The AI pastes generic warnings instead of making the practical change.

Bad:

```text
Be careful not to include copyrighted or sensitive material.
```

Better:

```text
Replace the Pokemon placeholder sounds before posting the clip. Hold any image
whose source art is not cleared.
```

Rule:
Name the practical gate. Do not pad it with boilerplate.

## 11. "What to ask next" endings

Problem:
The AI ends with suggested prompts or tries to steer the conversation when the
user only wanted the task handled.

Bad:

```text
Next, you could ask me to turn this into a polished public page.
```

Better:

```text
The draft is ready for review.
```

Rule:
Only suggest future prompts when asked for future prompts.

## 12. Voice costume instead of voice evidence

Problem:
The AI tries to mimic a person or project through a prose description rather than
through actual examples, constraints, and habits.

Bad:

```text
Write in a witty, chaotic, streamer-like voice.
```

Better:

```text
Use the provided exemplar lines as the primary voice source. Match rhythm,
message length, casing, punctuation, and recurring phrases. Do not invent a
generic personality.
```

Rule:
For persona work, examples carry voice. Descriptions only constrain edge cases.

## 13. Public docs that expose the workshop

Problem:
The AI includes handoff language, model names, draft scaffolds, source paths, or
private planning notes in public docs.

Bad:

```text
This came from the Codex scaffold and should be safe after sanitization.
```

Better:

```text
The public README links to the verified findings, reproducible runners, and test
commands.
```

Rule:
Public docs show the finished public shape. Private docs hold the workshop.

## 14. Turning every artifact into a research report

Problem:
The AI applies the same impersonal tone to everything.

Bad for showcase:

```text
The system demonstrates a combat-loop implementation with current limitations.
```

Better for showcase:

```text
Combat is finally readable enough to show in motion, though impact and pacing are
still rough.
```

Rule:
Tone depends on use case. Research docs are records. Devlogs can sound like a
person making something.

## 15. Turning every artifact into a devlog

Problem:
The AI uses first-person personal voice in technical reports where the repo wants
impersonal documentation.

Bad for research:

```text
I wanted to see if the method was actually robust, so I tried a heavier run.
```

Better for research:

```text
The heavier run tests whether the selected event family survives a larger
candidate set and stricter validation.
```

Rule:
Research and experiment docs should be standalone records, not conversation.

