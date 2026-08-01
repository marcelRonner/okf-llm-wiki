---
title: How this wiki works
type: topic
summary: The three layers, the three operations, and the rules that keep this wiki trustworthy.
created: 2026-08-01
updated: 2026-08-01
tags: [meta]
---

# How this wiki works

This wiki is a set of short, linked pages maintained mostly by an AI assistant. You decide what
goes in and what is true; the assistant does the bookkeeping. This page is both the explanation
and the first worked example of the format.

## Three layers

**Raw sources** live in `raw/`, exactly as they arrived, and are never edited. If a page and a
source disagree, the source wins — that is the whole reason to keep them.

**The wiki** is `wiki/`: everything written *about* those sources, plus everything you know that
never had a document behind it. This is the only layer that grows.

**The schema** is `.github/`: the page types, the required fields, the writing rules, and the
three operations. Changing the schema changes how everything else gets written, so it changes
slowly and deliberately.

## Three operations

| | What it does | How to run it |
|---|---|---|
| **Ingest** | Read new material, fold it into the pages it affects, file the original, log it | Drop files in `inbox/`, then `/ingest` |
| **Query** | Answer a question from the pages, with links and a confidence level | `/query` |
| **Lint** | Look for contradictions, staleness, orphans and gaps | `make lint`, then `/lint` |

Nothing enters or leaves the wiki except through these three.

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

**Orphans are not fine.** A page nothing links to will never be found again, so `make lint`
treats it as an error. Link every new page from somewhere.

## What is checked automatically

`make lint` verifies the things a script can verify: frontmatter present and valid, page filed
in the folder matching its type, links resolving, no orphans, `sources:` pointing at real source
pages, every file in `raw/` written up, inbox empty, dates sane, and the index current.

`/lint` handles the rest — contradictions between pages, claims that have gone stale, structural
drift, and whether anything on a person's page crosses the line into information that should not
be recorded. That split is deliberate: anything a computer can check reliably should never
depend on an assistant remembering it.

## Reading it

Two ways, over the same files:

- **Obsidian** — open `wiki/` as a vault. No build step, instant search, backlinks, graph view,
  works on a phone. This is the day-to-day way in.
- **`make serve`** — a searchable website, for sharing or reading on something without Obsidian.

Both work because pages use ordinary relative Markdown links rather than wikilinks.

## Open questions

- No publishing target is set up yet. `make build` produces `site/`; where it goes is undecided.
- There is no automatic trigger for ingest — files sit in `inbox/` until you run `/ingest`.

## Related

- [Index](../index.md) — every page in the wiki, grouped by type
- [Log](../log.md) — what has been ingested, changed and corrected
