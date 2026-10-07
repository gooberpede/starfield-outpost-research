# SPDX-License-Identifier: GPL-3.0-or-later
"""Focused 0.1.1 disposable qualification; never discovers/accesses Starfield.
Reads pinned local build/source identities; writes create-new ignored evidence.
Launches only the paired hidden fixture and adapter. Three cases: frozen existing
population with later unarmed threads, new-thread-only NO_HIT, and a fixture-only
retirement fault after durable capture to exercise exact-handle termination.
No runner kill. Adapter destructive recovery is gated by durable capture or
independently detected low disk plus verified retained target identity.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EVIDENCE = ROOT/".local-work/exp0002a-adapter-0.1.1"


def rows(path):
    # While a target is writing, ignore only the incomplete trailing line.
    data = path.read_bytes()
    return [json.loads(line) for line in data[:data.rfind(b"\n")+1].splitlines() if line]


def wait_until(predicate, seconds):
    deadline = time.monotonic()+seconds
    while not predicate():
        if time.monotonic() >= deadline:
            raise TimeoutError("bounded fixture/controller wait")
        time.sleep(.025)


def validate(native, target, mode, manifest, target_exit):
    get = lambda kind: [row for row in native if row["kind"] == kind]
    final = get("complete")[-1]
    fault, no_hit = mode == "retirement-fault", mode == "unarmed-only"
    assert all(row["version"] == "0.1.1" and row["source_id"] == manifest["source_id"] for row in native)
    assert not get("recovery_required")
    assert bool(get("failure")) == fault
    setup, armed = get("setup_started")[0], get("armed")[0]
    assert setup["tick_ms"]-target[0]["tick_ms"] >= 1500
    assert armed["thread_scope"] == "EXISTING_AT_ARMED"
    members = {row["tid"] for row in armed["members"]}
    trigger = next(row for row in target if row["kind"] == "trigger")
    assert trigger["tick_ms"]-armed["tick_ms"] >= 1900
    new_threads = get("new_thread_unarmed")
    later = {row["tid"] for row in new_threads}
    assert len(later) >= 2 and not members.intersection(later)
    assert all(row["tick_ms"] >= armed["tick_ms"] and not row["dr0_installed"] for row in new_threads)
    contexts = get("context")
    assert not any(row["tid"] in later and row["boundary"] in ("armed", "retired") for row in contexts)
    assert all(int(row["dr0"], 0) == 0 and int(row["dr7"], 0) == 0
               for row in contexts if row["tid"] in later)
    confirms = get("operator_confirm_received")
    assert len(confirms) == 1 and confirms[0]["tick_ms"] >= trigger["tick_ms"]
    captures = get("capture")
    assert len(captures) == (0 if no_hit else 1)
    if captures:
        c = captures[0]
        assert c["tid"] in members
        assert int(c["rip"], 0) == int(c["base"], 0)+int(manifest["fixture_rva"], 0)
        assert c["return_valid"] and c["stack"]["valid"]
        assert int(c["r8"], 0) == 0xffffffff and int(c["r9"], 0) == 0
        assert c["manager_50"]["valid"] and c["manager_50"]["hex"] == "2a000000"
        assert c["manager_8c"]["valid"] and c["manager_8c"]["hex"] == "07"
        stack = bytes.fromhex(c["stack"]["hex"])
        assert int.from_bytes(stack[:8], "little") == int(c["return_address"], 0)
        assert int.from_bytes(stack[40:48], "little") == 0x1122334455667788
        assert c["name"] == {"null": True}
        assert native.index(c) < native.index(get("capture_durable")[0]) < native.index(get("retirement_started")[0])
        assert final["evidence_complete"] and final["acquisition_status"] == "DURABLE_REQUEST"
    else:
        finished = get("capture_finished")[0]
        assert finished["reason"] == "NO_HIT" and finished["new_unarmed_threads"] >= 2
        assert 10000 <= finished["tick_ms"]-confirms[0]["tick_ms"] < 11500
        assert not get("capture_durable") and not final["evidence_complete"]
        assert final["acquisition_status"] == "NO_HIT_NEW_THREADS_PRESENT"
    if fault:
        assert "DISPOSABLE_ONLY" in get("failure")[0]["message"]
        permit = get("termination_authorized")[0]
        assert permit["pid"] == target[0]["pid"] and permit["evidence_complete"] and not permit["machine_safety"]
        assert permit["created_filetime"] == get("identity")[0]["created_filetime"]
        assert native.index(get("capture_durable")[0]) < native.index(permit)
        assert get("termination_completed")[0]["pid"] == target[0]["pid"]
        assert final["cleanup_status"] == "EXACT_TARGET_TERMINATED"
        assert final["target_outcome"] == "TERMINATED_EXACT_TARGET"
        assert target_exit == 0xe0000111
        assert all(not row["alive"] for row in get("health"))
    else:
        assert not get("termination_authorized")
        assert final["cleanup_status"] == "CLEAN_API_CHECKS_EVENT_STATE_NOT_PROVEN"
        assert target_exit == 0 and target[-1]["kind"] == "exit"
        initial = {row["tid"]: row for row in contexts if row["boundary"] == "initial"}
        retired = [row for row in contexts if row["boundary"] == "retired"]
        assert retired and all(row["dr0"] == initial[row["tid"]]["dr0"] and row["dr7"] == initial[row["tid"]]["dr7"]
                               and not (int(row["eflags"], 0)&0x100) for row in retired)
        assert get("cleanup_finished")[0]["debugger_absent"] and get("cleanup_finished")[0]["site_unchanged"]
        assert get("cleanup_finished")[0]["tick_ms"]-get("retirement_started")[0]["tick_ms"] < 15000
        counts = {}
        for row in native:
            if row["kind"] in ("suspend", "pending_resuspend"):
                counts[row["tid"]] = counts.get(row["tid"], 0)+1
            elif row["kind"] in ("resume", "pending_release"):
                counts[row["tid"]] = counts.get(row["tid"], 0)-1
        assert counts and all(value == 0 for value in counts.values())
        health = get("health")
        assert [row["delay"] for row in health] == [0, 1, 5, 15] and all(row["alive"] for row in health)
        beats = [row for row in target if row["kind"] == "heartbeat"]
        after = get("cleanup_finished")[0]["tick_ms"]
        first = next(row for row in beats if row["tick_ms"] >= after)
        last = beats[-1]
        assert last["tick_ms"]-after >= 15000 and last["calls"] == 1
        assert all(last["pulse"][i] > first["pulse"][i]+100 for i in range(3))
        assert last["tids"][0] in members and all(tid in later for tid in last["tids"][1:])
        assert last["caller_tid"] in (later if no_hit else members)
    return dict(passed=True, evidence_complete=final["evidence_complete"],
                acquisition=final["acquisition_status"], cleanup=final["cleanup_status"],
                target=final["target_outcome"], target_exit=target_exit,
                retained_hits=len(captures), new_unarmed_threads=len(later))


def qualify(build, output):
    build, output = build.resolve(), output.resolve()
    assert all(path.is_relative_to(EVIDENCE) for path in (build, output))
    manifest = json.loads((build/"manifest.json").read_text(encoding="utf-8"))
    assert manifest["live_enabled"] is False and manifest["version"] == "0.1.1"
    for name, value in manifest["binaries"].items():
        assert hashlib.sha256((build/name).read_bytes()).hexdigest() == value
    for name, value in manifest["sources"].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == value, "rebuild after source edit"
    output.mkdir()
    adapter, fixture = build/manifest["adapter_executable"], build/"request_fixture.exe"
    flags = subprocess.CREATE_NO_WINDOW
    subprocess.run([adapter, "--self-check"], check=True, timeout=5, creationflags=flags)
    blocked = subprocess.run([adapter, "--starfield", "1", output/"forbidden"],
                             capture_output=True, timeout=5, creationflags=flags)
    assert blocked.returncode == 2 and b"DISABLED:" in blocked.stderr
    assert not (output/"forbidden.native.jsonl").exists()
    result = dict(version="0.1.1", build_manifest_sha256=hashlib.sha256((build/"manifest.json").read_bytes()).hexdigest(),
                  termination_gate_self_checks=True, starfield_refused_before_access=True, cases={})
    for mode in ("fixed-existing", "unarmed-only", "retirement-fault"):
        prefix = output/mode
        target = debugger = None
        try:
            with (output/f"{mode}.fixture-output.txt").open("xb") as stdout, (output/f"{mode}.adapter-output.txt").open("xb") as debugout:
                target = subprocess.Popen([fixture, prefix, "unarmed-only" if mode == "unarmed-only" else "fixed-existing"],
                                          stdout=stdout, stderr=stdout, creationflags=flags)
                target_log = Path(str(prefix)+".fixture.jsonl")
                wait_until(lambda: target_log.exists() and target_log.stat().st_size > 0, 5)
                time.sleep(2)
                debugger = subprocess.Popen([adapter, "--fixture-retirement-fault" if mode == "retirement-fault" else "--fixture",
                                             str(target.pid), prefix], stdout=debugout, stderr=debugout, creationflags=flags)
                wait_until(lambda: Path(str(prefix)+".armed").exists() or debugger.poll() is not None, 25)
                assert Path(str(prefix)+".armed").exists(), "adapter failed before ARMED"
                time.sleep(1)
                Path(str(prefix)+".newthreads").touch(exist_ok=False)
                wait_until(lambda: any(row["kind"] == "heartbeat" and all(n >= 5 for n in row["pulse"]) for row in rows(target_log)), 10)
                time.sleep(1)
                Path(str(prefix)+".trigger").touch(exist_ok=False)
                time.sleep(.5)
                Path(str(prefix)+".confirm").touch(exist_ok=False)
                assert debugger.wait(timeout=45) == 0
                Path(str(prefix)+".stop").touch(exist_ok=False)
                target.wait(timeout=10)
            native, fixture_rows = rows(Path(str(prefix)+".native.jsonl")), rows(target_log)
            result["cases"][mode] = validate(native, fixture_rows, mode, manifest, target.returncode)
            print(json.dumps({mode: result["cases"][mode]}), flush=True)
        except Exception as error:
            if target and target.poll() is None:
                Path(str(prefix)+".stop").touch(exist_ok=True)
            result["cases"][mode] = dict(passed=False, error=str(error), target_pid=target.pid if target else None,
                                        adapter_pid=debugger.pid if debugger else None)
            raise
        finally:
            (output/"qualification.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    qualify(args.build, args.output)
