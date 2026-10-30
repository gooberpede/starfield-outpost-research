# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare D5U native comparison inputs and execute isolated qualified fixtures.

Reads authenticated static corpora and D5T owned fixture support. Writes only
ignored task-local inputs, logs and native receipts. Original generation runs in
separate disposable Python processes; no target, save, network, Ghidra or Git I/O.
Requires both disk floors and unchanged input pins. Fail closed on process errors.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import struct
import sys

from d5u_census import ROOT, LOCAL, inputs, resources, weights, write
sys.path.insert(0, str(ROOT/'research/resource-geometry'))
import geometry
from context import packed_seed_key


def main():
    c, cc, raster = inputs()
    census = json.loads((LOCAL/'census.json').read_text(encoding='utf8'))
    selected = [s for s in census['sources'] if s['catalogue']['raster_masks'] > 1
                or s['catalogue']['source_id'] in ('U01','U02')]
    selected = [s for s in selected if s['catalogue']['source_id'] != 'U04']
    out = LOCAL/sys.argv[1]
    out.mkdir(exist_ok=False)
    for name in ('start.py','native_probe.py','geometry.json','initial.json'):
        shutil.copyfile(ROOT/'.local-work/d5t'/name,out/name)
    shutil.copytree(ROOT/'.local-work/d5t/functions',out/'functions')
    results = []
    for source in selected:
        row = source['catalogue']
        corpus = cc if source['corpus']=='controls' else c
        chart, ax, ay, block = row['source_key'].split(':')
        chart, ax, ay = int(chart), int(ax), int(ay)
        body = corpus['bodies'][row['body'][2:]]
        w, h = row['width'],row['height']
        origin = [-200,-200]
        keys = {f'{x},{y}':packed_seed_key(chart,[ax,ay],origin,[x,y],body['system'],body['index'])
                for x in range(1,w+3) for y in range(1,h+3)}
        models = []
        masks = list(source['weights'])
        if row['source_id']=='U01':
            masks += ['1','3']  # Predeclared counterfactual equivalence control, not reachable masks.
        specifications = [(f'M{m}',int(m)) for m in masks]+[(f'M{masks[-1]}-repeat',int(masks[-1]))]
        if row['source_id']=='U26':
            specifications.insert(0,('CONTROL-adjacent-W0',0))
        for label, mask in specifications:
            ordered = [dict(resource=r['id'], rarity=r['rarity'],
                            block=corpus['generation_blocks'][r['block']]+[0,0],weight=v)
                       for r,v in zip(source['resources'],weights(corpus,source['resources'],mask))]
            if label=='CONTROL-adjacent-W0':
                bits = struct.unpack('<I',struct.pack('<f',ordered[0]['weight']))[0]
                ordered[0]['weight'] = struct.unpack('<f',struct.pack('<I',bits+1))[0]
            req = dict(source=row['source_key'],provenance='D5U fixed installed-main QS1 source-relative contract',
                       origin=origin,owner_key=int(row['body'],16),
                       clip_center=[-200+w//2*100,-200+h//2*100,0],
                       clip_half=[w//2*100+200,h//2*100+200,0],context_qualified=True,
                       order_qualified=True,cell_bounds=[1,w+3,1,h+3],ordered_resources=ordered,packed_keys=keys)
            full = geometry.populate_source(req,{int(k,16):v for k,v in corpus['constants'].items()})
            assert full['status']=='CONDITIONAL_PLANAR_SOURCE',full
            models.append(dict(label=label,mask=mask,request=req,full=full))
        model_path = out/(row['source_id']+'-model.json')
        write(model_path,dict(results=models,source=row))
        native_name = row['source_id']+'-native.json'
        env = dict(os.environ,D5S_OUTPUT=str(out))
        command = [sys.executable,'-B',str(Path(__file__).with_name('d5u_native.py')),native_name,str(model_path)]
        result = subprocess.run(command,cwd=ROOT,env=env,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        (out/(row['source_id']+'-stdout.log')).write_bytes(result.stdout)
        (out/(row['source_id']+'-stderr.log')).write_bytes(result.stderr)
        assert result.returncode==0,(row['source_id'],result.returncode,result.stderr[-2500:])
        assert not result.stderr and b'FAULT' not in result.stdout
        native = json.loads((out/native_name).read_text(encoding='utf8'))
        if row['source_id']=='U26':
            assert native['runs'][0]['weights'] != native['runs'][1]['weights']
            assert native['runs'][0]['regions'] == native['runs'][1]['regions']
        counts = [len(run['regions']) for run in native['runs']]
        results.append(dict(source_id=row['source_id'],native=native_name,model=model_path.name,counts=counts,
                            exact_model_points_bounds=True,spatial_probes=len(native['spatial_checks'])))
        print(row['source_id'],row['source_key'],counts,flush=True)
    write(out/'summary.json',results)


if __name__ == '__main__':
    main()
