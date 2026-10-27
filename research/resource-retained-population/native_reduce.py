# SPDX-License-Identifier: GPL-3.0-or-later
"""Reduce actual native-shaped reads without fixture epoch/oracle members.

Pure reduction of decoded D5L native-boundary events. No writes or process calls.
Bounded success means a proved copied region, final source-map ownership and
later same-region map reuse. It never means an intended resource census.
"""
import math
import struct

RETAIL_RVAS=(0x79fca3,0x79fcd0,0x79feaf,0x79b8ed,0x79acf2,0x79ff1d,0x79d8b2,0x79de92,0x79d910,0x975030,0x9829b0,0x983140,0x9828d5,0x982b70)
RETAIL_NEXT=(0x79fca6,0x79fcd4,0x78d660,0x79b8f1,0x79acf5,0x79ff24,0x79d8b5,0x79de96,0x79d915,0x975032,0x9829b5,0x983148,0x9828d8,0x982b75)
EVENTS=['native_'+x for x in 'visited lookup query mask append complete init reset destroy erase grid_clear source_init grid_init source_retire'.split()]


def context_consistent(r):
    b=bytes.fromhex(r['raw_context'])
    if len(b)<0x100:return False
    def q(at):return struct.unpack_from('<Q',b,at)[0]
    if q(0xf8)!=r['rip'] or q(0x98)!=r['rsp']:return False
    event=r['event']
    if event=='native_init':return q(0xb0)==r['procgen']
    if event=='native_reset':return q(0xa8)==r['procgen']
    if event=='native_destroy':return q(0x80)==r['procgen']
    if event=='native_source_retire':return q(0x80)==r['source']
    if event=='native_grid_clear':return q(0x80)==r['grid']
    if event=='native_grid_init':return q(0xf0)==r['grid']
    if event=='native_source_init':return q(0xe8)==r['source'] and q(0xd8)==r['grid']+0x10 and q(0xe0)==r['definition']
    if event=='native_erase':return not r['related_map'] or q(0x80)==r['procgen']+0x10
    if r['working_rsp']!=r['rsp']+(0x2e0 if event=='native_mask' else 0x560 if event=='native_append' else 0):return False
    if event not in ('native_mask','native_append') and (q(0xa0)!=r['working_rsp']+0x100 or q(0xe0)!=r['procgen']):return False
    if event=='native_visited':return q(0xa8)&255==r['operand'] and q(0xb0)==r['visited_key']
    if event=='native_lookup':return q(0x78)==r['operand']
    if event=='native_query':return q(0xb8)==r['descriptor_pointer'] and q(0xc0)==r['query_pointer']
    if event=='native_mask':return q(0x78)&255==r['operand']
    if event=='native_append' and r.get('selected'):return q(0x78)&0xffffffff==r['append_index'] and q(0x90)==r['collection']
    return True


def geographic_key(source, descriptor):
    """Reuse the owned D5B qualified chart-0 geographic decoder."""
    if len(source) != 0x70 or len(descriptor) != 0x2c or descriptor[0] != 0:
        return None
    x, y = struct.unpack_from('<2i', source, 0x10)
    dx = sum(struct.unpack_from('<i', descriptor, o)[0]*m for o,m in ((4,192),(0x14,12),(0x24,1)))
    dy = sum(struct.unpack_from('<i', descriptor, o)[0]*m for o,m in ((8,192),(0x18,12),(0x28,1)))
    return f'0:{dx+x}:{dy+y}:{struct.unpack_from("<I",source)[0]:08x}'


def shape(region):
    if not region or not region.get('read_complete'):
        return None
    h = bytes.fromhex(region['header'])
    p = bytes.fromhex(region['points'])
    if len(h) != 48:
        return None
    n, cap = struct.unpack_from('<II', h, 0x18)
    if not 0 < n <= cap <= 4096 or len(p) != n*16:
        return None
    if not all(math.isfinite(v) for v in struct.unpack('<4f', h[:16])+struct.unpack('<'+'f'*(len(p)//4), p)):
        return None
    return dict(fields=h[:0x15].hex(), count=n, points=p.hex())


def population_regions(population):
    out = {}
    if not population or not population.get('read_complete') or not population.get('wrapper'):
        return out
    slot=bytes.fromhex(population['slot_raw'])
    if len(slot)!=24 or struct.unpack_from('<2Q',slot)!=(population['source'],population['wrapper']) or struct.unpack_from('<I',slot,16)[0]==0xffffffff:
        raise ValueError('Owned source slot bytes')
    for resource in population['resources']:
        raw=bytes.fromhex(resource['resource_slot_raw']);h=bytes.fromhex(resource['collection_header'])
        if len(raw)!=24 or len(h)!=24 or struct.unpack_from('<I',raw)[0]!=resource['resource'] or struct.unpack_from('<Q',raw,8)[0]!=resource['collection'] or struct.unpack_from('<I',raw,16)[0]==0xffffffff:
            raise ValueError('Owned resource slot bytes')
        n,cap=struct.unpack_from('<II',h,8)
        if not 0<=n<=cap<=4096 or n!=len(resource['regions']):raise ValueError('Collection extent')
        if not 0<struct.unpack_from('<I',h)[0]<0xffffffff:raise ValueError('Collection reference state')
        data=struct.unpack_from('<Q',h,16)[0]
        for index, region in enumerate(resource['regions']):
            if region['address']!=data+index*48:raise ValueError('Collection data ancestry')
            value = shape(region)
            if value:
                key = (resource['resource'], resource['collection'], index)
                if key in out:
                    raise ValueError('Duplicate resource/collection/index')
                out[key] = value
    return out


def reduce(rows, expected_image, synthetic=False):
    session = None
    armed = False
    last = 0
    serial = 0
    generations = {}
    calls, retained, decisions, chains, rejected, threads = {}, {}, [], [], [], {}
    dead_procgen,dead_grid,dead_source=set(),set(),set()
    last_manager=None
    domain_epoch=0

    def epoch(kind, pointer):
        return generations.setdefault((kind, pointer), 1)

    def invalidate(kind, pointer, reason):
        generations[(kind, pointer)] = generations.get((kind, pointer), 1)+1
        for key in list(calls):
            c = calls[key]
            if c.get(kind) == pointer:
                decisions.append(dict(c, qualified=False, reason=reason))
                calls.pop(key)
        for key in list(retained):
            if retained[key].get(kind) == pointer:
                retained.pop(key)

    def gap(reason):
        nonlocal armed
        armed = False
        for c in calls.values():
            decisions.append(dict(c, qualified=False, reason=reason))
        calls.clear();retained.clear();generations.clear()
        rejected.append(dict(capture=last, reason=reason))

    for r in rows:
        kind = r['kind']
        if kind == 'SESSION':
            if session or r.get('schema') != 'sor-d5l-native/2' or r.get('synthetic') is not synthetic or r.get('image_sha256') != expected_image:
                raise ValueError('Pinned native ABI session required')
            session = r
            if not isinstance(r.get('pid'),int) or r['pid']<=0 or not r.get('creation_filetime_100ns') or len(r.get('sites',[]))!=14 or len(set(r['sites']))!=14:
                raise ValueError('Process/probe identity')
            if not synthetic and (r['sites']!=[r['module_base']+x for x in RETAIL_RVAS] or r['step_targets']!=[r['module_base']+x for x in RETAIL_NEXT]):
                raise ValueError('Retail probe relocation')
        elif kind == 'ARM_BARRIER':
            if not session or not r.get('readback') or r.get('sites') != 14:
                gap('unqualified_barrier')
            else:
                armed = True
                threads = {x['tid']:x['lifetime'] for x in r.get('threads',[])}
                if len(threads) != r.get('all_threads'):
                    gap('thread_barrier')
        elif kind == 'THREAD_ARMED':
            threads[r['tid']] = r['thread_lifetime']
        elif kind == 'THREAD_EXIT':
            if threads.get(r['tid']) == r['thread_lifetime']:
                for key in list(calls):
                    if key[:2] == (r['tid'],r['thread_lifetime']):
                        decisions.append(dict(calls.pop(key),qualified=False,reason='thread_exit'))
                threads.pop(r['tid'])
        elif kind == 'TARGET_EXCEPTION':
            if threads.get(r['tid']) != r['thread_lifetime']:
                gap('exception_thread_identity')
            else:
                for c in calls.values():
                    if c['context'][:2] == [r['tid'],r['thread_lifetime']]:
                        c['append_failures'].append(dict(reason='target_exception',code=r['code']))
        elif kind in ('GAP', 'STOP_COMMITTED'):
            gap(kind)
        elif kind == 'EXIT':
            armed = False
        elif kind == 'SAMPLE':
            if r['capture'] != last+1:
                gap('capture_sequence')
            last = r['capture']
            if not armed:
                rejected.append(dict(capture=last, reason='outside_coverage'))
                continue
            if not 0<=r['site']<14 or r['event']!=EVENTS[r['site']] or threads.get(r['tid']) != r['thread_lifetime'] or r['rip'] != session['sites'][r['site']]+1:
                gap('thread_or_site_identity')
                continue
            if not r.get('read_complete') or not r.get('native_abi'):
                gap('incomplete_native_read')
                continue
            if not context_consistent(r):
                gap('raw_context_mismatch')
                continue
            event = r['event']
            if last_manager != r['manager']:
                for c in calls.values():decisions.append(dict(c,qualified=False,reason='manager_identity_changed'))
                calls.clear();retained.clear();domain_epoch+=1;last_manager=r['manager']
            if event in ('native_init', 'native_reset', 'native_destroy'):
                invalidate('procgen', r['procgen'], event)
                if event=='native_destroy':dead_procgen.add(r['procgen'])
                elif not r.get('empty_source_map'):
                    gap('unqualified_initialization_or_reset')
                elif event=='native_init':dead_procgen.discard(r['procgen'])
                continue
            if event == 'native_grid_clear':
                invalidate('grid', r['grid'], event)
                dead_grid.add(r['grid'])
                continue
            if event == 'native_grid_init':
                invalidate('grid',r['grid'],event)
                if r.get('initialized_type'):dead_grid.discard(r['grid'])
                else:gap('grid_initialization_type')
                continue
            if event in ('native_source_init','native_source_retire'):
                invalidate('source', r['source'], event)
                if event=='native_source_init':dead_source.discard(r['source'])
                else:dead_source.add(r['source'])
                continue
            if event == 'native_erase':
                if r['related_map']:
                    invalidate('source', r['source'], event)
                    dead_source.add(r['source'])
                continue
            if not r.get('frame_valid'):
                gap('native_frame')
                continue
            if r['procgen'] in dead_procgen or r['grid'] in dead_grid or r['source'] in dead_source:
                rejected.append(dict(capture=last,reason='inactive_owner',event=event))
                continue
            source_bytes = bytes.fromhex(r['source_raw'])
            owner_bytes = bytes.fromhex(r['manager_raw'])
            descriptor_bytes = bytes.fromhex(r['descriptor_raw'])
            selected=geographic_key(source_bytes, descriptor_bytes)=='0:37536:20928:0029d20e' and struct.unpack_from('<I',owner_bytes,0x80)[0]==0x5e0de
            if selected!=r['selected']:
                gap('source_selector_mismatch');continue
            if not selected:
                rejected.append(dict(capture=last,reason='unrelated_source_or_owner'))
                continue
            key = (r['tid'], r['thread_lifetime'], r['working_rsp'], r['source'])
            life = [domain_epoch,r['manager'],r['procgen'],epoch('procgen',r['procgen']),r['grid'],epoch('grid',r['grid']),r['source'],epoch('source',r['source'])]
            if event == 'native_visited':
                if key in calls:
                    decisions.append(dict(calls.pop(key),qualified=False,reason='replaced_invocation'))
                serial += 1
                c = dict(token=serial,context=list(key),lifetime=life,manager=r['manager'],procgen=r['procgen'],grid=r['grid'],source=r['source'],
                         source_raw=r['source_raw'],query_raw=r['query_raw'],descriptor_raw=r['descriptor_raw'],owner_mode=owner_bytes[0x20],owner_id=owner_bytes[0x80:0x84].hex(),
                         first_capture=last,mask=None,decision='PENDING',regions={},append_failures=[],stages=['visited'])
                if r['operand'] not in (0,1) or r['visited_key'] != struct.unpack_from('<Q',source_bytes,0x68)[0]:
                    gap('visited_operand_or_identity')
                elif r['operand']:
                    decisions.append(dict(c,decision='VISITED_BYPASS',qualified=True,reason='guard_only'))
                else:
                    calls[key] = c
                continue
            c = calls.get(key)
            if not c:
                rejected.append(dict(capture=last,reason='missing_invocation'))
                continue
            if life != c['lifetime'] or r['source_raw'] != c['source_raw'] or r['query_raw'] != c['query_raw'] or r['descriptor_raw'] != c['descriptor_raw'] or c['owner_mode'] != owner_bytes[0x20] or c['owner_id'] != owner_bytes[0x80:0x84].hex():
                gap('identity_query_frame_changed')
                continue
            if event == 'native_lookup':
                pop = r['population']
                operand, cap = r['operand'], pop['capacity']
                if operand == cap and not pop['wrapper'] and pop['slot_index'] == cap:
                    retained.pop(tuple(life),None)
                    c['decision'] = 'MISS';c['stages'].append('miss')
                elif operand < cap and pop['slot_index'] == operand and pop['source'] == c['source'] and pop['wrapper']:
                    c['decision'] = 'HIT';c['stages'].append('hit');c['wrapper'] = pop['wrapper']
                    current = population_regions(pop)
                    old = retained.get(tuple(life))
                    matched = []
                    if old and old['wrapper'] == pop['wrapper']:
                        matched = [k for k,v in old['regions'].items() if current.get(k) == v]
                    decisions.append(dict(c,qualified=True,reason='occupied_source_slot',regions={}))
                    if matched:
                        chains.append(dict(construction=old['token'],reuse=c['token'],lifetime=life,mask=old['mask'],
                            construction_query=old['query_raw'],reuse_query=c['query_raw'],
                            regions=[dict(resource=k[0],collection=k[1],index=k[2],shape=current[k]) for k in matched],
                            population_partial=bool(old['append_failures']),basis='OBSERVED_BOUNDARIES_AND_COPIED_REGIONS'))
                    calls.pop(key)
                else:
                    gap('lookup_ancestry')
            elif event == 'native_query':
                pop = r['population']
                if c['decision'] != 'MISS' or pop['source'] != c['source'] or not pop['wrapper'] or not pop['read_complete']:
                    gap('insertion_ownership')
                else:
                    c['wrapper'] = pop['wrapper'];c['stages'].append('query')
            elif event == 'native_mask':
                if c['mask'] is not None or r['operand'] not in range(16) or 'query' not in c['stages']:
                    gap('mask_order_or_range')
                else:
                    c['mask'] = r['operand'];c['stages'].append('mask')
            elif event == 'native_append':
                value, temporary = shape(r.get('destination')), shape(r.get('temporary'))
                if c['mask'] is not None and r['append_index'] != 0xffffffff and value and value == temporary:
                    ident = (r['resource'],r['collection'],r['append_index'])
                    c['regions'][ident] = value
                else:
                    c['append_failures'].append(dict(capture=last,index=r['append_index'],reason='append_or_point_copy'))
            elif event == 'native_complete':
                calls.pop(key)
                actual = population_regions(r['population'])
                successful = {k:v for k,v in c['regions'].items() if actual.get(k) == v}
                qualified = bool(c['decision'] == 'MISS' and c['mask'] is not None and successful and
                                 c.get('wrapper') == r['population']['wrapper'] and r['population']['source'] == c['source'])
                c['regions'] = successful
                decisions.append(dict(c,regions=[dict(resource=k[0],collection=k[1],index=k[2],shape=v) for k,v in successful.items()],
                                      qualified=qualified,reason='witnessed_regions_only' if qualified else 'no_completed_owned_region'))
                if qualified:
                    retained[tuple(life)] = c
    decisions.extend(dict(c,regions={},qualified=False,reason='missing_terminal') for c in calls.values())
    for c in decisions:
        if isinstance(c['regions'],dict):
            c['regions'] = [dict(resource=k[0],collection=k[1],index=k[2],shape=v) for k,v in c['regions'].items()]
    decisions.sort(key=lambda c:c['first_capture'])
    return dict(schema='sor-d5l-native-reduction/2',synthetic=synthetic,session_identity=None if session is None else {k:session[k] for k in ('pid','creation_filetime_100ns','image_sha256','module_base')},decisions=decisions,chains=chains,rejected=rejected,
                first_ever='UNKNOWN',complete_intended_census=False)
