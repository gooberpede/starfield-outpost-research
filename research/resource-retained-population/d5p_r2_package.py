# SPDX-License-Identifier: GPL-3.0-or-later
"""Wrap the unchanged R1 DLL for proposed operator-owned Vortex installation.

Reads existing R1 build04, approved notices and completed R2 offline receipts.
Creates one new hash-bound ZIP/manifest under the qualification scratch child.
No compilation, deployment, target action or dependency download. Stdlib only.
"""
import json
from pathlib import Path
import sys
import zipfile
from d5p_r2_diagnostics import ROOT, DLL, PROFILE
from build import sha, guard


def main():
    out = Path(sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5p-r2')
    guard()
    qualification = json.loads((out / 'qualification.json').read_text())
    assert qualification['disposition'] == 'OFFLINE_CONTROLS_PASS' and qualification['dll_sha256'] == DLL
    r1 = ROOT / '.local-work/d5p/r1-build04'
    assert sha(r1 / 'SorRetainedPopulation.dll') == DLL
    files = {'Data/SFSE/Plugins/SorRetainedPopulation.dll': (r1 / 'SorRetainedPopulation.dll').read_bytes(),
             'ResearchNotices/PROJECT-LICENSE.txt': (ROOT / 'LICENSE').read_bytes(),
             'ResearchNotices/SFSE-PluginAPI-LICENSE.txt': (ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt').read_bytes(),
             'ResearchNotices/README.txt': b'Unchanged R1 build04 observer 0.2.0, sor-d5p/2, eleven hooks, full acquisition.\nNew distribution wrapper only, for proposed R2 context diagnosis.\nPROPOSAL ONLY - NOT AUTHORIZED FOR INSTALLATION OR RETAIL EXECUTION.\nOnly Data/SFSE/Plugins/SorRetainedPopulation.dll is a runtime component.\n'}
    archive = out / 'SorRetainedPopulation-R1-0.2.0-R2-proposal.zip'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist()) == set(files) and z.testzip() is None
        assert all(z.read(name) == data for name, data in files.items())
    import hashlib
    pins = ['docs/experiments/resource-retained-population/run-card-d5p-r2.md',
            'docs/experiments/resource-retained-population/d5p-r2-decision.md',
            'research/resource-retained-population/d5p_r2_diagnostics.py',
            'runtime/retained-population/read_capture.py']
    manifest = dict(schema='sor-d5p-r2-package/1', authority='PROPOSAL_ONLY_NOT_AUTHORIZED',
                    binary_origin='UNCHANGED_R1_BUILD04_NOT_REBUILT', profile=PROFILE,
                    plugin_version='0.2.0', evidence_schema='sor-d5p/2', hooks=11,
                    dll_sha256=DLL, dll_path=str(r1 / 'SorRetainedPopulation.dll'),
                    zip=str(archive), zip_sha256=sha(archive),
                    r1_build_sha256=sha(r1 / 'build.json'), qualification_sha256=sha(out / 'qualification.json'),
                    pins={p: sha(ROOT / p) for p in pins}, installed=qualification['installed'],
                    files={n: dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest()) for n, b in files.items()})
    with (out / 'package.json').open('x', encoding='utf8', newline='\n') as f:
        json.dump(manifest, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(zip=str(archive), sha256=manifest['zip_sha256'])))


if __name__ == '__main__':
    main()
