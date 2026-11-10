# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the two original JobSite pumps on one originally started pool.

Uses supplied JobSite storage and marker commands. The original receiver
and pump run on native workers. No rectangle or layer semantics are claimed.
"""
import argparse
import ctypes as C
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
from d5bj_workers import original_getter_sites
from d5bm_pool import CODE as POOL_CODE, DATA, RW_DATA, PoolRuntime, PTR, U64, available_bytes, ncall, pointer
from d5bm_pump_gate import PumpGate
from d5bm_server import Site, value, write

CODE = tuple(sorted(set(POOL_CODE) | {0x1428D8000, 0x1428D9000}))


class PumpTrace:
    def __init__(self):
        self.events = []
        self.stages = {}

    def record(self, stage, packet, **identity):
        previous = {"published": None, "entered": "published", "returned": "entered"}
        host.require(self.stages.get(packet) == previous[stage], "Duplicate or out-of-order pump packet")
        self.stages[packet] = stage
        self.events.append({"stage": stage, "packet": packet, **identity})


class ControlStop(ValueError):
    pass


def probe(kernel, pages, case):
    runtime = PoolRuntime(kernel)
    host.allocate_pages(kernel, pages)
    runtime.bind()
    buffers = [C.create_string_buffer(0x2A0) for _ in range(2)]
    content, procgen = [Site(C.addressof(buffer)) for buffer in buffers]
    sites = {site.address: site for site in (content, procgen)}
    names = {content.address: "content", procgen.address: "procgen"}
    for buffer in buffers:
        struct.pack_into("<6H", buffer, 0x28A, 1, 2, 4, 8, 16, 32)
        host.put(buffer, 0x296, "<H", 9)
    gate = PumpGate(runtime, content.address)
    gate.install()
    claims, packets, publications = [], {}, {}
    trace = PumpTrace()
    wakes = []
    pump = ncall(0x1428D89B0, None, PTR, C.c_float)

    def run_marker(packet):
        site, marker = packets[packet]
        member = runtime.membership()
        host.require(member and member["pool"] == runtime.pool
                     and value(site.receiver, "<I") == member["thread_id"]
                     and value(site.receiver + 4, "<I") == 0x10001
                     and value(site.address + 0x296, "<H") == 9,
                     "Marker lacked the original receiver lock and worker")
        with runtime.condition:
            host.require(all(row["packet"] != packet for row in claims), "Marker packet executed twice")
            claims.append({"site": names[site.address], "marker": marker, "packet": packet, **member})
            runtime.condition.notify_all()

    def start_pump(packet):
        with runtime.condition:
            address = publications.get(packet)
            member = runtime.membership()
            host.require(address in sites and member and member["pool"] == runtime.pool
                         and U64.from_address(packet + 0x10).value == address, "Foreign pump packet or owner")
            identity = {"site": names[address], "address": address, **member}
            trace.record("entered", packet, **identity)
        pump(address, 0)
        with runtime.condition:
            host.require(runtime.membership() == member, "Pump return changed native membership")
            trace.record("returned", packet, **identity)
            runtime.condition.notify_all()

    def wake_all(address):
        host.require(address in {site.address + 0x296 for site in sites.values()},
                     "Foreign pump state wake")

    def unexpected_getter():
        runtime.refuse("Selected state-9 wake entered its pool-getter/publication branch")

    callback = runtime.callback(None, (PTR,), start_pump)
    command = runtime.callback(None, (PTR,), run_marker)
    forbidden = runtime.callback(PTR, (), unexpected_getter)
    runtime.import_hook(0x143A402D8, None, (PTR,), wake_all)
    for page in pages:
        host.protect(kernel, page, 0x20 if page in CODE else 4 if page in RW_DATA else 2)
    host.flush(kernel)
    allocate = ncall(0x1422CE9F0, PTR, PTR, U64, U64)
    push = ncall(0x1428D2B80, U64, PTR, PTR)

    def append(site, marker):
        reservation = C.create_string_buffer(16)
        packet = site.reserve(C.addressof(reservation), 32, 8)
        C.memmove(packet, struct.pack("<4Q", 0, pointer(command), marker, 0), 32)
        packets[packet] = site, marker
        write(site.segment + 0xC, "<I", site.used)

    def publish(site):
        payload = allocate(memory + 0x418, 32, 8)
        host.require(payload and payload & -0x10000 in runtime.blocks, "Unowned pump marker")
        C.memmove(payload, struct.pack("<4Q", 0, pointer(callback), site.address, 0), 32)
        with runtime.condition:
            host.require(payload not in publications, "Supplied pump packet address was reused")
            publications[payload] = site.address
            trace.record("published", payload, site=names[site.address], address=site.address, pool=runtime.pool)
        push(runtime.pool, C.byref(U64(payload)))
        runtime.release_semaphore(U64.from_address(runtime.pool + 0xB8).value, 1, None)
        return payload

    def order():
        return [(row["site"], row["marker"]) for row in claims]

    def await_return(packet, quiescent):
        runtime.wait_for_progress(lambda: trace.stages[packet] == "returned", quiescent,
                                  f"selected pump return for {packet:#x}")

    cleanup_safe = False
    control_stop = None
    try:
        runtime.initialize()
        runtime.start()
        runtime.verify_site_getters(0x1428D1880, 0x1428D1880)
        memory = runtime.memory_context(0x145E60820)
        cleanup_safe = True
        append(content, 1)
        append(procgen, 2)
        if case != "normal":
            gate.arm()
        first = publish(content)
        if case == "normal":
            await_return(first, runtime.idle)
            await_return(publish(procgen), runtime.idle)
        else:
            held = gate.wait_until_held()
            eligible = {row[2] for row in runtime.threads.values() if row[0] == runtime.pool}
            host.require(held["thread_id"] in eligible, "Held worker is outside the shared pool")
            eligible.remove(held["thread_id"])

            def peer_quiescent():
                return eligible <= runtime.waiting and runtime.queues_empty()

            if case == "missing":
                runtime.wait_for_progress(peer_quiescent, lambda: False, "unpublished peer quiescence")
                host.require(gate.held and set(publications) == {first} and order() == [("content", 1)],
                             "Missing-peer control unexpectedly made progress")
                control_stop = "peer absent with eligible workers quiescent and queues empty"
            elif case == "fault":
                raise ControlStop("injected controller fault at held receiver")
            else:
                append(content, 3)
                wake = ncall(0x1428D96C0, U64, PTR)
                request = (U64 * 3)(content.address, pointer(forbidden), 0)
                with runtime.condition:
                    before = len(trace.events)
                    wake(C.byref(request))
                    host.require(len(trace.events) == before and order() == [("content", 1)],
                                 "Selected wake changed supplied publication or marker order")
                    wakes.append({"entry": 0x1428D96C0, "getter_guard": "not reached", **gate.frontier()})
                second = publish(procgen)
                await_return(second, peer_quiescent)
                gate.events["peer_frontier"] = gate.frontier()
                host.require(order() == [("content", 1), ("procgen", 2)]
                             and claims[1]["thread_id"] in eligible, "Wrong concurrent pump ordering")
                gate.release()
                gate.wait_until_resumed()
                await_return(first, runtime.idle)
                host.require(order() == [("content", 1), ("procgen", 2), ("content", 3)]
                             and all(claims[2][key] == held[key] for key in ("thread_id", "context", "pool")),
                             "Selected marker did not run on the resumed ContentManager worker")
    except ControlStop as error:
        host.require(case == "fault", "Unexpected controller control fault")
        control_stop = str(error)
    finally:
        try:
            if not cleanup_safe:
                runtime.refuse("Pump startup could not establish safe in-process cleanup")
            gate.cancel(control_stop or "controller cleanup")
            runtime.wait_for_progress(runtime.idle, lambda: False, "owned pump drain")
            host.require(all(stage == "returned" for stage in trace.stages.values()),
                         "Native pumps did not account for every supplied packet")
            runtime.stop()
            gate.close()
            for base in sorted({page & ~0xFFFF for page in pages}, reverse=True):
                host.require(kernel.VirtualFree(base, 0, 0x8000), "Private pump page release failed")
        except BaseException as error:
            runtime.refuse(f"Pump cleanup unsafe; owned-child STOP: {error}")
    terminal = [value(site.address + 0x296, "<H") for site in sites.values()]
    if case in ("missing", "fault"):
        host.require(control_stop and "cancelled_return" in gate.events and order() == [("content", 1)]
                     and terminal == [1, 9], "Missing/fault control did not cancel and drain the selected hold")
    else:
        expected = [("content", 1), ("procgen", 2)]
        if case == "pending":
            expected.append(("content", 3))
        host.require(order() == expected and terminal == [1, 1], "Original pumps did not finish both receivers")
    return {"case": case, "control_stop": control_stop, "gate": gate.events, "claims": claims,
            "packets": trace.events, "wakes": wakes, "terminal_states": terminal,
            "native_joins": len(runtime.joined), "call_restored": not gate.installed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", required=True, type=Path)
    parser.add_argument("--case", required=True, choices=("normal", "pending", "missing", "fault"))
    args = parser.parse_args()
    try:
        kernel, _ = host.host_preflight()
        exe = host.regular(args.exe)
        drives = {exe.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        drives.update(drive for drive in ("C:\\", "D:\\") if Path(drive).is_dir())
        host.require(all(available_bytes(kernel, drive) >= 40_000_000_000 for drive in drives),
                     "Insufficient caller-available disk floor")
        image = host.read_pinned(exe, host.EXE, "Starfield EXE", keep=True)
        original_getter_sites(image)
        pages = host.pe_pages(image, CODE, DATA)
        host.cpu_check(kernel)
        result = probe(kernel, pages, args.case)
        host.read_pinned(exe, host.EXE, "Starfield EXE after pump probe")
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f"D5BM pump control refused: {error}\n")
    print(json.dumps({"scope": "Two marker pumps on the original shared started pool",
                      "exe_sha256": host.EXE, **result}, sort_keys=True))


if __name__ == "__main__":
    main()
