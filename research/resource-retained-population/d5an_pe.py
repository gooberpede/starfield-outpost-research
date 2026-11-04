# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded stdlib reader for owned candidate PE exports/version metadata.

Reads a specified native DLL only; no writes, loading, dependency or process
operations. Addresses returned are DLL-relative RVAs and preferred image values.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import struct

def inspect(path):
    data=path.read_bytes()
    def require(v):
        if not v:raise ValueError('Malformed owned PE metadata')
    require(data[:2]==b'MZ');nt=struct.unpack_from('<I',data,0x3c)[0]
    require(data[nt:nt+4]==b'PE\0\0')
    sections=struct.unpack_from('<H',data,nt+6)[0];opt_size=struct.unpack_from('<H',data,nt+20)[0];opt=nt+24
    require(struct.unpack_from('<H',data,opt)[0]==0x20b)
    base=struct.unpack_from('<Q',data,opt+24)[0];image_bytes=struct.unpack_from('<I',data,opt+56)[0]
    table=opt+opt_size;regions=[]
    for index in range(sections):
        vsize,rva,size,offset=struct.unpack_from('<4I',data,table+index*40+8)
        require(offset+size<=len(data));regions.append((rva,size,offset))
    def read(rva,size):
        for start,length,offset in regions:
            if start<=rva and rva+size<=start+length:return data[offset+rva-start:offset+rva-start+size]
        raise ValueError('PE RVA outside file-backed section')
    def string(rva):
        value=bytearray()
        for n in range(4096):
            byte=read(rva+n,1)
            if byte==b'\0':return value.decode('ascii')
            value.extend(byte)
        raise ValueError('Unterminated PE export name')
    export_rva,export_size=struct.unpack_from('<2I',data,opt+112)
    directory=read(export_rva,40)
    count,names,functions_rva,names_rva,ordinals_rva=struct.unpack_from('<5I',directory,20)
    require(count<65536 and names<65536)
    exports={}
    for index in range(names):
        name_rva=struct.unpack('<I',read(names_rva+index*4,4))[0]
        ordinal=struct.unpack('<H',read(ordinals_rva+index*2,2))[0];require(ordinal<count)
        function=struct.unpack('<I',read(functions_rva+ordinal*4,4))[0]
        name=string(name_rva);require(name not in exports);exports[name]=function
    require('SFSEPlugin_Version' in exports)
    schema,version=struct.unpack('<2I',read(exports['SFSEPlugin_Version'],8))
    return dict(preferred_image_base=base,image_bytes=image_bytes,exports=exports,
        sfse_version_schema=schema,plugin_version=version,
        version='.'.join(str((version>>shift)&255) for shift in (24,16,8)))
