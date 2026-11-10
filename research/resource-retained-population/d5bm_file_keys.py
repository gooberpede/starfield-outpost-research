# SPDX-License-Identifier: GPL-3.0-or-later
"""Run bounded original resource-key and file-state controls in a private host.

Original routines are 0x1427d7580, 0x1422cca70 and 0x1427d4be0. The
case-fold helper and state objects are supplied seams. File bytes come from
the pinned ESM/PlanetData/DensityMaps projection. These controls do not run
DensityMapDB acquisition, complete a file load, or establish live readiness.
Invoke only in a separately owned disposable Windows process.
"""
import argparse
import ctypes as C
import json
from pathlib import Path
import shutil
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
import d5bm_files as inputs

CODE = (0x141E9E000, 0x1422CC000, 0x1427D4000, 0x1427D7000)
DATA = (0x144D58000, 0x144D59000)
KEY_ENTRY = 0x1427D7580
CASE_HELPER = 0x141E9EB70
STATE_ENTRY = 0x1427D4BE0
READY = 0x30000002
PENDING = 0x10000002


def key_controls(members):
    convert = host.callsite(KEY_ENTRY, 2, None)
    results = []
    for member in members.values():
        path = member.name.replace("/", "\\")
        values = []
        for spelling in (path, path.upper()):
            out = (C.c_uint32 * 3)()
            raw = C.create_string_buffer(spelling.encode("ascii"))
            convert(C.addressof(out), C.addressof(raw))
            values.append(tuple(out))
        host.require(values[0] == values[1] == member.archive_key,
                     f"Native resource key disagrees with archive record: {member.name}")
        results.append({"name": member.name, "native_key": values[0]})

    original = next(iter(members.values()))
    altered = original.name.removesuffix(".dds").replace("/", "\\") + "_missing.dds"
    out = (C.c_uint32 * 3)()
    raw = C.create_string_buffer(altered.encode("ascii"))
    convert(C.addressof(out), C.addressof(raw))
    host.require(tuple(out) not in {member.archive_key for member in members.values()},
                 "Altered path aliases a selected key")
    return results


def state_controls():
    invoke = C.WINFUNCTYPE(C.c_uint32, C.c_void_p, C.c_uint8)(STATE_ENTRY)
    results = []
    for name, before, expected_result, after in (
        ("supplied ready", READY, 0, READY),
        ("supplied pending", PENDING, 6, 0xA0000002),
    ):
        buffer = C.create_string_buffer(0x30)
        host.put(buffer, 0x14, "<I", before)
        result = invoke(C.addressof(buffer), 0)
        actual, = struct.unpack_from("<I", buffer, 0x14)
        host.require((result, actual) == (expected_result, after), f"Wrong native file-state result: {name}")
        results.append({"input": name, "before": before, "result": result, "after": actual})
    return results


def controls(kernel, pages, members):
    # Canonical path inputs are ASCII. Bind the needed case-table result
    # without entering the original game's CRT TLS or locale initialization.
    fold = C.create_string_buffer(bytes(range(128)).lower())
    host.allocate_pages(kernel, pages)
    try:
        C.memmove(CASE_HELPER, b"\x48\xb8" + struct.pack("<Q", C.addressof(fold)) + b"\xc3", 11)
        for page in pages:
            host.protect(kernel, page, 0x20 if page in CODE else 2)
        host.flush(kernel)
        return key_controls(members), state_controls()
    finally:
        for base in sorted({page & ~0xFFFF for page in pages}, reverse=True):
            host.require(kernel.VirtualFree(base, 0, 0x8000), f"Private release failed at {base:#x}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("exe", "esm", "planet-data", "density-maps"):
        parser.add_argument("--" + argument, required=True, type=Path)
    args = parser.parse_args()
    try:
        kernel, _ = host.host_preflight()
        exe, esm, planet, density = map(host.regular, (args.exe, args.esm, args.planet_data, args.density_maps))
        drives = {Path.cwd().anchor, Path(sys.executable).anchor, *(path.anchor for path in (exe, esm, planet, density))}
        drives.update(drive for drive in ("C:\\", "D:\\") if Path(drive).is_dir())
        host.require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives),
                     "Insufficient disk floor")
        image = host.read_pinned(exe, host.EXE, "Starfield EXE", keep=True)
        _, members = inputs.load(esm, planet, density)
        pages = host.pe_pages(image, CODE, DATA)
        host.cpu_check(kernel)
        keys, states = controls(kernel, pages, members)
        host.read_pinned(exe, host.EXE, "Starfield EXE after file controls")
    except (OSError, ValueError, struct.error, zlib.error) as error:
        parser.exit(1, f"D5BM file controls refused: {error}\n")
    print(json.dumps({
        "scope": "Native path conversion and supplied-object state controls only",
        "exe_sha256": host.EXE,
        "density_maps_sha256": inputs.ARCHIVE,
        "keys": keys,
        "altered_path_refused_by_selected_roster": True,
        "states": states,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
