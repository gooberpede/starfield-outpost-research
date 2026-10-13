# SPDX-License-Identifier: GPL-3.0-or-later
"""Read native fixture outputs; corruption controls write fresh disposable copies."""
import json
import hashlib
import struct
from pathlib import Path
import shutil
import sys
from inspect_history import inspect,SIZE

def main(root):
    root=Path(root);results={}
    def check(name,condition):
        if not condition:raise AssertionError(name)
        results[name]='PASS'
    normal=inspect(root/'normal');check('normal_committed_integrity',normal['integrity']=='PASS_COMMITTED_PREFIX')
    check('restoration_record_type_distinct',normal['events'][0]['kind']==10 and normal['events'][0]['operand']['length']==12)
    check('late_non_workshop_write_retained',any(s['identity_late_bound'] and s['sequences'][0]==1 for s in normal['segments']))
    check('pointer_reuse_split',len(normal['segments'])>=2 and normal['segments'][0]['workshop_id']!=normal['segments'][1]['workshop_id'])
    check('native_lifetime_never_invented',all(s['lifetime']=='UNPROVEN' for s in normal['segments']))
    check('command_producer_application',len(normal['command_links'])==1 and normal['command_links'][0]['producer_invocation'] is not None)
    check('command_cross_thread',normal['command_links'][0]['cross_thread'])
    check('unwind_paired',not normal['unfinished_invocations'] and any(e['phase']==3 for e in normal['events']))
    check('d3_outer_transition',any(e['kind']==2 and e['phase']==2 and e['identity']['d3']==2 for e in normal['events']))
    centers=[e for e in normal['events'] if e['kind']==8 and e['phase']==2];check('nonzero_compensation_and_center_raw_XYZ',centers[0]['identity']['compensation']['hex']==struct.pack('<3f',1.25,-2.5,0.75).hex() and centers[0]['output']['hex']==struct.pack('<3f',9.25,-12.5,12.75).hex())
    check('unchanged_not_false_no_write',normal['unchanged_conversion_candidates'] and normal['scoped_no_write']=='NOT_ESTABLISHED')
    high=inspect(root/'high-rate');check('16000_zero_silent_loss',high['committed_records']==16000 and high['integrity']=='PASS_COMMITTED_PREFIX' and not high['unfinished_invocations'])
    check('concurrent_threads',len({e['thread'] for e in high['events']})==8)
    summary=inspect(root/'high-rate',summary=True);check('streaming_prefix_same_accounting',summary['committed_records']==high['committed_records'] and summary['paired_invocations']==high['paired_invocations'] and not summary['events'])
    selected=inspect(root/'normal',workshops=[normal['segments'][0]['workshop_id']]);check('two_pass_late_binding',selected['committed_records']==normal['committed_records'] and selected['segments'][0]['sequences'][0]==1)
    literal=inspect(root/'normal',workshops=['f1517de43e171745','0efca066ee4c7b9b']);check('literal_run_card_IDs_select_early_writes',literal['selected_records']>0 and literal['segments'][0]['sequences'][0]==1 and {s['workshop_id'] for s in literal['segments']}=={'f1517de43e171745','0efca066ee4c7b9b'})
    dest=root/'incoherent';shutil.copytree(root/'normal',dest);p=dest/'events.bin';data=bytearray(p.read_bytes());struct.pack_into('<Q',data,88,8);p.write_bytes(data);p=dest/'records.jsonl';lines=p.read_text().splitlines();first=json.loads(lines[0]);first['sha256']=hashlib.sha256(data[:SIZE]).hexdigest();lines[0]=json.dumps(first);p.write_text('\n'.join(lines)+'\n',encoding='utf8',newline='\n');quarantine=inspect(dest)
    check('incoherent_identity_quarantined',quarantine['quarantined_identity_events'][0]['sequence']==1 and all(1 not in s['sequences'] for s in quarantine['segments']))
    stop=inspect(root/'stop-pending');check('STOP_finishes_pending',stop['committed_records']==2 and not stop['unfinished_invocations'])
    invalid=inspect(root/'invalid');check('invalid_fields_are_unavailable',invalid['integrity']=='PASS_COMMITTED_PREFIX' and not invalid['events'][0]['ref']['ok'])
    failed=inspect(root/'writer-failure');check('real_write_failure_not_negative',failed['integrity']=='FAIL_OR_PARTIAL' and failed['committed_records']==0)
    tail=inspect(root/'journal-failure');check('raw_before_journal_failure_retained',len(tail['recoverable_uncommitted_records'])==1 and tail['committed_records']==0)
    crash=inspect(root/'crash-child/crash');check('crash_after_flush_recovered',crash['committed_records']==2 and crash['integrity']=='PASS_COMMITTED_PREFIX' and not crash['terminal_present'])
    for name,mutation in [('corrupt',lambda b:b.__setitem__(256,b[256]^1)),('truncate',lambda b:b.__delitem__(slice(-20,None)))]:
        dest=root/name;shutil.copytree(root/'normal',dest);p=dest/'events.bin';b=bytearray(p.read_bytes());mutation(b);p.write_bytes(b);check(name+'_detected',inspect(dest)['integrity']=='FAIL_OR_PARTIAL')
    check('equivalence_separate',normal['scientific_equivalence'].startswith('NOT_TESTED') and normal['complete_lifetimes']==0)
    for name in ('partial-terminal','partial-emergency'):
        dest=root/name;shutil.copytree(root/'normal',dest);p=dest/('terminal.json' if name=='partial-terminal' else 'emergency-status.json');p.write_bytes(b'{"error":');recovered=inspect(dest)
        check(name+'_prefix_retained',recovered['committed_records']==normal['committed_records'] and recovered['integrity']=='FAIL_OR_PARTIAL' and recovered['transport_retirement']=='UNCONFIRMED_CORRUPT_METADATA')
    (root/'inspector-results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main(sys.argv[1])
