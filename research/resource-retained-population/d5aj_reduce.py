# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AJ versioned source-Grid qualification of authenticated native histories.

SOR-P-0002 adaptation of d5ai_reduce.py; historical method remains unchanged.

Reads stopped local sessions, exact DLL identity and geometry files. Writes one
exclusive JSON report. Uses the owned historical reader unchanged; no process,
save, database, network or Git operations. Requires unoptimized Python -E -B.
All joins are conditional on the independently reviewed ordinary native coverage.
Missing source history or an unqualified fence refuses attribution, never proves absence.
Only disjoint owning-Grid clears may bridge epochs in this version; all other
fences retain refusal. Generation, content lifetime and owner context stay separate.
"""
import sys
from d5aj_scope import continuity, METHOD
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B without optimization')

import argparse
import hashlib
import math
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
import read_capture
import d5ai_read_geometry
import d5ai_read_lifetime
import d5ai_lifetime
from d5ai_geometry import SCHEMA, compare, frame, load, normalize


def validate_candidate_identity(identity):
    if not isinstance(identity, dict):
        raise ValueError('Candidate identity must be an object')
    d5ai_read_lifetime.validate_identity(identity)
    if (identity.get('schema') != 'sor-d5x/4' or identity.get('geometry_schema') != 'sor-d5ai-raw/2' or
            identity.get('geometry_header_bytes') != 456 or identity.get('context_schema') != 'sor-d5ai-context/1'):
        raise ValueError('Candidate lacks qualified geometry/context metadata')
    contexts, geometry = identity.get('context_sites', []), identity.get('geometry_sites', [])
    if not isinstance(contexts, list) or not isinstance(geometry, list) or len(contexts) != 2 or len(geometry) != 3:
        raise ValueError('Missing complete geometry/context site inventory')
    addresses = []
    for site, reason in zip(contexts, (5, 6)):
        if (not isinstance(site, dict) or type(site.get('bytes')) is not int or site['bytes'] != 5 or
                type(site.get('reason')) is not int or site['reason'] != reason or
                not isinstance(site.get('guard_sha256'), str) or not re.fullmatch('[0-9a-f]{64}', site['guard_sha256'])):
            raise ValueError('Context site contract mismatch')
        addresses.append(site.get('va'))
    for site, width in zip(geometry, (5, 5, 9)):
        if (not isinstance(site, dict) or type(site.get('bytes')) is not int or site['bytes'] != width or
                not isinstance(site.get('preimage_sha256'), str) or not re.fullmatch('[0-9a-f]{64}', site['preimage_sha256'])):
            raise ValueError('Geometry site contract mismatch')
        addresses.append(site.get('va'))
    if any(type(p) is not int or not 0x10000 <= p < 0x7fffffffffff for p in addresses) or len(set(addresses)) != 5:
        raise ValueError('Duplicate or invalid observation site')
    if identity.get('retail'):
        base = identity['module_base']
        if addresses != [base + r for r in (0x789ce0, 0x788e70, 0x21e09ed, 0x21e0aa5, 0x21e0a7e)]:
            raise ValueError('Retail observation site RVA mismatch')


def process_certificate(identity):
    """A changed nonce/session hash is not itself proof of a new process."""
    if (type(identity.get('pid')) is not int or not 0 < identity['pid'] < 2 ** 32 or
            type(identity.get('creation_filetime')) is not int or not 0 < identity['creation_filetime'] < 2 ** 64 or
            not isinstance(identity.get('host_sha256'), str) or not re.fullmatch('[0-9a-f]{64}', identity['host_sha256'])):
        raise ValueError('Missing native process birth/image identity')
    return {k: identity[k] for k in ('pid', 'creation_filetime', 'host_sha256')}


def source_identity(events, source, header):
    """Qualify a private source birth through a completed native map scan."""
    end = header['completion_ticks']
    if not 0x10000 <= source < 0x7fffffffffff:
        raise ValueError('Source pointer is outside the qualified address domain')
    births = [e for e in events if e['kind'] == 14 and e['source'] == source and e['ticks'] < end]
    if not births:
        raise ValueError('No source birth before snapshot')
    birth = max(births, key=lambda e: (e['ticks'], e['sequence']))
    if birth['ticks'] >= header['ticks_begin'] or not birth['selection']:
        raise ValueError('Source birth overlaps snapshot or lacks allocation identity')
    if sum(e['kind'] == 14 and e['selection'] == birth['selection'] for e in events) != 1:
        raise ValueError('Duplicate allocation identity')
    if (birth['status'] or birth['hazards'] or
            birth['d'] != header['loss']):
        raise ValueError('Birth/snapshot hazard or loss mismatch')
    raw = bytes.fromhex(birth['source_bytes'])
    if birth['a'] != struct.unpack_from('<Q', raw, 0x68)[0]:
        raise ValueError('Constructor token disagrees with initialized bytes')
    pubs = [e for e in events if e['kind'] == 15 and e['source'] == source and
            birth['ticks'] < e['ticks'] < header['ticks_begin']]
    if (len(pubs) != 1 or pubs[0]['status'] or pubs[0]['hazards'] or
            pubs[0]['epoch'] != birth['epoch'] or pubs[0]['holder'] != birth['holder'] or
            pubs[0]['thread'] != birth['thread'] or pubs[0]['a'] < 0x10000 or
            pubs[0]['selection'] != 0):
        raise ValueError('No unique qualified publication')
    bridge = continuity(events, birth['ticks'], end, birth['epoch'], header['epoch'], birth['holder'])
    return dict(key=read_capture.source_key(birth), source_pointer=source,
                allocation=birth['selection'], birth_sequence=birth['sequence'],
                birth_ticks=birth['ticks'], publication_sequence=pubs[0]['sequence'],
                epoch=birth['epoch'], token=birth['a'], owning_grid=birth['holder'], continuity=bridge)


def generation(events, identity, holder, header):
    """Require a miss, exact output-holder generation and successful normal return."""
    candidates = []
    for g in events:
        if not (g['kind'] == 6 and g['invocation'] and g['selection'] and g['source'] == identity['source_pointer'] and
                g['proc'] == header['proc'] and
                g['d'] == holder + 8 and g['a'] == header['owner_formid'] and
                identity['birth_ticks'] < g['ticks'] < header['ticks_begin']):
            continue
        parts = [e for e in events if e['invocation'] == g['invocation'] and
                 e['selection'] == g['selection'] and e['source'] == g['source']]
        lookups = [e for e in parts if e['kind'] == 4]
        returns = [e for e in parts if e['kind'] == 8]
        descriptors = [e for e in parts if e['kind'] == 5]
        if (len(lookups) != 1 or len(returns) != 1 or len(descriptors) != 1 or lookups[0]['a'] != lookups[0]['b'] or
                lookups[0]['c'] != g['source'] or not lookups[0]['ticks'] < g['ticks'] < returns[0]['ticks'] < header['ticks_begin']):
            continue
        desc = descriptors[0]
        if (not lookups[0]['ticks'] < desc['ticks'] < g['ticks'] or
                desc['d'] not in (desc['holder'] + 0xc8, desc['holder'] + 0x1c0) or
                desc['descriptor'] != g['descriptor'] or returns[0]['descriptor'] != g['descriptor']):
            continue
        if any(e['status'] or e['hazards'] or e['epoch'] != g['epoch'] or
               e['proc'] != header['proc'] or any(e[field] != g[field] for field in ('thread', 'parent', 'request', 'frame'))
               for e in (lookups[0], desc, g, returns[0])):
            continue
        continuity(events, identity['birth_ticks'], g['ticks'], identity['epoch'], g['epoch'], identity['owning_grid'])
        continuity(events, g['ticks'], header['completion_ticks'], g['epoch'], header['epoch'], identity['owning_grid'])
        raw_descriptor = bytes.fromhex(desc['descriptor'])
        candidates.append(dict(invocation=g['invocation'], selection=g['selection'],
                               generate_sequence=g['sequence'], return_sequence=returns[0]['sequence'],
                               frame=dict(basis='consumed-descriptor-v1', owner_formid=f"{g['a']:08x}",
                                          descriptor_semantic=(raw_descriptor[:1] + raw_descriptor[4:]).hex()),
                               ticks=g['ticks'], return_ticks=returns[0]['ticks']))
    if len(candidates) > 1:
        raise ValueError('Multiple construction histories for one holder')
    return candidates[0] if candidates else None


def owner_context(events, header, expected_owner):
    """Carry an actual generator owner only across owner-preserving transitions.

    This relies on the separately pinned native owner-writer/reset proof. Current
    manager reads alone do not establish this certificate, especially for absence.
    """
    candidates = []
    for g in events:
        if not (g['kind'] == 6 and g['proc'] == header['proc'] and g['a'] == expected_owner and
                g['invocation'] and g['selection'] and not g['status'] and not g['hazards'] and
                g['ticks'] < header['ticks_begin']):
            continue
        returns = [e for e in events if e['kind'] == 8 and
                   all(e[k] == g[k] for k in ('invocation', 'selection', 'proc', 'source', 'thread', 'parent', 'frame', 'epoch', 'request'))]
        if (len(returns) != 1 or returns[0]['status'] or returns[0]['hazards'] or
                returns[0]['descriptor'] != g['descriptor'] or
                not g['ticks'] < returns[0]['ticks'] < header['ticks_begin']):
            continue
        if any(e['kind'] in (10, 11) and e['a'] in (0, 1, 5, 6) and
               g['ticks'] <= e['ticks'] <= header['completion_ticks'] for e in events):
            continue
        if any(e['kind'] == 6 and e['proc'] == header['proc'] and e['a'] != expected_owner and
               g['ticks'] <= e['ticks'] <= header['completion_ticks'] for e in events):
            continue
        permitted = sorted((e for e in events if e['kind'] in (10, 11) and
                            g['ticks'] <= e['ticks'] <= header['completion_ticks']),
                           key=lambda e: (e['ticks'], e['sequence']))
        expected_epoch, opened, valid = g['epoch'], {}, True
        for e in permitted:
            key = (e['thread'], e['proc'], e['a'])
            if (e['a'] not in (2, 3, 4) or e['status'] or e['ticks'] == g['ticks'] or
                    e['epoch'] != expected_epoch + 1):
                valid = False
                break
            expected_epoch += 1
            if e['kind'] == 10:
                if key in opened:
                    valid = False
                    break
                opened[key] = e
            elif key not in opened or opened.pop(key)['ticks'] >= e['ticks']:
                valid = False
                break
        if valid and not opened and expected_epoch == header['epoch']:
            candidates.append(g)
    if not candidates:
        raise ValueError('No uninterrupted actual generation-owner certificate for this consumer context')
    chosen = max(candidates, key=lambda g: (g['ticks'], g['sequence']))
    return dict(owner_formid=f'{expected_owner:08x}', proc=header['proc'],
                generate_sequence=chosen['sequence'], ticks=chosen['ticks'],
                rule='Actual generation owner carried with no reset/destructor/full owner transition; raw manager value is diagnostic')


def envelope(snapshot, events, session_id, target, expected_owner=0x5e0de):
    h = snapshot['header']
    if (h['boundary'] != 2 or h['preunlock_seen'] != 1 or h['scan_result'] != 1 or
            h['iterator'] != h['scan_capacity'] or h['scan_capacity'] != h['map_capacity'] or
            any(not 0x10000 <= h[k] < 0x7fffffffffff for k in ('proc', 'manager', 'consumer'))):
        raise ValueError('Incorrect or incomplete native area-consumer identity')
    if h['owner_formid'] != expected_owner:
        raise ValueError('Consumer owner differs from expected geographical body')
    if not snapshot['complete_representation'] or h['status'] or h['loss']:
        raise ValueError('Snapshot is not a complete loss-free consumer boundary')
    query = bytes.fromhex(h['query_hex'])
    query_scalars = struct.unpack('<3f', query[:12])
    radius, upper = (struct.unpack('<f', struct.pack('<I', h[name]))[0]
                     for name in ('radius_bits', 'upper_bits'))
    if not all(math.isfinite(v) for v in (*query_scalars, radius, upper)) or radius < 0:
        raise ValueError('Consumer query is outside the qualified finite domain')
    context = owner_context(events, h, expected_owner)
    matches, unknown, active = [], [], {}
    for holder in snapshot['holders']:
        try:
            identity = source_identity(events, holder['source_pointer'], h)
        except ValueError as error:
            unknown.append(dict(source_pointer=holder['source_pointer'], reason=str(error)))
            continue
        if identity['key'] in active:
            raise ValueError('Geographical identity collision in current map')
        active[identity['key']] = identity
        if identity['key'] == target:
            matches.append((holder, identity))
    if len(matches) > 1:
        raise ValueError('Ambiguous target geography')
    # Geographic selection requires uniqueness. An unidentified occupied holder
    # might be another allocation of the same geography; it cannot be dismissed
    # solely because one positively identified target is already present.
    if unknown:
        raise ValueError('Unidentified occupied holders prevent unique geographical selection or absence')
    chosen, identity = matches[0] if matches else (None, None)
    construction = None if chosen is None else generation(events, identity, chosen['holder_pointer'], h)
    if chosen is not None and construction is None:
        raise ValueError('No positively joined consumed generation frame for resident holder')
    # Absence is a complete map/consumer observation, requiring no invented
    # construction. Its frame is qualified against the baseline at comparison.
    coordinate_frame = None if construction is None else construction['frame']
    if coordinate_frame is not None:
        frame(coordinate_frame)
    resources = [] if chosen is None else [dict(resource=r['resource'], regions=r['regions']) for r in chosen['resources']]
    value = dict(schema=SCHEMA, session_id=session_id, snapshot_id=str(h['snapshot']),
                 source=dict(key=target, body_formid=f"{h['owner_formid']:08x}"), frame=coordinate_frame,
                 capture=dict(complete=True, status='OK', resource_slots=len(resources),
                              region_total=sum(len(r['regions']) for r in resources),
                              point_total=sum(v['count'] for r in resources for v in r['regions'])),
                 availability=dict(boundary_qualified=True, map_scan_complete=True,
                                   holder_present=chosen is not None, exposed=chosen is not None),
                 generation_quality='UNKNOWN', loss=h['loss'], population=resources)
    normalize(value)
    proof = dict(source=identity, holder_pointer=None if chosen is None else chosen['holder_pointer'],
                 collection_pointers=[] if chosen is None else [r['collection_pointer'] for r in chosen['resources']],
                 collection_graph=[] if chosen is None else [
                     dict(resource=r['resource'], collection_pointer=r['collection_pointer'],
                          region_capacity=r['region_capacity'], region_data=r['region_data'],
                          regions=[dict(storage, count=region['count']) for storage, region in
                                   zip(r['region_storage'], r['regions'])]) for r in chosen['resources']],
                 header=h, unknown_other_holders=unknown,
                 owner_context=context,
                 generation=construction)
    return value, proof


def inspect(session, dll_hash, target, expected_owner=0x5e0de):
    validate_candidate_identity(load(Path(session) / 'identity.json'))
    transport = read_capture.inspect(session, dll_hash)
    sidecar = d5ai_read_geometry.read_session(session)
    terminal = transport.get('terminal') or {}
    if not transport['complete_session'] or transport['damage'] or terminal.get('drops', 0):
        raise ValueError('Lifecycle transport is incomplete, damaged or lossy')
    if sidecar['errors'] or sidecar['identity_sha256'] != transport['identity_sha256']:
        raise ValueError('Sidecar integrity/session mismatch')
    if (terminal.get('geometry_failed') is not False or terminal.get('geometry_no_slot') != 0 or
            terminal.get('geometry_completed') != len(sidecar['snapshots']) or
            terminal.get('geometry_captured') != terminal.get('geometry_completed')):
        raise ValueError('Sidecar worker/terminal accounting mismatch')
    lifetime = d5ai_read_lifetime.read_prefix(session, terminal)
    raw = (Path(session) / 'events.bin').read_bytes()
    events = [read_capture.decode(raw[i + 16:i + 328]) for i in range(0, len(raw), 328)]
    observations, refused = [], []
    for snapshot in sidecar['snapshots']:
        try:
            value, proof = envelope(snapshot, events, transport['identity_sha256'], target, expected_owner)
            proof['lifetime_coverage'] = d5ai_read_lifetime.qualify_snapshot(snapshot, lifetime)
            proof['process_identity'] = process_certificate(sidecar['lifecycle_identity'])
            qualify_construction(proof, lifetime)
            observations.append(dict(envelope=value, proof=proof, raw_sha256=snapshot['sha256']))
        except ValueError as error:
            refused.append(dict(snapshot_id=snapshot['header']['snapshot'], reason=str(error)))
    return dict(method=METHOD, session=str(session), session_id=transport['identity_sha256'], observations=observations,
                refused=refused, events=events, lifetime=lifetime, lifecycle_raw_sha256=transport['raw_sha256'],
                scope='Conditional on pinned ordinary native ownership and hook coverage; no retail occurrence inferred')


def qualify_construction(proof, lifetime):
    """Refuse ABA/mutation between the consumed construction and copied content."""
    construction = proof['generation']
    if construction is None:
        return
    start, stop = construction['return_ticks'], proof['header']['ticks_end']
    if lifetime['qualified_from_ticks'] > start:
        raise ValueError('Content lifetime coverage began after construction')
    holder, collections = proof['holder_pointer'], set(proof['collection_pointers'])
    ends = {(e['thread'], e['invocation']): e for e in lifetime['events'] if e['phase'] == 'END'}
    for event in lifetime['events']:
        if event['phase'] != 'BEGIN' or event['ticks'] > stop:
            continue
        end = ends.get((event['thread'], event['invocation']))
        if end is not None and end['ticks'] < start:
            continue
        if (event['kind'] == 'HOLDER_RESOURCE_MAP' and event['allocation'] == holder or
                event['kind'] in ('COLLECTION_GEOMETRY', 'COLLECTION_MUTATION') and event['allocation'] in collections):
            raise ValueError('Copied content overlaps ending or mutation after frame-qualified construction')


def relation(before, after, before_events, after_events, lifetime=None):
    # Source-aware comparison is qualified on controls only; Episode A has no A1.
    a, b = before['envelope'], after['envelope']
    ap, bp = before['proof'], after['proof']
    certificate = dict(qualified=False, loss=0, relation='UNKNOWN',
                       before=[a['session_id'], a['snapshot_id']], after=[b['session_id'], b['snapshot_id']])
    storage = d5ai_lifetime.evaluate(before, after, lifetime) if lifetime is not None else dict(
        qualified=False, state='UNKNOWN', reason='No authenticated lifetime journal supplied')
    certificate['prior_storage'] = storage
    if not bp['source']:
        return certificate
    same = a['session_id'] == b['session_id']
    process_a, process_b = ap.get('process_identity'), bp.get('process_identity')
    distinct_process = bool(process_a and process_b and
                            (process_a['pid'], process_a['creation_filetime']) !=
                            (process_b['pid'], process_b['creation_filetime']))
    certificate['process_relation'] = ('DISTINCT_PROCESSES' if distinct_process else
                                       'SAME_PROCESS' if process_a and process_a == process_b else 'UNQUALIFIED')
    if same and ap['source'] and ap['source']['allocation'] == bp['source']['allocation'] and ap['holder_pointer'] == bp['holder_pointer']:
        ah, bh = ap['header'], bp['header']
        if (storage['qualified'] and storage['holder']['state'] == 'SURVIVES' and
                all(c['state'] == 'SURVIVES' for c in storage['collections']) and
                ah['proc'] == bh['proc'] and ap['source']['owning_grid'] == bp['source']['owning_grid'] and
                ah['completion_ticks'] < bh['ticks_begin']):
            try:
                bridge = continuity(before_events, ah['completion_ticks'], bh['completion_ticks'],
                                    ah['epoch'], bh['epoch'], ap['source']['owning_grid'])
            except ValueError:
                pass
            else:
                certificate.update(qualified=True, relation='CONTINUOUS', source_continuity=bridge)
    elif bp['generation']:
        # Different process is decisive lifetime separation. In one process,
        # require the new construction to follow the earlier completed snapshot.
        if (not same and distinct_process or same and
                bp['generation']['ticks'] > ap['header']['completion_ticks']):
            certificate.update(qualified=True, relation='RECONSTRUCTED')
    return certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('--dll-sha256', required=True)
    parser.add_argument('--target', default='0:37536:20928:0029d20e')
    parser.add_argument('--owner-formid', default='0005e0de')
    parser.add_argument('--before-snapshot', required=True)
    parser.add_argument('--after-snapshot', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    owner = int(args.owner_formid, 16)
    first = inspect(args.before, args.dll_sha256, args.target, owner)
    second = first if args.before.resolve() == args.after.resolve() else inspect(args.after, args.dll_sha256, args.target, owner)
    find = lambda report, identifier: next(v for v in report['observations'] if v['envelope']['snapshot_id'] == identifier)
    a, b = find(first, args.before_snapshot), find(second, args.after_snapshot)
    certificate = relation(a, b, first['events'], second['events'], second['lifetime'])
    result = dict(result=compare(a['envelope'], b['envelope'], certificate), certificate=certificate,
                  before=a, after=b, lifecycle_hashes=[first['lifecycle_raw_sha256'], second['lifecycle_raw_sha256']],
                  method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    import json
    with args.out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(result['result']['outcome'])


if __name__ == '__main__':
    main()
