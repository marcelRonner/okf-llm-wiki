---
title: Log
type: log
summary: Append-only record of every ingest, query and correction.
---

# Log

Newest first. **Entries are never edited or deleted.** If an entry turns out to be wrong, add a
new one saying so — the mistake and its correction are both part of the record.

Format:

```markdown
## YYYY-MM-DD — Ingest: short description

**Operation:** ingest | query | lint | correction
**Input:** what came in (link the raw file, or quote the question)
**Created:** [Page](projects/x.md), [Page](people/y.md)
**Updated:** [Page](systems/z.md) — what changed
**Flagged:** contradictions found, questions left open
**Notes:** anything a future reader would want to know
```

---

## 2026-08-01 — Wiki created

**Operation:** setup
**Input:** initial scaffold
**Created:** [How this wiki works](topics/how-this-wiki-works.md)
**Notes:** Empty wiki with the schema, the three operations, templates and the checks in place.
Nothing ingested yet.
