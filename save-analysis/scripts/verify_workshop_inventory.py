"""SPDX-License-Identifier: GPL-3.0-or-later
Original evidence audit: reads a completed ignored inventory, prior protected
corpus/static/frozen receipts and primary input hashes; exclusively writes a new
ignored validation receipt. Stdlib/project only, no target/save/database/Git
writes. Expectations derive from original action briefs, not detector output.
"""
import argparse
import collections
import json
from pathlib import Path
from inventory_historical_saves import ROOT, identity, guard
from research_workshop_inventory import write


def verify(run, output):
    guard()
    output.mkdir(parents=True,exist_ok=False)
    reproduction=json.loads((run/'reproduction.json').read_text())
    pins=[]
    def pin(path,expected=None):
        got=identity(path)
        if expected and got['sha256']!=expected: raise ValueError('HASH_CHANGED:'+str(path))
        pins.append(got)
        return got
    results={}
    for entry in reproduction['inputs']:
        p=run/(entry['series']+'-'+entry['label']+'.json')
        pin(p)
        x=json.loads(p.read_text())
        pin(Path(entry['pin']['path']),entry['pin']['sha256'])
        assert len(x['instances'])+len(x['unresolved_population'])==x['coverage']['framed_records']
        assert len(x['member_roles'])==len(x['instances'])
        assert sum(collections.Counter(r['role'] for r in x['member_roles']).values())==len(x['instances'])
        assert len({r['instance_identity'] for r in x['constructed_instances']})==len(x['constructed_instances'])
        assert all(r['owner_identity'] in {o['owner_identity'] for o in x['owners']} for r in x['constructed_instances'])
        assert not x['coverage']['complete_constructed_population']
        results[(entry['series'],entry['label'])]=x
    controls=[]
    # Original manual action brief: beacon, storage, extractor+solar, deletion.
    expected=[0,1,2,4,4,4,4,3]
    for i,count in enumerate(expected):
        for suffix in ('','C'):
            x=results[('manual-S0-S7C','S'+str(i)+suffix)]
            assert len(x['constructed_instances'])==count
            roots={r['instance_token'] for r in x['constructed_instances']}
            assert ('822c64' in roots)==(i>=1)
            assert ('822d48' in roots)==(i>=2)
            assert ('822da9' in roots)==(3<=i<=6)
            assert ('822dba' in roots)==(i>=3)
            controls.append(dict(label=x['label'],roots=count,action_expectation=True))
    def signature(x):
        return [(r['instance_identity'],r['owner_identity'],r['base_identity'],r['construction_definition'],r['root_kind'])
                for r in x['constructed_instances']]
    for i in range(8):
        assert signature(results[('manual-S0-S7C','S'+str(i))])==signature(results[('manual-S0-S7C','S'+str(i)+'C')])
    for label in ('L0','L0C','L1','L1C','L2','L2C','exit'):
        x=results[('output-link-L0-L2C',label)]
        assert len(x['constructed_instances'])==4
    for label in ('L1','L2'):
        assert signature(results[('output-link-L0-L2C',label)])==signature(results[('output-link-L0-L2C',label+'C')])
    for label in ('Save25','Save26'):
        x=results[('two-outpost',label)]
        assert len(x['owners'])==2 and len(x['constructed_instances'])==2
        assert sorted(o['direct_member_records'] for o in x['owners'])==[8,8]
        assert len({r['owner_identity'] for r in x['constructed_instances']})==2
    mature=results[('mature','Save52')]
    assert len(mature['owners'])==19
    assert collections.Counter(o['state'] for o in mature['owners'])=={'SAVED_DISABLED_CLEAR':17,'SAVED_DISABLED_SET':2}
    prior=ROOT/'.local-work/extractor-resource/run05/mature-Save52.json'
    pin(prior)
    old=json.loads(prior.read_text())
    assert old['source']['sha256']==mature['source']['sha256']
    members={r['token']:r for r in mature['instances']}
    owners={r['token']:r for r in mature['owners']}
    outside=old['unresolved_leads']
    assert len(outside)==17
    for r in outside:
        current=members[r['token']]
        assert current['base_identity']=='starfield.esm:2c60e9'
        assert owners[r['token']]['state']=='SAVED_DISABLED_CLEAR'
        assert current['owner_identity']==current['saved_reference']
    context_prior=ROOT/'.local-work/extractor-resource/context-crosschecks.json'
    pin(context_prior,'d9dcd1a46e1dff702ae3e0de5605ae5fecc37195576d5bfe23efbc3e85393725')
    selected=json.loads(context_prior.read_text())
    assert len(selected)==63
    roles={r['token']:r for r in mature['member_roles']}
    for r in selected:
        assert members[r['token']]['owner_identity']==members[r['beacon']]['saved_reference']
        assert roles[r['token']]['role']=='SINGLE_ROOT'
    # Comparative JSON is opened only after completed save extraction.
    extracted=ROOT/'.local-work/mature-save-validation/run-07/save-extraction.json'
    pin(extracted,'a1d4490a6b41c05ad08f68b2efa28f71d6ebac56cb9aabf55eb61356833b57e2')
    prior_beacons=json.loads(extracted.read_text())['beacons']
    names={r['token']:r['names'][0]['name_entry']['text'] for r in prior_beacons}
    network_path=ROOT/'.local-work/scratch/starfield-outposts-cao-tran-319-2026-09-28-124324.json'
    pin(network_path)
    network=json.loads(network_path.read_text())['networks'][0]['network']
    assert {names[r['token']] for r in mature['owners'] if r['state']=='SAVED_DISABLED_CLEAR'}=={o['name'] for o in network['outposts']}
    # Preserve prior native capture seal and frozen predictions/model.
    seal=ROOT/'.local-work/ship-relocation-050/live-20261013T031605991759Z/sealed-session-files.json'
    pin(seal,'e73dbe60db556b3654831a966aababe7026fc098e158674ea556cc97e02d16a3')
    sealed=json.loads(seal.read_text())
    for r in sealed: pin(Path(r['path']),r['sha256'])
    frozen=json.loads((ROOT/'.local-work/position-consolidation/check-03/receipt.json').read_text())['pins']
    for name,sha in frozen.items(): pin(ROOT/name,sha)
    protected=json.loads((ROOT/'.local-work/workshop-inventory/static-before.json').read_text())
    for r in protected['protected']: pin(Path(r['path']),r['sha256'])
    # Earlier source locations may no longer exist; archive pins are authoritative
    # research inputs here. Never infer this task removed original gameplay files.
    original_locations=[]
    for name in ('manual-S0-S7C','output-link-L0-L2C'):
        manifest=ROOT/('.local-work/'+name+'/manifest.json')
        pin(manifest)
        for sample in json.loads(manifest.read_text())['samples']:
            r=sample['source_before'];p=Path(r['path'])
            original_locations.append(dict(path=str(p),exists=p.exists(),label=sample['label']))
            if p.exists():pin(p,r['sha256'])
    for row in pins:
        assert identity(Path(row['path']))==row
    summary=dict(result='PASS',controls=controls,labels=len(results),unique_archives=len({x['source']['sha256'] for x in results.values()}),
        framed_records=sum(x['coverage']['framed_records'] for x in results.values()),
        mature_coverage=mature['coverage'],outside_base_mentions_reclassified_as_beacons=len(outside),
        prior_extractor_owners_checked=len(selected),network_names_checked=17,
        network_full_construction_oracle=False,seal_files=len(sealed),frozen_pins=len(frozen),
        static_database_and_executable_pins=len(protected['protected']),pins=pins,
        earlier_original_locations=original_locations,original_location_absence_is_not_task_deletion=True,
        review_required=True,validation_script=identity(Path(__file__)))
    write(output/'receipt.json',summary)
    write(output/'owner-context.json',[dict(o,context_label=names[o['token']]) for o in mature['owners']])
    guard()
    print(json.dumps({k:v for k,v in summary.items() if k not in ('pins','earlier_original_locations','controls')},indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--run',required=True)
    ap.add_argument('--receipt',required=True)
    args=ap.parse_args()
    if not all(n.isascii() and n.replace('-','').isalnum() for n in (args.run,args.receipt)):raise ValueError('RUN_NAME')
    base=ROOT/'.local-work/workshop-inventory'
    verify(base/args.run,base/args.receipt)
