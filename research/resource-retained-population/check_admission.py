# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise future admission checks against real offline metadata, without attachment.

Synthetic approval-shaped dictionaries stay in memory and grant no authority.
Reads a completed preflight/metadata; writes only one fresh local results JSON.
Never calls the collector main, launches a target or emits a real GO receipt.
"""
import copy
import json
from pathlib import Path
import sys
from build import LOCAL,pin
from collect_native import admission_checks


def main():
    preflight,output=(Path(x).resolve() for x in sys.argv[1:]);assert preflight.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    pre=json.loads(preflight.read_text());gate=dict(status='GO',phase='B',source=pre['source'],
        synthetic=True,approval_reference='SYNTHETIC CONTROL ONLY; NO LIVE AUTHORITY',cloud_confirmed=True,used=False,pid=1,
        creation_filetime_100ns=pre['created_filetime_100ns']+1,run_card=pre['run_card'],build_manifest=pre['build_manifest'],
        preflight=dict(path=str(preflight),sha256=pin(preflight)),
        allowed_interventions=['software_int3_14','all_stop_and_peer_suspend','owned_rip_tf_rearm','termination_teardown'],
        cloud_metadata_decision=dict(authorization_reference='SYNTHETIC CONTROL ONLY',scope='D5L_ONE_PROCESS_ONLY',historical_sha256=pre['sync']['historical_remotecache_sha256'],accepted_prospective_sha256=pre['sync']['remotecache_sha256']))
    admission_checks(gate);results=[dict(case='synthetic_exact_metadata',passed=True)]
    def refuse(name,change):
        g=copy.deepcopy(gate);change(g)
        try:admission_checks(g)
        except (AssertionError,KeyError):results.append(dict(case=name,passed=True));return
        raise AssertionError(name)
    refuse('missing_human_reference',lambda g:g.update(approval_reference=''))
    refuse('not_phase_b',lambda g:g.update(phase='A'))
    refuse('wrong_source',lambda g:g.update(source='unrelated'))
    refuse('wrong_card_pin',lambda g:g['run_card'].update(sha256='0'*64))
    refuse('missing_cloud_confirmation',lambda g:g.update(cloud_confirmed=False))
    refuse('preexisting_process',lambda g:g.update(creation_filetime_100ns=pre['created_filetime_100ns']-1))
    refuse('used_admission',lambda g:g.update(used=True))
    refuse('expanded_interventions',lambda g:g['allowed_interventions'].append('forced_reset'))
    if pre['status']=='OFFLINE_CHECKED_CLOUD_HOLD':
        refuse('cloud_mismatch_never_implicit',lambda g:g.pop('cloud_metadata_decision'))
        refuse('wrong_cloud_prospective_pin',lambda g:g['cloud_metadata_decision'].update(accepted_prospective_sha256='0'*64))
    with output.open('x',encoding='utf8') as s:json.dump(dict(synthetic_only=True,no_target_operations=True,cases=results),s,indent=2);s.write('\n')
    print(len(results),'admission controls PASS; no target operations')


if __name__=='__main__':main()
