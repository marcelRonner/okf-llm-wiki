#!/usr/bin/env python3
"""Mechanical consistency checks for the wiki.

Anything a computer can check reliably should not depend on an assistant remembering it.
This is the deterministic half of the lint operation; `.claude/skills/lint/SKILL.md`
covers contradictions, staleness and judgement.

Findings come at two severities, because "you have not finished this page yet" and "this page
points at a file that does not exist" are not the same problem, and treating them the same is
what made adding a page feel like breaking something.

  ERRORS — the wiki is wrong. These fail.
    E1  frontmatter is missing, invalid, or missing a required key
    E2  `type:` is unknown, or the page is filed in the wrong folder
    E3  a relative link points at a file that does not exist
    E4  a `sources:` entry is missing, is not a source page, or is not in OKF's shape
    E5  a source page's raw file is missing, or a raw file was never written up
    E6  `updated:` is before `created:`, or either is in the future
    E7  the page breaks OKF conformance — see `content/topics/open-knowledge-format.md`

  WARNINGS — the wiki is unfinished. These are reported and do not fail.
    W1  nothing links to this page, so nobody will find it except through the index
    W2  the description is still a placeholder, or is too long for the index
    W3  a draft that has been a draft for a long time
    W4  the page has grown past the length where it wants splitting
    W5  a tag that looks like a typo of an established one
    W6  material sitting unprocessed in inbox/
    W7  a type declared in schema.yml with no template or no folder
    W8  a source page with no `resource:`, or one pointing at a file that is gone
    W9  `stale_after:` has passed, or `verified:` is absent on a page old enough to want it

Usage:  python3 scripts/lint_wiki.py [--strict]
        --strict treats warnings as errors. Nothing uses it by default: a site that will not
        build because a page is 401 words is a check people learn to bypass. It is there for
        a CI job whose owner wants the higher bar (`make lint STRICT=1`).
Exit:   0 = clean (or warnings only), 1 = findings that fail
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from difflib import get_close_matches
from datetime import date, datetime

from wikilib import (FENCE_RE, INDEX, LIMITS, LOG, RAW, REQUIRED_KEYS, ROOT, TAGS, TEMPLATES,
                     TYPE_INFO, TYPES, WIKI, Page, as_date, blank_out, inbound_links, inbox_items,
                     pages)

# Filenames the Open Knowledge Format reserves, and so exempts from needing a `type`.
OKF_RESERVED = ("index.md", "log.md")

# OKF v0.2 enumerates these. `draft` is this wiki's old `stub`, `deprecated` its `superseded`.
OKF_STATUS = ("draft", "stable", "deprecated")
OKF_DATETIME_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")
OKF_ACTOR_RE = re.compile(r"(?:human|process):[^\s:]+$|[^\s/]+/[^\s/]+$")

errors: list[str] = []
warnings: list[str] = []

PLACEHOLDER = LIMITS.get("placeholder", "TODO")
MAX_DESCRIPTION = LIMITS.get("description_chars", 200)
MAX_WORDS = LIMITS.get("page_words", 400)
STUB_DAYS = LIMITS.get("stub_days", 90)
STALE_DAYS = LIMITS.get("unverified_days", 365)


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

        description = str(page.get("description") or "")
        if PLACEHOLDER in description:
            warn(page.path, 1, "W2", "description is still a placeholder — it is what the index shows")
        elif len(description) > MAX_DESCRIPTION:
            warn(page.path, 1, "W2", f"description is {len(description)} chars — over {MAX_DESCRIPTION}, keep it to one sentence")

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

        status = page.get("status")
        if status and status not in OKF_STATUS:
            error(page.path, 1, "E7", f"status '{status}' is outside OKF v0.2's set: {', '.join(OKF_STATUS)}")

        words = page.word_count()
        if words > MAX_WORDS:
            warn(page.path, 1, "W4", f"{words} words — past {MAX_WORDS}, look for a section that wants its own page")

        if page.get("status") == "draft" and updated:
            age = (today - updated).days
            if age > STUB_DAYS:
                warn(page.path, 1, "W3", f"draft untouched for {age} days — fill it, or admit it is not needed")


# --------------------------------------------------------------------------- W8, W9
def check_okf_families(all_pages: list[Page]) -> None:
    """The OKF v0.2 field families this wiki adopted, checked for the promises they make.

    `resource` and `verified` are only recommended by the spec, never required, so nothing here
    is an error. They are warnings because each one is a real question about the wiki rather than
    a defect: a source with no resource cannot be traced to its original, and a page nothing has
    verified is a page the owner has not yet said is true.
    """
    today = date.today()
    for page in all_pages:
        if page.get("type") == "source":
            resource = str(page.get("resource") or "").strip()
            if not resource:
                warn(page.path, 1, "W8", "no `resource:` — say where the original is, as a URL or ../raw/<file>")
            elif "://" not in resource and not (page.path.parent / resource).exists():
                warn(page.path, 1, "W8", f"resource: '{resource}' does not exist")

        stale_after = page.get("stale_after")
        if stale_after is not None:
            timestamp = normalise_okf_datetime(stale_after)
            if not timestamp:
                error(page.path, 1, "E7", "stale_after must be an ISO 8601 datetime with an explicit UTC offset")
            elif datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date() <= today:
                warn(page.path, 1, "W9", f"stale_after passed on {timestamp} — re-read it, then move the date or fix the page")

        verified = page.get("verified")
        updated = as_date(page.get("updated"))
        if not verified and updated and (today - updated).days > STALE_DAYS:
            warn(page.path, 1, "W9",
                 f"nothing has verified this in {(today - updated).days} days — `verified:` records that the owner read it and it was true")


# --------------------------------------------------------------------------- E7
def check_okf_conformance() -> None:
    """The three conformance criteria of OKF v0.2, §11.

    This walks `content/` directly rather than using `pages()`, because the criteria apply to
    every file in the bundle — including the generated section pages, which `pages()` excludes as
    furniture. Those are exactly where conformance was broken when it was first measured, so a
    check that skipped them would be worthless.

    Criterion 3 checks the reserved root log's required date-grouped, newest-first list structure.
    """
    for path in sorted(WIKI.rglob("*.md")):
        page = Page(path)
        if page.error:
            error(path, 1, "E7", f"OKF criterion 1: {page.error} — every file in the bundle needs parseable frontmatter")
            continue
        if path.name in OKF_RESERVED:
            continue
        if not str(page.get("type") or "").strip():
            error(path, 1, "E7", f"OKF criterion 2: no `type:` — every file that is not {' or '.join(OKF_RESERVED)} needs one")

    if LOG.exists():
        log = Page(LOG)
        body = blank_out(log.body, FENCE_RE)
        headings = [(lineno, text) for lineno, text in enumerate(body.splitlines(), 1)
                    if text.startswith("## ")]
        dates = []
        for lineno, text in headings:
            value = text[3:].strip()
            parsed = as_date(value)
            if not parsed or value != parsed.isoformat():
                error(LOG, lineno, "E7", "OKF criterion 3: log date headings must use exactly YYYY-MM-DD")
                continue
            dates.append((lineno, parsed))
        if not dates:
            error(LOG, 1, "E7", "OKF criterion 3: log.md needs at least one YYYY-MM-DD date heading")
        elif any(later > earlier for (_, earlier), (_, later) in zip(dates, dates[1:])):
            error(LOG, 1, "E7", "OKF criterion 3: log date headings must be newest first")
        lines = body.splitlines()
        for index, (lineno, _) in enumerate(dates):
            end = dates[index + 1][0] - 1 if index + 1 < len(dates) else len(lines)
            entries = [line for line in lines[lineno:end] if line.strip()]
            if not entries or not entries[0].startswith("- "):
                error(LOG, lineno, "E7", "OKF criterion 3: each date group must begin with a flat-list entry")
            for entry_line, entry in enumerate(lines[lineno:end], lineno + 1):
                if entry.strip() and not (entry.startswith("- ") or entry.startswith(("  ", "\t"))):
                    error(LOG, entry_line, "E7", "OKF criterion 3: log date groups may contain only list items or indented list continuations")


def check_okf_metadata(all_pages: list[Page]) -> None:
    """Validate the shape of adopted optional OKF trust and lifecycle metadata."""
    for page in all_pages:
        generated = page.get("generated")
        if generated is not None:
            if not isinstance(generated, dict):
                error(page.path, 1, "E7", "generated: must be a mapping with `by` and `at`")
                continue
            actor = str(generated.get("by") or "")
            timestamp = normalise_okf_datetime(generated.get("at"))
            if not OKF_ACTOR_RE.fullmatch(actor):
                error(page.path, 1, "E7", "generated.by must use `producer/version`, `human:<id>`, or `process:<id>`")
            if not timestamp:
                error(page.path, 1, "E7", "generated.at must be an ISO 8601 datetime with an explicit UTC offset")

        if page.get("verified") is None:
            continue
        events = page.verified_events()
        if not isinstance(events, list):
            error(page.path, 1, "E7", "verified: must be a mapping or list of mappings")
            continue
        for event in events:
            if not isinstance(event, dict):
                error(page.path, 1, "E7", "verified: every event must be a mapping with `by` and `at`")
                continue
            actor = str(event.get("by") or "")
            if not OKF_ACTOR_RE.fullmatch(actor):
                error(page.path, 1, "E7", "verified.by must use `producer/version`, `human:<id>`, or `process:<id>`")
            if not normalise_okf_datetime(event.get("at")):
                error(page.path, 1, "E7", "verified.at must be an ISO 8601 datetime with an explicit UTC offset")


def normalise_okf_datetime(value) -> str:
    """Return an OKF datetime string, including a UTC offset, or an empty string."""
    if isinstance(value, datetime):
        value = value.isoformat().replace("+00:00", "Z")
    value = str(value or "")
    return value if OKF_DATETIME_RE.fullmatch(value) else ""


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
def source_resources(page: Page) -> list[str]:
    """The `resource` of every `sources:` entry, in OKF v0.2's shape.

    v0.2 defines `sources` as a list of objects, each with a required `resource`. A bare string
    is rejected rather than tolerated: this wiki is the only producer of its own frontmatter, and
    a consumer reading `.resource` off a string silently gets nothing, which is a worse failure
    than a loud one.
    """
    listed = page.get("sources") or []
    if isinstance(listed, (str, dict)):
        listed = [listed]
    out = []
    for entry in listed:
        if isinstance(entry, dict):
            resource = str(entry.get("resource") or "").strip()
            if not resource:
                error(page.path, 1, "E4", "sources: an entry has no `resource:` — OKF v0.2 requires one per entry")
                continue
            out.append(resource)
        else:
            error(page.path, 1, "E4",
                  f"sources: '{entry}' is a bare string — OKF v0.2 wants `- resource: {entry}`")
    return out


def check_sources_field(all_pages: list[Page]) -> None:
    for page in all_pages:
        for entry in source_resources(page):
            target = (WIKI / entry).resolve()
            if not target.exists():
                error(page.path, 1, "E4", f"sources: '{entry}' does not exist (paths are relative to content/)")
            elif target.parent.name != TYPES["source"]:
                error(page.path, 1, "E4", f"sources: '{entry}' is not a source page")


# --------------------------------------------------------------------------- E5
def check_raw_pairing(all_pages: list[Page]) -> None:
    """Every source page has its raw file, and every raw file has been written up.

    Source pages with `origin: owner` are exempt: they record what the owner said in a `/note`,
    which never had a document behind it. That exemption is the whole reason the field exists —
    an owner statement is anchored and citable without a fabricated file in content/raw/.
    """
    source_pages = [p for p in all_pages if p.get("type") == "source"]

    referenced = set()
    for page in source_pages:
        if page.get("origin") == "owner":
            continue
        raw_links = [t for _, t in page.links() if "/raw/" in t or t.startswith("raw/")]
        if not raw_links:
            error(page.path, 1, "E5", "source page does not link to its file in content/raw/ (or set `origin: owner` if it never had one)")
        for target in raw_links:
            referenced.add(page.resolve(target).resolve())

    for item in sorted(RAW.iterdir()):
        if not item.is_file() or item.name in (".gitkeep", "_index.md"):
            continue
        if item.resolve() not in referenced:
            error(item, 1, "E5", "file in content/raw/ has no source page — it was filed but never written up")


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
    check_okf_conformance()
    check_okf_metadata(all_pages)
    check_okf_families(all_pages)
    check_raw_pairing(all_pages)
    check_tags(all_pages)
    check_inbox()
    check_schema()

    stubs = sum(1 for p in all_pages if p.get("status") == "draft")
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
