# D5J: shared beacon and native request follow-through

This closes the concrete branches identified by independent candidate01 REWORK.
The [report](report.md) retains the offline insufficiency conclusion after these
additional reads. Exact input/output identities are in [sources.csv](sources.csv).

All native addresses here are preferred static VAs, base `0x140000000`, for
Starfield.exe SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Object offsets are relative to the expressly identified object, never save offsets.
The local native exports are under
`.local-work/workshop-population-rework/specialist/`; they remain LOCAL-ONLY.

## Shared compiled behavior and native Workshop eligibility

`shared-checked.json`, produced by [shared.py](../../../research/terran-armada-recon/shared.py),
compares canonical VMAD bindings from the ordinary ACTI and all three faction
ACTIs. All bind `outpostbeaconscript` with the same seven object-valued properties
and status. Property order differs; the decoded property/value maps are equal.
No faction-specific beacon PEX is selected by these definitions.

Three shipped members were read from Starfield - Misc.ba2: outpostbeaconscript,
defaultquestchangelocationscript and its inherited ObjectReference interface.
All parse with complete object/file closure; nine malformed inputs are rejected
and 211 branch targets are bounded. This is a compiled-member check, not an
assumption of source/PEX equality or a running winning-archive claim.

In outpostbeaconscript, OnLoad calls GetCurrentLocation/AddKeyword at member
offsets 3203/3218, crew handling at 3246, survey queries/update at 3264–3391
and StartAttackTimer at 3457. OnWorkshopObjectPlaced calls companion handling
at 3505, GetValueResources at 3523 and conditionally starts the attack timer
at 3547. OnWorkshopMode calls tutorial IsRunning/EnterWorkshopMenu at 3621/3659.
These are event consumers. The complete compiled state/function set has no
Workshop creation/registration call or OnInit implementation. The inherited
ObjectReference PEX supplies interfaces; its native-declared functions do not
execute Papyrus initialization bodies. Development-source reading corroborates
the general event roles but is not used as shipped-byte equivalence proof.

The other attached shared script, defaultquestchangelocationscript, registers
player/ship location-change events at 3350–3410 and uses alias GetLocation,
IsChild and stage tests before SetStage at 4451. The installed VMAD supplies
stage 2000 and the location alias. This script handles arrival-stage behavior;
it does not create a beacon or a Workshop in its decoded functions.

Fresh `d5j-placement03.tsv`, function `0x140f51350`, shows the generic typed
Workshop accessor. Instructions `0x140f51364`–`0x140f5139d` require a base of
type `0x1e`, a valid keyword default pointer at `0x145f0b380` and a successful
keyword test. The inspected branch does not compare faction-specific base IDs.
With create flag clear, it reads extra type `0xbc`; with create flag set,
`0x140f513d7`–`0x140f51412` checks for that extra, allocates `0xa0` bytes,
calls constructor `0x140f4ffc0` and attaches the extra. The previously established
Workshop-keyword and typed-extra interpretation is retained from the
[Workshop-origin study](../workshop-origin-beacon-relocation-persistence.md).

This is positive **STATIC conditional eligibility** evidence for the shared
ACTI/keyword family. It does not identify the call history, create flag or
initialized operations of a selected faction instance. No native call was made.
The unresolved predicate is actual functional state and ordinary area-consumer
execution, rather than a hypothetical missing faction Papyrus initializer.

## Exact quest-request condition and invocation

The inherited primary initializer export `d5h-review-callbacks54.tsv`, freshly
read here, binds registration code `0x1353` to GetIsCurrentLocationExact:
name VA `0x144bcb140`, initializer instructions `0x1400e0fb4`–`0x1400e1024`,
callback `0x140c5b1d0`. It binds `0x1230` to HasKeyword: name VA
`0x144bc4d68`, instructions `0x1400d5982`–`0x1400d59f2`, callback `0x140c49960`.
The CTDA function indices are the corresponding `0x353` and `0x230`.
Fresh installed-PE string reads and fresh callback exports corroborate the joins.

`d5j-edges02.tsv` includes both callbacks. GetIsCurrentLocationExact instructions
`0x140c5b23c`–`0x140c5b253` check non-null operands, call current-location
getter `0x140b4e650` and compare identity to the resolved condition operand.
The decompiler incorrectly removes that reachable comparison as unreachable;
the instruction listing is decisive. HasKeyword instructions
`0x140c499df`–`0x140c49a38` perform the keyword-interface dispatch and set
the float result when the test succeeds. These names are no longer undecoded
search leads; neither condition alone computes planetary coordinates.

`d5j-alias04.tsv`, loader `0x140c9cfb0`, decodes ALPS as alias type 5,
LNAM into alias `+0x50`, and type-5 CTDA into the condition at alias `+0x28`.
The same export contains alias-fill function `0x140d049b0`. Its type-5 path
prepares candidate body IDs, supplies alias `+0x50` to `0x1418b5ea0`, and at
`0x140d05a7b` calls `0x1418af110` with manager, selected body ID, default
planet-content tree, request type 2, quest, condition and alias. Instructions
`0x140d05a1e`–`0x140d05a80` show the actual arguments and returned request ID.
The path subsequently polls `0x1418b34e0` and obtains the resulting location
through result `+0x2b0`; an unfilled request is an explicit possible outcome.
This is a real native placement-request edge reachable from the installed alias
representation, not an inference from a missing beacon before a quest stage.

`d5j-placement03.tsv` exports `0x1418af110`. Its request-node vtable identity
names BGSPlanetContentManager::QueueContentRequestOnPlanet. The function checks
manager enable/tree availability, carries quest/alias/condition context into a
queued resource-server node and returns a request ID. Its request-type-2 branch
mixes quest/alias identity and manager `+0x420` into request seed state. It also
has existing pending-content and failure branches. The installed template does
not fix these manager/session operands or the eventual placement result.
No complete placement-search algorithm or global seed persistence class is
claimed from this bounded read.

**Stopping boundary:** the shared script, generic native extra accessor, alias
loader, type-5 fill/request invocation and request-node construction have now
been inspected. Replacing the missing actual selected placement/frame with
template-local coordinates would still be invalid. Reconstructing all queue
history, manager seed state and terrain placement search would expand beyond
this reconnaissance while still lacking the selected save's actual state.
Metadata-only observation of an existing quest instance is the smaller remedy.
The generic constructor is an observed internal route, not a safe integration
point or authorization to invoke it. No full debugger or placement harness is
needed to support the bounded offline insufficiency result.
