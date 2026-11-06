# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay authenticated D5U fixed-input models in fresh disposable children.

Reads owned fixture support, the pinned executable and prior D5U receipts.
Copies support into an ignored output, and retains child stdout, stderr and
the complete replay. Original and protected inputs are read-only.
"""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from pathlib import Path
import shutil
import subprocess

import d5at_survey as s


def replay(out):
    s.guard()
    s.require(s.sha(sys.executable) == s.PINNED[Path(sys.executable)], 'Interpreter pin')
    prior = s.ROOT / '.local-work/d5u/native05'
    pins = {row['path']: row['sha256'] for row in s.read_csv(s.DOC / 'd5u-sources.csv')}

    def authenticate(path):
        s.require(s.sha(path) == pins[path.relative_to(s.ROOT).as_posix()], 'D5U evidence drift')

    tool = s.ROOT / 'research/resource-retained-population/d5u_native.py'
    authenticate(tool)
    out.mkdir()
    for name in ('start.py', 'native_probe.py', 'geometry.json', 'initial.json'):
        shutil.copyfile(prior / name, out / name)
    shutil.copytree(prior / 'functions', out / 'functions')
    rows = []
    for ordinal in ('U16', 'U19', 'U20', 'U21', 'U23', 'U26'):
        s.guard()
        model = prior / f'{ordinal}-model.json'
        original = prior / f'{ordinal}-native.json'
        authenticate(model)
        authenticate(original)
        guard = (
            "import os, runpy, sys\n"
            "if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):\n"
            "    raise RuntimeError('Optimization refused')\n"
            "sys.argv = sys.argv[1:]\n"
            "runpy.run_path(sys.argv[0], run_name='__main__')"
        )
        result = subprocess.run(
            [sys.executable, '-E', '-B', '-c', guard, str(tool), original.name, str(model)],
            env=dict(os.environ, D5S_OUTPUT=str(out)), capture_output=True)
        (out / f'{ordinal}-stdout.log').write_bytes(result.stdout)
        (out / f'{ordinal}-stderr.log').write_bytes(result.stderr)
        s.require(result.returncode == 0 and not result.stderr, f'{ordinal} native replay failed')
        new, old = s.load(out / original.name), s.load(original)
        fresh_free = new.pop('free')
        old.pop('free')
        s.require(new == old, f'{ordinal} native replay differs from authenticated primary')
        model_data = s.load(model)
        rows.append(dict(id=ordinal, key=model_data['results'][0]['request']['source'],
                         owner=model_data['results'][0]['request']['owner_key'],
                         variants=[dict(label=r['label'], mask=r['mask'], regions=len(r['full']['regions']),
                                        points=sum(len(p['points']) for p in r['full']['regions']))
                                   for r in model_data['results']],
                         fresh_sha256=s.sha(out / original.name), prior_sha256=s.sha(original), free=fresh_free))
    s.write(out / 'comparison.json', dict(rows=rows, floors=s.guard()))
    print('Six fresh native and independent model comparisons passed')


if __name__ == '__main__':
    out = Path(sys.argv[1]).absolute()
    s.require(out.is_relative_to(s.ROOT / '.local-work') and out == out.resolve()
              and not out.exists(), 'Fresh local output required')
    replay(out)
