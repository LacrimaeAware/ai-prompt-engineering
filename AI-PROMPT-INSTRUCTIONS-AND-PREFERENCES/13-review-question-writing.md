# Review question writing

Review queues are not surveys. They are a way to turn messy project context into
specific decisions the user can answer quickly.

## Core rule

Write questions as concrete decisions, implementation targets, or classification
calls. Do not ask vague status questions unless the status label is the whole
point of the review.

Bad:

```text
What direction should route telegraph icons take?
```

Good:

```text
Implement route-planning previews so the player can inspect future town bosses
before committing. Which visibility rule should the current docs/code target?
```

The good version says what feature exists, what the player experience is, and
what decision remains.

## Required fields

Each item should give the reviewer:

- a title naming the system and decision
- one direct question
- the current best guess, if there is one
- short context explaining why the question exists
- 3 to 5 answer choices when possible
- a free-answer note box for messy context

Do not make a separate `Other` flow when the reviewer already has a free-answer
box. The text box is the messy answer.

## Question shape

Prefer these verbs:

- implement
- confirm
- choose
- test
- keep
- cut
- merge
- split
- park

Avoid these vague openings:

- What direction should...
- How should we think about...
- What is the status of...
- Is this a thing...
- Thoughts on...

Use those only when rewritten into a concrete decision.

## Game design queues

Game questions should sound like a design producer asking for an actionable
call, not like a model summarizing a document.

Bad:

```text
What is the current status of route telegraph icons?
```

Good:

```text
Confirm the route-preview rule: show the bosses for all next 3 towns on map
hover and next-town selection; test whether route elite/boss previews appear
before route entry or only after the player enters that route.
```

Bad:

```text
What direction should party-size pressure take?
```

Good:

```text
Choose the current PC/party pressure rule: keep broader PC strategy, but test
paid PC unlocks and at least one master whose constraint is a 6-mon limit.
```

## Alias or identity queues

Alias questions should be strict and bounded. Do not include raw chat quotes,
private logs, or long source excerpts.

Bad:

```text
Are these two accounts the same person?
```

Good:

```text
Classify whether these two account handles should merge under one alias record.
Use only the summarized signals shown here, and choose same person, different
people, or not enough evidence.
```

## Good answer choices

Choices should be mutually useful, not just labels that force a second
conversation.

Bad:

```json
["live", "planned", "future_possible", "parked", "discarded"]
```

Good:

```json
[
  "implement now",
  "keep as design target, test timing",
  "park until adjacent system exists",
  "cut from current game",
  "needs clarification"
]
```

The answer should tell the next model or producer what to do next.

## Context field

Use `context` for short reviewer-facing explanation. Avoid the word `evidence`
unless the queue is actually judging a claim from evidence.

Good:

```json
{
  "context": [
    "The current design wants route planning and preparation to matter.",
    "The unresolved part is whether route elite/boss previews happen before route entry or only after entry."
  ]
}
```

## Producer checklist

Before handing off a queue, check:

- Can the user answer without opening the source repo?
- Does the question name the implementation consequence?
- Are the choices useful if copied directly into a task list?
- Is messy context preserved in the note field?
- Are private refs summarized rather than copied?
- Would a human producer ask it this way?

If the answer is no, rewrite the item before handing it to the user.
