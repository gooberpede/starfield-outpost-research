# Native cost, admission and accounting

Reader notation: [vtable versus object offsets](../../reference/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../reference/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer](report.md), [save correspondence](saves.md), [UI](ui.md).
`nNNN` means `.local-work/l2-budget/native/NNN.request.tsv`. Function/register
locators include exact line ranges, hashes and capped-export flags. Addresses
are hexadecimal **preferred static VAs**, image base `140000000`; subtract it
for RVAs. Fields are hexadecimal memory offsets, never save offsets.
Fresh EXE SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
retail file version 1.16.244.0; ESM SHA256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Every native export repeats imported-program SHA/base/language provenance.
Decompiler types sometimes misidentify float returns; XMM instructions control.
No function was invoked against Starfield.

## Charge operands and efficient evaluation

`140f4c7f0` (n005) receives an effective form and computes:

`charge = multiplier * (baseCost + applicableSurcharge + navmeshSurcharge)`.

BaseCost is INI setting `fBudgetBaseCost:Workshop`, initialized to 1.0 by
`14015a0d0`; allowance fallback `fBudgetBaseline:Workshop` initializes to
2500.0 at `14015a100`. `140306090` establishes INI-setting registration/storage
at object+8. These are compiled defaults, qualified by loaded overrides.
The three inspected installed/user INI files have no matching overrides;
this is not proof of every possible runtime or load-order override.

The alternative surcharge branches test form+2e: 4b adds actor setting; 24
adds the form's property selected by actor-value registry+80 times container
setting; 27 adds light setting. `140a179f0` returns a navmesh-bearing component
for types 1e/25/2f at +1a8, 29 at +138, 2a at +110 and 41 at +e8; nonnull
adds the navmesh setting. This is a component-presence query, not a traversal
of navmesh triangles. The branch labels do not establish that a passed NPC_
base is a runtime Actor: the actor comparison is literally type 4b.

| Setting | Native value slot | Compiled default | Installed main GMST value |
|---|---|---:|---:|
| fWorkshopBudgetActorCost | 145f0c870 | 1 | 000ba33d = 0 |
| fWorkshopBudgetContainerCost | 145f0c890 | 1 | 000ba33e = 0 |
| fWorkshopBudgetLightCost | 145f0c8b0 | 4 | 000ba33f = 0 |
| fWorkshopBudgetNavmeshCost | 145f0c8d0 | 1 | 000ba340 = 0 |

n003/n007 establish registration and setting type; fresh physical ESM records
and EXE constant reads are in definitions01.json/settings01.json. Compiled
defaults alone would give the wrong normal installed surcharge operands.

Multiplier lookup uses DFOB object 145f0be40, resolved value slot 145f0be88
(`140158670`). Valid AVIF type 6d enables property-sheet lookup. Initial
multiplier is 1; with a sheet, a zero result falls back to AVIF+178. No sheet
leaves 1. The main ESM census has no matching WorkshopBudgetMultiplier_DO
binding; do not fabricate a nonnull pointer from the registration name.
`1405ddbd0/14044b670` are component/property lookups. Actual overrides/selected
forms matter; there is no mesh/render measurement in this arithmetic.

`140f4c770` first filters the **reference**, then obtains its effective form
through `140b4cd10` and calls that arithmetic. It returns zero for the positive
`140f3ce30` marker/model predicate, a resolving 191 replacement relationship
(key slot 145e612f8), `140f3ced0`'s property/keyword predicate and the configured
OutpostPackinCollisionPrimitive keyword. n017 binds the latter DFOB at
145f0aa90+48; the adjacent OutpostInteriorCollisionPrimitive DFOB is a distinct
slot. The exact marker predicate tests virtual+820, base virtual+228/model
flags, light/base flags or the finite form-type selector `1405daca0`.
It is not a room/portal visibility or triangle-count query. Unknown broader
meaning of those virtuals is not replaced by a claim that every invisible
reference is free. n007/n022 retain the actual branches.

SingleWorkshopItem vtable 144c25298+1d0 resolves `140f64b00`: resolve its
representative handle at +50 and apply the reference filter/calculator.
PackIn vtable 144c254a0+1d0 resolves `140f6e260`: iterate handle count+50 /
array+58, skip failed resolutions and reference form flag 20, sum surviving
charges. These are selected item members, not all world objects. Generated
foundations/root grouping retain [Workshop rules](../workshop-membership/dependencies.md).
Neither one saved DA dummy nor every saved child independently equals a charge.

`140f33180` calls the item's virtual+1d0 at `140f33500` and stores XMM0 at
context+78 at `140f33506` (n014). Selection/edit construction paths
`140f5c1b0`, `140f62170`, `140f69b90`, `1421e1950` and `1421c8950` call it
(n015/n018). This **candidate-context cache** is the demonstrated cache;
no per-model cached triangle cost is required or established. Re-evaluation
requires selected reference/form/property state and current settings. Repeated
admission reads the stored float instead of rewalking members. A settings change
between candidate initialization and admission is not guaranteed to refresh it.

## Allowance, admission and action

`WorkshopBudgetBaseline_DO` initialization `1401586b0` creates object
145f0be98, value slot 145f0bee0. Main DFOB 00319871 points to AVIF 00319872
WorkshopBudgetBaseline, NAM0 0. `1421dcb10` reads the **selected Workshop's
effective AV** when that pointer is valid and its value >0; otherwise uses
fBudgetBaseline 2500. It does not use the player's deployment AV or L1 JNAM.

Registry builder `140d96b20` initializes current-budget AV at registry+450
from name WorkshopCurrentBudget, index dd (n003 exact registration window).
`140d96680` constructs its form identity as index+700 decimal, hence FormID
**00000399** (n011). The ordinary reference AV owner is reference+70.
Its virtual+8 yields base plus modifiers (`140b6ce20`); base getter
`140b6cfa0` first consults explicit BF, with default/definition paths after it.

At `1421dcc0f..1421dcc80`, enabled budgeting rejects when `U+C > M` and
writes frame+620. Equality is admitted. bBudgetEnabled false bypasses this
gate. `140f3f9a0` converts it to status **1e**, while L1 category full is 1f.
Other failures can take precedence. `140f7ba90` case 1e selects localized
sWorkshop_EXCEEDED_BUDGET (n021). `1421b2360/1421b2e20` require frame+193 ==2
before ordinary construction (n020). This is action enforcement through the
preview state, not a claim of a second atomic cap check in every factory.

Full means `U=M` for the exact ratio; a **positive** C then fails. A zero-cost
candidate can still fit at equality. When already U>M, ordinary nonnegative
C fails this comparator. Negative/NaN/artificial values are not a supported
gameplay contract. The examined load and existing-item reconstruction do not
iterate deleting content in response to U>M; supported ordinary retention is
scoped to those paths, not every scripted event in the game.

## Mutations, movement and restored state

`1421de3f0` snapshots context+78, invokes item virtual+A0, and only on success
calls `140f4c980(C, selectedWorkshop)` (n006). That helper, when enabled and
C>0, reads current effective U and sets the AV's **base** to U+C. Virtual+50
on the reference owner forwards through `14038a200` to virtual+20,
`140b6d190 -> 140b6cbe0 -> 1419af7c0`, obtaining BF and upserting a base row;
the reference change mask includes 80000000. Base replacement using effective
U is not a promise about arbitrary externally applied persistent modifiers.

Ordinary `1421de660` calls item virtual+1d0 at `1421de838`, then
`140f4ca70` at `1421de841`, before ordinary cleanup, when its special argument
is zero. This helper sets base to max(U-C,0), again only enabled and C>0.
It obtains deletion cost afresh; it does not retrieve an immutable price paid.
The nonzero special branch skips this debit. Such removal paths must not be
treated as synonymous with a saved disabled/deleted bit.

Move/rotate operation `1421b1450` removes/rebuilds selected wrapper maps and
transforms without either budget mutation helper. Candidate rebuilding can
refresh its cost; changing position alone does not add a second construction.
Kreet S6/S6C directly corroborate unchanged saved U after solar movement.
Move-related replacement/exceptional scripted operations beyond that ordinary
route retain their own conditions.

The [saved actor-value channel](saves.md) supplies U after load.
BF writer/loader `1419aec20/1419aeff0` store/restore AV identities, masked base
floats and a separate three-modifier section (n017); this is the independently
reused E2 persistence grammar, freshly exported here. It is **not** necessary
to infer U by recounting all saved REFRs. Existing root reconstruction
`1421c6f90 -> 1421c71b0` rebuilds wrappers from ownership/grouping; it does not
call the new-placement budget debit or discard over-budget roots. Thus ordinary
restoration reuses the saved counter, while candidate cost and display ratio
are recalculated. A universal repair/recount after arbitrary damage is not shown.

ExtraWorkshop's summary+7c..+90 is transient/reconstructed in this path.
Its complete writer `140f50660` and reader `140f50880` serialize resource/object
lists, name, +78 ordinal, +60 transform and +98 state, **not** the +7c summary.
The +78 ordinal here is ExtraWorkshop memory, unrelated to context+78 cost.
The previous E1 summary-persistence UNCLASSIFIED statement is refined for this
pinned ordinary serializer only, without rewriting historical evidence.

Changes to U or M can affect the next admission/ratio calculation. Accounting
emits refresh type 4; selected-owner entry emits type 5. Queue processing and
summary publication are separate, so immediate display freshness after an
arbitrary console/setting mutation is not promised. Existing cost values are
not a renderer performance measurement or a safe mod integration interface.
