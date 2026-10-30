# SPDX-License-Identifier: GPL-3.0-or-later
"""Test incremental native queue claims in a disposable process.

Conceptually extends the maintainer-owned D5S native_dispatch.py setup, loaded
verbatim only up to its run loop. Exact source hashes are required. Reads the
pinned EXE, original function metadata and registration receipt; writes one
fresh ignored receipt. The inherited setup maps original instructions locally
and substitutes successful allocation/TLS fixtures. No game, attachment, save,
database, installed-file, network or Git mutation. See the D5W ledger plan.
"""
from pathlib import Path
import hashlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '.local-work/d5s/native_dispatch.py'
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert os.name == 'nt'
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / '.local-work') and not output.exists()
    ledger = json.loads((ROOT / '.local-work/d5w/inherited-index.json').read_text())
    methods = [SOURCE, SOURCE.with_name('native_probe.py'), SOURCE.with_name('start.py')]
    for path in methods:
        key = str(path.relative_to(ROOT)).replace('\\', '/')
        expected = next(h for n, h in ledger['paths'].items() if n.replace('\\', '/') == key)
        assert sha(path) == expected, key
    # __file__ and import search intentionally refer to the preserved owned setup.
    sys.path.insert(0, str(SOURCE.parent))
    namespace = {'__file__': str(SOURCE), '__name__': 'd5w_disposable_fixture'}
    prefix = SOURCE.read_text(encoding='utf8').split('runs=[]', 1)[0]
    exec(compile(prefix, str(SOURCE) + ':setup-only', 'exec'), namespace)
    C, k = namespace['C'], namespace['k']
    order = namespace['reg']['density_order']
    count = len(order)
    runs = []
    for route in ('owner', 'peer'):
        for batch in (1, 100, 420, 600, 875, count):
            pool, owner = namespace['setup']()
            assert k.TlsSetValue(namespace['tls'], owner)
            worker = owner if route == 'owner' else owner + 0xc0
            holder = C.c_uint64()
            claims = []
            for low in range(0, count, batch):
                high = min(low + batch, count)
                for i in range(low, high):
                    payload = (C.c_uint64 * 2)(i + 0x10000, 0x20000)
                    namespace['dispatch'](pool, C.addressof(payload))
                for _ in range(low, high):
                    namespace['pop'](pool, C.byref(holder), worker, 0, 0)
                    assert holder.value
                    assert C.c_uint64.from_address(holder.value + 8).value == 0x1427ec2e0
                    claims.append(C.c_uint64.from_address(holder.value + 16).value - 0x10000)
            assert sorted(claims) == list(range(count))
            index = next(i for i in claims if all(-2 <= v < 12 for v in order[i]))
            runs.append(dict(route=route, activation_batch=batch, first_index=index,
                             first_query=order[index], claims=claims, contexts=5))
    assert k.TlsSetValue(namespace['tls'], None) and k.TlsFree(namespace['tls'])
    assert [r['first_query'] for r in runs if r['activation_batch'] == 1] == [[-2, 11]] * 2
    assert [r['first_query'] for r in runs if r['activation_batch'] == count] == [[10, 11], [-2, -2]]
    receipt = dict(schema='sor-d5w-native-claims/1', game_process=False,
                   scope='Queue claims only; fixed ready activation batches, not full engine execution or timing',
                   substitutions='Successful allocation, local TLS, five empty contexts, no semaphore waiters; density callbacks are tokens',
                   methods={str(p.relative_to(ROOT)): sha(p) for p in methods},
                   code_sha256=sha(__file__), functions=namespace['pins'],
                   executable_sha256=namespace['sha'](namespace['exe']),
                   registration_sha256=sha(SOURCE.with_name('registration.json')),
                   free=namespace['free'](), runs=runs)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in r.items() if k != 'claims'} for r in runs], indent=2))


if __name__ == '__main__':
    main()
