# Quantity, effective interval and realization

Reader notation: [vtable versus object offsets](../../audits/publication-readiness-b2/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../audits/publication-readiness-b2/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Report](arithmetic-report.md), [clock contract](arithmetic-clocks.md),
[modifiers](arithmetic-modifiers.md), [source pins](arithmetic-sources.csv).
Native static VAs use base 0x140000000 and the pinned retail executable in the
report. `aNN` below means `.local-work/recon/e1-arithmetic-NN.tsv`.

## Definition-derived base production

The existing IRES binding remains valid: resource AV at IRES+f8, interval global
at +100, recipe at +108. Loader 1409e7900/fixup 1409e8570 are preserved in
[the earlier native reference](production-native.md). New pinned definition
inventory `.local-work/e1-arithmetic/definitions03.json` independently reads the
installed main ESM; full fields remain local. The authored
[reader](../../../research/e1-extractors/arithmetic-definitions.py) uses the
existing strict ESM framing/decompression reader, without outside code.

| Main ESM example | Resource AV / IRES | Recipe / product | Nominal interval and quantity |
|---|---|---|---|
| Small Iron CONT 05ef19, ESM byte 5403487 | 05ef18 / 0057c7 | 05ef53 / MISC 00556e; recipe byte 1300253652 | NAM3 GLOB 05ed87 = .01f hours; resource PRPS = 1; recipe NNAM = 1 |
| Small He-3 CONT 06ac84, byte 5410474 | 05ed85 / 0057f5 | 05ed88 / MISC 00558e; recipe byte 1300251225 | Same common interval global; resource PRPS = 1; NNAM = 1 |
| Small liquid water CONT 27ab66, byte 5784407 | 05ef1e / 0083ec | 05ef6e / MISC 005591; recipe byte 1300256791 | Same common interval global; resource PRPS = 1; NNAM = 1 |

Offsets in this table are decimal physical ESM bytes. The example base/resource
association is definition-derived; it does not identify a live reference.
The three resource AVIFs have NAM0 = 0. Iron's HarvesterRateMult property is absent;
the gas and liquid bases explicitly carry 1. Do not substitute these raw fields
for a current effective producer AV or treat every size as one universal tier.

140f7bd20 reads global+48 and VMULSS 3600f (constant 144f04f78).
GLOB 05ed87's .01f bytes 0ad7233c multiplied in binary32 give exactly 36f.
The prior rarity globals give 54/72/90/108f seconds for the named interval
definitions; resource-to-global association must still be demonstrated.
140f7c1e0 supplies the same global-to-seconds conversion without actor dispatch.
The missing-global fallback reads fResourceDefaultProductionIntervalHours;
no current override was sampled.

Registration 140f7dfa0 at 140f7e1cc..1ec calls producer ActorValueOwner interface at object byte offset `0x70`,
method at vtable byte offset `0x18` keyed by
IRES+f8, VROUNDSS immediate 2 (toward positive infinity), then VCVTTSS2SI.
Its integer result becomes row+0c; the runtime row stride is 1c. New rows start
with zero countdown/interval and cached eligibility from reason==0. The
scheduler loops row+0c times, rechecking current reason on each iteration,
passing the same due-cycle count to 140f7d6a0. Thus for a settled ordinary
quantity 1 row, each due cycle requests one item; a normal N-iteration row
requests N×dueCycles across calls. This is not a universal NNAM multiplier.
An effective resource AV and the registration-time base AV can diverge.

## Effective interval and AV provenance

140f7bf10 (a08) combines 140f7bd20 with 140f7c000. It gets Workshop ExtraE2,
passes the producer's base into the timer and reads producer+70 virtual+8 for
HarvesterRateMult. The timer still folds selected eligible actors, then player,
through A1 operation 3 binary32 multiplication. The [accepted stacking rules](stacking-native.md)
are preserved: distinct assigned actors compose; old/new ranks replace during
normal settled transitions; no whole-transition atomicity or universal restoration
claim. This assignment does not reopen those findings.

The effective value query is now traced beyond its final multiply:

| Native operation | Source contract and decisive evidence |
|---|---|
| Reference AV interface | Constructor 140b21fd0, existing workshop-z-04.tsv at 140b22062..69, installs vtable 144b96a90 at reference+70. a05 reads slots: +8=140b6ce20, +18=140b6cfa0. |
| Effective getter 140b6ce20 | a06: special AV type+160==3 can redirect to resolved owner; ordinary path calls base getter then adds 140b6cb60's ExtraBF modifier total 1419ae7f0. |
| Base getter 140b6cfa0 | a06/a14 instructions: begins AVIF+178; ExtraBF explicit base lookup 1419af700 can return an override; otherwise adds ExtraE1 property value 14044b670 and base-sheet manager value 140b82b40. Instructions VADDSS at 140b6d0d9/104 establish float addition despite bad inferred decompiler returns. |
| Default value binding | AVIF loader 140d9d170 (a17/a18): NAM0 case 304d414e reads up to 4 bytes into object+178. AVIF 008407 NAM0 = 1 supplies the ordinary default. |
| Modifier total 1419ae7f0 | a07: locked per-AV row, sums binary32 slots+8,+c,+10; not a single PRPS scalar or a fresh perk selection. |
| Extra/base property sources | 140b6cb60 selects ExtraBF; 14044b670 selects matching pointer row+10 from ExtraE1; 140b82b40 selects matching base-sheet row+10 under manager protection. These are native provider contracts, not proof of a particular loaded override. |

Scheduler 140f7f1e0's direct effective getter substitutes 1 unless the value is
positive; unordered NaN also fails that ordered comparison. It multiplies the
timer return by the retained value at 140f7f674 and stores both remaining and
interval. There is no “subtract percentage” operation here. Medium/large raw
PRPS −.2/−.5 do not alone establish a loaded multiplier: an explicit base
override can bypass the fallback composition, and modifiers remain separate.
Positive infinity/extreme values are not qualified safe scheduling inputs.

The nominal presentation helper 140f7bf80 (a10/a12) calls producer+70 virtual+8
with IRES+f8, obtains the effective interval 140f7bf10, and returns
binary32((60f/interval)×effectiveResourceAV) when interval!=0, else 0.
Constant 144f04c30 is 60f. This is a rate per minute of the interval's seconds
domain. It reads effective resource quantity, while registration uses ceiling
of a base quantity: these contracts deliberately remain distinct.

Worked baseline: small Iron resource quantity 1, no active timer entries,
HarvesterRateMult default 1 with no overrides/modifiers gives interval 36 and
rate binary32(60/36)=1.6666666269302368 (bits 5555d53f little-endian).
This derives from definitions/native operations; it is not an internal value
captured in the screenshots. For He-3/water the nominal common interval and
quantity 1 are also established; their effective interval is 36×M after any
applicable timer entries, with M from the effective getter above. No guessed
current M is inserted. Illustrative active .95 then .5 with M=1 gives
17.100000381469727 seconds, rounding after each multiplication.

## Requested versus realized items

140f7d6a0 (a01/a10) returns for null resource; its special early object branch
can invoke 1405f7280 and emit ItemProduced before the zero-cycle guard. That
exception is retained. Ordinary selected resource resolves recipe+108 and
recipe+88 product, and 140f7d510 chooses producer or a qualified connected
destination. Capacity predicate 140f7c210 compares effective capacity against
current weight; it can reject producer/linked choices. This does not reconstruct
storage contents or general distribution logistics.

The three input-cap predicates are now identified through constructors/defaults:
140f7cab0 uses OutpostCategoryBuilders_DO (DFOB 23aed1→KYWD2731a0);
140f7cb70 uses OutpostIsFueledGenerator_DO (03e82b→03e82a);
140f7d030 includes that test and OutpostIsFueledCargoLink_DO
(03e829→216f84). See a07/a19 and definitions03. The ordinary inorganic examples
lack those keys. Their direct count path bypasses 140f7f6f0. On the special
branch that helper gathers input requirements, computes floor(available/required)
with VROUNDSS immediate 1, takes an unsigned minimum with requested cycles and
prepares consumption records. Full builder/organic behavior is deferred.

The ordinary insert at 140f7df73..95 supplies destination RCX, product RDX,
reason 9 R8D and requested integer count at stack+20 to 140b64fc0; no NNAM
load/multiply lies on that direct branch. Leveled products instead expand via
1405e9000 then 140b5d040, with a distinct ushort cycle argument and level input.
No universal count formula is imposed on that path.

General insertion 140b64fc0 (a10) calls 140b70a80, which computes a capacity-fit
count using capacity, existing weight and nonnegative item weight, with division
and integer conversion. The outer routine also handles count splitting,
inventory mutation, special item kinds and return/remainder bookkeeping.
Its count handling cannot be reduced to “this many accepted” from the helper
alone. The production caller does not inspect its returned count. Consequently
neither dispatch, a zero/nonzero event nor the requested count proves an exact
destination inventory delta. This is a concrete acceptance boundary, not a
claim that ordinary creation must fail.

After insertion the producer dispatches D8 Add Produced Items for the player,
refreshes and emits ItemProduced with selected count. The existing 502-PERK
census contains no D8 entries. Special Projects 04ce2d contains its .95 timer
entry but no extra-item grant entry. Newly located LVLI 04ce2a/2b/2c are
gas/liquid/solid RareExotic lists using LVLG 04ce2e, whose FLTV is 80.
Their existence establishes configured chance-bearing definitions, not an
active production effect or an exact percentage of extra realized output.

A full strict walk of 3,829,246 main-ESM records excluding NAVI (oversized input
guard) located exact incoming four-byte references to the three lists/perk;
list matches in CELL/NAVM geometry are untyped false candidates, while typed
perk matches are skill-list and recipe/research prerequisites. No typed grant
or use of those three lists was found in that coverage. All 5,033 installed PSC
sources also had no SpecialProjects/OnItemProduced vocabulary hit in this
bounded locator. Compiled-only scripts, dynamic native lookup, other event
consumers and DLC/mods remain outside that negative. No active random extra
quantity mechanism is claimed or fabricated. Raw findings and failed broad
scan are retained locally; see [review](arithmetic-review.md).

## Resource/size continuation — 2026-10-16

The [complete main-game interval mapping](resource-intervals.md) now follows every category-qualified extractor and closes the PRPS loader link. Raw values survive loading unchanged. On the explicit no-override fallback, small solids have factor 1, other small extractors factor 2, medium approximately .8 and large .5. The historical He-3/water base interval of 36 remains correct; their effective fallback interval is 72 when M=2. Previous examples that left M conditional remain preserved above.
