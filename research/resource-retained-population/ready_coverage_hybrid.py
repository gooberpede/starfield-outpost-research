# SPDX-License-Identifier: GPL-3.0-or-later
"""D5O qualification seal and enforced offline/future admission proof gate.

Check reads completed captures, independently authenticates receipts, and writes
fresh ignored checks/proof plus damaged disposable evidence copies. Prepare
verifies that proof and retains full archive/save protection. Collect delegates
all existing explicit approval/account/session/intervention gates and can attach
and terminate only the separately admitted target. Never collect in Phase A.
No launch, download, installation, original, analysis or Git writes.
"""
import argparse
import json
from pathlib import Path
import sys
import check_coverage_hybrid
import operate_coverage_hybrid
from build import ROOT, LOCAL, SRC, pin
from preservation_native import verify_build_files
from qualify import transport, decoder, old_qualification


def inventory(folder):
    return {str(p.resolve()):dict(bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns,
        sha256=pin(p)) for p in sorted(folder.rglob('*')) if p.is_file()}


def proof_check(path, build, qualification, full):
    proof = json.loads(path.read_text(encoding='utf8'))
    assert proof['schema']=='sor-d5o-qualification-proof/1' and proof['passed'] is True
    assert proof['build_manifest']==dict(path=str(build/'build.json'),sha256=pin(build/'build.json'))
    assert Path(proof['qualification'])==qualification
    assert all(pin(name)==value for name,value in proof['methods'].items())
    assert all(pin(name)==value for name,value in proof['checks'].items())
    actual_names = {str(p.resolve()) for p in qualification.rglob('*') if p.is_file()}
    assert actual_names==set(proof['inputs'])
    for name, expected in proof['inputs'].items():
        p = Path(name);st = p.stat()
        assert (st.st_size,st.st_mtime_ns)==(expected['bytes'],expected['mtime_ns'])
        if full: assert pin(p)==expected['sha256']
    return dict(path=str(path),sha256=pin(path))


def check(build, folder, output):
    build_pin = pin(build/'build.json')
    manifest = json.loads((build/'build.json').read_text())
    assert manifest['exit_code']==0 and verify_build_files(manifest)=={}
    inputs = inventory(folder)
    method_paths = [SRC/name for name in (
        'ready_coverage_hybrid.py','check_coverage_hybrid.py','qualify_coverage_hybrid.py',
        'operate_coverage_hybrid.py','hybrid.py','native_reduce.py','review_capture.py')]
    method_paths += [Path(m.__file__).resolve() for m in (transport,decoder,old_qualification)]
    methods = {str(p):pin(p) for p in method_paths}
    results = json.loads((folder/'results.json').read_text())
    assert all(r['build_sha256']==pin(build/'build.json') for r in results)
    saved = sys.argv
    try:
        sys.argv = ['check_coverage_hybrid.py',str(folder),str(output)]
        check_coverage_hybrid.main()
    finally:
        sys.argv = saved
    race = folder/'coverage-exit-race'
    control = [json.loads(s) for s in (race/'control.jsonl').read_text().splitlines()]
    events = [json.loads(s) for s in (race/'events.jsonl').read_text().splitlines()]
    denied = [r for r in control if r['action']=='PEER_SUSPEND_RESULT' and r['error']==5]
    assert len({r['debug_event_sequence'] for r in denied})==len(denied)
    deferred = [r for r in events if r['kind']=='DEFERRED_TRAP']
    assert len(deferred)==len(denied) and [r['tid'] for r in deferred]==[r['tid'] for r in denied]
    # Event/control journals are separate streams. Count and owner order bind
    # these deferrals; DEFERRED_TRAP itself has no serialized debug-event ID.
    checks = {str(p.resolve()):pin(p) for p in output.rglob('*.json')}
    assert inventory(folder)==inputs
    assert all(pin(name)==value for name,value in methods.items())
    assert pin(build/'build.json')==build_pin and verify_build_files(manifest)=={}
    proof = dict(schema='sor-d5o-qualification-proof/1',passed=True,
        build_manifest=dict(path=str(build/'build.json'),sha256=pin(build/'build.json')),
        qualification=str(folder),inputs=inputs,methods=methods,checks=checks,
        deferred_count=len(deferred),deferred_owner_order=True)
    target = output/'qualification-proof.json'
    with target.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(proof,stream,indent=2);stream.write('\n')
    proof_check(target,build,folder,True)
    print('Sealed complete qualification proof:',target)


def prepare(args):
    binding = proof_check(args.proof,args.build,args.qualification,True)
    scope = operate_coverage_hybrid.module('prepare_native')
    original_write = scope['write']
    def write(path, value):
        if path.name=='preflight.json':
            assert proof_check(args.proof,args.build,args.qualification,False)==binding
            value['d5o_qualification'] = binding
        original_write(path,value)
    scope['write'] = write
    sys.argv = ['prepare_native.py','--build',str(args.build),'--qualification',str(args.qualification),
                '--sites',str(args.sites),'--name',args.name]
    return scope['main']()


def collection_scope():
    scope = operate_coverage_hybrid.module('collect_native')
    original = scope['admission_checks']
    def admission(gate):
        pre = original(gate)
        bound = pre['d5o_qualification'];path = Path(bound['path'])
        assert pin(path)==bound['sha256']
        build = Path(pre['build_manifest']['path']).parent
        qualification = Path(pre['qualification']['path']).parent
        proof_check(path,build,qualification,False)
        return pre
    scope['admission_checks'] = admission
    return scope


def main():
    command = sys.argv.pop(1)
    if command=='collect':
        return collection_scope()['main']()
    p = argparse.ArgumentParser(description=__doc__)
    if command=='check':
        for name in ('build','qualification','output'):p.add_argument(name,type=Path)
        args = p.parse_args()
        args.build,args.qualification,args.output = (x.resolve() for x in (args.build,args.qualification,args.output))
        assert all(x.is_relative_to(LOCAL) for x in (args.build,args.qualification,args.output))
        return check(args.build,args.qualification,args.output)
    assert command=='prepare'
    for name in ('proof','build','qualification','sites'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--name',required=True);args=p.parse_args()
    for name in ('proof','build','qualification','sites'):
        value=getattr(args,name).resolve();assert value.is_relative_to(LOCAL);setattr(args,name,value)
    return prepare(args)


if __name__=='__main__':
    raise SystemExit(main())
