#!/usr/bin/env python3
"""Move or re-type a page, rewriting every link that pointed at it.

This exists so that choosing the wrong type is cheap. It used to be expensive — the relative
links that make the wiki work in both Obsidian and the built site all had to be found and fixed
by hand — which is why the assistant was told to stop and ask which type to use. Now it can pick
the obvious one, say what it picked, and you can overrule it in one command.

Usage:
    python3 scripts/move_page.py <page> [--type <type>] [--slug <new-slug>]

Examples:
    python3 scripts/move_page.py content/topics/acme-migration.md --type project
    python3 scripts/move_page.py content/people/jane.md --slug jane-doe
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

from wikilib import ROOT, TYPES, WIKI, Page, pages


def rewrite_links(old: Path, new: Path) -> list[str]:
    """Point every relative link at the page's new home. Returns the files changed."""
    changed = []
    for page in pages(include_special=True):
        if page.path.resolve() == old.resolve():
            continue
        text = page.text
        updated = text
        for _, target in page.links(include_generated=True):
            if page.resolve(target) != old.resolve():
                continue
            anchor = target.split("#", 1)[1] if "#" in target else None
            fixed = os.path.relpath(new, page.path.parent).replace(os.sep, "/")
            if anchor:
                fixed = f"{fixed}#{anchor}"
            updated = updated.replace(f"]({target})", f"]({fixed})")
        if updated != text:
            page.path.write_text(updated, encoding="utf-8")
            changed.append(page.wiki_rel)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("page", help="path to the page, e.g. content/topics/thing.md")
    parser.add_argument("--type", dest="new_type", choices=sorted(TYPES), default=None)
    parser.add_argument("--slug", default=None)
    args = parser.parse_args()

    old = (ROOT / args.page).resolve() if not Path(args.page).is_absolute() else Path(args.page)
    if not old.exists():
        print(f"move_page: {args.page} does not exist", file=sys.stderr)
        return 1
    if not args.new_type and not args.slug:
        print("move_page: give --type, --slug, or both — nothing to do otherwise", file=sys.stderr)
        return 1

    page = Page(old)
    new_type = args.new_type or page.get("type")
    if new_type not in TYPES:
        print(f"move_page: unknown type '{new_type}' — declare it in schema.yml first", file=sys.stderr)
        return 1

    slug = args.slug or old.stem
    new = WIKI / TYPES[new_type] / f"{slug}.md"
    if new.resolve() == old.resolve():
        print("move_page: already where you are asking to put it")
        return 0
    if new.exists():
        print(f"move_page: {new.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1

    # Retype the frontmatter before moving, so the page never sits in a folder that contradicts it.
    text = page.text
    if args.new_type and page.get("type") != new_type:
        text = re.sub(r"^type:.*$", f"type: {new_type}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated:.*$", f"updated: {date.today().isoformat()}", text, count=1, flags=re.MULTILINE)

    new.parent.mkdir(parents=True, exist_ok=True)
    new.write_text(text, encoding="utf-8")

    # The links inside the moved page are relative to where it now sits, so fix those too.
    moved = Page(new)
    fixed_self = moved.text
    for _, target in moved.links(include_generated=True):
        resolved = (old.parent / target.split("#")[0]).resolve()
        if not resolved.exists():
            continue
        anchor = target.split("#", 1)[1] if "#" in target else None
        rel = os.path.relpath(resolved, new.parent).replace(os.sep, "/")
        if anchor:
            rel = f"{rel}#{anchor}"
        if rel != target:
            fixed_self = fixed_self.replace(f"]({target})", f"]({rel})")
    if fixed_self != moved.text:
        new.write_text(fixed_self, encoding="utf-8")

    old.unlink()
    changed = rewrite_links(old, new)

    print(f"move_page: {old.relative_to(ROOT)} -> {new.relative_to(ROOT)}")
    if args.new_type:
        print(f"  type is now '{new_type}'")
    print(f"  rewrote links on {len(changed)} page(s)" + (f": {', '.join(changed)}" if changed else ""))
    print("  run `make index`, and add a line to content/log.md saying why it moved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
