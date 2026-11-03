# SPDX-License-Identifier: GPL-3.0-or-later
"""Derive a separate 0.9.0 D5AM offline candidate from authenticated 0.7.0 sources.

Reads the retained build16 manifest/source tree, installed pinned PE, approved
unchanged support headers and authored D5AM extensions. Writes only fresh
D5AM local candidate and build trees, compiled DLL/host, synthetic sessions and
receipts. Executes MSVC/MASM and owned disposable hosts. No deployment, game,
save/configuration mutation, Ghidra project access, download, network or Git write.
The new candidate is not qualified for retail deployment by successful compilation.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'.local-work/d5ai-recorder'
SOURCE=BASE/'candidate-build16/runtime/construction-winner'
VC=Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def replace(text,before,after,count=1):
    if text.count(before)!=count:
        raise ValueError('Checked source adaptation mismatch: '+before[:100])
    return text.replace(before,after)

def main():
    label=sys.argv[1]
    if not re.fullmatch('[a-z0-9-]+',label):
        raise ValueError('Fresh bounded label required')
    sys.path.insert(0,str(Path(__file__).parent))
    from d5am_lock_qualify import guard
    initial_free=guard()
    parent=ROOT/'.local-work/d5am';parent.mkdir(exist_ok=True)
    out=parent/label;out.mkdir(exist_ok=False)
    tree=out/'candidate';candidate=tree/'runtime/construction-winner';candidate.mkdir(parents=True)
    manifest=BASE/'build16/build.json'
    if sha(manifest)!='15d10475806aeb593ac7236a48ea1b71f8e3614bf8cdd7e1ded830b0fcdbf457':
        raise ValueError('Retained 0.7.0 build16 manifest mismatch')
    original=json.loads(manifest.read_bytes())
    pins={str(manifest):sha(manifest),str(Path(__file__)):sha(__file__)}
    for p in SOURCE.iterdir():
        if p.is_file():
            if original['inputs'].get(str(p))!=sha(p):
                raise ValueError('Retained derived-source mismatch: '+str(p))
            pins[str(p)]=sha(p)
            (candidate/p.name).write_bytes(p.read_bytes())
    for name in ('core.h','win_support.h','third_party/sfse/PluginAPI.h','third_party/sfse/LICENSE.txt'):
        p=ROOT/'runtime/exp0002'/name
        if original['inputs'].get(str(p))!=sha(p):
            raise ValueError('Approved support mismatch: '+name)
        pins[str(p)]=sha(p);target=tree/'runtime/exp0002'/name
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
    for name in ('d5am_causality.h','d5am_causality.asm','d5am_fixture.inc','d5am_scheduler.h','d5am_scheduler.asm','d5am_scheduler_fixture.inc'):
        p=ROOT/'runtime/construction-winner'/name;pins[str(p)]=sha(p)
        (candidate/name).write_bytes(p.read_bytes())
    def mutate(name,fn):
        p=candidate/name;p.write_text(fn(p.read_text(encoding='utf8')),encoding='utf8',newline='\n')
    causal_include='#include "d5ai_context.h"\n#include "d5am_causality.h"\n#include "d5am_scheduler.h"'
    for name in ('transport.cpp','plugin.cpp','fixture.cpp'):
        mutate(name,lambda text:replace(text,'#include "d5ai_context.h"',causal_include))
    mutate('fixture.cpp',lambda text:replace(text,'#include "d5am_scheduler.h"','#include "d5am_scheduler.h"\n#include "d5am_scheduler_fixture.inc"'))
    def observer(text):
        text=replace(text,'using U=uint64_t;','using U=uint64_t;\nnamespace causal {void register_owner(U) noexcept;void visited_done() noexcept;void lifecycle(U,U) noexcept;}\nnamespace scheduler {void provider() noexcept;}')
        text=replace(text,'Active activity;Scope scope{};','causal::register_owner(proc);\n Active activity;Scope scope{};')
        text=replace(text,'current=&scope;auto e=event(Entry);','current=&scope;scheduler::provider();auto e=event(Entry);')
        text=replace(text,'if(!stable(e))e.status|=LifetimeInvalid;emit(e);\n}\n// Constructor-private source:',
                     'if(!stable(e))e.status|=LifetimeInvalid;emit(e);causal::visited_done();\n}\n// Constructor-private source:')
        text=replace(text,'Active activity;++hazards;increment(epoch);if constexpr(N==0)++reset_depth;',
                     'if constexpr(N==0){causal::register_owner(a);causal::lifecycle(a,12);}\n if constexpr(N==1)causal::lifecycle(a,14);\n Active activity;++hazards;increment(epoch);if constexpr(N==0)++reset_depth;')
        text=replace(text,'if constexpr(N==0)--reset_depth;else increment(epoch);',
                     'if constexpr(N==0){--reset_depth;causal::lifecycle(proc,13);}else increment(epoch);')
        return text
    mutate('observer.h',observer)
    def transport(text):
        text=replace(text,'extern "C" {uint64_t visited_fall{},',
                     'extern "C" {std::atomic<uint64_t> D5AM_watched_lock{},D5AM_watched_state{},D5AM_generation{},D5AM_registry_serial{},D5AM_recursive_release_site{};\nvoid D5AM_capture(uint64_t lock,uint64_t old,uint64_t kind,uint64_t generation,uint64_t serial,uint64_t site) noexcept {winner::causal::capture(lock,uint32_t(old),uint32_t(kind),generation,serial,site,true,uint32_t(kind>>32),uint32_t(old>>32));}\nuint64_t visited_fall{},')
        text=replace(text,'bool guards(){Measure measure{Guard};','bool guards(){Measure measure{Guard};if(!causal::guards()||!scheduler::guards()){output_fault="causal_or_scheduler_guard";return false;}')
        text=replace(text,'bool drain(){Measure measure{Drain};','bool drain(){Measure measure{Drain};if(!causal::drain()||!scheduler::drain()){output_fault="causal_or_scheduler_write";return false;}')
        text=replace(text,'+metrics()+','+metrics()+causal::metrics()+scheduler::metrics()+',count=text.count('+metrics()+'))
        text=replace(text,',\\"qpc_frequency\\":'+ '"+std::to_string(frequency.QuadPart)+"', '')
        text=replace(text,'lifetime::close();CloseHandle(raw);','causal::close();scheduler::close();lifetime::close();CloseHandle(raw);')
        return text
    mutate('transport.cpp',transport)
    spec=importlib.util.spec_from_file_location('owned_pe',ROOT/'runtime/retained-population/build.py')
    pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)
    if sha(pe.GAME/'Starfield.exe')!=pe.GAME_HASH:
        raise ValueError('Installed PE identity')
    image=(pe.GAME/'Starfield.exe').read_bytes()
    native=[]
    for name,rva,size in (('reader',0x22cc350,126),('writer',0x22cc3d0,216),('release',0x2c45a0,81)):
        raw=pe.pe_read(image,rva,size)
        native.append('inline constexpr unsigned char d5am_original_'+name+'[]={'+','.join(str(b) for b in raw)+'};\n')
    (out/'d5am_native.generated.h').write_text(''.join(native),encoding='utf8',newline='\n')
    rvas=[0x22cc410,0x22cc48f,0x22cc3f2,0x22cc366,0x2c45c2,0x2c45e7,0x79fc85,0x79e027,0x21e0a87,0x79fcb3,0x22cc3c3,0x7a51b7,0x7a5386,0x7a547c,0x982a5a,0x982a92]
    hashes=[hashlib.sha256(pe.pe_read(image,rva,32)).hexdigest() for rva in rvas]
    helpers=[(0x22cc350,126),(0x22cc3d0,216),(0x2c45a0,81)]
    helper_hashes=[hashlib.sha256(pe.pe_read(image,rva,size)).hexdigest() for rva,size in helpers]
    extra='\nnamespace winner { inline const U causal_rvas[]={'+','.join(hex(rva) for rva in rvas)+'};\ninline const char* causal_hashes[]={'+','.join('"'+h+'"' for h in hashes)+'};}\n'
    extra+='namespace winner { inline const char* causal_helper_hashes[]={'+','.join('"'+h+'"' for h in helper_hashes)+'};}\n'
    scheduler_rvas=[0x76cea4,0x76d07b,0x7b56c5,0x7b57eb,0x27ec100,0x27e6a00,0x27e4ab0,0x27e4957,0x27e61a4,0x76d14f,0x7b585f,0x28d3960,0x28d2b80]
    scheduler_hashes=[hashlib.sha256(pe.pe_read(image,rva,32)).hexdigest() for rva in scheduler_rvas]
    target_sites=[0,1,2,3,9,10]
    target_rvas=[]
    for i in target_sites:
        call=pe.pe_read(image,scheduler_rvas[i],5)
        if call[0]!=0xe8:raise ValueError('Scheduler original CALL identity')
        target_rvas.append(scheduler_rvas[i]+5+int.from_bytes(call[1:],'little',signed=True))
    target_hashes=[hashlib.sha256(pe.pe_read(image,rva,32)).hexdigest() for rva in target_rvas]
    vtables=[0x4b3d0e8,0x4b3d138,0x4b406b8]
    vtable_hashes=[hashlib.sha256(pe.pe_read(image,rva,32)).hexdigest() for rva in vtables]
    callback_rva=0x27ec2e0;callback_hash=hashlib.sha256(pe.pe_read(image,callback_rva,32)).hexdigest()
    extra+='namespace winner { inline const U scheduler_rvas[]={'+','.join(hex(rva) for rva in scheduler_rvas)+'};\ninline const char* scheduler_hashes[]={'+','.join('"'+h+'"' for h in scheduler_hashes)+'};\ninline const U scheduler_vtables[]={'+','.join(hex(rva) for rva in vtables)+'};\ninline const char* scheduler_vtable_hashes[]={'+','.join('"'+h+'"' for h in vtable_hashes)+'};\ninline const char scheduler_callback_hash[]="'+callback_hash+'"; }\n'
    extra+='namespace winner { inline const char* scheduler_target_hashes[]={'+','.join('"'+h+'"' for h in target_hashes)+'};}\n'
    # Verify loader relocation domains rather than assuming every code hash is ASLR stable.
    import struct
    peoff=struct.unpack_from('<I',image,0x3c)[0];optional=peoff+24
    preferred=struct.unpack_from('<Q',image,optional+24)[0]
    rr,rs=struct.unpack_from('<II',image,optional+112+5*8)
    rawrel=pe.pe_read(image,rr,rs);relocations={};offset=0
    while offset<len(rawrel):
        page,size=struct.unpack_from('<II',rawrel,offset)
        if size<8 or size%2 or offset+size>len(rawrel):raise ValueError('Malformed relocation block')
        for entry in struct.unpack_from('<'+'H'*((size-8)//2),rawrel,offset+8):
            typ=entry>>12
            if typ:relocations[page+(entry&4095)]=typ
        offset+=size
    retained_identity=(BASE/'build16/identity.generated.h').read_text(encoding='utf8')
    retained_rvas=[int(x) for x in re.findall(r'\{(\d+),\d+,"[0-9a-f]{64}"\}',retained_identity)]
    code_ranges=[(r,32) for r in retained_rvas+rvas+scheduler_rvas+target_rvas+[callback_rva]]+helpers
    for r,n in code_ranges:
        if any(r<=a<r+n for a in relocations):raise ValueError('Relocated code guard requires separate canonicalization')
    vt_slots=[r+8*i for r in vtables for i in range(4)]
    if any(relocations.get(r)!=10 for r in vt_slots):raise ValueError('Vtable DIR64 domain mismatch')
    relocation_census=dict(preferred_base=hex(preferred),code_ranges=[dict(rva=hex(r),bytes=n) for r,n in code_ranges],
                           code_relocations=0,vtable_dir64_slots=[hex(r) for r in vt_slots])
    identity=(BASE/'build16/identity.generated.h').read_text(encoding='utf8')+extra
    (out/'identity.generated.h').write_text(identity,encoding='utf8',newline='\n')
    (out/'emitters.generated.h').write_bytes((BASE/'build16/emitters.generated.h').read_bytes())
    emitter=BASE/'build16/emitter-input.bin'
    if original['outputs'].get('emitter-input.bin')!=sha(emitter):
        raise ValueError('Native emitter input identity mismatch')
    pins[str(emitter)]=sha(emitter);(out/'emitter-input.bin').write_bytes(emitter.read_bytes())
    def plugin(text):
        text=replace(text,'0x00070000,"SOR Geometry Lifecycle Candidate"','0x00090000,"SOR Winner Causality Offline Candidate"')
        text=replace(text,'fs::path root=L"D:/Projects/starfield-outpost-research/.local-work/d5x/live";',
                     'fs::path root=L"D:/Projects/starfield-outpost-research/.local-work/d5am/live";')
        text=replace(text,'if(!geometry::configure_acquire(',
                     'U causal_locations[causal::site_count]{};for(unsigned i=0;i<causal::site_count;++i)causal_locations[i]=base+causal_rvas[i];\n  U scheduler_locations[13]{},scheduler_tables[3]{};for(unsigned i=0;i<13;++i)scheduler_locations[i]=base+scheduler_rvas[i];for(unsigned i=0;i<3;++i)scheduler_tables[i]=base+scheduler_vtables[i];\n  if(!causal::configure(causal_locations,causal_hashes,causal_helper_hashes)||!scheduler::configure(scheduler_locations,scheduler_hashes,scheduler_tables,scheduler_vtable_hashes,base+0x27ec2e0,scheduler_callback_hash,scheduler_target_hashes))return false;\n  if(!geometry::configure_acquire(')
        text=replace(text,'identity+=geometry::identity_metadata()+context::metadata()+lifetime::metadata();',
                     'identity+=geometry::identity_metadata()+context::metadata()+lifetime::metadata()+causal::metadata()+scheduler::metadata();')
        text=replace(text,'if(!install(geometry::edits,3,dirty)||','if(!install(causal::edits,causal::site_count,dirty)||!install(scheduler::edits,13,dirty)||!install(geometry::edits,3,dirty)||')
        text=replace(text,'if(!lifetime::begin()){','if(!lifetime::begin()||!causal::begin()||!scheduler::begin()){')
        return text
    mutate('plugin.cpp',plugin)
    def fixture(text):
        text=replace(text,'namespace {\nusing namespace winner;',
                     'namespace {\nusing namespace winner;\nvoid d5am_enable_provider(bool);void d5am_fixture_shared_phase(U);void d5am_fixture_writer(U);void d5am_fixture_finish();bool d5am_fixture_geometry_acquire(U);void d5am_fixture_geometry_release(U);')
        text=replace(text,'namespace {void d5ai_setup();void d5ai_fixture(Model&,const std::wstring&,HANDLE);}',
                     'namespace {void d5ai_setup();void d5ai_fixture(Model&,const std::wstring&,HANDLE);void d5am_setup_native();void d5am_run_native(U);void d5am_run_counter_faults();void d5am_run_loss_faults(U);void d5am_run_stop_fault(U,HANDLE);void d5am_run_owner_scope(U);void d5am_run_body_guard(HANDLE);void d5am_run_operand_fault(U);}')
        text=replace(text,'identity+=geometry::identity_metadata()+context::metadata()+lifetime::metadata();',
                     'if(s==L"d5am-native-lock"||s==L"d5am-native-stop"||s==L"d5am-native-guard"||s==L"d5am-native-operand"){d5am_setup_native();check(scheduler_fixture::setup_identity());}\n  identity+=geometry::identity_metadata()+context::metadata()+lifetime::metadata()+causal::metadata()+scheduler::metadata();if(s==L"d5am-native-lock"||s==L"d5am-native-stop"||s==L"d5am-native-guard"||s==L"d5am-native-operand")identity+=scheduler_fixture::metadata();')
        text=replace(text,'initialize_queue(sequence_origin);bool dirty=false;',
                     'initialize_queue(sequence_origin);check(causal::begin(true));check(scheduler::begin(true));bool dirty=false;')
        text=replace(text,'check(install(edits,18,dirty));',
                     'check(install(edits,18,dirty));if(s==L"d5am-native-lock"||s==L"d5am-native-stop"||s==L"d5am-native-guard"||s==L"d5am-native-operand")check(install(causal::edits,causal::site_count,dirty));')
        text=replace(text,'if(s!=L"prior-unknown"&&s!=L"ready-only")fixture_reset(m.proc_identity,0,0,0);',
                     'if(s!=L"prior-unknown"&&s!=L"ready-only")fixture_reset(m.proc_identity,0,0,0);')
        text=replace(text,'oracle("visited-store",*model,destination,token);}',
                     'oracle("visited-store",*model,destination,token);d5am_fixture_finish();}')
        text=replace(text,'extern "C" void fixture_after_token(uint64_t source){',
                     'extern "C" void fixture_after_token(uint64_t source){\n d5am_fixture_shared_phase(model->proc_identity);')
        text=replace(text,'extern "C" uint64_t fixture_driver(uint64_t frame,uint64_t proc){\n check(GetLastError()==0x9abc);',
                     'extern "C" uint64_t fixture_driver(uint64_t frame,uint64_t proc){\n check(GetLastError()==0x9abc);d5am_fixture_writer(proc);')
        text=replace(text,'if(s.starts_with(L"d5ai-"))d5ai_fixture(m,s,thread);',
                     'if(s==L"d5am-native-lock"||s==L"d5am-native-stop"||s==L"d5am-native-guard"||s==L"d5am-native-operand"){d5am_enable_provider(true);check(scheduler_fixture::invoke([&]{d5ai_fixture(m,L"d5ai-native-mask3a",thread);},10,11));d5am_enable_provider(false);d5am_run_native(m.proc_identity);if(s==L"d5am-native-stop")d5am_run_stop_fault(m.proc_identity,thread);if(s==L"d5am-native-guard")d5am_run_body_guard(thread);if(s==L"d5am-native-operand")d5am_run_operand_fault(m.proc_identity);}else if(s==L"d5am-causal-counter")d5am_run_counter_faults();else if(s==L"d5am-causal-loss")d5am_run_loss_faults(m.proc_identity);else if(s==L"d5am-causal-owners")d5am_run_owner_scope(m.proc_identity);else if(s.starts_with(L"d5ai-"))d5ai_fixture(m,s,thread);')
        text=replace(text,'if(s.starts_with(L"d5ai-"))d5ai_setup();',
                     'if(s.starts_with(L"d5ai-")||s==L"d5am-native-lock"||s==L"d5am-native-stop"||s==L"d5am-native-guard"||s==L"d5am-native-operand")d5ai_setup();')
        text=replace(text,'if(s.starts_with(L"d5ai-")){check(install(geometry::edits,3,dirty));',
                     'if(s.starts_with(L"d5ai-")||s==L"d5am-native-lock"||s==L"d5am-native-stop"||s==L"d5am-native-guard"||s==L"d5am-native-operand"){check(install(geometry::edits,3,dirty));')
        text+='\n#include "d5am_fixture.inc"\n'
        return text
    mutate('fixture.cpp',fixture)
    def fixture_asm(text):
        text=replace(text,'EXTERN reset_body:PROC','EXTERN reset_body:PROC\nEXTERN d5am_fixture_provider_finish:PROC')
        return replace(text,'finish:\n mov eax,12345h','finish:\n call d5am_fixture_provider_finish\n mov eax,12345h')
    mutate('fixture.asm',fixture_asm)
    def geometry_fixture(text):
        text=replace(text,'d5ai_native_mutex.lock_shared();auto readers=++d5ai_readers;',
                     'd5ai_native_mutex.lock_shared();auto readers=++d5ai_readers;if(d5am_fixture_geometry_acquire(lock))return d5ai_lock_result;')
        return replace(text,'--d5ai_readers;d5ai_native_mutex.unlock_shared();',
                       'd5am_fixture_geometry_release(m.proc_identity);--d5ai_readers;d5ai_native_mutex.unlock_shared();')
    mutate('d5ai_fixture.inc',geometry_fixture)
    commands=[f'call "{VC}"']
    for name,obj in (('bridges.asm','bridges.obj'),('fixture.asm','fixture-asm.obj'),('d5ai_bridge.asm','d5ai-bridge.obj'),('d5ai_context_fixture.asm','d5ai-context-fixture.obj'),('d5am_causality.asm','d5am-causality.obj'),('d5am_scheduler.asm','d5am-scheduler.obj')):
        commands.append(f'ml64 /nologo /c /Fo{obj} "{candidate/name}"')
    commands.extend([f'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD /I"{out}" "{candidate/"transport.cpp"}" "{candidate/"fixture.cpp"}" "{candidate/"plugin.cpp"}" bridges.obj fixture-asm.obj d5ai-bridge.obj d5ai-context-fixture.obj d5am-causality.obj d5am-scheduler.obj /LD /Fe:SorConstructionWinner.dll /link /Brepro /INCREMENTAL:NO bcrypt.lib',
                     f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD "{candidate/"host.cpp"}" /Fe:sor-d5x-fixture.exe /link /Brepro /INCREMENTAL:NO'])
    cmd=out/'build.cmd';cmd.write_text('@echo off\n'+'\nif errorlevel 1 exit /b 1\n'.join(commands)+'\n',encoding='utf8',newline='\r\n')
    derived={str(p.relative_to(tree)):sha(p) for p in tree.rglob('*') if p.is_file()}
    run=subprocess.run(['cmd','/d','/c',str(cmd)],cwd=out,capture_output=True)
    (out/'build.log').write_bytes(run.stdout+run.stderr)
    receipt=dict(schema='sor-d5am-candidate-build/1',authority='OFFLINE_ONLY',version='0.9.0-D5AM',
                 compilation=run.returncode,inputs=pins,derived=derived,causal_sites=[dict(rva=hex(r),guard_sha256=h) for r,h in zip(rvas,hashes)],
                 scheduler_sites=[dict(rva=hex(r),guard_sha256=h) for r,h in zip(scheduler_rvas,scheduler_hashes)],
                 scheduler_vtables=[dict(rva=hex(r),guard_sha256=h) for r,h in zip(vtables,vtable_hashes)],
                 scheduler_targets=[dict(site_index=i,rva=hex(r),guard_sha256=h) for i,r,h in zip(target_sites,target_rvas,target_hashes)],
                 scheduler_callback=dict(rva=hex(callback_rva),guard_sha256=callback_hash),
                 causal_helpers=[dict(rva=hex(rva),bytes=size,guard_sha256=h) for (rva,size),h in zip(helpers,helper_hashes)],
                 relocation_census=relocation_census,exe_sha256=pe.GAME_HASH,initial_free=initial_free,final_free=guard(),
                 source_unchanged=all(sha(p)==h for p,h in pins.items()),build_command_sha256=sha(cmd),
                 generated={name:sha(out/name) for name in ('identity.generated.h','emitters.generated.h','d5am_native.generated.h','emitter-input.bin')})
    if run.returncode==0:
        receipt['dll_sha256']=sha(out/'SorConstructionWinner.dll')
        requested=sys.argv[2:]
        cases=[r['case'] for r in original['cases']]+['d5am-native-lock','d5am-native-stop','d5am-native-guard','d5am-causal-counter','d5am-causal-loss','d5am-causal-owners','d5am-native-operand'] if requested==['--all'] else requested or ['normal','competing','nested','stop-under-production','d5ai-native-mask3a','d5ai-life-aba']
        expected={r['case']:r['expected'] for r in original['cases']}
        def qualify(case):
            guard()
            result=subprocess.run([str(out/'sor-d5x-fixture.exe'),str(out/'SorConstructionWinner.dll'),str(out/case),case],cwd=out,capture_output=True)
            (out/(case+'.log')).write_bytes(result.stdout+result.stderr)
            return dict(case=case,exit=result.returncode,expected=expected.get(case,0),pass_exit=result.returncode==expected.get(case,0))
        with ThreadPoolExecutor(max_workers=8) as pool:
            receipt['cases']=list(pool.map(qualify,cases))
    receipt['source_unchanged']=all(sha(p)==h for p,h in pins.items())
    (out/'build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(path=str(out),compilation=run.returncode,cases=receipt.get('cases',[]),dll_sha256=receipt.get('dll_sha256'))))
    if run.returncode or not receipt['source_unchanged'] or any(not r['pass_exit'] for r in receipt.get('cases',[])):
        raise RuntimeError('Candidate compilation, native case or source preservation failed; retained receipt controls')

if __name__=='__main__':
    main()
