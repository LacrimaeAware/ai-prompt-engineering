# Use cases and tone selection

The main mistake is using one voice for every artifact. Pick the lane first.

## Public showcase or devlog

Audience:
Someone curious about the project as a game, tool, or build journey.

Tone:
Human, specific, direct. First person is allowed if it sounds natural.

Do:

- Show what exists.
- Show what changed.
- Show what was learned.
- Show what still feels rough.
- Anchor claims in visible clips, screenshots, systems, or decisions.
- Mention AI use plainly if relevant, then move on.

Avoid:

- "Public boundary."
- "Sanitized."
- "Internal instructions."
- "This document records."
- Long defensive AI disclaimers.
- Audit language unless the page is actually an audit.

## Game bible or design bible excerpt

Audience:
Future self, collaborators, or public readers trying to understand the game.

Tone:
In-world enough to carry mood, but clear enough to guide implementation.

Do:

- Explain the fantasy, player experience, and mechanical role.
- Keep lore uncertain or spoiler-heavy material private until ready.
- Use show-don't-tell where tone matters.
- Keep protected inspirations as inspirations, not in-world labels.

Avoid:

- Meta commentary about prompts.
- "The AI generated this direction."
- Public explanations of what was removed.
- Overexplaining the document's purpose.

## Pipeline snapshot

Audience:
Someone trying to understand the current build state.

Tone:
Plain and practical. More devlog than audit.

Do:

- List current systems by status.
- Explain blockers in product terms.
- Include roughness honestly.
- Link to a checklist or roadmap when useful.

Avoid:

- Raw planning scratch.
- Private handoff notes.
- "Safe to publish" language.

## Research repo README

Audience:
Technical reader, future researcher, reviewer, or hiring reader.

Tone:
Impersonal technical report.

Do:

- State the question.
- Give the method.
- Put numbers first.
- Separate result from interpretation.
- Put caveats in the caveat section.
- Link to reproducible runners and tests.

Avoid:

- First-person narrative.
- Hype.
- Coaching language.
- "Honest" as a qualifier.
- Claims without metrics.

## Experiment note

Audience:
Future self and technical readers trying to reproduce one unit of work.

Tone:
Structured, factual, reproducible.

Shape:

1. Question.
2. Method.
3. Outputs.
4. Result.
5. Caveat.
6. Lesson.

Do:
Name computations, sample sizes, data split, generated artifacts, and exact
interpretation.

Avoid:
Turning the experiment into a diary entry.

## Public-readiness audit

Audience:
Private self before release.

Tone:
Direct, operational, possibly blunt.

This is one of the few places where it is correct to mention private material,
sanitization, raw logs, source snapshots, copied text, local paths, and release
blockers.

Do:

- Name the blocker.
- Name the fix.
- Name what can ship.
- Keep legal advice caveated.

Avoid:
Copying the audit language into the public artifact.

## Code comments

Audience:
Future maintainer reading code.

Tone:
Human maintenance note.

Do:

- Explain purpose when the code is not obvious.
- Explain invariants or non-obvious constraints.

Avoid:

- "Changed X to Y."
- "Per the user's request."
- "This was updated to..."
- Meta comments about prior discussion.

## Commit messages

Audience:
Repo history.

Tone:
Plain and specific.

Do:
State what changed and why.

Avoid:
Co-authored trailers unless the repo specifically wants them.

## Journal cleanup or archive canonicalization

Audience:
Future self.

Tone:
Preserve the speaker's meaning. Organize without inserting assistant personality.

Do:

- Keep originals.
- Preserve unrecoverable facts.
- Separate repeated emotional noise from concrete facts and decisions.
- Use categories and headers.
- Keep source traceability.

Avoid:

- Third-person psych summaries unless requested.
- Diagnosis.
- Motivational commentary.
- Removing details that cannot be recovered later.

## Persona and voice work

Audience:
Private tool or controlled output.

Tone:
Evidence-driven.

Do:

- Use exemplars as the primary voice source.
- Track message length, casing, punctuation, recurring words, emotes, and context.
- Keep real-user examples private unless permission exists.

Avoid:

- A generic prose personality sheet as the main voice source.
- Publishing raw quotes or identifiable scores without consent.

