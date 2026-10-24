# SPDX-License-Identifier: GPL-3.0-or-later
"""D3 offline investigation stages; run from repository root with CPython.

Reads existing D1/D2 evidence and pinned installed definitions. Writes exclusive
ignored receipts and new authored summaries only. No target or analysis-project
effects, dependencies, network, staging or modification of protected inputs.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import save52 as s

OUT = s.ROOT / '.local-work/resource-save52-d3'
DOC = s.ROOT / 'docs/experiments/resource-save52-d3'


def freeze():
    """Freeze the original acceptance text and immutable input inventories."""
    s.guard()
    OUT.mkdir(exist_ok=False)
    brief = s.ROOT / 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D3_save52_discrepancies_coverage.md'
    text = brief.read_text(encoding='utf8')
    DOC.mkdir(exist_ok=False)
    contract = text[text.index('### 6. Frozen acceptance contract'):text.index('### 7. Stop/return')]
    (DOC/'contract.md').write_bytes(('# D3 frozen contract\n\n'+contract).encode())
    s.write(OUT/'baseline.json', dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
        index_sha256=s.builder.pin(s.ROOT/'.git/index'),
        status=subprocess.check_output(['git','status','--short']).decode().strip(), brief_sha256=s.builder.pin(brief)))
    import protection
    audit = protection.audit()
    s.write(OUT/'protected-before.json', audit)
    if audit['changes']:
        raise ValueError('PROTECTION_FAILURE')
    paths = set()
    for root in ('resource-standalone','resource-save52'):
        paths.update(p for p in (s.ROOT/'.local-work'/root).rglob('*') if p.is_file())
    for root in ('resource-standalone','resource-save52','resource-geometry','resource-pattern-selection'):
        paths.update(p for p in (s.ROOT/'docs/experiments'/root).rglob('*') if p.is_file())
    paths.update((s.builder.ESM,s.builder.EXE,s.builder.ARCHIVE,s.source()))
    paths.update((s.ROOT/'.local-work/screengrabs').glob('20261024*.jpg'))
    paths.update((s.ROOT/'research/resource-standalone').glob('*.py'))
    s.write(OUT/'frozen-inputs.json',{str(p):s.builder.pin(p) for p in sorted(paths)})
    print('Frozen contract and input identities; protected audit:',audit['count'])


def inspect():
    """Read fresh selection records; retain raw operands only in local storage."""
    records = {h['formid']:(h,fs) for h,fs in s.esm_records(s.builder.ESM,
        {b'PNDT',b'BIOM',b'RSGD',b'IRES',b'ATMO'},repeated=True)}
    requests = json.loads((s.OUT/'requests-v1.json').read_text())
    rows = []
    import dataclasses
    from collections.abc import Mapping
    def plain(value):
        if dataclasses.is_dataclass(value):
            return {f.name:plain(getattr(value,f.name)) for f in dataclasses.fields(value)}
        if isinstance(value,Mapping):
            return {str(k):plain(v) for k,v in value.items()}
        if isinstance(value,(tuple,list,set,frozenset)):
            return [plain(v) for v in value]
        return value
    for bid in sorted({r['request']['body'] for r in requests}):
        prediction = s.builder.selections(records,int(bid,16))
        fs = records[int(bid,16)][1]
        atmosphere = [int.from_bytes(b,'little') for t,b in fs if t==b'INAM' and len(b)==4]
        rows.append(dict(body=bid,atmosphere=atmosphere,
            atmosphere_fields={str(a):[(t.decode(),b.hex()) for t,b in records[a][1]] for a in atmosphere if a in records},
            selection=plain(prediction)))
    # Dataclass enums and Decimal are retained as source-domain strings.
    with (OUT/'selection-inspect.json').open('x',encoding='utf8',newline='\n') as f:
        json.dump(rows,f,default=str,indent=2)
        f.write('\n')
    print('Selected bodies:',len(rows))


def predict():
    """Run final revision in a fresh isolated root; keep earlier trials intact."""
    import shutil
    root = OUT/'revision06'
    root.mkdir(exist_ok=False)
    shutil.copytree(OUT/'build-v6',root/'build-v1')
    shutil.copyfile(s.OUT/'requests-v1.json',root/'requests-v1.json')
    s.select_root(root)
    s.predict()


def compare():
    """Compare frozen outputs to existing positive witnesses, never refit inputs."""
    import collections
    import csv
    import struct
    import verify
    from save52_compare import classify
    root = OUT/'revision06'
    freeze = json.loads((root/'first-pass-v1/prediction-freeze.json').read_text())
    assert all(s.builder.pin(p)==h for p,h in {**freeze['inputs'],**freeze['files']}.items())
    inv = json.loads((s.OUT/'inventory-v2.json').read_text())
    corpus = json.loads((root/'build-v1/normalized.json').read_text())['payload']
    old = {}; new = {}
    cases = []
    def reasons_for(result):
        reasons = set()
        body = corpus['bodies'][result['request']['body']]
        for failure in result['failures']:
            reason = failure['reason']
            if reason=='UNSUPPORTED_RESOURCE_BRANCH' and 'source' in failure:
                x,y,_ = failure['source']
                tile = body['tiles'][f'{result["request"]["chart"]}:{x//192}:{y//192}']
                reason = body['biomes'][tile[2]]['status']
            reasons.add(reason)
        return sorted(reasons)
    def geometry(r):
        return [(v['resource'],v['ordered_xyzw_le'],v['native_bound_le']) for v in r['regions']]
    for row in inv['cases']:
        case = row['case']
        if row['eligibility']=='ACTIVE':
            old[case] = json.loads((s.OUT/'first-pass-v1'/(case+'-stdout.json')).read_text())
            new[case] = json.loads((root/'first-pass-v1'/(case+'-stdout.json')).read_text())
            assert old[case]['request']==new[case]['request']==row['request']
            reasons = reasons_for(new[case])
            cases.append(dict(case=case,control=row['control'],eligibility='SAVED_ACTIVE_QUALIFIED',
                d2=old[case]['status'],d3=new[case]['status'],
                d2_present=';'.join(k for k,v in old[case]['availability'].items() if v['status']=='PRESENT'),
                d3_present=';'.join(k for k,v in new[case]['availability'].items() if v['status']=='PRESENT'),
                geometry_equal=geometry(old[case])==geometry(new[case]),reason=';'.join(reasons)))
        else:
            cases.append(dict(case=case,control=row['control'],eligibility='DISABLED',d2='EXCLUDED_DISABLED',
                d3='EXCLUDED_DISABLED',d2_present='',d3_present='',geometry_equal='',reason='SAVED_DISABLED'))
    pairs = json.loads((s.OUT/'comparison-v3/pairs.json').read_text())
    comparisons = []
    for row in pairs:
        r = new[row['case']]
        comparisons.append(dict(case=row['case'],control=row['control'],resource=row['resource'],
            d2=row['outcome'],d3=classify(r,row['resource'],row['outcome']=='ALTERNATIVE_ADMISSION'),
            witness=';'.join(row['tokens']),reason=';'.join(reasons_for(r))))
    controls = []
    for case,folder,attempt,numbers in (
        ('D2-83388f','resource-region-ancestry',1,(299,325,696,716)),
        ('D2-82be17','resource-carinae',2,(1270,1280,1301))):
        bid = new[case]['request']['body']
        d1 = json.loads((s.ROOT/f'.local-work/resource-standalone/verify03/normalized-{bid}-stdout.json').read_text())
        assert geometry(d1)==geometry(new[case]), 'D1 full control regression'
        replay = json.loads((OUT/'d1-replay03'/(bid+'-stdout.json')).read_text())
        assert d1['request']==replay['request'] and geometry(d1)==geometry(replay), 'D1 request replay regression'
        for number in numbers:
            path = s.ROOT/f'.local-work/{folder}/retail-attempt0{attempt}/capture-{number:05d}.bin'
            native = verify.native(path)
            resource = f'{struct.unpack_from("<I",bytes.fromhex(native["selected"]["raw_resource"]),40)[0]:08x}'
            count = sum(r['resource']==resource and r['ordered_xyzw_le']==native['geometry']['ordered_xyzw']
                and r['native_bound_le']==native['geometry']['raw_region'][:32] for r in new[case]['regions'])
            assert count==1
            controls.append(dict(case=case,capture=number,resource=resource,matches=count,sha256=s.builder.pin(path)))
    for filename,rows in (('cases-final.csv',cases),('associations-final.csv',comparisons)):
        import io
        buffer = io.StringIO(newline='')
        writer = csv.DictWriter(buffer,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
        data = buffer.getvalue().encode()
        if (DOC/filename).exists():
            assert (DOC/filename).read_bytes()==data, 'Existing authored comparison differs'
        else:
            (DOC/filename).write_bytes(data)
    totals = collections.Counter(r['d3'] for r in comparisons if not r['control'])
    s.write(OUT/'comparison-final03.json',dict(time=s.now(),controls=controls,
        d1_requests_replayed_separately=True,full_control_paths=1429,
        totals=dict(totals),cases=cases,associations=comparisons,
        unverified_additions=[dict(case=k,resource=rid) for k,r in new.items() for rid,v in r['availability'].items()
            if v['status']=='PRESENT' and old[k]['availability'].get(rid,{}).get('status')!='PRESENT'
            and not any(p['case']==k and p['resource']==rid for p in pairs)]))
    print(dict(totals))


def d1():
    """Replay both original D1 requests against the revised corpus in isolation."""
    out = OUT/'d1-replay03'
    out.mkdir(exist_ok=False)
    results = []
    for bid in ('0005e0de','0005e4da'):
        command = [sys.executable,'-I','-S','-B',str(s.ROOT/'research/resource-standalone/isolate.py'),
            '--code',str(OUT/'build-v6/code'),'--corpus',str(OUT/'build-v6/normalized.json'),
            '--request',str(s.ROOT/f'.local-work/resource-standalone/verify03/{bid}-request.json')]
        result = subprocess.run(command,cwd=OUT/'revision06/first-pass-v1/empty',capture_output=True)
        (out/(bid+'-stdout.json')).write_bytes(result.stdout)
        (out/(bid+'-audit.json')).write_bytes(result.stderr)
        assert result.returncode==0
        audit = json.loads(result.stderr)
        assert not audit['inference_forbidden'] and audit['denied_probes']==8
        results.append(dict(body=bid,command=command,sha256=s.builder.pin(out/(bid+'-stdout.json'))))
    s.write(out/'receipt.json',results)


def tests():
    """Persist the actual stdlib test run, including stderr and exit status."""
    result = subprocess.run([sys.executable,'-B','-m','unittest','discover','-s',
        'research/resource-standalone','-v'],cwd=s.ROOT,capture_output=True)
    with (OUT/'tests-final02.txt').open('xb') as f:
        f.write(result.stdout+result.stderr)
    s.write(OUT/'tests-final02.json',dict(returncode=result.returncode,sha256=s.builder.pin(OUT/'tests-final02.txt')))
    assert result.returncode==0


def sources():
    """Inventory consulted inputs and screenshots; no proprietary payload export."""
    import csv
    files = []
    for name in ('resource-availability-cont-01.tsv','resource-availability-cont-05.tsv',
                 'resource-availability-cont-11.tsv','resource-availability-ui-34.tsv',
                 'resource-availability-ui-35.tsv','resource-milestone-b-producers-01.tsv'):
        files.append(s.ROOT/'.local-work/recon'/name)
    files += [s.builder.ESM,s.builder.EXE,s.builder.ARCHIVE,s.source()]
    files += sorted((s.ROOT/'.local-work/screengrabs').glob('20261024*.jpg'))
    files += list((s.OUT/'build-v1').glob('*.json'))
    files += [s.OUT/'requests-v1.json',s.OUT/'comparison-v3/pairs.json',s.OUT/'diagnostics-v3.json']
    files += [s.builder.OWNED/n for n in s.builder.OWNED_PINS]
    rows = [dict(source=f'D3-S{i:03d}',path=str(p.relative_to(s.ROOT)) if p.is_relative_to(s.ROOT) else str(p),
        bytes=p.stat().st_size,sha256=s.builder.pin(p),eligibility='LOCAL-ONLY input; metadata REVIEW-REQUIRED')
        for i,p in enumerate(files,1)]
    if (DOC/'sources.csv').exists():
        assert list(csv.DictReader((DOC/'sources.csv').open(encoding='utf8')))==[
            {k:str(v) for k,v in r.items()} for r in rows]
    else:
        with (DOC/'sources.csv').open('x',encoding='utf8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    records = {h['formid']:(h,fs) for h,fs in s.esm_records(s.builder.ESM,
        {b'PNDT',b'BIOM',b'RSGD',b'IRES'},repeated=True)}
    from corpus_d3 import ordinary
    gaps = []
    for bid in ('0005de4c','0005e0da','0005e0dc'):
        prediction = s.builder.selections(records,int(bid,16))
        for view in prediction.biome_results:
            biome = int(str(view.orchestration.biome.form_id),16)
            try:
                component,detail=ordinary(records,prediction,biome,{})
                status=component['status']
            except (ValueError,KeyError) as error:
                detail={};status=str(error)
            family=view.common_assignment.family
            root = int(str(family.root.form_id),16) if family else None
            alternatives=[]
            if root is not None:
                for other in prediction.biome_results:
                    if other is view or other.common_assignment.family is None or int(str(other.common_assignment.family.root.form_id),16)!=root:
                        continue
                    ob=int(str(other.orchestration.biome.form_id),16)
                    for tag,b in records[ob][1]:
                        if tag!=b'RNAM':continue
                        rid=int.from_bytes(b,'little');active=None
                        for t,raw in records[rid][1]:
                            if t==b'RNAM':active=int.from_bytes(raw,'little')
                            elif t==b'DNAM' and active==root:
                                alternatives.append(dict(biome=f'{ob:08x}',rsgd=f'{rid:08x}',
                                    dnam_sha256=s.hashlib.sha256(raw).hexdigest(),record_header=records[rid][0]))
                                break
            gaps.append(dict(detail,body=bid,biome=f'{biome:08x}',status=status,assignment=str(view.common_assignment.mechanism),
                root=f'{root:08x}' if root else None,alternatives=alternatives))
    s.write(OUT/'descriptor-ledger.json',gaps)


def preserve():
    """Rehash protected originals against old pins; authored D3 code may evolve."""
    import protection
    before=json.loads((OUT/'frozen-inputs.json').read_text())
    # This new task's driver was captured for chronology, not as an immutable
    # earlier model. Its initial digest is retained; final code is delivery-pinned.
    driver=str(Path(__file__).resolve())
    authored={str(Path(__file__).with_name(n).resolve()) for n in ('d3.py','corpus_d3.py','predictor_d3.py')}
    changed=[p for p,h in before.items() if p not in authored and s.builder.pin(p)!=h]
    old=json.loads((s.OUT/'frozen-after.json').read_text())['files']
    old_changed=[p for p,h in old.items() if s.builder.pin(p)!=h]
    audit=protection.audit()
    s.write(OUT/'protected-after.json',audit)
    s.write(OUT/'preservation.json',dict(time=s.now(),d3_frozen_count=len(before),d3_changed=changed,
        historical_frozen_count=len(old),historical_changed=old_changed,protected_count=audit['count'],
        protected_changes=audit['changes'],driver_initial_sha256=before.get(driver),driver_final_sha256=s.builder.pin(driver)))
    assert not changed and not old_changed and not audit['changes']


def preservation_correction():
    """Qualify the preserved first audit's task-code-only inventory differences."""
    receipt=json.loads((OUT/'preservation.json').read_text())
    allowed={str(Path(__file__).with_name(n).resolve()) for n in ('corpus_d3.py','predictor_d3.py')}
    assert set(receipt['d3_changed'])==allowed
    assert not receipt['historical_changed'] and not receipt['protected_changes']
    s.write(OUT/'preservation-corrected.json',dict(time=s.now(),original_receipt_sha256=s.builder.pin(OUT/'preservation.json'),
        immutable_changes=[],task_authored_code_changes=receipt['d3_changed'],
        historical_frozen_count=receipt['historical_frozen_count'],protected_count=receipt['protected_count'],
        reason='Initial inventory also captured new evolving D3 source; only these explicitly task-authored files differed. Original source expectations retained.'))


if __name__ == '__main__':
    globals()[sys.argv[1]]()
