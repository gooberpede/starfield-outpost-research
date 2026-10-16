# SPDX-License-Identifier: GPL-3.0-or-later
"""Original independent physical-record checks for the bounded interval study.
Reads inventory03, pinned ESM, owned historical catalog/cache, current CSVs and
protected/baseline manifests. Writes exclusive ignored verification JSON. No
target, save, configuration, database, index, network or installation mutation.
Stdlib CPython, repo cwd; uses owned catalog for independent category selection.
"""
from pathlib import Path
import argparse
import csv
import difflib
import hashlib
import json
import os
import struct
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from extractor_resources import definition_catalog
from inventory_historical_saves import guard


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True)
    args = ap.parse_args(); assert args.run.isalnum()
    base = ROOT/'.local-work/e1-intervals'; guard()
    inv = json.loads((base/'inventory03.json').read_text())
    esm = Path(inv['source']['path'])
    assert sha(esm) == inv['source']['sha256']
    checked = {}

    def record(offset, fid, kind):
        if fid in checked:
            return checked[fid]['fields']
        with esm.open('rb') as f:
            f.seek(offset); h = f.read(24)
            assert h[:4].decode() == kind and struct.unpack_from('<I', h, 12)[0] == fid
            n, flags = struct.unpack_from('<II', h, 4); assert n <= 16*1024*1024
            b = f.read(n); assert len(b) == n
        compressed = bool(flags & 0x40000)
        if compressed:
            size = struct.unpack_from('<I', b)[0]
            assert size <= 16*1024*1024
            raw = zlib.decompress(b[4:]); assert len(raw) == size; b = raw
        pos = 0; fs = {}; spans = []
        while pos < len(b):
            assert pos + 6 <= len(b)
            tag = b[pos:pos+4].decode(); count = struct.unpack_from('<H', b, pos+4)[0]; pos += 6
            if tag == 'XXXX':
                assert count == 4
                count = struct.unpack_from('<I', b, pos)[0]; tag = b[pos+4:pos+8].decode(); pos += 10
            assert pos + count <= len(b)
            fs.setdefault(tag, []).append(b[pos:pos+count])
            spans.append(dict(tag=tag, length=count, offset=pos if compressed else offset+24+pos,
                              domain='decompressed record payload' if compressed else 'physical ESM'))
            pos += count
        assert pos == len(b)
        checked[fid] = dict(formid=fid, offset=offset, type=kind, fields=fs, field_spans=spans)
        return fs

    def get(fs, k):
        assert len(fs[k]) == 1
        return fs[k][0]

    def integer(fs, k):
        b = get(fs, k); assert len(b) == 4
        return int.from_bytes(b, 'little')

    resources = inv['resources']; extractors = inv['container_candidates']
    assert len(resources) == 47 and len(extractors) == 154
    resource_ids = {r['formid'] for r in resources}
    assert len(resource_ids) == 47
    for r in resources:
        fs = record(r['offset'], r['formid'], 'IRES')
        assert integer(fs, 'NAM1') == r['resource_av']
        assert integer(fs, 'NAM2') == r['production_recipe']
        assert integer(fs, 'NAM3') == r['interval_global']
        av = record(r['av_offset'], r['resource_av'], 'AVIF')
        assert struct.unpack('<f', get(av, 'NAM0'))[0] == 0
        gf = record(r['global_offset'], r['interval_global'], 'GLOB')
        raw = get(gf, 'FLTV'); assert raw.hex() == r['hours_bytes']
        seconds = struct.unpack('<f', struct.pack('<f', struct.unpack('<f', raw)[0]*3600))[0]
        assert seconds == r['seconds']
        rf = record(r['recipe_offset'], r['production_recipe'], 'COBJ')
        assert integer(rf, 'CNAM') == r['product']
        assert get(rf, 'NNAM') == b'\x01\x00'
        pf = record(r['product_offset'], r['product'], 'MISC')
        assert get(pf, 'EDID').rstrip(b'\0').decode() == r['product_edid']
    for b in extractors:
        fs = record(b['offset'], b['formid'], 'CONT')
        assert integer(fs, 'KSIZ')*4 == len(get(fs, 'KWDA'))
        assert 0x8406 in struct.unpack('<'+'I'*(len(get(fs, 'KWDA'))//4), get(fs, 'KWDA'))
        assert len(b['resource_avs']) == 1
        av = b['resource_avs'][0]
        ps = b''.join(fs.get('PRPS', [])); assert len(ps) % 12 == 0
        rows = {struct.unpack_from('<I', ps, p)[0]:ps[p:p+12] for p in range(0, len(ps), 12)}
        assert rows[av].hex() == b['properties'][str(av)]['bytes']
        assert struct.unpack_from('<f', rows[av], 4)[0] == 1
        tier = b['tier_by_edid']; assert tier in {1, 2, 3}
        value = b['properties'].get('33799')
        if tier == 1:
            solid = 'OutpostHarvesterSolid_' in b['edid']
            assert (value is None) if solid else (value['value'] == 1)
            assert (0x8407 not in rows) if solid else (rows[0x8407].hex()==value['bytes'] and struct.unpack_from('<f',rows[0x8407],4)[0]==1)
            assert ('Driller01.nif' in b['model']) if solid else ('Small01.nif' in b['model'] or 'GasExtractor.nif' in b['model'])
        else:
            assert value['bytes'] == rows[0x8407].hex()
            assert value['value'] == struct.unpack('<f', bytes.fromhex('cdcc4cbe' if tier == 2 else '000000bf'))[0]
            assert ('Medium01.nif' if tier == 2 else 'Large01.nif') in b['model']
    cache_path = ROOT/'.local-work/extractor-resource/run01/static-records.json'
    cache = json.loads(cache_path.read_text())
    catalog = definition_catalog(cache['records'])
    expected = {int(k.split(':')[1], 16) for k in catalog if k.startswith('starfield.esm:')}
    assert expected == {b['formid'] for b in extractors}
    # All main-game IRES, including exclusions, match an earlier independently
    # collected catalog. No claim of DLC/mod override compatibility follows.
    cached_ids = {r['formid'] for r in cache['records'] if r['plugin']=='Starfield.esm' and r['type']=='IRES'}
    assert cached_ids == resource_ids | {r['formid'] for r in inv['excluded_ires']}
    for p in inv['dependencies']:
        assert sha(Path(p['path'])) == p['sha256']
    for r in json.loads((base/'protected-before.json').read_text()):
        p = Path(r['path']); assert p.stat().st_size == r['size'] and sha(p) == r['sha256']
    seed = json.loads((base/'baseline.json').read_text())
    assert sha(ROOT/'.git/index') == seed['index']['sha256']
    assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')).decode().strip() == seed['head']
    for r in seed['files']:
        p = Path(r['path']); old = (base/'baseline-tree'/p.relative_to(ROOT)).read_bytes(); new = p.read_bytes()
        assert not any(line.startswith('- ') for line in difflib.ndiff(old.decode('utf8').splitlines(True), new.decode('utf8').splitlines(True))), str(p)
    # Exact authored table inventory, not a production simulation oracle.
    rr = list(csv.DictReader((ROOT/'docs/experiments/inorganic-extractors/resource-intervals.csv').open(encoding='utf8',newline='')))
    bb = list(csv.DictReader((ROOT/'docs/experiments/inorganic-extractors/extractor-sizes.csv').open(encoding='utf8',newline='')))
    assert {int(r['ires_formid'],16) for r in rr} == resource_ids
    assert {int(b['base_formid'],16) for b in bb} == expected and len(bb) == 154
    for r in rr:
        src = next(s for s in resources if s['formid']==int(r['ires_formid'],16))
        assert float(r['base_seconds']) == src['seconds'] and int(r['interval_global'],16) == src['interval_global']
        assert int(r['ires_physical_offset']) == src['offset'] and r['hours_binary32_bytes_le'] == src['hours_bytes']
        assert int(r['resource_av'],16) == src['resource_av'] and int(r['extractor_definitions']) == len(src['extractors'])
    for r in bb:
        src = next(b for b in extractors if b['formid']==int(r['base_formid'],16))
        prop = src['properties'].get('33799',{})
        assert r['edid'] == src['edid'] and int(r['physical_offset']) == src['offset']
        assert int(r['tier_by_edid']) == src['tier_by_edid']
        assert r['rate_property_bytes'] == prop.get('bytes','')
        assert (r['rate_property']=='absent') if not prop else (float(r['rate_property'])==prop['value'])
        assert float(r['resource_quantity_property']) == 1
        assert r['construction_recipes'] == ';'.join(f"{q['formid']:06x}" for q in src['construction_recipes'])
    assert sha(esm) == inv['source']['sha256']; guard()
    for r in checked.values():
        del r['fields']
    result = dict(result='PASS', physical_records=len(checked), exact_field_spans=list(checked.values()),
                  resource_rows=47, linked_resources=45, extractor_rows=154,
                  category_catalog_equal=True, ires_census_equal=True, protected_inputs=18,
                  baseline_files_preserved=len(seed['files']), head_index_unchanged=True,
                  cache_sha256=sha(cache_path), verifier_sha256=sha(Path(__file__)),
                  limitations='Static framing/definition relationships; no game execution, measured timing or inventory acceptance oracle.')
    with (base/('verification'+args.run+'.json')).open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print('PASS physical records',len(checked),'47 resources,45 linked,154 bases; category/census/preservation')


if __name__ == '__main__':
    main()
