# SPDX-License-Identifier: GPL-3.0-or-later
"""D4B diagnostic replay v1: actual calls, frozen source/key/geometry semantics.

Reads verified D4A receipts and frozen D3 corpus/request. Writes fresh ignored
derivatives. This is an explicitly receipt-informed conditional experiment, not
a corrected blind corpus builder or a historical generation-epoch assertion.
No seed, source, family order, probability, saved input or frozen output edits.
"""
import copy
import argparse
import json
from pathlib import Path
import struct
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
                ('resource-standalone', 'resource-geometry', 'resource-pattern-selection')]
import predictor_d3 as predictor
import verify

OUT = ROOT / '.local-work/resource-tungsten-repair/replay01'


def write(name, value):
    with (OUT / name).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    OUT = parser.parse_args().output.resolve()
    assert OUT.is_relative_to(ROOT / '.local-work')
    OUT.mkdir(parents=True, exist_ok=False)
    base = ROOT / '.local-work/resource-tungsten-acquisition/retail-attempt01'
    rows = [json.loads(line) for line in (base / 'events.jsonl').read_text().splitlines()]
    samples = [r for r in rows if r['kind'] == 'SAMPLE']
    accepted = [r for r in samples if r.get('decision') == 'ACCEPT']
    corpus = ROOT / '.local-work/resource-save52-d3/build-v6/normalized.json'
    frozen = ROOT / '.local-work/resource-save52-d3/revision06/first-pass-v1/D2-81a75b-stdout.json'
    envelope, previous = json.loads(corpus.read_text()), json.loads(frozen.read_text())
    observed, bindings = {}, []
    for accept in accepted:
        entries = [r for r in samples if r['site'] == 'generation_entry' and r['source']['address'] == accept['source_key']]
        assert len(entries) == 1
        entry = entries[0]
        assert bytes.fromhex(entry['source']['raw']) == bytes.fromhex(accept['source_context']['raw_source'])
        calls = [r for r in samples if r['site'] == 'ordinary_resource_call' and
                 all(r[k] == entry[k] for k in ('tid', 'thread_lifetime', 'invocation_token'))]
        raw = bytes.fromhex(entry['source']['raw'])
        ax, ay = struct.unpack_from('<2i', raw, 0x10)
        # Current descriptor frame was independently derived by D4A, and equals
        # the unchanged request descriptor; no geometry alignment is performed.
        ox, oy = previous['request']['descriptor']
        source = f'0:{ox+ax}:{oy+ay}:{struct.unpack_from("<I",raw)[0]:08x}'
        resources = []
        for row in calls:
            ires = bytes.fromhex(row['ires']['raw'])
            fid = struct.unpack_from('<I', ires, 0x28)[0]
            rarity = ires[0x110]
            dnam = bytes.fromhex(row['selected_dnam']['raw'])
            block = list(struct.unpack_from('<8f', dnam, 40*(rarity+7))) + [0,0]
            weight = struct.unpack('<f', struct.pack('<I', row['effective_weight_bits']))[0]
            resources.append(dict(resource=f'{fid:08x}', block=block, weight=weight))
        observed[source] = resources
        bindings.append(dict(accept=accept['capture'], generation_entry=entry['capture'],
                             source=source, calls=[r['capture'] for r in calls],
                             historical_epoch='UNKNOWN'))
    original = predictor.geometry.populate_source
    generated = []
    def run(request, constants):
        request = copy.deepcopy(request)
        if request['source'] in observed:
            request['ordered_resources'] = observed[request['source']]
            request['provenance'] = 'D4B receipt-informed diagnostic v1; epoch UNKNOWN'
        result = original(request, constants)
        if request['source'] in observed:
            generated.append(dict(request=request, result=result))
        return result
    with patch.object(predictor.geometry, 'populate_source', side_effect=run):
        replay = predictor.predict(envelope, previous['request'])
    write('replay.json', replay)
    write('sources.json', generated)
    # Discriminator only, never a candidate correction: remove different-resource
    # rejection while retaining every original random draw, key and operand.
    with patch.object(predictor.geometry, 'populate_source', side_effect=run), \
         patch.object(predictor.geometry, 'competition_rejects', return_value=False):
        unopposed = predictor.predict(envelope, previous['request'])
    write('without-competition.json', unopposed)
    comparisons = []
    for accept in accepted:
        fid = f'{struct.unpack_from("<I",bytes.fromhex(accept["selected"]["raw_resource"]),0x28)[0]:08x}'
        geometry = accept['geometry']
        matches = [r for r in replay['regions'] if r['resource'] == fid and
                   r['ordered_xyzw_le'] == geometry['ordered_xyzw'] and
                   r['native_bound_le'] == geometry['raw_region'][:32]]
        unopposed_matches = [r for r in unopposed['regions'] if r['resource']==fid and
            r['ordered_xyzw_le']==geometry['ordered_xyzw'] and r['native_bound_le']==geometry['raw_region'][:32]]
        comparisons.append(dict(capture=accept['capture'], resource=fid,
            exact_matches=len(matches), cells=[r['cell'] for r in matches],
            without_competition_exact_matches=len(unopposed_matches)))
    write('summary.json', dict(version='D4B diagnostic replay v1',
        inputs={str(p):verify.pin(p) for p in (Path(__file__),corpus,frozen,base/'events.jsonl')},
        bindings=bindings, comparisons=comparisons,
        all_three_exact=all(r['exact_matches']==1 for r in comparisons),
        corpus_correction_established=False, historical_epoch='UNKNOWN'))
    print(json.dumps(comparisons))


if __name__ == '__main__':
    main()
