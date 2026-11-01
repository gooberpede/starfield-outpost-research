# SPDX-License-Identifier: GPL-3.0-or-later
"""Reduce schema 4 witnesses without a retrospective native source read.

Pure offline computation. Reads event dictionaries, writes no files, and never
reads a native pointer. Allocation identity comes from a constructor witness,
not token equality. Missing publication or observed invalidation refuses a conditional join.
Native path completeness remains a separately reviewed premise. Adapted from the
owned schema-3 reducer, whose historical semantics remain unchanged.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import struct
from bisect import bisect_left, bisect_right
from collections import defaultdict, Counter


def reduce(events, legacy_reduce, source_key, first_loss=0, last_loss=0):
    events = sorted(events, key=lambda e: e['sequence'])
    sequences = [e['sequence'] for e in events]
    if len(set(sequences)) != len(sequences) or any(b != a + 1 for a, b in zip(sequences, sequences[1:])):
        return dict(chains=[], diagnostics=[dict(outcome='SEQUENCE_GAP_OR_DUPLICATE')], identities=[])
    entry_counts = Counter(e['invocation'] for e in events if e['kind'] == 1)
    returns_by_invocation=defaultdict(list)
    for e in events:
        if e['kind']==9:returns_by_invocation[e['invocation']].append(e)
    selection_counts = Counter((e['invocation'], e['selection']) for e in events if e['kind'] == 2)
    births = [e for e in events if e['kind'] == 14]
    publications = [e for e in events if e['kind'] == 15]
    allocation_counts=Counter(e['selection'] for e in births)
    entries = {e['invocation']: e for e in events if e['kind'] == 1}
    by_source, published_by_source, parts_by_key = defaultdict(list), defaultdict(list), defaultdict(list)
    birth_by_sequence={e['sequence']:e for e in births}
    event_by_sequence={e['sequence']:e for e in events}
    for e in births:by_source[e['source']].append(e)
    for rows in by_source.values():rows.sort(key=lambda e:e['ticks'])
    birth_ticks={p:[b['ticks'] for b in rows] for p,rows in by_source.items()}
    for e in publications:published_by_source[e['source']].append(e)
    for e in events:parts_by_key[(e['invocation'],e['selection'])].append(e)
    fences=[e for e in events if e['kind']==10 and e['a'] in (1,2,3,4)]
    fence_ticks=sorted(e['ticks'] for e in fences)
    fence_sequences=sorted(e['sequence'] for e in fences)
    open_fences=defaultdict(list);spans=[]
    for e in events:
        if e['kind'] in (10,11) and e['a'] in (1,2,3,4):
            key=e['thread'],e['proc'],e['a']
            if e['kind']==10:open_fences[key].append(e)
            else:spans.append((open_fences[key].pop() if open_fences[key] else None,e))
    spans.extend((e,None) for rows in open_fences.values() for e in rows)
    identities, diagnostics, chains = [], [], []

    def definition(e):
        data=bytes.fromhex(e['source_bytes'])
        return (data[:4]+data[0x38:0x39]+data[0x3c:0x44]+data[0x4c:0x54]
                +data[0x5c:0x64]+data[0x68:0x70]).hex()

    def before(a,b):
        # Same-thread callback order disambiguates a QPC tick tie. Across threads
        # a tie is deliberately unordered, rather than guessed by admission.
        return a['ticks']<b['ticks'] or (a['ticks']==b['ticks'] and a['thread']==b['thread'] and a['sequence']<b['sequence'])

    # A producer reset epoch has one begin, one protected empty witness and one
    # normal end on the same thread. A later admitted end cannot retrospectively
    # certify an entry that executed before the reset actually completed.
    reset_parts=defaultdict(list)
    for e in events:
        if e['kind']==12 or (e['kind'] in (10,11) and e['a']==0):
            reset_parts[(e['proc'],e['epoch'])].append(e)
    certificates={}
    for key,rows in reset_parts.items():
        if sorted(e['kind'] for e in rows)!=[10,11,12]:continue
        begin,cold,end=(next(e for e in rows if e['kind']==kind) for kind in (10,12,11))
        if (any(e['status'] for e in rows) or
                len({e['thread'] for e in rows})!=1 or
                [begin['hazards'],cold['hazards'],end['hazards']]!=[1,1,0] or
                cold['a'] or cold['b'] or
                not begin['sequence']<cold['sequence']<end['sequence'] or
                not before(begin,cold) or not before(cold,end)):
            continue
        certificates[cold['sequence']]=end

    def identity(visited, boundary=None):
        observed=visited
        if boundary is not None:
            visited=dict(boundary,b=observed['b'],c=observed['c'])
        entry = entries.get(visited['invocation'])
        key=observed['invocation'],observed['selection']
        parts=parts_by_key[key]
        selections=[e for e in parts if e['kind']==2]
        decisions=[e for e in parts if e['kind']==3]
        if (not entry or entry_counts[observed['invocation']]!=1 or
                selection_counts[key]!=1 or len(decisions)!=1 or observed['a'] not in (0,1)):
            return None
        selected=selections[0]
        if any(e['status'] or e['hazards'] for e in (entry,selected,observed,visited)):
            return None
        if not before(entry,selected) or not before(selected,observed):
            return None
        if boundary is not None and not before(observed,boundary):
            return None
        if any(e[field]!=observed[field] for e in (entry,selected,visited)
               for field in ('proc','invocation','thread','parent','request','epoch')):
            return None
        if any(e[field]!=observed[field] for e in (selected,visited)
               for field in ('source','frame','selection')):
            return None
        source=visited['source'];rows=by_source[source];ticks=birth_ticks.get(source,[])
        index=bisect_right(ticks,entry['ticks'])-1
        if index<0:return None
        birth=rows[index]
        if not birth['selection'] or allocation_counts[birth['selection']]!=1 or birth['source']<0x10000:return None
        if not before(birth,entry):return None
        if index+1<len(rows) and rows[index+1]['ticks']<=visited['ticks']:return None
        if first_loss and birth['sequence'] <= last_loss and first_loss <= visited['sequence']:
            return None
        token = struct.unpack_from('<Q', bytes.fromhex(birth['source_bytes']), 0x68)[0]
        if birth['status'] or birth['hazards'] or birth['a'] != token or token != visited['b'] or birth['d']!=visited['c']:
            return None
        # Even an omitted invalidation changes the producer epoch. Refuse all
        # cross-epoch allocation joins, including sources surviving a reset.
        if birth['epoch']!=entry['epoch'] or birth['epoch']!=visited['epoch']:
            return None
        pubs = [p for p in published_by_source[source] if p['epoch']==birth['epoch']
                and before(birth,p)]
        if (len(pubs)!=1 or pubs[0]['holder']!=birth['holder'] or
                pubs[0]['thread']!=birth['thread'] or not before(pubs[0],entry) or
                pubs[0]['status'] or pubs[0]['hazards'] or pubs[0]['a']<0x10000 or
                pubs[0]['selection']!=0):
            return None
        # A global clear is deliberately conservative. Reset alone does not free
        # geographic sources; every other lifecycle fence rejects this join.
        if any((start is None or not before(visited,start)) and (end is None or not before(end,birth)) for start,end in spans):return None
        if visited['status'] or visited['hazards'] or entry['epoch'] != visited['epoch']:
            return None
        return dict(source_key=source_key(birth), source_definition=definition(birth), allocation=birth['selection'],
                    birth_sequence=birth['sequence'], publication_sequence=pubs[0]['sequence'],
                    visited_sequence=visited['sequence'], token=token, source=visited['source'],
                    invocation=visited['invocation'], selection=visited['selection'], epoch=visited['epoch'], proc=visited['proc'], bypass=bool(visited['a']))

    joins = {}
    for visited in (e for e in events if e['kind'] == 3):
        joined = identity(visited)
        if joined:
            identities.append(joined)
            joins[(visited['invocation'], visited['selection'])] = joined
        else:
            diagnostics.append(dict(outcome='UNQUALIFIED_SOURCE_LIFETIME', sequence=visited['sequence']))
    # Lookup payloads contain no source bytes in schema 4. Reconstruct only
    # after independently applying the allocation/publication/fence join through
    # lookup time. Never fill an unqualified pointer from a nearby geography.
    normalized=[]
    for event in events:
        if event['kind']==4:
            rows=parts_by_key[(event['invocation'],event['selection'])]
            visits=[e for e in rows if e['kind']==3]
            qualified=(len(visits)==1 and identity(visits[0],event))
            if bytes.fromhex(event['source_bytes'])!=bytes(0x70):
                qualified=False
                diagnostics.append(dict(outcome='SCHEMA4_UNEXPECTED_SOURCE_COPY',sequence=event['sequence']))
            if qualified:
                birth=birth_by_sequence[qualified['birth_sequence']]
                event=dict(event,source_bytes=birth['source_bytes'])
            else:
                event=dict(event,status=event['status']|8)
        normalized.append(event)
    legacy=legacy_reduce(normalized)
    diagnostics.extend(dict(d,outcome='SAMPLE_PREFIX_REQUIRES_APPEND_AND_IDENTITY')
                       if d['outcome']=='QUALIFIED_FIRST_CONSTRUCTION_SAMPLE' else d
                       for d in legacy['diagnostics'])
    parts_by_key=defaultdict(list)
    for event in normalized:parts_by_key[(event['invocation'],event['selection'])].append(event)
    token_groups,allocation_groups,prior_keys,prior_tokens=defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list)
    for j in identities:
        token_groups[(j['proc'],j['epoch'],j['token'])].append(j)
        allocation_groups[(j['proc'],j['allocation'],j['epoch'])].append(j)
        prior_keys[(j['proc'],j['epoch'],j['source_key'])].append(j['visited_sequence'])
        prior_tokens[(j['proc'],j['epoch'],j['token'])].append(j['visited_sequence'])
    for rows in (*prior_keys.values(),*prior_tokens.values()):rows.sort()
    known=set(joins)
    unknown_selections=[e['sequence'] for e in events if e['kind']==2 and (e['invocation'],e['selection']) not in known]
    for chain in legacy['chains']:
        key = chain['invocation'], chain['selection']
        joined = joins.get(key)
        parts = parts_by_key[key]
        reserves = [e for e in parts if e['kind'] == 16]
        stores = [e for e in parts if e['kind'] == 17]
        generated = [e for e in parts if e['kind'] == 8]
        reason = None
        if entry_counts[chain['invocation']] != 1 or selection_counts[key] != 1:
            reason = 'AMBIGUOUS_INVOCATION_OR_SELECTION'
        elif any(sum(e['kind']==kind for e in parts)!=1 for kind in (2,3,4,5,6,7,8)):
            reason = 'MISSING_OR_DUPLICATED_COMPLETE_SELECTION_BOUNDARY'
        elif chain['cold_sequence'] not in certificates or not before(certificates[chain['cold_sequence']],entries[chain['invocation']]):
            reason = 'EMPTY_RESET_CERTIFICATE_NATIVE_ORDER_INVALID'
        elif len(reserves)==1 and reserves[0]['a']==0xffffffff and not stores:
            reason='RESERVE_FAILED'
        elif not joined or joined['source_key'] != chain['source_key']:
            reason = 'UNQUALIFIED_SOURCE_LIFETIME'
        elif len(reserves) != 1 or len(stores) != 1 or len(generated) != 1:
            reason = 'MISSING_OR_AMBIGUOUS_APPEND_OUTCOME'
        elif (len(returns_by_invocation[chain['invocation']])>1 or
              any(not before(stores[0],returned) for returned in returns_by_invocation[chain['invocation']])):
            reason = 'CONTRADICTORY_NATIVE_RETURN'
        else:
            reserve, store = reserves[0], stores[0]
            if reserve['a'] == 0xffffffff:
                reason = 'RESERVE_FAILED'
            elif not chain['sample_sequence'] < generated[0]['sequence'] < reserve['sequence'] < store['sequence']:
                reason = 'APPEND_ORDER_INVALID'
            elif any(not before(a,b) for a,b in zip(
                    [e for e in parts if e['kind'] in (2,3,4,5,6,7,8,16,17)],
                    [e for e in parts if e['kind'] in (2,3,4,5,6,7,8,16,17)][1:])):
                reason = 'NATIVE_CAUSAL_ORDER_INVALID'
            elif any(e['status'] or e['hazards'] for e in (generated[0], reserve, store)):
                reason = 'APPEND_CONTEXT_INVALID'
            elif any(e['epoch'] != chain['epoch'] or e['proc'] != chain['proc'] or
                     e['source'] != chain['source'] or e['thread'] != chain['thread'] or e['request']!=chain['request']
                     or e['frame']!=parts[0]['frame'] or e['parent']!=parts[0]['parent'] for e in (generated[0], reserve, store)):
                reason = 'APPEND_EPOCH_OR_SOURCE_MISMATCH'
            elif reserve['a'] >= (reserve['c']&0xffffffff) or (reserve['c']&0xffffffff) > (reserve['c']>>32):
                reason='RESERVE_COUNT_OR_CAPACITY_INVALID'
            elif store['a'] != reserve['d']+reserve['a']*8 or store['b'] != joined['token']:
                reason = 'STORE_TOKEN_OR_DESTINATION_INVALID'
            elif first_loss and first_loss <= store['sequence'] and last_loss >= chain['cold_sequence']:
                reason = 'LOSS_BEFORE_APPEND'
            elif bisect_left(fence_sequences,store['sequence'])>bisect_right(fence_sequences,joined['birth_sequence']):
                reason = 'RETIREMENT_BEFORE_APPEND'
            elif any((start is None or not before(store,start)) and
                     (end is None or not before(end,birth_by_sequence[joined['birth_sequence']]))
                     for start,end in spans):
                # Admission can lag a different thread's native timestamp.
                # An unordered tie cannot establish lifetime through the store.
                reason = 'RETIREMENT_NATIVE_ORDER_AMBIGUOUS_THROUGH_APPEND'
            elif any(other['epoch'] == joined['epoch'] and other['token'] == joined['token']
                     and (other['source_key'], other['allocation']) != (joined['source_key'], joined['allocation'])
                     for other in token_groups[(joined['proc'],joined['epoch'],joined['token'])]):
                reason = 'TOKEN_COLLISION_OR_ALLOCATION_REUSE'
        if not reason:
            for rows in (prior_keys[(joined['proc'],joined['epoch'],joined['source_key'])],prior_tokens[(joined['proc'],joined['epoch'],joined['token'])]):
                if any(chain['cold_sequence']<seq<stores[0]['sequence'] and seq!=joined['visited_sequence'] for seq in rows):reason='PRIOR_ELIGIBLE_DECISION'
            if bisect_left(unknown_selections,stores[0]['sequence'])>bisect_right(unknown_selections,chain['cold_sequence']):reason='PRIOR_UNQUALIFIED_SELECTION'
            if stores[0]['c']!=birth_by_sequence[joined['birth_sequence']]['d']:reason='LOSS_DURING_SOURCE_LIFETIME'
            cold_event=next(e for e in parts_by_key[(0,0)] if e['sequence']==chain['cold_sequence'])
            if stores[0]['c']!=cold_event['c']:reason='LOSS_AFTER_COLD_BOUNDARY'
            if not before(cold_event,entries[chain['invocation']]):reason='COLD_NATIVE_ORDER_INVALID'
            for other in identities:
                if (other['proc'],other['epoch'])!=(joined['proc'],joined['epoch']):continue
                if other['visited_sequence']==joined['visited_sequence']:continue
                decision=event_by_sequence[other['visited_sequence']]
                if (other['source_key']==joined['source_key'] or other['token']==joined['token']):
                    if not before(decision,cold_event) and not before(stores[0],decision):
                        reason='PRIOR_OR_UNORDERED_NATIVE_DECISION'
            for selection in events:
                if selection['kind']!=2 or selection['epoch']!=joined['epoch']:continue
                if (selection['invocation'],selection['selection']) in known:continue
                if not before(selection,cold_event) and not before(stores[0],selection):
                    reason='PRIOR_OR_UNORDERED_UNQUALIFIED_SELECTION'
        if reason:
            diagnostics.append(dict(outcome=reason, invocation=chain['invocation'], selection=chain['selection']))
            continue
        later=[j for j in allocation_groups[(joined['proc'],joined['allocation'],joined['epoch'])]
               if j['bypass'] and before(store,event_by_sequence[j['visited_sequence']])]
        chains.append(dict(chain, allocation=joined['allocation'], visited_token=joined['token'],
                           store_sequence=store['sequence'], later_bypass=bool(later)))
    return dict(chains=chains, diagnostics=diagnostics, identities=identities)
