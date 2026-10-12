"""SPDX-License-Identifier: GPL-3.0-or-later
Offline matching-source audit. CPython stdlib plus existing project readers.
Reads sealed Q030 captures, prior pinned receipts and protected save copies.
Writes only a NEW ignored output directory; scratch decoder removes its own files.
No engine/process/database/network/config/Git mutation. Enforces C:/D: 40GB guard.
Run from repository root: python -B research/matching-source/verify.py OUTPUT
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
sys.path.insert(0, str(ROOT/'runtime/native-oracle-030'))
from verify_position_v2 import guard, digest
from inspect_events import decode, raw, SIZE
from planet_world_key import find_unit3_context, unit3_world_descriptors, qualified_grid
from stream_save import decoded_save
from validate_mature_outposts import directory
from outpost_planetary_location import global_suffix, extract
from outpost_planetary_location import body_catalog
from saved_world_components import find_world_components
from q_hierarchy_diagnostic import unpack, snap

ORDER = [(0,1),(4,4),(8,4),(16,1),(12,4),(20,4),(24,4),(32,1),(28,4),(36,4),(40,4)]


def pack(system, body, tag, x, y):
    if not (0 <= system < 2**18 and 0 <= body < 64 and 0 <= tag < 4
            and 0 <= x < 49152 and 0 <= y < 49152):
        raise ValueError('PACK_DOMAIN')
    return system << 41 | body << 35 | tag << 32 | y << 16 | x


def native_xy(key):
    q = qualified_grid(key)
    return [49151-q[k] if q['tag'] in (2,3) else q[k] for k in ('x','y')]


def main():
    out = Path(sys.argv[1]); space = guard(); out.mkdir(parents=True, exist_ok=False)
    protected = {}
    def read(path):
        p = ROOT/path if not Path(path).is_absolute() else Path(path)
        protected[str(p)] = digest(p)
        return json.loads(p.read_text(encoding='utf8'))
    previous = read('.local-work/q030-E-next-step/analysis.json')
    run = Path(read('.local-work/q030-revised-card-02/active-run-corrected.json')['run'])
    seal = read(run/'final-evidence-manifest.json')
    for p in seal['files']:
        assert digest(Path(p['path'])) == p['sha256']
        protected[p['path']] = p['sha256']
    lock = read('.local-work/q030-module-inventory-fix/release-lock-05.json')
    for p,h in lock['pins'].items():
        assert digest(Path(p)) == h
        protected[p] = h
    session = Path(read(run/'external-ready-observation.json')['session'])
    data = (session/'events.bin').read_bytes()
    assert hashlib.sha256(data).hexdigest() == previous['raw_sha256']
    journal = (session/'records.jsonl').read_bytes()
    assert hashlib.sha256(journal).hexdigest() == previous['journal_sha256']
    groups = {}
    for i,line in enumerate(journal.splitlines()):
        j = json.loads(line); block = data[i*SIZE:(i+1)*SIZE]
        assert j['offset'] == i*SIZE and j['length'] == SIZE
        assert hashlib.sha256(block).hexdigest() == j['sha256']
        e = decode(block)
        assert all(e[k] == j[k] for k in ('sequence','kind','invocation'))
        groups.setdefault(e['invocation'], []).append(e)
    assert len(data) == 144*SIZE and len(groups) == 18
    chains = []
    for n,es in groups.items():
        assert [e['kind'] for e in es] == [7,13,15,16,17,18,19,8]
        a,b = raw(es[4],'candidate',44),raw(es[4],'source',44)
        fields = [dict(offset=o,length=s,a=a[o:o+s].hex(),b=b[o:o+s].hex(),equal=a[o:o+s]==b[o:o+s]) for o,s in ORDER]
        old = next(r for r in previous['rows'] if r['invocation']==n)
        assert hex(next(f['offset'] for f in fields if not f['equal'])) == old['first_mismatch']
        descriptor = raw(es[0],'candidate',24)
        assert descriptor[:16].hex() == old['candidate_angles_hex']
        assert f'{struct.unpack_from("<I",descriptor,16)[0]:08X}' == old['candidate_key']
        geometry=lambda v:[v[0],*struct.unpack_from('<2i',v,4),*struct.unpack_from('<2i',v,20),*struct.unpack_from('<2i',v,36)]
        assert unpack(int(old['packed_B_key'],16))['geometry']==geometry(b)
        chains.append(dict(invocation=n,sequence=es[4]['sequence'],descriptor_hex=descriptor.hex(),
            candidate_key=old['candidate_key'],candidate_angles=list(struct.unpack('<2d',descriptor[:16])),
            A_hex=a.hex(),B_hex=b.hex(),fields=fields,source_key=old['packed_B_key'],
            flags=[raw(e,'extra',0x34)[32] for e in es[2:7]]))
    controls = []
    for tag in range(4):
        for x,y in ((0,0),(49151,49151),(10464,21120),(123,456)):
            key=pack(88327,15,tag,x,y); q=qualified_grid(key)
            assert [q['system_id'],q['body_index'],q['tag'],q['x'],q['y']]==[88327,15,tag,x,y]
            nx,ny=native_xy(key)
            rx,ry=(49151-nx,49151-ny) if tag in (2,3) else (nx,ny)
            assert pack(q['system_id'],q['body_index'],tag,rx,ry)==key
            controls.append(dict(key=f'{key:016x}',native_xy=[nx,ny]))
    assert pack(88327,15,1,10464,21120)==0x02b20e79528028e0
    assert native_xy(0x02b20e7a01c8007b)==[49028,48695]
    candidate_geometry=[1,54,110,8,0,0,0]
    assert unpack(0x02b20e79528028e0)['geometry']==candidate_geometry
    native_controls=[]
    for tag,x,y,expected in [
        (1,10463,21120,[1,54,110,7,0,11,0]),
        (1,10465,21120,[1,54,110,8,0,1,0]),
        (1,10464,21119,[1,54,109,8,15,0,11]),
        (1,10464,21121,[1,54,110,8,0,0,1]),
        (0,10464,21120,[0,54,110,8,0,0,0]),
        (2,38687,28031,[2,54,110,8,0,0,0]),
        (3,38687,28031,[3,54,110,8,0,0,0])]:
        key=pack(88327,15,tag,x,y)
        actual=unpack(key)['geometry'];assert actual==expected and actual!=candidate_geometry
        native_controls.append(dict(key=f'{key:016x}',geometry=actual,matching_candidate=False))
    for args,expected in [((1,54,110,3,0),[1,54,110,0,0,0,0]),
            ((1,54,110,4,0),candidate_geometry),((1,54,110,11,0),candidate_geometry),
            ((1,54,110,12,0),[1,55,110,0,0,0,0]),
            ((0,255,255,12,12),[1,0,255,0,0,0,0]),
            ((0,10,255,0,12),[1,245,255,0,0,0,0])]:
        actual=snap(*args);assert actual==expected
        native_controls.append(dict(snap_input=list(args),geometry=actual,
            basis='Instruction-derived synthetic control; not runtime execution'))
    # Check actual recovered instruction operands and edges, not a CFG invented
    # by the arithmetic model. Static addresses are preferred VAs, base140000000.
    cfg_checks=[]
    def instructions(path, expected):
        p=ROOT/path;protected[str(p)]=digest(p)
        ins={line.split('\t',1)[0]:line.split('\t',1)[1] for line in p.read_text(encoding='utf8').splitlines() if '\t' in line}
        for address,operand in expected.items():
            assert ins[address]==operand,(address,ins.get(address),operand)
            cfg_checks.append(dict(path=path,address=address,instruction=operand))
    instructions('.local-work/recon/static-exhaustion-46.tsv',{
        '140ad096f':'MOV RBX,qword ptr [RBX + 0x310]',
        '140ad0976':'CALL 0x14096efb0','140ad0986':'CALL 0x14096fb40',
        '140ad0a12':'TEST byte ptr [R15 + 0x20],0x1',
        '140ad0a17':'JZ 0x140ad0aba','140ad0ab5':'CALL 0x140b1e190'})
    instructions('.local-work/recon/static-exhaustion-46.tsv',{
        address:'JNZ 0x140ad0aba' for address in
        ('140ad0992','140ad099e','140ad09aa','140ad09b7','140ad09c3',
         '140ad09cf','140ad09db','140ad09e8','140ad09f4','140ad0a00','140ad0a0c')})
    instructions('.local-work/recon/durable-center-04.tsv',{
        '1407801b3':'CALL 0x14077f900','1407801be':'JNZ 0x14077fd96',
        '14077fec0':'CALL 0x14096f5c0','140780264':'CALL 0x14077e350',
        '14078026f':'JNZ 0x14077fd96'})
    instructions('.local-work/recon/activated-grid-01.tsv',{
        '14096efe5':'CMP R9D,0xc','14096f011':'CMP R9D,0x4',
        '14096f01e':'CMP R8D,0xc','14096f024':'TEST DL,DL',
        '14096f03f':'SUB EAX,dword ptr [RDI + 0x4]',
        '14096f066':'MOV qword ptr [RDI + 0x24],0x0'})
    for invalid in ((88327,15,4,0,0),(88327,15,1,49152,0),(-1,15,1,0,0)):
        try: pack(*invalid)
        except ValueError: pass
        else: raise AssertionError('INVALID_PACK_ACCEPTED')
    catalog=read('.local-work/save-capacity-location/esm-index-verified.json')['records']
    old_saves=read('.local-work/workshop-origin/final-03/before.json')
    saves=[dict(path=p,sha256=v['sha256']) for p,v in old_saves.items() if Path(p).name.startswith(('Save25_','Save26_'))]
    saves += read('.local-work/native-oracle-020/operations/continuation-live-postflight-supplement-01.json')['new_checkpoint_pins']
    saved=[]
    for pin in saves:
        p=Path(pin['path']); assert digest(p)==pin['sha256']; protected[str(p)]=pin['sha256']
        with decoded_save(p,out/'scratch') as (b,metrics):
            d=directory(b); units=global_suffix(b,d)
            context=find_unit3_context(b,d['regions']['region_R1'][0],units[4][0]-8)
            descriptors,_=unit3_world_descriptors(b,context)
            beacons=extract(b,catalog)['beacons']
            by_pair,_=body_catalog(catalog)
            body_keys={k:f'{v[0]["formid"]:08X}' for k,v in by_pair.items() if len(v)==1}
            component_run=find_world_components(b,*units[6],{int(r['parent_token'],16) for r in beacons},body_keys,descriptors)
            candidates=[]
            for n in (15,16):
                c=next(c for c in chains if c['invocation']==n)
                angles=bytes.fromhex(c['descriptor_hex'][:32]); positions=[]; a,z=units[6]
                while (a:=b.find(angles,a,z))>=0:
                    positions.append(a); a+=1
                points=[]
                for pos in positions:
                    # Scoped 30-byte site tuple: body ID, site ID, kind16, pair, repeated site ID.
                    body,site=struct.unpack_from('<II',b,pos-10)
                    repeated=struct.unpack_from('<I',b,pos+16)[0]
                    points.append(dict(pair_offset=pos,body_tagged=f'{body:08x}',site_tagged=f'{site:08x}',
                        kind=bytes(b[pos-2:pos]).hex(),repeated_equal=site==repeated,
                        world_components=[r for r in component_run['rows'] if int(r['world'],16)==site],
                        beacon_parent_matches=[dict(token=r['token'],parent=r['parent_token'],record_offset=r['record_start'])
                            for r in beacons if int(r['parent_token'],16)==site]))
                candidates.append(dict(invocation=n,points=points))
            saved.append(dict(path=str(p),sha256=pin['sha256'],metrics=metrics,context=context,
                descriptors=descriptors,candidates=candidates,beacons=beacons,
                component_run_bounds=[component_run['start'],component_run['end']]))
    assert all(digest(Path(p))==h for p,h in protected.items())
    receipt=dict(disk_before=space,disk_after=guard(),chains=chains,packing_controls=controls,
        native_geometry_controls=native_controls,cfg_checks=cfg_checks,
        saves=saved,protected=protected,seal_members=len(seal['files']),pins=len(lock['pins']),
        limits='Exact bytes / scoped saved joins; runtime remapping and future Q/E dispatch are unvalidated')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(chains=len(chains),comparisons=sum(len(c['fields']) for c in chains),saves=len(saved),
        controls=len(controls),protected=len(protected),receipt_sha256=digest(out/'receipt.json'))))


if __name__=='__main__':
    main()
