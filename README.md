# AI Prompt Engineering

A public-facing library of prompt instructions, failure modes, rewrite examples,
and tool specs for making AI-assisted work less generic, less leaky, and more
methodologically disciplined.

Start here:

- [CURRENT_STATE.md](CURRENT_STATE.md)
- [docs/README.md](docs/README.md)
- [docs/instructions/00-core-directives.md](docs/instructions/00-core-directives.md)
- [docs/examples/bad-good-examples.md](docs/examples/bad-good-examples.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)

Project layout:

- `docs/`: public instruction library, roadmap, examples, audits, and
  maintenance notes.
- `tools/`: local tools that support the instruction library.
- `dropoff/`: ignored intake/output area for raw handoffs and review exports.
- `private_docs/`: ignored source-specific notes and review queues.

Local tools:

- [tools/review_queue/README.md](tools/review_queue/README.md) for a private,
  keyboard-driven review queue used to classify handoff questions and export
  concise answer summaries.

Local handoffs and source-specific notes belong in `dropoff/` or
`private_docs/`. Those folders are ignored except for their README files.

The current re-entry handoff is in [CURRENT_STATE.md](CURRENT_STATE.md).
