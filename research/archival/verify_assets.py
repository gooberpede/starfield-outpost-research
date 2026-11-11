# SPDX-License-Identifier: GPL-3.0-or-later
"""Check the relocated asset ledger joins without opening any external evidence."""

from collections import Counter
import json

from sources import edition, historical_pin_bytes, read_current, sha


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def load(relative):
    return json.loads(read_current("research/evidence-data/" + relative))


def main():
    edition()
    historical = load("evidence-closure-d5bv/routes.json")
    distribution = load("evidence-distribution-d5bw/assets.json")
    access = load("evidence-distribution-d5bw/access-routes.json")
    supplements = load("evidence-access-d5bx/assets.json")
    crosswalk = load("evidence-access-d5bx/crosswalk.json")
    require(historical["publication"] == distribution["publication"] == "NOT READY / NOT CLEARED",
            "release status changed")
    require(set(historical["assets"]) == {row["d5bv_asset"] for row in distribution["assets"].values()} and len(historical["assets"]) == 7,
            "candidate identity inventory differs")
    for key, record in distribution["assets"].items():
        selected = historical["assets"][record["d5bv_asset"]]
        require(all(record[field] == selected[field] for field in ("basename", "bytes", "sha256", "member_count")),
                f"candidate identity differs: {key}")
        pin = record["member_index"]
        payload = historical_pin_bytes(pin["path"])
        require(sha(payload) == pin["sha256"], f"member index SHA-256 differs: {key}")
        node = json.loads(payload) if pin["path"].endswith(".json") else None
        if pin.get("json_pointer"):
            for piece in pin["json_pointer"].split("/")[1:]:
                node = node[piece.replace("~1", "/").replace("~0", "~")]
            require(len(node) == record["member_count"], f"member index count differs: {key}")
    require(len(supplements["workshop"]["members"]) == 3 and supplements["cargo"]["reader_operand"] == "--c3-context",
            "supplement contract differs")
    transitions = {
        "workshop": ("P-ROOT-COUNTS", "verify_d5bu_controls.py", "verify_d5bx_workshop.py"),
        "cargo": ("S-C23-SAVE52", "verify_d5bu_cargo.py", "verify_d5bu_cargo.py"),
    }
    require(set(crosswalk["controls"]) == {row[0] for row in transitions.values()},
            "supplement control routes differ")
    prefix = "save-analysis/scripts/"
    for key, (route, original, current) in transitions.items():
        record = supplements[key]
        prior = access["affected_routes"][route]
        require(len(record["sha256"]) == 64 and record["bytes"] > 0, f"bad supplementary pin: {key}")
        require(prior["reader"] == prefix + original and record["reader"] == prefix + current,
                f"reader crosswalk differs: {key}")
        require(sha(historical_pin_bytes(prior["reader"])) == prior["reader_sha256"],
                f"historical reader identity differs: {route}")
        require(record["reader"] in edition()["sources"], f"current reader identity is absent: {route}")
    selected_claims = Counter(route for row in historical["claims"].values() for route in row["selected_routes"])
    require(len(selected_claims) == 68 and sum(selected_claims.values()) == 126, "selected graph counts changed")
    print("PASS: seven candidate identities and member indexes, two supplement contracts and 126 selected joins")


if __name__ == "__main__":
    main()
