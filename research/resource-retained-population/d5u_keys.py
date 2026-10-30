# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute native key/query conversion and selected corner retention controls.

Reuses pinned owned D5T setup and installed PE in this disposable process only.
Reads D5U census/model inputs; writes one new ignored JSON receipt. No target,
save, installed/database/Git mutation, network or dependency installation.
Native corner cells use preallocated buffers; all 24 contributor permutations
are tested. This qualifies retention and coordinates, not an entire live scheduler.
"""
from pathlib import Path
import itertools
import os
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT/'.local-work/d5u'
support = ROOT/'.local-work/d5t'
sys.path.insert(0, os.environ['D5S_OUTPUT'])
source = (support/'native_keys.py').read_text(encoding='utf8').split('packed=[]')[0]
source = source.replace("Path(__file__).with_name('native_probe.py')", "Path("+repr(str(support/'native_probe.py'))+")")
source = source.replace("'14078d7b0','14096f5c0']", "'14078d7b0','14096f5c0','14078d660','140988670']")
exec(compile(source,'owned-D5T-key-setup','exec'))
sys.path.insert(0,str(ROOT/'research/resource-retained-population'))
from d5u_census import inputs
c, cc, raster = inputs()
census = json.loads((LOCAL/'census.json').read_text(encoding='utf8'))
query_convert = C.WINFUNCTYPE(C.c_void_p,*([C.c_void_p]*4))(0x14078d660)
normalize = C.WINFUNCTYPE(None,*([C.c_void_p]*3))(0x14096f5c0)
rows, packed = [], []
for item in census['sources']:
    row = item['catalogue']
    ch, ax, ay, block = row['source_key'].split(':')
    ch, ax, ay = int(ch),int(ax),int(ay)
    body = (cc if item['corpus']=='controls' else c)['bodies'][row['body'][2:]]
    put(master,0x58,'<I',body['system'])
    put(master,0x5c,'<I',body['index'])
    for at,value in [(0xc8,ch),(0xcc,ax//192),(0xd0,ay//192),
                     (0xdc,(ax%192)//12),(0xe0,(ay%192)//12),(0xec,0),(0xf0,0)]:
        put(manager,at,'<I',value)
    for q in item['coordinates']:
        xy = (C.c_int32*2)(q['x'],q['y'])
        descriptor = C.create_string_buffer(C.string_at(C.addressof(manager)+0xc8,48))
        normalize(C.addressof(master),C.addressof(descriptor),C.addressof(xy))
        d = bytes(descriptor)
        x = 192*struct.unpack_from('<i',d,4)[0]+12*struct.unpack_from('<i',d,20)[0]+struct.unpack_from('<i',d,36)[0]
        y = 192*struct.unpack_from('<i',d,8)[0]+12*struct.unpack_from('<i',d,24)[0]+struct.unpack_from('<i',d,40)[0]
        assert d[0]==ch and [x,y]==[q['face_x'],q['face_y']]
        converted = C.create_string_buffer(48)
        query_convert(C.addressof(manager),C.addressof(converted),C.addressof(manager)+0xc8,C.addressof(xy))
        assert bytes(converted)[0] == ch
        normalized = list(struct.unpack_from('<2d',bytes(converted),8))
        bias = C.c_double.from_address(0x144f046a8).value
        scale = C.c_double.from_address(0x144f04718).value
        assert normalized == [(v+bias)*(scale/49152)-bias for v in (x,y)]
        rows.append(dict(source_id=row['source_id'],query=[q['x'],q['y']],face=[x,y],
                         normalized_xy=normalized))
    model_path = LOCAL/'native03'/(row['source_id']+'-model.json')
    if model_path.exists():
        model = json.loads(model_path.read_text(encoding='utf8'))['results'][0]['request']
        for key, expected in model['packed_keys'].items():
            x,y = map(int,key.split(','))
            xy = (C.c_int32*2)(model['origin'][0]+x,model['origin'][1]+y)
            value = C.c_uint64()
            convert(C.addressof(manager),C.byref(value),C.addressof(xy))
            assert value.value == expected,(row['source_id'],key,value.value,expected)
            packed.append(dict(source_id=row['source_id'],cell=[x,y],key=value.value))

setter = C.WINFUNCTYPE(C.c_uint64,*([C.c_void_p]*4),C.c_uint8)(0x140988670)
hashpoint = C.WINFUNCTYPE(C.c_uint32,*([C.c_void_p]*6))(0x140982090)
crc_table = (C.c_uint32*256).from_address(0x144d58d70)


def fold(value, payload):
    for byte in payload:
        value = (value>>8)^crc_table[(value^byte)&255]
    return value


corners = []
target = '0:37440:20928:0029d211'
for dx,dy in [(-1,-1),(-1,11),(11,-1)]:
    qx,qy = 37440+dx,20928+dy
    contributors = []
    for tx in range((qx-23)//192,(qx+2)//192+1):
        for ty in range((qy-23)//192,(qy+2)//192+1):
            tile = c['bodies']['0005e0de']['tiles'][f'0:{tx}:{ty}']
            assert tile[1]==8
            for slot,(block,flags) in enumerate(c['patterns'][tile[0]]):
                if not flags&8:
                    continue
                sx,sy = divmod(slot,16)
                ax,ay = tx*192+sx*12,ty*192+sy*12
                w,h = [v-4 for v in c['source_blocks'][block]]
                x,y = qx-ax,qy-ay
                if not (-2<=x<w+2 and -2<=y<h+2):
                    continue
                assert not 0<=x<w and not 0<=y<h
                flag = (4 if x<0 else 8)|(2 if y<0 else 1)
                values = [ty,sx,sy,0,0,flags>>5]
                args = [C.c_uint32(v) for v in values]
                seed = hashpoint(*[C.byref(v) for v in args])
                low = (fold(fold(seed,struct.pack('<I',tx)),b'\0')<<2)&0xffffffff
                contributors.append(dict(source=f'0:{ax}:{ay}:{block}',flag=flag,visited_low=low))
    assert len(contributors)==4 and len({r['visited_low'] for r in contributors})==4
    identities = {r['source']:i+0x1000 for i,r in enumerate(contributors)}
    outputs = []
    for order in itertools.permutations(contributors):
        cell = C.create_string_buffer(0x80)
        xy = C.c_uint64()
        weight = C.c_uint64()
        for r in order:
            setter(C.addressof(cell),identities[r['source']],C.byref(xy),C.byref(weight),r['flag'])
        stored = [C.c_void_p.from_buffer(cell,k).value for k in (0x18,0x20,0x28,0x30)]
        assert identities[target] in stored and len(set(stored))==4 and None not in stored
        outputs.append(stored)
    assert all(v==outputs[0] for v in outputs)
    mask = next(q['mask'] for q in census['sources'][-1]['coordinates'] if q['x']==dx and q['y']==dy)
    corners.append(dict(query=[dx,dy],root=[dx+1,dy-1],mask=mask,contributors=contributors,
                        permutations=24,slots=outputs[0],target_slot_index=outputs[0].index(identities[target]),
                        visited_collision=False))
assert {v['mask'] for v in corners} == {0,1,3}
result = dict(functions=pins,queries=rows,packed_keys=packed,corners=corners,
              code_sha256=sha(__file__),free=free(),scope='Native coordinate/key/corner instructions; QS1 scheduling is a separate static proof')
destination = LOCAL/sys.argv[1]
assert not destination.exists()
destination.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS',len(rows),'queries',len(packed),'keys',[(v['query'],v['mask']) for v in corners])
