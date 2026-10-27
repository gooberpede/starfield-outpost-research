# SPDX-License-Identifier: GPL-3.0-or-later
"""Read three shipped shared PEX members and compare beacon VMAD bindings.

Reads the existing two investigation receipts and installed Misc BA2; writes
one exclusive local JSON. Checks object closure and malformed/branch controls.
No script VM, game, save, configuration or analysis-project execution/mutation.
The owned PEX grammar is deliberately limited; unsupported input fails closed.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from scan import DATA, OUT, ROOT, P, members, pin


def bindings(raw):
    p = 0

    def take(n):
        nonlocal p
        value = raw[p:p+n]
        assert len(value) == n
        p += n
        return value

    def h():
        return int.from_bytes(take(2), 'little')

    def string():
        return take(h()).decode()

    assert h() == 6 and h() == 2
    scripts = {}
    for _ in range(h()):
        name, status, props = string(), take(1), {}
        for _ in range(h()):
            prop = string()
            assert take(2) == b'\x01\x01'
            props[prop] = take(8).hex()
        scripts[name] = dict(status=status.hex(), properties=props)
    assert p == len(raw)
    return scripts


def main(out=OUT):
    out = Path(out).resolve()
    assert out.is_relative_to(ROOT / '.local-work')
    a = json.loads((out / 'installed.json').read_text())
    b = json.loads((out / 'joins.json').read_text())
    normal = next(v for v in b['records'] if v['formid'] == 0x2c60e9)
    expected = bindings(bytes.fromhex(dict(normal['fields'])['VMAD']))
    for key in ('02038ac8', '02038ac9', '02038aca'):
        actual = bindings(bytes.fromhex(dict(a['records'][key]['fields'])['VMAD']))
        assert actual == expected
    archive = DATA / 'Starfield - Misc.ba2'
    before = pin(archive)
    result, rejected, branches = {}, 0, 0
    wanted = {'scripts/outpostbeaconscript.pex', 'scripts/defaultquestchangelocationscript.pex', 'scripts/objectreference.pex'}
    for name, raw in members(archive, lambda n: n.lower() in wanted):
        decoded = P(raw).parse()
        result[name] = dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw), decoded=decoded)
        for bad in (raw[:-1], raw[:16], b'bad!' + raw[4:]):
            try:
                P(bad).parse()
            except (AssertionError, IndexError, ValueError, struct.error, UnicodeDecodeError):
                rejected += 1
            else:
                raise AssertionError('Malformed shared member accepted')
        for obj in decoded['objects']:
            for state, fs in obj['states']:
                for fn, f in fs:
                    for i, op in enumerate(f['ops']):
                        if op['op'] in (20, 21, 22):
                            delta = op['args'][-1]
                            assert delta[0] == 3 and 0 <= i + delta[1] <= len(f['ops'])
                            branches += 1
    assert set(result) == wanted and pin(archive) == before
    with (out / 'shared-checked.json').open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(archive=str(archive), sha256=before, members=result,
                       equal_beacon_bindings=expected, malformed_inputs_rejected=rejected,
                       bounded_branch_targets=branches), f, indent=2)
        f.write('\n')
    print('PASS three equal faction/ordinary bindings; three closed shared members;', rejected, 'malformed rejections;', branches, 'bounded branches')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=OUT)
    main(ap.parse_args().out)
