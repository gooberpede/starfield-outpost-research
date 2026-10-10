# SPDX-License-Identifier: GPL-3.0-or-later
"""Write one explicit settled operator checkpoint; never reads/writes game data.

Reads ready.json in a selected session, writes an exclusive .request via atomic
rename. stdlib only. STOP is a cooperative observer stop, not a game exit.
"""
import argparse
import json
import os
from pathlib import Path
import re

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('session',type=Path)
    p.add_argument('label')
    p.add_argument('--settled',action='store_true')
    a=p.parse_args()
    ready=json.loads((a.session/'ready.json').read_text())
    version=json.loads(Path(__file__).with_name('version.json').read_text())['version']
    if ready.get('version')!=version or not ready.get('ready'):
        raise ValueError('Wrong or incomplete session')
    if a.label=='STOP':
        with (a.session/'STOP').open('xb') as f:f.write(b'STOP\n');f.flush();os.fsync(f.fileno())
        return
    if not a.settled or not re.fullmatch(r'[A-Za-z0-9_-]{1,96}',a.label):
        raise ValueError('Explicit --settled and a simple unique label are required')
    target=a.session/(a.label+'.request')
    pending=a.session/(a.label+'.pending')
    if target.exists() or (a.session/a.label).exists():raise FileExistsError(target)
    with pending.open('xb') as f:
        f.write(('SETTLED '+a.label+'\n').encode());f.flush();os.fsync(f.fileno())
    pending.rename(target)  # Windows refuses replacing an existing request.
    print(target)

if __name__=='__main__':main()
