# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute only hash-pinned disposable C2B fixtures, never Starfield.

Requires installed Windows MSVC-built fixture/controller and Python stdlib.
Reads build/source pins; creates a fresh ignored receipt directory. No save,
definition, config, Git, database or network writes. No cleanup of prior data.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-tungsten-acquisition'
sys.path.insert(0, str(ROOT / 'research/resource-oracle-retail'))
from collect import pin, persist, write


def independent(path):
    """Separate framing parser; does not call C1B decode or collector readers."""
    raw = path.read_bytes()
    rows = []
    at = 0
    while at < len(raw):
        magic, seq, n, digest = struct.unpack_from('<4sQI32s', raw, at)
        at += 48
        assert magic == b'SRO1' and seq == len(rows)+1 and n <= 1048576
        body = raw[at:at+n]
        at += n
        assert len(body) == n and hashlib.sha256(body).digest() == digest
        rows.append(json.loads(body))
    assert at == len(raw) and [r['kind'] for r in rows] == ['SESSION', 'SAMPLE', 'END']
    ack = json.loads(path.with_suffix('.ack.json').read_text())
    assert ack['sha256'] == hashlib.sha256(raw).hexdigest() and ack['bytes'] == len(raw)
    return rows


def preserve(folder, session, row):
    complete = row['required_reads_complete'] and all(row[k]['status'] == 'COMPLETE' for k in ('geometry', 'selected', 'refresh_payload', 'source_context') if k in row)
    complete &= all(row.get(k,True) for k in ('qb_retained_read','closure_read','descriptor_read'))
    path = folder / f'capture-{row["capture"]:05d}.bin'
    ack = persist(path, [session, row, dict(kind='END', complete=complete)], synthetic=True)
    assert independent(path)[1] == row
    return ack


def main():
    from admission import Tracker
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();build=a.build.resolve();out=a.output.resolve()
    assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest=json.loads((build/'build.json').read_text(encoding='utf8'))
    assert manifest['exit_code']==0
    for p,h in manifest['files'].items():assert pin(p)==h,p
    out.mkdir(exist_ok=False)
    modes=('good','indexed-query','retained-cache','unrelated-first','wrong-workshop','wrong-body','unrelated-source',
           'empty-transfer','stack-reuse','contention','pointer-reuse','stale-transfer','wrong-caller','chlorine-only','no-hit','short-circuit',
           'empty','partial','partial-page','context-partial','context-owner','invalid-source',
           'corrupt','oversized','byte-budget','source-budget','empty-collection','corrupt-collection',
           'invalid-collection','guard-mismatch','ackfail','partial-ack','dropped-ack','crash-before','crash-after',
           'nested','new-thread','threads','mixed','sources','source-reuse','reject','wrong-resource','nonfinite','multi','maximum')
    unit=subprocess.run([str(build/"sor-d4a-context_tests.exe")],capture_output=True)
    write(out/"context-tests.json",dict(exit=unit.returncode,stdout=unit.stdout.decode(),stderr=unit.stderr.decode()))
    assert unit.returncode==0
    results=[]
    positive={'indexed-query','good','retained-cache','unrelated-first','short-circuit','crash-after','nested','new-thread','threads','mixed','sources','source-reuse','multi','maximum','stack-reuse','new-thread'}
    for mode in modes:
        folder=out/mode;folder.mkdir();tracker=Tracker();rows=[];useful=[];session=None
        command=[str(build/'sor-d4a-fixture-controller.exe'),'--synthetic-fixture',pin(build/'sor-d4a-fixture.exe'),mode]
        p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        for line in p.stdout:
            row=json.loads(line);row['synthetic']=True;rows.append(row)
            if row['kind']=='SESSION':session=row
            if row['kind']=='SAMPLE':
                preserve(folder,session,row)
                yes=tracker.feed(row)
                if yes:useful.append(row['capture'])
                response='REJECT' if mode=='ackfail' else 'ACK' if mode=='partial-ack' else f'ACK {row["capture"]}'+(' STOP' if yes and mode not in ('short-circuit','threads','stack-reuse','contention','crash-after','new-thread','nested') else '')
                if mode=='dropped-ack':p.stdin.close()
                else:p.stdin.write(response+'\n');p.stdin.flush()
            else:tracker.feed(row)
        code=p.wait(timeout=15);stderr=p.stderr.read()
        write(folder/'events.json',rows);write(folder/'stderr.json',dict(text=stderr))
        errors=[]
        if mode!='contention' and bool(useful)!=(mode in positive):errors.append('scientific selector')
        if mode!='contention' and code!=(2 if mode=='guard-mismatch' else 0):errors.append('controller exit')
        samples=[r for r in rows if r['kind']=='SAMPLE']
        if mode=='unrelated-first' and (not any(r['site']=='generation_entry' for r in samples) or useful and useful[0]<=3):errors.append('premature generation success')
        if mode=='retained-cache' and any(r['site'].startswith('generation') for r in samples):errors.append('cache requires producer')
        if useful and not any(r['kind']=='ACK_ACCEPTED' and r['accepted'] and r['capture']==useful[-1] for r in rows):errors.append('durable STOP ACK')
        if mode=='stack-reuse' and len(useful)!=2:errors.append('stack epoch reuse')
        if mode=='threads' and len(useful)!=3:errors.append('thread lifetime reuse')
        decisions=[r for r in rows if r.get('decision')]
        phases=[r for r in rows if r['kind']=='PHASE']
        if samples and mode not in ('guard-mismatch','ackfail','partial-ack','dropped-ack'):
            if not phases or not phases[0]['consumer_mode'] and mode!='unrelated-first':errors.append('consumer phase entry')
        if mode in ('ackfail','partial-ack','dropped-ack'):
            if len(samples)!=1 or useful or not any(r['kind']=='ACK_ACCEPTED' and not r['accepted'] for r in rows) or not rows[-1].get('stopped'):errors.append('rejected transport/disposal')
        if mode in ('good','indexed-query','retained-cache','unrelated-first','stack-reuse','threads','short-circuit'):
            for d in decisions:
                shape=d['geometry'];raw=bytes.fromhex(shape['raw_region'])
                if raw[:16]!=struct.pack('<ffff',10,20,0,3):errors.append('bound byte oracle')
                # Thread fixture deliberately changes X after each completed evaluation.
                if mode!='threads' and shape['ordered_xyzw']!=struct.pack('<ffff',10,20,0,3).hex():errors.append('point byte oracle')
                if d['source_context']['source_grid_i32']!=[-12,0,10,10,2,2,14,14]:errors.append('source anchor oracle')
                if int.from_bytes(bytes.fromhex(d['raw_binding_extra'])[0x98:0xa0],'little')!=0x9b597027e0107ee0:errors.append('Workshop byte oracle')
                if d['selected']['source_wrapper']!=int.from_bytes(bytes.fromhex(d['source_context']['raw_manager'])[0x130:0x138],'little') and d['procgen']!=int.from_bytes(bytes.fromhex(d['source_context']['raw_manager'])[0x130:0x138],'little'):errors.append('procgen owner oracle')
                if d['qb_retained_bits']!=(struct.pack('<fff',100,0,0).hex() if mode=='indexed-query' else '00'*12):errors.append('query byte oracle')
            if mode=='short-circuit' and len(decisions)!=1:errors.append('short circuit is incomplete census')
        if mode=='new-thread' and (len(useful)!=2 or sum(p['consumer_mode'] for p in phases)!=1):errors.append('new thread inherits global phase')
        if mode=='nested' and sum(p['consumer_mode'] for p in phases)!=1:errors.append('nested mode retained')
        if mode=='indexed-query':
            if not decisions or decisions[0]['qb_retained_bits']==decisions[0]['raw_descriptor'][:24]:errors.append('indexed coordinate domains distinguished')
        incomplete={'partial','partial-page','corrupt','oversized','byte-budget','nonfinite'}
        if mode in incomplete and not any(d['geometry']['status']=='INCOMPLETE' for d in decisions):errors.append('geometry loss classification')
        if mode in ('context-partial','context-owner') and not any(d['source_context']['status']=='INCOMPLETE' for d in decisions):errors.append('source loss classification')
        if mode in ('wrong-workshop','wrong-body','unrelated-source','stale-transfer','pointer-reuse','chlorine-only','empty-transfer') and not samples:errors.append('negative did not execute')
        if mode=='crash-after' and not any(r['kind']=='EXCEPTION' and r['code']==0xe0c1e001 for r in rows):errors.append('post-capture failure not exercised')
        if mode=='crash-before' and (samples or not any(r['kind']=='EXCEPTION' for r in rows)):errors.append('pre-evidence failure')
        if mode=='contention' and code and not any(r['kind']=='LOSS' for r in rows):errors.append('slot contention unaccounted')
        results.append(dict(mode=mode,controller_exit=code,samples=len(samples),useful=useful,errors=errors,
                            events_sha256=pin(folder/'events.json')))
        print(mode,errors,flush=True)
    write(out/'summary.json',dict(build_sha256=pin(build/'build.json'),context_tests_exit=unit.returncode,cases=results,passed=all(not r['errors'] for r in results)))
    assert all(not r['errors'] for r in results),results

if __name__=='__main__':main()
