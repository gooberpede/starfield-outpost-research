# D5J: Terran Armada faction outpost reconnaissance

2026-10-27, Australia/Sydney. [Authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5J_terran_armada_faction_outpost_reconnaissance.md`),
[candidate matrix](candidates.csv), [primary identities](sources.csv),
[methods](methods.md), [native and shared-script follow-through](native.md),
[review and acceptance](review.md).

**All three reported quests have installed faction beacon templates, but none
currently supplies a qualified exact planetary Workshop control.** Their local
template transforms are recoverable. The missing join is the instantiated
quest-location placement and its planetary/source frame, followed by evidence
that the resulting Workshop actually uses ordinary resource admission. These
are promising existing construction routes, rather than freeze-ready inputs.
This is a bounded offline insufficiency result, not a finding that the sites
cannot support ordinary resources or can never become useful controls.

The three titles and body leads agree with installed definitions, with the
English spelling `Nemeria IV-a`. Each faction has one matching beacon template
in the inspected DLC. Quest aliases select the beacon through a location
reference type, rather than directly forcing that authored REFR. Authored
template identity therefore does not establish the loaded reference identity.
No new outpost, resource prediction or native geometry was generated here.

## Installed scope and identity

The fresh EXE hash matches the existing 1.16.244.0 baseline. `SFBGS050.esm`
is 106,017,249 bytes, SHA-256
`0bda63ae7e4fa48e1149a62e557c56ce65ce8c97badfc6fad1a5a0faf5abeb9d`.
Its Main BA2 is pinned separately in [sources](sources.csv). The plugin's
TES4 MAST sequence is `starfield.esm`, `sfbgs00d.esm`. Its self-domain prefix
is consequently `0x02` in the records below. These are **file FormIDs**, not
loaded runtime IDs, light-plugin indices, saved tokens or addresses. The
`03028236` spelling inside a compiled fragment's name is not load-order evidence.
No separately authoritative Terran Armada product-version field was recovered;
the immutable file hashes identify the inspected content revision.

The installed context check covers 39 ESM/ESP files. Master-qualified header
walks find 32 overrides of SFBGS050-owned forms, all GBFM ship forms in
`BlueprintShips-SFBGS050.esm`; none overrides the candidate records below.
No loose `mqoutpost` or `outpostbeacon` PEX was found under Data/Scripts.
The current Plugins.txt lists Creations and an unstarred
`ResourceGenerationTest.esp`; loadorder.txt is empty and Starfield.ccc is absent
at the game root. ContentCatalog has no Terran Armada version entry. This
establishes an installed candidate graph without detected candidate overrides,
**not** a certified running effective load order or archive precedence. No
retail process was inspected. A future run must verify loaded modules/plugins
and winning scripts before treating this graph as its effective content.

## Compact comparison

All forms in the first four identity columns belong to SFBGS050.esm.
Body LCTN and PNDT forms belong to Starfield.esm. The CSV retains full raw
float32 template values, authored rotations and all three individual decisions.

| Candidate / quest | QUST | Beacon REFR / ACTI | World / location | Body LCTN / PNDT | Decision |
|---|---|---|---|---|---|
| FC / Give and Take | `0x02028236` | `0x0202b254` / `0x02038ac8` | `0x0202b007` / `0x0202b011` | `0x0001b6ca` / `0x0005dee9` | PROMISING_NEEDS_EXACT_OPERAND |
| RI / Favors for Favors | `0x02028237` | `0x0202b255` / `0x02038ac9` | `0x0202b032` / `0x0202b061` | `0x0001b060` / `0x0005e13c` | PROMISING_NEEDS_EXACT_OPERAND |
| UC / Quid Pro Quo | `0x02028235` | `0x0202b256` / `0x02038aca` | `0x0202b062` / `0x0202b096` | `0x0001b51a` / `0x0005df86` | PROMISING_NEEDS_EXACT_OPERAND |

The scientific value and missing operands are the same for all three:
an authored beacon can avoid manual beacon placement, and a quest-selected
location can avoid eyeballing a landing point. An exact instantiated frame,
ordinary source population/history and active Workshop callback remain missing.
There is no evidence-based ranking by mineral quality or geometry, and no
test-site prediction has been fitted to quest resources.

## Placement and initialization evidence

The primary local receipts are `installed.json` and `joins.json` beneath
`.local-work/terran-armada-recon/`; exact hashes are in sources.csv.
Their record fields and parsed instruction offsets are the primary locators.
All ESM offsets below are original file offsets; PEX offsets are decoded-member
byte offsets. No native address is inferred from a file offset.

| Evidence | FC | RI | UC |
|---|---|---|---|
| QUST file offset | 101958322 | 101966785 | 101949805 |
| Beacon template file offset | 89302225 | 89334099 | 89361083 |
| ACTI file offset | 283947 | 285202 | 286457 |
| Quest location alias number | 3 | 5 | 3 |
| Beacon alias number | 6 | 7 | 5 |
| Location request keyword, QUST LNAM | `0x0202cdd6` | `0x0202cdd4` | `0x0202cdd5` |
| PCBN request branch | `0x0202cdd9` | `0x0202cdd7` | `0x0202cdda` |
| PCCN world-content node | `0x0202cddb` | `0x0202cdd8` | `0x0202cddc` |

**INSTALLED / STATIC:** The REFR NAME fields select the corresponding ACTIs.
The enclosing group ancestry places them in persistent-cell groups
`0x0202b009`, `0x0202b035`, `0x0202b066` of their respective worldspaces.
Each has record flags `0x400`, DATA transform and no explicit XOWN or XESP.
The lack of these two fields does not prove player ownership, an always-enabled
instance or absence of inherited enabling/ownership rules.

Each LCTN LCSR begins with reference type `0x003e8651`, its beacon REFR and its
worldspace. Starfield.esm identifies that LCRT as `OutpostBeacon_RefType`.
The quest beacon aliases have ALFA pointing to the location alias and ALRT
`0x003e8651`. The map-marker aliases use LCRT `0x0002271f`,
`MapMarkerRefType`. This closes the authored location-to-beacon association;
it does not identify the instantiated runtime reference or certify fast travel.

The location aliases contain a CTDA with the respective body LCTN operand and
LNAM with the respective forced-location keyword. Each PCBN has a CTDA using
the matching keyword; each PCCN PCCC selects the corresponding worldspace and
PRTN selects the corresponding branch. All branches parent to main-file
`0x0037c675`, `PCM_UniqueLocationRequests`. Targeted native registration and
callback inspection identifies condition `0x353` as GetIsCurrentLocationExact
and `0x230` as HasKeyword. The alias loader and fill branch also close the
ALPS/LNAM-to-native-request join; [native evidence](native.md) gives decisive
instruction locations and the remaining placement operands.

**Placement classification: HYBRID / STATIC route.** The beacon is authored
in a template, while the ALPS location alias follows a native queued planet-content
request route. The actual invocation is at preferred static VA `0x140d05a7b`;
its request carries quest, alias and condition context. Completion resolves a
location from the request result, rather than reading a fixed planetary XYZ
from the template. Actual placement/Workshop registration in a selected save
remains UNRESOLVED. No runtime request or constructor event was observed.
The alternative of an already instantiated quest location remains possible;
these definitions and native paths do not identify when a selected save creates
or reuses it. The template is not a qualified fixed planetary site.

The bound main quest fragment scripts call stage 1000 and start their actor
quest at stage 100. Stage 1000 supplies an aliased power core and objective;
stage 2000 advances objectives. Stage 10000 obtains the beacon alias and adds
the VMAD-bound main-file keyword `0x001cd02b`, `BlockPlayerActivation`, then
stops the quest. GetRef/AddKeyword member offsets are FC 2138/2153,
RI 2577/2592 and UC 2058/2073. The shared quest script registers beacon
power-on/off events and compares an event object's base against the
faction-specific X-Tech harvester property. Actor-quest stage 10 enables guards
and scientists. These are installed scripted edges, not observed quest history
or proof of when native Workshop state becomes functional. Dialogue/scene
entry timing and other engine callers are outside the demonstrated edge set.

## Coordinate precision and resource comparability

**PROVEN / STATIC within these definitions:** template-local XYZ and rotation
are available, all 19 beacon keywords equal the ordinary
`Starfield.esm:0x002c60e9` keyword list, and all three specify
OutpostBuildAreaRadius `0x00063fc5` = 150. The extra property
WorkshopBudgetBaseline `0x00319872` = 500 differs from the ordinary beacon.
Neither the declared radius nor common keywords proves the runtime area,
compensated center, height operand, orientation or initialization path.

The body join has an independent numeric check: LCTN XNAM/YNAM gives the
system/body pair found in PNDT's BDST GNAM. FC is `0x0001d114` / 3,
RI `0x00014a7c` / 12, UC `0x00011ad7` / 1. The named PNDTs are
TernionIIIPlanetData, NemeriaIV-aPlanetData and StrixIPlanetData. Nearby
Ternion III-a, Proxima/Beta Ternion and Strix moons are lexical discovery
counterexamples, not alternate identities. The joins do not supply a site anchor.

The required transform chain is: **body definition → actual requested/retained
location placement → instantiated overlay/chart and anchor/rotation → current
terrain rebase/frame → beacon original position and Workshop compensation →
area center/radius/height → source-index selection and resource operations**.
The first body identity and authored template endpoint are installed; the middle
placement and frame operands and the initialized Workshop endpoint remain
UNKNOWN for these candidates. Substituting the POI origin or template XYZ for
the Workshop center would skip those joins. No unique planetary coordinate,
source key, repeatability across saves or fixed ordinary resource set is claimed.

For ordinary evaluation, [the existing native dependency study](../native-availability-map/region-dependencies.md)
supplies the manager/source/operation requirements. The ordinary and all three
faction ACTIs have exactly equal canonical VMAD beacon-script/property bindings.
The shipped shared beacon script handles load/crew/tutorial/attack events; it
does not itself create or register a Workshop. The generic native Workshop
accessor admits the ACTI/Workshop-keyword family without a faction-specific
base-ID test and can create the typed extra when its create flag is set.
This supports common static eligibility, but **the same area
callback and accepted-resource/operation-vector execution are not established
for a loaded faction Workshop**. Ownership, quest completion, loaded state and
effective properties remain required checks. A success installing X-Tech cannot
fill that gap: the three quest harvester bases `0x0207e613`–`0x0207e615` contain
the place-anywhere `0x0031986f` and skip-vein `0x00271128` AVIF properties.
[The earlier qualified native gate](../resource-availability/report.md#resource-gate-and-x-tech)
at preferred static VA `0x1421f68f0`, base `0x140000000`, tests property presence
and bypasses ordinary overlap for place-anywhere. That inherited result is not
reported as a new native replay. X-Tech objective completion tests power/base
identity rather than furnishing ordinary source geometry ground truth.

Native source populations can eventually validate source geometry without a
Workshop. A Workshop-bound ordinary ACCEPT and transfer can validate selected
footprint intersections. An ordinary extractor catalogue positive is weaker:
it concerns that selected build gate and cannot certify complete resource
membership, geometry or absence. None was newly observed here.

## Least intrusive next step, design only

Prefer an **already existing conventional outpost with a withheld source/region
control** over engineering a fixed ordinary POI. Its functional Workshop avoids
the quest request and ownership joins; a fixed POI still lacks proven Workshop
initialization. Existing controls whose geometry is already known must remain
regressions, rather than being relabelled independent prospective validation.

If a faction site is preferred, first obtain metadata only under a separately
approved read-only capture: effective content, quest stage, actual alias/reference,
body, location placement transform, chart/frame, original beacon and Workshop
center/radius/height. Select a pre-completion, functional candidate; do not
progress quests, create a beacon or call native construction for this purpose.
Stop that design if exact frame or ordinary callback identity cannot be joined.
Freeze exact sources, generator/corpus revision, all viable historical mask
alternatives and predicted geometry **before** inspecting resource collections,
ordinary catalogue results, native points or ACCEPT/transfer ground truth.
Then a separately approved observation can compare source geometry first and
Workshop admission second, retaining cache/history ambiguity. No experiment,
debugger implementation or live GO is included in this delivery. B6 and
publication remain on hold; all legacy outputs and Save52 classifications freeze.
