# SPDX-License-Identifier: GPL-3.0-or-later
"""Activate an already-ready 0.1.3 window before the operator CLICK NOW handoff.
Reads explicit ignored run evidence; creates durable .start and handoff receipt.
No target memory/control APIs, launch, attachment or game UI action. GetTickCount64
checks the native deadline on the same host; never resets an expired window.
"""
import argparse,ctypes,json,os,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def activate(prefix):
    prefix=prefix.resolve()
    assert prefix.is_relative_to(ROOT/'.local-work/exp0002a-adapter-0.1.3')
    path=lambda s:Path(str(prefix)+s)
    def rows():
        b=path('.native.jsonl').read_bytes()
        return [json.loads(x) for x in b[:b.rfind(b'\n')+1].splitlines()]
    before=rows()
    assert path('.armed').exists() and all(x['version']=='0.1.3' for x in before)
    assert any(x['kind']=='armed' for x in before)
    assert not any(x['kind'] in ['failure','target_exit','capture_finished','complete','capture_started'] for x in before)
    with path('.start').open('xb') as f:f.flush();os.fsync(f.fileno())
    end=time.monotonic()+3
    while not path('.active').exists():
        if time.monotonic()>end:raise TimeoutError('No active acknowledgement; DO NOT CLICK')
        time.sleep(.01)
    current=rows();active=next(x for x in current if x['kind']=='capture_started')
    assert not any(x['kind'] in ['failure','target_exit','capture_finished','complete'] for x in current)
    k=ctypes.WinDLL('kernel32');k.GetTickCount64.restype=ctypes.c_ulonglong
    now=k.GetTickCount64();remaining=active['deadline_tick_ms']-now
    assert remaining>=7000,'Insufficient remaining handoff time; DO NOT CLICK'
    receipt={'status':'CLICK_NOW','active_tick_ms':active['tick_ms'],'handoff_tick_ms':now,'deadline_tick_ms':active['deadline_tick_ms'],'remaining_ms':remaining,'clock_reset':False}
    with path('.handoff.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2);f.flush();os.fsync(f.fileno())
    print(json.dumps(receipt),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prefix',type=Path,required=True);activate(p.parse_args().prefix)
