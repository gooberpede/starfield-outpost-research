# SPDX-License-Identifier: GPL-3.0-or-later
"""Real-process qualification with a separately expressed synthetic oracle.

Executes only collect.py's guarded controller/fixture. Reads resulting native
receipts and compares independent expected ordered identities and decisions.
Writes exclusively a fresh run tree below repository .local-work; no cleanup.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import sys

from collect import collect, receipt, write, pin, ROOT, LOCAL


def oracle(mode, row):
    # Deliberately independent from target's arrays, memory ABI and filter loop.
    # This table never reaches the controller or target.
    populations = [[101, 202, 101], [303], [202, 303]]
    if mode == 'zero':
        populations[0] = []
    decision = row['site'] == 'sample_decision'
    selector, product = (([(0,101),(1,303),(2,202),(1,101)][row['depth']])
                         if decision else (0, 101))
    result = int(product in set(populations[selector]))
    return populations, selector, product, result


def inspect(folder, mode, expect_bad=False):
    rows = json.loads((folder/'events.json').read_text())
    session = next(r for r in rows if r['kind'] == 'SESSION')
    live, sequence, samples = {}, {}, []
    incomplete = []
    for row in rows:
        if row['kind'] == 'THREAD_BEGIN':
            assert row['tid'] not in live
            live[row['tid']] = row['lifetime']
        elif row['kind'] == 'THREAD_END':
            assert live.pop(row['tid']) == row['lifetime']
        elif row['kind'] == 'SAMPLE':
            samples.append(row)
            assert row['pid'] == session['pid'] and live[row['tid']] == row['thread_lifetime']
            token = row['thread_lifetime']
            sequence[token] = sequence.get(token, 0)+1
            assert row['thread_sequence'] == sequence[token]
            site = session['sites'][('sample_refresh', 'sample_retained', 'sample_decision').index(row['site'])]
            assert row['site_rva'] == site['rva'] and row['rip'] == session['module_base']+site['rva']
            if row['depth'] == 3:
                caller = row['return_va']-session['module_base']
                assert session['sites'][0]['rva'] <= caller < session['sites'][1]['rva']
            assert row['read_calls'] > 0 and row['read_bytes'] >= 136 and row['copy_ms'] <= 2000
            raw = bytes.fromhex(row['raw_evaluation'])
            values = struct.unpack('<17Q', raw)
            assert values[:4] == (0x433143534f525359, row['native_sequence'], row['visit'], row['depth'])
            assert values[-4:] == (row['selector'], row['produced'], row['result'], row['branch'])
            bad = any(p['status'] != 'COMPLETE' for p in row['populations'].values())
            if bad:
                incomplete.append(row)
                assert expect_bad
                assert row['populations']['spatial']['members'] is None
                continue
            pops, selector, product, result = oracle(mode, row)
            for i, tag in enumerate(('spatial', 'atmosphere', 'biome')):
                pop = row['populations'][tag]
                assert [m['id'] for m in pop['members']] == pops[i], (mode, tag, pop)
                pointers = list(struct.unpack('<'+'Q'*len(pops[i]), bytes.fromhex(pop['raw_pointer_bytes'])))
                assert pointers == [m['pointer'] for m in pop['members']]
                assert tuple(values[4+i*3:7+i*3]) == (pop['begin'], pop['end'], pop['capacity'])
                for m in pop['members']:
                    assert struct.unpack('<II', bytes.fromhex(m['raw'])) == (m['id'], 0x9f)
            assert (row['selector'], row['produced'], row['result']) == (selector, product, result)
            expected_fresh = {'sample_refresh':'THIS_REFRESH_REPLACED', 'sample_retained':'RETAINED_UNCHANGED_ID', 'sample_decision':'UNKNOWN'}
            assert row['freshness'] == expected_fresh[row['site']]
            if row['site'] == 'sample_refresh':
                assert row['branch'] == 1
            if row['site'] == 'sample_retained':
                assert row['branch'] == 2
    assert samples
    if expect_bad:
        assert len(incomplete) == 1
    else:
        assert not incomplete
        visits = {}
        for row in samples:
            visits.setdefault(row['visit'], []).append(row)
        for visit in visits.values():
            assert [(r['site'],r['depth']) for r in visit] == [('sample_refresh',0),('sample_decision',3),('sample_retained',0),
                ('sample_decision',0),('sample_decision',1),('sample_decision',2)]
            # The actual retained collection has the same bytes/pointer order, copied independently.
            assert visit[0]['populations'] == visit[2]['populations']
        assert set(r['native_sequence'] for r in samples) == set(range(1,len(samples)+1))
        resumes = [r for r in rows if r['kind'] == 'RESUME_VERIFIED']
        assert len(resumes) == len(samples)
    return dict(samples=len(samples), thread_lifetimes=len(sequence), visits=len({r['visit'] for r in samples}),
                thread_transitions=sum(x['tid']!=y['tid'] for x,y in zip(samples,samples[1:])),
                max_copy_ms=max(r['copy_ms'] for r in samples))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args(); output=a.output.resolve()
    assert output.is_relative_to(LOCAL.resolve())
    output.mkdir(parents=True, exist_ok=False)
    tests = []

    def test(name, fn):
        try:
            detail = fn(); tests.append(dict(name=name, status='PASS', detail=detail))
        except Exception as e:
            tests.append(dict(name=name, status='FAIL', error=repr(e)))
        write(output/f'{name}-test.json', tests[-1])
        print(name, tests[-1]['status'], flush=True)

    def normal(mode):
        path=output/mode
        r=collect(a.build,path,mode)
        assert r['acquisition'] == 'PASS' and r['controller_exit'] == 0
        detail=inspect(path,mode)
        assert detail['samples'] == (18 if mode=='threads' else 12)
        assert detail['thread_lifetimes'] == (3 if mode=='threads' else 1)
        if mode=='crash-after':
            assert r['target_exit']['code'] == 0xe043c1c1
            assert len(r['acknowledgements']) == 12
        else:
            assert r['target_exit']['code'] == 0
        return detail

    def negative(mode, fault='none'):
        name=mode if fault=='none' else fault
        path=output/name; r=collect(a.build,path,mode,fault)
        assert r['acquisition'] == 'FAIL' and r['controller_exit'] == 0
        if mode in ('bad-pointer','bad-count','overflow','budget','truncated','truncated-resource') or fault=='interrupt':
            detail=inspect(path,mode,expect_bad=True)
            bad=next(row for row in json.loads((path/'events.json').read_text()) if row['kind']=='SAMPLE' and row['populations']['spatial']['status']!='COMPLETE')
            expected={'bad-pointer':'pointer-read','bad-count':'range','overflow':'range','budget':'budget','truncated':'pointer-read','truncated-resource':'resource-read'}
            assert bad['populations']['spatial']['reason'] == expected.get(mode,'injected-interrupted-copy')
        else:
            detail=dict(captures=r['captures'],accepted_acknowledgements=len(r['acknowledgements']))
        if mode=='crash-before':
            assert r['target_exit']['code'] == 0xe043c1c0 and not r['acknowledgements']
        if fault in ('preack-stop','malformed'):
            assert not list(path.glob('*.ack.json'))
        return detail

    for mode in ('good','zero','threads','crash-after'):
        test(mode, lambda mode=mode:normal(mode))
    for mode in ('bad-pointer','bad-count','overflow','budget','truncated','truncated-resource','crash-before'):
        test(mode, lambda mode=mode:negative(mode))
    for fault in ('interrupt','drop','malformed','ackfail','preack-stop'):
        test(fault, lambda fault=fault:negative('good',fault))

    def stop():
        r=collect(a.build,output/'stop',limit=2)
        assert r['acquisition']=='PASS' and r['captures']==2 and len(r['acknowledgements'])==2
        assert r['target_exit']['stopped'] and r['target_exit']['code']==0xc1c0
        return 'Deliberate bounded STOP after verified ACK; target disposed.'
    test('stop',stop)

    def transport():
        p=subprocess.run([sys.executable,'-B',str(ROOT/'research/resource-ui-oracle/receipt_probe.py'),
                          '--self-test','--output',str(output/'c1b-transport')],capture_output=True,text=True)
        write(output/'transport-command.json',dict(command=p.args,code=p.returncode,stdout=p.stdout,stderr=p.stderr))
        assert p.returncode==0
        return 'Inherited eight tests: framing/digests/sequence/truncation/copy/budget/fsync/readback.'
    test('transport',transport)

    def isolation():
        try:
            collect(a.build,output/'forbidden-target',target=ROOT/'Starfield.exe')
        except AssertionError:
            assert not (output/'forbidden-target').exists()
        else:
            raise AssertionError('unallowlisted target accepted')
        p=subprocess.run([str(a.build.resolve()/'sor-c1c-controller.exe')],capture_output=True,text=True)
        assert p.returncode==2 and 'synthetic-only required' in p.stderr
        return dict(missing_guard_exit=p.returncode, wrong_target='refused before process creation')
    test('isolation',isolation)
    result=dict(tests=tests, passed=sum(t['status']=='PASS' for t in tests), total=len(tests),
                build_manifest_sha256=pin(a.build/'build.json'),
                source_sha256=pin(Path(__file__)), evidence='LOCAL-ONLY synthetic debug events and receipts')
    write(output/'qualification.json',result)
    return 0 if result['passed']==result['total'] else 1


if __name__=='__main__':
    raise SystemExit(main())
