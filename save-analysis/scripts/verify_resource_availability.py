"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline controls/reproducibility check. Reads local probe outputs and
prior owned research receipts; reopens approved saves read-only, cleans decoder
scratch, writes exclusive ignored check receipt. No target/network/Git effects.
Requires research_resource_availability saves run and extra run with old pins.
No expected availability set is inferred from these producer/object controls.
"""
import argparse
import json
from pathlib import Path

from inventory_historical_saves import ROOT, guard, identity
from research_resource_availability import audit, write
from stream_save import decoded_save


def check(run, extra, output):
    guard()
    output.mkdir(parents=True, exist_ok=False)
    inputs = sorted(run.glob('*.json'))+sorted(extra.glob('*.json'))
    paths = [p for p in inputs if 'data' in json.loads(p.read_text(encoding='utf8'))]
    prior = ROOT/'.local-work/extractor-resource/run05/mature-Save52.json'
    roots_path = ROOT/'.local-work/workshop-population-rework/roots03/inventory.json'
    members_path = ROOT/'.local-work/workshop-inventory/final05/mature-Save52.json'
    pins = {str(p): identity(p) for p in paths+[prior, roots_path, members_path]}
    controls = []
    mature = None
    for p in paths:
        v = json.loads(p.read_text(encoding='utf8'))
        source = Path(v['source']['path']); now = identity(source)
        if now['sha256'] != v['source']['sha256']: raise ValueError('SAVE_PIN')
        pins[str(source)] = now
        guard()
        with decoded_save(source, output/'scratch') as (b, m):
            fresh = audit(b)
            if fresh != v['data']: raise ValueError('NONDETERMINISTIC_AUDIT')
            if m['decoded_sha256'] != v['metrics']['decoded_sha256']:
                raise ValueError('DECODED_PIN')
        counts = [r['workshop']['resource_count'] for r in fresh['beacons']]
        if any('gap' in r for r in fresh['beacons']): raise ValueError('CORPUS_BEACON_GAP')
        if v['series'] == 'manual-S0-S7C':
            # Independently recorded actions in manual-save-corpus brief.
            expected = [] if v['label'] in ('S0', 'S0C') else [1] if v['label'].startswith(('S3','S4','S5','S6')) else [0]
            if counts != expected: raise ValueError('ACTION_CONTROL_REGISTRY_MISMATCH')
        if v['label'] in ('Save25','Save26','Save27','Save28'):
            if counts != [0, 0]: raise ValueError('TWO_BEACON_REGISTRY_CONTROL')
        if v['series'] == 'output-link-L0-L2C' and counts != [1]:
            raise ValueError('RELOAD_LINK_REGISTRY_CONTROL')
        if v['label'] == 'Save52': mature = v
        controls.append(dict(series=v['series'], label=v['label'], counts=counts,
                             deterministic=True, decoded_pin=True))
    if mature is None: raise ValueError('MATURE_CONTROL_MISSING')
    ext = json.loads(prior.read_text(encoding='utf8'))['instances']
    root_data = json.loads(roots_path.read_text(encoding='utf8'))
    roots = root_data['combined_roots']
    members = json.loads(members_path.read_text(encoding='utf8'))['instances']
    if len(roots) != 848 or len(ext) != 63: raise ValueError('POSITIVE_CONTROL_DRIFT')
    entries = [dict(owner=b['identity'], resource=g['resource_identity'], **row)
               for b in mature['data']['beacons'] for g in b['workshop']['resource_rows'] for row in g['rows']]
    matches = []
    for x in ext:
        rs = [r for r in entries if r['reference_identities'][0] == x['saved_reference']]
        rt = [r for r in roots if r['instance_identity'] == x['saved_reference']]
        ms = [r for r in members if r['saved_reference'] == x['saved_reference']]
        if (len(rs), len(rt), len(ms)) != (1, 1, 1): raise ValueError('NONUNIQUE_POSITIVE_CONTROL')
        r = rs[0]
        if r['reference_identities'][1] != x['base_identity']: raise ValueError('BASE_JOIN')
        if r['resource'] != x['definition']['associations'][0]['resource_identity']: raise ValueError('RESOURCE_JOIN')
        if not r['owner'] == rt[0]['owner_identity'] == ms[0]['owner_identity']: raise ValueError('OWNER_JOIN')
        matches.append(dict(reference=x['saved_reference'], owner=r['owner'], resource=r['resource'],
                            row_offset=r['offset'], record_offset=x['offset'], base=x['base_identity']))
    if {str(p): identity(Path(p)) for p in pins} != pins: raise ValueError('INPUT_CHANGED')
    result = dict(controls=controls, extractor_matches=matches, root_count=len(roots),
                  registry_rows=len(entries), registry_groups=sum(b['workshop']['resource_count'] for b in mature['data']['beacons']),
                  inputs=pins, availability_equality='NOT_TESTED',
                  availability_false_positives=None, availability_false_negatives=None)
    write(output/'checks.json', result)
    guard()
    return dict(samples=len(controls), roots=len(roots), extractors=len(matches), registry_rows=len(entries))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', type=Path, required=True)
    ap.add_argument('--extra', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    # Receipt output is constrained to ignored research work; input paths explicit.
    out = a.output.resolve()
    if not out.is_relative_to(ROOT/'.local-work/resource-availability'): raise ValueError('OUTPUT_SCOPE')
    print(check(a.run, a.extra, out))
