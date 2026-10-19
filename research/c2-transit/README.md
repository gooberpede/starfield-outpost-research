# C2 finite transit calculations

Use installed CPython 3.14, `-B`, from the repository root:
`python -B research/c2-transit/calculate.py --run calculation01`.
The [authorized scope](../../docs/implementation-briefs/CODEX_BRIEF_SOR_C2_transit_time_continuation.md)
and [interpretation](../../docs/experiments/cargo-links/transport/transit.md)
govern this finite aid; it is not a general shipping simulator.

Reads ignored `.local-work/c2-transit/baseline.json` and `definitions01.json`,
all 21 pinned protected files, EXE PE section metadata/two native float defaults,
Git HEAD/index and its own source. Requires the protected originals, matching
existing acquisitions and at least 40,000,000,000 caller-available bytes on both
C: and D:. Writes one exclusively created ignored JSON receipt named by `--run`.
No game/native execution, save/DB/configuration writes, staging/commit/push,
network access, installation or dependency download. CPython stdlib only.

It recomputes binary32 dock conversion and strict detached threshold crossings,
rejects six invalid arithmetic inputs, compares native defaults and verifies
protected bytes/HEAD/index. Phase envelopes and two-leg 12-second additions are
explicitly conditional calculations, not validated controller admission or a
measured error distribution. Large calendar precision loss, variable frame
rate, queues, full flight and fuel stalls are outside those ideal examples.
It also calculates three ideal event cycles and checks the steady expression;
movement creates arrival timer phase, so simply adding 12 to full dock ticks
is a conservative nominal budget, not the unique steady duration. The final
receipt is `.local-work/c2-transit/calculation03.json` (33 checks).

The PE section read adapts the maintainer-owned C2 `flightconstants.py` method;
protected-source checks and guard reuse [S1](../s1-storage/README.md), with the
prior [C2 verification aid](../c2-transport/README.md) as provenance. No outside
implementation was introduced. The ignored original finite inspection helpers,
requests, failures and readOnly/noanalysis commands are pinned in the transit
source ledger. `TransitCalls.java` scans **existing** Ghidra instructions and
emits candidate virtual-call/pointer-load windows; it does not disassemble,
analyze, invoke or mutate target code. Full-listing scans are candidate censuses,
not typed callee proofs or a universal absence test. `read_native.py` only
splits completed exports; resulting `.c` files are convenience derivatives.

The ignored package helper adapts the owned C2/C1 exporter to create exact
complete/task-only text patches and disposable `.local-work/review-patches` reconstruction trees.
It checks forward/reverse bytes without applying to this workspace or changing
its index/refs. Ignored raw payloads, analysis files and bulk receipts remain
LOCAL-ONLY. No new third-party reuse or permission basis.
