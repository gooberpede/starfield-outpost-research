# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline E1 verification; original project code, stdlib/project readers only.
Reads existing extractor caches, their pinned ESM/save inputs and native exports.
Checks cached CONT/AVIF/KYWD/IRES/COBJ fields directly at ESM record offsets.
Writes a new ignored receipt only; never decodes/writes saves, invokes native
code, changes analysis state, accesses a game process or downloads dependencies.
Requires repository cwd, installed CPython and the existing local evidence.
Usage: python -B research/e1-extractors/verify.py --run NAME
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from extractor_resources import definition_catalog, fields, qualified
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard


def pin(path):
    p = Path(path)
    with p.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return dict(path=str(p.resolve()), size=p.stat().st_size, sha256=digest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    if not args.run.replace('-', '').isalnum():
        raise ValueError('RUN_NAME')
    out = ROOT / '.local-work/e1-extractors' / (args.run + '.json')
    if out.exists():
        raise FileExistsError(out)
    guard()
    base = ROOT / '.local-work/extractor-resource'
    cache = base / 'run01/static-records.json'
    source = json.loads(cache.read_text())
    receipt = json.loads((base / 'run05/inputs-before.json').read_text())
    inputs = {}
    for expected in source['sources'] + receipt['saves']:
        actual = pin(expected['path'])
        assert actual['sha256'] == expected['sha256'].lower(), actual['path']
        assert actual['size'] == expected['size'], actual['path']
        inputs[actual['path']] = actual
    catalog = definition_catalog(source['records'])
    # The catalog is recomputed by the established reader; names do not select it.
    rows = [r for r in source['records'] if r['type'] in
            {'CONT', 'KYWD', 'AVIF', 'IRES', 'COBJ'}]
    defaults_path = ROOT / '.local-work/resource-availability/defaults02.json'
    defaults = [r for r in json.loads(defaults_path.read_text())['records']
                if r['type'] == 'DFOB' and r['edid'] in
                {'HarvesterRateMult', 'OutpostProductionHalted_DO'}]
    assert len(defaults) == 2
    rows += defaults
    checked = 0
    data = {Path(s['path']).name.lower(): Path(s['path']) for s in source['sources']}
    for row in rows:
        with data[row['plugin'].lower()].open('rb') as f:
            f.seek(row['offset'])
            h = f.read(24)
            n, flags, fid = struct.unpack_from('<III', h, 4)
            assert h[:4].decode() == row['type'] and fid == row['formid']
            b = f.read(n)
        if flags & 0x40000:
            size = struct.unpack_from('<I', b)[0]
            dec = zlib.decompressobj()
            b = dec.decompress(b[4:], size + 1)
            assert len(b) == size and dec.eof and not dec.unused_data and not dec.unconsumed_tail
        assert [(k.decode(), v.hex()) for k, v in subrecords(b)] == [tuple(x) for x in row['fields']]
        checked += 1
    # Retain the complete category census locally, including missing-family cases.
    masters = {r['plugin'].lower(): [v.rstrip(b'\0').decode().lower() for v in fields(r, 'MAST')]
               for r in source['records'] if r['type'] == 'TES4'}
    flags = {r['plugin'].lower(): r['flags'] for r in source['records'] if r['type'] == 'TES4'}
    selected_offsets = {(v['source_plugin'].lower(), v['record_offset']): k for k, v in catalog.items()}
    family = collections.Counter()
    selected = []
    for r in source['records']:
        key = selected_offsets.get((r['plugin'].lower(), r['offset']))
        if r['type'] != 'CONT' or key is None:
            continue
        p = r['plugin'].lower()
        kw = [qualified(p, v, masters[p], flags) for b in fields(r, 'KWDA')
              for v in struct.unpack('<' + 'I'*(len(b)//4), b)]
        families = [name for value, name in [('starfield.esm:299548', 'gas'),
                    ('starfield.esm:299549', 'solid'), ('starfield.esm:29954a', 'liquid')] if value in kw]
        family.update(families or ['missing'])
        selected.append(dict(base=key, offset=r['offset'], families=families,
                             models=[v.rstrip(b'\0').decode() for v in fields(r, 'MODL')]))
    native = [pin(p) for p in sorted((ROOT / '.local-work/recon').glob('e1-native-*.tsv'))]
    for row in native:
        text = Path(row['path']).read_text()
        assert 'SHA256\t7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28' in text
        log = Path(row['path'] + '.log').read_text(errors='replace')
        assert 'SCRIPT ERROR' not in log and 'Error running script' not in log
    after = [pin(p) for p in inputs]
    assert all(inputs[r['path']] == r for r in after)
    guard()
    result = dict(status='PASS', checked_definition_records=checked,
                  catalog_count=len(catalog), family_counts=dict(family),
                  selected=selected, inputs=list(inputs.values()),
                  cache=pin(cache), defaults_cache=pin(defaults_path), defaults=defaults,
                  native=native, script=pin(__file__),
                  limits=['No current-state or runtime validation', 'No fresh full-save decode',
                          'Cross-plugin family values are not inferred from bare local IDs'])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.open('x', encoding='utf8', newline='\n').write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', checked=checked, families=dict(family), native=len(native))))


if __name__ == '__main__':
    main()
