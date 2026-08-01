---
agent: agent
description: Answer a question from the wiki with citations, and offer to keep the answer as a page.
---

# Query

Answer a question using the wiki. The point is not just the answer — it is knowing **how much
the wiki actually supports it**.

## 1. Search properly

Do not answer from memory of this conversation. Search the files:

- Start with `wiki/index.md` to see what exists.
- Grep for the proper nouns and key terms in the question, including likely synonyms.
- Follow links out from whatever you find — the answer is often one hop away.
- Check `wiki/sources/` too. Something may have been ingested but not yet promoted to a page.

## 2. Answer

Structure:

> **Short answer** — one or two sentences.
>
> **Detail** — what the wiki says, with a link on every claim:
> "The migration was paused in March ([Acme Migration](wiki/projects/acme-migration.md))."
>
> **Confidence** — one of:
> - **Well supported** — several pages or a primary source agree
> - **Single source** — one page says this, name it
> - **Inferred** — the wiki does not say this; you are joining two facts. Show the join.
> - **Not in the wiki** — say so plainly and stop

**Never fill a gap with general knowledge without labelling it.** If you know something from
outside the wiki that is relevant, mark it clearly as outside knowledge, separately from what
the wiki says. Conflating the two destroys the wiki's value as a record.

If pages contradict each other, say so and give both, with dates. Do not average them.

## 3. Offer to keep it

If the answer took real work — several pages joined, a contradiction untangled, a conclusion
that is not written anywhere — offer to write it down:

> This isn't recorded anywhere. Want me to add it as `wiki/topics/…`?

Only if the owner agrees. Then follow the normal page rules, add a log entry, and run `make lint`.

An answer you had to reconstruct twice should have been a page the first time.

## 4. Note the gaps

If answering was hard because the wiki is thin somewhere, say where. That is a prompt for the
next ingest, and it is information the owner cannot get any other way.
