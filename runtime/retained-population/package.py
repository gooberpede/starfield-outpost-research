# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare one local review ZIP from an already qualified build; no deployment.

Reads pinned build/qualification, original source and existing notices. Writes
exclusive ignored package/source/manifest files. Stdlib only; no game or network.
"""
import json
from pathlib import Path
import shutil
import sys
import zipfile
from build import ROOT, SRC, LOCAL, sha, guard


def main():
    build=Path(sys.argv[1]).resolve()
    assert build.is_relative_to(LOCAL)
    guard()
    manifest=json.loads((build/'build.json').read_text())
    qualified=json.loads((build/'qualification.json').read_text())
    assert sha(build/'SorRetainedPopulation.dll')==manifest['dll_sha256']==qualified['dll_sha256']
    assert all(sha(p)==h for p,h in manifest['sources'].items())
    package=build/'deployment';package.mkdir(exist_ok=False)
    target=package/'Data/SFSE/Plugins/SorRetainedPopulation.dll';target.parent.mkdir(parents=True);shutil.copyfile(build/'SorRetainedPopulation.dll',target)
    notices=package/'ResearchNotices';notices.mkdir()
    shutil.copyfile(ROOT/'LICENSE',notices/'PROJECT-LICENSE.txt')
    shutil.copyfile(ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt',notices/'SFSE-PluginAPI-LICENSE.txt')
    (notices/'README.txt').write_text('D5P 0.1.0. Phase A review only; Phase B NOT AUTHORIZED.\nOnly Data/SFSE/Plugins/SorRetainedPopulation.dll is installed.\nSources and build/qualification manifests remain alongside this ZIP in the project.\n',encoding='utf8',newline='\n')
    archive=build/'SorRetainedPopulation-0.1.0-review.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(package.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(package).as_posix())
    files={p.relative_to(package).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p)) for p in package.rglob('*') if p.is_file()}
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(files)
        assert all(z.read(n)==(package/n).read_bytes() for n in files)
    result=dict(schema='sor-d5p-package/1',phase_b='NOT_AUTHORIZED',zip=str(archive),zip_sha256=sha(archive),
                dll_sha256=manifest['dll_sha256'],build_sha256=sha(build/'build.json'),qualification_sha256=sha(build/'qualification.json'),
                runtime_essential=['Data/SFSE/Plugins/SorRetainedPopulation.dll'],files=files)
    with (build/'package.json').open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
