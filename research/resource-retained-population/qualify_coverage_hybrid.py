# SPDX-License-Identifier: GPL-3.0-or-later
"""Run D5O on disposable Windows siblings and assert exact coverage diagnostics.

Reads a pinned build; writes fresh ignored SRO1/ACK/control/reduction receipts.
Creates, attaches, suspends and patches only synthetic targets. Fault controls
alter DR0/DR7 or call GetThreadContext with a null handle; cleanup terminates
only those targets. No retail execution, downloads, original or Git writes.
"""
import json
import sys
from pathlib import Path
import hybrid
import qualify_hybrid

FAULTS = ('coverage-api-failure', 'coverage-dr0-loss', 'coverage-dr7-loss', 'coverage-dr7-type-loss', 'coverage-gd-return-fault')
MODES = (*qualify_hybrid.namespace['MODES'], 'coverage-stress', 'coverage-exit', 'coverage-exit-race', 'coverage-gd-sanitized', *FAULTS)
source = qualify_hybrid.source
source = hybrid.replace(source, "'hardware-loss','slot-pressure')",
                        "'hardware-loss','slot-pressure',*FAULTS)")
namespace = dict(__name__='d5o_qualification', __file__=qualify_hybrid.namespace['__file__'], FAULTS=FAULTS)
exec(compile(source, namespace['__file__']+'[D5O adapted]', 'exec'), namespace)
namespace['reduce'] = hybrid.reducer().reduce
namespace['MODES'] = MODES


def validate(case):
    control = [json.loads(s) for s in (case/'control.jsonl').read_text().splitlines()]
    events = [json.loads(s) for s in (case/'events.jsonl').read_text().splitlines()]
    registers = {r['thread_lifetime']: r for r in control if r['action']=='THREAD_REGISTER'}
    reads = [r for r in control if r['action']=='COVERAGE_READ']
    for row in reads:
        identity = registers[row['peer_lifetime']]
        assert identity['owned_handle']==row['owned_handle']
        assert (row['peer_tid'], row['peer_lifetime'], row['peer_birth']) == (
            identity['tid'], identity['thread_lifetime'], identity['birth'])
        assert row['owned'] and (row['suspended'] or row['peer_tid']==row['tid'])
        assert row['event']==1 and row['pid'] and row['process_creation']
        assert row['requested_flags'] & 0x100010 == 0x100010
        if row['api_ok']:
            assert not row['error_meaningful'] and row['error']==0
            assert all(k in row for k in ('context_flags','dr0','dr1','dr2','dr3','dr6','dr7','eflags','rip'))
            if row['failure']=='none':
                assert row['dr0']==row['expected_dr0'] and not any(row[k] for k in ('dr1','dr2','dr3'))
                assert row['dr7'] & 0xffff20ff == 1
        else:
            assert row['error_meaningful'] and row['error'] and row['failure']=='api'
            assert 'dr0' not in row
    mode = case.name
    if mode=='coverage-stress':
        resets = {r['debug_event_sequence'] for r in reads if r['site']==7}
        assert len(resets)==32
        for event in resets:
            found = [r for r in reads if r['debug_event_sequence']==event]
            fenced = {r['peer_lifetime'] for r in control if r['debug_event_sequence']==event and r['action']=='PEER_SUSPENDED'}
            assert len(fenced)>=96
            assert len(found)==len(fenced)+1 and len({r['peer_lifetime'] for r in found})==len(found)
            assert {r['peer_lifetime'] for r in found}==fenced|{found[0]['thread_lifetime']}
            assert all(r['failure']=='none' for r in found)
        assert sum(r.get('site')==10 and r['kind']=='SAMPLE' for r in events)>=33
        assert json.loads((case/'reduction.json').read_text())['chains']
    if mode=='coverage-exit':
        retired = [r for r in control if r['action']=='COVERAGE_EXITED']
        assert retired and any(r['action']=='FIXTURE_RETAIN_EXITED' for r in control)
        assert any(r['action']=='FIXTURE_RETAIN_EXITED' and r['exit_code']==259 for r in control)
        assert all(any(s['action']=='COVERAGE_STATE' and s['sequence']==r['sequence']-1 and s['wait']==0 for s in control) for r in retired)
        assert not any(s['debug_event_sequence']==r['debug_event_sequence'] and s['peer_lifetime']==r['peer_lifetime'] for r in retired for s in reads)
    if mode=='coverage-gd-sanitized':
        injection = next(r for r in control if r['action']=='COVERAGE_FAULT_INJECTED')
        read = next(r for r in reads if r['sequence']>injection['sequence'])
        assert read['api_ok'] and not read['dr7']&0x2000 and not read['synthetic_return_fault']
        assert read['failure']=='none'
    if mode in FAULTS:
        failed = [r for r in reads if r['failure']!='none']
        assert len(failed)==1 and failed[0]['site']==7
        row = failed[0]
        assert row['peer_tid']!=row['tid'] and row['suspended']
        expected = {'coverage-api-failure':'api','coverage-dr0-loss':'dr0','coverage-dr7-type-loss':'dr7','coverage-gd-return-fault':'gd'}
        if mode=='coverage-dr7-loss':
            assert row['failure']==('dr0' if row['dr0']!=row['expected_dr0'] else 'dr7')
        else:
            assert row['failure']==expected[mode]
        assert row['synthetic_return_fault']==(mode=='coverage-gd-return-fault')
        if mode=='coverage-api-failure':
            assert row['error']==6 and row['api_handle']==0
        else:
            assert row['api_ok'] and row['api_handle']==row['owned_handle']
            if mode=='coverage-dr0-loss': assert row['dr0']!=row['expected_dr0']
            elif mode=='coverage-dr7-loss': assert not (row['dr7']&1)
            elif mode=='coverage-dr7-type-loss': assert row['dr0']==row['expected_dr0'] and row['dr7']&0x10000
            else: assert row['dr7']&0x2000
        assert any(r['action']=='CONTROLLER_FATAL' and r['sequence']>row['sequence'] for r in control)
        assert not any(r['kind']=='SAMPLE' and r.get('site')==7 for r in events)
        assert any(r['kind']=='STOP_COMMITTED' for r in events)
    return dict(mode=mode,coverage_reads=len(reads),passed=True)


if __name__ == '__main__':
    code = namespace['main']()
    out = Path(sys.argv[2])
    results = [validate(case) for case in sorted(out.iterdir()) if (case/'control.jsonl').is_file()]
    (out/'coverage-checks.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8',newline='\n')
    raise SystemExit(code)
