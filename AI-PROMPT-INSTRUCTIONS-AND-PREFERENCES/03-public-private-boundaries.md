# Public and private boundaries

This file is for making public artifacts without leaking the workshop.

## The rule

Private work can be messy. Public work should be normal.

Private docs may contain:

- raw notes
- prompt drafts
- handoff notes
- model-to-model scaffold suggestions
- local paths
- real usernames
- channel names
- raw logs
- copied source text for private research
- copyright-risk placeholders
- uncertain names or spoilers
- unresolved worries

Public docs should contain:

- project facts
- cleaned design decisions
- screenshots or clips that are safe to show
- reproducible commands
- selected results
- caveats that matter to readers
- links to public sources

## Do not publish

Hold, remove, or rewrite anything with:

- tokens, API keys, OAuth secrets, `.env` contents, or config secrets
- raw logs
- real usernames when consent or public context is not clear
- private quotes
- channel rosters
- local Windows paths
- database files
- handoff notes containing personal context
- private archives
- prompt transcripts
- raw model outputs that include personal context
- copied paper text or full source snapshots unless redistribution is cleared
- copyrighted placeholder sounds
- copyrighted background art or source art
- trademarked names used as in-world labels
- protected-series terms that make the project look derivative rather than inspired

## Public pages should not say

Avoid these phrases in public-facing pages:

- public boundary
- safe to publish
- sanitized
- no private data
- private archive
- internal instructions
- prompt context
- raw logs removed
- secrets removed
- this page is public
- this document records the sanitized version

Those phrases belong in private audits, not in the public page.

## Correct handling by artifact type

Public README:
Show what the project is, what works, and what is still rough. Do not mention the
private material behind it.

Public devlog:
Tell the story of one visible change or decision. Do not include raw planning
scratch or private user/channel details.

Public asset note:
This is the place to mention licenses, placeholders, asset provenance, or
replacement status. Keep it practical.

Private readiness audit:
This is the place to say what was removed, what must stay private, and what is
blocked before release.

## AI use

AI use is not a secret, but it should not swallow the page.

Good:

```text
AI speeds up prototyping for art, code, and tests. The kept work still has to fit
the game's tone, read clearly, and improve the build.
```

Bad:

```text
This AI-assisted project has been carefully sanitized and reviewed to avoid AI
slop, copyright risk, and private-data exposure.
```

Rule:
For public pages, make AI use a project fact. Do not make it the protagonist.

## Idea stealing

Most public documentation risk is not idea theft. The larger risks are:

- revealing private or embarrassing source material
- shipping copyrighted placeholders
- looking derivative because protected names or assets remain
- making the work look like an AI transcript instead of a real project

Reasonable showcase posture:

- Share enough to show the project is real.
- Keep spoilers, raw rosters, and unstable lore private until ready.
- Share decisions and tradeoffs at the level of player experience.
- Avoid publishing raw design dumps that do not yet represent the game.

## Release checklist

Before posting a page, clip, screenshot, or repo:

1. Check for raw logs, real usernames, channel names, private quotes, local paths,
   tokens, databases, and handoff notes.
2. Check media for copyrighted placeholder sounds or source art.
3. Check names for protected-series terms used as in-world labels.
4. Check AI/prototype art for coherence. If it represents the project badly, hold
   it or label it as early exploration in a small way.
5. Remove "public boundary" language from the public artifact.
6. Read the artifact as a stranger. It should make sense with no private context.

