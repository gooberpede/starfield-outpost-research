# SPDX-License-Identifier: GPL-3.0-or-later
"""Inspect Save52 global-type-3 tail without changing protected input.

Reads the existing policy-pinned controlled copy through owned D5Z methods and
the existing native-backed descriptor framing. Writes only a new ignored local
receipt directory and removes decoder scratch through its context manager.
Dependencies: CPython stdlib and repository-owned save readers; provenance is in
the D5AD source ledger. No game, database, configuration or original-save writes.
The selected-block zlib oracle checks bytes, while native writers/readers justify
the tail grammar. Typed values remain opaque u32, not inferred seeds or floats.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "d5z_save", ROOT / "research/resource-retained-population/d5z_save.py")
D5Z = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D5Z)


def decode_tail(data, offset=0):
    """Two legacy-ID arrays, then typed ID4/subkey2/value4 rows; exact bounds."""
    data = bytes(data)
    cursor = 0

    def take(size):
        nonlocal cursor
        if size < 0 or cursor + size > len(data):
            raise ValueError("TAIL_BOUNDS")
        result = data[cursor:cursor + size]
        cursor += size
        return result

    lists = []
    for name in ("legacy_list_a", "legacy_list_b"):
        count_offset = cursor
        count = int.from_bytes(take(4), "little")
        if count > (len(data) - cursor) // 3:
            raise ValueError("LEGACY_COUNT_BOUNDS")
        tokens = [take(3).hex() for _ in range(count)]
        lists.append(dict(name=name, count=count,
                          count_logical_offset=offset + count_offset,
                          legacy_tokens=tokens))
    count_offset = cursor
    count = int.from_bytes(take(4), "little")
    if count > (len(data) - cursor) // 10:
        raise ValueError("TYPED_COUNT_BOUNDS")
    rows = []
    for ordinal in range(count):
        start = cursor
        token = take(4)
        subkey = int.from_bytes(take(2), "little")
        value = int.from_bytes(take(4), "little")
        rows.append(dict(ordinal=ordinal, logical_offset=offset + start,
                         tagged_id_bytes=token.hex(), subkey_u16=subkey,
                         opaque_value_u32=value))
    if cursor != len(data):
        raise ValueError("TAIL_NOT_EXHAUSTED")
    return dict(lists=lists, typed_count=count,
                typed_count_logical_offset=offset + count_offset,
                typed_rows=rows, tail_bytes=cursor,
                end_logical_offset=offset + cursor)


def controls():
    """Independent struct packing plus wrong-width/count/truncation controls."""
    fixture = (struct.pack("<I", 1) + bytes.fromhex("010203") +
               struct.pack("<II", 0, 1) +
               struct.pack("<IHI", 0x00456789, 2, 0xabcdef01))
    result = decode_tail(fixture, 100)
    expected = struct.unpack_from("<IHI", fixture, 15)
    row = result["typed_rows"][0]
    if (result["lists"][0]["legacy_tokens"] != ["010203"] or
            row["logical_offset"] != 115 or
            (int.from_bytes(bytes.fromhex(row["tagged_id_bytes"]), "little"),
             row["subkey_u16"], row["opaque_value_u32"]) != expected):
        raise RuntimeError("POSITIVE_FIXTURE_MISMATCH")
    empty = decode_tail(struct.pack("<III", 0, 0, 0))
    if empty["typed_count"] != 0 or empty["tail_bytes"] != 12:
        raise RuntimeError("EMPTY_FIXTURE_MISMATCH")
    cases = dict(truncated=fixture[:-1], trailing=fixture + b"\0",
                 bad_list_count=struct.pack("<I", 0xffffffff) + fixture[4:],
                 bad_typed_count=fixture[:11] + struct.pack("<I", 2) + fixture[15:],
                 typed_id_wrong_width=fixture[:18] + fixture[19:])
    rejected = {}
    for name, value in cases.items():
        try:
            decode_tail(value)
        except ValueError as exc:
            rejected[name] = str(exc)
        else:
            raise RuntimeError("NEGATIVE_ACCEPTED:" + name)
    return dict(positive_nonempty=True, positive_empty=True,
                independent_struct_oracle=True, rejected=rejected)


def main():
    if sys.flags.optimize:
        raise RuntimeError("OPTIMIZATION_NOT_ALLOWED")
    out = Path(sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT / ".local-work") or out.exists():
        raise ValueError("FRESH_LOCAL_OUTPUT_REQUIRED")
    D5Z.guard()
    fixture_result = controls()
    out.mkdir(parents=True)
    # -E prevents inherited PYTHONOPTIMIZE from disabling the owned reader guards.
    subprocess.run([sys.executable, "-E", "-B", str(Path(D5Z.__file__)),
                    str(out / "prefix")], cwd=ROOT, check=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)
    prefix = json.loads((out / "prefix/save-prefix.json").read_text())
    source = Path(prefix["source"])
    before = D5Z.sha(source)
    start = prefix["world_descriptor_end"]
    length = prefix["remaining_unit3_bytes"]
    independent = D5Z.independent_slice(source, start, length)
    with D5Z.decoded_save(source, out / "scratch", seconds=float("inf"),
                          guard=D5Z.guard) as (buffer, metrics):
        selected = bytes(buffer[start:start + length])
        if selected != independent:
            raise RuntimeError("DECODER_DISAGREEMENT")
        result = decode_tail(selected, start)
        # A separate struct walk challenges the manual-width parser on real bytes.
        typed_start = result["typed_count_logical_offset"] - start + 4
        oracle = list(struct.iter_unpack("<IHI", selected[typed_start:]))
        manual = [(int.from_bytes(bytes.fromhex(row["tagged_id_bytes"]), "little"),
                   row["subkey_u16"], row["opaque_value_u32"])
                  for row in result["typed_rows"]]
        if oracle != manual:
            raise RuntimeError("STRUCT_ORACLE_DISAGREEMENT")
    after = D5Z.sha(source)
    if before != after or before != prefix["source_sha256"]:
        raise RuntimeError("PROTECTED_IDENTITY_CHANGED")
    if any((out / "scratch").iterdir()):
        raise RuntimeError("SCRATCH_REMAINS")
    receipt = dict(schema="sor-d5ad-save-tail/1", source=str(source),
                   source_bytes=source.stat().st_size, source_sha256=before,
                   source_unchanged=True, decoded_sha256=metrics["decoded_sha256"],
                   tail_sha256=hashlib.sha256(selected).hexdigest(),
                   script_sha256=D5Z.sha(__file__), inherited_reader_sha256=D5Z.sha(D5Z.__file__),
                   independent_selected_block_match=True, independent_struct_match=True,
                   controls=fixture_result, result=result,
                   scope="Native-backed type-3 tail grammar only; opaque typed values, no live-ID remap or runtime activation claim")
    (out / "save-tail.json").write_text(json.dumps(receipt, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    print(json.dumps({k: receipt[k] for k in
                     ("source_sha256", "tail_sha256", "source_unchanged", "controls")}, indent=2))
    print("typed_count", result["typed_count"], "tail_bytes", length,
          "end_logical_offset", hex(result["end_logical_offset"]))


if __name__ == "__main__":
    main()
