# SPDX-License-Identifier: GPL-3.0-or-later
"""Build and verify the versioned document archives (stdlib only)."""

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import ntpath
from pathlib import Path
import re
import stat
import zipfile
import zlib

EDITION = "D5BZ-1"
SUCCESSOR = "D5BZ-2"
EDITION_DATES = {EDITION: "2026-11-11", SUCCESSOR: "2026-11-12"}
ARCHIVES = {"audits": "audits.zip", "implementation-briefs": "implementation-briefs.zip"}
BRIEF = ("docs/implementation-briefs/"
         "CODEX_BRIEF_SOR_RG2_D5BZ_Comprehensive_Historical_Repository_Archival.md")
TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FIELDS = ("archive_id", "edition", "original_path", "member_path", "record_ids", "topic",
          "subject", "historical_date", "historical_status", "bytes", "sha256", "git_blob",
          "classification", "current_authority", "active_path")
IDENTIFIER = re.compile(r"(?<![A-Z0-9])(?:D[1-5][A-Z]{0,2}|B[0-6]|"
                        r"(?:SOR-)?(?:EXP-?\d{4}[A-Z]?|[A-Z]{1,3}\d[A-Z]?))(?![A-Z0-9])")

SUBJECTS = (
    ("Publication, evidence access and repository governance",
     "archive archival audit publication documentation evidence preservation readiness review synthesis workflow"),
    ("Resource generation and observation",
     "RG1 RG2 D5 generation extractor mask geometry density oracle population"),
    ("Production, power and logistics",
     "E1 E2 E3 P1 C1 C2 C3 S1 S2 production power cargo storage output fabricator"),
    ("Workshop, construction and membership",
     "BM1 BM2 CR1 CR2 CR3 L1 L2 L3 outpost workshop beacon construction crew robots membership"),
    ("Position, coordinates and world state",
     "position coordinates biome planetary grid anchor locations relocation"),
    ("Save research and experiment methods",
     "save corpus persistence EXP0002 observer debugger adapter framing"),
)
AUTHORITIES = {
    "Publication, evidence access and repository governance": "docs/reference/evidence-access.md",
    "Resource generation and observation": "docs/reference/resource-generation.md",
    "Production, power and logistics": "docs/reference/README.md",
    "Workshop, construction and membership": "docs/reference/identity.md",
    "Position, coordinates and world state": "docs/reference/position.md",
    "Save research and experiment methods": "docs/reference/access-and-save-framing.md",
}


def subject(path, topic):
    if re.search(r"(?i)(?:^|[^a-z0-9])D5B[FWXYZ](?:[^a-z0-9]|$)", path):
        return "Publication, evidence access and repository governance"
    words = set(re.findall(r"[A-Za-z0-9]+", (path + " " + topic).casefold()))
    scores = [(len(words & set(keywords.casefold().split())), label) for label, keywords in SUBJECTS]
    score, label = max(scores)
    return label if score else "Other historical records"


def historical_metadata(text, is_markdown):
    if not is_markdown:
        return "", ""
    front = "\n".join(text.splitlines()[:25])
    date = re.search(r"(?im)^(?:\*\*)?Date:(?:\*\*)?\s*(\d{4}-\d{2}-\d{2})", front)
    fields = re.findall(
        r"(?im)^(?:> )?(?:\*\*)?(?:independent )?(?:disposition|verdict|status):"
        r"(?:\*\*)?\s*([^\n]+)", front
    )
    headings = re.findall(
        r"(?im)^#{2,6} +(?:[^\n]*?)\b(ACCEPT|REWORK|ESCALATE)\s*$", text
    )
    quoted = re.findall(
        r"(?im)^> +\*\*(ACCEPT|REWORK|ESCALATE)\*\*(?:[ .:]|$)", text
    )
    opening = re.search(
        r"(?im)^\*\*((?:ACCEPT|REWORK|ESCALATE) for [^*\n]+)\*\*(?:\s|$)", front
    )
    explicit = re.findall(
        r"(?im)^(?:> )?\*\*(?:independent )?(?:disposition|verdict):\*\*"
        r"[ \t]*((?:ACCEPT|REWORK|ESCALATE)\b[^\n]*)", text
    )
    field = fields[0].strip(" *") if fields else ""
    verdict = (headings or quoted or ([opening[1]] if opening else explicit) or [field])[-1]
    return date[1] if date else "", verdict


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_edition(family, edition):
    require(family in ARCHIVES and edition in EDITION_DATES,
            f"unsupported archive edition: {family} {edition}")


def checked_names(names, family):
    seen = set()
    spelling = {}
    for name in names:
        parts = name.split("/")
        require(parts[:2] == ["docs", family] and len(parts) > 2, f"wrong archive root: {name!r}")
        require(all(part not in {"", ".", ".."} and
                    not re.search(r'[<>:"\\|?*\x00-\x1f\x7f]', part) and
                    part == part.rstrip(" .") and
                    not ntpath.isreserved(part) and part.isascii()
                    for part in parts), f"unsafe member path: {name!r}")
        key = name.casefold()
        require(key not in seen, f"duplicate or case-fold collision: {name}")
        seen.add(key)
        for end in range(1, len(parts)):
            parent = "/".join(parts[:end])
            require(spelling.setdefault(parent.casefold(), parent) == parent,
                    f"case-folded directory spelling collision: {parent}")
    for key in seen:
        parts = key.split("/")
        require(not any("/".join(parts[:n]) in seen for n in range(1, len(parts))),
                f"member conflicts with ancestor file: {key}")
    require(list(names) == sorted(names), "noncanonical member order")
    if family == "implementation-briefs":
        require(BRIEF in names, "governing D5BZ brief is missing")


def entries(path, family):
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        checked_names([info.orig_filename for info in infos], family)
        require(not archive.comment, "unexpected archive comment")
        for info in infos:
            name = info.orig_filename
            require(info.filename == name and not info.is_dir()
                    and info.create_system == 0 and info.external_attr == 0x20
                    and stat.S_IFMT(info.external_attr >> 16) == 0
                    and info.compress_type == zipfile.ZIP_DEFLATED
                    and info.date_time == TIMESTAMP and not info.extra and not info.comment
                    and info.flag_bits == 0, f"unsafe or noncanonical ZIP entry: {name}")
            with archive.open(info) as stream:
                yield name, stream.read()


def check_member(row, data):
    path = row["original_path"]
    require(row["member_path"] == path, f"misjoined index path: {path}")
    require(int(row["bytes"]) == len(data) and row["sha256"] == digest(data),
            f"member size or SHA-256 mismatch: {path}")


def read_index(directory, family):
    with (directory / "archive-index.csv").open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        require(tuple(reader.fieldnames or ()) == FIELDS, "index columns differ")
        rows = list(reader)
    require(rows, f"empty archive index: {family}")
    edition = rows[0]["edition"]
    check_edition(family, edition)
    require(all(row["archive_id"] == family and row["edition"] == edition for row in rows),
            f"mixed archive families or editions: {family}")
    return rows


def verify(directory, family, extract=None, sources=None):
    rows = read_index(directory, family)
    names = [row["original_path"] for row in rows]
    checked_names(names, family)
    if extract:
        extract.mkdir(parents=True, exist_ok=False)
    archive = directory / ARCHIVES[family]
    for row, (name, data) in zip(rows, entries(archive, family), strict=True):
        require(row["original_path"] == name, f"index missing, extra or misjoined at {name}")
        check_member(row, data)
        if sources:
            require((sources / name).read_bytes() == data, f"intake byte mismatch: {name}")
        if extract:
            target = extract / name
            target.parent.mkdir(parents=True, exist_ok=True)
            require(target.resolve().is_relative_to(extract.resolve()), f"escaped extraction root: {name}")
            with target.open("xb") as file:
                file.write(data)
            require(target.read_bytes() == data, f"extracted byte mismatch: {name}")
    return len(rows)


def metadata(family, row, data, active, edition=EDITION):
    path = row["path"]
    parts = path.split("/")
    text = data.decode("utf-8")
    heading = re.search(r"^# +(.+)$", text, re.M) if path.endswith(".md") else None
    topic = heading[1].strip() if heading else parts[-1]
    if len(parts) > 3:
        topic = f"{parts[2]} / {topic}"
    ids = list(dict.fromkeys(IDENTIFIER.findall((parts[-1] + " " + path + " " + topic).upper())))
    ids.sort(key=lambda identifier: identifier in {"RG1", "RG2", "SOR"})
    category = subject(path, topic)
    date, status = historical_metadata(text, path.endswith(".md"))
    authority = active.get(path, "")
    if edition == SUCCESSOR and any(identifier in ids for identifier in ("D5CA", "D5CB", "D5CC")):
        category = "Publication, evidence access and repository governance"
        current = "docs/PUBLICATION_RUN_CARD.md"
    elif path == BRIEF or path.startswith("docs/audits/archival-d5bz/"):
        current = "docs/archive-verification.md"
    else:
        current = AUTHORITIES.get(category, "docs/history/README.md")
    return dict(archive_id=family, edition=edition, original_path=path, member_path=path,
                record_ids=" ".join(ids), topic=topic, subject=category, historical_date=date,
                historical_status=status, bytes=len(data),
                sha256=digest(data), git_blob=row.get("git_blob", ""),
                classification=("ACTIVE_RELOCATED_COPY" if authority else "ARCHIVE_SOURCE"),
                current_authority=authority or current,
                active_path=authority)


def write_readme(folder, family, basename, rows, edition):
    title = "Implementation briefs and amendments" if family == "implementation-briefs" else "Historical audits and reviews"
    groups = Counter()
    for row in rows:
        parts = row["original_path"].split("/")
        if family == "audits":
            group = parts[2] if len(parts) > 3 else "Standalone audit records"
        else:
            ids = row["record_ids"].split()
            group = ids[0] if ids else row["subject"]
        groups[group] += 1
    inventory = "\n".join(f"| {group} | {count} |" for group, count in sorted(groups.items()))
    subjects = Counter(row["subject"] for row in rows)
    subjects_text = "\n".join(f"| {group} | {count} |" for group, count in sorted(subjects.items()))
    verification_anchor = ""
    if edition == SUCCESSOR:
        verification_anchor = "#d5bz-2-audit-update" if family == "audits" else "#d5bz-2-brief-update"
    content = f"""# {title}

Edition **{edition}**, {EDITION_DATES[edition]} (Australia/Sydney), preserves {len(rows)} exact
original files with their full repository-relative paths. See the
[publication run card](../PUBLICATION_RUN_CARD.md) for current release status.

Start with the [guides](../guides/README.md) for player questions, the
[technical references](../reference/README.md) for current findings and
verification, or [research history](../history/README.md) for negative and
superseded results. The [research identifier index](../history/research-identifiers.md)
and [claim and evidence-route lookups](../history/README.md) lead to primary
scientific sources. The [archive verification record](../archive-verification.md{verification_anchor})
records edition integrity and custody.

## Archive lookup

Open the [member CSV](archive-index.csv) for exact paths in alphabetical
order. Filter its topic, record ID and historical status columns, or search
from the repository root with Python 3.14:

```text
python -B research/archival/archive.py search docs/{family}/archive-index.csv D5BZ
```

Use a case-sensitive path from the CSV to retrieve a member of
[{basename}]({basename}). For example:

`{basename} :: {BRIEF if family == "implementation-briefs" else "docs/audits/documentation-synthesis-d5by/review.md"}`

A fragment in a historical citation identifies a heading inside the recovered
document. Use the member path up to the fragment when locating it in the CSV.
Dates and dispositions reflect identifiable historical metadata. Blank fields
leave identification to the original record. Exact bytes and the pre-migration
Git blob identify different representations when line endings differ. Files
with a current replacement have a separate active path in the CSV.

## Safe extraction

Keep the ZIP and CSV together and use a fresh, caller-owned output directory.
The verifier checks the complete member inventory, names, metadata and SHA-256
before writing each file. It checks the extracted bytes again.

```text
python -B research/archival/archive.py verify docs/{family} {family} --extract NEW_DIRECTORY
```

Historical commands, links, machine paths, permissions and verdicts describe
their original revisions. Use the [current evidence access contract](../reference/evidence-access.md)
for supported reader instructions. Historical Git revisions remain available
through the repository history.

## Subject groups

| Subject to filter in the CSV | Members |
| --- | ---: |
{subjects_text}

## {"Audit packages" if family == "audits" else "Brief and amendment identifiers"}

| {"Audit subject or package" if family == "audits" else "Identifier or subject"} | Members |
| --- | ---: |
{inventory}
"""
    (folder / "README.md").write_bytes(content.encode("utf-8"))


def build(output, sources, census, active, brief_edition=EDITION, audit_edition=EDITION):
    census = census["sources"]
    paths = {row["path"]: row for row in census}
    require(len(paths) == len(census), "duplicate census paths")
    require(all(any(path.startswith(f"docs/{family}/") for family in ARCHIVES) for path in paths),
            "unassigned census path")
    require(set(active) <= paths.keys(), "relocation without an archived source")
    check_edition("implementation-briefs", brief_edition)
    check_edition("audits", audit_edition)
    output.mkdir(parents=True, exist_ok=False)
    for family, basename in ARCHIVES.items():
        edition = brief_edition if family == "implementation-briefs" else audit_edition
        names = sorted(path for path in paths if path.startswith(f"docs/{family}/"))
        checked_names(names, family)
        folder = output / family
        folder.mkdir()
        rows = []
        with (folder / "archive-index.csv").open("x", encoding="utf-8", newline="") as index:
            writer = csv.DictWriter(index, FIELDS, lineterminator="\n")
            writer.writeheader()
            with zipfile.ZipFile(folder / basename, "x", allowZip64=False) as archive:
                for name in names:
                    row = paths[name]
                    data = (sources[family] / name).read_bytes()
                    require(row["bytes"] == len(data) and row["sha256"] == digest(data),
                            f"source changed since census: {name}")
                    info = zipfile.ZipInfo(name, TIMESTAMP)
                    info.create_system = 0
                    info.external_attr = 0x20
                    archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
                    rows.append(metadata(family, row, data, active, edition))
                    writer.writerow(rows[-1])
        write_readme(folder, family, basename, rows, edition)
        verify(folder, family, sources=sources[family])


def rebuild(docs, scratch):
    """Rebuild an edition from its adjacent indexes and independently checked members."""
    scratch.mkdir(parents=True, exist_ok=False)
    sources = {family: scratch / family for family in ARCHIVES}
    census = []
    active = {}
    editions = {}
    for family, source in sources.items():
        folder = docs / family
        verify(folder, family, extract=source)
        rows = read_index(folder, family)
        editions[family] = rows[0]["edition"]
        for row in rows:
            name = row["original_path"]
            census.append({"path": name, "sha256": row["sha256"], "bytes": int(row["bytes"]),
                           "git_blob": row["git_blob"]})
            if row["active_path"]:
                active[name] = row["active_path"]
    rebuilt = scratch / "rebuilt"
    build(rebuilt, sources, {"sources": census}, active, editions["implementation-briefs"], editions["audits"])
    for family, basename in ARCHIVES.items():
        for name in (basename, "archive-index.csv", "README.md"):
            require((rebuilt / family / name).read_bytes() == (docs / family / name).read_bytes(),
                    f"byte-exact rebuild differs: {family}/{name}")
    print(f"Audits {editions['audits']}, briefs {editions['implementation-briefs']}: ZIP, index and README rebuild match")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build_args = commands.add_parser("build")
    for name in ("output", "sources", "census", "relocations"):
        build_args.add_argument(name, type=Path)
    build_args.add_argument("--brief-edition", choices=EDITION_DATES, default=EDITION)
    build_args.add_argument("--audit-edition", choices=EDITION_DATES, default=EDITION)
    verify_args = commands.add_parser("verify")
    verify_args.add_argument("directory", type=Path)
    verify_args.add_argument("family", choices=ARCHIVES)
    verify_args.add_argument("--extract", type=Path)
    verify_args.add_argument("--sources", type=Path)

    rebuild_args = commands.add_parser("rebuild")
    rebuild_args.add_argument("docs", type=Path, help="directory containing both archive families")
    rebuild_args.add_argument("scratch", type=Path, help="fresh caller-owned directory")
    lookup_args = commands.add_parser("search")
    lookup_args.add_argument("index", type=Path)
    lookup_args.add_argument("query")
    args = parser.parse_args()
    if args.command == "build":
        census = json.loads(args.census.read_bytes())
        active = json.loads(args.relocations.read_bytes())
        build(args.output, dict.fromkeys(ARCHIVES, args.sources), census, active,
              args.brief_edition, args.audit_edition)
        print(f"Built and verified {len(census['sources'])} members using zlib {zlib.ZLIB_RUNTIME_VERSION}")
    elif args.command == "verify":
        print(f"{args.family}: {verify(args.directory, args.family, args.extract, args.sources)} members verified")

    elif args.command == "rebuild":
        rebuild(args.docs, args.scratch)
    else:
        query = args.query.casefold()
        with args.index.open(encoding="utf-8", newline="") as index:
            for row in csv.DictReader(index):
                fields = ("record_ids", "topic", "subject", "original_path", "historical_status")
                if any(query in row[field].casefold() for field in fields):
                    print(f"{row['record_ids']} | {row['topic']} | {row['historical_status']} | "
                          f"{row['original_path']}")


if __name__ == "__main__":
    main()
