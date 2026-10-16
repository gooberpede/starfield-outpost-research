# Frozen scope, regression and preservation ledger

2026-10-16, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation.
[Brief](../../../implementation-briefs/CODEX_BRIEF_SOR_experiment_A_x87_state_preservation.md),
[report](report.md), [source/commands](../../../../research/x87-preservation/README.md).
The brief's PASS/NO-GO definition is unchanged. No lowered required-state
definition or alternate breakpoint strategy was adopted.

The authorized experiment reads owned baseline source and historical receipts,
uses the existing MSVC/MASM/SDK/CPython toolchain and disposable authored inputs,
and writes only new source/docs and ignored `.local-work/x87-preservation/`
outputs. No retail executable is invoked. Target intervention is confined to
the fixture's own INT3 sites and process-local handler. A fault may end that
disposable process; no other process is opened or terminated. Stop on API/test
failure, protected-input mismatch, caller-available C:/D: space below
40,000,000,000 bytes, or writes outside the declared boundary. Run directories
are exclusive and retained, including failures. Cleanup is process-owned resource
exit; evidence deletion requires a later decision.

| Mandatory criterion | Result | Primary evidence and limit |
|---|---|---|
| Comparable unpatched/minimal/adversarial preconditions | PASS | Final paired runs use the same generated probe/seed/modes; six controls in each process. Minimal omits adversarial callback work; diagnostics remain common. |
| Three observation boundaries and measurement qualification | PASS | Every state frame has duplicate pre saves, first assembly VEH capture when trapped, raw FltSave, and immediate post-instruction save; all pre duplicates agree. No kernel-entry capture. |
| Every required x87 field and full pointers | PASS after correction | Corrected 99 minimal and 1,112 adversarial trapped frames match meaningful CW/SW/tag/opcode/80-bit payloads/FIP64/FDP64; selectors are separately recorded legacy zeros. Uncorrected pointers fail in every trapped frame. |
| First divergence localized without invented cause | PASS | Context lacks high words at entry while hardware retains them. Uncorrected hardware loses them by post boundary; exact OS instruction unknown. |
| Exactly one evidence-based correction or justified NO-GO | PASS | correction-plan.md predates implementation; entry data independently matches pre-state; one merged restore image plus leaf FXRSTOR64 strategy. |
| Nested and interrupted observations | PASS within fixture | One real nested REJECT inside ACCEPT, maximum depth 2; child and parent full states independently compared. Caught RaiseException interrupts handler work; C++ owned-group unwind remains in geometry controls. Arbitrary unwind through leaf restore NOT TESTED. |
| Concurrent re-entry/correlation isolation | PASS within fixture | Four-worker 1,000-probe phase; second four-worker STOP phase; nine total recorded thread IDs and maximum two simultaneous handlers. Per-probe before/entry/after and restore-image provenance agree, including distinct FDP stack addresses. |
| STOP, in-flight events, retirement/quiescence | PASS within fixture | Both final logs record STOP_inflight_confirmed=true; an explicit barrier holds a live handler, admission closes, barrier releases, all workers join before unpatch/unregister; post-retirement controls pass. No asynchronous removal qualification. |
| Both native-decision continuation classes | PASS | Authored ACCEPT MOV and REJECT ADD plus post-cleanup ACCEPT; exact RBX, flags and next-boundary state. No retail execution. |
| GP, flags, SSE/AVX, MXCSR and control flow | PASS | Native assertions and decoder independently compare all state probes including nested child; two arithmetic-flag patterns, three MXCSR modes, 16 distinct YMM patterns and XMM. |
| Evidence correspondence and decoder malformed controls | PASS | Corrected geometry decode: 64 frames, 46 complete/18 invalid, five threads; all complete bytes/uses and frozen replay agree; eight malformed controls rejected. New state decoder rejects four malformed variants. |
| Frozen evaluator regression | PASS | 12 test_resource_spatial tests; unchanged SHA256 500de4a2304e02fda1566a996ce58a865de5adc9625d34eb61569548916294cb. |
| Protected inputs, rights and provenance | PASS within selected inventory | 206 before/after SHA256 pins, HEAD/index and local evidence manifest; scope below. Existing owned toolchain lineage and consulted references recorded. No new code reuse permission basis. |
| Report, field table, reproducible code/commands, exact patches, prose and independent review | PASS subject to the exact [review record](review.md) | Package manifests and actual reviewer return identify accepted snapshot; maintainer integration/publication remains separate. |
| Retail safety and native spatial equivalence | NOT TESTED | Scope exclusion, not an offline preservation failure. No target survival/restoration outcome applies. |

## Receipts and provenance

The local root retains preservation-before.json, preservation-after.json,
verification.json, changed-files.json, complete-files.json, exclusions.json,
git-status-short.txt, evidence-files.json, regression.json, package.json and
package.sha256, plus the independent reviewer return. Each run directory retains
exact generated sources, MASM listing, tool hashes, build/run log and binary
state evidence. The complete file inventory with hashes is evidence-files.json;
build.json separately identifies its actual compiled source/tool snapshot.

Final host: GenuineIntel CPUID signature `0x000a0655`, XCR0 `0x1f`, Windows
`10.0.19045` as reported by CPython win32_ver, CPython 3.14.3, MSVC
19.51.36256.0, MASM/link 14.51.36256.0. This is host provenance, not a validated
Starfield build/runtime baseline. Existing compiler/runtime/SDK inputs remain
the previously authorized installed tools; no external implementation is copied.

The selected 206 pins cover inherited native/export/executable inputs, original
observer 0.8.0 source, frozen save-analysis scripts, prior/supplied briefs, the
entire baseline fixture source directory and historical native-11 run files,
and the Git index. preservation-before.json lists every exact path and hash.
This is not a recursive audit of all saves, capture archives, packages or Ghidra
databases. Unscanned protected collections were not opened or written. No
preservation claim is inferred merely from ignore rules. The installed executable
was hashed as data, not loaded. The prior 132-pin receipt supplied path selection;
every selected current byte was independently hashed for this task's baseline.

The scientific outcome is corrected scoped preservation PASS; the original route
remains FAIL. Instrumentation integrity is supported for the successful final
fixtures, with the initial harness failure retained. Only disposable processes
ran and exited; game survival/cleanup is not applicable. Authority compliance
includes no game, observer/DLL, Vortex package/deployment, save/settings/database,
staging, commit, push or external contact. Private binary evidence remains excluded
from review diffs and does not acquire publication clearance from this PASS.
