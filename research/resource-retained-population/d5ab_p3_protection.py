# SPDX-License-Identifier: GPL-3.0-or-later
"""Demonstrate current save-policy gates on disposable non-save byte fixtures.

Reads owned save_policy.py and current classification policy; invokes their
snapshot/admission/compare functions only on fresh ignored synthetic inputs.
Writes those inputs, restoration copies and receipts locally. No actual saves,
game/configuration/deployment/process/Git/network action. This is safeguard
parity evidence, never a retail preflight or a valid Starfield save rehearsal.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out=(ROOT/sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT/'.local-work/d5ab')
    out.mkdir(parents=True,exist_ok=False)
    (out/'source.py').write_bytes(Path(__file__).read_bytes())
    method=ROOT/'research/resource-carinae-source-context/save_policy.py'
    spec=importlib.util.spec_from_file_location('p3_policy',method)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    common_path=ROOT/'runtime/session-tools/common.py'
    common_spec=importlib.util.spec_from_file_location('p3_common',common_path)
    common=importlib.util.module_from_spec(common_spec)
    common_spec.loader.exec_module(common)
    policy=copy.deepcopy(module.load_policy())
    rows=[]
    free={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    assert min(free.values())>=40_000_000_000
    names=dict(manual='Save1_ABCD1234M41_000000_20261031010000_1_1_4.sfs',
               quick='Quicksave0_ABCD1234M41_000000_20261031010000_1_1_4.sfs',
               auto='Autosave1_ABCD1234M41_000000_20261031010000_1_1_4.sfs',
               exit='Exitsave0_ABCD1234M41_000000_20261031010000_1_1_4.sfs')
    root=out/'synthetic-active';root.mkdir()
    for kind,name in names.items():
        (root/name).write_bytes(('Disposable '+kind+' bytes, not a game save.').encode())
    # This synthetic policy preserves production grammar but supplies independent
    # explicit research designation data for a disposable nominal autosave.
    policy['designated']={names['auto']:dict(bytes=(root/names['auto']).stat().st_size,
        sha256=sha(root/names['auto']),evidence='P3 disposable research designation control')}
    policy['classified']={}
    original=module.snapshot(root,policy)
    backup=copy.deepcopy(original)

    def check(name,passed,**details):
        rows.append(dict(case=name,passed=bool(passed),**details))
        assert passed,rows[-1]

    initial=module.admission(original,backup,original,policy)
    check('complete-protected-backups',initial['ok'])
    part=module.partition(original,policy)
    check('manual-quick-designated-auto-protected',set(part['protected'])=={names[k] for k in ('manual','quick','auto')})
    for k in ('manual','quick','auto'):
        changed=copy.deepcopy(original);changed[names[k]]['sha256']='0'*64
        check('changed-'+k+'-refused',not module.admission(changed,backup,original,policy)['ok'])
    transient=copy.deepcopy(original);transient.pop(names['exit'])
    check('transient-rotation-diagnostic',module.admission(transient,backup,original,policy)['ok'])
    unknown=copy.deepcopy(original);unknown['unknown.sfs']=dict(bytes=1,sha256='0'*64)
    check('unclassified-addition-refused',not module.admission(unknown,backup,original,policy)['ok'])
    missing=copy.deepcopy(backup);missing.pop(names['auto'])
    check('designated-independent-backup-required',not module.admission(original,missing,original,policy)['ok'])
    altered=copy.deepcopy(backup);altered[names['exit']]['sha256']='0'*64
    check('historical-transient-backup-still-strict',not module.admission(original,altered,original,policy)['ok'])
    restored=out/'synthetic-restoration-copy.sfs'
    shutil.copyfile(root/names['manual'],restored)
    check('restoration-copy-exact',sha(restored)==original[names['manual']]['sha256'])
    (root/names['manual']).write_bytes(b'changed disposable fixture content')
    check('postflight-content-change-detected',not module.compare(original,module.snapshot(root,policy),policy)['ok'])
    visited=[]
    def exact_floor(drive):
        visited.append(drive)
        return 40_000_000_000
    check('both-drive-exact-floor',common.guard(query=exact_floor)=={d:40_000_000_000 for d in ('C:/','D:/')}
          and visited==['C:/','D:/'])
    for low in ('C:/','D:/'):
        try:
            common.guard(query=lambda d:39_999_999_999 if d==low else 40_000_000_000)
        except ValueError:
            rejected=True
        else:
            rejected=False
        check('low-disk-'+low[0]+'-refused',rejected)
    def unavailable(drive):
        raise OSError('Disposable unavailable-query oracle')
    try:
        common.guard(query=unavailable)
    except OSError:
        rejected=True
    else:
        rejected=False
    check('unavailable-disk-query-refused',rejected)
    try:
        common.verify_pins({str(restored):'0'*64})
    except ValueError:
        rejected=True
    else:
        rejected=False
    check('content-pin-mismatch-refused',rejected)
    result=dict(schema='sor-d5ab-p3-disposable-protection/1',passed=all(r['passed'] for r in rows),
                driver_sha256=sha(Path(__file__)),
                scope='Disposable fixture only; no actual save read or B2 preflight.',
                method=str(method),method_sha256=sha(method),
                common_guard_sha256=sha(common_path),
                policy_sha256=sha(module.POLICY_PATH),synthetic_policy=policy,
                original=original,initial_free=free,rows=rows)
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=result['passed'],tests=len(rows),out=str(out))))


if __name__=='__main__':
    main()
