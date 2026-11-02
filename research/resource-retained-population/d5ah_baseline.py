# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze repository bytes and authenticate offline inputs without target changes.

Uses owned D5AE baseline semantics (SOR-P-0002). Reads Git state, repository
text and pinned private inputs; writes fresh ignored D5AH receipts and baseline
copies. Stdlib only. No game, save, database-opening, network or Git mutation.
"""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    if len(sys.argv) > 1 and sys.argv[1] == '--inputs':
        # Preserve the inherited input roster and fail-closed checks verbatim;
        # only the fresh output namespace and governing brief are changed.
        inherited = ROOT / 'research/resource-retained-population/d5ae_baseline.py'
        source = inherited.read_text(encoding='utf8').replace(
            "'.local-work/d5ae'", "'.local-work/d5ah'").replace(
            'CODEX_BRIEF_SOR_RG2_D5AE_GC10_construction_winner_scheduling.md',
            'CODEX_BRIEF_SOR_RG2_D5AH_geometry_persistence_reconstruction.md')
        namespace = {'__file__': str(inherited), '__name__': 'd5ah_input_authentication'}
        exec(compile(source, str(inherited), 'exec'), namespace)
        arguments = sys.argv[:]
        try:
            sys.argv = [arguments[0], arguments[2]]
            namespace['main']()
        finally:
            sys.argv = arguments
        target = ROOT / '.local-work/d5ah' / arguments[2]
        result = json.loads(target.read_bytes())
        result['adaptation'] = dict(wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                    inherited_sha256=hashlib.sha256(inherited.read_bytes()).hexdigest(),
                                    transformed_source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                                    changes='Output root and governing brief basename only')
        target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')
        return
    out = ROOT / '.local-work/d5ah'
    out.mkdir(exist_ok=True)
    target = out / 'baseline.json'
    if target.exists():
        raise FileExistsError(target)
    files = {}
    names = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT)
    for raw in names.split(b'\0'):
        if not raw:
            continue
        name = raw.decode('utf8')
        source = ROOT / name
        if not source.is_file():
            files[name] = {'deleted': True}
            continue
        data = source.read_bytes()
        files[name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        copy = out / 'baseline-tree' / name
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(data)
    git = lambda *args: subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT).decode('utf8')
    result = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  head=git('rev-parse', 'HEAD').strip(), status=git('status', '--short'),
                  index_sha256=hashlib.sha256((ROOT / '.git/index').read_bytes()).hexdigest(),
                  files=files, interpreter=sys.executable)
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')
    print(result['head'], len(files), result['index_sha256'])


if __name__ == '__main__':
    main()
