# SOR-EXP-0014 — Two outposts, site anchors and beacon coordinates

2026-10-09, Australia/Sydney. SOR-EV-0020 / SOR-SAMPLE-0030. Completed bounded offline pass, **critical review required**. Authored report, selected numbers and scripts REVIEW-REQUIRED; saves, full extraction and proprietary native exports LOCAL-ONLY.

## Answer for review

| Element | Result |
|---|---|
| Question | Do Save25's two ordinary beacons in one continuously traversed landing area share a planetary anchor, and can their exact planetary positions be derived? |
| Best-supported answer | **Distinct anchors:** different serialized parents and different longitude/latitude pairs, both directly associated with Kreet. The saved site pair cannot be treated as one constant origin for the entire user-observed landing area. SOR-002 reuses the earlier Kreet angles bit for bit despite a different parent and slightly different local XYZ. |
| Confidence | PROVEN / SAVE for sampled identities, bytes and inequalities; **STRONG scoped semantic interpretation proposed for review** using the previously established overlay-angle semantics. Common underlying local frame is PROVISIONAL. Exact beacon-global conversion remains OPEN. |
| Coverage | Two recognized inline case-5 ordinary beacons in this Save25, header strings 1.16.244.0; fresh archived Save3/S1/S1C/L2C, Save2 and Save52 cross-checks. The user's uninterrupted on-foot traversal is SOURCE-REPORTED, not independently replayed. |
| Evidence | [Five-row beacon ledger](two-outpost-anchor/beacons.csv), [exact comparisons](two-outpost-anchor/comparisons.json), [source/copy manifest](two-outpost-anchor/manifest.csv), four targeted read-only native batches. Both records independently match base/self, saved-name queues and repeated overlay keys. |
| Limits | No precise beacon longitude/latitude is claimed. A direct PNDT association resolves SOR-003 to Kreet, but the old unframed cache search also admits a Uranus-shaped hit; its automatic concordance field remains null. Frame identity, terrain resolution/origin, fractional local-position projection and load authority are unresolved. Complete active-player membership is not claimed. |
| Next step | First resolve the per-body terrain-manager grid resolution and origin, and the reference-to-overlay frame mapping offline. Then test the derived projection against both Save25 pairs and a third independent placement. A live calibration would require a separate bounded brief. |

## Authorization, plan and provenance

The maintainer invoked [the retained brief](../implementation-briefs/CODEX_BRIEF_SOR_two_outpost_site_anchor_and_beacon_coordinates.md). Starting HEAD `162ffba899d71bb64877d86069e0a749c16cfe0f`; the supplied untracked brief was the only pre-existing change. Authorized: offline source/archive reads, protected-copy creation, existing project readers, targeted readOnly/noanalysis Ghidra exports, original numerical/inspection utilities and documentation. No game launch/load, debugger, instrumentation, deployment, save edits, database edits, staging, commit, push or external disclosure occurred.

Plan: hash/copy Save25 before decoding; enumerate supported candidates without a two-result constraint; resolve queued base/self/name/parent associations; compare parent, body, pair bits and local tuples separately; cross-check frozen controls; inspect the smallest native coordinate bridge; stop when the anchor question is answered and exact-conversion gaps are concrete. Stop on hash drift, corrupt/ambiguous essential framing, resource-guard failure or unexpected target/database mutation. Cleanup removes only decoder-created temporary scratch; archives, receipts and failed attempts are retained.

The user reports loading pristine Save3, placing SOR-002 approximately where the earlier beacon stood, then walking approximately north for a couple of kilometres to place SOR-003 without a landing-area transition. These are approximate placement conditions, not calibrated directions/distances. Save25 is a single state with both placements, not an action/no-action sequence. Labels never select a body or coordinate: they are read only after extraction to distinguish the saved records.

Save25 original is the exact filename in the brief, in the Steam-managed Saves directory. Final analysis archive is `.local-work/savegames/two-outpost-anchor/extract-04/` with the unchanged filename. Both are **2,403,744 bytes**, SHA-256 **`d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`**. Hash/size equality was verified before analysis and again afterwards. Source timestamp is 2026-10-09T10:22:24.520275Z. Decoder closes 26 BCPS streams into **6,553,789 bytes**, SHA-256 **`0c27c10c1f07d5a480da4f857072cafc17e198b981350e01de2fa6b09f972cfd`**. Original/copy locators and full metadata stay in the ignored manifest; originals were never written.

Controls use frozen EXP0012 identities, not filename guesses. Save3 is SOR-SAMPLE-0001; S1/S1C are 0008/0009; L2C is 0027; Save52 is 0029/HIST-0267; Save2 is HIST-0245. S0/S0C (0006/0007) were consulted through their [manifest](manual-save-corpus/manifest.csv) and [reviewed zero controls](ordinary-outpost-beacon-detection.md), not freshly decoded here. S1/S1C/L2C live originals no longer exist at their frozen paths; their verified archived copies remain available and match original manifest hashes and previously decoded hashes. This limitation is recorded rather than silently substituting another live save. Save3, Save2 and Save52 originals actually present, and all archives actually read, match pre/post identities.

Installed inputs: Starfield.exe SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; Starfield.esm `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`. Native import metadata matches that executable, preferred image base `0x140000000`. Header versions do not establish the entire originating module/load-order profile. Existing CPython 3.14.3, stdlib zlib/mmap, Ghidra 12.1.2 and JDK 21 were used; no installation or third-party implementation reuse. Provenance: SOR-S-0113/0124/0127/0128 and existing SOR-S-0105 separate-tool credit.

## Save25 side-by-side evidence

All decimal offsets here are **decoded logical save-stream offsets**, with half-open record ranges. Three-byte tokens are tagged saved identities before load remapping, not pointers, runtime handles, or stable cross-session FormIDs. Four-byte unit-6 keys encode those tagged values little-endian. Native static VAs and compressed-file offsets are separate domains.

| Property | SOR-002 | SOR-003 |
|---|---|---|
| Beacon token / record ordinal | `822821` / 10330 | `84b985` / 12009 |
| R3 logical record | [1344506,1344824), body 1344573 | [1474148,1474483), body 1474224 |
| Saved type | Inherited/conditional REFR, case 5; no explicit type byte | Same supported representation |
| First parent / base / self queue | 1344518: `822834 / 6c60e9 / 822821` | 1474160: `84b996 / 6c60e9 / 84b985` |
| Effective base | Starfield.esm ACTI `002C60E9` | Same ordinary beacon base |
| Saved flags / disabled | 1344587: `00400409`; disabled bit 0x800 clear, deleted bit 0x20 clear | 1474238: same flags, same states |
| Saved name association | Queue index 668, string text at 6020711, length 7, `SOR-002` | Queue index 672, text at 6020810, length 7, `SOR-003` |
| Direct PNDT token | 232341: `0043F59F` → Kreet PNDT `0003F59F` | 232371: same direct PNDT token |
| Overlay parent / repeated key | 232345 / 232367: `00822834` | 232375 / 232397: `0084B996` |
| Observed kind | `0200` | `0200` |
| Pair start / raw 16 bytes | 232351: `3e7c5616334dccbf74c911eda75ce0bf` | 232381: `33fe6f484321ccbfac01c6cd5c5fe0bf` |
| Longitude radians | -0.2211059435912563 | -0.2197651008318516 |
| Latitude radians | -0.5113105421317372 | -0.5116409319889974 |
| Derived site degrees | (-12.668437393036639, -29.295936084694606) | (-12.591612761932074, -29.314866029109545) |
| Kreet system/body-index lead | 296224: (88327,15), source world `8147f8` | 296298: (88327,15), source world `8147f8` |
| Local XYZ start / raw bytes | 1344574: `a266f542eb858843efd19241` | 1474225: `0369b243f0b019457220ffc1` |
| Local X | 122.70045471191406 | 356.8204040527344 |
| Local Y | 273.0462341308594 | 2459.05859375 |
| Local Z | 18.352506637573242 | -31.89084243774414 |
| Rotation | Shape 0, no float rotation components present in this conditional prefix; reconstructed rotation UNKNOWN | Same omission; no asserted zero rotation |
| Cell / frame | No separate parent R3 record found; underlying source-world token lead above, exact cell identity UNKNOWN | Same coverage limit |

The XYZ tuple is structurally owned by each consumed beacon initial-data prefix; it is not a name-adjacent float guess. Its loaded world/reference frame, units and authority remain provisional. The first queued parent is proved as a saved association; calling it the loaded parent cell would go beyond the reader. The name queue also contains the previously observed deployment/loop animation strings. Name-based correspondence does not establish application UUIDs or player ownership.

The ordinary detector independently reports **two ordinary disabled-clear candidates**, no additional known-base reference-only candidates, and exact closure of **25,976** R3 records. The scoped direct-base catalog does not cover every faction/template/override path. 13,860 dynamic records lack reconstructed base identities. These counts do not establish exactly two active player-owned outposts. Both initial prefixes decode successfully; the extra-prefix walk stops at its existing version-unqualified ExtraFlags boundary, which does not invalidate earlier identity/flag fields.

## Body resolver ambiguity retained

SOR-003 has **two** results from the old empirical cache-window search: offset **293363** produces `(system=0,body=7,world=45c8dc)` and matches Uranus PNDT `0005DEC7`; offset **296298** produces Kreet `(88327,15,8147f8)`. The former occurs among a different sequence of reference-bearing bytes; it is not a second direct PNDT/angle record. Without a closed cache grammar it remains an unqualified search hit, not a verified Uranus ownership edge. The old extractor correctly leaves `proposed_body_formid=null` because its unfiltered cache options disagree; this output was not changed to force agreement.

The separate repeated-key spatial association is unique for SOR-003 and explicitly contains Kreet PNDT. Kreet GNAM independently supplies (88327,15), and the Kreet-shaped cache entry corroborates it. STDT `0005E630 NarionStar` has DNAM 88327 in the installed catalog. Therefore the best-supported scoped body/system is **Kreet / Narion**, with the cache-search coverage flaw disclosed. It is not inferred from the name, user location or JSON. This is a concrete limitation of the old search predicate on a new sample, not evidence that the earlier Kreet native/angle interpretation is wrong. All previous evidence and code remain unchanged; globally reliable cache qualification needs a closed enclosing grammar.

## Shared versus distinct, and earlier controls

| Test | Save25 result | Interpretation |
|---|---|---|
| Parent identity equality | False | Distinct serialized overlay/site keys |
| Direct body equality | True, `0003F59F` | Same body, independently associated |
| Pair bitwise equality | False in both doubles | Distinct saved angular anchors, not rounding noise |
| Local XYZ equality | False | Delta (234.1199493408203,2186.0123596191406,-50.24334907531738) |
| Underlying frame identity | Same `8147f8` Kreet-shaped source-world lead; exact cell/frame unproved | Shared base world is supported as a lead; numerical subtraction alone does not prove a common frame |

Best category: **distinct anchors**, supported within this sample. Continuous on-foot traversal and distinct serialization overlays can coexist. The smallest supported distinction is separate generated outpost/site parents within the traversed region. No tile-boundary crossing, cell boundary, outpost-centred origin or universal one-overlay-per-outpost rule follows.

Euclidean local displacement is **2199.087670197188 unassigned units**; site-direction separation is **0.0012150281390800263 radians**, about 0.069616 degrees. Longitude increases by 0.0013408427594046868 and latitude decreases by 0.00033038985726019376. The user-reported northward walk is not used to label +Y, reverse latitude or infer a terrain scale. The engine's established +Z/+X/+Y spherical convention is not calibrated to the local compass.

S1/S1C both use parent `822c8d`; L2C uses `816f39`. All three and SOR-002 share the exact first 16-byte pair above. S1/S1C/L2C local XYZ is `(122.6921157836914,277.25439453125,18.35177230834961)`. S1→SOR-002 delta is `(0.00833892822265625,-4.208160400390625,0.0007343292236328125)`, distance **4.20816872670038 unassigned units**. These agree qualitatively with approximate colocation but do not prove a matched frame or distance in metres. SOR-002's new parent and source-world token differ from S1's `8147fc`; L2C's is `8147e1`. Thus angular equality survives identity remapping; equality of tokens across sessions is neither required nor assumed.

Fresh Save3 detection remains zero under the same predicate. Fresh Save52 has 19 ordinary candidates, 17 clear/two set; all 17 name-matched network body/system pairs still agree after save extraction. Its two Feynman V pairs remain distinct; broader diversity supports body-versus-site separation without defining Save25's local transform. The JSON was read only after extraction and never supplies decoder body/system inputs. Fresh Save2 player parent `41251b`, record 1519861, has pair at 271659 exactly matching installed New Atlantis CNAM after latitude/longitude reversal. This validates pair semantics and fixed-world anchor reuse, not precise beacon placement or all projection branches.

## Coordinate transformation investigation

The prior [native/ESM coordinate chain](planetary-surface-anchor-semantics.md#decisive-native-and-definition-chain) remains working knowledge: longitude-first/latitude-second radians and analytical body direction. This pass followed actual call edges, using four [hashed exports](two-outpost-anchor/native-exports.csv). All addresses below are preferred static VAs in the pinned executable; in-memory field offsets are not save offsets. No native function was invoked.

| Native location | New scoped observation / relevance |
|---|---|
| `140ad01d0`, `1407b6360` | String assembly/body-world naming, not a local-to-spherical conversion. Following these plausible neighbours did not supply a transform. |
| `140ad0400` at `140ad0444`, `140ad054a` | Name-based lookup, then conditional generated-world creation via `140bb8c20`; subsequent component setup. Supports separate world/overlay registration, not world-local axis calibration. |
| `140ad31a0` → `140ad30a0`, operands `140ad3120–13d` | Exterior cell path selects a world or overlay by two integer coordinates and inclusive bounds. A shared source world need not identify a single placement overlay. Exact saved cell correspondence is not recovered. |
| `140ad3b20` → `140ad3c30`, `140ad3d64–78` | Given eligible world state, obtains body association, searches overlay entries by world ID at component +0x30 and copies the +0x20/+0x28 pair. It retrieves a site's pair; it does not add reference XYZ. |
| `1418ab8d0`, `1418aba4b–69`, `1418aba73–7e` | One branch registers an input pair with an existing world ID; another calls `140ad0650` to create/register a world. Registration can reuse or create rather than requiring a fresh planetary landing region. No claim that either branch ran for Save25. |
| `14077fc20`, `14077fd02–96` and `1407800d6` branch | Gets overlay angles through `140ad3b20`; converts selected/overlay angles to terrain indices with `14096eb90`; takes integer displacement with `14096f940`; combines displacement ×100 with reference +0x8c/+0x90/+0x94, matching previously established reference-position offsets. |
| `14077fd96–fe68` | Splits XY with float constant approximately 0.01 and floor-like integer selection; retains a sub-100 local remainder, adds an angle-derived local offset from `14078d370`, stores XYZ separately. This distinguishes an indexed site point from the exact local reference residual. |
| `14077fe91–ff76` | Converts the pair to terrain indices, adds integer local grid offsets through `14096f5c0`, builds normalized indexed coordinates from a live configuration sum and terrain-manager +0x50, then calls `142332410` to return angles. The final `14077ff7f–14078004a` path resamples those indices again. |
| `14078d370` | Reads current frame pair from manager +0xb0 or +0x1a8, index-converts it and an input pair, obtains integer displacement ×100; optionally queries terrain height. A frame origin and terrain manager are inputs beyond the three beacon floats. |

The named decompiler types are not treated as verified prototypes. The grid/position/100 assertions above were checked against instruction operands. Relevant constants were independently reread from mapped PE sections: VA `144f03eec` float bytes `0ad7233c` = 0.009999999776482582; `144f044e8` float `0000803f` = 1; `144f04718` double = 1; `144f046a8` double = 0.5. Local validation records original file offsets. This is evidence for a grid split in that branch, **not a metre scale or a bit-exact implementation of all edge/negative-boundary cases**.

Tested competing explanations:

| Hypothesis / test | Outcome |
|---|---|
| One identical anchor for the entire reported landing area | Rejected for these two saved associations: different parents and pair bits. |
| Distinct parent IDs but identical Save25 angles | Rejected; both doubles differ. Conversely S1→SOR-002 demonstrates equal angles with distinct serialized parents. |
| The pair alone is exact, continuously varying beacon position | Unsupported; S1→SOR-002 retains exactly equal angles despite different XYZ. Native branch retains a fractional local remainder separately from indexed angles. Quantized beacon/site placement is still possible; equality alone cannot identify anchor physical centre. |
| XYZ is itself a body-centred vector or angular tuple | Unsupported by reference-prefix provenance, different representations and native grid/frame inputs; no direct XYZ-to-angle formula validated. |
| Shared base local frame | Consistent with same Save25 source-world lead and uninterrupted travel; not proved without cell/overlay transform closure. Cross-session S1 numerical similarity is corroboration only. |
| Fit a tangent rotation/scale from these two placements | Underdetermined: one displacement pair cannot establish origin, two independent axes, scale, grid snapping and height treatment. No fitted conversion or inferred radius is delivered. |

**Best-supported relation:** each beacon has a saved local transform associated with a distinct planetary site parent; that parent supplies a body-oriented angular anchor. There is a native route relating an overlay's angular terrain indices to reference local XYZ through a manager-origin/index displacement and residual. Applying only the anchor's analytical spherical equation locates the site direction, not the beacon.

**Exact missing stages:** (1) establish Save25's parent/cell/world-to-terrain-manager frame correspondence; (2) recover the manager-origin pair, terrain grid resolution at +0x50 and configuration values `145ea66f0 + 145ea6770` for Kreet under this placement state; (3) close face/seam orientation and integer-index transforms `14096eb90/14096f940/14096f5c0` for those inputs; (4) establish how the fractional local XY remainder and elevation should project for a precise reference point rather than a snapped site; (5) validate against independent positions. Geographic north/prime-meridian calibration and metric/elevation accuracy remain separate from engine-body angular coordinates. A physical radius is needed for a metric surface position, but must not be invented to replace the engine's grid mapping.

No precise global planetary beacon coordinate or accuracy bound is defensibly derived in this pass. This is a bounded missing-mechanism result, not a claim that further offline analysis cannot succeed.

## Secondary leads and next discriminating step

| Lead | Basis and smallest follow-up |
|---|---|
| Separate overlay versus base-world registration | Save25 distinct parent/pair and shared `8147f8` lead; `140ad31a0/140ad30a0` selects by cell bounds. Close the enclosing cache/cell grammar before treating `8147f8` as a fully proved common frame. |
| Indexed anchor / sub-grid remainder | `14077fc20` split and projection above. First reproduce the native branch with independently recovered Kreet grid inputs, checking both beacons without using rough north to choose axes. |
| Typed body association rather than arbitrary windows | The Uranus-shaped hit at 293363 is a counterexample to blindly trusting every empirical cache match. Decode its enclosing collection before globally tightening the resolver. |
| Projection, poles, texture and resources | Existing [PL01–PL06 and prior-art register](planetary-surface-anchor/prior-art-and-leads.md) retain author/source/access restrictions. This task performs no new web sweep or external-code reuse. Engine terrain-grid projection does not establish appearance/resource UV equivalence. |

Smallest next step: recover the specific terrain-manager origin/resolution inputs and close the index-to-local bridge, then independently predict the second Save25 anchor from the first frame and the two local tuples. A third non-collinear position is needed to validate a general local axis/scale interpretation. If offline recovery stalls, separately brief disposable-save observation of matched parent/cell/frame, manager origin/resolution and exact reference positions. No live actions are authorized by that proposal.

## Validation and review handoff

[Evidence/reproduction package](two-outpost-anchor/README.md) contains exact file inventory, actual checks, script effects, local receipts and full tracked-plus-untracked diffs. A separate arithmetic walk confirms Save25's 25,976-record count/end closure; direct byte rereads confirm both names, queued base/self/parent, flags, XYZ and repeated-key PNDT/pairs. **72 existing offline tests pass**. Original/archive/catalog/JSON/ESM/executable preservation and all **15** Ghidra project files agree. No cap or failed decompilation marker occurs in the four new selected native exports; branch coverage and runtime validation remain absent.

Retained attempts: extract-01 copied/verified Save25 then stopped because an old live control path was absent, before decoding; extract-02/03 succeeded on their then-current code; extract-04 is final and includes detector/fixed/network cross-checks. One ad-hoc PowerShell-quoted Python probe failed to parse and read no save; a saved local probe replaced it. Prior successful receipts were not overwritten. Critical review must assess the new cache ambiguity, conditional frame claims and exact native branch interpretation before integration or semantic promotion.

Suggested commit after review, **not performed**: `research: compare two-outpost site anchors and bound beacon coordinates`.
