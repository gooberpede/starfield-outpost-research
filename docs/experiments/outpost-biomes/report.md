# Outpost biome assignment and nominal territory

2026-10-20, Australia/Sydney. SOR-EXP-0059 / SOR-EV-0067.
[Authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_B1_outpost_biome_assignment_nominal_territory.md`), [frozen plan](plan.md), [review](review.md).
Authored findings REVIEW-REQUIRED; original saves, maps and native exports LOCAL-ONLY.

Reader context added 2026-10-21: [historical examples and access limits](../../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b2/evidence-dependencies.md`)
distinguishes the two named Feynman V sites and Carinae III-a, the Save52 alias
and the unestablished Carinae III-c label. This adds context, not new site evidence.

| Element | Best-supported result |
|---|---|
| Question | How can every biome with positive-area overlap with an ordinary nominal radius-150 outpost be identified? |
| Answer | **Enumerate every intersecting native terrain lookup cell, resolve its authoritative base BIOM identity, then deduplicate.** The mapped consumers floor local XY at the approximately 100-unit grid, transform the integer address into a hemisphere-square cell center, and read a discrete biome raster. They do not interpolate biome identities within that lookup cell. Testing the beacon or circumference alone is insufficient. |
| Confidence | PROVEN sampled map/save bytes and reproduced arithmetic; proposed STRONG / STATIC plus SAVE for the conditional ordinary base-biome model. Completeness is justified for this representation and qualified frame, separately from full loaded-game equivalence. |
| Tested coverage | Three installed version-5 maps, two 256×256 hemisphere rasters each; seven reread save inputs, 14 site/snapshot rows, seven distinct sites; both 0b and 2b saved-frame models. Save52's **Feynman V Cu Co Ni IL: FrozenNoLife09 + CanyonsNoLife06**. **Carinae III-a Rc Fe: HillsNoLife08 only**. A distinct Kreet Lab region is an independent control. |
| Inferred / unknown | The traversal extends to other successfully resolved ordinary base maps and qualified frames. Seam normalization is traced but seam-crossing footprints are not tested. Visual blending, special world/location overrides, historical effective load order/settings and actual restored runtime results are not measured. |
| Decisive evidence | [Native/definition chain](native.md), [enumeration and completeness derivation](nominal.md), [saved cases and counterexamples](saves.md), [source pins](sources.csv), [function locations](functions.csv). Feynman's two map rows are read at member-relative bytes 89,642 and 88,618, independently of its label/resources. |
| Limits | These results classify the nominal horizontal disk's base-biome field. They do not compute buildable area, count every historical outpost, certify visual biome extent, predict resource deposits, or establish safe native invocation. |
| Next discriminating step | Independent critical review of the qualified frame and cell traversal is sufficient for this scoped result. If actual post-load equivalence is separately required, compare one point in each of Feynman's two predicted sides using an identity-bound, separately authorized observation; no new live work is authorized here. |

## Causal result

Planet identity and its installed map select a finite field of BIOM FormIDs.
The ordinary reference/resource consumer first quantizes XY, so the relevant
spatial atoms are the preimages of that integer quantizer. For the three maps,
one raster pixel spans 192 fine indices per axis under installed defaults;
the 100-unit query cell is finer than the biome raster. A raster boundary can
cross an outpost, but this path does not select two identities inside one
query cell. Terrain textures, coast treatment and resource strips have separate
consumers. See [native branches](native.md).

The saved ordinary Workshop supplies a qualified local center and frame;
the accepted [geographic cell model](../coordinate-sufficiency/report.md) supplies
the corresponding terrain address. No exact continuous beacon longitude or
latitude is needed. In the mature 2b cases, use the qualified saved site cell;
substituting the secondary descriptor origin is a concrete error. Feynman's
descriptor is `(0,25152,32448)`, while its site base is `(0,25124,32446)`.
The [saved ledger](cases.csv) records both operands rather than choosing by name.

Feynman's nominal disk intersects 14 query cells. Twelve select FrozenNoLife09;
two in its upper cap select CanyonsNoLife06. The cap starts approximately
132.1123 local units above the center, inside the radius of 150. Carinae's
14 intersecting cells all select HillsNoLife08. The other Feynman V outpost,
`Feynman V Cu IL F`, crosses raster rows but both rows contain CanyonsNoLife06:
crossing a pixel boundary alone does not add a biome. Repeated historical
snapshots reproduce these same sites, not independent spatial replications.

The derivation includes fully enclosed cells, excludes zero-area tangency and
uses exact dyadic interval checks for the floating-point quantizer. It is a
finite partition argument, not a claim that a dense sampling grid must find
every patch. The demonstrator is a disposable research calculation, not an
importer or production enumerator.

## Effective territory and resources

[Secondary findings](effective-and-resources.md) retain L3's additional
location/encounter exclusion operation. Its Kreet Save31/33 nominal disk has
only MountainsLifeKreet; clipping can remove area but cannot add a base-biome
identity. Exact clipped geometry remains unavailable without the selected
loaded grid/location operands. Object collision/support remains another gate.

BIOM RNAM references lead to RSGD resource definitions; planet/per-biome
components, map masks and generation state select/configure generated resource
regions. Their strip geometry and competition differ from the base-biome raster.
Organic facility selection has a planet-scoped species/knowledge route.
Neither resources in a label nor saved extractor lists supplied the biome answer.

## Evidence state and handoff

This adds a conditional base-biome assignment/coverage result and representative
reconstructions. It preserves earlier geography, resource, membership and L3
claims and publication classifications. [Methods and failures](evidence.md)
retain inaccessible historical locators, unsupported grammar, early helper
errors and their corrections. All target/save/database inputs remain protected.
No game launch, debugger, deployment, save/configuration change, staging,
commit, push, external contact or disclosure occurred. Independent disposition,
actual checks, patches and remaining limits are in [review.md](review.md).
