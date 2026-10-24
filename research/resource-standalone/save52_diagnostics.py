# SPDX-License-Identifier: GPL-3.0-or-later
"""D2 post-answer diagnostics and native fixture checks, offline only.

Reads frozen predictions, seven protected native controls, exact installed
definitions and the existing independent manual network. Writes a fresh local
diagnostic receipt. Does not rerun/adjust prediction, mutate originals or operate
a target. Manual resource contents are never used as prediction inputs.
"""
import collections
import argparse
import csv
import dataclasses
import json
from pathlib import Path
import struct

import save52 as s
import verify


def run():
    inv = json.loads((s.OUT/'inventory-v2.json').read_text())
    cases = {r['case']:r for r in inv['cases']}
    predictions = {r['case']:json.loads((s.OUT/'first-pass-v1'/(r['case']+'-stdout.json')).read_text())
                   for r in inv['cases'] if r['eligibility']=='ACTIVE'}
    pins = {r['path'].replace('\\','/'):r['sha256'] for r in csv.DictReader(
        (s.ROOT/'docs/experiments/resource-pattern-selection/sources.csv').open(encoding='utf8'))}
    native = []
    inputs = {}
    for case,folder,attempt,numbers in (
        ('D2-83388f','resource-region-ancestry',1,(299,325,696,716)),
        ('D2-82be17','resource-carinae',2,(1270,1280,1301))):
        output = predictions[case]
        for number in numbers:
            path = s.ROOT/f'.local-work/{folder}/retail-attempt0{attempt}/capture-{number:05d}.bin'
            if s.builder.pin(path)!=pins[path.relative_to(s.ROOT).as_posix()]:
                raise ValueError('NATIVE_FIXTURE_IDENTITY')
            inputs[str(path)] = s.builder.pin(path)
            inputs[str(path.with_suffix('.ack.json'))] = s.builder.pin(path.with_suffix('.ack.json'))
            row = verify.native(path)
            resource = f'{struct.unpack_from("<I",bytes.fromhex(row["selected"]["raw_resource"]),40)[0]:08x}'
            matches = [r for r in output['regions'] if r['resource']==resource and
                       r['ordered_xyzw_le']==row['geometry']['ordered_xyzw'] and
                       r['native_bound_le']==row['geometry']['raw_region'][:32]]
            native.append(dict(case=case,capture=number,resource=resource,exact_matches=len(matches)))
            if len(matches)!=1:
                raise ValueError('NATIVE_GEOMETRY_REGRESSION')
        baseline = s.ROOT/'.local-work/resource-standalone/verify03'/('normalized-'+cases[case]['body']+'-stdout.json')
        old = json.loads(baseline.read_text())
        if [(r['resource'],r['ordered_xyzw_le'],r['native_bound_le']) for r in old['regions']] != [
            (r['resource'],r['ordered_xyzw_le'],r['native_bound_le']) for r in output['regions']]:
            raise ValueError('FULL_CONTROL_GEOMETRY_CHANGED')
        inputs[str(baseline)] = s.builder.pin(baseline)
    # This independent human-authored network is corroboration of saved cases,
    # not an exhaustive contemporary native oracle or predictor input.
    old = json.loads((s.ROOT/'.local-work/save-capacity-location/body-final-03/comparison.json').read_text())
    path = Path(old['source']['path'])
    if s.builder.pin(path)!=old['source']['sha256']:
        raise ValueError('MANUAL_NETWORK_PIN')
    inputs[str(path)] = s.builder.pin(path)
    network = json.loads(path.read_text())
    ops = next(n['network']['outposts'] for n in network['networks'] if n['id']==network['activeNetworkId'])
    membership = []
    for row in inv['cases']:
        matches = [o for o in ops if o['name'] in row['name']]
        membership.append(dict(case=row['case'],saved_state=row['eligibility'],manual_matches=len(matches),
            body_equal=bool(len(matches)==1 and int(matches[0]['bodyId'],16)==int(row['body'],16))))
    if sum(r['manual_matches']==1 and r['body_equal'] for r in membership)!=17:
        raise ValueError('MANUAL_MEMBERSHIP_CORROBORATION')
    pairs = json.loads((s.OUT/'comparison-v3/pairs.json').read_text())
    records = {h['formid']:(h,fs) for h,fs in s.esm_records(s.builder.ESM,
        {b'PNDT',b'SFTR',b'SFPT',b'SFBK',b'BIOM',b'RSGD',b'IRES'},repeated=True)}
    corpus = json.loads((s.OUT/'build-v1/normalized.json').read_text())['payload']
    lineage = json.loads((s.OUT/'build-v1/manifest.json').read_text())['lineage']
    diagnostics = []
    for p in pairs:
        if p['control'] or p['outcome']!='POTENTIAL_FALSE_NEGATIVE':
            continue
        case = cases[p['case']]
        body = int(case['body'],16)
        predicted = s.builder.selections(records,body)
        selection = []
        for v in predicted.biome_results:
            family = v.family_access.family if v.family_access else None
            selection.append(dict(biome=str(v.orchestration.biome.form_id),
                rsgd=str(v.orchestration.effective_rsgd.form_id),
                root=str(family.root.form_id) if family else None,
                emitted=[str(f) for f in family.emitted_form_ids] if family else [],
                special=str(v.orchestration.special_selection)))
        output = predictions[p['case']]
        sources = sorted({r['source'] for r in output['regions']})
        source_biomes = []
        for source in sources:
            chart,x,y,fid = source.split(':')
            tile = corpus['bodies'][case['body']]['tiles'][f'{chart}:{int(x)//192}:{int(y)//192}']
            source_biomes.append(dict(source=source,tile=tile,
                component=corpus['bodies'][case['body']]['biomes'][tile[2]]))
        diagnostics.append(dict(case=p['case'],resource=p['resource'],extractor_tokens=p['tokens'],
            request=output['request'],halo=output['halo'],source_count=output['source_count'],
            failures=output['failures'],sources=source_biomes,planet_selection=selection,
            nearby_tiles=[r for r in lineage if r['body']==case['body']],
            earliest_failure='Selected source-biome component omits saved extractor resource before numeric geometry',
            identity='Positive exact DIRECT4C owner plus CONT PRPS AVIF to IRES NAM1; no queued adjacency',
            historical_cache_epoch='UNKNOWN; extractor survival is not a contemporaneous native region witness',
            next_discriminator='Capture effective native source biome and full component resources at the same query before considering geometry changes'))
    ledger = json.loads((s.OUT/'comparison-v3/ownership-ledger.json').read_text())
    catalog = json.loads((s.OUT/'comparison-v3/extractor-definitions.json').read_text())
    coverage = dict(owner_linked_records=len(ledger['instances']),
        non_main_or_unresolved_base_members=sum(not (m.get('base_identity') or '').startswith('starfield.esm:') for m in ledger['instances']),
        main_non_extractor_members=sum((m.get('base_identity') or '').startswith('starfield.esm:') and m.get('base_identity') not in catalog for m in ledger['instances']),
        unknown_owner_members=sum(m['owner_identity'] is None for m in ledger['instances']),
        unresolved_other_records=len(ledger['unresolved_population']),
        qualification='These unknown members are not assumed to be extractors; validation is scoped to recognized main-ESM bases')
    branches = []
    for bid in sorted({r['body'] for r in lineage if r['status']!='ORDINARY_ONLY'}):
        selected = s.builder.selections(records,int(bid,16))
        for biome in sorted({r['biome'] for r in lineage if r['body']==bid and r['status']!='ORDINARY_ONLY'}):
            v = next(v for v in selected.biome_results if int(str(v.orchestration.biome.form_id),16)==int(biome,16))
            family = v.family_access.family if v.family_access else None
            branches.append(dict(body=bid,biome=biome,family_present=family is not None,
                selected_special=None if v.orchestration.special_selection is None else str(v.orchestration.special_selection.form_id),
                rsgd=str(v.orchestration.effective_rsgd.form_id),source=str(v.orchestration.rsgd_resolution_source),
                reason='SELECTED_SPECIAL' if v.orchestration.special_selection is not None else 'NO_ORDINARY_FAMILY'))
    property_values = []
    rows = json.loads((s.OUT/'comparison-v3/instances.json').read_text())
    bases = {r['base'] for r in rows if r['alternative_keys']}
    for h,fields in s.esm_records(s.builder.ESM,{b'CONT'},repeated=True):
        base = f'starfield.esm:{h["formid"]:06x}'
        if base not in bases:
            continue
        for tag,raw in fields:
            if tag==b'PRPS':
                for at in range(0,len(raw),12):
                    key,value = struct.unpack_from('<If',raw,at)
                    if key in (0x83ff,0x271128,0x31986f):
                        property_values.append(dict(base=base,key=f'0x{key:08x}',value=value,
                            interpretation='Native selection tests property presence, not numeric positivity'))
    s.write(s.OUT/'diagnostics-v3.json',dict(time=s.now(),inputs=inputs,native=native,membership=membership,
        manual_count=len(ops),diagnostics=diagnostics,coverage=coverage,unsupported_branches=branches,
        alternative_property_values=property_values,
        predictor_code_unchanged={p.name:s.builder.pin(p) for p in (s.OUT/'build-v1/code').glob('*.py')}))
    print(json.dumps(dict(native_exact=len(native),membership_correspondences=17,diagnostics=len(diagnostics),coverage=coverage)))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=s.OUT)
    s.select_root(ap.parse_args().root)
    run()
