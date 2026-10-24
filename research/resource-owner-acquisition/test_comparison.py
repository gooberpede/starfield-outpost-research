# SPDX-License-Identifier: GPL-3.0-or-later
"""Adversarial offline comparison checks using independently captured fixtures.

Reads D4D events/receipts and D4C frozen inputs; writes only fresh local reports
and a deliberately corrupted copy. Originals remain untouched. Stdlib only;
no target, save, configuration, download, analysis database or Git operations.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

from compare import ROOT, validate, first_divergence


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--qualification', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--d4c-model', type=Path, required=True)
    args = ap.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work')
    args.output.mkdir(exist_ok=False)
    rows = json.loads((args.qualification / 'map-direct/events.json').read_text())
    chain = validate(rows)['chains'][0]
    model = dict(components=copy.deepcopy(chain['components']), selected=chain['selected'], calls=chain['calls'].copy())
    checks = []
    assert first_divergence(chain, model)['domain'] == 'NO_WITNESSED_DIVERGENCE'
    checks.append('complete exact history')
    for domain, mutate in [
        ('component_order', lambda m: m['components'][0].update(identity=[0, 0])),
        ('root', lambda m: m['components'][0].update(root=123)),
        ('slots', lambda m: m['components'][0]['slots'].__setitem__(0, 0)),
        ('selected_root', lambda m: m.update(selected=123)),
        ('generation_call_sequence', lambda m: m['calls'].__setitem__(0, 123)),
        ('component_population', lambda m: m['components'].pop())]:
        altered = copy.deepcopy(model)
        mutate(altered)
        assert first_divergence(chain, altered)['domain'] == domain
        checks.append('first divergence: ' + domain)
    missing = [r for r in rows if r.get('site') != 'ordinary_resource_call']
    assert not validate(missing)['chains']
    checks.append('missing every call rejected against ready-array count')
    missing = [r for r in rows if r.get('site') not in ('ordinary_resource_call', 'candidate_ready')]
    assert not validate(missing)['chains']
    checks.append('missing ready and every call rejected by receipt sequence gap')
    missing = [r for r in rows if r.get('site') != 'map_cleanup']
    assert not validate(missing)['chains']
    checks.append('missing completion boundary rejected')
    changed = copy.deepcopy(rows)
    for row in changed:
        if row.get('site') in ('component_loop', 'map_cleanup', 'map_return'):
            for entry in row['map']['entries']:
                raw = entry['array']['raw']
                entry['array']['raw'] = raw.replace('ec830000', 'ed830000')
    contradiction = validate(changed)['chains'][0]
    assert contradiction['first_operation_divergence']['after_component'] == 1
    assert first_divergence(contradiction, model)['domain'] == 'staging_map_operation'
    assert contradiction['selected_array_reconciliation'] == 'UNKNOWN_FILTERING_OR_ALLOCATION'
    checks.append('witnessed divergent map retained with first before/after boundary')
    combined = copy.deepcopy(model)
    combined['components'][0]['slots'][0] = 0
    assert first_divergence(contradiction, combined)['domain'] == 'slots'
    checks.append('earlier component divergence precedes later operation discrepancy')
    d4c = json.loads(args.d4c_model.read_text())
    result = first_divergence(chain, d4c)
    assert result['domain'] == 'component_order'
    checks.append('existing frozen D4C input accepted without invented native keys')
    spec = importlib.util.spec_from_file_location('d4a_independent', ROOT / 'research/resource-tungsten-acquisition/qualify.py')
    module = importlib.util.module_from_spec(spec)
    # Import resolution is explicitly pinned to the existing owned modules.
    import sys
    sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
    spec.loader.exec_module(module)
    original = args.qualification / 'map-direct/capture-00001.bin'
    corrupted = args.output / 'corrupted.bin'
    data = bytearray(original.read_bytes())
    data[-1] ^= 1
    corrupted.write_bytes(data)
    try:
        module.independent(corrupted)
    except (AssertionError, ValueError):
        checks.append('corruption refused by independent SRO1 digest verifier')
    else:
        raise AssertionError('corrupt receipt accepted')
    (args.output / 'summary.json').write_text(json.dumps(dict(passed=True, checks=checks,
        d4c_synthetic_comparison=result, scope='SYNTHETIC_ONLY_NO_ARCHIMEDES_RESOLUTION'), indent=2) + '\n', encoding='utf8', newline='\n')
    print(len(checks), 'adversarial checks PASS')


if __name__ == '__main__':
    main()
