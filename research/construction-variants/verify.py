# SPDX-License-Identifier: GPL-3.0-or-later
"""BM1 finite offline checks; see README.md for exact reads/writes and limits."""
from pathlib import Path
import argparse
import collections
import csv
import hashlib
import json
import struct
import subprocess
import sys
import zlib

R = Path.cwd()
W = R / '.local-work/construction-variants'
D = R / 'docs/experiments/construction-variants'
sys.path[:0] = [str(R / 'save-analysis/scripts')]
from inventory_historical_saves import guard
from inspect_outpost_definitions import subrecords
from stream_save import decoded_save
from validate_mature_outposts import directory
from outpost_record_framing import Reader, iter_records
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value


def pin(path):
    path = Path(path)
    with path.open('rb') as f:
        return dict(path=str(path), bytes=path.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    out = W / ('verification-' + args.run + '.json')
    assert not out.exists()
    guard()
    checks = []

    def check(name, value):
        if not value:
            failure = W / ('failure-' + args.run + '.json')
            failure.open('x', encoding='utf8').write(json.dumps(
                dict(failed=name, prior_checks=checks), indent=2) + '\n')
        assert value, name
        checks.append(name)

    seed = json.loads((W / 'baseline.json').read_text(encoding='utf8'))
    protected = seed['protected'] + [seed['brief'], seed['index']] + seed['screenshots']
    for row in protected:
        check('protected ' + row['path'], pin(row['path']) == row)
    check('HEAD unchanged', subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']).decode().strip() == seed['head'])
    records = json.loads((W / 'definitions02.json').read_text())['records']
    records += json.loads((W / 'extra-definitions01.json').read_text())['records']
    by = {r['formid']: r for r in records}
    defs = list(csv.DictReader((D / 'definitions.csv').open(encoding='utf8')))
    esm = next(Path(p['path']) for p in seed['protected'] if Path(p['path']).name == 'Starfield.esm')
    with esm.open('rb') as f:
        for row in defs:
            r = by[int(row['formid'], 16)]
            f.seek(int(row['offset']))
            h = f.read(24)
            n, flags, fid = struct.unpack_from('<III', h, 4)
            check('physical header ' + row['formid'], h[:4].decode() == row['type'] and fid == r['formid'])
            b = f.read(n)
            if flags & 0x40000:
                size = int.from_bytes(b[:4], 'little')
                b = zlib.decompress(b[4:])
                check('decompression ' + row['formid'], len(b) == size)
            check('ordered fields ' + row['formid'],
                  [(k.decode(), v.hex()) for k, v in subrecords(b)] == [tuple(v) for v in r['fields']])
    rules = list(csv.DictReader((D / 'behavior-rules.csv').open(encoding='utf8')))
    counts = collections.Counter(r['behavior'] for r in rules)
    check('87 physical behaviors', len(counts) == 87)
    check('all behavior entry counts', all(counts[f'{r["formid"]:08x}'] == sum(
        k == 'ENAM' for k, v in r['fields']) for r in records if r['type'] == 'STBH'))
    small = [r for r in rules if r['behavior'] == '001e8d95']
    check('small wall 7 automatic 3 connected 4 unsnapped',
          collections.Counter(r['variant_category'] for r in small) ==
          {'00000000': 7, '00178b01': 3, '00068f5e': 4})
    check('unsnapped targets explicit', [r['target'] for r in small if
          r['variant_category'] == '00068f5e'] == ['001dcf7f', '001dced4', '001dd05d', '00068f6d'])
    check('medium differs', counts['001e8d94'] == 20)
    check('ordinary targets PKIN', all(r['target_type'] == 'PKIN' for r in small))
    check('airlock action3', all(r['action'] == '3' for r in rules if r['behavior'] in ['00178a51', '0027fad4']))
    check('breakable wall 4 stages', sum(k == 'DSTD' for k, v in by[0x3809d5]['fields']) == 4)
    templates = json.loads((W / 'templates02.json').read_text())
    hab = [r for r in templates['records'] if r['packin'] == 0x51f54]
    check('four actual wall templates', {r['formid'] for r in hab if r['base'] == 0x68f6d} ==
          {0x2c8c95, 0x2c8c96, 0x2c8c97, 0x2c8c98})
    check('nested middle present', any(r['base'] == 0x185b9 for r in hab))
    check('PTT2 identities are TRNS', all(by[i]['type'] == 'TRNS' for i in [0x2389ae, 0x178a46]))
    native = W / 'native'
    exports = sorted(native.glob('*.request.tsv'))
    for p in exports:
        s = p.read_text()
        check('native completed ' + p.name, p.with_name(p.name.replace('.tsv', '.done')).exists())
        check('native imported provenance ' + p.name,
              'SHA256\t' + seed['protected'][2]['sha256'] in s and 'BASE\t140000000' in s)
    n011 = (native / '011.request.tsv').read_text()
    check('B4 serializer four bytes', 'case 0xb4:' in n011 and 'case 0xcf:' in n011)
    check('DE serializer loader', 'case 0xde:' in n011 and 'FUN_140904560' in n011)
    check('stage model source/index serialization', 'case 0x53:' in n011 and 'plVar8[5] != lVar25' in n011)
    values = {}
    for line in (native / '026.request.tsv').read_text().splitlines():
        parts = line.split('\t')
        if len(parts) == 3 and parts[0] in ['144a4a8f0', '144a4a76c']:
            values[parts[0]] = int(parts[1], 16)
    check('B4 mask80 B5 mask0', values['144a4a8f0'] == 0x80)
    check('model53 mask80000000', values['144a4a76c'] & 0xffffffff == 0x80000000)
    total_rows = total_edges = total_de = 0
    for p in sorted(W.glob('saved2-*.json')):
        x = json.loads(p.read_text())
        path = Path(x['source']['path'])
        check('save original ' + x['label'], pin(path) == x['source'])
        selected = {r['record']['offset']: r for r in x['rows']}
        with decoded_save(path, W / 'verify-scratch') as (data, decoded):
            dr = directory(data)
            forms = struct.unpack_from('<' + 'I' * dr['reference_count'], data,
                                       dr['regions']['reference_u32'][0] + 4)
            plugins = plugin_tables(data)

            def resolve(token):
                return saved_form(token_value(token, forms), plugins)

            hits = 0
            for r in iter_records(data, *dr['regions']['region_R3'], dr['words'][9]):
                if r['offset'] not in selected:
                    continue
                row = selected[r['offset']]
                stored = row['record']
                check('saved envelope ' + x['label'] + ':' + str(r['offset']),
                      all(r[k] == stored[k] for k in ['token', 'flags', 'refs', 'strings', 'body', 'end']))
                check('saved identity ' + row['identity'], resolve(r['token']) == row['identity'])
                check('buffer153 ' + row['identity'], stored['buffer_version'] == 153)
                for e in row.get('extras', {}).get('extras', []):
                    check('actual extra tag ' + str(e['offset']), data[e['offset']] == int(e['type'], 16))
                    if e['type'] == 'de':
                        c = Reader(data, e['offset'] + 1, e['end'])
                        check('DE group count ' + str(e['offset']), c.count() == len(e['connections']))
                        for edge in e['connections']:
                            count = c.count()
                            pairs = [list(struct.unpack('<ii', c.take(8))) for _ in range(count)]
                            check('DE pairs ' + str(e['offset']), pairs == edge['pairs'])
                        check('DE body closure ' + str(e['offset']), c.p == c.end)
                        total_de += 1
                    if e['type'] == '4c':
                        for edge in e['entries']:
                            check('actual link mode ' + str(edge['offset']), data[edge['offset']] == edge['mode'])
                            if edge['keyword'] == 'starfield.esm:000191':
                                total_edges += 1
                hits += 1
            check('selected records all recovered ' + x['label'], hits == len(selected))
            total_rows += hits
        check('save post hash ' + x['label'], pin(path) == x['source'])
    positive = json.loads((W / 'saved2-HIST-0210.json').read_text())['rows']
    by_id = {r['identity']: r for r in positive}
    for suffix, source, target in [('a7e7', '1dcf7f', 'a78c'), ('a7e0', '1dced4', 'a78d'),
                                   ('a7de', '1dd05d', 'a78e'), ('a7d6', '1dd0b8', 'a78f')]:
        row = by_id['DYNAMIC:ff01' + suffix]
        es = row['extras']['extras']
        check('chosen PackIn ' + suffix, next(e['references'][0] for e in es if e['type'] == 'da') ==
              'starfield.esm:' + source)
        links = [v for e in es if e['type'] == '4c' for v in e['entries']]
        check('replacement and owner ' + suffix,
              any(e['keyword'] == 'starfield.esm:000191' and e['target'] == 'DYNAMIC:ff01' + target for e in links) and
              any(e['keyword'] == 'starfield.esm:054ba6' and e['target'] == 'DYNAMIC:ff01a75b' for e in links))
    for row in protected:
        check('post protected ' + row['path'], pin(row['path']) == row)
    guard()
    out.open('x', encoding='utf8', newline='\n').write(json.dumps(dict(
        checks=checks, count=len(checks), selected_rows=total_rows,
        replacement_edges=total_edges, DE_records=total_de,
        tool=pin(__file__), outcome='PASS mechanical/relationship checks; no RUNTIME validation'), indent=2) + '\n')
    print('PASS', len(checks), 'checks;', total_rows, 'selected records;', total_edges, 'replacement edges;', total_de, 'DE records')


if __name__ == '__main__':
    main()
