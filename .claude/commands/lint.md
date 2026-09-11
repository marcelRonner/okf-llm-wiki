---
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
