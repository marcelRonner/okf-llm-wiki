#!/usr/bin/env python3
"""Shared helpers for the wiki scripts: the schema, paths, frontmatter, links."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML is required — run: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "content"
INBOX = ROOT / "inbox"
RAW = WIKI / "raw"   # inside the bundle: an OKF consumer gets the evidence, not just the pages
TEMPLATES = ROOT / "templates"
SCHEMA_FILE = ROOT / "schema.yml"

INDEX = WIKI / "_index.md"
LOG = WIKI / "log.md"
TAGS = WIKI / "tags.md"

# --------------------------------------------------------------------------- the schema
# Loaded, never hardcoded. schema.yml is the one place a page type is defined; if you find
# yourself typing a type name into a script, that is the bug this module exists to prevent.


def _load_schema() -> dict:
    if not SCHEMA_FILE.exists():
        raise SystemExit(f"wikilib: {SCHEMA_FILE.relative_to(ROOT)} is missing — it defines the page types")
    data = yaml.safe_load(SCHEMA_FILE.read_text(encoding="utf-8")) or {}
    if not data.get("types"):
        raise SystemExit("wikilib: schema.yml has no `types:` — the wiki has no page types")
    for name, spec in data["types"].items():
        for key in ("folder", "label", "holds", "short"):
            if not spec.get(key):
                raise SystemExit(f"wikilib: schema.yml type '{name}' is missing `{key}:`")
    return data


SCHEMA = _load_schema()
TYPE_INFO: dict[str, dict] = SCHEMA["types"]
LIMITS: dict = SCHEMA.get("limits", {})

TYPES = {name: spec["folder"] for name, spec in TYPE_INFO.items()}
TYPE_LABELS = {name: spec["label"] for name, spec in TYPE_INFO.items()}

REQUIRED_KEYS = ("title", "type", "description", "created", "updated")

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)

# Blocks written by the scripts. Their contents are regenerated wholesale, so they are stripped
# before links are counted — otherwise generated backlinks would make every page look connected
# and the orphan check would silently pass on everything.
GENERATED_RE = re.compile(
    r"<!--\s*(\w+):start[^>]*-->.*?<!--\s*\1:end\s*-->", re.DOTALL | re.IGNORECASE
)


def blank_out(text: str, pattern: re.Pattern) -> str:
    """Replace matches with the same number of newlines, so line numbers stay correct."""
    return pattern.sub(lambda m: "\n" * m.group(0).count("\n"), text)


class Page:
    """A wiki page with parsed frontmatter."""

    def __init__(self, path: Path):
        self.path = path
        self.text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(self.text)
        if match:
            try:
                self.meta = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError as exc:
                self.meta, self.error = {}, f"invalid YAML frontmatter: {exc}"
            else:
                self.error = None if isinstance(self.meta, dict) else "frontmatter is not a mapping"
                if not isinstance(self.meta, dict):
                    self.meta = {}
            self.body = match.group(2)
        else:
            self.meta, self.body, self.error = {}, self.text, "missing frontmatter"

    @property
    def rel(self) -> str:
        return str(self.path.relative_to(ROOT))

    @property
    def wiki_rel(self) -> str:
        """Path relative to the wiki root — how Hugo and Obsidian refer to it."""
        return str(self.path.relative_to(WIKI))

    def get(self, key, default=None):
        return self.meta.get(key, default)

    def links(self, include_generated: bool = False) -> list[tuple[int, str]]:
        """Real (non-template, non-external) link targets with line numbers.

        Generated blocks are excluded by default: they are bookkeeping, not editorial links.
        """
        clean = blank_out(self.body, FENCE_RE)
        if not include_generated:
            clean = blank_out(clean, GENERATED_RE)
        offset = len(self.text.splitlines()) - len(clean.splitlines())
        out = []
        for lineno, line in enumerate(clean.splitlines(), 1):
            for target in LINK_RE.findall(line):
                target = target.split()[0].strip()
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if "{" in target or target.startswith("YYYY"):
                    continue  # convention template, not a real link
                out.append((lineno + offset, target))
        return out

    def resolve(self, target: str) -> Path:
        return (self.path.parent / target.split("#")[0]).resolve()

    def tags(self) -> list[str]:
        raw = self.get("tags") or []
        if isinstance(raw, str):
            raw = [raw]
        return [str(t).strip() for t in raw if str(t).strip()]

    def word_count(self) -> int:
        """Prose words only — frontmatter, code fences and generated blocks do not count."""
        body = blank_out(blank_out(self.body, FENCE_RE), GENERATED_RE)
        return len(re.findall(r"\b[\w'-]+\b", body))

    def verified_events(self):
        """`verified:` read as a list of events, in whichever shape it was written.

        OKF v0.2 makes this a consumer MUST (§5.2, §11): a single verifier may be written as a
        bare `{ by, at }` mapping with no list dash, and a consumer has to read it as a
        one-element list. Reading `self.get("verified")` and iterating it is how that requirement
        gets broken by accident — a bare mapping iterates as its own keys — so nothing in this
        repository does. The reader and the linter share this one function.

        A value that is neither a mapping nor a list comes back unchanged rather than being
        wrapped, so a validator can report the malformed shape instead of this function hiding it.
        """
        verified = self.get("verified")
        if verified is None:
            return []
        return [verified] if isinstance(verified, dict) else verified

    def is_generated(self) -> bool:
        return self.get("type") in ("index", "log", "tags")


def pages(include_special: bool = False) -> list[Page]:
    """All wiki pages, sorted. The generated catalogues and the log are excluded by default.

    So is every `_index.md`. Those are Hugo section pages — the titles and ordering behind the
    site's sidebar, stamped from schema.yml by `make schema`. They are furniture, not content:
    they carry no claim, cite no source, and should not appear in the catalogue or collect
    backlinks. The root `_index.md` is the generated catalogue itself, and is covered by the
    same rule.

    `content/raw/` is excluded unconditionally, `include_special` or not. It sits inside the
    bundle so that an OKF consumer receives the evidence along with the pages, but it is raw
    material, not wiki pages: it must never be given a required-key check, a word-count warning,
    a catalogue entry, a `generated:` stamp or a backlink block, because every one of those would
    write into a file whose body is supposed to be exactly what arrived. OKF's own two
    requirements — parseable frontmatter and a non-empty `type` — are checked separately, by the
    conformance walk that reads every file in the tree.
    """
    special = {LOG.resolve(), TAGS.resolve()}
    raw = RAW.resolve()
    found = []
    for path in sorted(WIKI.rglob("*.md")):
        if raw in path.resolve().parents:
            continue
        if not include_special and (path.name == "_index.md" or path.resolve() in special):
            continue
        found.append(Page(path))
    return found


def inbound_links(all_pages: list[Page]) -> dict[Path, list[Page]]:
    """Which pages link to each page, ignoring generated blocks and the generated catalogues."""
    incoming: dict[Path, list[Page]] = {p.path.resolve(): [] for p in all_pages}
    for page in all_pages:
        for _, target in page.links():
            resolved = page.resolve(target)
            if resolved.suffix == ".md" and resolved in incoming and resolved != page.path.resolve():
                incoming[resolved].append(page)
    return incoming


def as_date(value):
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def replace_block(text: str, name: str, body: str) -> str:
    """Swap the contents of a <!-- name:start --> … <!-- name:end --> block."""
    pattern = re.compile(
        rf"(<!--\s*{name}:start[^>]*-->\n).*?(\n<!--\s*{name}:end\s*-->)", re.DOTALL
    )
    if not pattern.search(text):
        raise SystemExit(f"wikilib: no <!-- {name}:start --> … <!-- {name}:end --> block to fill")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), text)


def inbox_items() -> list[Path]:
    return sorted(p for p in INBOX.iterdir() if p.is_file() and p.name != ".gitkeep")
