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
      --axis: var(--accent);
      --axis-weak: var(--accent-weak);
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
      --axis: var(--accent);
      --axis-weak: var(--accent-weak);
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 15px/1.45 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      height: 100vh;
      overflow: hidden;
    }

    header {
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      padding: 9px 14px;
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

    .queue-drawer {
      position: relative;
      min-width: min(620px, 100%);
    }

    .queue-drawer summary {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 6px 11px;
      background: var(--control);
      cursor: pointer;
      list-style: none;
    }

    .queue-drawer summary::-webkit-details-marker { display: none; }

    .queue-title {
      font-weight: 800;
    }

    .queue-summary {
      color: var(--muted);
      font-size: 13px;
    }

    .queue-controls {
      position: absolute;
      top: calc(100% + 8px);
      left: 0;
      width: min(880px, calc(100vw - 28px));
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
      z-index: 5;
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
      max-width: none;
      height: calc(100vh - 58px);
      margin: 0;
      padding: 0 16px;
      overflow: hidden;
    }

    .card {
      background: var(--panel);
      border: 0;
      border-radius: 0;
      box-shadow: none;
      padding: 14px 0;
      height: 100%;
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
      font-size: 22px;
      line-height: 1.2;
      margin: 0;
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

    .subject-grid {
      display: grid;
      gap: 10px;
      margin: 10px 0 14px;
    }

    .subject-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
    }

    .meta-chip {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 6px 11px;
      background: color-mix(in srgb, var(--axis-weak) 70%, var(--pill-bg));
      color: var(--text);
      font-size: 14px;
      font-weight: 750;
    }

    .meta-chip span {
      color: var(--muted);
      font-weight: 700;
    }

    .message-box,
    .context-box,
    .details-box,
    .guidance-box {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: var(--control-alt);
    }

    .message-box {
      border-left: 4px solid var(--axis);
      background: var(--axis-weak);
    }

    .message-text {
      font-size: 20px;
      line-height: 1.28;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }

    .context-box {
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      max-height: none;
      overflow: auto;
    }

    .chat-box,
    .marked-chat {
      background: #121314;
      color: #f2f2f2;
      border-color: #2c3035;
    }

    .marked-chat {
      box-shadow: 0 0 0 2px var(--axis-weak);
    }

    .marked-chat .section-title {
      color: #b9c0c9;
    }

    .chat-box {
      font-size: 17px;
      line-height: 1.38;
      padding: 9px 10px;
    }

    .chat-line {
      display: grid;
      grid-template-columns: minmax(88px, max-content) 1fr;
      gap: 8px;
      padding: 3px 5px;
      border-radius: 4px;
    }

    .chat-line.marked {
      background: color-mix(in srgb, var(--axis) 28%, transparent);
      outline: 1px solid color-mix(in srgb, var(--axis) 60%, transparent);
    }

    .chat-author {
      font-weight: 800;
      text-align: right;
      white-space: nowrap;
    }

    .chat-author::after {
      content: ":";
      color: inherit;
    }

    .chat-message {
      color: #f6f6f6;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }

    .marked-chat .chat-line {
      grid-template-columns: minmax(120px, max-content) 1fr;
      font-size: 19px;
    }

    .details-box {
      display: grid;
      gap: 6px;
      font-size: 13px;
      color: var(--muted);
    }

    .question-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 6px 0 10px;
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
      grid-template-columns: 1fr;
      gap: 10px;
      margin-top: 14px;
    }

    .left-choices {
      margin-top: 2px;
      padding: 10px 10px 12px;
      border: 1px solid color-mix(in srgb, var(--axis) 22%, var(--line));
      border-radius: 8px;
      background:
        linear-gradient(
          180deg,
          color-mix(in srgb, var(--axis-weak) 76%, var(--panel)) 0%,
          color-mix(in srgb, var(--axis-weak) 42%, var(--panel)) 100%
        );
    }

    .review-left .choices {
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      margin-top: 8px;
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

    .help-btn {
      border-radius: 50%;
      width: 30px;
      min-width: 30px;
      height: 30px;
      min-height: 30px;
      padding: 0;
      text-align: center;
      font-weight: 800;
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
      height: 100%;
    }

    .review-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(340px, 0.65fr);
      gap: 14px;
      height: 100%;
      min-height: 0;
    }

    .review-left,
    .review-right {
      min-height: 0;
      overflow: auto;
      border: 1px solid color-mix(in srgb, var(--axis) 35%, var(--line));
      border-radius: 8px;
      background:
        linear-gradient(
          180deg,
          color-mix(in srgb, var(--axis-weak) 88%, var(--panel)) 0%,
          color-mix(in srgb, var(--axis-weak) 54%, var(--panel)) 11%,
          var(--panel) 34%,
          var(--panel) 62%,
          color-mix(in srgb, var(--axis-weak) 50%, var(--panel)) 88%,
          color-mix(in srgb, var(--axis-weak) 82%, var(--panel)) 100%
        );
      box-shadow: var(--shadow);
      padding: 14px;
    }

    .review-right {
      position: sticky;
      top: 0;
      align-self: start;
      display: flex;
      flex-direction: column;
      max-height: calc(100vh - 86px);
    }

    .right-scroll {
      overflow: auto;
      flex: 1;
      min-height: 0;
      padding-right: 2px;
    }

    .choice-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 7px;
      align-items: stretch;
    }

    .choice-answer {
      width: 100%;
    }

    .choice-help-btn {
      width: 34px;
      min-width: 34px;
      min-height: 42px;
      padding: 0;
      text-align: center;
      font-weight: 900;
      color: var(--muted);
      background: var(--control-alt);
    }

    .choice-help-pop {
      grid-column: 1 / -1;
      border: 1px solid color-mix(in srgb, var(--axis) 22%, var(--line));
      border-radius: 7px;
      background: color-mix(in srgb, var(--axis-weak) 54%, var(--panel));
      color: var(--text);
      padding: 9px 10px;
      font-size: 13px;
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

    @media (max-width: 900px) {
      body { overflow: auto; height: auto; }
      main { height: auto; overflow: visible; padding: 0 10px 24px; }
      header { position: static; }
      .review-grid { grid-template-columns: 1fr; height: auto; }
      .review-left, .review-right { overflow: visible; max-height: none; }
      .review-right { position: static; }
      .queue-controls { position: static; width: calc(100vw - 28px); margin-top: 8px; }
    }
  </style>
</head>
<body>
  <header>
    <details class="queue-drawer" id="queueDrawer">
      <summary>
        <span class="queue-title">Review Queue</span>
        <span class="queue-summary" id="queueSummary">Loading...</span>
      </summary>
      <div class="bar queue-controls">
        <select id="queueSelect" aria-label="Queue"></select>
        <select id="itemSelect" aria-label="Question"></select>
        <button id="reloadBtn" class="secondary">Reload</button>
        <button id="themeBtn" class="secondary">Dark</button>
      </div>
    </details>
    <div class="bar small muted">
      <span>Keys: Q W E R... choices</span>
      <span>A previous</span>
      <span>S park</span>
      <span>D next</span>
    </div>
  </header>

  <main class="split">
    <section class="card" id="card">
      <div class="review-grid">
        <section class="review-left" id="reviewLeft">
          <div class="muted small" id="itemMeta"></div>
          <div class="question-row">
            <div class="question" id="question">Loading...</div>
            <button id="helpBtn" class="secondary help-btn" title="Show guidance">?</button>
          </div>
          <div class="guidance-box hidden" id="guidance"></div>
          <div class="subject-grid">
            <div class="subject-meta" id="subjectMeta"></div>
            <div class="message-box marked-chat">
              <div class="section-title">Marked message</div>
              <div class="message-text" id="messageText"></div>
            </div>
            <div id="contextWrap">
              <div class="section-title">Chat context</div>
              <div class="context-box chat-box" id="contextText"></div>
            </div>
            <div class="details-box hidden" id="subjectDetails"></div>
          </div>
          <div class="left-choices">
            <div class="section-title">Choices</div>
            <div class="choices" id="choices"></div>
          </div>
        </section>

        <aside class="review-right" id="reviewRight">
          <div class="right-scroll" id="rightScroll">
            <div class="status-row" id="status"></div>
            <div class="muted small" id="saveStatus"></div>

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

            <div id="evidenceWrap">
              <div class="section-title">Selection evidence</div>
              <ul class="evidence" id="evidence"></ul>
            </div>
          </div>
        </aside>
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
      draftTimer: null,
      guidanceOpen: false
    };

    const $ = (id) => document.getElementById(id);
    const CHOICE_KEYS = ["q", "w", "e", "r", "t", "y", "u", "i", "o"];
    const AXIS_TITLES = {
      validity: "Validity",
      literal_alignment: "Literal alignment",
      magnitude_distortion: "Magnitude distortion",
      play_frame: "Seriousness / bit frame",
      masking_facework: "Masking / facework",
      hostility: "Hostility",
      shock_attention: "Shock / attention"
    };
    const AXIS_HELP = {
      validity: "Should this row be eligible for semantic/intent training? Mark bot output, mod notices, pure links, pure ASCII/image text, command responses, and totally opaque fragments as not_valid. Short human messages can still be valid.",
      literal_alignment: "Aligned = conventional chat meaning points the same way as the intended stance, including normal emote/action/greeting use. Divergent = irony/reversal/gap. Unclear = no stable meaning or you cannot tell.",
      magnitude_distortion: "Literal/normal = ordinary strength. Overstated = hyperbole or exaggerated magnitude. Understated = deliberately downplayed. This axis is separate from irony.",
      play_frame: "Serious/plain = straightforward or no bit-frame. Bit/unserious = performed as a joke, riff, or unserious chat move. Bit-as-cover = the bit form covers aggression, status, criticism, or a risky stance.",
      masking_facework: "Absent = no obvious cover. Possible/present = humor or irony seems to launder criticism, aggression, status, or a socially risky stance.",
      hostility: "Low/none = not hostile. Mild/mock = teasing, mockery, casual insult. Present = direct hostility or aggressive attack.",
      shock_attention: "Present = shock value or attention-bid energy is the point. Low/none = ordinary chat, even if rude or dumb."
    };
    const AXIS_COLORS = {
      validity: ["#2f80ed", "#eaf3ff"],
      literal_alignment: ["#9b51e0", "#f3eaff"],
      magnitude_distortion: ["#f2994a", "#fff3e8"],
      play_frame: ["#27ae60", "#e9f8ef"],
      masking_facework: ["#eb5757", "#ffeded"],
      hostility: ["#d97706", "#fff2d9"],
      shock_attention: ["#e84393", "#ffeaf5"]
    };
    const USER_COLORS = [
      "#ff4f5f", "#ff9f1c", "#ffd166", "#06d6a0", "#2ee86f", "#00d1ff",
      "#3a86ff", "#7b61ff", "#b967ff", "#ff70a6", "#4dd599", "#f72585",
      "#43aa8b", "#90be6d", "#f9844a", "#c77dff"
    ];

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

    function displayQuestion(item) {
      const axis = item && item.subject && item.subject.axis;
      return item.question || AXIS_TITLES[axis] || "(no question)";
    }

    function guidanceText(item) {
      if (!item) return "";
      const axis = item.subject && item.subject.axis;
      return item.guidance || AXIS_HELP[axis] || item.question || "";
    }

    function applyAxisColor(item) {
      const axis = item && item.subject && item.subject.axis;
      const [strong, weak] = AXIS_COLORS[axis] || ["var(--accent)", "var(--accent-weak)"];
      document.documentElement.style.setProperty("--axis", strong);
      document.documentElement.style.setProperty("--axis-weak", weak);
    }

    function hashString(value) {
      let h = 0;
      const s = String(value || "").toLowerCase();
      for (let i = 0; i < s.length; i++) {
        h = ((h << 5) - h + s.charCodeAt(i)) | 0;
      }
      return Math.abs(h);
    }

    function colorForAuthor(author) {
      if (!author) return "#aeb4bd";
      return USER_COLORS[hashString(author) % USER_COLORS.length];
    }

    function normalizeLineText(value) {
      return String(value || "").trim().replace(/\s+/g, " ").toLowerCase();
    }

    function splitChatLine(line) {
      const text = String(line || "");
      const match = text.match(/^([A-Za-z0-9_]{1,32}):\s*(.*)$/);
      if (!match) return { author: "", message: text };
      return { author: match[1], message: match[2] };
    }

    function renderChatLine(author, message, marked = false) {
      const cls = marked ? "chat-line marked" : "chat-line";
      if (!author) {
        return `<div class="${cls}"><span></span><span class="chat-message">${escapeHtml(message)}</span></div>`;
      }
      return `<div class="${cls}"><span class="chat-author" style="color:${colorForAuthor(author)}">${escapeHtml(author)}</span><span class="chat-message">${escapeHtml(message)}</span></div>`;
    }

    function renderChatContext(context, markedAuthor, markedMessage) {
      const target = normalizeLineText(markedMessage);
      const targetAuthor = String(markedAuthor || "").toLowerCase();
      return String(context || "").split(/\r?\n/).map((line) => {
        const parsed = splitChatLine(line);
        const msg = normalizeLineText(parsed.message);
        const sameAuthor = parsed.author.toLowerCase() === targetAuthor;
        const marked = sameAuthor && target && (msg === target || msg.includes(target) || target.includes(msg));
        return renderChatLine(parsed.author, parsed.message, marked);
      }).join("");
    }

    function optionLabel(item, option) {
      const labels = item && item.option_labels;
      return labels && labels[option] ? labels[option] : option;
    }

    function optionHelp(item, option) {
      const help = item && item.option_help;
      return help && help[option] ? help[option] : "";
    }

    function renderSubject(item) {
      const subject = item && item.subject;
      $("subjectMeta").innerHTML = "";
      $("messageText").innerHTML = "";
      $("contextText").innerHTML = "";
      $("contextWrap").classList.add("hidden");
      $("subjectDetails").classList.add("hidden");
      $("subjectDetails").innerHTML = "";
      if (subject == null) return;
      if (typeof subject !== "object") {
        $("messageText").textContent = String(subject);
        return;
      }
      const chips = [];
      for (const key of ["channel", "author", "axis"]) {
        if (subject[key]) chips.push(`<span class="meta-chip"><span>${escapeHtml(key)}</span>${escapeHtml(subject[key])}</span>`);
      }
      $("subjectMeta").innerHTML = chips.join("");
      const message = subject.message || subject.token || subject.summary || subject.title || "";
      $("messageText").innerHTML = renderChatLine(subject.author || "", message, true);
      if (subject.context) {
        $("contextWrap").classList.remove("hidden");
        $("contextText").innerHTML = renderChatContext(subject.context, subject.author, message);
      }
      const hiddenKeys = new Set(["channel", "author", "axis", "message", "context", "title"]);
      const details = Object.entries(subject)
        .filter(([key]) => !hiddenKeys.has(key))
        .map(([key, value]) => `<div><strong>${escapeHtml(key)}:</strong> ${escapeHtml(typeof value === "object" ? JSON.stringify(value) : value)}</div>`);
      if (details.length) {
        $("subjectDetails").classList.remove("hidden");
        $("subjectDetails").innerHTML = details.join("");
      }
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

    function updateQueueSummary() {
      const c = counts();
      const queue = state.queue && state.queue !== ALL_QUEUES
        ? state.queue.replace(".jsonl", "")
        : "All queues";
      const pos = state.items.length ? state.index + 1 : 0;
      $("queueSummary").textContent = `${queue} · ${pos}/${state.items.length || 0} · ${c.pending} pending`;
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
      updateQueueSummary();
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
        renderSubject(null);
        $("guidance").classList.add("hidden");
        $("choices").innerHTML = "";
        $("evidence").innerHTML = "";
        syncItemSelect();
        return;
      }

      const source = item._queue ? ` | ${item._queue}` : "";
      applyAxisColor(item);
      $("itemMeta").textContent = `${state.index + 1} / ${state.items.length}${source} | ${item.id || "(no id)"} | ${item.answer_status || "pending"}`;
      setSaveStatus(item.draft_saved_at ? `Draft saved ${item.draft_saved_at}` : "");
      $("question").textContent = displayQuestion(item);
      const help = guidanceText(item);
      $("helpBtn").classList.toggle("hidden", !help);
      $("guidance").textContent = help;
      $("guidance").classList.toggle("hidden", !state.guidanceOpen || !help);
      renderSubject(item);

      const ev = evidenceList(item.context || item.evidence);
      $("evidenceWrap").classList.toggle("hidden", ev.length === 0);
      $("evidence").innerHTML = ev.map(e => `<li>${escapeHtml(e)}</li>`).join("");

      const options = item.options || [];
      $("choices").innerHTML = options.map((option, idx) => {
        const shortcut = CHOICE_KEYS[idx] || String(idx + 1);
        const key = shortcut ? `<span class="key">${escapeHtml(shortcut.toUpperCase())}</span>` : "";
        const help = optionHelp(item, option);
        const hint = help ? `<button type="button" class="choice-help-btn" data-help-index="${idx}" aria-label="Explain ${escapeHtml(optionLabel(item, option))}">?</button>` : "";
        const pop = help ? `<div class="choice-help-pop hidden" id="choiceHelp-${idx}">${escapeHtml(help)}</div>` : "";
        return `<div class="choice-row"><button class="choice-answer" data-option-index="${idx}">${key}${escapeHtml(optionLabel(item, option))}</button>${hint}${pop}</div>`;
      }).join("");
      document.querySelectorAll("[data-option-index]").forEach(btn => {
        btn.addEventListener("click", () => answerChoice(Number(btn.dataset.optionIndex)));
      });
      document.querySelectorAll("[data-help-index]").forEach(btn => {
        btn.addEventListener("click", (event) => {
          event.preventDefault();
          event.stopPropagation();
          const pop = $(`choiceHelp-${btn.dataset.helpIndex}`);
          if (pop) pop.classList.toggle("hidden");
        });
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

    async function saveDraftForLeave() {
      const item = state.items[state.index];
      if (!item) return;
      const note = $("note").value.trim();
      item.answer_note = note || null;
      if (item.answer_status === "answered" || note) {
        await saveDraft(itemQueue(item), item.id, note);
      }
    }

    function scrollToReviewTop() {
      $("reviewLeft").scrollTo({ top: 0, behavior: "smooth" });
      $("reviewRight").scrollTo({ top: 0, behavior: "smooth" });
      $("rightScroll").scrollTo({ top: 0, behavior: "smooth" });
      window.scrollTo({ top: 0, behavior: "smooth" });
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
        scrollToReviewTop();
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
      await saveDraftForLeave();
    }

    async function leaveAndMove(delta, options = {}) {
      const oldIndex = state.index;
      await commitCurrentForLeave(options);
      moveFromIndex(oldIndex, delta);
      render();
      scrollToReviewTop();
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
      scrollToReviewTop();
    });
    $("reloadBtn").addEventListener("click", async () => {
      await commitCurrentForLeave();
      await loadQueue(state.queue);
      scrollToReviewTop();
    });
    $("itemSelect").addEventListener("change", async (event) => {
      const selectedIndex = Number(event.target.value);
      if (!Number.isFinite(selectedIndex)) return;
      await commitCurrentForLeave();
      state.index = selectedIndex;
      render();
      scrollToReviewTop();
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
    $("helpBtn").addEventListener("click", () => {
      state.guidanceOpen = !state.guidanceOpen;
      render();
    });

    document.addEventListener("keydown", (event) => {
      const tag = event.target.tagName.toLowerCase();
      if (tag === "textarea" || tag === "input" || tag === "select") return;
      const key = event.key.toLowerCase();
      const choiceIdx = CHOICE_KEYS.indexOf(key);
      if (choiceIdx >= 0) {
        answerChoice(choiceIdx);
      } else if (/^[1-9]$/.test(key)) {
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
