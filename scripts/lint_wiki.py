#!/usr/bin/env python3
"""Mechanical consistency checks for the wiki.

Anything a computer can check reliably should not depend on an assistant remembering it.
This is the deterministic half of the lint operation; `.claude/commands/lint.md`
covers contradictions, staleness and judgement.

Findings come at two severities, because "you have not finished this page yet" and "this page
points at a file that does not exist" are not the same problem, and treating them the same is
what made adding a page feel like breaking something.

  ERRORS — the wiki is wrong. These fail.
    E1  frontmatter is missing, invalid, or missing a required key
    E2  `type:` is unknown, or the page is filed in the wrong folder
    E3  a relative link points at a file that does not exist
    E4  a `sources:` entry is missing, or is not a source page
    E5  a source page's raw file is missing, or a raw file was never written up
    E6  `updated:` is before `created:`, or either is in the future

  WARNINGS — the wiki is unfinished. These are reported and do not fail.
    W1  nothing links to this page, so nobody will find it except through the index
    W2  the summary is still a placeholder, or is too long for the index
    W3  a stub that has been a stub for a long time
    W4  the page has grown past the length where it wants splitting
    W5  a tag that looks like a typo of an established one
    W6  material sitting unprocessed in inbox/
    W7  a type declared in schema.yml with no template or no folder

Usage:  python3 scripts/lint_wiki.py [--strict]
        --strict treats warnings as errors. Nothing uses it by default: a site that will not
        build because a page is 401 words is a check people learn to bypass. It is there for
        a CI job whose owner wants the higher bar (`make lint STRICT=1`).
Exit:   0 = clean (or warnings only), 1 = findings that fail
"""

from __future__ import annotations

import sys
from collections import Counter
from difflib import get_close_matches
from datetime import date

from wikilib import (INBOX, INDEX, LIMITS, LOG, RAW, REQUIRED_KEYS, ROOT, TAGS, TEMPLATES,
                     TYPE_INFO, TYPES, WIKI, Page, as_date, inbound_links, inbox_items, pages)

errors: list[str] = []
warnings: list[str] = []

PLACEHOLDER = LIMITS.get("placeholder", "TODO")
MAX_SUMMARY = LIMITS.get("summary_chars", 200)
MAX_WORDS = LIMITS.get("page_words", 400)
STUB_DAYS = LIMITS.get("stub_days", 90)


def report(bucket: list[str], where, line, check: str, message: str) -> None:
    try:
        loc = where.relative_to(ROOT)
    except (AttributeError, ValueError):
        loc = where
    bucket.append(f"{loc}:{line or 1}: [{check}] {message}")


def error(where, line, check, message):
    report(errors, where, line, check, message)


def warn(where, line, check, message):
    report(warnings, where, line, check, message)


# --------------------------------------------------------------------------- E1, E2, E6, W2, W4
def check_pages(all_pages: list[Page]) -> None:
    today = date.today()
    for page in all_pages:
        if page.error:
            error(page.path, 1, "E1", page.error)
            continue

        missing = [k for k in REQUIRED_KEYS if not page.get(k)]
        if missing:
            error(page.path, 1, "E1", f"frontmatter missing: {', '.join(missing)}")

        summary = str(page.get("summary") or "")
        if PLACEHOLDER in summary:
            warn(page.path, 1, "W2", f"summary is still a placeholder — it is what the index shows")
        elif len(summary) > MAX_SUMMARY:
            warn(page.path, 1, "W2", f"summary is {len(summary)} chars — over {MAX_SUMMARY}, keep it to one sentence")

        type_name = page.get("type")
        if type_name and type_name not in TYPES:
            error(page.path, 1, "E2", f"unknown type '{type_name}' — declare it in schema.yml, or use one of: {', '.join(TYPES)}")
        elif type_name:
            expected = TYPES[type_name]
            actual = page.path.relative_to(WIKI).parts[0]
            if actual != expected:
                error(page.path, 1, "E2", f"type '{type_name}' belongs in content/{expected}/, but page is in content/{actual}/ — `make move` fixes this and the links")

        created, updated = as_date(page.get("created")), as_date(page.get("updated"))
        if page.get("created") and not created:
            error(page.path, 1, "E6", f"created: '{page.get('created')}' is not a YYYY-MM-DD date")
        if page.get("updated") and not updated:
            error(page.path, 1, "E6", f"updated: '{page.get('updated')}' is not a YYYY-MM-DD date")
        if created and updated and updated < created:
            error(page.path, 1, "E6", f"updated ({updated}) is before created ({created})")
        for label, value in (("created", created), ("updated", updated)):
            if value and value > today:
                error(page.path, 1, "E6", f"{label} ({value}) is in the future")

        words = page.word_count()
        if words > MAX_WORDS:
            warn(page.path, 1, "W4", f"{words} words — past {MAX_WORDS}, look for a section that wants its own page")

        if page.get("status") == "stub" and updated:
            age = (today - updated).days
            if age > STUB_DAYS:
                warn(page.path, 1, "W3", f"stub untouched for {age} days — fill it, or admit it is not needed")


# --------------------------------------------------------------------------- E3
def check_links(all_pages: list[Page]) -> None:
    for page in all_pages:
        for lineno, target in page.links():
            if not page.resolve(target).exists():
                error(page.path, lineno, "E3", f"broken link -> {target}")


# --------------------------------------------------------------------------- W1
def check_connected(all_pages: list[Page]) -> None:
    """Reachable by following editorial links out from the log.

    The generated catalogues are neither a starting point nor a stepping stone. index.md links
    to every page by construction, so any walk that is allowed to pass *through* it reaches
    everything and the check silently passes on a wiki full of unreachable pages — which is
    exactly what the first version of this did. Excluding them from the page list is not enough;
    they have to be excluded from the traversal. Generated backlink blocks are skipped for the
    same reason (see Page.links).
    """
    catalogues = {INDEX.resolve(), TAGS.resolve()}
    seen = set(catalogues)
    queue = [Page(LOG)] if LOG.exists() else []
    seen.update(p.path.resolve() for p in queue)

    while queue:
        page = queue.pop()
        for _, target in page.links():
            resolved = page.resolve(target)
            if resolved.suffix == ".md" and resolved.exists() and resolved not in seen:
                seen.add(resolved)
                queue.append(Page(resolved))

    incoming = inbound_links(all_pages)
    for page in all_pages:
        if page.path.resolve() in seen:
            continue
        if incoming[page.path.resolve()]:
            continue
        warn(page.path, 1, "W1", "nothing links here — it exists, but only the index will ever show it")


# --------------------------------------------------------------------------- E4
def check_sources_field(all_pages: list[Page]) -> None:
    for page in all_pages:
        listed = page.get("sources") or []
        if isinstance(listed, str):
            listed = [listed]
        for entry in listed:
            target = (WIKI / str(entry)).resolve()
            if not target.exists():
                error(page.path, 1, "E4", f"sources: '{entry}' does not exist (paths are relative to content/)")
            elif target.parent.name != TYPES["source"]:
                error(page.path, 1, "E4", f"sources: '{entry}' is not a source page")


# --------------------------------------------------------------------------- E5
def check_raw_pairing(all_pages: list[Page]) -> None:
    """Every source page has its raw file, and every raw file has been written up.

    Source pages with `origin: owner` are exempt: they record what the owner said in a `/note`,
    which never had a document behind it. That exemption is the whole reason the field exists —
    an owner statement is anchored and citable without a fabricated file in raw/.
    """
    source_pages = [p for p in all_pages if p.get("type") == "source"]

    referenced = set()
    for page in source_pages:
        if page.get("origin") == "owner":
            continue
        raw_links = [t for _, t in page.links() if "/raw/" in t or t.startswith("../../raw/")]
        if not raw_links:
            error(page.path, 1, "E5", "source page does not link to its file in raw/ (or set `origin: owner` if it never had one)")
        for target in raw_links:
            referenced.add(page.resolve(target).resolve())

    for item in sorted(RAW.iterdir()):
        if not item.is_file() or item.name == ".gitkeep":
            continue
        if item.resolve() not in referenced:
            error(item, 1, "E5", "file in raw/ has no source page — it was filed but never written up")


# --------------------------------------------------------------------------- W5
def check_tags(all_pages: list[Page]) -> None:
    """Catch tags that are near-misses of an established one.

    Not "used only once" — on a young wiki that is every tag, and a check that fires on
    everything gets ignored, which costs more than it saves. What is worth flagging is
    `architecure` sitting next to `architecture` on four other pages: a tag that splits a
    subject in two without either page looking wrong.
    """
    counts = Counter(tag for page in all_pages for tag in page.tags())
    established = {tag for tag, n in counts.items() if n > 1}
    if not established:
        return

    for page in all_pages:
        for tag in page.tags():
            if counts[tag] > 1:
                continue
            near = get_close_matches(tag, sorted(established), n=1, cutoff=0.85)
            if near:
                warn(page.path, 1, "W5", f"tag '{tag}' is one page's only use, and looks like '{near[0]}' — typo, or two names for one subject?")


# --------------------------------------------------------------------------- W6
def check_inbox() -> None:
    for item in inbox_items():
        warn(item, 1, "W6", "unprocessed — run /ingest, or move it out of inbox/")


# --------------------------------------------------------------------------- W7
def check_schema() -> None:
    for name, spec in TYPE_INFO.items():
        if not (TEMPLATES / f"{name}.md").exists():
            warn(TEMPLATES / f"{name}.md", 1, "W7", f"type '{name}' is declared in schema.yml but has no template")
        folder = WIKI / spec["folder"]
        if not folder.is_dir():
            warn(folder, 1, "W7", f"type '{name}' is declared in schema.yml but content/{spec['folder']}/ does not exist")


# --------------------------------------------------------------------- main
def main() -> int:
    strict = "--strict" in sys.argv
    all_pages = pages()

    check_pages(all_pages)
    check_links(all_pages)
    check_connected(all_pages)
    check_sources_field(all_pages)
    check_raw_pairing(all_pages)
    check_tags(all_pages)
    check_inbox()
    check_schema()

    stubs = sum(1 for p in all_pages if p.get("status") == "stub")
    noun = "page" if len(all_pages) == 1 else "pages"

    if not errors and not warnings:
        print(f"lint: OK — {len(all_pages)} {noun} ({stubs} stubs), no findings")
        return 0

    if errors:
        print(f"lint: {len(errors)} error(s)\n")
        for finding in sorted(errors):
            print(f"  {finding}")

    if warnings:
        if errors:
            print()
        print(f"lint: {len(warnings)} warning(s) — unfinished, not broken\n")
        for finding in sorted(warnings):
            print(f"  {finding}")

    print("\nSee .claude/rules/ for the conventions these checks enforce.")

    if errors:
        return 1
    if strict:
        print("lint: --strict, so warnings fail")
        return 1
    print(f"lint: no errors — {len(all_pages)} {noun} ({stubs} stubs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
