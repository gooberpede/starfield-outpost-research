# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded ProcGen rectangle completion and TargetBatchPage component.

Uses the owned D5BJ PE host and supplied allocator and command storage.
Executes original rectangle/wait producers, native receiver, graph trees
and follow-up. Supplies the resident-cell recorder and receiver progression.
Stops before dispatching the ready coordinate continuation.
"""
import argparse
import ctypes as C
import json
import os
from pathlib import Path
import shutil
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host

CODE = (
    0x1402b5000, 0x1402da000, 0x1402df000, 0x140323000, 0x140362000,
    0x1406db000, 0x14079c000, 0x14079d000, 0x1407af000, 0x1407b1000,
    0x140982000, 0x140996000, 0x14180d000, 0x14180e000, 0x141811000,
    0x1418aa000, 0x1422c7000, 0x1422c8000, 0x1422cd000, 0x1422ce000,
    0x142490000, 0x142491000, 0x142492000,
    0x1427e4000, 0x1427e5000, 0x1427e6000, 0x1427e7000, 0x1427e8000,
    0x1427e9000, 0x1427ea000, 0x1427eb000, 0x1427ec000,
    0x1427ed000, 0x1427ee000, 0x1428d7000, 0x1428d8000, 0x143663000,
)
DATA = (
    0x143a3f000, 0x143a40000, 0x144afc000, 0x144b00000, 0x144b3f000,
    0x144d9c000, 0x1458d5000, 0x145e60000, 0x145fd9000, 0x1461e1000, 0x1461ef000,
    0x1482df000,
)
WRITABLE = {0x145e60000, 0x145fd9000, 0x1461e1000, 0x1461ef000, 0x1482df000}
TRIPLE = (1, 2, 3)
RECTANGLE = (-16, -16, 23, 23)
CAPACITY = 0x400
P = C.c_void_p
U32 = C.c_uint32
require = host.require


def value(address, fmt):
    return struct.unpack(fmt, C.string_at(address, struct.calcsize(fmt)))[0]


def write(address, fmt, data):
    raw = struct.pack(fmt, data)
    C.memmove(address, raw, len(raw))


def key_at(address):
    return struct.unpack("<III", C.string_at(address, 12))


class Site:
    """Owned command segment with the original receiver cursor and commit ABI."""

    def __init__(self, address):
        self.address = address
        self.receiver = address + 0x40
        self.queue = address + 0x80
        self.storage = C.create_string_buffer(CAPACITY + 0x40)
        self.segment = C.addressof(self.storage)
        self.reservations = []
        self.used = 0
        write(address + 0x1d0, "<Q", self.segment)
        write(address + 0x1e4, "<I", CAPACITY)
        write(self.segment + 0x10, "<I", CAPACITY)

    def reserve(self, result, size, alignment):
        require(alignment == 8 and size in (32, 40, 56), "Unexpected server command size")
        span = size + 8
        offset = self.used
        require(offset + span < CAPACITY, "Component command segment exhausted")
        self.used += span
        header = self.segment + 0x40 + offset
        write(header, "<I", span)
        write(header + 4, "<I", CAPACITY)
        C.memmove(result, struct.pack("<QII", self.segment, offset, span), 16)
        packet = header + 8
        self.reservations.append(packet)
        return packet

    def cursor(self):
        return value(self.address + 0x1d8, "<I")

    def committed(self):
        return value(self.segment + 0x0c, "<I")


class NativeServer:
    """Composable fixture state, installed after the shared PE page mapping."""

    def __init__(self, kernel, crt):
        self.kernel = kernel
        self.crt = crt
        self.owner = C.create_string_buffer(0x500)
        self.manager = C.create_string_buffer(0x210)
        self.index = C.create_string_buffer(0x70)
        self.content = C.create_string_buffer(0x500)
        self.memory_tls = C.create_string_buffer(0x800)
        self.owner_ptr = C.addressof(self.owner)
        self.server = self.owner_ptr + 0x40
        self.table = self.server + 0x38
        self.manager_ptr = C.addressof(self.manager)
        self.content_ptr = C.addressof(self.content)
        self.procgen = Site(self.server + 0x140)
        self.service = Site(self.content_ptr + 0x40)
        self.callbacks = []
        self.cells = []
        self.allocations = {}
        self.frees = []
        self.graph_events = []
        self.lock_wakes = []
        self.rectangle = None
        self.wait_node = None
        write(self.server + 0x30, "<Q", self.procgen.receiver)
        write(self.server + 0x118, "<Q", self.server + 0x110)
        write(self.owner_ptr + 0x168, "<I", 1)
        write(self.owner_ptr + 0x440, "<Q", 1)
        write(self.manager_ptr + 0x80, "<I", 0x5e0de)
        write(self.manager_ptr + 0x120, "<Q", C.addressof(self.index))
        struct.pack_into("<III", self.manager, 0x60, *TRIPLE)
        write(C.addressof(self.memory_tls) + 0x418 + 0x8c, "<I", 0x200)

    def install(self):
        """Install private fixture seams before setting execute protections."""
        for slot, operand in (
            (0x145fd9c30, self.manager_ptr),
            (0x145fd9c38, self.owner_ptr),
            (0x1461e1d80, self.content_ptr),
        ):
            write(slot, "<Q", operand)
        write(0x145e60398, "<I", 2)
        # Select the declared allocation callback instead of the game's arena.
        write(0x145e60840, "<Q", 0)
        write(0x1461efd40, "<Q", 0)
        write(0x1482dfa10, "<I", 1)
        self.bind(0x143a3f418, self.kernel.GetCurrentThreadId)
        self.bind(0x143a40258, self.callback(C.c_int, (P,), self.clock))
        self.bind(0x143a402c8, self.callback(None, (P,), self.lock_wake))
        self.bind(0x143a3f390, self.callback(P, (U32,), self.get_memory_tls))
        self.hook(0x1422cdf60, self.callback(P, (P, P, U32, U32), self.reserve))
        self.hook(0x1427e4a30, self.callback(P, (P, U32), self.allocate_task))
        self.hook(0x1422c7ad0, self.callback(P, (P, U32, U32, C.c_uint8), self.allocate_tree))
        self.hook(0x1422ce9f0, self.callback(P, (P, U32, U32), self.allocate_followup))
        self.hook(0x1422ceb20, self.callback(None, (P, P), self.release))
        self.hook(0x1418aa1c0, self.callback(None, (P, P, C.c_uint8), self.resident_cell))
        self.bind_import(0x14366316c, self.crt.memset)

    def callback(self, result, args, operation):
        def invoke(*values):
            try:
                return operation(*values)
            except Exception as error:
                # A refused seam must not return an invalid pointer to native code.
                print(f"D5BM server seam stopped: {error}", file=sys.stderr, flush=True)
                os._exit(70)

        thunk = C.WINFUNCTYPE(result, *args)(invoke)
        self.callbacks.append(thunk)
        return thunk

    def bind(self, slot, function):
        write(slot, "<Q", C.cast(function, P).value)

    def bind_import(self, entry, function):
        thunk = C.string_at(entry, 6)
        require(thunk[:2] == b"\xff\x25", "Unexpected UCRT import thunk")
        self.bind(entry + 6 + struct.unpack_from("<i", thunk, 2)[0], function)

    def hook(self, entry, function):
        target = C.cast(function, P).value
        jump = b"\x48\xb8" + struct.pack("<Q", target) + b"\xff\xe0"
        C.memmove(entry, jump, len(jump))

    def clock(self, output):
        write(output, "<Q", 123)
        return 1

    def lock_wake(self, address):
        # Discriminator validation drops its transient lock at 0x14079cd9d.
        # The single-threaded component has no waiter to wake.
        require(address == self.manager_ptr + 0x70,
                f"Unqualified native lock wake: manager {address - self.manager_ptr:+#x}, "
                f"ProcGen {address - self.procgen.receiver:+#x}, "
                f"ContentManager {address - self.service.receiver:+#x}")
        self.lock_wakes.append("manager+0x70")

    def get_memory_tls(self, slot):
        require(slot == 1, "Unexpected memory TLS slot")
        return C.addressof(self.memory_tls)

    def reserve(self, queue, result, size, alignment):
        for site in (self.procgen, self.service):
            if queue == site.queue:
                return site.reserve(result, size, alignment)
        raise ValueError("Unqualified native command queue")

    def allocate(self, size, kind):
        storage = C.create_string_buffer(size + 15)
        address = (C.addressof(storage) + 15) & ~15
        self.allocations[address] = (storage, size, kind)
        return address

    def allocate_task(self, context, size):
        # The rectangle call leaves the checked mode byte minus three in
        # ECX. The wait call retains its owner. The original allocator uses
        # the size and ignores RCX on both paths.
        require((context, size) in ((0xff, 0xe0), (self.owner_ptr, 0x120)),
                "Unqualified task allocation")
        address = self.allocate(size, "rectangle" if size == 0xe0 else "wait")
        if size == 0xe0:
            require(self.rectangle is None, "Repeated rectangle allocation")
            self.rectangle = address
        else:
            require(self.wait_node is None, "Repeated wait allocation")
            self.wait_node = address
        return address

    def allocate_tree(self, manager, size, alignment, flags):
        require(manager == 0x145e603c0 and size in (0x200, 0x800) and alignment == flags == 1,
                "Unqualified graph page allocation")
        return self.allocate(size, "graph")

    def allocate_followup(self, memory, size, alignment):
        require(memory == C.addressof(self.memory_tls) + 0x418 and size == 0x68 and alignment == 8,
                "Unqualified follow-up allocation")
        return self.allocate(size, "target-page")

    def release(self, memory, address):
        require(memory == C.addressof(self.memory_tls) + 0x418 and address in self.allocations
                and address not in self.frees, "Unqualified or duplicate native release")
        _, _, kind = self.allocations[address]
        self.frees.append(address)
        if kind == "rectangle":
            head = value(self.server + 0x110, "<Q")
            require(head in self.allocations and self.allocations[head][2] == "target-page",
                    "Rectangle destruction did not leave the native follow-up pending")
            self.graph_events.append({
                "event": "rectangle_release", "readers": self.readers(),
                "state": value(address + 0xa8, "<B"), "page_is_linked": True,
            })
        if kind == "target-page":
            self.graph_events.append({
                "event": "target_page_release",
                "wrapper": hex(value(address + 0x10, "<Q")),
                "callback": hex(value(address + 0x18, "<Q")),
                "category": value(address + 0x28, "<I"),
                "target_count": value(address + 0x44, "<I"),
                "prerequisite": key_at(address + 0x48),
                "dependent": key_at(address + 0x58),
                "wait_prerequisites": value(self.wait_node + 0x90, "<I"),
                "wait_state": value(self.wait_node + 0xa8, "<B"),
            })

    def readers(self):
        return value(self.manager_ptr + 0x28, "<I")

    def resident_cell(self, content, coordinate, flag):
        require(content == self.content_ptr and flag == 1 and len(self.cells) < 1600
                and value(self.service.receiver + 4, "<I") == 0x10001,
                "Unexpected native rectangle resident-cell call")
        self.cells.append(struct.unpack("<ii", C.string_at(coordinate, 8)))

    def drain_site(self, site):
        require(site in (self.procgen, self.service)
                and value(self.server + 0x30, "<Q") == self.procgen.receiver,
                "Unqualified embedded receiver binding")
        native = host.callsite(0x1428d8060, 1, C.c_uint8)
        result = native(site.receiver)
        require(value(site.receiver, "<Q") == 0, "Unreleased native receiver lock")
        require(site.cursor() == site.committed(), "Native receiver did not consume its commands")
        return result

    def lookup(self, key):
        operand = (U32 * 3)(*key)
        result = (C.c_uint64 * 4)()
        host.callsite(0x142492430, 3)(self.table, result, operand)
        page, index = result[:2]
        if not page:
            require(index == 0x55, "Unexpected native absent-key sentinel")
            return None
        require(index < value(page + 4, "<I") and key_at(page + 0x18 + index * 12) == key,
                "Native lookup did not locate the exact key")
        return value(page + 0x418 + index * 8, "<Q")

    def admit_rectangle(self, triple, mode, ready):
        write(self.manager_ptr + 0x20, "<B", mode)
        write(C.addressof(self.index) + 0x60, "<B", ready)
        descriptor = (U32 * 7)(*triple, *RECTANGLE)
        output = C.create_string_buffer(0x28)
        return host.callsite(0x14079ce00, 2, C.c_uint8)(descriptor, output)

    def produce_wait(self, rectangle_key, pool=0, scope_tag=0):
        wait = (U32 * 3)()
        prerequisite = (U32 * 3)(*rectangle_key)
        descriptor = (U32 * 7)(*TRIPLE, *RECTANGLE)
        scope = (C.c_uint64 * 2)(pool, scope_tag)
        continuation = C.create_string_buffer(0x28)
        tracking_key = (U32 * 3)()
        native = host.callsite(0x1407afd70, 8)
        require(native(self.owner_ptr, wait, 0, scope, prerequisite, descriptor, continuation,
                       tracking_key) == C.addressof(wait), "Native wait producer returned another key")
        return tuple(wait)

    def notify_control(self, key):
        result = C.create_string_buffer(0x18)
        write(C.addressof(result) + 0x10, "<Q", self.server)
        operand = (U32 * 3)(*key)
        host.callsite(0x140362520, 2)(result, operand)

    def wait_status(self):
        return value(self.wait_node + 0xa8, "<B"), value(self.wait_node + 0x90, "<I")

    def consume_completion(self, receiver):
        require(receiver is self.procgen, "Completion receiver must match the bound ProcGen site")
        return self.drain_site(receiver)

    def component_probe(self, hold_page):
        for triple, mode, ready, expected in (
            ((1, 2, 4), 2, 1, 5), (TRIPLE, 3, 1, 3), (TRIPLE, 2, 0, 3),
        ):
            require(self.admit_rectangle(triple, mode, ready) == expected and not self.allocations
                    and not self.procgen.committed() and not self.readers(),
                    "Rectangle guard admitted work")
        require(self.admit_rectangle(TRIPLE, 2, 1) == 5 and self.rectangle and self.readers() == 1,
                "Native rectangle admission failed")
        rectangle_key = key_at(self.rectangle + 8)
        wait_key = self.produce_wait(rectangle_key)
        require(self.wait_node and wait_key == key_at(self.wait_node + 8) and wait_key != rectangle_key,
                "Native wait key mismatch")
        require(self.drain_site(self.procgen) == 1 and self.lookup(rectangle_key) == self.rectangle
                and self.lookup(wait_key) == self.wait_node and self.wait_status() == (1, 1)
                and value(self.rectangle + 0x94, "<H") == 2
                and value(self.rectangle + 0xa8, "<B") == 4 and self.service.committed(),
                "Original registration/Add/Commit failed to install the rectangle dependency")
        missing = (0xffffffff, 0xffffffff, 0x7fffffff)
        require(self.lookup(missing) is None, "Control key unexpectedly present")
        for key in (missing, wait_key):
            self.notify_control(key)
            require(self.drain_site(self.procgen) == 1 and self.wait_status() == (1, 1)
                    and self.lookup(rectangle_key) == self.rectangle and self.readers() == 1
                    and not self.frees, "Wrong-key or ineligible-state control changed the rectangle")
        cursor = self.procgen.cursor()
        require(self.drain_site(self.service) == 1
                and self.cells == [(x, y) for x in range(-16, 24) for y in range(23, -17, -1)],
                "Native rectangle traversal diverged")
        packet = self.procgen.reservations[-1]
        require(struct.unpack("<QQQ", C.string_at(packet, 24))
                == (0x144b00d68, 0x140362510, self.server)
                and key_at(packet + 0x18) == rectangle_key
                and self.procgen.committed() > cursor and self.procgen.cursor() == cursor
                and self.lookup(rectangle_key) == self.rectangle and self.readers() == 1
                and self.wait_status() == (1, 1), "Unqualified held rectangle completion")
        try:
            self.consume_completion(self.service)
        except ValueError as error:
            require(str(error) == "Completion receiver must match the bound ProcGen site",
                    "Unexpected wrong-receiver refusal")
        else:
            raise ValueError("Wrong receiver failed to refuse")
        require(self.procgen.cursor() == cursor and self.readers() == 1,
                "Wrong receiver altered the selected completion")
        if hold_page:
            write(self.server + 0x120, "<B", 1)
        require(self.consume_completion(self.procgen) == 1 and self.lookup(rectangle_key) is None
                and self.readers() == 0, "Original NotifyComplete did not erase and release the rectangle")
        held = None
        if hold_page:
            held = self.wait_status()
            require(held == (1, 1) and value(self.server + 0x110, "<Q")
                    and len(self.graph_events) == 1, "Held page failed to gate the dependent")
            write(self.server + 0x120, "<B", 0)
            host.callsite(0x1427e6c00, 1, None)(self.server)
        require(self.wait_status() == (2, 0)
                and self.lookup(wait_key) == self.wait_node and value(self.server + 0x110, "<Q") == 0
                and value(self.server + 0x118, "<Q") == self.server + 0x110
                and value(self.server + 0x58, "<Q"), "Original TargetBatchPage did not ready the wait")
        require(len(self.graph_events) == 2, "Unexpected rectangle/page lifetime")
        before, after = self.graph_events
        require(before == {"event": "rectangle_release", "readers": 0, "state": 6, "page_is_linked": True}
                and after["wrapper"] == "0x144d9cab0" and after["callback"] == "0x1427eecf0"
                and after["category"] == 0 and after["target_count"] == 2
                and after["prerequisite"] == rectangle_key and after["dependent"] == wait_key
                and (after["wait_state"], after["wait_prerequisites"]) == (2, 0),
                "Original page/rectangle lifetime did not match the selected edge")
        return {"tier": "server component, supplied resident-cell and receiver progression",
                "rectangle_key": rectangle_key, "wait_key": wait_key, "visits": len(self.cells),
                "held_page_wait_state": held, "transitions": self.graph_events,
                "lock_wakes": self.lock_wakes,
                "negative_controls": ["generation", "mode", "index", "stale key", "ineligible node state",
                                      "fixture refusal of wrong completion receiver"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", required=True, type=Path)
    parser.add_argument("--hold-page", action="store_true")
    args = parser.parse_args()
    try:
        kernel, crt = host.host_preflight()
        exe = host.regular(args.exe)
        drives = {exe.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        drives.update(drive for drive in ("C:\\", "D:\\") if Path(drive).is_dir())
        require(all(shutil.disk_usage(root).free >= 40_000_000_000 for root in drives),
                "Insufficient component disk floor")
        pages = host.pe_pages(host.read_pinned(exe, host.EXE, "Starfield EXE", keep=True), CODE, DATA)
        host.cpu_check(kernel)
        host.allocate_pages(kernel, pages)
        try:
            server = NativeServer(kernel, crt)
            server.install()
            for page in pages:
                protection = 0x20 if page in CODE else 4 if page in WRITABLE else 2
                host.protect(kernel, page, protection)
            host.flush(kernel)
            result = server.component_probe(args.hold_page)
        finally:
            for base in sorted({page & ~0xffff for page in pages}, reverse=True):
                require(kernel.VirtualFree(base, 0, 0x8000), f"Private release failed at {base:#x}")
        host.read_pinned(exe, host.EXE, "Starfield EXE after server control")
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f"D5BM server component refused: {error}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
