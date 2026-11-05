# SPDX-License-Identifier: GPL-3.0-or-later
"""Build the D5AR candidate only in a fresh ignored offline directory.

Reads authored sources, the specifically approved unchanged SFSE PluginAPI.h/MIT
notice, the pinned installed game/SFSE and installed Microsoft toolchain/SDK.
Writes a source lock, exact source snapshot, generated original-byte guards,
compiler logs, DLL and NOT-AUTHORIZED local ZIP. No game launch, deployment,
save/configuration/analysis-project/Git/network mutation occurs. A clean build
alone does not qualify the candidate for retail. Use pinned Python -E -B.
"""
import os
import sys
if sys.flags.optimize or not __debug__ or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Optimization forbidden; invoke pinned Python -E -B')

import hashlib
import json
from pathlib import Path
import struct
import subprocess
import zipfile
import shutil

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/resource-retained-population'))
from d5ar_native_inventory import disk_floor

SOURCE = Path(__file__).resolve().parent
GAME = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
GAME_HASH = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
SFSE_HASH = '28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    if len(sys.argv)!=2:
        raise ValueError("Exactly one fresh build label required")
    label = sys.argv[1]
    if not label or not label[0].isalnum() or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('Simple fresh build label required')
    output = ROOT / '.local-work/d5ar' / label
    if output.exists() or any(p.is_symlink() or p.is_junction() for p in (output, *output.parents)):
        raise ValueError('Fresh plain output required')
    before = disk_floor()
    if sha(GAME / 'Starfield.exe') != GAME_HASH or sha(GAME / 'sfse_1_16_244.dll') != SFSE_HASH:
        raise ValueError('Installed game/SFSE identity mismatch')
    if sha(ROOT / 'runtime/exp0002/third_party/sfse/PluginAPI.h') != '7b0bccaa54d7c65de4ee428b17c1fda9adb7b0bc8a880a432d0d848fff3ce4ab' or sha(ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt') != '7795510c3ee9970b5843639d79b7ab6d87d1a14a1e110e92fd0b09ff0e7628da':
        raise ValueError('Approved unchanged header/notice mismatch')
    sources = sorted(p for p in SOURCE.iterdir() if p.is_file())
    sources += [ROOT / 'runtime/exp0002/third_party/sfse/PluginAPI.h', ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt', ROOT / 'LICENSE',ROOT / 'research/resource-retained-population/d5ar_native_inventory.py']
    sources += [ROOT/'research/resource-retained-population'/name for name in ('d5ar_snapshot.py','d5ai_geometry.py','d5ad_baseline.py')]
    identities = {p.relative_to(ROOT).as_posix(): sha(p) for p in sources}
    lock = dict(schema='sor-d5ar-source-lock/1', files=identities)
    lock_bytes = json.dumps(lock, sort_keys=True, separators=(',', ':')).encode('ascii') + b'\n'
    lock_hash = hashlib.sha256(lock_bytes).hexdigest()
    output.mkdir(parents=True)
    (output / 'source-lock.json').write_bytes(lock_bytes)
    snapshot = output / 'sources'
    for path in sources:
        destination = snapshot / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != identities[path.relative_to(ROOT).as_posix()]:
            raise ValueError('Source changed during snapshot')
        destination.write_bytes(data)
    local_source = snapshot / SOURCE.relative_to(ROOT)
    host_commands = [f'call "{VC}"','if errorlevel 1 exit /b 1',
                     f'cl /nologo /std:c++20 /EHsc /W4 /WX /O2 /MD "{local_source / "plugin-fixture.cpp"}" /Fe:d5ar-plugin-fixture.exe /link /Brepro /INCREMENTAL:NO']
    (output / 'host-build.cmd').write_bytes(('@echo off\r\n'+'\r\nif errorlevel 1 exit /b 1\r\n'.join(host_commands)+'\r\n').encode('utf8'))
    host_result = subprocess.run(['cmd','/d','/c',str(output / 'host-build.cmd')],cwd=output,capture_output=True)
    (output / 'host-build.log').write_bytes(host_result.stdout+host_result.stderr)
    if host_result.returncode:
        raise RuntimeError('Pinned offline host build failed; retained host-build.log')
    image = (GAME / 'Starfield.exe').read_bytes()
    pe = struct.unpack_from('<I', image, 0x3c)[0]
    optional = struct.unpack_from('<H', image, pe + 20)[0]
    sections = [struct.unpack_from('<IIII', image, pe + 24 + optional + n * 40 + 8)
                for n in range(struct.unpack_from('<H', image, pe + 6)[0])]

    def native(rva, size):
        for _, start, length, offset in sections:
            if start <= rva and rva + size <= start + length:
                return image[offset + rva - start:offset + rva - start + size]
        raise ValueError('Native range missing')

    guards = [(rva, hashlib.sha256(native(rva, 32)).hexdigest()) for rva in
              (0x79d910, 0x1eaa950,0x21e07d0,0x21e0f50,0x21e0a46,0x1881660,0x789ce0,0x788e70,0x788bc0,0x21b2570,0xf3e0c2,0x384600,0xf3df70,0x982af8,0x982c32,0x365cdb0)]
    header = '#pragma once\nnamespace d5ar {\ninline constexpr unsigned game_version=(1u<<24)|(16u<<16)|(244u<<4);\n'
    for key, value in (('expected_game', GAME_HASH), ('expected_sfse', SFSE_HASH), ('source_lock_hash', lock_hash),
                       ('expected_fixture_host',sha(output / 'd5ar-plugin-fixture.exe'))):
        header += f'inline constexpr char {key}[]="{value}";\n'
    for name, rva, size in (('destroy_bytes',0x79d910,5),
                            ('area_bytes',0x21e07d0,7),('area_callback_bytes',0x21e0f50,7),('initializer_bytes',0x1881660,5),('installer_bytes',0x789ce0,5),('reset_bytes',0x788e70,5),('manager_destructor_bytes',0x788bc0,5),('operation_bytes',0x21b2570,5),('selection_release_bytes',0xf3e0c2,5),('source_clear_free_bytes',0x982af8,5),('source_retire_free_bytes',0x982c32,5)):
        header += f'inline constexpr uint8_t {name}[]={{' + ','.join(str(byte) for byte in native(rva,size)) + '};\n'
    header += 'struct SiteGuard {unsigned long long rva;const char* hash;};\ninline constexpr SiteGuard site_guards[]={\n'
    header += ''.join(f'{{{rva},"{digest}"}},\n' for rva, digest in guards) + '};\n}\n'
    (output / 'identity.generated.h').write_text(header, encoding='utf8', newline='\n')
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1', 'where cl', 'where link', 'where ml64',
                f'ml64 /nologo /c /Fobridges.obj "{local_source / "bridges.asm"}"',
                f'cl /Bv /nologo /std:c++20 /EHsc /W4 /WX /O2 /MD /I"{output}" "{local_source / "plugin.cpp"}" "{local_source / "writer.cpp"}" bridges.obj /LD /Fe:SorOutpostGeometrySnapshot.dll /link /Brepro /INCREMENTAL:NO bcrypt.lib',
                f'ml64 /nologo /c /Fobridge-probe-asm.obj "{local_source / "bridge-fixture.asm"}"',
                f'cl /nologo /std:c++20 /EHsc /W4 /WX /O2 /MD "{local_source / "bridge-fixture.cpp"}" bridges.obj bridge-probe-asm.obj /Fe:d5ar-bridge-fixture.exe /link /Brepro /INCREMENTAL:NO',
                'dumpbin /HEADERS SorOutpostGeometrySnapshot.dll', 'dumpbin /DEPENDENTS SorOutpostGeometrySnapshot.dll']
    script = '@echo off\r\n' + '\r\nif errorlevel 1 exit /b 1\r\n'.join(commands) + '\r\n'
    (output / 'build.cmd').write_bytes(script.encode('utf8'))
    result = subprocess.run(['cmd', '/d', '/c', str(output / 'build.cmd')], cwd=output, capture_output=True)
    (output / 'build.log').write_bytes(result.stdout + result.stderr)
    receipt = dict(schema='sor-d5ar-build/1', exit=result.returncode, source_lock_sha256=lock_hash,
                   source_preserved=all(sha(ROOT / path) == digest for path, digest in identities.items()),
                   guards=guards, interpreter_sha256=sha(sys.executable), vcvars_sha256=sha(VC),
                   free_before=before, free_after=disk_floor(), status='BUILD_ONLY_UNQUALIFIED_NOT_AUTHORIZED')
    if result.returncode:
        (output / 'build.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
        raise RuntimeError('Clean build failed; inspect retained build.log')
    dll = output / 'SorOutpostGeometrySnapshot.dll'
    receipt['dll_sha256'] = sha(dll)
    fixture = subprocess.run([str(output / 'd5ar-bridge-fixture.exe')], cwd=output, capture_output=True, timeout=20)
    (output / 'bridge-fixture.stdout').write_bytes(fixture.stdout)
    (output / 'bridge-fixture.stderr').write_bytes(fixture.stderr)
    receipt['bridge_fixture_exit'] = fixture.returncode
    if fixture.returncode:
        (output / 'build.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
        raise RuntimeError('Bridge ABI qualification failed; retained fixture logs')
    modes=[]
    for mode in range(62):
        destination=output/(f'exact-dll-{mode}' if mode!=7 else 'exact-dll-7-\u7814\u7a76-\u0394')
        destination.mkdir()
        if mode==7:(output/"SorOutpostGeometrySnapshot.output-path").write_bytes((str(destination)+"\n").encode("utf8"))
        try:
            run=subprocess.run([str(output / 'd5ar-plugin-fixture.exe'),str(dll),str(destination),str(mode)],
                               cwd=output,capture_output=True,timeout=90 if mode==4 else 30)
        except subprocess.TimeoutExpired as error:
            (destination/'stdout.log').write_bytes(error.stdout or b'')
            (destination/'stderr.log').write_bytes(error.stderr or b'')
            receipt['exact_dll_modes']=modes+[dict(mode=mode,exit='OWNED_FIXTURE_TIMEOUT')]
            (output/'build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
            raise
        (destination/'stdout.log').write_bytes(run.stdout)
        (destination/'stderr.log').write_bytes(run.stderr)
        modes.append(dict(mode=mode,exit=run.returncode))
    receipt['exact_dll_modes']=modes
    receipt['fixture_host_sha256']=sha(output / 'd5ar-plugin-fixture.exe')
    rejected=[]
    for kind in ('renamed','modified'):
        folder=output/('guard-'+kind);folder.mkdir()
        host=folder/('other-host.exe' if kind=='renamed' else 'd5ar-plugin-fixture.exe')
        shutil.copyfile(output/'d5ar-plugin-fixture.exe',host)
        if kind=='modified':
            with host.open('ab') as stream:stream.write(b'D5AR owned negative identity control')
        run=subprocess.run([str(host),str(dll),str(folder),'0'],cwd=output,capture_output=True,timeout=20)
        (folder/'stdout.log').write_bytes(run.stdout);(folder/'stderr.log').write_bytes(run.stderr)
        if run.returncode!=6 or list(folder.glob('*.snapshot.json')):raise RuntimeError('Host identity guard failed')
        rejected.append(dict(kind=kind,exit=run.returncode,sha256=sha(host)))
    receipt['negative_host_guards']=rejected
    if any(row['exit'] for row in modes):
        (output / 'build.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
        raise RuntimeError('Exact DLL qualification failed; retained per-mode logs')
    sys.path.insert(0,str(snapshot/'research/resource-retained-population'))
    from d5ar_snapshot import read_snapshot
    decoded=[]
    for artifact in sorted(output.glob('exact-dll-*/*.snapshot.json')):
        value,_=read_snapshot(artifact)
        decoded.append(dict(path=str(artifact.relative_to(output)),status=value['snapshot']['status'] if 'snapshot' in value else value.get('status'),sha256=sha(artifact)))
    receipt['independent_decoder']=dict(sha256=sha(ROOT/'research/resource-retained-population/d5ar_snapshot.py'),artifacts=decoded)
    tool=Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/bin/Hostx64/x64')
    receipt['toolchain']={name:sha(tool/name) for name in ('cl.exe','link.exe','ml64.exe','c1xx.dll','c2.dll')}
    sdk=Path('C:/Program Files (x86)/Windows Kits/10')
    receipt['windows_sdk_version']='10.0.26100.0'
    receipt['windows_sdk_files']={name:sha(sdk/name) for name in ('Include/10.0.26100.0/um/Windows.h','Lib/10.0.26100.0/um/x64/bcrypt.lib','Lib/10.0.26100.0/um/x64/kernel32.lib')}
    # Local review package only, never installed or uploaded. ZIP timestamps/order
    # are fixed; source snapshot rebuilds generated guards from the pinned PE.
    package=output/'SorOutpostGeometrySnapshot-0.1.0-NOT-AUTHORIZED.zip'
    entries={'SorOutpostGeometrySnapshot.dll':dll,'source-lock.json':output/'source-lock.json'}
    entries.update({str(p.relative_to(snapshot)).replace('\\','/'):p for p in snapshot.rglob('*') if p.is_file()})
    with zipfile.ZipFile(package,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,path in sorted(entries.items()):
            item=zipfile.ZipInfo(name,(1980,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16
            archive.writestr(item,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    receipt['package_sha256']=sha(package)
    receipt['package_status']='LOCAL_REVIEW_ONLY_NOT_AUTHORIZED_NO_DEPLOYMENT'
    receipt['source_preserved']=all(sha(ROOT/path)==digest for path,digest in identities.items())
    if not receipt['source_preserved']:
        (output/'build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
        raise RuntimeError('Workspace source changed during qualification; package remains snapshot-only development output')
    (output / 'build.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(output, receipt['dll_sha256'], lock_hash)


if __name__ == '__main__':
    main()
