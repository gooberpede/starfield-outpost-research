# SPDX-License-Identifier: GPL-3.0-or-later
"""Record a bounded D5B control suffix and disk metadata, never target memory.

Reads at most 65536 journal bytes plus filesystem/process-exit receipt metadata.
Appends one fsynced local health record and prints it. Python stdlib only. No
scientific raw-field interpretation, save scan, game input, target access, STOP,
configuration, network or Git mutation. The controller retains its own guards.
"""
from pathlib import Path
import datetime
import json
import os
import shutil

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'.local-work/resource-combined-acquisition'
journal=LOCAL/'retail-attempt01/events.jsonl'
with journal.open('rb') as stream:
    size=journal.stat().st_size
    stream.seek(max(0,size-65536))
    data=stream.read(65536)
controls=[]
for line in data.splitlines():
    try:
        row=json.loads(line)
        if row['kind'] in ('ACK_ACCEPTED','STOP_COMMITTED','EXIT','LOSS','EXCEPTION'):
            controls.append({k:row[k] for k in ('kind','capture','accepted','reason','code') if k in row})
    except (ValueError,KeyError):
        pass
value=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    scope='Bounded control suffix and filesystem metadata only',journal_bytes=size,
    last_control=controls[-4:],wrapper_exit=(LOCAL/'pilot-wrapper-exit01.json').exists(),
    free_bytes={drive:shutil.disk_usage(drive).free for drive in ('C:/','D:/')})
with (LOCAL/'pilot-health01.jsonl').open('a',encoding='utf8',newline='\n') as stream:
    stream.write(json.dumps(value)+'\n')
    stream.flush()
    os.fsync(stream.fileno())
print(json.dumps(value,indent=2))
