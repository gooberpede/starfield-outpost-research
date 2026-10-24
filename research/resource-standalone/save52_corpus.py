# SPDX-License-Identifier: GPL-3.0-or-later
"""D2 field-level projection, adapted from owned D1 builder at task HEAD.

Reads frozen label-free requests, pinned installed main definitions/PlanetData,
and D1 corpus constants. Writes one fresh local corpus/lineage receipt. Reuses
unchanged planetary selection and generation semantics. Unsupported biomes are
explicit status rows, never empty ordinary families. No save or answer reads.
"""
import copy
import argparse
import json
import math
from pathlib import Path
import re
import struct
import zlib

import save52 as s
import context
from predictor import validate, seal


def ordinary(records, prediction, biome, blocks):
    """Project the D1-supported component branch; preserve first failing stage."""
    v = next(v for v in prediction.biome_results if int(str(v.orchestration.biome.form_id),16)==biome)
    family = v.family_access.family if v.family_access else None
    if not family or v.orchestration.special_selection is not None:
        raise ValueError('NO_ORDINARY_FAMILY_OR_SELECTED_SPECIAL')
    rsgd = int(str(v.orchestration.effective_rsgd.form_id),16)
    raw_blocks = {}
    candidate = None
    for tag,raw in records[rsgd][1]:
        if tag==b'RNAM':
            candidate = int.from_bytes(raw,'little')
        elif tag==b'DNAM':
            raw_blocks[candidate] = raw
    for e in v.orchestration.effective_rsgd.entries:
        if e.resource_rarity.value=='Everywhere':
            fid = int(str(e.resource_form_id),16)
            if struct.unpack_from('<f',raw_blocks[fid],40*13+28)[0]!=0:
                raise ValueError('NONZERO_EVERYWHERE')
    root = int(str(family.root.form_id),16)
    raw = raw_blocks[root]
    chosen = [int(str(v),16) for v in family.emitted_form_ids]
    rarity = {f:int.from_bytes(s.builder.last(records[f][1],b'SNAM'),'little')&255 for f in chosen}
    if len(set(rarity.values()))!=len(chosen):
        raise ValueError('EQUAL_RARITY_ORDER')
    resources = []
    for fid in sorted(chosen,key=lambda f:-rarity[f]):
        block = list(struct.unpack_from('<8f',raw,40*(rarity[fid]+7)))
        key = s.hashlib.sha256(struct.pack('<8f',*block)).hexdigest()[:16]
        if key in blocks and blocks[key]!=block:
            raise ValueError('BLOCK_COLLISION')
        blocks[key] = block
        resources.append(dict(id=f'{fid:08x}',rarity=rarity[fid],block=key))
    return dict(status='ORDINARY_ONLY',resources=resources),dict(root=f'{root:08x}',rsgd=f'{rsgd:08x}',
        dnam_sha256=s.hashlib.sha256(raw).hexdigest(),selection_seed=prediction.planet.resource_creation_seed,
        selection_draws=prediction.final_draw_count)


def build():
    s.guard()
    out = s.OUT/'build-v1'
    out.mkdir(exist_ok=False)
    requests_path = s.OUT/'requests-v1.json'
    requests = json.loads(requests_path.read_text())
    baseline = s.ROOT/'.local-work/resource-standalone/build03/normalized.json'
    expected = '367a97b8669ff3978bd9bf0dab91873ad1067980c35a56dabdb6d1fe0c928ed2'
    if s.builder.pin(baseline)!=expected:
        raise ValueError('BASELINE_CORPUS_PIN')
    inputs = {str(p):s.builder.pin(p) for p in (requests_path,baseline,s.builder.ESM,s.builder.EXE,s.builder.ARCHIVE,
        Path(__file__),s.ROOT/'research/resource-standalone/builder.py',*s.builder.OWNED.glob('*.py'))}
    if inputs[str(s.builder.ARCHIVE)]!=s.builder.ARCHIVE_HASH or inputs[str(s.builder.ESM)]!=s.builder.DEFINITION or inputs[str(s.builder.EXE)]!=s.builder.EXE_HASH:
        raise ValueError('INSTALLED_PIN')
    if any(s.builder.pin(s.builder.OWNED/n)!=h for n,h in s.builder.OWNED_PINS.items()):
        raise ValueError('SELECTION_CODE_PIN')
    records = {h['formid']:(h,fs) for h,fs in s.esm_records(s.builder.ESM,
        {b'PNDT',b'SFTR',b'SFPT',b'SFBK',b'BIOM',b'RSGD',b'IRES'},repeated=True)}
    payload = copy.deepcopy(json.loads(baseline.read_text())['payload'])
    ids = {q['request']['body'] for q in requests if q['request']}
    def normalized(value):
        return re.sub('[^a-z0-9]','',value.lower())
    edids = {bid:normalized(s.builder.last(records[int(bid,16)][1],b'EDID').rstrip(b'\0').decode().removesuffix('PlanetData')) for bid in ids}
    maps = {}
    with s.builder.ARCHIVE.open('rb') as f:
        magic,version,kind,count,offset = struct.unpack('<4sI4sIQ',f.read(24))
        if (magic,version,kind)!=(b'BTDX',2,b'GNRL') or count>10000:
            raise ValueError('ARCHIVE_FRAMING')
        f.seek(32)
        entries = [struct.unpack('<I4sIIQIII',f.read(36)) for _ in range(count)]
        f.seek(offset)
        names = [f.read(int.from_bytes(f.read(2),'little')).decode() for _ in range(count)]
        member_pins = {}
        for bid,key in edids.items():
            matches = [(i,n) for i,n in enumerate(names) if n.startswith('planetdata/biomemaps/')
                       and n.endswith('.biom') and normalized(Path(n).stem)==key]
            if len(matches)!=1:
                raise ValueError('MAP_NAME_NOT_UNIQUE: '+bid)
            i,name = matches[0]
            off,packed,unpacked = entries[i][4:7]
            if off+(packed or unpacked)>s.builder.ARCHIVE.stat().st_size or unpacked>2_000_000:
                raise ValueError('MAP_BOUNDS')
            f.seek(off)
            raw = f.read(packed or unpacked)
            if packed:
                decoder = zlib.decompressobj()
                raw = decoder.decompress(raw,unpacked+1)
                if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
                    raise ValueError('MAP_COMPRESSION_CLOSURE')
            if len(raw)!=unpacked:
                raise ValueError('MAP_SIZE')
            maps[bid] = context.read_map(raw)
            member_pins[bid] = dict(name=name,bytes=len(raw),sha256=s.hashlib.sha256(raw).hexdigest())
    lineage = []
    for bid in sorted(ids):
        fs = records[int(bid,16)][1]
        system,parent,index = struct.unpack('<III',next(v for t,v in fs if t==b'GNAM' and len(v)==12))
        tree = s.builder.planet_tree(fs)
        tables = s.builder.decode_tree(records[tree][1])
        prediction = s.builder.selections(records,int(bid,16))
        body = payload['bodies'].setdefault(bid,dict(system=system,index=index,tiles={},biomes={}))
        tiles = set()
        # Include request halo plus one coarse tile for source/mask margins.
        for item in requests:
            q = item['request']
            if not q or q['body']!=bid:
                continue
            halo = q['radius']+400+2*payload['maximum_width']
            lo = [math.floor(q['descriptor'][k]+(q['query'][k]-halo)/100)//192-1 for k in (0,1)]
            hi = [math.floor(q['descriptor'][k]+(q['query'][k]+halo)/100)//192+1 for k in (0,1)]
            tiles.update((q['chart'],x,y) for x in range(max(0,lo[0]),min(255,hi[0])+1)
                         for y in range(max(0,lo[1]),min(255,hi[1])+1))
        for chart,x,y in sorted(tiles):
            pid,flags = tables[chart][x*256+y]
            biome = context.map_lookup(maps[bid],chart,x*192,y*192)
            mask = context.mask_lookup(maps[bid],chart,x*192,y*192)&15
            if pid not in records or records[pid][0]['type']!='SFPT':
                lineage.append(dict(body=bid,tile=[chart,x,y],status='MISSING_TYPED_SFPT',sfpt=f'{pid:08x}'))
                continue
            entries = list(zip(struct.unpack('<256I',s.builder.last(records[pid][1],b'FNAM')),
                               s.builder.last(records[pid][1],b'GNAM')))
            payload['patterns'][f'{pid:08x}'] = [[f'{f:08x}',g] for f,g in entries]
            for f,g in entries:
                if f and f in records and records[f][0]['type']=='SFBK':
                    payload['source_blocks'][f'{f:08x}'] = list(struct.unpack('<II',s.builder.last(records[f][1],b'DNAM')))
            if any(f and f'{f:08x}' not in payload['source_blocks'] for f,g in entries):
                raise ValueError('UNSUPPORTED_TYPED_PATTERN_DEPENDENCY')
            detail = {}
            try:
                component,detail = ordinary(records,prediction,biome,payload['generation_blocks'])
            except (ValueError,StopIteration,KeyError) as error:
                component = dict(status=str(error) or 'MISSING_BIOME_SELECTION',resources=[])
            body['biomes'][f'{biome:08x}'] = component
            body['tiles'][f'{chart}:{x}:{y}'] = [f'{pid:08x}',flags,f'{biome:08x}',mask]
            lineage.append(dict(body=bid,tile=[chart,x,y],sftr=f'{tree:08x}',sfpt=f'{pid:08x}',
                flags=flags,biome=f'{biome:08x}',mask=mask,status=component['status'],**detail))
    validate(seal(payload))
    s.write(out/'normalized.json',seal(payload))
    code = out/'code'
    code.mkdir()
    for p in (s.ROOT/'.local-work/resource-standalone/build03/code').glob('*.py'):
        (code/p.name).write_bytes(p.read_bytes())
    if any(s.builder.pin(p)!=h for p,h in inputs.items()):
        raise ValueError('INPUT_CHANGED')
    s.write(out/'manifest.json',dict(time=s.now(),schema='sor-d2-build/1',inputs=inputs,members=member_pins,
        lineage=lineage,bytes=(out/'normalized.json').stat().st_size,baseline_bytes=baseline.stat().st_size,
        corpus_sha256=s.builder.pin(out/'normalized.json'),code={p.name:s.builder.pin(p) for p in code.glob('*.py')},
        method='D1 constants and field schema; fresh whole-planet selection then halo tile projections; unchanged inference bundle'))
    print(json.dumps(dict(bytes=(out/'normalized.json').stat().st_size,bodies=len(ids),tiles=len(lineage),
                         unsupported=sum(r['status']!='ORDINARY_ONLY' for r in lineage))))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=s.OUT)
    s.select_root(ap.parse_args().root)
    build()
