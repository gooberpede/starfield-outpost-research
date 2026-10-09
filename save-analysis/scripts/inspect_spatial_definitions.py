"""SPDX-License-Identifier: GPL-3.0-or-later
Original observation-only ESM spatial catalog. Reads explicitly supplied ESM;
hashes before/after; exclusive local output. Stdlib/project reader only. The
underlying dictionary retains last repeated subrecord: not a component merger.
Only <=256-byte fields exported, raw local data never cleared for publication.
"""
import argparse
import json
from pathlib import Path
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import identity, guard


def main():
    ap=argparse.ArgumentParser();ap.add_argument('esm',type=Path);ap.add_argument('output',type=Path)
    args=ap.parse_args();guard();before=identity(args.esm);rows=[]
    for r,f in esm_records(args.esm,{b'PNDT',b'STDT',b'WRLD',b'CELL',b'LCTN'}):
        r['edid']=f.get(b'EDID',b'').rstrip(b'\0').decode('utf8','backslashreplace')
        r['fields']={k.decode():v.hex() for k,v in f.items() if len(v)<=256}
        rows.append(r)
    if identity(args.esm)!=before:raise RuntimeError('ESM_CHANGED')
    with args.output.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(dict(source=before,records=rows),f);f.write('\n')
    print(len(rows))


if __name__=='__main__':main()
