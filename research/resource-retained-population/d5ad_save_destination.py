# SPDX-License-Identifier: GPL-3.0-or-later
"""Read Save52's native-backed global-type-9 destination branch prefix.

Reads the existing policy-pinned controlled Save52 copy, the owned save decoder,
and an explicitly supplied pinned Starfield.esm. Writes selected numeric fields,
hashes, controls and limits only to a fresh ignored output directory; temporary
decoded scratch is removed. Stdlib and repository-owned readers only. No game,
database, save/configuration write or original-save restoration. The decoded
initial prefix is not a complete unit-9 decoder or historical execution trace.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "save-analysis/scripts"))
from inspect_outpost_definitions import esm_records
from outpost_membership import token_value
from planet_world_key import qualified_grid

SPEC = importlib.util.spec_from_file_location(
    "d5z_save", ROOT / "research/resource-retained-population/d5z_save.py")
D5Z = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D5Z)


def sha(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            result.update(block)
    return result.hexdigest()


def destination_prefix(data, logical_start=0):
    """Native initial ID3/u32/u32/ID3/XYZ/kind and optional context; no actor."""
    data = bytes(data)
    cursor = 0
    fields = []

    def take(name, size, fmt=None):
        nonlocal cursor
        if cursor + size > len(data):
            raise ValueError("DESTINATION_PREFIX_BOUNDS")
        raw = data[cursor:cursor + size]
        value = struct.unpack(fmt, raw) if fmt else raw.hex()
        if fmt and len(value) == 1:
            value = value[0]
        fields.append(dict(name=name, logical_offset=logical_start + cursor,
                           length=size, value=value))
        cursor += size
        return value

    world = take("saved_world_token", 3)
    grid_x = take("saved_grid_x_u32", 4, "<I")
    grid_y = take("saved_grid_y_u32", 4, "<I")
    destination = take("destination_token", 3)
    xyz = take("saved_local_xyz", 12, "<3f")
    kind = take("has_planet_context", 1, "<B")
    if kind not in (0, 1):
        raise ValueError("CONTEXT_KIND_UNQUALIFIED")
    context = None
    if kind == 1:
        system = take("context_system_id", 4, "<I")
        body_index = take("context_body_index", 4, "<I")
        pair = take("context_pair", 16, "<2d")
        key = take("context_world_key", 8, "<Q")
        context = dict(system_id=system, body_index=body_index, pair=pair,
                       world_key=f"{key:016x}", decoded_world_key=qualified_grid(key))
    actor = take("has_alternate_reference", 1, "<B")
    if actor != 0:
        raise ValueError("ALTERNATE_REFERENCE_BRANCH_NOT_DECODED")
    # Tag01 has direct static saved identity before engine load-order remapping.
    def direct(token):
        value = int(token, 16)
        if value == 0:
            return 0
        if value >> 22 != 1:
            return None
        return value & 0x3fffff
    return dict(fields=fields, saved_world_token=world,
                saved_world_direct_id=direct(world),
                destination_token=destination,
                destination_direct_saved_id=direct(destination),
                grid_u32=[grid_x, grid_y],
                grid_i32=[struct.unpack("<i", struct.pack("<I", value))[0]
                          for value in (grid_x, grid_y)],
                local_xyz=xyz, has_planet_context=kind, context=context,
                has_alternate_reference=actor, prefix_bytes=cursor,
                opaque_tail_bytes=len(data) - cursor,
                opaque_tail_sha256=hashlib.sha256(data[cursor:]).hexdigest())


def fixtures():
    key = 0x022e401882204260
    fixed = (bytes.fromhex("000000") + struct.pack("<II", 0, 0xffffffff) +
             bytes.fromhex("46bb29") + struct.pack("<3f", 1, 2, 3))
    with_context = fixed + b"\1" + struct.pack("<II2dQ", 71456, 3, 2, 4, key) + b"\0"
    without_context = fixed + b"\0\0"
    one, zero = destination_prefix(with_context), destination_prefix(without_context)
    if (one["prefix_bytes"] != 60 or zero["prefix_bytes"] != 28 or
            one["destination_direct_saved_id"] != token_value("46bb29", []) or
            one["grid_i32"] != [0, -1] or one["context"]["system_id"] != 71456):
        raise RuntimeError("POSITIVE_FIXTURE_MISMATCH")
    rejected = {}
    cases = dict(truncated_xyz=fixed[:-1],
                 truncated_context=with_context[:-2],
                 wrong_context_kind=fixed + b"\2\0",
                 alternate_reference=without_context[:-1] + b"\1")
    for name, value in cases.items():
        try:
            destination_prefix(value)
        except ValueError as exc:
            rejected[name] = str(exc)
        else:
            raise RuntimeError("NEGATIVE_ACCEPTED:" + name)
    return dict(context_present=True, context_absent=True,
                independent_saved_token_oracle=True, rejected=rejected)


def main():
    if sys.flags.optimize:
        raise RuntimeError("OPTIMIZATION_NOT_ALLOWED")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--esm", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(ROOT / ".local-work") or out.exists():
        raise ValueError("FRESH_LOCAL_OUTPUT_REQUIRED")
    D5Z.guard()
    policy = ROOT / "research/resource-carinae-source-context/save_policy.json"
    designated = json.loads(policy.read_text())["designated"]
    name = next(name for name in designated if name.startswith("Save52_"))
    source = ROOT / ".local-work/savegames" / name
    before = sha(source)
    if before != designated[name]["sha256"] or source.stat().st_size != designated[name]["bytes"]:
        raise ValueError("SAVE52_PIN_MISMATCH")
    esm_before = sha(args.esm)
    if esm_before != "1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7":
        raise ValueError("ESM_PIN_MISMATCH")
    controls = fixtures()
    out.mkdir(parents=True)
    with D5Z.decoded_save(source, out / "scratch", seconds=float("inf"),
                          guard=D5Z.guard) as (buffer, metrics):
        units = D5Z.global_suffix(buffer, D5Z.directory(buffer))
        start, end = units[9]
        selected = bytes(buffer[start:end])
        if selected != D5Z.independent_slice(source, start, end - start):
            raise RuntimeError("INDEPENDENT_UNIT9_MISMATCH")
        result = destination_prefix(selected, start)
        # Independent fixed-layout extraction checks the actual selected prefix.
        world, gx, gy, dest, x, y, z, kind = struct.unpack_from("<3sII3s3fB", selected)
        if (world.hex(), gx, gy, dest.hex(), (x, y, z), kind) != (
                result["saved_world_token"], *result["grid_u32"],
                result["destination_token"], result["local_xyz"],
                result["has_planet_context"]):
            raise RuntimeError("STRUCT_ORACLE_MISMATCH")
        a7, e7 = units[7]
        try:
            destination_prefix(buffer[a7:min(a7 + 136, e7)])
        except ValueError as exc:
            controls["actual_unit7_negative"] = str(exc)
        else:
            raise RuntimeError("WRONG_GLOBAL_UNIT_ACCEPTED")
    fid = result["destination_direct_saved_id"]
    records, bodies = [], []
    for record, fields in esm_records(args.esm, {b"CELL", b"PNDT"}):
        if record["formid"] == fid:
            records.append(dict(formid=f"{fid:08x}", record_type=record["type"],
                                editor_id=fields.get(b"EDID", b"").rstrip(b"\0").decode(),
                                record_offset=record["offset"], flags=record["flags"],
                                cell_data_hex=fields.get(b"DATA", b"").hex()))
        if record["type"] == "PNDT" and len(fields.get(b"GNAM", b"")) == 12:
            system, orbital, index = struct.unpack("<III", fields[b"GNAM"])
            if result["context"] and (system, index) == (
                    result["context"]["system_id"], result["context"]["body_index"]):
                bodies.append(dict(formid=f"{record['formid']:08x}",
                                   editor_id=fields.get(b"EDID", b"").rstrip(b"\0").decode(),
                                   record_offset=record["offset"]))
    if len(records) != 1 or records[0]["record_type"] != "CELL" or len(bodies) != 1:
        raise RuntimeError("INSTALLED_DESTINATION_NOT_UNIQUE")
    cell_data = bytes.fromhex(records[0]["cell_data_hex"])
    if len(cell_data) not in (2, 4) or not int.from_bytes(cell_data, 'little') & 1:
        raise ValueError("INSTALLED_INTERIOR_DATA_REQUIRED")
    if sha(source) != before or sha(args.esm) != esm_before:
        raise RuntimeError("INPUT_CHANGED")
    if any((out / "scratch").iterdir()):
        raise RuntimeError("SCRATCH_REMAINS")
    receipt = dict(schema="sor-d5ad-save-destination/1", source_sha256=before,
                   decoded_sha256=metrics["decoded_sha256"], esm_sha256=esm_before,
                   unit9=dict(logical_start=start, logical_end=end, length=end-start,
                              sha256=hashlib.sha256(selected).hexdigest()),
                   prefix=result, installed_destination=records[0],
                   installed_context_body=bodies[0], inputs_unchanged=True,
                   independent_selected_block_match=True, independent_struct_match=True,
                   controls=controls, script_sha256=sha(__file__),
                   methods={str(path.relative_to(ROOT)): sha(path) for path in (
                       Path(D5Z.__file__), ROOT / "save-analysis/scripts/outpost_membership.py",
                       ROOT / "save-analysis/scripts/inspect_outpost_definitions.py")},
                   limits="Initial branch prefix only. Saved IDs precede load remapping; successful runtime resolution, loaded globals, execution times and opaque tail remain separate.")
    (out / "destination.json").write_text(json.dumps(receipt, indent=2) + "\n",
                                         encoding="utf-8", newline="\n")
    print(json.dumps({key: receipt[key] for key in
                     ("unit9", "installed_destination", "installed_context_body", "controls")}, indent=2))


if __name__ == "__main__":
    main()
