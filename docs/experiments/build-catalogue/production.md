# Independent production aggregation cross-check

[Answer](report.md), [source pins](sources.csv), [functions](functions.csv).
Native addresses below are static VAs on freshly hashed retail 1.16.244.0 at
base `140000000`; object offsets are hexadecimal. `n001/n007/n022` are BM2 local
exports. [E1 arithmetic](../inorganic-extractors/arithmetic-production.md),
[E1 size correction](../inorganic-extractors/resource-intervals.md),
[E2](../organic-facilities/native.md), [E3](../fabricators/native.md) and
[P1](../power/fuel.md) supply the reviewed prior contracts, with their limits.

## Actual expression and population

Mask 2 in `1421f2cb0` zeros ExtraWorkshop+84 and calls `1421f36b0` on its
resource-keyed producer map +20. The helper walks occupied `18`-byte map slots,
then each resource bucket's `1c`-byte registration rows. A row contains producer
handle +00, base identity +04, bookkeeping +08, integer iterations +0c,
remaining/interval binary32 +10/+14 and cached reason-zero eligibility byte +18.
It is not a walk of all placed objects, all menu recipes or all storage inventories.

For every row whose cached byte is true, it resolves the producer handle and
excludes `140f7cb70`'s fueled-generator predicate. Failed resolution contributes
nothing and has handle-invalidation bookkeeping. It calls `140f7bf80` with the
bucket's IRES, resolved producer and owning Workshop context. Fresh n001
instructions establish:

```text
q = effective producer AV(IRES.resourceAV)          // binary32 getter
t = effective interval(IRES, producer, Workshop)   // binary32 seconds
r = t != 0 ? binary32(binary32(60f / t) * q) : 0f
total = binary32(total + r)                        // each included row
```

The actual division precedes multiplication (`VDIVSS`, then `VMULSS` in
`140f7bf80`); it is not assumed equivalent to computing `q*60/t` in unlimited
precision. `1421f3839` adds with `VADDSS`; `1421f383e` stores with `VMOVSS`. The scalar rate and
cache are binary32; there is no integer rounding of every term and no compensated
or double-precision accumulation. Hash-map/native row order can affect low bits.
No meaningful result for malformed NaNs, overflow or arbitrary negative intervals
is qualified by the ordinary positive finite examples.

Registration and normalization are independent. The registration paths
`140f7dfa0` and `140f83b90` create/update resource rows, using ceiling of a base
resource AV for scheduler iterations. Nominal `q` instead comes from the current
effective getter; it is not row +0c or COBJ NNAM. E3's earlier phrase “reaches
the shared registration” describes shared row machinery; the fresh `140f83b90`
export also contains its own row construction and is not asserted to be a direct
call to `140f7dfa0`.

| Producer class | Entry/inclusion basis | Exclusions/qualifications |
|---|---|---|
| Solid/liquid/gas/atmospheric extractor | Qualified resource property and ordinary Workshop producer registration | Resource selection/available context matter; atmospheric production uses the same rate helper, not a special global averaging clock. |
| Organic greenhouse/husbandry | E2 selected positive resource AV, shared resource-keyed row registration | Candidate availability/knowledge and actual selected AV are distinct; initial definitions' zero resource properties are not configured production. |
| Manufactured builder | E3 positive preset/selected resource AV; same row layout and aggregation | Tier labels, product recipe conditions and input stock are not an independent aggregate multiplier. |
| Fueled generator | Shared scheduling can register its fuel mechanism | Explicitly excluded by `140f7cb70`; consuming He-3 to power equipment is not item production in this sum. |
| Storage, unregistered forms, crew stations, solar/wind generation, freight arrival | No qualifying included resource row demonstrated for these operations | Inventory receipt or power generation is not automatically a production-rate contribution. This is a population/consumer statement, not a universal prohibition on custom resource-bearing forms. |

The interval helper `140f7bf10` combines resource-linked GLOB hours ×3600f,
eligible assigned-actor and player A1 timer effects and positive effective
HarvesterRateMult, substituting 1 when nonpositive. E1's getter precedence,
ExtraBF/ExtraE1/base-property contributions and settled perk stacking apply.
The fresh exports recheck this composition; actual participants/modifiers remain
unknown. A saved row's interval/countdown does not prove the current effective
interval or current eligibility after load.

## Mixed definition-grounded example

Assume all four rows resolve and have cached eligibility true; selected resource
AV is 1; no eligible actor/player timer effect, instance override, extra property
or AV modifier applies. Use the documented fallback default-plus-base-property
getter. These are **illustrative baseline operands from installed definitions**,
not an observed historical outpost, co-location claim or live total. The organic
choice is hypothetical positive configuration on a planet where that choice is
eligible; the base's actual default selected resource is zero.

| Term | Main-file producer / resource | Interval derivation | Binary32 rate per minute |
|---|---|---|---:|
| Inorganic | Small Iron CONT `0005ef19`, IRES `000057c7`, AV `0005ef18` | GLOB `0005ed87`: 36 seconds; factor 1 | 1.6666666269302368 |
| Atmospheric | Small Alkanes CONT `0020a8b4`, IRES `000057c9`, AV `0005ef10` | Linked GLOB `0005ef3f`: 54 seconds; raw rate property +1 plus default 1 gives factor 2: 108 seconds | 0.5555555820465088 |
| Organic | Small greenhouse CONT `002965f7`, selected Nutrient IRES `000777e6`, AV `002ac11b` | Linked GLOB `0005ed87`: 36 seconds; default factor 1 | 1.6666666269302368 |
| Manufactured | Adaptive Frame CONT `0027319f`, IRES `00245775`, AV `00245794` | GLOB `0014e8c2`: binary32 7.920000076293945 seconds; default factor 1 | 7.5757575035095215 |

In the displayed row order, binary32 accumulation produces
`11.464646339416504` nominal item units per engine elapsed minute. Exact
linked identities, source bytes, intermediate float bits and sum are reproduced
by [the verifier](../../../research/build-catalogue/verify.py) into local
verification receipts. The rate adds different products indiscriminately; it is
not an item-specific supply balance, mass rate, value rate or fabricator-input
sufficiency calculation. Counting Iron again as a fabricator ingredient does not
subtract its rate from this display sum.

Different intervals do not require synchronization because each term already
expresses a quantity per the same time unit. Adding those nominal slopes says
nothing about simultaneous due ticks, alignment, scheduler remainder loss,
input competition or accepted item counts. There is no least-common-multiple
window in this aggregate. Detailed scheduler and remote catch-up remain deferred.

## Cache, formatting and delivered output

Both screen adapters copy ExtraWorkshop+84. Build Mode binds `fProduction`;
Locations binds `fProductionPerMin`. The freshly verified installed SWF methods
retain E1's result: footer FormatNumberToString precision 2 slices ordinary
decimal text, while Locations rounds then uses toFixed(2). For the mixed example
the ordinary text is 11.46 on either screen; the discriminating one-Iron value
is footer 1.66 versus Locations 1.67. Decimal formatting does not change the
underlying binary32 sum. Unusual/scientific notation and actual screenshot bits
are outside that illustration.

The sum tests the **cached** eligibility byte, not a fresh `140f7d120` for every
row. Current halt, power, Health/destruction and required-input checks can change
actual scheduling/creation separately. Unsupported selection or unresolved row
removes a possible term; full producer/destination capacity can suppress accepted
output without a fresh zero nominal rate being proved. E1 creation does not
observe insertion's returned accepted quantity. Queue coalescing and asynchronous
UI delivery further separate the visible rate's epoch from current gameplay.
Thus underpowered, damaged, stalled or full equipment cannot be diagnosed from
the displayed number alone. No realized inventory-growth measurement or new
production simulator is delivered.
