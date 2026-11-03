# SPDX-License-Identifier: GPL-3.0-or-later
"""Join stopped core construction paths to the versioned causal sidecar.

Reads supplied immutable session files and an externally pinned candidate DLL
identity, using owned core and causal readers. Writes one fresh D5AM-local JSON
derivative. Stdlib only; no process, save, database, deployment or network work.
SOR-P-0002 covers the reader reuse. This checks exact invocation/selection/source/
thread/lock joins, not full task readiness, source-lifetime completeness, retail
firstness, geometry semantics or a normal winner distribution. Refuses damaged
recordings; retains missing causal edges as explicit incomplete observations.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import argparse
import importlib.util
import json
from pathlib import Path
from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / 'runtime/construction-winner'


def load(name):
    spec = importlib.util.spec_from_file_location('d5am_join_' + name, RUNTIME / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def inspect(session, dll):
    sys.path.insert(0, str(RUNTIME))
    core = load('read_capture')
    causal = load('d5am_read_causal')
    original = core.inspect(session, dll)
    if not original['complete_session'] or original['damage'] or original['terminal']['drops']:
        raise ValueError('A complete lossless core is required for this stopped join')
    sidecar = causal.read(session, dll)
    identity=json.loads((Path(session)/'identity.json').read_bytes())
    scheduler=load('d5am_read_scheduler').read(session,dll) if identity.get('scheduler_schema')=='sor-d5am-scheduler/1' else None
    raw = (Path(session) / 'events.bin').read_bytes()
    events = [core.decode(raw[i + 16:i + 328]) for i in range(0, len(raw), 328)]
    birth = {}
    publications = set()
    observations = []
    for e in events:
        if e['kind'] == 14:
            birth[e['source']] = e
        elif e['kind'] == 15:
            # Published carries the source/Grid/destination, not the private
            # allocation counter. Bind the latest same-thread constructor
            # witness instead of treating Published.selection (zero) as an ID.
            origin=birth.get(e['source'])
            if origin and origin['thread']==e['thread'] and origin['sequence']<e['sequence'] and not (origin['status'] or e['status']):
                publications.add((e['source'], origin['selection']))
        elif e['kind'] == 4:
            context = (e['thread'], e['invocation'], e['selection'], e['source'])
            rows = [r for r in sidecar['events'] if
                    (r['thread'], r['invocation'], r['selection'], r['source']) == context and
                    r['lock'] == e['proc'] + 0x40]
            by_kind = {kind: [r for r in rows if r['kind'] == kind] for kind in (2, 3, 9, 10, 11)}
            issues = []
            for kind in (2, 3, 9, 10, 11):
                if len(by_kind[kind]) != 1:
                    issues.append('MISSING_OR_AMBIGUOUS_CAUSAL_KIND_' + str(kind))
            source = birth.get(e['source'])
            if source is None or (e['source'], source['selection']) not in publications:
                issues.append('SOURCE_PUBLICATION_UNAVAILABLE')
            if not sidecar['sidecar_accounting_complete']:
                issues.append('CAUSAL_ACCOUNTING_UNQUALIFIED')
            if e['status'] or e['hazards'] or any(r['status'] or r['hazards'] for r in rows):
                issues.append('CONTEXT_OR_LIFECYCLE_UNCERTAINTY')
            if len({r['generation'] for r in rows}) > 1:
                issues.append('OWNER_GENERATION_AMBIGUITY')
            generations={r['generation'] for r in rows}
            histories=[h for h in sidecar['histories'] if h['lock']==e['proc']+0x40 and h['generation'] in generations]
            if len(histories)!=1 or any(issue in histories[0]['issues'] for issue in (
                    'MISSING_OR_DUPLICATE_REGISTRATION','UNKNOWN_INITIAL_HOLDERS')):
                issues.append('OWNER_LIFETIME_HISTORY_UNQUALIFIED')
            if not issues:
                ordered = [by_kind[k][0] for k in (11, 9, 2, 3, 10)]
                if [r['sequence'] for r in ordered] != sorted(r['sequence'] for r in ordered):
                    issues.append('SAME_THREAD_CAUSAL_SITE_ORDER_INVALID')
                if any(a['ticks'] > b['ticks'] for a, b in zip(ordered, ordered[1:])) or ordered[-1]['ticks'] > e['ticks']:
                    issues.append('SAME_THREAD_SITE_CLOCK_REVERSED')
                if any(r['request'] != e['request'] for r in rows):
                    issues.append('ORIGINAL_REQUEST_CONTEXT_MISMATCH')
            path = [r for r in events if r['invocation'] == e['invocation'] and r['selection'] == e['selection']]
            samples = [r for r in path if r['kind'] == 7]
            stores = [r for r in path if r['kind'] == 17]
            task_issues=[];task_rows=[];task_births=[]
            if scheduler is None:
                task_issues.append('NO_SCHEDULER_JOURNAL')
            else:
                task_rows=[r for r in scheduler['events'] if r['kind']==9 and
                           r['core_invocation']==e['invocation'] and r['thread']==e['thread']]
                if len(task_rows)!=1 or not task_rows[0]['allocation'] or task_rows[0]['status']:
                    task_issues.append('MISSING_OR_UNQUALIFIED_TYPED_PROVIDER_SCOPE')
                else:
                    task=task_rows[0]
                    task_births=[r for r in scheduler['events'] if r['kind']==1 and
                                 (r['node'],r['allocation'])==(task['node'],task['allocation'])]
                    if len(task_births)!=1 or task_births[0]['status'] or task_births[0]['sequence']>=task['sequence']:
                        task_issues.append('MISSING_OR_UNQUALIFIED_TYPED_PUBLICATION')
                    elif any(r['kind']==4 and (r['node'],r['allocation'])==(task['node'],task['allocation']) and
                             task_births[0]['sequence']<r['sequence']<task['sequence'] for r in scheduler['events']):
                        task_issues.append('TASK_RETIRED_BEFORE_PROVIDER')
                    if task['core_selection'] not in (0,e['selection']) or task['source'] not in (0,e['source']):
                        task_issues.append('TYPED_PROVIDER_CORE_CONTEXT_MISMATCH')
                    histories_for_task=[h for h in scheduler['histories'] if (h['node'],h['allocation'])==(task['node'],task['allocation'])]
                    if len(histories_for_task)!=1 or histories_for_task[0]['issues']:
                        task_issues.append('RECORDED_TYPED_TASK_HISTORY_UNQUALIFIED')
                    entries=[r for r in events if r['kind']==1 and r['invocation']==e['invocation'] and r['thread']==e['thread']]
                    if len(entries)!=1 or task['request']!=entries[0]['request']:
                        task_issues.append('MAPPED_WORKER_ORIGINAL_REQUEST_MISMATCH')
                if not scheduler['byte_accounting_complete']:
                    task_issues.append('SCHEDULER_ACCOUNTING_UNQUALIFIED')
            observations.append(dict(core_lookup=e['sequence'], invocation=e['invocation'], selection=e['selection'],
                thread=e['thread'], original_request=e['request'], source_key=core.source_key(source) if source else 'UNKNOWN',
                source_allocation=source['selection'] if source else 'UNKNOWN',
                result='MISS' if e['a'] == e['b'] else 'HIT', causal_events=[r['sequence'] for r in rows],
                direct_samples=[dict(sequence=r['sequence'], mask=r['a']) for r in samples],
                stored_events=[r['sequence'] for r in stores],
                boundary_join='JOINED' if not issues else 'INCOMPLETE', issues=issues,
                causal_qualification='INCONCLUSIVE',
                task_binding='JOINED' if not task_issues else 'INCOMPLETE',task_issues=task_issues,
                typed_task=[dict(allocation=r['allocation'],family=r['family'],task_request=r['request'],
                                 provider_scope_sequence=r['sequence']) for r in task_rows],
                owner_history_limits=histories[0]['issues'] if len(histories)==1 else ['UNKNOWN_OWNER_HISTORY']))
    return dict(schema='sor-d5am-causal-core-join/1', identity_sha256=original['identity_sha256'],
                core_sha256=original['raw_sha256'], causal_sha256=sidecar['raw_sha256'], dll_sha256=dll,
                observations=observations, joined=sum(r['boundary_join'] == 'JOINED' for r in observations),
                task_joined=sum(r['task_binding']=='JOINED' for r in observations),
                scheduler_sha256=scheduler['raw_sha256'] if scheduler else None,
                causal_histories=sidecar['histories'],
                sources={name: sha(RUNTIME / (name + '.py')) for name in ('read_capture', 'd5am_read_causal', 'd5am_read_scheduler','reduce_v3', 'reduce_v4')},
                limit='Exact recorded boundary association only. Geometry/lifetime, task completeness, cold-first, source-scoped invalidators and normal retail causality require their separate qualification.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('session', type=Path)
    p.add_argument('--dll-sha256', required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    target = args.out.absolute()
    if not target.resolve().is_relative_to(ROOT / '.local-work/d5am') or any(x.is_symlink() or x.is_junction() for x in (target, *target.parents)):
        raise ValueError('Fresh non-reparse D5AM-local derivative required')
    guard()
    result = inspect(args.session, args.dll_sha256)
    result['method_sha256'] = sha(__file__)
    guard()
    with target.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(observations=len(result['observations']), joined=result['joined'], out=str(target))))


if __name__ == '__main__':
    main()
