# SPDX-License-Identifier: GPL-3.0-or-later
"""Check the exact supplied B2 event projection, offline with Python stdlib.

Reads only the supplied ZIP. Writes no files, opens no native inputs and
performs no original-stream authentication. See the D5BO schema and audit.
"""

import argparse
from collections import Counter, defaultdict
import hashlib
from io import BytesIO
import json
from pathlib import Path
import zipfile


SCHEMA = "sor-d5bo-b2/1"
MEMBERS = ("manifest.json", "events.json")
RECORDS = 32141
MAX_MEMBER = 8_000_000
TARGET = (0, 37536, 20928, 0x29D20E)
QUERIES = ((4, -1), (5, 0))
BASE = "sequence kind ticks thread epoch hazards status invocation parent selection owner source frame x y".split()
EXTRA = {
    1: ("loss",), 2: (), 3: ("visited", "token", "loss"),
    4: ("slot", "capacity", "key", "current_epoch", "zero_source_copy"),
    5: ("descriptor_delta",), 6: ("body", "geographic_arg"),
    7: ("mask", "sample_arg"), 8: (), 9: (),
    10: ("fence",), 11: ("fence",),
    12: ("visited_control", "visited_data_present", "loss"), 13: (),
    14: ("grid", "token", "copied_token", "loss", "geography", "target_parts"),
    15: ("grid", "valid_destination", "grid_index"),
    16: ("index", "before_control", "after_control"),
    17: ("token", "loss", "base_delta"),
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, separators=(",", ":"), sort_keys=True) + "\n").encode("ascii")


def load_asset(path, expected_sha):
    with path.open("rb") as stream:
        data = stream.read(MAX_MEMBER + 1)
    return unpack_asset(data, expected_sha)


def unpack_asset(data, expected_sha):
    require(len(data) <= MAX_MEMBER and digest(data) == expected_sha, "PACKAGE_DIGEST")
    with zipfile.ZipFile(BytesIO(data)) as archive:
        require(tuple(archive.namelist()) == MEMBERS, "MEMBER_ROSTER")
        require(all(info.file_size <= MAX_MEMBER for info in archive.infolist()), "MEMBER_SIZE")
        manifest_bytes, event_bytes = (archive.read(name) for name in MEMBERS)
    manifest = json.loads(manifest_bytes)
    require(manifest["schema"] == SCHEMA and manifest["records"] == RECORDS, "MANIFEST_SCHEMA")
    require(manifest["omitted_frames"] == 0, "OMISSION_ACCOUNTING")
    require(manifest["events"] == {"bytes": len(event_bytes), "sha256": digest(event_bytes)}, "EVENT_DIGEST")
    return manifest, json.loads(event_bytes)


def before(a, b):
    return a["ticks"] < b["ticks"] or (
        a["ticks"] == b["ticks"] and a["thread"] == b["thread"] and a["sequence"] < b["sequence"]
    )


def decode(rows):
    require(isinstance(rows, list) and len(rows) == RECORDS, "FRAME_CENSUS")
    events = []
    for sequence, row in enumerate(rows, 1):
        require(isinstance(row, list) and len(row) >= len(BASE), "ROW_SCHEMA")
        require(type(row[1]) is int and row[1] in EXTRA and row[0] == sequence, "FRAME_SEQUENCE")
        fields = (*BASE, *EXTRA[row[1]])
        require(len(row) == len(fields), "ROW_SCHEMA")
        for name, value in zip(fields, row):
            if name == "target_parts":
                require(value is None or (isinstance(value, list) and len(value) == 8
                                          and all(type(v) is int for v in value)), "GEOGRAPHY_SCHEMA")
            else:
                require(type(value) is int, "ROW_SCHEMA")
        events.append(dict(zip(fields, row)))
    return events


def fence_audit(kinds):
    active, cold, resets, clears = {}, {}, [], []
    epoch = 1
    last_increment = None
    for e in sorted(kinds[10] + kinds[11] + kinds[12], key=lambda e: e["sequence"]):
        kind = e["kind"]
        if kind == 12:
            key = e["thread"], e["owner"], 0
            require(key in active and key not in cold and e["hazards"] == 1
                    and not (e["visited_control"] or e["visited_data_present"] or e["loss"])
                    and e["epoch"] == epoch and before(active[key], e), "COLD_WITNESS")
            cold[key] = e
            continue
        fence = e["fence"]
        require(fence in (0, 3) and e["owner"] > 0, "UNEXPECTED_LIFECYCLE")
        key = e["thread"], e["owner"], fence
        if kind == 10 or fence != 0:
            epoch += 1
            require(last_increment is None or last_increment["ticks"] < e["ticks"], "INCREMENT_ORDER")
            last_increment = e
        require(e["epoch"] == epoch, "EPOCH_ACCOUNTING")
        if kind == 10:
            require(not active and e["hazards"] == 1, "FENCE_BEGIN")
            active[key] = e
        else:
            require(key in active and e["hazards"] == 0 and before(active[key], e), "FENCE_PAIR")
            begin = active.pop(key)
            if fence == 0:
                require(key in cold and before(cold[key], e), "RESET_TRIAD")
                resets.append((begin, cold.pop(key), e))
            else:
                clears.append((begin, e))
    require(not active and not cold and epoch == 225 and len(resets) == 2 and len(clears) == 111,
            "FENCE_CENSUS")
    return resets, clears, epoch


def geography(parts):
    mode, world, x, y, tile_x, tile_y, fine_x, fine_y = parts
    return mode, x * 192 + tile_x * 12 + fine_x, y * 192 + tile_y * 12 + fine_y, world


def verify_rows(manifest, rows):
    require(manifest["recorded_transport"] ==
            {"durable": RECORDS, "drops": 0, "faults": 0, "loss_generation": 0},
            "TRANSPORT_ACCOUNTING")
    require(manifest["claim_tier"] == "bounded-recorded-event" and
            manifest["native_required"] == ["locked insertion between miss and generation"] and
            manifest["unproved"] == ["cold-first", "lock-acquisition times", "scheduler cause",
                                     "complete geometry", "population frequency"], "CLAIM_BOUNDARY")
    events = decode(rows)
    kinds, invocations, contexts = defaultdict(list), defaultdict(list), defaultdict(list)
    births, pubs, accesses = defaultdict(list), defaultdict(list), defaultdict(list)
    for e in events:
        kind = e["kind"]
        require(e["status"] == 0 and e.get("loss", 0) == 0, "RECORD_STATUS_OR_LOSS")
        require(kind in (10, 11, 12) or e["hazards"] == 0, "RECORD_HAZARD")
        kinds[kind].append(e)
        if e["invocation"]:
            invocations[e["invocation"]].append(e)
            contexts[e["invocation"], e["selection"]].append(e)
        if kind == 14:
            births[e["source"]].append(e)
        if kind == 15:
            pubs[e["source"]].append(e)
        if kind == 4:
            accesses[e["key"]].append(e)
            require(e["zero_source_copy"] == 1, "LOOKUP_SOURCE_COPY")
    require(len(kinds[13]) == 1 and events[0]["kind"] == 13, "READY_BOUNDARY")
    resets, clears, final_epoch = fence_audit(kinds)
    inversions = sum(a["ticks"] > b["ticks"] for a, b in zip(events, events[1:]))
    by_kind = {}
    for kind in (1, 2, 3, 9):
        key = ((lambda e: e["invocation"]) if kind in (1, 9)
               else (lambda e: (e["invocation"], e["selection"])))
        by_kind[kind] = {key(e): e for e in kinds[kind]}
        require(len(by_kind[kind]) == len(kinds[kind]), "AMBIGUOUS_SELECTION_CENSUS")
    require(by_kind[2].keys() == by_kind[3].keys(), "UNKNOWN_SELECTION_CENSUS")

    target_births = [e for e in kinds[14] if e["target_parts"] is not None]
    require(len(target_births) == 8 and all(geography(e["target_parts"]) == TARGET for e in target_births),
            "TARGET_GEOGRAPHY")
    contender_sources = [events[sequence - 1]["source"] for sequence in (8006, 8020)]
    require(contender_sources[0] == contender_sources[1], "COMPETING_SOURCE")
    matching_births = [e for e in target_births if e["source"] == contender_sources[0]]
    require(len(matching_births) == 1, "SOURCE_ALLOCATION")
    birth = matching_births[0]
    source, token, epoch = (birth[name] for name in ("source", "token", "epoch"))
    require(source > 0 and token > 0 and birth["selection"] > 0 and birth["copied_token"] == token
            and births[source] == [birth] and
            sum(e["selection"] == birth["selection"] for e in kinds[14]) == 1,
            "SOURCE_ALLOCATION")
    require([e for e in kinds[14] if e["geography"] == birth["geography"]] == target_births
            and all(e["token"] == token and e["copied_token"] == token for e in target_births)
            and all(e["epoch"] < epoch and before(e, birth) and
                    any(before(e, start) and before(end, birth) for start, end in clears)
                    for e in target_births if e is not birth), "EARLIER_SOURCE_CONTROLS")
    require(len(pubs[source]) == 1, "SOURCE_PUBLICATION")
    publication = pubs[source][0]
    require(before(birth, publication) and publication["thread"] == birth["thread"]
            and publication["grid"] == birth["grid"] > 0 and publication["valid_destination"] == 1
            and publication["epoch"] == epoch and publication["selection"] == 0, "SOURCE_PUBLICATION")
    require(all(e["source"] == source or e["token"] != token for e in kinds[3]
                if e["epoch"] == epoch), "TOKEN_COLLISION")

    selected = [e for e in kinds[2] if e["source"] == source]
    visits = [e for e in kinds[3] if e["source"] == source]
    require(len(selected) == len(visits) == 392, "TARGET_DECISION_CENSUS")
    require({(e["invocation"], e["selection"]) for e in selected} ==
            {(e["invocation"], e["selection"]) for e in visits}, "TARGET_SELECTION_COVERAGE")
    def context(visit):
        key = visit["invocation"], visit["selection"]
        parts = contexts[key]
        selection = [e for e in parts if e["kind"] == 2]
        whole = invocations[key[0]]
        entries = [e for e in whole if e["kind"] == 1]
        returns = [e for e in whole if e["kind"] == 9]
        require(len(entries) == len(selection) == len(returns) == 1 and
                sum(e["kind"] == 3 for e in parts) == 1, "INVOCATION_CONTEXT")
        entry, chosen, returned = entries[0], selection[0], returns[0]
        require(all(before(a, b) for a, b in zip([publication, entry, chosen, visit],
                                                 [entry, chosen, visit, returned])),
                "SELECTION_ORDER")
        require(all(e["epoch"] == epoch and e["owner"] == visit["owner"] > 0
                    and all(e[k] == visit[k] for k in ("thread", "parent", "x", "y"))
                    for e in (entry, returned, *parts)), "OWNER_EPOCH_OR_REQUEST")
        require(all(e["source"] == source and e["frame"] == visit["frame"] > 0
                    for e in parts if e["kind"] != 9), "SOURCE_OR_FRAME")
        require(visit["token"] == token and visit["visited"] in (0, 1), "VISITED_TOKEN")
        return entry, parts, returned

    outcomes = [e for e in visits if e["visited"] == 0]
    require(len(outcomes) == 2, "UNVISITED_CENSUS")
    earlier, later = sorted(outcomes, key=lambda e: e["ticks"])
    require(tuple((e["x"], e["y"]) for e in (earlier, later)) == QUERIES and
            (earlier["sequence"], later["sequence"]) == (8006, 8020), "CONTENDER_REQUESTS")
    require(earlier["owner"] == later["owner"], "COMPETING_OWNER")
    entry_a, path_a, return_a = context(earlier)
    entry_b, path_b, return_b = context(later)
    require([e["kind"] for e in path_a if e["kind"] != 9] == [2, 3, 4] and
            [e["kind"] for e in path_b if e["kind"] != 9] == [2, 3, 4, 5, 6, 7, 8, 16, 17],
            "CONSTRUCTION_BOUNDARIES")
    hit = path_a[2]
    miss, descriptor, generating, sample, generated, reserve, store = path_b[2:9]
    require(accesses[source] == [miss, hit] and
            [e for e in kinds[4] if e["source"] == source] == [miss, hit], "MAP_KEY_OR_COMPETITOR")
    require(all(e["current_epoch"] == epoch for e in (hit, miss)), "LOOKUP_EPOCH")
    require(miss["slot"] == miss["capacity"] and 0 <= hit["slot"] < hit["capacity"],
            "MAP_MISS_HIT")
    for lookup in kinds[4]:
        visit = by_kind[3].get((lookup["invocation"], lookup["selection"]))
        require(visit is not None and visit["visited"] == 0 and before(visit, lookup)
                and all(lookup[k] == visit[k] for k in
                        ("owner", "source", "frame", "thread", "parent", "x", "y", "epoch"))
                and lookup["key"] == lookup["source"] > 0
                and lookup["current_epoch"] == lookup["epoch"]
                and 0 <= lookup["slot"] <= lookup["capacity"], "LOOKUP_CONTEXT_OR_KEY")
    order = [earlier, later, miss, descriptor, generating, sample, generated, reserve, store, hit]
    require(all(before(a, b) for a, b in zip(order, order[1:])) and
            before(hit, return_a) and before(store, return_b), "PROTECTED_NATIVE_ORDER")
    other_a = [e for e in invocations[earlier["invocation"]] if e not in path_a
               and e["kind"] not in (1, 9)]
    other_b = [e for e in invocations[later["invocation"]] if e not in path_b
               and e["kind"] not in (1, 9)]
    require([e["kind"] for e in other_a] == [2, 3] and not other_b
            and other_a[0]["source"] == other_a[1]["source"] != source
            and other_a[0]["selection"] == other_a[1]["selection"] == return_a["selection"]
            and other_a[1]["visited"] == 1 and before(hit, other_a[0])
            and before(other_a[0], other_a[1]) and before(other_a[1], return_a)
            and not any(e["parent"] in (earlier["invocation"], later["invocation"]) for e in kinds[1]),
            "CONTENDER_CONTEXT")
    require(by_kind[1].keys() == by_kind[9].keys(), "RETURN_CENSUS")
    last_selection = {e["invocation"]: e for e in kinds[2]}
    for invocation, returned in by_kind[9].items():
        entry = by_kind[1][invocation]
        last = last_selection.get(invocation, entry)
        require(before(last, returned)
                and all(returned[k] == last[k] for k in ("selection", "source", "frame"))
                and all(returned[k] == entry[k] for k in ("owner", "thread", "parent", "x", "y", "epoch")),
                "RETURN_CONTEXT")
    require(descriptor["descriptor_delta"] == 0xC8 and generating["body"] == 0x5E0DE
            and generating["geographic_arg"] == sample["sample_arg"] > 0 and sample["mask"] == 3,
            "DESCRIPTOR_GENERATOR_SAMPLE")
    index = reserve["index"]
    pre = reserve["before_control"]
    post = reserve["after_control"]
    require(index == (pre & 0xFFFFFFFF) and index + 1 == (post & 0xFFFFFFFF) <= post >> 32
            and index <= pre >> 32 and store["base_delta"] == 8 * index
            and store["token"] == token, "RESERVE_OR_STORE")
    for visit in visits:
        context(visit)
        require(visit["owner"] == later["owner"], "TARGET_OWNER")
        if visit["visited"]:
            require(before(store, visit), "PRIOR_OR_UNORDERED_BYPASS")

    last_visit = max(visits, key=lambda e: e["ticks"])
    require(all(before(end, birth) or
                all(before(e, start) for e in (last_visit, return_a, return_b))
                for start, end in clears + [(start, end) for start, _, end in resets]),
            "INTERVENING_LIFECYCLE")
    uncertain = []
    for key, visit in by_kind[3].items():
        entry = by_kind[1].get(visit["invocation"])
        chosen = by_kind[2][key]
        require(entry is not None and before(entry, chosen) and before(chosen, visit)
                and all(entry[name] == chosen[name] == visit[name]
                        for name in ("thread", "parent", "owner", "epoch", "x", "y"))
                and all(chosen[name] == visit[name] for name in ("source", "frame")),
                "RECORDED_SELECTION_CONTEXT")
        possible = [b for b in births[visit["source"]] if before(b, entry)]
        latest = max(possible, key=lambda b: b["ticks"], default=None)
        if (latest is None or latest["epoch"] != visit["epoch"] or
                latest["token"] != visit["token"] or latest["copied_token"] != visit["token"] or
                not any(p["epoch"] == latest["epoch"] and p["grid"] == latest["grid"] and
                        p["thread"] == latest["thread"] and p["valid_destination"] == 1 and
                        before(latest, p) and before(p, entry) for p in pubs[visit["source"]])):
            uncertain.append(visit)
    require(len(uncertain) == 56 and
            all(before(hit, e) and e["source"] != source and e["token"] != token and e["visited"] == 1
                for e in uncertain), "UNQUALIFIED_DECISION_HISTORY")
    anchor = [end for _, _, end in resets if end["epoch"] == 113]
    require(len(anchor) == 1 and anchor[0]["owner"] == later["owner"] and
            all(end["epoch"] != epoch for _, _, end in resets), "COLD_FIRST_CERTIFICATE")
    first = min(kinds[1], key=lambda e: e["ticks"])
    intervening = [(start, end) for start, end in clears
                   if before(anchor[0], start) and before(end, first)]
    require(epoch == 207 and first["epoch"] == epoch and first["owner"] == later["owner"]
            and len(intervening) == 47 and epoch - anchor[0]["epoch"] == 2 * len(intervening)
            and not any(not before(e, anchor[0]) and not before(first, e)
                        for e in kinds[4] + kinds[16] + kinds[17]), "CARRIED_EMPTY_INTERVAL")
    require(inversions == 97, "ADMISSION_INVERSIONS")
    return {
        "frames": len(events), "kind_counts": dict(sorted(Counter(e["kind"] for e in events).items())),
        "admission_qpc_inversions": inversions, "birth": birth["sequence"],
        "publication": publication["sequence"], "allocation": birth["selection"],
        "earlier_matching_geography_token_births": [e["sequence"] for e in target_births if e is not birth],
        "entry": [entry_a["sequence"], entry_b["sequence"]],
        "unvisited": [earlier["sequence"], later["sequence"]],
        "miss": miss["sequence"], "hit": hit["sequence"], "sample": sample["sequence"],
        "mask": sample["mask"], "store": store["sequence"], "later_bypasses": len(visits) - 2,
        "other_source_selection": [e["sequence"] for e in other_a],
        "other_key_map_decisions": len(kinds[4]) - len(accesses[source]),
        "late_unqualified_decisions": [e["sequence"] for e in uncertain],
        "resets": [[start["sequence"], cold["sequence"], end["sequence"]] for start, cold, end in resets],
        "grid_clears": len(clears), "grid_clears_113_to_207": len(intervening),
        "first_entry": first["sequence"], "increments": final_epoch - 1,
        "cold_first": "refused: no same-owner epoch-207 reset triad and earlier eligible decision",
        "native_required": manifest["native_required"], "unproved": manifest["unproved"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset", type=Path)
    parser.add_argument("--sha256", required=True, help="exact candidate digest from the tracked audit")
    args = parser.parse_args()
    try:
        manifest, rows = load_asset(args.asset, args.sha256)
        print(json.dumps(verify_rows(manifest, rows), indent=2))
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as error:
        parser.exit(1, f"B2 refusal: {error}\n")


if __name__ == "__main__":
    main()
