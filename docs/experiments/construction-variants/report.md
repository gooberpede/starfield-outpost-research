# BM1: construction-component variants and dynamic configuration

2026-10-20, Australia/Sydney. SOR-EXP-0060 / SOR-EV-0068.
[Authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_BM1_construction_component_variants_dynamic_configuration.md),
[plan](plan.md), [review and frozen criteria](review.md).
Authored interpretation REVIEW-REQUIRED; proprietary/private evidence LOCAL-ONLY.

| Element | Answer |
|---|---|
| Question | What selects, changes and preserves construction-component variants? |
| Best-supported answer | Ordinary hab-wall CHANGE cycles condition-eligible entries in a **Snap Behavior (STBH)** category. Its ordinary alternatives are **PackIns**, generating an interior/exterior assembly linked back to the original component anchor. Automatic connection rules use the same action machinery with a different, ungrouped selection path. Initial geometry comes from the construction's PackIn templates. Foundation/stair generation, material swaps, animation and destructible stages are distinct mechanisms. |
| Confidence | Proposed STRONG STATIC/SAVE for the ordinary hab mechanism and positive saved assembly/connection joins. Exact action history, loaded rendering and extension implementation are untested. Independent disposition is in review.md. |
| Coverage | Freshly pinned main-game definitions and existing static analysis; all physical main-ESM STBH/STMP/STND populations; selected nested construction templates and five mature protected originals. No effective override/load-order merger or exhaustive player-object inventory. |
| Evidence | [Behavior census](behaviors.csv), [ordered rules](behavior-rules.csv), [definitions](definitions.csv), [native pins](functions.csv), [saved replacements](saved-replacements.csv), [source hashes](sources.csv). Decisive native and save examples follow below. |
| Limits | Floors/ceilings lack a demonstrated ordinary CHANGE catalogue in the inspected primary assembly; storage material definitions do not establish a decal picker. Ship definitions share the snap vocabulary, without transferring terrestrial input/owner/persistence guarantees. |
| Next step | Review the frozen criteria and exact patches. Optional paired CHANGE/reload observation requires a separate live authorization; no new save is requested by this assignment. |

## What an ordinary wall change actually changes

Four Wall Hab PKIN `00051f54` uses cell `00051ecf`. Four placed templates
`002c8c95`–`002c8c98` use component PKIN `00068f6d`, whose SNBH points to
STBH `001e8d95`, **OB_OPI_HabSmWalls01**. This is a child-component catalogue,
separate from the COBJ that constructs the hab. The behavior has 14 ordered
entries: seven ungrouped automatic rules, three entries in connected-wall
category `00178b01`, and four entries in unsnapped category `00068f5e`.
The last four choose three window PackIns and a plain wall PackIn. Their number
is a complete count of these physical entries, not of every possible hab or
every runtime-eligible choice.

Manual selection goes through `1421f4f30`, CycleBehaviorEvent, StateInspect's
handler `1421aec70`, StateCycleSnapBehavior entry `1421b2030`, and
`1421e48e0`. Candidate discovery/validation is `1421f0e80`, `1421f0b00`,
`140a316c0`, `1421f09a0` and `1421f0fc0`. These are **preferred static VAs**
on the pinned executable, image base `140000000`; they are not runtime pointers.
[The complete trace](manual-and-automatic.md) explains the predicates and failures.

The executor `140a32780` distinguishes replace (0), remove (1), and add (2).
The hab-wall rule chooses a PKIN, so replacement reaches `140b4d650`'s PackIn
branch: clear the previous replacement, create the target assembly at the anchor
transform, link generated references through keyword `00000191` to the anchor,
and propagate Workshop membership. The outer hab representative is not a newly
purchased hab. Interior and exterior pieces belong to the selected wall PackIn;
they are not independently interchangeable sides by default.

There is also a **different branch** for an ordinary non-PackIn base:
service `1418c1f10`/`1418cafc0` reaches the reference's base setter
`140b4d430`, preserving its reference identity and recording OriginalBaseObject
extra B4. That branch must not be substituted for the installed PKIN wall case.
This corrects an early investigation lead before documentation completion.

The mapped manual action has no COBJ ingredient check or resource withdrawal.
It updates construction members and refreshes item representations; it is not
the full placement transaction. [L2 budget](../build-budget/native.md) separately
filters replaced anchors and sums selected members. No claim follows that any
custom replacement is free of budget, collision or attachment consequences.

## Automatic geometry and other families

Connections `140904d60` and disconnections `140904f30` maintain reciprocal snap
relations and apply/revert behavior. Automatic `140a31050` evaluates **ungrouped**
rules against the actual two-reference context. Manual cycling uses nonzero
categories and can coordinate both connected sides. A visible doorway therefore
need not be a manually chosen catalogue entry or a whole-hab replacement.

[Mechanism taxonomy](mechanisms.md) and [extension map](extensibility.md) distinguish:

- Hab floors/ceilings: fixed/nested assembly geometry in the primary Four Wall
  Hab, with no equivalent grouped floor/ceiling rule demonstrated by its graph.
  Hex-stack foundation behaviors are a counterexample to a blanket claim that
  horizontal architecture cannot adapt.
- Airlock stairs: STBH action **3**, dispatched by foundation construction
  `140f5bd50`/`140f5bb30`, with support/snap-node and generated-child relations.
  This is separate from manual wall category cycling.
- Cargo components: fixed compartment identities/models and operational
  animation events on marker/light scripts. Their cargo pairing/inventory
  state is not a construction appearance selection.
- Storage appearance: real LMSW keyword/material-path collections exist,
  including warehouse white/red/blue declarations. This does not establish a
  selectable storage decal catalogue, nor an arbitrary persistent decal API.
- Damage: actual breakable-wall definitions have Health thresholds and
  stage-specific models. Damage/repair uses Health, destruction and model-swap
  state rather than the wall CHANGE category. No DEST exists on the inspected
  ordinary hab wall replacement definitions; importing breakable-wall behavior
  into them is an untested extension.
- Ships: ShipBehavior wall/door/hatch definitions use the same STBH/STMP/STND
  component vocabulary. Ship assembly and restoration contexts remain distinct;
  ordinary outpost CHANGE and Workshop identity rules do not transfer wholesale.

## What the saves establish

HIST-0210 positively joins one hab group `ff01a791` to four component anchors.
Replacement groups contain PKIN `001dcf7f` (window 1), `001dced4` (window 2),
`001dd05d` (window 3), and `001dd0b8` (doorway). Their actual geometry references
share the owner's WorkshopItem edge and link back to the corresponding anchor
with key `00000191`. Anchor `ff01a78f` has a counted DE connection to
`ff01a7b8`, node indices 6/8. [Exact offsets and limits](saves.md) distinguish
these save-local identities from runtime handles and current rendered state.

These are positive saved associations, not four snapshots of the user's pictured
wall. The photographs have no paired save/reference identity. Saved PKIN/child
identity, anchor flags, DA grouping, 4C links and DE connections jointly encode
the representation; a missing standalone “variant index” does not erase it.
Native reconstruction reads those channels. No rendered reload was performed.

## Prior work, rights and interpretation boundary

The [prior-work basis](methods.md) retains Workshop membership/population
corrections, L1–L3 admission/accounting, DA1 existing-reference repair, SD1/SD2
inventory/source distinctions, and the earlier Build Mode readiness audit.
None is silently promoted. No power-wire or furnishing preservation guarantee
is inferred merely because the hab's outer root survives.

Bethesda installed data/code/scripts and maintainer saves/screenshots are primary
inputs. Existing project-owned readers/exporters are reused under SOR-P-0002;
Ghidra/Temurin, CPython/stdlib and Git retain their prior tool provenance.
No outside implementation, download, licence acceptance, external contact,
fork/PR or disclosure was introduced. Game-derived source/native/asset/save
payloads remain local. No mod, game launch, observer, debugger, save/configuration
edit, static-analysis mutation, staging, commit or push occurred.
