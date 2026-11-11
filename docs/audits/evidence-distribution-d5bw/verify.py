"""Check D5BW metadata against pinned project records. Reads text and writes stdout."""
import argparse
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STATUS = "NOT READY / NOT CLEARED"
GROUPS = {
    "B4-F1-CORE": "B4-F1-CORE", "B4-F1-ADDENDUM": "B4-F1-ADDENDUM",
    "D5AS": "D5AS", "C19": "C19", "D5BH": "D5BH-EPISODE",
    "D5BI": "D5BI-N2", "D5BO": "D5BO-B2",
}
CUSTODY_DIRS = {
    "B4-F1-CORE": "b4-f1/packages", "B4-F1-ADDENDUM": "b4-f1/packages",
    "D5AS": "d5be/d5as-build02", "C19": "d5be/c19/rebuild-1",
    "D5BH": "d5bh/candidate-v1", "D5BI": "d5bi/candidate01", "D5BO": "d5bo",
}
CONTEXT_PATHS = {
    "WORKSHOP-BASELINE": "workshop-inventory/final05/mature-Save52.json",
    "WORKSHOP-TYPED": "workshop-population-rework/typed-full03/mature-Save52.json",
    "WORKSHOP-ALLA": "workshop-population-rework/specialist/alla-global01.json",
    "WORKSHOP-CANONICAL": "workshop-population-rework/canonical-candidates01.json",
    "CARGO-C3": "d5bu/c3-recovered/save01.json",
}
CONTEXTS = {
    "WORKSHOP-BASELINE": ("P-ROOT-COUNTS", "--root-context BASELINE"),
    "WORKSHOP-TYPED": ("P-ROOT-COUNTS", "--root-context TYPED"),
    "WORKSHOP-ALLA": ("P-ROOT-COUNTS", "--root-context ALLA"),
    "WORKSHOP-CANONICAL": ("P-ROOT-COUNTS", "--canonical-context"),
    "CARGO-C3": ("S-C23-SAVE52", "--c3-context"),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    def unique(pairs):
        result = dict(pairs)
        require(len(result) == len(pairs), "duplicate JSON key")
        return result

    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned(record):
    path = ROOT / record["path"]
    require(digest(path) == record["sha256"], f"source pin: {path.name}")
    return path


def member_records(path, pointer):
    if pointer is None:
        require(path.name == "b2-asset.md", "unexpected Markdown member index")
        text = path.read_text(encoding="utf8")
        return {
            name: {"bytes": int(size.replace(",", "")), "sha256": sha}
            for name, size, sha in re.findall(
                r"\| \x60(\w+\.json)\x60 \| ([\d,]+) \| \x60([a-f0-9]{64})", text
            )
        }
    data = load(path)
    for token in pointer[1:].split("/"):
        data = data[token]
    return data


def read_constants(path, names):
    source = ast.parse(path.read_text(encoding="utf8"))
    return {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in source.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names
    }


def validate(assets, access):
    require(assets["publication"] == access["publication"] == STATUS, "publication status")
    require(assets["selected_routes_source"]["path"] == "docs/audits/evidence-closure-d5bv/routes.json",
            "current route source")
    bv = load(pinned(assets["selected_routes_source"]))
    require(set(assets["assets"]) == set(GROUPS), "seven exact group IDs")
    for group, expected_id in GROUPS.items():
        row = assets["assets"][group]
        expected = bv["assets"][expected_id]
        require(row["d5bv_asset"] == expected_id, f"{group} upstream identity")
        require(row["disposition"] == "PROPOSE INCLUDE" and row["availability"] == "LOCAL ONLY",
                f"{group} authority")
        for field in ("basename", "bytes", "sha256", "member_count", "claims"):
            require(type(row[field]) is type(expected[field]) and row[field] == expected[field],
                    f"{group} {field}")
        require(row["local_candidate_path"] == f".local-work/{CUSTODY_DIRS[group]}/{row['basename']}",
                f"{group} custody locator")
        index = row["member_index"]
        require({k: index[k] for k in ("path", "sha256")} == expected["member_index"],
                f"{group} member index identity")
        pointer = f"/assets/{group}/members" if group in {"B4-F1-CORE", "B4-F1-ADDENDUM", "D5AS", "C19"} else "/members"
        if group == "D5BO":
            pointer = None
        require(index["json_pointer"] == pointer, f"{group} member index selector")
        members = member_records(pinned(index), pointer)
        require(type(row["reviewed_members"]) is int
                and len(members) == row["reviewed_members"] == expected["member_count"], f"{group} coverage")
        require(all(type(x["bytes"]) is int and x["bytes"] > 0
                    and re.fullmatch("[a-f0-9]{64}", x["sha256"]) for x in members.values()),
                f"{group} member pin")
        for name in ("review", "prior_assessment"):
            require((HERE / row[name]).is_file(), f"{group} review pointer")
        if group.startswith("B4-"):
            require(all(not name.startswith("B4-F061/") and
                        PurePosixPath(name).name == member["original_basename"]
                        for name, member in members.items()), f"{group} original basename or donor")
        else:
            require(bool(row["direct_reconstruction"]), f"{group} reconstruction disposition")

    for key in ("selected_routes", "selected_claim_route_pairs"):
        require(type(access[key]) is int and access[key] == bv["counts"][key], key)
    require(set(access["contexts"]) == set(CONTEXTS), "context IDs")
    require(set(access["affected_routes"]) == {row[0] for row in CONTEXTS.values()}, "affected routes")
    bu = load(ROOT / "docs/audits/original-save-verification-d5bu/routes.json")
    for route, row in access["affected_routes"].items():
        require(row["claims"] == list(bv["routes"][route]["claims"]), f"{route} claim joins")
        require(row["contexts"] == [key for key, value in CONTEXTS.items() if value[0] == route],
                f"{route} context joins")
        require(row["status"] == "LOCAL QUALIFICATION RETAINED; HOLD INDEPENDENT ACCESS",
                f"{route} access status")
        if route == "P-ROOT-COUNTS":
            require(row["reader_mode"] == "roots", f"{route} reader mode")
            require(row["fallback_route"] == "P-ROOT-TABLE"
                    and "C17-ROOT-TABLE" in bv["routes"][row["fallback_route"]]["claims"],
                    f"{route} fallback")
        else:
            require(row["fallback_claims"] == ["B4-C09", "B4-C23", "B4-C23-PRIVATE-COMPARATORS"]
                    and all(claim in bv["claims"] for claim in row["fallback_claims"]), f"{route} fallback")
        require(row["reader"] == bu["routes"][route]["reader"]["path"]
                and row["reader_sha256"] == bu["routes"][route]["reader"]["sha256"]
                and digest(ROOT / row["reader"]) == row["reader_sha256"], f"{route} reader pin")
    roots = read_constants(ROOT / access["affected_routes"]["P-ROOT-COUNTS"]["reader"],
                           {"ROOT_RECEIPTS", "CANONICAL_CONTEXT"})
    cargo = read_constants(ROOT / access["affected_routes"]["S-C23-SAVE52"]["reader"], {"C3_CONTEXT"})
    pins = dict(zip(CONTEXTS, (*roots["ROOT_RECEIPTS"], roots["CANONICAL_CONTEXT"], cargo["C3_CONTEXT"]),
                    strict=True))
    for identifier, (route, operand) in CONTEXTS.items():
        row = access["contexts"][identifier]
        require(row["route"] == route and row["operand"] == operand, f"{identifier} route or operand")
        require(row["local_path"] == f".local-work/{CONTEXT_PATHS[identifier]}",
                f"{identifier} custody locator")
        require(type(row["bytes"]) is int and (row["bytes"], row["sha256"]) == pins[identifier],
                f"{identifier} reader input pin")
        require(row["availability"] == "SECURED LOCALLY; INDEPENDENT ACCESS UNESTABLISHED",
                f"{identifier} access status")
    other = access["other_prerequisites"]
    d5ag = other["d5ag_native"]
    require(d5ag["route"] == "P-AG-FIXTURE" and d5ag["standalone_asset_route"] == "D5BF-D5AS"
            and d5ag["standalone_asset_route"] in bv["routes"][d5ag["route"]]["requires"],
            "conditional native asset dependency")
    require(d5ag["standalone_witness_route"] == "P-AS-BODIES"
            and "D5AS-BODY" in bv["routes"][d5ag["standalone_witness_route"]]["claims"],
            "standalone geometry witness")
    require(d5ag["contract"] == "docs/audits/public-evidence-d5bo/d5ag-reader.md"
            and (ROOT / d5ag["contract"]).is_file()
            and d5ag["availability"] == "CONDITIONAL ON LAWFUL MATCHING GAME FILES AND HOST",
            "conditional native contract and status")
    d5bd = other["d5bd_historical"]
    require(d5bd["edition"] == "research/function-catalogue/editions/d5bd.json"
            and d5bd["exact_rebuild_action"] == "D5BD-FROZEN-REBUILD"
            and d5bd["exact_rebuild_action"] in bv["actions"], "historical rebuild contract")
    require(d5bd["availability"] == "LOCAL OBJECT CONFIRMED; PUBLIC REACHABILITY UNESTABLISHED",
            "historical object access status")
    edition = load(ROOT / d5bd["edition"])
    require(d5bd["routes"] == [k for k, v in bv["routes"].items() if v["d5bs_catalogue_review"]],
            "catalogue route joins")
    require(d5bd["commit"] == edition["revision"] and d5bd["tree"] == edition["tree"],
            "historical object pins")


def verify_local_custody(assets, access):
    """Stream the approved, metadata-validated local paths and compare their identities."""
    rows = [(row["local_candidate_path"], row) for row in assets["assets"].values()]
    rows.extend((row["local_path"], row) for row in access["contexts"].values())
    local = (ROOT / ".local-work").resolve(strict=True)
    for relative, row in rows:
        path = (ROOT / relative).resolve(strict=True)
        require(path.is_relative_to(local) and path.is_file(), f"local custody path: {relative}")
        require(path.stat().st_size == row["bytes"], f"local custody size: {relative}")
        with path.open("rb") as stream:
            sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
        require(sha256 == row["sha256"], f"local custody digest: {relative}")


def adverse(assets, access):
    cases = [
        ("dropped asset", lambda a, b: a["assets"].pop("D5BI")),
        ("wrong member index", lambda a, b: a["assets"]["D5BH"]["member_index"].update(sha256="0" * 64)),
        ("false hosting", lambda a, b: a["assets"]["C19"].update(availability="PUBLIC")),
        ("missing canonical", lambda a, b: b["contexts"].pop("WORKSHOP-CANONICAL")),
        ("swapped root operand", lambda a, b: b["contexts"]["WORKSHOP-TYPED"].update(operand="--root-context BASELINE")),
        ("wrong C3 claim", lambda a, b: b["affected_routes"]["S-C23-SAVE52"].update(claims=["B4-C23"])),
        ("wrong C3 size type", lambda a, b: b["contexts"]["CARGO-C3"].update(bytes=3598255.0)),
        ("absent same-basename candidate", lambda a, b: a["assets"]["D5AS"].update(
            local_candidate_path=".local-work/missing/d5as-feynman-geometry-v1.zip")),
        ("absent C3 locator", lambda a, b: b["contexts"]["CARGO-C3"].update(local_path=".local-work/missing/save01.json")),
        ("wrong roots mode", lambda a, b: b["affected_routes"]["P-ROOT-COUNTS"].update(reader_mode="sd2")),
        ("wrong roots fallback", lambda a, b: b["affected_routes"]["P-ROOT-COUNTS"].update(fallback_route="missing")),
        ("wrong native contract", lambda a, b: b["other_prerequisites"]["d5ag_native"].update(contract="missing")),
        ("false historical access", lambda a, b: b["other_prerequisites"]["d5bd_historical"].update(availability="PUBLIC")),
        ("wrong legacy tree", lambda a, b: b["other_prerequisites"]["d5bd_historical"].update(tree="0" * 40)),
    ]
    for label, mutate in cases:
        trial_assets, trial_access = deepcopy(assets), deepcopy(access)
        mutate(trial_assets, trial_access)
        try:
            validate(trial_assets, trial_access)
        except ValueError as error:
            print(f"Rejected {label}: {error}")
        else:
            raise ValueError(f"adverse case accepted: {label}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative-controls", action="store_true")
    parser.add_argument("--local-custody", action="store_true",
                        help="also read and hash the twelve approved local inputs")
    args = parser.parse_args()
    assets = load(HERE / "assets.json")
    access = load(HERE / "access-routes.json")
    validate(assets, access)
    print("Verified seven candidate and five context metadata records.")
    if args.negative_controls:
        adverse(assets, access)
    if args.local_custody:
        verify_local_custody(assets, access)
        print("Verified all twelve local candidate and context byte identities.")


if __name__ == "__main__":
    main()
