# Robot contributions versus human crew

[Report](report.md), [catalogue](catalogue.csv), [CR2 consumers](../crew-skills/native.md),
[CR3 lifecycle](../crew-lifecycle/native.md). All examples are conditional
predictions from installed definitions and native instructions, not measured output.

The installed robot category has eight direct NPC constructions. Garden `04297c`
owns Garden `04297e` rank 1; Sanitation `0bd67e` owns Sanitation `04297f` rank 1;
Model A01 `1f416e` owns Engineering `21b8c8` rank 1; Model A02 `1d9250` owns
Management `21b8c3` rank 1; Model A03 `1d924e` owns outpost Fusion `20d24f` rank 1.
Security minibot `04297d`, Model S01 `1d8ee5` and Model A04 `337eab` have no direct
PRKR and have spell/perk template bit 3 clear. They therefore supply no demonstrated
ordinary A1 production or DB generator bonus. Their combat function is outside
this parcel. An ancestor Model A01 pointer in another template part does not grant
Engineering to them. Model A01's enabled part 3 points to `09b33e`; CR2's full NPC
and template analysis finds no additional crew skill there.

Each recipe's CNAM is its NPC, not a PKIN. The recipe/category census, all direct
grants and template masks are reproduced in [catalogue.csv](catalogue.csv).
CR2's five robots were a useful positive subset, not the complete construction
category. The three additional no-process-bonus variants are a prospective
coverage correction; the original CR2 report and its evidence remain intact.

| Robot | Exact selected operation | Supplied target/category | Ordinary consequence |
|---|---|---|---|
| Garden | A1 operation 3, binary32 approximately .91, rank 1 | Organic producer keyword `2c5a95` | Shorter qualifying greenhouse/husbandry interval; not every extractor or fabricator |
| Sanitation | A1 operation 3, approximately .91, sole selected rank 1 entry | Nonmanufactured and nonorganic; solid/liquid/gas family alternatives `299548/29954a/299549` | Shorter qualifying inorganic interval |
| Model A01 | Engineering A1 operation 3, approximately .91, rank 1 | Manufactured producer keyword `23ceb6` | Shorter qualifying fabricator interval |
| Model A02 | Management A1 operation 3, approximately .95, rank 1 | The five installed ordinary resource families | Shorter matching inorganic/organic/manufactured interval |
| Model A03 | DB operation 2, selected rank 1 has three alternative entries | Generator base PowerGenerated `0000032e`, bands below 6 / 6–below 12 / 12+ | Add 1 / add 2 / add 3 to each qualifying generator |
| Security / Model S01 / Model A04 | No possessed ordinary process perk demonstrated | Bit 3 clear, no direct PRKR | No A1/DB bonus from the ordinary definition; no invented production/defense-wide aura |

The full condition metadata remains in CR2 [entries.csv](../crew-skills/entries.csv);
R1 physically rechecks the selected ESM records. These are selected rank 1 grants:
Garden's defined ranks 2/3 are not automatically earned by construction. Neither
lower-rank summation nor a union of ancestor perks is justified. Current mods,
external grants and historical overrides would need separate qualification.

The actual chains are shared where demonstrated:

1. Placement script's AssignCrew reaches `142068d70 → 1404076b0`, owner ExtraE2
   and actor Extra4C CrewAssignment. Finalization/rank changes register the
   selected type 2 entries, rather than applying a permanent destination spell.
2. A1 `140f7bd20` enumerates that owner's E2, resolves an actor, checks life-state
   and Health, then `140c94060 → 140c93cf0` tests active storage, assignment
   environment 2, selected rank and producer-base conditions. Operation 3
   `140c94430` multiplies the accumulating duration. Player entries follow.
3. Scheduler `140f7f1e0` uses the old interval/remaining for due cycles, then adopts
   current modifiers at interval reset. [E1 arithmetic](../inorganic-extractors/arithmetic-production.md),
   [E2 stages](../organic-facilities/native.md) and [E3 stages](../fabricators/native.md)
   still govern reason, inputs, insertion and realized output. Faster timing
   changes neither recipe ingredients nor product count per successful cycle.
4. Power `140669880 → 140f3dd50` visits E2 actors with analogous state gates and
   dispatches DB per actor. It accumulates additions per generator. It has no
   separate player dispatch, unlike A1. [P1](../power/fuel.md) controls generator
   rating, fuel charge and subsequent allocation.

Two eligible Model A03 robots at a base 20 generator give `20 + 3 + 3 = 26` before
other AV modifiers. With a −10 modifier they give 16: bands use base 20, not the
modified 10. Preliminary base+modifiers at or below zero bypasses the crew fold;
the robots cannot revive base 20 with −20 into positive generation. At a base 6
generator the same two robots give `6 + 2 + 2 = 10`. This is not a single shared
+3 pool and does not imply sufficient fuel or actual powered consumers. An
ordinary human/Vasco ship Fusion perk `222f83` is a type 1 ship ability, not DB.
CR2's qualified human grant census establishes no ordinary human holder of `20d24f`.

Two Model A02 robots on an eligible inorganic producer give `.95² = .9025` of
baseline duration. Adding Lin's saved rank 3 Management gives `.9025 × .87 = .785175`;
an eligible player rank 4 Management factor .5 gives `.3925875`. The reciprocal is
the rate multiplier, not the duration reduction itself. Identical robot effects
stack because different E2 actors are dispatched; repeated assignment of one
actor is deduplicated by normal insertion.

On manufacturing, Model A01 .91 and Heller's rank 3 Engineering .77 give `.7007`;
Lin .87 gives `.609609`. Garden contributes nothing to that manufactured target.
On organic, Garden .91 and Model A02 .95 give `.8645`; Model A01's Engineering
fails. Security/Model S01/Model A04 do not supply these factors. Actual historical
participants/active buckets/output were not observed. The examples do not assert
those particular combinations were constructed in a retained save.

Ordinary inter-system fuel-marker family tests still fail these ordinary
production entries under [CR2's explicit negative](../crew-skills/processes.md).
The shared A1 mechanism alone cannot establish a fuel bonus. Storage capacity,
local transfer routing, cargo-link flight clocks and player construction/research
benefits retain their existing separate consumers. No new general robot aura or
robot power-demand gate occurs in the mapped A1/DB admission paths.
