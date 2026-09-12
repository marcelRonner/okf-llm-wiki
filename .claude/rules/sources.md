---
paths:
  - content/sources/**
---

# Source pages

One source page per item in `content/raw/`. It records **what the material said** and **what it changed
in the wiki** — it is the bridge between the immutable original and the pages derived from it.

File naming: `YYYY-MM-DD-short-slug.md`, where the date is the date of the material itself (when
the meeting happened, when the document was written), not the date you ingested it. If the
material has no date, use the ingest date and say so.

There is one other kind of source page — the monthly **owner notes** — described at the bottom
of this file. Everything above it describes document sources.

```markdown
# {What this source is}

One sentence: what it is, where it came from, and its date.

## Origin
| | |
|---|---|
| **File** | [`2026-08-01-name.pdf`](../raw/2026-08-01-name.pdf) |
| **Kind** | meeting notes / document / article / conversation / email thread |
| **Date** | 2026-08-01 |
| **Author** | who produced it |
| **Ingested** | 2026-08-02 |

## What it says
The substance, compressed. Long enough that you rarely need to reopen the original, short
enough to actually read. Preserve specifics — numbers, names, dates, commitments. Drop
pleasantries and repetition.

Do not editorialise here. Summary and interpretation are different things; this section is
summary. If you have an interpretation, put it under *What this changed*.

## Notable quotes
> Only when the exact wording matters — a commitment, a constraint, a striking phrase.

## What this changed
- Created [Page](../projects/x.md) — why
- Updated [Page](../systems/y.md) — what changed in it
- **Contradicts** [Page](../systems/z.md), which says X — flagged, not resolved

## Unresolved
What the source raised but did not settle. Questions for the owner go here.

## Related
```

## Rules

- **Never edit the raw file.** If it is unreadable or partial, say so on this page.
- **The source page is written once and rarely revisited.** It records what the material said at
  the time. If your understanding changes later, that belongs on the derived pages, not here.
- **Contradictions are reported, never resolved silently.** If a source disagrees with an
  existing page, record both, mark it under *What this changed*, and raise it with the owner.
  The source is not automatically right — it may be older, or wrong.
- **Every derived page links back here** via its `sources:` frontmatter. That is what makes it
  possible to ask "where did this claim come from?" later.
- If a source turns out to be worthless, still create the page and say so in one line. Otherwise
  you will re-ingest it in six months.

## Owner notes — the one source without a document

`content/sources/YYYY-MM-owner-notes.md`, one per month, created by `/note`. It records things the
owner said directly, which never had a document behind them and so have nothing to file in
`content/raw/`.

It is a source page because the alternative is worse. Without it, a fact the owner mentioned in
passing would sit on a page citing nothing, indistinguishable from a fact the assistant invented
— and the ability to tell those apart is the whole reason this wiki keeps sources at all.

It differs from a document source in four ways, and only these four:

- `origin: owner` in the frontmatter, which exempts it from the `content/raw/` pairing check. Without
  that key `make lint` reports E5 and is right to.
- It **accumulates**. A document source is written once; this one gets an entry appended every
  time the owner notes something in that month. Append at the bottom, under a `## YYYY-MM-DD`
  heading, so it reads chronologically.
- Entries are **quoted as said**, not summarised. The owner's words are the primary record here,
  exactly as a PDF's words are in `content/raw/`. Your writing goes on the derived page.
- It is **append-only**, like anything in `content/raw/`. If an entry turns out to be wrong, add a dated
  entry saying so and correct the derived page. Never edit or delete what was said.

Otherwise it behaves normally: derived pages cite it in `sources:`, and it records what it
changed.
