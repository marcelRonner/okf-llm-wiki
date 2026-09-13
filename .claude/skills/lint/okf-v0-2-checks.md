# OKF v0.2 — the check register

The numbered checks an OKF conformance assessment works through, each linked to the clause of the
specification it comes from. This file holds the **checks**; an assessment holds the **findings**
and refers to a check by its ID. Used by the reassessment prompt in [SKILL.md](SKILL.md#okf-v02-conformance-reassessment).

**Normative source:** [OKF SPEC.md v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).
Every `§` link below points into it. `content/references/2026-06-12-open-knowledge-format.md` in this repo is a
**summary** of that specification, not the normative text — it is too short to settle a check, and
several checks here rest on clauses it does not mention. Its wiki page is
[Open Knowledge Format](../../../content/topics/open-knowledge-format.md). There is no offline copy
of the full text, so an assessment reads the URL.

## The IDs

`OKF-<family>-<nn>`, where the family follows the specification's own division:

| Family | Covers | Spec |
|---|---|---|
| `BUN` | Bundle structure | §3 |
| `CPT` | Concept documents and frontmatter | §2, §4 |
| `SRC` | Provenance | §5.1 |
| `TRU` | Trust and the actor convention | §5.2, §5.3, §7 |
| `LIF` | Lifecycle | §5.4, §5.5 |
| `LNK` | Cross-linking and paths | §6 |
| `RSV` | Reserved files | §8, §9 |
| `CMP` | Attested computations | §10 |
| `CNF` | The conformance criteria and the consumer floor | §11 |
| `VER` | Versioning | §12 |

**An ID is permanent.** It identifies one check for the life of the register, so that two
assessments a year apart can be diffed row by row. Never renumber to close a gap, never reuse a
retired number, and add a new check at the end of its family. If a check's wording has to change,
change it in place and say so in the assessment that first uses the new wording — the ID is the
promise, the wording is the current best statement of it.

An assessment cites the register version it ran against: the date of the newest entry below.
Last changed 2026-09-12.

## Levels

`REQUIRED` marks the three §11 criteria, and nothing else. Failing one makes the bundle
non-conformant; failing anything else does not. `format` marks a definition of the format model
rather than an imperative. The rest are the specification's own RFC 2119 keywords, with the party
they bind: a `consumer MUST` is a promise about software reading the bundle, and cannot be
discharged by inspecting the bundle — it needs an acceptance test against the consumer in scope.

## Status vocabulary for an assessment

One of five, and no others — a checklist whose status column has a private vocabulary per row
cannot be diffed:

| Status | Means |
|---|---|
| `meets` | Satisfied, with evidence named. For a consumer requirement, name the consumer and the test. |
| `partial` | Satisfied in part, or satisfied but unproven — say which half is missing. |
| `not adopted` | An optional feature deliberately unused. Valid; carries no defect. |
| `deviates` | A SHOULD or recommendation knowingly not followed. Say what is gained. |
| `n/a` | The bundle has no concept that needs the feature, so there is nothing to satisfy. |

`not adopted` and `n/a` are kept apart on purpose: the first is a choice that could be revisited,
the second is a fact about the bundle.

## Bundle structure

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-BUN-01` | The bundle is a directory tree of Markdown files, organised however the producer likes; no mandatory top-level structure. | format | [§3](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#3-bundle-structure) | Inspect the tree. |
| `OKF-BUN-02` | `index.md` and `log.md` are not used for concept documents. Every other `.md` file is a concept. | producer MUST NOT | [§3.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#31-reserved-filenames) | List files named `index.md` or `log.md` and confirm each is a listing or a history, not a concept. |

## Concept documents

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-CPT-01` | Every concept is a UTF-8 Markdown file: a `---`-delimited YAML frontmatter block, then a body. | format | [§4](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#4-concept-documents) | Parse every non-reserved file as UTF-8 and split its frontmatter. |
| `OKF-CPT-02` | One concept per file. The concept ID is the file's bundle path with `.md` removed. | format | [§2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#2-terminology) | Look for files packing several unrelated concepts, and for paths that will not survive as identifiers. |
| `OKF-CPT-03` | `type` is present and non-empty. It is the only always-required key; a concept carrying just `type` conforms. | REQUIRED (see `OKF-CNF-02`) | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | Read `type` from every frontmatter block. |
| `OKF-CPT-04` | Type values are descriptive and self-explanatory. They are not centrally registered. | producer SHOULD | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | Read the set of type values in use and judge whether each is self-explanatory to a stranger. |
| `OKF-CPT-05` | A consumer tolerates an unknown `type`, typically by treating it as a generic concept. | consumer MUST | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | Feed the consumer a concept with a type it has never seen and confirm it loads. |
| `OKF-CPT-06` | `title` gives a human-readable display name. | recommended | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | Check frontmatter. |
| `OKF-CPT-07` | `description` is a single sentence summarising the concept. | recommended | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | Check frontmatter, and read the descriptions — a paragraph in the field is a miss even where the key is present. |
| `OKF-CPT-08` | `resource` is a URI identifying the underlying asset, on concepts that describe one. Absent on abstract concepts. | recommended | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | Separate asset-bound from abstract concepts, then check only the former. |
| `OKF-CPT-09` | `tags` is a YAML list of short strings. OKF specifies no tag-aggregation file; a consumer synthesises one. | recommended | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter), [§3.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#31-reserved-filenames) | Check the shape is a list, not a string. |
| `OKF-CPT-10` | Extra producer-defined frontmatter keys are allowed; a consumer preserves them when round-tripping and never rejects for them. | producer MAY / consumer MUST | [§4.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#41-frontmatter) | Feed the consumer a concept with an unknown key and confirm it loads and the key survives. |
| `OKF-CPT-11` | The body favours structural Markdown, and uses the conventional headings `# Schema`, `# Examples` and `# Computation` where they apply. | producer SHOULD | [§4.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#42-body) | Only applies where a concept has an asset schema, usage examples, or a computation. |

## Provenance

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-SRC-01` | `sources` is a list of mappings, and every entry has `resource` — a followable artifact, or a scope descriptor it names in prose. | REQUIRED within an entry | [§5.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | Reject a bare string and an entry with no `resource`. |
| `OKF-SRC-02` | A source the body cites has a stable `sources[].id`, with a Markdown footnote whose label is that ID. | SHOULD when the body attributes claims | [§5.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | Check for footnote-level attribution; if there is none, the check is about whether the bundle needs it. |
| `OKF-SRC-03` | `sources[].title` labels the source for a reader. | optional | [§5.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | Check frontmatter. |
| `OKF-SRC-04` | The credibility signals `author`, `usage_count` and `last_modified` are recorded where known — objective facts, never a score. | optional | [§5.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | Confirm any signal present is measured, not estimated. Inventing one is worse than omitting it. |
| `OKF-SRC-05` | `usage_window` frames every `usage_count` with a `{ from, to }` datetime range. | SHOULD when `usage_count` is used | [§5.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | Applies only where `usage_count` appears. |
| `OKF-SRC-06` | Lineage is expressed through links, not a lineage field: a `resource` pointing at another concept is itself the derivation edge. | format | [§5.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#51-provenance-sources) | Confirm internal sources are cited as paths a consumer can recurse into. |

## Trust

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-TRU-01` | `generated` is a mapping whose `by` is an actor and whose `at` is the content's last meaningful change. `by` is required within it. | SHOULD when present | [§5.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#52-trust-generated-and-verified) | Validate the mapping's shape and the datetime. |
| `OKF-TRU-02` | `verified` is a list of events, each with an actor `by` and a datetime `at`. Several entries record independent checks; recency is the latest `at`. | optional | [§5.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#52-trust-generated-and-verified) | Validate each event, and confirm every entry records something that actually happened. |
| `OKF-TRU-03` | A bare `verified` mapping is read as a one-element list. | consumer MUST | [§5.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#52-trust-generated-and-verified), [§11](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | Feed the consumer both spellings and confirm they are read the same way. |
| `OKF-TRU-04` | A consumer derives the trust tier from `verified`: absent ⇒ unverified, non-`human:` actors only ⇒ machine-confirmed, a `human:<id>` actor ⇒ human-reviewed. | consumer SHOULD | [§5.3](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#53-trust-tiers) | Exercise all three tiers against the consumer. Tiers are advisory, never access control. |
| `OKF-TRU-05` | Every actor-valued field uses `<producer>/<version>`, `human:<id>` or `process:<id>`. Human-authored or human-confirmed content MUST use the `human:` prefix. | producer MUST for `human:` | [§7](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#7-actor-convention) | Validate `generated.by` and every `verified[].by`; a human sign-off written any other way is invisible to tier derivation. |

## Lifecycle

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-LIF-01` | `status`, when present, is `draft`, `stable` or `deprecated`. Absent means `stable`. | optional | [§5.4](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#54-lifecycle-status) | Reject any other value. Confirm the absent case is read as stable, not as unknown. |
| `OKF-LIF-02` | `stale_after` is an absolute ISO 8601 datetime with an explicit UTC offset, and the concept is stale once `now >= stale_after`. | optional | [§5.5](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#55-lifecycle-stale_after) | Reject a bare date or a relative TTL, and test the boundary instant, not a day either side of it. |

## Cross-linking and paths

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-LNK-01` | Concepts link with standard Markdown, in one of two forms: bundle-relative absolute beginning with `/`, or an ordinary relative path. | format | [§6.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#61-links-between-concepts) | Inspect the link forms in use. |
| `OKF-LNK-02` | The bundle-relative absolute form is preferred, because it survives a document moving within its subdirectory. | recommended | [§6.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#61-links-between-concepts) | If relative links are used instead, the check is whether the reason is written down. |
| `OKF-LNK-03` | A consumer tolerates a broken link — an unresolvable target is not-yet-written knowledge, not malformed input. | consumer MUST | [§6.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#61-links-between-concepts), [§11](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | Feed the consumer a concept linking to a missing file and confirm it loads. A producer may still refuse to publish one. |
| `OKF-LNK-04` | Every path-valued field — `resource`, `sources[].resource`, `computation`, `executor.resource`, `attester.resource` — holds an absolute URL, a bundle-relative path, or a relative path. | format | [§6.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#62-path-valued-fields) | Resolve each one. A `sources[].resource` that is a scope descriptor is exempt — it is not a path. |
| `OKF-LNK-05` | External material, run instructions and code mirrored into the bundle live under `references/`. | convention | [§6.3](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#63-the-references-convention) | A naming convention only; another directory name is not a defect. |

## Reserved files

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-RSV-01` | `index.md`, where present, carries no frontmatter — except a bundle-root one, which may carry `okf_version` — and lists entries as links with descriptions under one or more headings. | REQUIRED if present (see `OKF-CNF-03`) | [§8](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#8-index-files) | Applies only to a file named exactly `index.md`. A differently named landing page is a concept document, and is checked as one. |
| `OKF-RSV-02` | `log.md`, where present, is a flat list of entries grouped newest-first under `## YYYY-MM-DD` headings. | REQUIRED if present (see `OKF-CNF-03`) | [§9](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#9-log-files) | Check heading form, descending order, and that each group holds list items. Entry prose is free-form; the bold leading word is a convention. |

## Attested computations

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-CMP-01` | A `type: Attested Computation` concept carries `runtime`, typed `parameters`, an `executor` with a `receipt` contract, an `attester`, and exactly one computation — an inline `# Computation` fence or a `computation` path, not both. | REQUIRED for that type | [§10.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#102-contract-fields) | Applies only where such a concept exists. |
| `OKF-CMP-02` | The attester is deterministic, runs without an LLM, and a consumer surfaces a failing attestation rather than dropping it. | SHOULD where computations exist | [§11](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance), [§10.6](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#106-verification-versus-attestation) | Exercise a failing attestation end to end and confirm the failure reaches the reader. |

## Conformance

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-CNF-01` | Every non-reserved `.md` file in the tree contains a parseable YAML frontmatter block. | **REQUIRED §11.1** | [§11](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | Walk every file in the bundle, not just the ones the producer's own tooling knows about. |
| `OKF-CNF-02` | Every frontmatter block contains a non-empty `type` field. | **REQUIRED §11.2** | [§11](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | The same walk. Generated files count. |
| `OKF-CNF-03` | Every reserved filename present follows §8 or §9 respectively. | **REQUIRED §11.3** | [§11](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | See `OKF-RSV-01` and `OKF-RSV-02`. |
| `OKF-CNF-04` | A consumer does not reject a bundle for a missing optional field, an unknown `type`, an unknown extra key, a broken link, or a missing `index.md`. | consumer MUST | [§11](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#11-conformance) | One acceptance test per clause, against the consumer in scope. This is the floor the format rests on: it is what lets a bundle be partial and still useful. |

## Versioning

| ID | Check | Level | Spec | How to check |
|---|---|---|---|---|
| `OKF-VER-01` | The bundle may declare `okf_version: "0.2"` in a bundle-root `index.md` — the only place frontmatter is permitted in an index file. | optional | [§12](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#12-versioning) | Depends on `OKF-RSV-01`: without a root `index.md` there is nowhere to declare it. |
| `OKF-VER-02` | A consumer meeting a version it does not understand attempts best-effort consumption rather than refusing the bundle. | consumer SHOULD | [§12](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md#12-versioning) | Feed the consumer a declared version from the future. |
