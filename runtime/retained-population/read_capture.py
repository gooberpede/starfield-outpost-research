# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent stdlib reader. Reads raw frames and flush receipts, never repairs.

Optional --out writes a new result file. Byte integrity and scoped scientific
classification are separate; an unacknowledged tail cannot establish a chain.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib

SIZE = 1416
HEADER = struct.Struct('<4I')
NAMES = ('sequence kind invocation parent thread epoch hazards status frame manager proc source wrapper collection index resource').split()


def decode(raw):
    e = dict(zip(NAMES,struct.unpack_from('<16Q',raw)))
    e['args'] = struct.unpack_from('<6Q',raw,128)
    e['count'] = struct.unpack_from('<I',raw,176)[0]
    e['owner'] = struct.unpack_from('<I',raw,180)[0]
    e['source_bytes'] = raw[184:296].hex()
    e['descriptor'] = raw[296:340].hex()
    e['bounds'] = raw[340:361].hex()
    e['native_count'] = struct.unpack_from('<I',raw,364)[0]
    e['points'] = raw[388:388+min(e['count'],64)*16].hex()
    return e


def geometry(e):
    return (e['bounds'],e['count'],e['points'])


def ownership(e):
    return tuple(e[n] for n in ('manager','proc','source','wrapper','collection','index','resource','epoch','owner'))+(e['args'][4],e['args'][5])


def reduce(events):
    invocations = {}
    constructions = []
    witnessed = []
    chains = []
    for e in events:
        if e['kind'] == 7:
            constructions.clear()
        if e['invocation']:
            invocations.setdefault(e['invocation'],[]).append(e)
        if e['kind']==2 and e['args'][2]==e['args'][3]:
            constructions=[p for p in constructions if (p['proc'],p['source'])!=(e['proc'],e['source'])]
        if e['kind'] == 6 and e['invocation']:
            parts=invocations[e['invocation']]
            visited=[p for p in parts if p['kind']==1 and p['args'][1]==0]
            misses=[p for p in parts if p['kind']==2 and p['args'][2]==p['args'][3]]
            queries=[p for p in parts if p['kind']==3]
            masks=[p for p in parts if p['kind']==4]
            copies=[p for p in parts if p['kind']==5 and p['status']==0 and any(
                t['kind']==11 and t['status']==0 and t['collection']==p['collection'] and t['args'][3]==p['args'][3] and geometry(t)==geometry(p)
                for t in parts)]
            consistent=all((p['status']==0 if p['kind'] not in (5,11) else not (p['status']&~48)) and p['hazards']==0 and p['epoch']==e['epoch'] and
                           p['source']==e['source'] and p['proc']==e['proc'] and p['manager']==e['manager'] and
                           p['owner']==e['owner'] and p['args'][4]==e['args'][4] and p['descriptor']==e['descriptor']
                           for p in parts)
            if (consistent and e['args'][2]==e['owner'] and visited and misses and queries and masks and
                e['count']>0 and any(p['collection']==e['collection'] and p['index']==e['index'] and geometry(p)==geometry(e) for p in copies)):
                constructions.append(e)
                witnessed.append(e)
        if e['kind']==2 and e['args'][2]!=e['args'][3] and not e['status'] and not e['hazards']:
            for completed in constructions:
                if (ownership(completed)==ownership(e) and geometry(completed)==geometry(e) and
                    completed['source_bytes']==e['source_bytes'] and completed['descriptor']==e['descriptor']):
                    chains.append(dict(construction=completed['invocation'],reuse=e['invocation'],epoch=e['epoch'],
                                       resource=e['resource'],point_count=e['count'],population_partial=any(
                                           p['kind'] in (5,11) and bool(p['status']&48) for p in invocations[completed['invocation']])) )
    completed=[e for e in events if e['kind']==6 and not e['status'] and not e['hazards'] and e['count']]
    joined={e['reuse'] for e in chains};constructed={e['invocation'] for e in witnessed};reused={e['construction'] for e in chains}
    return dict(complete_chains=chains,construction_witnesses=len(witnessed),
                construction_only=len(constructed-reused),retention_only=sum(e['invocation'] not in constructed for e in completed),
                hit_only=sum(e['kind']==2 and e['args'][2]!=e['args'][3] and e['invocation'] not in joined for e in events),
                contrary_geometry=sum(e['kind']==5 and bool(e['status']&32) for e in events),
                ordinary_masks=[e['args'][2] for e in events if e['kind']==4],
                bypass=sum(e['kind']==1 and bool(e['args'][1]) for e in events),
                hit_observations=sum(e['kind']==2 and e['args'][2]!=e['args'][3] for e in events),
                failed_observations=sum(bool(e['status']) for e in events))


def inspect(folder, expected_dll=None):
    folder=Path(folder)
    if expected_dll is None:
        raise ValueError('approved DLL hash is required')
    identity_bytes=(folder/'identity.json').read_bytes()
    identity=json.loads(identity_bytes)
    identity_hash=hashlib.sha256(identity_bytes).hexdigest()
    if identity.get('schema')!='sor-d5p/1' or identity.get('session_name')!=folder.name:
        raise ValueError('capture identity/session name')
    if expected_dll is not None and identity.get('dll_sha256')!=expected_dll:
        raise ValueError('unapproved DLL identity')
    raw=(folder/'events.bin').read_bytes()
    frames=[];at=0;errors=[]
    while at<len(raw):
        if len(raw)-at<16:
            errors.append('torn header');break
        magic,n,seq,crc=HEADER.unpack_from(raw,at)
        if magic!=0x31505253 or n!=SIZE or seq!=len(frames)+1:
            errors.append('frame identity/size/sequence');break
        if len(raw)-at-16<n:
            errors.append('torn payload');break
        payload=raw[at+16:at+16+n]
        if zlib.crc32(payload)!=crc:
            errors.append('CRC mismatch');break
        e=decode(payload)
        if e['sequence']!=seq or e['count']>64:
            errors.append('payload sequence/capacity');break
        frames.append(e);at+=16+n
    ack=0;verified_bytes=0;prefix_crc=0
    acknowledgments=(folder/'flush.jsonl').read_bytes()
    for line in acknowledgments.splitlines(keepends=True):
        if not line.endswith(b'\n'):
            errors.append('torn flush receipt');break
        try:
            r=json.loads(line)
            next_crc=zlib.crc32(raw[verified_bytes:r['bytes']],prefix_crc)
            if not (r['identity_sha256']==identity_hash and ack<r['records']<=len(frames) and r['bytes']==r['records']*(16+SIZE) and
                    next_crc==r['prefix_crc32']):
                raise ValueError('flush binding')
            ack=r['records'];verified_bytes=r['bytes'];prefix_crc=next_crc
        except (ValueError,KeyError,TypeError):
            errors.append('invalid flush receipt');break
    terminal=None
    if (folder/'terminal.json').exists():
        terminal=json.loads((folder/'terminal.json').read_text())
        if any(terminal.get(k)!=v for k,v in identity.items()):
            raise ValueError('terminal identity mismatch')
        if terminal['drops'] or terminal['failed'] or terminal['enqueued']!=ack or terminal['flushed']!=ack:
            errors.append('terminal loss/failure')
    result=reduce(frames[:ack])
    result.update(raw_records=len(frames),independently_verified_durable_records=ack,
                  unacknowledged_records=len(frames)-ack,errors=errors,
                  acquisition='INCOMPLETE' if errors or ack<len(frames) or not terminal else 'RETIRED',
                  capture_sha256=hashlib.sha256(raw).hexdigest(),identity=identity)
    # A verified prefix survives a torn later tail; it is never upgraded to
    # complete-session coverage or a qualified negative observation.
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder',type=Path);p.add_argument('--out',type=Path);p.add_argument('--dll-sha256',required=True)
    a=p.parse_args();result=inspect(a.folder,a.dll_sha256)
    text=json.dumps(result,indent=2)+'\n'
    if a.out:
        with a.out.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    print(text)


if __name__=='__main__':
    main()
