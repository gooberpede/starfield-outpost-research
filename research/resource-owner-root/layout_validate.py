# SPDX-License-Identifier: GPL-3.0-or-later
"""Versioned SFPT preparation correction and complete affected offline checks.

Reads pinned installed SFPTs and frozen D1/D3 corpora/requests; writes fresh
ignored corrected corpora, isolated predictions and post-prediction comparisons.
No native answer chooses the transpose rule. Existing answers are already known;
this is source-backed diagnostic correction, not a new blinded experiment.
No target, original, analysis-content, Git or network writes. Stdlib only.
"""
import argparse
import collections
import copy
import csv
import json
from pathlib import Path
import struct
import subprocess
import sys

from audit import ROOT, pin, write
from source_layout import install_fnam
sys.path.insert(0, str(ROOT / 'research/resource-standalone'))
import builder
import predictor_d3 as predictor
import verify
from save52_compare import classify


def expanded(payload):
    result = copy.deepcopy(payload)
    result['representation'] = 'expanded'
    for bid, body in result['bodies'].items():
        body['routes'] = {}
        for tile in body['tiles']:
            chart, cx, cy = map(int, tile.split(':'))
            rows = []
            for sx in range(16):
                for sy in range(16):
                    try:
                        values = predictor.resolve(payload, payload['bodies'][bid], chart,
                                                   cx*192+sx*12, cy*192+sy*12)
                        rows.append(list(values[:5]))
                    except (ValueError, KeyError):
                        rows.append(None)
            body['routes'][tile] = rows
    del result['patterns'], result['source_blocks']
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / '.local-work')
    out.mkdir(parents=True, exist_ok=False)
    assert pin(builder.ESM) == builder.DEFINITION
    records = {h['formid']: (h, fs) for h, fs in builder.esm_records(builder.ESM,
        {b'PNDT', b'SFTR', b'SFPT', b'SFBK'}, repeated=True)}
    sources = {'D3': ROOT / '.local-work/resource-save52-d3/build-v6/normalized.json',
               'D1': ROOT / '.local-work/resource-standalone/build03/normalized.json'}
    corrected, dependency_rows = {}, []
    for label, path in sources.items():
        payload = copy.deepcopy(json.loads(path.read_text())['payload'])
        for pid, serialized in payload['patterns'].items():
            h, fields = records[int(pid, 16)]
            assert not any(t == b'EFRM' for t, b in fields), 'Partial EFRM not supported'
            ids, flags = builder.last(fields, b'FNAM'), builder.last(fields, b'GNAM')
            assert len(ids) == 1024 and len(flags) == 256
            pairs = [[f'{fid:08x}', flag] for fid, flag in zip(struct.unpack('<256I', ids), flags)]
            assert serialized == pairs, 'Frozen extraction differs from modern serialized input'
            payload['patterns'][pid] = install_fnam(pairs)
            dependency_rows.append(dict(corpus=label, pattern=pid, header=h,
                fnam_sha256=builder.hashlib.sha256(ids).hexdigest(),
                gnam_sha256=builder.hashlib.sha256(flags).hexdigest()))
        if label == 'D1':
            payload['schema'] = 'sor-d3-corpus/1'
            for body in payload['bodies'].values():
                for biome in body['biomes'].values():
                    assert biome['status'] == 'ORDINARY_ONLY'
                    biome['status'] = 'ORDINARY_AND_SPECIAL'
        folder = out / label
        folder.mkdir()
        corrected[label] = payload
        # Canonical serialization keeps the production layout cost comparable.
        for variant, value in [('normalized', payload), ('expanded', expanded(payload))]:
            envelope = predictor.seal(value)
            predictor.validate(envelope)
            (folder / f'{variant}.json').write_bytes(predictor.canonical(envelope)+b'\n')
    write(out / 'preparation.json', dict(version='D4C SFPT installation v1; no owner-slot correction',
        installed_esm_sha256=pin(builder.ESM), frozen_inputs={str(p): pin(p) for p in sources.values()},
        patterns=dependency_rows, methods={str(p): pin(p) for p in
            (Path(__file__), Path(__file__).with_name('source_layout.py'))},
        sizes={label: dict(original_bytes=p.stat().st_size,
                          corrected_bytes=(out/label/'normalized.json').stat().st_size)
               for label, p in sources.items()}))
    code = ROOT / '.local-work/resource-save52-d3/revision06/build-v1/code'
    def infer(label, request_path, corpus):
        dest = out / label
        dest.mkdir(exist_ok=True)
        run = subprocess.run([sys.executable, '-I', '-S', '-B', str(ROOT/'research/resource-standalone/isolate.py'),
            '--code', str(code), '--corpus', str(corpus), '--request', str(request_path)], cwd=dest, capture_output=True)
        (dest / (request_path.stem+'-stdout.json')).write_bytes(run.stdout)
        (dest / (request_path.stem+'-audit.json')).write_bytes(run.stderr)
        assert run.returncode == 0, run.stderr.decode()
        audit = json.loads(run.stderr)
        assert not audit['inference_forbidden'] and audit['denied_probes'] == 8
        return json.loads(run.stdout)
    results, consequences = {}, []
    prior = ROOT / '.local-work/resource-save52-d3/revision06/first-pass-v1'
    for request in sorted(prior.glob('*-request.json')):
        result = infer('Save52-v1', request, out/'D3/normalized.json')
        case = request.name.removesuffix('-request.json')
        results[case] = result
        old = json.loads((prior / f'{case}-stdout.json').read_text())
        consequences.append(dict(case=case, old_status=old['status'], new_status=result['status'],
            old_sources=old.get('source_count'), new_sources=result.get('source_count'),
            old_paths=len(old['regions']), new_paths=len(result['regions']),
            availability_changes={fid: dict(old=old.get('availability',{}).get(fid,{}).get('status'),
                new=result.get('availability',{}).get(fid,{}).get('status'))
                for fid in set(old.get('availability',{})) | set(result.get('availability',{}))
                if old.get('availability',{}).get(fid,{}).get('status') != result.get('availability',{}).get(fid,{}).get('status')}))
    write(out/'case-consequences.json', consequences)
    rows = []
    associations = ROOT / 'docs/experiments/resource-save52-d3/associations-final.csv'
    for row in csv.DictReader(associations.open(encoding='utf8')):
        prediction = results[row['case']]
        new = classify(prediction, row['resource'], row['d3'] == 'ALTERNATIVE_ADMISSION')
        rows.append(dict(case=row['case'], resource=row['resource'], control=row['control'],
                         previous=row['d3'], corrected_source_layout=new, changed=new != row['d3']))
    write(out/'association-consequences.json', rows)
    # Preserve full-source identity evidence before inspecting geometry controls.
    c, body = corrected['D3'], corrected['D3']['bodies']['0005de4c']
    ax, ay = 27168, 35988
    tile = body['tiles']['0:141:187']
    tree = builder.planet_tree(records[0x5de4c][1])
    assert builder.decode_tree(records[tree][1])[0][141*256+187] == (int(tile[0],16), tile[1])
    write(out/'source-boundary.json', dict(owner='0005de4c', tree=f'{tree:08x}', pattern=tile[0],
        coarse=[141,187], coarse_flag=tile[1], subindices=[8,7], serialized_index=8*16+7,
        native_install_input_index=7*16+8,
        frozen_slot=json.loads(sources['D3'].read_text())['payload']['patterns'][tile[0]][8*16+7],
        corrected_slot=c['patterns'][tile[0]][8*16+7],
        corrected_resolve=list(predictor.resolve(c,body,0,ax,ay)),
        dimensions={f'{fid:08x}':list(struct.unpack('<2I',builder.last(records[fid][1],b'DNAM')))
                    for fid in (0x2c17d3,0x2c17d5)}))
    controls = []
    for variant in ('normalized', 'expanded'):
        for bid, folder, attempt, captures in (
            ('0005e0de','resource-region-ancestry','01',(299,325,696,716)),
            ('0005e4da','resource-carinae','02',(1270,1280,1301))):
            request = out / f'{bid}-request.json'
            if not request.exists():
                write(request, verify.request(bid))
            result = infer('controls-'+variant, request, out/'D1'/f'{variant}.json')
            for n in captures:
                capture = ROOT / f'.local-work/{folder}/retail-attempt{attempt}/capture-{n:05d}.bin'
                row = verify.native(capture)
                fid = f'{struct.unpack_from("<I",bytes.fromhex(row["selected"]["raw_resource"]),0x28)[0]:08x}'
                matches = [r for r in result['regions'] if r['resource']==fid and
                    r['ordered_xyzw_le']==row['geometry']['ordered_xyzw'] and
                    r['native_bound_le']==row['geometry']['raw_region'][:32]]
                controls.append(dict(variant=variant, body=bid, capture=n, exact_matches=len(matches),
                    callback_equal=all(r['callback']['accepted']==(row['decision']=='ACCEPT') for r in matches),
                    output_status=result['status']))
    write(out/'control-comparisons.json', controls)
    write(out/'summary.json', dict(version='D4C source layout v1; no owner-slot correction',
        cases=len(results), association_rows=len(rows), changed_associations=[r for r in rows if r['changed']],
        counts=dict(collections.Counter(r['corrected_source_layout'] for r in rows if r['control']=='False')),
        controls=controls, all_seven_both_variants=all(r['exact_matches']==1 and r['callback_equal'] for r in controls),
        source_boundary_sha256=pin(out/'source-boundary.json'), historical_epoch='UNKNOWN'))
    print(json.dumps(dict(cases=len(results), changed_associations=sum(r['changed'] for r in rows), controls=controls)))


if __name__ == '__main__':
    main()
