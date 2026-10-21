# L1 causal native and definition reference

Reader notation: [vtable versus object offsets](../../audits/publication-readiness-b2/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../audits/publication-readiness-b2/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer and matrix](report.md), [functions](functions.csv), [pins](sources.csv).
`nNNN` denotes `.local-work/l1-limits/native/NNN.request.tsv`; `rNNN` denotes
the retained R1 native export of that number. All function addresses here are
hexadecimal **preferred static VAs**, image base `140000000`. Subtract that
base for the RVA in the register. Fields and bytecode offsets are hexadecimal
unless explicitly decimal. None is a live pointer, save offset or callable ABI.

Freshly pinned EXE is retail 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
ESM SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Each used fresh export identifies that imported executable hash and base.
Decompiler pointer/return-type mistakes do not override instructions. In
particular `140f38a40`'s decompiled return incorrectly follows an unrelated
register; n004's final AL/DIL instructions establish the boolean return.

## Recipe limit, displayed count and accepted construction

1. Installed COBJ JNAM names a GLOB. Loader `140a02160` (r011) places it at
   COBJ+178; the decisive JNAM store is `140a0244b`. FNAM/BNAM category keywords
   do not select the shared quota. The raw names and IDs are in recipes.csv.
2. `140f3b170` (n002) traverses selected-context set `145f5d960`, storage
   `145f5d970`, extent `145f5d978`, skipping vacant slots. Each wrapper's
   virtual +40 supplies its representative handle. A successful resolver gives
   one reference; ExtraDA's construction identity is preferred, otherwise
   `140b4cd10` supplies base. `140f3b080` resolves the construction to COBJ.
   A match of that COBJ+178 pointer with the requested recipe's +178 increments
   once. It does not count every visual child, resource bay or foundation.
3. `1421dcb10` (n002, instructions `1421dcbce..1421dcbfc`) reads global+48,
   floors/clamps the threshold at zero, calls that count helper, and writes
   frame+61f when count >= threshold. A null JNAM skips this quota.
4. `140f3f9a0` (n002/n003) consumes +61f and selects candidate status `1f`.
   `14157b0c0` (n002) calls the same count helper for the `%d/%d` object card.
   Other failure gates can take precedence; a full quota does not guarantee
   that this is the first visible failure for an otherwise invalid placement.
5. Ordinary action handlers `1421b2360` and `1421b2e20` (n002) require
   frame+193 == 2. The former reaches `1421b10b0` only on the acceptable build
   route. Thus this is an action-enforcing preview status, not just grey menu
   decoration. No claim of an independent atomic threshold recheck inside the
   low-level placement operation or every script construction interface follows.

### Selected-outpost scope and updates

`1421b64c0` (r027) stores the destination at frame+608 and calls
`1421c6f90(145f5d960, destination, 1, ...)` (n002/r028). The builder compares
the destination handle with set+98, clears old context on change, and traverses
the owner's Extra4D reverse relationships filtered by WorkshopItem. Callback
`1421c71b0` resolves/deduplicates and creates single/compound wrappers;
`1421c6890` inserts them with set semantics. A globally addressed cache therefore
does not imply a universe-wide quota. Reconstruction uses saved/default
relationships; the resulting handles/set are transient runtime inputs.

`1421b10b0 -> 1421de3f0 -> wrapper virtual +A0` reaches single-item
`140f60f60 -> 1421dd600`; successful callers insert the wrapper. Removal
`1421de660 -> 140f34650 -> 140f404f0 -> 1421c6b90 -> 1421c77b0` erases it
and invalidates the slot. Move/edit `1421b1450` removes/rebuilds mappings through
`1421c6e30/1421c6d00`; it is not an unconditional second construction. Selection,
exit/reset and future refresh rebuild/recount instead of loading one numeric
per-category current-count scalar. These are the accepted [R1 chains](../robots/limits.md),
reused with their raw export pins, not newly discovered or live-tested here.

The helper has no direct Health, perk-rank or disabled-bit exclusion. Damage,
disablement or perk removal is not automatically a decrement. Actual deletion
through the mapped route changes the set; unresolved handles cannot count at
that evaluation. Universal event delivery for destroyed/disabled/default objects,
malformed state and stale/concurrent UI transitions remains unqualified. Existing
over-limit items are not evicted by a check that only returns an admission status.

### Cargo pads and skill application

COBJ `0021919f` builds PKIN `002191a0` (ordinary); COBJ `0021e700` builds
PKIN `0021903f` (fueled). Both JNAM values are GLOB `00190d57`, initial FLTV 3.
They share FNAM `0006d72d` with other miscellaneous recipes, but that keyword
does not create a miscellaneous-wide cap: the exact JNAM identity does.

Player perk `0023826f` rank 1 has type-0 entry to PlayerSkills QUST `002c59e4`,
stage **701 decimal** (`02bd`). Fresh shipped PEX
`Scripts/Fragments/Quests/QF_PlayerSkills_002C59E4.pex`, fully length-closed,
has `Fragment_Stage_0701_Item_00`: cast property to float at member-file offset
`2438`, then `Mod(OutpostManagementCargoLinksBonus)` at `243f`.
Installed quest VMAD property at payload+`1a9` is integer **3**; the global
property at payload+`4bb` resolves `00190d57`. These are VMAD-relative offsets,
not absolute ESM file offsets. The actual arithmetic is 3+3=6, once the normal
stage has run. It is not an intrinsic max-six constant or a sum of ranks 1–4.
Rank 2/3 stages 702/703 affect robot/station globals and rank 4 has its separate
production entry. [CR1](../crew/capacity.md)/[R1](../robots/limits.md) control
those reused results.

The installed property overrides matter: generic OutpostManagementBonus's PEX/
PSC default 1 is overridden to 3 too, but cargo uses its **own** configured
property. Reading the wrong property or a source default would not establish
the cargo limit. Quest-stage mutations and the current global remain distinct
from current perk possession; replay/abnormal progression can differ from the
ordinary one-stage application. No automatic reversal is established by simply
removing a perk. The card and count predicate reread the global on evaluation;
same-frame freshness after arbitrary mutation is not promised.

### Turrets and other groups

Turret GLOB `000f7c96` is 6. Seven recipes (compact laser plus three ordinary
laser and three ballistic definitions) share it: `0002c338`, `001099a6`,
`001099a7`, `001e663b`, `001e663c`, `001e663f`, `002e1819`.
Their direct outputs are NPC definitions `00113d5c`, `001099a4`, `001099a5`,
`001e663d`, `001e663e`, `001e6640`, `002e181c`. Shared quota follows JNAM,
not damage type or tier. The whole COBJ census and named threshold source census
find no ordinary turret threshold-increase fragment. Firing/power/targeting and
damage are outside L1, and a security robot is in the robot quota instead.

The same G chain applies to the other eight threshold globals. Their exact
recipe catalogue is retained rather than treating every named recipe as a
playable choice: some have quest/research conditions, missing FNAM or NNAM 0.
The CSV's NNAM value is raw metadata, not evidence of actual zero-output builds.
Armillary's additional COBJ conditions are OR-connected GetStageDone checks
against quests `002c6d74` stage 510, `0024ef9c` stage 10 and `0006cd98`
stage 110. This census does not resolve the full quest's cross-location state.

## Deployment allowance and ordinary beacon operation

DFOB `002a84f6` WorkshopMaxDeployed_DO binds AVIF `002a84f7`
OutpostMaxDeployed. Registration `1401594f0` (n010/n011) constructs default
object at `145f0c528`; its +48 value slot is `145f0c570`.
Player NPC `00000007` PRPS payload+`90` has AV `002a84f7`, float 8, followed
by its four-byte property metadata. PRPS entries here are **12 bytes**, not
eight; the initial exploratory eight-byte walk's end exception is preserved.
AVIF NAM0 alone is 0 and would give the wrong ordinary player baseline.

Habitation perk `0027cbc2` ranks 1–4 dispatch PlayerSkills stages 901–904.
Fresh compiled fragment SetValue operations are at member-file offsets
`22a8`, `2269`, `222a`, `21eb` respectively, setting **12,16,20,24**.
Quest VMAD OutpostMaxDeployed at payload+`358` binds `002a84f7`.
Unused OutpostMaxDeployedBonus source default 20 does not control these literals.
Normal rank dispatch reuses the [CR2 native rank lifecycle](../crew-skills/lifecycle.md);
these type-0 quest entries must not be interpreted as cumulative ability magnitudes.

`140f387f0` (n005) tests the player's effective AV via `1419776f0` and returns
reason **3** when <=0. The effective AV getter combines base and modifier inputs
(n006); it is a remaining-slot check, not a fresh enumeration of active beacons.
Ordinary integer states give allowed total minus charged deployments; arbitrary
fractional modifications are not rounded by this comparator.

`1415f69c0 -> 1415f6a90` (n003/n004) is the ordinary scanner action, directly
or queued. It calls `140f38a40` with no existing selected handle and then uses
the admission reason to show the exact max-number or missing-skills message.
`1415f9080` (n005) reuses this gate during confirmation and dispatches
WorkshopEngine::PlaceOutpostEvent for a new site, versus selection of an
existing valid beacon. Existing-beacon entry has its own reference/availability
checks and is not equivalent to admitting one more deployment.

The actual accepted build handler `1421b2e20` also requires frame+193 == 2;
its successful new-beacon path at `1421b3e88..1421b3ebb` (n011) invokes player
AV-owner virtual +30 with modifier index **2**, that AV and **-1.0** from
`144f0528c`. Ordinary removal `1421b7200` (n007/n011), after reference/item
cleanup, invokes the same modifier index with **+1.0** at
`1421b78de..1421b7911`. No per-planet, per-system or selected-outpost counter
participates in these operations. No separate final atomic max recheck is
established inside the low-level creation itself; admission/state refresh and
accepted action are separate stages.

“Deleted/abandoned outpost releases a slot” is supported for the ordinary mapped
RemoveOutpost operation, not every saved deleted/disabled bit. Disabling a beacon
does not itself execute the +1 instruction. Raw saved beacon counts therefore
cannot replace the player's effective allowance. The observed 19/17-clear saved
population is not a claimed nineteen-slot or seventeen-slot runtime charge.

## Planetary Habitation: exact environment predicates

DFOB `0003b6c2` -> CNDF `002dfd42`, OutpostAllowPlacementConditions.
Registration `1401571c0` (n003) creates object `145f0aca0`; value slot
`145f0ace8` is read by `140f387f0`. The actual caller constructs condition
context with player as subject and evaluates CNDF+38 via `140e466f0`. Failure
returns reason **2**, consumed as “Cannot place outpost: Missing skills.”

The four nested CNDFs are AND-connected. Inside each, the benign alternative
is OR-connected to GetPerkRank(`0027cbc2`) >= rank, with the rank check run on
explicit player reference `00000014` (CTDA run-on 2). This admits mixed hazards
only when **every** group passes, equivalently the highest present requirement:

| CNDF | Benign condition, or required rank | Exact rejected keyword(s) without that rank |
|---|---|---|
| `002dfd43` temperature | Nested `002e88ec`, or rank >=1 | `00295ec8` DeepFreeze, `00295ec2` Inferno |
| `002dfd47` pressure | BodyHasKeyword ==0, or rank >=2 | `00295ebe` PlanetPressure04Extreme |
| `002dfd46` atmosphere | Nested `002dfd45`, or rank >=3 | `00279292` Toxic, `00279293` Corrosive |
| `002dfd44` gravity | BodyHasKeyword ==0, or rank >=4 | `00295eba` PlanetGravity03Extreme |

`035a` is BodyHasKeyword, `0345` IsTrueForConditionForm and `01fb` GetPerkRank.
The fresh bounded registration scan (n016, 30,890 instructions, uncancelled)
binds command IDs `135a/1345/11fb` to condition callbacks
`140bf34a0/140c06e00/140bee630` respectively. n017/n018 establish their
actual use; n020 `1409e5a00` dispatches nested condition evaluation. Thus the
keyword and rank comparisons are established from native consumers, not names.

BodyHasKeyword resolves the subject's body/context through `140910690`, then
uses `140c0ad70`. n018/n019 show body-keyword/component sources, PNDT reached
through resolved body+`c0`, its direct keyword count+`1c0`/array+`1c8`, and
additional associated keyword sources. The helpers `140c0b0e0/140c0b1e0` test
those arrays and associated lists. It is not a direct comparison of gravity in
g, a temperature float, air oxygen, magnetosphere or solar output. PNDT KWDA
can corroborate a default keyword; current runtime sources can additionally
contribute, so static PNDT alone is not a universal current-context oracle.

The P1 solar/wind rating research uses the **same BodyHasKeyword consumer**,
independently re-established here. Its application is different: P1 chooses
generator definitions/ratings across several temperature/pressure classes; L1
uses these four specific hazard predicates. For example Frozen/Cold do not
require rank 1 here, whereas P1 uses them as a solar-rating branch. No oxygen
or general no-atmosphere prohibition follows from L1's atmosphere-toxicity gate.

### Other admission boundaries and persistence

`140f387f0` first rejects unsuitable current-cell/location contexts, with tests
through `140b58d50/1402cd1b0` (n020) and cell interior state. Location/ancestor
keyword test `140f38d80`, optional current-cell location checks, remaining
allowance and `14219bb40` vehicle state are distinct from environmental rank.
Reason codes consumed by `1415f6a90` are 1 restricted area, 2 missing skills,
3 max count, 4 invalid location, 5 exit vehicle. Existing-beacon selection has
its own availability path `140f3c8c0/140f3c7e0`. These are explicit dispatch
boundaries; their local geometry, city/POI policy and collision internals are L3.

CNDF is consulted for new admission. The two fully decoded PEX members include
OutpostBeaconScript.OnLoad; its observed ordinary work is location keyword,
crew/survey/timer handling, not a numeric/rank eviction loop. No such loop exists
in the mapped G count/admission or new-placement/removal operations either.
This supports prospective admission semantics within these paths, not a proof
that every load callback or arbitrary script preserves every over-limit object.
Save/load replay of global/player AV state and actual rank changes is not a
live measurement in this assignment. Low-level script creation and malformed
registry reconstruction remain outside a validated ordinary UI guarantee.
