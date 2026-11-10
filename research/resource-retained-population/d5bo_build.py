# SPDX-License-Identifier: GPL-3.0-or-later
"""Build one local proposed B2 derivative from immutable pinned evidence.

Run with Python -E -B. Reads only listed local originals and repository-owned
D5AC reconstruction, reader and reducer. Writes one new ZIP in local scratch.
No game, saves, network, database, Git or third-party execution. The D5AC
decoder, historical reader and SOR-P-0002 methods supply source provenance.
"""

import argparse
import io
import json
from pathlib import Path
import struct
import zipfile

from d5bo_verify import (BASE, EXTRA, RECORDS, SCHEMA, TARGET, digest, encoded,
                         geography, require, verify_rows)


ROOT = Path(__file__).resolve().parents[2]
SESSION = ROOT / ".local-work/d5x/live/session-5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1"
HISTORICAL = ROOT / ".local-work/d5ab/B2-APPROVED-002-notes/reader.json"
DLL_SHA = "9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc"
PINS = {
    "events.bin": "4a8feb68f667f417967a0cd4a332cefde768658d254ead8d555b3e5f44515218",
    "identity.json": "60ab253002916e04cdce854345dfde49bb539dddea4dcf40f5f690704360beef",
    "ready.json": "08d3c0dc6f8796b5be654052dbb9cf4a8de12d5e42645d91a78aecdd94f183a0",
    "terminal.json": "65e72cc787ea0889a8e5e011ed7f734fb737fff1cd59f54cdd62b999108c3ca4",
    "flush.jsonl": "8d9ddfed0af9f38f10bdaefef2269ade88bbac4c3ce5b564c973bda942cfe16d",
    "historical-reader.json": "95b6a5fdf2d3c84263ffa1cdb8b3d5a058c4fb3d70f61ddfd5ea1444ea7a82a2",
}
METHOD_PINS = {
    "runtime/construction-winner/observer.h":
        "bb5cccce9bd6fd390ee8a892f3403dc854d5ed0e7c9d89e31bd6592fb5dc8cd5",
    "runtime/construction-winner/read_capture.py":
        "645b028a18ff2a2033d68719fe75ac6e9abd81d5f7bd4ccc25deacf9ce758ede",
    "runtime/construction-winner/reduce_v4.py":
        "f3a7e533210f0df9aac166aab49e7c728b830ff392488fa7b970eac8e9366419",
    "research/resource-retained-population/d5ac_reconstruct.py":
        "cd1fdc62975d3e69d3acd0a71e2bcba9324166072d9ca61119a69dab2aaa8c7a",
}


def project(events):
    tables = {}

    def alias(domain, value):
        if not value:
            return 0
        labels = tables.setdefault(domain, {})
        return labels.setdefault(value, len(labels) + 1)

    contexts = {(e["invocation"], e["selection"]): e for e in events if e["kind"] == 16}
    for e in events:
        kind = e["kind"]
        a, b, c, d = (e[k] for k in "abcd")
        receiver = {1: "owner", 2: "map", 3: "grid", 4: "source"}.get(a, "owner") if kind in (10, 11) else "owner"
        row = {
            **e,
            "thread": alias("thread", e["thread"]),
            "owner": alias(receiver, e["proc"]),
            "source": alias("source", e["source"]),
            "frame": alias("frame", e["frame"]),
            "x": e["request"][0],
            "y": e["request"][1],
        }
        if kind == 1:
            row.update(loss=c)
        elif kind == 3:
            row.update(visited=a, token=alias("token", b), loss=c)
        elif kind == 4:
            row.update(slot=a, capacity=b, key=alias("source", c), current_epoch=d,
                       zero_source_copy=int(bytes.fromhex(e["source_bytes"]) == bytes(112)))
        elif kind == 5:
            row.update(descriptor_delta=d - e["holder"])
        elif kind == 6:
            row.update(body=a, geographic_arg=alias("geographic_arg", c))
        elif kind == 7:
            row.update(mask=a, sample_arg=alias("geographic_arg", c))
        elif kind in (10, 11):
            row.update(fence=a)
        elif kind == 12:
            row.update(visited_control=a, visited_data_present=int(bool(b)), loss=c)
        elif kind == 14:
            raw = bytes.fromhex(e["source_bytes"])
            pairs = [value for offset in (60, 76, 92) for value in struct.unpack_from("<ii", raw, offset)]
            parts = [raw[56], struct.unpack_from("<I", raw)[0], *pairs]
            key = geography(parts)
            row.update(grid=alias("grid", e["holder"]), token=alias("token", a),
                       copied_token=alias("token", struct.unpack_from("<Q", raw, 104)[0]), loss=d,
                       geography=alias("geography", key), target_parts=parts if key == TARGET else None)
        elif kind == 15:
            row.update(grid=alias("grid", e["holder"]), valid_destination=int(a >= 0x10000),
                       grid_index=b)
        elif kind == 16:
            row.update(index=a, before_control=b, after_control=c)
        elif kind == 17:
            reserve = contexts[e["invocation"], e["selection"]]
            row.update(token=alias("token", b), loss=c, base_delta=a - reserve["d"])
        yield [row[k] for k in (*BASE, *EXTRA[kind])]


def make_asset():
    for name, pin in METHOD_PINS.items():
        require(digest((ROOT / name).read_bytes()) == pin, f"METHOD_PIN {name}")
    for name, pin in PINS.items():
        path = HISTORICAL if name == "historical-reader.json" else SESSION / name
        require(digest(path.read_bytes()) == pin, f"ORIGINAL_PIN {name}")
    # Admit the exact historical source before its import executes.
    import d5ac_reconstruct as original

    raw = (SESSION / "events.bin").read_bytes()
    events = original.decode_frames(raw)
    reader = original.reader.inspect(SESSION, DLL_SHA)
    require(reader == json.loads(HISTORICAL.read_bytes()) and reader["complete_session"] and
            not reader["damage"] and not reader["chains"] and len(events) == RECORDS, "ORIGINAL_READER")
    terminal = reader["terminal"]
    for field in ("drops", "output_faults", "loss_generation"):
        require(terminal[field] == 0, f"ORIGINAL_TRANSPORT {field}")
    identity = json.loads((SESSION / "identity.json").read_bytes())
    rows = list(project(events))
    event_bytes = encoded(rows)
    manifest = {
        "schema": SCHEMA,
        "claim_tier": "bounded-recorded-event",
        "records": RECORDS,
        "omitted_frames": 0,
        "events": {"bytes": len(event_bytes), "sha256": digest(event_bytes)},
        "original": {"schema": identity["schema"], "frame_bytes": 328, "raw_bytes": len(raw),
                     "qpc_hz": 10_000_000, "sha256": PINS, "exe_sha256":
                     "7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28",
                     "dll_sha256": DLL_SHA},
        "recorded_transport": {"durable": terminal["acknowledged"], "drops": terminal["drops"],
                               "faults": terminal["output_faults"], "loss_generation": terminal["loss_generation"]},
        "native_required": ["locked insertion between miss and generation"],
        "unproved": ["cold-first", "lock-acquisition times", "scheduler cause", "complete geometry",
                     "population frequency"],
    }
    verify_rows(manifest, rows)
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compresslevel=9) as archive:
        for name, data in (("manifest.json", encoded(manifest)), ("events.json", event_bytes)):
            info = zipfile.ZipInfo(name)
            info.create_system = 0
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset", type=Path)
    args = parser.parse_args()
    path = args.asset.resolve()
    require(path.is_relative_to(ROOT / ".local-work/d5bo") and path.suffix == ".zip", "LOCAL_OUTPUT_ONLY")
    data = make_asset()
    with path.open("xb") as stream:
        stream.write(data)
    print(json.dumps({"bytes": len(data), "sha256": digest(data)}))


if __name__ == "__main__":
    main()
