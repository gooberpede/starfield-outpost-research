# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze D5AH identities without duplicating the entire tracked repository.

Reads Git inventory and repository files; writes one exclusive ignored receipt.
Stdlib/Git only. No target, save, analysis or Git mutation. The original baseline
copy helper stalled; this independent hash-only recovery preserves its scratch.
Task-owned new paths are distinguished from the supplied brief. Required old
bytes for tracked changes remain in HEAD, since initial status had no edits.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

from d5ae_baseline import guard

ROOT = Path(__file__).resolve().parents[2]


def main():
    guard()
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    def git(*args):
        return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT, env=env)
    head = git('rev-parse', 'HEAD').decode().strip()
    if head != '8df2052136420f3b61c30b7abe427eb83d89e4b1':
        raise ValueError('Original HEAD changed')
    if git('diff', 'HEAD', '--name-only').strip():
        raise ValueError('Tracked edits precede recovery snapshot')
    names = git('ls-files', '-z', '--cached', '--others', '--exclude-standard').decode().split('\0')[:-1]
    files = {}
    for name in names:
        data = (ROOT / name).read_bytes()
        files[name] = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    result = dict(head=head, index_sha256=hashlib.sha256((ROOT / '.git/index').read_bytes()).hexdigest(),
                  utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), files=files,
                  status=git('status', '--short').decode(),
                  initial_status='Only the supplied untracked D5AH brief; captured in initial tool result',
                  recovery='Hash-only snapshot; no reconstructed early timestamp; task paths are attributable new files')
    out = ROOT / '.local-work/d5ah/snapshot01.json'
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(head, len(files), result['index_sha256'])


if __name__ == '__main__':
    main()
