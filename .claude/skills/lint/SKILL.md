---
name: lint
description: Semantic health check of the wiki — contradictions, staleness, orphans, gaps. Read-only.
---

# Lint

A health check of the whole wiki. **Read-only** — do not edit anything. Produce a report and let
the owner decide what to act on.

Start by running `make lint`. That covers the mechanical checks (frontmatter, broken links,
orphans, index freshness, misfiled pages, unprocessed inbox). Report its result in one line and
**do not repeat what it already checks**. Everything below is what a script cannot judge.

Run this monthly, or after a burst of ingestion.

## What to look for

**1. Contradictions.** The same fact stated two ways on two pages. Check especially:
- a system's owner or a project's status stated differently in different places
- a decision page whose `Status` disagrees with how a project page describes the work
- numbers, dates, and commitments repeated across pages
- a source page that flagged a contradiction which was never resolved

**2. Staleness.** Pages whose claims have quietly expired:
- `status: active` projects with no dated note in six months — finished, abandoned, or just unrecorded?
- statements about who owns or runs something, older than a year
- decisions whose *Revisit if* conditions now appear to be met
- anything phrased as "currently", "recently", "soon" — these are undated claims in disguise

**3. Structural drift.**
- pages that have grown past ~400 words and contain a section wanting to be its own page
- the same idea explained on several pages instead of one page others link to
- `content/topics/` accumulating pages that are really projects, systems, or decisions
- stubs that have been stubs for months — either fill them or admit they are not needed

**4. Missing links.** Entities mentioned by name across several pages with no page of their own,
and pages that should reference each other but do not.

**5. Coverage gaps.** Where the wiki is thin in a way that matters — a project with no decisions,
a system with an empty *How it fails*, a decision nothing links to.

**6. Unapplied conventions.** A rule in `.claude/rules/` that no page follows. Either the
rule is dead and should go, or the pages are wrong. Say which you think it is.

## Output

One Markdown report, most severe first:

| # | Severity | Page | Finding | Suggested fix |
|---|---|---|---|---|

Severity: 🔴 contradiction, wrong claim, or boundary breach · 🟡 staleness or gap · ⚪ polish.

Give a `path:line` reference and quote the offending text for every finding. If a category is
clean, say so in one line rather than omitting it. End with the single change you would make
first, and why.

## OKF v0.2 conformance reassessment

When the owner asks to assess or re-assess Open Knowledge Format (OKF) v0.2 conformance, work
through [okf-v0-2-checks.md](okf-v0-2-checks.md) — the register of numbered checks, each linked to
the clause of the specification it comes from. Read it first. It also fixes the vocabulary: the
five statuses an assessment may use, and what `REQUIRED` means as against everything else.

Do not restate the checks from memory and do not invent a numbering of your own. The register's IDs
are the join between one assessment and the next, and a re-run that renumbers them destroys the
only thing that makes two assessments comparable.

> Assess the bundle the owner names — `content/` unless they say otherwise — against every check in
> `.claude/skills/lint/okf-v0-2-checks.md`. State the scope and the date. Read the normative
> specification at the URL the register names; the repository's `content/references/` summary of it is not
> sufficient to settle a check. Produce one table: check ID, status, evidence, remediation. Cover
> every ID in the register, in register order, and add no rows of your own — if something needs
> checking that the register has no ID for, say so under the table and propose the ID. Use only the
> register's five statuses. Do not record `meets` against a consumer requirement without naming the
> consumer and the acceptance test that proves it; `partial` is the honest status for a behaviour
> that is implemented but untested. Keep `not adopted` and `n/a` apart. Give a precise remediation
> for everything that is not `meets`, and none for what is. Then state the §11 result — conformant
> or not, on the strength of the three REQUIRED checks alone — and run `make test`, `make lint` and
> `make build` before reporting it.

Write the result to the owner-specified destination. If none is specified, report it in the chat;
do not create or ingest a wiki page without the owner asking.

If a check turns out to be wrongly worded, or the specification gains a clause the register misses,
change the register and say so in the assessment. Adding a check is normal; renumbering is not.
