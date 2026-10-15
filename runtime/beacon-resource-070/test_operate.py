# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline controls only. No live session controls, game or deployed writes."""
import json
import os
from pathlib import Path
import subprocess
import sys
from build import sha
from operate import manifest,process_state,session_path,stop_control

def main(build):
    build=Path(build);h=sha(build/'build.json');m=json.loads((build/'build.json').read_text());results={}
    def check(k,v):
        if not v:raise AssertionError(k)
        results[k]='PASS'
    check('pinned_manifest_and_protected',m['version']=='0.7.0' and len(m['protected'])>100)
    try:manifest(build,'0'*64)
    except ValueError:check('manifest_mismatch_refused',True)
    else:raise AssertionError('manifest accepted wrong hash')
    try:session_path(build/'fixtures')
    except ValueError:check('non_live_control_path_refused',True)
    else:raise AssertionError('control accepted fixture')
    check('metadata_only_self_active',process_state(os.getpid(),None)=='ACTIVE')
    check('PID_creation_mismatch_distinguished',process_state(os.getpid(),0)=='ORIGINAL_GONE_PID_REUSED')
    control=build/'stop-control';control.mkdir();(control/'operator-stop.flag').write_bytes(b'RUN\n');check('STOP_preallocated_idempotent',stop_control(control).startswith('STOP_REQUESTED') and stop_control(control).startswith('STOP_REQUESTED') and (control/'operator-stop.flag').read_bytes()==b'STOP')
    output=build/'offline-preflight.json'
    r=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('operate.py')),'preflight','--build',str(build),'--manifest-sha256',h,'--out',str(output)],capture_output=True)
    check('actual_offline_preflight',r.returncode==0 and json.loads(output.read_text())['status']=='PASS_OFFLINE_PINS')
    (build/'operational-results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main(sys.argv[1])
