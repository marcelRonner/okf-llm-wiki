---
agent: agent
description: Fold new material from inbox/ (or pasted text) into the wiki, then file, log, and reindex it.
---

# Ingest

Bring new material into the wiki. Work through the steps in order and do not skip the
confirmation step — a wrong ingest is expensive to unpick.

## 1. Find the material

Run `make inbox` to list unprocessed files.

- **Files in `inbox/`** — process all of them unless told otherwise.
- **Text the owner pasted or dictated** — treat it as a source too. Before anything else, write
  it verbatim to `inbox/YYYY-MM-DD-slug.md` so the raw record exists. Do not tidy it up.

If the inbox is empty and nothing was pasted, say so and stop.

## 2. Read and orient

For each item, read it fully, then establish:

- What kind of material is this, who produced it, and what date does it describe?
- Which existing pages does it touch? Search the wiki — do not assume it is all new.
  Check `wiki/index.md` first, then grep for the proper nouns in the material.
- What is genuinely new versus a restatement of what you already have?

## 3. Propose before writing

Show the owner a short plan and wait for a reply:

```
Source: <what it is, date>

Pages to create:
  wiki/projects/x.md      — why
Pages to update:
  wiki/people/y.md        — what changes
Contradictions found:
  wiki/systems/z.md says A, this source says B
Questions:
  - …
```

Ask about anything genuinely ambiguous. Do not ask about things you can decide yourself —
filing, naming, and wording are your job.

## 4. Write

- Create the **source page** in `wiki/sources/` first — it is the anchor everything else cites.
- Then create or update the derived pages, following the instructions for each type.
- Add `sources:` frontmatter on every page you touched, pointing at the source page.
- Set `updated:` to today on every page you touched.
- Link new pages from somewhere. A page nothing links to will never be found again.
- Create honest stubs for entities you now know exist but know little about.

**Do not resolve contradictions on your own.** Record both claims, mark the conflict on the
source page, and raise it.

## 5. File the original

Move each processed file from `inbox/` to `raw/`, renaming it to match its source page slug:

```
git mv inbox/notes.pdf raw/2026-08-01-acme-kickoff.pdf
```

The inbox should be empty when you finish.

## 6. Record and verify

- Add an entry at the top of `wiki/log.md` (see the format in that file).
- Run `make lint`. Fix everything it reports.
- Report back: what you created, what you updated, what contradicts what, and what you
  still need from the owner.

## Judgement calls

**When material is thin**, write the little you have rather than padding. A three-line page with
a date beats an invented paragraph.

**When material is huge**, do not try to capture all of it. Capture what is decision-relevant and
say in the source page what you left out, so a future you knows to reopen the original.

**When you are unsure whether something is a project, a system, or a topic**, ask. Moving pages
later is cheap; a wiki where the same kind of thing lives in three folders is not.
