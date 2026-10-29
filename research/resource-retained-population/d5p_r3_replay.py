# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay historical R2 bytes and damage only R3-owned disposable derivatives.

Reads existing R2 capture/receipts and R3 unchanged-DLL context outputs. Writes
one fresh ignored replay child with damaged copies and oracle results. Uses the
owned schema-2 decoder and CPython stdlib. No native execution, original writes,
game, deployment, save/configuration operations, downloads or Git writes.
"""
import json
from pathlib import Path
import re
import shutil
import sys
from d5p_r2_retail_analysis import analyze
from d5p_r2_diagnostics import ROOT, DLL, capture


def main():
    label = sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+', label)
    out = ROOT / '.local-work/d5p-r3' / label
    out.mkdir(exist_ok=False)
    result = analyze(ROOT / '.local-work/d5p-r2-retail')
    # JSON object keys are strings on disk; normalize in-memory integer keys.
    assert json.loads(json.dumps(result)) == json.loads((ROOT / '.local-work/d5p-r2-retail/analysis.json').read_text())
    damage = {}
    for name in ('torn-tail', 'corrupt-first', 'torn-ack', 'wrong-dll'):
        target = out / name / 'context-reasons'
        target.mkdir(parents=True)
        for filename in ('events.bin', 'identity.json', 'flush.jsonl'):
            shutil.copyfile(ROOT / '.local-work/d5p-r3/qualification01/context-reasons' / filename, target / filename)
        raw, ack, identity = (target / p for p in ('events.bin', 'flush.jsonl', 'identity.json'))
        if name == 'torn-tail':
            raw.write_bytes(raw.read_bytes() + b'abc')
        elif name == 'corrupt-first':
            data = bytearray(raw.read_bytes())
            data[100] ^= 1
            raw.write_bytes(data)
        elif name == 'torn-ack':
            ack.write_bytes(ack.read_bytes()[:-2])
        else:
            identity.write_text(identity.read_text().replace(DLL, '0' * 64), encoding='utf8', newline='\n')
        try:
            decoded = capture(target)
            assert decoded['authentication']['errors']
            assert len(decoded['diagnostics']) == (16 if name == 'torn-tail' else 0)
            damage[name] = dict(diagnostics=len(decoded['diagnostics']),
                                authentication=decoded['authentication']['record_authentication'])
        except ValueError:
            assert name == 'wrong-dll'
            damage[name] = 'REFUSED'
    with (out / 'replay.json').open('x', encoding='utf8', newline='\n') as stream:
        json.dump(dict(r2_exact_reduction=True, records=result['records'], demands=result['demands'],
                       extent_groups=result['extent_groups'], damage=damage), stream, indent=2)
        stream.write('\n')
    print(out)


if __name__ == '__main__':
    main()
