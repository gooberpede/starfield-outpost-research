# Worked native paths and bounded operand checks

[Native derivation](native.md), [remote lifecycle](lifecycle.md).
These are STATIC worked control/dataflow traces, with deterministic scalar
checks. They are not a game emulator, native replay, controlled live transition
or independent measurement. Hypothetical operands below are explicitly chosen;
actual saved examples live separately in saves.md. Assume valid ordinary forms,
finite positive C/w, sufficient source stock, no concurrent mutation and normal
source/receiver capability. Floats round to binary32 at each native operation.

| Case | Concrete path and outcome |
|---|---|
| Fitting transfer | Source stock 10, C75/W70, w.5. `140f84c40` admits; `140f84fc0` floor-fit 10 prepares quantity 10; source458 removes 10, receiver4d0 adds 10. Source becomes 0, receiver mass 75. The item visitor's return1 only continues. |
| Partial and full | Source 10, C75/W74, w.5 gives k2; descriptor2 removes/adds 2 and leaves 8 upstream when no other receiver. At W75, F0<w: filter rejects, no descriptor, stock 10 remains source. At W74.75, F.25<w also rejects, although W<C. Incompatible item rejects before quantity planning even with W0. |
| Fork | Cached vector[self,A,B], source10, both compatible, each C75: B W74 fits2, then A W73 fits4, remainder4 stays source. Reverse vector order matters; swapping vector operands changes allocation. This is not a first-created-edge policy or fairness proof. |
| Multi-hop | Directed source->A->B, ordinary stores, cache[self,A,B]. If B admits, original source can remove directly into B within this same mover call. A need not receive and forward a batch. No receiver-recursive mover call is needed. |
| Qualified link-add flush | Add A->B with B an ordinary eligible store: after successful validation/insertion and `140f7d0b0(B)`, caller seeds A and collects its upstream container sources through `140f8a020`. Each resolved selected source gets its own downstream redistribution invocation. If B is a builder/fuel consumer failing that predicate, insertion can succeed without this flush branch. |
| Merge | A->C and B->C are distinct source calls. Their snapshots/order determine C's space. No synchronization/fair-share policy is inferred from saved adjacency. |
| Cycle | Hypothetical admitted A->B->A: forward vector already contains A when revisited, so no append/repeat expansion. Mover skips self. This establishes finite traversal, not ordinary API permission to create this cycle or indefinite circulation. |
| Production overfill | Producer due3, compatible store C75/W74.5/w.5. `140f7d510` sees W<C and selects this single receiver. `140f7d6a0` requests3, valid generic add can bring W to76. It does not split1 here and2 to another receiver. Next due invocation sees changed state. |
| Full source, remote downstream room | Registered/resolvable unloaded extractor, own W=C, reachable compatible store W<C. Current reason's forward-capacity branch and final receiver selection permit creation at store. No source-buffer removal and no player/3D check in this route. Actual historical residency/power is not measured. |
| Skipped-time due path | I36, remaining5, elapsed50: large branch trunc(50/36)=1, not two phase-preserving cycles. Eligible producer creates one request at selected store, resets remaining/interval. I36/remaining5/elapsed10 likewise gives one, drops overshoot. Builders additionally cap by ingredients. |
| Missing individual producer | Same elapsed50, iterations2, pending0, Workshop resolves but producer does not. Pending becomes2 and handle becomes sentinel; no product added. Ordinary future sentinel recovery is not established. If the Workshop itself fails, even this pending update does not occur. |
| Matched return | Existing matching row pending3. True object-load event, current eligibility true: callback passes3 to production and clears pending. Eligibility false: no creation, pending still cleared. Recipe/capacity and actual insertion remain independent of the bookkeeping clear. |

## Multi-item counterexample to a whole-batch capacity guarantee

The verified cross-item exclusion test is `k*w+(C-W) >= C`, using the unchanged
receiver inventory during planning. Choose C75, W60, and two distinct compatible
item rows each q20/w.5. For each row floor-fit30 and k20; planned mass10 plus
free15 =25, below75, so that receiver is not added to the shared exclusion set.
Both descriptors may be planned before execution, each using the original W60.
Normal removal/addition of both raises mass to80. This is a **STATIC PREDICTION**,
not an observed bug or the demonstrated historical writer of overfull warehouse
stock. The instructions contradict a stronger universal reservation model, so
the report retains per-item fitting and explicitly limits whole-batch guarantees.

`verify.py` checks fixed expected scalar results using binary32 operations and
independent integer/decimal expectations, and checks decisive instruction/source
locators. Passing those checks verifies the accounting and evidence bindings;
it does not turn these worked traces into observed runtime output. No unsupported
universal atomicity, timing, absence or long-run throughput claim is substituted.
