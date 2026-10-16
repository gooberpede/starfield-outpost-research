# Resource intervals and extractor size arithmetic

2026-10-16. Bounded continuation of SOR-EXP-0038 / SOR-EV-0046 under the
[authorized chat follow-up](../../implementation-briefs/CODEX_BRIEF_SOR_E1_resource_intervals_extractor_sizes.md).
[Verification/review](resource-intervals-review.md), [resource table](resource-intervals.csv),
[all extractor definitions](extractor-sizes.csv).

| Element | Answer |
|---|---|
| Question | Which main-game inorganic resources use each base interval, and how do extractor sizes change it? |
| Best-supported answer | The 45 resources linked to the 154 main-game category-qualified extractor definitions use 36, 54, 72, 90 or 108 engine elapsed seconds. Definition-based duration factors are small solid 1, small gas/liquid/atmospheric 2, medium approximately .8 and large .5 on the native fallback path described below. Quantity remains one requested product per due cycle under the corresponding baseline. |
| Confidence/basis | Proposed STRONG / STATIC for the connected definition-to-native contract; exact record bytes and floating-point operations independently checked. |
| Coverage/completeness | Every main-game CONT selected by extractor category 008406 in the independent installed catalog: 154 definitions, 45 resources. All 47 main-game ResInorg IRES also mapped; two have no linked CONT extractor. Names alone do not define the extractor census. |
| Evidence | Pinned ESM, all selected physical records, existing getter/timer exports, new CONT PRPS loader and unchanged-value insertion/copy instructions. Source pins remain local. |
| Limits | Definition-only fallback excludes explicit instance base overrides, extra properties, effective modifiers and the provider's separate Health-AV branch. Actual participation, interval/countdown state, item acceptance and live timing were not observed. DLC/X-Tech and mod override merging are excluded. |
| Next step | Static rules are useful within that scope. A separately authorized live capture could check effective values and resulting timing; it is not needed to establish the traced arithmetic. |

## Resource mapping

These groups come from **IRES NAM3 links**, not a guessed rarity formula. Times
are binary32 results of the linked GLOB FLTV hours multiplied by 3600f. The exact
global IDs, bytes, AV/IRES identities and decimal physical record offsets for
every resource are in [resource-intervals.csv](resource-intervals.csv).

| Base seconds | Interval global (Starfield.esm) | Resources with linked extractor definitions |
|---|---|---|
| 36 | 05ed87, Common | Aluminum, Benzene, Chlorine, Copper, Helium-3, Iron, Lead, Nickel, Uranium, Water |
| 54 | 05ef3f, Uncommon | Alkanes, Argon, Beryllium, Chlorosilanes, Cobalt, Fluorine, Iridium, Silver, Tungsten |
| 72 | 05ef3e, Rare | Carboxylic Acids, Gold, Lithium, Mercury, Neodymium, Neon, Platinum, Tantalum, Tetrafluorides, Titanium, Vanadium |
| 90 | 05ef40, Exotic | Aldumite, Antimony, Caesium, Dysprosium, Europium, Indicite, Ionic Liquids, Palladium, Plutonium, Rothicite, Tasine, Xenon, Ytterbium |
| 108 | 05ef41, Unique | Veryl, Vytinium |

There are 10/9/11/13/2 linked resources in these groups, totaling 45. The other
two ResInorg definitions are Aqueous Hematite (90 seconds) and Caelumite
(108 seconds). Their interval links are established, but no category-qualified
main-game CONT extractor links to their AVs; these values are not advertised as
obtainable extractor production. This does not claim no scripted or exceptional
way of obtaining either item.

Counterexamples to reading rarity from names include Common Argon → Uncommon
interval, Uncommon Benzene → Common, Exotic Neon → Rare, and Unique Aldumite,
Indicite, Rothicite and Tasine → Exotic. Actual links control the calculation.
The old three common-resource examples remain valid **base intervals**, with
their size/effective-value qualification made more precise here.

## Size factors: a substantive small-tier exception

The native getter adds the AV default to the base property; the raw property is
neither a direct multiplier nor automatically an absolute replacement. AVIF
008407 has default NAM0=1. The PRPS loader preserves the property float without
subtracting that default. With no explicit instance base override, extra-property
contribution or effective modifier, and outside the provider's separate special
AV branch, the calculation is:

```text
size factor = binary32(1 + base PRPS contribution), absent contribution = 0
effective interval = binary32(actor/player-adjusted base interval × size factor)
```

The multiplication uses a positive effective value, substituting 1 otherwise.
All factors in the table are positive. Actual getter precedence and later
modifiers are described in [the arithmetic reference](arithmetic-production.md).
This continuation does not claim every loaded object has no overrides.

| Extractor tier/family | Raw rate PRPS | Definition-only factor | Interval relative to that family's small tier | Nominal throughput relative to small |
|---|---|---|---|---|
| Small solid (28) | Absent | 1 | 1 | 1 |
| Other small definitions (24, including atmospheric and powered variant) | 1 | 2 | 1 | 1 |
| Medium (51) | −0.20000000298023224 | 0.800000011920929 | About .8 for solids; .4 for other families | About 1.25× solids; 2.5× other families |
| Large (51) | −.5 | .5 | .5 for solids; .25 for other families | 2× solids; 4× other families |

Throughput comparisons assume equal resource quantity, eligible production and
the same other factors. They are reciprocal interval comparisons, not measured
inventory growth. The **small gas/liquid exception** corrects the tentative chat
suggestion that all sizes share factors 1/.8/.5. That suggestion was explicitly
conditional; the completed trace supports 2/.8/.5 for these small definitions.
The earlier arithmetic example for small He-3/water gave 36×M without inserting
a current M; this report establishes their definition-only fallback M=2.

For a common base interval of 36, small solid Iron gives 36 seconds, while small
gas He-3 and small liquid Water give 72 seconds on this fallback path. Medium
gives 28.80000114440918 and large gives 18 seconds, before actor/player factors.
For base intervals 54/72/90/108, medium gives
43.20000076293945/57.60000228881836/72/86.4000015258789 seconds; large gives
27/36/45/54. Small solids retain the base and other small definitions double it.
Binary32 rounding is part of these results; “20% shorter” is a convenient
approximation to the medium factor. It is not “20% more items per cycle.”

Every one of the 154 bases has exactly one linked inorganic resource property
of 1; its resource AV default is 0. The ordinary registration path's ceiling
therefore yields one iteration under the same no-override baseline. Every
associated resource recipe has NNAM=1, but NNAM is **not** independently used as
a direct-output multiplier in that branch. Size changes duration here, not the
requested product count. Effective resource AV, registration age, scheduler
rounding/countdown and storage acceptance can still separate displayed nominal
rate from actual output; the [clock](arithmetic-clocks.md) and
[realization](arithmetic-production.md) boundaries remain in force.

## Definition coverage and exceptions

The full selected type walk reads 707 CONT, 332 IRES, 1,107 AVIF, 2,677 GLOB,
3,009 COBJ, 5,931 KYWD and 1,319 MISC records from the pinned main ESM. All
category-qualified CONT records equal the independent prior catalog's **154
main-game bases**, with no unlinked category candidates. That catalog has 159
installed entries overall: the remaining five are SFBGS050 X-Tech definitions,
outside this main-game contract. The earlier identity reference lists four
X-Tech examples, not an exhaustive list of those five.

The 154 consist of 84 solid, 30 ordinary gas, 21 ordinary liquid and 19
atmospheric definitions. There are 51 definitions per standard tier plus the
extra small powered atmospheric He-3 variant 201b82, which has no main-game
construction COBJ link. The [table](extractor-sizes.csv) retains every base,
including that variant; a construction recipe link is not proof of current
player unlocks or that every menu exposes an object. Six resources have
atmospheric alternatives: Alkanes, Benzene, Chlorine, Fluorine, He-3 and Water.

Size tier names are independently corroborated by MODL filenames across all
154: Driller01 for small solids, Small/Medium/Large model variants elsewhere,
and GasExtractor for small atmospheric definitions. No new universal native
numeric size field is claimed. Three Tetrafluorides bases lack the usual
gas/liquid/solid family keys but still have extractor category 008406 and the
correct resource AV. Their rate properties follow the size table. Missing family
keys may affect conditional perk eligibility; this investigation does not force
all crew bonuses onto them. The powered variant and atmospheric/vein differences
do not establish that placement or operational eligibility are interchangeable.

Organic resources, manufactured items, mission-supply, test and other IRES are
excluded explicitly in the local inventory, rather than silently assigned a
rarity interval. The main-game-only scope excludes plugin override resolution,
new DLC resources and X-Tech's different properties.

## Native evidence chain

Pinned retail 1.16.244.0, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Static VAs below use preferred image base **0x140000000**; RVA is VA minus that
base. Object/row offsets are hexadecimal. ESM physical offsets are decimal.
`iNN` means ignored `.local-work/recon/e1-intervals-NN.tsv`; `aNN` means the
existing arithmetic export. No native function was invoked.

| Link | Decisive evidence |
|---|---|
| CONT PRPS → BGSPropertySheet | i07 loader 140a1a140: 140a1a6d0 compares 53505250 (little-endian PRPS); 6f6..714 selects CONT+118, adds 8 for sheet storage and calls 140452e20. i05 140a19cd0 independently returns base+118 for the component descriptor. |
| Raw value → native row | i04 140452e20 at 140452f70..fb7 reads 12-byte entries, preserves value bytes and calls append 1404536c0. i05 140453727..72a copies the value to native row+10; no subtraction/default normalization. Copy 140453740 at 7d4/821 preserves the float as well. |
| Base component retrieval | a12/a13 1409403e0 calls component descriptor 14044b590, resolves existing component or provider fallback. i01 binds its descriptor to BGSPropertySheet; i05 independently maps CONT component to +118. |
| Base property → getter | a07 140b82b40 resolves the base sheet through 1409403e0 and returns matching row+10 at 140b82bf8. Its separate +108 pointer comparison is Health: i08 14049a430 returns singleton 1461de020; i09 140d96b20 at 140d971f6..209 initializes +108 from the named Health registration (decompiled name Health, index18). That branch is distinct from WorkshopHarvesterRateMultAV. |
| Default + properties | a06/a14 140b6cfa0 starts AVIF+178 at 140b6d00d, can return an explicit instance base override at 03d, otherwise adds ExtraE1 contribution at 0d9 and base-sheet return at 104. AVIF loader 140d9d170's NAM0 binding was established in a17/a18. |
| Effective value → duration | a06 effective getter 140b6ce20 adds modifier total after base getter; earlier constructor evidence binds reference+70 virtual slots. 140f7c000 / scheduler 140f7f1e0 retain positive effective AV or 1 and multiply timer duration. |
| Resource → seconds / quantity | Existing 140f7bd20 reads IRES-linked interval global and multiplies by 3600f; 140f7dfa0 at 140f7e1cc..1ec ceilings resource base AV for registration. These accepted arithmetic contracts are preserved. |

The new rows extend the existing [native function register](../native-availability-map/functions.csv).
They are observed internals with analyst aliases, not validated integration APIs.
Definition links are DEFINITION-DERIVED; loaded overrides and effective values
remain unobserved, and the persistence classification of those states is not
reassigned by this study.

## Provenance and publication

Bethesda's installed Starfield.esm, SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`, and pinned
retail code are the primary sources. The owned strict ESM reader, independent
physical checker, prior extractor catalog and Ghidra reader supply methods;
there is no outside implementation reuse or new dependency. All raw definitions,
model paths, decompilation and analysis databases stay LOCAL-ONLY. Authored
interpretation/tables remain REVIEW-REQUIRED. Independent acceptance is distinct
from maintainer review, integration and publication permission.
