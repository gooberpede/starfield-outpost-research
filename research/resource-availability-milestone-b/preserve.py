# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only hash audit of inherited protected pins and sealed 070 session.
Stdlib only; writes exclusive local JSON receipt. No game/process/DB effects.
Use --phase before or after. Initial snapshot retains supplied untracked brief.
"""
import argparse, ctypes, hashlib, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/resource-availability-milestone-b'
def sha(p):
    with Path(p).open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def disk():
    result = {}
    for drive in ('C:/', 'D:/'):
        a, b, c = (ctypes.c_ulonglong() for _ in range(3))
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive, ctypes.byref(a), ctypes.byref(b), ctypes.byref(c)):
            raise OSError('disk query failed')
        result[drive] = a.value
        if a.value < 40_000_000_000: raise RuntimeError('DISK_GUARD')
    return result
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--phase', choices=['before','after'], required=True); args = ap.parse_args()
    disks = disk()
    inherited = json.loads((ROOT/'.local-work/continuous-beacon-preview/baseline.json').read_text())
    seal_path = ROOT/'.local-work/continuous-beacon-preview/run-20261014T233433728771Z/seal.json'
    seal = json.loads(seal_path.read_text())
    pins = dict(inherited['protected'])
    pins[str(seal_path)] = sha(seal_path)
    for name, r in seal['files'].items(): pins[str(Path(seal['session'])/name)] = r['sha256']
    results = []
    for p, expected in pins.items():
        actual = sha(p)
        results.append(dict(path=p, expected=expected, sha256=actual, equal=actual==expected))
    git = lambda *a: subprocess.check_output(['git',*a], cwd=ROOT).decode().strip()
    receipt = dict(phase=args.phase, disk=disks, head=git('rev-parse','HEAD'), index_sha256=sha(ROOT/'.git/index'),
                   pins=results, all_equal=all(r['equal'] for r in results), seal_sha256=sha(seal_path))
    if args.phase == 'before':
        files=[]
        for p in git('ls-files','--others','--exclude-standard').splitlines():
            target=BASE/'baseline-tree'/p; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes((ROOT/p).read_bytes())
            files.append(dict(path=str(ROOT/p),sha256=sha(ROOT/p)))
        # Export helper baseline interface.
        (BASE/'baseline.json').write_text(json.dumps(dict(head=receipt['head'],index=dict(sha256=receipt['index_sha256']),files=files),indent=2)+'\n',encoding='utf8')
    else:
        before=json.loads((BASE/'preservation-before.json').read_text())
        assert before['head']==receipt['head'] and before['index_sha256']==receipt['index_sha256']
        assert before['pins']==receipt['pins']
    with (BASE/('preservation-'+args.phase+'.json')).open('x',encoding='utf8') as f: json.dump(receipt,f,indent=2)
    print(json.dumps(dict(phase=args.phase,pins=len(results),all_equal=receipt['all_equal'],disk=disks)))
    assert receipt['all_equal'], 'PROTECTED_INPUT_MISMATCH'
if __name__ == '__main__': main()
