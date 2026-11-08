"""Read tracked-form research metadata. Never open the raw exports it names."""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = 0x140000000
MODULE = "Starfield.exe"
BUILD = "1.16.244.0"
SHA = "7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28"
ADDRESS = re.compile(r"(?<![0-9a-f])(?:0x)?(14[0-3][0-9a-f]{6})(?![0-9a-f])", re.I)
SYMBOL = re.compile(r"\b(?:FUN|LAB|thunk_FUN)_14[0-3][0-9a-f]{6}\b", re.I)
ALIAS = re.compile(r"\b(?:SOR-FN-\d{4}|[acdegilmnoprst]\d{2,3}|e1-\d+|L2-\d{3}|[A-Z\d]+-N\d{2,3})\b", re.I)
CODE_SPAN = re.compile(r"`([^`\n]+)`")
NAMED_ENTRY = re.compile(r"\b(constructor|destructor|wrapper|helper|callback|function) `(?:FUN_|0x)?(14[0-3][0-9a-f]{6})`", re.I)
MECHANISM = re.compile(
    r"\b(calls?|caller|callee|wrapper|callback|returns?|reads?|reader|writes?|writer|loads?|loader|tests?|checks?|"
    r"predicate|gates?|dispatch|thunk|constructor|destructor|updates?|resolves?|filters?|selects?|"
    r"consumes?|produces?|compares?|vtable)\b|→|->", re.I,
)
LEGACY = "docs/function-register.md"
LOOKUPS = "docs/audits/publication-readiness-b2/focused-export-lookups.csv"
D5AD_LEDGER = "docs/experiments/resource-retained-population/d5ad-sources.csv"
ALIAS_LEDGER_PATTERNS = {
    "docs/experiments/inorganic-extractors/arithmetic-sources.csv": ((r"\.local-work/recon/e1-arithmetic-(\d{2})\.tsv", "a"),),
    "docs/experiments/inorganic-extractors/resource-intervals-sources.csv": ((r"\.local-work/recon/e1-intervals-(\d{2})\.tsv", "i"),),
    "docs/experiments/storage/capacity-sources.csv": ((r"\.local-work/recon/s1-capacity-(\d{2})\.tsv", "c"),),
    "docs/experiments/organic-facilities/sources.csv": (
        (r"\.local-work/e2-organic/native/0(\d{2})\.request\.tsv", "e"),
        (r"\.local-work/recon/e2-specialist-(\d{2})\.tsv", "s"),
    ),
    "docs/experiments/power/sources.csv": (
        (r"\.local-work/p1-power/native/(\d{3})\.request\.tsv", "p"),
        (r"\.local-work/p1-power/native/(\d{3})\.request\.tsv", "P"),
    ),
    "docs/experiments/power/followup-sources.csv": (
        (r"\.local-work/p1-order/native/(\d{3})\.request\.tsv", "o"),
        (r"\.local-work/p1-order/native-r2/(012)\.request\.tsv", "o"),
    ),
    "docs/experiments/power/load-sources.csv": (
        (r"\.local-work/p1-load/native/(\d{3})\.request\.tsv", "L"),
        (r"\.local-work/p1-load/native-r2/(\d{3})\.request\.tsv", "L"),
        (r"\.local-work/p1-load/native-r2/(\d{3})\.request\.tsv", "L2-"),
    ),
    "docs/experiments/resource-geometry-mature-context/sources.csv": ((r"\.local-work/resource-geometry-mature-context/native/(\d{3})\.request\.tsv", "N"),),
    "docs/experiments/resource-pattern-selection/sources.csv": ((r"\.local-work/resource-pattern-selection/native/(\d{3})\.request\.tsv", "N"),),
    "docs/experiments/resource-geometry/sources.csv": ((r"\.local-work/resource-geometry/native/(\d{3})\.request\.tsv", "G"),),
}
ARCHIVES = {"docs/experiments/evidence", "docs/experiments/templates"}
VA_COLUMNS = {"va", "static_va", "function_static_va", "static_va_hex", "function_va", "entry_va", "entry_rva", "function", "va_start", "rva_start"}

THEMES = {
    "geography": "Geography and resource generation",
    "workshop": "Workshop identity, construction and position",
    "production": "Extractors, organic facilities and fabrication",
    "power": "Power and generator fuel",
    "inventory": "Storage, inventory and cargo",
    "population": "Crew, robots and defense",
    "interfaces": "UI, save framing and lifecycle",
}


def address(number):
    return f"0x{number:09x}"


def rva(number):
    return f"0x{number - BASE:08x}"


def text(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def sidecar(name, default):
    path = HERE / name
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.is_file() else default


def source_paths():
    yield LEGACY
    yield "docs/state-register.md"
    yield LOOKUPS
    for directory in ("docs/experiments", "docs/subsystems", "runtime", "docs/audits", "save-analysis", "research"):
        for path in sorted((ROOT / directory).rglob("*")):
            name = path.relative_to(ROOT).as_posix()
            if path.suffix not in {".md", ".csv"} or not path.is_file():
                continue
            if name == LOOKUPS or any(name.startswith(f"{prefix}/") for prefix in ARCHIVES):
                continue
            if name.startswith(("docs/audits/native-function-catalogue-d5bd/", "research/function-catalogue/")):
                continue
            if "third_party" not in path.parts:
                yield name


def theme(path, key=""):
    if path.endswith("native-availability-map/functions.csv") and key.startswith("N"):
        number = int(key[1:])
        if 95 <= number <= 128:
            return "population"
        if 73 <= number <= 234:
            return "production"
        if 235 <= number <= 312:
            return "power"
    scope = path.lower().split("/")[2:]
    folder = "/".join(scope)
    categories = (
        ("population", ("crew", "robot", "defense")),
        ("power", ("power/",)),
        ("interfaces", ("stored-resources", "locations-outpost", "save-thread", "save-framing", "access-and-save", "save-helper")),
        ("inventory", ("storage", "cargo", "container", "output-link")),
        ("production", ("inorganic-extractor", "organic-facilit", "fabricat", "production")),
        ("geography", ("resource-", "native-availability", "outpost-biomes", "native-oracle", "disappearing-deposits", "local-readiness", "continuous-beacon")),
    )
    for group, names in categories:
        if any(name in folder for name in names):
            return group
    return "workshop"


def first(row, *keys):
    return next((row[key].strip() for key in keys if row.get(key)), "")


def direct_address(value):
    match = ADDRESS.fullmatch(value.strip())
    return int(match[1], 16) if match else None


def cell(value):
    return " ".join(value.split())


def provenance(path, line, end, number, domain, status, reason, **extra):
    return {
        "path": path, "line": line, "end_line": end, "va": address(number) if number else "",
        "domain": domain, "status": status, "reason": reason, **extra,
    }


def csv_inventory(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        reader.fieldnames = [name.lower() for name in reader.fieldnames or ()]
        previous = reader.line_num
        for row in reader:
            start, previous = previous + 1, reader.line_num
            yield start, previous, row


def structured(path, line, end, row, identified, verified_boundary=None):
    use = first(row, "use", "claim")
    function_manifest = (
        path.endswith("d5ab-p1-sources.csv") and bool(row.get("function"))
        or use.startswith(("Primary compiled function cited", "Compiled function body", "Fresh read-only disposable-project function export"))
        or first(row, "category") in {"FRESH NATIVE FUNCTION", "INHERITED NATIVE FUNCTION", "NATIVE FUNCTION"}
    )
    is_function_table = PurePosixPath(path).name in {
        "functions.csv", "current-functions.csv", "transit-functions.csv", "native-functions.csv", "native-map.csv", "native.csv",
    }
    value = first(row, "function_static_va", "static_va", "static_va_hex", "entry_va", "function_va", "va", "function", "va_start")
    number = direct_address(value)
    if verified_boundary:
        source_va = verified_boundary.get("source_va", verified_boundary.get("va", ""))
        if source_va.lower() != value.lower() or verified_boundary["export_sha256"] != first(row, "sha256", "referenced_output_sha256"):
            raise ValueError(f"Stale boundary receipt at {path} line {line}")
        function_manifest = verified_boundary.get("verdict", "entry") == "entry"
    key = first(row, "key", "record_id", "id", "native_receipt", "locator" if path == LOOKUPS else "")
    role = first(row, "interpretive_alias", "alias", "operation", "role", "supported_role_and_limit")
    if verified_boundary and path == D5AD_LEDGER and use and not use.startswith((
        "Native state/persistence proof", "Input loader/readiness proof", "Native chronology/ordinary mutation proof",
        "Definition generic loader and typed link-resolution proof",
    )):
        role = use
    if function_manifest and verified_boundary and verified_boundary.get("verdict") == "entry" and path.endswith(("d5q-sources.csv", "d5r-sources.csv")):
        role = first(row, "claim")
    if not role or role.startswith(("See cited", "LOCATOR", "Unassigned semantic alias")) or role == "bounded supporting operation":
        role = first(row, "use") if path.endswith("robots/functions.csv") else ""
    symbol = SYMBOL.match(first(row, "original_name", "existing_symbol", "native_name", "analysis_name", "name", "original_function_and_range"))
    symbol = symbol[0] if symbol else ""
    source_export = first(row, "source", "export", "local_export", "local_evidence", "native_receipt", "export_path", "referenced_output", "evidence", "locator")
    export = PurePosixPath(source_export.replace("\\", "/")).name
    if not re.fullmatch(r"(?:[a-z][0-9]{2,3}|[a-z0-9_-]+(?:\.request)?\.tsv)", export, re.I):
        export = ""
    shorthands = sorted({alias for ledger in ALIAS_LEDGER_PATTERNS for alias in declared_export_aliases(ledger, source_export)})
    fields = dict(alias=key, symbol=symbol, export=export, shorthands=shorthands, group=theme(path, key), label=role,
                  detail=first(row, "supported_data_flow", "supported_role_and_limit"))
    if role and verified_boundary and path.endswith(("d5q-sources.csv", "d5r-sources.csv")):
        fields["detail"] = first(row, "limit", "missing_evidence")
    if path.endswith("native-availability-map/functions.csv"):
        fields["contracts"] = {name: row[name] for name in (
            "inputs", "outputs", "prerequisites", "effects", "edges", "limits", "confidence_basis", "decisive_window",
        ) if row.get(name)}
    fields["source_grade"] = first(row, "evidence_grade", "confidence_basis") or (first(row, "classification") if role else "")
    if verified_boundary and verified_boundary.get("verdict") == "contained":
        return provenance(path, line, end, number, "instruction-window", "cross-reference",
                          "Pinned window lies inside a different verified function section",
                          containing_entry_va=verified_boundary["entry_va"], **fields)
    if verified_boundary and verified_boundary.get("verdict") == "no-header":
        return provenance(path, line, end, number, "named-source-locator", "excluded",
                          "Named receiver census without a function-entry address", **fields)
    if not value and not first(row, "va_start", "rva_start", "entry_rva"):
        return provenance(path, line, end, None, "none", "excluded", "No entry or site address in this source row", **fields)
    if not number:
        return provenance(path, line, end, None, "mixed-or-range", "unresolved", "Source row has a range, abbreviated, non-retail or compound locator", **fields)
    supplied_rva = first(row, "rva", "rva_hex", "entry_rva")
    if supplied_rva and int(supplied_rva, 16) != number - BASE:
        raise ValueError(f"RVA mismatch in {path} line {line}")
    if first(row, "exe_sha256", "executable_sha256") not in {"", SHA} or first(row, "module") not in {"", MODULE} or first(row, "build") not in {"", BUILD}:
        raise ValueError(f"Unexpected explicit build in {path} line {line}")
    if first(row, "status").upper() == "NO_FUNCTION_AT":
        return provenance(path, line, end, number, "failed-entry-lookup", "excluded", "Original export reports NO_FUNCTION_AT", **fields)
    if "site" in first(row, "address_domain", "domain").lower() or symbol.lower().startswith("lab_"):
        return provenance(path, line, end, number, "instruction-site", "excluded", "Source classifies the locator as a site or label", **fields)
    if path == LOOKUPS and number in identified:
        return provenance(path, line, end, number, "export-selection", "cross-reference", "Existing experiment-qualified export lookup", **fields)
    if (is_function_table or function_manifest) and (role or number in identified):
        return provenance(path, line, end, number, "function-entry", "included", "Original function record and documented relevance", **fields)
    if is_function_table or function_manifest:
        return provenance(path, line, end, number, "function-entry", "excluded", "Export roster only. No individually linked research role recovered", **fields)
    if number in identified:
        return provenance(path, line, end, number, "window-or-site", "cross-reference", "Numerical match to an independently catalogued entry. Manifest domain stays separate", **fields)
    return provenance(path, line, end, number, "window-or-site", "unresolved", "Manifest coordinate alone does not establish an entry", **fields)


def manual_records():
    inputs = ("narrative.json", "legacy.json", "reconciled.json", "remaining-narrative.json", "closure-narrative.json")
    records = [row for name in inputs for row in sidecar(name, [])]
    characterization = sidecar("characterization.json", {})
    for va, entry in characterization.items():
        for source in entry["sources"]:
            records.append({**source, "va": va, "label": entry["label"], "detail": entry["purpose"]})
    group_sizes = Counter((r["line"], r.get("alias"), r.get("label")) for r in records if r["path"] == LEGACY)
    unique = {}
    for record in records:
        path, line = record["path"], record["line"]
        number = direct_address(record["va"])
        end = record.get("end_line", line)
        if not number or not 0 < line <= end <= len(text(path).splitlines()):
            raise ValueError(f"Invalid curated evidence in {record}")
        if path.startswith(("docs/reference/", "docs/guides/")):
            raise ValueError(f"Reference used as original entry evidence in {record}")
        if record.get("status") in {"excluded", "unresolved", "cross-reference"}:
            unique[path, line, number] = provenance(
                path, line, end, number, record["domain"], record["status"], record["reason"],
                alias=record.get("alias", ""), alias_kind=record.get("alias_kind", "source ID"), label="",
            )
            continue
        role = record["label"]
        if (path, line, number) in unique and not record.get("alias"):
            continue
        is_group = path == LEGACY and group_sizes[(line, record.get("alias"), role)] > 1
        unique[path, line, number] = provenance(
            path, line, end, number, "function-entry", "included", "Curated original report or register",
            alias=record.get("alias", ""), symbol=record.get("symbol", ""), export="",
            group=record.get("group", theme(path)), label="" if is_group else role,
            detail="" if is_group else record.get("detail", ""),
            group_scope=(record.get("detail") or role) if is_group else "",
        )
    return unique, characterization


def declared_export_aliases(path, source_path):
    normalized = source_path.replace("\\", "/")
    if "/.local-work/" in normalized:
        normalized = ".local-work/" + normalized.split("/.local-work/", 1)[1]
    for pattern, prefix in ALIAS_LEDGER_PATTERNS[path]:
        stem = re.fullmatch(pattern, normalized, re.I)
        if stem:
            yield prefix + stem[1]


def local_export_aliases(identified):
    ledger_rows = {path: {start: row for start, _, row in csv_inventory(path)} for path in ALIAS_LEDGER_PATTERNS}
    with (HERE / "export-aliases.csv").open(encoding="utf-8", newline="") as source:
        seen = set()
        for row in csv.DictReader(source):
            path, line = row["path"], int(row["line"])
            original = ledger_rows[path][line]
            possible = set(declared_export_aliases(path, first(original, "path", "locator")))
            number = direct_address(row["va"])
            key = (path, line, number, row["alias"])
            if (row["alias"] not in possible or row["export_sha256"] != original["sha256"]
                    or not number or int(row["header_line"]) < 1 or key in seen):
                raise ValueError(f"Invalid local export alias receipt at {key}")
            seen.add(key)
            status = "cross-reference" if number in identified else "excluded"
            yield provenance(path, line, line, number, "export-selection", status,
                             "Verified export membership in its original namespace",
                             alias=row["alias"], alias_kind="export shorthand", label="")


def inventory():
    curated, characterization = manual_records()
    original = {}
    paths = sorted(set(source_paths()))
    scanned = {}
    roster_by_folder = defaultdict(set)
    identified = {number for (_, _, number), row in curated.items() if row["status"] == "included"}
    with (HERE / "d5ad-boundaries.csv").open(encoding="utf-8", newline="") as source:
        boundary_rows = {(D5AD_LEDGER, int(row["line"])): row for row in csv.DictReader(source)}
    with (HERE / "scheduler-boundaries.csv").open(encoding="utf-8", newline="") as source:
        boundary_rows.update({(row["path"], int(row["line"])): row for row in csv.DictReader(source)})
    with (HERE / "residual-boundaries.csv").open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            key = (row["path"], int(row["line"]))
            if key in boundary_rows:
                raise ValueError(f"Duplicate boundary receipt at {key}")
            if row["verdict"] == "entry" and direct_address(row["source_va"]) != direct_address(row["entry_va"]):
                raise ValueError(f"Exact entry receipt has conflicting address at {key}")
            if row["verdict"] == "contained" and (not direct_address(row["entry_va"]) or direct_address(row["source_va"]) == direct_address(row["entry_va"])):
                raise ValueError(f"Interior window receipt has conflicting owner at {key}")
            if row["verdict"] not in {"entry", "contained", "no-header"}:
                raise ValueError(f"Unexpected boundary classification at {key}")
            boundary_rows[key] = row
    checked_boundaries = set()
    for path in paths:
        if path.endswith(".md"):
            original[path] = text(path).splitlines()
            scanned[path] = ("narrative", len(original[path]))
            continue
        rows = list(csv_inventory(path))
        fields = set(rows[0][2]) if rows else set()
        name = PurePosixPath(path).name
        if not fields.intersection(VA_COLUMNS) and name not in {"native-exports.csv", "native-sources.csv", "region-sources.csv"}:
            scanned[path] = ("other CSV header", len(rows))
            continue
        scanned[path] = ("address or export ledger", len(rows))
        original[path] = rows
        # Role-bearing rows supply the first structured relevance pass.
        for line, end, row in rows:
            boundary = boundary_rows.get((path, line))
            item = structured(path, line, end, row, set(), boundary)
            if boundary:
                checked_boundaries.add((path, line))
            if item["status"] == "included":
                identified.add(int(item["va"], 16))
            if item["domain"] == "function-entry":
                roster_by_folder[str(PurePosixPath(path).parent)].add(int(item["va"], 16))
    if checked_boundaries != set(boundary_rows):
        raise ValueError(f"Unused boundary receipts: {sorted(set(boundary_rows) - checked_boundaries)}")

    items = list(curated.values())
    items.extend(
        provenance(LEGACY, line, line, None, domain, "excluded", reason, alias=f"SOR-FN-{number:04d}")
        for line, number, domain, reason in (
            (201, 6, "papyrus-operation", "Papyrus TransferCargo operation"),
            (202, 7, "papyrus-operation", "Papyrus marker OnLoad operation"),
            (203, 8, "different-module", "CreationKit.exe registration group"),
            (204, 9, "different-module", "CreationKit.exe registration group"),
            (214, 12, "different-module", "CreationKit.exe coordinate cross-reference"),
            (268, 61, "historical-heading", "Organic investigation group heading with no unique entry"),
        )
    )
    corroborated = set()
    all_roster_entries = set().union(*roster_by_folder.values())
    for path, contents in original.items():
        if not path.startswith("docs/experiments/") or not path.endswith(".md"):
            continue
        if re.search(r"run-card|prospective|brief|protocol|plan|proposal", PurePosixPath(path).stem):
            continue
        roster = roster_by_folder[str(PurePosixPath(path).parent)]
        section = PurePosixPath(path).stem.replace("-", " ")
        for line, prose in enumerate(contents, 1):
            if prose.startswith(("## ", "### ")):
                section = prose.lstrip("# ").strip().replace("`", "").replace("**", "")
            if len(prose) > 1000 or not MECHANISM.search(prose):
                continue
            addresses = {int(match[1], 16) for span in CODE_SPAN.findall(prose) for match in ADDRESS.finditer(span)}
            named = {int(match[2], 16): match[1].lower() for match in NAMED_ENTRY.finditer(prose)}
            if re.search(r"NO_FUNCTION|guessed|unrelated|nonexistent|failed target|different family", prose, re.I):
                named = {}
            explicit = set(named) & all_roster_entries
            for number in sorted((addresses & roster) | explicit):
                if (path, line, number) in curated:
                    continue
                corroborated.add((path, line, number))
                identified.add(number)
                items.append(provenance(
                    path, line, line, number, "function-entry", "included",
                    "Explicit function relationship with an exact original roster entry" if number in explicit
                    else "Exact entry from the same experiment's function roster with a native mechanism reference",
                    alias="", symbol="", export="", group=theme(path), label="",
                    section=section, relation=named.get(number, "entry"),
                    detail=f"Original report discusses this roster entry under {section}.",
                ))
    for path, contents in original.items():
        if path.endswith(".csv"):
            items.extend(structured(path, line, end, row, identified, boundary_rows.get((path, line)))
                         for line, end, row in contents)
            continue
        for line, prose in enumerate(contents, 1):
            found = sorted({int(match[1], 16) for match in ADDRESS.finditer(prose)})
            aliases = sorted(set(ALIAS.findall(prose)), key=str.casefold)
            remaining = [address(va) for va in found if (path, line, va) not in curated and (path, line, va) not in corroborated]
            if remaining or aliases:
                unjoined = [va for va in remaining if int(va, 16) not in identified]
                if unjoined:
                    reason = "At least one address has no canonical numeric match. Classify its source domain before entry use"
                elif remaining:
                    reason = "All addresses have canonical numeric matches. The mentions have no independent entry classification"
                else:
                    reason = "Historical or export alias mention with no independent identity mapping on this line"
                items.append(provenance(
                    path, line, line, None, "mixed-text", "candidate", reason,
                    candidates=" ".join(remaining), mentions=" ".join(aliases),
                ))
    items.extend(local_export_aliases(identified))
    return items, scanned, characterization
