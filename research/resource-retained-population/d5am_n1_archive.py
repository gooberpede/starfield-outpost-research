# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AM source-locked entry to owned lossless session archive (SOR-P-0002).

Reads pinned plan/roots/seal/closed evidence; writes only exclusive D5AM-local
seal/archive/receipts outside sealed roots. No deletion, deployment, originals,
game, process or network actions. Does not grant a new trial or publication.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import importlib.util
from pathlib import Path
import re


def _session_namespace(session,live):
    """Production namespace predicate; no fixture switch is exposed by the CLI."""
    from d5ai_episode import require
    require(session.parent==live and re.fullmatch('session-[0-9a-f]{64}',session.name) is not None,
            'Postflight is outside the D5AM session namespace')


def association(plan,plan_hash,post,roots):
    """Bind this archive to one N1 plan/postflight; no science promotion."""
    import d5am_n1_stop as trusted
    from d5ai_episode import require
    require(plan.get('schema')==trusted.SCHEMA and plan.get('trial')=='N1' and
            Path(plan['live_root']).resolve()==trusted.LIVE,'Exact D5AM N1 plan namespace required')
    require(post.get('schema')=='sor-d5am-n1-postflight/1' and post.get('trial')=='N1' and
            post.get('plan_sha256')==plan_hash,'Postflight belongs to another plan/trial')
    session=Path(post['session']).resolve()
    _session_namespace(session,trusted.LIVE)
    raw=[Path(row['path']).resolve() for row in roots.values() if row['kind']=='raw-capture']
    require(raw==[session],'Exactly the bound N1 raw session is required')
    return dict(schema='sor-d5am-n1-archive-binding/1',trial='N1',plan_sha256=plan_hash,session=str(session))

def main():
    import d5am_n1_operations as operations
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('seal','create','verify'))
    p.add_argument('--plan',type=Path,required=True);p.add_argument('--plan-sha256',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--archive',type=Path)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--sha256',required=True)
    p.add_argument('--postflight',type=Path);p.add_argument('--postflight-sha256')
    p.add_argument('--partial-reason');p.add_argument('--archive-sha256')
    a=p.parse_args()
    plan=operations.original.pinned_json(a.plan,a.plan_sha256);operations.source_pins(plan)
    for path in (a.out,a.archive):
        if path is None:continue
        operations.require(path.resolve().is_relative_to(operations.ROOT/'.local-work/d5am'),'Fresh D5AM archive output required')
        operations.require(not any(p.is_symlink() or p.is_junction() for p in (path.absolute(),*path.absolute().parents)),
                           'No reparse archive output')
    path=operations.ROOT/'runtime/session-tools/archive.py';sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location('d5am_owned_archive',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    operations.require(not a.out.exists(),'Fresh archive receipt required')
    value=module.read(a.input,a.sha256);roots=value if a.action=='seal' else value['roots']
    module.outside(a.out,roots)
    if a.action=='seal':
        operations.require(a.postflight is not None and a.postflight_sha256 is not None,'Pinned N1 postflight required')
        post=module.read(a.postflight,a.postflight_sha256)
        binding=association(plan,a.plan_sha256,post,roots)
        result=module.seal(roots,a.postflight,a.postflight_sha256,a.partial_reason)
        binding['postflight_path']=str(a.postflight.resolve());result['d5am']=binding
    else:
        binding=value.get('d5am',{})
        operations.require(binding.get('schema')=='sor-d5am-n1-archive-binding/1','D5AM-bound seal required')
        post=module.read(Path(binding['postflight_path']),value['postflight_sha256'])
        expected=association(plan,a.plan_sha256,post,roots)
        operations.require({k:binding.get(k) for k in expected}==expected,'Seal belongs to another D5AM plan/session')
        if a.action=='create':
            operations.require(a.archive is not None,'Fresh archive path required')
            result=module.create(a.input,a.sha256,a.archive)
        else:
            operations.require(a.archive is not None and a.archive_sha256 is not None,'Exact archive pin required')
            result=module.verify(a.archive,value,a.archive_sha256)
    module.fresh(a.out,result)
    return 0

if __name__=='__main__':raise SystemExit(main())
