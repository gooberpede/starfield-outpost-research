# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute disposable native fixtures through the future transport, including loss.

Reads a verified build, launches only its hash-bound fixture controller; writes
fresh local SRO1, journals and results. The controller disposes fixture processes
on STOP/loss. Never invokes retail controller or admission/attachment entry point.
"""
import json
from pathlib import Path
import sys
from build import LOCAL,pin
from collect_native import pump
from native_reduce import reduce
from qualify import old_qualification


def main():
    build,out=(Path(x).resolve() for x in sys.argv[1:]);assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest=json.loads((build/'build.json').read_text());assert all(pin(p)==h for p,h in manifest['files'].items())
    out.mkdir(exist_ok=False);image=pin(build/'sor-d5l-native-fixture.exe');results=[]
    for fault in (None,'pre-arm-stop','idle-collector-loss','idle-pipe-loss'):
        dest=out/(fault or 'basic');command=[str(build/'sor-d5l-native-fixture-controller.exe'),'--synthetic-fixture',image,'idle' if fault else 'basic']
        try:code=pump(command,dest,dict(synthetic=True),pin(build/'build.json'),True,fault)
        except RuntimeError:
            assert fault=='idle-collector-loss';code=None
        rows=[json.loads(s) for s in (dest/'events.jsonl').read_text().splitlines()];session=next(r for r in rows if r['kind']=='SESSION')
        passed=old_qualification.target_absent(session['pid'])
        if fault:
            passed&=not any(r['kind']=='SAMPLE' for r in rows)
            if fault=='pre-arm-stop':passed&=code==0 and not (dest/'READY.json').exists()
            elif fault=='idle-collector-loss':passed&=(dest/'transport-failure.json').is_file()
            else:passed&=code==2 and any(r['kind']=='FAILURE_CLEANUP' for r in rows)
        else:passed&=code==0 and bool(reduce(rows,image,True)['chains']) and (dest/'READY.json').is_file()
        results.append(dict(case=fault or 'basic',passed=bool(passed),controller_exit=code,target_absent=old_qualification.target_absent(session['pid'])))
        print(results[-1],flush=True)
    (out/'results.json').write_text(json.dumps(results,indent=2)+'\n');assert all(r['passed'] for r in results)


if __name__=='__main__':main()
