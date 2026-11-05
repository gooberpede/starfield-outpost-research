# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit bounded PNDT/ATMO operands and their complete pinned-file override set.

Reads exact A0 file pins, owned ESM framing and retained original exports. Writes
ignored operands only. Does not decode reflected lists or use external xEdit
heuristics. ATMO effective resource membership remains unqualified here.
"""
import os, sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Pinned Python -E -B required')
import hashlib, json
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records


def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):
        raise ValueError('Fresh ignored output required')
    audit=ROOT/'.local-work/d5ar/a0-file-inputs05.json';pins=json.loads(audit.read_bytes())['inputs']
    files={n:h for n,h in pins.items() if Path(n).suffix.lower() in ('.esm','.esp','.esl')}
    if len(files)!=39 or any(sha(Path(n))!=h for n,h in files.items()):raise ValueError('A0 file roster changed')
    main_path=next(Path(n) for n in files if Path(n).name.lower()=='starfield.esm')
    records={h['formid']:(h,fs) for h,fs in esm_records(main_path,{b'PNDT',b'ATMO'},repeated=True)}
    nested=False;operands=[]
    for tag,raw in records[0x5e0de][1]:
        if tag==b'BDST':nested=True
        elif tag==b'BDED':nested=False
        elif tag==b'INAM' and nested:operands.append(raw)
    if len(operands)!=1 or len(operands[0])!=16 or operands[0].hex()!='9bc100000000803e0ad7233b6f12833a':raise ValueError('Actual PNDT nested INAM changed')
    current=int.from_bytes(operands[0][:4],'little');rows=[];seen=set()
    while current:
        if current in seen:raise ValueError('Serialized RFDP cycle')
        seen.add(current);h,fields=records[current]
        if h['type']!='ATMO':raise ValueError('Candidate does not resolve to main ATMO')
        parents=[raw for tag,raw in fields if tag==b'RFDP']
        if len(parents)>1 or parents and len(parents[0])!=4:raise ValueError('RFDP operand framing unsupported')
        rows.append(dict(header=h,fields=[dict(tag=t.decode('ascii'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),raw_hex=b.hex()) for t,b in fields]))
        current=int.from_bytes(parents[0],'little') if parents else 0
    overrides=[]
    for name,pin in files.items():
        path=Path(name);masters=[]
        for h,fields in esm_records(path,{b'TES4',b'ATMO'},repeated=True):
            if h['type']=='TES4':masters=[b.rstrip(b'\0').decode('utf8') for t,b in fields if t==b'MAST'];continue
            i=h['formid']>>24;master=masters[i] if i<len(masters) else path.name if i==len(masters) else 'UNRESOLVED'
            if path!=main_path and master.lower()=='starfield.esm' and h['formid']&0xffffff in seen:overrides.append(dict(file=name,header=h))
        if sha(path)!=pin:raise ValueError('File changed during audit')
    if overrides:raise ValueError('Serialized ATMO-chain override requires reconciliation')
    exports=[ROOT/'.local-work/d5ar'/name/'native.tsv' for name in ('atmosphere-setting-producer01','atmosphere-payload-read01','atmosphere-payload-apply01','atmosphere-component-copy01','atmosphere-component-store01','atmosphere-input-getter01','atmosphere-resource-fixup01')]
    checks=[(1,'140773450\tMOV R8D,0x10'),(1,'140773456\tJMP 0x1405b80b0'),(0,'140770a6b\tCALL 0x140773460'),(4,'140776d4e\tVMOVUPS XMM0,xmmword ptr [RBP]'),(4,'140776d53\tVMOVUPS xmmword ptr [RDX + 0x10],XMM0'),(5,'1409dd0d2\tMOV ECX,dword ptr [RAX + RCX*0x1 + 0x20]'),(5,'1409dd0e0\tCMP byte ptr [RAX + 0x2e],0xad')]
    texts=[p.read_text(encoding='utf8').splitlines() for p in exports]
    for i,line in checks:
        if line not in texts[i]:raise ValueError('Original payload/getter anchor changed')
    result=dict(status='PASS_SERIALIZED_ATMO_INPUT_AUDIT_NOT_EFFECTIVE_LIST',body='0x0005e0de',nested_inam16_hex=operands[0].hex(),first_u32_candidate='0x0000c19b',records=rows,
                actual_a0_pinned_files=39,overrides=overrides,native_field_anchors=len(checks),
                limits=['No REFL/RDIF effective resource-list decoding performed','Native file-namespace remap/normal initialization and historical context remain separately reviewable','No empty-atmosphere result follows from labels or an absent exporter CSV row'],
                scientific_external_xedit_code_or_heuristic_used=False,input_audit_sha256=sha(audit),methods={str(p.relative_to(ROOT)):sha(p) for p in exports},reader_sha256=sha(ROOT/'save-analysis/scripts/inspect_outpost_definitions.py'),method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],serialized_atmo_records=len(rows),overrides=len(overrides))))


if __name__=='__main__':main()
