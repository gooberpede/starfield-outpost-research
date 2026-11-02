# D5AI bounded population-storage lifetime witness

Status: the bounded design below is implemented and independently challenged in
the final native candidate and offline controls. Exact package acceptance is
recorded in the [review](d5ai-review.md) and [decision](d5ai-readiness-decision.md).
No retail or Stage B action is authorized. This retained design record is not a
claim of observed retail continuity or physical outer-object deallocation.

The controlling counterexample is map erasure with an externally retained
collection versus map erasure with its final owner released. A complete consumer
scan proves the same consumer unavailability in both cases. The final instrument
must additionally discriminate the previous population's storage history without
post-retirement traversal. Partial collection survival must remain distinct from
survival of the complete population.

The implemented bounded alternative starts from a qualified full snapshot, naming
the source allocation, holder and every constituent collection. A separate,
versioned, loss-accounted journal records qualified native lifetime-ending or
mutation boundaries. The [native ending proof](d5ai-population-ending-proof.md)
and [journal schema](d5ai-lifetime-schema.md) provide typed coverage and receiver
semantics; function names alone do not establish final destruction.
An unbroken journal with proven ending coverage can support continuity of an
already-observed content-vector lifetime. An observed ending invalidates that
old content continuity even if its address is reused. Missing history, loss,
overlap or unsupported mutation
must refuse continuity. A new allocation at the same pointer cannot restore it.

Consumer availability remains a separate result. No global physical absence is
claimed. No event or current pointer is a substitute for a qualified baseline
identity and complete intervening coverage. Empty populations require an explicit
case rather than vacuous collection-survival equality.

## Authorized offline experiment boundary

Allowed actions: read repository and retained native evidence; export targeted
native analysis from verified disposable Ghidra copies; build authored candidate
code; execute owned disposable fixture hosts; read their files; run independent
readers and adverse controls. Existing source/analysis originals are read-only.

Inputs: pinned executable windows and prior ownership evidence, authored fixture
objects and native stubs, qualified baseline geometry, exact candidate DLL and
reader sources. Outputs: local journal/raw receipts, build/source hashes,
machine-checkable classification controls and reviewed documentation. Raw native
evidence and binaries remain ignored and local.

Risks: incorrect lifetime hooks, unsafe copied reads, incomplete ending coverage,
ABA, queue or disk loss, owned-host crash and misleading apparent continuity.
Containment uses disposable hosts and copied analysis projects only. No game
launch, injection, deployment, live attachment, protected-save mutation or source
project alteration follows from this design.

STOP conditions: unexpected action outside the owned-host boundary, unexplained
input changes, caller-available space below 40,000,000,000 bytes on C: or D:,
unexpected protected-input change or evidence corruption. Preserve failed
receipts and refuse qualification. Expected adverse-host exits are separately
classified; evidence completeness and process survival are separate outcomes.

Cleanup: allow the declared owned host to finalize its worker and exit; retain
all receipts and failures. Do not terminate unrelated processes, delete raw
evidence, restore protected saves or alter game/profile configuration.

The [component qualification](d5ai-recorder-qualification.md) records actual
final-recorder controls for map-present storage,
map-erased external survival, final release, partial survival, pointer reuse and
lost history; strict producer/worker/reader/ACK/STOP correspondence; and independent
review of native coverage and both positive and negative classifications.
