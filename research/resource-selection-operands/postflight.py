# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only after-exit audit; writes a fresh ignored comparison, never restores.

Reads/hash-compares all live/backup saves and pinned definitions/config. Records
additions, removals and changes before reporting failure. No target, network,
Git/config/save mutation, installation or cleanup. Stdlib and existing Windows.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'.local-work/resource-selection-operands'
sys.path.insert(0,str(ROOT/'research/resource-oracle-retail'))
from saves import inventory
from collect import pin,write


def changes(before,after):
    return dict(new=sorted(set(after)-set(before)),missing=sorted(set(before)-set(after)),
                changed=[n for n in before.keys() & after.keys() if before[n]!=after[n]])


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--preflight',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    assert a.output.resolve().is_relative_to(LOCAL)
    assert subprocess.check_output(['powershell','-NoProfile','-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'],text=True).strip()=='0'
    pre=json.loads(a.preflight.read_text())
    live=inventory(Path(pre['live_path']));backup=inventory(Path(pre['backup_path']))
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    definitions={str(p):dict(bytes=p.stat().st_size,sha256=pin(p)) for p in (game/'Data').iterdir()
        if p.suffix.lower() in ('.esm','.esp','.esl')}
    config={}
    for folder in (game,Path('C:/Users/User/Documents/My Games/Starfield'),Path('C:/Users/User/AppData/Local/Starfield')):
        for p in folder.iterdir():
            if p.is_file() and (p.suffix.lower()=='.ini' or p.name.lower() in ('plugins.txt','loadorder.txt')):
                config[str(p)]=pin(p)
    result=dict(preflight_sha256=pin(a.preflight),live=live,backup=backup,
        live_changes=changes(pre['live'],live),backup_changes=changes(pre['backup'],backup),
        definitions=definitions,config=config,
        definition_changes=changes(pre['definitions'],definitions),config_changes=changes(pre['config'],config),
        changed_exe=pin('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')!=pre['exe_sha256'],
        restoration='NONE_PERFORMED_REQUIRES_NAMED_AUTHORITY')
    write(a.output,result)
    print(a.output,result['live_changes'],result['backup_changes'])
    assert not any(result['live_changes'].values()) and not any(result['backup_changes'].values())
    assert not any(result['definition_changes'].values()) and not any(result['config_changes'].values())
    assert not result['changed_exe']


if __name__=='__main__':
    main()
