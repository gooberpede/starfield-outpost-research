# D5AN validation commands and boundaries

2026-11-04, Australia/Sydney. Offline only. Execute from the repository root
using `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -E -B`.
New outputs are exclusive: the following records the actual final labels; use
fresh labels for another run. No command deploys a plugin or launches Starfield.
Local retained build16 inputs, approved support/toolchain and pinned installed
PE are prerequisites. A source-only checkout is not a standalone reproduction.

```powershell
$Python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $Python -E -B research/resource-retained-population/d5an_counter_build.py final09 --all
& $Python -E -B research/resource-retained-population/d5an_abi_qualify.py .local-work/d5an/final09 .local-work/d5an/abi-final09
& $Python -E -B research/resource-retained-population/d5an_scheduler_qualify.py scheduler-final09 .local-work/d5an/final09
& $Python -E -B research/resource-retained-population/d5an_counter_qualify.py .local-work/d5an/final09 .local-work/d5an/counter-final02
& $Python -E -B research/resource-retained-population/d5an_replay_qualify.py .local-work/d5an/final09 .local-work/d5an/replay-final02
& $Python -E -B research/resource-retained-population/d5an_native_census.py .local-work/d5an/final09 .local-work/d5an/native-final01
& $Python -E -B research/resource-retained-population/d5an_counter_package.py .local-work/d5an/final09 r1 --review-file docs/experiments/resource-retained-population/run-card-d5an-n2-proposal.md
& $Python -E -B research/resource-retained-population/d5an_n2_operations_qualify.py --build .local-work/d5an/final09 --plan .local-work/d5an/n2-proposal04/n2-plan-proposal.json --out .local-work/d5an/operations-final04
& $Python -E -B research/resource-retained-population/d5an_optimization.py .local-work/d5an/optimization-final03.json
```

`d5an_readiness.py` prepares the proposal using explicit `--build`, `--package`,
`--card`, `--out` and repeatable `--qualification` file arguments. Actual
proposal04 binds the final ABI, scheduler, counter, composition replay, nested
native replay and native census receipts, plus all 468 source/input pins.
The actual invocation and resulting plan/source-lock identities are retained in
the handoff and [report](d5an-report.md). Its authority is NONE.

The package tool rebuilds the frozen absolute-source recipe in a fresh working
directory and compares DLL bytes. A separately named build directory can embed
different fixture source paths and therefore have a different DLL hash; it
does not silently replace final09. Original failed/superseded paths are retained.

The counter reader's CLI accepts a session, `--dll-sha256` and `--dll` pointing
to the actual candidate. It requires the binary for D5AN image/export attribution;
legacy N1 reports remain LEGACY_NO_PROVENANCE. It never interprets state-1
partial fields as a complete first fault. The causal reader preserves legacy
bit restrictions unless D5AN is explicitly advertised.

Native hosts deliberately modify only their own private pages/counters and
include expected private crash/refusal cases. Finite fixture waits are engineering
bounds; they do not create a retail scientific deadline. The operations fixture
uses explicit retail-admission/protection/namespace substitutes, real ownership/
ACK/STOP and every-member archival. No fixture proves retail startup reliability,
universal liveness, task coverage or a winner distribution. Source/ABI, wire
integrity, science, preservation and target survival remain separate outcomes.
