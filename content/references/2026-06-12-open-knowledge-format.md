---
title: Open Knowledge Format — summary of the specification
type: reference
description: Summary of the OKF v0.2 specification and its announcement, written from the originals on 2026-09-11.
created: 2026-06-12
resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
---

# Open Knowledge Format — summary of the specification

Source: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
Announcement: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
Publisher: Google Cloud. v0.1 published 2026-06-12; the spec text read here is v0.2, which does
not state its own publication date.
Summarised 2026-09-11 from the specification and the announcement.

## What it is

An open specification for packaging knowledge as a directory of Markdown files with YAML
frontmatter, cross-linked into a graph that agents can read. It is a format rather than a platform:
no SDK, no runtime, no account, no central registry, no manifest file. A bundle ships as a git
repository, a tarball or a mounted filesystem. As the spec puts it, if you can `cat` a file you can
read OKF, and if you can `git clone` a repository you can ship it.

The stated purpose is producer/consumer independence: any agent should be able to consume knowledge
from any producer without custom integration work.

## Structure

File path is concept identity. One concept per Markdown file, organised hierarchically by concept
type — datasets, tables, metrics, playbooks, runbooks, APIs, or anything else the producer chooses.
There is no mandatory top-level structure.

## Frontmatter

`type` is the only always-required key. A concept carrying nothing but `type` is fully conformant.
It is a short string naming the kind of concept.

Recommended: `title` (display name), `description` (single-sentence summary), `resource` (a URI for
the underlying asset), `tags` (a list).

Bundles may carry arbitrary extra frontmatter keys and arbitrary body sections without breaking
consumers.

## Reserved filenames

- `index.md` — directory listings, for progressive disclosure as an agent walks the hierarchy.
- `log.md` — chronological update history.

Both are optional and may appear at any level. Every other `.md` file is a concept.

## Cross-linking

Two link forms are permitted: bundle-relative absolute paths beginning with `/`, interpreted from
the bundle root, and ordinary relative Markdown paths. The absolute form is recommended for
stability when documents move. Links form a graph beyond the filesystem hierarchy, traversable by
humans and agents alike.

## Conformance (§11)

A bundle conforms if:

1. every non-reserved `.md` file contains parseable YAML frontmatter;
2. every frontmatter block contains a non-empty `type`;
3. reserved filenames follow their specified structure where present.

Consumers MUST NOT reject a bundle for missing optional fields, unknown `type` values, or broken
links.

## What v0.2 changed

Two breaking changes: `timestamp` is replaced by `generated.at` inside a `generated: { by, at }`
structure, and a body `# Citations` list is superseded by a frontmatter `sources` field.

Additions, all backward-compatible: provenance through `sources` with credibility signals
(`author`, `usage_count`, `last_modified`); trust metadata through `generated` and `verified`, where
`verified` records multiple events each with `by` and `at`, yielding trust tiers from unverified to
machine-confirmed to human-reviewed; lifecycle through `status` and `stale_after`; an actor
convention naming who created or verified something; and a new `Attested Computation` concept type
with `executor` and `attester` resources, plus `runtime`, `parameters` and `computation` fields.

## Relationship to the LLM Wiki pattern

OKF is described as the first standardised, vendor-neutral formalisation of the LLM-wiki idea:
where the gist describes an architecture, this defines a structural contract a bundle can be
checked against.
