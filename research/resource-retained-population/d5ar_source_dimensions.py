# SPDX-License-Identifier: GPL-3.0-or-later
"""Check original constructor caller padding aliases; no target execution.

Reads retained pinned original exports and authenticated A0 input audit. Writes
one fresh ignored receipt. This is a scoped dataflow proof, not a live read,
shape inversion, setting-value certificate or full input-equivalence verdict.
"""
import os, sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Pinned Python -E -B required')
import json
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha


def main():
    out = Path(sys.argv[1]).resolve()
    before = guard()
    if not out.is_relative_to(ROOT / '.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('Fresh ignored non-reparse output required')
    names = ['.local-work/d5ab/lifetime-export01/native.tsv', '.local-work/d5am/owner-census05/native.tsv', '.local-work/d5ar/source-dimension-bounds01/native.tsv']
    paths = [ROOT / name for name in names]
    texts = [p.read_text(encoding='utf8') for p in paths]
    audit_path = ROOT / '.local-work/d5ar/effective-input-audit02.json'
    audit = json.loads(audit_path.read_bytes())
    if (audit['a0_birth'], audit['allocation'], audit['generation']) != (2082, 932, 8099):
        raise ValueError('Wrong authenticated A0 lineage')
    raw_source = bytes.fromhex(audit['source_prefix70_hex'])
    dimensions = [int.from_bytes(raw_source[a:a+4], 'little', signed=True) for a in (0x28, 0x2c)]
    padding = [int.from_bytes(raw_source[a:a+4], 'little', signed=True) for a in (0x20, 0x24)]
    if len(raw_source) != 0x70 or dimensions != [14, 14] or padding != [2, 2]:
        raise ValueError('Actual birth operands changed')
    paths.append(audit_path)
    checks = [
        (0, '1408497cd\tMOV R9D,dword ptr [RCX + 0x50]'),
        (0, '1408497d1\tMOV dword ptr [RBP + -0x44],R9D'),
        (0, '1408497d5\tMOV R10D,dword ptr [RCX + 0x54]'),
        (0, '1408497d9\tMOV dword ptr [RBP + -0x48],R10D'),
        (0, '1408497f0\tMOV dword ptr [RBP + 0x40],R9D'),
        (0, '1408497f4\tMOV dword ptr [RBP + 0x44],R10D'),
        (0, '140849bdb\tLEA R9,[RBP + 0x40]'),
        (0, '140849b11\tMOV EAX,dword ptr [RBP + -0x48]'),
        (0, '140849b16\tMOV EDX,dword ptr [R13 + 0x44]'),
        (0, '140849b1a\tSUB EDX,EAX'),
        (0, '140849b1c\tMOV EAX,dword ptr [RBP + -0x44]'),
        (0, '140849b21\tMOV ECX,dword ptr [R13 + 0x40]'),
        (0, '140849b25\tSUB ECX,EAX'),
        (0, '140849bf2\tCALL 0x140982d90'),
        (1, '1407852a6\tMOV RCX,qword ptr [RSI + 0x10]'),
        (1, '1407852aa\tMOV EAX,dword ptr [RCX + 0x50]'),
        (1, '1407852ad\tMOV dword ptr [RBP + 0x77],EAX'),
        (1, '1407852b0\tMOV EAX,dword ptr [RCX + 0x54]'),
        (1, '1407852b3\tMOV dword ptr [RBP + 0x7b],EAX'),
        (1, '1407852b6\tMOV RAX,qword ptr [RBP + 0x77]'),
        (1, '1407852ba\tMOV qword ptr [RBP + -0x49],RAX'),
        (1, '1407852be\tLEA RAX,[RBP + 0x77]'),
        (1, '1407852c2\tMOV qword ptr [RBP + -0x39],RAX'),
        (1, '1407852c6\tLEA RAX,[RBP + -0x49]'),
        (1, '1407852ca\tMOV qword ptr [RBP + -0x31],RAX'),
        (0, '1407862ab\tMOV R10,qword ptr [RCX]'),
        (0, '1407862b1\tMOV R11D,dword ptr [RDX + 0x40]'),
        (0, '1407862b8\tMOV R9D,dword ptr [RDX + 0x44]'),
        (0, '1407862c2\tMOV EAX,dword ptr [R10]'),
        (0, '1407862c7\tSUB R11D,EAX'),
        (0, '1407862ca\tMOV EAX,dword ptr [R10 + 0x4]'),
        (0, '1407862d5\tSUB R9D,EAX'),
        (0, '14078635a\tMOV R9,qword ptr [R14 + 0x8]'),
        (0, '140786382\tCALL 0x140982d90'),
        (0, '1407855bc\tLEA R9,[RSP + 0xb8]'),
        (0, '14078549f\tMOV R11D,dword ptr [0x145f60a90]'),
        (0, '1407854c0\tLEA R10D,[R11 + R11*0x1]'),
        (0, '1407854c4\tMOV dword ptr [RSP + 0xb8],R11D'),
        (0, '1407854cc\tSUB EAX,R10D'),
        (0, '1407854cf\tMOV dword ptr [RSP + 0xbc],R11D'),
        (0, '1407854de\tSUB EBX,R10D'),
        (0, '1407855c4\tLEA RAX,[RSP + 0xb0]'),
        (0, '1407855dc\tCALL 0x140982d90'),
        (2, '140983121\tMOV RCX,qword ptr [RSP + 0x310]'),
        (2, '140983129\tMOV EAX,dword ptr [RCX]'),
        (2, '14098312d\tCMOVL EAX,ESI'),
        (2, '140983130\tMOV dword ptr [R14 + 0x18],EAX'),
        (2, '14098313c\tMOV dword ptr [R14 + 0x1c],EAX'),
    ]
    for index, line in checks:
        if line not in texts[index].splitlines():
            raise ValueError('Original dataflow anchor changed: ' + line)
    start = texts[2].index('FUNCTION\t140982d00\t')
    end = texts[2].index('END_FUNCTION', start)
    body = texts[2][start:end]
    stores = [line for line in body.splitlines() if '\tMOV ' in line and line.split('\t', 1)[1].split(',', 1)[0].endswith(']')]
    if len(stores) != 4 or any('[RSP + ' not in line for line in stores):
        raise ValueError('Overlap predicate acquired non-stack writes')
    result = dict(status='PASS_SCOPED_CALLER_DIMENSION_RECONSTRUCTION',
                  exact_instruction_anchors=len(checks), overlap_predicate_nonstack_stores=[],
                  constructor='0x140982d90; Birth precedes final max(1,nominal) stores 0x140983130/0x14098313c',
                  theorem='All three ordinary source-constructor caller families subtract twice the same padding pair that the constructor retains at source+0x20/+0x24; overlap predicate does not modify the nominal argument.',
                  authenticated_A0_inputs={'definition_dimensions':dimensions, 'retained_padding':padding},
                  reconstructed_final_dimensions=[max(1,d-2*p) for d,p in zip(dimensions,padding)],
                  prerequisites=['Authenticated A0 Birth inputs supplied by effective-input-audit02; no geometry-equality inference', 'Examined original ordinary constructor caller graph and healthy completed constructor'],
                  not_certified=['Current stitch/coordinate-setting values at generation', 'Per-cell manager descriptor interval', 'Runtime resource selection/order or all effective non-mask input equivalence'],
                  inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}, method_sha256=sha(__file__), floors_before=before, floors_after=guard())
    with out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
