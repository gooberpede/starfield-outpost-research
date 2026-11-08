"""Generate or check D5BD documents from repository text and curated joins."""

import argparse
import csv
import io
import posixpath
import re
from collections import Counter, defaultdict
from pathlib import PurePosixPath
from urllib.parse import unquote

from inventory import BASE, BUILD, MODULE, ROOT, SHA, THEMES, address, inventory, rva, sidecar, text

DOC = "docs/functions"
AUDIT = "docs/audits/native-function-catalogue-d5bd"
BASELINE = "docs/audits/publication-readiness-b3/baseline-manifest.md"
EXTERNAL = "Internal-only observation. External invocation remains unvalidated."
REQUEST_NAMESPACES = {
    "build-budget": "n", "build-catalogue": "n", "construction-variants": "n",
    "containers-displays": "n", "crew-lifecycle": "n", "crew-skills": "n",
    "limits": "n", "locations-outpost": "n", "outpost-biomes": "n",
    "outpost-defense": "n", "robots": "n", "shared-outpost-storage": "n",
    "spatial-placement": "n", "transport": "n", "storage": "s",
}
FOCUS = {
    "geography": (("Source-population provider", "0x14079f860"), ("Runtime owner installation", "0x140789ce0"),
                  ("Workshop area updater", "0x1421e07d0"), ("Region consumer", "0x1421e0f50"),
                  ("Landscape Grid release", "0x140784730"),
                  ("Caller source-list append", "0x140988ab0"), ("Caller source-list cleanup", "0x14039ff30"),
                  ("Scheduler completion publication", "0x1427e5a00"), ("Scheduler ready scan", "0x1427e6d10"),
                  ("Native resource-setting loader", "0x140684160")),
    "workshop": (("GetWorkshop callback", "0x142073cf0"), ("Keyed lookup target", "0x140517d60"),
                 ("Indexed pair and residual", "0x14077fc20")),
    "production": (("Shared production scheduler", "0x140f7f1e0"), ("Pending production replay", "0x140f8c580"),
                   ("Crew production-timer contribution", "0x140f7bd20")),
    "power": (("Electrical neighbor worklist", "0x140677c50"), ("Crew contribution", "0x140f3dd50")),
    "inventory": (("Fuel readiness and charge", "0x140f7d120"), ("Frame elapsed dispatch", "0x1427342e0"),
                  ("Detached flight", "0x142731f50"), ("Full flight", "0x14271e190"), ("Display preflight", "0x141eb01a0")),
    "population": (("Ordinary crew admission", "0x1404074f0"), ("Script assignment bypass", "0x142068d70"),
                   ("Robot recipe quota", "0x140f3b170"), ("Crew production contribution", "0x140f7bd20"),
                   ("Crew power contribution", "0x140f3dd50")),
    "interfaces": (("Locations adapter", "0x141360e80"), ("Queued Locations receiver", "0x141361c10"),
                   ("Extra33 reader", "0x140404a10"), ("Extra33 writer", "0x140404cf0"),
                   ("Native save payload", "0x141814220"), ("SFTR factory lookup", "0x1404628b0"),
                   ("SFTR name registration", "0x1404613d0"), ("SFTR shutdown thunk", "0x14388f200"),
                   ("Type-7 PCM writer", "0x1418b1eb0"), ("Type-7 PCM reader", "0x1418b22c0")),
}
SOURCE_FIELDS = ("path", "line", "end_line", "va", "domain", "status", "reason", "alias", "symbol", "export", "label", "group_scope", "source_grade", "containing_entry_va", "candidates", "mentions")
REFERENCES = {
    "access-and-save-framing": "interfaces", "cargo": "inventory", "construction": "workshop",
    "containers-and-displays": "inventory", "crew-and-robots": "population", "defense": "population",
    "fabrication": "production", "identity": "workshop", "inorganic-production": "production",
    "locations-ui": "interfaces", "nominal-biomes": "geography", "organic-production": "production",
    "position": "workshop", "power": "power", "resource-generation": "geography", "shared-storage": "inventory",
    "storage-and-output-links": "inventory", "stored-resources": "interfaces",
}
PAIR_WITNESSES = {
    "access-and-save-framing": (("Type-7 PCM load", "0x1418b22c0"), ("Type-9 destination load", "0x141829ec0")),
    "cargo": (("Fuel and eligibility", "0x140f7d120"), ("Detached flight", "0x142731f50")),
    "construction": (("Recipe discovery", "0x140f4d630"), ("Placement status", "0x140f3f9a0")),
    "containers-and-displays": (("Display preflight", "0x141eb01a0"), ("Saved item fixup", "0x1412fd650")),
    "crew-and-robots": (("Ordinary crew insertion", "0x1404076b0"), ("Scripted assignment", "0x142068d70")),
    "defense": (("Integrity indicator", "0x14158a6e0"), ("Repair service", "0x1421e3f50")),
    "fabrication": (("Manufactured catalogue", "0x140f8be60"), ("Shared scheduler", "0x140f7f1e0")),
    "identity": (("Registration callback", "0x142073cf0"), ("Selected-owner member rebuild", "0x1421c6f90")),
    "inorganic-production": (("Point admission", "0x140f7c290"), ("Registered row traversal", "0x140f7ef20")),
    "locations-ui": (("Locations adapter", "0x141360e80"), ("Queued receiver", "0x141361c10")),
    "nominal-biomes": (("Biome resolution", "0x14078ee90"), ("Raster index", "0x1423390f0")),
    "organic-production": (("Species knowledge", "0x14130a3e0"), ("Selection application", "0x141583410")),
    "position": (("Placement pair and residual", "0x14077fc20"),),
    "power": (("Effective contribution", "0x140669880"), ("Pending-neighbor worklist", "0x140677c50")),
    "resource-generation": (("Population provider", "0x14079f860"), ("Resident area consumer", "0x1421e07d0")),
    "shared-storage": (("Player backing reference", "0x1405a3cc0"), ("Ingredient aggregation", "0x1417f6fa0")),
    "storage-and-output-links": (("Ordered endpoint admission", "0x140f84470"), ("Local transfer descriptor", "0x140f84fc0")),
    "stored-resources": (("Resource-count visitor", "0x14136be50"), ("Queued receiver", "0x141361c10")),
}


def csv_text(columns, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, columns, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def md_cell(value):
    return value.replace("|", "\\|").replace("\n", " ")


def relative(source, target):
    return posixpath.relpath(target, posixpath.dirname(source))


def link(label, page, target):
    return f"[{label}]({relative(page, target)})"


def cite(item, page):
    path = item["path"]
    label = PurePosixPath(path).parent.name.replace("-", " ") + " · " + PurePosixPath(path).stem.replace("-", " ")
    lines = str(item["line"])
    if item.get("end_line", item["line"]) != item["line"]:
        lines += f"–{item['end_line']}"
    return f"{link(label, page, path)} (line {lines})"


def entry_anchor(va):
    return "rva-" + rva(int(va, 16))


def entry_href(row):
    return row["theme"] + ".md#" + entry_anchor(row["va"])


def canonical(items, characterization):
    by_va = defaultdict(list)
    for item in items:
        if item["status"] == "included":
            if item["domain"] != "function-entry":
                raise ValueError(f"Non-entry candidate marked included: {item}")
            by_va[item["va"]].append(item)
    catalogue = []
    detail = {}
    for va, sources in sorted(by_va.items()):
        sources.sort(key=lambda s: (not bool(s.get("contracts")), not bool(s.get("label")), s["path"] == "docs/function-register.md", s["path"], s["line"]))
        rich = characterization.get(va, {})
        primary = sources[0]
        context = next((source for source in sources if source.get("section")), {})
        context_label = f"{context['section']} · {context['relation']}" if context else f"{THEMES[primary['group']]} native entry"
        label = rich.get("label") or primary["label"] or context_label
        if len(label) > 95:
            label = label[:92].rsplit(" ", 1)[0] + "…"
        grouped = any(source.get("group_scope") for source in sources)
        fallback = "Located member of an original operation group. Individual role remains unqualified." if grouped else "Entry linked by an original export roster."
        purpose = rich.get("purpose") or primary["label"] or context.get("detail") or fallback
        if len(purpose) > 150:
            purpose = purpose[:147].rsplit(" ", 1)[0] + "…"
        has_contract = any(set(s.get("contracts", {})) >= {"inputs", "outputs", "effects", "limits"} for s in sources)
        level = rich.get("level") or ("B" if has_contract else "C")
        if level not in {"A", "B", "C"} or (level == "A" and not rich.get("detail")):
            raise ValueError(f"Missing characterization basis for {va}")
        group = rich.get("theme", primary["group"])
        symbols = sorted({s["symbol"] for s in sources if s.get("symbol")})
        catalogue.append({
            "exe_sha256": SHA, "module": MODULE, "build": BUILD, "preferred_base": f"0x{BASE:x}",
            "rva": rva(int(va, 16)), "va": va, "label": label, "purpose": purpose, "level": level, "theme": group,
            "analysis_symbols": " ".join(symbols), "identity_basis": "Original pinned entry record",
            "semantic_basis": "STATIC unless the cited scope specifies additional evidence",
            "semantic_confidence": "Source-specific. See evidence and original assessment.",
            "review": "D5BD consolidation. See original review and D5BD audit.",
            "access": "REVIEW-REQUIRED metadata. LOCAL-ONLY native exports. EVIDENCE ACCESS PENDING.",
            "external_use": EXTERNAL,
            "entry": group + ".md#" + entry_anchor(va),
        })
        detail[va] = rich, sources
    return catalogue, detail


def alias_rows(items):
    for item in sorted(items, key=lambda s: (s["path"], s["line"], s["va"])):
        aliases = [(item.get("alias"), item.get("alias_kind", "source ID")), (item.get("symbol"), "analysis label"), (item.get("export"), "export selection")]
        aliases.extend((value, "export shorthand") for value in item.get("shorthands", ()))
        export = item.get("export", "")
        stem = re.fullmatch(r"(\d{3})\.request\.tsv", export)
        e1 = re.fullmatch(r"e1-native-(\d{2})\.tsv", export)
        namespace = REQUEST_NAMESPACES.get(PurePosixPath(item["path"]).parent.name)
        if item["path"].endswith("transport/transit-functions.csv"):
            namespace = "t"
        if stem and namespace:
            aliases.append((namespace + stem[1], "export shorthand"))
        if stem and item["path"] == "docs/experiments/robots/functions.csv":
            aliases.append(("r" + stem[1], "export shorthand"))
        s2 = re.fullmatch(r"s2-links-(\d{2})\.tsv", export)
        c1 = re.fullmatch(r"c1-cargo-(\d{2})\.tsv", export)
        if s2 and item["path"] == "docs/experiments/local-output-links/functions.csv":
            aliases.append(("n" + s2[1], "export shorthand"))
        if c1 and item["path"] == "docs/experiments/cargo-links/configuration-ui/functions.csv":
            aliases.append(("d" + c1[1], "export shorthand"))
        if e1:
            aliases.append(("e1-" + e1[1], "export shorthand"))
        for value, kind in dict.fromkeys(aliases):
            if not value:
                continue
            module, executable_hash = MODULE, SHA
            if item["domain"] == "different-module":
                module, executable_hash = "CreationKit.exe", ""
            if item["domain"] == "papyrus-operation":
                module, executable_hash = "", ""
            yield dict(item, alias=value, alias_kind=kind, module=module, exe_sha256=executable_hash,
                       entry_rva=rva(int(item["va"], 16)) if item["status"] == "included" or item["domain"] == "export-selection" and item["status"] == "cross-reference" else "")


def table_index(rows):
    lines = ["# Native functions by RVA", "", f"`{MODULE}` {BUILD}. Preferred VAs use base `0x{BASE:x}`.",
             "See the [build pin and ABI limits](README.md).", "", "| RVA | Preferred VA | Function | Purpose | Level |",
             "| --- | --- | --- | --- | --- |"]
    for row in rows:
        va, offset, label, purpose, level = (row[key] for key in ("va", "rva", "label", "purpose", "level"))
        lines.append(f"| `{offset}` | `{va}` | [{md_cell(label)}]({entry_href(row)}) | {md_cell(purpose)} | {level} |")
    return "\n".join(lines) + "\n"


def thematic(group, catalogue, detail):
    page = f"{DOC}/{group}.md"
    lines = [f"# {THEMES[group]}", "", "[Subject navigation and ABI limits](README.md) · [RVA index](index.md)", "",
             f"Entries use the pinned `{MODULE}` {BUILD} image. {EXTERNAL}", ""]
    by_va = {row["va"]: row for row in catalogue}
    lines += ["Follow a mapped path", ""]
    for label, va in FOCUS[group]:
        lines.append(f"- [{label}]({entry_href(by_va[va])})")
    lines.append("")
    for row in catalogue:
        if row["theme"] != group:
            continue
        va, offset, level = (row[key] for key in ("va", "rva", "level"))
        rich, sources = detail[va]
        lines += [f"## RVA {offset}", "", f"**{row['label']}** · Level {level} · preferred VA `{va}`", ""]
        if row["analysis_symbols"]:
            symbols = ", ".join(f"`{symbol}`" for symbol in row["analysis_symbols"].split())
            lines += [f"Analysis labels recorded in the original sources are {symbols}.", ""]
        if rich:
            lines += [rich["purpose"], "", rich["detail"], ""]
            if rich.get("pseudocode"):
                lines += ["Scoped pseudocode abstraction. It covers the described branch and omits unqualified paths.", "", "```text", rich["pseudocode"], "```", ""]
        else:
            scope = sources[0].get("detail") or row["purpose"]
            lines += [f"Recorded scope — {scope}", ""]
        contracts = [s for s in sources if s.get("contracts")]
        for item in contracts:
            lines += [f"Source contract from {cite(item, page)}.", ""]
            for key, title in (("inputs", "Inputs"), ("outputs", "Outputs"), ("prerequisites", "Conditions"),
                               ("effects", "Effects"), ("edges", "Mapped edges"), ("limits", "Limits"), ("confidence_basis", "Source assessment")):
                if item["contracts"].get(key):
                    fact = re.sub(r";(?=\S)", "; ", item["contracts"][key])
                    lines.append(f"- **{title}** — {fact}")
            lines.append("")
        if not contracts and not rich:
            lines += ["Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.", ""]
        lines += ["Original records", ""]
        for item in sources:
            original = cite(item, page)
            key = f" · `{item['alias']}`" if item.get("alias") else ""
            alternate = item.get("label", "")
            meaning = f" · {alternate}" if alternate and alternate != row["label"] else ""
            lines.append(f"- {original}{key}{meaning}")
            if item.get("detail") and item["detail"] != sources[0].get("detail") and not item.get("contracts"):
                lines.append(f"  {item['detail']}")
            if item.get("group_scope"):
                lines.append(f"  Original group scope — {item['group_scope']}")
        lines.append("")
    return "\n".join(lines)


def collisions(aliases, canonical_by_rva):
    grouped = defaultdict(list)
    for item in aliases:
        grouped[(item["alias_kind"], item["alias"])].append(item)
    rows = []
    for (kind, name), matches in sorted(grouped.items()):
        if len(matches) < 2:
            continue
        keys = {item["entry_rva"] for item in matches if item["entry_rva"]}
        for item in matches:
            entry = canonical_by_rva.get(item["entry_rva"], {})
            group_scope = item.get("group_scope")
            meaning = item.get("label") or (f"Original group scope — {group_scope}" if group_scope else entry.get("label", ""))
            rows.append(dict(item, distinct_entry_count=len(keys), meaning=meaning))
    return rows


def reference_walk(catalogue):
    path = f"{AUDIT}/crosswalk.md"
    address_re = re.compile(r"(?<![0-9a-f])(?:0x)?(14[0-3][0-9a-f]{6})(?![0-9a-f])", re.I)
    lines = ["# Subsystem crosswalk", "", "This pass runs after entry normalization. An exact address overlap is a navigation join.",
             "The files also contain globals, call sites and other coordinates. Unmatched tokens stay in the separate crosswalk CSV for review.", "",
             "| Pair | Subject | Entry overlaps | Catalogue evidence | Review note |", "| --- | --- | --- | --- | --- |"]
    va_map = {row["va"]: row for row in catalogue}
    observations = sidecar("crosswalk.json", {})
    interior = {
        "0x14079be20": ("0x14079c470", "Ordinary generation call site, linked to its callee"),
        "0x1407a1a3c": ("0x14079f860", "Density call site, linked to the provider"),
        "0x1407b526a": ("0x14079f860", "Layer call site, linked to the provider"),
    }
    hits = []
    for name, group in REFERENCES.items():
        reference = f"docs/reference/{name}.md"
        guide = f"docs/guides/{name}.md"
        unique = set()
        for source in (reference, guide):
            for line, prose in enumerate(text(source).splitlines(), 1):
                for token in sorted({match[1].lower() for match in address_re.finditer(prose)}):
                    va = "0x" + token
                    row = va_map.get(va)
                    if row:
                        unique.add(va)
                    result = "Exact numeric overlap" if row else "Unclassified token"
                    if int(va, 16) == BASE:
                        result = "Preferred image base"
                    if va in interior:
                        target, result = interior[va]
                        row = va_map[target]
                    if "0x14079fc37" <= va <= "0x14079ffa5" and not row and name == "resource-generation":
                        result = "Interior site in the source-population provider"
                        row = va_map["0x14079f860"]
                    hits.append(dict(path=source, line=line, va=va, candidate_rva=row["rva"] if row else "", result=result))
        note = observations.get(name, "Editorial comparison pending.")
        witnesses = " · ".join(link(label, path, f"{DOC}/{entry_href(va_map[va])}") for label, va in PAIR_WITNESSES[name])
        lines.append(f"| {link(name, path, reference)} / {link('guide', path, guide)} | {link(THEMES[group], path, f'{DOC}/{group}.md')} | {len(unique)} | {witnesses} | {md_cell(note)} |")
    return "\n".join(lines) + "\n", hits


def reports(items, scanned, catalogue):
    by_path = defaultdict(Counter)
    levels = {entry["va"]: entry["level"] for entry in catalogue}
    for item in items:
        by_path[item["path"]][item["status"]] += 1
        if item["status"] == "included":
            by_path[item["path"]][levels[item["va"]]] += 1
    return [dict(path=path, source_class=kind, rows_or_lines=size, **by_path[path]) for path, (kind, size) in sorted(scanned.items())]


def outputs():
    items, scanned, characterization = inventory()
    rows, detail = canonical(items, characterization)
    if not rows:
        raise ValueError("Empty catalogue")
    evidence = sorted(items, key=lambda s: (s["path"], s["line"], s["va"], s["status"]))
    alias = list(alias_rows(evidence))
    by_rva = {row["rva"]: row for row in rows}
    if len(by_rva) != len(rows) or list(by_rva) != sorted(by_rva):
        raise ValueError("Canonical entries must be unique and sorted")
    if any(item["entry_rva"] and item["entry_rva"] not in by_rva for item in alias):
        raise ValueError("An alias has no canonical entry target")
    if any(item.get("containing_entry_va") and rva(int(item["containing_entry_va"], 16)) not in by_rva for item in evidence):
        raise ValueError("An interior source window has no canonical enclosing entry")
    prohibited_entries = {
        0x14079BE20, 0x14079C4A0, 0x14079FC37, 0x14079FCB3, 0x14079FCCB,
        0x1407A1A3C, 0x1407B526A, 0x140AD0D3B, 0x140F4AC44, 0x1427E61A4, 0x140684B43, 0x1418A8B70,
    }
    if any(rva(site) in by_rva for site in prohibited_entries):
        raise ValueError("A documented interior instruction or call site was promoted to entry")
    for old_id, expected in {
        "0062": ({"0x021e0f50"}, {"0x02008540"}),
        "0063": ({"0x021f68f0", "0x0044b610"}, {"0x004074f0"}),
        "0064": ({"0x0079a330"}, {"0x004074a0"}),
    }.items():
        for path, expected_entries in zip(("docs/function-register.md", "docs/experiments/crew/functions.csv"), expected):
            got = {a["entry_rva"] for a in alias if a["path"] == path and a["alias"] == f"SOR-FN-{old_id}" and a["entry_rva"]}
            if got != expected_entries:
                raise ValueError(f"Historical collision regression for {old_id} in {path}: {got}")
    if not any(a["alias"] == "SOR-FN-0061" and a["path"] == "docs/function-register.md"
               and a["domain"] == "historical-heading" and not a["entry_rva"] for a in alias):
        raise ValueError("Missing historical organic heading locator")
    transit = [a for a in alias if a["path"].endswith("transport/transit-functions.csv") and a["alias_kind"] == "export shorthand"]
    if not transit or any(not re.fullmatch(r"t\d{3}", a["alias"]) for a in transit):
        raise ValueError("Transit export shorthand must use the original tNNN namespace")
    for shorthand, path, offset in (
        ("s001", "docs/experiments/storage/functions.csv", "0x00f7c210"),
        ("a01", "docs/experiments/inorganic-extractors/arithmetic-sources.csv", "0x00f7f1e0"),
    ):
        if not any(a["alias"] == shorthand and a["path"] == path and a["entry_rva"] == offset for a in alias):
            raise ValueError(f"Missing source-qualified export shorthand {shorthand}")
    power_exception = {a["va"] for a in alias if a["alias"] == "o012" and a["path"] == "docs/experiments/power/followup.md" and a["entry_rva"]}
    if power_exception != {"0x14065be30", "0x1405ccd00", "0x140f7f6f0"}:
        raise ValueError("Missing source-qualified o012 exception associations")
    crosswalk, hits = reference_walk(rows)
    if any(hit["result"] == "Unclassified token" for hit in hits):
        raise ValueError("The reference crosswalk still has an unclassified address token")
    result = {
        f"{DOC}/catalogue.csv": csv_text(tuple(rows[0]), rows),
        f"{DOC}/aliases.csv": csv_text(("alias", "alias_kind", "path", "line", "end_line", "module", "exe_sha256", "entry_rva", "va", "domain", "status", "reason", "label"), alias),
        f"{DOC}/evidence.csv": csv_text(SOURCE_FIELDS, (item for item in evidence if item["status"] in {"included", "cross-reference"})),
        f"{DOC}/index.md": table_index(rows),
        f"{AUDIT}/coverage.csv": csv_text(("path", "source_class", "rows_or_lines", "included", "excluded", "unresolved", "cross-reference", "candidate", "A", "B", "C"), reports(evidence, scanned, rows)),
        f"{AUDIT}/locators.csv": csv_text(SOURCE_FIELDS, (item for item in evidence if item["status"] not in {"included", "cross-reference"})),
        f"{AUDIT}/repeated-aliases.csv": csv_text(("alias", "alias_kind", "distinct_entry_count", "path", "line", "entry_rva", "domain", "meaning"), collisions(alias, by_rva)),
        f"{AUDIT}/crosswalk.md": crosswalk,
        f"{AUDIT}/reference-addresses.csv": csv_text(("path", "line", "va", "candidate_rva", "result"), hits),
    }
    for group in THEMES:
        result[f"{DOC}/{group}.md"] = thematic(group, rows, detail)
    for path, columns in ((f"{DOC}/index.md", 5), (f"{AUDIT}/crosswalk.md", 5)):
        table = [line for line in result[path].splitlines() if line.startswith("|")]
        if any(len(re.split(r"(?<!\\)\|", line)) != columns + 2 for line in table):
            raise ValueError(f"Inconsistent Markdown table width in {path}")
    return result, Counter(row["level"] for row in rows), Counter(item["status"] for item in evidence)


def check_links(generated):
    documents = {path: value for path, value in generated.items() if path.endswith(".md")}
    for path in (f"{DOC}/README.md", f"{AUDIT}/README.md", f"{AUDIT}/closure.md"):
        documents[path] = text(path)
    for path in ("README.md", "CREDITS.md", "docs/SOURCES.md", "docs/reference/README.md"):
        documents[path] = "\n".join(line for line in text(path).splitlines() if re.search(r"\]\([^\n]*(?:functions/README\.md|native-function-catalogue-d5bd/README\.md)\)", line))
    linked_paths = {}
    for origin, content in documents.items():
        for match in re.finditer(r"(?<!!)\[[^\]\n]+\]\(([^()\s]+)\)", content):
            target, _, fragment = unquote(match[1]).partition("#")
            if "://" in target:
                continue
            path = posixpath.normpath(posixpath.join(posixpath.dirname(origin), target)) if target else origin
            if path not in linked_paths:
                current = ROOT
                for part in PurePosixPath(path).parts:
                    if part not in {child.name for child in current.iterdir()} and path not in generated:
                        raise ValueError(f"Missing or incorrectly cased path {path} from {origin}")
                    current /= part
                linked_paths[path] = current
            if fragment:
                target_text = documents.get(path)
                if target_text is None:
                    target_text = text(path)
                headings = re.findall(r"^#{1,6} (.+)$", target_text, re.M)
                anchors = {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}
                if fragment not in anchors:
                    raise ValueError(f"Missing or incorrectly cased fragment {fragment} in {path} from {origin}")
    return len(linked_paths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite generated catalogue and audit tables")
    args = parser.parse_args()
    baseline = text(BASELINE)
    for pin in (MODULE, BUILD, SHA, f"0x{BASE:x}"):
        if pin not in baseline:
            raise ValueError(f"Missing baseline pin {pin}")
    generated, levels, counts = outputs()
    targets = check_links(generated)
    for name, content in generated.items():
        path = ROOT / name
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode("utf-8"))
        elif not path.is_file() or path.read_bytes() != content.encode("utf-8"):
            raise SystemExit(f"Stale or missing generated file: {name}")
    print(f"{sum(levels.values())} canonical entries {dict(sorted(levels.items()))}")
    print(f"Source accounting {dict(sorted(counts.items()))}")
    print(f"{len(generated)} deterministic files and {targets} distinct local link targets")


if __name__ == "__main__":
    main()
