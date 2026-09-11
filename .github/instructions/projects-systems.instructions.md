---
applyTo: "content/projects/**,content/systems/**"
---

# Projects and systems

The distinction is **does it end?** A project has a goal and finishes. A system keeps running
and needs maintaining. When a project ships something that then exists, the project page ends
and a system page begins — link them.

## Project pages

```markdown
# {Project name}

One sentence: what it is meant to achieve, and for whom.

## Status
`active` | `paused` | `shipped` | `abandoned` — as of {date}. One line on where it stands.

## Goal
What "done" means. If nobody has said, write "Not defined as of {date}" — that is
a finding, not a gap to paper over.

## Decisions
- [Decision title](../decisions/slug.md) — one line on what it settled

## How it is going
Dated notes, newest first. This is the part that actually gets read.
- **2026-08-01** — what happened, what it means

## Open questions

## Related
```

Frontmatter adds `status: active | paused | shipped | abandoned`.

## System pages

```markdown
# {System name}

One sentence: what it does and who depends on it.

## What it is for
The job it does, in the owner's terms, not the implementation's.

## How it works
Enough to reason about it. Link out rather than going deep.

## How it fails
The failure modes you have actually seen, each with a date and what was done.
This is usually the most valuable section on the page — write it even when it is thin.

## Who owns it
- Who to go to, and what "owns" means here

## Open questions

## Related
```

## Rules

- The **status line must carry a date.** A status with no date is a lie in waiting.
- **"How it is going" and "How it fails" are append-style**: add dated entries at the top, do not
  rewrite history. If an earlier entry turned out wrong, add a new entry saying so.
- A project with no linked decisions after a few months is suspicious — either decisions are
  being made and not recorded, or nothing is moving. Say so in the notes.
- Do not track tasks here. This is knowledge, not a to-do list. What belongs here is what you
  would need to explain the work to someone new.
