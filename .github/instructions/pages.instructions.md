---
applyTo: "wiki/**"
---

# How to write any page

These rules apply to every page regardless of type. The type-specific files add to them.

## Shape

```markdown
---
(frontmatter — see copilot-instructions.md)
---

# Title

One or two sentences saying what this is, for someone who arrived here from a search
and has no context. No heading above it.

## Sections appropriate to the type

## Open questions        ← optional, but use it freely
- Things you know you do not know. Better recorded than pretended away.

## Related
- [Another page](../topics/thing.md) — why it is related, in a few words

<!-- backlinks:start -->   ← GENERATED. Never write inside this block; `make index` overwrites it.
<!-- backlinks:end -->
```

Order matters: the orienting sentence comes first, before any detail. Someone skimming should
be able to stop after one line and still have learned something.

## Writing rules

- **Present tense for what is true now, past tense for what happened.**
- **Dates, not relative time.** "Since 2026-03" not "recently". "As of 2026-08-01" not "currently".
- **Name the source of a non-obvious claim** inline: "throughput is ~400/s ([load test](../sources/2026-07-load-test.md))".
- **Bullets for lists of things, prose for reasoning.** Do not bullet an argument into fragments.
- **No filler headings.** If a section would have one line under it, it is not a section.
- **British or American spelling — pick one and never mix.** This wiki uses British.

## Linking

- Plain relative Markdown links only: `[Acme](../orgs/acme.md)`
- Link the first meaningful mention of any entity that has a page, not every mention
- In the **Related** section, always say *why* — a bare list of links ages into noise
- Before linking to a page, check it exists. If it should exist but does not, create a stub:
  frontmatter, a title, and one honest sentence such as "Stub — only known from
  [source](../sources/x.md)."

## Stubs

A stub is a legitimate page, not a failure. It is better to have twenty honest stubs that
capture what you know than five long pages and fifteen facts lost. Mark them:

```yaml
status: stub
```

Remove the marker once the page says something useful on its own.

## What not to do

- Do not restate another page. Link to it.
- Do not write a summary of the wiki inside a page. That is what `wiki/index.md` is for.
- Do not add a "Last updated" line in the body — that is `updated:` in the frontmatter.
- Do not use headings as facts ("## Migration failed") — headings name topics, bodies make claims.
- Do not write inside a `<!-- name:start -->` … `<!-- name:end -->` block. `make index` and
  `make schema` overwrite them wholesale, so anything you put there is lost without warning.
  Backlinks are generated; the links you choose go in **Related**, and they are what the orphan
  check actually counts.
