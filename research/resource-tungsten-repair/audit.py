# SPDX-License-Identifier: GPL-3.0-or-later
"""D4B offline integrity and receipt audit, using owned D4A/D1 readers.

Reads existing source ledgers, receipts and protection manifests. Writes fresh
ignored JSON only. Requires game absence and both-drive free space. No target,
save, database, configuration, network or Git mutation. Run before/after tests.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/resource-tungsten-repair'
sys.path.insert(0, str(ROOT / 'research/resource-tungsten-acquisition'))
from qualify import independent
import protection


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=['before', 'after'])
    ap.add_argument('--label')
    args = ap.parse_args()
    label = args.label or args.phase
    assert label and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    assert subprocess.check_output(['powershell', '-NoProfile', '-Command',
        '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() == '0'
    ledgers = ['docs/experiments/resource-tungsten-acquisition/phase-b-sources.csv',
               'docs/experiments/resource-save52-d3/sources.csv']
    pins = {}
    for ledger in ledgers:
        for row in csv.DictReader((ROOT / ledger).open(encoding='utf8')):
            path = ROOT / row['path']
            assert pin(path) == row['sha256'], str(path)
            pins[str(path)] = row['sha256']
    frozen_roots = ('resource-save52', 'resource-save52-d3', 'resource-standalone')
    for folder in frozen_roots:
        for path in (ROOT / '.local-work' / folder).rglob('*'):
            if path.is_file():
                pins[str(path)] = pin(path)
    attempt = ROOT / '.local-work/resource-tungsten-acquisition/retail-attempt01'
    events = [json.loads(line) for line in (attempt / 'events.jsonl').read_text().splitlines()]
    session = next(r for r in events if r['kind'] == 'SESSION')
    samples = [r for r in events if r['kind'] == 'SAMPLE']
    assert len(samples) == 3027
    for row in samples:
        path = attempt / f'capture-{row["capture"]:05d}.bin'
        s, got, end = independent(path)
        assert s == session and got == row and end['complete']
        pins[str(path)] = pin(path)
        pins[str(path.with_suffix('.ack.json'))] = pin(path.with_suffix('.ack.json'))
    acks = [r for r in events if r['kind'] == 'ACK_ACCEPTED']
    assert [r['capture'] for r in acks] == list(range(1,3028)) and all(r['accepted'] for r in acks)
    protected = protection.audit()
    write(OUT / f'protected-{label}.json', protected)
    assert not protected['changes']
    identity = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    index_sha256=pin(ROOT / '.git/index'))
    if args.phase == 'before':
        write(OUT / 'baseline.json', dict(**identity, pins=pins,
            status=subprocess.check_output(['git', 'status', '--short'], text=True)))
    else:
        before = json.loads((OUT / 'baseline.json').read_text())
        assert all(before[k] == identity[k] for k in identity)
        assert before['pins'] == pins
    write(OUT / f'audit-{label}.json', dict(**identity, protected_changes=0,
        pinned_files=len(pins), receipts=3027, framed_records=9081, acknowledged=3027,
        tail=events[-4:], game_absent=True))
    print(args.phase, len(pins), 'pins; 3027 receipts; protected changes 0')


if __name__ == '__main__':
    main()
