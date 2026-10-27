# SPDX-License-Identifier: GPL-3.0-or-later
"""Reduce D5L disposable evidence using observed lifecycle probes.

Reads in-memory decoded events; no writes or target effects. Fixture packet
fields are not retail ABI. Epochs and invocation tokens are observer-generated
from explicit probes, never inferred from timestamps or equal geometry.
"""
import struct

PACKET = struct.Struct('<5Q2i2I')
FIELDS = 'magic manager source wrapper slot qx qy mask branch'.split()


def reduce(rows):
    session = None
    coverage = False
    last = 0
    owners, generations, sources, calls, retained = {}, {}, {}, {}, {}
    decisions, chains, rejected = [], [], []
    serial = 0

    def gap(reason):
        nonlocal coverage
        coverage = False
        rejected.append(dict(reason=reason))
        for c in calls.values():
            decisions.append(dict(c, qualified=False, reason='coverage_gap'))
        calls.clear()
        retained.clear()
        owners.clear()
        sources.clear()

    for r in rows:
        kind = r['kind']
        if kind == 'SESSION':
            if session is not None or r.get('synthetic') is not True or r.get('schema') != 'sor-d5l/1':
                raise ValueError('One pinned synthetic session required')
            session = r
        elif kind == 'ARM_BARRIER':
            coverage = bool(session and r.get('readback') and r.get('sites') == 12 and r.get('all_threads', 0))
        elif kind in ('GAP', 'STOP_COMMITTED'):
            gap(kind)
        elif kind == 'EXIT':
            coverage = False
        elif kind == 'SAMPLE':
            if r['capture'] != last+1:
                gap('capture_sequence')
            last = r['capture']
            if not coverage or not r.get('read_complete'):
                gap('coverage_or_read')
                continue
            raw = bytes.fromhex(r['raw_packet'])
            if len(raw) != PACKET.size:
                gap('packet_size')
                continue
            p = dict(zip(FIELDS, PACKET.unpack(raw)))
            if p['magic'] != 0x44354c5041434b31 or not p['manager'] or not p['source']:
                gap('identity')
                continue
            site, manager, source = r['site'], p['manager'], p['source']
            if site in (0, 9, 10):
                generations[manager] = generations.get(manager, 0)+1
                owners[manager] = generations[manager]
                retained = {k:v for k,v in retained.items() if k[0] != manager}
                for k in list(calls):
                    if calls[k]['lifetime'][0] == manager:
                        decisions.append(dict(calls.pop(k), qualified=False, reason='owner_fence'))
                if site == 10:
                    owners.pop(manager)
                continue
            if site == 1:
                sources[(manager, source)] = sources.get((manager, source), 0)+1
                retained = {k:v for k,v in retained.items() if not (k[0] == manager and k[2] == source)}
                for k in list(calls):
                    if calls[k]['lifetime'][0] == manager and calls[k]['lifetime'][2] == source:
                        decisions.append(dict(calls.pop(k), qualified=False, reason='source_fence'))
                continue
            life = (manager, owners.get(manager), source, sources.get((manager, source)))
            key = (r['tid'], r['thread_lifetime'], r['packet_address'])
            if site == 2:
                if key in calls:
                    gap('duplicate_entry')
                    continue
                serial += 1
                calls[key] = dict(token=serial, lifetime=list(life), query=[p['qx'], p['qy']],
                    mask=None, decision=None, inserted=False, completed=False, first_capture=last,
                    wrapper=0, population=None, stages=[2], identity_known=all(life))
                continue
            c = calls.get(key)
            if c is None:
                rejected.append(dict(capture=last, reason='missing_invocation'))
                continue
            if c['lifetime'] != list(life) or c['query'] != [p['qx'], p['qy']]:
                gap('lifetime_or_query_changed')
                continue
            c['stages'].append(site)
            slot_owned = False
            if r.get('slot_read'):
                sb = bytes.fromhex(r['slot'])
                if len(sb) == 24:
                    skey, holder, occupied, _ = struct.unpack('<QQII', sb)
                    slot_owned = skey == source and holder == p['wrapper'] and holder != 0 and occupied != 0xffffffff
            if site == 3:
                if p['branch'] not in (0, 2):
                    gap('invalid_visited_operand')
                    continue
                c['decision'] = 'VISITED_BYPASS' if p['branch'] == 2 else 'PENDING'
            elif site == 4:
                c['decision'] = 'MISS' if p['branch'] == 0 else 'HIT' if p['branch'] == 1 else 'INVALID'
                c['wrapper'] = p['wrapper']
                c['lookup_owned'] = slot_owned
            elif site == 5:
                c['inserted'] = slot_owned
                c['wrapper'] = p['wrapper']
            elif site == 7:
                c['mask'] = p['mask']
            elif site == 8:
                if r.get('population_complete_read'):
                    b = bytes.fromhex(r['population'])
                    if c['mask'] is not None and len(b) == 40 and int.from_bytes(b[:8], 'little') == 2 and struct.unpack('<8f', b[8:]) == tuple(float(i+c['mask']) for i in range(8)):
                        c['completed'] = True
                        c['population'] = r['population']
                c['owned'] = slot_owned and p['wrapper'] == c['wrapper']
            elif site == 11:
                calls.pop(key)
                miss = c['stages'] == [2, 3, 4, 5, 6, 7, 8, 11]
                hit = c['stages'] == [2, 3, 4, 11]
                bypass = c['stages'] == [2, 3, 11]
                qualified = bool(c['identity_known'] and (
                    (c['decision'] == 'MISS' and miss and c['completed'] and c['inserted'] and
                     c.get('owned') and c['mask'] in range(16)) or
                    (c['decision'] == 'HIT' and hit and c['wrapper'] and c.get('lookup_owned') and slot_owned) or
                    (c['decision'] == 'VISITED_BYPASS' and bypass)))
                c.update(qualified=qualified, last_capture=last,
                         reason='observed_fixture_contract' if qualified else 'incomplete_construction_or_order')
                decisions.append(c)
                if qualified and c['decision'] == 'MISS':
                    retained[life] = c
                elif qualified and c['decision'] == 'HIT':
                    old = retained.get(life)
                    if old and old['wrapper'] == c['wrapper'] and r.get('population_complete_read') and r['population'] == old['population']:
                        chains.append(dict(construction=old['token'], reuse=c['token'], lifetime=list(life),
                            mask=old['mask'], population=old['population'], basis='SYNTHETIC_OBSERVED_FENCES'))
    for c in calls.values():
        decisions.append(dict(c, qualified=False, reason='missing_exit'))
    decisions.sort(key=lambda c:c['first_capture'])
    return dict(schema='sor-d5l-reduction/1', synthetic=True, decisions=decisions,
                chains=chains, rejected=rejected, retail_result='NOT_TESTED', first_ever='UNKNOWN')
