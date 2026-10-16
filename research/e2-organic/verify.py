# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify E2 authored tables and cross-evidence joins; exclusive local receipt.
Reads local primary receipts, current installed pinned inputs, CSV/native sources.
Stdlib only; no original/save/analysis/Git writes, code invocation or network.
Requires prior E2 outputs; source hashes prove bytes, not native semantics.
"""
import argparse
import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import ROOT, pin
from inventory_historical_saves import guard

ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
args = ap.parse_args()
assert args.run.isalnum()
guard()
base = ROOT / '.local-work/e2-organic'
out = base / (args.run + '.json')
assert not out.exists()
doc = ROOT / 'docs/experiments/organic-facilities'
derived = json.loads((base/'derived02.json').read_text())
assemblies = json.loads((base/'assemblies02.json').read_text())
saved = json.loads((base/'saved02.json').read_text())
selected = json.loads((base/'selected-state02.json').read_text())
inventory = json.loads((base/'inventory02.json').read_text())
assert pin(Path(derived['source']['path'])) == derived['source']
assert pin(Path(saved['source']['path'])) == saved['source']
exe = pin(Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe'))
assert exe['sha256'] == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
assert [pin(Path(p['path'])) for p in inventory['text_sources']] == inventory['text_sources']
with (doc/'recipes.csv').open(newline='', encoding='utf8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == len(derived['resources']) == 90
assert len({r['ires'] for r in rows}) == 90
for row, r in zip(rows, derived['resources']):
    expected = dict(ires=r['formid'], edid=r['edid'], ires_physical_offset=str(r['offset']),
                    resource_av=r['av']['formid'], recipe=r['recipe']['formid'],
                    recipe_physical_offset=str(r['recipe']['offset']), product_misc=r['product']['formid'],
                    interval_global=r['interval_global']['formid'], nominal_seconds=str(r['seconds']),
                    recipe_nnam=str(r['recipe_count']), input_ires_quantities=';'.join(
                        x['formid']+':'+str(x['quantity']) for x in r['inputs']),
                    eligibility='DEFINITION_ONLY; native gates separate')
    assert row == expected
with (doc/'facilities.csv').open(newline='', encoding='utf8') as f:
    facilities = list(csv.DictReader(f))
assert len(facilities) == 6
for row, r in zip(facilities, derived['bases']):
    assert row['producer_cont'] == r['formid'] and row['edid'] == r['edid']
    assert int(row['cont_physical_offset']) == r['offset']
    assert float(row['organic_type']) == r['properties']['00000387']
    assert int(row['resource_property_count']) == len(r['resource_avs'])
    assert int(row['resource_nonzero']) == 0
    assert all(r['properties'][f'{i:08x}'] == 0 for i in r['resource_avs'])
    delta = r['properties'].get('00008407')
    assert (row['raw_harvester_delta'] == 'ABSENT') if delta is None else float(row['raw_harvester_delta']) == delta
    matches = [x for x in assemblies['references'] if x['base'] == int(r['formid'], 16)]
    assert len(matches) == 1
    ref = matches[0]
    for key, value in [('packin', ref['packin']), ('packin_cell', ref['cell']), ('template_refr', ref['formid'])]:
        assert row[key] == f'{value:08x}'
    assert int(row['template_physical_offset']) == ref['offset']
    co = next(x for x in derived['construction'] if x['formid'] == row['construction_cobj'])
    assert co['created']['formid'] == row['packin']
    assert int(row['construction_physical_offset']) == co['offset']
    project = f"{int.from_bytes(bytes.fromhex(co['conditions'][0])[12:16], 'little'):08x}" if co['conditions'] else 'NONE'
    assert row['research_project'] == project
by_ires = {'starfield.esm:' + r['formid'][2:]: r for r in derived['resources']}
av = {p['reference_identities'][0]: 'starfield.esm:' + by_ires[g['resource']]['av']['formid'][2:]
      for g in saved['organic_groups'] for p in g['producers']}
assert len(av) == len(selected['rows']) == 6
for row in selected['rows']:
    assert av[row['identity']] == row['selected_av'] and row['selected_value'] == 1.0
edges = {tuple(e) for e in saved['directed_edges']}
for trace in saved['upstream_water_traces']:
    assert trace['water_producer_paths']
    for path in trace['water_producer_paths']:
        assert path[0] == trace['producer']
        assert all((source, destination) in edges for destination, source in zip(path, path[1:]))
added = json.loads((base/'register-additions01.json').read_text())['added']
central = list(csv.DictReader((ROOT/'docs/experiments/native-availability-map/functions.csv').open(newline='', encoding='utf8')))
assert len({r['key'] for r in central}) == len(central)
for row in added:
    actual = next(r for r in central if r['key'] == row['key'])
    assert actual == row
    address = row['static_va'][2:]
    assert int(row['static_va'], 16) - 0x140000000 == int(row['rva'], 16)
    assert 'FUNCTION\t'+address+'\t' in (ROOT/row['source']).read_text()
result = dict(status='PASS', executable=exe, source=derived['source'], save=saved['source'],
              recipe_rows=90, facility_rows=6, physical_records_checked=derived['physical_records_checked'],
              csv_recipe_signatures_checked=derived['csv_recipe_signatures_checked'],
              selected_saved_av_joins=6, upstream_water_traces=6, native_register_rows=len(added),
              tool=pin(Path(__file__)), limits=['No runtime execution or actual inventory measurement',
              'Semantic native claims require instruction review; hashes/table equality alone are insufficient'])
with out.open('x', encoding='utf8', newline='\n') as f:
    json.dump(result, f, indent=2); f.write('\n')
guard()
print(json.dumps({k: v for k, v in result.items() if isinstance(v, (int, str))}))
