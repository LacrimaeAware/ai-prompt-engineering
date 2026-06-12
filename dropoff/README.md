# Dropoff

Other models can put temporary handoffs, raw proposals, and source-specific
notes here.

This folder is an intake area, not a public artifact. Its contents are ignored by
git except this README and `.gitkeep`.

Expected handoff shape:

```text
# Handoff: short title

## Source
Where this came from.

## Idea
The idea to absorb into the public instruction library or tool specs.

## Constraints
Privacy, publication, source, or implementation constraints.

## Suggested destination
Where the durable version probably belongs.

## Delete or archive after
What to do with this raw handoff after it has been cannibalized.
```

Durable lessons should be rewritten into the public docs. Source-specific
details, local paths, raw examples, and private project references should move to
`private_docs/`.
