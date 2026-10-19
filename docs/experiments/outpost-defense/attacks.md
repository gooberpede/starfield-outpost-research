# Initiation, lifecycle and Armillary correspondence

[Answer matrix](report.md), [locators](evidence.md), [contributors](defenses.md).
All script descriptions below are checked against shipped PEX, not accepted
solely from development comments. PEX offsets address uncompressed member bytes.

## Ordinary causal trace

1. Main-game beacon ACTI `002c60e9` attaches OutpostBeaconScript and binds
   SQ_Parent to quest `0007092c`. Its compiled OnLoad arms StartAttackTimer;
   OnWorkshopObjectPlaced does so only when the new object's GetValueResources
   array is nonempty. The compiled timer range is **12 to 48 seconds**, ID 1.
   The source's commented 120/480 alternative is not the shipped constant.
2. OnTimer calls SQ_Parent.CheckForAttack with ordinary arguments
   `(self, false, 0, 0.0)`. The full compiled function has instructions starting
   at member byte offsets **43725–45106** (the last call's operands follow). It rejects
   AllowAttacks=false, different current planet, or no ancestor location bearing
   LocTypeMajorOrbital. These gates also precede forced/test arguments and the
   Starborn special case. There is no distance-to-player calculation here.
3. The ancestor planet location holds LastAttackRoll AV `0024f6a0` and
   LastAttack AV `00127239`. Nonzero prior roll requires at least **0.04 game
   days** since the roll (0.96 game hours, despite the source's rounded “1 hour”
   comment); an ordinary prior attack requires **7 game days**. Both use
   Utility.GetCurrentGameTime, not the timer's seconds or the planet's local day.
   LastAttack<=0 admits the first attack. These timestamps are shared by checked
   outposts on the same ancestor location, not independent per-beacon clocks.
4. After special cases, it sums only positive values of MB_Parent.resourceAVs.
   Installed MB_Parent supplies **111** entries; OutpostCargoLinkAV is
   `000a46ff`. In ordinary notation, the human/creature selection threshold is
   `A = 0.10 + 0.01 * R + 0.05 * C + S`. `R` is that AV sum, not inventory
   wealth, visible buildings, elapsed output or a rate independently measured
   here. `C` is the current cargo-link AV. The installed sole special case uses
   its own event, so it does not add to `S` on that branch.
5. One RandomFloat(0,1) draw chooses creatures when `roll <= 0.08`; otherwise
   humans when `roll <= A`; otherwise nothing. With R=C=S=0, that predicts about
   8% creature-event requests and 2% human-event requests per eligible ordinary
   draw, not 8% plus 10%. A failed quest/alias selection is not an actual attack.
   There is no explicit A clamp, defense subtraction or population term in this
   complete function. It stamps LastAttackRoll after the ordinary selection,
   even when neither event is requested. Cooldown early returns do not stamp it.
6. Script events carry **akRef1=the checked beacon**. Installed story branch
   `00349c9f` has keyword-conditioned nodes `00349ca1` (ordinary humans),
   `0034d3e7` (creatures) and `00349ca0` (Starborn). The ordinary human node
   offers `00341fcd`, `000418b8`, `0008708e`; the creature node offers
   `00361a85`, `00361c0e`, `00361c0d`, `003076fa`. These are actual node NNAM
   relationships, not names alone.
7. Human quest alias **231** OutpostBeacon fills from script-event **R1**
   (ALFE SCPT, ALFD R1). Alias 232 creates AttackTarget marker base `0000003b`
   at alias 231. Landing-location conditions include distance from that beacon
   using global `00341fcf` (**2000 native distance units**) and condition form
   `00341fd0`, with landing/encounter marker eligibility. This is a spawn-location
   bound, not a 2000-unit player radius or a guaranteed landing in every terrain.
8. VMAD attaches OE_ShipsAddonScript, DefaultGroupSpawnQuestScript and
   SQ_OutpostAttackHumansScript. Quest start calls LandShip. Compiled generic
   spawn setup/Spawn reaches SpawnGroupReference, puts returned actors in the
   configured aliases/collections and sends SpawnEvent. The human handler sets
   attackers' Aggression to 1; actor arrival in the outpost location calls
   Actor.AttackOutpostObjects and StartAttack. The installed attackers collection
   has travel-to-target package `00346853`. Actual ship landing, spawning and
   combat success remain conditional, not observed in this assignment.
9. AttackOutpostObjects native binding `141fc53a0` requires a valid actor process
   and a valid outpost beacon, then follows that beacon's reverse WorkshopItem
   links. Native `141fe1740` admits references whose flags have bit **24 set**
   and destroyed bit **23 clear**, invoking `1419ce030` for each admitted target.
   GetDestructibleOutpostObjects uses the same flag filter in `1420c02b0`.
   This is positive attack-specific targeting of destructible Workshop objects;
   it is not proof that every hostile prefers these over every actor in combat.
10. If the attack has started and living attackers remain, AttackTarget.OnUnload
    obtains those objects and calls SetDestroyed on each whose Is3DLoaded is
    false. OnLoad instead reissues AttackOutpostObjects. Building during an
    active human attack starts a separate **3 second** retarget timer. An
    ordinary damage trace and this direct destruction shortcut are distinct.

The attack base class stamps the planet's attack timestamp on quest start and
again on StartAttack when enabled. Cleanup is **event-driven**: its subscribed
RECheckForCleanup stops the quest if all attackers are dead or the target's
current planet differs from the player's. REParent.SendCleanupEvent dispatches
that custom event. Different-planet cleanup is not a guarantee it precedes the
human target-unload handler. No unseen remote dice-based outcome is invented.

Creature quests use their own installed biome creature collections and travel
package `00361c0f`. Their compiled handler randomizes collection choice/count,
enables the selected collection and stops if no populated choice exists. The
human-only unloaded-object destruction override is absent from the complete
creature subclass and base. Roaming/prespawned creatures that happen to enter an
outpost are not thereby instances of these event-selected quests.

## Rearm and clocks

The beacon timer is **one-shot** in this mapped script: OnTimer does not call
StartAttackTimer again. The complete beacon's call sites are OnLoad and the
resource-bearing placement branch; OnUnload handles crew travel and does not
cancel/rearm this attack timer. Therefore the 12–48 second setting does not
define a periodic universe-wide polling frequency. Another load or qualifying
placement can arm another opportunity. Waiting/travel can advance the game-day
cooldowns, but these functions do not contain a wait-hours catch-up loop that
rolls once per missed interval. VM timer/load scheduling itself was not executed.

## Armillary and Starborn

The positive special-case correspondence is:

`Armillary mount construction/resource -> CheckForAttack eligibility ->
 CNDF 002baa4b -> separate 50% roll -> keyword 00349c9e -> node 00349ca0 ->
 quest 00349c9c -> shared human arrival/target/unload machinery`.

Installed SQ_Parent VMAD at property-relative bytes **5206–5335** configures one
special struct: chance **0.5**, condition `002baa4b`, event `00349c9e`.
The condition requires MQ204 (`002c6d74`) stage **620** done and the event
outpost's MQ_ArmillaryResourceAV (`001f36bf`) **>=1**. The ordinary timer calls
this before production/cargo probability. A successful SendStoryEventAndWait
that returns a quest ends CheckForAttack immediately, before the ordinary draw
and its LastAttackRoll stamp. If it returns no quest, ordinary selection remains.

PKIN `001ec78c` and mount ACTI `001ec794` each define Armillary resource 1;
the PKIN also defines Armillary build-count resource `001f818a`. The installed
special quest repeats condition `002baa4b` on the event reference. Its VMAD
sets **CountsAsAttack=false** (bytes 713–732); the installed stage-50 fragment
calls StartAttack(false). Thus the shared base TimestampAttack is suppressed
for this quest. The ordinary seven-day eligibility gate still runs **before**
the special roll; a previous ordinary attack can therefore suppress the check.
There is no additional Starborn cooldown in this mapped branch. That is not a
claim of unlimited real-time attacks: one-shot arming, quest availability and
landing eligibility remain prerequisites.

MQ204ArmillaryMountScript handles placement/removal by building/packing the
linked Armillary and starting MQ00's **0.5 second** reconciliation timer with
the owner Workshop. MQ00 checks the Workshop's Armillary resource; placement
retains Armillary/mount aliases and sets MQArmillaryLocation to 1 for ship or 2
for outpost; removal clears aliases and sets it to 0. The outpost attack
condition reads the resource, not that global or just possession of artifacts.
Consequently a bare artifact inventory or an attractive Armillary model does
not satisfy this positive outpost-specific mechanism. Reloaded effective
resource/alias coherence and exceptional relocation are unobserved; no
claim is made that every Starborn encountered near an outpost used this quest.

## Player-presence and remote-state matrix

| State | Initiation | Ongoing damage | Unload/distance and save/reload boundary |
|---|---|---|---|
| At a loaded outpost | Load/qualifying placement can arm one check; eligibility and landing selection still apply | Human arrival can explicitly target destructible objects; ordinary combat also exists | STRONG STATIC, no DA1 live observation |
| Exploring the same traversable terrain | Same-planet predicate can pass; standing in the build circle is not required | Surviving attackers can continue; target unload has a positive shortcut | Exact player distance/residency at timer/landing selection is not captured |
| Different terrain region on the same planet | No direct region-equality gate in CheckForAttack; valid nearby landing-location aliases still required | Previously running quest may persist until cleanup | No assertion that every distant beacon is loaded, armed or gets a usable event |
| On a different planet | Explicitly rejected before ordinary and Starborn rolls | Existing quest's cleanup requests Stop on the next cleanup event | Target-unload destruction can be a separate earlier callback; relative ordering OPEN |
| In orbit/ship interior | Depends on actual GetCurrentPlanet identities, not the colloquial label “off-world” | Same conditional attack/cleanup rules | No orbit-equivalence observation or guarantee |
| Wait/sleep/travel | Advances game-day eligibility, but no missed-roll replay in this script | Travel may unload targets or provoke cleanup | No elapsed-time abstract damage calculation in the mapped selector/unload resolution |
| Save/reload | Native state/script VM can restore inputs; a subsequent OnLoad can arm a new opportunity | Saved Health/destroyed state is distinct from quest start/resume | Actual timer remaining time, alias resumption and callback ordering in selected saves NOT TESTED |

All positive/negative logic entries are STRONG STATIC within the named script
and native paths. None is a newly observed runtime sequence. The user's reported
nearby attacks are compatible with this model; their lack of recalled remote
attacks is not used as absence evidence.
