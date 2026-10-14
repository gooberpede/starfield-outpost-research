"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline identity/definition checks, no target/database/network effects.
Read explicit owned static receipts, freshly pin input hashes, exclusively create
local result. Source ESM hashes are verified by the companion defaults scan and
save audit. No outside implementation. Record values are evidence, not placement.
"""
from pathlib import Path
import argparse
import json
import sys
import struct

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from extractor_resources import fields, one, qualified, u32, definition_catalog
from inventory_historical_saves import identity, guard

ap = argparse.ArgumentParser()
ap.add_argument('--defaults', type=Path, required=True)
ap.add_argument('--run', required=True)
args = ap.parse_args()
if not args.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
guard()
cache = ROOT/'.local-work/extractor-resource/run01/static-records.json'
before = {str(p): identity(p) for p in (cache, args.defaults)}
source = json.loads(cache.read_text(encoding='utf8'))
defaults = json.loads(args.defaults.read_text(encoding='utf8'))
records = source['records']
masters = {r['plugin'].lower(): [v.rstrip(b'\0').decode('utf8').lower() for v in fields(r,'MAST')]
           for r in records if r['type'] == 'TES4'}
flags = {r['plugin'].lower():r['flags'] for r in records if r['type'] == 'TES4'}
def key(r): return qualified(r['plugin'].lower(), r['formid'], masters[r['plugin'].lower()], flags)
def form(r, v): return qualified(r['plugin'].lower(), u32(v), masters[r['plugin'].lower()], flags)
by = {key(r):r for r in records if r['type'] != 'TES4'}
targets = {
    'OutpostCategoryHarvesters_DO': ('starfield.esm:008406','KYWD'),
    'HarvesterAtmosphere': ('starfield.esm:0083ff','AVIF'),
    'OutpostSkipResourceVeinCheck_DO': ('starfield.esm:271128','AVIF'),
    'OutpostHarvesterPlaceAnywhere_DO': ('starfield.esm:31986f','AVIF'),
    'WaterResource_DO': ('starfield.esm:0083ec','IRES'),
}
bindings = []
for name, (target, typ) in targets.items():
    matches = [r for r in defaults['records'] if r['type']=='DFOB' and r['edid']==name]
    if len(matches) != 1: raise ValueError('DEFAULT_NOT_UNIQUE:'+name)
    d = matches[0]
    if form(d, one(d,'DATA')) != target or by[target]['type'] != typ: raise ValueError('DEFAULT_TARGET:'+name)
    bindings.append(dict(name=name, dfob=key(d), dfob_offset=d['offset'], target=target,
                         target_type=typ, target_offset=by[target]['offset']))
catalog = definition_catalog(records)
xtech = []
for base in ('01662c','07e613','07e614','07e615'):
    k = 'sfbgs050.esm:'+base; r = by[k]
    props = {form(r, v[i:i+4]):struct.unpack_from('<f',v,i+4)[0]
             for v in fields(r,'PRPS') for i in range(0,len(v),12)}
    if 'starfield.esm:31986f' not in props or 'starfield.esm:271128' not in props:
        raise ValueError('XTECH_PROPERTY_CONTROL')
    a = catalog[k]['associations']
    if len(a)!=1 or a[0]['resource_identity']!='sfbgs00d.esm:033e3f': raise ValueError('XTECH_RESOURCE_JOIN')
    xtech.append(dict(base=k, offset=r['offset'], place_anywhere_present=True,
                     place_anywhere_value=props['starfield.esm:31986f'],
                     skip_vein_present=True, skip_vein_value=props['starfield.esm:271128'],
                     produced_resource=a[0]['resource_identity'],
                     placement='NOT_OBSERVED', gate='STATIC_BYPASS_IN_QUALIFIED_PROPERTY_BRANCH'))
after = {p: identity(Path(p)) for p in before}
if before != after: raise ValueError('RECEIPT_CHANGED')
out = ROOT/'.local-work/resource-availability'/(args.run+'.json')
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(dict(bindings=bindings, xtech=xtech, inputs=before, after=after,
                   script=identity(Path(__file__))), f, indent=2); f.write('\n')
guard()
print('default bindings', len(bindings), 'X-Tech controls', len(xtech))
