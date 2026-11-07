# Locations Stored Resources technical reference

[Guide](../guides/stored-resources.md) · [Reference index](README.md) · [Claim and evidence crosswalk](../audits/logistics-guides-d5bb/claims.md)

The reported STATIC path is the pinned retail 1.16.244.0 native image and
installed UI assets. Hexadecimal native VAs are preferred static addresses
at image base `0x140000000`. HIST-0036 rows are separately scoped SAVE
evidence. [Sources](../experiments/stored-resources/sources.csv) · [Methods](../experiments/stored-resources/methods.md).

## Outpost identity and contributing sources

```mermaid
flowchart LR
    W["Registered Workshop handle"] -->|resolve and qualify beacon| M["Workshop member inventories"]
    M -->|gate and substitute shared reference| I["Qualified inventory sources"]
    I -->|group stack units by resource FormID| A["Per-outpost aggregate"]
    A -->|queued replacement| P["Provider row arrays"]
    P -->|selection paints existing arrays| U["Stored Resources panel"]
```

The schematic shows one ordinary collection and repaint. Failed handles,
rejected items and later menu re-entry are omitted. It represents data
collection and UI delivery. Stock stays in source inventories.

Locations entry `0x14135E120` calls the collector `0x141360E80` over registered
Workshop handles. It requires the resolved qualified beacon/ExtraWorkshop
context and emits OutpostStaticData entries for the UI. The selected
EntryObject carries the Workshop reference's form identity as `uFormID`.
A saved beacon or nearby chest alone cannot establish a registry row or
eligible membership. Reverse WorkshopItem relationships supply members.
The collector applies the container-capability and effective nonzero
`OutpostBuildContainer` predicate, substitutes the player-held backing
inventory for a recognized fixture and deduplicates that source within
the outpost. The same backing inventory can contribute to more than one
qualifying outpost's display. Summing those rows would double-count it.
[Registry and provider](../experiments/stored-resources/provider.md) · [Member controls](../experiments/stored-resources/membership.md).

An outgoing cargo bay with effective build-container zero fails even
when it holds an eligible resource item. An incoming bay, eligible
chest or producer buffer can contribute without a local link or an
active production cycle. The collector adds no independent ship or
player pockets source and does not enumerate all remote chests.
[SD2's source vectors](shared-storage.md#providers-counts-and-removal)
share the member gate but add sources and plan spending.

## Item identity, units and presentation

For materialized inventory the collector locks the source inventory and
uses `0x14136BE50`. For an unmaterialized list it can walk base entries
through `0x14136C060` and `0x141361AD0`. The mapped default preparation
uses one when a base-entry count is zero on that branch. This specific
conversion does not establish a generic clamp on item-instance stack
counts or that every base entry reaches the UI. The physical item visitor
requires a MISC form with exactly one IRES association. Its IRES input
branch first resolves the associated physical item. A missing, multiple
or non-IRES association fails the mapped item path.
The item visitor sums actual stack counts and `0x14136BBB0` groups them
by associated **IRES FormID**, independent of MISC form identity. The
visitor computes units. It does not multiply by item mass or a rate.
[Item admission and default path](../experiments/stored-resources/aggregation.md).

The UI receiver sorts by resource name while inserting corresponding
counts at matching indices in `aResourceListA` and `aResourceListCountA`.
The compiled selection handler passes the selected arrays to
SetStoredResources and writes the count and name. The examined icon
path reads IRES metadata. Nonzero resource color selects the symbol and
color branch. Zero color selects the GNAM-named OrganicIcons clip, with
Generic requested for an empty selector. The qualified art cases include
manufactured resources.
[Presentation binding](../experiments/stored-resources/provider.md#source-inventories-to-selected-row) · [Exact icon controls](../experiments/stored-resources/icons.md#exact-installed-joins).

## Collection, delivery and saved boundaries

Source inventories may change between individual collection reads.
`0x14136AC90` queues an owned aggregate for `0x141361C10` through the
UI service. Selection changes paint the delivered arrays. The mapped
state has no inventory-event recount or independent periodic collector.
External menu re-entry and elapsed delivery latency remain unmeasured.
Missing registration or resolution can omit an entry or source even
when there is no direct player-distance or 3D test.
[Three refresh boundaries](../experiments/stored-resources/aggregation.md#three-separate-freshness-boundaries).

Physical inventories and Workshop identity persist in their respective
channels. The display aggregate has a collection lifetime and no
separately persisted universal inventory in the mapped path. HIST-0036
establishes selected qualified save rows, with runtime effective values
and screenshot epoch joins unavailable. Unsupported extras do not establish
empty stock. The original review returned REWORK for the omitted
default-entry zero preparation, then accepted the corrected review02
snapshot. The study also preserves an earlier correction that narrowed
its freshness claim. [Saved witnesses and screenshot boundary](../experiments/stored-resources/saves.md) · [Review history](../experiments/stored-resources/review.md).

## Repeat a tracked aggregation

From the repository root, project the tracked HIST-0036 rows onto the
reported base-property control. This holds the selected ordinary
effective gates equal to those defaults for the example.

```powershell
$rows = Import-Csv docs/experiments/stored-resources/cases.csv |
    Where-Object { $_.sample -eq 'HIST-0036' -and
        $_.workshop -eq 'DYNAMIC:ff04ba51' -and $_.resource -eq '0057e0' }
$rows | Select-Object reference,item,resource,quantity,base_build_av | ConvertTo-Csv -NoTypeInformation
($rows | Where-Object base_build_av -eq '1.0' | Measure-Object quantity -Sum).Sum
($rows | Measure-Object quantity -Sum).Sum
```

Expect three qualified listed contributions of 375, 94 and 12 for
481 units, and an outgoing 375 for a deliberately overinclusive 856.
The rows map MISC `0x0057DF` to IRES `0x0057E0`. This checks the
recorded association and projection, with no claim about other stocks,
exact loaded eligibility, screen output or conservation across epochs.
[Primary example and scope](../experiments/stored-resources/saves.md#positive-mature-mixed-source-witness).
