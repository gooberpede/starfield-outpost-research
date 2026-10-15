# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent stdlib decoder and frozen-evaluator plumbing check, no native calls.

Reads a fixture geometry.bin and frozen project-owned evaluator. Writes one JSON
receipt beside the input. Does not load binaries, game data, or borrowed pointers.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from resource_spatial import evaluate_region

HEADER = struct.Struct('<4I6Q6I4fI')
USE = struct.Struct('<2I11fIQ')
NAMES = ('magic version status reason token parent thread query source region '
         'case count bytes uses verdict terminal cx cy cz radius mxcsr').split()
REASONS = {0:'NONE',1:'CAPACITY',2:'READ_FAILED',3:'UNPROVEN_COHERENCE_OR_BUSY',
           4:'STOP',5:'MISSING_VERDICT',6:'ANCESTRY',7:'CHANGING_USE',
           8:'INTERRUPTED',9:'USE_CAPACITY',10:'MUTATION',11:'LIFECYCLE'}
EXPECTED = [False,True,False,True,True,True,False,True,True,True]
BRANCHES = ['zero_points','single_point_broadphase','broadphase_rejected',
            'quad_xy_containment','vertex_xy_radius_height','edge_3d_radius',
            'all_strips_rejected','quad_xy_containment','quad_xy_containment','quad_xy_containment']
PLANS = [[1],[1],[1],[1,2],[1,2,3,3],[1,2,3,3,3,3,4],
         [1,2,3,3,3,3,4],[1,2],[1,2,3,3,3,3,4,2],[1,2]]


def expected_points(case):
    if case == 0: return []
    if case in (1,2): return [[999,999,999,0]]
    if case == 7: return [[i,-i,2,1] for i in range(8192)]
    if case == 8: return [[-10,-10,0,1],[10,-10,0,1],[10,10,0,1]]
    return [[-5,0,20,2],[5,0,20,2]]


def expected_query(case):
    return {2:[12,0,0],3:[0,0,-900],4:[5,3,-100],5:[0,3,20],
            6:[0,8,20],8:[10,5,0]}.get(case,[0,0,0])


def expected_use(case,ordinal,kind):
    q=expected_query(case); translation=[1024,-2048,32]
    radius={3:0,4:2,5:1.1,8:0}.get(case,1)
    upper={3:-100,4:20,5:-10}.get(case,0)
    indexed=[q[i]-translation[i] for i in range(3)]
    return USE.pack(ordinal,kind,*indexed,*translation,*q,radius,upper,7,0x123456789abcdef0)


def decode(data):
    records=[]; offset=0; tokens=set()
    while offset < len(data):
        if offset+4 > len(data): raise ValueError('TRUNCATED_LENGTH')
        length=struct.unpack_from('<I',data,offset)[0]; offset+=4
        if length<HEADER.size+4 or offset+length>len(data): raise ValueError('TRUNCATED_GROUP')
        block=data[offset:offset+length]; offset+=length
        h=dict(zip(NAMES,HEADER.unpack_from(block)))
        if h['magic']!=0x31514f53 or h['version']!=1: raise ValueError('SCHEMA')
        if length!=HEADER.size+h['bytes']+h['uses']*USE.size+4: raise ValueError('LENGTH')
        if struct.unpack_from('<I',block,length-4)[0]!=0x454e4f44: raise ValueError('COMMIT_MARKER')
        if h['bytes']%16 or h['uses']>64 or h['bytes']>8192*16: raise ValueError('CAPACITY')
        if not h['token'] or h['token'] in tokens: raise ValueError('DUPLICATE_TOKEN')
        tokens.add(h['token'])
        if h['status'] not in (1,2,3) or h['reason'] not in REASONS: raise ValueError('STATUS')
        point_bytes=block[HEADER.size:HEADER.size+h['bytes']]
        points=list(struct.iter_unpack('<4f',point_bytes))
        uses=[USE.unpack_from(block,HEADER.size+h['bytes']+i*USE.size) for i in range(h['uses'])]
        if h['status']==1:
            if h['reason'] or h['bytes']!=h['count']*16 or not uses: raise ValueError('INCOMPLETE_VALID')
            if h['verdict'] not in (0,1) or h['terminal']!=(1 if h['verdict'] else 2): raise ValueError('VERDICT')
            if h['mxcsr'] & 0xffc0 != 0x1f80: raise ValueError('NUMERIC_ENVIRONMENT')
            if h['case']>=len(PLANS) or [u[1] for u in uses]!=PLANS[h['case']]:
                raise ValueError('MISSING_OR_WRONG_REQUIRED_USE_SITE')
            for i,u in enumerate(uses):
                if u[0]!=i or u[8:13]!=uses[0][8:13]: raise ValueError('UNQUALIFIED_USES')
                if USE.pack(*u)!=expected_use(h['case'],i,PLANS[h['case']][i]):
                    raise ValueError('USE_INPUT_BYTES_OR_PROVENANCE')
            if (h['query']!=h['token'] or h['source']!=h['case']+100 or h['region']!=h['case']+200
                    or [h['cx'],h['cy'],h['cz']]!=[0,0,0]
                    or h['radius']!=(30 if h['case']==8 else 10)):
                raise ValueError('HEADER_PROVENANCE')
        elif not h['reason'] or (h['status']==3 and h['verdict']!=2):
            raise ValueError('AMBIGUOUS_INVALID')
        records.append(dict(header=h,points=points,uses=uses,point_bytes=point_bytes,
                            sha256=hashlib.sha256(block).hexdigest()))
    for r in records:
        h=r['header']
        if h['parent'] and h['parent'] not in tokens: raise ValueError('MISSING_PARENT')
    return records


def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('path',type=Path)
    path=ap.parse_args().path; data=path.read_bytes(); records=decode(data)
    results=[]; reasons={}; threads=set(); complete=0
    for r in records:
        h=r['header']; threads.add(h['thread'])
        if h['status']!=1:
            reason=REASONS[h['reason']]; reasons[reason]=reasons.get(reason,0)+1
            continue
        complete+=1; case=h['case']
        expected=expected_points(case)
        assert r['point_bytes']==b''.join(struct.pack('<4f',*p) for p in expected)
        assert h['query']==h['token'] and h['source']==case+100 and h['region']==case+200
        use=r['uses'][0]; query=list(use[8:11]); radius,upper=use[11:13]
        assert query==expected_query(case)
        assert use[2:5]==tuple(query[i]-use[5+i] for i in range(3))
        assert use[13:]==(7,0x123456789abcdef0)
        out=evaluate_region(query,radius,upper,[h['cx'],h['cy'],h['cz']],h['radius'],r['points'])
        assert out['status']=='KNOWN' and out['accepted']==bool(h['verdict'])==EXPECTED[case],(case,out)
        assert out['branch']==BRANCHES[case],(case,out)
        results.append(dict(token=h['token'],case=case,verdict=bool(h['verdict']),
                            branch=out['branch'],geometry_sha256=hashlib.sha256(r['point_bytes']).hexdigest()))
    assert len(records)==64 and len(threads)>=5 and all(case in [x['case'] for x in results] for case in range(10))
    assert reasons=={'CAPACITY':1,'READ_FAILED':1,'UNPROVEN_COHERENCE_OR_BUSY':2,
                    'CHANGING_USE':1,'ANCESTRY':3,'STOP':2,'INTERRUPTED':1,
                    'USE_CAPACITY':1,'MISSING_VERDICT':2,'MUTATION':1,'LIFECYCLE':3},reasons
    assert any(r['header']['parent'] for r in records)
    negatives=[]
    def reject(label,changed):
        try: decode(changed)
        except ValueError as e: negatives.append(dict(test=label,diagnostic=str(e)))
        else: raise AssertionError(label)
    reject('truncated_tail',data[:-1]); reject('missing_terminal_group',data[:-10])
    bad=bytearray(data); struct.pack_into('<I',bad,4+12,0); bad[4+8:4+12]=struct.pack('<I',1)
    # First group is complete already; make its copied byte count inconsistent.
    struct.pack_into('<I',bad,4+72,16)
    reject('partial_geometry_as_valid',bad)
    length=struct.unpack_from('<I',data)[0]+4
    reject('duplicate_group_token',data+data[:length])
    # Remove a real required use from a multi-use complete group, retaining coherent framing.
    blocks=[]; at=0
    while at<len(data):
        n=struct.unpack_from('<I',data,at)[0]+4; blocks.append(bytearray(data[at:at+n])); at+=n
    target=next(b for b in blocks if HEADER.unpack_from(b,4)[13]>1 and HEADER.unpack_from(b,4)[2]==1)
    changed=bytearray(target); fields=list(HEADER.unpack_from(changed,4)); fields[13]-=1
    HEADER.pack_into(changed,4,*fields)
    del changed[-4-USE.size:-4]; struct.pack_into('<I',changed,0,len(changed)-4)
    reject('missing_consumed_use',bytes(changed))
    changed=bytearray(target); where=4+HEADER.size+HEADER.unpack_from(changed,4)[12]
    struct.pack_into('<I',changed,where,5)
    reject('reordered_use',bytes(changed))
    changed=bytearray(target)
    # Change the domain in the SECOND consumed use, leaving all arithmetic identical.
    changed[where+USE.size+USE.size-1]^=1
    reject('later_use_provenance_corruption',bytes(changed))
    # A robust direct terminal flip independent of field offset arithmetic.
    fields=list(HEADER.unpack_from(target,4)); fields[15]=2 if fields[14] else 1
    changed=bytearray(target); HEADER.pack_into(changed,4,*fields)
    reject('conflicting_terminal',bytes(changed))
    report=dict(status='PASS',schema='sor-offline-qualification/1',records=len(records),
                complete=complete,invalid=len(records)-complete,threads=len(threads),reasons=reasons,
                replay=results,decoder_negative_tests=negatives,
                input_sha256=hashlib.sha256(data).hexdigest(),
                evaluator_sha256=hashlib.sha256((ROOT/'save-analysis/scripts/resource_spatial.py').read_bytes()).hexdigest(),
                decoder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                meaning='Synthetic plumbing only; native equivalence NOT TESTED')
    (path.parent/'decode.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('replay',)}))


if __name__=='__main__': main()
