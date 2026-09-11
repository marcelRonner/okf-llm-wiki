@AGENTS.md

<!--
The contract lives in AGENTS.md, which Claude Code does not read on its own — its memory loader
looks for CLAUDE.md, .claude/CLAUDE.md, CLAUDE.local.md and .claude/rules/ and nothing else. The
import above is what connects the two, so the instructions stay in one file under the name every
other agent tool reads.

Per-folder writing rules are in .claude/rules/, scoped with `paths:`. They load when you touch a
matching file; AGENTS.md carries a routing table for the first write to a folder.
-->
