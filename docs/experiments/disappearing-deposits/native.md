# D1 native evidence and address domains

[Existing authoritative function register](../native-availability-map/functions.csv),
[source pins](../native-availability-map/sources.csv),
[generation lifecycle](../native-availability-map/region-lifecycle.md),
[output contract](../native-availability-map/output-contract.md),
[original producer association](../extractor-resource-association.md).
No new export or analysis-database edit was needed. N71/N72 add cross-references
to already exported point-query evidence; all other function entries are reused.

Native claims are STATIC on retail 1.16.244.0, executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
freshly rehashed. Preferred static base `0x140000000`; RVA = VA minus this base.
All windows below use static VAs; offsets after `+` are hexadecimal object fields.
These are OBSERVED-INTERNAL analyst aliases, not safe or supported mod interfaces.
No D1 runtime validation or native call occurred.

| D1 question | Register / RVA | Exact primary evidence and consequence |
|---|---|---|
| Can failed attempts be cached? | N15 `0079f860`; N16 `0079b520` | resource-milestone-b-producers-01.tsv: 14079fcb3 lock, 14079fde2..fe27 insertion, 14079fed3..ff18 setup/call, 14079ff1d..ff60 visited append; resource-availability-cont-01.tsv complete N16 decompilation and cleanup exits. Visited/cache entry is not a success certificate. |
| Is partial construction visible under the same lock? | N01 `021e07d0`; N15 | resource-availability-ui-15.tsv 1421e09d4..0a77 shared traversal versus provider exclusive region above. The mapped lock excludes that simple partial-write race; unrelated readers/writers are not covered by this conclusion. |
| Which cache survives? | N37 `0079ddf0`; N35/N36 | Existing event-oracle-08.tsv full reset and lifecycle ledger: source map/visited clear are explicit; exact travel/load event binding remains unresolved. Ordinary shutdown suggestions are not proof of which reset occurred. |
| How can a list be stale? | N01; N31 `01578500` | ui15 1421e0943..0960 spatial guard, 1421e0c77/c84 ATMO null/same skip, 1421e0e5b/e68 BIOM null/same skip; ui08 1415785af..8643 union/water append. Guard does not separately compare radius/upper. Correct UI folding does not establish fresh input. |
| Which list controls a selected harvester? | N34 `021f68f0` | ui10 complete decompilation, 1421f6b3a..6b5c selected population and pointer intersection. Presence helper 14044b610 differs from numeric property getter. PlaceAnywhere bypass; SkipResourceVeinCheck selects biome; otherwise HarvesterAtmosphere selects atmosphere; ordinary branch spatial. This is not full footprint/collision validation. |
| Can a point query distinguish geometry from area list? | N71 `0079df70`; N72 `00c5c550` | ui26 full N71: lock ProcGen+40, iterate occupied slots at +20/+28, call 1407affb0 for each resource map. ui22 N72: world/discriminator check, query using reference+8c, then test returned resource keywords. Numeric condition result is distinct from successful condition evaluation. It is not an exported whole-site enumeration API. |
| Can generation inputs change resource allocation? | N16/N18–N23 | Existing native-provenance and region-dependencies ledgers link per-biome component/RSGD choice, rarity ordering, packed key/CRC/MT state, bounds and competing-resource rejection. A shared planet/seed does not certify all consumed operands equal. No regeneration or terrain model was implemented. |
| What is persisted? | 00f50660 / 00f515a0 / 00f50880 | Existing Workshop serializer/loader evidence, referenced by resource-availability/native.md: resource-keyed producer rows persist outer resource, handle/base references and 17 row-body bytes. This is distinct from generated source regions and the operation's three vectors. Byte schema does not prove actual output or load authority. |

Names beginning `ui` refer to `.local-work/recon/resource-availability-ui-NN.tsv`.
The local native-checks.json verifies 39 inherited source-manifest entries
(duplicate paths may occur), not 39 newly generated exports. No proprietary
instruction text is copied into the authored patches.

Definition checks use the pinned project-derived static-records.json and its
unchanged installed ESM inputs. IRES→AVIF→COBJ joins and CONT PRPS values are
identities, not label-based guesses. PRPS entries are 12 bytes; key presence
is checked independently of numeric value. Relevant keys in Starfield.esm:
`0083ff` HarvesterAtmosphere, `271128` SkipResourceVeinCheck, `31986f`
PlaceAnywhere. All 22 distinct curated bases lack these keys. For comparison,
the existing catalog's atmospheric He-3 `0083fe` includes `0083ff`; ordinary
gas He-3 `06ac84`, `20a07c`, `20a084` do not. This qualifies source selection
under the mapped normal gate contract, not every dynamic property modification.
Exact definition physical record offsets are in local definition-flags.json.

Saved ownership is a decoded Extra4C counted entry, keyword `054ba6`, target mode
zero, unique ordinary beacon. Context queue adjacency alone is not used as owner
proof. Shared reader defaults remain unchanged; only the D1 diagnostic admits the
additional observed build-string pair after exact closure. Buffer version 153,
FormID, dynamic saved token, Workshop identifier bytes and runtime pointer are
separate domains. A body PNDT identity plus pair is not a captured runtime source key.
