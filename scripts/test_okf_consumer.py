#!/usr/bin/env python3
"""Acceptance checks for the wiki's minimal OKF reader behavior."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from wikilib import Page


class OkfConsumerAcceptanceTests(unittest.TestCase):
    def page(self, text: str) -> Page:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "concept.md"
        path.write_text(text, encoding="utf-8")
        return Page(path)

    def test_unknown_type_and_extension_are_consumable(self) -> None:
        page = self.page("""---
type: Future Concept
custom_extension: retained
---

# Future concept
""")
        self.assertIsNone(page.error)
        self.assertEqual(page.get("type"), "Future Concept")
        self.assertEqual(page.get("custom_extension"), "retained")

    def test_broken_relative_link_is_read_without_rejection(self) -> None:
        page = self.page("""---
type: Reference
---

See [later knowledge](missing.md).
""")
        self.assertIsNone(page.error)
        self.assertEqual(page.links(), [(5, "missing.md")])
        self.assertFalse(page.resolve("missing.md").exists())

    def test_optional_okf_metadata_can_be_absent(self) -> None:
        page = self.page("""---
type: Reference
---

# Minimal concept
""")
        self.assertIsNone(page.error)
        self.assertIsNone(page.get("sources"))
        self.assertIsNone(page.get("generated"))
        self.assertIsNone(page.get("verified"))
        self.assertIsNone(page.get("stale_after"))

    def test_bare_verified_mapping_reads_as_a_one_element_list(self) -> None:
        """OKF v0.2 §11: a consumer MUST treat a bare `verified` mapping as a one-element list."""
        bare = self.page("""---
type: Reference
verified: { by: "human:owner", at: 2026-09-12T00:00:00Z }
---

# Confirmed once, written without the list dash
""")
        listed = self.page("""---
type: Reference
verified:
  - { by: "human:owner", at: 2026-09-12T00:00:00Z }
---

# The same confirmation, written as a list
""")
        self.assertIsNone(bare.error)
        self.assertEqual(len(bare.verified_events()), 1)
        self.assertEqual(bare.verified_events(), listed.verified_events())

    def test_absent_verified_is_no_events_rather_than_an_error(self) -> None:
        """The unverified trust tier is a valid state, not a malformed one (§5.3)."""
        page = self.page("""---
type: Reference
---

# Never confirmed by anyone
""")
        self.assertEqual(page.verified_events(), [])


if __name__ == "__main__":
    unittest.main()
