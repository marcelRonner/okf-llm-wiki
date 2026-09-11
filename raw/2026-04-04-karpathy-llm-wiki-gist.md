# LLM Wiki — summary of Andrej Karpathy's gist

Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
Author: Andrej Karpathy. Created 2026-04-04.
Summarised 2026-09-11 from the gist itself. The gist is deliberately abstract, so that an agent
can instantiate a version fitted to a particular setup and domain.

## The problem it names

The ordinary way of using an LLM over documents is RAG: upload files, retrieve relevant chunks at
query time, generate an answer. The LLM rediscovers the knowledge from scratch on every question,
so nothing accumulates. A question needing five documents synthesised makes the model find and
piece together the same fragments again.

## The proposal

The LLM maintains a persistent wiki that sits between the reader and the raw sources, and queries
run against the wiki rather than the sources. The wiki is "a persistent, compounding artifact":
every source added and every question asked makes it richer, with the synthesis already done
rather than re-derived.

The stated economics: in a human wiki "the maintenance burden grows faster than the value", which
is why most die. With an LLM doing the maintenance, "the cost of maintenance is near zero".

## Three layers

- **Raw sources** — immutable documents: articles, papers, PDFs, images. The LLM reads them and
  never modifies them. Assets live alongside.
- **The wiki** — LLM-generated Markdown organised by category: summaries, entity pages, concept
  pages, cross-references. The LLM owns writing this layer entirely.
- **The schema** — a configuration file recording the structure conventions, the workflows and the
  operational procedures that guide the maintenance work.

## Folder structure

```
project/
├── raw/                 curated source documents, immutable
│   └── assets/          images and attachments
└── wiki/                LLM-maintained knowledge base
    ├── index.md         content catalogue by category
    ├── log.md           chronological operation record
    └── [content pages]
```

## The two special files

**`index.md`** is content-oriented: every page listed with a one-line summary and metadata,
organised by category. The LLM reads it first when answering, to work out which pages are
relevant — no embeddings, no vector search.

**`log.md`** is chronological and append-only, recording ingests, queries and lint runs. The gist
notes that if each entry starts with a consistent prefix such as `## [2026-04-02]`, the log stays
parseable with ordinary unix tools.

## Three operations

- **Ingest** — the owner adds a source to `raw/` and asks the LLM to process it. The LLM reads it,
  discusses the takeaways, writes a summary page, updates the index, revises the entity and concept
  pages it affects, and appends a log entry. One source might touch ten to fifteen pages.
- **Query** — questions are answered from the wiki, with citations. A good answer can be filed
  back into the wiki as a new page.
- **Lint** — periodic health-checking for contradictions, stale claims, orphan pages, missing
  cross-references and gaps in coverage.

## Provenance and contradictions

Pages cite back to their sources, and cross-references hold the graph together. Contradictions
between sources are flagged explicitly during maintenance rather than quietly absorbed.

## Division of labour

The human curates the sources and asks the questions. The LLM does everything else: summarising,
cross-referencing, and keeping dozens of pages consistent with each other.

## Suggested uses

Personal knowledge tracking, research deep-dives, reading companions in the manner of a fan wiki,
team and business internal wikis, competitive analysis, trip planning, course notes, hobby
research — any domain where knowledge accumulates.
