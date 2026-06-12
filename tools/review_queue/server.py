from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUEUE_DIR = ROOT / "private_docs" / "review_queues"
DEFAULT_EXPORT_DIR = ROOT / "dropoff" / "review_exports"
ALL_QUEUES = "__all__"
DEFAULT_PORT = 8991


INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Review Queue</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f7f4;
      --panel: #ffffff;
      --text: #191919;
      --muted: #666b72;
      --line: #d8d8d2;
      --accent: #1769aa;
      --accent-weak: #e6f1fb;
      --danger: #9f2d2d;
      --control: #ffffff;
      --control-alt: #fbfbfa;
      --pill-bg: #fafafa;
      --key-bg: #eef0f2;
      --key-text: #30363d;
      --code-bg: #15171a;
      --code-text: #f6f8fa;
      --shadow: 0 8px 28px rgba(0, 0, 0, 0.08);
    }

    html[data-theme="dark"] {
      color-scheme: dark;
      --bg: #111315;
      --panel: #1b1e22;
      --text: #f1f3f5;
      --muted: #a4abb3;
      --line: #343a40;
      --accent: #66a6d9;
      --accent-weak: #183247;
      --danger: #f08a8a;
      --control: #20242a;
      --control-alt: #171a1e;
      --pill-bg: #20242a;
      --key-bg: #2a3037;
      --key-text: #f1f3f5;
      --code-bg: #090b0d;
      --code-text: #f1f3f5;
      --shadow: 0 10px 32px rgba(0, 0, 0, 0.28);
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 15px/1.45 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    header {
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      padding: 12px 18px;
      display: flex;
      gap: 14px;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 2;
    }

    h1 {
      font-size: 18px;
      margin: 0;
      font-weight: 700;
    }

    .bar {
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }

    select, button, textarea, input {
      font: inherit;
    }

    select {
      min-width: 230px;
      padding: 7px 9px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--control);
      color: var(--text);
    }

    #itemSelect {
      min-width: min(520px, 100%);
      flex: 1 1 320px;
    }

    main {
      max-width: 980px;
      margin: 20px auto 56px;
      padding: 0 16px;
    }

    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 20px;
    }

    .status-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }

    .pill {
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 4px 9px;
      color: var(--muted);
      background: var(--pill-bg);
      font-size: 13px;
      min-height: 0;
    }

    button.pill {
      cursor: pointer;
      text-align: center;
    }

    button.pill.active {
      color: #fff;
      background: var(--accent);
      border-color: var(--accent);
    }

    .question {
      font-size: 24px;
      line-height: 1.2;
      margin: 6px 0 14px;
      font-weight: 750;
    }

    .subject {
      border: 1px solid var(--line);
      background: var(--control-alt);
      border-radius: 8px;
      padding: 12px;
      margin: 10px 0 14px;
      white-space: pre-wrap;
    }

    .section-title {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .06em;
      color: var(--muted);
      font-weight: 800;
      margin: 16px 0 7px;
    }

    .evidence {
      display: grid;
      gap: 8px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .evidence li {
      border-left: 3px solid var(--accent);
      background: var(--accent-weak);
      padding: 8px 10px;
      border-radius: 4px;
    }

    .choices {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 10px;
      margin-top: 14px;
    }

    button {
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 10px 12px;
      background: var(--control);
      color: var(--text);
      cursor: pointer;
      text-align: left;
      min-height: 42px;
    }

    button:hover {
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-weak);
    }

    button.primary {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      text-align: center;
      font-weight: 700;
    }

    button.secondary {
      color: var(--muted);
    }

    button.danger {
      color: var(--danger);
    }

    .key {
      display: inline-flex;
      justify-content: center;
      align-items: center;
      width: 24px;
      height: 24px;
      border-radius: 5px;
      background: var(--key-bg);
      color: var(--key-text);
      font-weight: 800;
      margin-right: 8px;
      font-size: 13px;
    }

    textarea {
      width: 100%;
      min-height: 84px;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: var(--control);
      color: var(--text);
      resize: vertical;
    }

    .note-area {
      margin-top: 14px;
      display: grid;
      gap: 8px;
    }

    .actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 14px;
    }

    .split {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }

    pre {
      background: var(--code-bg);
      color: var(--code-text);
      padding: 14px;
      border-radius: 8px;
      overflow: auto;
      max-height: 420px;
      white-space: pre-wrap;
    }

    .hidden { display: none; }
    .muted { color: var(--muted); }
    .small { font-size: 13px; }
  </style>
</head>
<body>
  <header>
    <div class="bar">
      <h1>Review Queue</h1>
      <select id="queueSelect" aria-label="Queue"></select>
      <select id="itemSelect" aria-label="Question"></select>
      <button id="reloadBtn" class="secondary">Reload</button>
      <button id="themeBtn" class="secondary">Dark</button>
    </div>
    <div class="bar small muted">
      <span>Keys: 1-9 choices</span>
      <span>A previous</span>
      <span>S park</span>
      <span>D next</span>
    </div>
  </header>

  <main class="split">
    <section class="card" id="card">
      <div class="status-row" id="status"></div>
      <div class="muted small" id="itemMeta"></div>
      <div class="muted small" id="saveStatus"></div>
      <div class="question" id="question">Loading...</div>
      <div class="subject" id="subject"></div>

      <div id="evidenceWrap">
        <div class="section-title">Context from source</div>
        <ul class="evidence" id="evidence"></ul>
      </div>

      <div class="section-title">Choices</div>
      <div class="choices" id="choices"></div>

      <div class="note-area">
        <label class="small muted" for="note">Your answer / notes</label>
        <textarea id="note" placeholder="Type freely here. This autosaves as you type."></textarea>
      </div>

      <div class="actions">
        <button id="useNoteBtn" class="secondary">Use typed answer</button>
        <button id="prevBtn" class="secondary"><span class="key">A</span>Previous</button>
        <button id="skipBtn" class="secondary"><span class="key">S</span>Park</button>
        <button id="nextBtn" class="secondary"><span class="key">D</span>Next</button>
        <button id="exportBtn" class="primary">Send everything so far</button>
      </div>
    </section>

    <section class="card hidden" id="exportCard">
      <div class="section-title">Markdown export</div>
      <p class="muted small" id="exportStatus">The current queue export is shown below.</p>
      <button id="copyExportBtn" class="primary">Copy export</button>
      <pre id="exportText"></pre>
    </section>
  </main>

  <script>
    const ALL_QUEUES = "__all__";

    const state = {
      queues: [],
      queue: null,
      items: [],
      index: 0,
      filter: "all",
      draftTimer: null
    };

    const $ = (id) => document.getElementById(id);

    function applyTheme(theme) {
      document.documentElement.dataset.theme = theme;
      localStorage.setItem("reviewQueueTheme", theme);
      $("themeBtn").textContent = theme === "dark" ? "Light" : "Dark";
    }

    function setSaveStatus(text) {
      $("saveStatus").textContent = text || "";
    }

    function itemQueue(item) {
      return item && (item._queue || state.queue);
    }

    function statusKind(item) {
      const status = item && item.answer_status;
      if (status === "answered") return "answered";
      if (["skipped", "ask_later"].includes(status)) return "parked";
      return "pending";
    }

    function matchesFilter(item, filter = state.filter) {
      if (!item) return false;
      if (filter === "all") return true;
      return statusKind(item) === filter;
    }

    function counts() {
      const total = state.items.length;
      const answered = state.items.filter(i => statusKind(i) === "answered").length;
      const parked = state.items.filter(i => statusKind(i) === "parked").length;
      const pending = state.items.filter(i => statusKind(i) === "pending").length;
      return { total, answered, parked, pending };
    }

    function titleForItem(item) {
      const subject = item && item.subject;
      if (subject && typeof subject === "object") {
        return subject.title || subject.summary || item.id || "(no id)";
      }
      return subject || item.question || item.id || "(no id)";
    }

    function subjectText(subject) {
      if (subject == null) return "";
      if (typeof subject === "string") return subject;
      if (typeof subject === "object") {
        return Object.entries(subject).map(([k, v]) => `${k}: ${typeof v === "object" ? JSON.stringify(v) : v}`).join("\n");
      }
      return String(subject);
    }

    function evidenceList(evidence) {
      if (!evidence) return [];
      if (Array.isArray(evidence)) {
        return evidence.map(e => typeof e === "object" ? Object.entries(e).map(([k, v]) => `${k}: ${v}`).join(" | ") : String(e));
      }
      if (typeof evidence === "object") {
        return Object.entries(evidence).map(([k, v]) => `${k}: ${v}`);
      }
      return [String(evidence)];
    }

    function filteredIndices(filter = state.filter) {
      return state.items
        .map((item, idx) => matchesFilter(item, filter) ? idx : -1)
        .filter(idx => idx >= 0);
    }

    function firstMatchingIndex(start = 0, filter = state.filter) {
      if (!state.items.length) return 0;
      for (let offset = 0; offset < state.items.length; offset++) {
        const idx = (start + offset) % state.items.length;
        if (matchesFilter(state.items[idx], filter)) return idx;
      }
      return -1;
    }

    function moveWithinFilter(delta) {
      const indices = filteredIndices();
      if (!indices.length) return;
      const currentPos = indices.indexOf(state.index);
      const base = currentPos >= 0 ? currentPos : 0;
      const nextPos = (base + delta + indices.length) % indices.length;
      state.index = indices[nextPos];
    }

    function moveFromIndex(start, delta) {
      if (!state.items.length) return;
      let idx = start;
      for (let offset = 0; offset < state.items.length; offset++) {
        idx = (idx + delta + state.items.length) % state.items.length;
        if (matchesFilter(state.items[idx])) {
          state.index = idx;
          return;
        }
      }
      const first = firstMatchingIndex(0);
      state.index = first >= 0 ? first : 0;
    }

    function syncItemSelect() {
      const indices = filteredIndices();
      if (!indices.length) {
        $("itemSelect").innerHTML = `<option value="">No ${state.filter} items</option>`;
        $("itemSelect").disabled = true;
        return;
      }
      $("itemSelect").disabled = false;
      $("itemSelect").innerHTML = indices.map((idx) => {
        const item = state.items[idx];
        const source = item._queue ? `${item._queue.replace(".jsonl", "")} | ` : "";
        const label = `${idx + 1}. ${source}${titleForItem(item)} [${statusKind(item)}]`;
        return `<option value="${idx}">${escapeHtml(label)}</option>`;
      }).join("");
      $("itemSelect").value = String(state.index);
    }

    function setFilter(filter, start = 0) {
      state.filter = filter;
      const first = firstMatchingIndex(start, filter);
      state.index = first >= 0 ? first : 0;
      render();
    }

    function render() {
      const c = counts();
      if (!matchesFilter(state.items[state.index])) {
        const first = firstMatchingIndex(0);
        if (first >= 0) state.index = first;
      }
      $("status").innerHTML = [
        ["all", `All ${c.total}`],
        ["pending", `Pending ${c.pending}`],
        ["answered", `Answered ${c.answered}`],
        ["parked", `Parked ${c.parked}`]
      ].map(([filter, text]) => {
        const active = filter === state.filter ? " active" : "";
        return `<button class="pill status-filter${active}" data-filter="${filter}">${text}</button>`;
      }).join("");
      document.querySelectorAll("[data-filter]").forEach(btn => {
        btn.addEventListener("click", async () => {
          const targetFilter = btn.dataset.filter;
          await commitCurrentForLeave();
          setFilter(targetFilter, state.index);
        });
      });

      const item = state.items[state.index];
      if (!item || !matchesFilter(item)) {
        $("itemMeta").textContent = "";
        setSaveStatus("");
        $("question").textContent = `No ${state.filter} items in this queue.`;
        $("subject").textContent = "";
        $("choices").innerHTML = "";
        $("evidence").innerHTML = "";
        syncItemSelect();
        return;
      }

      const source = item._queue ? ` | ${item._queue}` : "";
      $("itemMeta").textContent = `${state.index + 1} / ${state.items.length}${source} | ${item.id || "(no id)"} | ${item.answer_status || "pending"}`;
      setSaveStatus(item.draft_saved_at ? `Draft saved ${item.draft_saved_at}` : "");
      $("question").textContent = item.question || "(no question)";
      $("subject").textContent = subjectText(item.subject);

      const ev = evidenceList(item.context || item.evidence);
      $("evidenceWrap").classList.toggle("hidden", ev.length === 0);
      $("evidence").innerHTML = ev.map(e => `<li>${escapeHtml(e)}</li>`).join("");

      const options = item.options || [];
      $("choices").innerHTML = options.map((option, idx) => {
        const key = idx < 9 ? `<span class="key">${idx + 1}</span>` : "";
        return `<button data-option-index="${idx}">${key}${escapeHtml(option)}</button>`;
      }).join("");
      document.querySelectorAll("[data-option-index]").forEach(btn => {
        btn.addEventListener("click", () => answerChoice(Number(btn.dataset.optionIndex)));
      });

      $("note").value = item.answer_note || "";
      syncItemSelect();
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
    }

    async function saveDraft(queue, id, note) {
      if (!queue || !id) return;
      setSaveStatus("Saving draft...");
      const res = await fetch("/api/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          queue,
          id,
          answer_note: note || null
        })
      });
      if (!res.ok) {
        setSaveStatus("Draft save failed.");
        return;
      }
      const updated = await res.json();
      const idx = state.items.findIndex(item => item.id === id);
      if (idx >= 0) state.items[idx] = { ...updated.item, _queue: state.items[idx]._queue };
      setSaveStatus(`Draft saved ${updated.item.draft_saved_at || ""}`.trim());
      await loadQueuesPreserve();
    }

    function scheduleDraftSave() {
      const item = state.items[state.index];
      if (!item) return;
      const note = $("note").value;
      item.answer_note = note || null;
      clearTimeout(state.draftTimer);
      state.draftTimer = setTimeout(() => {
        state.draftTimer = null;
        saveDraft(itemQueue(item), item.id, note.trim());
      }, 250);
      setSaveStatus("Saving draft...");
    }

    async function flushDraftSave() {
      const item = state.items[state.index];
      if (!item) return;
      const note = $("note").value;
      clearTimeout(state.draftTimer);
      state.draftTimer = null;
      item.answer_note = note || null;
      await saveDraft(itemQueue(item), item.id, note.trim());
    }

    async function loadQueues() {
      const res = await fetch("/api/queues");
      state.queues = await res.json();
      $("queueSelect").innerHTML = state.queues.map(q => `<option value="${q.name}">${escapeHtml(queueOptionLabel(q))}</option>`).join("");
      const preferred = state.queue || (state.queues.some(q => q.name === ALL_QUEUES) ? ALL_QUEUES : state.queues[0] && state.queues[0].name);
      if (preferred) {
        $("queueSelect").value = preferred;
        await loadQueue(preferred);
      }
    }

    async function loadQueue(name) {
      state.queue = name;
      const res = await fetch(`/api/items?queue=${encodeURIComponent(name)}`);
      state.items = await res.json();
      state.filter = "all";
      const first = firstMatchingIndex(0, state.filter);
      state.index = first >= 0 ? first : 0;
      render();
    }

    async function saveAnswer(payload, options = {}) {
      const shouldAdvance = options.advance !== false;
      const oldIndex = state.index;
      const item = state.items[state.index];
      if (!item) return;
      clearTimeout(state.draftTimer);
      state.draftTimer = null;
      const note = $("note").value.trim();
      const res = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          queue: itemQueue(item),
          id: item.id,
          answer_note: note || payload.answer_note || null,
          ...payload
        })
      });
      if (!res.ok) {
        alert(await res.text());
        return;
      }
      const updated = await res.json();
      state.items[state.index] = { ...updated.item, _queue: item._queue };
      setSaveStatus(`Saved ${updated.item.answered_at || ""}`.trim());
      if (shouldAdvance) {
        moveFromIndex(oldIndex, 1);
        render();
      }
      await loadQueuesPreserve();
    }

    async function loadQueuesPreserve() {
      const res = await fetch("/api/queues");
      state.queues = await res.json();
      $("queueSelect").innerHTML = state.queues.map(q => `<option value="${q.name}">${escapeHtml(queueOptionLabel(q))}</option>`).join("");
      $("queueSelect").value = state.queue;
    }

    function queueOptionLabel(queue) {
      const answered = queue.answered ?? Math.max(0, queue.total - queue.pending);
      const parked = queue.parked ? `, ${queue.parked} parked` : "";
      const pending = queue.pending ? `, ${queue.pending} pending` : "";
      return `${queue.label || queue.name} (${answered}/${queue.total} answered${parked}${pending})`;
    }

    async function answerChoice(idx) {
      const item = state.items[state.index];
      const option = item && item.options && item.options[idx];
      if (!option) return;
      await saveAnswer({ answer: option, answer_status: "answered" });
    }

    async function commitCurrentForLeave(options = {}) {
      const item = state.items[state.index];
      if (!item) return;
      const note = $("note").value.trim();
      if (options.forcePark) {
        await saveAnswer({
          answer: item.answer || null,
          answer_status: "ask_later",
          answer_note: note || item.answer_note || null
        }, { advance: false });
        return;
      }
      if (item.answer_status === "answered") {
        await flushDraftSave();
      } else if (note) {
        await saveAnswer({ answer: note, answer_status: "answered", answer_note: note }, { advance: false });
      } else {
        await saveAnswer({ answer: item.answer || null, answer_status: "ask_later" }, { advance: false });
      }
    }

    async function leaveAndMove(delta, options = {}) {
      const oldIndex = state.index;
      await commitCurrentForLeave(options);
      moveFromIndex(oldIndex, delta);
      render();
    }

    async function exportSummary() {
      await flushDraftSave();
      const res = await fetch("/api/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ queue: state.queue })
      });
      if (!res.ok) {
        alert(await res.text());
        return;
      }
      const sent = await res.json();
      const text = sent.text;
      $("exportText").textContent = text;
      $("exportCard").classList.remove("hidden");
      $("exportStatus").textContent = `Export saved to ${sent.latest_path || sent.path}.`;
      try {
        await navigator.clipboard.writeText(text);
        $("exportStatus").textContent = `Export saved to ${sent.latest_path || sent.path} and copied to clipboard.`;
      } catch (_err) {
        $("exportStatus").textContent = `Export saved to ${sent.latest_path || sent.path}.`;
      }
      $("exportCard").scrollIntoView({ behavior: "smooth", block: "start" });
    }

    $("queueSelect").addEventListener("change", async (event) => {
      const selectedQueue = event.target.value;
      await commitCurrentForLeave();
      await loadQueue(selectedQueue);
    });
    $("reloadBtn").addEventListener("click", async () => {
      await commitCurrentForLeave();
      await loadQueue(state.queue);
    });
    $("itemSelect").addEventListener("change", async (event) => {
      const selectedIndex = Number(event.target.value);
      if (!Number.isFinite(selectedIndex)) return;
      await commitCurrentForLeave();
      state.index = selectedIndex;
      render();
    });
    $("note").addEventListener("input", scheduleDraftSave);
    $("useNoteBtn").addEventListener("click", () => {
      const answer = $("note").value.trim();
      if (!answer) {
        alert("Type an answer first.");
        return;
      }
      saveAnswer({ answer, answer_status: "answered", answer_note: answer });
    });
    $("skipBtn").addEventListener("click", () => leaveAndMove(1, { forcePark: true }));
    $("prevBtn").addEventListener("click", async () => {
      if (!state.items.length) return;
      await leaveAndMove(-1);
    });
    $("nextBtn").addEventListener("click", async () => {
      if (!state.items.length) return;
      await leaveAndMove(1);
    });
    $("exportBtn").addEventListener("click", exportSummary);
    $("copyExportBtn").addEventListener("click", async () => {
      const text = $("exportText").textContent;
      if (!text) return;
      await navigator.clipboard.writeText(text);
      $("exportStatus").textContent = "Export copied to clipboard.";
    });

    document.addEventListener("keydown", (event) => {
      const tag = event.target.tagName.toLowerCase();
      if (tag === "textarea" || tag === "input" || tag === "select") return;
      const key = event.key.toLowerCase();
      if (/^[1-9]$/.test(key)) {
        answerChoice(Number(key) - 1);
      } else if (key === "s") {
        $("skipBtn").click();
      } else if (key === "a") {
        $("prevBtn").click();
      } else if (key === "d") {
        $("nextBtn").click();
      }
    });

    $("themeBtn").addEventListener("click", () => {
      const current = document.documentElement.dataset.theme === "dark" ? "dark" : "light";
      applyTheme(current === "dark" ? "light" : "dark");
    });

    applyTheme(localStorage.getItem("reviewQueueTheme") || "light");
    loadQueues();
  </script>
</body>
</html>
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    items: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            text = line.strip().lstrip("\ufeff")
            if not text:
                continue
            try:
                item = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}:{line_no}: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"{path.name}:{line_no}: expected JSON object")
            items.append(item)
    return items


def write_jsonl(path: Path, items: list[dict]) -> None:
    if path.exists():
        backup = path.with_suffix(path.suffix + ".bak")
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def item_status_kind(item: dict) -> str:
    status = item.get("answer_status")
    if status == "answered":
        return "answered"
    if status in {"skipped", "ask_later"}:
        return "parked"
    return "pending"


def queue_counts(items: list[dict]) -> dict:
    answered = sum(1 for item in items if item_status_kind(item) == "answered")
    parked = sum(1 for item in items if item_status_kind(item) == "parked")
    pending = sum(1 for item in items if item_status_kind(item) == "pending")
    return {
        "total": len(items),
        "answered": answered,
        "parked": parked,
        "pending": pending,
        "unresolved": pending + parked,
    }


def make_export(queue_name: str, items: list[dict]) -> str:
    answered = [item for item in items if item.get("answer_status") == "answered"]
    unresolved = [item for item in items if item.get("answer_status") != "answered"]
    lines = [
        f"# Review export: {queue_name}",
        "",
        f"Generated: {utc_now()}",
        "",
        f"- Total: {len(items)}",
        f"- Answered: {len(answered)}",
        f"- Pending / unresolved: {len(unresolved)}",
        "",
        "## Answered",
        "",
    ]
    if not answered:
        lines.append("No answered items yet.")
    for item in answered:
        lines.extend(format_item_export(item))
    lines.extend(["", "## Pending / Unresolved", ""])
    if not unresolved:
        lines.append("No pending or unresolved items.")
    for item in unresolved:
        lines.extend(format_item_export(item))
    lines.append("")
    return "\n".join(lines)


def safe_export_stem(name: str) -> str:
    stem = Path(name).stem
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in stem).strip("_")
    return safe or "review_queue"


def write_export(queue_name: str, text: str) -> tuple[Path, Path]:
    DEFAULT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    stem = safe_export_stem(queue_name)
    timestamp = utc_now().replace(":", "").replace("+0000", "Z").replace("+00:00", "Z")
    path = DEFAULT_EXPORT_DIR / f"{timestamp}_{stem}.md"
    latest_path = DEFAULT_EXPORT_DIR / f"latest_{stem}.md"
    path.write_text(text, encoding="utf-8", newline="\n")
    latest_path.write_text(text, encoding="utf-8", newline="\n")
    return path, latest_path


def format_item_export(item: dict) -> list[str]:
    subject = item.get("subject")
    if isinstance(subject, dict):
        title = subject.get("title") or subject.get("summary") or item.get("id", "(no id)")
    else:
        title = subject or item.get("id", "(no id)")
    lines = [
        f"### {title}",
        "",
        f"- id: `{item.get('id', '')}`",
    ]
    if item.get("_queue"):
        lines.append(f"- queue: `{item['_queue']}`")
    lines.extend([
        f"- status: `{item.get('answer_status', 'pending')}`",
        f"- answer: {item.get('answer') if item.get('answer') is not None else ''}",
    ])
    if item.get("answer_note"):
        lines.append(f"- note: {item['answer_note']}")
    if item.get("question"):
        lines.append(f"- question: {item['question']}")
    lines.append("")
    return lines


class ReviewServer(BaseHTTPRequestHandler):
    queue_dir: Path = DEFAULT_QUEUE_DIR

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")

    def do_GET(self) -> None:
        try:
            parsed = urlparse(self.path)
            if parsed.path == "/":
                self.send_text(INDEX_HTML, "text/html; charset=utf-8")
                return
            if parsed.path == "/api/queues":
                self.send_json(self.list_queues())
                return
            if parsed.path == "/api/items":
                queue = parse_qs(parsed.query).get("queue", [""])[0]
                self.send_json(self.read_queue_items(queue))
                return
            if parsed.path == "/api/export":
                queue = parse_qs(parsed.query).get("queue", [""])[0]
                name, items = self.export_items(queue)
                self.send_text(make_export(name, items), "text/markdown; charset=utf-8")
                return
            self.send_error(HTTPStatus.NOT_FOUND)
        except ValueError as exc:
            self.send_error(HTTPStatus.BAD_REQUEST, str(exc))

    def do_POST(self) -> None:
        try:
            parsed = urlparse(self.path)
            if parsed.path == "/api/answer":
                self.handle_answer()
                return
            if parsed.path == "/api/draft":
                self.handle_draft()
                return
            if parsed.path == "/api/send":
                self.handle_send()
                return
            self.send_error(HTTPStatus.NOT_FOUND)
        except ValueError as exc:
            self.send_error(HTTPStatus.BAD_REQUEST, str(exc))

    def read_payload(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Expected JSON object")
        return payload

    def handle_answer(self) -> None:
        payload = self.read_payload()
        queue = payload.get("queue", "")
        item_id = payload.get("id")
        path = self.queue_path(queue)
        items = read_jsonl(path)
        for item in items:
            if item.get("id") == item_id:
                item["answer"] = payload.get("answer")
                item["answer_note"] = payload.get("answer_note")
                status = payload.get("answer_status", "answered")
                item["answer_status"] = status
                if status == "answered":
                    item["answered_at"] = utc_now()
                    item.pop("parked_at", None)
                else:
                    item["parked_at"] = utc_now()
                    if not item.get("answered_at"):
                        item["answered_at"] = None
                item["reviewer"] = payload.get("reviewer", "local-review-app")
                write_jsonl(path, items)
                self.send_json({"ok": True, "item": item})
                return
        self.send_error(HTTPStatus.NOT_FOUND, f"Item not found: {item_id}")

    def handle_draft(self) -> None:
        payload = self.read_payload()
        queue = payload.get("queue", "")
        item_id = payload.get("id")
        path = self.queue_path(queue)
        items = read_jsonl(path)
        for item in items:
            if item.get("id") == item_id:
                item["answer_note"] = payload.get("answer_note")
                item["draft_saved_at"] = utc_now()
                item["reviewer"] = payload.get("reviewer", "local-review-app")
                if not item.get("answer_status"):
                    item["answer_status"] = "pending"
                write_jsonl(path, items)
                self.send_json({"ok": True, "item": item})
                return
        self.send_error(HTTPStatus.NOT_FOUND, f"Item not found: {item_id}")

    def handle_send(self) -> None:
        payload = self.read_payload()
        queue = payload.get("queue", "")
        name, items = self.export_items(queue)
        text = make_export(name, items)
        path, latest_path = write_export(name, text)
        self.send_json({
            "ok": True,
            "queue": queue,
            "path": str(path),
            "latest_path": str(latest_path),
            "text": text,
        })

    def list_queues(self) -> list[dict]:
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        paths = self.queue_paths()
        file_items = [(path, read_jsonl(path)) for path in paths]
        all_items = [item for _path, items in file_items for item in items]
        all_counts = queue_counts(all_items)
        queues = [{
            "name": ALL_QUEUES,
            "label": "All review queues",
            **all_counts,
            "aggregate": True,
        }]
        for path, items in file_items:
            label = path.stem.replace("_", " ")
            counts = queue_counts(items)
            queues.append({
                "name": path.name,
                "label": label,
                **counts,
            })
        return queues

    def queue_paths(self) -> list[Path]:
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        return sorted(path for path in self.queue_dir.glob("*.jsonl") if not path.name.startswith("_"))

    def read_queue_items(self, name: str) -> list[dict]:
        if name == ALL_QUEUES:
            items: list[dict] = []
            for path in self.queue_paths():
                for item in read_jsonl(path):
                    item = dict(item)
                    item["_queue"] = path.name
                    items.append(item)
            return items
        return read_jsonl(self.queue_path(name))

    def export_items(self, name: str) -> tuple[str, list[dict]]:
        if name == ALL_QUEUES:
            return "all_review_queues", self.read_queue_items(ALL_QUEUES)
        path = self.queue_path(name)
        return path.name, read_jsonl(path)

    def queue_path(self, name: str) -> Path:
        if not name or Path(name).name != name or not name.endswith(".jsonl"):
            raise ValueError("Invalid queue name")
        path = (self.queue_dir / name).resolve()
        if self.queue_dir.resolve() not in path.parents:
            raise ValueError("Queue path escapes queue directory")
        return path

    def send_json(self, data: object) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text: str, content_type: str) -> None:
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local review queue app.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--queue-dir", type=Path, default=DEFAULT_QUEUE_DIR)
    args = parser.parse_args()

    ReviewServer.queue_dir = args.queue_dir.resolve()
    server = ThreadingHTTPServer((args.host, args.port), ReviewServer)
    print(f"Review queue app: http://{args.host}:{args.port}")
    print(f"Queue dir: {ReviewServer.queue_dir}")
    server.serve_forever()


if __name__ == "__main__":
    main()
