# Electrical graph, allocation and current-state contracts

[Report](report.md), [generation and fuel](fuel.md), [definitions](definitions.md),
[saved instances](saved.md), [function register](../native-availability-map/functions.csv).
The [allocation-order/switch follow-up](followup.md) refines the initial P1
interpretation and supplies the [save/runtime availability table](availability.md).
SOR-EXP-0041 / SOR-EV-0049. All new native interpretations are STATIC,
proposed STRONG within these paths, OBSERVED-INTERNAL and REVIEW-REQUIRED.
No native invocation or new runtime observation occurred.

Addresses are hexadecimal preferred static VAs for retail **1.16.244.0**,
executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Image base is `0x140000000`; RVA = VA minus that base. Object offsets and
strides are hexadecimal. `pNNN` locates the complete function export in
`.local-work/p1-power/native/NNN.request.tsv`; instruction listings sometimes
stop at 600 instructions, so use the complete decompilation plus specified
instruction windows. Original names remain `FUN_<VA>`; role names are aliases.
Raw exports stay LOCAL-ONLY. The register supplies explicit VA/RVA pairs.

## Categories are predicates, not display names

The existing AV constructor export `e1-stacking-08.tsv` binds PowerGenerated
at singleton +380, PowerRadiation +388, PowerRequired +390,
WorkshopSnapTransmitsPower +478, WorkshopPowerConnection +480 and
WorkshopPowerConnectionAndReceiver +488. These are **different properties**.
Installed PRPS identities are in [catalogue.csv](catalogue.csv). The relevant
native predicates are:

| Function / evidence | Actual test |
|---|---|
| `1406695c0`, prior E1 | CanBePowered keyword or effective CanBePoweredAV; applicability, not current powered state |
| `140669670`, p007 | Nonzero effective connection-and-receiver AV, with the Workshop-base exclusion branch |
| `140669700`, p007 | Nonzero effective connection AV (subject to Workshop-base exclusion), PowerConnection keyword, or receiver predicate |
| `1406697f0`, p007 | Positive **base** PowerGenerated, with the same Workshop-base exclusion |
| `1406699b0`, p007 | Positive base PowerRadiation and false `140f386a0`; this is radiation, not a switch-state query |
| `140669a10`, p013 | Nonzero effective snap-transmits-power AV |
| `140669a60`, p009 | Power-applicable non-connector, or receiver, excluding radiation/snap/special graph categories as shown in its branches |

Default-object initializers `14003e570/5b0/5f0` (p004/p007) bind
CanBePowered, CanBePoweredAV and PowerConnection containers. Runtime keyword
and effective AV tests mean an EditorID/name-only catalogue cannot certify
wire eligibility. A generator is also an eligible endpoint; a plain decorative
base with none of these predicates fails. The inspected lamppost candidates
have power/connection properties, while absent explicit demand is only a
definition observation. Query PowerRequired on the actual reference to obtain
current reference base demand through virtual +18, matching the allocator below.
Foundation art is not automatically an electrical relay.

## Authoritative pair admission and construction caller

`14066bd50` (p014) takes two reference operands. Both must satisfy
`140669700`. It queries their existing connection with `140669090` (p008):
no found connection accepts; a found **word 1** connection also accepts;
a found word other than 1 rejects. This permits replacing a simple relation
with an explicit one and rejects duplicate existing explicit links.
There is no generator-only rule and no producer/consumer direction requirement.
No degree/count limit or wire-length comparison occurs in this pair predicate.
That statement is scoped to this predicate, not a claim of unlimited UI wires.

The candidate highlighter `1421c45a0` (p019) expands assembly candidates,
applies the pair predicate and calls `140f4aab0` (p020). That helper requires
the candidate descriptor's world identity to equal the Workshop's context,
translates an indexed position using the current translation table, and calls
the Workshop spatial-boundary test `140f4a910` (p021). The nearest-candidate
selector `1421eb180` (p019) uses squared distance to the supplied cursor/query
position, rejects self and requires the same pair predicate. Candidate
selection, Workshop location and successful creation are separate contracts.
Neither function is a safe arbitrary-reference connection API.

The commit path `140f65ae0` (p016) resolves the selected endpoint handles and
calls `14066bfc0(a,b,3,null)`. It does not independently re-run every candidate
check. The latter adds reciprocal electrical memberships and reallocates;
its optional fourth reference instead represents a physical spline node,
adding endpoint↔spline memberships. The editing/replacement path
`140f65c50` removes the old connection through `14066e9b0` before adding the
new word-3 relation. A caller that bypasses selection cannot inherit its
validation guarantees.

`fWorkshopWireMaxLength`, container `145e8bf68`, value +8, is consumed by
`140668130` and `140668560` (p016) for cable bend/sag interpolation.
Those consumers do not reject long electrical edges. A universal physical
maximum must not be inferred merely from the setting's name. The inspected
creation chain has the explicit predicate/location restrictions above; UI
selection geometry may further limit what a player can select. Exact general
degree limits or a universal hard length are not asserted by this research.

## Graph representation and ordinary simple membership

ExtraPowerLinks is extra type **CB**, bound explicitly by allocator/getter
`1405431d0` (p006). Extra +18 is u32 count, +1c capacity, +20 array pointer;
element stride 8 is reference FormID +00 and u32 connection word +04.
`14065bf00` → `14065c2f0` (p009/p011) inserts under the extra-list lock,
deduplicating the full FormID/word pair. `14065bfc0` removes a membership.
The [load investigation](load-determinism.md#pinned-evidence-and-identity-correction)
corrects the initial P1 handle label using the writer and native GetFormID;
temporary traversal handles remain separate.
This is a per-reference graph, distinct from resource-transfer's global
destination→incoming-source map at `145916580`.

| Word | Supported origin/consumer evidence |
|---|---|
| 1 | Reciprocal simple memberships, including Workshop beacon links. `140669d60` (p012) creates these; saved samples corroborate actual beacon endpoints |
| 2 | Automatic graph relationships created by `14066f3e0` (p008) across classified categories; not a user-created visible wire by definition |
| 3 | Explicit endpoint connection from `140f65ae0`; reciprocal mature-save object links corroborate it |
| 0 / spline-mediated | Supported alternative through the optional spline reference in `14066bfc0`; physical cable geometry is separately represented |

These are enumerated words used by equality tests, not interchangeable Boolean
flags or an established bitmask. Do not call every CB entry a drawn cable.
`140668380/1406700f0` (p018) recover the two endpoints of a spline; traversal
can cross from one endpoint to the other without treating wire art as a device.
Definition XPLK loading `14065bc30` (p006) is a different channel from savegame
ExtraCB loading. Save framing and historical examples are in [saved.md](saved.md).

`140669ff0` (p009) gathers simple/snap relationship candidates;
`140669d60` admits radiating generators without existing live edges and
qualified consumer/receiver categories, then inserts reciprocal word 1.
Other paths include snap candidates and explicit topology changes.
Workshop ownership uses the separate linked-reference keyword at
`145f0b3d8`, not an assumed global list of every placed object.

## Traversal and graph partition

`140671f70` (p010) collects the generation side of an electrical component.
Setting `bWorkshopPowerNonRecursiveTraversal`, value `145e8c1a8`, defaults true
in `14003e540` (p004). It selects queue-based `140675c50` (p011); false selects
recursive `140676350`. Its neighbor callback `140678f60` (p026) resolves
direct/spline endpoints and calls `1406791d0` (p027), which applies the same
partition gate `140669c60` and checks visited identities before recursion.
The initial P1 description that the queue "preserves discovery order" was
insufficient: the follow-up proves front insertion and pending front promotion,
not FIFO. It deduplicates generator references and sums eligible contributions
from `140669880`; recursive forward order can differ.

`1406779e0` (p015) enumerates CB elements in stored order, resolving direct
endpoints or crossing a spline. `140677c50` (p017) checks visited and already
queued identities, promotes an already queued target to the front, or applies
edge gate `140669c60` (p012) and inserts a new target at the front.
This is how cycles terminate; the saved forest samples do not themselves test
cycle execution. Branches and multiple generators are represented naturally.

The edge gate has a **partition restriction**, not a switch-on Boolean:
when neither restriction byte is set, or a spline intermediary is supplied,
the edge can pass. Otherwise a direct endpoint passes only with word !=1.
The restriction is set for a receiver with a live word-3 edge, or an ordinary
radiating generator with a non-simple edge. `14066bec0` (p009) checks exactly
word 3; `140668fa0(mode=1)` (p008) tests whether all connection words are 1.
Thus a wired receiver/generator can prevent traversal through simple beacon
links. An electrical component is not automatically the whole Workshop.

`14066bad0` (p009/p013) additionally recognizes a non-generating radiating
connector with no resolved non-simple/spline link. It returns true for no
edges or only unresolved/non-spline word-1 endpoints after its prerequisites;
a resolved spline or word !=1 makes it false. It is not a generic
"has links" or "is switched off" predicate.

## Deficit allocation and the mixed case

`14066b100` (p007) is the consequential allocator. It obtains supply and a
generator seed vector from the generation traversal, adds the root/Workshop
candidate only on the specified no-generator cell-context fallback, and walks
the expanding vector by increasing index with a separate visited set. This
corrects the initial P1's ambiguous "discovery vector" description; the two
walks have different ordering rules, detailed in [the follow-up](followup.md).
For each eligible non-skipped candidate requiring power it adds **base
PowerRequired** (reference +70 virtual +18) to a cumulative binary32 demand.
It inserts that candidate into the powered result set only when cumulative
demand <= available supply, then explores eligible adjacent references.
Rejected demand is **not subtracted**. Relevant instructions are
`14066b51c..14066b54e`, including VADDSS at `14066b531` and comparison at
`14066b535`. This is neither common failure nor a smallest-load fitting algorithm.

For a fixed valid traversal with supply 10 and demands 6, 6, 1, cumulative
demand is 6, 12, 13: only the first consumer enters the result. Reversing those
same demands to 1, 6, 6 admits the first two. These are code arithmetic
examples, not observations of a particular outpost. No gameplay priority or
construction-time sort is consulted here; the current graph's discovery order,
stored edge order, root and skipped/visited categories determine the result.
The pointer-ordered set is visited/result bookkeeping, not a demonstrated
device-priority ranking. Construction order could influence stored topology;
it is not itself the allocator's explicit priority key.

**Mixed wired/unwired equipment does not obey one universal favored-group rule.**
The same allocator serves both, but link partition determines which generators
and consumers enter an invocation. One generator explicitly wired to a consumer
can form a component that excludes its word-1 beacon path; an unwired consumer
then cannot claim that component's supply simply because it shares the Workshop.
Two explicitly connected generators are deduplicated and summed within the
component; this is not double supply to independent pools. Consumers reached
within that component compete by the same cumulative-demand rule.
Other simple-connected generators/consumers can remain in the beacon component.
Always determine actual edge words, restriction predicates and reachability
before applying a shortage calculation. Summing all generator ratings on the
Workshop UI cannot predict which of these consumers is powered.

The logical graph rule is statically answerable. Which historical saved device
would win in a freshly loaded run additionally depends on restored edge order,
live handles, effective generation, root and current invalid/activation state.
That missing current instance state is not a missing allocation algorithm.

## Switches, current powered bit and recalculation

`140669ac0` (p009) rejects an invalid/disabled-category candidate through
`140f2fd40`, handles category exemptions and tests activator classification
`140a74420`. For that class, `1405cdc70(reference)==1` (or the supplied
same-reference override byte) excludes the node. The helper's activation-state
query includes reconstructed ExtraAction (type 0D), pending open/close work,
animation variables and a named interface override. The preliminary
"animation/script" interpretation is superseded by the exact getter precedence
and REFR difference-mask persistence in [the follow-up](followup.md#b-switch-getter-transitions-and-persistence).
The category default is explicitly named ActivatorIsSwitch by initializer
`14009bc60` (p027), container `145eaad10`, resolved keyword pointer +48.
Installed DFOB `001690a5`, ESM byte `1294811799`, binds keyword `001690a4`.
The allocator skips that node and its ordinary expansion; an off switch can
separate downstream consumers, while an alternate valid cycle/path can still
reach them. The numeric state is retained rather than assuming every activator's
animation poses map identically to On/Off. Generator ACTIs also carry switch
metadata; their state gate is distinct from rating and fuel charge.
Generation collection and consumer expansion are different stages: the
queue-based generation collector still enumerates edges after classifying an
invalid generator, and an ordinary non-generator switch does not itself prune
the generation callback. Do not model a switch as universally cutting both
stages. In particular, generation can be collected across a switch whose
allocation-node expansion is skipped; alternate paths and the exact root matter.

`14066f880` (p008) schedules recomputation directly or queues worker
`14066fa50` for the engine thread. The worker builds old and new powered sets;
old-only members call `14066abc0(ref,1)`, new-only members call
`14066abc0(ref,0)`. That setter writes ExtraFlags mask **40** as the inverse
of its second argument, marks reference change `80000000`, refreshes producer
eligibility, emits power events and updates animation/other consumers.
It is not a harmless getter. `14066d4b0` (p007) similarly refreshes owner-linked
components; `140f7c060` (p022) calls it after relevant actor-value changes.
Edge add/remove, fuel-charge transitions and reference events also reach the
recompute paths. These triggers are not a claim that every unloaded object is
always resident or immediately updated.

Current native power reads remain the E1 contract: reference +c8 extra list,
type 9c +18 mask 40 via locked `140531b10`, wrapped by IsPowered
`140c05630`. Null/wrapper completion must not be mistaken for true power.
Current production evaluator `140f7d120` separately reports reason 5 for
applicable missing power, reason 9 for halt, and reason 7 for insufficient
inputs. Powered, halted, charged, disabled and actually producing remain
separate state dimensions.

## Nominal, available and displayed values

`140669880` returns one nonnegative conditional contribution; it does not certify
that a particular consumer can reach it. `14066bcb0` (p017/p020/p021) is a
generation-accumulation callback. `140f83120` (p017) dispatches resource-AV
refresh and updates cached producer eligibility. `140f83450` (p017)
updates cached producer eligibility after state changes. Shared production-row
eligibility and Workshop aggregate fields are caches, not substitutes for
the electrical graph result set or live ExtraFlags.

Power-pair refresh `1421f2680` → parallel callback `1421f3690` → `1421f2890`
(p024) enumerates owner-linked objects and filters invalid/deleted categories.
It obtains generation through `140669880`, demand through base virtual +18,
converts each reference's values to integers, zeroes that reference's generation
when its current powered bit is false, and adds thread-local integer totals.
The pair feeds ExtraWorkshop +7c/+80 through the existing summary refresh
`1421f2cb0`; production is the separate +84 float. Per-reference truncation
before addition matters for fractional bonuses. This Workshop summary is not
the floating-point supply of a particular electrical component.
The [existing UI adapters](../inorganic-extractors/arithmetic-ui.md#common-statistic-and-separate-native-ui-adapters)
copy the cached 24-byte summary to the build footer and LOCATIONS model.
No raw save-derived sum is labelled the exact current HUD value, and no new
screen or running UI was sampled. Lifetimes require resolved
reference leases, a valid Workshop and the engine's thread/queue ordering;
an RVA alone grants none of those guarantees.
