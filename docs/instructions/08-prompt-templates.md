# Prompt templates

Copy only the block that matches the task. Add project-specific facts below it.

## Universal artifact cleanup

```text
Rewrite this artifact so it reads like the final public/internal document, not
like a response to instructions.

Rules:
- Follow constraints silently. Do not mention the constraints unless the artifact
  is explicitly an audit or instruction document.
- Remove prompt, chat, private archive, and internal-process references.
- Replace "this document..." framing with direct project facts.
- Keep claims proportional to evidence.
- Avoid hype, coaching language, and repeated caveats.
- No em dashes.
- Preserve the useful substance.
```

## Public showcase or devlog

```text
Turn this into a public-facing devlog/showcase entry.

Audience: someone curious about the project as a game/tool/build journey.

Rules:
- Sound like a solo maker documenting real progress.
- Say what changed, what exists now, what was learned, and what is still rough.
- Use first person only when it sounds natural.
- Do not mention prompts, internal instructions, private archives, sanitization,
  or "public boundary."
- Remove raw logs, real usernames, private quotes, local paths, tokens, and
  handoff notes.
- Replace or hold copyrighted placeholders and protected-series labels rather
  than explaining them in the post.
- Mention AI use at most once, plainly, only if relevant.
- No em dashes.
```

## Game bible excerpt

```text
Rewrite this as a clean game-bible excerpt.

Rules:
- Focus on player experience, fantasy, system role, and implementation-relevant
  invariants.
- Keep the tone evocative but not vague.
- Remove prompt/history/meta commentary.
- Remove spoilers, uncertain lore, private names, protected-series labels, and
  raw brainstorming unless explicitly marked private.
- Do not explain what was removed.
- No em dashes.
```

## Pipeline snapshot

```text
Create a pipeline snapshot from these notes.

Rules:
- Group by system area.
- For each area, state: working, in progress, planned, blocked, and current
  roughness.
- Use human wording, not raw planning scratch.
- Keep private process and prompt context out.
- Do not use "safe to publish" or "sanitized."
- No em dashes.
```

## Research or technical README

```text
Rewrite this as a technical README.

Rules:
- Use impersonal technical-report tone.
- Start with scope and current status.
- Put key results in a table with numbers first.
- Separate result, interpretation, and limitation.
- Link to reproducible commands, tests, and deeper docs.
- Remove private context, prior chats, prompt references, local paths, and raw
  scaffold notes.
- Avoid hype, coaching language, first-person diary voice, and "honest" as a
  qualifier.
- No em dashes.
```

## Experiment note

```text
Turn this into an experiment note with this structure:

# Experiment NN: short name

## Question
## Method
## Outputs
## Result
## Caveat
## Lesson

Rules:
- Name data, sample sizes, split, method, baseline, and generated artifacts.
- Put numbers before interpretation.
- State exactly what the experiment does and does not validate.
- Keep the tone factual and standalone.
- Remove private context and process chatter.
- No em dashes.
```

## Public-readiness audit

```text
Audit this repo/page for public release.

Rules:
- This is a private audit, so it may mention privacy, copyright, local paths,
  source snapshots, raw logs, and release blockers.
- Do not include raw secrets or raw private quotes in the audit output.
- Group findings as: blockers, review before release, safe to keep, suggested
  public shape, suggested private archive.
- Be operational: name the issue and the fix.
- This audit language must not be copied into the public artifact.
- No em dashes.
```

## Code changes

```text
Make the requested code change.

Rules:
- Match existing project patterns.
- Keep edits scoped.
- Comments inside code should explain purpose or non-obvious behavior only.
- Do not write comments that reference the prompt, prior discussion, or "as
  requested."
- For Godot/GDScript, avoid `:=` and ternary operators.
- Verify with the smallest useful test or command.
- Report changed files and verification plainly.
```

## Journal cleanup

```text
Clean and organize this into a private journal/archive note.

Rules:
- Preserve unrecoverable facts, dates, names, tasks, decisions, and project ideas.
- Use categories and headers, not one long list.
- Keep the speaker's meaning. Do not insert assistant personality.
- Do not diagnose, moralize, reassure, or coach.
- Compress repeated loops that add no new facts.
- Keep source traceability.
- Add tasks only when the source contains explicit tasks or decisions.
```

## No-meta rewrite pass

```text
Do a no-meta rewrite pass.

Remove:
- "this document records"
- "the goal is to"
- "safe to publish"
- "public boundary"
- "sanitized"
- "internal instructions"
- "prompt context"
- "as an AI"
- "it is important to note"
- "to be honest"
- repeated caveat blocks

Replace each with the direct fact, decision, result, limitation, or action.
```

