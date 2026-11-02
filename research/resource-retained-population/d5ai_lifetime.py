# SPDX-License-Identifier: GPL-3.0-or-later
"""Reduce an authenticated ending journal for a previously captured population.

Pure offline reduction; no I/O, native execution, pointer reads or target action.
The native reader must independently authenticate the complete journal prefix,
loss counters and producer-safe coverage watermark. This module does not turn a
caller assertion into native coverage. See `d5ai-population-ending-proof.md`.
"""
from d5ai_geometry import normalize, uint

SCHEMA = 'sor-d5ai-lifetime/1'
KINDS = {'HOLDER_RESOURCE_MAP', 'COLLECTION_GEOMETRY', 'COLLECTION_MUTATION'}


def evaluate(before, after, journal):
    """Keep consumer exposure separate from survival of baseline content storage.

    A matching BEGIN irrevocably ends continuity of the old content identity,
    even if the pointer is later reused. END confirms only the clear body's
    return. It does not assert outer object deallocation or heap nonexistence.
    """
    result = dict(qualified=False, state='UNKNOWN', holder=None, collections=[],
                  before=[before['envelope']['session_id'], before['envelope']['snapshot_id']],
                  after=[after['envelope']['session_id'], after['envelope']['snapshot_id']],
                  consumer_exposed=after['envelope']['availability']['exposed'])
    try:
        normalize(before['envelope'])
        normalize(after['envelope'])
        if before['envelope']['availability']['exposed'] is not True:
            raise ValueError('No exposed qualified baseline')
        session = before['envelope']['session_id']
        if session != after['envelope']['session_id']:
            raise ValueError('Baseline storage cannot be tracked across processes/sessions')
        if (journal['schema'] != SCHEMA or journal['session_id'] != session or
                journal['complete'] is not True or uint(journal['loss'], 64)):
            raise ValueError('Incomplete, foreign or lossy ending journal')
        ah, bh = before['proof']['header'], after['proof']['header']
        start, stop = uint(ah['ticks_begin'], 64), uint(bh['completion_ticks'], 64)
        if not start < uint(ah['ticks_end'], 64) <= stop:
            raise ValueError('Invalid baseline/return observation interval')
        if uint(journal['qualified_from_ticks'], 64) > start:
            raise ValueError('Ending coverage began after the baseline')
        if uint(journal['qualified_through_ticks'], 64) < stop:
            raise ValueError('Journal prefix does not cover return completion')
        holder = uint(before['proof']['holder_pointer'], 64)
        pointers = before['proof']['collection_pointers']
        if not holder or not isinstance(pointers, list) or any(not uint(p, 64) for p in pointers):
            raise ValueError('Missing baseline allocation graph')
        graph = before['proof']['collection_graph']
        represented = {r['resource']: r for r in before['envelope']['population']}
        if (len(graph) != len(represented) or len(pointers) != len(graph) or
                [r['collection_pointer'] for r in graph] != pointers or
                {r['resource'] for r in graph} != set(represented)):
            raise ValueError('Baseline allocation graph cardinality/resource association differs')
        allocated, content, aliases = set(), set(), {}
        for resource in graph:
            pointer = resource['collection_pointer']
            regions = represented[resource['resource']]['regions']
            capacity, data = uint(resource['region_capacity'], 32), uint(resource['region_data'], 64)
            if len(resource['regions']) != len(regions) or len(regions) > capacity or (capacity and not data):
                raise ValueError('Baseline region allocation shape differs')
            if not capacity and data:
                raise ValueError('Non-null zero-capacity region backing ownership is unqualified')
            shape = dict(capacity=capacity, data=data, regions=resource['regions'], content=regions)
            if pointer in aliases and aliases[pointer] != shape:
                raise ValueError('Aliased collection has contradictory allocation shape/content')
            aliases[pointer] = shape
            if capacity:
                allocated.add(pointer)
            if regions:
                content.add(pointer)
            for index, (shape, region) in enumerate(zip(resource['regions'], regions)):
                point_capacity = uint(shape['point_capacity'], 32)
                point_data = uint(shape['point_data'], 64)
                if (shape['count'] != region['count'] or
                        shape['region_address'] != data + index * 48 or
                        point_capacity < region['count'] or (point_capacity and not point_data)):
                    raise ValueError('Baseline point allocation shape differs')
                if not point_capacity and point_data:
                    raise ValueError('Non-null zero-capacity point backing ownership is unqualified')
                if point_capacity:
                    allocated.add(pointer)
        # Native sharing can make several resource keys refer to one collection.
        # Track each distinct content lifetime exactly once, preserving aliases.
        targets = {('HOLDER_RESOURCE_MAP', holder)}
        targets.update(('COLLECTION_GEOMETRY', p) for p in pointers)
        intervals, opened, seen = {}, {}, set()
        result['recorded_exception_sequences'] = []
        previous_sequence = 0
        for event in journal['events']:
            sequence = uint(event['sequence'], 64)
            if sequence != previous_sequence + 1:
                raise ValueError('Ending journal sequence gap, duplicate or reorder')
            previous_sequence = sequence
            ticks, thread = uint(event['ticks'], 64), uint(event['thread'], 64)
            kind, phase = event['kind'], event['phase']
            pointer, invocation = uint(event['allocation'], 64), uint(event['invocation'], 64)
            status = uint(event['status'], 32)
            if (kind not in KINDS or phase not in ('BEGIN', 'END') or not pointer or not thread or not invocation or
                    status not in (0, 16) or phase == 'BEGIN' and status != 0):
                raise ValueError('Malformed or failed ending event')
            if status:
                result['recorded_exception_sequences'].append(sequence)
            key = (thread, invocation)
            target = ('COLLECTION_GEOMETRY' if kind == 'COLLECTION_MUTATION' else kind, pointer)
            if phase == 'BEGIN':
                if key in seen:
                    raise ValueError('Ending invocation identity reused')
                seen.add(key)
                opened[key] = event
            else:
                begin = opened.pop(key, None)
                if (begin is None or (begin['kind'], begin['allocation'], begin['receiver'], begin['parent']) !=
                        (kind, pointer, event['receiver'], event['parent']) or
                        begin['sequence'] >= sequence or begin['ticks'] > ticks):
                    raise ValueError('Unmatched, contradictory or tied ending interval')
                if target in targets:
                    intervals.setdefault(target, []).append(dict(begin=begin, end=event))
        # A later unfinished event is irrelevant to the measured prefix, but an
        # interval intersecting the return prevents a complete survival verdict.
        if any(e['ticks'] <= stop for e in opened.values()):
            raise ValueError('Content ending remains unfinished in measured prefix')
        def state(kind, pointer):
            answer = dict(allocation=pointer, state='SURVIVES', ending_sequences=[],
                          post_ending_address_activity=[])
            established = None
            operations = sorted(intervals.get((kind, pointer), []), key=lambda v: v['begin']['sequence'])
            for operation in operations:
                begin, end = operation['begin'], operation['end']
                if end['ticks'] < start or begin['ticks'] > stop:
                    continue
                # This is an old-content certificate, not an address identity.
                # Once normal teardown completes, later strictly separated
                # activity at that address cannot restore the old content or
                # erase the established ending. Only this exact typed target's
                # ending qualifies; holder teardown cannot end a collection.
                if (established is not None and established['end']['sequence'] < begin['sequence'] and
                        established['end']['ticks'] < begin['ticks']):
                    answer['post_ending_address_activity'].append(dict(kind=begin['kind'],
                                                                      begin_sequence=begin['sequence'],
                                                                      end_sequence=end['sequence'], end_status=end['status']))
                    continue
                if begin['kind'] == 'COLLECTION_MUTATION':
                    answer.update(state='UNKNOWN', reason='Baseline collection mutated before a qualified ending')
                    return answer
                if end['status'] != 0:
                    answer.update(state='UNKNOWN', reason='Baseline ending interval exited exceptionally')
                    return answer
                if begin['ticks'] <= ah['ticks_end']:
                    answer.update(state='UNKNOWN', reason='Baseline copy overlaps a content ending')
                    return answer
                if begin['ticks'] == stop or end['ticks'] >= stop:
                    answer.update(state='UNKNOWN', reason='Return boundary overlaps or ties content ending')
                    return answer
                if established is not None:
                    answer.update(state='UNKNOWN', reason='Later address activity overlaps or ties the old ending')
                    return answer
                established = operation
                answer.update(state='ENDED', ending_sequences=[begin['sequence']],
                              ending_end_sequence=end['sequence'], ending_end_ticks=end['ticks'])
            return answer

        result['holder'] = state('HOLDER_RESOURCE_MAP', holder)
        result['collections'] = [state('COLLECTION_GEOMETRY', p) for p in sorted(set(pointers))]
        for item in result['collections']:
            item.update(has_nested_backing=item['allocation'] in allocated,
                        has_represented_regions=item['allocation'] in content)
        surviving = sum(v['state'] == 'SURVIVES' for v in result['collections'])
        surviving_backing = sum(v['state'] == 'SURVIVES' and v['has_nested_backing'] for v in result['collections'])
        result['census'] = dict(baseline_collections=len(result['collections']), surviving_content_lifetimes=surviving,
                               unresolved_content_lifetimes=sum(v['state'] == 'UNKNOWN' for v in result['collections']),
                               baseline_with_nested_backing=len(allocated), surviving_with_nested_backing=surviving_backing,
                               baseline_with_regions=len(content),
                               surviving_with_regions=sum(v['state'] == 'SURVIVES' and v['has_represented_regions']
                                                          for v in result['collections']))
        if result['holder']['state'] == 'UNKNOWN' or any(v['state'] == 'UNKNOWN' for v in result['collections']):
            raise ValueError('Unresolved baseline content history; inspect per-allocation facts')
        if result['holder']['state'] == 'SURVIVES' and any(v['state'] == 'ENDED' for v in result['collections']):
            raise ValueError('Collection ended while immutable owning baseline map survives')
        if not pointers:
            classification = 'NO_BASELINE_GEOMETRY'
        elif not allocated and surviving == len(result['collections']):
            classification = 'EMPTY_CONTENT_LIFETIMES_SURVIVE'
        elif surviving == len(result['collections']):
            classification = 'COMPLETE_COLLECTION_GEOMETRY_SURVIVES'
        elif surviving and not surviving_backing:
            classification = 'ONLY_EMPTY_CONTENT_LIFETIMES_SURVIVE'
        elif surviving:
            classification = 'PARTIAL_COLLECTION_GEOMETRY_SURVIVES'
        else:
            classification = 'PRIOR_COLLECTION_GEOMETRY_ENDED'
        result.update(qualified=True, state=classification,
                      scope='Prior content-vector lifetimes, not outer object frees or global heap census')
    except (ValueError, KeyError, TypeError, OverflowError) as error:
        result['reason'] = str(error)
    return result
