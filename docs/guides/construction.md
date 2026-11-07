# Construction and placement

**Why can an object appear in Build Mode but still fail to build?**
The menu discovers recipes and shows eligible choices or certain locked
ones. Confirmation passes a different set of checks for the selected
candidate, including materials, budget, quota, territory, support and
collision. In the traced Starfield 1.16.244.0 ordinary route, confirmation needs
an accepted placement status before it creates the object.
[Catalogue and admission trace](../experiments/build-catalogue/eligibility.md).

## From a recipe to a placed object

A recipe's first menu keyword can put it in a configured category. Its
target can be a list with several choices under one icon, as with chairs.
The selected leaf is a prospective object. Some unmet research and perk
conditions leave a visible lock. A failed quest condition can hide an
entry altogether. Even an unlocked chair can fail at the proposed position.
[Catalogue and conditions](../experiments/build-catalogue/report.md).

Quota and budget can stop a build independently. A quota counts items in
a selected outpost that share a recipe limit global. Regular and inter-system
cargo pads share three slots by default, six with the documented Management
rank change. With budgeting enabled, the Build Limit gate compares
accumulated usage plus the candidate charge with the selected allowance.
The meter shows a rounded usage ratio. An assembly can consume several units.
The Kreet beacon-only checkpoint has **one root and seven usage units**.
Placing a new beacon also has its own player deployment allowance and
environment gate. [Numerical limits](../experiments/limits/report.md) ·
[Budget and saved counterexample](../experiments/build-budget/saves.md).
See [crew and robots](crew-and-robots.md) for robot quota and human slot
cost, and [defense](defense.md) for turret condition and repair.

## Why moving the preview can change the result

Location and encounter restrictions can block a candidate within the nominal
radius. Objects and terrain can also obstruct a position. An eligible rock
can enter the preview's clearing set as the candidate moves, leaving the
physics query with one fewer obstruction. A nearby actor ordinarily does
not pass the same scenery selector. This explains how deeper overlap can
succeed in the mapped mechanism. The pictured Kreet rock's exact identity,
pivot and hit list remain unverified.
[Spatial mechanism and screenshot limits](../experiments/spatial-placement/report.md).

The saved construction can include an owner, placed references and local
positions. Confirmed scenery suppression has its own saved change state.
Preview fade and physics results are transient. The game has a restoration
path, but the historical report of a rock returning after travel or reload
has no matched before-and-after witness. The drawn border also reflects
loaded territory and cannot stand in for the complete placement test.
[Scenery persistence and open incident](../experiments/spatial-placement/persistence.md).

## Changing a choice or changing a wall

Cycling a chair before placement selects a prospective recipe leaf. CHANGE
on an existing ordinary hab wall instead selects a Snap Behavior rule.
The inspected wall replaces generated pieces around an existing anchor,
with the outer hab still representing the construction. Snap connections can
also select automatic rules. A separate native branch can override an
existing non-PackIn reference's base. The saved hab evidence records
different replacement groups on different sides. Paired CHANGE and rendered
reload behavior remain unmeasured.
[Variant mechanism and witness](../experiments/construction-variants/report.md).

The [construction reference](../reference/construction.md) maps the stages
and provides a recipe-quota check. See [identity](identity.md) for how the
saved roots are counted, [nominal biomes](nominal-biomes.md) for the difference
between coverage and usable territory, and [resource generation](resource-generation.md)
for the extractor's separate local resource requirement.
