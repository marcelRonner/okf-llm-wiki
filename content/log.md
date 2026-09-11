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

## 2026-08-02 — Schema change: a fourth operation, and lint learns two severities

**Operation:** correction
**Input:** the owner reported that adding a page or a topic was harder than it should be
**Created:** [Checks and finding things](topics/checks-and-finding-things.md) — split out of the
page below when documenting these changes pushed it past the 400-word rule it exists to explain
**Updated:** [How this wiki works](topics/how-this-wiki-works.md) — three operations became four

**What changed and why:**

- **`/note` added** as a fourth operation. The wiki had one door and it was built for documents:
  writing down something the owner simply knew meant manufacturing a file in `inbox/`, moving it
  to `raw/`, writing a source page, then writing the real page — four artefacts for one fact.
  `/note` takes their words directly. To keep every claim traceable rather than exempting notes
  from the rule, the owner's words are anchored in a monthly `sources/YYYY-MM-owner-notes.md`
  page marked `origin: owner`.
- **Lint split into errors and warnings.** Previously every finding failed, so `make new` left
  the repository in a broken state until the page was finished — the tooling punished capture.
  Errors (broken links, misfiled pages, missing sources) fail; warnings (unlinked pages,
  placeholder summaries, ageing stubs) are reported. `make build` still fails on both.
- **The orphan check now works.** It had been seeded from `index.md`, which links every page by
  construction, so it could never fire — an unlinked page passed lint clean while three files
  promised the check was being made. It now walks out from `log.md` and counts real inbound
  links, ignoring generated backlink blocks.
- **`schema.yml` is now the only definition of the page types.** They had been restated in six
  places read by three audiences with nothing checking they agreed. The failure mode was not
  untidiness: when `.github/` and the linter disagreed about which types existed, the assistant
  trusted both and would resolve the contradiction by rewriting pages to satisfy the linter.
  Generated restatements are now stamped by `make schema` and `make build` fails if they drift.
- **`make move` added**, which re-types a page and rewrites every link to it. This is what let
  "ask the owner which type to use" be replaced with a decision ladder — guessing wrong now
  costs one command instead of a manual link hunt.
- **`wiki/tags.md` and per-page backlinks are now generated**, giving two ways to find a page
  besides the type folder it happens to sit in.

**Flagged:** nothing was ingested and no claim changed — this is a change to how the wiki is
written, not to what it says.

---

## 2026-08-01 — Wiki created

**Operation:** setup
**Input:** initial scaffold
**Created:** [How this wiki works](topics/how-this-wiki-works.md)
**Notes:** Empty wiki with the schema, the three operations, templates and the checks in place.
Nothing ingested yet.
