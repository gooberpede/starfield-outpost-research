# SPDX-License-Identifier: GPL-3.0-or-later
"""Apply the maintainer's save-file hold using frozen namespace metadata only.

No file/container payload reads. Preserve whole-estate accounting and clearly
separate save, opaque-container, current-work and unknown holds. No retirement.
"""
from collections import defaultdict
import csv
import argparse
import json
from pathlib import Path
import re
import sqlite3

from inventory import ROOT,LOCAL,DOC,csvout,write
from archive import pin


def held(path,top,extension):
    lower=path.lower()
    if extension=='.sfs':return 'HELD-SAVED-FILES'
    if top in ('savegames','third-party'):return 'HELD-SAVE-CORPUS-ROOT'
    if extension in ('.zip','.7z','.rar','.gz','.tar','.zst'):return 'HELD-OPAQUE-CONTAINER'
    if extension in ('.bin','.dat','.raw') and ('.sfs.' in lower or re.search(r'decompress|decoded|inflated|save[-_]stream|save[-_]payload',lower)
            or top in ('manual-S0-S7C','output-link-L0-L2C','historical-inventory','manual-corpus-coordinate-correction','mature-save-offbook','mature-save-validation','save-capacity-location','p1-save29-derivatives','resource-save52')):
        return 'HELD-POSSIBLE-RAW-SAVE'
    if top=='evidence-archive-discovery':return 'LOOSE-ACTIVE-STAGE-A'
    if top in ('scratch','(root-files)'):return 'LOOSE-UNKNOWN'
    return None


def main():
    from archive import space
    space(1024*1024*1024)
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--label',required=True);args=ap.parse_args()
    if not args.label.isalnum():raise ValueError('Fresh alphanumeric label')
    label=args.label
    source=LOCAL/'inventory03.sqlite';summary=json.loads((LOCAL/'inventory-summary03.json').read_text())
    assert pin(source)==summary['inventory_sha256']
    db=sqlite3.connect(f'file:{source.as_posix()}?mode=ro',uri=True)
    owners=sqlite3.connect(f'file:{(LOCAL/"candidate-owners03.sqlite").as_posix()}?mode=ro',uri=True)
    target=LOCAL/f'candidate-owners-scoped{label}.sqlite'
    if target.exists():raise RuntimeError('Refuse scoped candidate overwrite')
    out=sqlite3.connect(target)
    out.execute('create table candidate(path text primary key,area text,scope_state text,scheme_a text,scheme_b text,bytes integer,allocation_estimate integer,role text)')
    physical={r[0]:r[1:] for r in owners.execute('select path,area,scheme_a,scheme_b from owner')}
    groups=defaultdict(lambda:dict(files=0,bytes=0,allocation_estimate=0))
    for path,top,size,allocation,ext,role in db.execute('select path,directory,bytes,allocation_estimate,extension,role from files'):
        area,scheme_a,scheme_b=physical[path];reason=held(path,top,ext)
        state=reason or 'ELIGIBLE-NON-SAVE-PROPOSAL'
        if reason:scheme_a=scheme_b=reason
        out.execute('insert into candidate values(?,?,?,?,?,?,?,?)',(path,area,state,scheme_a,scheme_b,size,allocation or 0,role))
        groups[state]['files']+=1;groups[state]['bytes']+=size;groups[state]['allocation_estimate']+=allocation or 0
    out.commit()
    rows=[]
    for scheme,column in (('A-nine-system','scheme_a'),('B-six-system','scheme_b')):
        for owner,n,size in out.execute(f'select {column},count(*),sum(bytes) from candidate group by {column} order by sum(bytes) desc'):
            areas=[r[0] for r in out.execute(f'select distinct area from candidate where {column}=? order by area',(owner,))]
            rows.append(dict(scheme=scheme,candidate_archive=owner,files=n,logical_bytes=size,research_areas='; '.join(areas),
                member_types=('Saved payloads/copies; outside current proposal' if owner.startswith('HELD-SAVED') else 'Save-corpus metadata/payloads held separately' if owner.startswith('HELD-SAVE-CORPUS') else 'Opaque contents UNKNOWN; not a non-save qualification' if owner.startswith('HELD-OPAQUE') else 'Known/possible raw save representation; held' if owner.startswith('HELD-POSSIBLE') else 'Loose active or unknown working content' if owner.startswith('LOOSE') else 'Non-save native/capture/receipt/derived/working mix; preserve original roles'),
                access_frequency='UNKNOWN per member; research-on-demand proposed',
                dependencies='One central path/owner index; controlled extraction or explicit locator adaptation',
                decision='HELD / not current archival scope' if owner.startswith(('HELD','LOOSE')) else 'PROPOSED; no approved boundary or migration'))
    # Preserve the original pre-amendment authored table as a local derivative.
    with (LOCAL/f'archive-options-before-scope{label}.csv').open('xb') as f:f.write((DOC/'archive-options.csv').read_bytes())
    csvout('archive-options.csv',list(rows[0]),rows)
    breakdown=[dict(scope_state=key,**value) for key,value in sorted(groups.items())]
    csvout('scope-accounting.csv',list(breakdown[0]),breakdown)
    assert sum(r['files'] for r in breakdown)==summary['files']
    assert sum(r['bytes'] for r in breakdown)==summary['logical_bytes']
    eligible=groups['ELIGIBLE-NON-SAVE-PROPOSAL']
    proof=json.loads((LOCAL/'reproduction-proof.json').read_text())
    proof_paths={r[0] for r in out.execute("select path from candidate where scope_state='ELIGIBLE-NON-SAVE-PROPOSAL'")}
    reusable=[r for r in proof if r['path'] in proof_paths]
    retention=dict(eligible_files=eligible['files'],eligible_bytes=eligible['bytes'],eligible_allocation_estimate=eligible['allocation_estimate'],
        essential_files=eligible['files']-len(reusable),essential_bytes=eligible['bytes']-sum(r['bytes'] for r in reusable),
        reproducible_candidate_files=len(reusable),reproducible_candidate_bytes=sum(r['bytes'] for r in reusable),
        target_bytes=10_000_000_000,required_complete_ratio=10_000_000_000/eligible['bytes'],
        held=breakdown,whole_estate_files=summary['files'],whole_estate_bytes=summary['logical_bytes'],
        no_saved_file_payload_work=True,amendment='scope-amendment.md')
    write(LOCAL/f'scope-summary{label}.json',retention)
    csvout('retention.csv',['tier','files','logical_bytes','decision','evidence'],[
        dict(tier='Complete current non-save proposal',files=retention['eligible_files'],logical_bytes=retention['eligible_bytes'],decision='KEEP all unique/primary/unknown content; current scope only',evidence='Frozen inventory03 + accepted scope amendment'),
        dict(tier='Essential current non-save proposal',files=retention['essential_files'],logical_bytes=retention['essential_bytes'],decision='Only proven deterministic stand-ins omitted as a proposal; no deletion',evidence='reproduction-proof.json; retain builder, baseline, ZIP and actual receipts'),
        dict(tier='Proven reproducible stand-in candidate',files=len(reusable),logical_bytes=sum(r['bytes'] for r in reusable),decision='Future retirement needs explicit retention/cutover approval',evidence='Exact pinned builder, original manifest and fresh byte-hash equality'),
        *[dict(tier=r['scope_state'],files=r['files'],logical_bytes=r['bytes'],decision='HELD; preserved and outside current backup/recovery denominator',evidence='Metadata scope rule; uncertain content is not called disposable') for r in breakdown if r['scope_state']!='ELIGIBLE-NON-SAVE-PROPOSAL']])
    with (LOCAL/f'benchmark-measurements-before-scope{label}.csv').open('xb') as f:f.write((DOC/'benchmark-measurements.csv').read_bytes())
    old=list(csv.DictReader((DOC/'benchmark-measurements.csv').read_text().splitlines()))
    filtered=[r for r in old if r['sample']!='protected-save-copy']
    csvout('benchmark-measurements.csv',list(filtered[0]),filtered)
    print(json.dumps(retention,indent=2))


if __name__=='__main__':main()
