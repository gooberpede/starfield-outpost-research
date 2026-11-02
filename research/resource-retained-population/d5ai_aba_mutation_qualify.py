# SPDX-License-Identifier: GPL-3.0-or-later
"""Capture old collection ending then mutation at its reused numeric address.

Reads frozen16 source/object inputs and approved installed compiler. Copies them
into a fresh ignored tree, adds one fixture-only mutation call after the existing
ABA restoration, compiles only fixture.obj and relinks retained producer/plugin/
ASM objects. Executes the unchanged owned host once. Production headers and
candidate16 are never modified. This is a distinct test DLL, not candidate16.
Risks: source mismatch, compile/ABI/host/guard or witness failure. STOP on any;
preserve all artifacts. Both drives retain the 40 GB caller-available floor plus
reserve. No game, save, deployment, foreign process intervention or network.
"""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
from common import fresh, guard, sha
from d5ai_read_geometry import read_session
from d5ai_read_lifetime import read_prefix, qualify_snapshot
from d5ai_operations import worker_json

VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def main():
    build, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    free = guard({'D:/': 64 * 1024 * 1024})
    out.mkdir(exist_ok=False)
    fresh(out / 'contract.json', dict(schema='sor-d5ai-combined-ABA-contract/1',
        question='Can the unchanged observer record a baseline collection ending followed by same-address mutation and a completed absent return?',
        allowed='Read frozen16 sources/objects; add only a fixture stimulus; compile fixture.obj; relink; run owned host once; authenticate files',
        outputs=str(out), risks=['Source/compile/ABI/guard failure', 'Missing or nonstrict witness order', 'Disk exhaustion'],
        stop='Any pin, guard, native exit, frame, loss or timing/order failure', cleanup='Keep original and derived trees, binaries and receipts; no deletion',
        initial_free=free, candidate16_modified=False, no_retail_authority=True))
    candidate = next((build / 'sources').rglob('d5ai_fixture.inc')).parent
    copied = out / 'runtime/construction-winner'
    copied.mkdir(parents=True)
    pins = {str(p): sha(p) for p in [Path(__file__), VC, *[p for p in candidate.iterdir() if p.is_file()]]}
    for source in candidate.iterdir():
        if source.is_file():
            (copied / source.name).write_bytes(source.read_bytes())
    support = out / 'runtime/exp0002'
    for name in ('win_support.h', 'core.h', 'third_party/sfse/PluginAPI.h', 'third_party/sfse/LICENSE.txt'):
        source = build / 'sources/runtime/exp0002' / name
        target = support / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        pins[str(source)] = sha(source)
    before = (copied / 'd5ai_fixture.inc').read_text(encoding='utf8')
    line = '   put(n.resources,0,uint32_t(0x57d4));put(n.resources,8,U(n.collection));put(n.resources,16,uint32_t(0));put(n.collection,0,uint32_t(1));put(n.collection,8,uint32_t(1));put(n.collection,12,uint32_t(1));put(n.collection,16,U(n.region));\n'
    if before.count(line) != 1:
        raise ValueError('Exact owned ABA fixture replacement required')
    after = before.replace(line, line + '   // Combined offline witness: mutate the restored graph at the same address.\n   check(d5ai_fixture_life_mutation(U(n.collection)+8,1,2,3)==0xc012);\n')
    (copied / 'd5ai_fixture.inc').write_text(after, encoding='utf8', newline='\n')
    (out / 'fixture-before.inc').write_text(before, encoding='utf8', newline='\n')
    for name in ('identity.generated.h', 'emitters.generated.h', 'emitter-input.bin', 'sor-d5x-fixture.exe'):
        source = build / name
        (out / name).write_bytes(source.read_bytes())
        pins[str(source)] = sha(source)
    objects = ('transport.obj', 'plugin.obj', 'bridges.obj', 'fixture-asm.obj', 'd5ai-bridge.obj', 'd5ai-context-fixture.obj')
    for name in objects:
        pins[str(build / name)] = sha(build / name)
    changed = [p.name for p in copied.iterdir() if p.is_file() and sha(p) != sha(candidate / p.name)]
    if changed != ['d5ai_fixture.inc']:
        raise ValueError('Unexpected source delta')
    fresh(out / 'derivation.json', dict(original_include_sha256=sha(candidate / 'd5ai_fixture.inc'),
        changed_include_sha256=sha(copied / 'd5ai_fixture.inc'), changed_files=changed,
        change='One actual typed mutation call after existing graph restoration; no production header or observer source change',
        retained_objects={name: pins[str(build / name)] for name in objects}))
    script = ('@echo off\ncall "' + str(VC) + '"\nif errorlevel 1 exit /b 1\n'
              'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD /DSOR_QUEUE_CAPACITY=32768 /I"' + str(out) + '" /c "' + str(copied / 'fixture.cpp') + '" /Fofixture.obj\n'
              'if errorlevel 1 exit /b 1\nlink /DLL /OUT:SorConstructionWinner.dll fixture.obj ' + ' '.join('"' + str(build / name) + '"' for name in objects) + ' /Brepro /INCREMENTAL:NO /MAP:combined.map bcrypt.lib\n')
    (out / 'build.cmd').write_text(script, encoding='utf8', newline='\r\n')
    compiled = subprocess.run(['cmd', '/d', '/c', str(out / 'build.cmd')], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(compiled.stdout + compiled.stderr)
    result = dict(schema='sor-d5ai-combined-ABA-native/1', inputs=pins, compilation=compiled.returncode,
                  candidate16_sha256=sha(build / 'SorConstructionWinner.dll'), actual_artifact='Fixture-only derivative DLL; retained16 transport/plugin/ASM, unchanged production headers with inline/COMDAT source-matched code')
    if compiled.returncode == 0:
        dll = out / 'SorConstructionWinner.dll'
        result['test_dll_sha256'] = sha(dll)
        session = out / 'session'
        run = subprocess.run([str(out / 'sor-d5x-fixture.exe'), str(dll), str(session), 'd5ai-life-aba'], cwd=out, capture_output=True)
        (out / 'native.stdout').write_bytes(run.stdout)
        (out / 'native.stderr').write_bytes(run.stderr)
        result['native_exit'] = run.returncode
        if run.returncode == 0:
            try:
                raw = read_session(session)
                terminal = worker_json(session / 'terminal.json')
                journal = read_prefix(session, terminal)
                assert not raw['errors'] and len(raw['snapshots']) == 2 and not terminal['failed']
                before, returned = raw['snapshots']
                assert before['complete_representation'] and returned['complete_representation']
                assert before['holders'] and not returned['holders']
                qualify_snapshot(before, journal)
                qualify_snapshot(returned, journal)
                collection = before['holders'][0]['resources'][0]['collection_pointer']
                ending = next(e for e in journal['events'] if e['kind'] == 'COLLECTION_GEOMETRY' and e['phase'] == 'END' and e['allocation'] == collection)
                mutation = next(e for e in journal['events'] if e['kind'] == 'COLLECTION_MUTATION' and e['phase'] == 'BEGIN' and e['allocation'] == collection)
                assert ending['status'] == mutation['status'] == 0 and ending['sequence'] < mutation['sequence'] and ending['ticks'] < mutation['ticks']
                assert len(journal['events']) == 6 and not journal['open_intervals']
                fresh(out / 'geometry.json', raw)
                fresh(out / 'journal.json', journal)
                result.update(baseline_collection=collection, old_ending=ending, new_same_address_mutation=mutation,
                              strict_sequence_and_QPC_order=True, baseline_and_absent_return_qualified=True,
                              event_records=6, native_capture_scope='Owned model baseline/ABA/mutation; actual unchanged observer/transport, not retail occurrence')
            except Exception as error:
                result['verification_error'] = repr(error)
        result['link_map_sha256'] = sha(out / 'combined.map')
    result['inputs_unchanged'] = all(sha(path) == digest for path, digest in pins.items())
    result['status'] = 'PASS' if result.get('strict_sequence_and_QPC_order') and result['inputs_unchanged'] else 'FAIL'
    result['final_free'] = guard()
    fresh(out / 'qualification.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'inputs'}))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    main()
