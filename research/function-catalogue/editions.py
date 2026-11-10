"""Resolve explicit edition inputs from local Git blobs and isolate test writes."""

import hashlib
import io
import json
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory, mkdtemp

from inventory import BASE, BUILD, MODULE, SHA, scan_candidate

TOOL = "research/function-catalogue"
HISTORICAL = "d5bd"
HISTORICAL_REVISION = "6e799a428a765aa196a24d3c1de8ae133260aa08"
HISTORICAL_TREE = "7a1f6fdd6728a8f98bc92ef7ee6c9b24a62f0e0e"
TEST_ROOT = ".local-work/function-catalogue"
EDITION_ID = re.compile(r"test-[a-z0-9]+(?:-[a-z0-9]+)*-v[1-9][0-9]*")
BUILD_ID = dict(module=MODULE, version=BUILD, exe_sha256=SHA, preferred_base=f"0x{BASE:x}")
HEX40 = re.compile(r"[0-9a-f]{40}")
HEX64 = re.compile(r"[0-9a-f]{64}")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def matches(pattern, value):
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate manifest key: {key}")
        result[key] = value
    return result


def safe_path(value):
    return isinstance(value, str) and all(
        re.fullmatch(r"[A-Za-z0-9_.-]+", part) and not part.startswith(".") and not part.endswith(".")
        and not re.fullmatch(r"(?:CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(?:\..*)?", part, re.I)
        for part in value.split("/")
    )


def support_path(path):
    if path in {"README.md", "CREDITS.md"}:
        return True
    return (
        path.startswith(("docs/", TOOL + "/"))
        and not path.startswith(("docs/experiments/evidence/", "docs/experiments/templates/"))
        and "third_party" not in path.casefold().split("/")
        and path.endswith((".md", ".csv", ".json", ".py"))
    )


def namespace(edition):
    return "." if edition == HISTORICAL else f"{TEST_ROOT}/{edition}"


def read_manifest(repo, edition):
    if edition != HISTORICAL and not matches(EDITION_ID, edition):
        raise ValueError(f"Unsupported edition identifier: {edition!r}")
    path = local_path(repo, f"{TOOL}/editions/{edition}.json")
    manifest = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    fields = {"schema", "edition", "build", "revision", "tree", "namespace", "sources", "outputs"}
    if not isinstance(manifest, dict) or manifest.keys() != fields or type(manifest["schema"]) is not int or manifest["schema"] != 1:
        raise ValueError("Malformed or unsupported manifest schema")
    if manifest["edition"] != edition or manifest["build"] != BUILD_ID:
        raise ValueError("Manifest edition or executable build is incompatible")
    if manifest["namespace"] != namespace(edition):
        raise ValueError("Manifest output namespace would cross the edition boundary")
    revision, tree = manifest["revision"], manifest["tree"]
    if not matches(HEX40, revision) or not matches(HEX40, tree):
        raise ValueError("Manifest must pin a full Git commit and tree")
    if edition == HISTORICAL and (revision, tree) != (HISTORICAL_REVISION, HISTORICAL_TREE):
        raise ValueError("Historical manifest must pin the accepted D5BD commit and tree")

    seen = set()
    paths = []
    if not isinstance(manifest["sources"], list) or not manifest["sources"]:
        raise ValueError("Manifest sources must be a nonempty ordered list")
    for source in manifest["sources"]:
        if not isinstance(source, dict) or source.keys() != {"path", "role", "sha256"}:
            raise ValueError("Malformed source entry")
        name, role = source["path"], source["role"]
        if not safe_path(name) or not matches(HEX64, source["sha256"]):
            raise ValueError(f"Malformed source path or digest: {name!r}")
        if name.casefold() in seen:
            raise ValueError(f"Duplicate manifest source: {name}")
        if not ((role == "scan" and scan_candidate(name)) or (role == "support" and support_path(name))):
            raise ValueError(f"Ineligible source or role: {name}")
        seen.add(name.casefold())
        paths.append(name)
    if paths != sorted(paths):
        raise ValueError("Manifest sources must be sorted by path")

    outputs = manifest["outputs"]
    if not isinstance(outputs, dict) or not outputs:
        raise ValueError("Manifest outputs must be a nonempty digest map")
    for name, sha in outputs.items():
        if not safe_path(name) or name.casefold() in seen or not matches(HEX64, sha):
            raise ValueError(f"Unsafe or colliding output path or digest: {name}")
        seen.add(name.casefold())
    return manifest


def git(repo, *args, request=None):
    result = subprocess.run(
        ["git", "--no-replace-objects", "--no-lazy-fetch", "-C", str(repo), *args],
        input=request, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise RuntimeError(f"Local Git {args[0]} failed: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


def git_paths(repo, revision):
    paths = {}
    for row in git(repo, "ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
        if row:
            metadata, path = row.split(b"\t", 1)
            mode, kind, oid = metadata.split()
            if kind == b"blob" and mode in {b"100644", b"100755"}:
                paths[path.decode("utf-8")] = oid
    return paths


def git_blobs(repo, paths, selected):
    selected = list(selected)
    for path in selected:
        if path not in paths:
            raise ValueError(f"Missing regular Git source: {path}")
    request = b"".join(paths[path] + b"\n" for path in selected)
    response = io.BytesIO(git(repo, "cat-file", "--batch", request=request))
    result = {}
    for path in selected:
        header = response.readline().split()
        if len(header) != 3 or header[:2] != [paths[path], b"blob"]:
            raise ValueError(f"Missing or invalid Git blob: {path} ({paths[path].decode()})")
        size = int(header[2])
        data = response.read(size)
        if len(data) != size or response.read(1) != b"\n":
            raise ValueError(f"Truncated Git blob: {path}")
        result[path] = data
    if response.read(1):
        raise ValueError("Unexpected Git blob data")
    return result


def historical_outputs(repo, selected):
    return git_blobs(repo, git_paths(repo, HISTORICAL_REVISION), selected)


class SourceSet:
    def __init__(self, repo, manifest):
        revision = manifest["revision"]
        object_type = git(repo, "cat-file", "-t", revision).strip()
        tree = git(repo, "rev-parse", "--verify", f"{revision}^{{tree}}").decode().strip()
        if object_type != b"commit" or tree != manifest["tree"]:
            raise ValueError(f"Manifest revision/tree mismatch: {revision}")
        paths = git_paths(repo, revision)
        inputs = manifest["sources"]
        data = git_blobs(repo, paths, (row["path"] for row in inputs))
        for row in inputs:
            path = row["path"]
            if digest(data[path]) != row["sha256"]:
                raise ValueError(f"Selected source digest mismatch: {path}")
        self.scan_paths = tuple(row["path"] for row in inputs if row["role"] == "scan")
        self._text = {path: content.decode("utf-8-sig") for path, content in data.items()}
        self._used = set()

    def text(self, path):
        if path not in self._text:
            raise ValueError(f"Required source absent from manifest: {path}")
        self._used.add(path)
        return self._text[path]

    def sidecar(self, name):
        return json.loads(self.text(f"{TOOL}/{name}"))

    def sidecar_csv(self, name):
        return io.StringIO(self.text(f"{TOOL}/{name}"), newline="")

    def check_used(self):
        unused = self._text.keys() - self._used
        if unused:
            raise ValueError(f"Unexpected unused manifest sources: {sorted(unused)}")


def local_path(repo, path):
    """Reject links, junctions and other reparse points along a local path."""
    current = repo
    for part in PurePosixPath(path).parts:
        current /= part
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Unsafe linked local path: {current}")
    return current


def drift(repo, manifest):
    selected = {row["path"] for row in manifest["sources"] if row["role"] == "scan"}
    listed = git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    candidates = {path.decode("utf-8") for path in listed.split(b"\0") if path}
    for path in sorted(candidates - selected):
        if not scan_candidate(path):
            continue
        source = local_path(repo, path)
        if source.is_file():
            yield dict(path=path, sha256=digest(source.read_bytes()),
                       reason="Broad-scan candidate outside the selected scan set")


def write_receipt(repo, manifest, data):
    edition = manifest["edition"]
    if not matches(EDITION_ID, edition) or manifest["namespace"] != namespace(edition):
        raise ValueError("Only a separate technical edition can write outputs")
    root = local_path(repo, namespace(edition))
    root.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=root, prefix="pending-") as temporary:
        stage = Path(temporary) / "files"
        for name, content in data.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        # Allocate an exclusive parent before exposing the complete output tree.
        receipt = Path(mkdtemp(dir=root, prefix="run-"))
        try:
            stage.rename(receipt / "files")
        except OSError:
            receipt.rmdir()
            raise
    return receipt / "files"
