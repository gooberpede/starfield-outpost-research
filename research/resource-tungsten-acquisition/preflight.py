# SPDX-License-Identifier: GPL-3.0-or-later
"""OFFLINE inventory/guard/backup audit; never launches or attaches to a game.

Reads installed definitions/config, live saves and C1D independent backups, source
pins and synthetic qualifications. Classifies live save kinds prospectively,
hashes protected saves and all historical backup records, and rehearses Save52
restoration in a new ignored scratch file. Writes a fresh local receipt, never restores
live saves or changes Cloud/config, Git, databases or prior evidence. Python
stdlib, existing Windows/Git tooling; no downloads/dependencies.
"""
import argparse
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import datetime

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-tungsten-acquisition'
sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
from saves import inventory, SAVES, EXPECTED
from collect import pin, write
from save_policy import load_policy, policy_hash, snapshot, partition, admission
from protection import audit, sync_snapshot

GAME = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--qualification', type=Path, required=True)
    ap.add_argument('--name', required=True)
    a = ap.parse_args()
    assert a.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in a.name)
    assert subprocess.check_output(['powershell','-NoProfile','-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() == '0'
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/')) >= 40_000_000_000
    out = LOCAL / a.name
    out.mkdir(exist_ok=False)
    build = a.build.resolve()
    assert build.is_relative_to(LOCAL)
    manifest = json.loads((build/'build.json').read_text())
    assert manifest['exit_code'] == 0
    for p,h in manifest['files'].items():
        assert pin(p) == h, p
    q = json.loads(a.qualification.read_text())
    assert q['passed'] is True
    assert q['build_sha256'] == pin(build/'build.json') and len(q['cases']) == 46 and all(not c['errors'] for c in q['cases'])
    policy = load_policy()
    protection = audit(policy)
    sync = sync_snapshot(policy)
    write(out/'protected-audit.json', protection)
    write(out/'sync-audit.json', sync)
    assert not protection['changes'] and sync['matches_historical']
    exe = GAME/'Starfield.exe'
    assert pin(exe) == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    definitions = {str(p):dict(bytes=p.stat().st_size,sha256=pin(p))
        for p in (GAME/'Data').iterdir() if p.suffix.lower() in ('.esm','.esp','.esl')}
    assert definitions[str(GAME/'Data/Starfield.esm')]['sha256'] == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    config = {}
    for folder in (GAME, Path('C:/Users/User/Documents/My Games/Starfield'),Path('C:/Users/User/AppData/Local/Starfield')):
        for p in folder.iterdir():
            if p.is_file() and (p.suffix.lower()=='.ini' or p.name.lower() in ('plugins.txt','loadorder.txt')):
                config[str(p)] = pin(p)
    approved_installed = json.loads((ROOT/'.local-work/resource-carinae/pilot-preflight02/preflight.json').read_text())
    assert definitions == approved_installed['definitions'] and config == approved_installed['config']
    previous = json.loads((ROOT/'.local-work/resource-oracle-retail/preflight-saves.json').read_text())
    live = snapshot(SAVES, policy)
    backup_path = Path(previous['backup_path'])
    backup = inventory(backup_path)
    result = admission(live, backup, previous['backup'], policy)
    write(out/'save-corpus-diagnostic.json', dict(live=live, backup=backup, historical=previous['backup'], policy=policy, result=result))
    assert result['ok'], result
    n = next(name for name, row in policy['designated'].items() if row['sha256'] == EXPECTED)
    assert live[n] == backup[n] and live[n]['sha256'] == EXPECTED
    scratch = out/'restore-rehearsal.sfs'
    shutil.copyfile(backup_path/n,scratch)
    assert pin(scratch) == EXPECTED
    b=exe.read_bytes();nt=struct.unpack_from('<I',b,60)[0]
    count=struct.unpack_from('<H',b,nt+6)[0];opt=struct.unpack_from('<H',b,nt+20)[0]
    sections=[struct.unpack_from('<8sIIIIIIHHI',b,nt+24+opt+i*40) for i in range(count)]
    def at(rva,n):
        for s in sections:
            if s[2]<=rva and rva+n<=s[2]+s[3]:
                return b[s[4]+rva-s[2]:s[4]+rva-s[2]+n]
        raise ValueError('unmapped RVA')
    guards={hex(r):at(r,16).hex() for r in (0x21e07d0,0x21e1772,0x21e174e,0x21e0bf4,0x79b520,0x79be20,0x79ff1d)}
    for r,dest in ((0x21e0a46,0x21e0f50),(0x21b6931,0x21e07d0),(0x21e0bf4,0x12ed2a0)):
        c=at(r,5);assert c[0]==0xe8 and r+5+struct.unpack_from('<i',c,1)[0]==dest
    assert at(0x21e174e,4)==bytes.fromhex('4883c330')
    assert at(0x21e1772,4)==bytes.fromhex('488b5e08')
    write(out/'preflight.json', dict(schema='sor-d4a-preflight/2',save_policy=policy,save_policy_sha256=policy_hash(policy),
        protected_live=partition(live,policy)['protected'],status='OFFLINE_CHECKED_NOT_AUTHORIZED', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        build_sha256=pin(build/'build.json'), controller_sha256=pin(build/'sor-d4a-controller.exe'),
        qualification_sha256=pin(a.qualification), guards=guards,definitions=definitions,config=config,
        code_pins={str(p):pin(p) for p in (ROOT/'research/resource-tungsten-acquisition').glob('*.py')},
        exe_sha256=pin(exe),live=live,backup=backup,backup_path=str(backup_path),live_path=str(SAVES),
        protected_audit_sha256=pin(out/'protected-audit.json'),sync=sync,
        save52=n,restore_rehearsal_sha256=pin(scratch),cloud_current='UNKNOWN_REQUIRES_FRESH_OPERATOR_CONFIRMATION',
        free_bytes={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}))
    print(out, 'offline only', len(live), 'live and backup saves',len(definitions),'definitions')


if __name__ == '__main__':
    main()
