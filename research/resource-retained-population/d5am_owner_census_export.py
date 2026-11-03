# SPDX-License-Identifier: GPL-3.0-or-later
"""Export bounded native windows from a fresh verified disposable project.

Reads the D5X original-core roster and owned D5S Java exporter/command. Copies
only pinned project files to a fresh disposable directory under D:/tools, then opens
that copy read-only with no analysis. Writes fresh ignored D5AM owner census receipts and
logs; Ghidra housekeeping is confined to the copy. No original project open,
game, save, network, symbols/types/comments or Git mutation. Stdlib and the
already installed Ghidra/JDK only. SOR-P-0002: adapted owned d5ai_ownership_export.py and its D5AH/D5S method.
Original helper xrefs and receiver-rooted bodies are data for a bounded caller
census, not an automatic proof excluding arbitrary computed lock users.
Stop on identity, disk-floor, path, subprocess or output-completeness failure.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import json
from pathlib import Path
import shutil
import subprocess

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]


def main():
    label = sys.argv[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('Simple output label required')
    out = ROOT / '.local-work/d5am' / label
    copy = Path('D:/tools') / ('sor-d5am-' + label)
    if any(p.is_symlink() or p.is_junction() for path in (out,copy) for p in (path,*path.parents)):
        raise ValueError('Reparse output/project copy prohibited')
    if out.exists() or copy.exists():
        raise FileExistsError('Fresh output and project required')
    guard()
    originals = json.loads((ROOT/'.local-work/d5x/identity05/identity.json').read_bytes())['database']
    original_root = Path('D:/ReverseEngineering/Starfield/GhidraProject')
    for path, expected in originals.items():
        if sha(path) != expected:
            raise ValueError('Original baseline mismatch: '+path)
    copy.mkdir()
    copied = {}
    for path, expected in originals.items():
        source = Path(path)
        target = copy/source.relative_to(original_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source,target)
        if sha(target) != expected:
            raise ValueError('Copy mismatch: '+str(target))
        copied[str(target)] = expected
    guard()
    old = ROOT/'.local-work/d5s/export01'
    command = json.loads((old/'command.json').read_bytes())
    command = [s.replace(str(old),str(out)).replace(str(original_root),str(copy)) for s in command]
    at = command.index('-postScript')
    command = command[:at]+['-postScript','ExploreD5S.java',str(out/'native.tsv'),*sys.argv[2:],
                           '-log',str(out/'ghidra.log'),'-scriptlog',str(out/'script.log')]
    if str(copy) not in command or any(str(original_root) in s for s in command):
        raise ValueError('Original launch prohibited')
    if '-readOnly' not in command or '-noanalysis' not in command:
        raise ValueError('Read-only flags required')
    out.mkdir(parents=True)
    reader = old/'ExploreD5S.java'
    (out/reader.name).write_bytes(reader.read_bytes())
    for name in ('ghidra-settings','ghidra-cache','java-tmp','java-home'):
        (out/name).mkdir()
    receipt = dict(command=command,originals=originals,copied=copied,
                   interpreter_sha256=sha(sys.executable),java_executable_sha256=sha(command[0]),
                   ghidra_utility_sha256=sha(command[command.index('-cp')+1]),
                   method_sha256=sha(__file__),reader_sha256=sha(reader),free_before=guard(),
                   origin_method='research/resource-retained-population/d5ag_export.py',
                   origin_sha256=sha(ROOT/'research/resource-retained-population/d5ag_export.py'))
    (out/'command.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    with (out/'stdout.log').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:
        result = subprocess.run(command,cwd=ROOT,stdout=stdout,stderr=stderr,
                                creationflags=subprocess.CREATE_NO_WINDOW)
    for path,expected in dict(originals,**copied).items():
        if sha(path) != expected:
            raise ValueError('Post-export drift: '+path)
    if result.returncode or not (out/'native.tsv').read_text(encoding='utf8').endswith('END\n'):
        raise RuntimeError('Export failed: '+str(result.returncode))
    receipt.update(exit=result.returncode,native_sha256=sha(out/'native.tsv'),
                   original_core_preserved=True,copy_core_preserved=True,free_after=guard())
    (out/'result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(output=str(out),sha256=receipt['native_sha256'])))


if __name__ == '__main__':
    main()
