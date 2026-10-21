# Save52 positive examples and runtime correspondence

[Answer](report.md), [C1 principal identity proof](../configuration-ui/save52.md),
[mature owner/name anchors](../../mature-save-validation/beacons.csv).
Offsets below are decimal **decoded logical-stream offsets**. They are neither
compressed file offsets nor native addresses. `ff` identities are save-era
resolved FormIDs, not stable live handles or cross-save identities.

The protected Save52 copy is 16,411,136 bytes, SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Fresh C2 `save02.json` frames all 205,557 R3 records and the 246-edge local-link
envelope. Candidate marker queues select75 records; **61 actually have a
qualifying ordinary/fueled marker base**, matching the earlier broader-window
coverage without promoting all 61 to active-player pads. One-hop queued references
and ship endpoints yield929 inspected records and24 selected ship-base matches.
This is a finite cargo investigation, not an exhaustive Workshop/ship census.

Nineteen ship inventories close under the established empty-stack-extra subset:
**11 stocked,8 explicit empty**. Four more stop after Extra33 at Extra30 and one
at ExtraD9. They are **five unknown inventories**, not five empty ships. Extra30
is an existing polymorphic-node representation; its full per-node interpretation
is not necessary for the positively decoded stocked/direction examples and is
not silently skipped. Principal C1's bounded Extra33 flags02/count2/mask00
extension is reused with provenance; all other flags/masks remain rejected.

## Selected independently grounded ships

| Example | Saved records and endpoint identities | Inventory / direction evidence | What it establishes |
|---|---|---|---|
| Principal ordinary pair | Ship ff02dc37 / GBFM255cc6 at 2344136; endpoint01 VII-b ff02c3c4; endpoint02 I ff03444c, both base2a6c3f | Empty item list2344497..2344498. AV2457af=1 at 2344468; Current255cc3→I landing ff03444b at 2344491. Both outgoing/incoming role keys match C1's four empty bays | Common hold, both directions' compartment identity, saved target02. Does not establish physically landed, in flight, timer ID or historical emptiness throughout operation |
| Stocked ordinary, VIII-b ↔ VII-b | Ship ff019341 /255cc6 at 2271664;01marker ff01ca84 owned ff044cc6 (VIII-b);02ff04d26f owned ff025f95 (VII-b), both2a6c3f | Inventory2272007..2272030: He-3 MISC00558e×558 and Gold005579×3. Current→01 landing ff01ca83 at 2272001 | Positive mixed freight in ordinary ship; He-3 here is cargo, not evidence of fuel consumption. No shipment provenance or causal return inference |
| Stocked inter-system, Schrod II ↔ Feynman V | Ship ff01c5b7 /GBFM219042 at 2276744;01ff0217b5 owned ff04ff81 (Schrod II);02ff04fad9 owned ff03388f (Feynman V), both ACTI219523 | Inventory2277095..2277107: Ionic Liquids MISC00557a×7, quantity bytes at 2277097; Current→01 landing ff0217b4 at 2277088. Ship incoming01 ff0217c8, outgoing01 ff0217bf; incoming02 ff04faec, outgoing02 ff04fae3 | Independently grounded different-system fueled link with real stock. No explicit destination AV override in this qualified BF section; do not invent a saved 0 byte |
| Stocked inter-system direction control, Carinae III-a ↔ Feynman IX | Ship ff047b8b /219042 at 2436024;01ff020ce1 owned ff02be17 (Carinae III-a);02ff02b86b owned ff02a0c0 (Feynman IX), both219523 | Inventory2436372..2436384: Lithium00557f×3; destination AV=1 at 2436339; Current→02 landing ff02b86a at 2436366 | Positive stock coexists with explicit opposite-target selection; direction agrees with script. Target is not a timestamped departure/arrival observation |

Owner/name associations use the earlier independently extracted beacon table,
then fresh explicit marker owner links, reciprocal peers, pad→ship and ship→pad/
child keys. Ship base and fueled marker definitions are freshly reread. Printed
names alone, He-3 stock alone, or an `InterSystem` filename would not suffice.
These two different-system examples provide the requested comparison without
requiring additional mature saves. No assumption of synchronized screenshots or
linear save history is introduced.

## Entity/field correspondence matrix

| Entity / field | Definition → serialized representation | Load/reconstruction → runtime consumer/effect | Classification / boundary |
|---|---|---|---|
| Both pad markers | Ordinary ACTI2a6c3f / fueled219523; template ownership/child references. Saved base and Extra4C owner 054ba6 | Reference/base restoration; Workshop identity and current reference resolution; marker script | Base DEFINITION-DERIVED; explicit owner/reference PERSISTED; runtime handles RECONSTRUCTED. Membership completeness is not inferred |
| Reciprocal route | LinkActive255cc8 on both pad markers | C1/S1 Extra4C `140562ef0` restores/remaps queued identities and reverse links; menu/script change events apply route lifecycle | PERSISTED relation; reverse index RECONSTRUCTED; UI pending choice TRANSIENT |
| Shared assigned ship | Pad LinkShip255cc7→same ff ship; ship keys217856/217855→both markers | Current reference lookup and script Create/ClearCargoLink; reverse links supply readiness participants | PERSISTED links; successful resolution/recreated scripting is not guaranteed by saved existence |
| Both outgoing bays | CONT219171 in sampled assemblies; marker2a6c45 and ship255ccc/255ccb | Restored reference inventory; timer0's outgoing selection and capacity-respecting source removal | Stock/links PERSISTED, default contents DEFINITION-DERIVED, per-call transfer plan TRANSIENT |
| Both incoming bays | CONT219173; marker2a6c46 and ship255cca/255cc9; local downstream map separate | Arrival receiving selection then S2 redistribution; installed incoming link prohibition prevents ordinary local upstream insertion | Stock/links PERSISTED; effective capacity MIXED; redistributable path cache RECONSTRUCTED |
| Landing markers01/02 | Ship255cce/255ccd and pad2a6c47; distinct identities from pad marker | Linked-reference target in Travel package, actual native path/landing admission | PERSISTED identity; current location/3D and path request are separate state |
| Selected target / next direction | Current255cc3 and AV2457af; actual principal and Lithium controls above | Extra4C remapping and effective AV interface → package condition and receiving-key comparison | PERSISTED selection; native movement phase UNKNOWN from these fields alone. Current changes before physical departure |
| Hold cargo | Ship reference inventory branch after supported extras, explicit item/stack quantities | `1406448b0` restores items; `1406447c0` saves; generic removal/addition changes hold and bays | PERSISTED physical stock; no separate ordinary manifest/provenance queue read by TransferCargo |
| Effective capacity/weight | CarryWeight, shielded-capacity AV and ship components, instance/modifier extras; item definitions/stacks | Effective AV/provider query and perkAA → current C; inventory weight cache rebuild/invalidation → current W | MIXED/RECONSTRUCTED; UI300 or empty saved hold does not measure current effective C |
| Ship script requires fuel / cached waits | PEX mutable RequiresFuel, timersInitialized, G and three game-hour fields; default seconds/constants from PEX, marker VMAD supplies fuel flag to creation | VM script instance/property restoration, OnInit/guarded initializer; existing timer callback uses current instance | Mutable VM state PERSISTED by VM, constants DEFINITION-DERIVED. Historical Save52 values/VM object join are **not decoded** by the narrow REFR reader |
| Pending game-time timer | Native manager+70 entries: bound script identity, timerID, due-current remainder, pause state | `1420fa390 → 1420fa920 → 1420f8970` writes remaining deadline, ID, serialized script handle, pause fields; `1420fa9a0 → 1420fcc70 → 1420f8d00` remaps script identity and rebuilds heap against current clock | PERSISTED remaining work; absolute heap pointers/order RECONSTRUCTED. Not a per-cycle missed-voyage counter; specific Save52 timer is UNKNOWN |
| Travel execution | Installed NPC package pair/template; native BGSProcedureTravelExecState saves fields40/41/43, optional target object and request/path state | `140e0a140/140e0a360` save/load procedure state, dynamic target type and path request; FlyLand `140ea6420/140ea6540` serializes/remaps its extra state | PERSISTED subset and RECONSTRUCTED pointers; actor tail/extra-node history is not fully decoded. No inferred exact flight phase/duration |
| Light/animation state | Marker AV333d22; quest animationStates definitions | Marker OnLoad reads AV and republishes light animation; ship callbacks set it | PERSISTED presentation AV, TRANSIENT light events. Not freight mutation authority |
| Controller / events | QUST2a6c44 and bound scripts; native timer manager/VM event queues | Package end→ArriveAtOutpost; due timer→OnTimerGameTime; cleanup→cancel | Quest/VM state MIXED; dispatched event stacks TRANSIENT or VM-persisted as applicable, not inferred from graph/hold |

Timer serialization is positively traced at native level rather than assumed
from script names. The saver writes due-minus-current; game-time heap has zero
real-time wrap-period conversion, while real-time heaps pass86400000 separately.
Restoration reads/remaps the bound script handle and rebuilds the timed entry.
Invalid/unbound script or invalid negative remaining-time cases can be warned,
discarded or adjusted; no guarantee every corrupt entry survives. The remaining
Save52 actor/VM bytes are not labelled empty, and no general VM/save extractor
was built merely to obtain a historical timer value irrelevant to the normal
one-shot scheduling rule.
