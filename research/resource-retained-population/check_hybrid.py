# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate D5N primary receipts and run supplemental offline controls.

Reads completed disposable qualification; writes a fresh ignored check folder
and deliberately damaged evidence copies there. Originals stay intact. Uses
owned independent SRO1 decoder, receipt binder and adversarial tests. No target,
network, installation, protected input, analysis or Git effects.
"""
import json
from pathlib import Path
import shutil
import sys
import check_native
import hybrid
import review_capture
from build import LOCAL, pin


def main():
    folder, output = (Path(x).resolve() for x in sys.argv[1:])
    assert folder.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    output.mkdir(exist_ok=False)
    review_capture.reduce = hybrid.reducer().reduce
    reports = {}
    for case in sorted(folder.iterdir()):
        if not case.is_dir() or not (case/'events.jsonl').exists():
            continue
        report = review_capture.checked(case, True)
        rows = [json.loads(x) for x in (case/'events.jsonl').read_text().splitlines()]
        control = [json.loads(x) for x in (case/'control.jsonl').read_text().splitlines()]
        assert not any(r['action']=='PATCH_INTENT' and r['site']==10 for r in control)
        hardware = [r for r in rows if r.get('site')==10 and r['kind']=='SAMPLE']
        assert all(hybrid.hybrid_context(r, next(x for x in rows if x['kind']=='SESSION')) for r in hardware)
        reports[case.name] = dict(receipts=report['receipts'], chains=len(report['reduction']['chains']),
            hardware_samples=len(hardware), journal_sha256=report['journal_sha256'])
        assert report['reduction']==json.loads((case/'reduction.json').read_text())
    assert reports['crash']['chains'] and not reports['early-crash']['chains']
    # These copies test complete journal/receipt/ACK binding rather than merely
    # treating a successfully decoded prefix as a complete acquisition.
    refusals = {}
    for fault in ('missing-ack','changed-ack','missing-receipt','corrupt-receipt'):
        target = output/fault
        shutil.copytree(folder/'basic', target)
        receipt = sorted(target.glob('capture-*.bin'))[-1]
        ack = receipt.with_suffix('.ack.json')
        if fault=='missing-ack':
            ack.unlink()
        elif fault=='changed-ack':
            ack.write_text('{}\n', encoding='utf8')
        elif fault=='missing-receipt':
            receipt.unlink()
        else:
            raw=bytearray(receipt.read_bytes());raw[len(raw)//2]^=1;receipt.write_bytes(raw)
        try:
            review_capture.checked(target, True)
        except (ValueError, KeyError, AssertionError, OSError, RuntimeError, UnicodeError):
            refusals[fault]=True
        else:
            raise AssertionError(fault)
    check_native.reduce = hybrid.reducer().reduce
    saved=sys.argv
    try:
        sys.argv=['check_native.py', str(folder), str(output/'adversarial')]
        check_native.main()
    finally:
        sys.argv=saved
    result=dict(cases=reports, receipt_refusals=refusals,
        post_crash_independent_authentication=True, historical_reducer_changed=False,
        inputs={str(p):pin(p) for p in (hybrid.SRC/'hybrid.py', hybrid.SRC/'native_reduce.py')})
    (output/'checks.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf8', newline='\n')
    print(len(reports), 'cases independently authenticated; four receipt refusals; crash ordering distinguished')


if __name__ == '__main__':
    main()
