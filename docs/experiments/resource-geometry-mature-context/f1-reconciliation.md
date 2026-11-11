# Mature observations: real disagreements, one supported Water explanation

2026-10-22, Australia/Sydney. [Continuation authority](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_A1_F1_mature_vein_observation_reconciliation.md`),
[plan](f1-plan.md), [checks/reproduction](f1-validation.md), [cumulative review](f1-review.md).
Authored REVIEW-REQUIRED; raw images/native/save/definition evidence LOCAL-ONLY.

**The current model does not reconstruct the complete actual resource inventory
of either mature outpost. Feynman Ionic Liquids and Carinae Iron are genuine
observed-versus-predicted disagreements. Water can be admitted independently of
localized veins through the terrestrial extractor's native skip-vein branch.
Copper has a concrete singleton-disk candidate that contains its saved extractor.
No supported seed or geometry correction yet resolves IL or Iron.**

The established seed/owner/static initialization mechanics remain supported.
Their application to the complete mature spatial result is unvalidated and now
has concrete counterexamples, not merely unspecified epoch uncertainty. Earlier
chat wording implying that actual Save52 inventory could already be calculated
was too strong. Mathematical agreement of two implementations shares assumptions
and native interpretation; it cannot override the new observations.

## Claim-level comparison

All predictions below refer to frozen v2 nominal radius150 and its declared
coordinate transform, not to image-derived coordinates. [Machine table](f1-claims.csv)
adds screenshot IDs, preview errors, rates and saved witnesses. P/T mean certified
bounded_region / exact tapered_strips area. UNKNOWN is retained, not absence.

| Site/resource | P / T | Supplied in-game evidence | Disposition |
|---|---|---|---|
| Feynman Nickel | PRESENT / PRESENT | Yellow region S006; saved extractor838366 | Resource identity agrees; bounded point contains hardware, tapered point misses. Footprint/consumer correspondence unresolved. |
| Feynman Cobalt | PRESENT / PRESENT | Blue region S004, overlap rejection; extractor838360 | Same distinction as Nickel. |
| Feynman Copper | PRESENT / UNKNOWN | Near-circular region S005, overlap rejection; extractor83836a | Supported singleton disk at saved point; screenshot primitive/extent not registered. |
| Feynman Ionic Liquids | ABSENT / ABSENT | Cyan region S001/S002, extractor83836b; maintainer reports production | UNRESOLVED substantive mismatch, also demonstrated at independently saved hardware. |
| Feynman Fluorine | PRESENT / PRESENT | Not in supplied visible extractor menu; no shown patch/hardware at P3 | UI discrepancy clue; actual resource absence NOT ESTABLISHED. Menu refresh/conditions and spatial query are unbound. |
| Feynman Water | ABSENT / ABSENT (veins) | Water preview S003; maintainer reports successful placement anywhere | Separate admission mechanism supported; [Water note](f1-water.md). No captured construction/selected-base identity in pixels. |
| Carinae Alkanes | PRESENT / PRESENT | Approximately two distinct shown patches S007/S008; extractor82bea9 | Presence and separation qualitatively compatible; saved point misses modeled footprints. Native consumer correspondence unresolved. |
| Carinae Iron | ABSENT / UNKNOWN | Approximately two distinct shown patches S009/S010; extractor82bea6 | UNRESOLVED substantive mismatch. Outside-build-area error in S009 does not negate S010 or the saved inside-circle hardware. |
| Carinae Rothicite | PRESENT / PRESENT | Distinct region S011, overlap rejection; extractor82bea4 | Identity agrees; saved point misses modeled footprints. Spatial equivalence unvalidated. |

Source IDs are RG2A1-POST-S001…S011 from [eleven image hashes](post-review-screenshots.csv).
Feynman UI shows IL44, Water111, Cobalt148, Copper222, Nickel222 per hour;
Carinae shows Alkanes74, Iron222, Rothicite89. These are displayed per-extractor
rates, not measured throughput, ore quantity or vein counts. The maintainer
identifies about two Iron and two Alkanes deposits, supported by the distinct
views. A connected visible patch is not necessarily one generated path.

An IRES definition, selected generator family, menu option, colored preview,
saved constructed extractor and observed ongoing production are separate facts.
Overlap and territory rejection show failure of that attempted placement, not
resource absence. Frames without rejection text do not alone prove construction.
No screenshot contains a qualified FormID/XYZ channel; all Save52 attribution
and the Water-anywhere statement are maintainer reports. Filenames encode local
time-like strings, not independently verified gameplay timestamps or timezone.

## Copper and repeated patches: primitive tests

Whole frozen Feynman sources have 46 Copper paths, 13 singletons. Only one Copper
path has certified positive-area radius150 overlap: source
`0:25116:32448:00257f38`, cell(11,1), point
`(-2663.88427734375,-44.542327880859375,0)`, width/radius23.968467712402344.
The declared translation maps its center to saved-site XY
`(136.11572265625,155.457672119140625)`. The independently saved Copper extractor
is `(137.2880859375,148.99472045898438,0.36666804552078247)` and lies inside that
disk. No seed/offset was fitted to it. A finite positive disk already exists in
the model; the image does not require inventing another primitive.

Native `14079b020` tests positive-width point disks and max-width segment
volumes after its bound. Native area callback `1421e1146–1421e1154` accepts a
count-one region after XY sphere/query overlap without inspecting point width/Z.
For this singleton its native sphere equals its point/radius, so the planar
zero-radius-query product is a disk. This does not generalize multi-point sphere
broadphase into filled circular availability. Exact tapered_strips deliberately
returns UNKNOWN for a singleton; the sampled point convention is a separate disk.

Multiple overlapping disks/short paths can also form a near-circular union in
general. They are not required by the frozen nominal Copper result: other Copper
paths are certified disjoint from the nominal circle. We cannot register the
photographed boundary to that disk, distinguish image rasterization, or prove
exact circularity from perspective. Existing raster builder `1407a0820` and
aggregate sampler `14079ee50` are separate products; the inspected exports do
not establish the colored preview's drawing consumer or a raster-to-path identity.

Carinae has 505 Alkanes paths (113 singletons), 259 Iron (130 singletons),
131 Rothicite (13 singletons) across the four whole sources. Five Alkanes paths
intersect the nominal circle. Their native-bound overlap graph has two separated
groups of sizes4 and1, proving at least two disconnected bounded-product groups;
edges within the four-path group do not prove its footprints connect. Four
multi-point strips are area-positive and the singleton has strip-area UNKNOWN.
This supports multiple patches as plausible geometry, not an exact screenshot
join or an assertion that five paths mean five deposits. No Iron bounded path
intersects the circle; merely changing union interpretation cannot produce the
observed Iron patches. One Rothicite path is area-positive.

The existing exact native-area evaluator, supplied modeled planar Z=0/height0
and radius150, accepts Ni/Co/Cu/F and Alkanes/Rothicite, rejects IL/Iron/Water.
This diagnostic retains singleton and broadphase semantics, but is not an
observed callback or actual height/placement invocation. It shows that selecting
this already modeled consumer does not resolve the two main absence errors.

## Independent saved spatial witnesses

[Seven exact joins and point diagnostics](f1-witnesses.csv) link recognized
case5 extractor base/resource records to the later closed-extras/native-root
projection: unique WorkshopItem owner, matching base, record offset, raw XYZ and
parent. All seven have saved disabled/deleted clear. The P3 parent is84ec80,
ownerff03388f; P4 parent84655c, ownerff02be17. Save52 SHA256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Offsets are decompressed logical-save-stream bytes, not original ESM offsets.
These are supported hardware witnesses, not output state or exact vein extent.

Applying unchanged frozen translations gives bounded-point hits for P3 Ni/Co/Cu,
and tapered-point hit only for Cu; P3 IL and all three P4 hardware points miss
both products. The IL extractor is53.3616 from its beacon, Iron82.7839; both
are well inside nominal150. Their nearest matching native-bound point gaps are
221.6371 and233.2978 respectively. Thus unmeasured small rounding or selecting
disks instead of strips cannot bridge those point gaps. The numbers are modeled
XY separation diagnostics, not a measured extractor footprint or exact native
error bound. The earlier hardware projection independently establishes explicit Workshop
membership within its saved scope; it does not identify a screenshot ghost.

## Causal challenges and supported dispositions

| Assumption challenged | Actual test / result | Consequence |
|---|---|---|
| PNDT owner/key | Actual loader/lookup/setter still supports385246/386266; no alternate value in supplied evidence. P3 three saved bounded hits, including Cu singleton, use it. | No justified owner substitution; numeric fitting rejected. Historical actual manager field remains unbound. |
| Snapped descriptor vs saved-site frame | Untuned whole-source control switches only to the preexisting saved-site origin and corresponding clip/query/key translation. All ten source key sets change. Feynman155 paths, no nominal positive resources or four saved hits; Carinae849, Alkanes/Rothicite nominal positives but no three saved hits, one unresolved clipped arrangement. | That simple alternative fails to explain IL/Iron or improve held-out witnesses. Do not replace v2 frame. No global claim that every other context is ruled out. |
| Family/RSGD | v2 explicitly generates IL once elsewhere and Iron259 times; they were not omitted from eligibility. Main-family root descriptor and descending rarity agree with inspected14079b520/14079c540. Carinae uses PNDT override18ce04, distinct from BIOM RNAM83f1. | Missing resource definitions or a blanket absent family do not explain the local negatives. Actual selected component/descriptor is the named remaining acquisition edge. |
| Atmosphere | Existing empty-local/inherited-Water alternatives retain the same main families and draw counts; final views differ. | This tested alternative alone does not repair IL/Iron. Water skip gate is independent of atmosphere. |
| Mask/weight | Frozen conservative source neighborhoods uniform8 Feynman,4 Carinae; IL inactive multiplier0.01, Iron full1. | A zero or accidentally omitted Iron weight is not the cause. Actual effective mask/settings remain unobserved; no arbitrary retuning. |
| RNG/order | Existing85 regressions and independent1051-path regeneration; whole-source ordered competition retained. New control recomputes changed keys, not translated final paths. | Reproducibility of the implementation stands; shared interpretation is not native equivalence. |
| Geometry consumer | Separate bounded, tapered, exact native-area diagnostic and native spheres; IL/Iron negatives persist. Cu count-one disk is a supported positive control. | Disk/strip distinction explains Cu UNKNOWN, not the IL/Iron mismatches. Alkanes/Rothicite hardware misses remain consumer/context questions. |
| Cache/source lifetime | Existing miss-generation/visited bookkeeping lacks completeness/freshness proof; no same-epoch selected descriptor/CTPerBiomeData/region map is supplied. | Specific missing consumed inputs, not a finding that stale cache caused anything. |

No changed generator or prediction v3 is warranted by current evidence. Preserve
all v1/v2, complete geometry receipts and prior reviews. Their local geometry
products remain reproducible conditional baselines; the operational inference
“zero Water paths means no extractable Water” is withdrawn. Likewise the mature
predictions must not be presented as actual complete resource inventories.

The smallest useful existing-offline extension is an exact selected-context
receipt joining manager+80, selected descriptor+0xc8/+0x1c0 and owner-grid origin,
CTPerBiomeData/RSGD descriptor/weight and ProcGen source/resource regions to one
of these saved extractor/site identities. If none exists, a separately authorized
coherent observation at the IL/Iron hardware can compare that consumed region
against the already frozen point prediction. A common-frame map/landmark join
with saved coordinates, known camera orientation/scale and consumer identity
would permit screenshot geometry registration. No pixel polygon or live action
has been invented here. B6, observer NO-GO and publication gates remain unchanged.

## Status and chronology

Original final01 accepted a qualified offline package before these observations.
The informal subsequent addenda changed seven reviewed files and added three
records; they were not covered by that acceptance. This F1 reports and reviews
the entire cumulative tree afresh. Original brief/reviewer returns and frozen
predictions keep their exact bytes. The maintainer's deletion premise for the
other Feynman outpost was withdrawn: it is an optional candidate, not a mandatory
test or newly approved reserve. [Current site status](active-candidates.md).
Scientific closure of IL/Iron is **UNRESOLVED**; assignment/documentation acceptance
is a separate [independent decision](f1-review.md).
