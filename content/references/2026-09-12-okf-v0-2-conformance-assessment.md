---
title: OKF v0.2 conformance assessment — 2026-09-12
type: reference
description: This wiki assessed against every check in the OKF v0.2 register on 2026-09-12, keyed by check ID.
created: 2026-09-12
---

# Open Knowledge Format v0.2 — conformance assessment

**Assessed:** 2026-09-12
**Scope:** the bundle at `content/`, which since 2026-09-12 includes the originals in
`content/references/`. The repository around it — scripts, instructions, templates, the built
site — is outside the bundle.
**Specification:** [OKF SPEC.md v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md), read at that URL.
**Checks:** the register at [`.claude/skills/lint/okf-v0-2-checks.md`](../../.claude/skills/lint/okf-v0-2-checks.md), version 2026-09-12 — all 41 IDs, in register order. Each ID below links to the clause of the specification it comes from.
**Validation:** `make test` → 5 tests OK · `make lint` → no errors, 3 W4 length warnings ·
`make build` → 31 pages · `hugo --panicOnWarning` → clean.

## Result

**Conformant with OKF v0.2 as of 2026-09-12**, on the three REQUIRED checks `OKF-CNF-01`,
`OKF-CNF-02` and `OKF-CNF-03` alone.

26 meets · 1 partial · 7 not adopted · 1 deviates · 6 n/a.

| Check | Status | Evidence | Remediation |
|---|---|---|---|
| [`OKF-BUN-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#3-bundle-structure) | meets | The bundle is `content/`: a directory tree of 24 Markdown files — pages under typed folders, originals under `references/`. |  |
| [`OKF-BUN-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#31-reserved-filenames) | meets | Only `content/log.md` uses a reserved name, and it is the history. There is no `index.md`; Hugo's `_index.md` is not a reserved name. |  |
| [`OKF-CPT-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#4-concept-documents) | meets | All 24 files parse as UTF-8 with a delimited frontmatter block, including the originals, which gained headers on 2026-09-12 (E7 criterion 1). |  |
| [`OKF-CPT-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#2-terminology) | meets | One concept per file; the path is the ID. `make move` rewrites every link when a page's path must change. |  |
| [`OKF-CPT-03`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | Non-empty `type` on 24/24 (E7 criterion 2). |  |
| [`OKF-CPT-04`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | Seven values: `source`, `topic`, `reference`, `section`, `index`, `tags`, `log`. Each names what the file is; E2 rejects a page type not declared in `schema.yml`. |  |
| [`OKF-CPT-05`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | Local reader: `make test` → `test_unknown_type_and_extension_are_consumable` loads `type: Future Concept`. | Test any other consumer before relying on it. |
| [`OKF-CPT-06`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | `title` on 24/24; E1 requires it on pages. |  |
| [`OKF-CPT-07`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | `description` on 24/24; W2 caps page descriptions at 200 characters, so a paragraph cannot creep in. |  |
| [`OKF-CPT-08`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | All 5 source pages carry `resource`. Two originals carry the public URL they were summarised from; the other three are themselves the asset and rightly carry none. Abstract topics omit it. W8 guards source pages. |  |
| [`OKF-CPT-09`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | `tags` on all 10 concept pages, every one a YAML list. Originals and generated pages omit them. W5 catches near-duplicate tags. |  |
| [`OKF-CPT-10`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | meets | Local reader: the same test preserves an unknown `custom_extension` key. Hugo builds pages carrying the producer-defined keys. |  |
| [`OKF-CPT-11`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#42-body) | n/a | No concept has an asset schema, usage examples, or a computation. | Use `# Schema`, `# Examples` or `# Computation` if such a page is written. |
| [`OKF-SRC-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | meets | Every `sources` entry is a mapping with `resource`; E4 rejects a bare string or a missing `resource`. |  |
| [`OKF-SRC-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | not adopted | No footnotes anywhere; attribution is page-level through `sources`. | Add an `id` and a matching footnote where one claim, not the whole page, needs the citation. |
| [`OKF-SRC-03`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | not adopted | Only `resource` is used in `sources` entries. | Add `title` where a path does not describe its source. |
| [`OKF-SRC-04`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | not adopted | No `author`, `usage_count` or `last_modified` on any entry. | Record only measured signals. An invented one is worse than none. |
| [`OKF-SRC-05`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | n/a | No `usage_count` exists to frame. |  |
| [`OKF-SRC-06`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | meets | Internal sources are cited as bundle paths (`sources/…`), so the derivation edge is in the graph and a consumer can recurse — the 2026-09-11 checklist source page cites the specification's. |  |
| [`OKF-TRU-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#52-trust-generated-and-verified) | meets | `generated` on all 10 concept pages: `by: wiki-keeper/1.0`, `at` an explicit-UTC datetime, stamped by `make index`; E7 validates both. Originals carry none, since nothing generated them here. |  |
| [`OKF-TRU-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#52-trust-generated-and-verified) | not adopted | `verified` on 0 of 24. Valid: the whole bundle sits at the unverified tier. | The owner adds an entry on reading a page and finding it true. `AGENTS.md` forbids the assistant from writing it; W9 raises the question after 365 days. |
| [`OKF-TRU-03`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#52-trust-generated-and-verified) | meets | Local reader: `Page.verified_events()` in `scripts/wikilib.py`, proven by `make test` → `test_bare_verified_mapping_reads_as_a_one_element_list`, which fails `2 != 1` when the normalisation is removed. The linter uses the same function. |  |
| [`OKF-TRU-04`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#53-trust-tiers) | not adopted | No trust-tier derivation or presentation anywhere. | Build it only if a reader needs the distinction; while `OKF-TRU-02` is unused every page is one tier. |
| [`OKF-TRU-05`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#7-actor-convention) | meets | The only actor value in use is `wiki-keeper/1.0`, matching `<producer>/<version>`; E7 enforces the convention on `generated.by` and `verified[].by`. | The `human:` prefix is accepted but never exercised. The first `verified` entry must use it, or the sign-off is invisible to tier derivation. |
| [`OKF-LIF-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#54-lifecycle-status) | meets | No page sets `status`, so all read as `stable`. E7 rejects any value outside the three. |  |
| [`OKF-LIF-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#55-lifecycle-stale_after) | not adopted | No page uses it. The validator is ready: E7 rejects a bare date or a missing offset, W9 warns once the instant passes. | Set it on the agent-instruction-formats source page, whose own *Unresolved* section says nothing re-checks the vendor behaviour it dates. |
| [`OKF-LNK-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#61-links-between-concepts) | meets | Every link in the bundle is a standard relative Markdown link. Three climb out of it to repository files — the log to `README.md`, the 2026-09-11 checklist original to the `lint` skill, and this assessment to the check register — which a consumer handed only the bundle will see as broken, and must tolerate (`OKF-LNK-03`). |  |
| [`OKF-LNK-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#61-links-between-concepts) | deviates | No bundle-absolute links, by choice: `/topics/x.md` resolves neither in Obsidian nor in an editor's preview. One file readable in both places is what is gained. | Recorded as deliberate on the Open Knowledge Format topic page; revisit if Obsidian gains support. |
| [`OKF-LNK-03`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#61-links-between-concepts) | meets | Local reader: `make test` → `test_broken_relative_link_is_read_without_rejection`. E3 refusing to *publish* a broken link is producer policy, not consumer rejection. |  |
| [`OKF-LNK-04`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#62-path-valued-fields) | meets | All 7 `resource` values resolve, and none leaves the bundle: the local ones are `../references/…` from a source page. W8 checks `resource`, E4 checks `sources[].resource`. |  |
| [`OKF-LNK-05`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#63-the-references-convention) | meets | The originals live in `content/references/`, the directory §6.3 names, since 2026-09-12. |  |
| [`OKF-RSV-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#8-index-files) | n/a | No `index.md` exists. `content/_index.md` is a concept document with `type: index` and is checked as one. | A root `index.md` added for OKF consumers must carry no frontmatter but `okf_version`. |
| [`OKF-RSV-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#9-log-files) | meets | `content/log.md`: `## YYYY-MM-DD` headings, newest first, list items and indented continuations only. E7 checks all four, and exercised them on the 2026-09-12 restoration of the full log. Its frontmatter is an addition §9 does not forbid, unlike §8 for `index.md`. |  |
| [`OKF-CMP-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#102-contract-fields) | n/a | No `Attested Computation` concept. |  |
| [`OKF-CMP-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | n/a | No computation, executor or attester. |  |
| [`OKF-CNF-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | meets | REQUIRED. 24/24 files parse. The E7 walk reads every file, including generated section pages and originals. |  |
| [`OKF-CNF-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | meets | REQUIRED. Non-empty `type` on 24/24. Removing one from an original fails E7 — tested on 2026-09-12. |  |
| [`OKF-CNF-03`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | meets | REQUIRED. `log.md` is the only reserved file present, and conforms — see `OKF-RSV-02`. |  |
| [`OKF-CNF-04`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | partial | Four of five clauses have tests against the local reader: missing optional fields, unknown type, unknown key, broken link. The missing-`index.md` clause holds — the bundle has none and the reader never looks for one — but nothing asserts it. | Assert it in `test_okf_consumer.py`, or record it as untestable for a reader that has no index concept. |
| [`OKF-VER-01`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#12-versioning) | not adopted | No root `index.md`, so nowhere to declare it. Depends on `OKF-RSV-01`. |  |
| [`OKF-VER-02`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#12-versioning) | n/a | Nothing in the repository reads `okf_version`. |  |

## Since the previous run

The same register was first run earlier on 2026-09-12, before three of its findings were acted
on. That run was reported in conversation and not filed. Three checks changed:

- `OKF-TRU-03` partial → meets — the acceptance test was added.
- `OKF-LNK-04` partial → meets — the originals moved inside the bundle, so no `resource` escapes it.
- `OKF-LNK-05` not adopted → meets — their directory was renamed from `raw/` to `references/`.

Against the unnumbered [2026-09-11 checklist](2026-09-11-okf-v0-2-conformance-checklist.md), the
§11 result is unchanged. The difference is coverage: twelve checks it had no row for, and a status
vocabulary two assessments can be compared in.

## Not covered by the register

Nothing surfaced that needs a new check ID.

One thing worth recording that the register deliberately does not judge: moving the originals
inside the bundle required editing evidence twice. Each Markdown original gained a frontmatter
header, and one link in the 2026-09-11 checklist original was rewritten to follow its move, at the
owner's explicit instruction. Both are recorded in `content/log.md`. The conformance result does
not depend on either being the right call.
