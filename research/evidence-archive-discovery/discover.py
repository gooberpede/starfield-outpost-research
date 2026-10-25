# SPDX-License-Identifier: GPL-3.0-or-later
"""Join frozen metadata to authored sources; propose two inactive ownership schemes.

Reads hash-bound existing documentation/CSV and fixed metadata, not bulk payloads.
Writes aggregate authored tables and one local candidate-owner/dependency database.
Every unknown/primary member remains KEEP; no retirement or production index.
"""
import csv
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess

from inventory import ROOT,LOCAL,DOC,csvout,write


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    from archive import space
    space(1024*1024*1024)
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label',default='03')
    args=ap.parse_args()
    if not args.label.isalnum():raise ValueError('Fresh alphanumeric label')
    label=args.label
    start=json.loads((LOCAL/'start.json').read_text())
    db=sqlite3.connect(f'file:{(LOCAL/"inventory03.sqlite").as_posix()}?mode=ro',uri=True)
    summary=json.loads((LOCAL/'inventory-summary03.json').read_text())
    assert sha((LOCAL/'inventory03.sqlite').read_bytes())==summary['inventory_sha256']
    files=db.execute('select path,directory,area,bytes,allocation_estimate,device,file_id,extension,role,original_pin from files').fetchall()
    area_by_directory={r[1]:r[2] for r in files}
    tops={r[1] for r in files}
    pins={};references={};dependencies=[];documents=[]
    source_names=set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')[:-1])|set(start['files'])
    for name in sorted(source_names):
        if not name.startswith(('docs/','research/','runtime/','historical-methods/')) or Path(name).suffix not in ('.md','.csv','.py','.ps1','.cpp','.json'):
            continue
        raw=(ROOT/name).read_bytes()
        if b'\0' in raw:
            continue
        try:
            text=raw.decode('utf8')
        except UnicodeDecodeError:
            continue
        # Freeze the actual source version before semantic/path interrogation.
        digest=sha(raw)
        if name in start['files']:
            assert digest==start['files'][name]['sha256'],name
        else:
            blob=subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT)
            assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n'),name
        docs_for_top=set()
        for line_number,line in enumerate(text.splitlines(),1):
            for match in re.finditer(r'\.local-work[/\\]+([A-Za-z0-9_-]+)',line):
                top=match.group(1)
                if top in tops:
                    docs_for_top.add(top)
                    dependencies.append(dict(consumer=name,line=line_number,source_directory=top,
                        reference='literal local-path mention; not proof of executed read',
                        required_access='controlled extraction or explicit locator adaptation',
                        physical_owner='central owner table; cross-system reference only'))
        ids=sorted(set(re.findall(r'SOR-EXP-\d{4}|RG2-[A-Z]\d+[A-Z]?',text)))
        for top in docs_for_top:
            references.setdefault(top,[]).append(dict(source=name,ids=ids,sha256=digest))
        if docs_for_top or name.endswith('sources.csv'):
            documents.append(dict(path=name,sha256=digest))
        if name.endswith('.csv'):
            try:
                rows=csv.DictReader(text.splitlines())
                for row in rows:
                    digest=row.get('sha256','')
                    path=row.get('path') or row.get('locator') or row.get('source') or row.get('file')
                    if path and re.fullmatch('[0-9a-fA-F]{64}',digest or ''):
                        absolute=Path(path) if Path(path).is_absolute() else ROOT/path
                        if absolute.is_relative_to(ROOT/'.local-work'):
                            pins.setdefault(os.path.normcase(os.path.normpath(str(absolute))),[]).append(dict(sha256=digest.lower(),ledger=name,ledger_sha256=sha(raw)))
            except (csv.Error,ValueError):
                pass
    ownerdb=sqlite3.connect(LOCAL/f'candidate-owners{label}.sqlite')
    ownerdb.execute('create table owner(path text primary key,area text,scheme_a text,scheme_b text,bytes integer,role text,reason text)')
    # Shared controlled saves have one corpus owner; consumers reference it.
    overrides={'manual-S0-S7C':'persistence-save-corpora','disappearing-deposits':'resources-production'}
    scheme_a={a:a for a in {r[2] for r in files}}
    scheme_a['power']='resources-production'
    scheme_a['unclassified-working']='LOOSE-UNKNOWN'
    scheme_b={'identity-location-lifecycle':'settlement-layout-lifecycle','construction-limits-defense':'settlement-layout-lifecycle',
        'resources-production':'production-storage-power','storage-links':'production-storage-power','power':'production-storage-power',
        'cargo-transport':'cargo-transport','crew-robots':'crew-robots','persistence-save-corpora':'persistence-save-corpora',
        'native-observation-infrastructure':'shared-methods-provenance','governance-publication-review':'shared-methods-provenance',
        'unclassified-working':'LOOSE-UNKNOWN'}
    grouped={};directories={}
    for path,top,old_area,size,allocation,device,file_id,ext,role,original_pin in files:
        area=overrides.get(top,old_area)
        owner_a=scheme_a[area];owner_b=scheme_b[area]
        reason='Provisional system owner; KEEP all content'
        if top=='evidence-archive-discovery':
            owner_a=owner_b='LOOSE-ACTIVE-STAGE-A';reason='Current inventory/prototype workspace remains loose'
        if ext=='.sfs':
            owner_a=owner_b='persistence-save-corpora';reason='Shared saved-input owner; protection and duplicate-copy identity still require review'
        ownerdb.execute('insert into owner values(?,?,?,?,?,?,?)',(path,area,owner_a,owner_b,size,role,reason))
        row=grouped.setdefault(area,dict(area=area,files=0,logical_bytes=0,allocation_estimate=0,original_pins=0,directories=set(),roles=set(),ids=set(),sources=set()))
        row['files']+=1;row['logical_bytes']+=size;row['allocation_estimate']+=allocation or 0;row['original_pins']+=bool(original_pin)
        row['directories'].add(top);row['roles'].add(role)
        for ref in references.get(top,[]):
            row['ids'].update(ref['ids']);row['sources'].add(ref['source'])
        directories.setdefault(top,dict(directory=top,area=area,files=0,bytes=0,source_refs=len(references.get(top,[])),ids=set()))
        directories[top]['files']+=1;directories[top]['bytes']+=size
        for ref in references.get(top,[]):directories[top]['ids'].update(ref['ids'])
    ownerdb.commit()
    fields=['research_area','files','logical_bytes','allocation_estimate','original_D5G_pins','directories','roles','linked_experiment_IDs','status','ownership_uncertainty','source_records','candidate_disposition']
    out=[]
    for area,row in sorted(grouped.items()):
        out.append(dict(zip(fields,(area,row['files'],row['logical_bytes'],row['allocation_estimate'],row['original_pins'],
            '; '.join(sorted(row['directories'])),'; '.join(sorted(row['roles'])),'; '.join(sorted(row['ids'])) or 'UNKNOWN: no direct authored-ID join',
            'Current Stage A active; other members retain historical bytes; future reuse UNKNOWN' if area=='governance-publication-review' else 'Historical evidence retained; active dependency/reuse per member UNKNOWN',
            'Provisional thematic owner; linked IDs are mentions, not exclusive experiment membership',
            '; '.join(sorted(row['sources'])),'KEEP; no exclusion or deletion approved'))))
    csvout('research-areas.csv',fields,out)
    csvout('research-areas-by-size.csv',fields,sorted(out,key=lambda r:(-r['logical_bytes'],-r['files'])))
    dfields=['directory','area','files','bytes','source_refs','linked_experiment_IDs','status','disposition']
    csvout('directory-inventory.csv',dfields,[dict(directory=x['directory'],area=x['area'],files=x['files'],bytes=x['bytes'],source_refs=x['source_refs'],linked_experiment_IDs='; '.join(sorted(x['ids'])) or 'UNKNOWN',status='ACTIVE Stage A' if x['directory']=='evidence-archive-discovery' else 'Historical/current reuse UNKNOWN',disposition='KEEP; no retirement authority') for x in sorted(directories.values(),key=lambda r:-r['bytes'])])
    write(LOCAL/f'dependency-mentions{label}.json',dependencies)
    concise={}
    for row in dependencies:
        owner=overrides.get(row['source_directory'])
        if owner is None:
            owner=area_by_directory[row['source_directory']]
        consumer_class='documentation' if row['consumer'].startswith('docs/') else 'historical-methods' if row['consumer'].startswith('historical-methods/') else 'runtime-tools' if row['consumer'].startswith('runtime/') else 'research-tools'
        key=(owner,consumer_class)
        item=concise.setdefault(key,dict(research_area=owner,consumer_class=consumer_class,literal_mentions=0,consumer_files=set(),example_consumer=row['consumer'],example_line=row['line'],adaptation='Controlled extraction or explicit locator adapter; literal mentions do not prove execution'))
        item['literal_mentions']+=1;item['consumer_files'].add(row['consumer'])
    short=[]
    for key,row in sorted(concise.items()):
        row['consumer_files']=len(row['consumer_files']);short.append(row)
    csvout('dependencies.csv',list(short[0]),short)
    options=[]
    for scheme,column in (('A-nine-system','scheme_a'),('B-six-system','scheme_b')):
        for owner,n,size in ownerdb.execute(f'select {column},count(*),sum(bytes) from owner group by {column} order by sum(bytes) desc'):
            areas=[r[0] for r in ownerdb.execute(f'select distinct area from owner where {column}=? order by area',(owner,))]
            options.append(dict(scheme=scheme,candidate_archive=owner,files=n,logical_bytes=size,research_areas='; '.join(areas),
                member_types='Original captures, native exports, receipts and derivatives mixed; retain member-level roles',
                access_frequency='UNKNOWN; offline research-on-demand, not measured',
                dependencies='Central original-path locator; legacy paths need controlled extraction/adaptation',
                decision='Loose hold' if owner.startswith('LOOSE') else 'PROPOSED; merge/split needs maintainer approval'))
    csvout('archive-options.csv',list(options[0]),options)
    write(LOCAL/f'source-reference-pins{label}.json',documents)
    write(LOCAL/f'expected-sample-pin-candidates{label}.json',pins)
    write(LOCAL/f'discovery-summary{label}.json',dict(areas=len(out),directories=len(directories),files=sum(r['files'] for r in out),logical_bytes=sum(r['logical_bytes'] for r in out),dependency_mentions=len(dependencies),source_files=len(documents),scheme_A_archives=sum(not r['candidate_archive'].startswith('LOOSE') for r in options if r['scheme']=='A-nine-system'),scheme_B_archives=sum(not r['candidate_archive'].startswith('LOOSE') for r in options if r['scheme']=='B-six-system'),no_final_mapping=True))
    print(json.dumps(json.loads((LOCAL/f'discovery-summary{label}.json').read_text()),indent=2))


if __name__=='__main__':
    main()
