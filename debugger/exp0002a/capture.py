# SPDX-License-Identifier: GPL-3.0-or-later
"""DISABLED HISTORICAL x64dbg TOOLING. All SFSE/profile checks below are obsolete
for prospective Stage B; ordinary Steam without SFSE is now required. The CLI
refuses before parsing or target access. Do not revive historical_main_disabled.

One authorized manual-save trace; no launch, deployment or native invocation.

Reads existing integrity baseline, protected-parent hashes/metadata, installed
game/SFSE files, selected process identity/code and save-directory metadata.
Invokes installed x64dbg headless with private settings; attaches, temporarily
sets four software execution breakpoints, resumes, removes them and detaches.
Writes only a new .local-work/exp0002a run directory. No console, save parsing,
save writes/deletion, gameplay register edits, exception suppression, or kill.

Run ONLY after the operator has reached the ordinary NEW manual-save slot and
agreed to act after ARMED. A stalled cleanup keeps the controller/debugger alive
for recovery; it must not be killed. This is an execution intervention.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from process_read import ProcessRead
from transport import Transport

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'research/exp0002'))
from prepare import metadata, equal_bytes

TOOL = 'SOR-EXP-0002A-x64dbg-capture-v4'
DEBUGGER = Path('D:/tools/x64dbg/release/x64/headless.exe')
PLAN_PATH = Path(__file__).with_name('capture_plan.json')
GAME_HASH = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
DEBUGGER_HASHES = {
    'headless.exe': '44ece2d8f81c1acbf4c85b45fe89e11875f0e1a0d2ba0c8c8c1a56bf85164268',
    'x64dbg.dll': 'dc9d5ff18d6e5fc9d667a2c2bc8fa9cce15fa5e0da9728222259a4525d542c0f',
    'x64bridge.dll': '39730aea3509e275bc2d69d8d27f22695821b7caffa30943fa0dcf36f9f558cd',
}


def write_new(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n'); f.flush(); os.fsync(f.fileno())


def space():
    result = {v: shutil.disk_usage(v).free for v in ('C:/','D:/')}
    if min(result.values()) < 40_000_000_000:
        raise RuntimeError('low_disk_space')
    return result


def parents():
    baseline = json.loads((ROOT/'.local-work/exp0002/integrity-before.json').read_text())
    result = {k: metadata(baseline[k]['path']) for k in ('original','backup')}
    for k in result:
        for field in ('sha256','size','mtime_ns'):
            if result[k][field] != baseline[k][field]:
                raise RuntimeError('protected_parent_changed')
    if not equal_bytes(result['original']['path'],result['backup']['path']):
        raise RuntimeError('protected_parent_not_equal')
    return result


def inventory(directory):
    files = list(directory.iterdir())
    if len(files) > 2000:
        raise RuntimeError('save_inventory_bound')
    return {p.name: {'size': p.stat().st_size, 'mtime_ns': p.stat().st_mtime_ns}
            for p in files if p.is_file()}


def thread_inventory(pid):
    # pid is validated integer; fixed read-only PowerShell, no shell-built paths.
    command = (f'$p = Get-Process -Id {pid} -ErrorAction Stop; '
               '$items = @($p.Threads | Select-Object Id, '
               '@{n="created_utc";e={$_.StartTime.ToUniversalTime().ToString("o")}}); '
               '$items | ConvertTo-Json -Compress')
    p = subprocess.run(['pwsh','-NoProfile','-Command',command],capture_output=True,text=True,timeout=10)
    if p.returncode:
        return {'unavailable': p.stderr[:1000]}
    data = json.loads(p.stdout)
    if isinstance(data,list) and len(data)>512:
        return {'unavailable':'thread_inventory_cap'}
    return data


def log_format(label):
    # Fixed-sized hex reads avoid unbounded string output and preserve encoding
    # uncertainty. Validity bits distinguish failed reads from zero/null values.
    common = ('SOR_HIT '+label+' tid={u:tid()} tick={u:GetTickCount()} rip={p:cip}'
              ' rcx={p:rcx} rdx={p:rdx} r8={p:r8} r9={p:r9} rax={p:rax} rsp={p:rsp}'
              ' stack_valid={mem.valid(rsp)&&mem.valid(rsp+5F)} stack={mem;60@rsp}')
    if label == 'SERIALIZER_ENTRY':
        common += (' name_valid={mem.valid(r9)&&mem.valid(r9+103)} name_hex={mem;104@r9}'
                   ' rcx_valid={mem.valid(rcx)} rcx_pointee={p:ReadQword(rcx)}')
    elif label == 'REQUEST_ENTRY':
        common += (' state_valid={mem.valid(rcx+50)&&mem.valid(rcx+8C)}'
                   ' state50={ReadDword(rcx+50)} busy8c={ReadByte(rcx+8C)}')
    elif label == 'COMPLETION_WAKE':
        common += ' wake_byte_valid={mem.valid(rcx)} wake_byte={ReadByte(rcx)}'
    return common


def main():
    # Retained historical implementation only. The reviewed correction selects
    # a different one-site backend and revokes this live entry point.
    raise SystemExit('DISABLED: historical x64dbg capture; EXP0002A correction requires review before live work')


def historical_main_disabled():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--operator-new-slot-ready', action='store_true')
    # HISTORICAL ONLY: obsolete SFSE-profile flag; never a current Stage-B requirement.
    parser.add_argument('--profile-sfse-only-confirmed', action='store_true', help='OBSOLETE historical-only flag; Stage B uses ordinary Steam without SFSE')
    args = parser.parse_args()
    if not (args.operator_new_slot_ready and args.profile_sfse_only_confirmed):
        parser.error('Fresh operator scene/profile confirmation required')
    if not re.fullmatch('[a-z0-9-]+',args.name) or args.pid <= 0:
        parser.error('Positive PID and simple new run name required')
    plan = json.loads(PLAN_PATH.read_text())
    expected = [0x183c590,0x166c1c3,0x1814220,0x183b86d]
    if (plan['game_sha256'] != GAME_HASH or plan['armed_seconds'] != 10
        or plan['per_site_hit_cap'] != 25 or [int(s['rva'],0) for s in plan['sites']] != expected):
        raise RuntimeError('Unreviewed plan parameters')
    protected = parents()
    debugger_files = [metadata(DEBUGGER.parent/name) for name in DEBUGGER_HASHES]
    if any(x['sha256'] != DEBUGGER_HASHES[x['filename']] for x in debugger_files):
        raise RuntimeError('Debugger identity changed')
    if any((DEBUGGER.parent/'plugins').glob('*.dp64')):
        raise RuntimeError('Unreviewed debugger plugin autoload')
    reader = ProcessRead(args.pid)
    executable = metadata(reader.path())
    if executable['sha256'] != GAME_HASH or Path(executable['path']).name.lower() != 'starfield.exe':
        raise RuntimeError('Wrong target executable')
    if reader.debugged():
        raise RuntimeError('Existing debugger; refusing attach')
    game_dir = Path(executable['path']).parent
    sfse = metadata(game_dir/'sfse_1_16_244.dll')
    if sfse['sha256'] != '28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b':
        raise RuntimeError('SFSE identity changed')
    if (game_dir/'Data/SFSE/Plugins/SorExp0002.dll').exists():
        raise RuntimeError('Retire historical observer through Vortex before this trace')
    saves = Path(protected['original']['path']).parent
    before_saves = inventory(saves)
    root = ROOT/'.local-work/exp0002a'/args.name
    if root.resolve() != root.absolute():
        raise RuntimeError('Redirected output root')
    root.mkdir()
    preflight = dict(tool=TOOL, utc=datetime.now(timezone.utc).isoformat(), pid=args.pid,
                     classification='LOCAL-ONLY', game=executable, sfse=sfse,
                     parents=protected, free=space(), saves=before_saves,
                     debugger=debugger_files, plan=metadata(PLAN_PATH), threads=thread_inventory(args.pid),
                     source=[metadata(p) for p in Path(__file__).parent.glob('*.py')],
                     observer_semver=None, observer_package=None,
                     user_reported_profile='SFSE only; historical observer retired',
                     operator_action='one ordinary new-slot manual save; no console')
    write_new(root/'preflight.json',preflight)
    t = Transport(DEBUGGER, root/'debugger')
    attached = False
    armed = []
    original = {}
    base = None
    reason = 'setup_incomplete'
    captured = []
    observed_files = []
    detached = False
    restored = False
    try:
        attached = True  # Attempted attach requires verified cleanup even on timeout.
        t.command(f'attach .{args.pid}',10)
        deadline = time.monotonic()+5
        while time.monotonic()<deadline and not any('[STATE] paused' in s for s in t.lines):
            time.sleep(.05)
        if not any('[STATE] paused' in s for s in t.lines) or not reader.debugged():
            raise RuntimeError('Attach pause not confirmed')
        if any('Breakpoint at ' in s and ' set!' in s for s in t.lines):
            raise RuntimeError('Unexpected automatic breakpoint during attach')
        lines = t.command('log "SOR_BASE {p:mod.main()} SFSE={p:sfse_1_16_244.dll}"')
        value = next(s for s in lines if s.startswith('SOR_BASE '))
        base = int(value.split()[1],16)
        if not base or int(value.split('SFSE=')[1].strip(),16) == 0:
            raise RuntimeError('Game/SFSE module unavailable')
        for site in plan['sites']:
            address = base+int(site['rva'],0)
            data = reader.read(address,32)
            if hashlib.sha256(data).hexdigest() != site['sha256']:
                raise RuntimeError('Loaded site mismatch: '+site['label'])
            original[address] = data
        write_new(root/'sites-validated.json',dict(module_base=hex(base),plan=plan))
        for site in plan['sites']:
            address = base+int(site['rva'],0)
            # Register attempted arm before issuing it, so failed acknowledgments
            # still lead to cleanup of this exact site.
            armed.append(address)
            t.command(f'bp {address:X}')
            t.command(f'SetBreakpointLog {address:X}, "{log_format(site["label"])}"')
            t.command(f'SetBreakpointCondition {address:X}, "$breakpointcounter>=19"')
        space()
        write_new(root/'prepared.json',dict(utc=datetime.now(timezone.utc).isoformat(),
                                           coordination='waiting up to 60 seconds for arm.signal'))
        print('PREPARED: paused at attach; controller must create arm.signal within 60 seconds.',flush=True)
        deadline = time.monotonic()+60
        while not (root/'arm.signal').exists():
            if time.monotonic() >= deadline:
                raise RuntimeError('Arming handoff timeout')
            if t.error or not reader.alive():
                raise RuntimeError(t.error or 'Target exited before arming')
            space()
            time.sleep(.05)
        start_index = len(t.lines)
        start = time.monotonic()
        write_new(root/'armed.json',dict(utc=datetime.now(timezone.utc).isoformat(),seconds=10,
                                        module_base=hex(base),intervention='four software execution breakpoints'))
        t.command('run')
        print('ARMED: perform the agreed ordinary NEW manual save now; 10-second window.',flush=True)
        last_inventory = before_saves
        reason = 'ten_second_bound'
        while time.monotonic()-start < 10:
            space()
            if t.error:
                raise RuntimeError(t.error)
            recent = t.lines[start_index:]
            captured = [s.strip() for s in recent if s.startswith('SOR_HIT ')]
            if any('ExceptionCode:' in s for s in recent):
                reason = 'unexpected_exception'; break
            if not reader.alive():
                reason = 'target_exited'; break
            counts = {s['label']:sum(('SOR_HIT '+s['label']+' ') in h for h in captured) for s in plan['sites']}
            if any(v>=25 for v in counts.values()):
                reason = 'hit_bound'; break
            now_files = inventory(saves)
            if now_files != last_inventory:
                observed_files.append(dict(elapsed=time.monotonic()-start,files=now_files))
                last_inventory = now_files
            if counts['NEW_SLOT_RETURN'] and counts['COMPLETION_WAKE']:
                reason = 'request_return_and_completion_candidate_observed'; break
            time.sleep(.05)
    except Exception as error:
        reason = repr(error)
    finally:
        # No forced termination. Detach plus byte restoration are independently
        # checked through read-only OS APIs, not inferred from command success.
        if attached and reader.alive():
            try:
                t.send('pause')
                for address in armed:
                    t.send(f'bc {address:X}')
                t.send('detach')
                deadline = time.monotonic()+10
                while time.monotonic()<deadline and reader.debugged():
                    time.sleep(.05)
                detached = not reader.debugged()
                restored = all(reader.read(a,32)==b for a,b in original.items()) if original else None
            except Exception as error:
                reason += '; cleanup='+repr(error)
        elif not reader.alive():
            detached = True
            restored = None  # Process exited; never claim successful restoration.
        if not detached or restored is False:
            write_new(root/'recovery-required.json',dict(reason=reason,detached=detached,restored=restored))
            print('RECOVERY REQUIRED: leave debugger/controller alive; no automatic kill/retry.',flush=True)
            while True:
                time.sleep(1)
        t.exit_detached()
        captured = [s.strip() for s in t.lines if s.startswith('SOR_HIT ')]
        try:
            protected_after = parents()
        except Exception as error:
            protected_after = {'integrity_error': repr(error)}
            reason += '; protected_parent_recheck_failed'
        result = dict(tool=TOOL,reason=reason,utc=datetime.now(timezone.utc).isoformat(),
                      hits=captured,files=observed_files,after_saves=inventory(saves),
                      parents_after=protected_after,detached=detached,site_bytes_restored=restored,
                      validated_site_count=len(original), attempted_site_count=len(armed),
                      target_alive=reader.alive(),scientific_result='UNASSESSED',
                      save_durability='NOT_ESTABLISHED',new_save_cleanup='NOT_PERFORMED')
        write_new(root/'result.json',result)
        reader.close()
        print(json.dumps({k:result[k] for k in ('reason','detached','site_bytes_restored','target_alive')},indent=2))


if __name__ == '__main__':
    main()
