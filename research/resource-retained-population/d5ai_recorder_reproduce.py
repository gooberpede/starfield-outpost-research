# SPDX-License-Identifier: GPL-3.0-or-later
"""Recompile an exact retained recipe into a fresh offline output directory.

Reads the selected candidate sources at their retained original paths, generated
identity headers and approved installed toolchain. Reuses exact source paths to
test byte reproducibility separately from source-tree relocation. Writes fresh
ignored objects, logs, DLL, host and one native typed-ending session. Never runs
the game, deploys a DLL, contacts a process, changes saves or uses the network.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

from d5ae_baseline import guard

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    guard()
    out.mkdir(exist_ok=False)
    native = next((build / 'sources').rglob('d5ai_lifetime.h')).parent
    # Recover the actual source locations from the immutable derivation receipt.
    source = ROOT / '.local-work/d5ai-recorder' / ('candidate-' + build.name) / 'runtime/construction-winner'
    for path in native.iterdir():
        if path.is_file() and sha(path) != sha(source / path.name):
            raise ValueError('Retained source correspondence failure: ' + path.name)
    paths = [p for p in source.iterdir() if p.is_file()]
    paths += [build / name for name in ('identity.generated.h', 'emitters.generated.h', 'build.cmd', 'emitter-input.bin')]
    inputs = {str(p): sha(p) for p in paths}
    (out / 'build.cmd').write_bytes((build / 'build.cmd').read_bytes())
    (out / 'emitter-input.bin').write_bytes((build / 'emitter-input.bin').read_bytes())
    compiled = subprocess.run(['cmd', '/d', '/c', str(out / 'build.cmd')], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(compiled.stdout + compiled.stderr)
    result = dict(schema='sor-d5ai-exact-reproduction/1', inputs=inputs, compilation=compiled.returncode,
                  source_paths_reused=True, source_relocation_tested=False, free=guard())
    if compiled.returncode == 0:
        result['dll_sha256'] = sha(out / 'SorConstructionWinner.dll')
        result['original_dll_sha256'] = sha(build / 'SorConstructionWinner.dll')
        result['byte_identical'] = result['dll_sha256'] == result['original_dll_sha256']
        case = 'd5ai-life-external-collection'
        run = subprocess.run([str(out / 'sor-d5x-fixture.exe'), str(out / 'SorConstructionWinner.dll'), str(out / case), case], cwd=out, capture_output=True)
        (out / 'native.stdout').write_bytes(run.stdout)
        (out / 'native.stderr').write_bytes(run.stderr)
        result['native_exit'] = run.returncode
    result['inputs_unchanged'] = all(sha(path) == digest for path, digest in inputs.items())
    result['status'] = 'PASS' if result.get('byte_identical') and result.get('native_exit') == 0 and result['inputs_unchanged'] else 'FAIL'
    (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'inputs'}))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
