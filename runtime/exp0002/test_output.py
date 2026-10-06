# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate bytes emitted by the production native serializer in a fake process."""
import copy
import json
from pathlib import Path
import sys
import validate as v

fixture=json.loads(Path(sys.argv[1]).read_text())
assert fixture['kind']=='SYNTHETIC'
v.snapshot(fixture['snapshot'])
assert v.form(fixture['null_query'])=='NULL_RESULT'
assert v.form(fixture['failed_query'])=='READ_FAILED'
data=dict(schema='SOR-EXP-0002-native-v1',kind='SYNTHETIC',terminal='CHECKPOINT_COMPLETE',checkpoint='A2',
          scanned_entries=2,snapshot_atomic=False,observer_sha256='a'*64,executable_sha256='b'*64,module_profile_sha256='c'*64,
          module_base='0x7ff600000000',player=fixture['snapshot'],references=[])
for role,base in [('beacon',0x2c60e9),('storage',0x23aed9)]:
    snap=copy.deepcopy(fixture['snapshot']);snap['stored_base']['form_id']=hex(base)
    data['references'].append(dict(role=role,snapshot=snap,GetWorkshop=fixture['null_query'],GetCurrentLocation=fixture['null_query'],GetWorldSpace=fixture['null_query']))
v.checkpoint(data,synthetic=True)
checks=4
def rejected(obj):
    global checks
    try:v.checkpoint(obj,synthetic=True)
    except (ValueError,KeyError):checks+=1;return
    raise AssertionError('Invalid fixture accepted')
bad=copy.deepcopy(data);bad['references'].reverse();rejected(bad)
bad=copy.deepcopy(data);bad['references'][1]['GetWorkshop']=fixture['failed_query'];rejected(bad)
bad=copy.deepcopy(data);bad['player']['coordinates']['reference_xyz']['value'][0]=float('nan');rejected(bad)
bad=copy.deepcopy(data);bad['terminal']='CHECKPOINT_STARTED';rejected(bad)
bad=copy.deepcopy(data);bad['kind']='RUNTIME';rejected(bad)
try:v.trace([dict(event='ARMED')])
except ValueError:checks+=1
else:raise AssertionError('Missing trace terminal accepted')
records=[]
for name,stack in [('CALLBACK','0x1000'),('TAIL','0x1000'),('RETURN','0x1008')]:
    records.append(dict(kind='RUNTIME',sequence=len(records),event=name,thread_id=1,elapsed_ms=10,rsp=stack,
                        rip='0x2000',return_site='0x2000',rcx='0x3000',rdx='0x4000',r8='0x0',
                        selected_r8_plus_c8='0x3000',key_global='0x4000',correlated=True))
records.append(dict(kind='RUNTIME',sequence=3,event='TERMINAL',complete=True))
assert v.trace(records)=='STRUCTURALLY_COMPLETE_SCIENTIFIC_RESULT_UNASSESSED';checks+=1
for key,value in [('r8','0x1'),('rsp','0x9999'),('thread_id',2),('elapsed_ms',5001)]:
    bad=copy.deepcopy(records);bad[1][key]=value
    try:v.trace(bad)
    except ValueError:checks+=1
    else:raise AssertionError('Bad trace correlation/bound accepted')
for path in Path(sys.argv[1]).parent.glob('*-anomaly.json'):
    v.anomaly(json.loads(path.read_text()),synthetic=True);checks+=1
example=json.loads(Path(sys.argv[1]).with_name('ambiguous-anomaly.json').read_text())
for key,value in [('queries_invoked',1),('reason','entry_read_failed'),('instrument_available',False),('kind','RUNTIME')]:
    bad=copy.deepcopy(example);bad[key]=value
    try:v.anomaly(bad,synthetic=True)
    except ValueError:checks+=1
    else:raise AssertionError('Invalid anomaly accepted')
bad=copy.deepcopy(example);bad['expected_counts']['storage']=0
try:v.anomaly(bad,synthetic=True)
except ValueError:checks+=1
else:raise AssertionError('Wrong expected count accepted')
sync=json.loads(Path(sys.argv[1]).with_name('synchronization.json').read_text())
v.synchronization(sync);checks+=1
for key,value in [('operator_settled',False),('reloaded_and_settled',False),('synchronization','events_required')]:
    bad=copy.deepcopy(sync);bad[key]=value
    try:v.synchronization(bad)
    except ValueError:checks+=1
    else:raise AssertionError('Invalid synchronization evidence accepted')
print(json.dumps(dict(kind='SYNTHETIC',checks=checks,terminal='OUTPUT_TESTS_COMPLETE')))
