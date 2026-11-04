# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AM N1 content-first protection using owned D5AL neutral methods (SOR-P-0002).

Reads protected namespace/size and positively hashes selected guarded files;
never scans protected save content while live. Full audits remain offline.
No target, configuration, original-save, deployment or network writes.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
from pathlib import Path
import d5al_content as neutral
from d5ai_episode import require,sha
from common import guard,regular

POLICY='sor-d5am-n1-content-timestamp/1'
content_guard=neutral.content_guard
archive_hashes=neutral.archive_hashes

def compare_protection(before,after):
    result=neutral.compare_protection(before,after)
    result['timestamp_policy']=POLICY
    return result

def lightweight(plan,preflight):
    import d5am_n1_operations as operations
    operations.source_pins(plan)
    require(plan.get('timestamp_policy')==POLICY,'D5AM content-first policy required')
    guard();module=operations.legacy();pm=module.policy_module();policy=pm.load_policy()
    previous=preflight['protection']
    require(pm.policy_hash(policy)==previous['save_policy_sha256'],'Save policy changed')
    current=pm.partition(pm.sizes(previous['live_path'],policy),policy)
    require(not current['unclassified'],'Unclassified live save')
    require(current['protected']=={n:dict(bytes=r['bytes']) for n,r in previous['protected_live'].items()},
            'Protected live namespace/size changed')
    for folder,names in preflight['remote_protected_sizes'].items():
        remote=pm.partition(pm.sizes(folder,policy),policy)
        require(not remote['unclassified'] and remote['protected']==names,'Protected remote namespace/size changed')
    configs,definitions=previous['config'],previous['definitions']
    require(not set(configs)&set(definitions),'Ambiguous input guard roster')
    require(set(previous['file_guards'])==set(configs)|set(definitions),'Incomplete input guard roster')
    diagnostics=[]
    for path,row in previous['file_guards'].items():
        value=content_guard(path,row,(configs|definitions)[path])
        if value['timestamp_changed']:diagnostics.append(value)
    for path,row in previous['installed'].items():
        value=content_guard(path,row,row['sha256'])
        if value['timestamp_changed']:diagnostics.append(value)
    require(sha(regular(plan['sfse_path']))==plan['sfse_sha256'],'SFSE changed')
    deployed=regular(plan['deployed_dll'])
    require(sha(deployed)==plan['dll_sha256'],'Effective candidate changed')
    require(not [p.name for p in deployed.parent.glob('Sor*.dll') if p!=deployed],'Competing SOR plugin')
    return dict(state='PASS_LIGHTWEIGHT',raw_verified=False,save_content_rehashed=False,
                timestamp_policy=POLICY,timestamp_changes=diagnostics,transient_names=sorted(current['transient']))
