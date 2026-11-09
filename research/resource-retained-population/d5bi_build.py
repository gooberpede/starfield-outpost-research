# SPDX-License-Identifier: GPL-3.0-or-later
"""Revalidate sealed originals and write a fresh D5BI-local candidate.

Reuse owned D5AP/D5BH methods under SOR-P-0002. Reads the original archive,
loose retained roots and exact source locks. No original, game or Git writes.
"""
import argparse
import io
import json
from pathlib import Path
import zipfile

import d5ap_analyze as original
import d5bi_verify as verifier
from d5bh_verify import BIRTH_SLICES
from d5ai_read_geometry import read_session
from d5ai_read_lifetime import read_prefix
import d5am_read_scheduler
import d5an_read_causal
import d5an_read_counter
import read_capture

ARCHIVE_NAME = 'N2-evidence01.zip'
ASSET = 'SOR-D5BI-N2-projected-evidence-v1.zip'
PLAN = '0adf5c4613fbbefc8335e657e1e4cf1e8a8792e87a77aa98b6a6dac0a31a9dff'
EMITTER = 'd3900246e4f6826f520cd1d2e5617c44fd58f5fa61f054346b0b23cc63bbce3c'


def encoded(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('ascii') + b'\n'


def core_projection(event, padding):
    row = dict(event)
    raw = bytes.fromhex(row.pop('source_bytes'))
    row['birth_fields'] = None
    if row['kind'] == 14:
        row['birth_fields'] = [raw[at:at+size].hex() for at, size in BIRTH_SLICES]
    else:
        verifier.require(not any(raw), 'Unexpected source object copy outside birth')
    desc = row['descriptor']
    row['descriptor'] = desc[:2] + desc[8:]
    row['pad_class'] = padding.setdefault(desc[2:8], len(padding))
    return row


def journal_bytes(channel, rows):
    fields = verifier.FIELDS[channel]
    header = dict(schema=verifier.SCHEMA, channel=channel, identity_sha256=verifier.IDENTITY, fields=fields)
    output = io.BytesIO(encoded(header))
    output.seek(0, 2)
    pad = {}
    for event in rows:
        row = core_projection(event, pad) if channel == 'core' else event
        output.write(encoded([row[k] for k in fields]))
    return output.getvalue()


def geometry_projection(raw, core):
    h = raw['header']
    fields = ('request snapshot proc epoch hazards loss ticks_begin ticks_end status map_capacity holders '
              'resources regions points lock_owner lock_state thread boundary consumer completion_ticks '
              'completion_epoch completion_hazards iterator scan_capacity scan_result manager owner_formid '
              'preunlock_seen lifetime_start lifetime_end').split()
    holders = []
    for row in raw['holders']:
        rs = row['resources']
        current = {k: row[k] for k in ('source_pointer', 'holder_pointer', 'resource_capacity')}
        current['counts'] = [len(rs), sum(len(r['regions']) for r in rs),
                             sum(region['count'] for r in rs for region in r['regions'])]
        source = verifier.source.source_identity(core, row['source_pointer'], h)
        if source['key'] == read_capture.TARGET:
            current['collections'] = [
                dict(resource=r['resource'], collection_pointer=r['collection_pointer'],
                     region_capacity=r['region_capacity'], region_data=r['region_data'],
                     regions=[dict(address=s['region_address'], point_capacity=s['point_capacity'],
                                   point_data=s['point_data'], count=g['count'])
                              for s, g in zip(r['region_storage'], r['regions'], strict=True)])
                for r in rs]
        holders.append(current)
    return dict(identity_sha256=verifier.IDENTITY, header={k: h[k] for k in fields}, holders=holders)


def load_original():
    guard = original.guard()
    seal, locators, plan, auth = original.authenticate()
    old = original.OLD
    with zipfile.ZipFile(old / ARCHIVE_NAME) as archive:
        names = archive.namelist()
        verifier.require(len(names) == len(set(names)) == 175 and
                         set(names) == {*locators, 'SOR-MANIFEST.json'} and
                         archive.read('SOR-MANIFEST.json') == (old / 'seal01.json').read_bytes() and
                         all(archive.getinfo(name).file_size == p['size'] for name, p in seal['files'].items()),
                         'Original archive inventory or embedded seal mismatch')
    verifier.require(seal['files']['plan/n2-plan.json']['sha256'] == PLAN and
                     plan['save52_sha256'] == verifier.SAVE and plan['dll_sha256'] == verifier.PROCESS['dll_sha256'],
                     'Original plan/baseline mismatch')
    session = Path(seal['roots']['raw']['path'])
    dll = plan['dll_sha256']
    # Reuse the accepted D5AP enrichment seam. Raw validation is unchanged.
    enrich = d5an_read_causal.registration_windows
    try:
        d5an_read_causal.registration_windows = lambda rows, issues: verifier.HistoryIndex(rows, issues).export()
        causal = d5an_read_causal.read(session, dll)
    finally:
        d5an_read_causal.registration_windows = enrich
    scheduler = d5am_read_scheduler.read(session, dll)
    core = read_capture.inspect(session, dll)
    terminal = core['terminal']
    lifetime = read_prefix(session, terminal)
    geometry = read_session(session)
    counter = d5an_read_counter.read(session, dll, plan['dll'])
    verifier.require(core['complete_session'] and not core['damage'] and core['identity_sha256'] == verifier.IDENTITY and
                     not core['firstness_refusals'] and causal['sidecar_accounting_complete'] and
                     causal['native_bridge_accounting_complete'] and not causal['reasons'] and
                     all(not h['issues'] for h in causal['histories']) and
                     scheduler['byte_accounting_complete'] and scheduler['native_bridge_accounting_complete'] and
                     not scheduler['coverage_refusals'] and lifetime['complete'] and not lifetime['loss'] and
                     counter['complete'] and not geometry['errors'] and len(geometry['snapshots']) == 1,
                     'Original channel integrity or coverage check failed')
    emitter = original.ROOT / '.local-work/d5ao/final05/candidate/runtime/construction-winner/d5am_causality.h'
    verifier.require(original.sha(emitter) == EMITTER and 'e.ticks=tick()' in emitter.read_text(encoding='utf8'),
                     'Original emitter timing premise changed')
    identity = geometry['lifecycle_identity']
    verifier.source.validate_candidate_identity(identity)
    raw = (session / 'events.bin').read_bytes()
    rows = [read_capture.decode(raw[i+16:i+328]) for i in range(0, len(raw), 328)]
    snapshot = geometry['snapshots'][0]
    value, proof = verifier.source.envelope(snapshot, rows, verifier.IDENTITY, read_capture.TARGET)
    verifier.source.qualify_construction(proof, lifetime)
    verifier.qualify_snapshot(snapshot, lifetime)
    certificate = dict(schema=verifier.SCHEMA, identity_sha256=core['identity_sha256'],
                       process={k: identity[k] for k in verifier.PROCESS}, baseline=verifier.BUILD,
                       terminal={k: terminal[k] for k in verifier.TERMINAL_FIELDS},
                       lifetime_mark=lifetime['coverage_mark'], lifetime_original_sha256=lifetime['raw_prefix_sha256'])
    return (certificate, snapshot, dict(core=rows, causal=causal['events'],
            scheduler=scheduler['events'], lifetime=lifetime['events']), value, proof, guard, seal, auth)


def build(out):
    certificate, snapshot, channels, value, proof, guard, seal, auth = load_original()
    projected_snapshot = geometry_projection(snapshot, channels['core'])
    members = {'session.json': encoded(certificate), 'geometry.json': encoded(projected_snapshot),
               **{k + '.jsonl': journal_bytes(k, v) for k, v in channels.items()}}
    result = verifier.interpret(*verifier.parse(members))
    verifier.require(result['retained']['source'] == proof['source'] and
                     result['retained']['generation'] == proof['generation'] and
                     result['retained']['owner'] == proof['owner_context'] and
                     result['retained']['counts'] == [value['capture'][k] for k in
                                                      ('resource_slots', 'region_total', 'point_total')],
                     'Projected snapshot differs from original attribution')
    original.guard()
    out.mkdir(exist_ok=False)
    package = out / ASSET
    with zipfile.ZipFile(package, 'x') as archive:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    inputs = {k: p for k, p in seal['files'].items() if k in (
        'raw/events.bin', 'raw/causal.bin', 'raw/scheduler.bin', 'raw/lifetimes.bin', 'raw/geometry-1.bin',
        'raw/geometry-1.json', 'raw/identity.json', 'raw/terminal.json', 'raw/ready.json', 'raw/flush.jsonl',
        'raw/lifetimes-flush.jsonl', 'plan/n2-plan.json', 'plan/d5ao-n2-source-lock.json')}
    manifest = dict(schema=verifier.SCHEMA,
                    candidate=dict(name=ASSET, bytes=package.stat().st_size, sha256=original.sha(package)),
                    members={k: dict(bytes=len(v), sha256=verifier.sha(v)) for k,v in sorted(members.items())},
                    source_members=inputs, source_archive=dict(name=ARCHIVE_NAME, bytes=61260786,
                        sha256=original.ARCHIVE, seal_sha256=original.SEAL, payloads=174),
                    source_lock_sha256=auth['source_lock_sha256'], source_pin_count=484,
                    emitter_sha256=EMITTER, interpretation_tier='PROJECTED_N2_EVENT_RELATIONSHIPS')
    original.write(out / 'manifest.json', manifest)
    original.write(out / 'original-reconciliation.json', dict(auth=auth, floors=guard, original_members=seal['files'],
        projected_members=manifest['members'], result=result, builder_sha256=original.sha(__file__),
        verifier_sha256=original.sha(verifier.__file__)))
    print(json.dumps(manifest['candidate'], indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('new_output', type=Path)
    args = parser.parse_args()
    out = args.new_output.absolute()
    root = original.ROOT / '.local-work/d5bi'
    verifier.require(out.parent == root and out.resolve().parent == root and not out.exists() and
                     not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)),
                     'Use a fresh direct child of .local-work/d5bi')
    build(out)


if __name__ == '__main__':
    main()
