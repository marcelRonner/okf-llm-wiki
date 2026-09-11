---
title: How this wiki works
type: topic
summary: The three layers, the four operations, and the rules that keep this wiki trustworthy.
created: 2026-08-01
updated: 2026-08-02
tags: [meta]
---

# How this wiki works

This wiki is a set of short, linked pages maintained mostly by an AI assistant. You decide what
goes in and what is true; the assistant does the bookkeeping. This page is both the explanation
and the first worked example of the format.

## Three layers

**Raw sources** live in `raw/`, exactly as they arrived, and are never edited. If a page and a
source disagree, the source wins — that is the whole reason to keep them.

**The wiki** is `content/`: everything written *about* those sources, plus everything you know that
never had a document behind it. This is the only layer that grows.

**The schema** is `schema.yml` and `.github/`: the page types, the required fields, the writing
rules, and the operations. Changing the schema changes how everything else gets written, so it
changes slowly and deliberately. The page types are defined once, in `schema.yml`; every other
file that lists them is generated from it, because a schema that disagrees with its own
validator turns the assistant into an agent of data loss.

## Four operations

| | What it does | How to run it |
|---|---|---|
| **Note** | Write down something you know, with no document behind it | `/note`, then the thing |
| **Ingest** | Read new material, fold it into the pages it affects, file the original, log it | Drop files in `inbox/`, then `/ingest` |
| **Query** | Answer a question from the pages, with links and a confidence level | `/query` |
| **Lint** | Look for contradictions, staleness, orphans and gaps | `make lint`, then `/lint` |

Nothing enters or leaves the wiki except through these four.

Note and ingest differ in what they take, not what they produce. Ingest starts from a document
and must preserve it in `raw/`. Note starts from your own words, which never had a document, and
anchors them in that month's `sources/YYYY-MM-owner-notes.md` instead. Use ingest when losing the
exact wording would lose something; otherwise note.

There were three operations at first, and the missing one showed. Everything had to arrive as a
document, so writing down something you simply knew meant manufacturing a file to put in `inbox/`
— four artefacts for one fact. The fast path was added on 2026-08-02 rather than loosening the
rule that every claim is traceable, which is why owner notes are a source page and not an
exemption.

## Why the rules are what they are

**One fact in one place.** The moment a fact is written twice, the two copies start drifting and
you have no way to tell which is right. Everything else links instead.

**Dates on every claim.** "Currently" is a claim with an expiry date and no label. A wiki with
dated claims ages gracefully; one without becomes untrustworthy in about a year, and once you
stop trusting it you stop reading it.

**Sources are immutable.** Being able to go back to what was actually said is what separates a
knowledge base from a pile of opinions.

**Stubs are fine.** Twenty honest stubs capture more than five polished pages and fifteen facts
lost. A stub says "this exists and here is the little I know", which is a real contribution.

**Orphans are not fine, but they are not emergencies.** A page nothing links to will never be
found again, so `make lint` reports it — as a warning. Link every new page from somewhere.

## What is checked, and how you find things

`make lint` verifies what a script can verify, and separates *the wiki is wrong* from *the wiki
is unfinished* — only the first fails. Three generated views make a page findable: the index, the
tag listing, and the backlinks at the foot of each page. Both are described in
[Checks and finding things](checks-and-finding-things.md).

`/lint` handles what a script cannot — contradictions between pages, claims that have gone stale,
structural drift, and whether anything on a person's page crosses the line into information that
should not be recorded. That split is deliberate: anything a computer can check reliably should
never depend on an assistant remembering it.

## Reading it

Two ways, over the same files:

- **Obsidian** — open `content/` as a vault. No build step, instant search, backlinks, graph view,
  works on a phone. This is the day-to-day way in.
- **`make serve`** — a searchable website, for sharing or reading on something without Obsidian.

Both work because pages use ordinary relative Markdown links rather than wikilinks.

## Open questions

- No publishing target is set up yet. `make build` produces `site/`; where it goes is undecided.
- There is no automatic trigger for ingest — files sit in `inbox/` until you run `/ingest`.
- Whether the monthly owner-notes pages should be split when they get long, or left as one long
  chronological record per month. Unresolved until one of them actually gets long.

## Related

- [Checks and finding things](checks-and-finding-things.md) — what `make lint` verifies, and the three ways a page gets found
- [Index](../_index.md) — every page in the wiki, grouped by type
- [Tags](../tags.md) — every subject in use, and what carries it
- [Log](../log.md) — what has been ingested, changed and corrected

<!-- backlinks:start GENERATED by `make index` — do not edit -->

## Linked from

- [Checks and finding things](checks-and-finding-things.md)
<!-- backlinks:end -->
