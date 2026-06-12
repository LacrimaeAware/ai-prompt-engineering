# Review Queue Prototype

Local human-in-the-loop review app for JSONL question queues.

Run:

```powershell
python tools/review_queue/server.py
```

Then open:

```text
http://127.0.0.1:8991
```

The app reads ignored local queues from:

```text
private_docs/review_queues/
```

Controls:

- `1` through `9`: choose visible options.
- `A`: previous card.
- `S`: park this card and move next.
- `D`: next card.
- Type in `Your answer / notes` freely. It autosaves after each short pause.
- Pressing `D`/Next with typed text marks that text as the answer.
- Pressing `D`/Next with no text parks the card for later.
- Click `All`, `Pending`, `Answered`, or `Parked` to filter the visible stack.
- Use the question dropdown to jump directly to a card in the current filter.
- Click buttons when there are many options or when a mouse is easier.
- Switching queues saves the current note first.
- `All review queues` shows every queue together while still saving answers back
  to the original JSONL file.

Use `Send everything so far` to write Markdown to:

```text
dropoff/review_exports/
```

The export is also shown on the page and copied to the clipboard when the
browser allows it.
