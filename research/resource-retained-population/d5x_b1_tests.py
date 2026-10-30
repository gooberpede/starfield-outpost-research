# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise B1 reporting on authentic frozen captures and labelled derivatives.

Reads existing local native evidence and the unchanged DLL/reader manifests.
Writes only a fresh ignored audit test tree, damaged/semantic/scale derivatives,
SQLite spools and receipts. No native processes or live control writes. Original
captures stay untouched. Tracemalloc measures Python allocations, not total RSS.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tracemalloc
import zlib

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
BUILD = ROOT / '.local-work/d5x/build24'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_derivative(source, dest, rows, label):
    dest.mkdir()
    for name in ('identity.json', 'ready.json', 'terminal.json'):
        shutil.copyfile(source/name, dest/name)
    crc = 0
    with (dest/'events.bin').open('xb') as stream:
        for sequence, row in enumerate(rows, 1):
            row = dict(row, sequence=sequence)
            payload = struct.pack('<18Q2i', *(row[n] for n in decoder.NAMES), *row['request']) + bytes.fromhex(row['source_bytes']) + bytes.fromhex(row['descriptor']) + bytes(4)
            frame = struct.pack('<4I', 0x31505253, 312, sequence, zlib.crc32(payload)) + payload
            stream.write(frame)
            crc = zlib.crc32(frame, crc)
    count = sequence
    terminal = json.loads((dest/'terminal.json').read_text())
    for field in ('written','flushed','enqueued','enqueued_snapshot','dequeued_snapshot','acknowledged'):
        terminal[field] = count
    (dest/'terminal.json').write_text(json.dumps(terminal)+'\n', encoding='utf8', newline='\n')
    ack = dict(records=count, bytes=count*328, identity_sha256=sha(dest/'identity.json'), prefix_crc32=crc, drops=0)
    (dest/'flush.jsonl').write_text(json.dumps(ack)+'\n', encoding='utf8', newline='\n')
    (dest/'DERIVED.json').write_text(json.dumps(dict(classification='DERIVED_NOT_NATIVE_OBSERVATION', label=label, source=str(source)))+'\n', encoding='utf8', newline='\n')


def main():
    out = Path(sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT/'.local-work/d5x-b1-audit')
    out.mkdir(parents=True, exist_ok=False)
    reporter = load('audit_reporter', HERE/'d5x_b1_report.py')
    reporter_pin, test_pin = sha(HERE/'d5x_b1_report.py'), sha(__file__)
    global decoder
    decoder = reporter.decoder()
    manifest = json.loads((BUILD/'build.json').read_text())
    assert manifest['source_unchanged'] and len(manifest['cases']) == 56
    assert all(sha(BUILD/n)==digest for n,digest in manifest['outputs'].items())
    originals, negatives, memory = [], [], []
    expected = {'normal':1,'mask-zero':1,'prior-unknown':1,'edge':2,'corner':4,'nested':2,
                'ready-only':0,'source-absent':0,'selection-only':0,'visited':0,'map-hit':0,
                'skip-sample':0,'missing-descriptor':0,'in-flight-loss':0,'interrupt':0,
                'temporary-descriptor':0,'bad-read':0,'overlap-reset':0,'crash-sample':1,
                'crash-before':0,'crash-after':1,'loss-one':2,'loss-many':2,
                'missing-lookup':0,'missing-generator':0,'missing-sample':0,
                'clear':2,'destroy':2,'erase':2,'reused-pointer':2,'reset':2,
                'write-fault':1,'flush-fault':1,'ack-fault':1,'disk-fault':1,'ack-write-fault':1,
                'schedule-old-first':1,'schedule-fresh-first':1,'reset-closeout':1}
    exercised = set()
    for case, count in expected.items():
        result = reporter.report(BUILD/case, out/('original-'+case))
        ok = result['correlated_paths'] == count and len(result['sites']) == 14 and not result['native_absence_proven']
        if case == 'prior-unknown':
            frozen = decoder.inspect(BUILD/case, reporter.DLL)
            ok &= not frozen['chains'] and result['target_paths'] == 1
        if case == 'ready-only':
            ok &= result['evidence_grade'] == 'STARTUP_ONLY' and all(s['exercise']=='NOT_OBSERVED' for s in result['sites'])
        if case == 'crash-sample':
            ok &= not result['complete_transport'] and result['target_paths'] == 1
        if case == 'loss-many':
            ok &= result['aggregate_known_drops'] == 37
        exercised.update(s['site'] for s in result['sites'] if s['authenticated_witness_records'])
        originals.append(dict(case=case, passed=bool(ok), paths=result['correlated_paths'], outcomes=result['path_outcomes']))
    assert exercised == set(range(14)), 'NATIVE_FIXTURE_COVERAGE_MISSING_SITE'
    source = BUILD/'prior-unknown'
    raw = (source/'events.bin').read_bytes()
    warm = [decoder.decode(raw[n+16:n+328]) for n in range(0,len(raw),328)]
    for name in ('order','duplicate-descriptor','duplicate-generator','duplicate-sample','request','thread','parent','source','frame','epoch','pointer','branch','entry-missing','selection-missing','sample-missing','decision-epoch','map-source'):
        rows = copy.deepcopy(warm)
        event = lambda kind: next(e for e in rows if e['kind']==kind)
        if name=='order':
            a,b=rows.index(event(5)),rows.index(event(6));rows[a],rows[b]=rows[b],rows[a]
        elif name.startswith('duplicate-'):
            kind={'duplicate-descriptor':5,'duplicate-generator':6,'duplicate-sample':7}[name]
            e=event(kind);rows.insert(rows.index(e)+1,copy.deepcopy(e))
        elif name in ('request','thread','parent','source','frame','epoch'):
            if name=='request':event(7)['request'][0]+=1
            else:event(7)[name]+=1
        elif name=='pointer':event(7)['c']+=8
        elif name=='branch':event(3)['a']=1
        elif name=='entry-missing':rows.remove(event(1))
        elif name=='selection-missing':rows.remove(event(2))
        elif name=='sample-missing':rows.remove(event(7))
        elif name=='decision-epoch':event(4)['d']+=1
        elif name=='map-source':event(4)['c']+=8
        dest=out/('derived-'+name);write_derivative(source,dest,rows,name)
        result=reporter.report(dest,out/('report-'+name))
        negatives.append(dict(case=name, passed=result['correlated_paths']==0, outcomes=result['path_outcomes']))
    hit_raw=(BUILD/'map-hit/events.bin').read_bytes()
    hit=[decoder.decode(hit_raw[n+16:n+328]) for n in range(0,len(hit_raw),328)]
    for name,field in (('hit-source','c'),('hit-epoch','d')):
        rows=copy.deepcopy(hit);next(e for e in rows if e['kind']==4)[field]+=1
        dest=out/('derived-'+name);write_derivative(BUILD/'map-hit',dest,rows,name)
        result=reporter.report(dest,out/('report-'+name))
        negatives.append(dict(case=name,passed=result['path_outcomes']=={'CONTRADICTORY_MAP_OPERANDS_OR_DECISION_EPOCH':1},outcomes=result['path_outcomes']))
    def many_hits():
        yield from hit[:4]
        for invocation in range(1000):
            for event in hit[4:]:
                row=copy.deepcopy(event);row['invocation']+=invocation*10
                if row['selection']:row['selection']+=invocation*10
                yield row
    dest=out/'derived-many-hits';write_derivative(BUILD/'map-hit',dest,many_hits(),'many-admitted-records-without-downstream-path')
    result=reporter.report(dest,out/'report-many-hits')
    negatives.append(dict(case='many-hits',passed=result['correlated_paths']==0 and result['authenticated_records']>5000 and result['evidence_grade']=='PARTIAL_NATIVE_COVERAGE',outcomes=result['path_outcomes']))
    for mode in ('torn-frame','payload-flip','torn-ack','wrong-identity','bad-sequence','truncated-prefix'):
        folder=ROOT/'.local-work/d5x/qualification05'/mode
        try:
            result=reporter.report(folder,out/('damage-'+mode))
            negatives.append(dict(case=mode,passed=bool(result['damage']),damage=result['damage']))
        except ValueError as error:
            # A changed identity must refuse before interpreting any native bytes.
            negatives.append(dict(case=mode,passed=mode=='wrong-identity' and str(error)=='RECEIPT_IDENTITY_MISMATCH',refusal=str(error)))
    cli=subprocess.run([sys.executable,'-B',str(HERE/'d5x_b1_report.py'),str(source),str(out/'wrong-dll'),'--dll-sha256','0'*64],capture_output=True)
    negatives.append(dict(case='wrong-dll',passed=cli.returncode==2 and (out/'wrong-dll/refusal.json').exists()))
    cli=subprocess.run([sys.executable,'-B',str(HERE/'d5x_b1_report.py'),str(BUILD/'guard-mismatch'),str(out/'not-installed')],capture_output=True)
    negatives.append(dict(case='not-installed',passed=cli.returncode==2 and (out/'not-installed/refusal.json').exists()))
    ready_raw=(BUILD/'ready-only/events.bin').read_bytes()
    seed=decoder.decode(ready_raw[16:328])
    for count in (10000,40000):
        dest=out/f'derived-scale-{count}'
        write_derivative(BUILD/'ready-only',dest,(seed for _ in range(count)),f'scale-{count}')
        for method in ('frozen','streamed'):
            tracemalloc.start()
            if method=='frozen':result=decoder.inspect(dest,reporter.DLL);valid=result['complete_session']
            else:result=reporter.report(dest,out/f'scale-report-{count}');valid=result['complete_transport']
            _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            memory.append(dict(records=count,method=method,python_peak_bytes=peak,passed=valid))
    assert all(sha(BUILD/n)==digest for n,digest in manifest['outputs'].items())
    assert reporter_pin==sha(HERE/'d5x_b1_report.py') and test_pin==sha(__file__), 'AUDIT_SOURCE_CHANGED_DURING_TESTS'
    result=dict(schema='sor-d5x-b1-audit-tests/1', original=originals, negative=negatives, memory=memory,
                reporter_sha256=sha(HERE/'d5x_b1_report.py'),test_method_sha256=sha(__file__),
                frozen_build_sha256=sha(BUILD/'build.json'),frozen_reader_sha256=reporter.READER,
                passed=all(r['passed'] for r in originals+negatives+memory),
                limits='Existing native observations only; semantic and scale derivatives are labelled. No native rerun. Python peak excludes SQLite C allocations/OS cache/RSS.')
    (out/'tests.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=result['passed'],failures=[r for r in originals+negatives+memory if not r['passed']],memory=memory),indent=2))
    return 0 if result['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
