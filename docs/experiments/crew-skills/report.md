# CR2: what assigned crew skills actually change

**Prospective R1 correction, 2026-10-18:** the [eight-variant installed robot category](../robots/report.md) extends the five process-perk robots below with Security minibot, Model S01 and Model A04, whose ordinary definitions have no demonstrated A1/DB bonus. Historical CR2 census/primary evidence remains intact; the five positive process grants are unchanged.

2026-10-18, Australia/Sydney. SOR-EXP-0048 / SOR-EV-0056. Proposed STRONG / STATIC and sampled SAVE findings; authored synthesis REVIEW-REQUIRED, primary payloads LOCAL-ONLY. [Frozen contract](plan.md), [review](review.md).

**Assignment supplies actors to particular consumers; it does not convert every skill in the Crew screen into an outpost bonus.** A displayed skill is a possessed crew-flagged perk. Its selected rank must contain an effect, and that effect must reach a consumer with the right environment, target and conditions. Timers, power, ship capacity, abilities and combat use different paths and combination rules.

The ordinary human outpost bonuses positively established here are **Outpost Management production timing** and **Outpost Engineering manufacturing timing**. Management covers the five installed resource families; Engineering covers manufactured resources. Neither grants the player's construction/research/crew-station benefits. Heller's Geology entry has no native perk-effect entries; it cannot supply the player's Geology extraction mechanics by sharing its name. Payloads has a ship-capacity entry, and ordinary crew Aneutronic Fusion grants a ship reactor ability. They do not directly enlarge dedicated outpost stores or raise outpost generator output.

A consequential exception is a **separate outpost Aneutronic Fusion definition**, `0020d24f`: its native power consumer adds power per eligible actor, and **constructible ModelA03 robot `001d924e` directly possesses it**. This is not the ship skill `00222f83` found on Vasco, Andromeda and generic Fusion Systems Specialists. Rafael's quest fragment has an unused property for the outpost form, but grants Engineering, ship Engineering and Management instead. A property or attractive definition is not a possessed skill. The qualified human recruit-grant census establishes no ordinary human holder of the outpost power form; the robot grant supplies a positive definition-level participant.

| Requested case | Best-supported answer | Decisive difference |
|---|---|---|
| Outpost Management `21b8c3` | Selected ranks 1/2/3 multiply qualifying production duration by .95/.91/.87, per eligible assigned actor | A1 operation3 and resource-family conditions; actual Workshop E2 actors are dispatched |
| Outpost Engineering `21b8c8` | .91/.83/.77 for manufactured products; no ordinary inorganic/organic timing entry | Manufactured keyword `23ceb6` on the supplied producer base |
| Payloads `222f84` | Ship capacity ×1.1 for the selected contributing crew actor; rank selection is strongest qualifying entry rank, not sum of all crew | Ship's own E2 → AA selector; ordinary CONT capacity does not take that path |
| Crew Aneutronic Fusion `222f83` | Type1 ability `198bb6` targets ship reactor AV `198bb8` | Environment1 and destination ability application; distinct from DB power entry |
| Outpost Aneutronic Fusion `20d24f` | ModelA03 robot's additive generator bonus +1/+2/+3 by power band, all at selected rank1 | Environment2, DB operation2, generator context; actual assigned/eligible robot still required |
| Geology `21b8cc` | Displayed role/skill, no PRKE effect entries in this form | Owning/displaying this form supplies no A1/DB/AA entry; configured companion gifts are a separate script path |
| Pistols `27df98` | Actor/weapon damage effects with pistol and player-Isolation conditions; no outpost-wide turret/production aura | Combat consumer supplies attacking actor/weapon/target; any additional crew lookup is the ship wrapper, not an outpost E2 loop |

[Catalogue](catalogue.csv), [population](population.csv), [entry metadata](entries.csv) and [population method](population.md) distinguish positive grants, conditional grants, template candidates, helpers and exclusions. The census is a bounded installed main-game definition result, not every NPC bearing a crew keyword, every DLC/mod override, or a census of loaded actors.

## Stacking is determined by the consumer

The accepted [E1 timer contract](../inorganic-extractors/stacking-native.md) remains intact: different eligible assigned actors multiply duration, even with the same skill. One actor's normal rank transition unregisters the old rank and registers the new rank; it does not sum lower ranks. Player timer entries are evaluated afterward. [Worked examples](stacking.md) use actual scalar payloads and separate predictions from measurements.

Power's DB consumer also visits actors individually, but its operation adds to generator base contribution. Ship capacity uses the highest qualifying crew entry rank and then the selected owner/player actor. Type1 abilities use assignment-driven destination application with competing-rank suppression/removal. A single universal “highest skill wins” or “all crew stack” rule is therefore incorrect.

**The 5-He-3 fuel marker does use A1 timing, but ordinary Management/Engineering entries fail its category conditions.** The freshly inspected fueled marker lacks all five ordinary resource-family keywords. An unconditional selected Constellation Guide timer entry can produce `108 × .95 = 102.6` seconds, subject to current state; that is a player/magazine example, not a crew Management fuel discount. The five-unit ingredient cost does not change with duration. [Process matrix](processes.md) connects this to organic/fabricator stages, power, storage, freight and local links.

## What the real saves add

Fresh HIST-0255 reads recover **Lin's Management rank3 and Demolitions rank1**, **Heller's Engineering rank3 and Geology rank1**, alongside their reciprocal saved assignment to `ff047885` from [CR1](../crew/current-assignments.md). HIST-0024 supplies Vasco's ship Fusion rank1, Shields rank2 and EM rank1; HIST-0255 also supplies Moara's EM/Marksmanship rank2. Nine explicit rank rows across four actors are in [saved-ranks.csv](saved-ranks.csv). These are decoded saved ranks, not guesses from base-NPC perks or quest history.

The Lin/Heller pair therefore provides a real saved overlapping manufacturing-skill example: conditional selected timer factors .87 and .77 would give .6699 of base manufacturing duration. Their saved assignment and ranks do not measure active bucket registration, actor Health/eligibility, current producer state, elapsed scheduling or realized inventory output after load. Earlier mature HIST-0021/22/24 and later comparison saves with no qualified extra-rank block remain **UNKNOWN**, not rank zero. The positive unassigned HIST-0255 roster is independent of missing actor links. [Persistence and lifecycle](lifecycle.md) preserves these distinctions.

## Scope and readiness

Fresh installed executable hash `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, main ESM hash `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`; existing native analysis has that executable SHA and image base `140000000`. All native addresses are hexadecimal preferred static VAs; subtract the image base for RVA. FormIDs and decimal decoded-save offsets are separate domains. [Functions](functions.csv) and [sources](sources.csv) locate primary evidence.

Scientific confidence is proposed STRONG within the traced ordinary mechanisms and qualified saved subset. Coverage and remaining exceptions are itemized in the focused documents. Runtime realization, universal post-load coherence, remote actor residency/arrival/death and safe external integration remain unvalidated; CR3 retains those questions. No game, live observer, save/configuration change, new dependency, network acquisition, staging, commit, push or publication is part of this work. Completion disposition comes from the eight-criterion [independent review](review.md), not this report's own confidence statement.
