# SPDX-License-Identifier: GPL-3.0-or-later
"""Prove one bounded reproducible tier and prepare a non-executed cargo pilot.

Reads generated historical stand-ins and future-pilot files without writing them.
All other primary/unknown content stays essential. Fresh candidate hashes are
explicitly not historical validation or deletion approval. Writes local receipts
and authored aggregate retention tables only.
"""
import hashlib
import json
from pathlib import Path
import sqlite3

from inventory import ROOT,LOCAL,DOC,csvout,write
from archive import pin,space


def main():
    space(1024*1024*1024)
    metadata=sqlite3.connect(f'file:{(LOCAL/"inventory03.sqlite").as_posix()}?mode=ro',uri=True)
    summary=json.loads((LOCAL/'inventory-summary03.json').read_text())
    assert pin(LOCAL/'inventory03.sqlite')==summary['inventory_sha256']
    prior=ROOT/'research/preservation-verification/qualify.py'
    if pin(prior)!='69681fbc9a98ccddb8c9ba4f7a2db03a4cb72a98b64f6a05a79e2b5d97785034':
        raise RuntimeError('Prior synthetic builder identity changed')
    fixture=ROOT/'.local-work/preservation-verification/run04/performance'
    if pin(fixture/'baseline.sqlite')!='77b04422e3c682888519783f937aa267c621d4722017043239cea859130075f3':
        raise RuntimeError('Prior fixture baseline changed')
    db=sqlite3.connect(f'file:{(fixture/"baseline.sqlite").as_posix()}?mode=ro',uri=True)
    proofs=[]
    for name,digest,size in db.execute("select path,digest,bytes from pins where path like '%.dat'"):
        path=fixture/name
        if name.startswith('historical/'):
            i=int(path.stem);n=1024 if i%64<48 else 16384 if i%64<63 else 262144
            regenerated=hashlib.sha256(bytes([i%251])*n).hexdigest()
        elif name.startswith('scientific/'):
            i=int(path.stem.split('-')[-1]);regenerated=hashlib.sha256(bytes([i])*4096).hexdigest()
        else:
            label=path.stem;label={'backup-manual':'manual-save','backup-quick':'quicksave','backup-designated':'designated-save'}.get(label,label)
            regenerated=hashlib.sha256(hashlib.sha256(label.encode()).digest()*8192).hexdigest()
        if regenerated!=digest or pin(path)!=digest:raise RuntimeError('Reproduction proof mismatch')
        proofs.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=digest,bytes=size,
            basis='Exact pinned builder formula + original fixture manifest + fresh current hash'))
    write(LOCAL/'reproduction-proof.json',proofs)
    all_files=summary['files'];all_bytes=summary['logical_bytes'];removable=sum(r['bytes'] for r in proofs)
    fields=['tier','files','logical_bytes','retention','evidence','confidence','permission_state']
    rows=[dict(zip(fields,('complete archival estate',all_files,all_bytes,'Retain all observed files including candidates',
        'Frozen inventory03; roles and ownership uncertainty preserved','Measured metadata; not payload semantics','NOT AUTHORIZED for migration'))),
        dict(zip(fields,('essential conservative estate',all_files-len(proofs),all_bytes-removable,'Retain every primary/unknown and all unique execution receipts',
        'Only proven run04 deterministic .dat payloads omitted from proposed essential set','Conservative; no claim that all other derivatives are irreplaceable','Retention proposal needs maintainer approval'))),
        dict(zip(fields,('reproducible stand-in candidate',len(proofs),removable,'Candidate for later approved retirement; originals unchanged here',
        'reproduction-proof.json: 4120 formula/manifest/current-byte equalities; retain builder, ZIP, baseline and test receipts','PROVEN current-byte reproducibility within this bounded synthetic set','No deletion approval')))]
    csvout('retention.csv',fields,rows)
    pilot=[]
    for path,size,prior_pin,role in metadata.execute("select path,bytes,original_pin,role from files where area='cargo-transport' order by path"):
        actual=pin(ROOT/path)
        if prior_pin is not None and actual!=prior_pin:raise RuntimeError('Pilot prior pin mismatch')
        pilot.append(dict(path=path,bytes=size,sha256=actual,prior_D5G_expected=prior_pin,
            provenance='Fresh Stage A candidate identity; not historical validation' if prior_pin is None else 'Prior expected hash freshly matched',
            role=role,disposition='NOT AUTHORIZED: complete cargo-system pilot candidate; no source moved/deleted'))
    for row in pilot:
        if pin(ROOT/row['path'])!=row['sha256']:raise RuntimeError('Pilot changed during qualification')
    write(LOCAL/'cargo-pilot-candidates.json',pilot)
    result=dict(complete_files=all_files,complete_bytes=all_bytes,essential_files=all_files-len(proofs),essential_bytes=all_bytes-removable,
        proven_reproducible_files=len(proofs),proven_reproducible_bytes=removable,
        target_compressed_bytes=10_000_000_000,required_complete_ratio=10_000_000_000/all_bytes,
        required_essential_ratio=10_000_000_000/(all_bytes-removable),
        pilot_files=len(pilot),pilot_bytes=sum(r['bytes'] for r in pilot),pilot_original_pin_matches=sum(r['prior_D5G_expected'] is not None for r in pilot),
        pilot_fresh_hash_passes=2,all_other_retirement_classes='UNKNOWN / HOLD; naming and age are not proof',
        no_real_deletion=True,no_final_retention_approval=True)
    write(LOCAL/'retention-summary.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
