"""Exercise the CLI with only the tooling, manifests and local Git object store."""

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from editions import HISTORICAL_REVISION, TOOL, digest, git
from inventory import BASE, BUILD, MODULE, ROOT, SHA

TECHNICAL = "test-d5bs-v1"
AUDIT = "docs/audits/native-function-catalogue-d5bd"


class EditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scratch = tempfile.TemporaryDirectory(prefix="d5bs-")
        cls.addClassCleanup(scratch.cleanup)
        cls.scratch = Path(scratch.name)
        cls.git_dir = git(ROOT, "rev-parse", "--absolute-git-dir").decode().strip()

    def fixture(self, name):
        root = self.scratch / name
        tool = root / TOOL
        tool.mkdir(parents=True)
        for file in ("editions.py", "inventory.py", "verify.py"):
            shutil.copyfile(ROOT / TOOL / file, tool / file)
        shutil.copytree(ROOT / TOOL / "editions", tool / "editions")
        return root

    def cli(self, root, *args, error=None, seed="1"):
        env = dict(os.environ, GIT_DIR=self.git_dir, GIT_WORK_TREE=str(root), GIT_OPTIONAL_LOCKS="0")
        env.update(PYTHONHASHSEED=seed, PYTHONIOENCODING="utf-8")
        result = subprocess.run(
            [sys.executable, "-B", str(root / TOOL / "verify.py"), *args],
            cwd=root, env=env, encoding="utf-8", capture_output=True,
        )
        if error is None:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn(error, result.stderr)
            print(f"{root.name}: {result.stderr.splitlines()[-1]}")
        return result.stdout

    def manifest(self, root, edition=TECHNICAL):
        return root / TOOL / "editions" / f"{edition}.json"

    def hashes(self, output):
        return dict((path, sha) for line in output.splitlines() if "  docs/" in line
                    for sha, path in [line.split("  ", 1)])

    def files(self, root):
        return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}

    def test_historical_isolation_and_drift(self):
        root = self.fixture("historical")
        before = self.files(root)
        expected = json.loads(self.manifest(root, "d5bd").read_bytes())["outputs"]
        original = self.cli(root)
        self.assertEqual(self.files(root), before)
        self.assertEqual(self.hashes(original), expected)
        self.assertIn("2095 canonical entries {'A': 18, 'B': 366, 'C': 1711}", original)
        self.assertIn("325 distinct local link targets", original)
        name = "docs/audits/d5bs-disposable-control.md"
        control = root / name
        control.parent.mkdir(parents=True)
        probe = b"Prose names instruction site 0x14079be20 and SOR-FN-0062.\n"
        control.write_bytes(probe)
        changed = root / "docs/function-register.md"
        changed.write_text("A deliberately altered selected checkout file.\n", encoding="utf-8")
        after_injection = self.files(root)
        self.assertEqual(self.cli(root, seed="2"), original)
        rows = list(csv.DictReader(self.cli(root, "--drift").splitlines()))
        self.assertIn(dict(path=name, sha256=digest(probe),
                           reason="Broad-scan candidate outside the selected scan set"), rows)
        self.assertNotIn("docs/function-register.md", {row["path"] for row in rows})
        self.assertEqual(self.files(root), after_injection)
        print("Historical output hashes survive an unselected audit and altered checkout source.")

    def test_technical_two_clean_runs(self):
        results = []
        for name, seed in (("clean-a", "1"), ("clean-b", "2")):
            root = self.fixture(name)
            # Historical-path sentinels must survive technical writes.
            accepted = json.loads(self.manifest(root, "d5bd").read_bytes())["outputs"]
            for path in accepted:
                marker = root / path
                marker.parent.mkdir(parents=True, exist_ok=True)
                marker.write_bytes(path.encode())
            before = self.files(root)
            stdout = self.cli(root, "--edition", TECHNICAL, "--write", seed=seed)
            receipt = Path(stdout.splitlines()[0].removeprefix("Technical edition receipt: "))
            self.assertTrue(receipt.is_relative_to(root / ".local-work/function-catalogue" / TECHNICAL))
            self.assertEqual(self.files(root), before | {
                (receipt / path).relative_to(root).as_posix(): data
                for path, data in self.files(receipt).items()
            })
            files = self.files(receipt)
            self.assertEqual({path: digest(data) for path, data in files.items()}, self.hashes(stdout))
            self.assertEqual(set(files), set(accepted))
            changed = {path for path in files if digest(files[path]) != accepted[path]}
            self.assertEqual(changed, {f"{AUDIT}/coverage.csv", f"{AUDIT}/locators.csv"})
            results.append(files)
        self.assertEqual(results[0], results[1])

        catalogue = list(csv.DictReader(results[0]["docs/functions/catalogue.csv"].decode().splitlines()))
        keys = [(row["exe_sha256"], row["module"], row["rva"]) for row in catalogue]
        self.assertEqual(len(set(keys)), len(catalogue))
        self.assertEqual(Counter(row["level"] for row in catalogue), {"A": 18, "B": 366, "C": 1711})
        for row in catalogue:
            self.assertEqual((row["exe_sha256"], row["module"], row["build"]), (SHA, MODULE, BUILD))
            self.assertEqual(int(row["va"], 16) - BASE, int(row["rva"], 16))
        crosswalk = results[0][f"{AUDIT}/crosswalk.md"].decode()
        self.assertEqual(sum(row.startswith("| [") for row in crosswalk.splitlines()), 18)
        print("Two technical runs with different hash seeds agree. All 16 historical sentinels survived.")

    def test_bad_manifests_leave_all_files_unchanged(self):
        historical = git(ROOT, "show", f"{HISTORICAL_REVISION}:docs/functions/README.md")
        for case, error in (
            ("missing-blob", "Missing regular Git source"),
            ("missing-member", "Required source absent from manifest"),
            ("different-bytes", "Selected source digest mismatch"),
            ("wrong-edition", "Manifest edition or executable build is incompatible"),
            ("wrong-build", "Manifest edition or executable build is incompatible"),
            ("wrong-tree", "Manifest revision/tree mismatch"),
            ("malformed", "Expecting property name"),
            ("duplicate-source", "Duplicate manifest source"),
            ("output-collision", "Unsafe or colliding output path"),
            ("wrong-output-digest", "Generated output digest mismatch"),
            ("historical-namespace", "Manifest output namespace would cross the edition boundary"),
        ):
            with self.subTest(case=case):
                root = self.fixture(case)
                path = self.manifest(root)
                manifest = json.loads(path.read_bytes())
                rows = manifest["sources"]
                if case == "missing-blob":
                    rows.append(dict(path="docs/audits/no-d5bs-such-file.md", role="scan", sha256="0" * 64))
                    rows.sort(key=lambda row: row["path"])
                elif case == "missing-member":
                    rows[:] = [row for row in rows if not row["path"].endswith("/crosswalk.json")]
                elif case == "different-bytes":
                    row = next(row for row in rows if row["path"] == "docs/functions/README.md")
                    self.assertNotEqual(row["sha256"], digest(historical))
                    row["sha256"] = digest(historical)
                    local_copy = root / row["path"]
                    local_copy.parent.mkdir(parents=True)
                    local_copy.write_bytes(historical)
                elif case == "wrong-edition":
                    manifest["edition"] = "d5bd"
                elif case == "wrong-build":
                    manifest["build"]["exe_sha256"] = "0" * 64
                elif case == "wrong-tree":
                    manifest["tree"] = "0" * 40
                elif case == "duplicate-source":
                    rows.insert(0, rows[0].copy())
                elif case == "output-collision":
                    manifest["outputs"][rows[0]["path"]] = rows[0]["sha256"]
                elif case == "wrong-output-digest":
                    manifest["outputs"]["docs/functions/catalogue.csv"] = "0" * 64
                elif case == "historical-namespace":
                    manifest["namespace"] = "."
                path.write_text("{" if case == "malformed" else json.dumps(manifest), encoding="utf-8")
                before = self.files(root)
                self.cli(root, "--edition", TECHNICAL, "--write", error=error)
                self.assertEqual(self.files(root), before)
                self.assertFalse((root / ".local-work").exists())

    def test_default_write_is_rejected(self):
        root = self.fixture("historical-write")
        before = self.files(root)
        self.cli(root, "--write", error="--write requires an explicit technical edition")
        self.assertEqual(self.files(root), before)
        self.assertFalse((root / ".local-work").exists())

    def test_existing_namespace_file_is_preserved(self):
        root = self.fixture("namespace-file")
        conflict = root / ".local-work/function-catalogue" / TECHNICAL
        conflict.parent.mkdir(parents=True)
        conflict.write_bytes(b"pre-existing file")
        before = self.files(root)
        self.cli(root, "--edition", TECHNICAL, "--write", error=str(conflict.name))
        self.assertEqual(self.files(root), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
