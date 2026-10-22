# Qualification, preservation and risk report

[Report/criteria](report.md), [contract](contract.md), [card](run-card.md).
All paths below are relative to repository root unless absolute. Raw artifacts
remain ignored/local. No game launch, retail attachment or retail measurement
occurred. Compiler execution and disposable synthetic Windows debugging are the
only target executions. Read-only installed-file/save audits do not grant Phase B.

## Executed commands and primary receipts

Use installed Python3.14.3 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe` for `python` below.
Installed MSVC19.51.36256.0/MASM and Windows SDK are build prerequisites, not
vendored/downloaded dependencies. Exact compiler commands/versions/input/output
SHA256s are in each immutable build.json/build.log.

```powershell
python -B research/resource-region-ancestry/build.py --name build06
python -B research/resource-region-ancestry/qualify.py --build .local-work/resource-region-ancestry/build06 --output .local-work/resource-region-ancestry/qualification05
python -B research/resource-region-ancestry/preflight.py --build .local-work/resource-region-ancestry/build06 --qualification .local-work/resource-region-ancestry/qualification05/qualification.json --name offline-preflight03
python -B research/resource-oracle-retail/qualify.py --build .local-work/resource-oracle-retail/build14 --output .local-work/resource-oracle-retail/qualification-c1e-regression01
python -B research/resource-oracle-collector/qualify.py --build .local-work/resource-oracle-collector/build08 --output .local-work/resource-oracle-collector/qualification-c1e-regression01
```

Earlier offline-preflight01/02 and qualifications remain preserved;03 is the
final inventory including Python source pins. Later reproduction requires fresh
output names. Final analyzer outputs, after-exit audit and protection checks are
listed in the local delivery metadata. `collect.py --help` was exercised; its
retail branch was **not** executed, qualified as a whole, or given a GO receipt.
The C1D decoder/debug-event/transport core it adapts has fresh regressions.

| Final synthetic group | Primary behavior and scope |
|---|---|
| good/copper/reject/empty | Actual target memory and representative broadphase/count-one/count-zero decisions. Accepted pointer enters a real temporary set; rejection contributes none. Resource namespace copied through unchanged C1D associated-file reader. |
| multi/multi-reject | Fixture executes consecutive-segment geometry on target-owned points, both outcomes. This independent double-arithmetic union is a fixture decision oracle, **not retail tapered/height implementation equivalence**. |
| mixed/sources | Reject region0 then accept region1; two distinct source wrappers/ordinals with IL/Cu reduced to one transfer. Exact selected collection and region ordinal; same-ID/time lookup is not used. |
| nested/threads | Inner rejected updater/outer accepted updater, distinct entry tokens and parent chain; three thread lifetimes with changed point memory. No pointer/time generation epoch. Finite coverage does not exhaust all concurrent-writer/unwind/scheduler paths. |
| wrong-workshop/wrong-source/wrong-caller/stale-transfer | Failed identity/source/return-caller ancestry stays UNKNOWN; no useful native-equivalence promotion. |
| wrong-resource/outside-region | Resource-slot key/type or exact region membership fails; copied bytes alone do not qualify lineage. |
| partial/corrupt/oversized/byte-budget/maximum | Unreadable point data, count>capacity, huge capacity, explicit16-byte copy budget refusal, and actual4096-point/64KiB copy. Failed lists null, observed empty list distinct. Allocation-byte refusal occurs before resizing; actual OS out-of-memory is not injected. |
| invalid-source/source-budget/empty-collection/corrupt-collection/invalid-collection/invalid-procgen | Partial source/collection ancestry and failed required source reads, durable loss reason, incomplete END; invalid pointers never become empty native populations. |
| guard-mismatch/ackfail/crash-before/crash-after/completion | Fatal guard LOSS, rejected ACK and disposal, zero pre-evidence acquisition, durable evidence before crash, and same-stop verified ACK/STOP termination. Failures and acquisition versus target survival are separate. |

**32/32 cases PASS;99 memory receipts /297 SRO1 frames.** Existing C1D40 decoder
assertions +13 actual attachment scenarios and unchanged C1C19 cases freshly pass.
Negative acquisitions marked FAIL inside those regression logs are expected
test outcomes, not failed qualification cases. Each C1E case preserves config,
command, synthetic-labelled events, raw samples/ACKs, stderr, results and hashes.
Separate framing parser precedes every ACK; independent critic separately parsed
all99 final receipts/297 frames and ACK digests/lengths.

Final engineering-metrics-final.json: max copy47ms, max reader67,380 bytes/stop,
largest framed capture138,785 bytes, including the4096-point case. These are
warm disposable-fixture observations, not retail cold-page/lock-duration maxima
or justified healthy-session timeouts. Read ceilings remain64KiB/read and1MiB/stop;
region/point capacities4096. Retail full owner/alias lifetime safety, AVX/YMM/XSTATE
preservation, physical disk failure and exhaustive concurrency remain untested.

## Preserved failures and independent rework

- Build01/02 were intermediate. Qualification01 failed to locate the renamed
  fixture (inherited c1d filename), then its test harness indexed a missing
  decision. No game action. Corrected binary name and defensive reporting.
- Qualification02's22 cases passed but independent review found that the fixed
  transfer list and packet-supplied verdict failed to test causality/geometry.
  No scientific promotion from that suite. Reworked actual temporary set and
  representative target-memory predicates; mixed/source/nesting tests added.
- Qualification03 tested error accounting and temporary reduction while fixture
  verdict controls were still intermediate;04 added actual geometry branches.
- Build05 failed on Windows min/max macros; NOMINMAX corrected build06. The
  failed build and failed qualification admission were preserved, never launched.
- Review found END.complete ignored failed required reads and useful STOP lacked
  query-read flags. Corrected harness/wrapper/analyzer; qualification05 explicitly
  tests invalid-procgen complete=false. No original receipt was edited.
- Read-only postflight originally omitted newly added definitions/config files;
  corrected full set comparison preserves additions/removals/changes before
  assertions. Authored text encoding was checked; an intermediate Windows-default
  decoding error was corrected from original HEAD bytes plus intended additions.

## Preservation and intervention risks

Phase A inventories all271 live saves/3,060,578,336 bytes and the independently
held271 backups; both match prior master inventory. Scratch restore rehearsals
match Save52 master SHA; live originals/backups never overwritten. Installed39
definition files and existing config are hash-recorded; this is an installed
inventory, not a runtime load map/effective override certificate. Cloud status
today is UNKNOWN until fresh operator confirmation. All prior2264 selected
code/doc/raw-receipt files plus229 inherited protected input pins are rechecked
in protected-final.json; frozen complete-geometry files are independently checked
by analyzer. HEAD/index remain initial baseline; no staging/commit/push.

Windows all-stop debugging changes scheduling, debug/control state and potentially
lock duration. Full copied bytes establish a stopped snapshot, not historical
producer stability, an owner lease, no ABA, catalogue truth or a renderer. The
minimal selected-region copy reduces read cost while preserving evidence needed
for new geometry. If a read fails, preserve partial receipts and classify loss;
if a disposable future retail game crashes after externally verified bytes, report
survival separately. Source/config/free-space failure stops affected operations.
No unbounded allocation or arbitrary scientific event/time cutoff is introduced.

## Files and effects

`build.py`: reads owned source/toolchain, writes fresh ignored binaries/logs.
`qualify.py`: verifies build pins, executes only sibling hash-pinned synthetic
fixture/controller and writes fresh local receipts. `controller.cpp/sample.inc`
and `ancestry.h`: C1D debug engine plus source-specific external reads; synthetic
and retail builds distinct. `fixture.cpp/asm`: synthetic memory/stack/decision
target only. `preflight.py`: file hashes, zero-process check and scratch save
copy; no launch or restore. `postflight.py`: hashes complete file sets after exit,
records differences and never restores. `analyze.py`: closed-file independent
parse/join/conditional replay, no target writes. Future `collect.py`: gated
new-process attachment and bounded external transport, debugger intervention and
declared disposal only under fresh human approval. Scripts use existing installed
toolchain/stdlib and owned pipeline; no download/network/analysis database writes.

Final patch/status/file/exclusion manifests and independent disposition are in
[review](review.md). Saves, raw native memory/exports, receipts, binaries, scratch
copies, toolchain logs and reviewer working outputs remain ignored/local. Their
hashes/locations are supplied locally, never treated as publication clearance.
