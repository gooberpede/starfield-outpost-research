"""SPDX-License-Identifier: GPL-3.0-or-later
Read explicit local Q ledger/geometry/saved receipts; emit selected CSV to stdout.
No writes or target access. Omits memory/pointers; output remains REVIEW-REQUIRED.
"""
import argparse,csv,hashlib,io,json
from pathlib import Path


def index(ledger,geometry,saved):
    columns=['invocation','begin_sequence','end_sequence','thread','candidate_key',
        'descriptor_sha256','begin_raw_offset','begin_raw_sha256','end_raw_offset','end_raw_sha256',
        'return_u32','latch_before_after','predicted_candidate_geometry','geometry_status',
        'save27_angle_offset','save28_angle_offset','saved_wire_identity','saved_kind_hex',
        'actual_path','E_C_center_grid']
    out=io.StringIO(newline='');w=csv.DictWriter(out,columns,lineterminator='\n');w.writeheader()
    for row,g,s27,s28 in zip(ledger,geometry['invocations'],saved[0]['rows'],saved[1]['rows'],strict=True):
        assert row['invocation']==g['invocation']==s27['invocation']==s28['invocation']
        a,b=row['journal']
        w.writerow(dict(invocation=row['invocation'],begin_sequence=row['begin_sequence'],
            end_sequence=row['end_sequence'],thread=row['thread'],candidate_key=row['candidate_form'],
            descriptor_sha256=hashlib.sha256(bytes.fromhex(row['candidate_hex'])).hexdigest(),
            begin_raw_offset=a['offset'],begin_raw_sha256=a['sha256'],end_raw_offset=b['offset'],end_raw_sha256=b['sha256'],
            return_u32=row['uint32_return'],latch_before_after=row['output_before_hex']+'/'+row['output_after_hex'],
            predicted_candidate_geometry=json.dumps(g['modes']['avx']['candidate_geometry'],separators=(',',':')),
            geometry_status='PREDICTION: res256 B12 component-match; native result UNKNOWN',
            save27_angle_offset=json.dumps(s27['exact_angle_positions']),save28_angle_offset=json.dumps(s28['exact_angle_positions']),
            saved_wire_identity=s27['proposed_saved_token'],saved_kind_hex=s27['neighbors'][0]['preceding6_hex'][-4:],
            actual_path='UNKNOWN: early preserve OR hierarchy/flag skip then disjoint rectangle',
            E_C_center_grid='0/0/0/0 linked observed events'))
    return out.getvalue()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('ledger','geometry','saved'):p.add_argument(n,type=Path)
    a=p.parse_args();print(index(*(json.loads(getattr(a,n).read_text()) for n in ('ledger','geometry','saved'))),end='')
