# Saved manufacturing instances and local input paths

The mature corpus contains saved fabricators: **105 inspected saves have
manufactured producer rows**. Save52 alone is not the coverage basis.
The complete frozen 278-row inventory was consulted; its 184 fully fingerprinted
profiles with positive beacon counts were selected for the existing ordinary
beacon parser. Of those, 122 parsed, 41 retained unqualified-header parser gaps,
and 21 frozen original paths were unavailable. Across the 105 positive parses
there are 1,190 producer-row observations. These are repeated observations in
uncontrolled historical saves, not 1,190 distinct machines or independent trials.
The remaining inventory rows were not newly decoded for E3. Neither that
selection nor a zero positive row count proves universal fabricator absence.

Evidence is saved-state corroboration, separate from native instructions and
loaded measurements. Local receipts are
`.local-work/e3-fabricators/saved01/summary.json`, the individual `HIST-*.json`
receipts and progress ledgers. The source inventory remains
`.local-work/historical-inventory/scan-04/inventory.json`. The
[historical methodology](../historical-save-inventory-triage.md) governs these
labels; header version strings do not identify a verified originating executable.
Raw saves, personal paths, full envelopes and body fields remain local-only.

## Method, provenance and preservation

[saved.py](../../../research/e3-fabricators/saved.py) reuses the owned
[E2 saved-reader method](../../../research/e2-organic/saved.py), the established
ordinary-beacon producer-row grammar and saved directional link envelope.
Every available original was checked against its frozen SHA-256 and size before
decoding and rehashed after the attempted analysis, including parser gaps.
One save was decoded at a time to cleaned local scratch. No source save was
changed, restored or loaded in the game. The 41 parser gaps preserve the
reader's `UNQUALIFIED_SAVE_HEADER_BUILD` restriction; no version guard was
bypassed. Missing original paths, including rotated exit saves, remain
`UNAVAILABLE_FROZEN_SOURCE` rather than negative observations.

The first pass stopped on missing HIST-0167; its completed per-save receipts
were retained. The resumed pass revalidated their source hashes and continued
with explicit unavailable-source rows. This is a recovered evidence-acquisition
failure, not a failed semantic test or corruption finding.

For each recognized Workshop resource row, the outer IRES key identifies the
resource, and the inner two saved references identify the producer reference
and producer base. Existing native save/restore evidence in
[E1](../inorganic-extractors/native.md) establishes the producer-map contract.
Outgoing edges are the envelope group member → group key. Reversing that map
provides incoming edges. The E3 receipts retain exact resolved source/destination
identities and decompressed-stream row offsets. A file-relative main-ESM FormID,
save-local queued token and resolved dynamic identity remain distinct domains.

## Representative state and direct connection corroboration

HIST-0036, SHA-256
`7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37`,
has 14 manufactured resource groups and 17 producer rows. Both recorded header
version strings are `1.16.244.0`. The independently decoded logical stream hashes
to the value retained in its receipt; this is not a new live observation.
[details.py](../../../research/e3-fabricators/details.py), local `detail05.json`,
joins all 307 saved edge endpoints it can identify to reference prefixes and
main-game definitions. It retains record offsets, base identities, names,
keywords, producer-resource keys, immediate incoming/outgoing identities and
the full visited incoming adjacency used for each fabricator trace.

All 17 fabricator records have closed counted extras. Their ExtraBF sections
contain **no explicit selected-resource AV override**. Each saved base instead
has the corresponding selected AV preset = 1 in its definition, agreeing with
the saved producer-map IRES. Thus this sample corroborates saved base identity
and producer registration, with a **DEFINITION-DERIVED** selected AV value. It
does not demonstrate a newly selected output written into ExtraBF or the loaded
effective AV. Initial detail passes incorrectly assumed a leading ExtraBF and
then an explicit selected AV; those failed local receipts remain preserved.
The corrected reader consumes the supported preceding extras and records the
absence of the selected AV within both actual BF sections.

| Producer / base | Saved selected resource | Exact saved support, decompressed-stream bytes |
|---|---|---|
| `ff01a9f1` / CONT `003a861c` | Aldumite Drilling Rig IRES `00202f59` | REFR starts 3,076,059; BF [3,076,162, 3,076,170) |
| `ff03107b` / CONT `001b02c5` | Tau Grade Rheostat IRES `00245772` | REFR starts 4,266,093; BF [4,266,196, 4,266,204) |
| `ff022310` / CONT `0022174d` | Semimetal Wafer IRES `00245779` | REFR starts 3,382,012; BF [3,382,115, 3,382,123) |

The dynamic labels in the table abbreviate resolved `DYNAMIC:ff...` identities;
they are not runtime addresses. Definition-derived presets do not imply that
changing the selected output always replaces the reference base; native
configuration and persistence paths remain separately documented in
[native.md](native.md).

## Upstream chains, multiple candidates and boundaries

The detailed traces find **24 local required-resource producer witness paths**,
53 storage/buffer-boundary path observations and 29 incoming-cargo-boundary
path observations across the 17 starting fabricators. Counts repeat endpoints
when reached from different starts; they are not disjoint object populations.
There are zero detected cycles in this sample's traversed incoming adjacency.
The algorithm retains a visited set and one BFS witness path per node, with
all visited incoming adjacency recorded; it does not claim exhaustive simple
path enumeration or universal loop absence. The native cycle behavior is a
separate instruction-backed finding.

The following arrows show **upstream search order**, from consumer back toward
sources. Every underlying saved transfer edge runs from the right-hand object
toward the left-hand consumer.

* Positron Battery producer `ff01d4e7` reaches Tau Grade Rheostat producer
  `ff05ee43` directly. The latter's registered IRES `00245772` is an exact
  required input of Battery COBJ `002457c8`. The Battery has three immediate
  incoming edges and one outgoing edge in this saved state.
* Semimetal Wafer producer `ff022310` reaches `ff038411` through buffer
  `ff03841e`. The reached producer registers Zero Wire IRES `0024576e`, an
  exact required input of Wafer COBJ `002457c4`. Its two other witnessed paths
  pass buffers `ff0514e3` / `ff0514e2` and reach registered Antimony IRES
  `000057d3` / Gold IRES `000057d2` producers. These are structural supply
  paths for all three recipe input identities; quantities are not evaluated.
* Zero Wire producers `ff038411` and `ff038416` each reach two different Copper
  producers, `ff040ff8` and `ff0514cc`, through the same buffer `ff0514e1`.
  This positively demonstrates multiple local candidates for one input identity,
  without selecting which inventory would be consumed or asserting sufficiency.
* Aldumite Drilling Rig producer `ff01a9f1` reaches registered Aldumite IRES
  `00005df5` producer `ff04fd23` through buffer `ff04fd2c`. Its other recipe
  requirements remain separately listed, including any unreached identities.
  Finding this path does not certify the complete drilling-rig supply chain.

Positive endpoint labels retain their definition evidence. Registered local
producers use actual saved producer-map resource keys, allowing inorganic,
organic and manufactured inputs to be matched by exact IRES identity. Storage
labels join the actual saved base to named OutpostStorage CONT definitions
and retain their KWDA; the keyword conjunction for a generic storage classifier
is not asserted. Incoming cargo labels use exact main-ESM CONT identities
`00100b62`, `00219173`, `002a6c3b`; outgoing cargo uses `00100b63`, `00219171`,
`002a6c3a`. These are explicit positive definition matches, with unrecognized
endpoints labelled UNKNOWN. In the detailed endpoint population there are
123 storage bases, 101 registered local producers, 37 incoming cargo bases,
37 outgoing cargo bases and nine unknown endpoints. No inventory is counted.

Structural traversal can continue through a local storage buffer where saved
incoming edges exist, while preserving the buffer-boundary label. Traversal
stops at an incoming cargo endpoint; no remote cargo source or cross-planet
continuation is inferred. `unreached_required_resources` means no local matching
producer witness was identified by this traversal. It does not exclude items
already in storage, cargo arrivals, default references outside the saved subset
or other unrecognized sources. A connected link never establishes sustained
inputs, current recipe availability, powered operation or accepted output.
