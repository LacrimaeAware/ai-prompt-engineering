# Code comments and commits

This file is for coding tasks, generated snippets, comments inside code blocks,
implementation notes, and git messages.

## Code comments

Code comments should read as if a human maintainer wrote them for the codebase.
They should describe purpose, invariants, or non-obvious mechanics.

## Do not use comments for conversation

Bad:

```python
print("four")  # Changed from three to four per the request
```

Better:

```python
print("four")  # Prints the selected value
```

Bad:

```gdscript
# Efficient and algorithmic approach requested by the user
for i in range(count):
    process_item(i)
```

Better:

```gdscript
# Process each item once in index order.
for i in range(count):
    process_item(i)
```

## No meta comments

Avoid comments that mention:

- the prompt
- the user
- the assistant
- previous discussion
- "we changed"
- "now this does"
- "as requested"
- "temporary fix from AI"

Use comments that mention:

- data shape
- invariant
- side effect
- reason a surprising branch exists
- performance constraint
- external API behavior

## Implementation responses

When reporting code work back to the user:

- Be concise.
- Mention files changed.
- Mention tests run.
- Mention anything not run.
- Avoid long self-analysis.
- Avoid "what to ask next" unless requested.

## Godot-specific preferences

For Godot/GDScript work:

- Avoid type inference with `:=`.
- Avoid ternary operators.
- Prefer explicit, readable control flow.
- Keep comments about game-system purpose, not chat history.

## Commit messages

Good:

```text
Add headless balance simulator
```

```text
Document public release blockers
```

```text
Update showcase clips and roadmap links
```

Bad:

```text
Apply requested changes
```

```text
Sanitize public boundary and follow privacy instructions
```

```text
AI-assisted cleanup
```

## Co-authored trailers

Default:
Do not add `Co-Authored-By` unless the repo explicitly asks for it.

Reason:
Several local repos forbid it, and deployed sites may reject unrecognized
contributors.

## Debug notes

Debug output should be useful to a maintainer:

Good:

```text
adapter=beeline dataset=dream4 seed=0 aupr=0.412
```

Bad:

```text
Trying the next thing because the last attempt was wrong
```

## Final code artifact check

Before finishing code:

1. Remove conversational comments.
2. Remove stale TODOs created only by the assistant.
3. Keep comments that explain non-obvious logic.
4. Run the smallest useful verification.
5. Report verification plainly.

