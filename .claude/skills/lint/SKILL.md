---
name: lint
description: Semantic health check of the wiki — contradictions, staleness, orphans, gaps. Read-only, except an OKF reassessment, which files its result.
---

# Lint

A health check of the whole wiki. **Read-only** — do not edit anything. Produce a report and let
the owner decide what to act on. The one exception is an OKF conformance reassessment, whose report
is filed as described at the end of this file.

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
through [okf-v0-2-checks.md](okf-v0-2-checks.md) — the register of numbered checks, each with a
short name and a link to the clause of the specification it comes from. Read it first. It also fixes
the vocabulary: the five statuses an assessment may use, and what `REQUIRED` means as against
everything else.

Do not restate the checks from memory and do not invent a numbering of your own. The register's IDs
are the join between one assessment and the next, and a re-run that renumbers them destroys the
only thing that makes two assessments comparable.

> Assess the bundle the owner names — `content/` unless they say otherwise — against every check in
> `.claude/skills/lint/okf-v0-2-checks.md`. Read the normative specification at the URL the register
> names; the repository's `content/references/` summary of it is not sufficient to settle a check.
> Cover every ID in the register exactly once, and add no rows of your own — if something needs
> checking that the register has no ID for, say so under *Register notes* and propose the ID. Use
> only the register's five statuses. Do not record `meets` against a consumer requirement without
> naming the consumer and the acceptance test that proves it; `partial` is the honest status for a
> behaviour that is implemented but untested. Keep `not adopted` and `n/a` apart. Give a precise
> remediation for everything that is not `meets`, and none for what is. State the §11 result —
> conformant or not, on the strength of the three mandatory checks alone. Run `make test`,
> `make lint` and `make build` before filing, and record their results under *Scope*.

### The report

A reader must learn what was checked without opening the register, and see the verdict before the
detail. So every row carries the check's **name** next to its ID, and the rows are grouped: the three
checks that decide conformance first, then one table per family.

```markdown
---
title: OKF v0.2 conformance assessment
type: reference
description: This wiki assessed against every check in the OKF v0.2 register on YYYY-MM-DD, keyed by check ID.
created: YYYY-MM-DD
---

# Open Knowledge Format v0.2 — conformance assessment

## Scope          → two-column table: Bundle, Assessed, Specification, Register, Validation
## Result         → conformant or not, on the three mandatory checks alone; then a table
                    Family | meets | partial | not adopted | deviates | n/a — one row per section
                    below, and a Total row; then every check whose status changed since the
                    previous assessment, as `ID` name: before → after
## Needs attention → one bullet per `partial` or `deviates` check: ID, name, remediation in one
                    line. "Nothing." if there is none
## Mandatory checks → OKF-CNF-01, OKF-CNF-02, OKF-CNF-03 — the §11 conformance criteria
## Bundle structure → OKF-BUN-*
## Concept documents → OKF-CPT-*
## Provenance     → OKF-SRC-*
## Trust          → OKF-TRU-*
## Lifecycle      → OKF-LIF-*
## Cross-linking and paths → OKF-LNK-*
## Reserved files → OKF-RSV-*
## Attested computations → OKF-CMP-*
## Consumer floor → OKF-CNF-04
## Versioning     → OKF-VER-*
## Register notes → only when the run changed the register, or found something it has no ID for
```

Every check section is one table, rows in register order:

| Check | Name | Status | Evidence | Remediation |
|---|---|---|---|---|
| [`OKF-BUN-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#3-bundle-structure) | Markdown directory tree | meets | … | |

**Check** links the clause the register links; **Name** is copied verbatim from the register;
**Status** is one of the five words and nothing more, since decoration breaks the diff. Every
register ID appears exactly once. The register itself sits outside the bundle, so name its path in
backticks rather than linking it.

### Filing it

Unless the owner asks for the result in the chat only, a reassessment is filed — it is the one thing
`/lint` writes, and it enters the wiki the way any document does:

1. Write the report to `content/references/YYYY-MM-DD-okf-v0-2-conformance-assessment.md`, dated the
   day of the run. It is an original from then on, immutable like every other.
2. **Never edit or replace an earlier assessment.** Compare against the newest one, which is what
   the *changed since* list under *Result* is for. Earlier originals and their source pages stay.
3. Ingest it by `.claude/skills/ingest/SKILL.md`: a source page in `content/sources/` whose
   description states the verdict and the counts, and whose *What it says* gives the verdict and the
   *Needs attention* list; the [Open Knowledge Format](../../../content/topics/open-knowledge-format.md)
   topic updated to point at the new assessment as the current one.
4. Add an `**Assessment:**` entry to `content/log.md` linking the source page, with the verdict and
   the counts on the same line.
5. Run `make lint`, and report the verdict, the counts and *Needs attention* to the owner, with a link.

If a check turns out to be wrongly worded, or the specification gains a clause the register misses,
change the register and say so in the assessment. Adding a check is normal; renumbering is not.
