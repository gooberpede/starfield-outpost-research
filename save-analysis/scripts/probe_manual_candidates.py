"""Corpus-specific candidate probes, not a general record parser.

Reads a verified analysis run's decoded files/analysis.json. Writes a fresh
candidate JSON beside them. Exact signatures were discovered in this corpus;
roles, 3-byte identities, tagged definition IDs and float meanings are hypotheses.
No live inputs, network, dependencies beyond CPython stdlib, or target effects.
Usage: python save-analysis/scripts/probe_manual_candidates.py --run analysis-01
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct

BASE = Path(__file__).resolve().parents[2] / '.local-work/manual-S0-S7C'
MAIN = {'beacon':'3a822c5d03070192', 'storage':'3a822d486b03009a',
        'extractor':'3a822da96b03009a', 'solar':'3a822dba0f030092'}
TOKENS = {'beacon':'822c5d', 'storage':'822d48', 'extractor':'822da9', 'solar':'822dba'}
LINK = bytes.fromhex('04822c5d08822d4804822da9')
BEACON_XYZ = bytes.fromhex('5d62f54290a08a436ed09241')


def hits(b, needle):
    return [x.start() for x in re.finditer(re.escape(needle),b)]


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run',required=True); args=ap.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]+',args.run):
        raise SystemExit('Simple run name required')
    directory=BASE/args.run
    analysis=json.loads((directory/'analysis.json').read_text())
    output=[]
    for sample in analysis['samples']:
        label=sample['label'];b=(directory/f'{label}.decoded.bin').read_bytes()
        assert hashlib.sha256(b).hexdigest()==sample['decoded_sha256']
        row=dict(label=label, decoded_sha256=sample['decoded_sha256'], candidates={},
                 link_motif_offsets=hits(b,LINK), header_location=b[46:46+struct.unpack_from('<H',b,44)[0]].decode('ascii'),
                 name_offsets={name:hits(b,name.encode()) for name in ['Kreet Outpost 1','SOR-001']})
        for role,signature in MAIN.items():
            offsets=hits(b,bytes.fromhex(signature))
            if len(offsets)>1:
                raise ValueError(f'Ambiguous main signature: {label}/{role}')
            info=dict(main_offsets=offsets, token_offsets=hits(b,bytes.fromhex(TOKENS[role])))
            if offsets:
                off=offsets[0]; w=b[off:off+512]
                info['window_512_sha256']=hashlib.sha256(w).hexdigest()
                if role=='solar':
                    info.update(float_offset=off+50, float_hex=w[50:62].hex(),
                                float32le=list(struct.unpack_from('<3f',w,50)))
                if role=='beacon':
                    info['position_pattern_offsets']=[off+x for x in hits(w,BEACON_XYZ)]
                    info['float32le_interpretation']=list(struct.unpack('<3f',BEACON_XYZ))
                if role=='storage':
                    info['counter_probe_u32_at_101']=struct.unpack_from('<I',w,101)[0]
            row['candidates'][role]=info
        strings=['outpostbeaconscript','OBJ_Outpost_Beacon_Deploy','OBJ_Outpost_Beacon_On_LP',
                 'OBJ_Harvester_Solid_Small_Start','OBJOutpost_Solar_Array_LP_Play',
                 'KreetPlanetWorld','::SNarionA_PAnselon_MKreet_var','latitude','longitude']
        row['string_offsets']={s:hits(b,s.encode()) for s in strings}
        output.append(row)
    result=dict(script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                analysis_sha256=hashlib.sha256((directory/'analysis.json').read_bytes()).hexdigest(),
                main_signatures=MAIN, tokens=TOKENS, link_motif=LINK.hex(), samples=output)
    with (directory/'candidates.json').open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,indent=2);f.write('\n')
    for row in output:
        print(row['label'],{k:v['main_offsets'] for k,v in row['candidates'].items()},row['link_motif_offsets'])


if __name__=='__main__':
    main()
