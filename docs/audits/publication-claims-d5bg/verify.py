"""Validate D5BG tracked text and exercise four failure modes. Read-only."""

import argparse
import copy
import csv
import json
from collections import Counter
from pathlib import Path, PurePosixPath


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STATUSES = ("READY", "READY — QUALIFIED", "ACTION REQUIRED",
            "MAINTAINER DECISION", "HISTORICAL ONLY")
EDGE_STATES = {"READY", "CONDITIONAL", "HELD", "CONTEXT"}
B4 = "docs/audits/publication-readiness-b4/claim-evidence.csv"
D5AX = "docs/audits/publication-architecture-d5ax/claim-evidence-dependencies.csv"
ASSETS = "docs/audits/release-assets-d5bf/release-assets.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def index(rows, kind, errors):
    result = {}
    for row in rows:
        key = row["id"]
        if key in result:
            errors.append(f"duplicate {kind} {key}")
        result[key] = row
    return result


def exact_file(source):
    relative = PurePosixPath(source)
    if relative.is_absolute() or ".." in relative.parts or "\\" in source:
        return False
    path = ROOT
    for part in relative.parts:
        if not path.is_dir() or part not in {child.name for child in path.iterdir()}:
            return False
        path /= part
    return path.is_file()


def check(matrix, graph, ledger):
    errors = []
    claims = index(matrix["claims"], "claim", errors)
    edges = index(graph["edges"], "edge", errors)
    actions = index(ledger["actions"], "action", errors)
    historic = {row["id"] for row in read_csv(ROOT / B4)}
    ax_rows = read_csv(ROOT / D5AX)
    ax_keys = {(row["claim"], row["node"]) for row in ax_rows}
    topics = {path.stem for path in (ROOT / "docs/guides").glob("*.md")}
    topics -= {"README", "AUTHORING-STANDARD"}
    b1 = {row["id"]: row["claim"] for row in read_csv(ROOT / B4)}
    if matrix["historical_labels"] != b1:
        errors.append("B1/B4 crosswalk differs from B4 IDs and labels")
    if {key for row in claims.values() for key in row["historical"]} != historic:
        errors.append("B4 claim coverage mismatch")
    if {key for row in claims.values() for key in row["topics"]} != topics:
        errors.append("subsystem topic coverage mismatch")
    if any(not exact_file(f"docs/reference/{topic}.md") for topic in topics):
        errors.append("missing reference pair")
    for row in claims.values():
        if row["id"] in historic and row["id"] not in row["historical"]:
            errors.append(f"historical ID lacks own join {row['id']}")
    if historic - claims.keys():
        errors.append("historical IDs lack primary rows")
    for source in {p for row in (*claims.values(), *edges.values(), *actions.values())
                   for p in row["sources"]}:
        if not exact_file(source):
            errors.append(f"missing or incorrectly cased source {source}")

    reached = set()
    selected = set()

    def visit(key, chain):
        if key not in edges:
            errors.append(f"missing dependency {key}")
            return set()
        if key in chain:
            errors.append(f"dependency cycle {key}")
            return set()
        edge = edges[key]
        if edge["materiality"] == "SUPPORTING":
            for child in edge["requires"]:
                visit(child, chain | {key})
            reached.add(key)
            return set()
        branch = {key}
        for child in edge["requires"]:
            branch.update(visit(child, chain | {key}))
            if child in edges and edges[child]["materiality"] != "INDISPENSABLE":
                errors.append(f"indispensable edge requires supporting edge {child}")
        reached.update(branch)
        return branch

    for key, row in claims.items():
        for field in ("proposition", "basis", "pins", "confidence", "coverage",
                      "limits", "wording", "sources", "edges"):
            if not row[field]:
                errors.append(f"empty {field} in {key}")
        status = row["status"]
        if status not in STATUSES:
            errors.append(f"invalid disposition {key}")
        branch = set()
        for edge_id in row["edges"]:
            branch.update(visit(edge_id, set()))
        if status != "HISTORICAL ONLY":
            selected.update(branch)
        ready = branch and all(edges[item]["state"] == "READY" for item in branch)
        if (status in STATUSES[:2] and not ready
                or status == "ACTION REQUIRED" and ready):
            errors.append(f"contradictory disposition {key}")
        if status in STATUSES[2:4] and not any(key in a["claims"] for a in actions.values()):
            errors.append(f"missing decision or closure action {key}")

    for key, edge in edges.items():
        if edge["state"] not in EDGE_STATES:
            errors.append(f"invalid edge state {key}")
        materiality = edge["materiality"]
        if (materiality not in {"INDISPENSABLE", "SUPPORTING"}
                or materiality == "INDISPENSABLE" and edge["state"] == "CONTEXT"):
            errors.append(f"invalid materiality {key}")
        if edge.get("asset"):
            asset = read_json(ROOT / ASSETS)["assets"].get(edge["asset"], {})
            if (edge["state"] != "CONDITIONAL" or edge.get("hosting") != "PENDING RELEASE"
                    or asset.get("hosted_url") != "PENDING RELEASE"
                    or asset.get("proposed_release_eligibility") != "APPROVED FOR PROPOSED RELEASE"
                    or edge.get("sha256") != asset.get("sha256")):
                errors.append(f"pending candidate incorrectly represented {key}")
        for prior in edge.get("predecessors", []):
            if tuple(prior) not in ax_keys:
                errors.append(f"unknown D5AX join {prior} in {key}")
    if edges.keys() - reached:
        errors.append(f"orphan evidence edges {sorted(edges.keys() - reached)}")
    for key, action in actions.items():
        if set(action["claims"]) - claims.keys() or set(action["edges"]) - edges.keys():
            errors.append(f"unknown claim or edge in action {key}")
        if not all(action[field] for field in ("gap", "choices", "acceptance", "sources")):
            errors.append(f"missing action detail {key}")
    counts = {
        "claims": dict(Counter(row["status"] for row in claims.values())),
        "selected_indispensable": dict(Counter(edges[key]["state"] for key in selected)),
        "all_indispensable": dict(Counter(edge["state"] for edge in edges.values()
                                          if edge["materiality"] == "INDISPENSABLE")),
        "historical_only_indispensable": dict(Counter(edges[key]["state"]
                                                      for key in reached - selected
                                                      if edges[key]["materiality"] == "INDISPENSABLE")),
    }
    if matrix["counts"] != counts:
        errors.append("recorded counts differ from unique graph counts")
    return errors, counts


def negative_controls(matrix, graph, ledger):
    def repeat(change, expected):
        inputs = copy.deepcopy((matrix, graph, ledger))
        change(*inputs)
        errors, _ = check(*inputs)
        if not any(expected in item for item in errors):
            raise SystemExit(f"negative control failed to reject {expected}")
        print(f"REJECTED {expected}")

    def add_missing(m, g, a):
        m["claims"][0]["edges"].append("NONEXISTENT")

    def mark_hosted(m, g, a):
        next(edge for edge in g["edges"] if edge.get("asset"))["hosting"] = "HOSTED"

    def duplicate_claim(m, g, a):
        m["claims"].append(m["claims"][0])

    def promote_held(m, g, a):
        next(row for row in m["claims"] if row["status"] == "ACTION REQUIRED")["status"] = "READY"

    repeat(add_missing, "missing dependency")
    repeat(mark_hosted, "pending candidate incorrectly represented")
    repeat(duplicate_claim, "duplicate claim")
    repeat(promote_held, "contradictory disposition")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    data = [read_json(HERE / name) for name in ("claims.json", "evidence-edges.json", "actions.json")]
    errors, counts = check(*data)
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps(counts, ensure_ascii=True, sort_keys=True))
    if args.negative_controls:
        negative_controls(*data)


if __name__ == "__main__":
    main()
