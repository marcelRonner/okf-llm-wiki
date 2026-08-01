#!/usr/bin/env python3
"""Mechanical consistency checks for the wiki.

Anything a computer can check reliably should not depend on an assistant remembering it.
This is the deterministic half of the lint operation; `.github/prompts/lint.prompt.md`
covers contradictions, staleness and judgement.

Checks:
    W1  Every page has valid frontmatter with the required keys
    W2  `type:` is known, and the page lives in the folder matching its type
    W3  Every relative link resolves to a file that exists
    W4  Every page is reachable by following links from index.md or log.md
    W5  Every `sources:` entry points at an existing source page
    W6  Every source page's raw file exists, and every raw file has a source page
    W7  `inbox/` is empty (anything left in it is unprocessed material)
    W8  `updated:` is not older than `created:`, and neither is in the future

Index freshness is checked separately by `build_index.py --check`, which `make lint` runs.

Usage:  python3 scripts/lint_wiki.py
Exit:   0 = clean, 1 = findings
"""

from __future__ import annotations

import re
import sys
from datetime import date

from wikilib import (INBOX, INDEX, LOG, RAW, REQUIRED_KEYS, ROOT, TYPES, WIKI,
                     Page, inbox_items, pages)

findings: list[str] = []


def report(where, line, check: str, message: str) -> None:
    try:
        loc = where.relative_to(ROOT)
    except (AttributeError, ValueError):
        loc = where
    findings.append(f"{loc}:{line or 1}: [{check}] {message}")


def as_date(value):
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- W1, W2, W8
def check_frontmatter(all_pages: list[Page]) -> None:
    today = date.today()
    for page in all_pages:
        if page.error:
            report(page.path, 1, "W1", page.error)
            continue

        missing = [k for k in REQUIRED_KEYS if not page.get(k)]
        if missing:
            report(page.path, 1, "W1", f"frontmatter missing: {', '.join(missing)}")

        summary = page.get("summary")
        if summary and len(str(summary)) > 200:
            report(page.path, 1, "W1", "summary is longer than 200 chars — it goes in the index, keep it to one sentence")

        type_name = page.get("type")
        if type_name and type_name not in TYPES:
            report(page.path, 1, "W2", f"unknown type '{type_name}' — expected one of: {', '.join(TYPES)}")
        elif type_name:
            expected = TYPES[type_name]
            actual = page.path.relative_to(WIKI).parts[0]
            if actual != expected:
                report(page.path, 1, "W2", f"type '{type_name}' belongs in wiki/{expected}/, but page is in wiki/{actual}/")

        created, updated = as_date(page.get("created")), as_date(page.get("updated"))
        if page.get("created") and not created:
            report(page.path, 1, "W8", f"created: '{page.get('created')}' is not a YYYY-MM-DD date")
        if page.get("updated") and not updated:
            report(page.path, 1, "W8", f"updated: '{page.get('updated')}' is not a YYYY-MM-DD date")
        if created and updated and updated < created:
            report(page.path, 1, "W8", f"updated ({updated}) is before created ({created})")
        for label, value in (("created", created), ("updated", updated)):
            if value and value > today:
                report(page.path, 1, "W8", f"{label} ({value}) is in the future")


# --------------------------------------------------------------------------- W3
def check_links(all_pages: list[Page]) -> None:
    for page in all_pages:
        for lineno, target in page.links():
            if not page.resolve(target).exists():
                report(page.path, lineno, "W3", f"broken link -> {target}")


# --------------------------------------------------------------------------- W4
def check_reachable(all_pages: list[Page]) -> None:
    seen = set()
    queue = [Page(p) for p in (INDEX, LOG) if p.exists()]
    seen.update(p.path.resolve() for p in queue)

    while queue:
        page = queue.pop()
        for _, target in page.links():
            resolved = page.resolve(target)
            if resolved.suffix == ".md" and resolved.exists() and resolved not in seen:
                seen.add(resolved)
                queue.append(Page(resolved))

    for page in all_pages:
        if page.path.resolve() not in seen:
            report(page.path, 1, "W4", "orphan — nothing links here, so nobody will find it")


# --------------------------------------------------------------------------- W5
def check_sources_field(all_pages: list[Page]) -> None:
    for page in all_pages:
        listed = page.get("sources") or []
        if isinstance(listed, str):
            listed = [listed]
        for entry in listed:
            target = (WIKI / str(entry)).resolve()
            if not target.exists():
                report(page.path, 1, "W5", f"sources: '{entry}' does not exist (paths are relative to wiki/)")
            elif target.parent.name != "sources":
                report(page.path, 1, "W5", f"sources: '{entry}' is not a source page")


# --------------------------------------------------------------------------- W6
def check_raw_pairing(all_pages: list[Page]) -> None:
    source_pages = [p for p in all_pages if p.get("type") == "source"]

    referenced = set()
    for page in source_pages:
        raw_links = [t for _, t in page.links() if "/raw/" in t or t.startswith("../../raw/")]
        if not raw_links:
            report(page.path, 1, "W6", "source page does not link to its file in raw/")
        for target in raw_links:
            referenced.add(page.resolve(target).resolve())

    for item in sorted(RAW.iterdir()):
        if not item.is_file() or item.name == ".gitkeep":
            continue
        if item.resolve() not in referenced:
            report(item, 1, "W6", "file in raw/ has no source page — it was filed but never written up")


# --------------------------------------------------------------------------- W7
def check_inbox() -> None:
    for item in inbox_items():
        report(item, 1, "W7", "unprocessed — run /ingest, or move it out of inbox/")


# --------------------------------------------------------------------------- main
def main() -> int:
    all_pages = pages()

    check_frontmatter(all_pages)
    check_links(all_pages)
    check_reachable(all_pages)
    check_sources_field(all_pages)
    check_raw_pairing(all_pages)
    check_inbox()

    stubs = sum(1 for p in all_pages if p.get("status") == "stub")

    if not findings:
        print(f"lint: OK — {len(all_pages)} pages ({stubs} stubs), no findings")
        return 0

    print(f"lint: {len(findings)} finding(s)\n")
    for finding in sorted(findings):
        print(f"  {finding}")
    print("\nSee .github/instructions/ for the conventions these checks enforce.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
