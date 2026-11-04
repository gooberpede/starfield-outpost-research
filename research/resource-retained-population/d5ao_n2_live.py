# SPDX-License-Identifier: GPL-3.0-or-later
"""Bind the approved N2 episode to a fresh prospective source-locked plan.

SOR-P-0002: source-informed D5AO readiness/N1 bundle methods. Reads unchanged
approved proposal, current authorization, new forecast and optional actual
independent review receipt. Writes exclusive local plan/lock/manifest only.
No game, deployment, live worker command, protected-file write, Git or network
operation. This tool does not grant launch GO or invent independent review.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import copy
import json
from pathlib import Path
import re
import d5ao_n2_operations as operations
from d5am_lock_qualify import ROOT,guard,sha

LOCAL=ROOT/'.local-work/d5ao/n2-live01'
DOC=ROOT/'docs/experiments/resource-retained-population'
BRIEF=ROOT/'docs/implementation-briefs/CODEX_AMENDMENT_SOR_D5AO_N2_live_2026-11-04.md'
OLD=ROOT/'.local-work/d5ao/n2-proposal-final01/n2-plan-proposal.json'


def require(value,message):
    if not value:raise ValueError(message)


def fresh(path,value):
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('label')
    p.add_argument('--review',type=Path);a=p.parse_args()
    require(re.fullmatch('[a-z0-9-]+',a.label),'Fresh simple label required')
    free=guard();out=LOCAL/a.label;require(not out.exists(),'Exclusive output required')
    require(not any(x.is_symlink() or x.is_junction() for x in (out,*out.parents)),'Reparse path refused')
    require(sha(OLD)=='3ffcf1cbc8248b42920ec5a35eda6ac52d6ca68841071e219694b5ff124f9aad','Approved proposal changed')
    plan=copy.deepcopy(json.loads(OLD.read_bytes()));operations.verify_plan(plan)
    require(sha(plan['deployed_dll'])==plan['dll_sha256'],'Effective deployed candidate mismatch')
    prediction=DOC/'d5ao-n2-prediction-text-v1.md';measurement=DOC/'d5ao-n2-measurement-adjudication.md'
    decision_path=LOCAL/'prospective-decision.json';decision=json.loads(decision_path.read_bytes())
    require(decision['prediction_sha256']==sha(prediction) and decision['authorization_sha256']==sha(BRIEF),'Prospective authority/forecast mismatch')
    for path,digest in plan['package_pins'].items():require(sha(path)==digest,'Frozen prior input changed: '+path)
    plan.update(state='N2_PREDICTION_REVIEW_PENDING',prediction_path=str(prediction),prediction_sha256=sha(prediction),
        measurement_path=str(measurement),measurement_sha256=sha(measurement),
        authorization_path=str(BRIEF),authorization_sha256=sha(BRIEF),
        prospective_trial_decision=dict(state='RECORDED_PROSPECTIVE_MAINTAINER_DECISION',trial='N2',
            prediction_mode='NEW_PROSPECTIVE_FORECAST',sha256=sha(decision_path),prediction_sha256=sha(prediction)),
        prediction_decision='New prospective PRED-03 v1 for explicitly approved N2; N0/N1 forecasts remain consumed historical INCONCLUSIVE.')
    extra=[BRIEF,prediction,measurement,decision_path,Path(__file__).resolve(),LOCAL/'prediction-controls02.json']
    extra += [Path(__file__).with_name(n) for n in ('d5ao_n2_prediction_oracle.py','d5ao_n2_prediction_controls.py','d5ao_n2_delivery.py')]
    for path in extra:plan['package_pins'][str(path.resolve())]=sha(path)
    if a.review:
        review=a.review.resolve();value=json.loads(review.read_bytes())
        require(review.is_relative_to(LOCAL) and value['verdict']=='ACCEPT_N2_TECHNICAL_READINESS','Actual local independent readiness receipt required')
        for key in ('prediction_sha256','run_card_sha256','dll_sha256'):
            require(value[key]==plan[key],'Reviewed binding mismatch: '+key)
        require(value['prospective_trial_decision_sha256']==sha(decision_path),'Reviewed prospective decision mismatch')
        expected=operations.required_sources()|{Path(x).resolve() for x in plan['package_pins']}
        require(value['sources']=={str(x):sha(x) for x in sorted(expected)},'Review must bind exact entire prospective source closure')
        actual=value['actual_return_path'];require(sha(actual)==value['actual_return_sha256'],'Independent return changed')
        plan['package_pins'][str(review)]=sha(review);plan['package_pins'][str(Path(actual).resolve())]=sha(actual)
        plan['review']=dict(state='INDEPENDENTLY_REVIEWED_N2_TECHNICAL_ACCEPT',scope='D5AO_N2_0.9.3_READINESS',
            receipt_path=str(review),receipt_sha256=sha(review),prediction_sha256=sha(prediction),
            run_card_sha256=plan['run_card_sha256'],prospective_trial_decision_sha256=sha(decision_path))
        plan['state']='N2_REVIEWED_REQUIRES_FRESH_PREFLIGHT_AND_PROCESS_BINDING'
    paths=operations.required_sources()|{Path(x).resolve() for x in plan['package_pins']}
    lock=dict(schema=operations.POLICY,interpreter=sys.executable,interpreter_sha256=sha(sys.executable),
        dll_sha256=plan['dll_sha256'],sources={str(x):sha(x) for x in sorted(paths)})
    out.mkdir();lockpath=out/'d5ao-n2-source-lock.json';fresh(lockpath,lock)
    plan.update(d5ao_n2_source_lock=str(lockpath),d5ao_n2_source_lock_sha256=sha(lockpath))
    operations.verify_plan(plan);planpath=out/'n2-plan.json';fresh(planpath,plan)
    fresh(out/'manifest.json',dict(schema='sor-d5ao-n2-live-binding/1',plan=str(planpath),plan_sha256=sha(planpath),
        source_lock_sha256=sha(lockpath),source_count=len(paths),launch_go=False,initial_free=free,final_free=guard()))
    print(json.dumps(dict(plan=str(planpath),sha256=sha(planpath),sources=len(paths),launch_go=False)))


if __name__=='__main__':main()
