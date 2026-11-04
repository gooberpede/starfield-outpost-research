# SPDX-License-Identifier: GPL-3.0-or-later
# D5AN source-informed owned adaptation of d5am_guard_package.py under SOR-P-0002.
"""Reproduce a frozen D5AM candidate and create a fresh local review archive.

Reads a completed D5AM build, its frozen derived source and explicit review
files. Runs the retained build command with the same source/include paths in a
fresh output directory, pins the selected installed MSVC/MASM executables and
byte-compares the resulting DLL. Writes only fresh D5AM local build, manifest
and ZIP outputs. No deployment, Vortex operation, game, save/configuration write,
network, analysis project operation, Git staging or publication occurs.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile
from d5am_lock_qualify import ROOT,VC,guard,sha
from d5an_pe import inspect as inspect_pe

RELEASE_CASES={'d5an-contention','d5an-overflow-core','d5an-overflow-own','d5an-overflow-causal',
    'd5an-before-owner','d5an-teardown','d5an-causal-core','d5an-asm-core','d5an-asm-bridge',
    'd5an-causal-asm-core','d5an-causal-asm-bridge','d5an-serial-publish','d5an-serial-retire',
    'd5an-provenance-pending','d5an-scheduler-loss','d5an-scheduler-exhaustion',
    'd5an-teardown-scheduler','d5an-teardown-core','d5an-written-scheduler','d5an-token-scheduler',
    'd5an-stop-teardown','d5an-serial-native','d5an-timing'}

def check(condition,message):
    if not condition:
        raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build',type=Path);parser.add_argument('label')
    parser.add_argument('--review-file',type=Path,action='append',default=[])
    args=parser.parse_args();build=args.build.resolve()
    check(build.is_relative_to(ROOT/'.local-work/d5an'),'D5AM frozen build required')
    check(re.fullmatch('[a-z0-9-]+',args.label) is not None,'Bounded fresh label required')
    initial=guard();out=ROOT/'.local-work/d5an'/('package-'+args.label);out.mkdir(exist_ok=False)
    receipt=json.loads((build/'build.json').read_bytes())
    check(receipt.get('schema')=='sor-d5an-candidate-build/1' and receipt.get('version')=='0.9.2-D5AN','Candidate build identity')
    check(receipt.get('compilation')==0 and receipt.get('source_unchanged') is True,'Completed unchanged-source build required')
    check(sha(build/'build.cmd')==receipt.get('build_command_sha256'),'Frozen build-command identity mismatch')
    original_path=ROOT/'.local-work/d5ai-recorder/build16/build.json'
    check(sha(original_path)=='15d10475806aeb593ac7236a48ea1b71f8e3614bf8cdd7e1ded830b0fcdbf457','Original regression contract identity')
    original=json.loads(original_path.read_bytes())
    required={r['case'] for r in original['cases']}|{'d5am-native-lock','d5am-native-stop','d5am-native-guard','d5am-causal-counter','d5am-causal-loss','d5am-causal-owners','d5am-native-operand','d5am-guard-alias','d5am-guard-overlap','d5am-guard-outside','d5am-guard-relay','d5am-guard-preimage','d5am-guard-patch'}
    required |= RELEASE_CASES
    cases=receipt.get('cases',[]);seen={r['case'] for r in cases}
    check(len(seen)==len(cases) and required==seen,'Exact complete mandatory native regression inventory required')
    expected={row['case']:row['expected'] for row in original['cases']}
    expected.update({name:0 for name in required-set(expected)})
    check(all(row.get('expected')==expected[row['case']] and row.get('exit')==expected[row['case']] for row in cases),'Native exits differ from the authenticated original/new regression contract')
    check(all(r.get('pass_exit') is True and r.get('exit')==r.get('expected') for r in cases),'A mandatory case failed')
    pins={str(build/'build.json'):sha(build/'build.json'),str(build/'build.cmd'):sha(build/'build.cmd'),str(Path(__file__)):sha(__file__),str(Path(__file__).with_name('d5an_pe.py')):sha(Path(__file__).with_name('d5an_pe.py'))}
    for path,digest in receipt['inputs'].items():
        check(sha(path)==digest,'Current input differs from frozen candidate: '+path)
        pins[path]=digest
    tree=build/'candidate'
    for path,digest in receipt['derived'].items():
        full=tree/path;check(sha(full)==digest,'Frozen derived-source drift: '+path);pins[str(full)]=digest
    for name in ('identity.generated.h','emitters.generated.h','d5am_native.generated.h','emitter-input.bin'):
        check(sha(build/name)==receipt.get('generated',{}).get(name),'Generated native input mismatch: '+name)
        pins[str(build/name)]=sha(build/name)
    dll=build/'SorConstructionWinner.dll'
    check(sha(dll)==receipt['dll_sha256'],'Candidate DLL mismatch')
    pe=inspect_pe(dll)
    check(pe['plugin_version']==0x00090200 and pe['sfse_version_schema']==1,'Actual DLL version metadata mismatch')
    tool_probe=out/'tool-probe.cmd'
    tool_probe.write_text('@echo off\ncall "'+str(VC)+'"\nif errorlevel 1 exit /b 1\nwhere cl\nwhere link\nwhere ml64\n',encoding='utf8',newline='\r\n')
    probe=subprocess.run(['cmd','/d','/c',str(tool_probe)],cwd=out,capture_output=True)
    (out/'tool-probe.log').write_bytes(probe.stdout+probe.stderr);check(probe.returncode==0,'Tool selection probe failed')
    tools={}
    for line in probe.stdout.decode('utf8',errors='replace').splitlines():
        path=Path(line.strip())
        if path.name.lower() in ('cl.exe','link.exe','ml64.exe') and path.is_file():
            tools.setdefault(path.name.lower(),dict(path=str(path),sha256=sha(path)))
    check(set(tools)=={'cl.exe','link.exe','ml64.exe'},'Exact selected compiler/assembler/linker paths unavailable')
    rebuild=out/'rebuild';rebuild.mkdir()
    # The retained command has absolute frozen source/include paths and relative
    # output paths. Changing only cwd preserves source-location bytes while
    # writing every rebuilt object, library, executable and DLL into this child.
    command=(build/'build.cmd').read_bytes()
    (rebuild/'build.cmd').write_bytes(command)
    run=subprocess.run(['cmd','/d','/c',str(rebuild/'build.cmd')],cwd=rebuild,capture_output=True)
    (out/'rebuild.log').write_bytes(run.stdout+run.stderr)
    reproduced=dict(compilation=run.returncode,original_sha256=sha(dll))
    if run.returncode==0:
        reproduced['rebuilt_sha256']=sha(rebuild/'SorConstructionWinner.dll')
        reproduced['byte_equal']=dll.read_bytes()==(rebuild/'SorConstructionWinner.dll').read_bytes()
    check(all(sha(p)==h for p,h in pins.items()),'Input changed during reproduction')
    summary=dict(schema='sor-d5an-candidate-package/1',authority='OFFLINE_ONLY_NOT_AUTHORIZED_FOR_DEPLOYMENT',
                 version='0.9.2-D5AN',source_build=str(build),source_build_sha256=sha(build/'build.json'),
                 inputs=pins,selected_tools=tools,reproduction=reproduced,initial_free=initial,final_free=guard())
    if run.returncode or reproduced.get('byte_equal') is not True:
        (out/'package.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n')
        raise RuntimeError('Frozen-source reproduction failed; preserved receipt and outputs control')
    review={}
    for given in args.review_file:
        path=given.resolve()
        check(path.is_file() and path.suffix in ('.py','.md','.json'),'Explicit review text file required')
        check(any(path.is_relative_to(ROOT/folder) for folder in ('runtime','research','docs')),'Review text outside authored repository scope')
        relative=path.relative_to(ROOT).as_posix();review[relative]=dict(sha256=sha(path),bytes=path.stat().st_size)
    summary['review_files']=review
    summary['dll_sha256']=sha(dll);summary['native_cases']=len(cases)
    summary['pe_metadata']=pe
    summary['native_source_set']=dict(inputs=receipt['inputs'],derived=receipt['derived'],generated=receipt['generated'],build_command_sha256=receipt['build_command_sha256'])
    summary['native_source_set_sha256']=hashlib.sha256(json.dumps(summary['native_source_set'],sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()
    manifest=(json.dumps(summary,indent=2)+'\n').encode('utf8')
    archive=out/('SorConstructionWinner-0.9.2-D5AN-counter-'+args.label+'-NOT-AUTHORIZED.zip')
    payload={'Data/SFSE/Plugins/SorConstructionWinner.dll':dll.read_bytes(),
             'COPYING':(ROOT/'LICENSE').read_bytes(),
             'SFSE-PluginAPI-MIT.txt':(ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt').read_bytes(),
             'candidate-lock.json':manifest,
             'README.txt':b'Offline review candidate. Deployment and live observation require separate authorization. Raw and proprietary evidence remain local; this archive has no publication clearance.\n'}
    for relative in review:
        payload['review/'+relative]=(ROOT/relative).read_bytes()
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as zipped:
        for name,data in sorted(payload.items()):
            entry=zipfile.ZipInfo(name,(1980,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o644<<16
            zipped.writestr(entry,data)
    with zipfile.ZipFile(archive) as zipped:
        check(len(zipped.namelist())==len(payload),'ZIP inventory mismatch')
        check(all(zipped.read(name)==data for name,data in payload.items()),'ZIP byte round-trip mismatch')
    check(all(sha(ROOT/p)==item['sha256'] for p,item in review.items()),'Review file changed during archive creation')
    check(all(sha(p)==h for p,h in pins.items()),'Input changed during archive creation')
    summary['archive']=str(archive);summary['archive_sha256']=sha(archive)
    summary['archive_members']={name:dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest()) for name,data in payload.items()}
    (out/'package.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(archive=str(archive),archive_sha256=sha(archive),dll_sha256=sha(dll),reproduced=True,native_cases=len(cases))))

if __name__=='__main__':
    main()
