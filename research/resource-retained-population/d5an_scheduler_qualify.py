# SPDX-License-Identifier: GPL-3.0-or-later
# Owned D5AM component method adapted under SOR-P-0002; uses exact D5AN object.
"""Qualify the separate D5AM scheduler component in a disposable owned host.

Reads pinned installed PE, retained native exports and owned sources. Writes a
fresh local build/receipt and synthetic wire streams; runs MSVC/MASM and the
authored fixture DLL in this Python process. No game, deployment, save, analysis
project, dependency installation, network or Git mutation. Native instruction
bytes remain local. Synthetic tasks do not establish retail scheduling rates.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import ctypes as C
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import threading
import zlib

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
EXE_SHA = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
RVAS = [0x76cea4, 0x76d07b, 0x7b56c5, 0x7b57eb, 0x27ec100, 0x27e6a00, 0x27e4ab0,
        0x27e4957, 0x27e61a4, 0x76d14f, 0x7b585f, 0x28d3960, 0x28d2b80]
FIELDS = 'sequence kind thread ticks node allocation family server rank serial dependencies registered state_flags pool mode status core_invocation core_selection source claim_context route epoch hazards extra'.split()


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    label = sys.argv[1]
    check(re.fullmatch('[a-z0-9-]+', label) is not None, 'Fresh bounded output label required')
    sys.path.insert(0, str(HERE))
    from d5am_chronology import guard
    initial_free = guard()
    build=Path(sys.argv[2]).resolve()
    check(build.is_relative_to(ROOT/'.local-work/d5an'),'D5AN exact build required')
    out = ROOT / '.local-work/d5an' / label
    out.mkdir(exist_ok=False)
    paths = [Path(__file__), HERE / 'd5an-scheduler-fixture.cpp', HERE / 'd5am-scheduler-fixture.asm',
             ROOT / 'runtime/construction-winner/d5an_scheduler.h', ROOT / 'runtime/construction-winner/d5am_scheduler.asm',
             ROOT / 'runtime/retained-population/build.py']
    paths += [build/'d5am-scheduler.obj',ROOT/'runtime/construction-winner/d5an_counter.h']
    pins = {str(p): sha(p) for p in paths}
    check(sha(ROOT/'runtime/construction-winner/d5an_scheduler.h')==sha(build/'candidate/runtime/construction-winner/d5am_scheduler.h'),'Exact header identity')
    check(sha(ROOT/'runtime/construction-winner/d5an_counter.h')==sha(build/'candidate/runtime/construction-winner/d5an_counter.h'),'Exact helper identity')
    (out/'scheduler.obj').write_bytes((build/'d5am-scheduler.obj').read_bytes())
    check(sha(EXE) == EXE_SHA, 'Installed PE identity')
    exports = {
        '.local-work/d5ae/export02/native.tsv': 'e1f4ccf559a01411bf05c11a793bf2e1a90220e7c580bb455f1787acd6275599',
        '.local-work/d5ae/export03/native.tsv': '25d6455a678dc953eec2a0d1f521296777e467f1613c7b600c23b7920c6d5b05',
        '.local-work/d5ae/export05/native.tsv': '5da3f0fd1442e5f2a128f48421117826397cfc1c1f76f146059952902b900483',
        '.local-work/d5s/export20/native.tsv': '9efd0287fac24d167e5321766cdfc1b42a7575446f754e36a04bccbdf4a7678a',
        '.local-work/d5r/export01/native.tsv': '0ce62129bd4e6057318e62a3e2fbb588000ed160d51ab9373206085aabc4e785',
    }
    for relative, expected in exports.items():
        path = ROOT / relative
        check(sha(path) == expected, 'Retained native export identity')
        pins[str(path)] = expected
    spec = importlib.util.spec_from_file_location('owned_pe', ROOT / 'runtime/retained-population/build.py')
    pe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe)
    image = EXE.read_bytes()
    nt=struct.unpack_from('<I',image,0x3c)[0];optional=nt+24
    check(struct.unpack_from('<H',image,optional)[0]==0x20b and
          struct.unpack_from('<Q',image,optional+24)[0]==0x140000000,'Pinned PE64 preferred base')
    reloc_rva,reloc_bytes=struct.unpack_from('<II',image,optional+112+5*8)
    reloc_raw=pe.pe_read(image,reloc_rva,reloc_bytes);relocations={};cursor=0
    while cursor<len(reloc_raw):
        page,size=struct.unpack_from('<II',reloc_raw,cursor)
        check(size>=8 and size%2==0 and cursor+size<=len(reloc_raw),'Bounded PE relocation block')
        for entry in struct.unpack_from('<'+str((size-8)//2)+'H',reloc_raw,cursor+8):
            if entry>>12:relocations[page+(entry&4095)]=entry>>12
        cursor+=size
    vt_rvas=[0x4b3d0e8,0x4b3d138,0x4b406b8]
    for rva in vt_rvas:
        check({a:t for a,t in relocations.items() if rva<=a<rva+32}=={rva+i*8:10 for i in range(4)},
              'Exact four VT DIR64 fields required')
    code_ranges=[(r,32) for r in RVAS+[0x22cc410,0x22cc48f,0x22cc3f2,0x22cc366,0x2c45c2,
                  0x2c45e7,0x79fc85,0x79e027,0x21e0a87,0x79fcb3,0x22cc3c3,0x27ec2e0]]
    code_ranges += [(0x22cc350,126),(0x22cc3d0,216),(0x2c45a0,81)]
    target_sites=[0,1,2,3,9,10];targets=[]
    for i in target_sites:
        call=pe.pe_read(image,RVAS[i],5);check(call[0]==0xe8,'Original typed call opcode')
        target=RVAS[i]+5+struct.unpack_from('<i',call,1)[0]
        targets.append(target);code_ranges.append((target,32))
    check(targets==[0x27e5630]*4+[0x76c560,0x7b5160],'Exact source-pinned typed original targets')
    check(not [(a,t) for a,t in relocations.items() if any(r<=a<r+n for r,n in code_ranges)],
          'Unexpected relocation inside a guarded code window/body')
    sites = [dict(rva=rva, window=pe.pe_read(image, rva, 32).hex(),
                  guard_sha256=hashlib.sha256(pe.pe_read(image, rva, 32)).hexdigest()) for rva in RVAS]
    source_copy=out/'sources';source_copy.mkdir()
    for path in paths:
        (source_copy/path.name).write_bytes(path.read_bytes())
    (out/'inputs.json').write_text(json.dumps(dict(source_sha256=pins,sites=sites,installed_pe_sha256=EXE_SHA,
        interpreter=dict(path=sys.executable,sha256=sha(sys.executable))),indent=2)+'\n',encoding='utf8',newline='\n')
    commands = [f'call "{VC}"',
                f'ml64 /nologo /c /Fofixture.obj "{HERE / "d5am-scheduler-fixture.asm"}"',
                f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD /arch:AVX "{HERE / "d5an-scheduler-fixture.cpp"}" scheduler.obj fixture.obj /LD /Fe:SorConstructionWinner-0.9.2-D5AN-scheduler-component.dll /link /Brepro /INCREMENTAL:NO /EXPORT:D5AM_sched_probe']
    command = out / 'build.cmd'
    command.write_text('@echo off\n' + '\nif errorlevel 1 exit /b 1\n'.join(commands) + '\n', encoding='utf8', newline='\r\n')
    built = subprocess.run(['cmd', '/d', '/c', str(command)], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(built.stdout + built.stderr)
    check(built.returncode == 0, 'Native component build failed; preserve build.log')
    dll_path = out / 'SorConstructionWinner-0.9.2-D5AN-scheduler-component.dll'
    dll = C.CDLL(str(dll_path))
    class Event(C.Structure):
        _fields_ = [(field, C.c_uint64) for field in FIELDS] + [('request', C.c_int32 * 2),
                   ('native_key', C.c_uint32 * 3), ('discriminator', C.c_uint32 * 3), ('queue', C.c_uint64 * 6)]
    class Cookie(C.Structure):
        _fields_ = [(name, C.c_uint64) for name in 'key_low key_high vtable allocation serial slot'.split()]
    check(C.sizeof(Event) == 272 and C.sizeof(Cookie) == 48, 'Component layout')
    for name, args, result in [
        ('D5AM_initialize', [], C.c_uint64), ('D5AM_vtable', [C.c_uint], C.c_uint64),
        ('D5AM_vtable_guard',[C.c_uint64,C.c_uint64,C.c_char_p],C.c_uint64),
        ('D5AM_target_guard',[C.c_uint64,C.c_char_p],C.c_uint64),
        ('D5AM_dispatch_argument',[C.c_uint64],None),
        ('D5AM_ready_serial',[C.c_uint64,C.c_uint64,C.c_uint],None),
        ('D5AM_register', [C.c_uint64, C.c_uint], C.c_uint64), ('D5AM_stage', [C.c_uint64, C.c_uint64], None),
        ('D5AM_cookie', [C.c_uint64, C.POINTER(Cookie)], None), ('D5AM_stale', [C.c_uint64, C.POINTER(Cookie)], None),
        ('D5AM_callback', [C.c_uint64, C.c_uint64], C.c_uint64), ('D5AM_pop', [C.POINTER(Event)], C.c_uint64),
        ('D5AM_request_mismatch',[C.c_uint64],C.c_uint64),
        ('D5AM_metric', [C.c_uint], C.c_uint64), ('D5AM_sched_probe', [C.c_uint64, C.c_uint64, C.c_void_p], None),
        ('D5AM_claim', [C.c_uint64, C.c_uint64], C.c_uint64), ('D5AM_publish', [C.c_uint64, C.c_uint64], C.c_uint64),
        ('D5AM_claim_pool', [C.c_uint64, C.c_uint64,C.c_uint64], C.c_uint64),
        ('D5AM_admission_pause',[C.c_uint64,C.c_uint64,C.c_uint64],None),
        ('D5AM_action',[C.c_uint,C.c_uint64,C.c_uint64,C.c_uint64],C.c_uint64),
        ('D5AM_enabled', [C.c_uint], None), ('D5AM_registry_busy', [C.c_uint64, C.c_uint], None),
        ('D5AM_offer', [C.c_uint64, C.c_uint], None), ('D5AM_pause', [C.c_uint64, C.c_uint64], None),
        ('D5AM_counter', [C.c_uint, C.c_uint64], None), ('D5AM_serial', [C.c_uint64, C.c_uint64], None),
        ('D5AM_written', [], C.c_uint64),
    ]:
        function = getattr(dll, name)
        function.argtypes, function.restype = args, result
    k = C.WinDLL('kernel32', use_last_error=True)
    k.SetLastError.argtypes = [C.c_uint]
    k.CreateEventW.argtypes = [C.c_void_p, C.c_int, C.c_int, C.c_wchar_p]
    k.CreateEventW.restype = C.c_void_p
    k.WaitForSingleObject.argtypes = [C.c_void_p, C.c_uint]
    k.SetEvent.argtypes = [C.c_void_p]
    k.CloseHandle.argtypes = [C.c_void_p]
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_uint,C.c_uint];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_uint,C.POINTER(C.c_uint)]
    k.VirtualFree.argtypes=[C.c_void_p,C.c_size_t,C.c_uint]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    cases, captures, backing = [], {}, []
    def initialize():
        check(dll.D5AM_initialize() == 1, 'Host AVX/state initialization')
    def node(key=1, family=0):
        data = C.create_string_buffer(0x100)
        backing.append(data)
        address = C.addressof(data)
        populate(address, key, family)
        return address
    def populate(address, key, family=0):
        C.memset(address, 0, 0x100)
        C.c_uint64.from_address(address).value = dll.D5AM_vtable(family)
        C.memmove(address + 8, struct.pack('<3I', key, 23, 0), 12)
        C.c_ubyte.from_address(address + 0xa0).value = 2
        C.c_ubyte.from_address(address + 0xa8).value = 2
        C.memmove(address + 0xb0, struct.pack('<2i3I', 5, 0, 195, 109, 0), 20)
    def drain():
        rows, event = [], Event()
        while dll.D5AM_pop(C.byref(event)):
            row = {field: getattr(event, field) for field in FIELDS}
            row.update(request=list(event.request), native_key=list(event.native_key), discriminator=list(event.discriminator), queue=list(event.queue))
            rows.append(row)
        return rows
    def passed(name, rows=None, **details):
        cases.append(dict(name=name, result='PASS', **details))
        if rows is not None:
            captures[name] = rows
    passed('exact-pe-relocation-map',vtable_dir64_slots=12,guarded_code_ranges=len(code_ranges))
    for target in sorted(set(targets)):
        raw=pe.pe_read(image,target,32);expected=hashlib.sha256(raw).hexdigest().encode('ascii')
        owned=C.create_string_buffer(raw)
        check(dll.D5AM_target_guard(C.addressof(owned),expected),'Static PE target guard positive failed')
        passed('original-target-static-positive-'+hex(target),guard_sha256=expected.decode())
        owned[15]=bytes([owned.raw[15]^1])
        check(not dll.D5AM_target_guard(C.addressof(owned),expected),'Modified original target learned as baseline')
        passed('original-target-changed-byte-refused-'+hex(target))
    for index,rva in enumerate(vt_rvas):
        static=pe.pe_read(image,rva,32);values=struct.unpack('<4Q',static);digest=hashlib.sha256(static).hexdigest().encode('ascii')
        for moved_base in (0x180000000,140702155276288):
            projected=(C.c_uint64*4)(*(v-0x140000000+moved_base for v in values))
            check(dll.D5AM_vtable_guard(C.addressof(projected),moved_base,digest),'ASLR VT canonical positive failed')
            passed('vtable-aslr-'+str(index)+'-'+hex(moved_base),canonical_sha256=digest.decode())
            projected[2]^=1
            check(not dll.D5AM_vtable_guard(C.addressof(projected),moved_base,digest),'Changed relocated callback admitted')
            passed('vtable-aslr-corruption-'+str(index)+'-'+hex(moved_base))
        projected[0]=moved_base-1
        check(not dll.D5AM_vtable_guard(C.addressof(projected),moved_base,digest),'Below-image VT operand admitted')
        projected[0]=moved_base+0x100000000
        check(not dll.D5AM_vtable_guard(C.addressof(projected),moved_base,digest),'Out-of-image VT operand admitted')
        passed('vtable-aslr-pointer-domain-'+str(index))
    initialize()
    a = node()
    check(dll.D5AM_register(a, 1) == 0x123456, 'Original register result changed')
    rows = drain()
    check([r['kind'] for r in rows] == [1, 2, 3, 7, 9, 8] and all(r['allocation'] == 1 and not r['status'] for r in rows), 'Birth before synchronous dispatch/provider')
    passed('publication-before-synchronous-work', rows)
    initialize()
    a, b = node(), node(2, 2)
    dll.D5AM_register(a, 0);dll.D5AM_register(b, 0);drain()
    check(dll.D5AM_callback(a, b) == 0x55, 'Original worker result changed')
    rows = drain();providers = [r for r in rows if r['kind'] == 9]
    check([r['allocation'] for r in providers] == [1, 2, 1] and all(r['core_invocation'] and not r['status'] for r in providers), 'Nested TLS scope did not restore parent')
    passed('density-layer-nested-provider-join', rows)
    initialize();a = node();dll.D5AM_stage(a, 3);rows = drain()
    check(rows[0]['status'] & 2 and not rows[0]['allocation'], 'Preexisting task acquired invented birth')
    passed('preexisting-task-refused', rows)
    for same_key in (False, True):
        initialize();a = node();dll.D5AM_register(a, 0);old = Cookie();dll.D5AM_cookie(a, C.byref(old));dll.D5AM_stage(a, 4)
        populate(a, 1 if same_key else 2);dll.D5AM_register(a, 0);dll.D5AM_stale(a, C.byref(old));rows = drain()
        check(rows[-1]['status'] & 4 and not rows[-1]['allocation'] and rows[-2]['allocation'] == 2, 'Task address ABA promoted stale allocation')
        passed('same-key-aba' if same_key else 'changed-key-aba', rows)
    initialize();a = node();dll.D5AM_register(a, 0);dll.D5AM_register(a, 0);rows = drain()
    check(rows[-1]['status'] & 16 and not rows[-1]['allocation'], 'Duplicate live publication accepted')
    passed('duplicate-publication-refused', rows)
    initialize();a = node();dll.D5AM_register(a, 0);dll.D5AM_registry_busy(a, 1);dll.D5AM_stage(a, 3);rows = drain()
    check(rows[-1]['status'] & 4 and not rows[-1]['allocation'], 'Odd registry serial accepted')
    passed('in-progress-registry-refused', rows)
    for replacement in (1,2):
        initialize();a=node(family=0);dll.D5AM_register(a,0);drain()
        C.c_uint64.from_address(a).value=dll.D5AM_vtable(replacement)
        dll.D5AM_stage(a,3);changed=drain()
        check(len(changed)==1 and changed[0]['status']&4 and not changed[0]['allocation'],
              'Same-key replacement vtable promoted old allocation')
        passed('same-key-different-'+('density-vtable' if replacement==1 else 'task-family'),changed)
    initialize();a=node();dll.D5AM_register(a,0);drain()
    check(dll.D5AM_request_mismatch(a)==0x55,'Native callback result changed for mismatch control')
    mismatch=drain();providers=[row for row in mismatch if row['kind']==9]
    check(len(providers)==1 and providers[0]['status']&4,'Original provider/task request mismatch was promoted')
    passed('provider-task-original-request-mismatch-refused',mismatch)
    pattern = struct.pack('<4Q', 0x0123456789abcdef, 0xfedcba9876543210, 0xa55aa55aa55aa55a, 0x55aa55aa55aa55aa)
    def admission_run(label,phase,operation,original_check=None,pre_original_check=None):
        ready=k.CreateEventW(None,0,0,None);resume=k.CreateEventW(None,0,0,None)
        check(ready and resume,'Admission pause handles unavailable')
        dll.D5AM_admission_pause(ready,resume,phase)
        outcome=[];errors=[]
        def run():
            try:outcome.append(operation())
            except BaseException as error:errors.append(repr(error))
        producer=threading.Thread(target=run);before=dll.D5AM_metric(0);producer.start()
        reached=k.WaitForSingleObject(ready,5000)==0
        try:
            check(reached,'Admission barrier was not reached: '+label)
            core,own,bridge=(dll.D5AM_metric(n) for n in (12,3,9))
            check((core==own==bridge==0) if phase==0 else (core>0 and (own>0 or bridge>0)),
                  'Wrong STOP admission interval counters: '+label)
            if pre_original_check:pre_original_check()
            dll.D5AM_enabled(0)
        finally:
            k.SetEvent(resume);producer.join(5);k.CloseHandle(ready);k.CloseHandle(resume)
        check(not producer.is_alive() and not errors,'Paused producer failed to resume: '+label)
        rows=drain()
        check((not rows and dll.D5AM_metric(0)==before) if phase==0 else bool(rows),
              'Post-STOP late admission or admitted-prefix loss: '+label)
        check(all(dll.D5AM_metric(n)==0 for n in (3,9,12)),'Admission rollback/quiescence unbalanced: '+label)
        if original_check:original_check(outcome)
        passed(label+'-phase'+str(phase),rows,phase=phase,pre_disable=dict(core=core,own=own,bridge=bridge),
               scope='Actual admission primitive; disable models STOP cut. Worker terminal/flush qualified separately.')
    for phase in (0,1):
        for kind in (2,3,4,5,6,10,11):
            initialize();a=node();dll.D5AM_register(a,0);drain();C.c_uint32.from_address(a+0x90).value=1
            output=C.create_string_buffer(592)
            baseline_calls=dll.D5AM_metric(14)
            def native_operation(a=a,kind=kind,output=output):
                dll.D5AM_sched_probe(a,kind,output);return 1
            def native_original(outcome,kind=kind,a=a,output=output):
                check(output.raw[64:576]==pattern*16,'Admission probe changed live YMM state')
                flags=struct.unpack_from('<Q',output.raw)[0]
                check(bool(flags&0x40) and C.c_uint32.from_address(a+0x90).value==0 if kind==6 else bool(flags&1),
                      'Admission race changed native instruction/flags')
                if kind in (10,11):check(dll.D5AM_metric(14)==2,'Native entry original helper not called exactly once')
            def native_before(kind=kind,a=a,baseline_calls=baseline_calls):
                if kind in (10,11):check(dll.D5AM_metric(14)==baseline_calls,'Original helper ran before admission')
                if kind==6:check(C.c_uint32.from_address(a+0x90).value==1,'Native ADD ran before admission barrier')
            admission_run('native-admission-'+str(kind),phase,native_operation,native_original,native_before)
        for action in range(10):
            initialize();a=node(family=2 if action==5 else 0)
            if action>=4:dll.D5AM_register(a,0);drain()
            baseline_calls=dll.D5AM_metric(14)
            context=C.create_string_buffer(0x100);command=(C.c_uint64*4)(0,0x123456780,a,0x7777);address=C.c_uint64(C.addressof(command)|1)
            expected=0x123456 if action<4 else 0x55 if action<6 else 0x123 if action==6 else C.addressof(address) if action==7 else 0x88 if action==8 else 0x99
            def cpp_operation(action=action,a=a,context=context,address=address):
                return dll.D5AM_action(action,a,C.addressof(context),C.addressof(address))
            def cpp_original(outcome,action=action,baseline_calls=baseline_calls,expected=expected):
                check(outcome==[expected] and dll.D5AM_metric(14)-baseline_calls==(1 if action<8 else 0),
                      'C++ original operation changed across admission race')
            def cpp_before(baseline_calls=baseline_calls):
                check(dll.D5AM_metric(14)==baseline_calls,'C++ original helper ran before admission')
            admission_run('cpp-admission-'+str(action),phase,cpp_operation,cpp_original,cpp_before)
    for target in ('cpp-own','native-own','native-bridge','native-core'):
        initialize();a=node();dll.D5AM_register(a,0);drain();C.c_uint32.from_address(a+0x90).value=1
        counter=5 if target.endswith('own') else 7 if target=='native-bridge' else 6
        dll.D5AM_counter(counter,2**64-1)
        if target=='cpp-own':dll.D5AM_stage(a,3)
        else:
            output=C.create_string_buffer(592);dll.D5AM_sched_probe(a,6,output)
            check(C.c_uint32.from_address(a+0x90).value==0 and struct.unpack_from('<Q',output.raw)[0]&0x40 and
                  output.raw[64:576]==pattern*16,'Saturation changed original decrement/flags/YMM')
        check(not drain() and dll.D5AM_metric(11)&1,'Saturated admission emitted a false healthy event')
        expected=[2**64-1 if counter==n else 0 for n in (5,7,6)]
        check([dll.D5AM_metric(n) for n in (3,9,12)]==expected,'Saturation failed to roll back other counters')
        passed('admission-saturation-rollback-'+target)
    for kind in (2, 3, 4, 5, 6, 10, 11):
        initialize();a = node();dll.D5AM_register(a, 0);drain();C.c_uint32.from_address(a + 0x90).value = 1
        output = C.create_string_buffer(592);k.SetLastError(0x1234)
        dll.D5AM_sched_probe(a, kind, output);rows = drain();words = struct.unpack_from('<8Q', output.raw)
        check(output.raw[64:576] == pattern * 16, 'Live YMM state changed')
        check((words[1] == a if kind not in (10,11) else words[1] == 0x123 if kind==11 else bool(words[1])) and
              (words[4] == 0x8888888888888888 if kind!=10 else bool(words[4])) and words[6] == 0xaaaaaaaaaaaaaaaa, 'Volatile GPR changed')
        check(words[5] == (0x123456789 if kind == 5 else 1 if kind==10 else 0x9999999999999999), 'Native R9 semantics changed')
        check(struct.unpack_from('<Q', output.raw, 576)[0] == 0x1234, 'Native LastError changed')
        check([r['kind'] for r in rows] == ([11,12] if kind==11 else [kind]) and all(not r['status'] for r in rows) and
              (dll.D5AM_metric(8) >= 4 if kind not in (10,11) else True), 'Bridge event/unwind witness failed')
        if kind == 6:
            check(C.c_uint32.from_address(a + 0x90).value == 0 and words[0] & 0x40, 'Dependency decrement/branch ZF changed')
        else:
            check(words[0] & 1, 'Native carry flag changed')
        check(dll.D5AM_metric(9) == 0, 'Bridge producer did not retire')
        passed('bridge-abi-' + str(kind), rows, unwind_stack_frames=dll.D5AM_metric(8), all_sixteen_ymm=True)
    for argument in (0,1,0x101,0x1234567800000080):
        initialize();a=node();dll.D5AM_register(a,0);drain()
        C.c_ubyte.from_address(a+0xa0).value=0x5a;dll.D5AM_dispatch_argument(argument)
        output=C.create_string_buffer(592);dll.D5AM_sched_probe(a,3,output);rows=drain()
        check(len(rows)==1 and rows[0]['kind']==3 and rows[0]['extra']==argument&255 and rows[0]['mode']==0x5a,
              'Dispatch incoming R8B was conflated with raw node+a0 byte')
        check(struct.unpack_from('<Q',output.raw,32)[0]==argument and output.raw[64:576]==pattern*16 and
              struct.unpack_from('<Q',output.raw)[0]&1 and dll.D5AM_metric(8)>=4,
              'Dispatch operand probe changed native argument/flags/YMM/unwind')
        passed('dispatch-native-r8-low-byte-'+hex(argument),rows,all_sixteen_ymm=True)
    for consumed in (0,1,0xffffffffffffffff):
        initialize();a=node();dll.D5AM_register(a,0);drain()
        replacement=0x9876543210;dll.D5AM_ready_serial(consumed,replacement,1)
        output=C.create_string_buffer(592);dll.D5AM_sched_probe(a,5,output);rows=drain()
        check(len(rows)==1 and rows[0]['kind']==5 and rows[0]['extra']==consumed and rows[0]['serial']==0,
              'Consumed native tree serial conflated with old node serial or later reread')
        check(struct.unpack_from('<Q',output.raw,40)[0]==consumed and dll.D5AM_metric(15)==a and dll.D5AM_metric(16)==replacement and
              output.raw[64:576]==pattern*16 and struct.unpack_from('<Q',output.raw)[0]&1 and
              not dll.D5AM_metric(6),'Ready probe changed native R9/stackMOV/flags/YMM or treated engineMAX as observer fault')
        passed('ready-consumed-serial-no-reread-'+hex(consumed),rows,mutated_tree=replacement,
               limits='Tests stolen read/stackMOV only. Native later node+88 assignment and insertion are distinct boundaries.')
    original_add=pe.pe_read(image,0x27e61a4,7)
    check(original_add==bytes.fromhex('838090000000ff'),'Guarded dependency instruction differs')
    code=bytes.fromhex('4889c8')+original_add+bytes.fromhex('9c58c3')
    memory=k.VirtualAlloc(None,4096,0x3000,4);check(memory,'Owned instruction page allocation failed');C.memmove(memory,code,len(code));old=C.c_uint()
    check(k.VirtualProtect(memory,4096,0x20,C.byref(old)) and k.FlushInstructionCache(k.GetCurrentProcess(),memory,4096),'Owned instruction page execute guard failed')
    native_add=C.WINFUNCTYPE(C.c_uint64,C.c_void_p)(memory)
    for value in (0,1,2,0x80000000):
        initialize();a=node();dll.D5AM_register(a,0);drain();shadow=C.create_string_buffer(0x100)
        C.c_uint32.from_address(C.addressof(shadow)+0x90).value=value;expected_flags=native_add(C.addressof(shadow))
        C.c_uint32.from_address(a+0x90).value=value;output=C.create_string_buffer(592);dll.D5AM_sched_probe(a,6,output)
        actual_flags=struct.unpack_from('<Q',output.raw)[0]
        check(actual_flags&0x8d5==expected_flags&0x8d5 and C.c_uint32.from_address(a+0x90).value==(value-1)&0xffffffff,'Original ADD flags/operand differ from bridge')
        passed('original-add-flags-'+str(value),drain(),arithmetic_flags=actual_flags&0x8d5)
    check(k.VirtualFree(memory,0,0x8000),'Owned instruction page release failed')
    initialize();a = node();C.c_uint64.from_address(a).value = 0x123;C.c_uint32.from_address(a + 0x90).value = 2
    output = C.create_string_buffer(592);dll.D5AM_sched_probe(a, 6, output)
    check(not drain() and C.c_uint32.from_address(a + 0x90).value == 1 and output.raw[64:576] == pattern * 16, 'Unmatched native path changed')
    passed('unmatched-native-filter', all_sixteen_ymm=True)
    initialize();a = node();dll.D5AM_register(a, 0);drain()
    context = C.create_string_buffer(0x100);command_data = (C.c_uint64 * 4)(0, 0x123456780, a, 0x7777);address = C.c_uint64(C.addressof(command_data) | 1)
    check(dll.D5AM_claim(C.addressof(context), C.addressof(address)) == C.addressof(address), 'Claim result changed')
    check(dll.D5AM_publish(C.addressof(context), C.addressof(address)) == 0x123, 'Queue result changed')
    rows = drain();check([r['kind'] for r in rows] == [10, 11, 12] and all(r['allocation'] == 1 and not r['status'] for r in rows), 'Claim/queue boundary joins failed')
    passed('queued-claim-and-publication-boundaries', rows)
    # The same owned command address/tag alone is never a task lifetime ID.
    tagged=C.addressof(command_data)|1
    check(all(r['extra']==tagged for r in rows),'Native tagged command operand was not copied')
    check(rows[0]['pool']==0 and rows[0]['claim_context']==C.addressof(context),'Actual claim argument/context differs')
    passed('tagged-command-native-operands',rows)
    pool=C.create_string_buffer(64)
    dll.D5AM_claim_pool(C.addressof(context),C.addressof(address),C.addressof(pool))
    copied=drain();check(len(copied)==1 and copied[0]['pool']==C.addressof(pool) and copied[0]['extra']==tagged,'Actual claim pool operand missing')
    passed('claim-actual-pool-operand',copied)
    command_data[1]=0xdeadbeef
    dll.D5AM_publish(C.addressof(context),C.addressof(address));check(not drain(),'Foreign reused command callback was admitted')
    passed('reused-command-foreign-callback-refused')
    command_data[1]=0x123456780
    dll.D5AM_stage(a,4);populate(a,2)
    dll.D5AM_claim_pool(C.addressof(context),C.addressof(address),C.addressof(pool))
    stale=drain();last=stale[-1]
    check(last['kind']==10 and last['extra']==tagged and last['status'] and not last['allocation'],'Same command tag promoted retired/reused task')
    passed('same-command-tag-node-aba-refused',stale)
    dll.D5AM_register(a,0);drain()
    dll.D5AM_claim_pool(C.addressof(context),C.addressof(address),C.addressof(pool));renewed=drain()
    check(len(renewed)==1 and renewed[0]['allocation']==2 and not renewed[0]['status'] and renewed[0]['extra']==tagged,'New task lifetime was not distinct at reused command address')
    passed('reused-command-new-task-allocation',renewed)
    initialize();a = node();dll.D5AM_register(a, 0);drain();ready = k.CreateEventW(None, 0, 0, None);resume = k.CreateEventW(None, 0, 0, None)
    check(ready and resume, 'Fixture pause handles unavailable')
    dll.D5AM_pause(ready, resume);output = C.create_string_buffer(592)
    producer = threading.Thread(target=lambda: dll.D5AM_sched_probe(a, 6, output));producer.start()
    check(k.WaitForSingleObject(ready, 5000) == 0 and dll.D5AM_metric(9) == 1, 'Native copied-cookie pause not reached')
    dll.D5AM_stage(a, 4);populate(a, 2);dll.D5AM_register(a, 0);dll.D5AM_pause(0, 0);k.SetEvent(resume);producer.join(5)
    check(not producer.is_alive(), 'Native fixture producer did not resume')
    rows = drain();late = [r for r in rows if r['kind'] == 6]
    check(len(late) == 1 and late[0]['status'] & 4 and not late[0]['allocation'] and dll.D5AM_metric(9) == 0, 'Paused native producer ABA promoted new task')
    k.CloseHandle(ready);k.CloseHandle(resume)
    passed('native-paused-producer-aba', rows)
    initialize();a = node();dll.D5AM_register(a, 0);drain();dll.D5AM_enabled(0);dll.D5AM_stage(a, 3);dll.D5AM_sched_probe(a, 6, output)
    check(not drain() and not dll.D5AM_metric(9), 'Inert STOP emitted scheduler events')
    passed('inert-stop')
    initialize();dll.D5AM_offer(10000, 4);rows = drain()
    check(len(rows) + dll.D5AM_metric(2) == 40000 and dll.D5AM_metric(2) and dll.D5AM_metric(6), 'Queue saturation accounting failed')
    check([r['sequence'] for r in rows] == list(range(1, len(rows) + 1)), 'Concurrent admission sequence invalid')
    passed('queue-saturation', None, offered=40000, admitted=len(rows), losses=dll.D5AM_metric(2))
    initialize();dll.D5AM_recursive_offer();check(dll.D5AM_metric(2) == dll.D5AM_metric(7) == 1, 'Recursive event loss not counted')
    passed('reentrancy-loss')
    initialize();collision = C.create_string_buffer(65 * 0x80000 + 0x100)
    for i in range(65):
        pointer = C.addressof(collision) + i * 0x80000;populate(pointer, i + 1);dll.D5AM_register(pointer, 0)
    rows = drain();check(rows[-1]['status'] & 32 and not rows[-1]['allocation'] and dll.D5AM_metric(4) == 1, 'Bounded registry saturation hidden')
    passed('registry-saturation', rows)
    for counter in range(8):
        initialize();a = node();dll.D5AM_counter(counter, 2**64 - 1)
        if counter == 0:
            dll.D5AM_register(a, 0)
        elif counter == 1:
            dll.D5AM_register(a, 0);dll.D5AM_registry_busy(a, 1);dll.D5AM_register(a, 0)
        elif counter==2:
            dll.D5AM_stage(a, 3)
        elif counter in (3,4):
            dll.D5AM_recursive_offer()
        elif counter in (5,6):
            dll.D5AM_stage(a,3)
        else:
            dll.D5AM_register(a,0);drain();dll.D5AM_sched_probe(a,6,output)
        check(dll.D5AM_metric(6), 'Counter wrap did not fail closed')
        metric=[10,4,5,2,7,3,12,9][counter]
        check(dll.D5AM_metric(metric)==2**64-1,'Saturated counter did not retain MAX')
        passed('counter-overflow-' + str(counter), drain(),saturated_value=dll.D5AM_metric(metric))
    initialize();dll.D5AM_counter(8,2**64-1);check(not dll.D5AM_written() and dll.D5AM_metric(13)==2**64-1 and dll.D5AM_metric(6),'Writer counter overflow not saturated')
    passed('writer-counter-overflow')
    initialize();a = node();dll.D5AM_register(a, 0);dll.D5AM_serial(a, 2**64 - 2);dll.D5AM_stage(a, 4)
    check(dll.D5AM_metric(6), 'Registry serial overflow not refused')
    passed('registry-serial-overflow', drain())
    for flags,environment in ((['-E','-B','-O'],None),(['-E','-B','-OO'],None),(['-E','-B'],dict(os.environ,PYTHONOPTIMIZE='1'))):
        refused=subprocess.run([sys.executable,*flags,str(Path(__file__)),'unused'],capture_output=True,text=True,env=environment)
        check(refused.returncode!=0 and 'optimization is forbidden' in refused.stderr,'Qualification optimization not refused')
        passed('optimization-refusal-'+str(flags)+('-environment' if environment else ''))
    for path, expected in pins.items():
        check(sha(path) == expected, 'Pinned source changed during qualification')
    identity = 'c' * 64
    for name, rows in captures.items():
        if not rows:
            continue
        data = bytearray(struct.pack('<4Q64s', 0x314843534d413544, 1, 272, 0, identity.encode()))
        for row in rows:
            payload = struct.pack('<24Q2i6I6Q', *(row[f] for f in FIELDS), *row['request'], *row['native_key'], *row['discriminator'], *row['queue'])
            data += struct.pack('<II', len(payload), zlib.crc32(payload)) + payload
        (out / (name + '.bin')).write_bytes(data)
    receipt = dict(state='PASS', cases=cases, source_sha256=pins, dll_sha256=sha(dll_path), installed_pe_sha256=EXE_SHA,
                   sites=sites, free_before=initial_free, free_after=guard(), synthetic_identity=identity,
                   evidence='Exact integrated scheduler object and matching production header with owned task objects, guarded original sites and a separate ABI oracle. Native game scheduler and retail worker distribution were not executed.',
                   derivative_framing='The .bin files are qualifier-authored frames around actual admitted producer Event values. Original event sequences are preserved, including gaps before each drained subset. Synthetic identity c*64 is not a SHA-256 preimage or production identity/ACK/flush proof; production readers must refuse incompatible identity or sequence completeness.',
                   limits='Component qualification only. Full candidate integration, old observer regression, actual producer spool/flush replay and complete original native helper pathway tests remain separate.')
    (out / 'qualification.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(state='PASS', cases=len(cases), captures=len(captures), dll_sha256=receipt['dll_sha256'])))


if __name__ == '__main__':
    main()
