# SPDX-License-Identifier: GPL-3.0-or-later
"""D2 post-freeze positive-only comparator; separate from prediction process.

Requires immutable prediction manifest. Reads pinned Save52 and fresh installed
main definitions; reuses exact DIRECT4C owner and extractor-resource readers.
Writes new ignored comparison/identity evidence only. No target, network,
original mutations or post-answer predictor execution. Non-main bases remain
unqualified; no queued-keyword adjacency is accepted as ownership.
"""
import collections
import argparse
import json
from pathlib import Path
import struct

import save52 as s
from extractor_resources import definition_catalog, plugin_tables
from workshop_inventory import audit, ownership_ledger
from outpost_membership import token_value


def classify(prediction, resource, alternative=False):
    if alternative:
        return 'ALTERNATIVE_ADMISSION'
    value = prediction.get('availability',{}).get(resource,{}).get('status')
    if value=='PRESENT':
        return 'POSITIVE_CORRESPONDENCE'
    if value=='ABSENT_WITHIN_PROVEN_SCOPE':
        return 'POTENTIAL_FALSE_NEGATIVE'
    if value is None and prediction.get('status')=='CONDITIONAL_GEOMETRY':
        return 'POTENTIAL_FALSE_NEGATIVE'
    return 'UNSUPPORTED_INDETERMINATE'


def run(label):
    freeze_path = s.OUT/'first-pass-v1/prediction-freeze.json'
    freeze = json.loads(freeze_path.read_text())
    if any(s.builder.pin(p)!=h for p,h in {**freeze['inputs'],**freeze['files']}.items()):
        raise ValueError('FREEZE_CHANGED')
    if not label.replace('-','').isalnum():
        raise ValueError('OUTPUT_LABEL')
    out = s.OUT/label
    out.mkdir(exist_ok=False)
    s.write(out/'answer-access.json',dict(time=s.now(),freeze_time=freeze['time'],
        freeze_sha256=s.builder.pin(freeze_path),operation='First comparator launch; resolve extractor bases/resources and exact owner edges'))
    records = []
    source_pin = s.builder.pin(s.builder.ESM)
    if source_pin!=s.builder.DEFINITION:
        raise ValueError('DEFINITION_PIN')
    for h,fs in s.esm_records(s.builder.ESM,{b'TES4',b'CONT',b'COBJ',b'AVIF',b'IRES',b'MISC',b'LVLI',b'KYWD'},repeated=True):
        edid = next((v.rstrip(b'\0').decode('utf8','backslashreplace') for t,v in fs if t==b'EDID'),'')
        records.append(dict(**h,plugin='Starfield.esm',edid=edid,fields=[(t.decode(),v.hex()) for t,v in fs]))
    catalog = definition_catalog(records)
    definitions = {f'starfield.esm:{r["formid"]:06x}':r for r in records}
    inv = json.loads((s.OUT/'inventory-v2.json').read_text())
    cases = {r['token']:r for r in inv['cases']}
    roster_path = s.OUT/'requests-v1.json'
    roster = json.loads(roster_path.read_text())
    actual = [dict(case=r['case'],control=r['control'],request=r['request'])
              for r in inv['cases'] if r['eligibility']=='ACTIVE']
    if actual!=roster or s.builder.pin(roster_path)!=freeze['inputs'][str(roster_path)]:
        raise ValueError('INVENTORY_DIFFERS_FROM_FROZEN_ROSTER')
    predictions = {r['case']:json.loads((s.OUT/'first-pass-v1'/(r['case']+'-stdout.json')).read_text())
                   for r in cases.values() if r['eligibility']=='ACTIVE'}
    with s.decoded_save(s.source(),s.OUT/'scratch',seconds=float('inf')) as (b,metrics):
        ledger = ownership_ledger(audit(b))
        s.write(out/'ownership-ledger.json',ledger)
        s.write(out/'extractor-definitions.json',catalog)
        rows = []
        unqualified = []
        for member in ledger['instances']:
            base = member.get('base_identity')
            if base not in catalog:
                continue
            owners = {r['owner_identity']:r['token'] for r in ledger['owners']}
            tok = owners.get(member.get('owner_identity'))
            owner = cases.get(tok)
            qualification = catalog[base]
            if owner is None or owner['eligibility']!='ACTIVE' or qualification['status']!='ASSOCIATED':
                unqualified.append(dict(token=member['token'],base=base,owner=member.get('owner_identity'),
                    reason='OWNER_INACTIVE_OR_UNRESOLVED_OR_AMBIGUOUS_RESOURCE'))
                continue
            prefix = member.get('prefix',{})
            if prefix.get('disabled') is not False or prefix.get('deleted') is not False:
                unqualified.append(dict(token=member['token'],base=base,owner=owner['case'],reason='EXTRACTOR_STATE_NOT_CLEAR'))
                continue
            association = qualification['associations'][0]
            resource = association['resource_identity'].split(':')[1].zfill(8)
            props = []
            for tag,raw in definitions[base]['fields']:
                if tag=='PRPS':
                    blob = bytes.fromhex(raw)
                    props.extend(struct.unpack_from('<I',blob,i)[0] for i in range(0,len(blob),12))
            bypass = sorted(set(props)&{0x83ff,0x271128,0x31986f})
            if resource=='000083ec':
                bypass.append('Water/Everywhere')
            row = dict(case=owner['case'],control=owner['control'],extractor_token=member['token'],
                record_offset=member['offset'],offset_domain='DECODED_LOGICAL_STREAM',base=base,
                owner_identity=member['owner_identity'],owner_edges=member['ownership_evidence'],
                resource=resource,label=association['resource_label'],definition=association,
                alternative_keys=bypass,prediction_status=predictions[owner['case']]['status'])
            row['outcome'] = classify(predictions[owner['case']],resource,bool(bypass))
            rows.append(row)
        s.write(out/'instances.json',rows)
        s.write(out/'unqualified.json',unqualified)
    pairs = []
    for case,resource in sorted({(r['case'],r['resource']) for r in rows}):
        members = [r for r in rows if r['case']==case and r['resource']==resource]
        outcomes = {r['outcome'] for r in members}
        # Different admission branches cannot silently become one ordinary pair.
        for outcome in sorted(outcomes):
            group = [r for r in members if r['outcome']==outcome]
            pairs.append(dict(case=case,control=members[0]['control'],resource=resource,label=members[0]['label'],
                outcome=outcome,extractors=len(group),tokens=[r['extractor_token'] for r in group]))
    extras = []
    for case,pred in predictions.items():
        for resource,status in pred.get('availability',{}).items():
            if status['status']=='PRESENT' and not any(r['case']==case and r['resource']==resource for r in pairs):
                extras.append(dict(case=case,resource=resource,outcome='UNVERIFIED_EXTRA_PREDICTION'))
    s.write(out/'pairs.json',pairs)
    s.write(out/'extras.json',extras)
    held = [r for r in pairs if not r['control']]
    summary = dict(time=s.now(),freeze_sha256=s.builder.pin(freeze_path),
        counts=dict(collections.Counter(r['outcome'] for r in held)),held_out_pairs=len(held),
        held_out_instances=sum(r['extractors'] for r in held),unqualified=len(unqualified),
        held_out_extras=sum(not cases[r['case'][3:]]['control'] for r in extras),
        definitions_sha256=source_pin,definition_scope='Pinned installed main ESM; non-main bases unqualified',
        decoded_sha256=metrics['decoded_sha256'],save_sha256=s.builder.pin(s.source()),
        code={str(p.relative_to(s.ROOT)):s.builder.pin(p) for p in [Path(__file__),
            s.ROOT/'save-analysis/scripts/workshop_inventory.py',s.ROOT/'save-analysis/scripts/extractor_resources.py']})
    if s.builder.pin(s.builder.ESM)!=source_pin or any(s.builder.pin(p)!=h for p,h in freeze['files'].items()):
        raise ValueError('INPUT_CHANGED')
    s.write(out/'summary.json',summary)
    print(json.dumps(summary))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run',required=True)
    ap.add_argument('--root',type=Path,default=s.OUT)
    args=ap.parse_args()
    s.select_root(args.root)
    run(args.run)
