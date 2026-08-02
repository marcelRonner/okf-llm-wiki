#!/usr/bin/env python3
"""Scaffold a new page type: its folder, its template, and its instruction file.

Adding a type used to mean six edits across five files, with nothing checking they agreed. Now
the type is declared once in schema.yml and this script creates what the declaration implies.

The parts this cannot do for you are the parts worth doing: describing what belongs in the type
(`holds:` in schema.yml) and writing the sections its pages should have. Both are left as TODO
markers, and `make lint` will keep mentioning them until you write them.

Usage:
    1. Add the type to schema.yml
    2. python3 scripts/new_type.py <type>
    3. Edit templates/<type>.md and .github/instructions/<type>.instructions.md
    4. make schema && make lint

A new type fragments the wiki, so prefer an existing one unless you can say in a sentence why
none of them fits. The assistant is told not to add types on its own — that decision is yours.
"""

from __future__ import annotations

import sys

from wikilib import ROOT, TEMPLATES, TYPE_INFO, WIKI

INSTRUCTIONS_DIR = ROOT / ".github" / "instructions"

TEMPLATE = """---
title: {{{{TITLE}}}}
type: {name}
summary: {{{{SUMMARY}}}}
created: {{{{DATE}}}}
updated: {{{{DATE}}}}
tags: []
status:
---

# {{{{TITLE}}}}

One or two sentences for someone who arrived from a search with no context.

## TODO — the sections a {name} page should have

Replace this with the real structure. Look at templates/topic.md for the shape, and at another
type close to this one for how much detail is worth asking for.

## Open questions

## Related
"""

INSTRUCTION = """---
applyTo: "wiki/{folder}/**"
---

# {label}

TODO — what makes a good {name} page.

Say what belongs here that does not belong on any other type, what the sections are for, and
what should never be recorded. Delete this file and remove the type from schema.yml if it turns
out an existing type covered it after all.

## What belongs here

## What does not

## Sections
"""


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    name = sys.argv[1]
    if name not in TYPE_INFO:
        print(f"new_type: '{name}' is not in schema.yml — declare it there first", file=sys.stderr)
        print(f"          known types: {', '.join(TYPE_INFO)}", file=sys.stderr)
        return 1

    spec = TYPE_INFO[name]
    created = []

    folder = WIKI / spec["folder"]
    if not folder.exists():
        folder.mkdir(parents=True)
        (folder / ".gitkeep").touch()
        created.append(f"wiki/{spec['folder']}/")

    template = TEMPLATES / f"{name}.md"
    if not template.exists():
        template.write_text(TEMPLATE.format(name=name), encoding="utf-8")
        created.append(str(template.relative_to(ROOT)))

    instructions = INSTRUCTIONS_DIR / spec.get("instructions", f"{name}.instructions.md")
    if not instructions.exists():
        instructions.write_text(
            INSTRUCTION.format(name=name, folder=spec["folder"], label=spec["label"]),
            encoding="utf-8",
        )
        created.append(str(instructions.relative_to(ROOT)))

    if not created:
        print(f"new_type: '{name}' already has everything it needs")
        return 0

    print(f"new_type: created {', '.join(created)}")
    print("  now write the TODO sections, then run `make schema` to restamp the docs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
