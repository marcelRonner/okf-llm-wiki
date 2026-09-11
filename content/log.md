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
**Created:** [Page](projects/x.md), [Page](decisions/y.md)
**Updated:** [Page](systems/z.md) — what changed
**Flagged:** contradictions found, questions left open
**Notes:** anything a future reader would want to know
```

---

## 2026-09-11 — Schema change: the instructions moved out of .github/

**Operation:** correction
**Input:** the owner asked for the instructions and prompts to live somewhere less tied to GitHub
Copilot, so a second assistant could read them
**Updated:** `AGENTS.md` (was `.github/copilot-instructions.md`), `.claude/rules/` (was
`.github/instructions/`), `.claude/commands/` (was `.github/prompts/`)
**Notes:** No rule changed meaning. This is where they live, not what they say.

`AGENTS.md` is the name every agent tool but Claude Code reads, and `CLAUDE.md` is one line that
imports it — Claude Code's loader looks only for `CLAUDE.md`, `.claude/CLAUDE.md`,
`CLAUDE.local.md` and `.claude/rules/`, so without that line the contract would be invisible to
it. The per-folder rules kept their globs: `applyTo:` became `paths:`, which is the same idea in
the other tool's dialect. The four operations became `.claude/commands/`, so `/note` and the rest
still work by name.

`.github/` is now **generated** from those files by `make schema`, and `make build` fails if it has
drifted. The alternative was two hand-maintained copies of every rule, which is the failure this
repo already had once and built `schema.yml` to stop: when two statements of the same rule
disagree, the assistant trusts both and resolves it by rewriting pages. Deleting a rule now also
deletes its mirror, so Copilot cannot go on loading something that no longer exists.

One gap worth knowing: a `paths:` glob attaches only after a file in that folder has been read, so
it cannot inform the *first* write to a folder. `AGENTS.md` carries a routing table naming which
rules file to open for which folder, which is the manual version of the same thing.

---

## 2026-09-11 — Schema change: the person and org types are gone

**Operation:** correction
**Input:** the owner asked for people and orgs to be removed from the wiki entirely
**Updated:** `schema.yml` — `person` and `org` deleted, five types remain; every generated
restatement of the schema followed from `make schema`
**Notes:** Both folders held nothing but scaffolding, so no page was lost and no link broke.

What went with them: `templates/person.md`, `templates/org.md`,
`.github/instructions/people-orgs.instructions.md`, and the `content/people/` and `content/orgs/`
folders. The type table in `.github/copilot-instructions.md`, the frontmatter enum, the README
layout tree and the section pages are generated, so they restamped themselves.

Hand-written prose that named the removed types was rewritten rather than deleted where the point
it was making still stood: the *Who owns it* section on system pages now asks who to go to instead
of linking a person page, and the ingest checklist still guards against material that is sensitive
about a named individual — a source page can quote a meeting full of people without the wiki
having a page for any of them. What did go is `/lint`'s boundary check, which existed only to
police person and org pages against a rule file that no longer exists.

The decision ladder in `.github/copilot-instructions.md` lost a rung: there is no longer a
question to ask about people, so a name that needs recording belongs in whichever project,
system or decision it turns up in.

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
