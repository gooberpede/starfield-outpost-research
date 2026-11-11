# SPDX-License-Identifier: GPL-3.0-or-later
"""Resolve current evidence operands and explicitly identified historical source pins."""

from functools import cache
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research/evidence-data"
RELOCATIONS = json.loads((ROOT / "research/archival/relocations.json").read_bytes())
EDITION = DATA / "current-edition.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def exact_file(root, name):
    if "\\" in name or name.startswith("/") or ":" in name:
        return None
    path = root
    for piece in name.split("/"):
        if piece in {"", ".", ".."} or not path.is_dir():
            return None
        exact = next((child for child in path.iterdir() if child.name == piece), None)
        if exact is None or exact.is_symlink() or exact.is_junction():
            return None
        path = exact
    return path if path.is_file() else None


def read_current(name):
    path = exact_file(ROOT, name)
    if path is None:
        raise ValueError(f"missing, unsafe or incorrectly cased current source: {name}")
    return path.read_bytes()


@cache
def edition():
    manifest = json.loads(EDITION.read_bytes())
    if manifest["edition"] != "D5BZ-1" or manifest["publication"] != "NOT READY / NOT CLEARED":
        raise ValueError("unexpected source edition or publication status")
    for old, new in RELOCATIONS.items():
        if manifest["sources"][new]["prior_path"] != old:
            raise ValueError(f"unjoined relocation: {old}")
    for path, record in manifest["sources"].items():
        data = read_current(path)
        if len(data) != record["bytes"] or sha(data) != record["sha256"]:
            raise ValueError(f"current source SHA-256 differs: {path}")
    return manifest


@cache
def historic_member(name):
    folder = name.split("/")[1]
    basename = {"audits": "audits.zip", "implementation-briefs": "implementation-briefs.zip"}[folder]
    with zipfile.ZipFile(ROOT / "docs" / folder / basename) as archive:
        return archive.read(name)


def source_exists(name):
    if name in RELOCATIONS:
        return exact_file(ROOT, RELOCATIONS[name]) is not None
    if name.startswith(("docs/audits/", "docs/implementation-briefs/")):
        try:
            historic_member(name)
        except KeyError:
            return False
        return True
    return exact_file(ROOT, name) is not None


@cache
def historical_pin_bytes(name):
    """Resolve a historical identity while checking its declared current counterpart."""
    manifest = edition()
    current = RELOCATIONS.get(name, name)
    record = manifest["sources"].get(current)
    if name in RELOCATIONS and record["prior_sha256"] == record["sha256"]:
        return read_current(current)
    if name.startswith(("docs/audits/", "docs/implementation-briefs/")):
        return historic_member(name)
    if record and record["prior_sha256"] != record["sha256"]:
        data = subprocess.check_output(
            ["git", "show", f"{manifest['baseline_revision']}:{name}"], cwd=ROOT,
            env=dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_NO_REPLACE_OBJECTS="1",
                     GIT_OPTIONAL_LOCKS="0"),
        )
        if sha(data) != record["prior_sha256"]:
            raise ValueError(f"historical Git source SHA-256 differs: {name}")
        return data
    return read_current(name)
