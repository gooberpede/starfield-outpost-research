# Ranked event-associated acquisition design

SOR-EXP-0024; DESIGN ONLY, REVIEW-REQUIRED. No hook implementation, build,
deployment or live execution authorized. All static VA/RVAs refer exclusively to
the [pinned retail module](../event-associated-position-oracle-and-build-mode.md).
These are observed internals, not supported mod integration points.

## Selection

| Rank | Native event / expected gain | Reachability and acquisition risk |
|---|---|---|
| 1 | Natural `140f4ab80` entry and return: independently produced12-byte center, actual reference and caller; catches zero and nonzero compensation branches. | Seven traced direct code callers include border/descriptor/clamp as well as the gated ProcGen publisher. More opportunities than the stale shared tuple, but actual Save25/26 event frequency is not proven. One scoped entry bridge and one common-exit bridge, original instructions replayed; no return-address replacement. |
| 2 | `140ad0b90` post-quantization at140ad0d3b: center, translation, body/resolution, floor and native hierarchy on one invocation. | Highest grid information gain; natural terrain/site candidate path may not run when opening an existing workshop. Stack context requires a qualified bridge or narrowly controlled debugger capture. Zero hits are NOT_OBSERVED. |
| 3 | `1421b2570` post-center/post-radius/publication plus reset/disable trace: explains stored tuple event history. | Exact producer identity recoverable, but publication is gated by selected-object/list predicates; cannot guarantee a center oracle for every build-open episode. More sites and ownership/state data; use for forensic discrimination. |
| 4 | `140f4a140` descriptor /140f4ac50 natural predicate and1421bb860 clamp: radius/frame/actual geometric consumption. | Useful local-boundary cross-check; not grid equivalence or complete build permission. Descriptor construction itself is not a safe worker-thread query. Add only if the separately approved experiment needs radius or bounds authority. |

Rank1 is the first center instrument to implement after review; rank2 is a
separate optional adapter for a naturally occurring event, not a requirement to
force terrain generation. A rank1 record whose return-address is140ad0c3b can
share a scope/TID with rank2; it cannot merge unrelated invocations by matching
XYZ or nearby timestamps. No numerical center equality is used to select identity.

## Candidate1: actual center helper, RVA00f4ab80

Observed ABI at entry: RCX=reference, RDX=caller-owned writable12-byte XYZ
output, [RSP]=return-address/caller, no radius result. The helper copies
reference+8c/+94, conditionally resolves ordinary activator/Workshop keyword and
extra-bc, then adds its compensation. Output is caller-owned scratch, often
stack storage; it expires/reuses after the caller continues.

The first complete instructions are VA140f4ab80 (5-byte RBX save), ab85 (PUSH
RDI), ab86 (4-byte SUB RSP,30), continuationab8a. A future5-byte near-jump
entry bridge can replay the complete5-byte first instruction and resumeab85,
provided a nearby bridge allocation and exact raw-byte check succeed. No generic
stolen-instruction length guess. Every normal branch joins epilogueac44:
restore RBX (5 bytes), ADD RSP,30 (4), POP RDI, RET at ac4e. A separate5-byte
near-jump at **140f4ac44 / RVA00f4ac44** can record then replay the restore and
resumeac49. RDI then holds the output pointer, RBX the reference, and the
original return-address is at current RSP+38. Entry/exit scope records must be
paired by TID and TLS nesting, with the original caller/stack token checked.
This avoids changing the engine return-address or relying on a C++ inferred
return type. Windows unwind behavior through both bridges still needs fixture
qualification; no working bridge is claimed here.

Record before continuing the natural engine thread:

- Module hash/base, exact site/preimage bytes, event sequence, QPC/time, TID,
  scope/parent-scope, caller RVA, original stack pointer, entry/output addresses.
- Entry reference pointer, runtime FormID at+28, base pointer/type at+98,
  parent/frame handles with their domains, reference12-byte XYZ and raw evidence
  for resolved concrete extra-bc identity and identifier+98/compensation+60.
- Exit output12 raw bytes and read status, reference/output/caller scope match,
  branch qualification, relevant parent/world/selected-frame evidence and MXCSR.
- Any unreadable field, unsupported extra/identity/frame, reentrancy/unmatched
  exit or dropped event explicitly; no replacement zeros or inferred ID.

Association rule: join actual reference to ordinary base002C60E9 and independently
captured concrete Workshop identifier+98 (002=`f1517de43e171745`,
003=`0efca066ee4c7b9b`), retaining raw bytes and candidate alternatives. Prior
FormIDs FF01AB50/FF01AB8F are supporting session-local clues, not stable saved
tokens. Acquire the already-established guarded census/extra mapping on its
qualified worker; copy safe identity fields on the invoking thread while the
reference is live. Do not traverse arbitrary extra lists or call engine lookup
APIs from a hook just to fill a field. If the live-time raw association cannot
be qualified, the output is UNASSOCIATED even if it equals a frozen prediction.
If cached association is used, record its epoch, pointer/header rechecks and
limits; a pointer-only join across loading is insufficient.

An entry/normal exit pair proves a fresh computation for that input, including
the zero-vector bypass. It independently tests saved durable center **only**
after parent/body/frame equivalence is established. It does not produce radius,
quantization, effective permissions or continuous geographical coordinates.
Missing exit after an exception is PARTIAL, not a bad center. Repeated exact
values are repeated events, not new independent samples.

## Candidate2: native grid, RVA00ad0d3b

Keep the existing [typed callback contract](../engine-oracle/oracle-contract.md)
and [raw format](../../../debugger/engine-oracle/contract.py). Natural call chain:
14077e350→140ad92e0→140ad08d0→140b1e190→140ad8ec0→140ad0b90. Site/overlay
filtering and reference enumeration happen on the game's own thread.

At **140ad0d3b**, immediately after14096f5c0: RBX=current reference;
RSI=six-pointer context; RBP-49=translatedXYZ12bytes; RBP-9=result hierarchy
44bytes; RBP+6f=floorXY two signed ints. Copy **values**, not only stack pointers:
context+08 candidate hierarchy, +10 landscape** (body+54/resolution+50),
+18 source hierarchy, +20 translationXYZ, +28 bounds; retain result boolean
pointer+00. Entry/reference/helper scope and native input base must accompany
post-call result. Capture the exact binary32 scale and MXCSR/precondition state
before claiming arbitrary-domain reproduction.

A scoped internal-site bridge can copy these bounded payloads and replay the
verified complete overwritten instructions. Its exact preimage and relocation
plan must be produced from pinned bytes during implementation review; do not
reuse the center helper's patch length. Alternative: reviewed software
breakpoint auto-continue adapter with all-thread handling and copied context.
Both change execution and scheduling; neither is non-invasive. Hardware
breakpoint use ranks below them because the earlier native-save adapter
encountered STATUS_SINGLE_STEP failures/new-thread problems. That history is
specific evidence, not a categorical debugger ban. A debugger option must
demonstrate reliable qualification and a reason its smaller installation scope
outweighs its stop/exception/detach exposure. Existing two-thread sentinel
transport tests do not prove retail reachability or safety.

One qualified callback can supply center *and* grid intermediates independently.
For center comparison capture pre-translation helper output too; translatedXYZ
alone is not an unconditional same-frame center. Native-input replay tests
arithmetic; saved→loaded end-to-end validation additionally requires observed
base/translation/frame reconciliation. Do not call the callback artificially or
broaden gameplay/placement scope to get a hit. Ordinary operator activity and
terrain candidate work are expected opportunities, not guaranteed triggers.

## Candidate3: publication/invalidation forensic trace

Sites: center-return1421b2901 / RVA021b2901 (RBX actual workshop reference,
RSP+50 center); radius-return1421b2935 / RVA021b2935 (XMM0, verify exact
instruction boundary in implementation); store1421b29b1 / RVA021b29b1
(RDI owner,16-byte source loaded at29ac); reset1407a6690 / RVA007a6690;
activation1407a50d0 / RVA007a50d0. Record operation-context/state+630,
selected object and derived-list count/eligibility, global145f5d8e8 reference,
owner allocation epoch and root chain, tuple before/after, enable argument and
e8/e9/ea. Correlate within one producer scope, not by later snapshot coincidence.
Record descriptor input separately from global-workshop input.

These events discriminate publish→reset→disable retention from a never-entered
publisher, failed gate, root replacement or active missed update. Center-return
already supplies a fresh center even if later invalidated. Publication alone
does not validate all permissions or prove UI-open events invoke that state.
Rank1 is simpler and less gate-dependent for the primary scientific comparison.

## Frame and exact comparison contract

Keep [frozen validation protocol](../engine-oracle/validation-protocol.md),
[inputs](../engine-oracle/inputs.json) and [predictions](../engine-oracle/predictions.json)
byte-identical. Inputs SHA9fe2924ff7bc444714fbab685893b8d8e0572dc2c7aad96cbd06de8aac93ad91;
predictions SHAa8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487.
002 center=`a266f542eb858843efd19241`;003=`0369b243f0b019457220ffc1` in both saves.

Require exact12-byte equality after independent identity, freshness, body and
same-frame qualification. Preserve moved003 rawXYZ differing from its durable
center, unmoved002 and distinct-site controls, closed/inactive negative events,
both observed002 outcomes and all mismatches. Unknown frame is UNASSESSED;
unreadable identity is PARTIAL; zero-hit is NOT_OBSERVED. No epsilon or fitted
offset. Float32 translatedXYZ/scale/floor order and native floor integers/grid
cell must match exactly for resolution256/block12. Compare hierarchy tag and
coarse/sub/fine integers, flattening coarse*192+sub*12+fine; preserve opaque
asset handles without invented expectations. Residual is derived from captured
intermediates, not independently observed unless a separate native residual
output is acquired. Different final frames must be reconciled explicitly.

## Implementation gates and future experiment boundaries

1. Review this design, then authorize a separate offline instrumentation brief.
   Pin preimage bytes/complete instructions, original bridge source, version,
   module hash and exact raw schema. No unapproved assembler/detour dependency.
2. Build an original disposable fixture with both branches, nested/reentrant
   and concurrent invocations, exceptions/unwinding, missing identity, stale
   associations, zero hits, saturated transport, worker I/O errors and disarm.
   Verify GPR/flags/vector/MXCSR/stack/home-space preservation and exact outputs
   against an uninstrumented fixture. Validate instruction replay and active
   bridge lifetime. Preserve every failed qualification as well as repairs.
3. Install only at a separately authorized quiescent phase, never patch live
   bytes while uncoordinated threads may execute them. Fixed payload copying on
   invoking threads; no engine calls, heap allocation, blocking disk I/O or locks
   there. Worker flushes complete raw records plus journal/hash/health evidence.
   Preallocate transport based on measured rate; no small scientific quota.
   Explicit lost-record counters invalidate affected completeness claims.
4. A new reviewed live card must name protected Save25/26 copies, exact permitted
   natural actions, finite experiment phase boundaries, hooks/sites, start/stop,
   module verification, source-save protection, evidence flush and exit policy.
   Keep40,000,000,000-byte free-space guard on C: and D:. Isolated unknown or
   unreadable scientific observations continue; actual corrupt scope/transport,
   failed byte verification, storage integrity or machine safety stops capture.
5. Disarm stops recording cooperatively. Do not unload/restore code until all
   bridge invocations have drained under a qualified protocol; alternatively
   retain inert bridges and buffers until normal process exit. Record crashes
   and debugger effects. Complete flushed evidence may remain scientifically
   usable after an authorized crash-tolerant capture; no pre-evidence crash pass.

The successful broad observer informs guarded reads, association and raw-journal
preservation; it cannot alone turn a shared retained value into an event oracle.
Maintainer-authored `gooberpede/starfield-reference-handles`, local revision
`6a77579a184c64e0c080c8f3b7883c34bd17e24b`, was consulted read-only under
SOR-P-0002: `plugin/reference-observer/README.md`, `src/snapshot.h`,
`src/event_buffer.h`, `src/menu_return.h`, and `debugger/native/README.md`.
Exact hashes in local source receipt. Adopt lifetime/scope/health separation
conceptually; do not import its fixed event quotas, addresses, claim coverage
or embedded third-party dependencies. No sibling code was copied. Existing
SFSE-interface permission SOR-P-0001 does not approve a new hook dependency.
