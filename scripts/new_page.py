#!/usr/bin/env python3
"""Create a new wiki page from its template, with frontmatter filled in.

Saves the assistant (and you) from hand-typing frontmatter and getting the folder wrong.

Usage:
    python3 scripts/new_page.py <type> "<title>" [--summary "..."] [--slug my-slug] [--stub]
                                                 [--link-from wiki/projects/x.md]

Examples:
    python3 scripts/new_page.py project "Acme Migration"
    python3 scripts/new_page.py person "Jane Doe" --summary "Platform lead at Acme"
    python3 scripts/new_page.py topic "Event sourcing" --link-from wiki/projects/acme-migration.md

`--link-from` appends the new page to another page's `Related` section. A page nothing links to
is one you will never find again, so it is worth the extra flag at creation time rather than a
warning to clean up later.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date

from wikilib import ROOT, TEMPLATES, TYPE_INFO, TYPES, WIKI


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def link_from(source_rel: str, target_path, title: str) -> None:
    """Append a Related entry on an existing page, creating the section if it has none."""
    source = (ROOT / source_rel).resolve()
    if not source.exists():
        print(f"new_page: --link-from {source_rel} does not exist; page created but unlinked", file=sys.stderr)
        return

    rel = os.path.relpath(target_path, source.parent).replace(os.sep, "/")
    entry = f"- [{title}]({rel}) — "
    text = source.read_text(encoding="utf-8")

    if re.search(r"^## Related\s*$", text, re.MULTILINE):
        # Insert directly under the heading, so the newest link is the one you see first.
        text = re.sub(r"(^## Related\s*\n)", rf"\1\n{entry}\n", text, count=1, flags=re.MULTILINE)
    else:
        text = text.rstrip("\n") + f"\n\n## Related\n\n{entry}\n"

    source.write_text(text, encoding="utf-8")
    print(f"new_page: linked from {source_rel} — say why, the dash is left open on purpose")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("type", choices=sorted(TYPES))
    parser.add_argument("title")
    parser.add_argument("--summary", default="")
    parser.add_argument("--slug", default=None)
    parser.add_argument("--stub", action="store_true", help="mark the page as a stub")
    parser.add_argument("--link-from", default=None, metavar="PAGE",
                        help="append this page to PAGE's Related section")
    args = parser.parse_args()

    today = date.today().isoformat()
    slug = args.slug or slugify(args.title)

    # Some types sort chronologically, so their filenames lead with a date. schema.yml decides.
    if TYPE_INFO[args.type].get("dated_filenames") and not re.match(r"\d{4}-\d{2}-\d{2}-", slug):
        slug = f"{today}-{slug}"

    target = WIKI / TYPES[args.type] / f"{slug}.md"
    if target.exists():
        print(f"new_page: {target.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1

    template = TEMPLATES / f"{args.type}.md"
    if not template.exists():
        print(f"new_page: no template at {template.relative_to(ROOT)} — run `make new-type TYPE={args.type}`", file=sys.stderr)
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

    if args.link_from:
        link_from(args.link_from, target, args.title)
    else:
        print("  nothing links here yet — `make lint` will say so (a warning, not an error)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
