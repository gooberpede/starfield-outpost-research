# Existing-reference grid observer 0.4.0

Offline candidate under the [brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_existing_reference_grid_oracle_integrated.md).
[Schema](schema.md), [report](../../docs/experiments/existing-reference-grid/report.md),
[integrated run card](../../docs/experiments/existing-reference-grid/run-card.md).
No deployment, live execution or Git mutation is authorized by this implementation.

Runtime payload: `Data/SFSE/Plugins/SorNativePositionOracle.dll` only. The DLL
uses established dynamic /MD linkage to the already installed Microsoft runtime
and Windows system APIs. Build receipt pins System32 MSVCP140, VCRUNTIME140,
VCRUNTIME140_1 and ucrtbase prerequisites; none is bundled or deployed. No neighbor config,
README, manifest, source hashes or qualification report is read at runtime.
ZIP notices remain review/distribution material. No optional-text waiver exists.

Fifteen guarded complete CALL edits and RX leaf relays: enclosing route, eligibility,
search, fallback, source descriptor, native grid, two displacement sites, two
reference-angle sites, Q, E, sentinel selection, explicit-body selection, explicit
producer. The final bridge reads the proven selected RDI and operation RSI at
CALL 17DF4E2, forwards the four real native arguments and has MASM unwind metadata.
No entry detour, native call synthesis, debugger, forced key or dynamic unload.
STOP drains admitted work; all CALLs/relays stay resident and inert until normal exit.
Timing/execution are affected; fixture qualification is separate from retail safety.

| Tool | Reads, writes, effect |
|---|---|
|plugin/core/route/patch/health and producer bridge|Future approved own-process natural boundaries only; startup edits, TLS copies, bounded MPSC queue, durable session records and worker controls. No use against Starfield in this assignment.|
|build.py|Pinned on-disk game/SFSE, protected inputs, sources, installed MSVC/MASM/SDK; exclusive ignored outputs, compiler/linker and original disposable native fixtures only. No downloads/deployment/game execution.|
|route_tests.cpp and assembly|Original synthetic ABI bodies and memory, test-process CALL edits/restoration, thread/FP/exception controls and local raw evidence. Synthetic arithmetic is not a retail semantic oracle.|
|route_inspect.py/test_route.py|Immutable raw/journal/health/frozen inputs and original adversarial derivatives; exclusive outputs only; no process access.|
|operate.py|Future approved receipt/nonce/STOP helper; limited process metadata only when invoked live. Deployed preflight checks runtime-essential DLL only. No config or save mutation.|
|Retained branch/generic fixture/inspect modules|Project 030 transport regressions; schema 3 fixtures remain schema 3. They are not the schema 4 live analysis CLI.|

Build: CPython `runtime/native-oracle-040/build.py --name NEW --sfse EXACT_PATH
--vcvars EXACT_PATH` from repository root. Paths/hashes are pinned in the report/card.
Both C: and D: must have at least 40,000,000,000 caller-available bytes, with documented
write reserves. Queue 4096 is buffering, not a scientific event quota; saturation
stops admission and records loss. No event-count ceiling. Windows system DLLs and
existing compiler/SDK are separately installed tools, not new downloads.

Sources adapted from maintainer-authored runtime/native-oracle-030 at the task's
starting HEAD; hashes/modes in the report source ledger. Existing SFSE header and
MIT notice remain unchanged under SOR-P-0001. No other third-party implementation.
