---
title: Log
type: log
description: Append-only chronological record of wiki operations and corrections.
---

# Log

Newest first. **Entries are never edited or deleted.** If an entry turns out to be wrong, add a
new one saying so — the mistake and its correction are both part of the record.

Format — date groups holding list entries, which is what the Open Knowledge Format requires of a
reserved `log.md` (§9). The detail of an entry goes underneath it, indented:

```markdown
## YYYY-MM-DD

- **Ingest:** short description
  - **Input:** what came in (link the raw file, or quote the question)
  - **Created:** [Page](projects/x.md), [Page](decisions/y.md)
  - **Updated:** [Page](systems/z.md) — what changed
  - **Flagged:** contradictions found, questions left open
  - **Notes:** anything a future reader would want to know
```

## 2026-09-12

- **Correction:** Closed the open points from the 2026-09-12 conformance assessment, and two defects
  found while doing it.
  - **Input:** the owner asked for every open point to be fixed, with a proposal for each
  - **Updated:** [Agent instruction formats](topics/agent-instruction-formats.md) — `stale_after`
    set; `AGENTS.md`, `README.md`, `Makefile`, `scripts/wikilib.py`, `scripts/lint_wiki.py`,
    `scripts/test_okf_consumer.py`; new `scripts/verify_page.py` and `scripts/test_verify_page.py`
  - **Flagged:** two defects, both fixed. `AGENTS.md` showed a `verified:` example with `by: owner`
    and a bare date, which `make lint` rejects twice over — anyone following the instructions
    would have failed E7. And W9 compared `stale_after` by calendar date, so a page was reported
    stale up to a day early; OKF defines staleness as an instant, `now >= stale_after`.
  - **Notes:** What each open point became:

    `OKF-CNF-04` — an acceptance test now reads a bundle containing no `index.md` or `_index.md`
    and asserts every concept loads. The missing-index clause was true before; now it is proven.

    `OKF-LIF-02` — `stale_after: 2027-03-12T00:00:00Z` on the agent-instruction-formats topic. Six
    months, because it records how two vendors' tools behave, and both ship changes monthly. It
    goes on the topic page rather than the source page: the source records what was true on
    2026-09-11 and cannot go stale, whereas the topic is what a reader relies on today. Staleness
    is now `Page.is_stale()`, tested at the exact instant and one second before.

    `OKF-TRU-02` and `-05` — not written, and not writable by the assistant. Instead `make verify
    PAGE=…` gives the owner one command that appends a correct `human:owner` event with a UTC
    timestamp, keeps earlier confirmations, and leaves `updated:` alone. It refuses originals in
    `content/references/`, which are evidence rather than claims.

    `status: superseded` in `AGENTS.md` became `deprecated`, the value `make lint` accepts.

    The 2026-09-12 assessment itself is not re-filed, and still records `OKF-CNF-04` as partial and
    `OKF-LIF-02` as not adopted. Both are fixed after it, and the next reassessment will say so.

- **Ingest:** the 2026-09-12 OKF v0.2 conformance assessment
  - **Input:** the owner asked for the reassessment to be added to the wiki, after acting on its
    findings
  - **Created:** [OKF v0.2 conformance assessment, 2026-09-12](sources/2026-09-12-okf-v0-2-conformance-assessment.md)
    — `source`: it is what one document said — and its original,
    [`2026-09-12-okf-v0-2-conformance-assessment.md`](references/2026-09-12-okf-v0-2-conformance-assessment.md)
  - **Updated:** [Open Knowledge Format](topics/open-knowledge-format.md) — points at this assessment
    as current, and now states the two deliberate divergences
  - **Flagged:** the filed assessment is a re-run after the fixes below, not the run first reported
    in conversation, which was never filed. It lists the three checks that changed between the two.
  - **Notes:** conformant; 26 meets, 1 partial, 7 not adopted, 1 deviates, 6 n/a.

- **Correction:** Renamed `content/raw/` to `content/references/`, and rewrote one link inside an
  original.
  - **Input:** the owner asked for `OKF-LNK-05` to pass, which wants mirrored external material under
    `references/`, and explicitly instructed the link fix despite the rule against editing originals
  - **Updated:** every file naming the folder — `AGENTS.md`, `README.md`, `schema.yml`, the rules,
    skills, register, template, scripts and render hook, and the source pages; link targets in this
    log. Entry prose above that says `raw/` is left as written, because it was true when written.
  - **Flagged:** **an original's body was edited.** In
    [`2026-09-11-okf-v0-2-conformance-checklist.md`](references/2026-09-11-okf-v0-2-conformance-checklist.md),
    the link to the reassessment prompt changed from `../.claude/skills/lint/SKILL.md#…` to
    `../../.claude/skills/lint/SKILL.md#…`. It had been written for the file's first location and
    stopped resolving when the folder moved inside `content/`. This was the owner's call, made
    knowing the rule; it is the only change to that body, and nothing else in it was touched.
  - **Notes:** the site section is now titled *References*, at `/references/`.

- **Correction:** Moved the raw originals inside the Open Knowledge Format bundle, from `raw/` to
  `content/raw/`, and gave each Markdown original a frontmatter header.
  - **Input:** the owner asked for the assessed scope to include the raw folder, after the
    reassessment found two source pages whose `resource:` left the bundle (`OKF-LNK-04`), and chose
    moving the folder over declaring the whole repository the bundle
  - **Updated:** `AGENTS.md`, `README.md`, `schema.yml`, `.claude/rules/sources.md`, the `ingest`,
    `note` and `lint` skills, the check register, `templates/source.md`, `scripts/wikilib.py`,
    `scripts/lint_wiki.py`, `scripts/build_schema.py`, `layouts/_markup/render-link.html`, the four
    source pages, [How this wiki works](topics/how-this-wiki-works.md) and
    [Checks and finding things](topics/checks-and-finding-things.md); new `content/raw/_index.md`
  - **Flagged:** the immutability rule narrowed. It said raw files are never edited; it now says
    their bodies are never edited, and a Markdown original gains a frontmatter header once, when
    filed. The alternative was an unconformant bundle: OKF requires parseable frontmatter and a
    `type` on every `.md` file in it, and none of the four originals had any. The three originals
    already committed were checked afterwards and their bodies are byte-identical.
  - **Notes:** The originals are now published with the site, and the links to them from source
    pages resolve there — before the move they were dead links on the built site. One link inside
    the 2026-09-11 checklist original was written for the old location and now points nowhere;
    since its body cannot be edited, the render hook no longer warns about links inside originals,
    matching the exemption `make lint` already gave them.

    Also added the acceptance test for `OKF-TRU-03`: `Page.verified_events()` reads a bare
    `verified` mapping as a one-element list, as OKF requires of a consumer, and the linter now uses
    it instead of its own copy.

- **Correction:** Restored the expanded text of every log entry that was shortened to a single line
  on 2026-09-11, keeping the date-group structure it was shortened to reach.
  - **Input:** the owner asked for the detail back
  - **Updated:** this file
  - **Notes:** OKF §9 asks for date-grouped list entries; it does not ask for short ones. The
    reformatting was necessary and stays, the discarding was not. Each entry's *Operation* field is
    now the bold word that opens its bullet, which is §9's own convention, and the rest of the
    fields are indented under it.

    The six single-line entries under 2026-09-11 stay as they are. Those were written as one line
    each rather than written long and cut down, so there is no expanded text to restore. What they
    record is accurate; it is just thin, and reconstructing detail from memory would be inventing
    it.

- **Correction:** Gave the OKF conformance checks stable IDs, and linked each one to the clause of
  the specification behind it.
  - **Input:** the owner asked whether the new conformance checklist and its prompt were sound, and
    for indexes on the checks and a source link per check
  - **Updated:** `.claude/skills/lint/okf-v0-2-checks.md` (new — 41 numbered checks in ten families),
    `.claude/skills/lint/SKILL.md` — the reassessment section now works through the register
  - **Flagged:** the prompt had named `raw/2026-06-12-open-knowledge-format.md` as the
    specification. That file is a summary, and does not contain the clauses roughly half the checks
    rest on — per-claim footnote attribution, `usage_window`, the `human:` actor prefix, the §8 and
    §9 reserved-file structures, trust tiers, the computation contract. An assessment now reads the
    published `SPEC.md` at its URL.
  - **Notes:** The register holds the checks and an assessment holds the findings, joined by the ID,
    so two assessments a year apart can be diffed row by row. Twelve checks had no row before. The
    status vocabulary went from eight ad-hoc values to five, and a consumer requirement may no
    longer be marked met without naming the consumer and the test that proves it.

## 2026-09-11

- **Correction:** Clarified the distinction between immutable `raw/` evidence and the linked summaries in `content/sources/` in [README.md](../README.md).
- **Ingest:** Filed the [OKF v0.2 conformance checklist](references/2026-09-11-okf-v0-2-conformance-checklist.md), created its source page, and linked the scoped assessment from [Open Knowledge Format](topics/open-knowledge-format.md).
- **Correction:** Added a reusable OKF v0.2 conformance reassessment prompt to the `lint` skill and linked it from the assessment checklist in `inbox/`.
- **Correction:** Normalised this log into date groups containing only Markdown list entries, and strengthened E7 to enforce that required OKF structure.
- **Correction:** Added OKF reader acceptance checks for unknown types and extra metadata, missing optional metadata, and broken links; `make build` now runs them.
- **Correction:** Removed a superseded, scope-specific work record at the owner’s request. It will be re-added later with a different scope.

- **Ingest:** the LLM Wiki pattern and the Open Knowledge Format
  - **Input:** two summaries the owner asked for, written from the primary sources —
    [`raw/2026-04-04-karpathy-llm-wiki-gist.md`](references/2026-04-04-karpathy-llm-wiki-gist.md) and
    [`raw/2026-06-12-open-knowledge-format.md`](references/2026-06-12-open-knowledge-format.md)
  - **Created:** [Karpathy's LLM Wiki gist](sources/2026-04-04-karpathy-llm-wiki-gist.md),
    [Open Knowledge Format specification](sources/2026-06-12-open-knowledge-format.md),
    [LLM Wiki](topics/llm-wiki.md), [Open Knowledge Format](topics/open-knowledge-format.md) — both
    `topic`: concepts that keep coming up and fit no other type
  - **Updated:** [How this wiki works](topics/how-this-wiki-works.md) — it described the three layers and
    the operations without ever saying where they came from; it now cites the gist
  - **Flagged:** this wiki fails one of OKF's three conformance criteria. The five generated section
    pages carry no `type`, so a strict consumer reads them as untyped concepts. Recorded on the topic
    page with the fix; not fixed here, because an ingest records what a source says rather than acting
    on it.
  - **Notes:** Five pages, which is past the threshold where `/ingest` says to propose and wait. The
    owner pre-authorised, so the plan was stated and the work done in one pass.

  The wiki now describes its own architecture, which is worth saying plainly: the three layers in
  *How this wiki works* were built from this gist, and `schema.yml`'s `type`, the `sources:` key and
  `status:` all match what OKF v0.2 specifies without having been copied from it. Two divergences are
  deliberate rather than accidental — relative links, which keep the files working in Obsidian, and
  `_index.md`, which Hugo requires where the pattern says `index.md`.

- **Ingest:** agent instruction formats
  - **Input:** [`raw/2026-09-11-agent-instruction-formats.md`](references/2026-09-11-agent-instruction-formats.md)
    — a research note on what Claude Code and GitHub Copilot each read as instructions, written while
    moving this wiki's own instructions out of `.github/`
  - **Created:** [Research note — agent instruction formats](sources/2026-09-11-agent-instruction-formats.md),
    [Agent instruction formats](topics/agent-instruction-formats.md) — chose `topic`: it is a concept
    that keeps coming up and fits no other type, which is rung five of the ladder
  - **Updated:** [How this wiki works](topics/how-this-wiki-works.md) — its schema layer still said the
    schema lived in `schema.yml` and `.github/`, which stopped being true when the instructions moved;
    it now names `AGENTS.md` and `.claude/rules/` and links the new topic
  - **Flagged:** two things the source left unresolved, both recorded on its page — nothing re-checks
    that the vendor behaviour dated here is still true, and whether Copilot can invoke a skill by typed
    name without a prompt file was never settled
  - **Notes:** The first ingest with a document behind it, so also the first exercise of the `raw/`
    pairing. Also the first time the wiki's own instructions were loaded while writing to it: `CLAUDE.md`
    imports `AGENTS.md`, and the routing table sent me to `.claude/rules/sources.md` and
    `.claude/rules/pages.md` before the first write to either folder.

  Separately, and not from the source: the four operations are typable in Copilot again. Each
  `.github/prompts/*.prompt.md` is now an eleven-line door that names its skill and stops, rather than
  a second copy of the procedure.

- **Correction:** most of the Copilot mirror was redundant
  - **Input:** the owner asked why the generator was still producing Copilot prompt files when the
    operations had become skills
  - **Updated:** deleted `.github/prompts/` and `.github/copilot-instructions.md`;
    `scripts/build_schema.py` now mirrors only `.claude/rules/`
  - **Notes:** The answer was that the generator had been written against Copilot's older prompt-file
    format, which was the only invocable-operation format it had at the time. That is no longer true,
    and it was checked against the VS Code and GitHub documentation rather than assumed.

  VS Code reads `AGENTS.md` at the workspace root, and discovers skills from `.github/skills/`,
  `.claude/skills/` and `.agents/skills/`. So the contract and the four operations were already being
  read where they are written, by both tools, and the mirror was copying them for nothing. Five of the
  nine generated files are gone.

  What still needs mirroring is exactly one thing: path-scoped rules. The `.claude/rules` location
  Copilot supports is user-profile only (`~/.claude/rules`), so a project's scoped rules must be
  restated as `.github/instructions/*.instructions.md`, where `paths:` is spelled `applyTo:`. If that
  ever changes, the phase and the whole `.github/` directory can go.

  One thing given up knowingly: Copilot's prompt files could be invoked by typing `/note`, whereas a
  skill is matched on its description. The four typed doors still exist in Claude Code; in Copilot the
  operations are now triggered by asking for them. Worth re-adding a prompt file as a thin shim if
  typing `/note` there turns out to matter.

- **Correction:** the four operations are skills
  - **Input:** the owner asked why the operations could not be agents, and for the answer to be
    written down rather than left in a chat
  - **Updated:** `.claude/skills/<name>/SKILL.md` (was `.claude/commands/<name>.md`), `README.md` —
    new *Why the four operations are skills, and not agents* section
  - **Notes:** No operation changed behaviour. `/note`, `/ingest`, `/query` and `/lint` are still typed
    by name and still run in the conversation you type them in.

  Skills are a directory rather than a file, so an operation has somewhere to keep a helper script,
  and they load progressively — only the `description` sits in context until the skill runs. That
  makes four operations cost four lines instead of four hundred.

  Agents were the real question, and the answer is that they run in a *separate* conversation and
  return a summary. For `/note` that breaks the wiki's foundation: the owner's exact words have to
  reach the month's owner-notes page verbatim, and a summary boundary on the way in is where they
  would stop being verbatim. It also costs the typed door — "nothing enters or leaves the wiki except
  through these four" means four things the owner can type, and an agent cannot be typed.

  `/lint` is the exception, and the README says so: read-only, reads every page, keeps nothing
  verbatim, and its output genuinely is a summary. If a full lint ever crowds out the conversation it
  was run from, the move is to keep `/lint` as the skill and have it delegate to an agent. Not needed
  at two pages.

- **Correction:** the instructions moved out of .github/
  - **Input:** the owner asked for the instructions and prompts to live somewhere less tied to GitHub
    Copilot, so a second assistant could read them
  - **Updated:** `AGENTS.md` (was `.github/copilot-instructions.md`), `.claude/rules/` (was
    `.github/instructions/`), `.claude/commands/` (was `.github/prompts/`)
  - **Notes:** No rule changed meaning. This is where they live, not what they say.

  `AGENTS.md` is the name every agent tool but Claude Code reads, and `CLAUDE.md` is one line that
  imports it — Claude Code's loader looks only for `CLAUDE.md`, `.claude/CLAUDE.md`,
  `CLAUDE.local.md` and `.claude/rules/`, so without that line the contract would be invisible to
  it. The per-folder rules kept their globs: `applyTo:` became `paths:`, which is the same idea in
  the other tool's dialect. The four operations became `.claude/commands/`, so `/note` and the rest
  still work by name.

  `.github/` is now **generated** from those files by `make schema`, and `make build` fails if it has
  drifted. The alternative was two hand-maintained copies of every rule, which is the failure this
  repo already had once and built `schema.yml` to stop: when two statements of the same rule
  disagree, the assistant trusts both and resolves it by rewriting pages. Deleting a rule now also
  deletes its mirror, so Copilot cannot go on loading something that no longer exists.

  One gap worth knowing: a `paths:` glob attaches only after a file in that folder has been read, so
  it cannot inform the *first* write to a folder. `AGENTS.md` carries a routing table naming which
  rules file to open for which folder, which is the manual version of the same thing.

- **Correction:** the person and org types are gone
  - **Input:** the owner asked for people and orgs to be removed from the wiki entirely
  - **Updated:** `schema.yml` — `person` and `org` deleted, five types remain; every generated
    restatement of the schema followed from `make schema`
  - **Notes:** Both folders held nothing but scaffolding, so no page was lost and no link broke.

  What went with them: `templates/person.md`, `templates/org.md`,
  `.github/instructions/people-orgs.instructions.md`, and the `content/people/` and `content/orgs/`
  folders. The type table in `.github/copilot-instructions.md`, the frontmatter enum, the README
  layout tree and the section pages are generated, so they restamped themselves.

  Hand-written prose that named the removed types was rewritten rather than deleted where the point
  it was making still stood: the *Who owns it* section on system pages now asks who to go to instead
  of linking a person page, and the ingest checklist still guards against material that is sensitive
  about a named individual — a source page can quote a meeting full of people without the wiki
  having a page for any of them. What did go is `/lint`'s boundary check, which existed only to
  police person and org pages against a rule file that no longer exists.

  The decision ladder in `.github/copilot-instructions.md` lost a rung: there is no longer a
  question to ask about people, so a name that needs recording belongs in whichever project,
  system or decision it turns up in.

## 2026-08-02

- **Correction:** a fourth operation, and lint learns two severities
  - **Input:** the owner reported that adding a page or a topic was harder than it should be
  - **Created:** [Checks and finding things](topics/checks-and-finding-things.md) — split out of the
    page below when documenting these changes pushed it past the 400-word rule it exists to explain
  - **Updated:** [How this wiki works](topics/how-this-wiki-works.md) — three operations became four
  - **Flagged:** nothing was ingested and no claim changed — this is a change to how the wiki is
    written, not to what it says.

  What changed and why:

  - **`/note` added** as a fourth operation. The wiki had one door and it was built for documents:
    writing down something the owner simply knew meant manufacturing a file in `inbox/`, moving it
    to `raw/`, writing a source page, then writing the real page — four artefacts for one fact.
    `/note` takes their words directly. To keep every claim traceable rather than exempting notes
    from the rule, the owner's words are anchored in a monthly `sources/YYYY-MM-owner-notes.md`
    page marked `origin: owner`.
  - **Lint split into errors and warnings.** Previously every finding failed, so `make new` left
    the repository in a broken state until the page was finished — the tooling punished capture.
    Errors (broken links, misfiled pages, missing sources) fail; warnings (unlinked pages,
    placeholder summaries, ageing stubs) are reported. `make build` still fails on both.
  - **The orphan check now works.** It had been seeded from `index.md`, which links every page by
    construction, so it could never fire — an unlinked page passed lint clean while three files
    promised the check was being made. It now walks out from `log.md` and counts real inbound
    links, ignoring generated backlink blocks.
  - **`schema.yml` is now the only definition of the page types.** They had been restated in six
    places read by three audiences with nothing checking they agreed. The failure mode was not
    untidiness: when `.github/` and the linter disagreed about which types existed, the assistant
    trusted both and would resolve the contradiction by rewriting pages to satisfy the linter.
    Generated restatements are now stamped by `make schema` and `make build` fails if they drift.
  - **`make move` added**, which re-types a page and rewrites every link to it. This is what let
    "ask the owner which type to use" be replaced with a decision ladder — guessing wrong now
    costs one command instead of a manual link hunt.
  - **`wiki/tags.md` and per-page backlinks are now generated**, giving two ways to find a page
    besides the type folder it happens to sit in.

## 2026-08-01

- **Initialization:** Wiki created
  - **Input:** initial scaffold
  - **Created:** [How this wiki works](topics/how-this-wiki-works.md)
  - **Notes:** Empty wiki with the schema, the three operations, templates and the checks in place.
    Nothing ingested yet.
