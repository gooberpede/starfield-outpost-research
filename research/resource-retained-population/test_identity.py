# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify admission identity with a disposable child and synthetic mismatches.

Reads current/child query tokens, runs an installed Python child waiting on its
pipe, writes one exclusive local receipt. Closes that pipe and waits for its
child only. No debugger, Starfield, admission/GO file, elevation or Git mutation.
Run once in the sandbox and once in the approved ordinary-user context.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
from identity import compatible, require_ordinary, snapshot


def main():
    destination = Path(sys.argv[1]).resolve()
    child = subprocess.Popen([sys.executable,'-I','-c','import sys; sys.stdin.read()'],stdin=subprocess.PIPE)
    try:
        caller, target = snapshot(os.getpid()), snapshot(child.pid)
        expected = 'codexsandbox' not in caller['account'].lower() and not caller['elevated']
        try:
            real = require_ordinary(child.pid)
            accepted = True
        except RuntimeError as error:
            real = dict(refusal=str(error))
            accepted = False
        checks = dict(real_context_result=accepted is expected)
        ordinary = dict(sid='SYNTHETIC_SID',account='host\\ordinary',session=1,elevated=False)
        checks['ordinary_predicate'] = compatible(ordinary,ordinary)
        for field, value in (('sid','OTHER_SID'),('session',2),('elevated',True)):
            changed = dict(ordinary,**{field:value})
            checks['refuse_'+field] = not compatible(ordinary,changed)
        sandbox = dict(ordinary,account='host\\CodexSandboxOffline')
        checks['refuse_sandbox'] = not compatible(sandbox,sandbox)
    finally:
        child.stdin.close()
        child.wait(timeout=10)
    result = dict(checks=checks,passed=all(checks.values()),caller=caller,target=target,
                  ordinary_real_accepted=accepted,identity_result=real,child_exit=child.returncode)
    with destination.open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(result)
    assert result['passed'] and child.returncode==0


if __name__ == '__main__':main()
