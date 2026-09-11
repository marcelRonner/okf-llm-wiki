# Knowledge Wiki

A personal knowledge wiki that an AI assistant maintains. You decide what goes in and what is
true; the assistant reads new material, works out which pages it affects, writes them, keeps the
links and the catalogue correct, and records what happened.

Plain Markdown files. No database, no lock-in — readable in any editor, on any machine, in ten
years' time.

## Setup

The site is built with [Hugo](https://gohugo.io/) and the [Docsy](https://www.docsy.dev/) theme.
Docsy is a Hugo module, so it needs Go to fetch it and Node to build its stylesheets — Hugo
itself must be the *extended* build.

```bash
brew install hugo go node                        # hugo must be the extended build
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt                  # PyYAML, for the scripts in scripts/
npm install                                      # Docsy's assets, and Dart Sass for Hugo
make lint          # should pass on the empty wiki
make serve         # http://localhost:1313
```

Nothing is installed globally beyond those three tools: Dart Sass is a project-local npm
dependency, and `make` puts `node_modules/.bin` on Hugo's PATH so it is found.

**Open this folder directly in VS Code** (not a parent folder). Both assistants look for their
instructions at the workspace root — Copilot in `.github/`, Claude Code in `CLAUDE.md` and
`.claude/` — so opening a parent leaves you with an assistant that has no instructions at all.

### Obsidian

Open `content/` as a vault. Then in **Settings → Files and links**:

- **Use [[Wikilinks]]** → **off**
- **New link format** → **Relative path to file**

This matters: the wiki uses ordinary relative Markdown links so the same files work in Obsidian
*and* in the built site with no plugins. Wikilinks would break the site.

## Daily use

**To write down something you know** — `/note` in Copilot or Claude Code, followed by the thing. No file,
no inbox, no confirmation round-trip. The assistant works out which page it belongs on, writes
it, and records what you said verbatim in that month's `content/sources/YYYY-MM-owner-notes.md` so
the claim has a dated anchor like any other. This is the fast path, and most days it is the only
one you need.

**To add a document** — drop files into `inbox/` (PDFs, notes, exports, anything), then run
`/ingest`. The assistant reads them, files the original into `raw/`, writes the pages they
affect, and logs the change. It writes straight away for small, uncontentious material and stops
to propose a plan when the material contradicts something or spans a lot of pages.

The difference between the two: use `/ingest` when losing the exact wording would lose something.
Otherwise `/note`.

**To ask something** — `/query`. Answers come with links and a confidence level: well supported,
single source, inferred, or not in the wiki. If the answer took real work, it offers to keep it
as a page.

**To check its health** — `make lint` for the mechanical checks, `/lint` for the judgement ones
(contradictions, staleness, gaps). Monthly is about right.

## Layout

<!-- schema-layout:start GENERATED from schema.yml by `make schema` — do not edit -->
```
inbox/              drop new material here — should be empty when you are done
raw/                originals, immutable, never edited
content/            the vault, and Hugo's content directory
├── _index.md   GENERATED catalogue — do not edit, run `make index`
├── tags.md     GENERATED tag listing — every tag, and what carries it
├── log.md      append-only history of every operation
├── projects/   work with a goal and an end
├── systems/    things that keep running and need maintaining
├── decisions/  what was chosen, what was rejected, why
├── topics/     concepts that fit nowhere else
└── sources/    one page per item in raw/, plus monthly owner notes
templates/          the shape of each page type
scripts/            index generation and the mechanical checks
schema.yml          the page types — edit here, run `make schema`
AGENTS.md           the schema in prose: layers, operations, provenance, rules
CLAUDE.md           one line, importing AGENTS.md for Claude Code
.claude/            rules/ per-folder writing rules, commands/ the four operations
.github/            GENERATED mirror of the above, in the layout Copilot reads
hugo.yaml           the site build: Docsy as a Hugo module, and the theme's settings
layouts/            the one template this site overrides — see _markup/render-link.html
go.mod  package.json  pinned versions of the theme and its assets
```
<!-- schema-layout:end -->

## Commands

| | |
|---|---|
| `make lint` | Regenerate the catalogue, then check the wiki. **Errors fail, warnings are reported.** |
| `make index` | Regenerate `content/_index.md`, `content/tags.md` and the backlink blocks |
| `make schema` | Restamp the type tables in `.github/` and this README from `schema.yml` |
| `make serve` | Live-reload site at <http://localhost:1313> |
| `make build` | Check nothing is stale or broken, then build the site into `site/` |
| `make lint STRICT=1` | The same checks, but warnings fail too — for CI, if you want the higher bar |
| `make build STRICT=1` | The same, and Hugo's own warnings fail too — an unresolved Markdown link, say |
| `make inbox` | What is waiting to be ingested |
| `make new TYPE=project TITLE="Acme Migration" [FROM=content/topics/x.md]` | New page from its template, linked from `FROM` |
| `make move PAGE=content/topics/x.md TYPE=project` | Re-type or rename a page, rewriting every link to it |
| `make new-type TYPE=meeting` | Scaffold a type you have declared in `schema.yml` |

### Errors versus warnings

`make lint` distinguishes *the wiki is wrong* from *the wiki is unfinished*, and only the first
fails. Broken links, misfiled pages and claims citing a source that does not exist are errors.
Unlinked pages, placeholder summaries, ageing stubs, over-long pages and unprocessed inbox items
are warnings — visible every time, but they never stop you.

This matters more than it sounds. When every finding failed, creating a page put the repo in a
broken state until you finished it, so the tooling punished exactly the thing you most want to
be cheap.

`make build` does not fail on warnings either — a site that will not build because a page is 401
words is a check people learn to bypass, and a bypassed check is worse than none. What `make
build` does refuse is a *stale* generated file, since a published site that disagrees with the
wiki it was built from is a correctness problem. `STRICT=1` on either target fails on warnings
if you want that.

## Where the rules live

| File | What it governs |
|---|---|
| `schema.yml` | **The page types.** The one place they are defined; everything else is generated from it |
| `AGENTS.md` | The schema in prose: layers, operations, provenance, frontmatter, cross-cutting rules |
| `CLAUDE.md` | One line. Claude Code reads no `AGENTS.md`, so this imports it |
| `.claude/rules/pages.md` | How to write any page |
| `.claude/rules/projects-systems.md` | Projects and systems |
| `.claude/rules/decisions.md` | Decision records |
| `.claude/rules/sources.md` | Source pages, their link to `raw/`, and the owner-notes pages |
| `.claude/commands/` | `/note`, `/ingest`, `/query`, `/lint` |
| `.github/` | **Generated.** The same instructions in the layout Copilot reads |

Each rules file carries a `paths:` glob, so only the ones relevant to the folder being edited get
loaded rather than all of them on every request. Because that glob is spelled `applyTo:` in
Copilot's dialect and the two tools disagree about where any of this lives, `.github/` is
generated from the files above by `make schema` — the same treatment as every other restatement
here. Edit the source; `make build` fails if the mirror has drifted.

The one thing a `paths:` glob cannot do is load a rule *before* the first write to a folder, since
it attaches only once a file there has been read. `AGENTS.md` carries a short routing table for
that case.

## Adding a page type

Still rare — a new type fragments the wiki, so prefer an existing one unless you can say in a
sentence why none fits. But it is now one edit rather than six:

1. Declare it in `schema.yml`
2. `make new-type TYPE=<type>` — creates the folder, the template and the rules file
3. Write the TODO sections it left you
4. `make schema && make lint`

The type list used to live in six places read by three different audiences — the scripts, the
assistant, and you — with nothing checking they agreed. That is worse than untidy: when
`.github/` and the linter disagreed about which types existed, the assistant trusted both and
resolved the contradiction by rewriting *pages* to satisfy the linter. Now `schema.yml` is the
only definition, and `make build` fails if any generated restatement of it has drifted.

## How the site is built

Hugo renders `content/` with Docsy, pulled in as a Hugo module and pinned in `go.mod`. There is
no `menu:` in `hugo.yaml` on purpose: Docsy builds the sidebar from the folder tree, so adding a
page never means editing the config. The section titles and their order come from `schema.yml`,
stamped into each `content/<folder>/_index.md` by `make schema`.

Two things in `hugo.yaml` are worth knowing before you change them:

- **`layouts/_markup/render-link.html`.** Pages link to each other with ordinary relative
  Markdown links (`../projects/acme.md`) so the same files work in Obsidian, on GitHub, and in the
  built site. MkDocs rewrote those to the published URL by itself; Hugo does not, and would ship
  `href="…jane.md"`, which 404s. This hook resolves them. A link that resolves to no page — one
  into `raw/`, say — is passed through untouched and warns; `make build STRICT=1` makes that fail.
- **The `mounts:` under the Docsy import.** Docsy's sidebar chrome lives in `layouts/docs/`, which
  Hugo only reaches for pages whose `type` is `docs`. Every page here already has a `type` — this
  wiki's page type — so mounting `layouts/docs` at the layout root makes that chrome the site-wide
  default instead. The other mounts are Docsy's own and have to be restated because declaring any
  replaces them; re-check them against the theme's `hugo.yaml` after `hugo mod get -u`.

## Publishing

`make build` produces a static site in `site/`. Nothing is wired up to host it — that is a
deliberate gap, since where this goes depends on how private the contents are. Options, roughly
in order of how much thought they need:

- **Nowhere.** Obsidian locally is enough for most personal wikis.
- **A private host** over FTP/rsync/S3 from a CI job, the way a small internal site is deployed.
- **GitHub Pages** — trivial, but the repository and the site are public unless the repo is
  private and Pages is set to private, which needs a paid plan.

These are your private notes whatever they are about, so decide the hosting question before you
decide the automation question.
