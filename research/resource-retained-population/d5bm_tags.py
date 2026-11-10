# SPDX-License-Identifier: GPL-3.0-or-later
"""Run the original C1 BIOM tag map producer from exact main-file rows.

The fixture supplies main-file-only subrecord projection, one owned interned
string object per selected FNAM, and private allocation. It keeps original
map initialization, lookup, insertion, tag selection and GNAM vector growth.
It stops at the live map object used by the native density enumerator.
"""
import argparse
import ctypes as C
import json
import os
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
from d5bm_pool import available_bytes
from d5bm_server import value, write

ROOT = Path(__file__).resolve().parents[2]
CODE = (
    0x1402b7000, 0x1402ba000, 0x1402c5000, 0x1402dc000, 0x140320000, 0x1405b6000,
    0x1405b7000, 0x1422c7000,
    0x1422cb000, 0x1422cc000, 0x1427b1000, 0x1427b2000, 0x1428ca000,
    0x1428cb000, 0x14365c000, 0x143663000,
)
HASH_TABLE = 0x144d58d70
HASH_PAGES = (0x144d58000, 0x144d59000)
DATA = (0x143a3f000, 0x144af7000, *HASH_PAGES, 0x144f04000, 0x145e60000, 0x1461e1000)
WRITABLE = {0x145e60000, 0x1461e1000}
BIOME = 0x00145440
SHAPE = (("Talus", 16), ("FlatOuter", 45), ("Flow", 21), ("FlatInner", 59))
P = C.c_void_p
Q = C.c_uint64
U = C.c_uint32
require = host.require


def verify_hash_table(pages):
    offset = HASH_TABLE - HASH_PAGES[0]
    table = b"".join(pages[page] for page in HASH_PAGES)[offset:offset + 256 * 4]
    expected = []
    for index in range(256):
        for _ in range(8):
            index = (index >> 1) ^ (0xedb88320 if index & 1 else 0)
        expected.append(index)
    require(table == struct.pack("<256I", *expected), "Original BIOM hash table differs or is incomplete")
    return host.digest(table)


def verify_owner_scalar(pages):
    # Original first-GNAM-owner constructor reads 0x144f044e8.
    bits, = struct.unpack_from("<I", pages[0x144f04000], 0x4e8)
    require(bits == 0x3f800000, "Original GNAM owner scalar differs")
    return bits


def load_groups(esm):
    sys.path.insert(0, str(ROOT / "save-analysis/scripts"))
    from inspect_outpost_definitions import esm_records

    esm = host.regular(esm)
    host.read_pinned(esm, host.ESM, "Starfield main ESM")
    candidates = [(header, fields) for header, fields in esm_records(esm, {b"BIOM"}, repeated=True)
                  if header["formid"] == BIOME]
    require(len(candidates) == 1, "Expected one main-file C1 BIOM")
    name = None
    enabled = False
    groups = {}
    for tag, data in candidates[0][1]:
        if tag == b"FNAM":
            require(data.endswith(b"\0") and b"\0" not in data[:-1], "Invalid C1 FNAM")
            name = data[:-1].decode("ascii")
            require(name not in groups, "Repeated C1 FNAM")
            groups[name] = []
            enabled = False
        elif tag == b"BNAM":
            require(len(data) == 4, "Invalid C1 BNAM")
            enabled = struct.unpack("<I", data)[0] != 0
        elif tag == b"GNAM":
            require(name is not None and enabled and len(data) == 0x54, "Invalid C1 GNAM")
            # The main file is the selected namespace. The original loader
            # resolves this first FormID word before calling the publisher.
            formid, = struct.unpack_from("<I", data)
            require(0 < formid < 0x01000000, "GNAM FormID outside the main-file namespace")
            groups[name].append(data)
    require(tuple((name, len(rows)) for name, rows in groups.items()) == SHAPE,
            "Unexpected C1 FNAM/BNAM/GNAM roster")
    host.read_pinned(esm, host.ESM, "Starfield main ESM after tag read")
    return groups


def qualify_main_file(esm, groups):
    """Authenticate the source namespace independently of the native map."""
    from inspect_outpost_definitions import esm_records

    records = esm_records(esm, {b"TES4"}, repeated=True)
    try:
        header, fields = next(records)
    finally:
        records.close()
    require(header["offset"] == 0 and header["formid"] == 0 and header["flags"] == 0x81
            and all(tag != b"MAST" for tag, _ in fields),
            "The remap fixture requires the ordinary main master with no master dependencies")
    selected = {struct.unpack_from("<I", row)[0] for rows in groups.values() for row in rows}
    references = {}
    with esm.open("rb") as source:
        size = os.fstat(source.fileno()).st_size
        at, ends = 0, [size]
        while at < size:
            while len(ends) > 1 and at == ends[-1]:
                ends.pop()
            source.seek(at)
            kind, length, flags, formid = struct.unpack_from("<4sIII", source.read(24))
            end = at + (length if kind == b"GRUP" else length + 24)
            require(at + 24 <= end <= ends[-1], "Selected main master has invalid group bounds")
            if kind == b"GRUP":
                ends.append(end)
                at += 24
                continue
            if formid in selected:
                require(formid not in references and flags == 0 and kind in (b"PKIN", b"LVLP"),
                        "Selected GNAM reference has a duplicate, unexpected type or record flags")
                references[formid] = {"type": kind.decode("ascii"), "offset": at}
            at = end
        require(at == size and all(end == size for end in ends), "Selected main master did not close")
    require(references.keys() == selected, "Selected GNAM reference is absent from the exact main master")
    require(len(references) == 80 and sum(row["type"] == "PKIN" for row in references.values()) == 77,
            "Unexpected selected GNAM reference roster")
    host.read_pinned(esm, host.ESM, "Starfield main ESM after FormID reference walk")
    return references


class NativeTags:
    def __init__(self, kernel, crt):
        self.kernel = kernel
        self.crt = crt
        self.object = C.create_string_buffer(0x80)
        self.owner = C.addressof(self.object)
        self.table = self.owner + 0x18
        self.storage = {}
        self.released = set()
        self.callbacks = []
        self.names = {}
        self.allocation_trace = []

    def buffer(self, size, kind):
        storage = C.create_string_buffer(size + 15)
        pointer = (C.addressof(storage) + 15) & ~15
        self.storage[pointer] = (storage, size, kind)
        self.allocation_trace.append(("allocate", kind, pointer, size))
        return pointer

    def arena(self, owner, size, alignment, enabled):
        require(owner == 0x145e603c0 and size == 8 * 0x18 and alignment == 8 and enabled == 1,
                f"Unexpected tag arena request {size:#x}/{alignment:#x}/{enabled:#x}")
        return self.buffer(size, "buckets")

    def object_allocate(self, size):
        require(size in (0x18, 0x30), "Unexpected tag object size")
        return self.buffer(size, "tag-owner" if size == 0x18 else "gnam-owner")

    def array_allocate(self, size, alignment):
        require(alignment == 8 and 0x40 <= size <= 0x10000 and (size % 0x54 == 0 or size % 0x10 == 0),
                "Unexpected tag array allocation")
        return self.buffer(size, "array")

    def arena_release(self, owner, pointer, enabled):
        require(owner == 0x145e603c0 and enabled == 1, "Unexpected tag arena owner")
        self.release(pointer, "buckets", 8 * 0x18)

    def array_release(self, pointer, size):
        if pointer or size:
            self.release(pointer, "array", size)

    def object_release(self, pointer, size):
        require(size in (0x18, 0x30), "Unexpected tag object release size")
        self.release(pointer, "tag-owner" if size == 0x18 else "gnam-owner", size)

    def release(self, pointer, kind, size):
        require(self.owns(pointer, size, kind) and self.storage[pointer][1] == size, "Unexpected tag release")
        self.released.add(pointer)
        self.allocation_trace.append(("release", kind, pointer, size))

    def owns(self, pointer, size, kind):
        record = self.storage.get(pointer)
        return record is not None and pointer not in self.released and record[1] >= size and record[2] == kind

    def null_intern_release(self, holder):
        require(holder and not value(holder, "<Q"),
                "Non-null intern release requires a qualified native intern-table owner")

    def hook(self, address, result, types, operation):
        def invoke(*arguments):
            try:
                return operation(*arguments)
            except Exception as error:
                print(f"D5BM tag seam stopped: {error}", file=sys.stderr, flush=True)
                os._exit(70)

        function = C.WINFUNCTYPE(result, *types)(invoke)
        self.callbacks.append(function)
        C.memmove(address, b"\x48\xb8" + struct.pack("<Q", C.cast(function, P).value) + b"\xff\xe0", 12)

    def bind(self):
        write(0x145e60398, "<I", 2)
        write(0x145e60840, "<Q", 0)
        write(0x1461e1db0, "<Q", self.owner)
        self.hook(0x1422c7320, P, (Q,), self.object_allocate)
        self.hook(0x1422c7ad0, P, (P, Q, Q, C.c_uint8), self.arena)
        self.hook(0x1422c7d40, None, (P, P, C.c_uint8), self.arena_release)
        self.hook(0x1402ba260, P, (Q, Q), self.array_allocate)
        self.hook(0x1402ba340, None, (P, Q), self.array_release)
        # Sized delete jumps to the real object-free entry with RDX
        # intact. Keep its eight-byte stub and adjacent array destructor.
        require(C.string_at(0x14365cdb0, 8) == bytes.fromhex("e9 ab a7 c6 fe cc cc cc"),
                "Original sized tag delete thunk differs")
        self.hook(0x1422c7560, None, (P, Q), self.object_release)
        self.hook(0x1428caea0, None, (P,), self.null_intern_release)
        host.bind_imports(self.crt, {"memmove": (0x14366317e, 0x143a3fcc0)})

    def effective_row(self, raw, file_ptr, references):
        formid, = struct.unpack_from("<I", raw)
        require(formid in references, "GNAM FormID has no authenticated main record")
        resolved = U(formid)
        # Mirrors the selected 0x1409e0cf0..0x1409e0d3a loader branch.
        if not 1 <= formid <= 0x7ff:
            selected = C.WINFUNCTYPE(P, P, U)(0x1405b62a0)(file_ptr + 0x1e0, formid)
            require(not selected, "GNAM unexpectedly selected a master instead of the source file")
            C.WINFUNCTYPE(None, P, P)(0x1405b78c0)(file_ptr, C.byref(resolved))
        require(resolved.value == formid, "Native remap disagrees with the qualified main-file slot")
        return struct.pack("<I", resolved.value) + raw[4:]

    def lookup(self, biome):
        key = U(biome)
        capacity = value(self.table + 0x18, "<Q")
        buckets = value(self.table + 0x10, "<Q")
        require(capacity == 8 and self.owns(buckets, capacity * 0x18, "buckets"),
                "Native BIOM lookup has no owned buckets")
        index = C.WINFUNCTYPE(Q, P, P)(0x1402dca60)(self.table, C.byref(key))
        if index == capacity:
            return None
        require(index < capacity, "Unexpected native BIOM table index")
        entry = buckets + index * 0x18
        require(value(entry, "<I") == biome, "Native BIOM map returned a different key")
        pointer = value(entry + 8, "<Q")
        require(self.owns(pointer, 0x18, "tag-owner"), "Missing owned tag vector")
        return pointer

    def publish(self, groups, references):
        C.WINFUNCTYPE(P, P)(0x1403206a0)(self.owner + 0x10)
        require(value(self.table + 0x18, "<Q") == 8 and self.lookup(BIOME) is None,
                "Native BIOM table initialization differs")
        publish = C.WINFUNCTYPE(None, P, U, P, P)(0x1427b1a60)
        # Owned, ordinary full master. Flags at +0x1b8, no master table
        # at +0x1e0 and main load index at +0x218. No loaded game state.
        file = C.create_string_buffer(0x220)
        file_ptr = C.addressof(file)
        write(file_ptr + 0x1b8, "<I", 1)
        effective = {name: [self.effective_row(row, file_ptr, references) for row in rows]
                     for name, rows in groups.items()}
        for name, rows in effective.items():
            text = name.encode("ascii") + b"\0"
            string = self.buffer(0x18 + len(text), "intern")
            self.names[string] = name
            write(string + 0x10, "<I", 1)
            C.memmove(string + 0x18, text, len(text))
            holder = Q(string)
            for row in rows:
                record = (C.c_char * 0x54).from_buffer_copy(row)
                publish(self.owner, BIOME, C.byref(holder), record)
        owner = self.lookup(BIOME)
        require(owner is not None and self.lookup(BIOME ^ 1) is None
                and value(owner, "<I") == 1, "Native BIOM map key or ownership differs")
        count = value(owner + 8, "<I")
        entries = value(owner + 0x10, "<Q")
        require(count == len(effective) and self.owns(entries, count * 0x10, "array"),
                "Native tag vector is missing or has the wrong size")
        result = []
        live = {value(self.table + 0x10, "<Q"), owner, entries}
        for index, (name, rows) in enumerate(effective.items()):
            name_ptr = value(entries + 0x10 * index, "<Q")
            records = value(entries + 0x10 * index + 8, "<Q")
            require(self.names.get(name_ptr) == name and self.owns(name_ptr, 0x18 + len(name) + 1, "intern")
                    and value(name_ptr + 0x10, "<I") == 2 and self.owns(records, 0x30, "gnam-owner"),
                    "Native tag vector did not retain the selected interned object")
            length = value(records + 8, "<I")
            data = value(records + 0x10, "<Q")
            require(length == len(rows) and self.owns(data, length * 0x54, "array"),
                    "Native GNAM vector has the wrong size or storage")
            expected = b"".join(rows)
            actual = C.string_at(data, len(expected))
            require(actual == expected, "Native GNAM rows differ from effective loader input")
            live.update((name_ptr, records, data))
            result.append({"tag": name, "gnam_rows": length, "gnam_sha256": host.digest(actual),
                           "raw_sha256": host.digest(b"".join(groups[name]))})
        require(live == self.storage.keys() - self.released, "Tag allocation graph has unaccounted backing")
        return {"tags": result, "lookup": {"present": BIOME, "absent": BIOME ^ 1},
                "allocations": self.allocation_trace, "live_at_disposal": sorted(live),
                "disposal": "fixture storage after synchronous native return; no native map destructor"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", required=True, type=Path)
    parser.add_argument("--esm", required=True, type=Path)
    args = parser.parse_args()
    try:
        kernel, crt = host.host_preflight()
        exe, esm = map(host.regular, (args.exe, args.esm))
        drives = {exe.anchor, esm.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        drives.update(drive for drive in ("C:\\", "D:\\") if Path(drive).is_dir())
        require(all(available_bytes(kernel, root) >= 40_000_000_000 for root in drives),
                "Insufficient component disk floor")
        pages = host.pe_pages(host.read_pinned(exe, host.EXE, "Starfield EXE", keep=True), CODE, DATA)
        hash_table = verify_hash_table(pages)
        owner_scalar = verify_owner_scalar(pages)
        groups = load_groups(esm)
        references = qualify_main_file(esm, groups)
        host.cpu_check(kernel)
        host.allocate_pages(kernel, pages)
        try:
            tags = NativeTags(kernel, crt)
            tags.bind()
            for page in pages:
                host.protect(kernel, page, 0x20 if page in CODE else 4 if page in WRITABLE else 2)
            host.flush(kernel)
            result = tags.publish(groups, references)
        finally:
            for base in sorted({page & ~0xffff for page in pages}, reverse=True):
                require(kernel.VirtualFree(base, 0, 0x8000), f"Private release failed at {base:#x}")
        host.read_pinned(exe, host.EXE, "Starfield EXE after tag control")
        host.read_pinned(esm, host.ESM, "Starfield main ESM after tag control")
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f"D5BM tag component refused: {error}\n")
    print(json.dumps({"scope": "Original tag-map publication with supplied intern and main-file loader seams",
                      "biome": BIOME, "exe": host.EXE, "esm": host.ESM, "crc_table_sha256": hash_table,
                      "gnam_owner_scalar_bits": owner_scalar, "source_references": references,
                      **result}, sort_keys=True))


if __name__ == "__main__":
    main()
