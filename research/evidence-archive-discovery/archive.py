# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable Stage A tar.zst/ZIP prototype with one logical central SQLite index.

Original stdlib implementation informed by owned session-tools archive safety.
Reads only marked copied/synthetic trees. Never migrate/delete original evidence.
An externally supplied index digest authenticates archive/member expectations.
"""
import hashlib
import io
import json
import os
import ntpath
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import stat
import struct
import tarfile
import time
import unicodedata
import uuid
import zipfile
from compression.zstd import ZstdFile

ROOT=Path(__file__).resolve().parents[2]
SPACE=ROOT/'.local-work/evidence-archive-discovery'
MARKER='STAGE_A_DISPOSABLE'
CHUNK=1024*1024


class ArchiveError(RuntimeError):
    pass


def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def guard(path):
    path=Path(path).absolute()
    if not path.is_relative_to(SPACE) or not path.resolve().is_relative_to(SPACE.resolve()):
        raise ArchiveError('Output outside isolated Stage A workspace')
    for parent in (path,*path.parents):
        if parent.exists() and parent.lstat().st_file_attributes & 0x400:
            raise ArchiveError('Reparse escape')
    return path


def space(reserve=0):
    values={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    if values['C:/']<40_000_000_000 or values['D:/']<40_000_000_000+reserve:
        raise ArchiveError('Free-space/write-reservation guard')
    return values


def safe_name(name):
    parts=name.split('/')
    if (not name or name.startswith('/') or any(c in name for c in '\\:<>"|?*')
            or any(ord(c)<32 for c in name) or any(p in ('','.','..') or p.endswith((' ','.')) for p in parts)
            or any(ntpath.isreserved(p) for p in parts)
            or any(re.fullmatch(r'(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(\..*)?',p) for p in parts)):
        raise ArchiveError('Unsafe member name')
    if len(name.encode('utf8'))>4096:
        raise ArchiveError('Bounded canonical path length')
    return PurePosixPath(name)


def names_valid(names):
    seen=set()
    for name in names:
        safe_name(name)
        key=unicodedata.normalize('NFC',name).casefold()
        if key in seen:
            raise ArchiveError('Duplicate/case/Unicode collision')
        seen.add(key)
    if any(str(parent) in seen for name in seen for parent in PurePosixPath(name).parents if str(parent)!='.'):
        raise ArchiveError('File/ancestor collision')


def publish(partial,target):
    """Retry only transient Windows rename refusal; never replace a destination."""
    partial=guard(partial);target=guard(target)
    for attempt in range(5):
        if target.exists():raise ArchiveError('Publish destination already exists')
        try:
            partial.rename(target)
            return attempt
        except PermissionError as exc:
            if getattr(exc,'winerror',None) not in (5,32) or attempt==4:raise
            time.sleep(0.05*(attempt+1))


def init_index(path):
    space(4*1024*1024)
    path=guard(path)
    if path.exists():
        raise ArchiveError('Refuse index overwrite')
    db=sqlite3.connect(path)
    db.execute('create table archives(id text primary key, filename text, format text, digest text, bytes integer, grouping_version text)')
    db.execute('create table members(archive_id text, path text, digest text, bytes integer, original_location text, research_system text, primary key(archive_id,path))')
    db.execute('create table cross_references(consumer_system text, original_location text, owner_archive text, member_path text)')
    db.execute('create table aliases(archive_id text, original_location text, member_path text, digest text, bytes integer, primary key(archive_id,original_location))')
    db.execute('pragma user_version=2')
    db.commit();db.close()


def register(index,archive_id,archive,fmt,members,version='STAGE-A-PROTOTYPE'):
    """Register only caller-authenticated, already verified disposable members."""
    metadata=sum(len(n.encode('utf8'))*3+len(r['original_location'].encode('utf8'))*2+1024 for n,r in members.items())
    space(Path(index).stat().st_size*2+metadata*4+8*1024*1024)
    db=sqlite3.connect(guard(index))
    try:
        with db:
            db.execute('insert into archives values(?,?,?,?,?,?)',(archive_id,str(guard(archive)),fmt,pin(archive),Path(archive).stat().st_size,version))
            db.executemany('insert into members values(?,?,?,?,?,?)',[(archive_id,n,r['sha256'],r['bytes'],r['original_location'],r['system']) for n,r in members.items()])
            db.executemany('insert into aliases values(?,?,?,?,?)',[(archive_id,r['original_location'],n,r['sha256'],r['bytes']) for n,r in members.items()])
    finally:
        db.close()
    return pin(index)


def load(index,expected_index,archive_id):
    path=guard(index)
    if path.stat().st_size>256*1024*1024:
        raise ArchiveError('Master-index size bound')
    raw=path.read_bytes()
    if len(raw)>256*1024*1024 or hashlib.sha256(raw).hexdigest()!=expected_index:
        raise ArchiveError('Master-index identity mismatch')
    db=sqlite3.connect(':memory:')
    try:
        db.deserialize(raw)
        db.execute('pragma trusted_schema=off')
        if db.execute('pragma user_version').fetchone()[0] not in (0,2):
            raise ArchiveError('Unsupported index schema')
        row=db.execute('select filename,format,digest,bytes from archives where id=?',(archive_id,)).fetchone()
        if row is None:
            raise ArchiveError('Missing archive identity')
        members={n:dict(sha256=d,bytes=s,original_location=o,system=a) for n,d,s,o,a in db.execute('select path,digest,bytes,original_location,research_system from members where archive_id=?',(archive_id,))}
        if not members or len(members)>300000 or any(r['bytes']<0 for r in members.values()):
            raise ArchiveError('Prototype member bound')
        names_valid(members)
        if db.execute('pragma user_version').fetchone()[0]==2:
            aliases=list(db.execute('select original_location,member_path,digest,bytes from aliases where archive_id=?',(archive_id,)))
            names_valid([r[0] for r in aliases])
            for original,name,digest,size in aliases:
                if name not in members or members[name]['sha256']!=digest or members[name]['bytes']!=size:
                    raise ArchiveError('Alias content identity mismatch')
        return row,members,len(raw)
    finally:
        db.close()


def stream_members(archive,fmt,members,sink=None):
    """Bound decoding by authenticated member counts/sizes; never extractall()."""
    archive=guard(archive)
    names_valid(members)
    seen=set();payload=0
    def consume(name,size,reader):
        nonlocal payload
        safe_name(name)
        if name in seen or name not in members or size!=members[name]['bytes']:
            raise ArchiveError('Missing/extra/substituted member metadata')
        seen.add(name);digest=hashlib.sha256();remaining=size
        output=sink(name) if sink else None
        try:
            while remaining:
                data=reader.read(min(CHUNK,remaining))
                if not data:
                    raise ArchiveError('Truncated member')
                remaining-=len(data);digest.update(data);payload+=len(data)
                if output:output.write(data)
            if digest.hexdigest()!=members[name]['sha256']:
                raise ArchiveError('Member hash mismatch')
        finally:
            if output:output.close()
    if fmt=='tar.zst':
        bound=sum(((r['bytes']+511)//512)*512+512+8704 for r in members.values())+10240
        decoded=0
        with ZstdFile(archive,'rb') as z:
            def read(n):
                nonlocal decoded
                data=z.read(n);decoded+=len(data)
                if decoded>bound:
                    raise ArchiveError('Archive expansion bound')
                return data
            class Limited:
                def read(self,n):return read(n)
            pending_path=None
            while True:
                header=read(512)
                if len(header)!=512:
                    raise ArchiveError('Truncated tar header/footer')
                if header==b'\0'*512:
                    if pending_path is not None:raise ArchiveError('Unconsumed PAX path')
                    second=read(512)
                    if second!=b'\0'*512:
                        raise ArchiveError('Missing tar end marker')
                    while True:
                        tail=read(10240)
                        if not tail:break
                        if tail.strip(b'\0'):
                            raise ArchiveError('Hidden trailing tar content')
                    break
                info=tarfile.TarInfo.frombuf(header,'utf8','strict')
                if info.type==tarfile.XHDTYPE:
                    if pending_path is not None or info.size<=0 or info.size>8192:
                        raise ArchiveError('PAX metadata bound')
                    raw=read(info.size);padding=read((-info.size)%512)
                    if len(raw)!=info.size or padding.strip(b'\0'):
                        raise ArchiveError('Truncated PAX data')
                    offset=0;attributes={}
                    while offset<len(raw):
                        end=raw.find(b' ',offset,offset+12)
                        if end<0 or not raw[offset:end].isdigit():raise ArchiveError('PAX record length')
                        length=int(raw[offset:end]);record=raw[end+1:offset+length]
                        if length<=end-offset+2 or offset+length>len(raw) or not record.endswith(b'\n'):
                            raise ArchiveError('PAX record bounds')
                        key,separator,value=record[:-1].partition(b'=')
                        if key!=b'path' or not separator or key in attributes:raise ArchiveError('Unsupported PAX override')
                        attributes[key]=value.decode('utf8','strict');offset+=length
                    pending_path=attributes.get(b'path')
                    if pending_path is None:raise ArchiveError('Missing PAX path')
                    safe_name(pending_path)
                    continue
                if info.type not in (tarfile.REGTYPE,tarfile.AREGTYPE) or info.pax_headers or info.sparse:
                    raise ArchiveError('Links/special/extended tar member rejected')
                consume(pending_path or info.name,info.size,Limited());pending_path=None
                padding=read((-info.size)%512)
                if len(padding)!=(-info.size)%512 or padding.strip(b'\0'):
                    raise ArchiveError('Invalid tar member padding')
    elif fmt=='zip':
        if len(members)>65534:raise ArchiveError('ZIP alternative is sample-scale only; use tar.zst for large member populations')
        # Bound central-directory construction before ZipFile loads its members.
        with Path(archive).open('rb') as f:
            f.seek(max(0,Path(archive).stat().st_size-65557));tail=f.read()
        pos=tail.rfind(b'PK\x05\x06')
        if pos<0 or len(tail)-pos<22:
            raise ArchiveError('Missing ZIP end record')
        count=struct.unpack_from('<H',tail,pos+10)[0]
        central=struct.unpack_from('<I',tail,pos+12)[0]
        if count!=len(members) or central>len(members)*8192:
            raise ArchiveError('ZIP central-directory bound')
        with zipfile.ZipFile(archive) as z:
            infos=z.infolist();names_valid([i.filename for i in infos])
            for info in infos:
                kind=(info.external_attr>>16)&0o170000
                if info.is_dir() or kind not in (0,stat.S_IFREG) or info.flag_bits&1 or len(info.extra)>4096:
                    raise ArchiveError('ZIP special/encrypted member')
                with z.open(info) as f:consume(info.filename,info.file_size,f)
    else:
        raise ArchiveError('Unsupported format')
    if seen!=set(members):
        raise ArchiveError('Missing expected member')
    return dict(member_count=len(seen),payload_bytes_hashed=payload,member_hash_invocations=len(seen))


def verify(index,expected_index,archive_id):
    start=time.perf_counter();row,members,index_bytes=load(index,expected_index,archive_id)
    filename,fmt,digest,size=row;archive=guard(filename)
    if archive.stat().st_size!=size or pin(archive)!=digest:
        raise ArchiveError('Archive-byte identity mismatch')
    hashed=time.perf_counter()
    result=stream_members(archive,fmt,members)
    result.update(index_bytes_hashed=index_bytes,archive_bytes_hashed=size,
        archive_hash_seconds=hashed-start,full_member_verify_seconds=time.perf_counter()-hashed,
        wall_seconds=time.perf_counter()-start,archive_sha256=digest)
    return result


def resolve(index,expected_index,consumer_system,original_location):
    """Resolve a cross-system locator under an authenticated index version."""
    path=guard(index)
    if path.stat().st_size>256*1024*1024:raise ArchiveError('Index size bound')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_index:raise ArchiveError('Resolver index identity mismatch')
    db=sqlite3.connect(':memory:')
    try:
        db.deserialize(raw)
        rows=db.execute('select owner_archive,member_path from cross_references where consumer_system=? and original_location=?',
                        (consumer_system,original_location)).fetchall()
        if len(rows)!=1:raise ArchiveError('Missing/ambiguous central locator')
        version=db.execute('pragma user_version').fetchone()[0]
        alias=db.execute('select member_path,digest,bytes from aliases where archive_id=? and original_location=?',(rows[0][0],original_location)).fetchone() if version==2 else None
    finally:db.close()
    archive_id,name=rows[0];row,members,_=load(index,expected_index,archive_id)
    if name not in members or (members[name]['original_location']!=original_location and alias!=(name,members[name]['sha256'],members[name]['bytes'])):
        raise ArchiveError('Cross-reference ownership mismatch')
    return dict(archive_id=archive_id,member_path=name,archive=row,members=members,expected=members[name])


def add_alias(index,expected_index,archive_id,original_location,member_path):
    """Add a caller-intake-verified duplicate path; never infer equality by name."""
    space(Path(index).stat().st_size*2+len(original_location.encode('utf8'))*8+1024*1024)
    row,members,_=load(index,expected_index,archive_id)
    safe_name(original_location)
    if member_path not in members:raise ArchiveError('Missing alias owner')
    db=sqlite3.connect(guard(index))
    try:
        if db.execute('pragma user_version').fetchone()[0]!=2:raise ArchiveError('Alias writer requires schema 2')
        current=[r[0] for r in db.execute('select original_location from aliases where archive_id=?',(archive_id,))]
        names_valid([*current,original_location])
        with db:db.execute('insert into aliases values(?,?,?,?,?)',(archive_id,original_location,member_path,members[member_path]['sha256'],members[member_path]['bytes']))
    finally:db.close()
    return pin(index)


def restore_alias(index,expected_index,consumer_system,original_location,destination):
    """Restore one centrally resolved original path, freshly verifying its owner."""
    found=resolve(index,expected_index,consumer_system,original_location)
    target=guard(destination)
    if target.exists():raise ArchiveError('Alias destination exists')
    space(found['expected']['bytes']+(len(PurePosixPath(original_location).parents)+3)*8192)
    filename,fmt,digest,size=found['archive'];filename=guard(filename)
    if pin(filename)!=digest:raise ArchiveError('Alias archive identity mismatch')
    partial=guard(target.with_name(target.name+'.partial-'+uuid.uuid4().hex));partial.mkdir(parents=True,exist_ok=False)
    def sink(name):
        if name!=found['member_path']:return None
        path=guard(partial/safe_name(original_location));path.parent.mkdir(parents=True,exist_ok=True)
        return path.open('xb')
    stream_members(filename,fmt,found['members'],sink)
    if pin(partial/original_location)!=found['expected']['sha256']:raise ArchiveError('Alias restored-byte mismatch')
    publication_retries=publish(partial,target)
    return dict(original_location=original_location,canonical_member=found['member_path'],owner_archive=found['archive_id'],sha256=found['expected']['sha256'],publication_retries=publication_retries)


def pack(copy_root,index,archive_id,fmt,members,interrupt=None):
    start=time.perf_counter();copy_root=guard(copy_root)
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,100}',archive_id):raise ArchiveError('Unsafe archive identifier')
    if not (copy_root/MARKER).is_file():raise ArchiveError('Disposable marker required')
    names_valid(members);total=sum(r['bytes'] for r in members.values())
    # Conservative write reservation includes compression/container expansion,
    # per-member headers/metadata and the bounded SQLite index + rollback journal.
    space(total*2+len(members)*16384+512*1024*1024)
    target=guard(copy_root.parent/'archives'/(archive_id+('.tar.zst' if fmt=='tar.zst' else '.zip')))
    target.parent.mkdir(exist_ok=True)
    if target.exists():raise ArchiveError('Refuse archive overwrite')
    partial=target.with_name(target.name+'.partial')
    if partial.exists():raise ArchiveError('Refuse partial overwrite')
    read_bytes=0
    class Source:
        def __init__(self,stream):self.stream=stream;self.digest=hashlib.sha256();self.bytes=0
        def read(self,n=-1):
            nonlocal read_bytes
            data=self.stream.read(n);self.digest.update(data);self.bytes+=len(data);read_bytes+=len(data)
            if interrupt:interrupt(self.bytes)
            return data
    with partial.open('xb') as output:
        if fmt=='tar.zst':
            container=tarfile.open(fileobj=output,mode='w:zst',format=tarfile.PAX_FORMAT,level=3)
        elif fmt=='zip':
            container=zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)
        else:raise ArchiveError('Unknown packaging format')
        with container:
            for name,row in members.items():
                source=guard(copy_root/name)
                if source.stat().st_size!=row['bytes']:raise ArchiveError('Intake size mismatch')
                with source.open('rb') as stream:
                    reader=Source(stream)
                    if fmt=='tar.zst':
                        info=tarfile.TarInfo(name);info.size=row['bytes'];info.mode=0o600;info.mtime=0
                        container.addfile(info,reader)
                    else:
                        info=zipfile.ZipInfo(name);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(stat.S_IFREG|0o600)<<16
                        with container.open(info,'w',force_zip64=True) as writer:
                            while data:=reader.read(CHUNK):writer.write(data)
                    if reader.bytes!=row['bytes'] or reader.digest.hexdigest()!=row['sha256']:
                        raise ArchiveError('Copied-input hash mismatch during packaging')
    created=time.perf_counter()
    # Authenticate member-to-intake equality before index publication.
    member_validation=stream_members(partial,fmt,members)
    digest=pin(partial);archive_size=partial.stat().st_size
    publication_retries=publish(partial,target)
    anchor=register(index,archive_id,target,fmt,members)
    return dict(id=archive_id,format=fmt,input_bytes=total,archive_bytes=archive_size,
        archive_sha256=digest,index_sha256=anchor,compression_ratio=archive_size/total if total else None,
        creation_seconds=created-start,initial_member_validation_seconds=time.perf_counter()-created,
        packaging_payload_bytes_read_hashed=read_bytes,initial_member_payload_bytes_hashed=member_validation['payload_bytes_hashed'],
        archive_bytes_hashed=archive_size*2,wall_seconds=time.perf_counter()-start,publication_retries=publication_retries,
        note='Two archive digest passes: pin partial then register final; manifest pin is additional small control I/O')


def restore(index,expected_index,archive_id,destination,fail_after=None):
    start=time.perf_counter();row,members,index_bytes=load(index,expected_index,archive_id)
    target=guard(destination)
    if target.exists():raise ArchiveError('Restore destination already exists')
    total=sum(r['bytes'] for r in members.values())
    directories={str(parent) for name in members for parent in PurePosixPath(name).parents if str(parent)!='.'}
    space(total+(len(members)+len(directories)+2)*8192)
    filename,fmt,digest,size=row;archive=guard(filename)
    if archive.stat().st_size!=size or pin(archive)!=digest:raise ArchiveError('Restore archive identity mismatch')
    partial=guard(target.with_name(target.name+'.partial-'+uuid.uuid4().hex))
    partial.mkdir(parents=True,exist_ok=False)
    def sink(name):
        path=guard(partial/safe_name(name))
        path.parent.mkdir(parents=True,exist_ok=True)
        stream=path.open('xb')
        if fail_after is None:return stream
        class Failing:
            def write(self,data):
                if stream.tell()+len(data)>fail_after:raise OSError('Injected restore write failure')
                return stream.write(data)
            def close(self):stream.close()
        return Failing()
    result=stream_members(archive,fmt,members,sink)
    # Independent full reread of restored bytes before publication.
    for name,expected in members.items():
        if pin(partial/name)!=expected['sha256']:raise ArchiveError('Restored member mismatch')
    publication_retries=publish(partial,target)
    result.update(wall_seconds=time.perf_counter()-start,restored_bytes_rehashed=total,
        archive_bytes_hashed=size,index_bytes_hashed=index_bytes,committed_destination=str(target),publication_retries=publication_retries)
    return result
