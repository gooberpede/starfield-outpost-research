# SPDX-License-Identifier: GPL-3.0-or-later
"""Export D5AG task-only and complete review diffs without staging.

SOR-P-0002: adapts the owned D5AF byte-exact review exporter by task namespace,
adds explicit external-HEAD transition verification and inventories D5AG replay
outputs outside the primary receipt directory.
Reads baseline, current text, HEAD/index and local evidence; writes fresh ignored
patches/manifests and standalone apply trees. Stdlib and Git only. No target,
save, analysis, network or Git-state mutation. Inherited checks reject output,
encoding, link, applicability, coverage, scope or index drift. Keep scratch.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    transition_path = ROOT/'.local-work/d5ag/head-transition.json'
    baseline = json.loads((ROOT/'.local-work/d5ag/baseline.json').read_bytes())
    if sys.argv[1:] == ['--pin-head-transition']:
        if transition_path.exists():
            raise FileExistsError(transition_path)
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
        subprocess.run(['git', 'merge-base', '--is-ancestor', baseline['head'], head], cwd=ROOT, check=True)
        names = subprocess.check_output(['git', 'diff', '--name-only', baseline['head'], head], cwd=ROOT).decode().splitlines()
        rows = {}
        for name in names:
            data = subprocess.check_output(['git', 'show', head+':'+name], cwd=ROOT)
            digest = hashlib.sha256(data).hexdigest()
            if digest != baseline['files'][name]['sha256']:
                raise ValueError('External commit differs from task-start bytes: '+name)
            rows[name] = digest
        receipt = dict(original_head=baseline['head'], original_index_sha256=baseline['index_sha256'],
                       head=head, index_sha256=hashlib.sha256((ROOT/'.git/index').read_bytes()).hexdigest(),
                       committed_paths_equal_task_start=rows,
                       reason='Externally created commit; agent performed no Git mutation')
        transition_path.write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf8', newline='\n')
        print(json.dumps(dict(head=head, matching_committed_paths=len(rows))))
        return
    inherited = ROOT / 'research/resource-retained-population/d5af_package.py'
    source = inherited.read_text(encoding='utf8').replace('d5af', 'd5ag').replace('D5AF', 'D5AG')
    transition = json.loads(transition_path.read_bytes())
    if transition['original_head'] != baseline['head']:
        raise ValueError('Head transition baseline mismatch')
    source = source.replace(
        "baseline=json.loads((ROOT/'.local-work/d5ag/baseline.json').read_bytes())",
        "baseline=json.loads((ROOT/'.local-work/d5ag/baseline.json').read_bytes()); "
        "baseline.update(json.loads((ROOT/'.local-work/d5ag/head-transition.json').read_bytes()))")
    source = source.replace(
        "for p in sorted((ROOT/'.local-work/d5ag').rglob('*')):",
        "for p in sorted(list((ROOT/'.local-work/d5ag').rglob('*')) + "
        "list((ROOT/'.local-work/d5ac/d5ag01').rglob('*')) + "
        "list((ROOT/'.local-work/d5ag-specialist').rglob('*'))):")
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'd5ag_package_adapter'}
    exec(compile(source, str(inherited), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
