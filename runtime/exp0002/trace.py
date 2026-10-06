#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Future Gate B only: bound one approved diagnostic using completed A2R identity.

Reads local build/ready/checkpoint records. Runs original Windows debugger,
creates explicit TRACE request after its armed marker, waits for its bounded
completion. Never launches/kills Starfield, touches saves, or deploys anything.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import time

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--session',type=Path,required=True)
    p.add_argument('--build',type=Path,required=True)
    p.add_argument('--gate-b-approved',action='store_true')
    p.add_argument('--separate-diagnostic-approved',action='store_true')
    p.add_argument('--operator-settled',action='store_true')
    a=p.parse_args()
    if not (a.gate_b_approved and a.separate_diagnostic_approved and a.operator_settled):p.error('Separate live diagnostic authority and explicit settled confirmation required; nothing executed')
    shell=shutil.which('pwsh')
    if not shell:raise RuntimeError('Existing PowerShell 7 required; no install or policy change is performed')
    root=Path(__file__).resolve().parents[2]
    if a.session.resolve().parent!=root/'.local-work/exp0002-live':raise ValueError('Wrong session root')
    def read(name):return json.loads((a.session/name).read_text(encoding='utf-8'))
    ready=read('ready.json');checkpoint=read('A2R.json')
    if checkpoint['terminal']!='CHECKPOINT_COMPLETE' or read('complete.json')['terminal']!='CHECKPOINT_SEQUENCE_COMPLETE':raise ValueError('Complete checkpoint sequence required')
    if (a.session/'failure.json').exists() or (a.session/'trace-armed.json').exists():raise ValueError('Failed/previous trace session; no retry')
    build=json.loads((a.build/'build.json').read_text(encoding='utf-8'))
    exe=a.build/'workshop-trace.exe'
    if hashlib.sha256(exe.read_bytes()).hexdigest()!=build['trace_sha256'] or ready['observer_sha256']!=build['plugin_sha256']:raise ValueError('Build identity mismatch')
    selected=[x for x in checkpoint['references'] if x['role']=='storage']
    if len(selected)!=1:raise ValueError('Exactly one selected storage required')
    identity=selected[0]['snapshot']['identity']
    args=[str(exe),'--gate-b-approved',str(ready['pid']),str(checkpoint['thread_id']),identity['pointer'],identity['form_id'],str(a.session.resolve()),'one-operation']
    with (a.session/'trace-console.txt').open('xb') as log:
        process=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT)
        start=time.monotonic()
        while not (a.session/'trace-armed.json').exists() and process.poll() is None and time.monotonic()-start<6:time.sleep(.02)
        try:
            if (a.session/'trace-armed.json').exists() and process.poll() is None:
                subprocess.run([shell,'-NoProfile','-File',str(Path(__file__).with_name('request.ps1')),'-Session',str(a.session),'-Checkpoint','TRACE','-GateBApproved','-OperatorSettled','-SeparateDiagnosticApproved'],check=True,timeout=3)
        finally:
            # Do not kill debugger or target if an OS cleanup call stalls.
            try:status=process.wait(timeout=12)
            except subprocess.TimeoutExpired:raise RuntimeError('Debugger has not exited; preserve evidence and request operator recovery, no automatic kill')
    if status:raise RuntimeError(f'Diagnostic incomplete, exit {status}; see trace.jsonl/trace-console.txt')
    print('Trace terminal written; scientific interpretation and target outcome still require review.')

if __name__=='__main__':main()
