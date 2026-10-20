# Saved cases, broad search and independent controls

[Answer](report.md), [case operands](cases.csv), [selected cells](cells.csv),
[sample hashes](samples.csv), [historical search inventory](corpus.csv).
Offsets in cases/cells are decoded logical-stream offsets or map-member offsets
as explicitly named; no token is a live FormID or handle.

## Broad corpus search

The frozen historical inventory has 278 stable HIST IDs, 275 bounded fingerprint
entries and three first-stream/header-only entries. Its historical statuses
are 196 SUPPORTED and 82 PARTIAL; those statuses are not assertions that the
current modern semantic readers support every build. Fresh source locator/hash
checks find 255 accessible unchanged originals and 23 missing originals.
All 278 inventory entries were searched for retained beacon-name metadata;
no absent name is treated as proof of absent outposts. The 23 missing paths,
historical errors and first-stream coverage limits remain in local `survey.json`.
The earlier inventory's hashes and original IDs are preserved.

The frozen detector reports `Feynman V Cu Co Ni IL` in 70 entries and
`Carinae III-a Rc Fe` in 43. Exact named metadata exists outside Save52:
HIST-0035 contains both; HIST-0210 and HIST-0267 provide later witnesses.
Fresh full decodes, separate arithmetic record walks and ordinary case-5
prefixes verify the selected beacons. Names label the recovered records only
after extraction. The broad search is metadata triage across the whole frozen
corpus, followed by seven selected rereads; it is not a new full semantic scan
of all 255 accessible files or a census of active player outposts.

The remembered Memory Substrate/Palladium site remains **unidentified**.
No retained beacon name or manual network entry explicitly identifies Memory
Substrate farming. `Carinae V-c Pd Ni` is a positive Palladium lead in 34
historical entries and the independent manual network, with nickel/palladium
production reported there. Selected snapshots recover that ordinary beacon
and Carinae V-c body association, but those facts do not connect it to Memory
Substrate, a clipped incident or the user's remembered site. Organic recipe
definitions establish three Memory Substrate producer variants, not a site:
[E2 recipe records](../organic-facilities/recipes.csv). No identification is forced.

## Priority controls

| Role | Actual witness / positive identity | Conditional nominal result |
|---|---|---|
| Priority multi-biome | Save52 / HIST-0267, beacon token `83388f`, parent `84ec80`, Workshop identifier bytes `c3a5866f4cfcf585`, PNDT `0005e0de` | 14 cells: 12 FrozenNoLife09 (`000fc61c`), 2 CanyonsNoLife06 (`00145440`). |
| Priority single-biome | Save52 / HIST-0267, token `82be17`, parent `84655c`, identifier `91bac704da9b1e34`, PNDT `0005e4da`; also positively recovered in HIST-0035 and HIST-0210 | 14 cells, HillsNoLife08 (`001160d9`) only. Single-biome status is calculated, not assumed from the name. |
| Same-body contrast | `Feynman V Cu IL F`, distinct saved site `(0,37536,20928)` in the same three snapshots | 15 cells cross pixel rows 147/146, both CanyonsNoLife06. It is not the priority site. |
| Independent held-out region | New-character controlled Kreet Save39 near the Lab, beacon `841421`, parent `839160`, identifier `41da48765780cc0c`, PNDT `0003f59f` | 15 cells, VolcanicRoughLifeKreet (`002c9985`). Uses independent source origin `(14304,12768)` and recovered center cell `(14314,12779)`. |
| Earlier geographic controls | Kreet Save25 SOR-002 and SOR-003, two distinct saved parents, shared source origin `(10464,21120)` | 15 and 13 cells respectively, MountainsLifeKreet (`0023c0ce`). |
| Effective-footprint witness | L3 Save31/33 SOR-004, beacon `829ab6`, parent `8193af`, identifier `3362182395aa9fbb` | 14 nominal cells, MountainsLifeKreet. Clipping is independently recorded by L3; no photographed BIOM label is invented. |

The named multi/single contrast is supported by independently read installed
map bytes and native address/lookup semantics. The manual network also reports
two selected biome entries for the priority Feynman site and one for Carinae,
but these are manual application values, not decoded save BIOM IDs or an
independent in-game measurement. No direct screenshot/UI-observed membership
is claimed. Saved extractors/resource labels never choose the result.

## Actual frame correspondence and counterexamples

Both mature priority sites use frame 2b, zero explicit compensation and local
centers respectively `(83.460693359375,67.88771057128906,-0.153639554977417)`
and `(86.6380615234375,70.4791259765625,6.211387634277344)`.
Their body-associated saved angular tuples recover the accepted site bases
`(0,25124,32446)` and `(0,21399,15640)`. HIST-0210/0267 independently recover
the typed world→secondary descriptor joins; record offsets, descriptor offsets,
Workshop offsets and map locators are in cases.csv/cells.csv.

HIST-0035's scoped unit-3 envelope locator fails uniqueness, so it has no newly
qualified full descriptor/world-array run here. Its positive body/site/ordinary
record and Workshop fields remain useful corroboration; it is not the sole
geographic authority. A repeated site in three snapshots is temporal byte
correspondence, not three independent spatial controls. The specimens are not
assumed to form a complete linear history merely from filenames/timestamps.

Save25's older broad automatic body concordance leaves SOR-003 null because
of an ambiguous cache lead. The fresh typed parent/world/descriptor join and
the direct Kreet point agree and resolve this task's body selection; the old
null result is retained rather than rewritten. Its unrelated whole-component
decoder gap at `140d4ae40` remains; the separately qualified world run still
supports the geographic join. Other cases close the supported component body.

The negative-X L3 case tests real negative floor: center Y `-96.75476837`
selects qY=-1 and center address `(1,10464,21119)`, rather than truncation to
the origin row. A saved site anchor can therefore differ from the calculated
current lookup cell. No exact continuous beacon point is inferred from either.

All selected originals/archives were hash-checked before/after decoding, with
complete compressed stream length/checksum/EOF validation and independent R3
framing agreement. [The coordinate report](../coordinate-sufficiency/report.md)
and [L3 record](../spatial-placement/saves.md) retain their original acquisition
limits and testimony; no save was loaded, created or modified here.
