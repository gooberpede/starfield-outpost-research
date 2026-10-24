# SPDX-License-Identifier: GPL-3.0-or-later
"""Rerun frozen D2/D3 requests and seven D1 native controls without refitting.

Reads immutable bundles/requests/native receipts. Writes fresh ignored outputs
only; isolated inference forbids game/save/native evidence reads. Uses owned
D1 isolation/verification methods and Python stdlib. No target or Git effects.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/resource-standalone'))
import verify


def main():
    out = ROOT / '.local-work/resource-tungsten-repair/regressions01'
    out.mkdir(parents=True, exist_ok=False)
    results = []
    for label, source in [('D2', ROOT / '.local-work/resource-save52'),
                          ('D3', ROOT / '.local-work/resource-save52-d3/revision06')]:
        build, previous = source / 'build-v1', source / 'first-pass-v1'
        dest = out / label
        dest.mkdir()
        for request in sorted(previous.glob('*-request.json')):
            command = [sys.executable, '-I', '-S', '-B', str(ROOT / 'research/resource-standalone/isolate.py'),
                '--code', str(build/'code'), '--corpus', str(build/'normalized.json'), '--request', str(request)]
            run = subprocess.run(command, cwd=dest, capture_output=True)
            (dest / request.name.replace('-request', '-stdout')).write_bytes(run.stdout)
            (dest / request.name.replace('-request', '-audit')).write_bytes(run.stderr)
            assert run.returncode == 0, run.stderr.decode()
            expected = previous / request.name.replace('-request', '-stdout')
            assert json.loads(run.stdout) == json.loads(expected.read_text()), str(request)
            audit = json.loads(run.stderr)
            assert not audit['inference_forbidden'] and audit['denied_probes'] == 8
            results.append(dict(version=label, case=request.stem, output_sha256=verify.pin(dest / expected.name),
                                exact_semantic_equality=True, denied_probes=8))
    verify.save(out / 'roster.json', results)
    verify.run(ROOT / '.local-work/resource-standalone/build03', out / 'seven-controls')
    print(len(results), 'frozen D2/D3 requests; seven controls in both representations PASS')


if __name__ == '__main__':
    main()
