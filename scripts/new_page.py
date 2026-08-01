#!/usr/bin/env python3
"""Create a new wiki page from its template, with frontmatter filled in.

Saves the assistant (and you) from hand-typing frontmatter and getting the folder wrong.

Usage:
    python3 scripts/new_page.py <type> "<title>" [--summary "..."] [--slug my-slug] [--stub]

Examples:
    python3 scripts/new_page.py project "Acme Migration"
    python3 scripts/new_page.py person "Jane Doe" --summary "Platform lead at Acme"
    python3 scripts/new_page.py decision "Use Postgres for the event store"
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date

from wikilib import ROOT, TYPES, WIKI

TEMPLATES = ROOT / "templates"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("type", choices=sorted(TYPES))
    parser.add_argument("title")
    parser.add_argument("--summary", default="")
    parser.add_argument("--slug", default=None)
    parser.add_argument("--stub", action="store_true", help="mark the page as a stub")
    args = parser.parse_args()

    today = date.today().isoformat()
    slug = args.slug or slugify(args.title)

    # Decisions and sources sort chronologically, so their filenames lead with a date.
    if args.type in ("decision", "source") and not re.match(r"\d{4}-\d{2}-\d{2}-", slug):
        slug = f"{today}-{slug}"

    target = WIKI / TYPES[args.type] / f"{slug}.md"
    if target.exists():
        print(f"new_page: {target.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1

    template = TEMPLATES / f"{args.type}.md"
    if not template.exists():
        print(f"new_page: no template at {template.relative_to(ROOT)}", file=sys.stderr)
        return 1

    content = (
        template.read_text(encoding="utf-8")
        .replace("{{TITLE}}", args.title)
        .replace("{{SUMMARY}}", args.summary or "TODO — one sentence, this appears in the index")
        .replace("{{DATE}}", today)
        .replace("{{STATUS}}", "stub" if args.stub else "")
    )
    # Drop an empty status line rather than leaving `status:` dangling.
    content = "\n".join(l for l in content.splitlines() if l.strip() != "status:") + "\n"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"new_page: created {target.relative_to(ROOT)}")
    print("  remember: link it from somewhere, or `make lint` will report it as an orphan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
