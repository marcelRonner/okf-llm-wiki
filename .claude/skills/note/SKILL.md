---
name: note
description: Write down something the owner knows, with no document behind it. The fast path into the wiki.
---

# Note

The owner knows something and wants it in the wiki. There is no document, no file in `inbox/`,
nothing to file in `content/references/` — just what they said.

What they said: $ARGUMENTS

**This operation is optimised for not interrupting them.** `/ingest` exists for material that
needs careful reading and a plan before anything is written. This does not. Read what they said,
work out where it goes, write it, and report. Ask nothing you can decide yourself.

## 1. Take the note at face value

Whatever the owner typed after `/note` is the note. If they said it in the conversation rather
than after the command, use that — do not make them retype it.

Do not tidy their words before recording them. What goes in the owner-notes page is what they
said; what goes in the wiki page is your writing.

## 2. Anchor it

Every claim in this wiki has to trace back to something dated. For a note, that anchor is the
month's owner-notes source page: `content/sources/YYYY-MM-owner-notes.md`.

If this month's page does not exist, create it:

```markdown
---
title: Owner notes — YYYY-MM
type: source
origin: owner
description: What the owner said in YYYY-MM that was not written down anywhere else.
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [owner-notes]
---

# Owner notes — YYYY-MM

Things the owner said directly, with no document behind them. Each entry is dated and quoted as
said. **Append only** — entries are never edited or removed, exactly like anything in `content/references/`.
This page is what lets a page written from a note cite something instead of asserting it.

## YYYY-MM-DD

> what they said, verbatim

Written up as: [Page](../topics/x.md)
```

`origin: owner` matters — it tells `make lint` not to look for a file in `content/references/` that was never
going to exist. Without it you get an E5 error.

Then append this note's entry, under today's date, at the **bottom** of the page. Chronological,
because it is a record and not a catalogue.

## 3. Work out what it touches

Search before writing — a note is usually about something already in the wiki.

- Check `content/_index.md`, then grep for the proper nouns in the note.
- Check `content/tags.md` if the note is about a subject rather than a named thing.

Then decide: does this update an existing page, or need a new one? Updating is more common than
the owner expects. Prefer it.

For a new page, choose the type with the ladder in `AGENTS.md` and say in one line
which you chose. **Do not ask which type to use.** If you get it wrong the owner runs
`make move`, which costs one command.

## 4. Write

- Update or create the page, following the instructions for its type.
- Add `sources: [sources/YYYY-MM-owner-notes.md]` to every page you touched.
- Attribute the claim inline where it is not obvious: "the event store runs on Postgres
  (owner, 2026-08-02)".
- Set `updated:` to today.
- Link the page from somewhere real. `make new TYPE=… TITLE=… FROM=content/…` does this for you.
- Create honest stubs for anything the note implies exists but says little about.

**Stop and ask only if the note contradicts what a page already says.** That is the one case
worth interrupting for: record both claims with their dates, do not resolve it yourself, and
raise it. Everything else — filing, naming, wording, which page — is your job.

## 5. Record and verify

- Add an entry at the top of `content/log.md` with `**Operation:** note`.
- Run `make lint`. Fix every error. Report the warnings.
- Report back in a few lines: what you wrote, where, and what you were unsure about.

## Judgement calls

**A note is often smaller than a page.** One sentence added to an existing page is a complete,
successful `/note` — do not inflate it into a new page to look productive.

**A note is sometimes bigger than it looks.** "We decided to drop the vendor" is a decision page
with a rejected option and a date, not a line on the org page. Write the page the note deserves.

**If the note is really a document** — the owner pasting three pages of meeting minutes — say so
and switch to `/ingest`, which will preserve it in `content/references/` properly. The dividing line is whether
losing the exact wording would lose anything.
