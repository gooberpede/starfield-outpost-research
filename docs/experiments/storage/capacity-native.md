# Capacity and receiving: native derivation

[Report](capacity-report.md), [saved calculations](capacity-saves.md).
All addresses are **preferred static VAs**, image base `140000000`; RVA = VA minus
that base. Object offsets are hexadecimal. No runtime address or callable ABI is
qualified. Existing named classes come from analysis-state RTTI; semantic aliases
are analyst labels, OBSERVED-INTERNAL.

Fresh executable SHA-256:
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM:
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Local `cNN` below denotes `.local-work/recon/s1-capacity-NN.tsv`, exported with
owned OutpostRecon.java, existing Ghidra 12.1.2/JDK21, readOnly/noanalysis.
Full native bytes/decompilation remain local. Return types inferred as integers
by the decompiler do not override actual XMM float instructions.

## Capacity and item weight

`140f7c210` (c01, `140f7c235..281`) obtains nonactor reference+70 virtual+8,
keyed by `14049a430`'s +80 CarryWeight binding, and compares occupied W against C
using VCOMISS / SETNC. Ordered finite W >= C is full. Actor type 4b takes
`14190bee0`; generic fit also has a separate special base-type 41 branch.
Ordinary CONT does not inherit those actor calculations.

`140d96b20` (c04) names CarryWeight and installs its binding at manager+80.
The actual AVIF `000002dc` has NAM0 = 0. Each selected CONT supplies its own
CarryWeight PRPS. The effective interface vtable `144b96a90`, installed by
`140b21fd0` at `140b22062..69` (fresh c06/c11), maps virtual+8 to
`140b6ce20`, virtual+18 to `140b6cfa0` (inherited [AV contract](../inorganic-extractors/arithmetic-production.md#effective-interval-and-av-provenance), refreshed c01).
The ordinary base getter begins AVIF+178; explicit ExtraBF base lookup
`1419af700` can return early. Otherwise ExtraE1 property and base property-sheet
providers add their contributions. The effective getter adds ExtraBF modifier
total `1419ae7f0` (three binary32 modifier slots). Special AV type3 can redirect
to an owner. Effective C therefore is not universally the raw 75/150/300 field.
Perk effects relevant to these nonactor paths must arrive through actual provider
state; this trace does not apply player carrying-capacity perks to every store.
No separate per-insertion outpost perk calculation was found in these functions;
that bounded observation is not universal perk exclusion.

`1405fc440` (c01) obtains item mass from an instance provider's virtual+38 when
present and not sentinel, otherwise the form-type component. MISC type28 uses
component+130, float+8, hence MISC+138. `140a94740` (c07) installs the weight
component vtable at MISC+130. MISC loader `140a94c30` (c10) dispatches DATA
`41544144` at `140a94d3e..45` to `1405e1f40` (c11). That generic DATA reader
processes available value/health/weight components in order. MISC's value is
present, health absent, weight present: weight is DATA+4 binary32. Component
getter identities are in c12–c15; the health getter must not be mislabeled weight.
The selected MISC records' eight-byte DATA fields were physically reread.

## Occupied weight, cache and persistence

`140b69760` (c01) locks reference+a0/+a8. If the materialized inventory exists,
its +3c float is cached W; `bf800000` (−1f, c03 constant window) is invalid.
On that sentinel it walks item rows at inventory+30, count+28, stride28, calls
CalcContainerWeight virtual+8 and sums binary32 terms, then writes +3c
(`140b697b1..140b6983c`). The vtable `144b95c08` maps that callback to
`140b69650` (c03/c04).

The callback excludes the player-only special condition, checks item virtual+130,
sums 32-bit stack counts (stack stride10, quantity+8), clamps mass to >=0 and
calls owner virtual+4c8 for per-item weight. Ordinary reference constructor installs
main vtable `144b95fb8`; +4c8 = `144b96480` = `140b69c10` (c06/c08), whose actual
instructions are VMOVAPS XMM0,XMM2; RET. Thus ordinary reference weight adjustment
is identity. MISC virtual+130 = `1402b76b0` (c09/c13), accepting when item form
flag bit2 is clear; selected definitions satisfy this. For positive ordinary
counts the executable procedure is:

```
W = binary32 fold-add over admitted item rows:
      binary32(binary32(sum_of_stack_counts_u32) * max(instance_or_base_mass, 0f))
```

Actual count conversion zero-extends the 32-bit sum before VCVTSI2SS
(`140b69700..70b`, c04). Signed quantities on disk do not prove intuitive signed
negative weight arithmetic; wrap/overflow/negative/corrupt cases are unqualified.
No materialized inventory takes a distinct base-container fallback: skip item
flag bit5, use absolute signed base counts and base mass (`140b69999..140b69a08`,
c01). Do not mix that path with explicit changed inventory rows or infer that
null inventory means empty. Actor/player adjustments later in the function do
not apply to ordinary CONT references.

Mutation `140645ca0` (c04, `140645ded..140645e11`) invalidates inventory+3c to
−1f after row changes. The actual generic add reaches it through
`140643240` -> `140643360`; first-row insertion also goes through that list
mutation family. The mapped cache is per inventory, not per requested item and
not an immutable saved value. Inherited/future provider changes require valid
engine invalidation; universal alias/concurrency closure is not claimed.

Fresh `1406447c0` / `1406448b0` (c08/c13) write/read item count and rows, not
cached W or a dedicated full flag. [S1 wire grammar](native.md#link-and-inventory-persistence-are-separate)
remains unchanged: queued item identity, compact stack count, stack ExtraDataList,
signed i32 count and item bookkeeping. REFR mask08000020 governs this branch.
The full predicate is derived at query time; this is scoped to mapped paths,
not an absence proof across unrelated status/presentation channels.

## Fit computation does not enforce all generic additions

`140b70a80` (c01, `140b70b20..6f`) uses binary32 scalar arithmetic and ordinary
unsigned request q. Unless the receiver is the player, C>0, w>0 and
binary32(binary32(q*w)+W)>C, it returns q. Otherwise it returns zero when C−W<=0,
or truncates positive binary32((C−W)/w) with VCVTTSS2SI. Equality is not overflow.
There is no epsilon or round-to-nearest integer. Nonpositive capacity bypasses
this clamp, and nonpositive mass clamps to zero; these are not universal
zero-capacity/full rules. NaN/infinity/extreme counts are outside the qualified
ordinary model.

`140b64fc0` (c01) calls that helper at `140b65155`, computes q−fit at
`140b6515a..5e`, but tests and copies original q at `140b65162..17a` into the
mutation-loop remainder. `140b6574d..58` passes that loop's count to
`140643240`; the loop decrements its own original remainder. It does **not**
replace q with fit. The ordinary return is q−fit after a valid mutation path;
there are capability/type branches and special form-type behavior, so this is
not a universal success oracle. Caller-provided source availability and other
validation remain separate. No ONAM filter is read in this ordinary add path.

Production `140f7d510` (c07) selects a buffer/connected destination using
`140f7c210` (W>=C), additional readiness predicate `140f7d0b0` and product
compatibility `140f84020`. It does not ask how many requested units fit.
`140f7d6a0` (c03 decompilation; c20/c21 actual call at `140f7df8f`) sends the batch to
`140b64fc0` and does not use its return to count actual rejected units. S1/E1's
requested versus realized warning remains; the stronger newly checked result is
that a valid direct batch can cross the nominal boundary. Historic over-capacity
stock does not reveal its original writer or historical effective C.

## Local output-link redistribution admission and execution

`140f84020` (c03/c11) is the per-item destination filter: resolve ordinary product,
require a CONT, then base+258 ONAM null accepts, present-empty rejects, populated
list accepts exact item or keyword match. This differs from link-pair validation
and from merely checking existing stock category. A mismatch can reject with
plenty of free weight.

`140f84d70` (c06) is a concrete redistribution operation: obtains destination
references, visits source inventory rows with `140f84fc0`, then executes every
prepared 40-byte descriptor using source virtual+458 (`140f84ede`). It refreshes
source/destination inventory-related presentation afterward. It is not only a
theoretical fit helper. Source virtual+458 = `140b66680` via vtable144b96410
(c09/c10). Its param3+28 is the destination; the prepared descriptor's +1c is
the requested quantity. The receiving/removal family consumes that quantity;
S2 owns which destination is chosen, routing/retry policy and timing.

The actual bounded ordinary mutation chain is followed through:
`140b66680` -> `140b67a30` -> `140b89690` -> `140b8f540` -> `140b67100`
(c11/c13–c16). The callback passes descriptor+1c to `140b7c100` or the
instance-selected `140b7bd20` (c17/c18). These subtract the available selected
source stack quantity, bounded by the request, and call `140b67380` with that
**actual removed quantity**. The latter decrements the descriptor remainder and
passes removed count to destination virtual+4d0 at `140b67894` (c20).
Vtable144b96488 resolves this to `140b4ef90` (c21), which hands off to
`140b4cbc0` -> `140b64fc0` at `140b4cceb` (c22). The receiver's TESContainer
capability gate precedes that final add. The caller's descriptor already carries
the bounded quantity. This grounds ordinary partial receiving in actual
subtraction/addition, while source shortage, failed capability and exceptional
branches are separate from planned fit. Virtual+488 (`140b64e10`, c11) is an event
emitter, **not** the mutation oracle.

`140f84fc0` (c02/c15) obtains the item's provider-aware mass, filters destinations
through `140f89d00` / `140f84c40` (c02): unresolvable, excluded, incompatible,
or free weight < one unit are removed. For positive mass it computes C−W,
VDIVSS then VROUNDSS immediate1 (floor), VCVTTSS2SI and min(fit, remaining)
at `140f85580..5b8`. The count is stored in the descriptor at +1c and destination
at +28; **that bounded count**, not the original whole stack, reaches virtual458.
Thus full and fractional-free-space cases issue no descriptor; partial and
entire fit issue their corresponding bounded counts. Source quantity/actual
removal and concurrent changes can still affect realized deltas. Visitor return1
is continuation, not accepted-count feedback. Nonpositive-weight items take a
separate whole-remaining path after filter admission; negative/extreme mass
behavior is not generalized.

Manual ContainerMenu `141eb01a0` (c02/c07) calls the fit helper at141eb0787:
zero takes the feedback/refusal branch; nonzero is stored back into the subsequent
requested count at `141eb0c37`. Its captured predicate at `141eaf090` remains
the precise unresolved manual category boundary from accepted S1. These minimal
differences suffice to reject a fictitious universal manual/script/local policy.

## Preserved failed paths and limits

c05 and c06 attempted unsupported `win:start:end` selectors. OutpostRecon expects
`win:VA`; Ghidra logged script NullPointerException although process exit was 0.
Earlier complete function/data exports in those files remain individually usable;
no missing later selector is claimed. c07/c09 reran windows with correct syntax.
c08/c09/c12–c15 retain several interior-address guesses as NO_FUNCTION_AT; those
are not negative semantic evidence. Explicit field/table guesses were checked
against constructors and actual instruction targets, not trusted from names.
c17/c19 also retain failed windows whose guessed centers were not instruction
starts; c20/c21/c22 export the checked production and receiver call spans.
Large functions retain the 600-instruction cap; full decompilation can extend
beyond it, and claimed machine spans must be exported separately if beyond cap.
No symbols/types/comments, executable bytes or analysis state were modified.
