# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate exact historical member citations and current reader command paths."""

import csv
from pathlib import PurePosixPath
import re
import sys
from urllib.parse import unquote

from sources import ROOT, historic_member

sys.path.insert(0, str(ROOT / "research/evidence-data/documentation-synthesis-d5by"))
from verify import anchors, git_paths

LOCATOR = re.compile(r"`(audits|implementation-briefs)\.zip :: (docs/[^#`]+)(?:#([^`]+))?`", re.IGNORECASE)
COMMAND = re.compile(r"(?:^|\s)((?:docs|research|save-analysis)/[A-Za-z0-9_./-]+\.(?:py|json|csv|zip))(?=\s|$)")
ARCHIVE_NAMES = ("audits", "implementation-briefs")


def member_citations(text, inventories, load=historic_member):
    errors = []
    for archive, name, fragment in LOCATOR.findall(text):
        if archive not in inventories or name not in inventories[archive]:
            errors.append(f"missing or incorrectly cased archive member {archive}.zip :: {name}")
        elif fragment and unquote(fragment) not in anchors(load(name).decode("utf-8")):
            errors.append(f"missing archive fragment {name}#{fragment}")
    return errors


def selected_paths():
    changed = set(git_paths("diff", "--diff-filter=ACMRT", "--name-only", "HEAD"))
    changed.update(git_paths("ls-files", "--others", "--exclude-standard"))
    for name in ("guides", "reference", "history"):
        changed.update(PurePosixPath(path.relative_to(ROOT).as_posix())
                       for path in (ROOT / "docs" / name).rglob("*.md"))
    return sorted(path for path in changed if path.suffix == ".md" and (ROOT / path).is_file()
                  and not (path.as_posix().startswith("docs/implementation-briefs/") and path.name != "README.md")
                  and not path.as_posix().startswith("docs/audits/archival-d5bz/"))


def command_paths(text):
    errors = []
    for line in text.splitlines():
        if not line.lstrip().startswith(("python ", "python.exe ", "py ")):
            continue
        for name in COMMAND.findall(line):
            path = ROOT / name
            if not path.is_file() or name.startswith(("docs/audits/", "docs/implementation-briefs/")) and (
                path.name not in {"archive-index.csv", "audits.zip", "implementation-briefs.zip"}
            ):
                errors.append(f"stale reader command path {name}")
    return errors


def main():
    members = {}
    for archive in ARCHIVE_NAMES:
        with (ROOT / "docs" / archive / "archive-index.csv").open(encoding="utf-8", newline="") as file:
            members[archive] = {row["member_path"] for row in csv.DictReader(file)}
    paths = selected_paths()
    errors = []
    command_surface = {
        "docs/PUBLICATION_RUN_CARD.md", "docs/reference/evidence-access.md",
        "docs/reference/b3-methods.md", "research/evidence-data/README.md",
        "docs/audits/README.md", "docs/implementation-briefs/README.md",
    }
    for path in paths:
        text = (ROOT / path).read_text(encoding="utf-8")
        issues = member_citations(text, members)
        if path.as_posix() in command_surface:
            issues += command_paths(text)
        errors.extend(f"{path}: {error}" for error in issues)
    for error in errors:
        print(error)
    print(f"{len(paths)} pages checked for archive citations and {len(command_surface)} current command surfaces. "
          f"{len(errors)} problems.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
