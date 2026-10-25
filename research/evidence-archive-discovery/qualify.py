# SPDX-License-Identifier: GPL-3.0-or-later
"""Adversarial archive tests on newly generated disposable inputs only.

One central test-index instance covers this suite, not one sidecar per test.
Fault archives/index copies are test vectors, never production evidence. No
original evidence deletion, migration, ACL change, target operation or upload.
"""
import hashlib
import argparse
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import tarfile
import zipfile
from compression.zstd import ZstdFile

import archive as a
from inventory import LOCAL,write


def main():
    a.space(1024*1024*1024)
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--label',required=True);args=ap.parse_args()
    if not args.label.isalnum():raise ValueError('Fresh alphanumeric label')
    out=LOCAL/('qualification'+args.label);out.mkdir(exist_ok=False)
    write(out/'freeze.json',dict(expected='All named attacks DETECT; negative controls, long-path roundtrip, central references and 70000-member tar validation ALLOW',
        cases=['unsafe names','duplicates','case/Unicode collisions','ancestor collision','tar symlink/hardlink/special/PAX overrides','corruption','truncation','missing/extra/substituted member','index substitution','archive+index co-substitution','interrupted packaging','failed restore','existing destination','reparse destination','expansion bomb','space guard','long path','central cross-reference','empty member roundtrip','transient publication retry','permanent publication refusal','70000-member tar'],
        method_sha256=a.pin(Path(a.__file__))))
    copies=out/'copies';copies.mkdir();(copies/a.MARKER).write_text('synthetic only\n',encoding='utf8')
    content={'.local-work/synthetic/native.bin':b'\x07\x93'*2048,'.local-work/synthetic/receipt.txt':b'Original receipt.\n'}
    members={}
    for name,data in content.items():
        target=copies/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        members[name]=dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),original_location=name,system='synthetic')
    index=out/'master.sqlite';a.init_index(index)
    rows=[]
    def test(name,expected,fn):
        try:
            fn();observed='ALLOW';detail=''
        except Exception as exc:
            observed='DETECT';detail=type(exc).__name__+': '+str(exc)
        row=dict(case=name,expected=expected,observed=observed,passed=expected==observed,detail=detail)
        rows.append(row)
        print(name,observed,flush=True)
    for fmt in ('tar.zst','zip'):
        identity='qa-negative-'+fmt.replace('.','-')
        packed=a.pack(copies,index,identity,fmt,members)
        test('negative-'+fmt,'ALLOW',lambda identity=identity,anchor=packed['index_sha256']:a.verify(index,anchor,identity))
        test('restore-'+fmt,'ALLOW',lambda identity=identity,anchor=packed['index_sha256']:a.restore(index,anchor,identity,out/identity))
    unsafe=['../escape','/absolute','C:/drive','\\\\server\\share','a\\b','a:stream','a/NUL.txt','a/trailing.','a/trailing ','a//empty','a/./dot','a/COM¹.txt','a/LPT²','a/CONIN$','a/CONOUT$']
    for i,name in enumerate(unsafe):test('unsafe-name-'+str(i),'DETECT',lambda name=name:a.names_valid([name]))
    for name,names in [('duplicate',['a','a']),('case-collision',['a','A']),('unicode-collision',['é','e\u0301']),('ancestor-collision',['a','a/b'])]:
        test(name,'DETECT',lambda names=names:a.names_valid(names))
    def forged(label,kind):
        target=out/(label+'.tar.zst')
        with ZstdFile(target,'wb') as z,tarfile.open(fileobj=z,mode='w|',format=tarfile.PAX_FORMAT) as t:
            selected=dict(content)
            if kind=='missing':selected.pop(next(iter(selected)))
            if kind=='extra':selected['.local-work/synthetic/extra.bin']=b'extra'
            if kind=='substitution':selected[next(iter(selected))]=b'z'*len(next(iter(selected.values())))
            for name,data in selected.items():
                info=tarfile.TarInfo(name);info.size=len(data)
                if kind in ('symlink','hardlink','fifo'):
                    info.type={'symlink':tarfile.SYMTYPE,'hardlink':tarfile.LNKTYPE,'fifo':tarfile.FIFOTYPE}[kind];info.linkname='../outside';info.size=0
                if kind=='pax-size':info.pax_headers={'size':'99999999999'}
                if kind=='bomb':info.size=6_000_000_000
                if kind=='bomb':
                    # Header only: decoder must reject before attempting expansion.
                    z.write(info.tobuf(format=tarfile.USTAR_FORMAT));break
                t.addfile(info,io.BytesIO(data) if info.isreg() else None)
        return target
    for kind in ('missing','extra','substitution','symlink','hardlink','fifo','pax-size','bomb'):
        target=forged(kind,kind);identity='qa-'+kind
        anchor=a.register(index,identity,target,'tar.zst',members)
        test(kind,'DETECT',lambda identity=identity,anchor=anchor:a.verify(index,anchor,identity))
    base=Path(sqlite3.connect(index).execute("select filename from archives where id='qa-negative-tar-zst'").fetchone()[0])
    for kind in ('corrupt','truncated'):
        raw=bytearray(base.read_bytes())
        if kind=='corrupt':raw[len(raw)//2]^=1
        else:raw=raw[:-10]
        target=out/(kind+'.tar.zst');target.write_bytes(raw)
        anchor=a.register(index,'qa-'+kind,target,'tar.zst',members)
        test(kind,'DETECT',lambda kind=kind,anchor=anchor:a.verify(index,anchor,'qa-'+kind))
    expected_index=a.pin(index)
    tampered=out/'malicious-index.sqlite';tampered.write_bytes(index.read_bytes())
    db=sqlite3.connect(tampered);db.execute("update members set digest=?",('0'*64,));db.commit();db.close()
    test('index-substitution','DETECT',lambda:a.verify(tampered,expected_index,'qa-negative-tar-zst'))
    # A co-replaced archive/index cannot choose its own new expected root.
    db=sqlite3.connect(tampered);db.execute("update archives set digest=?",('1'*64,));db.commit();db.close()
    test('archive-and-index-co-substitution','DETECT',lambda:a.verify(tampered,expected_index,'qa-negative-tar-zst'))
    unsupported=out/'unsupported-index.sqlite';unsupported.write_bytes(index.read_bytes())
    bad=sqlite3.connect(unsupported);bad.execute('pragma user_version=999');bad.close()
    test('unsupported-index-schema','DETECT',lambda:a.verify(unsupported,a.pin(unsupported),'qa-negative-tar-zst'))
    test('decoder-root-escape','DETECT',lambda:a.stream_members(Path(__file__),'tar.zst',members))
    pair=out/'co-substituted-index.sqlite';pair.write_bytes(index.read_bytes())
    replacement=out/'substitution.tar.zst'
    co=sqlite3.connect(pair)
    co.execute("update archives set filename=?,digest=?,bytes=? where id='qa-negative-tar-zst'",
               (str(replacement),a.pin(replacement),replacement.stat().st_size))
    first=next(iter(content));co.execute("update members set digest=? where archive_id='qa-negative-tar-zst' and path=?",
        (hashlib.sha256(b'z'*len(content[first])).hexdigest(),first));co.commit();co.close()
    co=sqlite3.connect(pair);co.execute("update aliases set digest=? where archive_id='qa-negative-tar-zst' and member_path=?",
        (hashlib.sha256(b'z'*len(content[first])).hexdigest(),first));co.commit();co.close()
    test('co-substitution-internal-control','ALLOW',lambda:a.verify(pair,a.pin(pair),'qa-negative-tar-zst'))
    test('genuine-co-substitution-trusted-root','DETECT',lambda:a.verify(pair,expected_index,'qa-negative-tar-zst'))
    for kind in ('missing','extra','substitution','duplicate','case','symlink','truncated'):
        target=out/('zip-'+kind+'.zip')
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
            items=list(content.items())
            if kind=='missing':items.pop()
            if kind=='extra':items.append(('.local-work/synthetic/extra',b'extra'))
            if kind=='substitution':items[0]=(items[0][0],b'z'*len(items[0][1]))
            if kind=='duplicate':items[1]=(items[0][0],items[1][1])
            if kind=='case':items[1]=(items[0][0].upper(),items[1][1])
            for name,data in items:
                info=zipfile.ZipInfo(name);info.compress_type=zipfile.ZIP_DEFLATED
                if kind=='symlink':info.external_attr=(0o120777)<<16
                z.writestr(info,data)
        if kind=='truncated':
            raw=target.read_bytes();target.write_bytes(raw[:-20])
        anchor_zip=a.register(index,'qa-zip-'+kind,target,'zip',members)
        test('zip-'+kind,'DETECT',lambda kind=kind,anchor_zip=anchor_zip:a.verify(index,anchor_zip,'qa-zip-'+kind))
    def interrupt(n):raise InterruptedError('Injected packaging interruption')
    test('interrupted-packaging','DETECT',lambda:a.pack(copies,index,'qa-interrupted','tar.zst',members,interrupt))
    db=sqlite3.connect(index)
    assert db.execute("select count(*) from archives where id='qa-interrupted'").fetchone()[0]==0
    assert not (out/'archives/qa-interrupted.tar.zst').exists()
    anchor=a.pin(index)
    test('failed-restore','DETECT',lambda:a.restore(index,anchor,'qa-negative-tar-zst',out/'failed-restore',fail_after=1))
    assert not (out/'failed-restore').exists()
    test('existing-destination','DETECT',lambda:a.restore(index,anchor,'qa-negative-tar-zst',copies))
    link=out/'junction';target=out/'junction-target';target.mkdir()
    subprocess.run(['cmd','/c','mklink','/J',str(link),str(target)],check=True,capture_output=True)
    test('reparse-destination','DETECT',lambda:a.restore(index,anchor,'qa-negative-tar-zst',link/'escape'))
    assert not (target/'escape').exists()
    old=a.shutil.disk_usage
    try:
        a.shutil.disk_usage=lambda path:type('Usage',(),dict(free=39_000_000_000))()
        test('free-space-guard','DETECT',lambda:a.space())
    finally:a.shutil.disk_usage=old
    longname='.local-work/synthetic/'+'/'.join(['segment-abcdefghij']*16)+'/member.txt'
    target=copies/longname;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'long-path')
    longmembers={longname:dict(bytes=9,sha256=hashlib.sha256(b'long-path').hexdigest(),original_location=longname,system='synthetic')}
    packed=a.pack(copies,index,'qa-long-path','tar.zst',longmembers)
    test('long-path-roundtrip','ALLOW',lambda:a.restore(index,packed['index_sha256'],'qa-long-path',out/'long-restore'))
    # Two consumers reference one physical payload owner in this index version.
    with db:
        db.executemany('insert into cross_references values(?,?,?,?)',[(consumer,next(iter(members)),'qa-negative-tar-zst',next(iter(members))) for consumer in ('production','storage')])
    def crossrefs():
        resolved=db.execute('select distinct owner_archive,member_path from cross_references').fetchall()
        assert len(resolved)==1
        anchor=a.pin(index)
        for consumer in ('production','storage'):
            found=a.resolve(index,anchor,consumer,next(iter(members)))
            a.verify(index,anchor,found['archive_id'])
            captured=io.BytesIO()
            class Sink:
                def write(self,data):captured.write(data)
                def close(self):pass
            a.stream_members(found['archive'][0],found['archive'][1],found['members'],
                             lambda name:Sink() if name==found['member_path'] else None)
            assert captured.getvalue()==content[found['member_path']]
            assert hashlib.sha256(captured.getvalue()).hexdigest()==found['expected']['sha256']
    test('central-cross-reference','ALLOW',crossrefs)
    alias='.local-work/synthetic/second-original-path.bin';canonical=next(iter(members))
    anchor=a.add_alias(index,a.pin(index),'qa-negative-tar-zst',alias,canonical)
    with db:db.execute('insert into cross_references values(?,?,?,?)',('second-system',alias,'qa-negative-tar-zst',canonical))
    def alias_roundtrip():
        a.restore_alias(index,a.pin(index),'second-system',alias,out/'alias-restore')
        assert (out/'alias-restore'/alias).read_bytes()==content[canonical]
        assert db.execute("select count(*) from members where archive_id='qa-negative-tar-zst'").fetchone()[0]==len(members)
    test('duplicate-path-one-payload-alias','ALLOW',alias_roundtrip)
    zero='.local-work/synthetic/empty.bin';(copies/zero).write_bytes(b'')
    zero_members={zero:dict(bytes=0,sha256=hashlib.sha256(b'').hexdigest(),original_location=zero,system='synthetic')}
    packed=a.pack(copies,index,'qa-empty-member','tar.zst',zero_members)
    test('empty-member-roundtrip','ALLOW',lambda:a.restore(index,packed['index_sha256'],'qa-empty-member',out/'empty-restore'))
    for permanent in (False,True):
        source=out/('publish-partial-'+str(permanent));source.mkdir();(source/'data').write_bytes(b'probe')
        destination=out/('publish-final-'+str(permanent));original_rename=Path.rename;calls=[0]
        def refused(path,target):
            if path==source and (permanent or calls[0]==0):
                calls[0]+=1;error=PermissionError('Injected Windows publication refusal');error.winerror=5;raise error
            return original_rename(path,target)
        def publication_control():
            retries=a.publish(source,destination)
            assert retries==1 and (destination/'data').read_bytes()==b'probe'
        try:
            Path.rename=refused
            test('permanent-publication-refusal' if permanent else 'transient-publication-retry','DETECT' if permanent else 'ALLOW',publication_control)
        finally:Path.rename=original_rename
        if permanent:assert source.exists() and not destination.exists()
    scale_members={f'.local-work/scale/{i:06d}.bin':dict(bytes=0,sha256=hashlib.sha256(b'').hexdigest(),original_location=f'.local-work/scale/{i:06d}.bin',system='scale') for i in range(70000)}
    target=out/'scale.tar.zst'
    with ZstdFile(target,'wb') as z,tarfile.open(fileobj=z,mode='w|',format=tarfile.PAX_FORMAT) as t:
        for name in scale_members:t.addfile(tarfile.TarInfo(name),io.BytesIO(b''))
    anchor=a.register(index,'qa-scale',target,'tar.zst',scale_members)
    test('70000-member-tar','ALLOW',lambda:a.verify(index,anchor,'qa-scale'))
    write(out/'results.json',dict(tests=rows,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),
        index_sha256=a.pin(index),scale_members=70000,no_original_writes=True,no_original_deletions=True,
        limitations='Software fault tests only; no power-loss durability test; ZIP alternative intentionally sample-scale'))
    if any(not r['passed'] for r in rows):raise a.ArchiveError('Qualification failure; preserve all vectors')
    print('all controls passed',len(rows),flush=True)


if __name__=='__main__':main()
