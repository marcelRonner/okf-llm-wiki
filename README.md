# Knowledge Wiki

A personal knowledge wiki that an AI assistant maintains. You decide what goes in and what is
true; the assistant reads new material, works out which pages it affects, writes them, keeps the
links and the catalogue correct, and records what happened.

Plain Markdown files. No database, no lock-in — readable in any editor, on any machine, in ten
years' time.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make lint          # should pass on the empty wiki
make serve         # http://127.0.0.1:8000
```

**Open this folder directly in VS Code** (not a parent folder). Copilot only loads
`.github/copilot-instructions.md`, `.github/instructions/` and `.github/prompts/` from the
workspace root, so opening a parent leaves the assistant with no instructions at all.

### Obsidian

Open `wiki/` as a vault. Then in **Settings → Files and links**:

- **Use [[Wikilinks]]** → **off**
- **New link format** → **Relative path to file**

This matters: the wiki uses ordinary relative Markdown links so the same files work in Obsidian
*and* in the built site with no plugins. Wikilinks would break the site.

## Daily use

**To add something** — drop files into `inbox/` (PDFs, notes, exports, anything), then run
`/ingest` in Copilot chat. Pasting or dictating text works too; it gets written to `inbox/` first
so the raw record exists. The assistant proposes what it will do before writing, files the
original into `raw/`, and logs the change.

**To ask something** — `/query` in Copilot chat. Answers come with links and a confidence level:
well supported, single source, inferred, or not in the wiki. If the answer took real work, it
offers to keep it as a page.

**To check its health** — `make lint` for the mechanical checks, `/lint` for the judgement ones
(contradictions, staleness, gaps). Monthly is about right.

## Layout

```
inbox/              drop new material here — should be empty when you are done
raw/                originals, immutable, never edited
wiki/               the vault, and the site's docs_dir
├── index.md        GENERATED catalogue — do not edit, run `make index`
├── log.md          append-only history of every operation
├── projects/       work with a goal and an end
├── systems/        things that keep running and need maintaining
├── decisions/      what was chosen, what was rejected, why
├── people/         who does what
├── orgs/           companies, teams, vendors
├── topics/         concepts that fit nowhere else
└── sources/        one page per item in raw/ — what it said, what it changed
templates/          the shape of each page type
scripts/            index generation and the mechanical checks
.github/            the schema: instructions and the three operation prompts
```

## Commands

| | |
|---|---|
| `make lint` | Frontmatter, links, orphans, `raw/` pairing, inbox, index freshness |
| `make index` | Regenerate `wiki/index.md` from page frontmatter |
| `make serve` | Live-reload site |
| `make build` | Lint, then a strict site build into `site/` |
| `make inbox` | What is waiting to be ingested |
| `make new TYPE=person TITLE="Jane Doe"` | New page from its template |

## Where the rules live

| File | What it governs |
|---|---|
| `.github/copilot-instructions.md` | The schema: layers, operations, page types, frontmatter, cross-cutting rules |
| `.github/instructions/pages.instructions.md` | How to write any page |
| `.github/instructions/projects-systems.instructions.md` | Projects and systems |
| `.github/instructions/decisions.instructions.md` | Decision records |
| `.github/instructions/people-orgs.instructions.md` | People and organisations — **including what not to record** |
| `.github/instructions/sources.instructions.md` | Source pages and their link to `raw/` |
| `.github/prompts/` | `/ingest`, `/query`, `/lint` |

Each `.instructions.md` file has an `applyTo:` glob, so Copilot loads only the ones relevant to
the folder being edited rather than all of them on every request.

## Adding a page type

Rare, and deliberately a little effortful:

1. Add it to `TYPES` and `TYPE_LABELS` in `scripts/wikilib.py`
2. Create `templates/<type>.md`
3. Create `wiki/<folder>/`
4. Add `.github/instructions/<type>.instructions.md` with an `applyTo` glob
5. Add it to the page-type table in `.github/copilot-instructions.md`
6. `make lint`

## Publishing

`make build` produces a static site in `site/`. Nothing is wired up to host it — that is a
deliberate gap, since where this goes depends on how private the contents are. Options, roughly
in order of how much thought they need:

- **Nowhere.** Obsidian locally is enough for most personal wikis.
- **A private host** over FTP/rsync/S3 from a CI job, the way a small internal site is deployed.
- **GitHub Pages** — trivial, but the repository and the site are public unless the repo is
  private and Pages is set to private, which needs a paid plan.

Given this wiki will hold notes on people and organisations, decide the hosting question before
you decide the automation question.
