# Natural terrain-output acquisition preparation 0.1.0

Original disposable-only fixture/transport for [EXP0021](../../docs/experiments/durable-position-engine-oracle.md).
The [native contract](../../docs/experiments/engine-oracle/oracle-contract.md)
defines retail RVA ad0d3b. `contract.py` decodes raw results and explicitly labels
SYNTHETIC versus RUNTIME. It does not query the game or compute expected outputs.
`fixture.cpp`/`fixture.asm` arrange sentinel bytes matching the captured layout
on two independent fixture threads; these bytes are not native Starfield results.

`qualify.py` reads these sources, installed MSVC/SDK/x64dbg and original project
exp0002a transport/process reader; writes a NEW ignored engine-oracle run root;
builds/launches only this fixture, attaches x64dbg, inserts one auto-continue INT3,
captures raw output, pauses/removes it, verifies 32 restored bytes and independently
verifies detach. The fixture exits normally after release. Zero-hit mode performs
the same cleanup with no captured hit. No live-target option, game/save/database
access, native-save automation, dependency download or deployment. Prerequisites:
installed tools at explicitly supplied paths and 40 GB free on C: and D:.

```powershell
python -B debugger/engine-oracle/qualify.py --run review-NEW --debugger D:/tools/x64dbg/release/x64/headless.exe --vcvars 'C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat'
python -B debugger/engine-oracle/qualify.py --run zero-NEW --zero-hit --debugger D:/tools/x64dbg/release/x64/headless.exe --vcvars 'C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat'
python -B -m unittest discover -s debugger/engine-oracle -p 'test_*.py'
```

Each log line is flushed with disk checks; no tiny volume quota. Evidence is
non-atomic and debugger execution is intrusive. Failure receipts remain local;
cleanup failures are disclosed, never treated as semantic success. Qualification
does not establish retail reachability, safe ABI, live debugger cleanup or native
algorithm equivalence. Future live implementation/preflight needs separate review
and authorization. See [review receipts](../../docs/experiments/engine-oracle/review.md).
