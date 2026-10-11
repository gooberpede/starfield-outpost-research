"""SPDX-License-Identifier: GPL-3.0-or-later
Offline 0.1.3 WAL verifier/materializer; reads local evidence only. Creates NEW
explicit output, fsyncs derived sections/journal; never reads a target process.
The WAL is authoritative. A final incomplete frame is recoverable, not committed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct

MAGIC=b'SOREP013'
HEADER=88

def decode(path):
    data=Path(path).read_bytes();offset=0;previous=bytes(32);index=1;rows=[]
    while offset<len(data):
        left=len(data)-offset
        if left<HEADER:break
        magic=data[offset:offset+8]
        if magic!=MAGIC:raise ValueError('WAL magic integrity')
        length,sequence=struct.unpack_from('<QQ',data,offset+8)
        prior=data[offset+24:offset+56];digest=data[offset+56:offset+88]
        if sequence!=index or prior!=previous:raise ValueError('WAL sequence/chain integrity')
        if length>left-HEADER:break
        payload=data[offset+HEADER:offset+HEADER+length]
        actual=hashlib.sha256(struct.pack('<Q',sequence)+prior+payload).digest()
        if actual!=digest:raise ValueError('WAL frame integrity')
        row=json.loads(payload)
        if not isinstance(row,dict) or not isinstance(row.get('kind'),str):raise ValueError('WAL row schema')
        if row['kind']=='raw':
            b=bytes.fromhex(row['data_hex'])
            if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('WAL raw integrity')
        rows.append(row);previous=digest;index+=1;offset+=HEADER+length
    return rows,{'version':'0.1.3','wal_sha256':hashlib.sha256(data).hexdigest(),'committed_frames':index-1,'committed_bytes':offset,'incomplete_tail_bytes':len(data)-offset,'final_chain_sha256':previous.hex()}

def disk():
    # On Windows shutil.disk_usage uses caller-available bytes; failure propagates.
    import shutil
    if any(shutil.disk_usage(d).free<40_000_000_000 for d in ('C:/','D:/')):raise OSError('disk guard')

def durable(path,data):
    disk()
    with Path(path).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())

def materialize(source,output):
    source=Path(source);output=Path(output)
    rows,receipt=decode(source/'epochs.wal');disk();output.mkdir(exist_ok=False)
    count=0;terminal=None
    # Validation finishes BEFORE any output. Derived journal remains prefix-safe
    # if a write fails; retry only into another explicit NEW directory.
    with (output/'records.jsonl').open('xb') as journal:
        for original in rows:
            row=dict(original)
            if row['kind']=='terminal':terminal=row;continue
            if row['kind']=='raw':
                count+=1;name=f'raw-{count}.bin'
                durable(output/name,bytes.fromhex(row.pop('data_hex')));row['file']=name
            disk();journal.write((json.dumps(row,separators=(',',':'))+'\n').encode());journal.flush();os.fsync(journal.fileno())
    if terminal is not None and not receipt['incomplete_tail_bytes']:
        durable(output/'complete.json',(json.dumps(terminal)+'\n').encode())
    receipt.update(raw_sections=count,output=str(output),terminal=terminal)
    durable(output/'materialization.json',(json.dumps(receipt,indent=2)+'\n').encode())
    return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('source',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    print(json.dumps(materialize(a.source,a.output),indent=2))
