# SPDX-License-Identifier: GPL-3.0-or-later
"""Corroborate Save52's native-backed context/body join against installed PNDT.

Reads an explicitly selected D5Z prefix receipt, the policy-pinned controlled
Save52 copy, and an explicitly supplied pinned Starfield.esm. The existing owned
ESM walker and packed-key decoder supply framing/arithmetic; native evidence is
in the D5AD source ledger. Writes a fresh ignored receipt directory only.
Dependencies: CPython stdlib and repository-owned modules. No game, database,
configuration, protected original or save-copy writes. C:/D: free-space guards
remain active; pre/post hashes protect the selected input identities.
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
from planet_world_key import qualified_grid, unit3_world_descriptors

SPEC = importlib.util.spec_from_file_location(
    "d5z_save", ROOT / "research/resource-retained-population/d5z_save.py")
D5Z = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D5Z)


def sha(path):
    """Hash through fixed-size reads without changing the input file."""
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            result.update(block)
    return result.hexdigest()


def main():
    if sys.flags.optimize:
        raise RuntimeError("OPTIMIZATION_NOT_ALLOWED")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--esm", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(ROOT / ".local-work") or out.exists():
        raise ValueError("FRESH_LOCAL_OUTPUT_REQUIRED")
    D5Z.guard()
    prefix_before = sha(args.prefix)
    prefix = json.loads(args.prefix.read_text())
    save = Path(prefix["source"])
    policy = ROOT / "research/resource-carinae-source-context/save_policy.json"
    designated = json.loads(policy.read_text())["designated"]
    name = next(name for name in designated if name.startswith("Save52_"))
    expected_save = designated[name]
    expected_path = (ROOT / ".local-work/savegames" / name).resolve()
    if save.resolve() != expected_path:
        raise ValueError("CONTROLLED_COPY_PATH_MISMATCH")
    save_before = sha(save)
    if (save_before != expected_save["sha256"] or
            save.stat().st_size != expected_save["bytes"] or
            prefix["source_sha256"] != save_before):
        raise ValueError("SAVE52_PIN_MISMATCH")
    esm_before = sha(args.esm)
    if esm_before != "1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7":
        raise ValueError("ESM_PIN_MISMATCH")
    context = prefix["context"]
    payload = D5Z.independent_slice(save, context["start"], context["length"])
    if int.from_bytes(payload[:8], "little") != prefix["key_u64"]:
        raise ValueError("PREFIX_KEY_MISMATCH")
    descriptors, end = unit3_world_descriptors(
        payload, dict(start=0, length=len(payload), strings=context["strings"]))
    if end + context["start"] != prefix["world_descriptor_end"]:
        raise ValueError("DESCRIPTOR_BOUNDARY_MISMATCH")
    for row, old in zip(descriptors, prefix["world_descriptors"], strict=True):
        if (row["body"], row["key"], row["world_token"]) != (
                old["body"], old["key"], old["world_token"]):
            raise ValueError("DESCRIPTOR_RECEIPT_MISMATCH")
    bodies = {}
    for record, fields in esm_records(args.esm, {b"PNDT"}):
        gnam = fields.get(b"GNAM", b"")
        if len(gnam) == 12:
            system, orbital, index = struct.unpack("<III", gnam)
            bodies[record["formid"]] = dict(
                system_id=system, body_index=index,
                editor_id=fields.get(b"EDID", b"").rstrip(b"\0").decode(),
                record_offset=record["offset"])
    decoded = qualified_grid(prefix["key_u64"])
    matches = [dict(formid=f"{fid:08x}", **row) for fid, row in bodies.items()
               if (row["system_id"], row["body_index"]) ==
               (decoded["system_id"], decoded["body_index"])]
    if len(matches) != 1 or matches[0]["editor_id"] != "JemisonPlanetData":
        raise ValueError("CONTEXT_BODY_MISMATCH")
    rows = []
    for descriptor in descriptors:
        body = bodies[int(descriptor["body"], 16)]
        if (body["system_id"], body["body_index"]) != (
                descriptor["system_id"], descriptor["body_index"]):
            raise ValueError("DESCRIPTOR_BODY_MISMATCH")
        rows.append(dict(ordinal=descriptor["ordinal"], body=descriptor["body"],
                         installed_gnam_match=True))
    if (sha(args.esm) != esm_before or sha(save) != save_before or
            sha(args.prefix) != prefix_before):
        raise RuntimeError("INPUT_CHANGED")
    D5Z.guard()
    receipt = dict(schema="sor-d5ad-save-body/1", esm_sha256=esm_before,
                   prefix_receipt_sha256=prefix_before, save_sha256=save_before,
                   context_decoded=decoded, context_installed_body=matches[0],
                   descriptor_rows=rows, descriptor_count=len(rows),
                   independent_source_payload_match=True, inputs_unchanged=True,
                   method_sha256=sha(__file__), methods={
                       str(path.relative_to(ROOT)): sha(path) for path in (
                           Path(D5Z.__file__),
                           ROOT / "save-analysis/scripts/inspect_outpost_definitions.py",
                           ROOT / "save-analysis/scripts/planet_world_key.py")},
                   scope="Saved context/body identity only; no runtime demand or selected loaded-frame claim")
    out.mkdir(parents=True)
    (out / "body-check.json").write_text(json.dumps(receipt, indent=2) + "\n",
                                        encoding="utf-8", newline="\n")
    print(json.dumps({key: receipt[key] for key in
                     ("context_installed_body", "descriptor_count", "inputs_unchanged")}, indent=2))


if __name__ == "__main__":
    main()
