---
title: Log
type: log
description: Append-only chronological record of wiki operations and corrections.
---

# Log

Newest first. **Entries are never edited or deleted.** If an entry turns out to be wrong, add a
new one saying so — the mistake and its correction are both part of the record.

Format — date groups holding list entries, which is what the Open Knowledge Format requires of a
reserved `log.md` (§9). The detail of an entry goes underneath it, indented:

```markdown
## YYYY-MM-DD

- **Ingest:** short description
  - **Input:** what came in (link the raw file, or quote the question)
  - **Created:** [Page](projects/x.md), [Page](decisions/y.md)
  - **Updated:** [Page](systems/z.md) — what changed
  - **Flagged:** contradictions found, questions left open
  - **Notes:** anything a future reader would want to know
```

## 2026-09-13

- **Update:** [Open Knowledge Format](topics/open-knowledge-format.md) — OKF reassessments are filed
  one per run and never replace an earlier one; each report puts the mandatory checks first, groups
  the rest by family, and names every check next to its ID.

## 2026-09-12

- **Ingest:** [OKF v0.2 conformance assessment](sources/2026-09-12-okf-v0-2-conformance-assessment.md)
  — conformant; 28 of 41 checks met, none partial. [Open Knowledge Format](topics/open-knowledge-format.md)
  points to it as current.
- **Initialization:** Starting point for a new wiki: the schema, the four operations, the checks, and
  sample pages describing the pattern it implements.
