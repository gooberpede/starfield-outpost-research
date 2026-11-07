# Outpost defense

A beacon loading or a qualifying placement can schedule an attack check.
An eligible check can request an encounter, which still needs a usable quest
and spawn setup. Turrets, crew and robots can affect combat without supplying
a defense score to the mapped attack selector. Build Mode's **Integrity**
indicator reports a separate condition, the selected object's current Health
relative to its permanent Health on the supported paths.

[Technical reference](../reference/defense.md) ·
[Attack and damage study](../experiments/outpost-defense/report.md) and
[independent review](../experiments/outpost-defense/review.md)

## When an attack can start

| Situation | Mapped consequence |
| --- | --- |
| Beacon loads or an object with a nonempty value-resource list is placed | The beacon can arm one random check 12–48 seconds later. The callback has no periodic self-rearm. |
| Callback runs | Attacks must be allowed and the player's current planet must match the qualifying planet context. Prior checks and ordinary attacks can suppress a new check through shared game-day timestamps. Standing in the build circle is unnecessary for this predicate. |
| Outpost has Armillary resource and the quest stage qualifies | A separate 50% roll can request a Starborn quest before ordinary selection. This is per eligible check. A successfully returned quest skips ordinary selection and does not stamp the ordinary attack cooldown. |
| Ordinary selector runs | Positive production-resource actor values and the cargo-link value affect the draw. A requested human or creature encounter still needs a usable quest and spawn context. |

These are shipped script and definition paths on 1.16.244.0. The seconds
describe an opportunity timer, the days describe planet-location cooldowns,
and the percent describes a conditional draw. Observed raid frequency and the
order of every travel callback remain open.
[Attack decision trace](../experiments/outpost-defense/attacks.md)

## What defenders can change

Turrets and combatants can matter once enemies engage. The selector does not
read their counts or an aggregate defense value. In the mapped human attack
path, surviving attackers matter even after the target unloads. If the attack
has started and an eligible destructible object's 3D is absent, the unload
handler can set it destroyed directly. Starting a check on another planet
fails the ordinary same-planet gate. An attack already in progress can reach
unload and cleanup through separate callbacks.
[Defense contributors](../experiments/outpost-defense/defenses.md) ·
[Presence and unload cases](../experiments/outpost-defense/attacks.md#player-presence-and-remote-state-matrix) ·
[Crew and robots](crew-and-robots.md) · [Power](power.md)

## Read the object's condition

A historical large He-3 extractor stores a Health damage modifier of −144.
With permanent Health 400 under the pinned definition and no other override,
that gives 256 current Health and predicts an Integrity ratio of 0.64.
Another same-base object at the same owner has no saved Health override and
predicts full Integrity under the same premises. The comparison supplies
neither an attack history nor a recorded screen state. If the denominator is
unavailable or nonpositive, the card hides the indicator.
[Saved contrasts](../experiments/outpost-defense/persistence.md#purpose-selected-corpus-and-controls)

Partial damage can coexist with a clear destroyed flag. Destruction, disabling
and deletion have separate state channels. The ordinary repair action has
eligibility checks and works on the existing construction, restoring qualifying
Health damage and clearing destroyed state. Partial damage alone does not
establish repair-menu eligibility. The study mapped repair without observing
a live repair or reload.
[Damage and repair](../experiments/outpost-defense/integrity.md)
