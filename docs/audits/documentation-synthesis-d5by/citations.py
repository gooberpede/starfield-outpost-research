"""Inventory research identifiers in the bounded D5BY reader corpus.

Uses the standard library, reads authored Markdown and prints CSV. The
generated table flags unclassified terms for editorial review.
"""

from collections import defaultdict
import csv
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs"
PATTERN = re.compile(
    r"(?<![\w-])(?:D5[A-Z]{1,3}|B4-C\d{2}|B4-F\d{3}|"
    r"GC-\d+(?:–\d+)?|HIST-\d{4}|SOR-(?:FN|ST|EV|EXP|F)-\d{4}|"
    r"C19|RC1|BM[12]|LO1|CR[123]|SD[123]|QS1|[A-Z][0-9])\b"
)
LOCAL = {
    "A0": "Resource episode baseline",
    "A1": "Resource return episode or another report's local checkpoint",
    "B0": "Independent initial construction or historical release policy stage",
    "B1": "Biome investigation or historical release preparation stage",
    "B2": "Context-sensitive observed construction attempt or earlier publication pass",
    "B3": "Historical publication method and baseline pass",
    "B4": "Historical publication evidence selection",
    "B5": "Historical creator and retention preparation",
    "B6": "Independent release candidate preflight",
    "F1": "Original-save asset selection family",
    "N2": "Resource generation target episode",
    "Q1": "Question ordinal scoped to the named brief",
    "Q2": "Question ordinal scoped to the named brief",
    "Q3": "Question ordinal scoped to the named brief",
    "Q4": "Question ordinal scoped to the named brief",
    "QS1": "D5U ordinary query surface in the fixed-input U26 control",
}
ADMIN = {
    "D5AW", "D5AX", "D5AY", "D5AZ", "D5BA", "D5BB", "D5BC", "D5BE",
    "D5BF", "D5BG", "D5BH", "D5BI", "D5BJ", "D5BO", "D5BP", "D5BQ",
    "D5BR", "D5BS", "D5BT", "D5BU", "D5BV", "D5BW", "D5BX",
}


def rows():
    pages = [
        DOCS / "README.md", DOCS / "research-roadmap.md", DOCS / "first-release-scope.md",
        DOCS / "history/claims.md", DOCS / "history/evidence-routes.md",
    ]
    for layer in ("guides", "reference"):
        pages.extend(sorted((DOCS / layer).glob("*.md")))
    hits = defaultdict(list)
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for token in sorted(set(PATTERN.findall(text))):
            hits[token].append(page.relative_to(ROOT).as_posix())
    indexes = (
        "history/research-identifiers.md", "history/save-identifiers.md",
        "history/claims.md",
    )
    lookups = {p: (DOCS / p).read_text(encoding="utf-8") for p in indexes}
    for token, paths in sorted(hits.items()):
        matched = [p for p, text in lookups.items()
                   if re.search(r"(?<![\w-])" + re.escape(token) + r"(?![\w-])", text)]
        if token in LOCAL:
            result = "Context-specific", LOCAL[token]
        elif token in ADMIN:
            result = "Administrative history", "docs/history/research-identifiers.md and the audit index"
        elif any(not p.endswith("claims.md") for p in matched) or token.startswith("B4-C") and matched:
            result = "Indexed", ", ".join(f"docs/{p}" for p in matched)
        elif token.startswith(("SOR-FN-", "SOR-ST-", "SOR-EXP-", "SOR-EV-")):
            result = "Stable record", "Function, state or experiment register in the cited source context"
        elif token in {"H3", "H4"}:
            result = "Context-specific", "Local report hypothesis ordinal"
        else:
            result = "CHECK", "Resolve or explicitly classify the term"
        yield token, len(paths), *result, ", ".join(paths)


def main():
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(("source_id", "pages", "classification", "lookup_or_scope", "path"))
    unclassified = 0
    for row in rows():
        writer.writerow(row)
        unclassified += row[2] == "CHECK"
    return int(bool(unclassified))


if __name__ == "__main__":
    raise SystemExit(main())
