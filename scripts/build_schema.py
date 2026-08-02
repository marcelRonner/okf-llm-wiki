#!/usr/bin/env python3
"""Regenerate everything that restates the page types, from schema.yml.

The type list used to exist in six places read by three different audiences — the scripts, the
assistant, and you — with nothing checking they agreed. That is a worse bug than it sounds: when
`.github/` and the linter disagree about which types exist, the assistant trusts both, and
resolves the contradiction by rewriting your *pages* to satisfy the linter.

So the schema is declared once in schema.yml and stamped into the files that need to restate it:

    .github/copilot-instructions.md   the page-type table + the frontmatter example
    README.md                         the wiki/ layout tree

Usage:
    python3 scripts/build_schema.py            # write the generated blocks
    python3 scripts/build_schema.py --check    # exit 1 if any are stale (used by `make build`)
"""

from __future__ import annotations

import sys

from wikilib import ROOT, TYPE_INFO, replace_block

INSTRUCTIONS = ROOT / ".github" / "copilot-instructions.md"
README = ROOT / "README.md"


def types_table() -> str:
    rows = ["| Type | Folder | Holds |", "|---|---|---|"]
    for name, spec in TYPE_INFO.items():
        rows.append(f"| `{name}` | `wiki/{spec['folder']}/` | {spec['holds']} |")
    return "\n".join(rows)


def frontmatter_example() -> str:
    enum = " | ".join(TYPE_INFO)
    return "\n".join([
        "```yaml",
        "---",
        "title: Human readable name",
        f"type: {enum}",
        "summary: One sentence. This is what appears in the index — make it worth reading.",
        "created: YYYY-MM-DD",
        "updated: YYYY-MM-DD",
        "tags: [lowercase-kebab, another]",
        "sources: [sources/some-source.md]   # source pages this page draws on; omit if none",
        "---",
        "```",
    ])


def layout_tree() -> str:
    entries = [
        ("index.md", "GENERATED catalogue — do not edit, run `make index`"),
        ("tags.md", "GENERATED tag listing — every tag, and what carries it"),
        ("log.md", "append-only history of every operation"),
    ]
    entries += [(f"{spec['folder']}/", spec["short"]) for spec in TYPE_INFO.values()]

    width = max(len(name) for name, _ in entries) + 2
    lines = ["```"]
    lines.append("inbox/              drop new material here — should be empty when you are done")
    lines.append("raw/                originals, immutable, never edited")
    lines.append("wiki/               the vault, and the site's docs_dir")
    for i, (name, desc) in enumerate(entries):
        branch = "└──" if i == len(entries) - 1 else "├──"
        lines.append(f"{branch} {name.ljust(width)}{desc}")
    lines.append("templates/          the shape of each page type")
    lines.append("scripts/            index generation and the mechanical checks")
    lines.append("schema.yml          the page types — edit here, run `make schema`")
    lines.append(".github/            the schema in prose: instructions and the operation prompts")
    lines.append("```")
    return "\n".join(lines)


BLOCKS = {
    INSTRUCTIONS: {"schema-types": types_table, "schema-frontmatter": frontmatter_example},
    README: {"schema-layout": layout_tree},
}


def main() -> int:
    check = "--check" in sys.argv
    stale: list[str] = []

    for path, blocks in BLOCKS.items():
        if not path.exists():
            print(f"schema: {path.relative_to(ROOT)} is missing", file=sys.stderr)
            return 1
        current = path.read_text(encoding="utf-8")
        updated = current
        for name, render in blocks.items():
            updated = replace_block(updated, name, render())
        if updated == current:
            continue
        if check:
            stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"schema: updated {path.relative_to(ROOT)}")

    if stale:
        print(f"schema: STALE — run `make schema` ({', '.join(stale)})", file=sys.stderr)
        return 1

    print("schema: up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
