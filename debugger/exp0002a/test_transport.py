# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit synthetic-only x64dbg qualification; no game/save access.

Runs the original fixture.exe with a new trigger path, attaches installed
x64dbg headless, observes one marker on two threads or a zero-hit timeout,
removes its breakpoint, detaches and lets the fixture exit normally. Never
terminates either process. Writes only a new ignored evidence directory.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import re
import subprocess
import time
from transport import Transport
from process_read import ProcessRead
from capture import log_format

K = C.WinDLL('kernel32', use_last_error=True)
K.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
K.OpenProcess.restype = W.HANDLE
K.CheckRemoteDebuggerPresent.argtypes = [W.HANDLE, C.POINTER(W.BOOL)]
K.CheckRemoteDebuggerPresent.restype = W.BOOL
K.CloseHandle.argtypes = [W.HANDLE]


def debugged(pid):
    h = K.OpenProcess(0x400, False, pid)
    if not h:
        raise C.WinError(C.get_last_error())
    try:
        value = W.BOOL()
        if not K.CheckRemoteDebuggerPresent(h, C.byref(value)):
            raise C.WinError(C.get_last_error())
        return bool(value.value)
    finally:
        K.CloseHandle(h)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixture', type=Path, required=True)
    p.add_argument('--debugger', type=Path, required=True)
    p.add_argument('--name', required=True)
    p.add_argument('--zero-hit', action='store_true')
    p.add_argument('--hit-cap', action='store_true')
    a = p.parse_args()
    if a.fixture.name != 'fixture.exe' or not re.fullmatch('[a-z0-9-]+', a.name):
        p.error('Explicit original fixture.exe and simple new run name required')
    root = Path(__file__).resolve().parents[2]/'.local-work/exp0002a'/a.name
    root.mkdir()
    trigger = root/'trigger.txt'
    transport = Transport(a.debugger, root/'debugger')
    target = subprocess.Popen([str(a.fixture.resolve()), str(trigger)]+(['cap'] if a.hit_cap else []))
    reader = ProcessRead(target.pid)
    detached = False
    try:
        transport.command(f'attach .{target.pid}', 10)
        # Attach command completion is qualified by an actual stopped context.
        time.sleep(.3)
        context = transport.command('log "SOR_CONTEXT {p:cip} {u:tid()}"')
        print(''.join(context))
        assert reader.debugged()
        address_lines = transport.command('log "SOR_ADDRESS {p:fixture.exe:sor_marker}"')
        address = int(next(s.split()[1] for s in address_lines if s.startswith('SOR_ADDRESS ')),16)
        original = reader.read(address,32)
        for label in ('REQUEST_ENTRY','NEW_SLOT_RETURN','SERIALIZER_ENTRY','COMPLETION_WAKE'):
            rendered = transport.command('log "'+log_format(label).replace('SOR_HIT','SOR_FORMAT')+'"')
            assert any(s.startswith('SOR_FORMAT '+label+' ') for s in rendered)
            assert not any('???' in s.split(' stack_valid=')[0] for s in rendered)
        transport.command('bp fixture.exe:sor_marker')
        assert reader.read(address,1) == b'\xcc'
        transport.command('SetBreakpointLog fixture.exe:sor_marker, "SOR_HIT tid={u:tid()} rip={p:cip} rcx={p:rcx} rdx={p:rdx} r8={p:r8} r9={p:r9} rsp={p:rsp} stack={mem;40@rsp}"')
        transport.command('SetBreakpointCondition fixture.exe:sor_marker, "$breakpointcounter>=19"')
        transport.command('run')
        if not a.zero_hit:
            trigger.write_text('synthetic only\n')
        start = time.monotonic()
        while time.monotonic()-start < 1.5:
            if transport.error:
                raise RuntimeError(transport.error)
            time.sleep(.02)
        transport.command('pause')
        transport.command('bc fixture.exe:sor_marker')
        transport.command('detach', 10)
        end = time.monotonic()+3
        while time.monotonic()<end and debugged(target.pid):
            time.sleep(.05)
        detached = not debugged(target.pid)
        if not detached:
            raise RuntimeError('Detach unconfirmed')
        restored = reader.read(address,32) == original
        assert restored
        transport.exit_detached()
        if a.zero_hit:
            trigger.write_text('release synthetic target after detach\n')
        target.wait(timeout=10)
        hits = [s.strip() for s in transport.lines if s.startswith('SOR_HIT ')]
        tids = {re.search(r'tid=(\d+)', s)[1] for s in hits}
        passed = target.returncode == 0 and ((not hits) if a.zero_hit else (len(hits)==25 if a.hit_cap else (len(hits)==2 and len(tids)==2)))
        result = dict(passed=passed, zero_hit=a.zero_hit, hits=hits, detached=detached,
                      hit_cap=a.hit_cap, site_bytes_restored=restored,
                      target_exit=target.returncode, elapsed=time.monotonic()-start,
                      evidence_kind='SYNTHETIC', live_game_qualification=False)
        (root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
        if not passed:
            raise RuntimeError('Synthetic qualification failed')
    except Exception:
        print('Failure; preserved log:',root)
        if target.poll() is None and not detached:
            try:
                transport.command('detach', 5)
                detached = not debugged(target.pid)
            except Exception:
                pass
        if detached or target.poll() is not None:
            if transport.process.poll() is None:
                transport.exit_detached()
        else:
            print('RECOVERY REQUIRED: debugger remains alive; no kill or automatic retry.')
        raise


if __name__ == '__main__':
    main()
