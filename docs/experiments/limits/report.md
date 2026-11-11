# L1: numerical construction and environmental admission

Ordinary outposts start with **eight deployment slots**. Planetary Habitation
ranks 1–4 set the base allowance to **12/16/20/24** and progressively permit
extreme temperature, pressure, toxic/corrosive atmosphere and extreme gravity.
The scanner's native admission gate reads the player's remaining allowance and
the actual planetary condition form. Successful ordinary beacon placement
subtracts one slot; ordinary removal restores one.

At each selected outpost, regular and inter-system cargo pads share **three
construction slots**, increased to **six** by Outpost Management rank 1.
All seven installed turret recipes share **six slots**; no ordinary skill
increase was found in the bounded definition/script census. These are native
admission checks, with object-card counts and rejected build actions, rather
than a periodic eviction rule. Six is a configured ordinary threshold, not an
unmodifiable engine ceiling.

2026-10-19, Australia/Sydney. SOR-EXP-0051 / SOR-EV-0059.
[Brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_L1_numerical_perk_limits.md`),
[frozen plan](plan.md), [native explanation](native.md), [save corroboration](saves.md),
[recipe census](recipes.csv), [category census](categories.csv),
[function register](functions.csv), [source pins](sources.csv), [review](review.md).
Proposed STRONG / STATIC with bounded SAVE corroboration; authored
REVIEW-REQUIRED, primary game/native/save payloads LOCAL-ONLY.

## Limits matrix

In this table, **G** is the shared COBJ JNAM gate described in native.md:
current selected-Workshop construction representatives, grouped by the exact
limit-global pointer, compared with its current nonnegative floored value.
It is not grouping by menu category or summing PackIn children. **P** is the
scanner/player deployment and planetary-condition gate. No live run was made.

| Category | Scope | Base value | Perk/definition changes | Counted entity | Enforcement | UI feedback | Persistence inputs | Confidence / coverage |
|---|---|---:|---|---|---|---|---|---|
| Outpost deployment | Player across bodies/systems | 8 | Habitation 1/2/3/4 sets base 12/16/20/24 | Remaining player AV; ordinary placement/removal -1/+1 modifier | P: `140f387f0`, consumed by `140f38a40`; successful build `1421b2e20` | Max-number message; scanner remaining count and availability | Player base/modifiers and reconstructed references; observed beacon total alone is insufficient | STRONG STATIC; effective loaded/saved player allowance not decoded here |
| Regular + inter-system cargo pads | Selected outpost, one shared group | 3 | Management rank 1 quest stage 701 adds installed integer 3 | Constructed pad assembly representative | G, global `00190d57`; both COBJ recipes | Shared n/max card; status `1f` blocks ordinary build | Saved construction identity/owner and mutable global | STRONG STATIC; actual Save52 groups of 1–6, mixed types |
| Turrets | Selected outpost, shared ballistic/laser/compact group | 6 | No ordinary threshold increase found | Direct constructed turret representative | G, global `000f7c96`, seven recipes | n/6 card and status `1f` | Actual historical turret actors; complete owner join remains open for the sampled pair | STRONG STATIC; two actual saved bases corroborated, ownership gap explicit |
| Landing pads | Selected outpost, shared variants | 1 | No ordinary increase found | Assembly representative | G, `0022f4c9`, four installed recipes | n/1 and status `1f` | Saved assembly/root/owner | STRONG for G; catalogue includes conditional Starstation recipe, not four universally available choices |
| Transfer Container | Selected outpost | 1 | No ordinary increase found | Constructed container | G, `002ce192`, COBJ `002ce193` | n/1 and status `1f` | Reference/base/owner, global | STRONG STATIC; no joined saved witness in selected roots |
| Mannequins | Selected outpost, shared display variants | 6 | No ordinary increase found | Construction representative | G, `003f4aee`, 23 installed recipes | n/6 and status `1f` | Saved/default construction and global | STRONG for G; conditional/zero-NNAM definitions retained, not all claimed available |
| Memorial easels | Selected outpost, shared companion variants | 1 | Quest availability conditions are additional | Constructed easel | G, `0007875a`, four recipes | n/1 and status `1f` | Quest progression, reference/base/owner, global | STRONG bounded definition/native chain; no sampled save witness |
| Armillary mount | Selected outpost for G; additional quest conditions | 1 | No skill change found; COBJ carries quest-stage OR conditions | Constructed mount | G, `001f818b`, COBJ `0023baa6` | n/1 and status `1f`, plus recipe availability | Quest and construction state | STRONG for numerical G; complete Armillary quest/lifecycle is outside this census |
| Crew Stations | Selected outpost | 3 | Management rank 3 adds 3 | Station assembly, separate from crew slots | Reuse [CR1 capacity](../crew/capacity.md) | Shared native card/build gate | Saved station roots; effective capacity is separate | Existing CR1 scoped result reused |
| Robots | Selected outpost | 3 | Management rank 2 adds 3 | Construction, separate from operating/assigned actor count | Reuse [R1 limits](../robots/limits.md) | Shared native card/build gate | Saved actor/root/owner and global | Existing R1 scoped result reused |
| Harvesters, generators, ordinary storage, builders and other no-JNAM recipes | Selected menu/context | No JNAM numerical quota | Research, recipe, resource, placement and other gates remain separate | Not counted by G without JNAM | Bounded negative: G skipped when recipe+178 is null | Other statuses can still reject placement | Definitions plus saved constructed objects | STRONG for absence of this quota in the census; no claim of unlimited construction under every engine gate |
| Extreme environment | Current reference's planetary context, perk rank on player | Non-extreme categories allowed | Rank 1 temperature; 2 pressure; 3 atmosphere; 4 gravity | Four AND-connected condition groups, each benign OR sufficient rank | P -> CNDF `002dfd42`, BodyHasKeyword and GetPerkRank | Missing-skills message; scanner can keep action available to explain failure | PNDT/default and body-associated keyword sources; actual selected rank | STRONG STATIC; saved body examples are corroboration, not a historical admission trace |

## Census and completeness

The fresh main-ESM walk covers **all 3,009 COBJ records**. Exactly **51** carry
JNAM, all among **576** records whose editor ID contains `outpost` (case
insensitive). They form nine global groups: 7 turrets, 4 landing pads, 8 robots,
23 mannequins, 4 easels, 2 cargo pads, and one each Armillary, Crew Station and
Transfer Container. The remaining **525** name-selected recipes lack JNAM.
The accompanying CSV preserves every candidate, including test assets, missing
menu categories and condition counts; editor naming does not prove ordinary
availability. This is exhaustive for the physical COBJ/JNAM census of this ESM,
not an exhaustive playable-object or winning-load-order catalogue.

Positive category coverage includes all 204 harvester-category recipes, 11 power
recipes, 16 storage recipes and 12 builder recipes without JNAM. The Transfer
Container belongs to storage by name but has its own JNAM and miscellaneous
menu category; it must not be hidden inside an “unlimited storage” statement.
Different generators and storage sizes do not acquire a numerical allowance
merely from their common menu keyword. Limits for research/resources, recipe
availability and local placement remain independent.

All **5,033** installed development PSC members were searched for the named
threshold globals and deployment AV. The only direct named references occur in
PlayerSkills. Its shipped PEX was freshly fully decoded, and installed quest
VMAD values were read rather than substituted from source defaults. This is
support for the ordinary skill changes above, not proof that every possible
native writer, unnamed property or mod is absent. Native code supplies the
actual construction and planetary admission mechanisms.

## Worked cases and persistence

These are native-supported **predictions**, unless a SAVE witness is named.

- Two regular pads plus one inter-system pad fill the baseline quota; another
  pad of either kind is blocked. Management rank 1 raises the threshold to six,
  leaving three places. Save52 owner `ff01bf2a` actually has four regular and
  two inter-system supported assembly roots; owner `ff025f95` also has six.
- Four ballistic plus two laser turrets fill the same six-slot group. Replacing
  a model is not a fresh six-slot allowance; ordinary removal releases its
  representative before a later build. Death/disablement is not a condition in
  the count helper and does not itself prove slot release.
- An ordinary new character has base 8. With five successful unreimbursed
  placements and no other modifiers, remaining allowance is 3. Learning
  Habitation rank 1 sets base 12, leaving 7 under those same modifiers; it does
  not add a further 12. Effective allowance <=0 rejects the next entry.
- Deep Freeze plus Extreme Gravity requires rank 4: rank 1 passes temperature
  but still fails the gravity group. High pressure alone is not the Extreme
  pressure keyword. Airless bodies are not automatically forbidden by these
  four groups. Kreet's installed keywords pass with no Habitation rank.

The category count is RECONSTRUCTED from currently resolvable construction
items. Thresholds are DEFINITION-DERIVED plus mutable global state; deployment
is MIXED player AV state. Persisted references are not a serialized authoritative
current counter. The six saved scans corroborate actual beacon/turret presence
and contrasting populations, not post-load coherence or a perk-loss experiment.
The sampled player's extras stop before the relevant AV at unsupported E7/96;
therefore no claimed exact historical deployment allowance follows from counting
disabled-clear beacons. Existing membership completeness qualifications remain.

Above-limit saved or scripted populations are not automatically removed by the
mapped admission code. A lowered quota blocks new admissions while the existing
construction list can remain. Skill-stage Mod/SetValue operations are distinct
from continuously recomputing a limit from a perk tooltip; removing a perk does
not, by itself, establish reversal of an earlier quest-stage global/base change.
Environment predicates read current rank for a new beacon admission, but no
environment-driven eviction is present in the inspected construction/load paths.
Arbitrary scripts, stale UI state, exceptional disable/destroy cleanup and
general modded over-limit load behaviour are not runtime validated.

## L1 / L2 / L3 boundary

L1 is this numerical and body/environment admission study. **L2** separately
owns the thin overall Build Limit meter, complexity accounting and any
triangle/draw-call explanation. **L3** separately owns local site restrictions,
POI/city exclusion, clipped/intersecting build circles, 150-unit territory,
dynamic actor/static collision, harvestables, PackIn scenery, terrain and
rocks/trees returning after travel/reload. Native dispatches into location,
current-cell and preview validation are identified without decoding their
geometry or importing Fallout 4 mechanics as Starfield facts.

No calculator, importer, gameplay mod, live observer or safe integration point
is delivered. A live perk-loss/over-limit control is optional only if its actual
behaviour becomes consequential; this study does not authorize it. Review and
publication/integration permissions remain independent of scientific confidence.
