# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise refusals against disposable in-memory variants of the B2 candidate.

Run with Python -E -B. Reads the supplied asset, writes no files and executes
no game or native code. Semantic controls intentionally run below the digest gate.
"""

import argparse
import copy
import json
from pathlib import Path

from d5bo_verify import BASE, EXTRA, load_asset, unpack_asset, verify_rows


def change(rows, seq, field, value):
    row = rows[seq - 1]
    row[(*BASE, *EXTRA[row[1]]).index(field)] = value


def read(rows, seq, field):
    row = rows[seq - 1]
    return row[(*BASE, *EXTRA[row[1]]).index(field)]


def expect(name, reason, run, results):
    try:
        run()
    except ValueError as error:
        if str(error) != reason:
            raise RuntimeError(f"{name}: expected {reason}, got {error}") from error
        results[name] = reason
    else:
        raise RuntimeError(f"{name}: unexpectedly accepted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset", type=Path)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    manifest, rows = load_asset(args.asset, args.sha256)
    positive = verify_rows(manifest, rows)
    results = {}
    changes = (
        ("changed request", 8020, "x", 4, "CONTENDER_REQUESTS"),
        ("changed source", 8020, "source", 99999, "COMPETING_SOURCE"),
        ("changed owner", 8020, "owner", 99999, "COMPETING_OWNER"),
        ("changed epoch", 8091, "current_epoch", 208, "LOOKUP_EPOCH"),
        ("changed visited token", 8020, "token", 99999, "VISITED_TOKEN"),
        ("changed map key", 8091, "key", 99999, "MAP_KEY_OR_COMPETITOR"),
        ("reversed native order", 8339, "ticks", read(rows, 8091, "ticks") - 1, "PROTECTED_NATIVE_ORDER"),
        ("changed miss sentinel", 8091, "slot", 0, "MAP_MISS_HIT"),
        ("competing lookup uses target key", 2473, "key", read(rows, 2074, "source"), "MAP_KEY_OR_COMPETITOR"),
        ("competing lookup uses invalid key", 2473, "key", -1, "LOOKUP_CONTEXT_OR_KEY"),
        ("constructing return uses wrong source", 8110, "source", 99999, "RETURN_CONTEXT"),
        ("losing return omits different source", 8345, "source", read(rows, 2074, "source"), "RETURN_CONTEXT"),
        ("changed publication receiver", 2075, "grid", 99999, "SOURCE_PUBLICATION"),
        ("unexpected retirement", 1730, "fence", 4, "UNEXPECTED_LIFECYCLE"),
        ("broken epoch accounting", 1731, "epoch", 208, "EPOCH_ACCOUNTING"),
        ("broken Cold witness", 882, "visited_data_present", 1, "COLD_WITNESS"),
        ("changed store destination", 8106, "base_delta", 160, "RESERVE_OR_STORE"),
        ("changed sample", 8094, "mask", 0, "DESCRIPTOR_GENERATOR_SAMPLE"),
        ("late unqualified visit relabelled", 31886, "token", read(rows, 2074, "token"),
         "UNQUALIFIED_DECISION_HISTORY"),
    )
    for name, seq, field, value, reason in changes:
        altered = list(rows)
        altered[seq - 1] = rows[seq - 1].copy()
        change(altered, seq, field, value)
        expect(name, reason, lambda: verify_rows(manifest, altered), results)
    expect("earlier contrary event omitted", "FRAME_CENSUS",
           lambda: verify_rows(manifest, rows[:8005] + rows[8006:]), results)
    for claim in ("cold-first", "unique scheduler cause"):
        altered_manifest = copy.deepcopy(manifest)
        altered_manifest["claim_tier"] = claim
        expect(claim, "CLAIM_BOUNDARY", lambda: verify_rows(altered_manifest, rows), results)
    expect("wrong package hash", "PACKAGE_DIGEST", lambda: load_asset(args.asset, "0" * 64), results)
    expect("truncated package", "PACKAGE_DIGEST",
           lambda: unpack_asset(args.asset.read_bytes()[:-1], args.sha256), results)
    print(json.dumps({"positive": positive, "negative": results}, indent=2))


if __name__ == "__main__":
    main()
