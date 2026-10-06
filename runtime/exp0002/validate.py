#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only validation of native output shape/correlation, never engine truth."""
import argparse
import json
import math
from pathlib import Path

CHECKPOINTS=('A0','A0C','A1','A1C','A2','A2R')
ANOMALY_REASONS={'selected_counts_disagree','ambiguous_selection','collection_changed','unstable_identity',
 'nonfinite_transform','player_or_load_changed','loading_before_task','selection_time_budget','checkpoint_time_budget_after_query',
 'selected_identity_changed_before_query','reference_changed_during_queries','final_snapshot_load_changed',
 'player_context_unavailable','exterior_context_unavailable','collection_scope_bound','player_context_changed','cell_context_changed'}
def require(value,message):
    if not value:raise ValueError(message)

def synchronization(data):
    # Legacy first-run records remain readable; new metadata must be explicit.
    if 'synchronization' not in data:return
    require(data['synchronization']=='operator_settled_fresh_state_v1','synchronization model')
    require(data.get('operator_settled') is True,'operator confirmation')
    require(data.get('reloaded_and_settled') is (data['checkpoint']=='A2R'),'reload confirmation')
    counters=data['load_notifications']
    require(counters.get('role')=='telemetry_only','notification role')
    require(all(type(counters.get(n)) is int and 0<=counters[n]<=0xffffffff for n in ('pre','post')),'optional counters')
def form(value):
    require(isinstance(value,dict),'form object')
    state=value.get('status')
    require(state in ('OBSERVED','NULL_RESULT','READ_FAILED'),'form status')
    if state=='NULL_RESULT':require(value.get('pointer') is None,'null pointer')
    else:
        require(isinstance(value.get('pointer'),str) and int(value['pointer'],16)>0,'pointer identity')
        if state=='OBSERVED':
            require(0<=int(value['form_id'],16)<=0xffffffff,'FormID width')
            require(value.get('resolved_handle') is None,'unqualified handle')
    return state
def snapshot(value):
    for key in ('identity','stored_base','stored_parent_cell'):require(form(value[key])=='OBSERVED','incomplete selected identity')
    coords=value['coordinates']
    for name in ('reference_xyz','rotation_raw'):
        vector=coords[name]['value'];require(isinstance(vector,list) and len(vector)==3 and all(type(x) in (float,int) and math.isfinite(x) for x in vector),'finite XYZ')
        require(coords[name]['units']=='UNKNOWN','unqualified coordinate units')
    for name in ('cell_local_xyz','worldspace_xyz','body_relative_xyz','surface_map','latitude_longitude'):require(coords[name] is None,'unavailable derived domain')
    require(value['loaded_3d'] is None,'unqualified 3D state')
def checkpoint(data,synthetic=False):
    synchronization(data)
    require(data['schema']=='SOR-EXP-0002-native-v1','schema')
    require(data['kind']==('SYNTHETIC' if synthetic else 'RUNTIME'),'evidence kind')
    require(data['terminal']=='CHECKPOINT_COMPLETE','terminal')
    cp=data['checkpoint'];require(cp in CHECKPOINTS,'checkpoint')
    roles=[r['role'] for r in data['references']]
    expected=[] if cp in ('A0','A0C') else ['beacon'] if cp in ('A1','A1C') else ['beacon','storage']
    require(roles==expected,'selected roles/order')
    require(0<=data['scanned_entries']<=8192 and data['snapshot_atomic'] is False,'bounded non-atomic capture')
    for field in ('observer_sha256','executable_sha256','module_profile_sha256'):require(len(data[field])==64 and int(data[field],16)>=0,'hash')
    require(int(data['module_base'],16)%65536==0,'module base alignment')
    snapshot(data['player'])
    for ref in data['references']:
        snapshot(ref['snapshot'])
        expected_base=0x2c60e9 if ref['role']=='beacon' else 0x23aed9
        require(int(ref['snapshot']['stored_base']['form_id'],16)==expected_base,'base selection')
        for query in ('GetWorkshop','GetCurrentLocation','GetWorldSpace'):require(form(ref[query])!='READ_FAILED','query read failure')
def anomaly(data,synthetic=False):
    synchronization(data)
    require(data['schema']=='SOR-EXP-0002-anomaly-v1','anomaly schema')
    require(data['kind']==('SYNTHETIC' if synthetic else 'RUNTIME'),'anomaly evidence kind')
    require(data['terminal']=='ANOMALY_RECORDED' and data['instrument_available'] is True,'anomaly disposition')
    require(data['reason'] in ANOMALY_REASONS,'unsafe reason labelled as anomaly')
    cp=data['checkpoint'];require(cp in CHECKPOINTS+('TRACE',),'anomaly checkpoint')
    stage=5 if cp=='TRACE' else CHECKPOINTS.index(cp)
    require(data['expected_counts']==dict(beacon=int(stage>=2),storage=int(stage>=4)),'expected counts')
    require(set(data['observed_counts'])=={'beacon','storage'} and all(type(v) is int and 0<=v<=8192 for v in data['observed_counts'].values()),'observed counts')
    require(type(data['counts_complete']) is bool and type(data['candidates_truncated']) is bool,'count qualification')
    require(0<=data['scanned_entries']<=8192 and 0<=data['queries_invoked']<=6,'anomaly bounds')
    require(data['snapshot_atomic'] is False and len(data['candidates'])<=16,'bounded non-atomic candidates')
    if data['reason'] in {'selected_counts_disagree','ambiguous_selection','collection_changed','unstable_identity','loading_before_task','selection_time_budget','collection_scope_bound'}:
        require(data['queries_invoked']==0,'unqualified selection must not invoke targets')
    if data['candidates_truncated']:require(not data['counts_complete'],'truncated scan is incomplete')
    for candidate in data['candidates']:
        require(int(candidate['pointer'],16)>0 and 0<=int(candidate['base_form_id'],16)<=0xffffffff,'candidate identity')
        for field in ('position','rotation_raw'):
            v=candidate[field];require(len(v)==3 and all((type(x) in (int,float) and math.isfinite(x)) or (type(x) is str and x in {'NaN','+Infinity','-Infinity'}) for x in v),'observed vector')
    require(len({c['pointer'] for c in data['candidates']})==len(data['candidates']),'candidate deduplication')
def trace(records):
    require(records and records[-1]['event']=='TERMINAL','trace terminal missing')
    require(all(x['kind']=='RUNTIME' and x['sequence']==i for i,x in enumerate(records)),'trace kind/sequence')
    require(len(records)<=300,'record cap')
    if not records[-1]['complete']:return 'INCOMPLETE'
    rows={}
    for name in ('CALLBACK','TAIL','RETURN'):
        matching=[r for r in records if r['event']==name];require(len(matching)==1,'one selected operation');rows[name]=matching[0]
    a,b,c=(rows[n] for n in ('CALLBACK','TAIL','RETURN'))
    require(a['sequence']<b['sequence']<c['sequence'],'trace order')
    require(a['thread_id']==b['thread_id']==c['thread_id'],'thread correlation')
    require(a['rsp']==b['rsp'] and int(c['rsp'],16)==int(a['rsp'],16)+8,'stack correlation')
    require(b['rcx']==a['selected_r8_plus_c8'] and b['rdx']==a['key_global'] and int(b['r8'],16)==0,'callback-to-tail operands')
    require(c['rip']==a['return_site'],'return provenance')
    require(all(r['correlated'] and r['elapsed_ms']<=5000 for r in (a,b,c)),'capture bound/correlation')
    return 'STRUCTURALLY_COMPLETE_SCIENTIFIC_RESULT_UNASSESSED'
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('path',type=Path);p.add_argument('--trace',action='store_true');a=p.parse_args()
    raw=a.path.read_bytes();require(len(raw)<=(1250000 if a.trace else 32768),'file bound')
    if a.trace:
        lines=raw.splitlines();require(all(len(x)<=4096 for x in lines),'line bound');print(trace([json.loads(x) for x in lines]))
    else:
        data=json.loads(raw)
        if data.get('schema')=='SOR-EXP-0002-anomaly-v1':
            anomaly(data);print('ANOMALY_RECORDED; inspect evidence and current failure.json before acknowledged continuation')
        else:checkpoint(data);print('STRUCTURALLY_COMPLETE; live meaning and profile still require review')
if __name__=='__main__':main()
