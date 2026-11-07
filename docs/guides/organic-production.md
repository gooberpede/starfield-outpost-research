# Organic production

A greenhouse or animal husbandry facility chooses a product from supported
resources associated with domesticable species on the planet. A resource can
appear in its menu before the player knows enough to select it. Once selected,
the facility still needs power where applicable, enough ingredients from
reachable sources, a due production cycle and an acceptable output receiver.
The species and recipe paths below are mapped for Starfield 1.16.244.0.
[Organic production report](../experiments/organic-facilities/report.md) ·
[Independent review](../experiments/organic-facilities/review.md#independent-review02-acceptance-and-final-review-artifacts).

## Why a product can appear

The greenhouse consults planet-keyed flora records. Husbandry consults the
corresponding fauna records. The mapped consumer checks whether a species can
be domesticated and whether its resource is supported by the facility. It has
no local-biome filter or test for a currently spawned wild creature. A plant
associated with a different biome on the same planet can therefore qualify
when the planet cache contains it. An operator's reported Savannah-to-desert
example is consistent with that mechanism. The evidence does not establish
cache completeness for every visit or planet. [Species and candidate evidence](../experiments/organic-facilities/native.md#candidate-producer-planet-species-domesticability-and-knowledge).

Scanning can reveal a domesticability category for a species on that planet.
The upstream scanner checks Botany for plants and Zoology for animals on the
mapped ordinary conditions. The menu reads the resulting knowledge state.
A visible unknown row prompts for scanning. A known row can be chosen if it
isn't already the current recipe, subject to successful application and any
link-change confirmation. A currently built row identifies selection, without
saying whether the facility can run. Actual scan thresholds depend on the
eligible category list and required count. The reviewed evidence has no live
scan-to-unlock series for either facility.
[Scanner and menu evidence](../experiments/organic-facilities/native.md#knowledge-acquisition-the-indirect-skill-and-scan-gate).

## Why a selected product can sit idle

The chosen resource determines the recipe. In the tracked main-file
catalogue, greenhouse recipes require one Water per cycle. The two
fauna-specific input patterns add two Fiber or two Nutrient per cycle.
The labels herbivore and carnivore describe these recipe patterns. The
selector follows the animal's resource properties and recipe links.
A greenhouse and a husbandry facility can both produce the same Nutrient
item while requiring different ingredients.

The ordinary builder checks eligible upstream stock when evaluating
production and caps the due batch by the scarcest required ingredient.
For example, Water can be plentiful while a selected husbandry recipe that
uses Fiber as feed is idle because the sources have fewer than two Fiber.
A source may supply through a linked storage buffer. The scheduled
production path requests ingredient removal from those
sources and can create output directly at a compatible receiver. A menu row,
an input link and an inventory increase are evidence of different stages.
[Recipe patterns](../experiments/organic-facilities/definitions.md#recipe-enumeration-and-inputs) ·
[Input and output contracts](../experiments/organic-facilities/native.md#input-cap-consumption-and-production-status).

## What survives a save

Save52 contains six qualified greenhouse configurations whose saved selected
resource values agree with the producer rows. Links and countdown data have
their own saved representations. The loaded engine resolves identities and
evaluates current production conditions. The transient menu is built again
from its inputs. The inspected positive subset does not demonstrate a saved
husbandry instance. The current knowledge, effective rate, feed stocks and
accepted output of a loaded facility remain unobserved.
[Saved-state evidence](../experiments/organic-facilities/native.md#persistence-and-authority).

[Technical reference and tracked recipe check](../reference/organic-production.md) ·
[Glossary](../reference/glossary.md#availability-and-production) ·
[Evidence and access](../audits/production-guides-d5ba/claims.md).
