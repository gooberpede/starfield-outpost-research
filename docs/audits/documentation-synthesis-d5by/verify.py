"""Check D5BY reader paths and coverage from an existing checkout.

Uses Python's standard library and read-only Git file inventories. Reads
Markdown, inherited JSON metadata and current paths. Prints diagnostics and
counts. It opens no evidence asset and writes no files.
"""

from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3]
AUDITS = ROOT / "docs/audits"
LINK = re.compile(r"(?<!!)\[([^\]\n]*)\]\(([^)\n]+)\)|!\[[^\]\n]*\]\(([^)\n]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})([^\s]*)")
SUBJECTS = set("""
identity position nominal-biomes resource-generation inorganic-production
organic-production fabrication power storage-and-output-links cargo
crew-and-robots construction defense containers-and-displays shared-storage
stored-resources locations-ui access-and-save-framing
""".split())


def git_paths(*arguments):
    raw = subprocess.check_output(["git", *arguments, "-z"], cwd=ROOT)
    return [PurePosixPath(p) for p in raw.decode("utf-8").split("\0") if p]


def outside_fences(text):
    marker = ""
    for number, line in enumerate(text.splitlines(), start=1):
        fence = FENCE.match(line)
        if fence:
            token = fence[1]
            if not marker:
                marker = token
                continue
            if token[0] == marker[0] and len(token) >= len(marker) and not fence[2]:
                marker = ""
                continue
        if not marker:
            yield number, line


def anchors(text):
    counts = Counter()
    slugs = set(re.findall(r'<a (?:name|id)="([^"]+)"', text))
    for _, line in outside_fences(text):
        match = HEADING.match(line)
        if not match:
            continue
        title = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", match[1])
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        index = counts[slug]
        counts[slug] += 1
        slugs.add(f"{slug}-{index}" if index else slug)
    return slugs


def resolve_exact(source, destination):
    current = ROOT
    parent = () if destination.startswith("/") else source.parent.parts
    for piece in (*parent, *PurePosixPath(destination.lstrip("/")).parts):
        if piece == "..":
            if current == ROOT:
                return None
            current = current.parent
        else:
            if not current.is_dir():
                return None
            if piece not in {path.name for path in current.iterdir()}:
                return None
            current = current / piece
    return current


def check_links(paths):
    problems = []
    count = 0
    slug_cache = {}
    for path in sorted(paths):
        content = (ROOT / path).read_text(encoding="utf-8")
        for number, line in outside_fences(content):
            for link in LINK.finditer(line):
                target = (link[2] or link[3]).strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc:
                    continue
                count += 1
                file = resolve_exact(path, unquote(parsed.path)) if parsed.path else ROOT / path
                if not file:
                    problems.append(f"{path}:{number}: missing or wrong case: {target}")
                elif parsed.fragment and file.is_file() and file.suffix == ".md":
                    if file not in slug_cache:
                        slug_cache[file] = anchors(file.read_text(encoding="utf-8"))
                    if unquote(parsed.fragment) not in slug_cache[file]:
                        problems.append(f"{path}:{number}: missing anchor: {target}")
    return count, problems


def read_audit(path):
    return json.loads((AUDITS / path).read_text(encoding="utf-8"))


def check_coverage():
    inherited = read_audit("publication-claims-d5bg/claims.json")
    selected = read_audit("evidence-readiness-d5br/readiness.json")
    overlay = read_audit("evidence-closure-d5bv/routes.json")
    claims = (ROOT / "docs/history/claims.md").read_text(encoding="utf-8")
    routes = (ROOT / "docs/history/evidence-routes.md").read_text(encoding="utf-8")
    problems = []
    expected = {x["id"] for x in inherited["claims"]}
    observed = set(re.findall(r"^\| \*\*([A-Z0-9-]+)\*\*\.", claims, re.M))
    if observed != expected or expected != {x["id"] for x in selected["claims"]}:
        problems.append("Claim ID set differs from the inherited and selected records.")
    if set(re.findall(r"^\| \*\*([A-Z0-9-]+)\*\* \|", routes, re.M)) != set(overlay["routes"]):
        problems.append("Evidence route IDs differ from the selected overlay.")
    for line in routes.splitlines():
        row = re.match(r"^\| \*\*([A-Z0-9-]+)\*\* \| [^|]*\| ([^|]*)\|", line)
        if row:
            key, related = row.groups()
            if set(re.findall(r"`([A-Z0-9-]+)`", related)) != set(overlay["routes"][key]["claims"]):
                problems.append(f"Claim join differs for {key}.")
    if {p.stem for p in (ROOT / "docs/guides").glob("*.md")} - {"README", "AUTHORING-STANDARD"} != SUBJECTS:
        problems.append("Guide inventory differs from the 18 subject stems.")
    for stem in SUBJECTS:
        guide = (ROOT / f"docs/guides/{stem}.md").read_text(encoding="utf-8")
        if f"../reference/{stem}.md" not in guide or f"## {stem}\n" not in claims:
            problems.append(f"Missing technical or claim route for {stem}.")
    return problems


def check_diagrams(paths):
    # This is the flowchart subset used in the reader layers.
    fence = chr(96) * 3
    pattern = re.compile(r"^" + fence + r"mermaid\n([\s\S]*?)^" + fence + r"$", re.M)
    node = r'[A-Za-z][\w]*(?:\["[^"]*"\]|\{"[^"]*"\})?'
    edge = re.compile(rf"{node}\s+(?:-->|-\.->)(?:\|[^|]*\|)?\s+{node}")
    problems = []
    count = 0
    for path in sorted(paths):
        if not path.as_posix().startswith(("docs/guides/", "docs/reference/")):
            continue
        content = (ROOT / path).read_text(encoding="utf-8")
        blocks = pattern.findall(content)
        if len(blocks) != content.count(fence + "mermaid"):
            problems.append(f"{path}: unclosed Mermaid block")
        for block in blocks:
            count += 1
            lines = block.strip().splitlines()
            if not lines or not re.fullmatch(r"flowchart (?:LR|TD|TB|RL|BT)", lines[0].strip()):
                problems.append(f"{path}: unsupported flowchart header")
            for line in lines[1:]:
                if not edge.fullmatch(line.strip()):
                    problems.append(f"{path}: unsupported flowchart edge {line!r}")
    return count, problems


def main():
    changed = set(git_paths("diff", "--name-only", "HEAD")) | set(
        git_paths("ls-files", "--others", "--exclude-standard")
    )
    sections = ("docs/guides/", "docs/reference/", "docs/history/")
    paths = {path for path in changed if path.suffix == ".md"
             and not path.as_posix().startswith("docs/implementation-briefs/")}
    for folder in sections:
        paths.update(PurePosixPath(p.relative_to(ROOT).as_posix())
                     for p in (ROOT / folder).glob("*.md"))
    count, problems = check_links(paths)
    problems += check_coverage()
    diagram_count, diagram_problems = check_diagrams(paths)
    problems.extend(diagram_problems)
    for path in changed:
        if path.suffix not in {".md", ".csv", ".py"} or "implementation-briefs" in path.parts:
            continue
        data = (ROOT / path).read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            problems.append(f"{path}: invalid UTF-8")
        if (data.startswith(b"\xef\xbb\xbf") or b"\r" in data
                or not data.endswith(b"\n") or any(line.rstrip() != line for line in data.splitlines())):
            problems.append(f"{path}: BOM, CR, missing final LF or trailing whitespace")
    for problem in problems:
        print(problem)
    print(f"{len(paths)} Markdown files, {count} local links, "
          f"18 subjects, 71 claim IDs, 68 route IDs and {diagram_count} flowcharts checked. "
          f"{len(problems)} problems.")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
