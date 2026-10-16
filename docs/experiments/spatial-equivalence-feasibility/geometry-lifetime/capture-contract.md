# Conditional minimal evidence and correlation contract

[G/O verdict](report.md), [native operands](operands.md), [lifetime](ownership.md).
Research schema `sor-native-region-design/1` is **proposed, not implemented**.
No new decoder, observer, target patch or event output is authorized by this file.

## Records and owned data

Every record includes session ID, measured executable hash/runtime base, schema
version, monotonic thread-local sequence, thread ID plus thread-lifetime token,
updater invocation, callback invocation, nesting depth and parent invocation.
Wall time is diagnostic and never a join key. Use a per-thread stack of active
frames plus explicit helper call ancestry, not one process-global pending slot.

| Record | Minimal fields / exact representation |
|---|---|
| SESSION | Build and tool/evaluator hashes; native RVA/site/instruction guards; numeric-domain policy; instrumentation version; storage capacities; owner protection evidence revision. No semantic claim from a hash alone |
| CALLBACK_BEGIN | Parent updater token; natural return site; native closure address, descriptor/index/domain; source slot key/address/value; ProcGen pointer and qualified lifetime epoch. All pointers u64 and invocation-local |
| REGION_BEGIN | Unique token within callback; resource slot ordinal/key; resolved IRES pointer and optional independently read FormID; collection pointer; region ordinal/address; observed count/capacity/pointer; read statuses. Broadphase source bound words and count source must be bound to actual uses |
| GEOMETRY | For passing count>1, original count and total byte length; complete ordered count*16 owned XYZ-width bytes; chunk indices/offsets if transport fragments, content digest and final suffix. Count0/1 or broadphase reject records unused geometry explicitly. No borrowed-pointer worker reads |
| USE | Region token; strip ordinal, stage, helper call ordinal/return-site token; consumed component mask; exact reduced coordinate words, radius and upper where used; branch-specific native source/derived words and read status as in operand map. MXCSR control/status. Native broadphase sum captured separately from original radius inputs |
| PATH | Executed broadphase/count branch; containment completion or first-positive cross; called vertex result; called edge comparison and optional segment subbranch. Unvisited paths explicitly absent, never synthesized as false |
| REGION_END | Same token and pointer ancestry, actual terminal RVA and ACCEPT/REJECT; terminal native register witness; reason when witnessed, otherwise UNKNOWN reason. Exactly one terminal; subsequent integrity suffix closes owned group |
| CALLBACK_END / ABORT / STOP / LOSS | Normal callback exit with active-frame census, exception/unwind/ancestry mismatch or read/capacity failure, last admitted token and drain state. Sticky lost-record count plus group identities where available. Durable suffix/flush status separate from callback completion |

Nothing in this schema implies writing an epoch/token into the engine. Observer
side association would need separately qualified storage and native owner epoch
evidence. Region pointers reused in later callbacks remain different evaluations.
Count/capacity bounds and allocation arithmetic are checked before reads; refusal
is integrity evidence, not a gameplay outcome. Counts may exceed finite observer
capacity without becoming false native regions. Owned capacity is an engineering
integrity limit, not a scientific event/time quota.

## Native result versus evidence result

`native_decision` is ACCEPT, REJECT, NOT_EVALUATED or UNKNOWN. ACCEPT/REJECT require
an observed matching terminal edge before RBX changes. NOT_EVALUATED requires
positive traversal evidence that the candidate/path was skipped, for example
short-circuit after an earlier acceptance. If a full source/collection census was
not captured, do not invent identities/counts for all unseen later regions.

`evidence_status` is COMPLETE or INCOMPLETE/UNKNOWN independently. A native ACCEPT
with lost geometry remains ACCEPT with incomplete comparison evidence. An entry
with no terminal is UNKNOWN, not REJECT. A pre-admission STOP may produce a
NOT_EVALUATED diagnostic, but cannot assert the native routine did not later run.
Per-branch NOT_EVALUATED is separate from the whole region's decision.

Normal callback exit with an open region, duplicate/mismatched/late terminal,
unresolved recursive same-pointer ancestry, cross-thread terminal, unexplained ordinal,
unwind, STOP mid-copy and transport truncation all forbid full replay. Keep
flushed complete groups and original failures. Nesting pushes/pops frames without
overwriting the parent; same-pointer recursion is admissible only with separately
identified complete parent/child frames. Concurrent threads have separate identities.
Helper observations require a recognized active parent and native call/return
site; unrelated global helper calls cannot attach by timestamp or pointer alone.

STOP closes new observation admission, allows already admitted native calls to
finish under a qualified bounded retirement protocol, drains owned groups, then
removes interception only after proven quiescence. Missing quiescence is a safety
failure, not permission to remove a site while executing. Synthetic cooperative
STOP does not establish this protocol for retail or arbitrary unwind.

## Independent replay admission

Before looking at native verdicts, freeze evaluator hash and numeric rules.
An admitted pair requires all of the following together:

1. Qualified build/sites and owner lifetime/payload protection for its entire
   snapshot; successful checked source reads and complete owned bytes, without
   truncation, overflow or unexplained mutation. Matching headers cannot certify G.
2. Exact source-to-consumer provenance for branch-required bounds/count/scalars,
   and every executed re-resolution. Per-use equality/stability rules in the
   operand map must hold. Missing unexecuted vertices/strips need no fabricated
   reads, but multi-point full geometry is still required by this experiment.
3. Unique entry-to-terminal association, complete native path record and durable
   group suffix, no missing/lost/aborted ancestors, and known numeric mode/domain.
4. Independent invocation of unchanged frozen `evaluate_region`, with source
   geometry and original sufficient operands. Native helper/quad values serve
   diagnostics rather than fitting the full evaluator. A reduced helper comparison
   is labelled separately and cannot satisfy full-region coverage.

Native and replay true/false are compared only after admission. Preserve genuine
disagreements with exact original bits. Report admitted unique configurations,
accepted/rejected branches, repeats, short-circuit omissions and exclusions by
reason. Zero admitted pairs for a branch means NOT TESTED. Partial evidence must
not bias reporting toward easy accepted candidates: rejected regions and
all-strips-exhausted terminals are explicit required coverage categories.

## Separate prerequisites before any live observer

Current candidate RVAs in the operand map are source locators only. Separate
review must establish original byte guards and instruction liveness at each
chosen site, safe invocation-owned storage without reserved fixture registers,
exact GP/flags/SIMD/x87/LastError preservation, unwind/exception-chain behavior,
owner and alias protection, full-copy capacity/cold-page costs under +40,
nonblocking capture/transport, admission-loss visibility, quiescent STOP and
retail compatibility. The accepted x87 correction's R15-owned image does not
establish a retail register reservation or continuation storage contract.

A future operator card would state protected save inputs, interventions and
timing effects, finite scientific scenario/coverage, build/module admission,
40,000,000,000-byte free-space guards on C: and D:, evidence flushing, recovery
and target exit policy. Healthy captures do not end solely for event count,
elapsed time or delayed polling. None of those operator actions occurred here.
