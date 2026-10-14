"""SPDX-License-Identifier: GPL-3.0-or-later
Read-only selective installed definition context, all header types, no classes
excluded by name. Stdlib/project only. Caller owns local output and source pins.
Fields retained are identity/type/EditorID/keywords only; no assets.
"""
import struct
import zlib
from pathlib import Path
from extractor_resources import qualified
from inspect_outpost_definitions import esm_records, subrecords
from inventory_historical_saves import identity, guard


def context(paths, wanted):
    guard()
    if len({p.name.lower() for p in paths})!=len(paths): raise ValueError('DUPLICATE_PLUGIN_NAME')
    headers = {}
    sources = []
    for p in paths:
        pin = identity(p)
        row, fs = next(esm_records(p, {b'TES4'}, repeated=True))
        headers[p.name.lower()] = dict(flags=row['flags'],
            masters=[v.rstrip(b'\0').decode('utf8').lower() for k,v in fs if k==b'MAST'])
        sources.append(pin)
    flags = {p:h['flags'] for p,h in headers.items()}
    result = {}
    census = {}
    for path, pin in zip(paths, sources):
        guard()
        nrecords = 0
        with path.open('rb') as f:
            p, stack, total = 0, [path.stat().st_size], path.stat().st_size
            while p < total:
                while p == stack[-1] and len(stack)>1: stack.pop()
                if p+24>stack[-1]: raise ValueError('CONTEXT_HEADER_BOUNDS')
                f.seek(p); h=f.read(24)
                tag=h[:4]; size, rf, fid=struct.unpack_from('<III',h,4)
                end=p+(size if tag==b'GRUP' else size+24)
                if not p+24<=end<=stack[-1]: raise ValueError('CONTEXT_GROUP_BOUNDS')
                if tag==b'GRUP': stack.append(end); p+=24; continue
                nrecords += 1
                key=qualified(path.name.lower(),fid,headers[path.name.lower()]['masters'],flags)
                if key in wanted:
                    # Existing reader's decompression/subrecord checks reused.
                    raw=f.read(size)
                    if rf&0x40000:
                        length=int.from_bytes(raw[:4],'little')
                        dec=zlib.decompressobj(); data=dec.decompress(raw[4:],length+1)
                        if len(data)!=length or not dec.eof or dec.unused_data or dec.unconsumed_tail:
                            raise ValueError('CONTEXT_ZLIB_CLOSURE')
                        raw=data
                    fs=list(subrecords(raw))
                    edid=next((v.rstrip(b'\0').decode('utf8','backslashreplace') for k,v in fs if k==b'EDID'),None)
                    kw=b''.join(v for k,v in fs if k==b'KWDA')
                    if len(kw)%4: raise ValueError('CONTEXT_KEYWORD_WIDTH')
                    result.setdefault(key,[]).append(dict(plugin=path.name, offset=p,
                        offset_domain='ORIGINAL_ESM_FILE', record_type=tag.decode('ascii'),
                        formid=fid, editor_id=edid, flags=rf,
                        keywords=[qualified(path.name.lower(),int.from_bytes(kw[i:i+4],'little'),
                            headers[path.name.lower()]['masters'],flags) for i in range(0,len(kw),4)]))
                p=end
            if p!=total or any(e!=total for e in stack[1:]): raise ValueError('CONTEXT_CLOSURE')
        if identity(path)!=pin: raise ValueError('CONTEXT_INPUT_CHANGED')
        census[path.name]=nrecords
    return dict(schema='workshop-definition-context/1', records=result, sources=sources,
                header_census=census, selection='EXACT_REQUESTED_IDENTITIES_ALL_RECORD_TYPES')


if __name__=='__main__':
    import argparse
    import json
    ap=argparse.ArgumentParser()
    ap.add_argument('--esm',type=Path,nargs='+',required=True)
    ap.add_argument('--wanted',type=Path,required=True,help='JSON list of exact qualified identities')
    ap.add_argument('--run',required=True)
    args=ap.parse_args()
    if not args.run.isascii() or not args.run.replace('-','').isalnum(): raise ValueError('RUN_NAME')
    data=context(args.esm,set(json.loads(args.wanted.read_text(encoding='utf8'))))
    out=Path(__file__).resolve().parents[2]/'.local-work/workshop-inventory'/('definition-'+args.run+'.json')
    with out.open('x',encoding='utf8',newline='\n') as f:
        json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
    print(out)
