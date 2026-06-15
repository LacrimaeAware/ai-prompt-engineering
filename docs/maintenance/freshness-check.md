# Freshness Check

This is the repeatable maintenance pass for this repo.

Use it when returning from a break, before public pushes, or as the basis for a
recurring automation.

Active automation:

- `ai-prompt-engineering-weekly-freshness-audit`
- weekly documentation freshness and repo hygiene pass
- local checkout: this repository

## Goal

Keep the repo easy to resume, public-safe, and internally consistent.

The pass should answer:

- What changed since the last state update?
- Are README links and doc paths still correct?
- Are roadmap items current, stale, done, or blocked?
- Are raw handoffs and source-specific notes still ignored?
- Does the review queue tool still start and compile?
- Is there anything safe and useful to commit and push?

## Steps

1. Inspect git state.

```powershell
git status --short --branch --ignored
git remote -v
git log --oneline --decorate -5
```

2. Pull only if the working tree is clean or the local changes are understood.

```powershell
git pull --ff-only
```

3. Check the public documentation tree.

```powershell
rg --files docs README.md CURRENT_STATE.md tools
rg -n "AI-PROMPT-INSTRUCTIONS-AND-PREFERENCES|source-map|HANDOFF_FROM" README.md CURRENT_STATE.md docs tools
```

4. Check privacy boundaries.

```powershell
rg -n "[A-Za-z]:\\\\|\\.env|token|secret|API key|raw log|private quote" -g "!private_docs/**" -g "!dropoff/processed/**" -g "!dropoff/review_exports/**"
git check-ignore -v dropoff/review_exports/latest_all_review_queues.md private_docs/review_queues/*.jsonl
```

5. Verify the review queue tool.

```powershell
python -m py_compile tools/review_queue/server.py
$proc = Start-Process python -ArgumentList 'tools/review_queue/server.py --queue-dir tools/review_queue/samples --port 8992' -WorkingDirectory '.' -WindowStyle Hidden -PassThru
try {
  Start-Sleep -Seconds 2
  Invoke-RestMethod "http://127.0.0.1:8992/api/queues"
  Invoke-RestMethod "http://127.0.0.1:8992/api/items?queue=demo_queue.jsonl"
} finally {
  if ($proc -and !$proc.HasExited) { Stop-Process -Id $proc.Id }
}
```

For a manual UI check, run:

```powershell
python tools/review_queue/server.py
```

Then open:

```text
http://127.0.0.1:8991
```

If a server is already running, use:

```powershell
Invoke-RestMethod "http://127.0.0.1:8991/api/queues"
```

6. Refresh docs when needed.

Update:

- `CURRENT_STATE.md` for current status and next agenda
- `docs/README.md` for navigation changes
- `docs/ROADMAP.md` for done, next, blocked, or stale work
- `tools/review_queue/README.md` if tool behavior changed

Do not copy private queue payloads, raw handoffs, usernames, source maps, or
local paths into public docs.

7. Commit and push only after checks pass.

```powershell
git diff --check
python -m py_compile tools/review_queue/server.py
git status --short
git add -A
git diff --cached --check
git commit -m "Refresh documentation state"
git push
```

## Current Watch Items

- The review queue prototype works, but v2 should write per-answer results
  incrementally into ignored result folders so producer repos do not need a
  manual export step.
- Keep the public-safe demo queue aligned with the live UI and API so smoke
  tests stay useful.
- Prompt packs under `docs/packs/` are still planned.
- A lightweight lint/check script would make freshness checks less manual.
