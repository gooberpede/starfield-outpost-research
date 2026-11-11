# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise archive and current-operand refusal paths on invented data."""

import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

import archive
import sources
from verify_navigation import command_paths, member_citations


class Refusals(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = "docs/audits/test/sample.md"
        self.rows = [archive.metadata("audits", {"path": self.path}, b"# Sample\n", {})]

    def write(self, members, rows=None):
        with (self.root / "archive-index.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, archive.FIELDS)
            writer.writeheader()
            writer.writerows(self.rows if rows is None else rows)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.root / "audits.zip", "w") as file:
                for name, data, mode in members:
                    entry = zipfile.ZipInfo(name, archive.TIMESTAMP)
                    entry.create_system = 0 if mode == 0x20 else 3
                    entry.external_attr = mode
                    file.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED)

    def test_safe_roundtrip(self):
        self.write([(self.path, b"# Sample\n", 0x20)])
        extracted = self.root / "extracted"
        self.assertEqual(archive.verify(self.root, "audits", extracted), 1)
        self.assertEqual((extracted / self.path).read_bytes(), b"# Sample\n")

    def test_removed_extra_duplicate_case_collision_and_path_types(self):
        valid = (self.path, b"# Sample\n", 0x20)
        for members in (
            [],
            [valid, ("docs/audits/test/z.md", b"extra", 0x20)],
            [valid, valid],
            [valid, (self.path.upper().replace("DOCS/AUDITS", "docs/audits"), b"x", 0x20)],
            [valid, ("docs/audits/Test/another.md", b"x", 0x20)],
            [("docs/audits/../sample.md", b"x", 0x20)],
            [("/docs/audits/sample.md", b"x", 0x20)],
            [("C:/docs/audits/sample.md", b"x", 0x20)],
            [("//host/docs/audits/sample.md", b"x", 0x20)],
            [("docs/audits/CON.txt", b"x", 0x20)],
            [(self.path, b"x", 0o120777 << 16)],
            [(self.path, b"x", 0o010644 << 16)],
        ):
            with self.subTest(members=members):
                self.write(members)
                with self.assertRaises(ValueError):
                    archive.verify(self.root, "audits")

    def test_modified_byte_and_index_join(self):
        for data, rows in ((b"# sample\n", None), (b"# Sample\n", []),
                           (b"# Sample\n", [dict(self.rows[0], member_path="docs/audits/wrong.md")]),
                           (b"# Sample\n", [dict(self.rows[0], edition="different-edition")])):
            with self.subTest(data=data, rows=rows):
                self.write([(self.path, data, 0x20)], rows)
                with self.assertRaises(ValueError):
                    archive.verify(self.root, "audits")

    def test_governing_brief_required(self):
        with self.assertRaisesRegex(ValueError, "governing D5BZ brief"):
            archive.checked_names(["docs/implementation-briefs/other.md"], "implementation-briefs")

    def test_stale_citation_and_current_command(self):
        inventories = {"audits": {self.path}}
        load = lambda name: b"# Current heading\n"
        key = f"audits.zip :: {self.path}"
        self.assertEqual(member_citations(f"`{key}#current-heading`", inventories, load), [])
        self.assertIn("missing archive fragment", member_citations(f"`{key}#old-heading`", inventories, load)[0])
        self.assertIn("incorrectly cased archive member",
                      member_citations(f"`{key.upper().replace('AUDITS.ZIP', 'audits.zip')}`", inventories, load)[0])
        self.assertEqual(command_paths("python -B docs/audits/test/verify.py"),
                         ["stale reader command path docs/audits/test/verify.py"])

    def test_review_status_prefers_final_explicit_disposition(self):
        text = ("# Review\n\n**Disposition:** REWORK for the first round.\n"
                + "\n" * 30 + "## Final review\n\n**Disposition:** ACCEPT for pre-seal review.\n")
        self.assertEqual(archive.historical_metadata(text, True)[1], "ACCEPT for pre-seal review.")
        scoped = "**ACCEPT for the local scope.** Independent review03 checked the result.\n"
        self.assertEqual(archive.historical_metadata(scoped, True)[1], "ACCEPT for the local scope.")

    def test_no_legacy_or_private_fallback(self):
        current = "research/evidence-data/test/asset.json"
        for alternate in ("docs/audits/test/asset.json", ".local-work/test/asset.json",
                          "research/evidence-data/test/renamed.json"):
            path = self.root / alternate
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"{}")
        with patch.object(sources, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "missing, unsafe or incorrectly cased current source"):
                sources.read_current(current)


if __name__ == "__main__":
    unittest.main()
