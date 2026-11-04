# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute bounded D5AQ startup and raster controls in an owned native host.

Reads pinned installed PE/PlanetData, retained D5S fixture methods/metadata and
authenticated static member metadata. Writes one fresh local receipt directory.
SOR-P-0002 lineage: D5S private-page/key setup; D5H map grammar and math exports.
Original projection, quantization, landing snap, current-center conversion and
ordinary raster sampler execute. The CPU dispatch thunk is supplied explicitly
for each original FMA/non-FMA fast path; scalar imports bind the installed CRT.
Definition lookup is the retained null callback after coordinate reconstruction.
These substitutions do not execute whole startup, node readiness or a game.

Requires Windows x64, pinned CPython with -E -B, retained local evidence and
40,000,000,000 caller-available bytes on C:/D:. Refuses identity/shape/result
mismatch, optimized Python, reparse paths and existing outputs. No downloads,
game/observer/save/configuration access, database opening or Git mutation.
Private mappings disappear at process exit; all original inputs are retained.
"""
import os
import sys
if (not __debug__ or sys.flags.optimize
        or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0')):
    raise SystemExit('Optimized Python is prohibited; invoke pinned Python -E -B')
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import zlib

ROOT = Path(__file__).resolve().parents[2]
PINNED_PY = Path('C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe')
EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
ARCHIVE = EXE.parent/'Data/Starfield - PlanetData.ba2'
PINS = {
    'docs/experiments/resource-retained-population/d5s-sources.csv': 'c8ed2286ddf03e64079d1dea3eeafa68571b781f8c1c7a83b4b57ac06081bce3',
    '.local-work/d5s/start.py': '28d82cce04a946025b3a332d79e59f5d94e199259ac22fd3194dca5ede15d2b7',
    '.local-work/d5s/native_probe.py': '5abaf40caf407a40c362f8f95c174fa98c08b8ac488bbc472927005350e56979',
    '.local-work/d5s/native_keys.py': 'ebd5fe5f152364a1886a7070e7a47b9bcc434cd488f3b72ac16c3ee8a190ce06',
    '.local-work/d5s/geometry.json': '9594ab2aa34856bcc3b8ecb249b46b0063ef4b5d1af80d4e557542f2d6657ccf',
    '.local-work/d5s/initial.json': '3d138719956c22b7cf5f97559f856a51ea95d4e7b5c511a945a00cde6880b63a',
    '.local-work/recon/activated-grid-01.tsv': '63d779c0066b6657db66f68355c8fcb54c78c3222326cf230a3e9d2075a83408',
    '.local-work/recon/surface-projection-14.tsv': 'adfad6c38019098a8b37b398e3a0a8211f64fa582289af69d231ab30d2b5e230',
    '.local-work/workshop-population-rework/specialist/d5h-gap14.tsv': '276431e7a52a6dc457e416636fca4a94b377912925153e237fe8d258a4f4eb15',
    '.local-work/workshop-population-rework/specialist/d5-mask01.tsv': 'bacbe8742ce465782016dcdc075173da373d65958dfebce5a085998965722051',
    '.local-work/workshop-population-rework/specialist/d5-raster02.tsv': '61db16bcd3fb9422689a82ac640bf0147f03db7cb3b9d4ca391f3001c412d383',
    '.local-work/d5s/functions/14078d4b0.txt': '26e5d3c38480165fdc155118b77d16f517454ab9aa47f613b25137944bdb300f',
}
EXE_HASH = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ARCHIVE_HASH = '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5'
RANGES = [(0x14096ecb0,0x14096ef02),(0x14096efb0,0x14096f1a0),
          (0x14096f940,0x14096fa8f),(0x142332410,0x14233256d),
          (0x1423321f0,0x14233240a),(0x14374dcd2,0x14374dcef),
          (0x14374e650,0x14374e74a),(0x14374dda0,0x14374df93),
          (0x14078d4b0,0x14078d5b1),(0x1434ca8d6,0x1434ca965),
          (0x1423390f0,0x1423391ce),(0x142339340,0x14233942f)]
METADATA_PINS = {
    '1402fbc20': 'bd57b237e664f026a5be8cd5dee11911a2d06a40cc9486b7a8ce4005036a9cef',
    '142346f80': '12035b17cd584cc3976b876d1bcf2e929370c6d08b7464c725011e1f42d838db',
    '1407ac0d0': 'a1cc8511b6306f79ba1c2c76f33e4f204f81047be44841073a7d900b0c0813d9',
    '1407ac2f0': '68f426b600c8ae9c86aba0d6025e43d0e49ab1bf0a6d80265da2ce83239c51db',
    '1407aedd0': '3d3f3ea0587d118235b034272cbd74925581f51a682158de22f777232ad4afce',
    '140970d50': '1ba27251f3632660b5fe9264bbf1d0579cae756e58ad4dc2828ccf2a1bc6eec3',
    '140982090': '79fd57de9816c4048966d6c223b482086ddeaae664ae5395fc72370850a2b083',
    '14078d7b0': 'f595d79cfa540c05e2a161995bef5112c6d160372bdf3b55f53a25e30864df71',
    '14096f5c0': 'b10fb77a93d0ead991159988afd3ed5dd16f1889bd2dd1ce04e3df1d1481240b',
    '14078d660': 'a5f96564721504c6fb6c4f737e6371a3fbedb414dd9b9ed5e2ad6f317db26650',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def ordinary_path(path):
    for part in (path, *path.parents):
        require(not part.is_symlink() and not part.is_junction(), 'Reparse path: '+str(part))


def guard():
    values = {drive: shutil.disk_usage(drive).free for drive in ('C:/','D:/')}
    require(min(values.values()) >= 40_000_000_000, 'Disk floor: '+str(values))
    return values


def load_masks():
    """Read the pinned BA2 member and validate the complete two-face grammar."""
    manifest = ROOT/'.local-work/resources-evidence-consolidation/d5r-input-lease01/.local-work/resource-save52/build-v1/manifest.json'
    require(sha(manifest) == '9d2ff9012a573595227c8feda5345de35286b807103665486239ddbe8cbfa9de', 'Static member manifest')
    member = json.loads(manifest.read_bytes())['members']['0005e0de']
    with ARCHIVE.open('rb') as stream:
        magic,version,kind,count,name_at = struct.unpack('<4sI4sIQ',stream.read(24))
        require((magic,version,kind)==(b'BTDX',2,b'GNRL') and count<10000,'BA2 header')
        stream.seek(32)
        entries=[struct.unpack('<I4sIIQIII',stream.read(36)) for _ in range(count)]
        stream.seek(name_at)
        names=[stream.read(int.from_bytes(stream.read(2),'little')).decode() for _ in range(count)]
        require(names.count(member['name'])==1,'Unique map member')
        start,packed,size=entries[names.index(member['name'])][4:7]
        require(size==member['bytes'] and size<2_000_000,'Map member size')
        require(start+(packed or size)<=ARCHIVE.stat().st_size,'Map member bounds')
        stream.seek(start)
        blob=stream.read(packed or size)
    if packed:
        decoder=zlib.decompressobj()
        blob=decoder.decompress(blob,size+1)
        require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,'Map decompression')
    require(len(blob)==size and hashlib.sha256(blob).hexdigest()==member['sha256'],'Map payload identity')
    version,flags,items=struct.unpack_from('<BBI',blob)
    require(version==5,'Map version')
    at=6+4*items
    face_count,=struct.unpack_from('<I',blob,at);at+=4
    require(face_count==2,'Map face count')
    result=[]
    for _ in range(2):
        width,height,points=struct.unpack_from('<III',blob,at);at+=12
        require((width,height,points)==(256,256,65536),'Map dimensions')
        at+=4*points
        mask_count,=struct.unpack_from('<I',blob,at);at+=4
        require(mask_count==points,'Mask dimensions')
        result.append(blob[at:at+points]);at+=points
    require(at==len(blob),'Map trailing bytes')
    return result,dict(path=str(manifest),sha256=sha(manifest),member=member)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    require(Path(sys.executable).resolve()==PINNED_PY.resolve(),'Pinned interpreter path')
    require(sha(PINNED_PY)=='cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b','Pinned interpreter bytes')
    out=args.out.resolve()
    require(out.is_relative_to(ROOT/'.local-work/d5aq') and not out.exists(),'Fresh D5AQ output required')
    ordinary_path(out)
    before=guard()
    for name,expected in PINS.items():
        ordinary_path(ROOT/name)
        require(sha(ROOT/name)==expected,'Input pin: '+name)
    require(sha(EXE)==EXE_HASH and sha(ARCHIVE)==ARCHIVE_HASH,'Installed input identities')
    require(sha('C:/Windows/System32/ucrtbase.dll')=='3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9','Host CRT identity')
    # Authenticate every metadata file before the retained native mapper reads it.
    metadata={}
    for entry,expected in METADATA_PINS.items():
        name=f'.local-work/d5s/functions/{entry}.txt'
        ordinary_path(ROOT/name)
        require(sha(ROOT/name)==expected,'Function metadata: '+entry)
        metadata[name]=sha(ROOT/name)
    masks,map_pin=load_masks()
    out.mkdir(parents=True,exist_ok=False)
    setup=(ROOT/'.local-work/d5s/native_keys.py').read_text(encoding='utf8').split('packed=[]')[0]
    setup=setup.replace("'14078d7b0','14096f5c0']", "'14078d7b0','14096f5c0','14078d660']")
    os.environ['D5S_OUTPUT']=str(ROOT/'.local-work/d5s')
    sys.path.insert(0,str(ROOT/'.local-work/d5s'))
    host={'__file__':str(ROOT/'.local-work/d5s/native_keys.py'),'__name__':'d5aq_native_host'}
    exec(compile(setup,'authenticated-owned-D5S-native-setup','exec'),host)
    C,k,page,write,offset,data,put=[host[v] for v in ('C','k','page','write','offset','data','put')]
    manager,master=host['manager'],host['master']
    require(C.sizeof(C.c_void_p)==8,'Windows x64 host')
    code=set()
    for low,high in RANGES:
        for address in range(low&~4095,(high+4096)&~4095,4096):
            page(address);code.add(address)
    for name in PINS:
        if name.endswith('.tsv') or name.endswith('14078d4b0.txt'):
            for line in (ROOT/name).read_text(encoding='utf8').splitlines():
                if re.match(r'^[0-9a-f]+\t[A-Z]',line):
                    for address in re.findall(r'\[0x([0-9a-f]+)\]',line):page(int(address,16))
    page(0x14374dcc0);code.add(0x14374dcc0&~4095)
    for thunk,name in ((0x1434ca8d6,'cos'),(0x1434ca960,'fmod'),(0x1434ca906,'atan2')):
        raw=data[offset(thunk):offset(thunk)+6]
        require(raw[:2]==b'\xff\x25','Import thunk '+hex(thunk))
        target=thunk+6+struct.unpack_from('<i',raw,2)[0]
        write(target,struct.pack('<Q',C.cast(getattr(host['crt'],name),C.c_void_p).value))
    for address in code:
        prior=C.c_ulong()
        require(bool(k.VirtualProtect(address,4096,0x20,C.byref(prior))),'Code protection')

    def branch(address):
        old=C.c_ulong()
        require(bool(k.VirtualProtect(0x14374d000,4096,4,C.byref(old))),'Dispatcher writable')
        write(0x14374dcc0,b'\xe9'+struct.pack('<i',address-0x14374dcc5))
        require(bool(k.VirtualProtect(0x14374d000,4096,0x20,C.byref(old))),'Dispatcher executable')
        require(bool(k.FlushInstructionCache(k.GetCurrentProcess(),None,0)),'Instruction flush')

    project=C.WINFUNCTYPE(C.c_void_p,C.c_void_p,C.c_void_p)(0x142332410)
    quantize=C.WINFUNCTYPE(C.c_void_p,C.c_void_p,C.c_void_p,C.c_uint32)(0x14096ecb0)
    snap=C.WINFUNCTYPE(C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p)(0x14096efb0)
    center=C.WINFUNCTYPE(C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p)(0x14078d4b0)
    convert=C.WINFUNCTYPE(C.c_void_p,*([C.c_void_p]*4))(0x14078d660)
    sample=C.WINFUNCTYPE(C.c_uint8,C.c_void_p,C.c_void_p)(0x142339340)
    raster=C.create_string_buffer(0x30);faces=C.create_string_buffer(2*0x30)
    arrays=[C.create_string_buffer(payload) for payload in masks]
    put(raster,0x18,'<Q',C.addressof(faces))
    for index,array in enumerate(arrays):
        put(faces,index*0x30,'<I',256);put(faces,index*0x30+4,'<I',256)
        put(faces,index*0x30+0x20,'<Q',C.addressof(array))
    rows=[];startup=[]
    for label,native in (('fma',0x14374e650),('nonfused',0x14374dda0)):
        branch(native)
        for x in range(-2,12):
            for y in range(-2,12):
                xy=(C.c_int32*2)(x,y);square=C.create_string_buffer(24);angles=(C.c_double*2)()
                convert(C.addressof(manager),C.addressof(square),C.addressof(manager)+0xc8,C.addressof(xy))
                project(C.addressof(angles),C.addressof(square))
                mask=sample(C.addressof(raster),C.addressof(angles))
                require(mask==(0 if y<0 else 3),'Native all-196 mask mismatch '+str((label,x,y,mask)))
                rows.append(dict(branch=label,original_int2=[x,y],mask=mask,angles=list(angles)))
                if (x,y)==(0,0):
                    descriptor=C.create_string_buffer(48);landing=C.create_string_buffer(48);local=(C.c_int32*2)()
                    quantize(C.addressof(descriptor),C.addressof(angles),256)
                    snap(C.addressof(master),C.addressof(landing),C.addressof(angles))
                    center(C.addressof(manager),C.addressof(local),C.addressof(angles))
                    decode=lambda b:[b.raw[0]]+[struct.unpack_from('<i',b.raw,at)[0] for at in (4,8,20,24,36,40)]
                    require(decode(descriptor)==decode(landing)==[0,195,109,8,0,0,0] and list(local)==[0,0],'Startup numeric preimage')
                    startup.append(dict(branch=label,angles=list(angles),quantized=decode(descriptor),snapped=decode(landing),center=list(local)))
    result=dict(status='PASS',scope='Native numeric initializer preimage and all-196 ordinary sampler; supplied file/raster/owner state, not whole startup or retail',
                startup=startup,rows=rows,counts_per_branch={'mask0':28,'mask3':168},
                substitutions=['Original FMA/nonfused CPU fast paths selected by private dispatcher thunk','Installed CRT scalar imports','Retained null definition lookup after coordinate reconstruction','Supplied authentic map bytes in private face buffers'],
                pins=PINS,metadata=metadata,map_pin=map_pin,exe_sha256=EXE_HASH,archive_sha256=ARCHIVE_HASH,
                method_sha256=sha(__file__),ranges=[dict(start=hex(a),end=hex(b),sha256=hashlib.sha256(data[offset(a):offset(b)+1]).hexdigest()) for a,b in RANGES],
                disk_before=before,disk_after=guard())
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(status='PASS',out=str(out),native_queries=len(rows),startup=startup)))


if __name__=='__main__':
    main()
