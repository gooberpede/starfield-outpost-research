# SPDX-License-Identifier: GPL-3.0-or-later
"""RG1 original bounded base-surface context reconstruction.

Lineage: owned B1 version-5 BIOM parser and activated-grid matrices; new primary
static source/selector trace is documented in resource-geometry/native.md.
Pure stdlib; accepts owned installed-input derivatives, never modifies a target.
Only 256-square ordinary maps and interior chart 0/1 are qualified here.
"""
import hashlib
import struct
import math
from geometry import Draws, f32, add, mul

MATRICES = ((1,0,0,1),(0,-1,1,0),(-1,0,0,-1),(0,1,-1,0),
            (1,0,0,-1),(0,1,1,0),(-1,0,0,1),(0,-1,-1,0))


def crc_bytes(data):
    crc=0
    for b in data:
        crc ^= b
        for _ in range(8): crc=(crc>>1) ^ (0xedb88320 if crc&1 else 0)
    return crc


def read_map(blob):
    """Owned B1 grammar; all payload stays caller-owned/local."""
    version,flags,n=struct.unpack_from('<BBI',blob)
    if version!=5: raise ValueError('unsupported BIOM version')
    catalog=list(struct.unpack_from('<'+str(n)+'I',blob,6));p=6+4*n
    faces_count,=struct.unpack_from('<I',blob,p);p+=4
    if faces_count!=2: raise ValueError('two hemisphere faces required')
    faces=[]
    for _ in range(2):
        width,height,count=struct.unpack_from('<III',blob,p);p+=12
        if width!=256 or height!=256 or count!=width*height:
            raise ValueError('qualified ordinary 256-square map required')
        values=list(struct.unpack_from('<'+str(count)+'I',blob,p));p+=4*count
        masks,=struct.unpack_from('<I',blob,p);p+=4
        if masks!=count: raise ValueError('mask extent mismatch')
        mask=list(blob[p:p+count]);p+=count
        faces.append(dict(values=values,mask=mask))
    if p!=len(blob): raise ValueError('BIOM closure')
    return dict(version=version,flags=flags,catalog=catalog,faces=faces)


def select_patterns(m, biome_styles, registered_patterns, system, body_index,
                    *, surface_seed=0x20201215, rotate=False):
    """Ordinary 0096e060 path with direct 256-square BIOM input.
    Registry order is input order; no resource/biome sort substitutes for it.
    Returns native coarse (column, inverted-row) tables and draw receipt.
    """
    choices={}
    for pattern in registered_patterns:
        choices.setdefault(pattern['style'],[]).append(pattern['id'])
    seed=crc_bytes(struct.pack('<III',body_index,system,surface_seed))
    rng=Draws(seed);tables=[]
    for face in m['faces']:
        table=[(0,0)]*65536
        for i,biome in enumerate(face['values']):
            candidates=choices.get(biome_styles.get(biome),[]) if biome_styles.get(biome) else []
            if not candidates: continue
            index=int(mul(f32(len(candidates)),rng.uniform())) if len(candidates)>1 else 0
            fid=candidates[index];flags=8
            if rotate:
                flags |= int(mul(rng.uniform(),4.0))*32
                # 0030b640 with bound ffffffff excludes raw ffffffff.
                while True:
                    word=rng.rng.getrandbits(32);rng.words.append(word)
                    if word!=0xffffffff: break
                if word<0x7fffffff: flags|=128
            col=i%256;row=i//256
            table[col*256+(255-row)]=(fid,flags)
        tables.append(table)
    digest=hashlib.sha256(b''.join(struct.pack('<I',w) for w in rng.words)).hexdigest()
    return dict(seed=seed,tables=tables,draw_count=len(rng.words),words_sha256=digest)


def rotate_cell(x,y,orientation,n=16):
    a,b,c,d=MATRICES[orientation];center=(n-1)/2
    return int(center+a*(x-center)+b*(y-center)),int(center+c*(x-center)+d*(y-center))


def remap_pattern(pattern, blocks, orientation, *, merge=2, step=12):
    """0096bba0's whole-footprint relocation; preserve underlying slot words."""
    raw=pattern['entries']
    if orientation==0: return raw
    inverse=(4-orientation)%4 if orientation<4 else orientation
    out=[(0,0)]*256
    for y in range(16):
        for x in range(16):
            fid,flags=raw[x*16+y]
            if not flags&8: continue
            width,height=blocks[fid]['dimensions']
            sx,sy=(width-merge)//step,(height-merge)//step
            p=rotate_cell(x,y,inverse);q=rotate_cell(x+sx-1,y+sy-1,inverse)
            xx,yy=min(p[0],q[0]),min(p[1],q[1])
            for i in range(sx):
                for j in range(sy):
                    if not (0<=xx+i<16 and 0<=yy+j<16 and x+i<16 and y+j<16):
                        raise ValueError('unsupported pattern footprint overflow')
                    out[(xx+i)*16+yy+j]=raw[(x+i)*16+y+j]
    return out


def source_at(tag,i,j,world_origin,selected,patterns,blocks,*,padding,merge=2,step=12):
    """Resolve one interior base-grid source via coarse pattern and anchor slot.
    Source origin is returned in both geographic fine cells and generator units;
    the latter is explicitly not fed through a /100 correction for seed hashing.
    """
    if tag not in (0,1) or not (0<=i<49152 and 0<=j<49152):
        raise ValueError('qualified interior chart required')
    cx,cy=i//192,j//192;sx,sy=(i%192)//step,(j%192)//step
    pid,pflags=selected['tables'][tag][cx*256+cy]
    if pid not in patterns: raise ValueError('missing selected surface pattern')
    grid=remap_pattern(patterns[pid],blocks,pflags>>5,merge=merge,step=step)
    fid,flags=grid[sx*16+sy]
    if not flags&8:
        sx-=(flags>>4)&3;sy-=(flags>>6)&3
        if not (0<=sx<16 and 0<=sy<16): raise ValueError('invalid source anchor')
        fid,flags=grid[sx*16+sy]
    if not flags&8 or fid not in blocks: raise ValueError('unqualified source anchor')
    ax,ay=cx*192+sx*step,cy*192+sy*step
    dimensions=[v-2*padding for v in blocks[fid]['dimensions']]
    if min(dimensions)<=0: raise ValueError('nonpositive source dimensions')
    local=[ax-world_origin[0],ay-world_origin[1]]
    native=[100*(v-padding) for v in local]
    origin_cell=[ax,ay]
    radius_half=[(v//2)*100+merge*100 for v in dimensions]
    center=[native[k]+(dimensions[k]//2)*100 for k in (0,1)]
    start=merge>>1
    return dict(id=f'{tag}:{ax}:{ay}:{fid:08x}',block=fid,pattern=pid,
                coarse_pattern_flags=pflags,source_flags=flags,dimensions=dimensions,
                geographic_origin=origin_cell,local_cell_origin=local,padding=padding,
                origin=native,clip_center=center+[0],clip_half=radius_half+[0],
                cell_bounds=[start,dimensions[0]+2*merge-start,start,dimensions[1]+2*merge-start],
                resource_biome=map_lookup(selected.get('map'),tag,ax,ay) if selected.get('map') else None)


def map_lookup(m,tag,i,j):
    if tag not in (0,1) or not (0<=i<49152 and 0<=j<49152):
        raise ValueError('qualified map domain required')
    return m['faces'][tag]['values'][(255-j//192)*256+i//192]


def mask_lookup(m,tag,i,j):
    if tag not in (0,1) or not (0<=i<49152 and 0<=j<49152):
        raise ValueError('qualified mask domain required')
    return m['faces'][tag]['mask'][(255-j//192)*256+i//192]


def packed_seed_key(tag,world_origin,origin,cell,system,body_index):
    """Interior 0078d7b0 + 0096f5c0, no seam/wrap or unsupported tag guesses."""
    if type(system) is not int or not 0<=system<2**18 or type(body_index) is not int or not 0<=body_index<64:
        raise ValueError('system/body key domain')
    x=world_origin[0]+origin[0]+cell[0]
    y=world_origin[1]+origin[1]+cell[1]
    if tag not in (0,1) or not (0<=x<49152 and 0<=y<49152):
        raise ValueError('seed coordinate crosses unimplemented seam')
    return (((((system<<6)|body_index)<<3|tag)<<16|y)<<16)|x


def neighborhood(tag, world_origin, center, radius, selected, patterns, blocks,
                 *, maximum_width, padding=2, merge=2, step=12):
    """Finite conservative owner-cell halo; generate whole returned sources.

    Requires nonnegative bounded widths and ordinary rectangular base sources.
    A retained center lies inside source clip expanded by W; a strip lies within
    another W. Padding + merge cells conservatively cover clip beyond ownership.
    This does not truncate walks or earlier competition to the query disk.
    """
    if radius<=0 or maximum_width<0: raise ValueError('positive disk/nonnegative width required')
    halo=radius+100*(padding+merge)+2*maximum_width
    lo=[math.floor(world_origin[k]+(center[k]-halo)/100) for k in (0,1)]
    hi=[math.floor(world_origin[k]+(center[k]+halo)/100) for k in (0,1)]
    sources={}
    for i in range(lo[0],hi[0]+1):
        for j in range(lo[1],hi[1]+1):
            s=source_at(tag,i,j,world_origin,selected,patterns,blocks,
                        padding=padding,merge=merge,step=step)
            sources[s['id']]=s
    return dict(owner_cell_bounds=[lo,hi],halo_native=halo,
                maximum_width=maximum_width,sources=list(sources.values()))
