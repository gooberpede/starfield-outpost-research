# L3: POI territory, placement collision and scenery suppression

2026-10-19, Australia/Sydney. SOR-EXP-0053 / SOR-EV-0061.
[Frozen plan/amendments](plan.md), [native chain](native.md),
[six saves](saves.md), [visual witnesses](screenshots.md),
[persistence](persistence.md), [review/package](review.md).

| Element | Best-supported result |
|---|---|
| Question | Why can an outpost be valid beside a POI, lose usable territory on that side, reject marginal rock overlap, yet admit deeper overlap? |
| Answer | Placement combines territory/location eligibility, candidate support and physics, and a separate eligible-scenery clearing pass. The ordinary beacon definition supplies radius 150. Location/encounter restrictions can reject positions inside that radius; border construction also accounts for excluded cell/location areas. Eligible scenery can enter the clearing set as the candidate moves and then stop blocking the physics query. Actors do not become ordinary eligible scenery merely by overlapping more deeply. |
| Confidence/basis | Proposed STRONG / STATIC for the bounded native mechanisms; PROVEN / SAVE for reported bytes and positive root joins; visible messages are direct screenshot observations, with scenario attribution supplied by the user. Exact photographed object/path association remains PROVISIONAL. |
| Coverage | Installed retail 1.16.244.0, main ESM, six new Kreet saves and eleven original screenshots. Ordinary exterior construction and the inspected native routes; no universal all-category or arbitrary terrain reconstruction. |
| Evidence | Native locators in functions.csv; installed definitions/source hashes in sources.csv; Save30/31/33 and Save34/35/36, independent record walks, decoded offsets, primary mask/position rereads and protected originals. |
| Limits | No rejected-candidate XYZ/physics trace, exact photographed rock identity, actual loaded POI interval/encounter object or travel/reload incident is available. These gaps prevent replay of the individual screenshots and historical reappearance, without invalidating the ordinary mechanism. |
| Next step | Review this offline result. A future live discriminator is optional and requires separate approval; none was executed. |

## Plain-language answers

**Why is beacon placement refused near a POI?** The proposed position can be in
a restricted cell/location/encounter context even when the scenery appears empty.
The native validator has a territorial status `0x16`, separate from collision
status `0x04`. The supplied POI beacon and solar images both visibly say
**Area is restricted**. The brief's contrary beacon-message description is
preserved and corrected in the witness ledger. The identified POI is Abandoned
Industrial Compound; its displayed 203 m marker distance is not an exclusion radius.

**Why can a valid outpost have a clipped usable region?** Its beacon can pass at
one position while another proposed object position fails the surrounding
location/encounter tests. Nominal radial membership, territorial permission and
drawn border are separate native operations. The circular border builder gathers
disallowed cell/location groups and intersects its radial boundary with their
rectangles. This explains qualitative clipping without requiring a saved bespoke
polygon. The installed beacon property is 150 native units; no metric conversion
or exact clipped area is inferred from the pictures.

**Why can deeper overlap work when marginal overlap fails?** Clearing and physics
do not ask the same geometric question. The native preview/update path collects
nearby scenery with a candidate-size-dependent padded radius and a category,
property, ownership and territory eligibility classifier. Selected references are
temporarily hidden/faded and put in an ignore set used by collision testing.
A marginal mesh hit can remain outside that set; moving deeper can bring an
eligible reference into it. The two solar screenshots support this explanation,
but do not capture the original reference pivot, bounds or selected hit list.
Thus the general mechanism is STRONG STATIC; the particular rock's transition is
PROVISIONAL, not a proven replay or a universal overlap threshold.

**How are animals treated?** Ordinary actor/NPC bases do not pass the normal
scenery eligibility selector. A remaining actor hit can block the candidate and
produce status `0x04`. The extractor screenshot directly witnesses the intersection
message beside animals; species, hit shape and which animal caused the hit remain
unknown. Player hits have additional collector handling. This does not assert
that every actor or every placement mode follows an identical filter.

**What is saved?** Constructed roots, owner links and positions are saved, along
with per-reference Workshop-bulldozed change state. Both new sequences have
positive bulldozing-channel records after construction: POI 0 → 1 → 4 and clutter
0 → 1 → 12. That is neither a list of photographed rocks nor a count of all hidden
environmental objects. Preview clearing lists and physics results are transient;
the ordinary border is reconstructed from positions, definitions and world state.

**Why might a rock return?** Temporary preview clearing has explicit restoration;
confirmed construction additionally sets persisted bulldozed state. The loader
restores that state, and native cleanup can clear it. A scene hidden only by the
temporary path can return normally. A genuinely committed rock returning would
require distinguishing loss/clearing of its saved state from resolution to a
different generated reference or failure to apply suppression to its new scene.
The historical incident was not reproduced in this corpus. Its cause stays OPEN.

## Worked outcome matrix

Statuses below are hexadecimal. Saved inputs identify actual constructed
references; rejected previews are not invented as saved objects.

| Candidate/context | Native predicate/stage | Visible outcome | Saved inputs | Transient inputs / confidence and discriminator |
|---|---|---|---|---|
| SOR-004 beacon toward compound | cell/location NoPlacement ancestry and encounter eligibility; status `0x16` | restricted | Save31 beacon ff029ab6; accepted retained position | proposed rejected XYZ and resolved location/encounter unknown; STRONG mechanism, screenshot-path association PROVISIONAL |
| SOR-004 accepted beacon | same decision chain, all required gates pass | placed beacon and clipped nearby border | Save31→33 stable beacon/root/XYZ | actual rejected/accepted geometric delta unmeasured; SAVE positive plus user association |
| SOR-004 solar inside | selected-outpost territory then location/encounter status `0x16` | restricted | Save33 solar ff03aaa6 is a constructed control, not the rejected preview | rejection XYZ/footprint unknown; cannot derive radius from the 203 m marker distance |
| SOR-004 solar outside | same ordinary chain plus success status `0x02`/action gate | white permissive preview, no visible error | positive owner/root solar in Save33 | photograph-to-reference identity unknown; screenshot alone does not prove action confirmation |
| SOR-005 beacon marginal/deeper rock overlap | eligibility/nearby clearing versus remaining collision; status `0x04` versus permissive result | red intersection versus white preview | Save35 beacon ff041cc1, one bulldozed-channel reference | exact rock class/pivot/bounds absent; STRONG static mechanism, PROVISIONAL instance explanation |
| SOR-005 solar marginal/deeper overlap | padded radius classifier→temporary ignore/fade→physics | red intersection versus white preview and absent large rock | Save36 solar ff042cdc; twelve bulldozing-channel references overall | two image viewpoints are not a measured swept test; same-rock identity/depth supplied by filenames/user |
| SOR-005 extractor/animals | actor not admitted as ordinary scenery; remaining overlap collector | intersection | Save36 extractor ff042f7c is actual construction elsewhere/at another epoch | animal identity and exact hit unknown; visible witness plus STRONG ordinary category distinction |

Sources: Bethesda installed EXE/ESM/development scripts and existing Ghidra
analysis; maintainer saves/screenshots; owned Workshop-root, position, L1/L2 and
extra-reader research reused with provenance in [methods](../../../research/spatial-placement/README.md).
No outside implementation, new dependency or web source was used. Authored
interpretation/metadata REVIEW-REQUIRED; primary proprietary/personal bytes
LOCAL-ONLY. Confidence supplies no publication, integration or live authority.
