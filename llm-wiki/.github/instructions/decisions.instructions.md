---
applyTo: "wiki/decisions/**"
---

# Decision pages

A decision page exists to answer one question later: **why did we do it that way?** The value is
almost entirely in the rejected alternatives and the reasoning. A page that records only the
outcome is barely worth writing.

File naming: `YYYY-MM-DD-short-slug.md` — the date is when it was *decided*, so the folder sorts
chronologically.

```markdown
# {The decision, as a statement}

Title it as what was decided, not as the question. "Use Postgres for the event store", not
"Which database?". Someone scanning the folder should learn the answer without opening it.

## Status
`proposed` | `accepted` | `superseded` | `reversed` — as of {date}.
If superseded or reversed, link to what replaced it and say what changed.

## Context
What was true at the time that made this a question at all. Constraints, pressures, what was
already committed. Write it so it stays readable once those facts have changed.

## Decision
What was chosen. One paragraph.

## Alternatives considered
| Option | Why not |
|---|---|
| … | … |

Be honest here. "Nobody had used it" is a real reason and worth recording — later you will want
to know whether the reason was technical or circumstantial.

## Consequences
What this commits you to, including the costs. Both the good and the annoying.

## Revisit if
The conditions that would make this worth reopening. If you can name them, name them — this is
what turns a decision log into something that pays you back.

## Related
```

## Rules

- **Never edit a decision's Context or Decision after it is `accepted`.** They record what was
  believed at the time. If reality changed, change `Status`, add a new decision page, and link
  the two. This is the whole point of the type.
- **Every decision links to at least one project or system.** A decision floating free is one
  nobody will find when they need it.
- **Record decisions you disagreed with**, and say so in Context. Those are the ones you will
  most want the reasoning for later.
- If the owner describes a decision in passing during ingest, do not silently file it — ask
  whether it was really decided, by whom, and when. A guessed decision date is worse than none.
