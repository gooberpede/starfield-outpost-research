# External adapter latency — SOR-EXP-0026 / SOR-EV-0034

**Current disposition — SOR-EXP-0028:** [ABANDON EXTERNAL DEBUGGER PATH](thread-control-final-report.md).
The final offline thread-control repair attempt is complete and fails the safe
retirement gate. [Final review](thread-control-final-review.md) preserves all
baselines and negative evidence. Earlier candidate/procedure/latency descriptions
below remain historical; no new live candidate or exploratory attachment follows.

2026-10-11 Australia/Sydney. [Authorized follow-up](../../implementation-briefs/CODEX_BRIEF_SOR_event_adapter_latency.md),
SOR-D-0045. REVIEW-REQUIRED; all raw/private artifacts LOCAL-ONLY. No Starfield
launch/attachment/deployment, save/database mutation, staging, commit or push.

**The dominant measured cost is the synchronous evidence writer.** A timing-only
0.1.2 derivative's serial center-only control spends169.078 seconds in the writer
path across 83 boundaries; memory APIs total 3.341 milliseconds, control APIs
15.954 milliseconds and explicit suspension0.560 milliseconds. Required disk
queries cost192.413 milliseconds. Native memory acquisition/replay does not
explain the second-scale pauses in this fixture. [Full comparison and receipts](qualification.md).

0.1.3 preserves the exact two-site center and independently optional five-site
grid contracts, but writes one ordered append-only evidence file. Each logical
field/event retains its own synchronous durable append. Conventional separate
raw-file/journal creation moves to offline materialization after detach. A
memory-only writer queue or a boundary-wide commit would lose0.1.2's already
completed field prefixes on an adapter crash during later collection; neither
is used. Durability is not exchanged for latency.

| Element | Scoped answer |
|---|---|
| Confidence | Direct QPC observations with exclusive component accounting; high confidence in the sampled I/O bottleneck. Test outcomes establish only disposable behavior. |
| Coverage | Pinned 1.16.244.0 guards; same original fixture workload, center/full/independence/zero/retirement/writer controls; storage/scheduler/load effects remain machine-specific. |
| Completeness | Pure kernel transport cannot be isolated from the scheduler and instruction execution by debugger timestamps. The replay-delivery upper bound is reported separately; unrelated waits are not called debugger overhead. |
| Acquisition correctness | All process reads and identity/pairing decisions stay at the stopped boundary. Offline expansion never dereferences a target pointer. Raw native outputs, argument/context bytes and acquisition timestamps survive in the WAL. |
| Durability | Completed logical operations call FlushFileBuffers before returning; full frame bytes, hash and metadata are together. No backlog or early continue on an unacknowledged field. Earlier valid prefixes remain recoverable without a terminal record. Physical power-loss/storage-device honesty is untested for both versions. |
| Next step | Review final comparison/qualification and the [two-site center-only smoke proposal](operator-card.md); separately authorize any live action. Grid stays off for that first smoke. |

## Why the writer changes

0.1.2 creates a new raw file with WRITE_THROUGH, writes/flushes it, hashes it,
then writes/flushes a journal record on each field. 0.1.3 keeps one WAL handle,
serializes the raw bytes/metadata together and flushes once per logical record.
The raw file/derived journal representation is regenerated only after detach.
Hex encoding doubles raw payload size, a measured-size tradeoff for a simple
original parser and no additional dependency. No acquisition quota is introduced.

The [Microsoft FlushFileBuffers contract](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers)
describes the explicit flush and warns of repeated-flush inefficiency. This is
SOR-S-0137 consultation, not copied implementation or proof of hardware behavior.
Full asynchronous acquisition would require either accepting a volatile loss
window or waiting for a durable acknowledgement before continuing. The latter
still leaves the durable write inside the stopped interval. The selected modest
change removes avoidable representation work while preserving field durability.

## Baseline, reproduction and review

The immutable copied0.1.2 baseline, all six candidate-07 controls/raw sections,
original source/helper snapshots, generated guards, compiler receipts and prior
review artifacts are under ignored `.local-work/event-latency/baseline-012/`.
[Baseline hash manifest](../../../.local-work/event-latency/baseline.json) covers
all 2683 copied files; originals are unchanged. For reproduction, copy its
`working-tree/` into a NEW scratch tree and use that tree's source README command
with a NEW run name and the pinned installed MSVC/SDK/game. Do not run a build in
the preserved baseline itself. The original versioned ZIP is preserved too.

The profiling derivative has separate source snapshots and compiler/fixture/
adapter hashes; it is not substituted for the 0.1.2 baseline. Its original
preparer and exact built sources are retained in the review package. Current
0.1.3 reproduction uses [the source README](../../../debugger/event-oracle/README.md).
No new third-party code, licence acceptance, download, contact or disclosure.
`capture_epoch.h` is an attributed local adaptation of this project's collector;
shared observer 0.1.1/EXP0002 sources remain unchanged. Existing SOR-S-0132/
SOR-P-0002 provenance applies to the inherited methods.

- [Qualification, failures and numerical comparison](qualification.md).
- [WAL format and measurement contract](transport.md).
- [Center-only prospective operator card](operator-card.md).
- [Review manifests, patches and package](review.md).

## Procedure follow-up after adapter approval

2026-10-11 SOR-D-0046:0.1.3 approved; [exact center-only run card](center-only-live-run-card.md)
and [read-only operational-check review](procedure-review.md) prepared before
attachment. Ordinary Steam launch proposed, no SFSE/Vortex deployment. Approved
adapter/source unchanged; no live execution or scientific promotion.

## First authorized center-only attempt

2026-10-11: maintainer approved the exact card and accepted stall exposure.
[Attempt result](center-smoke-20261011-result.md): preflight PASS; adapter 0.1.3
exited before READY/evidence, original code/no debugger independently confirmed
while target survived. User exited normally, protected inputs unchanged.
No acquisition/live qualification; root cause UNKNOWN, no automatic retry.

## Startup fail-fast diagnosis and candidate 0.1.4

[EXP0027 investigation](startup-failfast-investigation.md) reproduces 0.1.3's
secondary timing-write exception masking primary startup errors. [Fault map](startup-fault-map.md),
[candidate qualification](startup-014-qualification.md) and [review](startup-review.md)
retain exact baselines and a separate threaded runtime counterexample. Original
primary rejection remains unknown; no new live readiness/attachment authority.
