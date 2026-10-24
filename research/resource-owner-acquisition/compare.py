# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate ordered D4D boundary receipts and compare a frozen D4C model.

Reads supplied JSON events or decoded receipts and an optional frozen model;
writes an exclusive ignored JSON result. Uses owned D4C logical transitions and
stdlib only. No target, generation, fitting, save, network or Git effects.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/resource-owner-root'))
from owner_map import reconstruct


def words(blob, width=4):
    if blob.get('status') != 'COMPLETE':
        raise ValueError('INCOMPLETE_ARRAY')
    raw = bytes.fromhex(blob['raw'])
    if len(raw) != blob['count']*width or blob['count'] > blob['capacity']:
        raise ValueError('ARRAY_LENGTH')
    return list(struct.unpack('<' + ('I' if width == 4 else 'Q')*blob['count'], raw))


def mapping(blob):
    if blob['status'] != 'COMPLETE':
        raise ValueError('INCOMPLETE_MAP')
    result = {}
    for entry in blob['entries']:
        if entry['key'] in result:
            raise ValueError('DUPLICATE_MAP_KEY')
        result[entry['key']] = words(entry['array'])
    return result


def component(row):
    raw = bytes.fromhex(row['component']['raw'])
    if len(raw) != 0x8c:
        raise ValueError('COMPONENT_LENGTH')
    return dict(identity=struct.unpack_from('<QQ', raw, 0x10),
                biome=struct.unpack_from('<I', raw, 0x60)[0],
                root=struct.unpack_from('<I', raw, 0x70)[0],
                slots=list(struct.unpack_from('<6I', raw, 0x74)))


class State(dict):
    """Streaming active invocations plus receipt sequence integrity tokens."""
    def __init__(self):
        super().__init__()
        self.sequences = {}
        self.last_capture = 0


def validate(rows, state=None, finalize=True):
    """Return complete chains; every edge is checked against later observations.

    Boundary agreement witnesses the logical whole-row effect. Individual
    allocator outcomes remain UNKNOWN. Missing boundaries reject coverage;
    mismatched observed/model contents remain explicit scientific discrepancies.
    """
    active, chains, rejected = (state if state is not None else State()), [], []
    for row in rows:
        if row['kind'] == 'THREAD_END':
            active.sequences.pop((row['tid'], row['lifetime']), None)
        if row['kind'] == 'SAMPLE':
            thread = (row['tid'], row['thread_lifetime'])
            if (row['capture'] != active.last_capture+1 or
                    row['thread_sequence'] != active.sequences.get(thread, 0)+1):
                rejected.append(dict(capture=row['capture'], reason='RECEIPT_SEQUENCE_GAP'))
                active.clear()
            active.last_capture = row['capture']
            active.sequences[thread] = row['thread_sequence']
        if row['kind'] in ('LOSS', 'EXCEPTION', 'PHASE'):
            for k in active:
                rejected.append(dict(key=k, reason='OBSERVATION_GAP'))
            active.clear()
            continue
        if row['kind'] != 'SAMPLE' or row.get('diagnostic_scope') != 'ORDERED_OWNER_CONSTRUCTION':
            continue
        key = (row['pid'], row['tid'], row['thread_lifetime'], row.get('invocation_token'))
        site = row['site']
        if site == 'generation_entry':
            active[key] = dict(components=[], snapshots=[], calls=[], selected=None,
                source=row['source']['raw'], completed=False, cleanup=False, entry=row,
                source_identity=None, candidate_pointers=None, candidate_ready=False)
            active[key].update(first_operation_divergence=None, call_rarities=[], native_selected_array=None)
        chain = active.get(key)
        if chain is None:
            rejected.append(dict(key=key, capture=row['capture'], reason='ORPHAN_STOP'))
            continue
        try:
            if not row['frame_matches'] or not row['required_reads_complete']:
                raise ValueError('FRAME_OR_READ')
            if row['source_retained']['raw'] != chain['source']:
                raise ValueError('SOURCE_REUSE')
            m = bytes.fromhex(row['current_manager']['raw'])
            s = bytes.fromhex(chain['source'])
            offset = 0x1c0 if m[0x20] == 3 else 0xc8
            coarse = struct.unpack_from('<2i', m, offset+4)
            sub = struct.unpack_from('<2i', m, offset+0x14)
            fine = struct.unpack_from('<2i', m, offset+0x24)
            source_xy = struct.unpack_from('<2i', s, 0x10)
            if (m[offset] not in (0, 1) or any(v < 0 or v >= 16 for v in sub) or
                    any(v < 0 or v >= 12 for v in fine) or
                    any(v < 0 or v >= 256 for v in coarse)):
                raise ValueError('UNQUALIFIED_MANAGER_FRAME')
            anchor = [coarse[i]*192+sub[i]*12+fine[i]+source_xy[i] for i in (0, 1)]
            identity = f'{m[offset]}:{anchor[0]}:{anchor[1]}:{struct.unpack_from("<I", s)[0]:08x}'
            owner = struct.unpack_from('<I', m, 0x80)[0]
            if chain['source_identity'] is None:
                chain['source_identity'], chain['owner'] = identity, owner
                if owner != chain['entry']['owner_key_u32']:
                    raise ValueError('GENERATION_OWNER_MISMATCH')
            elif (identity, owner) != (chain['source_identity'], chain['owner']):
                raise ValueError('MANAGER_CONTEXT_CHANGED')
            if site in ('component_loop', 'map_cleanup'):
                observed_map, stage = mapping(row['map']), words(row['staging'])
                predicted = reconstruct(chain['components'])
                if observed_map != predicted['maps'] or stage != predicted['discarded_staging']:
                    if chain['first_operation_divergence'] is None:
                        chain['first_operation_divergence'] = dict(domain='staging_map_operation',
                            after_component=len(chain['components'])-1, capture=row['capture'],
                            expected_map=predicted['maps'], observed_map=observed_map,
                            expected_staging=predicted['discarded_staging'], observed_staging=stage)
                chain['snapshots'].append(dict(capture=row['capture'], mapping=observed_map, staging=stage))
                if site == 'component_loop':
                    if row['component_ordinal'] != len(chain['components']):
                        raise ValueError('COMPONENT_ORDINAL')
                    item = component(row)
                    registered = int.from_bytes(bytes.fromhex(row['registered_component_type']['raw']), 'little')
                    expected_key = (chain['owner'] << 32) | registered | 0x10000
                    iterator = bytes.fromhex(row['iterator']['raw'])
                    upper_key = struct.unpack_from('<QQ', iterator, 0x28)
                    if item['identity'][0] != expected_key or not 0 <= item['identity'][1] <= 0xffffffffffff or upper_key != (expected_key, 0xffffffffffff):
                        raise ValueError('OWNER_TYPE_OR_RANGE')
                    if chain['components'] and item['identity'] <= chain['components'][-1]['identity']:
                        raise ValueError('KEY_ORDER')
                    chain['components'].append(item)
                else:
                    if row['visited_count'] != len(chain['components']):
                        raise ValueError('VISIT_COUNT')
                    chain['cleanup'] = True
            elif site == 'map_return':
                if not chain['cleanup'] or mapping(row['map']) != chain['snapshots'][-1]['mapping']:
                    raise ValueError('MAP_COMPLETION')
                chain['selected'] = struct.unpack('<I', bytes.fromhex(row['selected_root']['raw']))[0]
                chain['native_selected_array'] = mapping(row['map']).get(chain['selected'])
                chain['completed'] = True
            elif site == 'candidate_ready':
                if not chain['completed']:
                    raise ValueError('CANDIDATES_BEFORE_MAP_RETURN')
                chain['candidate_pointers'] = words(row['candidate_array'], 8)
                chain['candidate_ready'] = True
            elif site == 'ordinary_resource_call':
                if not chain['completed']:
                    raise ValueError('CALL_BEFORE_MAP_RETURN')
                pointers = words(row['candidate_array'], 8)
                if chain['candidate_pointers'] is None:
                    chain['candidate_pointers'] = pointers
                elif chain['candidate_pointers'] != pointers:
                    raise ValueError('CANDIDATE_ARRAY_CHANGED')
                # RDX is independently recorded in the native CONTEXT. The raw
                # IRES read address must occupy the next ordered list position.
                call = len(chain['calls'])
                if call >= len(pointers) or row['ires']['address'] != pointers[call]:
                    raise ValueError('CALL_POINTER_ORDER')
                raw = bytes.fromhex(row['ires']['raw'])
                if len(raw) != 0x118 or raw[0x2e] != 0x9f:
                    raise ValueError('IRES_TYPE')
                if int.from_bytes(bytes.fromhex(row['family_root_formid']['raw']), 'little') != chain['selected']:
                    raise ValueError('SELECTED_ROOT_CHANGED')
                chain['calls'].append(struct.unpack_from('<I', raw, 0x28)[0])
                chain['call_rarities'].append(raw[0x110])
            elif site == 'generation_return':
                if not chain['completed'] or not row['construction_completed']:
                    raise ValueError('UNFINISHED_CONSTRUCTION')
                if chain['candidate_pointers'] is not None and len(chain['calls']) != len(chain['candidate_pointers']):
                    raise ValueError('UNFINISHED_CALL_SEQUENCE')
                chain['trace'] = reconstruct(chain['components'])['trace']
                expected_ids = ([chain['selected']] + chain['native_selected_array']) if chain['native_selected_array'] is not None else []
                chain['selected_array_reconciliation'] = ('EXACT_IDS_AND_DESCENDING_RARITY'
                    if chain['candidate_ready'] and Counter(expected_ids) == Counter(chain['calls']) and
                    chain['call_rarities'] == sorted(chain['call_rarities'], reverse=True)
                    else 'UNKNOWN_FILTERING_OR_ALLOCATION')
                chain['generation_epoch'] = None
                chain['candidate_call_coverage'] = ('COMPLETE' if chain['candidate_ready'] else 'UNKNOWN_SKIPPED_PATH_OR_GAP')
                chain['consumer_join'] = None
                chain['status'] = 'COMPLETE_CONSTRUCTION_NO_HISTORICAL_JOIN'
                chains.append(chain)
                active.pop(key)
        except (ValueError, KeyError, TypeError, struct.error) as e:
            rejected.append(dict(key=key, capture=row['capture'], reason=str(e)))
            active.pop(key, None)
    if finalize:
        for key in active:
            rejected.append(dict(key=key, reason='MISSING_RETURN'))
    return dict(schema='sor-d4d-comparison/1', chains=chains, rejected=rejected)


def first_divergence(chain, model):
    """Compare native-witness order before derived operations and final calls."""
    operation = chain['first_operation_divergence']
    def earlier(component_difference):
        if operation is not None and operation['after_component'] < component_difference['index']:
            return operation
        return component_difference
    a, b = chain['components'], model['components']
    for index in range(max(len(a), len(b))):
        if index >= min(len(a), len(b)):
            return earlier(dict(domain='component_population', index=index))
        # D4C's installed hypothesis has BIOM labels, not witnessed native keys.
        # Compare that projection explicitly; never manufacture its key words.
        identity_field = 'biome' if isinstance(b[index].get('identity'), str) else 'identity'
        for field in (identity_field, 'root', 'slots'):
            left, right = a[index][field], b[index][field]
            if field in ('identity', 'slots'):
                left, right = list(left), list(right)
            if left != right:
                return earlier(dict(domain='component_order' if field in ('identity', 'biome') else field, index=index))
    if operation is not None:
        return operation
    predicted = reconstruct(b)
    strip_identity = lambda trace: [{k:v for k,v in row.items() if k != 'identity'} for row in trace]
    if strip_identity(chain['trace']) != strip_identity(predicted['trace']):
        return dict(domain='staging_map_operation')
    if chain['selected'] != model.get('selected', model.get('selected_root')):
        return dict(domain='selected_root')
    if 'calls' not in model:
        return dict(domain='MODEL_CALL_SEQUENCE_UNKNOWN')
    if chain['calls'] != model['calls']:
        return dict(domain='generation_call_sequence', index=next((i for i, (x,y) in enumerate(zip(chain['calls'], model['calls'])) if x != y), min(len(chain['calls']),len(model['calls']))))
    return dict(domain='NO_WITNESSED_DIVERGENCE')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument('--events', type=Path)
    source.add_argument('--captures', type=Path)
    ap.add_argument('--model', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work')
    receipt_hashes = {}
    if args.captures:
        import hashlib
        import importlib.util
        sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
        spec = importlib.util.spec_from_file_location('d4d_receipt_verifier', ROOT / 'research/resource-tungsten-acquisition/qualify.py')
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        event_path = args.captures / 'events.json'
        if event_path.exists():
            rows = json.loads(event_path.read_text(encoding='utf8'))
        else:
            rows = [json.loads(line) for line in (args.captures / 'events.jsonl').read_text(encoding='utf8').splitlines()]
        for row in rows:
            if row['kind'] != 'SAMPLE':
                continue
            path = args.captures / f'capture-{row["capture"]:05d}.bin'
            decoded = verifier.independent(path)
            if decoded[1] != row:
                raise ValueError('EVENT_RECEIPT_DISAGREEMENT')
            receipt_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    else:
        rows = json.loads(args.events.read_text(encoding='utf8'))
    result = validate(rows)
    result['input_scope'] = 'VERIFIED_SRO1_AND_EVENTS' if args.captures else 'SUPPLIED_DECODED_EVENTS_ONLY'
    result['receipt_sha256'] = receipt_hashes
    result['synthetic'] = all(r.get('synthetic') is True for r in rows if r['kind']=='SAMPLE')
    if args.model:
        model = json.loads(args.model.read_text())
        result['comparisons'] = [first_divergence(c, model) for c in result['chains']]
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(len(result['chains']), 'complete chains;', len(result['rejected']), 'rejected fragments')


if __name__ == '__main__':
    main()
