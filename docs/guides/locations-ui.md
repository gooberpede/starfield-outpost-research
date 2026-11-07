# The Locations outpost panel

The Locations outpost panel combines a list of qualified Workshop entries,
copied summary badges and separately requested information about the selected
body. Use it to find a listed outpost and read the collected summary.
Selecting a row can repaint old badge values while the map and body details
update through another provider.

[Technical reference](../reference/locations-ui.md) ·
[Field-lineage study](../experiments/locations-outpost/report.md) and
[independent review](../experiments/locations-outpost/review.md) ·
[Stored Resources guide](stored-resources.md)

## Read each badge in its own units

| Display | What it counts or describes |
| --- | --- |
| Outposts Built | Entries admitted from the registered Workshop collection, over the player's base outpost maximum. Placement uses its own effective remaining allowance. |
| Cargo Links | Resolved, enabled local endpoints that meet the summary's active-link test. A pair spans endpoints. A built pad or counted endpoint does not establish a currently operating route. |
| Crew | Assignment handles in the Workshop's list, which can include auto-assigned robots. The badge cannot tell you how many actors are present, charge slots or supply skill effects. |
| Total and Needed Power, Production, Build Limit | Copied Workshop summary values. Production is a nominal rate. Budget comes from usage and allowance. Inspect actual power, output or placement through their respective systems. |

The collector resolves the Workshop registry and excludes entries under its
decorate-only keyword rule. Registration and the screen's filters define this
list. An arbitrary saved beacon record or a current physical census uses
different evidence.
[Identity](identity.md) · [Cargo](cargo.md) · [Crew](crew-and-robots.md) ·
[Power](power.md) · [Collector and fields](../experiments/locations-outpost/field-lineage.md)

## Read the map as a schematic

The detail panel uses the selected body's containing system. Faction comes
from the resolved location owner and faction category. Level comes from the
mapped system location's data. These describe system context. They give
neither the player's level nor a measurement of combat difficulty at the
selected outpost. The upper crosshairs mark the selected **system**. The
orbital view draws the system's star, planet and moon hierarchy and
highlights the selected **body**. These providers supply no surface image
of the beacon site.
[Metadata and graphics](../experiments/locations-outpost/native-and-ui.md#assetdata-selection-and-technical-boundary)

For example, changing selection can show another entry's copied Crew badge
and request that body's faction and level separately. The panel's visible
values can therefore come from different refresh epochs. The mapped
retail 1.16.244.0 paths explain that separation without identifying the
exact refresh times of the historical screens. For the separately
collected inventory rows, see [Stored Resources](stored-resources.md).
[Refresh paths](../experiments/locations-outpost/native-and-ui.md#refresh-boundaries)
