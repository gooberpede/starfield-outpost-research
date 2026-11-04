# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate retained N1 bytes and D5AN protected baseline without live work.

Reads the closed N1 raw root, historical proof/build, initial D5AN fingerprints
and selected protected save/backup/database files. Writes one fresh local JSON
receipt only. Adapts the maintainer-owned N1 failure-proof framing method under
SOR-P-0002; source provenance is recorded in the receipt. Uses Python stdlib;
no game, deployment, database open, save/configuration, Git or network writes.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
from pathlib import Path
import hashlib
import json
import struct
import zlib
import argparse
import subprocess
import zipfile
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'.local-work/d5an'
SESSION=ROOT/'.local-work/d5am/live/session-838701ec716cd8bccf0929c4beb9f7e8bfe816b5fb77328007ba9e1cb77b06a8'

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--preservation',action='store_true')
    args=parser.parse_args();out=args.out.resolve()
    require(out.is_relative_to(LOCAL) and not out.exists(),'Exclusive task-local receipt required')
    require(not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'Reparse output refused')
    from d5am_lock_qualify import guard
    free=guard()
    proof_path=ROOT/'.local-work/d5am/n1-live01/failure-proof03.json'
    proof=json.loads(proof_path.read_bytes())
    current={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in SESSION.iterdir() if p.is_file()}
    require(current==proof['original_files'],'Nine original N1 files differ')
    identity=json.loads((SESSION/'identity.json').read_bytes())
    ready=json.loads((SESSION/'ready.json').read_bytes())
    terminal=json.loads((SESSION/'terminal.json').read_bytes())
    idh=sha(SESSION/'identity.json')
    require(all(ready.get(k)==v and terminal.get(k)==v for k,v in identity.items()),'READY/terminal identity mismatch')
    require(ready['ready'] is True and terminal['failed'] is True and terminal['resident_inert'] is True,'Retained operational outcome differs')
    require(terminal['scheduler_counter_contention'] is True and terminal['scheduler_failed'] is True and terminal['output_fault']=='causal_or_scheduler_guard','Retained counter outcome differs')
    raw=(SESSION/'events.bin').read_bytes()
    require(len(raw)==328,'Unexpected core length')
    magic,size,sequence,crc=struct.unpack_from('<4I',raw)
    require((magic,size,sequence)==(0x31505253,312,1) and zlib.crc32(raw[16:])==crc,'Core CRC/framing mismatch')
    require(struct.unpack_from('<2Q',raw,16)==(1,13),'Expected lone internal READY')
    flush=[json.loads(line) for line in (SESSION/'flush.jsonl').read_bytes().splitlines()]
    require(len(flush)==1 and flush[0]['identity_sha256']==idh and flush[0]['records']==1 and flush[0]['bytes']==328 and flush[0]['prefix_crc32']==zlib.crc32(raw),'Flush prefix mismatch')
    for name in ('causal.bin','scheduler.bin','lifetimes.bin'):
        data=(SESSION/name).read_bytes()
        require(len(data)==96,'Sidecar not header-only: '+name)
        require(data[64:]==bytes.fromhex(idh) if name=='lifetimes.bin' else data[32:]==idh.encode(),'Sidecar identity mismatch')
    require(not any((SESSION/name).exists() for name in ('p4-owner.json','p4-state.json','request.txt','STOP','geometry-request-1.json')),'Unexpected ownership/command artifact')
    baseline_path=LOCAL/'baseline.json';baseline=json.loads(baseline_path.read_bytes())
    require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==baseline['head'],'HEAD changed')
    require(sha(ROOT/'.git/index')==baseline['index']['sha256'],'Index changed')
    old_selected=ROOT/'.local-work/d5am/selected-preservation03.json'
    selected=json.loads(old_selected.read_bytes())['rows']
    protected={p:dict(bytes=Path(p).stat().st_size,sha256=sha(p)) for p in selected}
    require(protected==selected,'Historical selected protected content changed')
    preserved={}
    if args.preservation:
        paths=list(baseline['preserved'])
        def compare(path):
            p=Path(path);return dict(bytes=p.stat().st_size,sha256=sha(p))==baseline['preserved'][path]
        with ThreadPoolExecutor(max_workers=4) as pool:
            preserved=dict(zip(paths,pool.map(compare,paths)))
        require(all(preserved.values()),'Original evidence/source/package baseline changed')
    historical={
        'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe':'7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28',
        '.local-work/d5am/package-final23/SorConstructionWinner-0.9.0-D5AM-final23-NOT-AUTHORIZED.zip':'41d9952804431867929ad15f1093468cfb4360c454af03fa24f73de39dc75cde',
        '.local-work/d5am/package-guard-final02/SorConstructionWinner-0.9.1-D5AM-guard-final02-NOT-AUTHORIZED.zip':'816274053c800cd3de724bebafe5df7acfa46b0b41e87d39021ff5fbc0290a07',
        '.local-work/d5am/n0-archive01/N0-startup-failed-evidence.zip':'584a2a61c744d3491448d377f44613db922f666b66167b0dff82bc60962c2d0d',
        '.local-work/d5am/n1-archive01/n1-failed-session.zip':'e16329fa3adda3445c4f0dcbeac0ef6b403ae5a69b4b6be5d01484745c4f4f47',
        '.local-work/d5am/n1-prediction-freeze-v1.json':'a7a2a098ae2d7b87203b73057ab1ed4ddf9f2eb9eb5786aedb3aa64c2dab0ffc',
        'docs/experiments/resource-retained-population/d5am-n1-prediction-text-v1.md':'514da87c5e34be408c9f58d1adf1f45d2c74f8fa424df88e08eb2841ef423c1c'}
    require(all(sha(ROOT/p)==h for p,h in historical.items()),'Reported historical package/archive/prediction pin changed')
    archives={}
    for folder,name in (('n0-archive01','N0-startup-failed-evidence.zip'),('n1-archive01','n1-failed-session.zip')):
        base=ROOT/'.local-work/d5am'/folder;seal=json.loads((base/'seal.json').read_bytes())
        actual={label+'/'+p.relative_to(Path(row['path'])).as_posix() for label,row in seal['roots'].items() for p in Path(row['path']).rglob('*') if p.is_file()}
        require(actual==set(seal['files']),'Historical sealed-root inventory changed')
        with zipfile.ZipFile(base/name) as archive:
            require(len(archive.namelist())==len(seal['files'])+1 and set(archive.namelist())==set(seal['files'])|{'SOR-MANIFEST.json'},'Historical archive roster mismatch')
            require(json.loads(archive.read('SOR-MANIFEST.json'))==seal,'Historical embedded seal mismatch')
            for member,row in seal['files'].items():
                root,relative=member.split('/',1);original=Path(seal['roots'][root]['path'])/relative
                require(original.stat().st_size==row['size'] and sha(original)==row['sha256'],'Historical sealed original differs: '+member)
                with archive.open(member) as stream:
                    require(hashlib.file_digest(stream,'sha256').hexdigest()==row['sha256'],'Historical ZIP member differs: '+member)
        archives[folder]=dict(payloads=len(seal['files']),originals_equal=True,every_member_equal=True)
    build=ROOT/'.local-work/d5am/guard-final02'
    binary=build/'SorConstructionWinner.dll'
    tools=json.loads((ROOT/'.local-work/d5am/package-guard-final02/package.json').read_bytes())['selected_tools']
    tool_results={name:sha(row['path'])==row['sha256'] for name,row in tools.items()}
    require(all(tool_results.values()),'Historical pinned toolchain changed')
    require(sha(binary)==identity['dll_sha256'],'Historical N1 compiled binary mismatch')
    result=dict(schema='sor-d5an-evidence-audit/1',status='PASS',method_sha256=sha(__file__),
        owned_method_basis=dict(path='.local-work/d5am/n1-live01/failure-proof03.py',sha256=sha(ROOT/'.local-work/d5am/n1-live01/failure-proof03.py')),
        original_files=current,identity_sha256=idh,core=dict(records=1,kind=13,crc32=zlib.crc32(raw)),
        terminal={k:terminal[k] for k in ('failed','resident_inert','output_fault','scheduler_counter_contention','scheduler_failed','scheduler_counter_overflow','causal_native_counter_faults')},
        selected_protected=protected,preserved=preserved,historical_pins=historical,historical_archives=archives,selected_tools=tools,tools_equal=tool_results,
        initial_free=free,final_free=guard(),
        interpretation='N1 records aggregate scheduler fault bit 2 and no producer/thread provenance. A bounded-refusal path is supported; its exact operation, interleaving and historical cause remain unknown. No acquisition or loss-absence claim follows.')
    with out.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(status='PASS',original_files=len(current),protected=len(protected),preserved=len(preserved))))

if __name__=='__main__':
    main()
