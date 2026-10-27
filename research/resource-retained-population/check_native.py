# SPDX-License-Identifier: GPL-3.0-or-later
"""Adversarial replay of real disposable-process receipts; no target operations.

Reads a native qualification folder; writes only fresh task-local results and
one deliberately corrupted copy. Never edits source observations or predictions.
Supplemental reducer tests do not substitute for actual debugger qualification.
"""
import copy
import json
from pathlib import Path
import struct
import sys
from build import LOCAL
from native_reduce import reduce
from qualify import decoder


def main():
    folder,output=(Path(x).resolve() for x in sys.argv[1:]);assert folder.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    output.mkdir(exist_ok=False);base=[json.loads(x) for x in (folder/'basic/events.jsonl').read_text().splitlines()]
    image=next(r['image_sha256'] for r in base if r['kind']=='SESSION');results=[]
    def evaluate(name,change,expected=0):
        rows=copy.deepcopy(base);change(rows)
        try:r=reduce(rows,image,synthetic=True);passed=len(r['chains'])==expected;detail=dict(chains=len(r['chains']),reasons=[x['reason'] for x in r['rejected']])
        except (ValueError,KeyError,IndexError,struct.error,TypeError) as e:passed=expected==0;detail=dict(rejected=type(e).__name__)
        assert passed,(name,detail);results.append(dict(case=name,passed=True,**detail))
    def sample(rows,event,decision=None):
        return next(r for r in rows if r.get('event')==event and (decision is None or (r.get('operand',0)<r.get('lookup_capacity',0))==decision))
    def drop(rows,event):
        rows[:]=[r for r in rows if r.get('event')!=event]
        n=0
        for r in rows:
            if r['kind']=='SAMPLE':n+=1;r['capture']=n
    for event in ('native_visited','native_lookup','native_query','native_mask','native_append','native_complete'):
        evaluate('missing_'+event,lambda rows,e=event:drop(rows,e))
    evaluate('raw_context_tamper',lambda r:sample(r,'native_mask').update(raw_context='00'*1232))
    evaluate('wrong_thread_lifetime',lambda r:sample(r,'native_lookup',True).update(thread_lifetime=99999))
    evaluate('wrong_probe_name',lambda r:sample(r,'native_mask').update(event='native_query'))
    evaluate('negative_probe_index',lambda r:sample(r,'native_mask').update(site=-1))
    evaluate('capture_sequence',lambda r:sample(r,'native_mask').update(capture=9999))
    evaluate('missing_barrier',lambda r:r.__setitem__(slice(None),[x for x in r if x['kind']!='ARM_BARRIER']))
    evaluate('read_failure',lambda r:sample(r,'native_append').update(read_complete=False))
    evaluate('bad_native_frame',lambda r:sample(r,'native_query').update(frame_valid=False))
    evaluate('query_changed_mid_invocation',lambda r:sample(r,'native_query').update(query_raw='0000000000000000'))
    evaluate('descriptor_changed_mid_invocation',lambda r:sample(r,'native_mask').update(descriptor_raw='00'*44))
    evaluate('manager_identity_changed',lambda r:sample(r,'native_lookup',True).update(manager=123))
    evaluate('forged_population_source',lambda r:sample(r,'native_lookup',True)['population'].update(source=123))
    evaluate('forged_owned_slot',lambda r:sample(r,'native_lookup',True)['population'].update(slot_raw='00'*24))
    def corrupt_data(rows):
        resource=sample(rows,'native_lookup',True)['population']['resources'][0];b=bytearray.fromhex(resource['collection_header']);struct.pack_into('<Q',b,16,123);resource['collection_header']=b.hex()
    evaluate('collection_data_pointer_corruption',corrupt_data)
    evaluate('failed_copy',lambda r:sample(r,'native_append')['temporary'].update(points='00'*32))
    evaluate('changed_retained_geometry',lambda r:sample(r,'native_lookup',True)['population']['resources'][0]['regions'][0].update(points='00'*32))
    def bad_append(rows):
        r=sample(rows,'native_append');r['append_index']=0xffffffff;b=bytearray.fromhex(r['raw_context']);struct.pack_into('<Q',b,0x78,0xffffffff);r['raw_context']=b.hex()
    evaluate('false_success_after_append_minus_one',bad_append)
    def contrary(rows):
        r=sample(rows,'native_mask');r['operand']=3;b=bytearray.fromhex(r['raw_context']);struct.pack_into('<Q',b,0x78,3);r['raw_context']=b.hex()
    evaluate('direct_mask_preserved_despite_unchanged_points',contrary,1)
    evaluate('fixture_oracle_ignored',lambda r:[x.update(fixture_oracle=dict(reset_phase=999)) for x in r],1)
    raw=bytearray(next((folder/'basic').glob('capture-*.bin')).read_bytes());raw[len(raw)//2]^=1;p=output/'corrupt.bin';p.write_bytes(raw)
    refused=False
    try:decoder.independent(p)
    except (ValueError,RuntimeError,UnicodeError,AssertionError):refused=True
    assert refused;results.append(dict(case='sro1_corruption',passed=True))
    refused=False
    try:reduce(base,image,synthetic=False)
    except ValueError:refused=True
    assert refused;results.append(dict(case='synthetic_never_retail',passed=True))
    (output/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(len(results),'native counterexample controls PASS')


if __name__=='__main__':main()
