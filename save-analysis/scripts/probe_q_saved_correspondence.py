# SPDX-License-Identifier: GPL-3.0-or-later
"""Original local offline correspondence probe. Reads pinned Save27/28 originals,
creates exclusive immutable analysis copies, decoder scratch and selected JSON
under .local-work/q-to-e/saved-correspondence. No target/config/database/network.
40GB guards and before/after SHA256. Angle byte equality is not runtime ID mapping.
"""
from pathlib import Path
import hashlib,json,shutil,sys
ROOT=Path('D:/Projects/starfield-outpost-research')
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from verify_position_v2 import guard,digest
from stream_save import decoded_save
from outpost_planetary_location import global_suffix
from validate_mature_outposts import directory
from outpost_record_framing import iter_records
from reconcile_q_calls import saved_token_for_candidate
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--ledger',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
out=args.output;guard();out.mkdir()
pins=json.loads((ROOT/'.local-work/native-oracle-020/operations/continuation-live-postflight-supplement-01.json').read_text())['new_checkpoint_pins']
ledger=json.loads(args.ledger.read_text())
results=[]
for pin in pins:
    original=Path(pin['path']);before=digest(original);assert before==pin['sha256']
    copy=out/original.name;shutil.copyfile(original,copy);assert digest(copy)==before
    with decoded_save(copy,out/'scratch') as (b,metrics):
        d=directory(b);a,z=global_suffix(b,d)[6];rows=[]
        records=list(iter_records(b,*d['regions']['region_R3'],d['words'][9]))
        for r in ledger:
            angles=bytes.fromhex(''.join(r['angle_hex']));positions=[];p=a
            while (p:=b.find(angles,p,z))>=0:positions.append(p);p+=1
            key=int(r['candidate_form'],16)
            token=saved_token_for_candidate(key)
            matches=[dict(offset=x['offset'],end=x['end'],token=x['token'],
                explicit_type=x['explicit_type'],flags=x['flags']) for x in records if x['token']==token]
            rows.append(dict(invocation=r['invocation'],exact_angle_positions=positions,
                proposed_saved_token=token,numeric_saved_domain_record_matches=matches,
                neighbors=[dict(angle_offset=p,preceding6_hex=bytes(b[p-6:p]).hex(),
                    following4_hex=bytes(b[p+16:p+20]).hex()) for p in positions],
                limitation='Numeric tagged-ID correspondence is not independently validated runtime load remapping'))
        results.append(dict(source=str(original),sha256=before,copy=str(copy),
            metrics=metrics,global_unit6=[a,z],rows=rows))
    assert digest(original)==before and digest(copy)==before
guard();(out/'receipt.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
print(json.dumps([dict(source=r['source'],matched=[v['invocation'] for v in r['rows'] if v['exact_angle_positions']]) for r in results]))
