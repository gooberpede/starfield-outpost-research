"""Inventory D5BY reader links and fixed tooling references.

Reads tracked names, selected Markdown, and reader source with the Python
standard library and read-only Git commands. Prints CSV to stdout.
"""

import csv
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
FIXED = (
    "README.md", "docs/README.md", "docs/research-roadmap.md",
    "docs/first-release-scope.md", "docs/DECISIONS.md",
    "docs/RESEARCH_STATE.md", "docs/PROVENANCE.md", "docs/PUBLICATION.md",
    "docs/PUBLICATION_RUN_CARD.md", "WORKFLOW.md", "AGENTS.md",
    "docs/SAVE_PROTECTION.md", "docs/RESEARCH_EXECUTION_PROTOCOL.md",
)
VERIFIER_PATH = "docs/audits/documentation-synthesis-d5by/verify.py"
RELATIVE_VERIFIER_INPUTS = (
    "publication-claims-d5bg/claims.json",
    "evidence-readiness-d5br/readiness.json",
    "evidence-closure-d5bv/routes.json",
)
LAYERS = ("guides", "reference", "history")
PREFIXES = ("docs/audits/", "docs/implementation-briefs/")
LINK = re.compile(r"\]\(([^)\s]+)\)")
LOCATOR = re.compile(r"docs/(?:audits|implementation-briefs)/[\w./-]+")
OWNERS = {
    "outpost-rc1-2026-10": ("Technical reference owner", "Relocate the scientific source and review group. Index the administrative gap reconciliation."),
    "release-assets-d5bf": ("Evidence reader owner", "Preserve machine operands. Archive the administrative narrative and use evidence access."),
    "evidence-derivative-d5bi": ("Evidence reader owner", "Preserve the machine manifest. Use evidence access for the reader route and archive administrative context."),
    "evidence-access-d5bx": ("Evidence reader owner", "Preserve the asset operand. Use evidence access for the reader route."),
    "production-guides-d5ba": ("Documentation and verifier owner", "Use the claim lookup. Defer changes to exact D5BV-pinned links until snapshot-aware replay is qualified."),
    "logistics-guides-d5bb": ("Documentation and verifier owner", "Use the claim lookup. Defer changes to exact D5BV-pinned links until snapshot-aware replay is qualified."),
}


def recommend(path, kind):
    original = path.split("#", 1)[0]
    name = PurePosixPath(original).name
    if name == "README.md" and original.count("/") == 2:
        return "Archive custodian", "Retain the directory index and add exact archive-member locators."
    if original.startswith("docs/implementation-briefs/"):
        return "Governance and archive owners", "Index the historical authority. Apply the standing rule from its stable governing page."
    group = original.split("/")[2]
    if kind == "tool path" or name.endswith((".json", ".csv", ".py")):
        return "Evidence reader owner", "Check exact path and byte consumers before relocation. Preserve an active machine operand or qualify the revised closure."
    return OWNERS.get(group, (
        "Documentation and archive owners",
        "Use scope, access or subject routes for current findings. Index this original for historical retrieval.",
    ))


def files():
    for name in (*FIXED, VERIFIER_PATH):
        yield ROOT / name
    for layer in LAYERS:
        yield from sorted((ROOT / "docs" / layer).glob("*.md"))
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8")
    for name in tracked.split("\0"):
        if name.startswith(("save-analysis/", "research/")) and name.endswith(".py"):
            yield ROOT / name


def census():
    for file in files():
        relative = file.relative_to(ROOT).as_posix()
        tool = file.suffix == ".py"
        data = file.read_text(encoding="utf-8")
        for number, line in enumerate(data.splitlines(), start=1):
            for match in LINK.finditer(line) if not tool else ():
                link = match[1]
                if "://" in link:
                    continue
                target, sep, fragment = link.partition("#")
                path = posixpath.normpath(posixpath.join(posixpath.dirname(relative), target))
                if path.startswith(PREFIXES):
                    kind = "fragment link" if sep else "link"
                    full = path + sep + fragment
                    yield relative, number, kind, full, *recommend(full, kind)
            if relative == VERIFIER_PATH:
                for operand in RELATIVE_VERIFIER_INPUTS:
                    if '"' + operand + '"' in line:
                        path = "docs/audits/" + operand
                        kind = "relative tool operand"
                        yield relative, number, kind, path, *recommend(path, kind)
            for match in LOCATOR.finditer(line):
                if any(link.start() <= match.start() < link.end() for link in LINK.finditer(line)):
                    continue
                path = match[0].rstrip("./")
                if path.count("/") < 2:
                    continue
                kind = "tool path" if tool else "text locator"
                yield relative, number, kind, path, *recommend(path, kind)


def main():
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(("path", "line", "reference_kind", "locator", "owner", "proposed_7b_handling"))
    writer.writerows(census())


if __name__ == "__main__":
    main()
