# OKF v0.2 compliance — what was changed, and where each point now lives

Written 2026-09-11, after working through nine fixes against the Open Knowledge Format v0.2.
This records what was done and where to look, so the next reader does not have to re-derive it
from the git history.

The spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

## The headline

Conformance with OKF v0.2 turned out to be **one fix**, not nine. The spec's conformance section
has three criteria and only ever requires `type`. Everything else in this list is interoperability
quality — a consumer must not reject a bundle for any of it.

Before this work: criteria 1 and 3 passed; criterion 2 failed on five files.
After: conformant, and a lint error now guards it.

## Fix 1 — `type` on the generated section pages (the only compliance fix)

The five `content/<folder>/_index.md` files carried `title`, `description` and `weight` but no
`type`, so a strict consumer read them as five untyped concepts.

Now stamped `type: section` by `scripts/build_schema.py`'s `section_pages()`. These files are OKF's
`index.md` — directory listings — under the name Hugo insists on, so they are not reserved and do
need a type.

## Fix 9 — the criteria as a lint check

`scripts/lint_wiki.py`, error code **E7**, function `check_okf_conformance()`.

It walks `content/` directly rather than through `pages()`, because the criteria apply to every
file in the bundle including the section pages `pages()` excludes as furniture. A check that used
`pages()` would have passed on the exact breakage it exists to catch.

Criterion 3 is checked only for presence and parseability. Whether `log.md` is genuinely
chronological is judgement, and belongs to the `/lint` skill rather than to a script.

## Fix 2 — `sources` was a collision, not an omission

v0.2 defines `sources` as a list of objects, each with a required `resource`. This wiki had a list
of strings, so a consumer reading `.resource` got nothing — silently. That is worse than a missing
optional field.

    sources:
      - resource: sources/2026-04-04-karpathy-llm-wiki-gist.md

In `lint_wiki.py`, `source_resources()` reads the object form and **rejects a bare string** with a
message naming the replacement, so the old shape cannot come back. E4 covers it.

## Fix 5 — `resource` on source pages

Each source page now names its original: the public URL where one exists, otherwise
`../../raw/<file>`. Added to `templates/source.md` so every future source page carries one.

**W8** warns when a source page has no `resource`, or when a relative one points at a file that is
gone. It earned its keep immediately: the first `resource` written here said `../raw/` where the
file is two levels up, and W8 caught it.

## Fix 6 — `verified`, the owner's key

    verified:
      - by: owner
        at: 2026-09-11

This is the one worth having for its own sake rather than for the spec. This wiki is built on the
owner deciding what is true, and had no way to record that they had done so — every page was
equally unverified, whether read carefully or written unattended.

**`AGENTS.md` instructs the assistant never to write it.** An assistant asserting that the owner
checked something would destroy the only signal separating "checked" from "merely written". Append
entries rather than replacing them, so the history of confirmations survives.

**W9** reports pages nothing has verified for longer than `unverified_days` in `schema.yml`
(currently 365). That is a question for the owner, never something to silence.

## Fix 7 — `generated: { by, at }`

v0.2 replaced v0.1's flat `timestamp` with this. It duplicates `updated:`, so it is **stamped by
`make index`** rather than hand-written — two dates maintained by hand drift, and nothing would
notice. See `apply_generated()` in `scripts/build_index.py`. `by: assistant` is honest; these pages
are written by one.

## Fix 8 — `stale_after`

An optional per-page date after which the page should be re-read, generalising the global
`stub_days`. **W9** warns once it passes. Vendor behaviour is the obvious use: the two source pages
on Claude Code and Copilot describe products that will move.

## Fix 3 — `status` was the second collision

v0.2 enumerates `draft`, `stable`, `deprecated`. This wiki used `stub` and `superseded`.

Now the spec's set, enforced by **E7**. `stub` became `draft` and `superseded` became `deprecated`,
which is a genuine loss of vocabulary — `superseded` implied a link to the replacement, and `stub`
carried the argument in `.claude/rules/pages.md` that a stub is a legitimate page rather than a
failure. That argument was kept and reworded rather than dropped.

## Fix 4 — `summary` became `description`

v0.2 recommends `description`. The rename went through `schema.yml` (including
`summary_chars` → `description_chars`), `AGENTS.md`, the rules, the skills, five templates, six
scripts, every content page, and the `make new DESCRIPTION=` flag.

It also ended an internal inconsistency: the generated section pages already used `description`
while every hand-written page used `summary`.

Genuine English uses of the word — "returns a summary", "never summarised in place" — were left
alone. Only the key and the things named after it changed.

## Deliberately not done

- **Bundle-relative absolute links** (`/topics/x.md`). Recommended by the spec, but it would break
  the Obsidian relative-path setup the README configures, to upgrade "permitted" to "recommended".
- **`index.md` instead of `_index.md`.** Hugo requires the underscore; a bare `index.md` would turn
  each section into a leaf bundle and collapse the tree. The spec makes `index.md` optional, so its
  absence costs nothing.
- **`Attested Computation`.** A v0.2 type for computed data assets with executors and attesters.
  Nothing here is one.

## What this cost, and what to watch

Six new lint findings now exist: E7 in two forms, E4's shape check, W8, and W9 in two forms. Each
was verified by making it fire and then pass. The risk they carry is the ordinary one — a check
nobody reads is worse than no check — so if W9's unverified warning becomes background noise,
raising `unverified_days` is the honest response rather than deleting the check.

The `verified` key is the one to actually use. Everything else here is bookkeeping that happens
without the owner; that one is the only key in the wiki that only the owner can fill.
