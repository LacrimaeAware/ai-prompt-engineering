# Showcase, devlog, and game docs

This file is for public game pages, game bible excerpts, pipeline snapshots, and
development journey posts.

## Desired public feel

The public face should feel like a solo game maker documenting a real project.
It should not feel like:

- an audit memo
- a chat transcript
- a prompt compliance report
- a defensive AI disclosure
- a privacy checklist

## What public showcase can include

- A concise statement of what the game is.
- Short dated devlogs around one visible change or decision.
- Design notes rewritten from the living bible.
- Pipeline snapshots with current status and rough edges.
- Art/media notes about prototype evolution and style direction.
- Bible excerpts after spoilers, uncertain lore, and private naming notes are
  removed.
- Clips and screenshots that are safe to post.

## What public showcase should avoid

- Internal prompts.
- Handoff notes.
- Raw logs.
- Real usernames or channel context.
- Local paths.
- Protected-series names as in-world labels.
- Copyrighted placeholder sounds.
- Copyrighted art or background sources.
- Repeated AI disclaimers.
- "safe to publish" language.

## Devlog voice

Good devlog voice:

```text
Combat is finally readable enough to show in motion. The next pass is mostly
impact: hit timing, move spacing, and making 2v2 fights easier to parse.
```

Bad devlog voice:

```text
This public-facing update documents a sanitized combat milestone while avoiding
private pipeline details and placeholder assets.
```

Rule:
Say the game thing. Do not say the hidden process.

## AI use in a showcase

A good AI-use note is short, direct, and tied to quality control.

Example:

```text
AI helps me prototype art, code, and test ideas quickly. I still judge the kept
work by coherence, readability, and whether it makes the game feel better.
```

Do not repeat this on every page. Put it in the README or one process note, then
let the project speak.

## Game bible excerpts

Use bible excerpts when they add player-facing or design-facing clarity.

Good excerpts:

- world tone
- type identity
- combat identity
- creature identity profiles
- current system invariants
- player experience goals

Hold back:

- spoilers
- unresolved lore
- private names
- raw roster dumps
- protected-inspiration language
- notes that are still mostly argument with yourself

## World and tone notes

For a creature roguelike, auto-battler, or similarly systems-heavy game, the
useful tone reference is:

- mythic
- cyclical
- reflective
- PG-13 dark
- show-don't-tell
- not grim for its own sake
- strategic first, creature fantasy second, collection fantasy third

The public page should make the world feel larger and more coherent, not explain
the prompt history behind the world.

## Pipeline snapshots

Pipeline snapshots should answer:

- What works?
- What is in progress?
- What is planned?
- What is visibly rough?
- What changed since the last snapshot?
- What is the next player-facing improvement?

Avoid raw planning scratch. Avoid "everything possible someday" lists unless the
page is explicitly a roadmap.

## Art and media notes

Good:

```text
The backgrounds are still prototype art, but they are starting to give each route
a stronger sense of place. The next pass is consistency: lighting, scale, and
making sure combat readability comes before scenery.
```

Bad:

```text
Although the art uses AI and may be detected as AI-generated, the project is not
trying to hide AI use, and future work may replace assets that appear too AI.
```

Rule:
Frame art by what it does for the game. Discuss AI or copyright only where that
information helps the reader.

## Copyright and placeholder handling

For public media:

- Replace or mute Pokemon placeholder sounds.
- Replace copyrighted background art.
- Avoid protected names as in-world labels.
- Keep inspiration references in a separate "inspirations" sentence, not as the
  project's identity.

Do not write public prose about removing unsafe material unless it is an asset
license note.

## "Quality, not slop" checklist

Before posting, ask:

- Is the page about the project, not the prompt?
- Does each paragraph add a fact, decision, clip, or useful limitation?
- Does the AI-use note appear at most once?
- Does the writing sound like a person making a thing?
- Are rough edges stated plainly without apology?
- Are unsafe assets removed rather than explained?
- Could a stranger understand the page without knowing the private archive?
