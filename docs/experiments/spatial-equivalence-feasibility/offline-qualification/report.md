# Internal spatial-decision observation: offline qualification

2026-10-15, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation.
[Authorized brief](../../../implementation-briefs/CODEX_BRIEF_SOR_experiment_A_internal_observation_offline_qualification.md).
Authored results are REVIEW-REQUIRED; local native evidence/builds remain LOCAL-ONLY.

| Element | Answer |
|---|---|
| Question | Can a finite internal-edge fixture preserve relevant execution state and own complete operands paired with its actual decision? |
| Best-supported answer | **PASS, scoped synthetic qualification**, independently accepted within the limits below. A process-local exception probe resumes both tested terminal instruction classes faithfully; owned variable geometry and actual-use snapshots are independently decoded and replayed. This is not retail readiness. |
| Confidence | Direct disposable-process execution and independent byte-level decoding for the stated controls; STATIC grounding for retail boundaries. No new game-runtime finding. |
| Coverage | Two terminal instruction classes; direct/post-cleanup acceptance; rejection; GPR/flags/SSE/AVX/MXCSR controls; nested/concurrent entries; cooperative STOP; complete arrays through 8,192 points; 10 authored geometry/lifetime cases; 18 invalid/not-evaluated groups; eight decoder-negative controls. |
| Evidence | [Contract and schema](contract.md), [source and commands](../../../../research/internal-observation-qualification/README.md), local `native-11/run.log`, `build.json`, `geometry.bin`, `decode.json`, and [review](review.md). |
| Limits | Full x87 environment preservation **FAILS**. Synthetic leases/versions and fixed quads do not establish native writers, lifetimes, strip reconstruction, retail use-site capture or unwind/retirement safety. Spatial native equivalence is **NOT TESTED**. |
| Next step | Maintainer critical review. Any retail implementation and pre-live scientific-value review need a separate brief and approval; no observer or session follows this PASS. |

## Gate results

The original gates and frozen scope are detailed in [contract.md](contract.md).
No acceptance criterion was changed to rehabilitate a failed retail candidate.

| Criterion | Result | Actual evidence and precise limit |
|---|---|---|
| G1: relevant state and both correct terminal continuations | PASS for tested SSE/AVX classes | ACCEPT MOV preserves flags and loads RBX from closure+8; REJECT ADD changes RBX and arithmetic flags before original continuation. All GPRs/RSP and all 16 distinct YMM register/lane patterns compare; x87 values/control and MXCSR compare. Both arithmetic-flag patterns and three MXCSR controls exercise an adversarial callback. Entry/other use-site instructions are not executable qualifications. |
| G1: concurrency, reentry, interruption and cooperative retirement | PASS within fixture contract | Four workers, observed maximum two simultaneous handlers, one nested probe, caught RaiseException, C++ unwind of an active owned group, STOP while workers remain active, then join/quiesce, restore bytes, remove handler and run unpatched controls. No concurrent site removal or arbitrary asynchronous unwind is claimed. |
| G2: complete owned geometry and failure integrity | PASS for synthetic ownership protocol | Independent exact point and every-use byte checks, source storage freed before decode, zero/one/multi/large arrays, guarded bad pointer, count/use/pool capacity, synchronous mid-copy versioned ABA, missing/mismatched/duplicate/late terminals and STOP/unwind diagnostics. Uncooperative unversioned writers remain unsupported. |
| G3: actual-use/terminal ancestry and independent replay plumbing | PASS for finite fixture cases | Native fixed-quad branch arithmetic consumes the captured per-use locals. Exception-context RSI supplies a separately bound invocation token; terminal site supplies true/false. Decoder requires each fixture's broadphase/containment/per-vertex/edge resolution trace and rejects later-use provenance corruption. Frozen evaluator agrees for 46 complete groups. No native strip/rotation equivalence is inferred. |
| Additional full x87 environment diagnostic | FAIL, retained | Windows exception continuation changes high x87 instruction-pointer bits; `native-11` reports 1,110 pointer-loss diagnostics. This state is observable and excluded from the scoped SSE/AVX result. Native relevance beyond the mapped path is unproved. |
| Retail safety / real spatial equivalence | NOT TESTED | No game, SFSE, target invocation or real native operand/verdict pair. |

## What actually ran

MSVC **19.51.36256.0**, MASM/link **14.51.36256.0**, installed Windows SDK,
CPython **3.14.3**, Git **2.53.0.windows.1**. Exact executable/source/setup hashes
are in `native-11/build.json`; schema/source/evaluator/output hashes are in
`decode.json` and the local package manifest. The installed game hash and
P16 instruction facts were freshly checked without executing game code.

The fixture installs one-byte traps only into its own authored terminal
instructions. A process-local VEH alters only exception-context RIP, selecting
an authored equivalent leaf continuation. The callback deliberately clobbers
volatile GPRs, SIMD lanes, AVX upper halves, x87 stack and MXCSR. Exception
continuation restores the tested native-relevant state, including branch flags;
the original displaced instruction then executes before the original next
instruction. This exercises a different mechanism from historical guarded CALL
wrappers. It does not modify the rejected 0.8.0 candidate.

Native geometry capture uses fixed preallocated slots, immediate guarded reads,
cooperative leases and immutable owned copies. The finite decision fixture uses
declared fixed quads, per-use query resolutions, scalar comparisons and actual
terminal branches. **Its point arrays test complete ownership and frozen-evaluator
plumbing; it does not construct those quads by executing native strip normalization
or rotation.** Its bounded edge arithmetic also is not the exact native distance
transcription. Inputs stay away from discriminating rounding boundaries. These
choices qualify provenance and representative branch plumbing, not independent
algorithm agreement. Synthetic source IDs and token-bearing closure words are
fixture ancestry, not proposed writes to real engine objects.

There are **64 persisted frames: 46 COMPLETE, 17 INCOMPLETE and one NOT_EVALUATED**
across five thread IDs. All complete point bytes and every full 64-byte Use match
independently authored expected inputs. All 46 replay Booleans and expected
diagnostic branches agree using unchanged evaluator SHA256
`500de4a2304e02fda1566a996ce58a865de5adc9625d34eb61569548916294cb`.
Repeated case-one frames deliberately exhaust the pool; they add stress repetitions,
not independent scientific configurations. Ten authored cases cover broadphase,
zero/one, containment, vertex, edge, all-strips rejection, large array, later-strip
acceptance and expired source storage. No natural occurrence is asserted.

Invalid reasons are count capacity (1), failed read (1), uncertified/busy source
(2), changing consumed query (1), ancestry (3), STOP (2, including NOT_EVALUATED),
interruption (1), use capacity (1), missing verdict/unwind (2), versioned mutation
(1) and lifecycle violations (3). A further pool admission is refused and counted
with sticky overflow. This is a deliberately failed instrumentation stress case,
correctly detected; it is not a lossless-run PASS. No incomplete group is replayed.

Eight independent decoder controls reject truncated tail, missing group suffix,
partial geometry, duplicate token, missing actual-use record, reordered use,
corrupted later-use provenance and conflicting terminal. They operate on owned
derivatives, leaving original `geometry.bin` unchanged. The 12 frozen spatial
unit tests were also rerun and passed; they remain synthetic controls.

## Cost, failure history and interpretation

In `native-11`, 1,000 parallel state probes took **1,446,600 ns aggregate wall
time**, including fixture setup/assertions. This is not a per-trap latency or
retail pause bound. Mean capture-group costs over 1,000 artificial iterations
were **34 ns / 27 ns / 2,927 ns** for 0 / 2 / 8,192 points. An allocating copy
alternative measured **2,776 ns** for 8,192 points. Allocation was not faster or
slower reliably at this sample size; preallocation was selected for bounded
ownership and failure behavior, not a speed claim. These are warm synthetic
throughput observations, without tail-latency, cold-page or retail contention
coverage. Copy cost scales with supplied bytes; many real per-use exceptions
could be consequential. Borrowing a pointer for worker copying cannot qualify
lifetime and was rejected without benchmarking a scientifically invalid route.

Retain local attempts `native`, `native-02` through `native-11`: the initial
assembler failed scoped-label handling; `native-02/03` exposed full-x87 pointer
loss; `native-04/05` separated that FAIL from mapped-state coverage; `native-06`
failed a MASM alignment declaration. Later rework added genuine branch operands,
identity/lifecycle checks, complete-use byte validation and STOP/unwind controls.
An early decoder assumed MXCSR status flags must be zero; it was corrected to
require the qualified control mode while retaining sampled sticky status bits.
Those bits do not change the fixture's masked, finite arithmetic decisions.
Logs and generated assembly/binaries remain local. Source snapshots are retained
from `native-09` onward; earlier runs retain source hashes, not full source copies.

The scoped PASS is an engineering result, not approval to integrate or publish.
Full x87, retail dispatch/exception compatibility, original stack walking/unwind,
all-thread quiescence, native coherent geometry ownership, real per-use capture,
continuous draining/durable flushing and native numeric coverage remain separate.
No claim of persistence, remote-source completeness, resource generation or
safe mod integration follows. See the [scientific decision](decision.md).
