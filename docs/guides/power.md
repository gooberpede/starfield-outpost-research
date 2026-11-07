# Power and generator fuel

An ordinary outpost device gets power through the electrical component the
engine assesses. The generator you build supplies a base rating. Current
actor values, eligible crew, activation and fuel can change the contribution.
The network and its traversal order then determine which devices fit. This
account covers the mapped Starfield 1.16.244.0 paths and the qualified Save29
case. [Power report](../experiments/power/report.md) ·
[Allocation and switch review](../experiments/power/review.md#focused-allocation-orderswitch-follow-up).

## Why the same generator can have a different rating

Planet temperature selects among fixed ordinary solar forms. Atmosphere
pressure selects among ordinary wind forms when the construction rule
admits wind. Basic solar ratings are 2, 4, 6 or 8. Basic wind ratings are
3, 6 or 10. On a body without an atmosphere the wind construction gate
fails. A zero shown in the comparison exporter represents that failure.
The ordinary contribution code has no day/night or weather operand in the
mapped path. The evidence comes from the variant definitions and native
code. It does not cover arbitrary mod-added effects.
[Generator variants](../experiments/power/definitions.md#planet-selection-and-exporter-exceptions) ·
[Contribution](../experiments/power/fuel.md#current-generator-contribution).

The fueled generator's base rating is 20. Its resource recipe requests
one Helium-3 per ordinary fuel cycle admitted by the input check. A local
resource link can make fuel available from reachable storage. The baseline interval is 36 engine
elapsed seconds per cycle before effective timer modifiers. The scheduler's
charge transitions can suppress or restore contribution and trigger a
network refresh. The cited work traced removal requests and charge changes
in the native path. Actual stock changes and the delay from adding fuel
to delivered power were unobserved. Cargo-link Helium-3 accounting belongs
to the future cargo documentation. [Generator fuel and charge](../experiments/power/fuel.md) ·
[Cargo transport evidence](../experiments/cargo-links/transport/report.md).

## Why a small device can stay off during a shortage

The electrical graph has both simple beacon connections and explicit
connections. Traversal can restrict crossing simple links at explicit
endpoints. A generator elsewhere in the same outpost can therefore be
unreachable from the devices under assessment. An open switch can prevent
assessment from expanding through it. An alternate path can still reach a
device, and the generation pass has its own rules.

For an eligible component with supply 10 and demands 6, 6, 1 discovered in
that order, the cumulative demands are 6, 12, 13. Only the first device
fits. The failed second device's demand stays in the sum, so the final
one-unit device is off even though the first used only six units of supply.
This fixed-order example illustrates the mapped accumulator. Root,
generator seeds, edge order and gates determine the actual discovery order.
[Deficit and partition rules](../experiments/power/native.md#deficit-allocation-and-the-mixed-case) ·
[Follow-up ordering evidence](../experiments/power/followup.md#a-roots-generation-seeds-and-assessment).

## What survives a save

Saved electrical connections preserve reference identities and connection
words. The powered bit records an earlier result and can be restored before
the engine recalculates. In Save29 three reported fresh-process reloads
showed extractor #1 on and #2 off. The saved beacon's ordered connections
lead from one solar generator to #1 then #2. Under the qualified ordinary
load inputs, supply 6 admits the first demand of 5. The second raises
cumulative demand to 10 and fails. The independently assessed native
explanation is deterministic recalculation for this setup. Restoring the
old bits would also match the observations, and historical worker execution
was untraced. Other graphs, effective values and load orders can differ.
[Save29 derivation](../experiments/power/save29-authority.md) ·
[Independent authority review](../experiments/power/save29-authority-review.md).

[Technical reference and tracked allocation check](../reference/power.md) ·
[Glossary](../reference/glossary.md#availability-and-production) ·
[Evidence and access](../audits/production-guides-d5ba/claims.md).
