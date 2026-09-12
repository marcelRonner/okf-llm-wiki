---
title: OKF v0.2 conformance checklist — the 2026-09-11 assessment
type: reference
description: This wiki assessed against OKF v0.2 on 2026-09-11, before the checks had IDs.
created: 2026-09-11
---

# Open Knowledge Format v0.2 — wiki conformance checklist

**Assessed:** 2026-09-11  
**Specification:** https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md  
**Scope:** the Markdown bundle under `content/`. The repository’s code, raw material, generated
site, and assistant configuration are outside the assessed bundle.

## How to read this checklist

**Required** items are the three conditions in OKF v0.2 §11. Failure of any one makes the bundle
non-conformant. **Recommended** and **optional** items do not affect conformance, but show whether
the bundle exposes the provenance, trust, lifecycle, and navigation information an OKF consumer
can use. “Not applicable” means the repository has no concept that needs the feature, rather than
that the feature is missing.

## Reassessment method

This checklist was produced using the reusable [OKF v0.2 conformance reassessment prompt](../.claude/skills/lint/SKILL.md#okf-v02-conformance-reassessment) in the `lint` skill. The prompt requires the
specification source, a declared scope, a normative-level table, evidence-backed findings, and the
`make test`, `make lint`, and `make build` validation sequence. Re-run that prompt when the bundle
or the assessment scope changes.

| Area | Check parameter | Level | Repository finding as of 2026-09-11 | Status | How to check |
|---|---|---|---|---|---|
| Bundle | A hierarchical collection of Markdown documents forms the bundle. | Format model | `content/` is a Markdown directory tree. | Meets | Inspect `content/`. |
| Bundle | Files are UTF-8 Markdown. | Required for concept documents | All current `content/**/*.md` files are readable as UTF-8 by the wiki tooling. | Meets | Parse every Markdown file as UTF-8. |
| Concepts | One concept is represented by one Markdown file; its path is its concept ID. | Format model | Pages are individual Markdown files organised by type folders. | Meets | Review page layout and avoid packing unrelated concepts into one file. |
| Frontmatter | Every non-reserved `.md` file begins with parseable YAML frontmatter. | **Required, §11.1** | The E7 linter walk reports no violations. | Meets | Run `make lint`; inspect all non-reserved Markdown files. |
| Frontmatter | Every frontmatter block has a non-empty `type`. | **Required, §11.2** | Content pages and Hugo `_index.md` section pages carry a non-empty type. | Meets | Run `make lint`; inspect every frontmatter block. |
| Types | Consumers tolerate unknown type values; producers use descriptive values. | Consumer MUST / producer SHOULD | Wiki-specific values such as `topic` and `section` are descriptive; this is a consumer interoperability requirement, not a property this repository can prove alone. | Partly checkable | Test the intended consumer with an unknown type. |
| Frontmatter | `title` is a human-readable display name. | Recommended | All present concept pages have `title`. | Meets | Check frontmatter. |
| Frontmatter | `description` is a one-sentence summary. | Recommended | All present concept pages have `description`; three long pages trigger only the local body-length warning, not a description warning. | Meets | Run `make lint`; review descriptions for one-sentence form. |
| Frontmatter | `resource` identifies the underlying asset when a concept describes one. | Recommended | Every source page has a public URL or a path to its raw original; abstract topic pages appropriately omit it. | Meets | Run `make lint`; review source-page `resource` fields. |
| Frontmatter | `tags` is a YAML list of short strings for cross-cutting categorisation. | Recommended | Concept pages use YAML tag lists; generated index, tag, log, and section pages omit tags. | Meets | Inspect frontmatter and generated tags view. |
| Extensions | Unknown extra frontmatter keys and arbitrary Markdown body sections are preserved and tolerated by consumers. | Consumer MUST / producer MAY | `make test` verifies the wiki’s reader accepts an unknown type and preserves an unknown frontmatter key. Hugo also builds the existing producer-defined metadata. | Meets for local consumers | Run `make test` and `make build`; test other consumers before using them. |
| Sources | `sources` is a list of mappings; each mapping has `resource`. | SHOULD when present | Every present `sources` entry uses `- resource: ...`; E4 rejects a bare string or an entry with no resource. | Meets | Run `make lint`. |
| Sources | A source cited per claim has a stable `sources[].id`, with a matching Markdown footnote label. | SHOULD when body attribution is used | This wiki cites source pages at page level and does not use per-claim footnotes or source IDs. That is valid, but fine-grained attribution is unavailable. | Not adopted | Add stable IDs and matching footnotes where individual claims need attribution. |
| Sources | Optional credibility signals (`author`, `usage_count`, `last_modified`, `usage_window`) are recorded where known. | Optional | No `sources` entry carries these signals. | Not adopted | Add only objective, known signals; do not invent them. |
| Trust | `generated` is a mapping with an OKF actor in `by` and an explicit-offset ISO 8601 datetime in `at`. | SHOULD when present | Generated metadata uses `wiki-keeper/1.0` and UTC timestamps; E7 validates the shape when present. | Meets | Run `make lint`. |
| Trust | `verified` is a mapping or list of mappings, each with an OKF actor and explicit-offset ISO 8601 datetime. | Optional | No page is verified. This is valid and denotes the unverified trust tier; owner confirmation has not been recorded. | Not adopted | Record only actual verification events, using `human:<id>` for a human review. |
| Trust | A consumer derives unverified, machine-confirmed, and human-reviewed trust tiers from `verified`. | Consumer SHOULD | The wiki has no trust-tier presentation layer. The metadata validator accepts the required event shapes, but no tier derivation is implemented. | Not adopted | Add and test a consumer-facing trust-tier view if the information is needed. |
| Lifecycle | `status`, if supplied, is `draft`, `stable`, or `deprecated`; absent means stable. | Optional | No content page currently sets `status`; absent therefore means stable. The local linter rejects unsupported values when supplied. | Meets | Run `make lint`; inspect status values. |
| Lifecycle | `stale_after`, if supplied, is an absolute ISO 8601 datetime with an explicit UTC offset; stale when `now >= stale_after`. | Optional | No page currently uses `stale_after`. E7 now rejects a non-datetime or missing-offset value and W9 reports a date that has passed. | Not adopted / validator meets | Add explicit-offset datetimes and test stale-at-boundary behaviour when the field is used. |
| Links | Concept links use standard Markdown, either relative or bundle-relative absolute paths. | Permitted | Editorial links are relative standard Markdown paths. | Meets | Inspect links; run `make lint` for the local no-broken-link policy. |
| Links | Bundle-relative absolute links are preferred because moves do not change them. | Recommended | The wiki deliberately uses relative links for Obsidian compatibility. | Does not follow recommendation | Use `/path/to/page.md` only if the publishing and editing tools support it. |
| Links | Consumers tolerate broken links. | Consumer MUST | `make test` verifies that the wiki reader loads a concept carrying a broken relative link. The producer linter intentionally rejects broken editorial links. | Meets for local reader | Run `make test`; test other consumers before using them. |
| Reserved files | `index.md`, when present, has no frontmatter except optional root `okf_version`, and uses heading-grouped Markdown lists of links with descriptions. | **Required if present, §8 and §11.3** | No `index.md` exists in `content/`; Hugo uses `_index.md`, which is a normal concept document rather than OKF’s reserved filename. | Not applicable | If adding `index.md`, validate its reserved-file structure. |
| Reserved files | `log.md`, when present, is a newest-first flat list grouped under `## YYYY-MM-DD` headings. | **Required if present, §9 and §11.3** | `content/log.md` has date-only newest-first headings and only list items within each date group. E7 rejects a missing group, malformed date, ascending order, free-standing prose, and non-list entries. | Meets | Run `make lint`; inspect the log after edits. |
| Computation | A `type: Attested Computation` concept supplies `runtime`, typed `parameters`, executor and attester contracts, and exactly one computation representation when applicable. | Required for that type | No attested-computation concept exists. | Not applicable | Validate only when such a concept is added. |
| Computation | Attesters are deterministic and consumers surface a failing attestation. | SHOULD when computation concepts exist | No computation or attester exists. | Not applicable | Test executor, receipt, attester, and failure-display flows. |
| Versioning | The bundle-root reserved `index.md` may declare `okf_version: "0.2"`. | Optional | There is no reserved root `index.md`, so no version declaration is present. | Not adopted | Add it only with an OKF-formatted root `index.md`. |
| Consumer behaviour | Missing optional families, unknown types/keys, broken links, and missing indexes do not cause rejection. | Consumer MUST | `make test` covers the local reader’s handling of absent optional metadata, unknown type and key values, and broken links. A missing optional index is inherent to the current bundle, which has no reserved `index.md`. | Meets for local reader | Run `make test`; add equivalent acceptance tests for any future importer. |

## Required-conformance result

The bundle is **conformant with OKF v0.2 as of 2026-09-11**. The E7 check confirms parseable
frontmatter on each non-reserved Markdown file, a non-empty `type` in every frontmatter block, and
the required structure of the reserved `content/log.md` file.

## Priority remediation order

1. If `stale_after` is adopted, set it as an ISO 8601 datetime with an explicit UTC offset and
   add a boundary test for its intended lifecycle.
2. Add source IDs, Markdown footnotes, and credibility signals only where individual claims need
   that additional evidence.
3. Add a trust-tier presentation layer if readers need to distinguish unverified, machine-confirmed,
   and human-reviewed content.
4. Add equivalent acceptance tests before adopting another importer, transformer, or publisher.
