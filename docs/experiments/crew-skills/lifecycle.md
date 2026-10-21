# Assignment, effects and saved ranks

[Admission](native.md), [actual rank rows](saved-ranks.csv), [CR1 assignment witnesses](../crew/current-witnesses.csv), [native locators](functions.csv). STATIC sequencing and historical SAVE evidence are separate. No historical sample was loaded or resaved.

## From recruitment to the first possible consequence

1. Recruitment/quest progression supplies availability and may grant/increment a skill. The ten selected compiled quest fragments contain40 actual AddPerk operations with exact installed VMAD identities; an unused property does not grant anything. Normal rank mutation changes one actor/perk rank, then dispatches or queues entry removal/registration through1418c4f00/1418c50a0. A granted rank can precede active entry registration when that work is queued.
2. Normal assignment1404076b0 checks/deduplicates the actor handle, removes another owner's relationship through140407a10, updates the destination E2 list and keyed CrewAssignment and removes availability. Owner/list mutation is native work in the operation; Papyrus assignment/travel/role notifications are separate downstream work. See [CR1](../crew/lifecycle.md). Repeatedly assigning the same actor does not append a second ordinary contribution.
3. Type1 ability refresh140408bb0/14040a230/14040a9d0 can apply destination effects after environment/rank/competition checks; magic-effect work may be queued. Old destination removal and competing-actor replacement are distinct operations. A type2 timing entry does not become an applied destination spell through this path.
4. A1 and DB are queried from actor entries **at use time**. Once the new list, relationship and active entry registration are visible, the next qualifying evaluation can consume them. Physical arrival is not an operand of these loops; unresolved handles, the virtual exclusion predicate, nonpositive Health, environment and entry conditions remain gates. CR3 must qualify when real remote actors satisfy them.
5. A timer query and actual item creation are separated by scheduling. The resource row stores interval/remaining values; [E1](../inorganic-extractors/arithmetic-production.md) resets them from current modifiers after due processing. A changed actor is not itself proof that a partially elapsed old countdown was instantly rescaled. Current reason, inputs, due cycles and receiving decide the first observable inventory consequence. No required fixed number of seconds or universal travel delay follows from native ordering.

Unassignment/transfer removes the old owner membership before later per-call folds; ability removal has its own path. Dismissal and generic unassigned-unload cleanup are additional [CR1 role/script transitions](../crew/report.md), not universal synonyms for perk deletion. Normal rank changes unregister the old active entry and register the new; no whole-transition atomicity is proven. A queued rank/ability refresh can introduce transient observations without requiring an invented fixed delay.

## Persistence channels

| State | Classification | Supported correspondence |
|---|---|---|
| Base NPC perk ranks, PERK entries, scripts and resource keywords | DEFINITION-DERIVED | Direct PRKR versus conditional quest grants and template-part inheritance are separately recorded |
| Additional actor owned-perk/rank list | PERSISTED | Actor writer141916b30 marks mask400000 when actor+360 exists and calls1412b60a0; loader141917e40 bit22 calls1412b6eb0. First list writes identities to relocation queue and one byte per rank to body |
| Other two actor perk-state lists | PERSISTED representation; semantic roles not promoted here | Serializer writes a second identity-only list and third identity/u32 list; loaders1412b6eb0/1412b7020 distinguish these from the first ranked list. Duplicate identities across lists are not extra crew bonuses |
| E2 assigned identities, actor4C relationship, available/ship registry | PERSISTED identities / RECONSTRUCTED handles | [CR1 real-save joins](../crew/current-assignments.md) establish positive assigned and available populations independently |
| Active entry-point buckets and selected condition context | RECONSTRUCTED / TRANSIENT | Definition entry pointers and actor buckets are not serialized in the owned-rank wire list. Normal registration and per-call selection are traced; complete restoration ordering/coherence is CR3 |
| Applied ability effects and AV changes | MIXED | A separate magic-effect/AV persistence mechanism can coexist with reconstructed perk registration; no universal “all bonuses saved” or “nothing saved” claim |
| Producer remaining/interval and reason snapshot | PERSISTED row / current recomputation | Existing E1/E2/E3/C3 save maps persist scheduling scalars. They do not identify which historical contributor produced a number or prove the value remains authoritative after load |
| Current evaluated power/capacity/timer factor | TRANSIENT calculation, potentially consumed into other state | Native per-call operands, active entries and current contexts must be qualified separately from saved rank and assignment |

## Purposefully selected real evidence

Start with HIST-0255 (mature Save41) and independent positive assignment HIST-0021/22/24. Widen to HIST-0036, HIST-0077 and Save52 for later named-actor/explicit crew-perk references; none is an absence oracle. Seven protected originals were freshly streamed and typed; every selected Actor row, supported result and failure reason remains in `.local-work/cr2-skills/<sample>-ranks01.json`.

| Sample / actor | Positive saved information | Remaining boundary |
|---|---|---|
| HIST-0255 Lin005639 | Ranked list9729786..9729791: Demolitions1 at 9729787, Management3 at 9729788; keyed assignmentff047885 and reciprocal E2 | Actual current entries, Health and output unobserved |
| HIST-0255 Heller00563c | Ranked list9732032..9732037: Geology1 at 9732033, Engineering3 at 9732034; same keyed owner/reciprocal E2 | Geology's presence does not create an A1 entry; actual effective producer context unobserved |
| HIST-0024 Vasco0057be | Fusion1/Shields2/EM1 at 7919722/23/24; installed ACHR NAME0057bb independently confirms base | Assignment parser does not close that leading-extra branch; rank evidence remains useful without invented assignment |
| HIST-0255 Moara29c982 | EM2/Marksmanship2 at 11014101/02; fresh installed ACHR NAME015df3 confirms identity | Assignment remains UNKNOWN in this acquisition |
| HIST-0255 Barrett005788, Sam29d488, Andreja0059a9 | Independently framed saved available registry from CR1; positive unassigned-roster inputs | This suffix reader rejects their layout. Actual possessed rank remains UNKNOWN, not inferred from direct base grants |
| HIST-0021/22/24 Lin/Heller and later comparisons | Positive assignment where independently decoded; unsupported/no explicit extra-rank block reported | Missing explicit additional rank list is not zero skill and not unassigned. Definition inheritance and other state can supply ranks |

All ranges are decimal decompressed-stream offsets, end exclusive. Identity tokens/FormIDs are interpreted through each save's plugin/reference tables. They are not current handles, runtime addresses or compressed-file offsets. These historical snapshots are observational, potentially affected by mods/patches; they are not a controlled action/no-action chronology.

## Independent tail boundary and fail-closed limits

The new [pure decoder](../../../research/cr2-skills/saved.py) uses typed buffer153 Actor framing and CR1's native-backed private header. It derives the perk-block **end from the independently framed record end**, not from finding an expected rank byte pattern. In the qualified branch, the native suffix is translated vector12 + raw12 + clock flag1/float4 + optional bit25 vector12 + terminal Boolean1 =42 bytes. `140acc660/740` verify the vector/queue split; `141a154d0/155d0` verify the clock; writer141916b30 and loader141917e40 verify order. Body and relocation queue cursors are separate.

The diagnostic enumerates possible starts of the native three-list grammar ending at that boundary, requires a unique nonempty rank list, known PERK identities and closed counts/queue scope. Neither quest expected ranks nor specific Lin/Heller byte patterns are acceptance predicates. It reads the second identity list and third u32-list independently. It does not name those two lists “removed” or “active bonuses” without further proof.

Wrong type/version, unsupported mask/clock, truncation, non-PERK identities and ambiguous framing fail closed. General active/base-rank census, all possible Actor trailing layouts, every default/alias reconstruction, automatic E2/4C repair, and final loaded effect coherence remain OPEN. These limits do not erase the explicit saved ranks now recovered. No live pair or observer is required to establish those existing positive facts.
