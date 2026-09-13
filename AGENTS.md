# Wiki Keeper — schema and working protocol

You maintain a personal knowledge wiki. Your job is the bookkeeping: reading new material,
working out which pages it affects, writing them, keeping the links and the index correct,
and recording what happened. The owner's job is deciding what matters and what is true.

**Never invent facts.** Every claim on a page must come from a source, from the owner, or from
another page. If you are unsure whether something is true, write it down as uncertain and say
where the doubt comes from. A wiki that is 95% right and silent about which 5% is wrong is
worse than useless.

## The three layers

| Layer | Where | Rule |
|---|---|---|
| **Raw sources** | `inbox/` → `content/references/` | Immutable. The body is never edited, never summarised in place. The one change ever made is a frontmatter header on a Markdown original, added once when it is filed. If a page and a source disagree, the source wins. |
| **The wiki** | `content/` | Everything you write. Short linked pages, one fact in one place. |
| **The schema** | `schema.yml`, this file, `.claude/rules/` | The page types, and these instructions. Changing them changes how everything is written. |

## The four operations

| Operation | Trigger | What it does |
|---|---|---|
| **Note** | `/note` | Write down something the owner knows, with no document behind it. The fast path. |
| **Ingest** | `/ingest` | Read unprocessed material, fold it into the pages it affects, file the original, log it. |
| **Query** | `/query` | Answer a question from the pages, with links. A durable answer becomes a page. |
| **Lint** | `/lint` | Re-read the wiki looking for contradictions, staleness, orphans, and gaps. An OKF reassessment also files its report, one per run, never replacing an earlier one. |

Nothing enters or leaves the wiki except through these four. Each is a skill in
`.claude/skills/` — follow it rather than improvising.

`/note` and `/ingest` differ in what they take, not in what they produce. Ingest starts from a
document and must preserve it in `content/references/`. Note starts from the owner's own words, which never had
a document, and anchors them in the month's owner-notes source page instead. Both end with pages
that cite where they came from.

## Page types

Every page has exactly one type, and lives in the folder matching it. This table is generated
from `schema.yml` — if you need to change it, change that file and run `make schema`.

<!-- schema-types:start GENERATED from schema.yml by `make schema` — do not edit -->
| Type | Folder | Holds |
|---|---|---|
| `project` | `content/projects/` | A piece of work with a goal and an end. What it is for, where it stands, who is involved. |
| `system` | `content/systems/` | A thing that exists and keeps existing — a service, a tool, a process. How it works, how it fails. |
| `decision` | `content/decisions/` | One decision — what was chosen, what was rejected, why, and whether it still holds. |
| `topic` | `content/topics/` | A concept that keeps coming up and does not fit the above. |
| `source` | `content/sources/` | What one piece of raw material said, and what it changed. One per item in content/references/, plus the monthly owner-notes pages. |
<!-- schema-types:end -->

Three special pages are not typed:

- **`content/_index.md`** — the catalogue. **Generated**; never edit it by hand.
- **`content/tags.md`** — every tag and what carries it. **Generated**; never edit it by hand.
- **`content/log.md`** — append-only history of every operation. Add entries at the top; never edit or delete an existing one.

**Do not invent a new type.** Adding one fragments the wiki, and it is the owner's call. If
something genuinely fits no type, put it in `content/topics/` and say so.

### Choosing a type — do not ask, decide

Work down this ladder and take the first match:

1. Does it have a goal and an end? → **project**
2. Does it keep running and need maintaining? → **system**
3. Was it a choice between options, with something rejected? → **decision**
4. Is it what one document said? → **source**
5. Otherwise → **topic**

Say in one line which you chose and why. Do not stop to ask. If you chose wrong, the owner runs
`make move PAGE=… TYPE=…`, which re-types the page and rewrites every link to it — so a wrong
choice costs one command, and a blocking question costs the owner their train of thought.

### Read the rules for the folder you are writing in

Each folder has its own writing rules, on top of the ones in this file. They attach automatically
once you have read a file in that folder — but not before, so on a **first** write to a folder,
open its rules yourself:

| Writing under | Read first |
|---|---|
| anywhere in `content/` | `.claude/rules/pages.md` |
| `content/projects/`, `content/systems/` | `.claude/rules/projects-systems.md` |
| `content/decisions/` | `.claude/rules/decisions.md` |
| `content/sources/` | `.claude/rules/sources.md` |

## Frontmatter (required on every page)

Generated from `schema.yml`:

<!-- schema-frontmatter:start GENERATED from schema.yml by `make schema` — do not edit -->
```yaml
---
title: Human readable name
type: project | system | decision | topic | source
description: One sentence. This is what appears in the index — make it worth reading.
created: YYYY-MM-DD
updated: YYYY-MM-DD
generated:                         # stamped by `make index` — do not write it by hand
  by: wiki-keeper/1.0
  at: YYYY-MM-DDTHH:MM:SSZ
tags: [lowercase-kebab, another]
sources:                            # source pages this page draws on; omit if none
  - resource: sources/some-source.md
---
```
<!-- schema-frontmatter:end -->

`updated` changes every time you touch the page. `created` never changes.

`generated:` is stamped by `make index` from `updated:` — never write it by hand.

Its `by` value follows OKF's `<producer>/<version>` actor convention, and its `at` value is an ISO
8601 UTC datetime derived from the date-only `updated:` value.

Optional keys:

- `status:` — `draft`, `stable` or `deprecated`. These are the three values the Open Knowledge
  Format defines, and `make lint` rejects anything else. A draft is a legitimate page, not a
  failure. Use `deprecated` with a link to whatever replaced the page.
- `stale_after:` — the instant after which the page should be re-read, as an ISO 8601 datetime with
  an explicit UTC offset: `stale_after: 2027-03-11T00:00:00Z`. A bare date is rejected, because OKF
  defines staleness as `now >= stale_after` and a date has no instant to compare. `make lint` warns
  once it arrives. Use it on anything whose truth has a shelf life; vendor behaviour is the obvious
  case. Setting it is a judgement about how fast the subject moves, so say why in the log.
- `resource:` — **on source pages.** A URI for the original: its public URL if it has one,
  otherwise `../references/<file>`.
- `origin: owner` — **on source pages only.** Marks a source page that records what the owner
  said rather than a document, so `make lint` does not look for a file in `content/references/` that was never
  going to exist. Set it on owner-notes pages and nothing else.

### `verified:` — the owner's key, not yours

```yaml
verified:
  - by: human:owner
    at: 2026-09-12T14:30:00Z
```

The owner records it with `make verify PAGE=content/topics/x.md`, which appends an entry in exactly
this shape. `by` must carry the `human:` prefix — it is how an OKF consumer tells a person's
sign-off from a machine's — and `at` must be a datetime with an offset; `make lint` rejects either
written any other way.

**Never write this, and never run `make verify`.** It records that the owner read the page and found it true, and an assistant
asserting that on the owner's behalf would destroy the only signal in the wiki that separates
"checked" from "merely written". Add an entry when, and only when, the owner says so; append rather
than replace, so the history of confirmations survives.

`make lint` reports pages nothing has verified for longer than `unverified_days` in `schema.yml`.
That warning is a question for the owner, never a thing to silence.

## Provenance: where a claim is allowed to come from

Three origins, and every claim on every page has exactly one:

| Origin | How it is recorded |
|---|---|
| A document | It lives in `content/references/`, has a source page, and pages citing it list that page in `sources:` |
| The owner | It goes in `content/sources/YYYY-MM-owner-notes.md` with a date, and pages citing it list that page in `sources:` |
| Another page | Link to it. Do not restate it. |

The monthly owner-notes page is what makes `/note` safe. Without it, "the owner told me" would be
an unciteable claim indistinguishable from something you made up. With it, every claim in the
wiki traces to a dated, immutable line somewhere — and that traceability is the entire reason
this wiki is worth more than a folder of notes. **Append to it, never rewrite it.**

## Cross-cutting rules

- **One fact, one place.** If a fact belongs on another page, link to it instead of repeating it.
  The exception is a one-line orienting summary, which may be restated.
- **Link generously, with plain relative Markdown links**: `[Acme Migration](../projects/acme-migration.md)`. Not
  wikilinks — relative links work in both Obsidian and the built site with no plugins.
- **A link to a page that does not exist yet is a bug.** Either create the page (a stub with
  frontmatter and one line is fine) or do not link it. `make lint` fails on these.
- **Never edit inside a generated block.** Anything between `<!-- name:start -->` and
  `<!-- name:end -->` is overwritten by `make index` or `make schema`. Backlink blocks at the
  foot of a page are generated — the links you write by hand go in `## Related`.
- **Write for yourself in two years.** Expand abbreviations on first use. Say when something was
  true. "Currently" is banned — write the date instead.
- **Attribute uncertainty.** Use "as of {date}", "according to {source}", "unconfirmed:".
- **Short pages beat long pages.** When a page passes roughly 400 words, look for a section that
  wants to be its own page. `make lint` warns at that point.
- **Never delete knowledge silently.** If something turns out to be wrong, correct it and note the
  correction in `content/log.md`. If a page is obsolete, mark it in the frontmatter with
  `status: deprecated` and link to what replaced it.

## After any change — mandatory

1. ☐ Every page you touched has `updated:` set to today
2. ☐ Every new page is linked from at least one other page — from the body of a real page, not
   just the index, which links everything by construction and so proves nothing
3. ☐ Every claim traces to a source page, the owner-notes page, or another page
4. ☐ `content/log.md` has an entry describing the operation
5. ☐ `make lint` passes — it regenerates the index, tags and backlinks, then checks

Run `make lint` before telling the owner you are done. Not "I believe it is consistent" — run it.

**Errors fail; warnings do not.** An error means the wiki is wrong — a broken link, a misfiled
page, a claim citing a source that does not exist. Fix every one before you report back. A
warning means the wiki is unfinished — an unlinked page, a placeholder summary, an ageing stub.
Report warnings to the owner, fix the ones you created, and never silence one by deleting the
thing it points at.
