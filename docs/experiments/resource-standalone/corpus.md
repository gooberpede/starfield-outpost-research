# Portable corpus and field dependency inventory

2026-10-24, Australia/Sydney. Authored format description, REVIEW-REQUIRED.
[Algorithm](algorithm.md), [rights](rights.md), [validation](validation.md).
Actual extracted JSON and complete geometry remain ignored and LOCAL-ONLY.

## Wire format

UTF-8 JSON uses an envelope with `payload` and `sha256`. The digest is SHA-256 of
payload JSON with lexicographically sorted object keys, comma/colon separators,
no NaN, and no added whitespace. Arrays preserve order. A newline after the
envelope is outside the payload digest. Numeric token spelling is CPython 3.14
`json.dumps` formatting, including `1.0` versus `1` and its exponent spelling;
sorting keys and removing spaces alone is not cross-language canonicalization.
A reader in another language can avoid reserializing numbers: use a JSON lexer
to locate the complete payload value's original byte span in the builder's
canonical envelope and hash that span directly, then parse and validate its
operands. Suppliers should preserve those canonical payload bytes and digest;
changing float token spellings requires recomputing the canonical representation.
Do not hash a parsed JavaScript or other language's reserialization and assume
its numeric spelling equals CPython's. This is integrity checking, not a signed
authenticity claim. The schema is `sor-d1-corpus/1`; the request schema is
`sor-d1-request/1`; the response schema is `sor-d1-response/1`.

The definition identity is the SHA-256 of the supported main ESM. The builder
also verifies EXE and PlanetData hashes. A different definition/schema is rejected,
even if its record identifiers look familiar. Build manifests hold the extraction
lineage and code pins separately from the minimized inference payload. Those
manifests are local-only and can include local paths. Payloads contain no absolute
paths, save identifiers, native pointers, expected geometries or request cache.

All eight-character record keys are lowercase hexadecimal main-file FormIDs,
without a display prefix inside the wire identifier. They are not runtime
pointers or saved tokens. Typed domains below apply independently of JSON's
unbounded integer syntax. Float operands are exact binary32 values represented
by round-trippable decimals; every generator operation explicitly rerounds.

## Request and response

Requests have exactly these eight fields: `schema`, `definition`, `body`, `chart`,
`descriptor`, `query`, `radius`, `upper`. Body is a corpus key; chart is integer
0/1; descriptor is two interior fine-cell coordinates divisible by 96. Query is
three finite normal/zero binary32 values in translated native units; radius is
positive and upper is the consumer's absolute upper scalar in that frame.
No source anchor, SFPT ID or expected resource/region is accepted.

Location selection is explicit. The corpus covers Feynman chart-0 tiles
(130,168), (130,169), and Carinae chart-0 tile (111,81), in 192-fine-cell units.
It can resolve requests beyond the two witness footprints while their complete
halo, source footprints, mask margins and key domain remain supported. Such
additional locations are inferred capability, not independently observed native
validation. No whole-planet or longitude/latitude guarantee is made.

Responses preserve the actual request, definition/corpus identity, coordinate
provenance, halo, source count, whole-source ordered geometry, exact XYZW/bound
hex, geometric area results, callback results and resource statuses. UNKNOWN and
PARTIAL retain failures; missing records or coverage are never default zeros.
An omitted resource entry does not mean absence. `exhaustive` means all modeled
sources in this halo resolved, while `native_census` and `historical_epoch` stay
UNKNOWN. The final catalogue is always separately unqualified.

## Retained inference fields

Every row is required unless its variant is excluded or it is marked optional.
Game-derived numeric data
is separate from authored field names, schema strings, status vocabulary and
algorithm rules. Derived fields inherit the input rights boundary.

| Field | Origin and domain | Consumer / sharing | Why retained; derivation |
|---|---|---|---|
| `schema`, `representation` | Authored revision/variant | Validation / global | Required interpretation and compatibility fields. |
| `game_version` | Optional descriptive build label derived from pinned baseline | Human provenance / global | Retained for readability; not required by prediction. Definition hash is authoritative. |
| `definition` | Main ESM SHA-256 | Compatibility / global | Pins identity; derivable only by preparation read, not by inference. |
| `constants` | 16 EXE binary32 operands, keyed by preferred static VA | Polynomial / global | Exact native rounding coefficients and angular scales; not runtime addresses. |
| `settings` | Six GMST DATA LE binary32 values, Common through Special | Chance / global | Installed values, including inactive Exotic; active branch may avoid them. Defaults are not substituted. |
| `maximum_width` | Maximum over installed RSGD generation blocks; nonnegative native units | Conservative halo / global | Bounds source discovery. A tighter selected-block bound is a possible refinement, not used in the delivered reference. |
| `generation_blocks[key][0:2]` | Selected root RSGD DNAM, attempt min/max; binary32 | Generation / shared block | Attempt count and fractional draw. |
| `generation_blocks[key][2:4]` | Width min/max, native units; binary32 | Generation/competition/halo / shared block | Path widths, not area percentages. |
| `generation_blocks[key][4:6]` | Step-length min/max, native units; binary32 | Walk / shared block | Next accepted-point displacement. |
| `generation_blocks[key][6]` | Maximum turn, degrees; binary32 | Heading / shared block | Converted with pinned radians scale. |
| `generation_blocks[key][7]` | Cell chance in percent; binary32 | First gate / shared block | Combined with mask/rarity weight; independent of attempt count. |
| `patterns[id][slot]` | SFPT FNAM uint32 + GNAM uint8, native X-major order, 256 pairs | Normalized lookup / pattern | Contains all entries needed for direct/one-backlink resolution. |
| `source_blocks[id]` | SFBK DNAM two LE uint32 raw dimensions | Normalized frame / source block | Nominal dimensions subtract four; no geometry precomputation. |
| `bodies[id].system`, `.index` | PNDT BDST GNAM LE uint32 tuple projection; system < 2^18, index < 64 | Packed key / body | Owner is body key on qualified producer path; no runtime owner pointer. |
| `tiles[chart:cx:cy][0:2]` | PNDT→SFTR selected SFPT/flag byte; native slot cx*256+cy | Lookup / body tile | Resolved tree projection; only raw flag 0x08 supported. |
| `tiles[...][2:4]` | Biome-map uint32 identity + low mask nibble, raster row inversion | Source biome/weight / body tile | Source-anchor biome and uniform footprint mask, distinct from beacon biome. |
| `biomes[id].status` | Authored qualification from preparation | Admission / body biome | Unsupported branches remain explicit. |
| `biomes[id].resources[].id` | IRES FormID | Resource identity and competition / body biome | All selected competing resources; not caller-filtered. |
| `resources[].rarity` | IRES SNAM low byte, ordinary 0 through 5 | Weight / resource | Branch chooses 1 or installed inactive setting. |
| `resources[].block` and array order | Selected root-DNAM block content reference and descending unique rarity | Generation / biome and shared block | Transitive derived component projection; never sort by FormID. |
| `routes[tile][slot]` | Expanded variant: anchor X/Y, SFBK identity, nominal dimensions; or null unresolved route | Expanded lookup / body tile | Replaces patterns/source-block tables, not generated points or seeded requests. |

Block references use the first 16 hexadecimal characters of SHA-256 of eight
LE binary32 values. The builder checks any collision before deduplicating.
There are four distinct blocks, three patterns and 106 referenced source-block
dimensions in the normalized delivered corpus. Sixteen constants and three
body-biome projections are shared across two body rows and three tile rows.
The preparation inventory measures 32 generation floats, 16 constants, six
settings, one width bound, four body-key integers, 12 tile scalar values and
24 resource scalar values plus three biome-status fields. Normalized lookup adds
768 FormID/flag pairs and 212 raw-dimension integers; expanded lookup instead
contains 768 resolved five-scalar routes and no unresolved slots in this corpus.
Counts exclude object-key spellings and are recorded in the local
`field-inventory05.json` preparation receipt.

The constant key semantics are: inverseTwoPi `0x144f0416c`; twoPi `0x144f049f4`;
halfPi `0x144f04654`; pi `0x144f048dc`; negativeHalfPi `0x144f052b0`;
negativePi `0x144f052f8`; degreesToRadians `0x144f03f50`; sine coefficients
s1..s5 at `0x144f04178`, `0x144f03ed4`, `0x144f03e00`, `0x144f03d80`,
`0x144f03d40`; cosine c2..c5 at `0x144f03fd4`, `0x144f03e48`,
`0x144f03dc4`, `0x144f03d58`. Addresses are build-specific provenance labels;
another implementation may map them to these symbolic names.

## Transitive preparation closure and omissions

The builder walks the pinned ESM read-only, with record/group bounds and compressed
closure checks. Full records remain preparation inputs, never fixtures. PNDT
FNAM selects the linked SFTR; BIOM maps come from the pinned BA2 members. Source
patterns retain every referenced typed SFBK dimension. Planetary components are
computed from all relevant definitions before projecting the supplied biomes.
All used module and file hashes, archive-member hashes, roots, RSGDs, selected
DNAM hashes and resource order are written to the ignored build manifest.

| Upstream dependency | Preparation use | Inference treatment / limitation |
|---|---|---|
| PNDT RSCS, PPBD order/chance/shuffle/override and BIOM fallback | Full planetary selection stream | Replaced by per-body-biome component projection; not a runtime cache witness. |
| Ordered RSGD root candidates and seven selection chances | Special/Common weighted selection | Replaced by selected resources and root blocks after complete planetary generation. |
| IRES child order, rarity and family probabilities | Family descent and occupancy | All selected competing IDs/order/rarities retained; unselected family branches omitted after projection. |
| Shared capacity, earlier biomes and atmosphere occupancy | Affects root/family selection | Empty atmospheric occupancy is the declared preparation model; historical effective occupancy unknown. |
| BIOM style, SFPT registry order, surface/random seed and rotation | Needed for generated surface trees | Not consumed by pinned PNDT-linked precomputed SFTR; raw flags enforced. No regenerated-tree fallback. |
| Grid block size, stitch/merge, padding, units and orientation | Qualified native frame rules | Authored algorithm constants 12, 2, 2 and 100; whole-pattern rotations unsupported. |
| GMST executable defaults versus installed DATA | C1H establishes distinction | Installed six-setting vector retained; no historical console/plugin override claim. |
| Zero-chance Everywhere Water in one Feynman biome | Own DNAM rarity-6 chance verified exactly zero | Geometry pass omitted: strict chance gate cannot emit a path; independent per-cell reseed means no later draw shift. Water catalogue/skip-vein status remains UNKNOWN. |
| Nonzero Everywhere, selected Special, tied rarity, mixed mask, default source | Additional native rules or operands needed | Builder rejects unsupported component classes; predictor records unresolved source cases. |
| Terrain heights, POI overlays, loaded source caches and epoch | Potential final consumer/runtime inputs | Not reconstructed. Planar vein result is not final catalogue or safe integration advice. |

Normalized referential integrity checks cover every pattern, block, biome,
resource and generation-block reference. Expanded checks require a 256-entry
route array for each tile and validate entry arity, typed integer domains,
aligned same-tile anchors and positive dimensions. Null entries explicitly
denote unresolved routes. The verifier separately checks normalized/expanded
output equality on both tested requests; a re-sealed hash alone does not prove
a route's semantics.
Both variants reject missing constants, malformed types, corrupt digests,
unsupported schema/definition and unsound width bounds. See the removal and
redundancy ledger in [storage.md](storage.md).
