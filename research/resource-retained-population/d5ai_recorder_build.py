# SPDX-License-Identifier: GPL-3.0-or-later
"""Build a separate offline D5AI derivative without altering schema-4 sources.

Reads owned construction-winner sources, approved unchanged PluginAPI header,
installed pinned EXE/tools and identity inputs. Writes only fresh ignored D5AI
candidate/build trees, logs, receipts and disposable captures. Compiles and runs
owned native hosts; never starts, attaches to, deploys into or changes Starfield.
SOR-P-0002 covers the explicitly recorded source-informed adaptations. Stop on
source replacement mismatch, identity drift, failed disk guards or compilation.
"""
from pathlib import Path
import hashlib
import json
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'runtime/construction-winner'
CASES = ('d5ai-normal d5ai-empty d5ai-read-fault d5ai-malformed d5ai-arena-full '
         'd5ai-overflow d5ai-retire-during d5ai-concurrent d5ai-interrupted '
         'd5ai-exclusive d5ai-stale-arm d5ai-held-worker d5ai-consumer-partial d5ai-unfinished '
         'd5ai-native-mask0 d5ai-native-mask3a d5ai-native-mask3b').split()
CASES.extend('d5ai-retained d5ai-rebuilt-equal d5ai-rebuilt-different d5ai-unavailable'.split())
CASES.extend('d5ai-write-fault d5ai-flush-fault d5ai-receipt-fault d5ai-worker-exit d5ai-process-exit d5ai-stop-during'.split())
CASES.extend('d5ai-file-arm d5ai-foreign-arm'.split())
CASES.extend('d5ai-last-false d5ai-missing-preunlock'.split())
CASES.append('d5ai-stop-admission')
CASES.extend('d5ai-context-late-zero d5ai-context-mid-gap d5ai-context-owner-change d5ai-context-clean'.split())
CASES.extend(('d5ai-life-'+name) for name in 'external-holder external-collection final partial aba mutation empty-null empty-spare stalled overflow'.split())
CASES.extend('d5ai-life-stop d5ai-life-stop-admitted d5ai-life-write-fault d5ai-life-flush-fault d5ai-life-ack-fault'.split())
CASES.extend('d5ai-life-counter-token d5ai-life-counter-generation d5ai-life-counter-loss'.split())
CASES.remove('d5ai-overflow')
CASES.insert(0, 'd5ai-overflow')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def replace(text, before, after, count=1):
    if text.count(before) != count:
        raise ValueError('Owned source adaptation mismatch: ' + before[:100])
    return text.replace(before, after)


def retail_guard_rows(build):
    """Return exact new-site plan pins from the retained generated PE receipts."""
    text = (Path(build) / 'identity.generated.h').read_text(encoding='utf8')

    def digest(name):
        match = re.search(r'inline constexpr char ' + re.escape(name) + r'\[\]="([a-f0-9]{64})";', text)
        if not match:
            raise ValueError('Missing generated PE guard: ' + name)
        return match[1]

    geometry = [(0x21e09ed, (b'\xe8' + struct.pack('<i', 0x22cc350-(0x21e09ed+5))).hex()), (0x21e0aa5, '488b7c2470'), (0x21e0a7e, '488d4b04baffffffff')]
    return dict(geometry_schema='sor-d5ai-raw/2', geometry_header_bytes=456,
                geometry_sites=[dict(rva=rva, bytes=len(bytes.fromhex(raw)),
                                     preimage_sha256=hashlib.sha256(bytes.fromhex(raw)).hexdigest()) for rva, raw in geometry],
                context_schema='sor-d5ai-context/1',
                context_sites=[dict(rva=rva, bytes=5, reason=reason, guard_sha256=digest('context_' + name + '_hash'))
                               for rva, reason, name in ((0x789ce0, 5, 'owner'), (0x788e70, 6, 'reset'))],
                lifetime_schema='sor-d5ai-lifetime/1', lifetime_header_bytes=96, lifetime_event_bytes=96, lifetime_capacity=32768,
                lifetime_sites=[dict(rva=rva, bytes=5, kind=kind, allocation_adjustment=adjustment,
                                     guard_sha256=digest('lifetime_' + name + '_hash'))
                                for rva, kind, adjustment, name in ((0x7aab10, 'HOLDER_RESOURCE_MAP', 16, 'holder'),
                                  (0x7ac260, 'COLLECTION_GEOMETRY', 8, 'collection'), (0x7ac2f0, 'COLLECTION_MUTATION', 8, 'mutation'))])


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use installed Python -E -B')
    label = sys.argv[1]
    if not re.fullmatch('[a-z0-9-]+', label):
        raise ValueError('Fresh bounded label required')
    task = ROOT / '.local-work/d5ai-recorder'
    task.mkdir(exist_ok=True)
    tree = task / ('candidate-' + label)
    tree.mkdir(exist_ok=False)
    candidate = tree / 'runtime/construction-winner'
    candidate.mkdir(parents=True)
    inputs = {}
    outputs = {}
    native_path=ROOT/'.local-work/d5ah/geometry01/control.json'
    native=json.loads(native_path.read_bytes())
    ledger=ROOT/'docs/experiments/resource-retained-population/d5ah-sources.csv'
    import csv
    expected=next(row['sha256'] for row in csv.DictReader(ledger.open(encoding='utf8')) if Path(row['path'])==native_path)
    if sha(native_path)!=expected:raise ValueError('Native geometry oracle identity mismatch')
    inputs[str(native_path)]=expected
    inputs[str(ledger)]=sha(ledger)
    generated=[];sizes=[]
    for i,run in enumerate(native['runs']):
        packet=bytearray(struct.pack('<I',len(run['population'])))
        for resource in run['population']:
            packet.extend(struct.pack('<II',int(resource['resource'],16),len(resource['regions'])))
            for region in resource['regions']:
                packet.extend(bytes.fromhex(region['header']))
                packet.extend(struct.pack('<I',region['count']))
                packet.extend(bytes.fromhex(region['points']))
        generated.append('inline constexpr unsigned char d5ai_population_'+str(i)+'[]={'+','.join(str(b) for b in packet)+'};\n')
        sizes.append(len(packet))
    generated.append('inline constexpr const unsigned char* d5ai_population_data[]={d5ai_population_0,d5ai_population_1,d5ai_population_2};\n')
    generated.append('inline constexpr size_t d5ai_population_size[]={'+','.join(map(str,sizes))+'};\n')
    (candidate/'d5ai_population.generated.h').write_text(''.join(generated),encoding='utf8',newline='\n')
    outputs[str(candidate/'d5ai_population.generated.h')]=sha(candidate/'d5ai_population.generated.h')
    for p in BASE.iterdir():
        if not p.is_file():
            continue
        inputs[str(p)] = sha(p)
        text = p.read_text(encoding='utf8')
        if p.name == 'transport.cpp':
            text = replace(text, '#include "observer.h"', '#include "d5ai_geometry.h"\n#include "d5ai_context.h"')
            text = replace(text, 'return true;}\nbool publish(', 'if(!geometry::guards()){output_fault="geometry_guard";return false;}if(!context::guards()){output_fault="context_guard";return false;}return true;}\nbool publish(')
            text = replace(text, 'bool ok=drain()&&guards()&&disk();', 'bool ok=drain()&&geometry::drain_sidecar()&&guards()&&disk();')
            text = replace(text, 'ok=disk()&&guards()&&(fixture_pause.load()||drain());',
                           'ok=disk()&&guards()&&geometry::poll_request()&&geometry::drain_sidecar()&&(fixture_pause.load()||drain());')
            text = replace(text, '!valid||!drain()||!enabled', '!valid||!lifetime::drain()||!drain()||!enabled')
            text = replace(text, 'while(active.load())Sleep(10);', 'while(active.load()||geometry::active_capture.load())Sleep(10);')
            text = replace(text, 'if(!drain())broken=true;}', 'if(!drain()||!geometry::drain_sidecar())broken=true;}')
            text = replace(text, 'if(!drain()||!geometry::drain_sidecar())broken=true;}', 'geometry::finish_uncompleted();if(!drain()||!geometry::drain_sidecar())broken=true;}')
            text = replace(text, '+metrics()+', '+metrics()+geometry::metrics()+lifetime::metrics()+', count=text.count('+metrics()+'))
            text = replace(text, 'geometry::drain_sidecar()', '(lifetime::drain()&&geometry::drain_sidecar())', count=text.count('geometry::drain_sidecar()'))
            text = replace(text, 'bool guards(){Measure measure{Guard};', 'bool guards(){Measure measure{Guard};if(!lifetime::guards()){output_fault="lifetime_guard";return false;}')
            text = replace(text, 'CloseHandle(raw);CloseHandle(ack);', 'lifetime::close();CloseHandle(raw);CloseHandle(ack);')
            text += '\n#include "d5ai_lifetime_transport.inc"\n#include "d5ai_transport.inc"\n'
        elif p.name == 'plugin.cpp':
            text = replace(text, '0x00040000,"SOR Construction Winner"', '0x00070000,"SOR Geometry Lifecycle Candidate"')
            text = replace(text, '#include "transport.h"', '#include "transport.h"\n#include "d5ai_geometry.h"\n#include "d5ai_context.h"')
            text = replace(text, 'if(!configure(locations,lengths,hashes))',
                           'if(!geometry::configure_acquire((void*)(base+0x21e09ed),geometry_call_hash,geometry_target_hash)||!geometry::configure_completion((void*)(base+0x21e0aa5),geometry_complete_hash)||!geometry::configure_preunlock((void*)(base+0x21e0a7e),geometry_preunlock_hash)||!context::configure((void*)(base+0x789ce0),(void*)(base+0x788e70),context_owner_hash,context_reset_hash)||!lifetime::configure((void*)(base+0x7aab10),(void*)(base+0x7ac260),(void*)(base+0x7ac2f0),lifetime_holder_hash,lifetime_collection_hash,lifetime_mutation_hash)||!configure(locations,lengths,hashes))')
            text = replace(text, 'Event ready{};ready.kind=Ready;',
                           'if(!install(geometry::edits,3,dirty)||!install(context::edits,2,dirty)||!install(lifetime::edits,3,dirty)){enabled=false;return dirty;}enabled=false;if(!lifetime::begin()){broken=true;return dirty;}enabled=true;\n  Event ready{};ready.kind=Ready;')
            text = replace(text, 'auto id=identity+"}\\n";identity_hash=sor::sha_bytes(id.data(),id.size());if(!sor::write_new(session/L"identity.json",id))return false;', '')
            text = replace(text, 'raw=CreateFileW', 'identity+=geometry::identity_metadata()+context::metadata()+lifetime::metadata();auto id=identity+"}\\n";identity_hash=sor::sha_bytes(id.data(),id.size());if(!sor::write_new(session/L"identity.json",id))return false;\n  raw=CreateFileW')
        elif p.name == 'fixture.cpp':
            text = replace(text, 'U host_allocation=++host_allocations,geometry{};', 'U host_allocation=++host_allocations,geometry{},d5ai_output=0x2222;')
            text = replace(text, '&&output==0x2222', '&&output==m.d5ai_output')
            text = replace(text, '0x5e0de,0x1111,0x2222);', '0x5e0de,0x1111,m.d5ai_output);')
            text = replace(text, 'U result=*model->shared_hit?2:8;', 'U capacity{};memcpy(&capacity,(void*)(a+0x18),8);U result=*model->shared_hit?(capacity>2?2:0):capacity;if(model->d5ai_output!=0x2222){result=capacity;U data{};memcpy(&data,(void*)(a+0x10),8);for(U i=0;i<capacity;++i){uint32_t used{};U key{};memcpy(&used,(void*)(data+i*24+16),4);memcpy(&key,(void*)(data+i*24),8);if(used!=UINT32_MAX&&key==model->source){result=i;break;}}}')
            text = replace(text, 'if(result==8){', 'if(result==*(U*)(proc+0x28)){')
            text = replace(text, 'invoke_descriptor(U(m.descriptor)-(m.temporary_descriptor?0x1c0:0xc8),', 'invoke_descriptor((m.d5ai_output==0x2222?U(m.descriptor)-(m.temporary_descriptor?0x1c0:0xc8):geometry::fixture_manager),')
            text = replace(text, ':geometry::fixture_manager),0x20000,U(m.descriptor),U(m.query));', ':geometry::fixture_manager),0x20000,(m.d5ai_output==0x2222?U(m.descriptor):geometry::fixture_manager+0xc8),U(m.query));')
            text = replace(text, 'extern "C" void native_generate(', 'namespace {void d5ai_fixture_publish(Model&);}\nextern "C" void native_generate(')
            text = replace(text, 'oracle("generator-output",m,m.geometry,m.generation_outcome);', 'if(m.d5ai_output!=0x2222)d5ai_fixture_publish(m);\n oracle("generator-output",m,m.geometry,m.generation_outcome);')
            text = replace(text, '#include "transport.h"', '#include "transport.h"\n#include "d5ai_geometry.h"\n#include "d5ai_context.h"')
            text = replace(text, 'extern "C" __declspec(dllexport) int D5X_Qualify',
                           'namespace {void d5ai_setup();void d5ai_fixture(Model&,const std::wstring&,HANDLE);}\nextern "C" __declspec(dllexport) int D5X_Qualify')
            text = replace(text, 'check(install(edits,18,dirty));enabled=true;',
                           'check(install(edits,18,dirty));if(s.starts_with(L"d5ai-")){check(install(geometry::edits,3,dirty));check(install(context::edits,2,dirty));check(install(lifetime::edits,3,dirty));check(lifetime::begin());}enabled=true;')
            text = replace(text, 'check(configure(locations,lengths,hashes));', 'check(configure(locations,lengths,hashes));if(s.starts_with(L"d5ai-"))d5ai_setup();')
            text = replace(text, 'if(s==L"later-bypass"){', 'if(s.starts_with(L"d5ai-"))d5ai_fixture(m,s,thread);\n  if(s==L"later-bypass"){')
            text = replace(text, 'auto id=identity+"}\\n";', 'identity+=geometry::identity_metadata()+context::metadata()+lifetime::metadata();\n  auto id=identity+"}\\n";')
            text += '\n#include "d5ai_fixture.inc"\n'
        elif p.name == 'observer.h':
            text = replace(text, 'reserve_original{},fences[5]{};', 'reserve_original{},fences[7]{};')
        target = candidate / p.name
        target.write_text(text, encoding='utf8', newline='\n')
        outputs[str(target)] = sha(target)
    # Relative includes resolve to explicitly copied, hash-bound owned support.
    for name in ('core.h', 'win_support.h', 'third_party/sfse/PluginAPI.h', 'third_party/sfse/LICENSE.txt'):
        source = ROOT / 'runtime/exp0002' / name
        target = tree / 'runtime/exp0002' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        inputs[str(source)] = sha(source)
        outputs[str(target)] = sha(target)
    builder = (BASE / 'build.py').read_text(encoding='utf8')
    builder = replace(builder, 'SRC = Path(__file__).parent', 'SRC = Path(' + repr(str(candidate)) + ')')
    builder = replace(builder, "ROOT / '.local-work/d5x' / label", "ROOT / '.local-work/d5ai-recorder' / label")
    builder = replace(builder, 'selected_cases = sys.argv[2:] or CASES',
                      'CASES[:0]=' + repr(CASES) + '\n    selected_cases = sys.argv[2:] or CASES')
    builder = replace(builder, "(out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')",
                      "geometry_call=pe.pe_read(image,0x21e09ed,32)\n    assert geometry_call[0]==0xe8\n    geometry_target=0x21e09ed+5+struct.unpack_from('<i',geometry_call,1)[0]\n    assert geometry_target==0x22cc350\n    header+='inline constexpr char geometry_call_hash[]=\\\"'+hashlib.sha256(geometry_call).hexdigest()+'\\\";\\n'\n    header+='inline constexpr char geometry_target_hash[]=\\\"'+hashlib.sha256(pe.pe_read(image,geometry_target,32)).hexdigest()+'\\\";\\n'\n    header+='inline constexpr char geometry_complete_hash[]=\\\"'+hashlib.sha256(pe.pe_read(image,0x21e0aa5,32)).hexdigest()+'\\\";\\n'\n    assert pe.pe_read(image,0x21e0aa5,5)==bytes.fromhex('488b7c2470')\n    (out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')")
    builder = replace(builder, "(out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')",
                      "header+='inline constexpr char geometry_preunlock_hash[]=\\\"'+hashlib.sha256(pe.pe_read(image,0x21e0a7e,32)).hexdigest()+'\\\";\\n'\n    assert pe.pe_read(image,0x21e0a7e,9)==bytes.fromhex('488d4b04baffffffff')\n    (out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')")
    builder = replace(builder, 'f\'ml64 /nologo /c /Fobridges.obj "{SRC / "bridges.asm"}"\',',
                      'f\'ml64 /nologo /c /Fobridges.obj "{SRC / "bridges.asm"}"\',\n                f\'ml64 /nologo /c /Fod5ai-bridge.obj "{SRC / "d5ai_bridge.asm"}"\',\n                f\'ml64 /nologo /c /Fod5ai-context-fixture.obj "{SRC / "d5ai_context_fixture.asm"}"\',')
    builder = replace(builder, "(out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')",
                      "header+='inline constexpr char context_owner_hash[]=\\\"'+hashlib.sha256(pe.pe_read(image,0x789ce0,32)).hexdigest()+'\\\";\\n'\n    header+='inline constexpr char context_reset_hash[]=\\\"'+hashlib.sha256(pe.pe_read(image,0x788e70,32)).hexdigest()+'\\\";\\n'\n    assert pe.pe_read(image,0x789ce0,5)==bytes.fromhex('48895c2408')\n    assert pe.pe_read(image,0x788e70,5)==bytes.fromhex('4053555657')\n    (out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')")
    builder = replace(builder, "(out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')",
                      "for name,rva,offset in [('holder',0x7aab10,8),('collection',0x7ac260,8),('mutation',0x7ac2f0,16)]:\n        assert pe.pe_read(image,rva,5)==bytes([0x48,0x89,0x5c,0x24,offset])\n        header+='inline constexpr char lifetime_'+name+'_hash[]=\\\"'+hashlib.sha256(pe.pe_read(image,rva,32)).hexdigest()+'\\\";\\n'\n    (out / 'identity.generated.h').write_text(header, encoding='utf8', newline='\\n')")
    builder = replace(builder, 'bridges.obj fixture-asm.obj /LD', 'bridges.obj fixture-asm.obj d5ai-bridge.obj d5ai-context-fixture.obj /LD')
    builder = replace(builder, "'p3-store-access-fault': 0xc0000005", "'p3-store-access-fault': 0xc0000005, 'd5ai-process-exit':74")
    code_path = tree / 'derived-build.py'
    code_path.write_text(builder, encoding='utf8', newline='\n')
    receipt = dict(schema='sor-d5ai-source-derivation/1', inputs=inputs, derived=outputs,
                   derivation_sha256=sha(__file__), derived_builder_sha256=sha(code_path),
                   scope='Owned source-informed candidate; unchanged schema-4 record layout; independent raw geometry sidecar; offline only')
    (tree / 'derivation.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    namespace = {'__file__': str(BASE / 'build.py'), '__name__': 'd5ai_derived_build'}
    exec(compile(builder, str(code_path), 'exec'), namespace)
    result = namespace['main']()
    if not all(sha(p) == digest for p, digest in inputs.items()):
        raise ValueError('Source drift during build')
    return result


if __name__ == '__main__':
    raise SystemExit(main())
