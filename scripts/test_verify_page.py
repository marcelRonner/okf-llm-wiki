#!/usr/bin/env python3
"""Checks for scripts/verify_page.py — the command the owner uses to record a verification."""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from lint_wiki import OKF_ACTOR_RE
from verify_page import add_verification
from wikilib import Page, okf_datetime

AT = datetime(2026, 9, 12, 14, 30, tzinfo=timezone.utc)
PAGE = """---
title: A page
type: topic
updated: 2026-09-01
{verified}tags: [meta]
---

# A page

Body text, which must come through untouched.
"""


class VerifyPageTests(unittest.TestCase):
    def read(self, text: str) -> Page:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "page.md"
        path.write_text(text, encoding="utf-8")
        return Page(path)

    def test_first_verification_is_a_valid_okf_event(self) -> None:
        page = self.read(add_verification(PAGE.format(verified=""), "owner", AT))
        self.assertIsNone(page.error)
        [event] = page.verified_events()
        self.assertEqual(event["by"], "human:owner")
        self.assertTrue(OKF_ACTOR_RE.fullmatch(event["by"]))
        self.assertEqual(okf_datetime(event["at"]), AT)

    def test_appends_rather_than_replaces(self) -> None:
        earlier = "verified:\n  - by: process:nightly\n    at: 2026-09-01T02:00:00Z\n"
        page = self.read(add_verification(PAGE.format(verified=earlier), "owner", AT))
        self.assertEqual([e["by"] for e in page.verified_events()], ["process:nightly", "human:owner"])

    def test_a_bare_mapping_becomes_a_list_and_survives(self) -> None:
        bare = 'verified: { by: "human:owner", at: 2026-09-01T09:00:00Z }\n'
        page = self.read(add_verification(PAGE.format(verified=bare), "owner", AT))
        self.assertEqual(len(page.verified_events()), 2)

    def test_everything_else_is_untouched(self) -> None:
        original = PAGE.format(verified="")
        page = self.read(add_verification(original, "owner", AT))
        self.assertEqual(page.body, original.split("---\n", 2)[2])
        self.assertEqual(str(page.get("updated")), "2026-09-01")
        self.assertEqual(page.get("tags"), ["meta"])

    def test_refuses_a_malformed_existing_value(self) -> None:
        with self.assertRaises(ValueError):
            add_verification(PAGE.format(verified="verified: yes\n"), "owner", AT)


if __name__ == "__main__":
    unittest.main()
