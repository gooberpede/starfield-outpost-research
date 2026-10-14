# Placement preview and spinner — static branch findings

SOR-FN-0057 / SOR-ST-0027, SOR-EV-0032. STATIC/OBSERVED-INTERNAL, authored
interpretation REVIEW-REQUIRED. [Pinned build/address domain](../event-associated-position-oracle-and-build-mode.md).
Evidence: event-oracle-06..13 existing-analysis exports. No failed gameplay
episode, UI asset extraction, new instrumentation or live observation here.

## UI properties are a separate channel

`14158e280` (RVA 0158e280) constructs **WorkshopStateDataModel**, singleton
`1461eefd0`; destructor 14158e410 releases it. At model+4e0 it constructs
TUIDataToFlash<WorkshopStateData> through `14158f230`. The latter explicitly
binds the following names and typed value containers. Payload offsets refer to
the embedded object as constructed, not a promise that the displayed Flash
value always points into that original storage: the service can select/copy
shuttled containers through virtual+58.

| Property | Value payload in constructed model | Meaning supported here |
|---|---|---|
| uCurrentState | +540 uint32 | State value transported to UI; numeric enum names not all recovered. |
| uSecondaryMode | +560 uint32 | Separate mode. |
| bShowSpinner | +580 byte | Explicit spinner request/value, not radius. |
| bFlycamActive | +5a0 byte | Separate overhead-camera UI property. |
| bAutoFoundationMode | +5c0 byte | Separate mode. |
| bBlockInput | +5e0 byte | Separate blocking property; spinner is not itself the entire input predicate. |
| bPrecisePlacementMode | +600 byte | Separate placement property. |

`1421f6420` (RVA 021f6420) takes a boolean in CL and queues a command through
service 145fd9cd0 if the model's event shuttle/model pointer is available.
Command callback 1415902a0→**14158fa50** obtains the selected WorkshopStateData
container via model+500 virtual+58, holds model+4f8 lock, updates spinner
property (selected property-base+58, container at+40) and marks it changed.
This is an **asynchronous request→service execution→UI data** chain. An emitted
request alone does not prove delivery, change notification or a displayed frame.
`14158e570` writes model+6f0 then queues 141590400→14158f570 to update current
state; other property updates likewise have distinct commands. The model's
offset+630 lock belongs to WorkshopInfoData; do not confuse it with the engine
operation-context+630 state byte or ProcGen flags.

## Native initialization, waiting and advance

RTTI/vtable names distinguish WorkshopEngine::StateCreateReferences,
StateWait3D, StateSetupReferences and StateUpdatePlacement from separate
WorkshopUI::StateUpdateNewItemPlacement. Tables/singletons:

- CreateReferences 144d49f58, entry 1421b62c0: obtains a descriptor/selection,
  initializes the reference interface, changes context+630 (5→6, other nonzero→1),
  obtains a reference adapter and dispatches subsequent engine work.
- Wait3D144d4a1d8, entry **1421b5720** is defined instructions/LAB rather than
  an existing Ghidra function. It loads two timer settings145f5cd88/145f5cda8
  into state+8/+c and clears operation-context+622. No function was created.
- Wait3D update slot+130 at 144d4a308→**1421b5970** (RVA 021b5970).
  It subtracts frame delta 145fbf9a8 from a positive state+8 timer; crossing 0
  requests spinner-on via 1421f6420(1). A second timer crossing calls 1421bb4a0.
- That second call constructs/queues WorkshopEngine::CancelEvent only under
  global 145f5de49 and 145f5de48/dispatch conditions. It is not unconditional
  recovery from every wait. No observed timer values or guaranteed deadline.
- Advance requires context+268 interface non-null and virtual+38 returning
  true. If context+622 is clear and a selected reference handle qualifies,
  it resolves the reference, visits its 3D nodes via virtual+560 and 1424181e0,
  builds the context+5c0 readiness collection, then sets +622=1.
- **14241e7f0** (RVA 0241e7f0) checks readiness of that collection: two pointer
  ranges, resource objects at entry+20, high-bit status tests at resource+14,
  nested resource path+20→+30 for the first range, and an additional byte+48
  condition in the second. Null or nonqualifying state returns AL=0. The
  high-bit status categories are not given invented semantic enum names.
- Only AL=true continues reference-map setup and switches context+210 to
  singleton 14597a9e8→**StateSetupReferences** table 144d49038. Waiting continues
  if outer virtual readiness or resource readiness remains false.
- Wait3D exit slot+18 **1421b5750** is defined XOR ECX,ECX then a tail jump to
 1421f6420: requests spinner-off. Re-entering initializes timers/latch again.

This supports a concrete **persistent waiting-state hypothesis**: after the
spinner timer expires, unresolved interface/resource readiness can leave this
state waiting and never reach its spinner-off exit; alternatively an exit/off
request can occur but fail to reach/refresh displayed UI. It does not demonstrate
a deadlock, identify the actual pending resource, prove those globals/timers
have particular values during the user's failure, or prove every spinner source
passes through this state. Refall1421f6420 additionally finds 1421bc020,
1421ba960 and 1421ae7f0 callers; those are retained secondary leads, not silently
claimed exhausted spinner sources. The complete UI render/input event loop is
outside primary graph closure.

## Boundary failure is distinguishable

The effective radius/descriptor and ordinary circle predicate follow
140f38e30→140f4a140→140f4ac50, with separate 1421bb860 clamp. These do not read
the observed ProcGen radius. The traced wait timer/readiness routine does not
test ProcGen+9c. ProcGen itself has an inactive projected-decal consumer and
partial reset. Phase 1's zero-radius snapshots during reportedly functional
build-open intervals refute zero-in-that-buffer as sufficient symptom evidence.
They do not measure the effective getter value or rule out a shared upstream
selection/scene-initialization failure.

| Hypothesis | Most discriminating future observation / falsifier |
|---|---|
| Shared tuple is retained but inactive | Publish/reset/disable sequence and owner epoch; e8=0 consumer skip while independently qualified boundary/preview succeeds supports this. Active consumer with wrong fresh center would challenge it. |
| Wait3D never becomes ready | State+210 remains Wait3D; timer-on event; virtual+38 and 14241e7f0 return snapshots identify false gate and exact resource flags. Exit event while spinner persists falsifies this as sole cause. |
| UI delivery/render lag or lost off event | Pair 1421f6420 request with 14158fa50 execution, selected-container old/new bytes and displayed epoch. Off applied and displayed correctly would challenge it; off requested but not applied separates service failure. |
| Actual geometry rejects placement | Natural 140f4ac50 input descriptor/point/frame and return, effective radius 140f38e30, placement status/error and blocked action in same episode. Positive radius alone does not prove allowed placement. |
| Shared upstream selection fault connects both issues | Same operation/reference/scene epoch shows pending preview plus missed producer gate; independence controls show one recovers while other remains. Temporal proximity or equal centers alone does not establish causation. |
| Incorrect/reused worker pointer | Allocation/destruction/root epochs and in-event owner identity disagree with passive buffer address. Equal brackets alone cannot falsify this. |

A subsequent reviewed failure-capture design should use ordinary good→bad→
exit/re-enter→recovered controls, associate camera mode, selected item, workshop,
resource readiness and UI transport events by context/TID/scopes, and preserve
both successful and failed paths. No artificial resource completion, memory
patch, forced timeout, cancellation or gameplay action is authorized now.
Avoid adding these secondary hooks to the first center experiment unless their
extra execution exposure is separately justified. No spinner fix is proposed.

## Prior art and evidentiary boundary

[Prior-art ledger](prior-art.md) credits LarannKiar's primary changelog and
limited indexed firsthand Steam reports. Optional Traversal Stutter beta
regressions concern that mod's preview behavior; they do not establish a vanilla
fix or the native cause above. Overhead-view reports motivate flycam/readiness
controls; mod status and current-build equivalence are unknown. No third-party
implementation, binary, dependency or asset was incorporated.
