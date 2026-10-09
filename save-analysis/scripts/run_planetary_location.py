"""SPDX-License-Identifier: GPL-3.0-or-later
Invoked offline research runner. Frozen manifests choose inputs; reads one
mapped save at a time, hashes originals/archives and catalog/JSON. Exclusive
ignored output; save extraction is closed/hashed before comparison. No game,
dependency/network, database, source-save or Git effects. See SOR-EXP-0012.
"""
import argparse
import json
from pathlib import Path
import sys
from investigate_active_outposts import specs
from inventory_historical_saves import ROOT,identity,metadata,guard
from stream_save import decoded_save
from outpost_planetary_location import extract
from validate_mature_outposts import directory,pool


def write(p,data):
    with p.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(data,f,indent=2,allow_nan=False);f.write('\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True)
    ap.add_argument('--catalog',type=Path,required=True);ap.add_argument('--network',type=Path,required=True)
    args=ap.parse_args()
    if not args.run.replace('-','').isalnum():raise ValueError('run name')
    out=ROOT/'.local-work/save-capacity-location'/args.run;out.mkdir(exist_ok=False)
    guard(out);catalog=json.loads(args.catalog.read_text());by_id={r['formid']:r for r in catalog['records']}
    before={str(args.catalog):identity(args.catalog),str(args.network):identity(args.network)}
    esm=Path(catalog['source']['path']);before[str(esm)]=identity(esm)
    if before[str(esm)]['sha256']!=catalog['source']['sha256']:raise ValueError('ESM_HASH')
    results=[]
    for label in ['Save3','S1','S1C','L2C','HIST-0245','HIST-0267']:
        s=next(s for s in specs() if s['label']==label)
        if label=='HIST-0267':
            archive=ROOT/'.local-work/savegames'/Path(s['source']['path']).name
            s=dict(s,copy=dict(s['copy'],path=str(archive)))
        for role in ['source','copy']:
            p=Path(s[role]['path']);v=identity(p)
            if v['sha256']!=s[role]['sha256']:raise ValueError('SAVE_HASH')
            before[str(p)]=v
        with decoded_save(s['copy']['path'],out/'scratch') as (b,m):
            data=extract(b,catalog['records']);_,strings=pool(b,directory(b))
            # Names are diagnostics for correspondence; extract never reads them.
            for r in data['beacons']:
                r['name_for_comparison']=strings[r['string_indices'][0]]['text'] if r['string_indices'] else None
            results.append(dict(label=label,source=s,metrics=m,metadata=metadata(b),extraction=data))
        print(label,[(r['token'],r['proposed_body_formid']) for r in data['beacons']],flush=True)
    write(out/'save-derived.json',results)
    write(out/'extraction-frozen.json',identity(out/'save-derived.json'))
    j=json.loads(args.network.read_text());network=next(n['network'] for n in j['networks'] if n['id']==j['activeNetworkId'])
    comparison=[];save=next(r for r in results if r['label']=='HIST-0267')
    for r in save['extraction']['beacons']:
        matches=[p for p in network['outposts'] if p['name']==r['name_for_comparison']]
        p=matches[0] if len(matches)==1 else None
        bd=by_id.get(r['proposed_body_formid']);gnam=bytes.fromhex(bd['fields']['GNAM']) if bd else None
        system=int.from_bytes(gnam[:4],'little') if gnam else None
        comparison.append(dict(token=r['token'],parent=r['parent_token'],name=r['name_for_comparison'],
            saved_disabled=r['saved_disabled'],save_body=r['proposed_body_formid'],save_system=system,
            body_editor_id=bd['edid'] if bd else None,
            json_body=p['bodyId'] if p else None,json_system=p['systemId'] if p else None,
            body_match=(int(p['bodyId'],16)==r['proposed_body_formid']) if p else None,
            system_match=(int(p['systemId'])==system) if p else None,
            correspondence='UNIQUE_NAME_EQUALITY; APPLICATION_UUID_NOT_MAPPED' if p else 'NO_NAME_MATCH',
            direct_body_agreement=r['independent_direct_agreement'],points=r['points']))
    write(out/'comparison.json',dict(source=identity(args.network),outposts=comparison))
    after={p:identity(Path(p)) for p in before}
    if before!=after:raise RuntimeError('INPUT_CHANGED')
    write(out/'preservation.json',dict(before=before,after=after))
    write(out/'tools.json',dict(python=sys.version,argv=sys.argv,scripts=[identity(p) for p in Path(__file__).parent.glob('*.py')]))


if __name__=='__main__':main()
