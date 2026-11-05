# SPDX-License-Identifier: GPL-3.0-or-later
"""Recheck the existing controlled Save52 type-3 tail for input suitability.

Reads exact A0 archive/protection, existing D5AD receipt, controlled save and
existing owned selected-block decoder. No new save grammar, broad parser,
source/save modification or game/tool process. Writes fresh ignored receipt.
"""
import os, sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Pinned Python -E -B required')
import hashlib, importlib.util, json, zipfile
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha
import d5al_baseline as baseline


def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):
        raise ValueError('Fresh ignored output required')
    archive=baseline.ARCHIVE/'episode-a.zip'
    if sha(archive)!=baseline.ANCHORS[archive]:raise ValueError('A0 archive changed')
    with zipfile.ZipFile(archive) as zipped:
        pre=json.loads(zipped.read('notes/preflight01/receipt.json'))['protection']
        card=zipped.read('notes/approved-card.md')
    name=pre['save52'];pin=pre['save_policy']['designated'][name]
    policy_path=ROOT/'research/resource-carinae-source-context/save_policy.json'
    policy=json.loads(policy_path.read_bytes())
    if policy['designated'][name]!=pin or b'Save52' not in card:raise ValueError('A0 Save52 policy/route mismatch')
    receipt_path=ROOT/'.local-work/d5ad-save/tail01/save-tail.json'
    if sha(receipt_path)!='e5893c0ac55463784da425a4c55d1c9600468a5cb074d4f898291feeb5fe7b98':raise ValueError('D5AD-SV35 changed')
    receipt=json.loads(receipt_path.read_bytes());save=ROOT/'.local-work/savegames'/name
    if Path(receipt['source']).resolve()!=save.resolve() or save.stat().st_size!=pin['bytes'] or sha(save)!=pin['sha256'] or receipt['source_sha256']!=pin['sha256']:
        raise ValueError('Controlled save identity mismatch')
    method=ROOT/'research/resource-retained-population/d5ad_save_tail.py'
    spec=importlib.util.spec_from_file_location('d5ar_existing_tail',method);tail=importlib.util.module_from_spec(spec);spec.loader.exec_module(tail)
    fixture_controls=tail.controls()
    result=receipt['result'];start=result['lists'][0]['count_logical_offset'];length=result['tail_bytes']
    selected=tail.D5Z.independent_slice(save,start,length)
    if hashlib.sha256(selected).hexdigest()!=receipt['tail_sha256'] or tail.decode_tail(selected,start)!=result:
        raise ValueError('Existing independent slice/parser disagrees')
    if result['typed_count']!=88 or any(row['subkey_u16']!=0 for row in result['typed_rows']):
        raise ValueError('Saved typed row population changed')
    if sha(save)!=pin['sha256']:raise ValueError('Controlled save changed during inspection')
    output=dict(status='PASS_EXISTING_SAVE52_TYPE3_TAIL_IS_SEPARATE_COMPONENT',source_sha256=pin['sha256'],source_bytes=pin['bytes'],
                original_a0_save52_policy_match=True,approved_card_sha256=hashlib.sha256(card).hexdigest(),
                independent_selected_block_match=True,typed_rows=88,all_subkeys_zero=True,controls=fixture_controls,
                native_semantic_binding='D5AD saved-state matrix: 0x1403a6ae0/0x1403a70a0 and 0x1403a7eb0/0x1403a74e0/0x1403a7cc0 serialize/restore PlanetWorldSpaceData GameDaysPassed at component+0x10, not AtmosphereModifier.',
                atmosphere_modifier_recovered=False,
                limit='This bounded existing parser cannot extract a different component merely by reinterpreting its opaque u32 values. No broad save parser or PNDT INAM shortcut added.',
                inputs={str(p.relative_to(ROOT)):sha(p) for p in (archive,policy_path,receipt_path,method,Path(tail.D5Z.__file__))},method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(output,indent=2)+'\n')
    print(output['status'])


if __name__=='__main__':main()
