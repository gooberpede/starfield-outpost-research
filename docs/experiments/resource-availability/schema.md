# Executable partial reconstruction and input contract

2026-10-14. [Frozen contract](contract.md). Project-authored GPL-3.0-or-later
code, stdlib and existing owned readers only. No live sampler or observer exists
in this implementation. Static function aliases below are OBSERVED-INTERNAL,
not supported mod integration APIs.

## Conditional native UI identity fold

[resource_availability.py](../../../save-analysis/scripts/resource_availability.py)
implements the final identity projection observed in pinned retail
`FUN_141578500`, `FUN_1421f8120` and `FUN_14042e250`. It does not generate terrain,
solve placement, reproduce resource information strings/icons or schedule events.

`sor-resource-ui-input/1` JSON has the following required fields:

| Field | Type and exact meaning |
|---|---|
| `schema` | String `sor-resource-ui-input/1`. |
| `exe_sha256` | Pinned executable `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Another build fails qualification. |
| `session`, `evidence` | Nonempty strings identifying one invocation/lifetime and original evidence. Syntax cannot establish provenance, simultaneity or genuine game execution. |
| `first`, `second`, `special` | Each is null for **unobserved**, or an observed JSON array of operands. Empty array means observed empty. Native source ranges are static globals `145f5d800..808`, `145f5d818..820`, `145f5d830..838`; these are locations of vectors, not their contents. |
| operand `pointer` | Unsigned 64-bit same-session runtime VA. Zero is null. Pointer equality is used for deduplication; it is not a FormID, saved token, static VA or file offset. |
| operand `form_id` | Unsigned 32-bit same-session runtime FormID, or null only for a null pointer. It is read at the source form object's +0x28. Qualified plugin identities need independent load-table resolution. |
| operand `qualified_identity` | Optional independently mapped plugin-qualified identity string, or null. Never inferred from pointer/numeric resemblance. |
| `selector_observed` | Boolean. False must accompany null `selected_form_id`. |
| `selected_form_id` | Null for an observed null selector, otherwise unsigned 32-bit runtime FormID at the selected form's +0x28 (`145efb1f0` holds the pointer). |
| `allocations_complete` | Null/unprovided means unknown; false means incomplete native allocation; true qualifies the model's successful-allocation precondition. Native allocation failure can drop rows. An authored assertion cannot prove this state in a game invocation. |

The first two arrays form an ordered union by **pointer equality**, retaining
first occurrences. The special array appends every entry whose FormID matches
the selector, without that union's deduplication. Null common entries produce no
UI row. A null special entry with a nonnull selector would be dereferenced by the
native filter and is rejected. Conflicting identities for one pointer invalidate
the snapshot instead of choosing a lifetime silently.

Output `sor-resource-ui-result/1` preserves evidence/session, ordered `ui_rows`,
and separately a sorted mathematical `ui_form_set`. Only successful, supplied
operands yield `CONDITIONAL_UI_PROJECTION`. Missing inputs yield `UNKNOWN` with
null result arrays; allocation failure yields `INCOMPLETE_NATIVE_ALLOCATION`.
Every result retains `extractor_placement=NOT_EVALUATED`. UI rows can contain
duplicates even though the mathematical set does not. This is a partial
calculation; it is never an independent site availability prediction from a save.

Run against an explicitly authored or separately captured input:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/resource_availability.py INPUT.json
```

The command reads only the supplied JSON and prints JSON to stdout. There are no
downloads, target/process reads, game writes, saved-byte writes or dependencies.
Synthetic tests qualify arithmetic/control flow, not retail set equality.

The independently callable `region_broadphase(center_xy, region_xy,
region_radius, query_radius, point_count)` additionally reproduces the first
resource-region callback's binary32 XY comparison at `1421e1119..1421e1154`.
Inputs must already share the callback's translated frame; a saved local center
alone cannot supply that join. Each subtraction, multiplication and addition
rounds independently to binary32, as in the instructions. Coverage is finite
normal/zero inputs and intermediates, nonnegative radii and u32 counts. Invalid,
overflowing and subnormal operands fail rather than guessing MXCSR behavior.
Passing broadphase with one point gives callback acceptance; zero points or a
failed broadphase give rejection. Passing with multiple points remains unknown
until the actual descriptor/segment containment tests are supplied. This is
neither a full region enumerator nor a valid extractor-footprint verdict.

`harvester_resource_gate` reproduces only `1421f68f0`'s already-qualified
harvester/property branch. Its produced-resource and first/second/special
collections are observed tuples of nonnull same-session pointers, or null for
unobserved. The three named flags are actual AVIF key-presence booleans (or
unknown), following resolved defaults and `14044b610`; float values are not
presence booleans. PlaceAnywhere presence returns the scoped bypass. Otherwise
SkipResourceVeinCheck selects the special list, ahead of HarvesterAtmosphere
selecting the second list; ordinary selects the first. Any produced-pointer
intersection passes; a genuinely observed empty produced list fails. Missing
selected inputs return unknown. The caller must independently qualify category,
base/property resolution, successful list construction and snapshot lifetime;
native early/default branches are not modeled by this restricted function.
Every result retains `extractor_placement=NOT_EVALUATED`.

`biome_rnam_resources(biome_identity, definitions)` separately takes a qualified
definition context mapping identities to actual `kind` and ordered `rnam`
tuples. It follows BIOM RNAM → RSGD RNAM → IRES, preserving occurrences and
reporting a separate set. Missing/wrong-kind/conflicting/unqualified edges yield
UNKNOWN and null lists. An explicitly supplied empty list is distinct. The
caller owns original ESM decoding and load/override qualification. This models
only those declared identity edges; it performs no spatial BIOM lookup,
PNDT override, chance/RNG selection or resource-region construction. Every
result retains `local_availability=NOT_EVALUATED`.

`compare_sets(expected, observed)` accepts independently acquired same-domain
sets and returns exact equality and false-positive/false-negative identities.
Unobserved input (`None`) returns NOT_TESTED with null counts/lists; an observed
empty set is distinct. The caller owns independent acquisition and identity
mapping. Screenshot labels cannot be compared to runtime FormIDs without that join.

## Saved producer registry audit

[research_resource_availability.py](../../../save-analysis/scripts/research_resource_availability.py)
walks all directory-framed R3 records, selects ordinary inline-base case-5 beacon
candidates and consumes their bounded Workshop prefix through the existing
project reader. This does not establish total outpost population or full REFR
extra-list closure. It extends the existing explicit resource-reader branch;
historical readers/interpretations are preserved.

The outer group consumes one queued saved form reference and a little-endian
body u32 row count. Each row consumes two queued references and 17 body bytes,
with decompressed-stream offsets preserved. Native serialization resolves a
handle for the first reference and serializes a FormID for the second; those
in-memory domains remain distinct even though both become wire reference tokens.
The parser reports exact raw body hex locally without inventing field meanings.
Resolution uses that save's FormRef array and full/small/medium plugin tables.

Reproduction from existing pinned inputs:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_resource_availability.py --inputs .local-work/workshop-inventory/inputs27.json --static .local-work/extractor-resource/run01/static-records.json --run FRESH
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_resource_availability.py --inputs .local-work/resource-availability/inputs-extra.json --static .local-work/extractor-resource/run01/static-records.json --run FRESH-EXTRA
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/verify_resource_availability.py --run .local-work/resource-availability/FRESH --extra .local-work/resource-availability/FRESH-EXTRA --output .local-work/resource-availability/FRESH-CHECKS
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s save-analysis/scripts -p test_resource_availability.py
```

The additional input manifest contains the two explicitly pinned Save27/28
originals read without modification, because no archived copies were located
under `.local-work/savegames`. Original hashes agree with the prior Q030 baseline;
before/after identities and exact source locations are retained locally.
No glob-derived gameplay expectations are used. Fresh run names are required;
outputs are exclusively created under ignored local research work. The disk-backed
decoder cleans temporary scratch. Both C:/D: must retain 40,000,000,000 bytes.
The verifier replays all samples and joins the mature registry to prior extractor,
member and 848-root receipts. All assertions are engineering/scoped association
checks, not availability or production oracles.

## Installed default/property verification

[inspect-defaults.py](../../../research/resource-availability/inspect-defaults.py)
reads all 38 source-pinned installed ESMs with the existing ESM reader, selects
TES4/DFOB/DOBJ and writes a fresh local receipt. It rechecks the source cache and
every ESM before/after; no downloaded parser/tool is used.
[validate-definitions.py](../../../research/resource-availability/validate-definitions.py)
joins exact default names/DATA identities to actual target record types and
checks the four explicit X-Tech bases' PRPS keys/produced resources. It reads
only the pinned derived definition receipts; original source-byte qualification
is provided by the companion scanner. No installed record implies a placed
instance or historic save-era content equality.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability/inspect-defaults.py --run FRESH-DEFAULTS
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability/validate-definitions.py --defaults .local-work/resource-availability/FRESH-DEFAULTS.json --run FRESH-DEFINITIONS
```

These scripts enforce the C:/D: guard and create exclusive outputs. The first
reads Bethesda installed data; the second does no original ESM scan of its own.
All proprietary fields remain in ignored local receipts.

[inspect-resource-definitions.py](../../../research/resource-availability/inspect-resource-definitions.py)
freshly scans all 38 pinned sources for TES4/ATMO/BIOM/RSGD, with original hashes
rechecked before/after and exclusive local output.
[project-biome-definitions.py](../../../research/resource-availability/project-biome-definitions.py)
resolves each file-relative RNAM in its actual master/compact context and applies
the pure identity projection. Differing projected overrides and absent RNAM
fields remain unknown. Identical projected edges do not establish equivalence
of all other definition fields. It never uses the resulting membership as the
site availability list.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability/inspect-resource-definitions.py --run FRESH-RESOURCE-DEFINITIONS
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability/project-biome-definitions.py --definitions .local-work/resource-availability/FRESH-RESOURCE-DEFINITIONS.json --run FRESH-BIOM-PROJECTION
```

The supported RSGD loader pairs a nonzero RNAM resource ID with a subsequent
DNAM. The installed 68 pairs have 560-byte DNAM payloads; the first DNAM word
is not interpreted as the resource identity. RNAM projections concern declared
definitions, not actual spatial or CTPerBiome-selected descriptor state.

## Generation partial and archived-input checks

`generation_seed(packed_cell_key: uint64, manager_owner_key: uint32)` implements
the native initial-zero/no-final-XOR CRC of twelve little-endian bytes.
`first_mt_word(seed: uint32)` sets the explicit 624-word native recurrence in
installed CPython's MT state, then obtains the first tempered word.
`generation_first_gate(key, owner_key, chance, weight)` returns UNKNOWN if any
operand is missing; otherwise it reproduces the binary32 first chance gate.
Chance is the selected DNAM float at `40*(rarity+7)+28`, rarity is IRES SNAM's
low byte, and weight is a qualified native caller operand. Owner key is the
observed manager+80 scalar, not a generally interchangeable saved FormID.
The exact range upper is binary32 bits `0x3f7fff58`. Normal/zero finite arithmetic
is the qualified domain; subnormal/overflow contexts are rejected. No later
count, position, overlap, region assembly or local availability is calculated.
The owned reproducer's seed-5489 reference test was consulted and credited;
source/native-informed code is not described as clean-room work.

[probe-archived-operands.py](../../../research/resource-availability/probe-archived-operands.py)
checks nine initial archived checkpoints and nineteen original-manifest pins.
[probe-phase1-operands.py](../../../research/resource-availability/probe-phase1-operands.py)
checks sixteen later journals and 65 used pins, journal-record raw hashes and
the union of captured address extents against required ProcGen hash-slot arrays.
It separates prior independently sealed raw identities from current journal pins.
Neither probe attaches to a process; current capture source cannot retroactively
supply bytes missing from an older capture.
[check-component-catalog.py](../../../research/resource-availability/check-component-catalog.py)
compares fresh S1/Save52 43-section replay against the original qualified receipts,
rechecks original source pins and records unresolved runtime-owner/storage-ID and
CTPerBiome/stream mappings. Framing closure is not source semantics.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability/probe-archived-operands.py --run FRESH-ARCHIVE
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability/probe-phase1-operands.py --run FRESH-PHASE1
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_workshop_components.py --inputs .local-work/workshop-inventory/inputs27.json --labels S1 Save52 --run FRESH-COMPONENTS
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability/check-component-catalog.py --fresh .local-work/workshop-population-rework/FRESH-COMPONENTS --run FRESH-CATALOG
```

These probes enforce the space guard, exclusively write ignored receipts and
pin used inputs before/after. Existing decoder scratch cleans itself. They read
local protected files; no game/save/database/configuration/Git/network changes.
