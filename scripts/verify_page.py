#!/usr/bin/env python3
"""Record that the owner read a page and found it true: append an OKF `verified` event.

**Run by the owner, never by the assistant.** `verified:` is the one signal in this wiki that
separates "checked" from "merely written", and AGENTS.md forbids the assistant from writing it.
This script exists so that the owner's confirmation costs one command instead of hand-typing YAML
that is easy to get subtly wrong: an actor without the `human:` prefix, or a date without a time
and offset, fails lint.

Usage:
    make verify PAGE=content/topics/llm-wiki.md [WHO=owner]

It appends `{ by: human:<WHO>, at: <now, UTC> }` to the page's `verified:` list, creating the list
if there is none and turning a bare single mapping into a list first, so every earlier confirmation
survives. The `human:` prefix is not decoration: OKF consumers derive the human-reviewed trust tier
from it (§5.3, §7), and a sign-off written any other way is invisible to them.

`updated:` is deliberately left alone. Confirming a page is not changing it, and OKF keeps the two
apart for that reason (§5.2): content can change without re-confirmation, and facts can be
re-confirmed without regeneration.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from wikilib import FRONTMATTER_RE, REFERENCES, ROOT, WIKI, verified_events

# The `verified:` key and everything belonging to it: indented lines, or list items written flush.
VERIFIED_BLOCK_RE = re.compile(r"^verified:.*\n(?:(?:[ \t]+|- ).*\n)*", re.M)
WHO_RE = re.compile(r"[^\s:]+")


def _scalar(value) -> str:
    if isinstance(value, datetime):
        if value.tzinfo:
            return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return value.isoformat()
    return str(value)


def add_verification(text: str, who: str, at: datetime) -> str:
    """Return `text` with one more verification event; the body and every other key untouched."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("page has no frontmatter to record a verification in")

    meta = yaml.safe_load(match.group(1)) or {}
    events = verified_events(meta if isinstance(meta, dict) else {})
    if not isinstance(events, list) or not all(isinstance(e, dict) for e in events):
        raise ValueError("existing `verified:` is malformed — fix it by hand first, so nothing is lost")
    events = events + [{"by": f"human:{who}", "at": at}]

    lines = ["verified:"]
    for event in events:
        for i, (key, value) in enumerate(event.items()):
            lines.append(f"  {'- ' if i == 0 else '  '}{key}: {_scalar(value)}")
    block = "\n".join(lines) + "\n"

    frontmatter = match.group(1) + "\n"
    if VERIFIED_BLOCK_RE.search(frontmatter):
        frontmatter = VERIFIED_BLOCK_RE.sub(lambda _: block, frontmatter, count=1)
    else:
        frontmatter += block
    return text[: match.start(1)] + frontmatter.rstrip("\n") + text[match.end(1):]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("page", help="the page to mark verified, e.g. content/topics/llm-wiki.md")
    parser.add_argument("--who", default="owner", help="the id after `human:` (default: owner)")
    args = parser.parse_args()

    if not WHO_RE.fullmatch(args.who):
        print(f"verify: '{args.who}' cannot be an actor id — no spaces or colons", file=sys.stderr)
        return 1
    path = (ROOT / args.page).resolve()
    if not path.is_file() or WIKI.resolve() not in path.parents:
        print(f"verify: {args.page} is not a page under content/", file=sys.stderr)
        return 1
    if REFERENCES.resolve() in path.parents:
        print("verify: originals in content/references/ are evidence, not claims — verify the page written from them",
              file=sys.stderr)
        return 1

    try:
        new = add_verification(path.read_text(encoding="utf-8"), args.who, datetime.now(timezone.utc))
    except ValueError as exc:
        print(f"verify: {exc}", file=sys.stderr)
        return 1
    path.write_text(new, encoding="utf-8")
    print(f"verify: recorded human:{args.who} on {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
