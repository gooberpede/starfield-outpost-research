# SPDX-License-Identifier: GPL-3.0-or-later
"""Import the live wrapper without main; verify its exact selector and receipts.

Reads pinned Python sources and existing synthetic events, writes one exclusive
ignored JSON result. No target, approval consumption, process attachment, save,
configuration, network, database or Git effects. Python stdlib only.
"""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--qualification', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work')
    spec = importlib.util.spec_from_file_location('d4d_live_wrapper_no_main', HERE / 'collect.py')
    wrapper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wrapper)
    assert Path(wrapper.admission_module.__file__).resolve() == HERE / 'admission.py'
    assert wrapper.Tracker.__module__ == 'd4d_live_admission'
    results = []
    for mode in ('map-cache', 'map-bound', 'map-bound-wrong-source', 'map-bound-wrong-workshop'):
        tracker = wrapper.Tracker()
        events = json.loads((args.qualification / mode / 'events.json').read_text(encoding='utf8'))
        useful = [r['capture'] for r in events if tracker.feed(r)]
        assert bool(useful) == (mode == 'map-bound'), mode
        results.append(dict(mode=mode, useful=useful))
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(dict(passed=True, selector_file=str(wrapper.admission_module.__file__),
            selector_module=wrapper.Tracker.__module__, no_main_executed=True, cases=results), stream, indent=2)
        stream.write('\n')
    print('exact wrapper selector; four receipt regressions PASS')


if __name__ == '__main__':
    main()
