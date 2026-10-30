# SPDX-License-Identifier: GPL-3.0-or-later
"""Report fourteen-site B1 evidence independently of cold-winner qualification.

Reads a stopped/crashed session and the unchanged pinned D5X reader (decode only).
Streams raw/ACK authentication into a fresh local SQLite spool; writes JSON,
Markdown and exhaustive path JSONL only below a new ignored audit directory.
No native execution, repair of originals, live control writes, deployment, save,
network or Git effects. SQLite/CPython stdlib only. No total evidence-size cap.
"""
import argparse
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import struct
import zlib

ROOT = Path(__file__).resolve().parents[2]
DLL = '20160e2ccdf183c84baddae0214c0438eb471b3eb0ec34dee0632bb5880ddaeb'
READER = '1251527e82e39ff597c9921bcc4dfd9c9211575856cc08f64a2490c024ee978a'
NAMES = ('provider', 'selected', 'visited', 'lookup', 'converter_scope', 'generator',
         'sampler_return', 'reset', 'destroy', 'erase', 'grid_clear', 'retire',
         'reset_unlock', 'normalizer_consumption')
SITE_KINDS = ((1, 9), (2,), (3,), (4,), (5,), (6, 8), (7,),
              (10, 11), (10, 11), (10, 11), (10, 11), (10, 11), (12,), (5,))
FRAME = 328


def disk_guard():
    for drive in ('C:/', 'D:/'):
        available = ctypes.c_ulonglong()
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), ctypes.byref(available), None, None):
            raise OSError('DISK_QUERY_FAILED:' + drive)
        if available.value < 40_000_000_000 + 16 * 1024 * 1024:
            raise OSError('DISK_FLOOR_OR_ANALYSIS_RESERVE:' + drive)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def metadata(path):
    # Actual worker metadata is fixed-shape and below this parser allocation bound.
    # This rejects malformed metadata, not a session's raw volume or duration.
    with Path(path).open('rb') as stream:
        raw = stream.read(65537)
    if len(raw) > 65536:
        raise ValueError('METADATA_SHAPE_TOO_LARGE')
    return json.loads(raw), raw


def decoder():
    path = ROOT / 'runtime/construction-winner/read_capture.py'
    if sha(path) != READER:
        raise ValueError('FROZEN_READER_MISMATCH')
    spec = importlib.util.spec_from_file_location('frozen_decode', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference(event):
    return dict(sequence=event['sequence'], kind=event['kind'], ticks=event['ticks'])


def path_result(entry, entry_count, records, module):
    """Use bounded boundary state; a cold certificate is deliberately not required."""
    counts = {k: 0 for k in range(2, 8)}
    first = {}
    context_bad = bool(entry and (entry['status'] or entry['hazards']))
    invalid_ref = dict(reference(entry), status=entry['status'], hazards=entry['hazards'], reasons=['entry_status_or_hazard']) if context_bad else None
    for event in records:
        k = event['kind']
        if k not in counts:
            continue
        counts[k] += 1
        first.setdefault(k, event)
        problems = []
        if entry:
            problems += ['entry.'+n for n in ('invocation','proc','request','thread','parent','epoch') if event[n]!=entry[n]]
        selected = first.get(2)
        if selected:
            problems += ['selection.'+n for n in ('source','frame','selection') if event[n]!=selected[n]]
        if event['status']:
            problems.append('native_status')
        if event['hazards']:
            problems.append('lifecycle_hazard')
        context_bad |= bool(problems)
        if problems and invalid_ref is None:
            invalid_ref = dict(reference(event), status=event['status'], hazards=event['hazards'], reasons=problems)
    result = dict(invocation=entry['invocation'] if entry else next(iter(first.values()), {}).get('invocation'),
                  selection=first.get(2, {}).get('selection'),
                  evidence=[reference(first[k]) for k in sorted(first)],
                  cold_winner_qualification='NOT_EVALUATED_BY_B1_REPORTER',
                  target=False)
    if entry:
        result['entry'] = reference(entry)
        result['request'] = entry['request']
        context_bad |= bool(entry['status'] or entry['hazards'])
    reason = None
    if not entry:
        reason = 'MISSING_ORIGINAL_REQUEST_INDETERMINATE'
    elif entry_count != 1:
        reason = 'CONTRADICTORY_ENTRY_MULTIPLICITY'
    elif context_bad:
        reason = 'INVALID_EXERCISED_CONTEXT'
    elif any(n > 1 for n in counts.values()):
        reason = 'CONTRADICTORY_BOUNDARY_MULTIPLICITY'
    elif not first:
        reason = 'PROVIDER_ONLY_SELECTION_NOT_OBSERVED'
    elif 2 not in first:
        reason = 'MISSING_SELECTION_INDETERMINATE'
    elif 3 not in first:
        reason = 'MISSING_VISITED_INDETERMINATE'
    elif first[3]['a']:
        reason = 'EXPECTED_VISITED_BYPASS'
    elif 4 not in first:
        reason = 'MISSING_LOOKUP_INDETERMINATE'
    elif first[4]['c'] != first[2]['source'] or first[4]['d'] != entry['epoch']:
        reason = 'CONTRADICTORY_MAP_OPERANDS_OR_DECISION_EPOCH'
    elif first[4]['a'] != first[4]['b']:
        reason = 'EXPECTED_MAP_HIT'
    elif 5 not in first:
        reason = 'MISSING_CONVERTER_OR_NORMALIZER_INDETERMINATE'
    elif first[5]['d'] != first[5]['holder'] + 0xc8:
        reason = 'DESCRIPTOR_FRAME_CONTEXT_UNQUALIFIED'
    elif 6 not in first:
        reason = 'MISSING_GENERATOR_INDETERMINATE'
    elif 7 not in first:
        reason = 'MISSING_SAMPLER_RETURN_PREREQUISITE_OR_LOSS_UNKNOWN'
    elif first[7]['a'] > 15:
        reason = 'SAMPLE_OUTSIDE_ORDINARY_NIBBLE'
    elif first[7]['c'] != first[6]['c']:
        reason = 'CONTRADICTORY_GEOGRAPHIC_POINTER'
    if reason == 'EXPECTED_VISITED_BYPASS' and any(k in first for k in range(4, 8)):
        reason = 'CONTRADICTORY_BRANCH_ACTIVITY'
    if reason == 'EXPECTED_MAP_HIT' and any(k in first for k in range(5, 8)):
        reason = 'CONTRADICTORY_BRANCH_ACTIVITY'
    # Validate observed prefix order even if a later boundary is absent/bypassed.
    observed = [entry['sequence']] if entry else []
    observed += [first[k]['sequence'] for k in range(2, 8) if k in first]
    if entry and not context_bad and observed != sorted(set(observed)):
        reason = 'CONTRADICTORY_BOUNDARY_ORDER'
    if reason is None:
        reason = 'CORRELATED_ORDINARY_PATH_NO_COLD_REQUIREMENT'
        result.update(mask=first[7]['a'], source_key=module.source_key(first[4]),
                      owner=first[6]['a'], target=module.source_key(first[4]) == module.TARGET and first[6]['a'] == 0x5e0de)
    result.update(outcome=reason, correlated=reason == 'CORRELATED_ORDINARY_PATH_NO_COLD_REQUIREMENT',
                  first_invalid_reference=invalid_ref,
                  absence_proven=False, hook_failure_demonstrated=False)
    if reason == 'CONTRADICTORY_MAP_OPERANDS_OR_DECISION_EPOCH':
        result['map_contradiction'] = dict(reference(first[4]), actual_source=first[4]['c'],
            selected_source=first[2]['source'], actual_epoch=first[4]['d'], invocation_epoch=entry['epoch'])
    result['explanation'] = ('Authenticated local path; cold/winner and operational PASS are separate.' if result['correlated'] else
        'Observed branch bypasses downstream construction for this selection.' if reason in ('EXPECTED_VISITED_BYPASS','EXPECTED_MAP_HIT') else
        'An exercised context contradicts correlation; inspect the first invalid reference, not a presumed hook cause.' if reason=='INVALID_EXERCISED_CONTEXT' else
        'Boundary evidence is contradictory; no complete path is established.' if reason.startswith('CONTRADICTORY') else
        'The named prerequisite is not established; native branch, capture loss and unsupported context may remain inseparable.')
    return result


def report(folder, out, expected_dll=DLL):
    folder, out = Path(folder).resolve(), Path(out).resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5x-b1-audit'):
        raise ValueError('OUTPUT_MUST_BE_FRESH_IGNORED_AUDIT_DIRECTORY')
    out.mkdir(parents=True, exist_ok=False)
    disk_guard()
    module = decoder()
    identity, identity_bytes = metadata(folder / 'identity.json')
    if identity.get('schema') != 'sor-d5x/2' or identity.get('dll_sha256') != expected_dll or expected_dll != DLL:
        raise ValueError('WRONG_DLL_OR_SCHEMA')
    if [s['index'] for s in identity['sites']] != list(range(14)):
        raise ValueError('FOURTEEN_SITE_IDENTITY_REQUIRED')
    if not isinstance(identity.get('nonce'), str) or len(identity['nonce']) != 64 or any(c not in '0123456789abcdef' for c in identity['nonce']):
        raise ValueError('STARTUP_NONCE')
    origin = identity.get('sequence_origin', 0)
    if not isinstance(origin, int) or not 0 <= origin < 2**63 or (identity['retail'] and origin):
        raise ValueError('SEQUENCE_ORIGIN')
    terminal = metadata(folder / 'terminal.json')[0] if (folder / 'terminal.json').exists() else None
    ready = metadata(folder / 'ready.json')[0] if (folder / 'ready.json').exists() else None
    for receipt in (terminal, ready):
        if receipt and not all(receipt.get(k) == v for k, v in identity.items()):
            raise ValueError('RECEIPT_IDENTITY_MISMATCH')
    installed = bool(ready and ready.get('ready') is True and ready.get('hooks') == 14)
    if identity['retail']:
        baseline = json.loads((ROOT / '.local-work/d5x/compatibility01.json').read_text())
        for site, (rva, pin) in zip(identity['sites'], baseline['sites'].items()):
            if site.get('rva') != int(rva, 16) or site.get('va') != identity['module_base'] + int(rva, 16) or site['guard_sha256'] != pin['raw_sha256']:
                raise ValueError('RETAIL_SITE_GUARD_IDENTITY')
        if identity.get('host_sha256') != next(v for k, v in baseline['installed'].items() if k.endswith('Starfield.exe')) or identity.get('sfse_sha256') != next(v for k, v in baseline['installed'].items() if k.endswith('sfse_1_16_244.dll')):
            raise ValueError('RETAIL_HOST_IDENTITY')
    db = sqlite3.connect(out / 'events.sqlite')
    db.execute('PRAGMA cache_size=-2048')
    db.execute('PRAGMA temp_store=FILE')
    db.execute('CREATE TABLE e(seq INTEGER PRIMARY KEY,k INTEGER,inv TEXT,sel TEXT,a TEXT,status INTEGER,hazards INTEGER,data TEXT)')
    # Maintain the index during guarded ingestion; avoid an unguarded bulk sort.
    db.execute('CREATE INDEX invocation_selection ON e(inv,sel,seq)')
    damage = []
    parsed = durable = rolling = 0
    last_ack = None
    identity_hash = hashlib.sha256(identity_bytes).hexdigest()
    with (folder / 'flush.jsonl').open('rb') as ack_stream, (folder / 'events.bin').open('rb') as raw_stream:
        def next_ack():
            line = ack_stream.readline(65537)
            if not line:
                return None
            try:
                if len(line) > 65536 or not line.endswith(b'\n'):
                    raise ValueError('TORN_OR_OVERSIZED_ACK')
                value = json.loads(line)
                if value['identity_sha256'] != identity_hash or value['bytes'] != value['records'] * FRAME or value['records'] < 0:
                    raise ValueError('ACK_IDENTITY_OR_LENGTH')
                return value
            except (ValueError, KeyError, TypeError) as error:
                damage.append('ACK_INTEGRITY:' + str(error))
                return None
        ack = next_ack()
        while True:
            while ack is not None and ack['records'] == parsed:
                if ack['prefix_crc32'] != rolling:
                    damage.append('ACK_PREFIX_CRC')
                    ack = None
                    break
                if terminal is None or parsed <= terminal['acknowledged']:
                    durable, last_ack = parsed, ack
                previous = parsed
                ack = next_ack()
                if ack is not None and ack['records'] < previous:
                    damage.append('ACK_REGRESSION')
                    ack = None
            raw = raw_stream.read(FRAME)
            if not raw:
                break
            if len(raw) != FRAME:
                damage.append('TORN_FRAME')
                break
            magic, size, low, checksum = struct.unpack_from('<4I', raw)
            event = module.decode(raw[16:])
            if magic != 0x31505253 or size != 312 or low != ((origin + parsed + 1) & 0xffffffff) or event['sequence'] != origin + parsed + 1 or zlib.crc32(raw[16:]) != checksum or event['kind'] not in range(1, 14):
                damage.append('FRAME_INTEGRITY_OR_SEQUENCE')
                break
            parsed += 1
            if event['sequence'] >= 2**63:
                damage.append('ADMISSION_COUNTER_DOMAIN')
                break
            rolling = zlib.crc32(raw, rolling)
            db.execute('INSERT INTO e VALUES(?,?,?,?,?,?,?,?)', (event['sequence'], event['kind'], str(event['invocation']), str(event['selection']), str(event['a']), event['status'], event['hazards'], json.dumps(event)))
            if parsed % 128 == 0:
                db.commit()
                disk_guard()
        if ack is not None:
            damage.append('ACK_BEYOND_VALID_PREFIX')
    db.commit()
    limit = origin + durable
    path_counts, correlated = {}, 0
    target_paths = 0
    with (out / 'paths.jsonl').open('x', encoding='utf8', newline='\n') as stream:
        for (inv,) in db.execute('SELECT DISTINCT inv FROM e WHERE seq<=? AND inv<>\'0\'', (limit,)):
            row = db.execute('SELECT data FROM e WHERE seq=(SELECT min(seq) FROM e WHERE inv=? AND k=1 AND seq<=?)', (inv, limit)).fetchone()
            entry = json.loads(row[0]) if row else None
            entry_count = db.execute('SELECT count(*) FROM e WHERE inv=? AND k=1 AND seq<=?', (inv, limit)).fetchone()[0]
            selections = db.execute('SELECT DISTINCT sel FROM e WHERE inv=? AND sel<>\'0\' AND seq<=?', (inv, limit))
            had_selection = False
            for (selection,) in selections:
                had_selection = True
                records = (json.loads(r[0]) for r in db.execute('SELECT data FROM e WHERE inv=? AND sel=? AND seq<=? ORDER BY seq', (inv, selection, limit)))
                result = path_result(entry, entry_count, records, module)
                stream.write(json.dumps(result) + '\n')
                path_counts[result['outcome']] = path_counts.get(result['outcome'], 0) + 1
                if sum(path_counts.values()) % 128 == 0:
                    disk_guard()
                correlated += result['correlated']
                target_paths += result['correlated'] and result['target']
            if not had_selection and entry:
                result = path_result(entry, entry_count, (), module)
                stream.write(json.dumps(result) + '\n')
                path_counts[result['outcome']] = path_counts.get(result['outcome'], 0) + 1
                if sum(path_counts.values()) % 128 == 0:
                    disk_guard()
    sites = []
    known_loss = max((r.get('drops', 0) for r in (terminal, last_ack) if r), default=0)
    for site, name in enumerate(NAMES):
        disk_guard()
        kinds = SITE_KINDS[site]
        condition = 'k IN (' + ','.join(map(str, kinds)) + ')'
        if 7 <= site <= 11:
            condition += f" AND a='{site-7}'"
        count, minimum, maximum = db.execute(f'SELECT count(*),min(seq),max(seq) FROM e WHERE {condition} AND seq<=?', (limit,)).fetchone()
        tail = db.execute(f'SELECT count(*) FROM e WHERE {condition} AND seq>?', (limit,)).fetchone()[0]
        invalid = db.execute(f'SELECT count(*) FROM e WHERE {condition} AND seq<=? AND status<>0', (limit,)).fetchone()[0]
        hazard_fail = 'hazards<>0' if site not in (7,8,9,10,11,12) else '0'
        bad_row = db.execute(f'SELECT data FROM e WHERE {condition} AND seq<=? AND (status<>0 OR {hazard_fail}) ORDER BY seq LIMIT 1', (limit,)).fetchone()
        bad = json.loads(bad_row[0]) if bad_row else None
        sites.append(dict(site=site, name=name, installation='GUARD_VERIFIED_READY' if installed else 'NOT_ESTABLISHED',
                          exercise='POSITIVELY_WITNESSED' if count else 'UNACKNOWLEDGED_TAIL_ONLY' if tail else 'NOT_OBSERVED',
                          witness='INDIRECT_CONVERTER_AND_NORMALIZER' if site == 4 else 'RETURN_SIDE' if site == 6 else 'DIRECT',
                          authenticated_witness_records=count, parsed_unacknowledged_records=tail,
                          first_sequence=minimum, last_sequence=maximum, status_failure_records=invalid,
                          first_invalid_reference=dict(reference(bad), status=bad['status'], hazards=bad['hazards']) if bad else None,
                          correlated_complete_paths=correlated if site in (0,1,2,3,4,5,6,13) else None,
                          missing_reason='INDETERMINATE_NOT_PER_SITE_LOSS_OR_EXECUTION_COUNTER',
                          per_site_loss_count=None, native_absence_proven=False, hook_failure_demonstrated=False))
    orphan = db.execute('SELECT count(*) FROM e WHERE inv=\'0\' AND k BETWEEN 2 AND 8 AND seq<=?', (limit,)).fetchone()[0]
    success = bool(terminal and not terminal['failed'])
    complete = bool(success and not damage and durable == terminal['written'] == terminal['flushed'] == terminal['acknowledged'] and terminal['enqueued'] == origin + durable and (folder/'events.bin').stat().st_size == durable * FRAME)
    hook_fault = bool(terminal and terminal.get('output_fault') in ('hook_guard','relay_guard','target_guard'))
    invalid_paths = sum(count for name,count in path_counts.items() if name=='INVALID_EXERCISED_CONTEXT' or name.startswith('CONTRADICTORY'))
    if hook_fault:
        for site in sites:
            site['hook_failure_demonstrated'] = 'AGGREGATE_HOOK_INTEGRITY_FAILURE_NOT_SITE_LOCALIZED'
    grade = 'ENGINEERING_FAILURE_OR_UNCERTAINTY' if damage or (terminal and terminal['failed']) or not installed or (invalid_paths and not target_paths) else 'CORRELATED_PATH_PREFIX' if target_paths else 'PARTIAL_NATIVE_COVERAGE' if any(s['authenticated_witness_records'] for s in sites) else 'STARTUP_ONLY'
    result = dict(schema='sor-d5x-b1-coverage/1', source_session=str(folder), retail=identity['retail'],
                  dll_sha256=expected_dll, reporter_sha256=sha(__file__), frozen_reader_sha256=READER,
                  identity_sha256=identity_hash, raw_sha256=sha(folder/'events.bin'), flush_sha256=sha(folder/'flush.jsonl'),
                  sequence_origin=origin, parsed_records=parsed, authenticated_records=durable, damage=damage, terminal_success=success,
                  complete_transport=complete, aggregate_known_drops=known_loss, loss_site_assignment='UNAVAILABLE',
                  orphan_authenticated_records=orphan, sites=sites, path_outcomes=path_counts,
                  correlated_paths=correlated, target_paths=target_paths, evidence_grade=grade,
                  invalid_context_or_contradictory_paths=invalid_paths,
                  engineering_context_review='REQUIRED' if invalid_paths else 'NO_CORRELATION_FAILURE_OBSERVED',
                  b1_final_disposition='OPERATIONAL_AND_INDEPENDENT_REVIEW_REQUIRED' if identity['retail'] else 'DISPOSABLE_FIXTURE_ONLY',
                  full_b1_pass=False, full_b1_gate='LOCAL_PATH_EVIDENCE_ONLY; FRESH_CHALLENGE, RETAIL_PHASES, PROTECTION, STOP/POSTFLIGHT AND INDEPENDENT_GRADING_REQUIRED',
                  startup_identity_and_challenge_check='SEPARATE_REQUIRED_GATE',
                  protection_and_gameplay_completion='SEPARATE_REQUIRED_GATE',
                  scientific_winner='NOT_EVALUATED', native_absence_proven=False,
                  limits=['No per-site execution/drop counters; silent sites remain indeterminate.',
                          'Site 4 and site 13 failure cannot be separated by absent Descriptor.',
                          'SQLite disk spool and streamed path output; no full raw/event list in RAM.',
                          'CRC plus externally pinned identities detect damage, not malicious forgery.'])
    (out/'coverage.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')
    lines = ['# D5X-B1 observed boundary coverage', '', f'Evidence: {grade}. Final B1: {result["b1_final_disposition"]}.', '',
             f'Authenticated records: {durable}; correlated ordinary paths: {correlated}; target paths: {target_paths}.',
             f'Known aggregate drops: {known_loss}; complete transport: {complete}. No native absence proof.', '',
             '| Site | Installed | Exercise | Authenticated / tail | Native status failures |', '|---|---|---|---|---|']
    lines += [f'| {s["site"]} {s["name"]} | {s["installation"]} | {s["exercise"]} | {s["authenticated_witness_records"]} / {s["parsed_unacknowledged_records"]} | {s["status_failure_records"]} |' for s in sites]
    lines += ['', 'Path outcomes (exhaustive references in paths.jsonl):', '']
    lines += [f'- {name}: {count}.' for name, count in path_counts.items()]
    lines += ['', 'Missing Descriptor cannot distinguish site 4 from site 13. Sampler evidence is return-side.',
              'Bypass/hit describe particular observed paths; silence elsewhere remains INDETERMINATE.',
              'A cold first-construction winner is neither required nor inferred for this B1 report.', '']
    (out/'coverage.md').write_text('\n'.join(lines), encoding='utf8', newline='\n')
    db.close()
    disk_guard()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('session', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--dll-sha256', default=DLL)
    args = parser.parse_args()
    try:
        result = report(args.session, args.output, args.dll_sha256)
        print(json.dumps(dict(grade=result['evidence_grade'], correlated_paths=result['correlated_paths'], output=str(args.output)), indent=2))
    except (ValueError, KeyError, OSError, TypeError) as error:
        # Refusal is observable diagnostic output; it never becomes trusted coverage.
        result = dict(schema='sor-d5x-b1-refusal/1', evidence_grade='ENGINEERING_FAILURE_OR_UNCERTAINTY',
                      reason=str(error), sites=[dict(site=i, installation='NOT_ESTABLISHED', exercise='NOT_OBSERVED',
                              native_absence_proven=False) for i in range(14)])
        output = args.output.resolve()
        if not isinstance(error, FileExistsError) and output.is_relative_to(ROOT/'.local-work/d5x-b1-audit') and output.exists() and not (output/'coverage.json').exists():
            (output/'refusal.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')
        print(json.dumps(result, indent=2))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
