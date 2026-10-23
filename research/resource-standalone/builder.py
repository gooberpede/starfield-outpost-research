# SPDX-License-Identifier: GPL-3.0-or-later
"""D1 offline corpus builder, run from repository root with installed CPython.

Reads hash-pinned installed main ESM/EXE/PlanetData archive and
maintainer-owned planetary selection modules. Writes exclusive ignored output
directory, two corpus variants and a flat code copy. No native geometry inputs,
historical predictions, target execution, downloads or source mutations.
Selected biome components are recomputed before minimizing the dependency set.
"""
import argparse
import copy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import time
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'research/resource-geometry'),str(ROOT/'save-analysis/scripts'),
               str(ROOT/'research/resource-pattern-selection'),str(Path(__file__).parent)]
from inspect_outpost_definitions import esm_records
from installed import decode_tree, planet_tree, ESM
import context
from predictor import SCHEMA, DEFINITION, canonical, seal, validate, resolve

EXE = ESM.parent.parent/'Starfield.exe'
EXE_HASH = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ARCHIVE = ESM.parent/'Starfield - PlanetData.ba2'
ARCHIVE_HASH = '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5'
OWNED = Path('D:/Projects/starfield-resource-reproducer/src/starfield_resource_reproducer')
OWNED_PINS = {
    '__init__.py':'27e8febb48ada44153ea2add9969a2c50a9831a74d9755fdd53c549a888b1cc2',
    'candidates.py':'1dd6a94264441a1ad7f6cf297f6c9f81693bb14bf07da03b3d0f0a080b88e16a',
    'diagnostics.py':'e01c5e4d7bf4f69ec13edcf2a93711478be3910f524d05707571dfc94776d4d0',
    'domain.py':'e100a1ad51fb7e1107a05811567b89a82188848679c55c6b0dbb669adc8826bc',
    'generation.py':'fc104fb92f24b7db48d246b9720b40c38a8e6209309d1f5d31a216dc7ca0c96b',
    'prng.py':'a806ac1b114ac107acba0bf4c5a6552859a6f2e4d393ef8edd107bc7eaaacfee',
}
MAPS = {'0005e0de': ('feynman v', [(0,130,168),(0,130,169)]),
        '0005e4da': ('carinae iii-a', [(0,111,81)])}
MAP_HASHES = {'0005e0de':'bd06d24e8ca1788481f6a4388c0e262b863b8b376a521752cf3d286c69f23863',
              '0005e4da':'bd9a3370b1c1b827cecdbdce318ee1f8af0608c4aade8e4e443968c2a720550f'}
CONSTANTS = (0x144f0416c,0x144f049f4,0x144f04654,0x144f048dc,0x144f052b0,
             0x144f052f8,0x144f03d80,0x144f03d40,0x144f03e00,0x144f03ed4,
             0x144f04178,0x144f03dc4,0x144f03d58,0x144f03e48,0x144f03fd4,0x144f03f50)
GMSTS = (0x2d40c0,0x226b0c,0x226b0e,0x226b0d,0x2f031c,0x2d40ce)


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def write(path, value):
    with Path(path).open('xb') as stream:
        stream.write(canonical(value)+b'\n')


def last(fields, tag):
    return next(value for key,value in reversed(fields) if key == tag)


def installed_maps():
    """Owned B1 BA2 framing, with bounded exact two-member decompression."""
    names={f'planetdata/biomemaps/{name}.biom':body for body,(name,tiles) in MAPS.items()}
    result={}
    with ARCHIVE.open('rb') as stream:
        magic,version,kind,count,names_offset=struct.unpack('<4sI4sIQ',stream.read(24))
        if (magic,version,kind)!=(b'BTDX',2,b'GNRL') or count>10000:
            raise ValueError('unsupported PlanetData archive')
        stream.seek(32)
        entries=[struct.unpack('<I4sIIQIII',stream.read(36)) for _ in range(count)]
        stream.seek(names_offset)
        filenames=[stream.read(int.from_bytes(stream.read(2),'little')).decode() for _ in range(count)]
        for i,name in enumerate(filenames):
            if name not in names: continue
            body=names[name];off,packed,unpacked=entries[i][4:7]
            if unpacked!=655414 or off+(packed or unpacked)>ARCHIVE.stat().st_size:
                raise ValueError('map bounds')
            stream.seek(off);blob=stream.read(packed or unpacked)
            if packed:
                decoder=zlib.decompressobj();blob=decoder.decompress(blob,unpacked+1)
                if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail: raise ValueError('map compressed closure')
            if len(blob)!=unpacked or hashlib.sha256(blob).hexdigest()!=MAP_HASHES[body]:raise ValueError('map identity')
            if body in result:raise ValueError('duplicate member')
            result[body]=blob
    if set(result)!=set(MAPS):raise ValueError('missing map member')
    return result


def selections(records, body):
    """Adapt owned RG1 planetary adapter; no catalogue or geometry lookup."""
    sys.path.insert(0,str(OWNED.parent))
    from starfield_resource_reproducer.domain import (FormId,GenerationRarity,RSGDSource,
        ResourceRef,RSGDResourceEntry,RSGDDefinition,Biome,Planet,IRESNode)
    from starfield_resource_reproducer.generation import generate_planet
    def num(fid,tag): return int.from_bytes(last(records[fid][1],tag),'little')
    def ed(fid): return last(records[fid][1],b'EDID').rstrip(b'\0').decode()
    rarities = list(GenerationRarity)
    def ref(fid): return ResourceRef(FormId(f'{fid:08x}'),ed(fid),ed(fid),rarities[num(fid,b'SNAM')&255],'Starfield.esm')
    nodes = {FormId(f'{fid:08x}'):IRESNode(ref(fid).form_id,ed(fid),ed(fid),ref(fid).rarity,
        tuple(ref(int.from_bytes(b,'little')) for t,b in fs if t==b'CNAM'),'Starfield.esm')
        for fid,(h,fs) in records.items() if h['type']=='IRES' and num(fid,b'SNAM')<7}
    def rsgd(fid,source):
        entries=[]; resource=None
        for tag,b in records[fid][1]:
            if tag==b'RNAM': resource=int.from_bytes(b,'little')
            if tag!=b'DNAM': continue
            rr=ref(resource)
            chances=[Decimal(str(struct.unpack_from('<f',b,i*40+28)[0])) for i in range(7)]
            entries.append(RSGDResourceEntry(len(entries),rr.form_id,rr.editor_id,rr.name,rr.rarity,'Starfield.esm',*chances))
        return RSGDDefinition(source,FormId(f'{fid:08x}'),ed(fid),'Starfield.esm',tuple(entries))
    biomes=[]
    for tag,b in records[body][1]:
        if tag!=b'PPBD': continue
        biom,chance,unknown,override=struct.unpack_from('<IfII',b)
        refs=[int.from_bytes(v,'little') for t,v in records[biom][1] if t==b'RNAM']
        if len(refs)>1: raise ValueError('ambiguous BIOM RSGD')
        biomes.append(Biome(len(biomes),FormId(f'{biom:08x}'),ed(biom),ed(biom),'Starfield.esm',
            Decimal(str(chance)),str(unknown),unknown,rsgd(override,RSGDSource.PNDT) if override else None,
            rsgd(refs[0],RSGDSource.BIOM) if refs else None))
    planet=Planet(FormId(f'{body:08x}'),ed(body),ed(body),'Starfield.esm',num(body,b'RSCS'),tuple(biomes))
    predicted=generate_planet(planet,nodes,atmospheric_records=[])
    return predicted


def build(destination):
    start=time.perf_counter()
    destination=destination.resolve()
    if not destination.is_relative_to(ROOT/'.local-work') or destination.exists():
        raise ValueError('fresh ignored output directory required')
    if min(shutil.disk_usage(d).free for d in ('C:/','D:/')) < 40_000_000_000:
        raise ValueError('disk guard')
    sources=[ESM,EXE,ARCHIVE,*OWNED.glob('*.py'),Path(__file__),
             ROOT/'research/resource-pattern-selection/installed.py',ROOT/'save-analysis/scripts/inspect_outpost_definitions.py',
             *[ROOT/p for p in ('research/resource-geometry/geometry.py','research/resource-geometry/context.py',
                'save-analysis/scripts/resource_availability.py','save-analysis/scripts/resource_spatial.py',
                'research/resource-standalone/predictor.py')]]
    pins={str(p):pin(p) for p in sources}
    if pins[str(ESM)]!=DEFINITION or pins[str(EXE)]!=EXE_HASH:
        raise ValueError('definition/executable pin')
    if pins[str(ARCHIVE)]!=ARCHIVE_HASH:raise ValueError('archive pin')
    maps=installed_maps()
    # Owned module pins are a version gate, not a geometry oracle or cache read.
    if any(pin(OWNED/name)!=sha for name,sha in OWNED_PINS.items()):
        raise ValueError('owned selection module changed')
    records={h['formid']:(h,fs) for h,fs in esm_records(ESM,
        {b'PNDT',b'SFTR',b'SFPT',b'SFBK',b'BIOM',b'RSGD',b'IRES',b'GMST'},repeated=True)}
    payload=dict(schema=SCHEMA,definition=DEFINITION,game_version='1.16.244.0',representation='normalized',
        constants={},settings=[],maximum_width=0,generation_blocks={},patterns={},source_blocks={},bodies={})
    blob=EXE.read_bytes(); pe=struct.unpack_from('<I',blob,0x3c)[0]
    n=struct.unpack_from('<H',blob,pe+6)[0]; opt=struct.unpack_from('<H',blob,pe+20)[0]
    sections=[struct.unpack_from('<IIII',blob,pe+24+opt+i*40+8) for i in range(n)]
    for va in CONSTANTS:
        rva=va-0x140000000; s=next(s for s in sections if s[1]<=rva<s[1]+s[2])
        payload['constants'][hex(va)]=struct.unpack_from('<f',blob,s[3]+rva-s[1])[0]
    for fid in GMSTS:
        payload['settings'].append(struct.unpack('<f',last(records[fid][1],b'DATA'))[0])
    payload['maximum_width']=max(max(struct.unpack_from('<2f',b,40*(i+7)+8))
        for h,fs in records.values() if h['type']=='RSGD' for t,b in fs if t==b'DNAM' for i in range(7))
    lineage=[]
    for body,(name,tiles) in MAPS.items():
        fid=int(body,16); fs=records[fid][1]
        system,parent,index=struct.unpack('<III',next(v for t,v in fs if t==b'GNAM' and len(v)==12))
        tree=planet_tree(fs); table=decode_tree(records[tree][1])
        m=context.read_map(maps[body])
        prediction=selections(records,fid)
        out=dict(system=system,index=index,tiles={},biomes={})
        for chart,x,y in tiles:
            pid,flags=table[chart][x*256+y]
            biome=context.map_lookup(m,chart,x*192,y*192)
            mask=context.mask_lookup(m,chart,x*192,y*192)&15
            out['tiles'][f'{chart}:{x}:{y}']=[f'{pid:08x}',flags,f'{biome:08x}',mask]
            pfs=records[pid][1]
            entries=list(zip(struct.unpack('<256I',last(pfs,b'FNAM')),last(pfs,b'GNAM')))
            payload['patterns'][f'{pid:08x}']=[[f'{f:08x}',g] for f,g in entries]
            for f,g in entries:
                if f in records and records[f][0]['type']=='SFBK':
                    payload['source_blocks'][f'{f:08x}']=list(struct.unpack('<II',last(records[f][1],b'DNAM')))
            view=next(v for v in prediction.biome_results if int(str(v.orchestration.biome.form_id),16)==biome)
            family=view.family_access.family if view.family_access else None
            rsgd=int(str(view.orchestration.effective_rsgd.form_id),16)
            everywhere=[e for e in view.orchestration.effective_rsgd.entries if e.resource_rarity.value=='Everywhere']
            if not family or view.orchestration.special_selection is not None:
                raise ValueError('supported tile requires ordinary family without Special')
            omitted_everywhere=[]
            for entry in everywhere:
                efid=int(str(entry.resource_form_id),16); candidate=None; extra=None
                for tag,b in records[rsgd][1]:
                    if tag==b'RNAM': candidate=int.from_bytes(b,'little')
                    if tag==b'DNAM' and candidate==efid: extra=b;break
                if extra is None or struct.unpack_from('<f',extra,40*(6+7)+28)[0]!=0:
                    raise ValueError('nonzero or unresolved Everywhere geometry')
                omitted_everywhere.append(f'0x{efid:08x}')
            root=int(str(family.root.form_id),16); raw=None; candidate=None
            for tag,b in records[rsgd][1]:
                if tag==b'RNAM': candidate=int.from_bytes(b,'little')
                if tag==b'DNAM' and candidate==root: raw=b;break
            if raw is None: raise ValueError('missing root descriptor')
            chosen=[int(str(v),16) for v in family.emitted_form_ids]
            rarity={f:int.from_bytes(last(records[f][1],b'SNAM'),'little')&255 for f in chosen}
            if len(set(rarity.values()))!=len(chosen): raise ValueError('unqualified equal-rarity order')
            resources=[]
            for f in sorted(chosen,key=lambda f:-rarity[f]):
                block=list(struct.unpack_from('<8f',raw,40*(rarity[f]+7)))
                key=hashlib.sha256(struct.pack('<8f',*block)).hexdigest()[:16]
                if key in payload['generation_blocks'] and payload['generation_blocks'][key]!=block:
                    raise ValueError('block hash collision')
                payload['generation_blocks'][key]=block
                resources.append(dict(id=f'{f:08x}',rarity=rarity[f],block=key))
            out['biomes'][f'{biome:08x}']=dict(status='ORDINARY_ONLY',resources=resources)
            lineage.append(dict(body=body,tile=[chart,x,y],pndt=f'0x{fid:08x}',sftr=f'0x{tree:08x}',
                sfpt=f'0x{pid:08x}',biome=f'0x{biome:08x}',root=f'0x{root:08x}',rsgd=f'0x{rsgd:08x}',
                rsgd_dnam_sha256=hashlib.sha256(raw).hexdigest(),resource_order=[r['id'] for r in resources],
                selection_seed=prediction.planet.resource_creation_seed,selection_draws=prediction.final_draw_count,
                omitted_zero_chance_everywhere=omitted_everywhere))
        payload['bodies'][body]=out
    validate(seal(payload))
    expanded=copy.deepcopy(payload); expanded['representation']='expanded'
    for bid,body in expanded['bodies'].items():
        body['routes']={}
        for tile in body['tiles']:
            chart,cx,cy=map(int,tile.split(':')); rows=[]
            for sx in range(16):
                for sy in range(16):
                    try:
                        ax,ay,fid,dx,dy,biome=resolve(payload,payload['bodies'][bid],chart,cx*192+sx*12,cy*192+sy*12)
                        rows.append([ax,ay,fid,dx,dy])
                    except (ValueError,KeyError): rows.append(None)
            body['routes'][tile]=rows
    del expanded['patterns']; del expanded['source_blocks']
    validate(seal(expanded))
    if any(pin(p)!=h for p,h in pins.items()): raise ValueError('protected builder input changed')
    destination.mkdir(parents=True)
    code=destination/'code';code.mkdir()
    for relative in ('research/resource-geometry/geometry.py','research/resource-geometry/context.py',
                     'save-analysis/scripts/resource_availability.py','save-analysis/scripts/resource_spatial.py',
                     'research/resource-standalone/predictor.py'):
        text=(ROOT/relative).read_text(encoding='utf8')
        # Flat bundle imports only its sibling authored modules and stdlib.
        text='\n'.join(line for line in text.splitlines() if not line.startswith('sys.path.insert('))+'\n'
        (code/Path(relative).name).write_bytes(text.encode('utf8'))
    measures=[]
    for label,data in (('normalized',payload),('expanded',expanded)):
        env=seal(data);write(destination/f'{label}.json',env)
        raw=(destination/f'{label}.json').read_bytes()
        measures.append(dict(representation=label,bytes=len(raw),zlib9_bytes=len(zlib.compress(raw,9)),
            sha256=hashlib.sha256(raw).hexdigest(),payload_sha256=env['sha256']))
    receipt=dict(schema='sor-d1-build/1',publication='LOCAL-ONLY',inputs=pins,lineage=lineage,
        build_seconds=time.perf_counter()-start,variants=measures,
        code={p.name:pin(p) for p in code.glob('*.py')},
        record_counts={k:len(payload[k]) for k in ('bodies','patterns','source_blocks','generation_blocks','constants')},
        fields_retained='Numeric geometry dependencies only; eight used floats per generation block',
        map_members={f'planetdata/biomemaps/{MAPS[b][0]}.biom':MAP_HASHES[b] for b in MAPS},
        assumptions='Pinned main ESM/PlanetData; no plugin/archive override merge; empty atmospheric occupancy model; historical effective epoch UNKNOWN')
    write(destination/'manifest.json',receipt)
    print(json.dumps(dict(destination=str(destination),variants=measures,seconds=receipt['build_seconds'])))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    build(p.parse_args().output)
