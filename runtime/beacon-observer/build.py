# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline build/qualification/package, stdlib and installed MSVC/SDK only.

Reads game/SFSE/header/sibling/export/save hashes. Writes exclusive ignored build
directory. Runs MSVC and the original disposable tests.exe, never the game or
SFSE. No downloads, install, target/database edits, or Vortex operations.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import struct
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'research/exp0002'))
from prepare import GAME_HASH, pe_layout, file_offset

SITES={
    'player':0x177a1f0,'formid':0x204d600,'base':0x20706b7,
    'position':0x2072580,'rotation':0x20702e0,'cell':0x208b990,
    'world':0x208b9e0,'cached_branch':0x910690,'terrain_origin':0x78d1f0,
    'grid':0x78d660,'projection':0x2332410,'workshop':0xf4ffc0,
    'extra_chain':0x517d60,
    'pool_callbacks':0x3c6b20,'pool_release':0x189f8d0,
    'native_workshop_output_writer':0x21b29ac,'native_workshop_output_owner':0x21b294d,
}
SFSE_HASH='28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def disk():
    import shutil
    values={v:shutil.disk_usage(v).free for v in ('C:/','D:/')}
    if min(values.values())<40_000_000_000:raise RuntimeError('Disk guard')
    return values
def run(args,out,log):
    p=subprocess.run(args,cwd=out,capture_output=True)
    (out/log).write_bytes(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError(f'{log}: exit {p.returncode}')
def verify(out):
    rows=0
    for journal in (out/'fixtures').rglob('records.jsonl'):
        for line in journal.read_text().splitlines():
            row=json.loads(line);rows+=1
            if row.get('kind')=='raw':
                p=journal.parent/row['file']
                assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    assert rows>=10
    assert json.loads((out/'fixtures/missing/complete.json').read_text())['terminal']=='CAPTURE_PARTIAL'
    assert 'cyclic_extra_chain' in (out/'fixtures/cyclic/records.jsonl').read_text()
    assert (out/'fixtures/interrupted/records.jsonl').read_text()=='{"durable":true}\n'
    full=[json.loads(line) for line in (out/'fixtures/full-pool/records.jsonl').read_text().splitlines()]
    refs=[r for r in full if r.get('kind')=='reference']
    assert len(refs)==2 and all(r['observational_handle_association'] for r in refs)
    assert next(r for r in full if r.get('kind')=='census')['ordinary_candidates']==2
    assert sum(r.get('bytes',0) for r in full if r.get('root')=='handles.pool')==33_554_432
    assert 'trusted_root_identity_mismatch' in (out/'fixtures/wrong-player/records.jsonl').read_text()
    stale=[json.loads(line) for line in (out/'fixtures/stale-slot/records.jsonl').read_text().splitlines()]
    assert not next(r for r in stale if r.get('kind')=='reference')['observational_handle_association']
    return {'json_rows':rows,'raw_hashes':'PASS','partial_and_recovery':'PASS'}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--name',required=True)
    p.add_argument('--vcvars',type=Path,required=True)
    p.add_argument('--sfse',type=Path,required=True,help='Exact deployed or Vortex-staged SFSE DLL to hash only')
    a=p.parse_args()
    if not a.name.replace('-','').isalnum():raise ValueError('Simple name')
    initial=disk();version=json.loads((SOURCE/'version.json').read_text())
    v=version['version'];major,minor,patch=map(int,v.split('.'));integer=(major<<24)|(minor<<16)|patch
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    sfse=a.sfse
    sample=json.loads((ROOT/'.local-work/two-outpost-anchor/exact-beacon-01/manifest.json').read_text())
    save=Path(sample['source']['path'])
    protected=[game,sfse,sfse.parent/'sfse_loader.exe',save,Path(sample['copy']['path'])]
    protected=[x for x in protected if x.exists()]
    before={str(x):{'sha256':sha(x),'size':x.stat().st_size,'mtime_ns':x.stat().st_mtime_ns} for x in protected}
    if sha(game)!=GAME_HASH or sha(sfse)!=SFSE_HASH:raise ValueError('Installed module mismatch')
    if sha(save)!='d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5':raise ValueError('Save25 mismatch')
    out=ROOT/'.local-work/beacon-observer-builds'/a.name;out.mkdir(parents=True,exist_ok=False)
    data=game.read_bytes();_,size,sections=pe_layout(data);guards=[]
    for name,rva in SITES.items():
        pos=file_offset(sections,rva,32);guards.append(dict(name=name,rva=rva,sha256=hashlib.sha256(data[pos:pos+32]).hexdigest()))
    header=f'#pragma once\ninline constexpr char observer_version[]="{v}";\ninline constexpr unsigned observer_version_int={integer};\ninline constexpr char expected_game_hash[]="{GAME_HASH}";\ninline constexpr char expected_sfse_hash[]="{SFSE_HASH}";\nstruct Guard{{unsigned rva;const char* hash;}};\ninline constexpr Guard guards[]={{\n'+''.join('{'+hex(g['rva'])+',"'+g['sha256']+'"},\n' for g in guards)+'};\n'
    (out/'identity.generated.h').write_text(header,encoding='utf-8',newline='\n')
    for target,source,flags in [('plugin','plugin.cpp',['/LD','/Fe:SorBeaconObserver.dll']),('tests','tests.cpp',['/Fe:tests.exe'])]:
        rsp=out/(target+'.rsp')
        rsp.write_text('\n'.join(['/nologo','/std:c++20','/EHsc','/W4','/MD','/O2','/DUNICODE','/D_UNICODE',f'/I"{out}"',f'"{SOURCE/source}"',*flags,'/link','/INCREMENTAL:NO','bcrypt.lib'])+'\n',encoding='utf-8')
        cmd=out/(target+'.cmd')
        cmd.write_text(f'@echo off\ncall "{a.vcvars}"\nif errorlevel 1 exit /b 1\nwhere cl.exe\nwhere link.exe\ncl.exe /Bv @{rsp.name}\n',encoding='utf-8',newline='\r\n')
        run(['cmd.exe','/d','/c',str(cmd)],out,target+'-build.txt')
    run([str(out/'tests.exe'),str(out/'fixtures'),str(out/'SorBeaconObserver.dll')],out,'tests.txt');qualification=verify(out)
    control=out/'control-fixture';control.mkdir();(control/'ready.json').write_text(json.dumps({'version':v,'ready':True}))
    def request(label,*extra):
        return subprocess.run([sys.executable,'-B',str(SOURCE/'request.py'),str(control),label,*extra],capture_output=True)
    assert request('baseline','--settled').returncode==0
    assert (control/'baseline.request').read_bytes()==b'SETTLED baseline\n'
    assert request('baseline','--settled').returncode!=0
    assert request('../escape','--settled').returncode!=0 and request('unsettled').returncode!=0
    assert request('STOP').returncode==0 and (control/'STOP').read_bytes()==b'STOP\n'
    qualification['request_controls']='PASS'
    run([sys.executable,'-B',str(SOURCE/'inspect_capture.py'),str(out/'fixtures/full-pool'),'--output',str(out/'inspected.json')],out,'inspection.txt')
    inspected=json.loads((out/'inspected.json').read_text())
    assert len(inspected['references'])==2 and inspected['raw_sections']>=512
    run([sys.executable,'-B',str(SOURCE/'inspect_capture.py'),str(out/'fixtures/native-output'),'--output',str(out/'native-output.json')],out,'native-output.txt')
    native=json.loads((out/'native-output.json').read_text())['native_workshop_output']
    assert native['equal_bracket_values']
    assert native['before']['center_float32_hex']==struct.pack('<3f',321.25,-42.5,17).hex()
    assert native['before']['radius_float32_hex']==struct.pack('<f',150).hex()
    assert native['before']['flags_e8_e9_ea']==[1,0,0]
    qualification['native_stored_output_no_recomputation']='PASS'
    # Recovery is tested on a derivative; original fixture remains unchanged.
    recovery=out/'recovery-fixture';recovery.mkdir()
    (recovery/'records.jsonl').write_bytes(b'{"kind":"begin"}\n{"incomplete"')
    run([sys.executable,'-B',str(SOURCE/'inspect_capture.py'),str(recovery),'--output',str(out/'recovered.json')],out,'recovery.txt')
    assert json.loads((out/'recovered.json').read_text())['journal_truncated_final_line']
    qualification['offline_inspection']='PASS'
    fields=out/'field-fixture';fields.mkdir();field_rows=[]
    terrain=bytearray(0x200);terrain[0x20]=3;terrain[0xc8]=1;terrain[0x1c0]=2
    struct.pack_into('<I',terrain,0x80,0x3f59f)
    struct.pack_into('<2i',terrain,0x1c4,54,110)
    grid=bytearray(0x100);struct.pack_into('<I',grid,0x50,256)
    for i,(root,b) in enumerate([('terrain',terrain),('terrain.grid',grid),('stitch.block',struct.pack('<I',10)),('stitch.merge',struct.pack('<I',2))]):
        name=f'raw-{i}.bin';(fields/name).write_bytes(b)
        field_rows.append(dict(kind='raw',root=root,file=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
    (fields/'records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in field_rows))
    run([sys.executable,'-B',str(SOURCE/'inspect_capture.py'),str(fields),'--output',str(out/'fields.json')],out,'fields.txt')
    f=json.loads((out/'fields.json').read_text())
    assert f['terrain']['selected_origin_offset']=='0x1c0' and f['terrain']['origins']['0x1c0']['coarse_xy']==[54,110]
    assert f['grid']['candidate_axis_steps']==49152
    (fields/'raw-0.bin').write_bytes(b'corrupt')
    corrupted=subprocess.run([sys.executable,'-B',str(SOURCE/'inspect_capture.py'),str(fields),'--output',str(out/'must-not-exist.json')],capture_output=True)
    assert corrupted.returncode!=0 and not (out/'must-not-exist.json').exists()
    qualification['decoded_fields_and_corruption']='PASS'
    package=out/'package';plugin=package/'Data/SFSE/Plugins';plugin.mkdir(parents=True)
    (plugin/'SorBeaconObserver.dll').write_bytes((out/'SorBeaconObserver.dll').read_bytes())
    (plugin/'SorBeaconObserver.config').write_text(str(ROOT/'.local-work/beacon-observer-live')+'\n',encoding='utf-8',newline='\n')
    notice=package/'ResearchNotices';notice.mkdir()
    for dest,src in [('SFSE-PluginAPI-LICENSE.txt',ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt'),('PROJECT-LICENSE.txt',ROOT/'LICENSE'),('README.md',SOURCE/'README.md')]:
        (notice/dest).write_bytes(src.read_bytes())
    archive=out/f'SorBeaconObserver-{v}.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for f in package.rglob('*'):
            if f.is_file():z.write(f,f.relative_to(package))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
        assert hashlib.sha256(z.read('Data/SFSE/Plugins/SorBeaconObserver.dll')).hexdigest()==sha(out/'SorBeaconObserver.dll')
        assert z.read('Data/SFSE/Plugins/SorBeaconObserver.config')==(str(ROOT/'.local-work/beacon-observer-live')+'\n').encode()
    after={str(x):{'sha256':sha(x),'size':x.stat().st_size,'mtime_ns':x.stat().st_mtime_ns} for x in protected}
    assert before==after
    sources=[*SOURCE.glob('*.*'),ROOT/'runtime/exp0002/win_support.h',ROOT/'runtime/exp0002/core.h',ROOT/'runtime/exp0002/third_party/sfse/PluginAPI.h',ROOT/'research/exp0002/prepare.py']
    manifest=dict(utc=datetime.now(timezone.utc).isoformat(),version=v,version_integer=integer,authority='OFFLINE_NOT_DEPLOYED',sfse_input=str(sfse),sfse_deployed=(game.parent/'sfse_1_16_244.dll').exists(),image_size=size,package_sha256=sha(archive),dll_sha256=sha(out/'SorBeaconObserver.dll'),guards=guards,qualification=qualification,protected_before=before,protected_after=after,sources={str(x.relative_to(ROOT)):sha(x) for x in sources if x.is_file()},disk_initial=initial,disk_final=disk(),vcvars=str(a.vcvars),vcvars_sha256=sha(a.vcvars))
    tools={}
    for line in (out/'plugin-build.txt').read_text(errors='replace').splitlines():
        if line.strip().lower().endswith(('\\cl.exe','\\link.exe')) and Path(line.strip()).exists():tools[line.strip()]=sha(Path(line.strip()))
    manifest['toolchain']=tools
    (out/'build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'build':str(out),'dll':manifest['dll_sha256'],'package':manifest['package_sha256'],'qualification':qualification}))
if __name__=='__main__':main()
