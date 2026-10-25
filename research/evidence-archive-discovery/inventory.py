# SPDX-License-Identifier: GPL-3.0-or-later
"""Inventory .local-work metadata only; never read/hash its payload population.

Reads namespace/stat metadata, prior expected pin receipts and tracked research
text. Writes a fresh ignored SQLite inventory and authored aggregate CSVs. No
original mutation, tool install, archive migration, deletion or target operation.
"""
from collections import defaultdict
import csv
import argparse
import ctypes
from ctypes import wintypes
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import time

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'.local-work/evidence-archive-discovery'
DOC=ROOT/'docs/experiments/evidence-archive-discovery'


def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def write(path,value):
    from archive import space
    payload=(json.dumps(value,indent=2)+'\n').encode('utf8')
    space(len(payload)+1024*1024)
    with path.open('xb') as f:f.write(payload)


def csvout(name,fields,rows):
    from archive import space
    space(64*1024*1024)
    DOC.mkdir(parents=True,exist_ok=True)
    with (DOC/name).open('w',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def area(top):
    """Provisional thematic ownership, not an approved archive boundary."""
    if top.startswith(('resource-','extractor-resource','outpost-biomes','engine-oracle','continuous-beacon','matching-source','native-availability','e1-','e2-','e3-')):
        return 'resources-production'
    if top.startswith(('cargo','c1-','c2-','c3-')):
        return 'cargo-transport'
    if top.startswith(('p1-','power')):
        return 'power'
    if top.startswith(('s1-','s2-','sd1-','sd2-','sd3-','save-capacity','output-link')) or top=='manual-S0-S7C':
        return 'storage-links'
    if top.startswith(('crew','cr1-','cr2-','cr3-','r1-','robots')):
        return 'crew-robots'
    if top.startswith(('l1-','l2-','l3-','da1-','build-catalogue','construction-variants')):
        return 'construction-limits-defense'
    if top.startswith(('historical-','savegames','save-menu','third-party','mature-save','manual-corpus','save-capacity')):
        return 'persistence-save-corpora'
    if top.startswith(('b0','b1-','b2','b3','b4','b5','rc1','rr1','coverage-audit','reviews','review-','diffs','completion-protocol','editorial','spacing-','prose-','typography','preservation-verification','evidence-archive-discovery')):
        return 'governance-publication-review'
    if top in ('recon','builds') or top.startswith(('event-','beacon-observer','adapter-','x87-','internal-observation','spatial-equivalence','local-readiness','session-tools','static-exhaustion','thread-control')):
        return 'native-observation-infrastructure'
    if top.startswith(('active-outpost','activated-','durable-','coordinate-','coordinate','cross-session','position-','ship-','spatial-','surface-','two-outpost','ordinary-beacon','existing-reference','fallback-grid','exact-beacon','geometry-','structural-','membership-','workshop-','lo1-','q-','q030-','native-oracle','native-output','exp0002')) or top=='screengrabs':
        return 'identity-location-lifecycle'
    return 'unclassified-working'


def role(path,pinned):
    ext=Path(path).suffix.lower()
    if ext in ('.sfs','.gbf','.gdt','.gpr'):
        return 'critical-or-original-candidate; KEEP', 'UNKNOWN exact ownership'
    if ext in ('.raw','.jsonl','.sro1','.wal','.png','.jpg'):
        return 'primary-observation-candidate; KEEP', 'UNKNOWN until source-specific review'
    if ext in ('.obj','.pdb','.lib','.exp'):
        return 'reproduction-candidate; HOLD', 'Requires exact source/toolchain proof'
    if any(x in path for x in ('/cases/','/qualification','/performance/','/review-patches/')):
        return 'working-or-qualification-candidate; HOLD', 'Names alone do not establish reproducibility'
    if ext in ('.json','.log','.tsv','.csv','.txt','.md','.diff'):
        return 'receipt-or-derived-or-evidence; KEEP', 'Semantics UNKNOWN without ledger'
    return 'other-or-unknown; KEEP', 'UNKNOWN'


def main():
    from archive import space
    space(1024*1024*1024)
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label',default='02')
    args=ap.parse_args()
    if not args.label.isalnum():
        raise ValueError('Alphanumeric fresh label required')
    start=time.perf_counter()
    for drive in ('C:/','D:/'):
        if shutil.disk_usage(drive).free<40_000_000_000:
            raise RuntimeError('Free-space guard')
    prior=ROOT/'.local-work/resource-predictability-contrast/audit-before.json'
    if pin(prior)!='a243c67c0e451aac21cbb5fcb671c9e94ad2b3806406d0fdec1b2626f153ab9b':
        raise RuntimeError('Prior inventory identity mismatch')
    expected=json.loads(prior.read_text())['pins']
    normalized={os.path.normcase(os.path.normpath(k)):v for k,v in expected.items()}
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.GetDiskFreeSpaceW.argtypes=[wintypes.LPCWSTR,*([ctypes.POINTER(wintypes.DWORD)]*4)]
    spc,bps,free,total=(wintypes.DWORD() for _ in range(4))
    if not kernel.GetDiskFreeSpaceW('D:\\',ctypes.byref(spc),ctypes.byref(bps),ctypes.byref(free),ctypes.byref(total)):
        raise ctypes.WinError(ctypes.get_last_error())
    cluster=spc.value*bps.value
    dbpath=LOCAL/('inventory'+args.label+'.sqlite')
    if dbpath.exists():
        raise RuntimeError('Refuse inventory overwrite')
    # Hold rows in memory while scanning; write inventory after namespace freeze
    # so it cannot count its own growing database as evidence storage.
    rows=[];errors=[];directories=0
    stack=[ROOT/'.local-work']
    while stack:
        folder=stack.pop()
        try:
            entries=list(os.scandir(folder))
        except OSError as exc:
            errors.append(dict(path=str(folder),error=str(exc)));continue
        for entry in entries:
            path=Path(entry.path)
            try:
                # DirEntry.stat gives zero identity fields on this Windows build.
                st=path.stat(follow_symlinks=False)
                if st.st_file_attributes & 0x400:
                    errors.append(dict(path=str(path),error='REPARSE: not followed'));continue
                if entry.is_dir(follow_symlinks=False):
                    directories+=1;stack.append(path);continue
                if not entry.is_file(follow_symlinks=False):
                    errors.append(dict(path=str(path),error='Unsupported namespace node'));continue
                rel=path.relative_to(ROOT).as_posix()
                tail=path.relative_to(ROOT/'.local-work').parts
                top=tail[0] if len(tail)>1 else '(root-files)'
                digest=normalized.get(os.path.normcase(os.path.normpath(str(path))))
                evidence_role,uncertainty=role(rel,bool(digest))
                allocated=None if st.st_file_attributes & (0x800|0x200) else ((st.st_size+cluster-1)//cluster)*cluster
                rows.append((rel,top,area(top),st.st_size,allocated,str(st.st_dev),str(st.st_ino),st.st_nlink,
                             Path(entry.name).suffix.lower(),evidence_role,uncertainty,digest,st.st_mtime_ns))
            except OSError as exc:
                errors.append(dict(path=str(path),error=str(exc)))
    frozen=datetime.datetime.now(datetime.timezone.utc).isoformat()
    db=sqlite3.connect(dbpath)
    db.execute('create table files(path text primary key, directory text, area text, bytes integer, allocation_estimate integer, device text, file_id text, links integer, extension text, role text, uncertainty text, original_pin text, mtime_ns integer)')
    db.executemany('insert into files values(?,?,?,?,?,?,?,?,?,?,?,?,?)',rows)
    db.execute('create index files_directory on files(directory)')
    db.execute('create index files_area on files(area)')
    db.commit()
    fields=['directory','proposed_research_system','files','logical_bytes','ordinary_allocation_estimate','allocation_unknown_files','D5G_original_pins','status','ownership','candidate_disposition']
    agg=[]
    for directory,system,n,b,a,u,p in db.execute('select directory,area,count(*),sum(bytes),sum(allocation_estimate),sum(allocation_estimate is null),sum(original_pin is not null) from files group by directory,area order by sum(bytes) desc,directory'):
        agg.append(dict(zip(fields,(directory,system,n,b,a or 0,u,p,'UNKNOWN current use; preserved historical content','Provisional thematic assignment; source-specific ownership pending','KEEP; candidate consolidation only'))))
    csvout('directory-inventory.csv',fields,agg)
    fields2=['proposed_research_system','files','logical_bytes','ordinary_allocation_estimate','allocation_unknown_files','D5G_original_pins','directories','roles','status','experiment_IDs','candidate_disposition']
    areas=[]
    for system,n,b,a,u,p in db.execute('select area,count(*),sum(bytes),sum(allocation_estimate),sum(allocation_estimate is null),sum(original_pin is not null) from files group by area order by area'):
        dirs=[r['directory'] for r in agg if r['proposed_research_system']==system]
        areas.append(dict(zip(fields2,(system,n,b,a or 0,u,p,';'.join(sorted(dirs)),'Primary/critical/derived/working/diagnostics mixed; file roles in local index','UNKNOWN active/historical per member','UNKNOWN until ledger join; directory names are not IDs','KEEP; proposal only'))))
    csvout('research-areas.csv',fields2,areas)
    csvout('research-areas-by-size.csv',fields2,sorted(areas,key=lambda r:(-r['logical_bytes'],-r['files'])))
    overlap=sum(row[11] is not None for row in rows)
    existing={os.path.normcase(os.path.normpath(str(ROOT/row[0]))) for row in rows}
    inside={p for p in normalized if p.startswith(os.path.normcase(str(ROOT/'.local-work'))+os.sep)}
    result=dict(utc_freeze=frozen,namespace='.local-work',files=len(rows),directories=directories,
        logical_bytes=sum(r[3] for r in rows),ordinary_allocation_estimate=sum(r[4] or 0 for r in rows),
        allocation_unknown_files=sum(r[4] is None for r in rows),cluster_bytes=cluster,
        unique_file_objects=len({(r[5],r[6]) for r in rows}),errors=errors,
        D5G_total_pins=len(normalized),D5G_inside_local_work=len(inside),D5G_current_overlap=overlap,
        D5G_inside_missing=len(inside-existing),D5G_outside_local_work=len(normalized)-len(inside),
        current_not_in_D5G=len(rows)-overlap,wall_seconds=time.perf_counter()-start,
        payload_population_hashed=False,inventory_sha256=pin(dbpath),
        allocation_method='Cluster-round ordinary logical sizes; compressed/sparse UNKNOWN; excludes MFT/ADS/ACL and directory allocation; hardlinks separately identified',
        snapshot_scope='Metadata observed during traversal, not atomic snapshot; includes task start receipts existing then, excludes later outputs')
    write(LOCAL/('inventory-summary'+args.label+'.json'),result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
