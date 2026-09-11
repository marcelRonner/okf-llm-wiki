# Research note: agent instruction formats across Claude Code and GitHub Copilot

Written 2026-09-11 while moving this wiki's instructions out of `.github/`. Findings come from two
places: reading the Claude Code binary shipped with VS Code extension 2.1.268, and the VS Code /
GitHub Copilot documentation as it stood on 2026-09-11.

## The four mechanisms

There are four distinct things people lump together as "instructions", and they differ in *when*
they enter the model's context:

1. **Always-on instructions.** Loaded on every request. `AGENTS.md`, `CLAUDE.md`,
   `.github/copilot-instructions.md`.
2. **Path-scoped instructions.** Loaded only when a file matching a glob is touched.
   `.claude/rules/*.md` with `paths:`; `.github/instructions/*.instructions.md` with `applyTo:`.
3. **Invocable operations.** Loaded when named. Skills (`SKILL.md`, matched on `description`),
   and Copilot prompt files (`.github/prompts/*.prompt.md`, invoked by typing `/name`).
4. **Delegated agents.** Run in a *separate* context window and return a summary.
   `.claude/agents/*.md`. Not invocable by typing a name.

## What Claude Code 2.1.268 actually loads

Read out of the binary's memory loader. Per directory, walking from the working directory down to
any file it touches, it reads:

- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `CLAUDE.local.md`
- `.claude/rules/` (recursive)

And nothing else. In particular **it does not read `AGENTS.md`** — the string appears in the binary
only inside the `/init` prompt and the Codex importer. A repo wanting one copy under the neutral
name needs a `CLAUDE.md` containing `@AGENTS.md`.

Project skills are discovered from `.claude/skills/`. `.agents/skills/` appears in the binary only
as a directory the `/import` command reads *from*, not a native load path.

Rule files in `.claude/rules/` are partitioned by whether they declare `paths:`. Without it, a rule
is always loaded. With it, the rule loads only when a touched file matches, using gitignore-style
matching relative to the directory containing `.claude/`. A trailing `/**` is stripped, so
`content/x/**` and `content/x` behave identically.

Both path-scoped rules and nested `CLAUDE.md` files are **trigger-based**: they attach *after* the
tool call that touched a matching file, not before. So neither can inform the first write to a
folder. They are loaded once per session per path and cleared on compaction.

## What VS Code / Copilot reads

From the VS Code documentation on 2026-09-11:

- Always-on: `.github/copilot-instructions.md`, **`AGENTS.md`** ("VS Code automatically detects an
  `AGENTS.md` Markdown file in the root of your workspace and applies the instructions in this file
  to all chat requests within this workspace"), nested `AGENTS.md`, and `CLAUDE.md`.
- Path-scoped: `.instructions.md` files with an `applyTo` glob, in `.github/instructions` for a
  workspace, or `~/.copilot/instructions` / `~/.claude/rules` for a user profile. The `.claude/rules`
  location is **user-profile only** — not project.
- Skills: discovered from `.github/skills/`, `.claude/skills/` **and** `.agents/skills/`. Required
  `SKILL.md` frontmatter is `name` (lowercase, hyphens, max 64 chars) and `description` (max 1024).
  GitHub's changelog dates Copilot's Agent Skills support to 2025-12-18.

## Where the two tools agree and disagree

They have converged on almost everything. `SKILL.md` is a cross-tool standard read by both from the
same directories. `AGENTS.md` is read by both — Copilot natively, Claude Code via a one-line import.

They diverge in exactly one place that matters to a project: **project-level path-scoped rules**.
Claude Code reads `.claude/rules/`; Copilot reads `.github/instructions/` for a workspace and only
consults `.claude/rules` at user level. A project wanting both has to state its scoped rules twice,
in two dialects (`paths:` versus `applyTo:`).

The second, smaller divergence: Copilot matches a skill on its `description`, and has no way to
invoke one by typing its name. Typing `/name` in Copilot requires a prompt file.

## Consequences for a project that wants both

- The contract belongs in `AGENTS.md`, with `CLAUDE.md` as a one-line import.
- Operations belong in `.claude/skills/<name>/SKILL.md`, read by both tools unchanged.
- Scoped rules must be written once and generated into the other dialect, or they will drift.
- A typed `/name` door in Copilot needs a prompt file, which can be a stub that names the skill
  rather than a second copy of it.
- Nested per-directory instruction files are a trap in a Hugo repo: anything named `AGENTS.md`
  under `content/` would be published as a page unless excluded in config.

## Sources consulted

- Claude Code native binary, VS Code extension `anthropic.claude-code-2.1.268-darwin-arm64`
- https://code.visualstudio.com/docs/agent-customization/agent-skills
- https://code.visualstudio.com/docs/agent-customization/custom-instructions
- https://code.visualstudio.com/docs/agent-customization/overview
- https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/
