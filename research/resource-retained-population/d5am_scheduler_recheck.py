# SPDX-License-Identifier: GPL-3.0-or-later
"""Re-execute the owned D5W native queue contrast under pinned D5AM authority.

Reads the exact owned method and inherited authenticated inputs. Runs it in a
disposable Python child with -E -B; writes fresh D5AM-local logs/receipts only.
The child maps original instructions with declared allocation/TLS substitutes.
No game, controller, deployment, save, database, network or Git write occurs.
Child exit releases fixture pages. SOR-P-0002 covers verbatim method reuse.
This tests queue rules, not normal retail frequencies. Stop on source, native
oracle, subprocess or disk failure; retain diagnostics and all original inputs.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import re
import subprocess
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
METHOD = ROOT / 'research/resource-retained-population/d5w_native.py'
METHOD_PIN = '5d784e145f44b3931dd5a6795bb60030f32454ea5e5112be50979b7c88742174'


def main():
    if len(sys.argv) != 2 or not re.fullmatch('[a-z0-9-]+', sys.argv[1]):
        raise ValueError('Fresh bounded label required')
    out = ROOT / '.local-work/d5am' / sys.argv[1]
    if any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('Reparse output path')
    free = guard()
    if sha(METHOD) != METHOD_PIN:
        raise ValueError('Owned method differs from starting source pin')
    out.mkdir(parents=True, exist_ok=False)
    command = [sys.executable, '-E', '-B', str(METHOD), str(out / 'native-queue.json')]
    result = subprocess.run(command, capture_output=True)
    (out / 'stdout.txt').write_bytes(result.stdout)
    (out / 'stderr.txt').write_bytes(result.stderr)
    if result.returncode:
        raise RuntimeError('Native fixture failed; retained diagnostic at ' + str(out))
    native = json.loads((out / 'native-queue.json').read_bytes())
    if len(native['runs']) != 12 or native['game_process'] is not False or sha(METHOD) != METHOD_PIN:
        raise ValueError('Native contract/source changed')
    receipt = dict(schema='sor-d5am-scheduler-recheck/1', command=command,
                   method_sha256=METHOD_PIN, wrapper_sha256=sha(__file__),
                   interpreter_sha256=sha(sys.executable), exit=result.returncode,
                   native_receipt_sha256=sha(out / 'native-queue.json'),
                   runs=[{k: v for k, v in row.items() if k != 'claims'} for row in native['runs']],
                   initial_free=free, final_free=guard(),
                   scope='Original queue instructions with explicit allocation/TLS/context substitutions; no retail distribution.')
    with (out / 'qualification.json').open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(result='PASS', runs=12, out=str(out))))


if __name__ == '__main__':
    main()
