# SPDX-License-Identifier: GPL-3.0-or-later
"""Read another bounded function set on the verified D5AH disposable project.

Reuses the exact completed export01 command, copy and owned exporter after
verifying all original/copied core pins. Writes a fresh output directory only;
Ghidra opens only the disposable project, read-only with no analysis. Rechecks
core files and space afterward. No game, save, network or Git mutation.
SOR-P-0002: adapts d5ag_export.py without making another full project copy.
"""
import json
from pathlib import Path
import subprocess
import sys
from d5ad_baseline import guard, sha
ROOT=Path(__file__).resolve().parents[2]
def main():
    if sys.flags.optimize or not __debug__:raise RuntimeError('Use Python -E -B')
    prior=ROOT/'.local-work/d5ah-extractor/export01'
    r=json.loads((prior/'result.json').read_bytes())
    if not r['original_core_preserved'] or not r['copy_core_preserved']:raise RuntimeError('Copy not qualified')
    label=sys.argv[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):raise ValueError('Simple label')
    out=ROOT/'.local-work/d5ah-extractor'/label
    if out.exists():raise FileExistsError(out)
    free=guard()
    pins=dict(r['originals'],**r['copied'])
    for name,digest in pins.items():
        if sha(name)!=digest:raise ValueError('Pre-export drift '+name)
    cmd=[s.replace(str(prior),str(out)) for s in r['command']]
    at=cmd.index('-postScript')
    cmd=cmd[:at]+['-postScript','ExploreD5S.java',str(out/'native.tsv'),*sys.argv[2:],'-log',str(out/'ghidra.log'),'-scriptlog',str(out/'script.log')]
    if '-readOnly' not in cmd or '-noanalysis' not in cmd or any('D:/ReverseEngineering' in s or 'D:\\ReverseEngineering' in s for s in cmd):raise ValueError('Unsafe command')
    out.mkdir()
    (out/'ExploreD5S.java').write_bytes((prior/'ExploreD5S.java').read_bytes())
    for n in ('ghidra-settings','ghidra-cache','java-tmp','java-home'):(out/n).mkdir()
    result=dict(command=cmd,pins=pins,prior_receipt_sha256=sha(prior/'result.json'),free_before=free,method_sha256=sha(__file__))
    (out/'command.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    with (out/'stdout.log').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:
        run=subprocess.run(cmd,cwd=ROOT,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
    for name,digest in pins.items():
        if sha(name)!=digest:raise ValueError('Post-export drift '+name)
    if run.returncode or not (out/'native.tsv').read_text().endswith('END\n'):raise RuntimeError('Export incomplete')
    result.update(exit=run.returncode,native_sha256=sha(out/'native.tsv'),free_after=guard(),core_preserved=True)
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(output=str(out),sha256=result['native_sha256'])))
if __name__=='__main__':main()
