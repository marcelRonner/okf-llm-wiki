#!/usr/bin/env python3
"""Shared helpers for the wiki scripts: paths, frontmatter parsing, link extraction."""

from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML is required — run: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
INBOX = ROOT / "inbox"
RAW = ROOT / "raw"

INDEX = WIKI / "index.md"
LOG = WIKI / "log.md"

# type -> folder. The single place this mapping is defined.
TYPES = {
    "project": "projects",
    "system": "systems",
    "decision": "decisions",
    "person": "people",
    "org": "orgs",
    "topic": "topics",
    "source": "sources",
}

TYPE_LABELS = {
    "project": "Projects",
    "system": "Systems",
    "decision": "Decisions",
    "person": "People",
    "org": "Organisations",
    "topic": "Topics",
    "source": "Sources",
}

REQUIRED_KEYS = ("title", "type", "summary", "created", "updated")

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


class Page:
    """A wiki page with parsed frontmatter."""

    def __init__(self, path: Path):
        self.path = path
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
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
            self.meta, self.body, self.error = {}, text, "missing frontmatter"

    @property
    def rel(self) -> str:
        return str(self.path.relative_to(ROOT))

    @property
    def wiki_rel(self) -> str:
        """Path relative to the wiki root — how MkDocs and Obsidian refer to it."""
        return str(self.path.relative_to(WIKI))

    def get(self, key, default=None):
        return self.meta.get(key, default)

    def links(self) -> list[tuple[int, str]]:
        """Real (non-template, non-external) link targets with line numbers."""
        clean = FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), self.body)
        offset = len(self.path.read_text(encoding="utf-8").splitlines()) - len(clean.splitlines())
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


def pages(include_special: bool = False) -> list[Page]:
    """All wiki pages, sorted. index.md and log.md are excluded unless asked for."""
    special = {INDEX.resolve(), LOG.resolve()}
    found = []
    for path in sorted(WIKI.rglob("*.md")):
        if not include_special and path.resolve() in special:
            continue
        found.append(Page(path))
    return found


def inbox_items() -> list[Path]:
    return sorted(p for p in INBOX.iterdir() if p.is_file() and p.name != ".gitkeep")
