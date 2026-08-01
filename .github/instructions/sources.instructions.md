---
applyTo: "wiki/sources/**"
---

# Source pages

One source page per item in `raw/`. It records **what the material said** and **what it changed
in the wiki** — it is the bridge between the immutable original and the pages derived from it.

File naming: `YYYY-MM-DD-short-slug.md`, where the date is the date of the material itself (when
the meeting happened, when the document was written), not the date you ingested it. If the
material has no date, use the ingest date and say so.

```markdown
# {What this source is}

One sentence: what it is, where it came from, and its date.

## Origin
| | |
|---|---|
| **File** | [`raw/2026-08-01-name.pdf`](../../raw/2026-08-01-name.pdf) |
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
- Updated [Page](../people/y.md) — what changed in it
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
