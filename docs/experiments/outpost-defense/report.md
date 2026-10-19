# DA1: outpost attacks, defenses and Integrity

2026-10-19, Australia/Sydney. SOR-EXP-0054 / SOR-EV-0062.
[Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_DA1_outpost_defense_attacks_integrity.md),
[frozen plan](plan.md), [review/package](review.md).

| Question | Best-supported answer | Confidence, basis and coverage |
|---|---|---|
| What causes ordinary attacks, and how often? | A beacon load or placement of a resource-bearing object arms a one-shot random 12–48 second timer. Its callback checks the same planet, permission and planet-wide cooldowns, then rolls from production-resource values and cargo-link count. This is an opportunity check, not an attack every 12–48 seconds. | STRONG STATIC: shipped PEX, installed properties, story nodes and attack quests. Actual encounter frequency is unmeasured. [Attack trace](attacks.md). |
| Must the player be at the beacon? Can attacks occur off-world? | The check requires the player's current planet to match; it does not require standing within the build circle. Nearby landing/spawn-location eligibility further restricts whether a quest starts. An already started human attack can destroy unloaded destructible objects when its target unloads while attackers survive. | STRONG STATIC for these explicit paths. Different-planet initiation is rejected; orbit and all same-planet terrain configurations are not equated. Event ordering during travel remains unobserved. |
| What does an outpost Armillary change? | After MQ204 stage 620 and with positive Armillary resource at the checked outpost, a separate 50% special-case roll can start a Starborn quest before the ordinary roll. It shares eligibility but has its own event/quest and does not stamp the ordinary seven-day attack cooldown. | STRONG STATIC. This is a per-eligible-check probability, not a measured arrival rate or a universal trigger. [Armillary trace](attacks.md#armillary-and-starborn). |
| Do defenses lower the chance or resolve attacks numerically? | The mapped selector reads resource AVs, cargo links and the installed Armillary special case. It reads no turret, tower, crew, robot or aggregate defense score. Human unload resolution checks surviving attackers and destructible objects, without a defense-versus-attack score. | STRONG bounded negative supported by complete relevant script functions and native target collectors. Physical combat can affect whether attackers remain alive. [Contributor matrix](defenses.md). |
| What is Integrity? | The Build-mode card publishes current effective Health divided by permanent Health. Destructible nonactors obtain definition Health from their destructible component; actor turrets use actor Health. A missing/nonpositive denominator gives the hidden sentinel, not a measured zero-health object. | STRONG STATIC plus positive SAVE damage. Small Iron extractor and solar defaults are 200; fueled generator 300. Ordinary storage and cargo compartments inspected here have no destructible component. [Object matrix](integrity.md). |
| What happens at damage/destruction and repair? | Partial damage is retained as a negative Health damage modifier. Zero-health destruction and explicit SetDestroyed are separate from disable/delete. Ordinary native repair restores Health damage, clears destroyed state and refreshes the existing construction and owner. The mapped repair action has no ingredient-removal or repair-cost check. | STRONG STATIC for the traced ordinary action; no live repair was performed. Production and power consult invalid/destroyed state; passive storage inventory/link movement has different gates. [Native chain](integrity.md#damage-and-operational-consequences). |
| What is saved? | Five partially damaged owned devices in HIST-0255 retain Health damage in ExtraBF. Other selected snapshots provide undamaged serialized-state controls. Native serialization/restoration separately covers AV modifiers, form flags and keyed ownership. Both historical turret actors now have qualified explicit Workshop owner joins. | PROVEN sampled bytes; STRONG SAVE/STATIC interpretation. No saved attack cause/history or repair transition is claimed. [Persistence](persistence.md). |

The user reports attacks near a visited outpost, occasional Armillary-associated
Starborn and possible watchtower utility. These are SOURCE-REPORTED observations,
not controlled trials. The supplied Kreet screenshot directly shows an Iron
extractor with a full Integrity bar, operating cost 5 and nominal 100/hour.
It does not identify a damaged object or establish an attack, repair or reload.

The useful distinction is **off-world initiation versus damage after leaving an
attack already in progress**. The first is rejected by the mapped scheduler;
the second has a positive scripted unload path. Neither a lack of remote attack
notifications nor remote production proves that distant outposts undergo the
same combat simulation as loaded ones.

Coverage is pinned retail 1.16.244.0/main ESM, 38 fully closed shipped PEX members,
selected native functions and four purpose-selected mature saves. Native
addresses are preferred static hexadecimal VAs at image base `140000000`;
subtract that base for RVA. FormIDs and decimal decoded-save offsets are distinct.
[Evidence and exact registers](evidence.md) identify primary material and checks.
No new RUNTIME observation or safe mod interface is delivered. Authored synthesis
and metadata are REVIEW-REQUIRED; proprietary/save/movie exports remain LOCAL-ONLY.

Concrete remaining gaps are historical attack authorship of damage, actual
travel/unload/cleanup event order, loaded effective overrides and exact saved
quest/timer resumption for these snapshots. None prevents the scoped ordinary
causal explanation above. A prospective discriminator is specified in
[persistence.md](persistence.md#remaining-gaps-and-prospective-discriminator);
it was not executed and supplies no live authority.
