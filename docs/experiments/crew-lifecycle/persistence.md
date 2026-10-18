# Saved participants and ordinary reconstruction

[Answer](report.md), [all corpus decisions](corpus.csv), [all E2 members](instances.csv), [qualified generic instances](witnesses.csv), [native lifecycle](native.md). The saved evidence is observational, potentially mod/bug affected, and does not establish a linear controlled history. Sample IDs retain CR1's frozen HIST numbering.

## Search coverage and why these witnesses qualify

CR1 selected203 earlier mature inputs from its278-save inventory before assignment acquisition. CR3 read every retained corpus receipt, preserved all97 build qualification failures as NOT TESTED, and followed **all23 nonempty E2 positive saves** with fresh protected-original reads. The other83 previously supported inputs have no nonempty ordinary beacon E2 in that prior search; they were not freshly decoded again and are not claimed free of assignments. No arbitrary subset or Save52 absence is used as a generic-crew negative.

The new positive reads cover43 E2 member rows. Thirty-five have a decoded reciprocal actor CrewAssignment:32 generic actors with selected template-part evidence, Lin/Heller and one DLC actor whose class is outside this main-game comparison. Eight HIST-0255 members stop on unsupported leading extra9C; they retain positive E2 membership but UNKNOWN actor link/template/rank. Two named rows and the DLC row have no selected generic slot3. There is no claim of43 fully characterized contributors. The principal positive available and ship controls come from the independently bounded CR1 registry, not missing actor links.

For generics, the reader closes the actual Extra2B prefix: source26f937, compact count15, saved selected-slot maskFF5D, queued selected templates, distinct created-NPC identity, zero nested NPC change mask and nested self. It expands enabled mask bits **by slot**, selects slot3's actual queued identity and independently checks that selection from the raw prefix/queue. Native `140cd77d0` selects spell/perk part3; source26f937 has bit3 enabled, selected Engineering/Management/Security bases have bit3 clear and direct PRKR rank1. Other template parts, including appearance and stats, do not create that skill. The selected inherited base grant, not absence of an additional rank list, supports the ordinary reconstructed rank.

| Real saved instance | Independently qualified assignment | Perk source and effect path | Exact decisive locators |
|---|---|---|---|
| HIST-0255 Lin005639 | Reciprocal outpostff047885 | Explicit saved Management3 → entry replay → A1 .87 | Actor9727539;4C mode9729048; rank byte9729788; E2 at6919420. CR2 ranked block9729786..9729791. |
| HIST-0255 Heller00563c | Same reciprocal outpost | Explicit saved Engineering3 → entry replay → manufactured A1 .77; Geology1 has no PRKE | Actor9729833;4C mode9731318; rank byte9732034; same independently read E2. Rank block9732032..9732037. |
| HIST-0021 genericff04e381 | Reciprocal outpostff02a587, beacon2c60e9 | Selected slot3=02e91c → Engineering PRKR1 → ordinary reconstructed base rank → A1 .91 on manufacturing | Actor9769132; slot3 queue byte9769166; createdNPCff04e081;2B9770740;4C mode9770766; owner E2 at4211213. |
| HIST-0024 genericff058402 | Reciprocal outpostff02e122 | Independent Engineering witness, selected02e91c | Actor11352510; mode11354143; nestedNPCff0580ac; exact selected queue offset in witnesses.csv. |
| HIST-0255 genericff084217 | Reciprocal outpostff038542 | Selected slot3=02fdf7 → Management PRKR1 → A1 .95 on eligible families | Actor14263331; slot3 queue14263365;2B14264943; mode14264967; createdNPCff08419b. |
| HIST-0259 genericff0192bc | Reciprocal outpostff1a461d | Independent Management witness02fdf7 | Actor5088805; slot3 queue5088839; mode5090485; createdNPCff019247. |
| HIST-0255 genericff084219 | Reciprocal outpostff047885, alongside Lin/Heller | Selected slot3=26f93b → Pistols PRKR1; qualifying actor combat, no A1 timer entry | Actor14267739; slot3 queue14267773; mode14269390; createdNPCff08419c. |
| HIST-0024 genericff03f5ac | Reciprocal outpostff02e122 | Independent Security26f93b contrast | Actor10599609; mode10601277; createdNPCff03c3ed. |
| HIST-0255 Sarah005986 | Actual4C targetff02a419 is in saved owned-ship array | Different destination; not a member of Lin/Heller's outpost E2 | Mode9750456; CR1 registry-boundary01 receipt. Effective loaded ship child/name still UNKNOWN. |
| HIST-0255 Barrett005788, Sam29d488, Andreja0059a9 | Positive saved available/unassigned roster | Separate population; no automatic outpost contribution from availability | R1 unit6 roster tokens2195730/34/38; independent world-component successor boundary, CR1 current-roster.csv. |

Every numeric save offset above is **decimal decompressed logical-stream offset**, end exclusive for ranges. It is neither a compressed-file offset nor a runtime handle. Slot3 queue offsets are computed from the independently framed record reference-queue start and selected mask index; mode/rank bytes occupy the separate record body. [Witnesses](witnesses.csv) preserve all32 generic rows rather than only attractive examples. These are21 Engineering,2 Management and9 Security snapshot witnesses across23 saves, not32 independently observed recruitments.

Physical ESM rereads confirm source NPC26f937 at26186570, Engineering02e91c at22295650, Management02fdf7 at22303797, and Security26f93b at26189829. These are original ESM-file offsets, distinct from decoded-save offsets. The verification receipt records exact PERK rereads too. Full payloads remain local.

## Saved inputs to transient consumers

| Item | Persistence class | Reconstruction and authority boundary |
|---|---|---|
| Owner ExtraE2 count and saved actor identities | PERSISTED identities, RECONSTRUCTED handles | Loader1404089e0 reads count,140306e40 remaps identity/casts Actor/obtains handle. Failures produce sentinel. Runtime capacity, array pointer and owner field are not wire identities. |
| Actor CrewAssignment26beac in4C | PERSISTED explicit relationship, MIXED default context | Mode0 restores handle representation; mode1 differs. The getter can consult Extra80/defaults; saved reciprocal agreement is strong ordinary input evidence, not a universal conflict-repair proof. |
| Generic Extra2B source, selected template slots, created NPC | PERSISTED reconstruction inputs | Saved selected part3 closes the earlier template-candidate gap. Nested NPC zero-change branch plus current definitions reconstruct base grants; unsupported nested changes remain rejected. |
| Main NPC PRKR/PERK entry/scalars/conditions | DEFINITION-DERIVED | Actual selected template gives the perk-bearing base. Installed main-ESM values do not audit every historical/current plugin override. |
| Lin/Heller additional selected perk ranks | PERSISTED rank identities/bytes | Actor writer141916b30/private mask400000 →1412b60a0; reader141917e40 →1412b6eb0. Queue identities and body rank bytes have distinct locations. Missing explicit block never means zero total rank. |
| Other two actor perk-state lists | PERSISTED representations, roles only partly classified | Native loaders distinguish identity-only and identity/u32 lists;1412b62f0 null pruning is not evidence of an additional universal crew contributor array. |
| Active per-actor entry buckets | RECONSTRUCTED / TRANSIENT | Actor finalization clears buckets then BB0 replays base and additional ranks. Process storage, actor validity and service execution are prerequisites. The serialized owned-rank block is not bucket pointers. |
| Effective A1/DB value | TRANSIENT query | Current E2 actors, state, active entries and context supply each fold. No separate persisted all-outpost timing aura is required by these consumers. This is a scoped mechanism, not absence of every possible magic-effect record. |
| Type1 applied ability/AV effects | MIXED | Separate assignment-driven application/removal and magic-effect persistence may coexist; do not substitute this for type2 entry reconstruction. |
| Producer row interval/remaining/pending/eligibility | PERSISTED-capable row, current recomputation | Saved historical scalars resume as scheduling inputs where restored; later due branch recomputes interval. No contributor identity is encoded by the scalar alone. |
| Physical arrival, graphics and process state | Current TRANSIENT state plus other persisted actor inputs | Assignment/position does not reveal current eligibility or active entry storage. No historical save was loaded here. |

The ordinary required order is: identities/forms and selected NPC context become usable; actor assignment context and selected ranks restore; appropriate process storage exists; entry replay completes; a current E2 actor resolves and passes gates when the consumer runs. OwnerE2, actor4C and active entries need not be restored in one transaction. A premature query can lack an effect without disproving its saved rank. Complete global scheduling/concurrency, defaults disagreement repair and actual loaded coherence are not proven by this local chain.

## Remaining evidence and materiality

1. **Actual remote actor process/bucket retention.** Need actor identity/handle generation, process level, process+8 and A1 entries at the same remote interval reset. This decides whether a real remote actor takes the supported contributing or missing-storage branch. Ordinary actor3D absence alone does not discriminate them.
2. **Actual save-load settled participation.** Need the same positive named/generic actors after ordinary load, with restored E2/4C, selected rank, active entries and current Health/state. Native reconstruction is established; execution/order for these historical samples is not witnessed.
3. **Realized output.** Need due-row scalars, elapsed caller, current reason/inputs and destination inventory delta over a matched transition. A nominal factor or restored interval is insufficient. This is material to a production guarantee, not to identifying the ordinary query mechanism.
4. **Unsupported8 E2 members, overrides and conflicting/default state.** Extend only if exhaustive membership/current actor classification is required. Their positive owner-list identities remain retained; the32 qualified generic positives do not depend on resolving them.

Any live discriminator requires a separate approved bounded brief. No new missing generic witness is required for the present saved-instance comparison; no universal runtime, importer or publication claim follows.
