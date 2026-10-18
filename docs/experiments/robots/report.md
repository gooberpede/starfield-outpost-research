# R1: constructible outpost robots, limits and contribution lifecycle

2026-10-18, Australia/Sydney. SOR-EXP-0050 / SOR-EV-0058.
[Frozen contract](plan.md), [review](review.md), [source pins](sources.csv),
[native locators](functions.csv). Proposed STRONG / STATIC ordinary mechanism
with sampled SAVE corroboration. Authored interpretation REVIEW-REQUIRED;
proprietary/native/save payloads LOCAL-ONLY. Independent acceptance is separate
from scientific confidence, integration and publication.

| Required question | Best-supported ordinary-case answer | Decisive evidence and scope |
|---|---|---|
| 1. Which variants and bonuses? | **Eight** direct NPC constructions: Garden, Sanitation, Model A01/A02/A03, Security minibot, Model S01 and Model A04. The first five have process perks; the final three have no demonstrated ordinary A1/DB bonus. | [Catalogue](catalogue.csv), [effects](effects.md). Fresh full robot-category recipes and NPC/perk/template records correct CR2's five-variant subset. |
| 2. How many? | Shared per-outpost construction threshold 3, ordinarily 6 after player Management rank 2's configured +3. It counts constructed items sharing the limit global, not assigned humans or currently contributing actors. Auto-assigned placed robots ordinarily cost 0 human slots. | [Native limit model](limits.md), current-context item reconstruction, actual count/admission and compiled quest/placement paths. No additional robot-number comparator in A1/DB; no ordinary global universe cap established in these paths. |
| 3. How registered/owned? | Direct constructed actor is the single construction's representative. WorkshopItem owner and CrewAssignment are separate keyed relationships; placement auto-assignment uses shared E2/4C insertion with capacity bypass. Ordinary reassignment is disabled by configured AV. | [Lifecycle](lifecycle.md), [eight reciprocal real joins](instances.csv). NPC identity, selected generated NPC and runtime handle remain distinct. |
| 4. What stacks? | Eligible robot A1 timing entries multiply per actor alongside human entries, then player entries. Model A03's separate outpost Fusion adds per eligible robot per generator; ship Fusion is different. | [End-to-end chains and examples](effects.md). Base 20 plus two eligible Model A03 robots predicts 26; manufacturing/Garden/security contrasts preserve target conditions. |
| 5. Remote and exceptional states? | Arrival/3D is not a direct A1/DB operand. Assignment, resolution, life-state/Health and active buckets are prerequisites. Damage/death/disablement can stop contributions without freeing construction count. Deconstruction has native registry and script unassignment cleanup. | [State matrix](lifecycle.md), [count cleanup](limits.md), shared CR3 instruction-backed process/bucket/replay contracts. Historical loaded/remote operating state NOT TESTED. |
| 6. Persistence/restoration? | Actor/base/template identity, Workshop owner and E2/4C assignment persist; definition grants and item counts reconstruct. Actor finalization replays selected base/additional ranks into active buckets. Saved assignment does not serialize a permanent operational bonus. | [Saved/runtime correspondence](persistence.md), eight actual HIST-0255 robots across four mixed-crew owners; 137 readable mature inputs searched after a 278-input metadata inventory. Robot-only witness unavailable in that bounded corpus. |
| 7. Human comparison? | Shared membership, effect dispatch and actor restoration; different acquisition/admission, construction ownership, zero-cost/reassignment configuration and robot-specific target/perk grants. | [Succinct comparison](comparison.md), precise shared native functions and divergences. |

**Configured**, **assigned**, **eligible**, **contributing** and **observed operating**
are separate states. A robot definition configures a potential rank; a real saved
E2/4C join supports assignment. Current Health, life-state, matching environment,
target conditions and active entries qualify an evaluation. Realized product or
power allocation needs its downstream process state. No retained save was loaded,
and no robot's actual running output was measured in this assignment.

## Catalogue correction and coverage

The installed main ESM contains eight nondeleted recipes in the robot limit
category, each with a unique NPC CNAM and no intermediate PackIn requirement.
[Catalogue](catalogue.csv) records exact recipe/base identities, physical ESM
offsets, direct ranks and template-part qualifications. [Effects](effects.md)
records actual selectors and final consumers. This is complete observed coverage
of that installed main-game category, not every DLC/mod/quest robot or any robot
actor bearing a convenient keyword. Vasco, Delta, general NPCs, combat mechanics,
materials and research prerequisites are excluded.

CR2's five process-perk robots remain valid positives. Its census did not include
three additional buildable combat variants, and CR3's eight unsupported `9C` members
are now positively identified as constructed robots with reciprocal links. These
are transparent prospective corrections; earlier evidence/review history remains
unchanged. The new reader adds a known fixed-u32 Extra9C branch before the first
4C; it does not pretend to close opaque actor extra `15` tail or every default/extra grammar.

## Evidence and material gaps

EXE 1.16.244.0 SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Native addresses are hexadecimal preferred static VAs, image base `140000000`;
RVA subtracts that base. Object offsets are hexadecimal. Save locations are
decimal decompressed-stream offsets; ESM locations are physical file offsets.
FormIDs, saved dynamic IDs, handles and pointers are not interchangeable.

The strongest saved participant is Model A03 actor `ff07258a` at owner `ff062012`,
with separately decoded same-owner E2 and actor WorkshopItem/CrewAssignment
edges. Garden has two independent actor identities. Security/combat variants
provide assigned no-process-perk contrasts. Human Lin/Heller and generic
Management/Security witnesses come from the accepted prior CR1–CR3 contracts.
They supply mixed populations and conditional expected effects, not a controlled
intervention or measured stacking.

Material gaps are bounded: no robot-only positive in 137 readable mature saves;
one selected historical ExitSave is unavailable; three process-bonus variants
lack a real saved positive here; actual loaded entry retention/output and every
generic disable/death cleanup route remain unobserved. [Persistence](persistence.md)
gives the smallest future save pair and concrete falsifiers. These do not erase
positive native mechanisms or the eight real joins, nor authorize new gameplay.

All work is offline. No game launch, attachment, observer/plugin, deployment,
save/configuration modification, database content edit, network acquisition,
staging, commit, push or publication is authorized. The task-owned read-only
analysis worker's acquisition/restart deviations and preservation checks are
disclosed in [review](review.md). Completion follows the original eight-criterion
independent decision, not this report's own confidence statement.
