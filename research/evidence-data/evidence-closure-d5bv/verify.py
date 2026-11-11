"""Validate the D5BV current view using only repository text and metadata."""

import argparse
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "archival"))
from sources import edition, historical_pin_bytes


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AUDITS = ROOT / "docs/audits"
DATA = HERE.parent
BG = AUDITS / "publication-claims-d5bg"
BR = AUDITS / "evidence-readiness-d5br" / "readiness.json"
BU = AUDITS / "original-save-verification-d5bu"
BT = AUDITS / "reader-qualification-d5bt"
BS = AUDITS / "native-function-catalogue-d5bs"
BT_ROUTES = {"S-P1-S29-ORIGINAL", "S-SD1-H21"}
SELECTED_REPLACEMENTS = {
    "C06-CENSUS": {"D5BF-CORE", "P-FAB-0036"},
    "C14-CENSUS": {"D5BF-CORE", "P-SHARED-CORE-CENSUS", "P-SHARED-ORIGINALS", "P-SHARED-STATIC"},
    "C18-FULL-CONTROLS": {"D5BF-CORE", "P-POSITION-CORE", "P-POSITION-METHOD"},
    "C19-D1-SAVED": {"P-D1-SITE-TABLE"},
}
SUPERSEDED_PINS = {
    ("P-FAB-0036", "save-analysis/scripts/verify_d5bu_fabricators.py"): (
        "df0a1b72d235ed684b4cfbf1930aadd017694fc6bde78bd95ee4053e4e09432a",
        "5e67d9d1a1319c54c9003e14db4f0893762f1ae20e3137f16ffed8f10d79dafc",
        BU / "whitespace-correction.md",
    ),
    ("S-P1-S29-ORIGINAL", "research/p1-power/saved_instances.py"): (
        "cff89cb5385e2d8665ac38e01a7dd57e95a7b8aee97f975931f9ef55d97abf35",
        "844a164609a07c4e3086d36d9ac577ba0c79eab42a3725b25a10abc0627c2ebe",
        BT / "provenance.md",
    ),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = dict(pairs)
    require(len(result) == len(pairs), "duplicate JSON key")
    return result


def read(path):
    return json.loads(historical_pin_bytes(path.relative_to(ROOT).as_posix()),
                      object_pairs_hook=unique_object)


def digest(path):
    return hashlib.sha256(historical_pin_bytes(path.relative_to(ROOT).as_posix())).hexdigest()


def pin(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}


def check_source_pin(route_id, path, expected_hash):
    actual = digest(ROOT / path)
    if actual == expected_hash:
        return None
    require((route_id, path) in SUPERSEDED_PINS, f"{route_id}: unknown pin delta {path}")
    old, new, record = SUPERSEDED_PINS[(route_id, path)]
    require((old, new) == (expected_hash, actual), f"{route_id}: evidence pin {path}")
    return {"prior": old, "current": new, "record": pin(record)}


def indexed(path, field):
    rows = read(path)[field]
    result = {row["id"]: row for row in rows}
    require(len(result) == len(rows), f"duplicate ID in {path.name}")
    return result


def closure(edges, route_ids, parents=frozenset()):
    result = set(route_ids)
    require(not (result & parents), "dependency cycle")
    for route_id in route_ids:
        result.update(closure(edges, edges[route_id]["requires"], parents | {route_id}))
    return result


def source_graph(br):
    claims = indexed(BG / "claims.json", "claims")
    actions = indexed(BG / "actions.json", "actions")
    edges = indexed(BG / "evidence-edges.json", "edges")
    require((len(claims), len(actions), len(edges)) == (71, 31, 110), "inherited counts")
    require(set(actions) == set(br["inherited_action_ids"]), "inherited action IDs")
    for materiality, ids in br["inherited_edge_ids_by_materiality"].items():
        require(set(ids) == {k for k, v in edges.items() if v["materiality"] == materiality},
                f"inherited {materiality} edge IDs")
    for row in br["source_ledgers"]:
        require(digest(ROOT / row["path"]) == row["sha256"], f"ledger drift: {row['path']}")
    inherited = {row["id"]: row for row in br["claims"]}
    require(len(br["claims"]) == len(inherited) and claims.keys() == inherited.keys(),
            "inherited claim IDs")
    joins = defaultdict(list)
    for claim_id, row in inherited.items():
        require(row["status"] == claims[claim_id]["status"], f"{claim_id}: claim status")
        require(set(row["inherited_roots"]) == set(claims[claim_id]["edges"]),
                f"{claim_id}: inherited roots")
        require(set(row["inherited_action_ids"]) ==
                {k for k, a in actions.items() if claim_id in a["claims"]},
                f"{claim_id}: inherited actions")
        selected = row["selected_routes"]
        require(len(selected) == len(set(selected)), f"{claim_id}: duplicate route")
        require(closure(edges, selected) == set(selected), f"{claim_id}: selected dependency omitted")
        replacements = set(selected) - closure(edges, claims[claim_id]["edges"])
        require(replacements == SELECTED_REPLACEMENTS.get(claim_id, set()),
                f"{claim_id}: unexpected selection outside inherited closure")
        for route_id in selected:
            joins[route_id].append(claim_id)
    require((len(joins), sum(map(len, joins.values()))) == (68, 126), "selected counts")
    return claims, actions, edges, inherited, joins


def asset_projection(br, routes):
    assets = {}
    for asset_id, asset in br["assets"].items():
        ledger = ROOT / asset["ledger"]
        require(digest(ledger) == asset["ledger_sha256"], f"{asset_id}: asset ledger drift")
        selected_claims = {
            claim_id for route in routes.values() if asset_id in route["members_by_asset"]
            for claim_id in route["claims"]
        }
        assets[asset_id] = {
            **{k: asset[k] for k in ("basename", "bytes", "sha256", "member_count")},
            "member_index": pin(ledger),
            "claims": sorted(selected_claims),
            "availability": "PENDING RELEASE",
        }
    require(len(assets) == 7, "seven asset groups required")
    return assets


def claim_projection(inherited, routes):
    result = {}
    for index, (claim_id, row) in enumerate(inherited.items()):
        selected = row["selected_routes"]
        result[claim_id] = {
            "selection_record": f"/claims/{index}",
            "inherited_status": row["status"],
            "inherited_root_edges": row["inherited_roots"],
            "inherited_action_ids": row["inherited_action_ids"],
            "selected_tier": row["tier"],
            "selected_routes": selected,
            "verified_original_routes": [k for k in selected if routes[k]["d5bu_evidence_record"]],
            "deferred_exact_routes": row["deferred_exact_routes"],
            "support_only_dependencies": row["support_only_dependencies"],
            "supporting_routes": row["supporting_routes"],
            "release_disposition": "PENDING CANDIDATE REVIEW",
        }
    return result


def action_projection(actions, claim_views, edges):
    result = {}
    for action_id, action in actions.items():
        claim_routes = {}
        for claim_id in action["claims"]:
            claim = claim_views[claim_id]
            claim_routes[claim_id] = {
                "selected_routes": claim["selected_routes"],
                "verified_original_routes": claim["verified_original_routes"],
                "selected_action_edges": [k for k in action["edges"] if k in claim["selected_routes"]],
                "deferred_action_edges": [k for k in action["edges"] if k in claim["deferred_exact_routes"]],
                "support_only_action_edges": [
                    k for k in action["edges"]
                    if k in claim["support_only_dependencies"] or k in claim["supporting_routes"]
                ],
                "selected_tier": claim["selected_tier"],
            }
        result[action_id] = {
            "inherited_kind": action["kind"],
            "inherited_edges": {k: edges[k]["state"] for k in action["edges"]},
            "claim_routes": claim_routes,
            "item7_disposition": "Confirm selected tier, resolve access and clearance, and freeze for B6.",
        }
    return result


def selected_route(route_id, row, edges, actions, inherited, claim_ids, original, receipt_pins):
    edge = edges[route_id]
    require(edge["materiality"] == "INDISPENSABLE", f"{route_id}: materiality")
    require(all(row[k] == edge[k] for k in ("state", "materiality", "requires")),
            f"{route_id}: inherited edge")
    prerequisites = sorted(closure(edges, edge["requires"]))
    members = row["members_by_asset"]
    pins = row["qualification_sources"] + row["method_pins"] + row.get("import_pins", [])
    if original:
        require(original["status"] == "verified original check", f"{route_id}: D5BU status")
        require(sorted(original["claims"]) == claim_ids, f"{route_id}: D5BU claim join")
        require(sorted(original["requires"]) == sorted(edge["requires"]) and
                sorted(original["transitive_requires"]) == prerequisites and
                original["members"] == members, f"{route_id}: D5BU operand join")
        require(all(original["claims"][k] == inherited[k]["inherited_action_ids"]
                    for k in claim_ids), f"{route_id}: D5BU action join")
        require(original["receipts"] and all(
            receipt_pins.get(r["locator"]) == r["sha256"] for r in original["receipts"]
        ), f"{route_id}: D5BU receipt index join")
        pins = pins + [original["reader"]]
    pin_deltas = {}
    for source in pins:
        path = source["path"]
        delta = check_source_pin(route_id, path, source["sha256"])
        if delta:
            pin_deltas[path] = delta
    if original:
        local = "VERIFIED AT SELECTED ORIGINAL TIER"
        conditions = f"D5BU batch {original['batch']} in methods.md; see item7-handoff.md"
    elif route_id == "P-AG-FIXTURE":
        local = "PRIOR QUALIFICATION ON COMPATIBLE HOST"
        conditions = row["requirements"]
    else:
        local = "PRIOR SELECTED TIER QUALIFICATION"
        conditions = row["requirements"]
    return {
        "claims": {
            k: {"inherited_status": inherited[k]["status"], "selected_tier": inherited[k]["tier"],
                "inherited_action_ids": inherited[k]["inherited_action_ids"],
                "relation": ("Inherited root" if route_id in inherited[k]["inherited_roots"]
                             else "Selected prerequisite" if any(
                                 route_id in closure(edges, edges[other]["requires"])
                                 for other in inherited[k]["selected_routes"])
                             else "Selected replacement root")}
            for k in claim_ids
        },
        "edge_state": edge["state"],
        "materiality": edge["materiality"],
        "inherited_edge_action_ids": sorted(k for k, a in actions.items() if route_id in a["edges"]),
        "prior_d5br_disposition": row["disposition"],
        "requires": edge["requires"],
        "transitive_requires": prerequisites,
        "modality": {
            "S-P1-S29-ORIGINAL": "Original SFS ordered electrical graph reader",
            "S-SD1-H21": "Original SFS component reader",
        }.get(route_id, row["reader_type"]),
        "members_by_asset": members,
        "local_qualification": local,
        "prior_evidence_record": f"/route_records/{route_id}",
        "d5bu_evidence_record": f"/routes/{route_id}" if original else None,
        "d5bt_reader_review": route_id in BT_ROUTES,
        "d5bs_catalogue_review": route_id.startswith("G-CATALOGUE-"),
        "source_pin_deltas": pin_deltas,
        "portability_and_execution_conditions": conditions,
        "d5bv_execution": "METADATA ONLY",
        "rights_privacy": "PENDING CANDIDATE REVIEW",
        "transfer_retention": "PENDING APPROVAL" if members else "NO DIRECT ASSET",
        "frozen_candidate_b6": "PENDING",
        "hosting_byte_verification": "PENDING RELEASE" if members else "NO DIRECT ASSET",
        "final_publication_authorization": "PENDING",
        "next_action": "Item 7. Bind approved evidence and method to freeze and independent B6.",
        "further_local_verification_at_selected_tier": "NONE IDENTIFIED",
    }


def expected():
    br = read(BR)
    bu = read(BU / "routes.json")
    receipt_pins = read(BU / "receipts.json")["local_receipt_sha256"]
    bu_sources = read(BU / "source-manifest.json")["current_project_source_sha256"]
    claims, actions, edges, inherited, joins = source_graph(br)
    require(bu["crosswalk_sha256"] == digest(BR), "D5BU input crosswalk pin")
    original_ids = {k for k in joins if br["route_records"][k]["disposition"] != "READY FOR B6"}
    blocked_ids = {k for k in joins if br["route_records"][k]["disposition"] == "BLOCKED"}
    require(blocked_ids == BT_ROUTES, "D5BT routes differ from the two D5BR barriers")
    require(original_ids == set(bu["routes"]) == set(bu["verified_original_route_ids"]) and
            len(original_ids) == bu["original_route_count"] == 14 and
            bu["release_routes_closed"] == 0, "D5BU selected IDs/count or release drift")
    require(len(bu_sources) == 44, "D5BU source closure count")
    for path, expected_hash in bu_sources.items():
        check_source_pin("P-FAB-0036", path, expected_hash)
    routes = {
        k: selected_route(k, br["route_records"][k], edges, actions, inherited,
                          sorted(joins[k]), bu["routes"].get(k), receipt_pins)
        for k in sorted(joins)
    }
    outside_selection = set(edges) - routes.keys()
    claim_views = claim_projection(inherited, routes)
    return {
        "schema": "sor-d5bv-current-evidence/1",
        "publication": "NOT READY / NOT CLEARED",
        "sources": {
            "d5br": pin(BR),
            "d5br_review": pin(BR.with_name("review.md")),
            "d5bu": pin(BU / "routes.json"),
            "d5bu_review": pin(BU / "review.md"),
            "d5bu_receipts": pin(BU / "receipts.json"),
            "d5bu_source_manifest": pin(BU / "source-manifest.json"),
            "d5bt_review": pin(BT / "review.md"),
            "d5bt_provenance": pin(BT / "provenance.md"),
            "d5bs_review": pin(BS / "review.md"),
        },
        "counts": {
            "inherited_claims": len(claims),
            "inherited_actions": len(actions),
            "inherited_edges": len(edges),
            "inherited_claim_statuses": dict(sorted(Counter(c["status"] for c in claims.values()).items())),
            "selected_routes": len(routes),
            "selected_claim_route_pairs": sum(len(r["claims"]) for r in routes.values()),
            "d5br_import_pin_relationships": sum(
                len(br["route_records"][k].get("import_pins", [])) for k in joins
            ),
            "d5bu_project_source_pins": len(bu_sources),
            "local_qualifications": dict(sorted(Counter(r["local_qualification"] for r in routes.values()).items())),
            "outside_selected_inventory": len(outside_selection),
            "release_routes_cleared": 0,
        },
        "unselected_held_edges": sorted(k for k in outside_selection if edges[k]["state"] == "HELD"),
        "claims": claim_views,
        "actions": action_projection(actions, claim_views, edges),
        "assets": asset_projection(br, routes),
        "routes": routes,
    }


def validate(actual, reference):
    require(isinstance(actual, dict) and actual.keys() == reference.keys(),
            "unexpected top-level schema")
    for section, expected_value in reference.items():
        actual_value = actual[section]
        if section == "routes":
            require(isinstance(actual_value, dict) and actual_value.keys() == expected_value.keys(),
                    "selected route IDs differ")
            for route_id, row in expected_value.items():
                require(same_json(actual_value[route_id], row), f"route differs: {route_id}")
        else:
            require(same_json(actual_value, expected_value), f"{section} differs")


def same_json(actual, expected):
    # Serialization preserves JSON types even where Python considers them equal.
    return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)


def negative_controls(reference):
    def missing_route(data):
        data["routes"].pop("P-BIOME-METHOD")

    def wrong_claim(data):
        data["routes"]["S-SD1-H21"]["claims"]["B4-C21-SAVE29-ORIGINAL"] = {}

    def hosted(data):
        data["assets"]["C19"]["availability"] = "HOSTED"

    def release(data):
        data["routes"]["P-BIOME-METHOD"]["final_publication_authorization"] = "CLEARED"

    def historical(data):
        data["unselected_held_edges"].remove("S-P1-THREE-LOADS")
        data["routes"]["S-P1-THREE-LOADS"] = data["routes"]["S-P1-S29-ORIGINAL"]

    def asset(data):
        data["routes"]["P-AG-FIXTURE"]["members_by_asset"] = {}

    def dependency(data):
        data["routes"]["P-BIOME-ORIGINALS"]["transitive_requires"].remove("P-BIOME-METHOD")

    def shared_edge_leakage(data):
        claim = data["actions"]["DECIDE-D5AQ-EXACT-FIXTURE"]["claim_routes"]["D5AQ-EXACT-FIXTURE"]
        claim["deferred_action_edges"].remove("P-AO-N2")
        claim["selected_action_edges"].append("P-AO-N2")

    def numeric_review_flag(data):
        data["routes"]["S-P1-S29-ORIGINAL"]["d5bt_reader_review"] = 1

    def boolean_release_count(data):
        data["counts"]["release_routes_cleared"] = False

    def floating_route_count(data):
        data["counts"]["selected_routes"] = 68.0

    for mutate in (missing_route, wrong_claim, hosted, release, historical, asset, dependency,
                   shared_edge_leakage, numeric_review_flag, boolean_release_count, floating_route_count):
        changed = copy.deepcopy(reference)
        mutate(changed)
        try:
            validate(changed, reference)
        except ValueError as error:
            print(f"PASS rejected {mutate.__name__}: {error}")
        else:
            raise ValueError(f"accepted negative control: {mutate.__name__}")


def main():
    edition()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    reference = expected()
    validate(read(AUDITS / "evidence-closure-d5bv/routes.json"), reference)
    print("PASS: 71 claims, 31 actions, 110 edges, 68 selected routes, 126 joins, zero release clearances")
    if args.negative_controls:
        negative_controls(reference)


if __name__ == "__main__":
    main()
