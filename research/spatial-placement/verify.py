# SPDX-License-Identifier: GPL-3.0-or-later
"""L3 primary correspondence verifier. See README for reads/writes/authority.

Stdlib and existing owned readers only; no original/DB/Git writes. New exclusive
ignored receipt, temporary decoding scratch. Source/private payloads stay local.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import struct
import subprocess
import sys

R = Path.cwd()
W = R / '.local-work/l3-placement'
sys.path[:0] = [str(R / 'save-analysis/scripts')]
from inventory_historical_saves import guard
from stream_save import decoded_save
from workshop_inventory import audit, ownership_ledger, constructed_inventory
from workshop_population import typed_records
from validate_mature_outposts import directory
from test_outpost_record_framing import independent
from inspect_outpost_definitions import esm_records


def pin(p):
    p = Path(p)
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert re.fullmatch('[A-Za-z0-9-]+', a.run)
    out = W / (a.run + '.json')
    assert not out.exists()
    guard()
    seed = json.loads((W / 'baseline.json').read_text())
    checks = []

    def check(label, value):
        checks.append(label)
        assert value, label

    for p in seed['protected'] + [seed['index'], seed['brief']]:
        check('protected:' + p['path'], pin(p['path']) == p)
    check('HEAD', subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == seed['head'])
    for row in seed['inputs'] + seed['screenshots']:
        for kind in ['source', 'copy']:
            check(kind + ':' + row[kind]['path'], pin(row[kind]['path']) == row[kind])
        check('copy-readonly:' + row['copy']['path'], bool(Path(row['copy']['path']).stat().st_file_attributes & 1))
    check('six-originals', len(seed['inputs']) == 6)
    check('eleven-witnesses', len(seed['screenshots']) == 11)

    samples = list(csv.DictReader((R / 'docs/experiments/spatial-placement/samples.csv').open(encoding='utf8')))
    observed = []
    for row in samples:
        x = json.loads((W / (row['label'] + '.json')).read_text())
        with decoded_save(Path(x['source']['copy']['path']), W / 'scratch', seconds=float('inf')) as (b, metrics):
            check(row['label'] + ':hash', metrics['decoded_sha256'] == row['decoded_sha256'])
            check(row['label'] + ':build-format-buffer', b.find(b'1.16.244.0') >= 0 and struct.unpack_from('<I', b, 16)[0] == 27 and b[20] == 153)
            d = directory(b)
            arithmetic = independent(b, *d['regions']['region_R3'], d['words'][9])
            raw = audit(b)
            check(row['label'] + ':independent-framing', [(r['offset'], r['end'], r['token'], r['change_flags']) for r in raw['records']] == [r[:4] for r in arithmetic])
            inv = constructed_inventory(ownership_ledger(raw, None), None)
            check(row['label'] + ':positive-roots', inv['constructed_instances'] == x['inventory']['constructed_instances'])
            records = list(typed_records(b))
            bulldozed = [r for r in records if r['form_type'] == 0x4a and r['flags'] & 0x1000000]
            check(row['label'] + ':counts', len(records) == int(row['framed_records']) and len(bulldozed) == int(row['bulldozed_channel']) and len(inv['constructed_instances']) == int(row['supported_roots']))
            for beacon in x['beacons']:
                rec, p = beacon['record'], beacon['prefix']
                check(row['label'] + ':beacon-position', list(struct.unpack_from('<3f', b, rec['body'] + 1)) == p['xyz'])
                check(row['label'] + ':beacon-flags', struct.unpack_from('<IH', b, p['saved_flags_offset']) == (p['saved_form_flags'], p['saved_aux_flags']))
                for extra in beacon['extras']['extras']:
                    if extra['type'] == 'bf':
                        for section in extra['sections']:
                            for v in section['values']:
                                check(row['label'] + ':BF:' + v['av'], struct.unpack_from('<f', b, v['offset'])[0] == v['value'])
            observed.append(dict(sample=row['label'], framed=len(records), roots=len(inv['constructed_instances']), bulldozed_channel=len(bulldozed), decoded_sha256=metrics['decoded_sha256']))

    esm = next(Path(p['path']) for p in seed['protected'] if Path(p['path']).name == 'Starfield.esm')
    defs = json.loads((W / 'definition-details01.json').read_text())
    ids = {r['formid'] for r in defs}
    fresh = {h['formid']: (h, fs) for h, fs in esm_records(esm, {b'PKIN', b'ACTI', b'STAT', b'DFOB', b'AVIF', b'KYWD'}, repeated=True) if h['formid'] in ids}
    for rec in defs:
        h, fs = fresh[rec['formid']]
        check('physical-definition:' + hex(rec['formid']), h['offset'] == rec['offset'] and [(k.decode(), v.hex()) for k, v in fs] == [tuple(v) for v in rec['fields']])
    prps = dict(fresh[0x2c60e9][1])[b'PRPS']
    props = {struct.unpack_from('<I', prps, i)[0]: struct.unpack_from('<f', prps, i + 4)[0] for i in range(0, len(prps), 12)}
    check('ordinary-definition-radius150', props[0x63fc5] == 150.0)

    register = list(csv.DictReader((R / 'docs/experiments/spatial-placement/functions.csv').open(encoding='utf8')))
    seen = {}
    for row in register:
        path = R / row['source']
        if path not in seen:
            seen[path] = path.read_text()
            check('native-source:' + row['source'], pin(path)['sha256'] == row['source_sha256'])
            check('native-build:' + row['source'], 'SHA256\t' + next(p['sha256'] for p in seed['protected'] if Path(p['path']).name == 'Starfield.exe') in seen[path])
        lines = seen[path].splitlines()
        check('native-locator:' + row['va'], lines[int(row['first_line']) - 1].startswith('FUNCTION\t' + row['va'] + '\t') and int(row['last_line']) <= len(lines))
    # Independent required native chain correspondence, not a semantic simulator.
    required = {
        '017': ['0x1000000', '0xd3', 'FUN_140f30380'],
        '021': ['>> 0x18 & 1', 'cVar10 << 2'],
        '026': ['fVar2 * fVar2 + fVar1 * fVar1 <= param_3 * param_3', 'OutpostNoPlacement'],
    }
    for n, words in required.items():
        text = (W / 'native' / (n + '.request.tsv')).read_text()
        for word in words:
            if word == 'OutpostNoPlacement':
                text = (W / 'native/019.request.tsv').read_text()
            check('native-contract:' + n + ':' + word, word in text)
    check('index-after', pin(seed['index']['path']) == seed['index'])
    guard()
    result = dict(result='PASS', checks=checks, count=len(checks), observations=observed,
                  verifier=pin(Path(__file__)), head=seed['head'],
                  limits='Primary correspondence only; no physics execution, live reload, photograph/reference join or independent semantic acceptance.')
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print('PASS', len(checks), out)


if __name__ == '__main__':
    main()
