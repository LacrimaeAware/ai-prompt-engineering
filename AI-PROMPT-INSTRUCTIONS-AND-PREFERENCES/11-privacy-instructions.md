# Privacy Instructions

This file turns privacy into prompt behavior.

## Main rule

Do the privacy work. Do not narrate the privacy work in the public artifact.

Bad:

```text
This public page has been sanitized and contains no private logs, real
usernames, or internal instructions.
```

Good:

```text
The page shows the current build, the visible systems, and the next player-facing
work.
```

## Prompt rule

Use this instruction when asking an AI to prepare public material:

```text
Prepare this as a public artifact.

Privacy rules:
- Remove private data, raw logs, real usernames, private quotes, local paths,
  secrets, handoff notes, prompt text, and source-specific internal context.
- Do not mention that those things were removed.
- Replace private context with the public project fact it supported.
- If an unsafe asset or claim cannot be made public, omit it or mark it for
  private review outside the public artifact.
- The output should read like normal public material, not a privacy audit.
```

## Public artifact rule

Public artifacts may include:

- project facts
- public screenshots or clips
- cleaned design decisions
- reproducible commands
- selected metrics
- limitations that matter to the reader
- license or asset notes when relevant

Public artifacts should not include:

- private logs
- real usernames without consent or public context
- private quotes
- channel rosters
- local paths
- tokens or config secrets
- handoff notes
- model-to-model planning notes
- prompt text
- raw source excerpts copied from private research
- "safe to publish" language

## Private audit rule

Private audits are allowed to discuss privacy directly.

Use a private audit when the task is:

- checking whether a repo can become public
- finding local paths or secrets
- reviewing copied source text
- deciding whether logs or screenshots can ship
- triaging raw handoffs from another model
- identifying source-specific release blockers

Private audit language should not be pasted into the public artifact.

## Dropoff rule

Other-model handoffs go in `dropoff/`.

After a handoff is processed:

1. Extract the reusable rule, schema, example, or tool spec.
2. Add the durable version to the public instruction library.
3. Move source-specific remnants to `private_docs/`.
4. Do not leave raw handoffs at repo root.

## Private docs rule

Use `private_docs/` for:

- source maps naming local repos
- raw handoff files
- private examples
- local paths
- repo-specific context
- personal or sensitive details
- notes that should inform prompt rules but not be public

The public library should stand without this folder.

## Asset and copyright rule

For public pages, handle unsafe assets directly:

- replace copyrighted placeholder sounds
- replace copyrighted source art
- rename protected-series labels
- hold clips or screenshots that cannot be cleaned

Do not turn those operations into a public paragraph unless the page is an
asset/license note.

## Example rewrite

Bad:

```text
Public boundary: this showcase only includes code, docs, and sanitized visuals.
No raw logs, real quotes, channel rosters, local configs, or API secrets are
included.
```

Good:

```text
This showcase covers the current combat loop, route flow, prototype creature
art, and the systems that are stable enough to explain publicly.
```

## Final check

Before publishing, ask:

- Does the artifact contain private data?
- Does it mention private data instead of simply omitting it?
- Does it expose prompt context or handoff language?
- Does a stranger have enough public context to understand it?
- Does any safety note belong in a private audit instead?
