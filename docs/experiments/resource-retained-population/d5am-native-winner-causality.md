# D5AM native winner causality

2026-11-03, Australia/Sydney. Parent questions D5AM-Q2/Q3 and GC-10 remain
open pending completion and independent review of the full D5AM contract.

**The compiled path permits two different reversals of an earlier visited
observation: delay before writer registration, and overtaking after registration.**
Existing retail timestamps do not discriminate these reversals. This is a
revalidated static constraint, not a new measurement of their normal frequency.
All addresses below are preferred static VAs for Starfield 1.16.244.0, image
base `0x140000000`; member offsets are bytes.

| Element | Supported scope |
|---|---|
| Question | Which conditions can change which eligible request first constructs the target source? |
| Answer | Ingress, prerequisite completion, dispatch route, queue service and progress can change the arriving contenders. The shared visited test reserves no writer position. Pending writers compete through a non-ticket CAS; readers can enter while writers are pending. |
| Confidence | PROVEN / STATIC for the inspected predicates; historical placement of B2's delay remains UNKNOWN. |
| Primary evidence | D5AE source ledger and retained native exports; D5AF lock/provider exports and native controls; observer source inspection. Exact local pins are below. |
| Exclusions | No measured OS fairness, retail probability, usual request identity, cold-first certificate, or cross-build address transfer. |

## Conditional graph and discriminating counterfactuals

| Mechanism | Native condition and boundary | Positive and contrary continuations | Required measurement |
|---|---|---|---|
| Geographic registration head start | `0x14079d080 → 0x1407af970` enumerates rectangle X ascending/Y descending; `0x1407b4bb0` registers neighboring layer work. Warm keys merge. | Earlier enumeration can make work available earlier. A prerequisite-bearing earlier key can remain pending while a later ready key executes. Enumeration is not global execution order. | Original request, producer/context, task lifetime/key, registration and dependency state. |
| Dependency readiness | Count `node+0x90`, state `+0xa8`, rank `+0x80` have separate roles. Commit `0x1427e70e0`, dependency removal `0x1427e5e80` and evaluator `0x1427e6830` distinguish ready result 2 from results 4/5 and deferred completion. | Last dependency can enable dispatch; a decrement alone need not publish runnable work. | Dependency transition, evaluator result and later publication, joined by task allocation. |
| Ready-tree order | `0x1427e4950` assigns serial `node+0x88`; bound helpers order unsigned rank then serial. | The named scan can consider lower rank/serial first. Immediate rank-zero registration through `0x1427e6a00 → 0x1427e56d0` can bypass that scan. | Effective rank/serial, actual route and dispatch result. |
| Worker locality | `0x1427eb6b0` handles matching TLS import/publication; `0x1428d3960` has owner-back, peer-front CAS and external queue routes. | Identical publication order can produce different claims as pool/context availability changes. Direct/inline execution is a separate route. | Task/callback identity, pool/context, queue endpoint, successful claim and callback entry. |
| Provider eligibility | Density `0x14076c560 → 0x1407a1940` can reuse an aggregate; layer `0x1407b5160` has its own admitted call. Provider selects actual source and tests its token. | A warm aggregate suppresses provider invocation; a visited token suppresses this construction path. Source publication alone does not prove an eligible consumer. | Provider entry plus caller/task join, selection, visited result, complete lifetime and reuse history. |
| Pre-registration delay | Shared release at `0x14079fc85`, visited observer at `0x14079fca3`, exclusive call at `0x14079fcb3`. | A stamps first but returns from its observer later; B registers/acquires first. No lock overtaking is needed. | Callback tail and exclusive-call/registration boundaries, retaining observer cost. |
| Writer overtaking | Pending increment `0x1422cc410`; predicate `state & 0xffc00fff`; ownership CAS `0x1422cc42b`; successful owner publication `0x1422cc48f`. | A registers first but is delayed before a successful CAS; B registers later and wins. Pending bits `0x003ff000` do not form a ticket. | Exact XADD operand and successful CAS path, lock identity, TID and native interval constraints. A later callback QPC alone cannot timestamp the atomic transition. |
| Readers and foreign sources | Reader XADD `0x1422cc366` tests exclusive bits `0xffc00000`; provider shared release `0x14079fc85`; exclusive release `0x1402c45a0`. | Pending writers alone do not bar new readers. An unrelated source on the same ProcGen lock can occupy it between target observations. | All users of the watched owner lock, including users with no provider TLS; acquisition/release state and completeness. |
| Recursion | `0x1422cc3ed` compares native owner TID; same-owner branch increments depth at `0x1422cc3f2`. | Same-thread recursion bypasses the nonowner loop. Two distinct target threads cannot both be that same native owner. | Native owner TID and depth, not observer parent ID. |
| Protected authority | `0x14079fccb` lookup, holder insertion `0x14079fdf9`, generator `0x14079ff18`, visited reserve/store, release `0x14079ffa5`. | First constructing miss owns generation; a waiter that already passed visited can later hit. Raster delay inside this interval cannot let a same-owner waiter construct first. | Existing lookup/generation/store events plus stronger admission chain. |

The native scheduler contains no geographic-coordinate or mask-priority operand
in the inspected dispatch/claim path. This bounded statement does not exclude
OS progress differences, generic rank updates or another admitted producer.
See [D5AE scheduler](d5ae-scheduler-causality.md) and
[readiness](d5ae-eligibility-readiness-map.md) for the exact receiver and caller
qualifications. Those earlier findings are reused with provenance, not claimed
as D5AM discoveries.

The fresh D5AM scheduler replay in
`.local-work/d5am/scheduler01/qualification.json` executes the pinned owned
D5W native queue method and passes its twelve original dispatcher/claim,
owner/peer and activation-batch cases. Allocator/TLS/empty-context setup and
callback tokens are explicit fixture substitutions. This corroborates the
bounded compiled queue constraints; it does not measure retail worker timing.

## Observation-equivalence witness

Keep B2's recorded visited order A then B, B's protected miss/sample/store, and
A's later hit fixed. In history H1, A is delayed inside the visited callback
before writer registration; B acquires and constructs before A registers. In
history H2, A registers first, then loses progress before its successful CAS;
B registers later and wins the CAS. Both obey the inspected native predicates
and produce the same recorded events. The schema has no event whose value
differs between H1 and H2. Static semantics establish possibility; they do not
identify which historical continuation occurred. Re-decoding the same fields
cannot recover the missing discriminator.

There is also no unique inference from equal complete geometry to equal request
identity, eligibility order or mask. D5AK/D5AL geometry equality remains useful
output evidence within its recorded context; it is not a scheduler observation.

The fresh [D5AM chronology](d5am-retail-chronology.md) supplies a concrete
request-identity counterexample: B2 constructs from `[5,0]`, A0 from `[8,3]`,
A1 from `[-1,11]` and B0 from `[0,0]`; every recorded winning ordinary sample is
`0x3`. The complete A0/A1/B0 normalized populations agree. These are four
constructions across three historical sessions with their original route and
instrumentation differences. They do not establish a normal winner distribution
or prove that all requests with sample `0x3` always generate equal geometry.

## Measurement influence and feasible continuation

A pending-registration probe necessarily executes between registration and a
later CAS; it can permit the overtaking it observes. A successful-path probe
holds the lock longer before later protected work. A reader probe can extend a
reader cohort. Even a native fast gate on unrelated locks costs instructions.
Lossless recording therefore cannot establish negligible influence.

The [new native qualification](d5am-native-qualification.md) positively exercises
this influence: an admitted post-Pending callback hold lets a later writer win
the original ownership CAS. Its disjoint callback brackets distinguish that
actual controlled overtaking from pre-registration delay. This new private
measurement does not identify which of the two historical B2 continuations
occurred or close the normal-retail consistency question.

A feasible bounded design uses a preallocated owner-lock registry, populated
from positive owner lifecycle evidence, and native filtering before a C++
callback. It must preserve registers, flags and displaced atomic semantics;
capture exact old packed operands rather than rereading a racing lock later;
record unscoped same-lock users; version owner lifetimes against ABA; and refuse
complete history when registration begins with unknown holders. Provider TLS
alone is insufficient. These requirements are engineering work, not proof that
such an extension is impossible. Until qualified, the full instrument remains
INCOMPLETE and has no deployment authority.

## Primary pins checked during D5AM

Read-only file hashing revalidated the following retained exports; no Ghidra
project was opened or modified for this audit:

| Local input | SHA-256 | Applied understanding |
|---|---|---|
| `.local-work/d5af/prelock-export01/native.tsv` | `bad793664b90b987bd5dc4d91fb70936a2d9590029b17dc2eb7e7d1e2c807b47` | Direct instruction review of reader, exclusive helper and release establishes pending-bit exclusion, success path and wake semantics. |
| `.local-work/d5q/export01/native.tsv` | `60cc949338e9e0211b87f56c376e1a057d8b7af2da6f9e34a4ae3e84339f8fcd` | Provider interval review keeps visited release, observer work, exclusive call and protected lookup separate. |
| `.local-work/d5ae/export02/native.tsv` | `e1f4ccf559a01411bf05c11a793bf2e1a90220e7c580bb455f1787acd6275599` | Dependency/commit source for the readiness graph. |
| `.local-work/d5ae/export03/native.tsv` | `25d6455a678dc953eec2a0d1f521296777e467f1613c7b600c23b7920c6d5b05` | Constructor and ready insertion review distinguishes count, rank, state and serial. |
| `.local-work/d5ae/export05/native.tsv` | `5da3f0fd1442e5f2a128f48421117826397cfc1c1f76f146059952902b900483` | Retained dispatch source pin; detailed semantics inherited from D5AE, not a fresh full-function export. |
| `.local-work/d5r/export01/native.tsv` | `0ce62129bd4e6057318e62a3e2fbb588000ed160d51ab9373206085aabc4e785` | Retained queue source pin; D5AE's native queue controls remain separately scoped from retail scheduling. |

The precise earlier function windows and owned native-control receipt pins are
in [D5AE sources](d5ae-sources.csv), [D5AF sources](d5af-sources.csv) and
[D5AF methods](d5af-methods-and-tests.md). Hash equality authenticates retained
bytes; it does not independently verify every inherited interpretation.
