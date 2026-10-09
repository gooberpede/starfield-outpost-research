"""SPDX-License-Identifier: GPL-3.0-or-later

Offline hypothesis runner, not an active-outpost classifier. Reads verified
Save3/S/L archives and frozen historical/donor source inventories. Hashes
originals and archives before/after; processes immutable bytes in memory.
Writes fresh ignored numeric JSON only; no save/target/database effects.
Uses existing project-authored framing/directory/window methods, stdlib only.
Physical <=128 MiB, decoded <=64 MiB, disk guards inherited. Larger saves
remain INDETERMINATE; missing/changed source aborts. Never emits NO_ACTIVE_OUTPOSTS.
"""
from pathlib import Path
import argparse, collections, datetime as dt, json, re, struct, sys
from inventory_historical_saves import (ROOT, MAX_DECODED, MAX_PHYSICAL,
    framing, transform, identity, guard, metadata, candidate_windows, sha)
from validate_mature_outposts import directory, envelopes
from outpost_record_framing import records as frame_records, beacon_prefix


def features(b):
    d=directory(b);a,z=d['regions']['region_R3']
    rows=candidate_windows(b,a,z,'6c60e9',0x3a)
    for r in rows:
        r['word_at_plus4']=struct.unpack_from('<I',b,r['offset']+4)[0]
        r['bit25']=bool(r['word_at_plus4']&0x02000000)
    es=[e for e in envelopes(b,d) if e['qualifies']]
    members=es[0]['parsed']['beacons'] if len(es)==1 and 'parsed' in es[0] else None
    framed=frame_records(b,a,z,d['words'][9])
    reference_candidates=[r for r in framed if '6c60e9' in r['refs']]
    for r in reference_candidates:r['case5_diagnostic']=beacon_prefix(b,r)
    return dict(directory_offset=d['offset'],directory_words=d['words'],
        record_count=len(framed),record_region=[a,z],
        reference_candidates=reference_candidates,
        explicit_types=dict(collections.Counter(str(r['explicit_type']) for r in framed)),
        windows=rows,bit25_set=sum(r['bit25'] for r in rows),
        bit25_clear=sum(not r['bit25'] for r in rows),
        collection_members=members,
        bit25_tokens=sorted(r['token'] for r in rows if r['bit25']),
        status='INDETERMINATE',reason='case-5 inline-base coverage excludes alternate initial-data paths; workshop registration, resolved keywords and player ownership not fully reconstructed')


def specs():
    old=json.loads((ROOT/'.local-work/exp0002/integrity-before.json').read_text())
    yield dict(label='Save3',sample_id='SOR-SAMPLE-0001',source=old['original'],copy=old['backup'])
    for folder in ['manual-S0-S7C','output-link-L0-L2C']:
        m=json.loads((ROOT/'.local-work'/folder/'manifest.json').read_text())
        for s in m['samples']:
            if not re.fullmatch(r'[SL]\dC?',s['label']):continue
            yield dict(label=s['label'],sample_id=s['sample_id'],source=s['source_before'],copy=s['copy'])
    # Read only identity/ID fields here. Previous classifications are deliberately
    # excluded from the extraction and are consulted in a separate comparison.
    for group,path in [('HIST',ROOT/'.local-work/historical-inventory/scan-04/inventory.json'),
                       ('TDX',ROOT/'.local-work/third-party/the-daily-xperience-1798/scan-03/inventory.json')]:
        for s in json.loads(path.read_text()):
            yield dict(label=s['inventory_id'],group=group,source=s['source'],copy=s['source'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args()
    if not args.run.replace('-','').isalnum():raise ValueError('run name')
    out=ROOT/'.local-work/active-outpost'/args.run;out.mkdir(exist_ok=False)
    guard(out);records=[];preserved={};inputs={}
    for s in specs():
        guard(out)
        for role in ['source','copy']:
            v=s[role];p=Path(v['path']);key=str(p.resolve())
            if key not in inputs:
                actual=identity(p)
                if actual['sha256']!=v['sha256'] or actual['size']!=v['size']:raise ValueError('input mismatch: '+s['label'])
                inputs[key]=actual
        p=Path(s['copy']['path']);physical=p.read_bytes()
        if sha(physical)!=s['copy']['sha256']:raise ValueError('read mismatch')
        r=dict(label=s['label'],sample_id=s.get('sample_id'),source_sha256=sha(physical),source_size=len(physical))
        try:
            if len(physical)>MAX_PHYSICAL:raise ValueError('physical resource bound')
            f,sp=framing(physical);r['framing']=f
            if f['declared_decoded_size']>MAX_DECODED:raise ValueError('decoded resource bound')
            raw=transform(physical,sp,True);r.update(decoded_sha256=sha(raw),metadata=metadata(raw),features=features(raw))
            del raw
        except (ValueError,struct.error) as e:r.update(status='INDETERMINATE',reason=str(e))
        records.append(r)
        if len(records)%50==0:print('processed',len(records),flush=True)
    def write(name,v):
        with (out/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
    write('features-frozen.json',records);frozen=identity(out/'features-frozen.json')
    # Outcome comparison occurs only after feature predictions have been frozen.
    comparisons=[]
    for path in [ROOT/'.local-work/historical-inventory/scan-04/inventory.json',ROOT/'.local-work/third-party/the-daily-xperience-1798/scan-03/inventory.json']:
        for old in json.loads(path.read_text()):
            new=next(r for r in records if r['label']==old['inventory_id'])
            comparisons.append(dict(label=new['label'],old_classification=old['classification'],
                bit25_set=new.get('features',{}).get('bit25_set'),bit25_clear=new.get('features',{}).get('bit25_clear')))
    write('comparison-after-freeze.json',comparisons)
    for key,v in inputs.items():
        actual=identity(Path(key))
        if actual!=v:raise ValueError('source changed during research')
        preserved[key]=actual
    write('preservation.json',dict(before=inputs,after=preserved))
    write('run.json',dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        python=sys.version,python_identity=identity(Path(sys.executable)),
        scripts={str(p.relative_to(ROOT)):identity(p) for p in Path(__file__).parent.glob('*.py')},
        frozen=frozen,records=len(records),unique_sources=len({r['source_sha256'] for r in records}),
        inputs_preserved=len(inputs),status='FEATURE_RESEARCH_ONLY'))
    print('Frozen',frozen['sha256'],'records',len(records),'preserved',len(inputs))
    print('Profile counts',dict(collections.Counter((r.get('features',{}).get('bit25_set'),r.get('features',{}).get('bit25_clear')) for r in records)))

if __name__=='__main__':main()
