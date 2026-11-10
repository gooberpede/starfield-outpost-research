# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise original resident-file load/ready transitions in a disposable host.

This component keeps the original synchronous acquisition wrapper, payload
object construction, BC4 decode loop, state transition and re-acquisition.
It supplies archive I/O, legacy DDS header classification, cache lookup,
allocation and private TLS. A later integrated run must qualify these seams
on the actual keys enumerated by the native layer and density producers.
"""
import argparse
import ctypes as C
import json
import math
import os
from pathlib import Path
import shutil
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
import d5bm_files as inputs

CODE = (0x1402BA000, 0x1422C7000, 0x1422C8000, 0x1427B0000, 0x1427B1000,
        0x1427B3000, 0x1427D4000, 0x1427D5000, 0x1427EF000, 0x1428CA000)
DATA = (0x143A40000, 0x144CB3000, 0x144F04000, 0x144F05000, 0x145E60000, 0x145FB5000)
ENTRY = 0x1427B3930
DIMENSION = 1400
HEADER = 128
BLOCK_BYTES = 980_000
INITIAL = 0x10000001
READY = 0x30000001
P = C.c_void_p
U = C.c_uint32
Q = C.c_uint64


def header_size(body):
    host.require(len(body) == HEADER + BLOCK_BYTES and body[:4] == b"DDS "
                 and struct.unpack_from("<5I", body, 4) == (124, 659463, DIMENSION, DIMENSION, BLOCK_BYTES)
                 and struct.unpack_from("<I", body, 28)[0] == 1
                 and struct.unpack_from("<I", body, 76)[0] == 32 and body[84:88] == b"BC4U",
                 "Unsupported selected density DDS")
    return HEADER


def f32(value):
    return struct.unpack("<f", struct.pack("<f", value))[0]


def decode_reference(body):
    """Scalar byte-domain oracle for the selected single-level BC4U member."""
    raw = memoryview(body)[header_size(body):]
    count = DIMENSION // 4
    out = bytearray(DIMENSION * DIMENSION)
    one_fifth, one_seventh = f32(1 / 5), f32(1 / 7)
    for by in range(count):
        for bx in range(count):
            start = 8 * (by * count + bx)
            a, b = raw[start:start + 2]
            denominator = 7 if a > b else 5
            scale = one_seventh if a > b else one_fifth
            values = [a, b]
            values.extend(int(f32(((denominator - n) * a + n * b) * scale))
                          for n in range(1, denominator))
            if denominator == 5:
                values.extend((0, 255))
            indices = int.from_bytes(raw[start + 2:start + 8], "little")
            for y in range(4):
                for x in range(4):
                    out[(4 * bx + x) * DIMENSION + (DIMENSION - 1 - 4 * by - y)] = values[indices & 7]
                    indices >>= 3
    return bytes(out)


def pointer(location):
    return C.c_uint64.from_address(location)


def word(location):
    return C.c_uint32.from_address(location)


class Resident:
    def __init__(self, member):
        self.member = member
        self.header = header_size(member.body)
        self.backing = []
        self.callbacks = []
        self.events = []
        self.stream = self.buffer(0x20)
        self.node = self.buffer(0x30)
        self.read_buffer = self.buffer(len(member.body))
        self.private_tls = self.buffer(0x200)
        C.c_uint8.from_address(self.private_tls + 0xBC).value = 1
        self.payload = self.buffer(0x18)
        self.decoded = self.buffer(DIMENSION * DIMENSION)
        self.database = self.buffer(0x80)
        self.cache = self.buffer(0x80)
        self.auxiliary = self.buffer(0x20)
        self.vtable = self.buffer(0x38)
        pointer(self.stream).value = self.vtable
        pointer(self.stream + 8).value = len(member.body)
        pointer(self.vtable).value = self.callback(None, (P, U), self.close)
        pointer(self.vtable + 0x10).value = self.callback(None, (P,), self.finish_read)
        pointer(self.vtable + 0x30).value = self.callback(U, (P, P, Q, P), self.read)
        struct.pack_into("<3I", (C.c_char * 0x30).from_address(self.node), 8, *member.archive_key)
        word(self.node + 0x14).value = INITIAL

    def buffer(self, size):
        value = C.create_string_buffer(size)
        self.backing.append(value)
        return C.addressof(value)

    def callback(self, result, args, operation):
        def checked(*values):
            try:
                return operation(*values)
            except Exception as error:
                # This runner owns its disposable process. Do not return an
                # invalid pointer into the original continuation.
                print(f"D5BM resident seam stopped: {error}", file=sys.stderr, flush=True)
                os._exit(70)
        target = C.WINFUNCTYPE(result, *args)(checked)
        self.callbacks.append(target)
        return C.cast(target, P).value

    def hook(self, entry, result, args, operation):
        target = self.callback(result, args, operation)
        C.memmove(entry, b"\x48\xb8" + struct.pack("<Q", target) + b"\xff\xe0", 12)

    def acquire(self, db, key, _, enabled, out):
        host.require(db == self.database and enabled == 1, "Unexpected resource-read operands")
        if tuple((U * 3).from_address(key)) != self.member.archive_key:
            self.events.append("wrong_key_refused")
            return 2
        host.require(word(self.stream + 0x10).value == 0, "Stream still owned")
        word(self.stream + 0x10).value = 0x1000
        pointer(out).value = self.stream
        self.events.append("archive_member_acquired")
        return 0

    def find(self, cache, key, initial):
        host.require(cache == self.cache and initial == 0x10000000
                     and tuple((U * 3).from_address(key)) == self.member.archive_key,
                     "Wrong private cache lookup")
        self.events.append("matching_key_found")
        return self.node

    def open_stream(self, out, source, _, mode):
        current = pointer(source).value
        references = word(self.stream + 0x10).value
        host.require(mode == 1 and current == self.stream and references == 0x1000,
                     f"Unexpected stream owner (mode {mode}, matched {current == self.stream}, refs {references:#x})")
        word(self.stream + 0x10).value += 0x1000
        struct.pack_into("<QQB", (C.c_char * 0x18).from_address(out), 0, self.stream, 0, 1)
        return out

    def read(self, source, out, count, written):
        host.require(source == self.stream and out == self.read_buffer and count == len(self.member.body),
                     "Wrong DDS read operands")
        C.memmove(out, self.member.body, count)
        pointer(written).value = count
        self.events.append("authentic_member_read")
        return 0

    def close(self, source, flag):
        host.require(source == self.stream and flag == 1 and word(source + 0x10).value == 0,
                     "Stream close at nonterminal reference count")
        self.events.append("stream_closed")

    def finish_read(self, source):
        host.require(source == self.stream, "Wrong read completion receiver")

    def temporary(self, out, size, alignment):
        host.require(size == len(self.member.body) and alignment == 8, "Unexpected temporary allocation")
        pointer(out).value = self.read_buffer
        return out

    def allocate_payload(self, _, size, zero_a, zero_b):
        host.require((size, zero_a, zero_b) == (0x18, 0, 0), "Unexpected payload allocation")
        return self.payload

    def allocate_decoded(self, size, flags):
        host.require(size == DIMENSION * DIMENSION and flags == 1, "Unexpected decoded allocation")
        return self.decoded

    def notify(self, state):
        host.require(state == self.node + 0x14 and word(state).value == READY, "Wrong native wake state")
        self.events.append("native_ready_wake")

    def message(self, _, key):
        host.require(tuple((U * 3).from_address(key)) == self.member.archive_key, "Wrong ready-message key")
        self.events.append("native_ready_message")

    def bind(self):
        self.hook(0x1427D52A0, U, (P, P, P, U, P), self.acquire)
        self.hook(0x1427B3BE0, P, (P, P, U), self.find)
        # The original caller sets R9B and leaves the rest of R9 unspecified.
        self.hook(0x1427EF0E0, P, (P, P, P, C.c_uint8), self.open_stream)
        self.hook(0x1422C84C0, P, (P, Q, U), self.temporary)
        self.hook(0x1422C7AD0, P, (P, U, U, U), self.allocate_payload)
        self.hook(0x1402BA260, P, (Q, U), self.allocate_decoded)
        # The selected null smart-pointer releases are vacuous. Refuse if
        # the original path presents a real pointer to either release.
        def null_release(holder):
            host.require(pointer(holder).value == 0, "Unexpected nonnull auxiliary release")
        self.hook(0x1428CAEA0, None, (P,), null_release)
        pointer(0x143A402D8).value = self.callback(None, (P,), self.notify)
        pointer(0x144CB3070).value = self.callback(None, (P, P), self.message)

        # Initializer and temporary free ownership belong to the fixture.
        word(0x145E60398).value = 2
        word(0x145E60398 + 0x120).value = 2
        pointer(0x145FB5968).value = self.read_buffer
        for entry, register in ((0x1427B0FB2, b"\x48\xbf"), (0x1427B0D0E, b"\x48\xbd")):
            C.memmove(entry, register + struct.pack("<Q", self.private_tls) + b"\x90\x90", 12)
        # Source-derived seam for the legacy BC4U DDS header only. Original
        # body length, allocation and BC4U decode remain downstream.
        boundary = 0x1427B1103
        jump = b"\x41\xbf" + struct.pack("<I", self.header)
        jump += b"\xe9" + struct.pack("<i", 0x1427B11B3 - boundary - 11)
        C.memmove(boundary, jump, len(jump))

    def run(self, oracle):
        invoke = C.WINFUNCTYPE(U, P, P, P, P, U, P)(ENTRY)
        for key, expected in (((self.member.archive_key[0] ^ 1, *self.member.archive_key[1:]), 2),
                              (self.member.archive_key, 0), (self.member.archive_key, 0)):
            request = (U * 3)(*key)
            out = Q()
            code = invoke(self.database, self.cache, C.addressof(request), C.addressof(out), 1, self.auxiliary)
            host.require(code == expected, "Unexpected original acquisition result")
            host.require(out.value == (self.node if expected == 0 else 0), "Wrong returned handle")
            host.require(word(self.node + 0x14).value == (INITIAL if expected else READY), "Wrong live state")
        host.require(pointer(self.node + 0x20).value == self.payload
                     and pointer(self.payload + 0x10).value == self.decoded, "Missing decoded payload")
        actual = C.string_at(self.decoded, len(oracle))
        host.require(actual == oracle, "Decoded native payload differs from scalar byte oracle")
        host.require(self.events.count("authentic_member_read") == 1
                     and self.events.count("native_ready_wake") == 1
                     and self.events.count("stream_closed") == 2, "Unexpected load or re-acquisition history")
        return {"member": self.member.receipt(), "events": self.events, "initial_state": INITIAL,
                "final_state": READY, "decoded_sha256": host.digest(actual), "decoded_size": len(actual)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("exe", "esm", "planet-data", "density-maps"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    try:
        kernel, _ = host.host_preflight()
        exe, esm, planet, density = map(host.regular, (args.exe, args.esm, args.planet_data, args.density_maps))
        drives = {Path.cwd().anchor, Path(sys.executable).anchor, *(path.anchor for path in (exe, esm, planet, density))}
        drives.update(drive for drive in ("C:\\", "D:\\") if Path(drive).is_dir())
        host.require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives), "Insufficient disk floor")
        image = host.read_pinned(exe, host.EXE, "Starfield EXE", keep=True)
        projected, members = inputs.load(esm, planet, density)
        chosen = members[projected[0x00257F2C][0]]
        oracle = decode_reference(chosen.body)
        pages = host.pe_pages(image, CODE, DATA)
        host.cpu_check(kernel)
        resident = Resident(chosen)
        host.allocate_pages(kernel, pages)
        try:
            resident.bind()
            for page in pages:
                host.protect(kernel, page, 0x20 if page in CODE else 4)
            host.flush(kernel)
            result = resident.run(oracle)
        finally:
            for base in sorted({page & ~0xFFFF for page in pages}, reverse=True):
                host.require(kernel.VirtualFree(base, 0, 0x8000), f"Private release failed at {base:#x}")
        host.read_pinned(exe, host.EXE, "Starfield EXE after resident control")
    except (OSError, ValueError, struct.error, zlib.error) as error:
        parser.exit(1, f"D5BM resident control refused: {error}\n")
    print(json.dumps({"scope": "Original synchronous ready wrapper and decode with fixture I/O/cache",
                      "exe_sha256": host.EXE, "density_maps_sha256": inputs.ARCHIVE, **result}, sort_keys=True))


if __name__ == "__main__":
    main()
