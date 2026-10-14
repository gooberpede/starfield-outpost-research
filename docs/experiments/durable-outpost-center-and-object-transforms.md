# SOR-EXP-0018 — Durable outpost center and placed-object transforms

2026-10-10, Australia/Sydney. SOR-EV-0026 / SOR-F-0023–0024 / SOR-ST-0023 / SOR-FN-0047–0049 / SOR-D-0037. Authorized by the retained [brief](../implementation-briefs/CODEX_BRIEF_SOR_durable_outpost_center_object_transforms.md) and the user's execution request. ANALYZED; critical review required. Authored results REVIEW-REQUIRED; raw inputs and bulk exports LOCAL-ONLY. [Selected tables, reproduction and complete review package](durable-center/README.md).

## Executive answer

**The durable local workshop center is reproducible from saved bytes and is exactly invariant across the deliberate beacon move. The controlled terrain origin is independently present in all nine existing runtime snapshots. Exact continuous center longitude/latitude is still OPEN.** This is a strong partial result, not the brief's complete geographic solution.

| Element | Answer and scope |
|---|---|
| Settled working model | Read the ordinary reference's saved initial XYZ and its typed Workshop compensation; compute `C = float32(P + delta)`. In the observed loaded Kreet frame, terrain origin is `(tag=1,I0=10464,J0=21120)`, resolution 256, block+merge 12, scale 100 native units per fine step. |
| Confidence | PROVEN sampled bytes/arithmetic; STATIC selected typed data flow; scoped STRONG interpretation proposed for preserved local center and ordinary reference transforms. Geographic fractional embedding and general saved-to-loaded frame selection remain PROVISIONAL/OPEN. Prior accepted findings retain their own review status. |
| Coverage | Fresh decodes of 23 archived saves, 128 selected reference prefixes; seven manual action/control pairs; both Save25/26 beacons; 19 mature beacon compensations; 53 mature storage and one same-base extractor references; nine existing snapshots / 18 beacon observations. All selected headers contain two 1.16.244.0 strings; historical loaded configuration is not inferred from them. |
| Geographic validation | Forty-one repeated/independent site/fixed-point rows reproduce the discrete projection, maxima `8.881784197001252e-16` longitude and `3.3306690738754696e-16` latitude radians. Repeated manual rows are controls, not forty-one independent geographical sites. |
| Completeness | No complete continuous planetary transform, full REFR/extra schema, all placed-object classes, authoritative ownership or safe integration interface is claimed. |
| Precise missing pieces | General selection/restoration of the ActivatedOverlayProperty translation for the serialized parent, and a demonstrated continuous consumer defining the subcell phase/embedding. The controlled loaded origin itself is now observed, rather than missing. |

Ordinary storage/extractor/solar references encode their own float32 XYZ and conditional float32 rotations in initial case 5. They are not encoded simply as displacement from the Workshop center. The controlled ordinary objects share a saved parent; the beacon has a different parent. A reference-frame difference is directly calculable; calling it a workshop-relative physical transform requires aligning those parents. No separate Workshop rotation enters the compensated-center helper.

## Bounded experiment plan

Question: can the persisted compensated workshop center be placed in the planetary chart independently of beacon movement, and what frame contains ordinary object translations?

Allowed: hash/read existing archived saves, installed definitions/executable and existing observer captures; export existing native analysis with `-readOnly -noanalysis`; execute existing project readers and independently authored stdlib numerical/record probes; consult public prior art and Wayback; write original reports and selected numerical tables. No game launch/load, debugger, deployment, save/configuration/database edits, dependencies, external communication/upload, staging, commit or push.

Inputs: protected Save25/26, manual S0–S7C archives, frozen Save3/S1/S1C/L2C/Save52/Save2 receipts, installed pinned executable/ESM and existing Ghidra project, nine observer checkpoints. Controls: unchanged SOR-002, within-session manual no-action successors, prior live no-action/reload checkpoints; Save25/26 themselves are not an isolated same-session save control. Held-out checks: mature same-body outposts and fixed cities after the controlled Kreet model.

Outputs: fresh ignored `.local-work/durable-center/` receipts and `.local-work/recon/durable-center-*.tsv`; original scripts, authored report and selected tables. Risks: wrong native type, token remapping, ambiguous save grammar, numerical overfitting and scratch exhaustion. Stop on mismatched trusted hashes, corruption, unsupported record branches (affected branch only), uncontrolled output, or free space below 40,000,000,000 bytes on relevant drives. Temporary decode mappings are cleaned by their existing context manager; originals and prior receipts are preserved.

Success: reproducible invariant geographic center without fitted per-outpost constants; useful partial success: exact local invariance, typed object transforms and a discriminating explanation of the missing terrain mapping. Falsification: compensation fails across move/reload; frame/orientation predicates disagree; model predicts different centers after relocation; held-out points need fitted corrections. Passing parser tests alone does not validate semantics.

## Provenance and address domains

Starting HEAD `278d901815496a0acce19f1ee39f7c4c194859a9`; the supplied brief was the sole pre-existing untracked file. No delegation occurred. CPython 3.14.3/stdlib/zlib and existing project readers were executed; Ghidra 12.1.2/JDK 21 exports used `-readOnly -noanalysis`, Xmx2G. No external implementation/dependency was incorporated. Bethesda's installed executable/content and user-controlled saves/captures remain SOR-S-0127/0128/0132 inputs, with prior project framing provenance SOR-S-0124 and separate tool credits SOR-S-0105/0113.

Pinned Starfield.exe SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, preferred image base `0x140000000`; installed Starfield.esm `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`. All native addresses below are static VAs in that executable; RVA = VA minus image base. Member offsets describe memory, not save offsets. All saved positions/field locations in tables are decoded-stream offsets. Saved tokens are remappable identities, not runtime handles or stable FormIDs.

The protected archive paths and original hashes come from frozen manifests, not filename matching alone. Save25 SOR-SAMPLE-0030 original `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`, decoded `0c27c10c1f07d5a480da4f857072cafc17e198b981350e01de2fa6b09f972cfd`; Save26 SOR-SAMPLE-0031 original `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104`, decoded `bb07dd976e369349a602c40461a4017b51aed88b81cc0acc5483220d9fcb6160`. Twenty-five archive/catalog/ESM receipts covering 23 saves are hashed before/after; separate native/database receipts protect the installed inputs. The database baseline was acquired after starting the first read-only export; its limited timing is disclosed, with all 17 protected file hashes also matching the earlier SOR-EV-0025 baseline. Four Ghidra index files (`idata/~index.bak`, `idata/~index.dat`, `versioned/~index.bak`, `versioned/~index.dat`) changed filesystem timestamps during read-only opening; sizes and hashes remained identical. No timestamps were restored and no analysis-content edit is observed. Original session files are freshly checked against the prior manifest: 5,265 files, nine non-atomic captures. No new live evidence was acquired.

## Transformation map

```text
saved reference token/base/parent + case-5 initial XYZ P_wire
  -> typed Workshop extra 0xbc, compensation delta
  -> C_wire = float32(P_wire + delta)
  -> select parent/world overlay and its valid ActivatedOverlayProperty
  -> apply the branch's frame translation T to reach loaded terrain frame
  -> C_loaded (controlled Save25/26: observed XYZ agrees exactly)
  -> qXY = floor(float32(C_loaded.XY * float32(0.01)))
  -> residualXY = float32(C_loaded.XY - 100*qXY), plus retained Z
  -> terrain origin + integer displacement, with hemisphere/seam handling
  -> (I,J,tag); N = 16*(10+2)*256 = 49152
  -> grid-centre square ((I+.5)/N-.5, (J+.5)/N-.5)
  -> native 142332410 -> quantized longitude/latitude
  -> continuous use of residualXY/Z: NOT established
```

The existing mathematical [projection](../../save-analysis/scripts/beacon_terrain_projection.py) implements the independently recovered nonlinear hemisphere chart. Its angular inverse is validated at discrete centers. In the controlled loaded frame the candidate continuous chart inputs can be written `s=I0+C.X/100`, `t=J0+C.Y/100`; this is a useful residual-preserving representation, **not validation of an exact geographic embedding**. Converting it with an arbitrarily selected half-step phase invents precision.

| Typed stage | Native evidence; direct observation versus interpretation |
|---|---|
| Saved initial transforms | `141835c20` reads XYZ (12 bytes), then one 4-byte rotation per shape bit 0/1/2, with separate parent/base/self reference queues handled by `141835610`. No Workshop subtraction occurs in this reader. |
| Omitted rotation default | `141835610` initializes the local transform rotation from constants `144ae80f0/144ae80f8`; fresh PE reads show all twelve bytes zero. Omitted axes therefore become zero in this initial-data branch, rather than carrying an uninitialized angle. This does not prove final runtime rotation after other processing. |
| Reference rotation restoration | `140b4e260` writes reference members +0x80/+0x84/+0x88. Type 0x4b additionally wraps Z by float32 `2*pi`, constant `144f049f4`, bytes `db0fc940` (PE offset 82,853,876). This supports radians for the restored reference angle family; full Euler order/handedness is unqualified. |
| Compensated center | Prior typed `140f4ab80` reads reference +0x8c/+0x90/+0x94 and Workshop extra +0x60/+0x64/+0x68. It adds translation without a Workshop orientation matrix. Prior producer/save/load chain remains in [EXP0017](workshop-origin-beacon-relocation-persistence.md). |
| Frame preparation | Fresh `141856d10`, called at `14181ae1b/14181b356`, copies reference XYZ, selects a world from the cell/active-world context, and conditionally subtracts a valid translation returned by `140ada3a0`. Predicate includes reference+0xd3 bit 1, overlay world kind and `140ada760` result. This is branch-dependent frame handling, not a universal absolute XYZ copy. |
| Active map selection | `140ad30a0` searches the world-keyed active edges, requires invalid byte edge+0x55 clear, and compares occupied integer XY against inclusive bounds edge+0x30..+0x3c. `140ad7200` retrieves the particular two-world-keyed edge. |
| Translation payload | `140ada3a0` returns `(100*int32(payload+8),100*int32(payload+0xc),float32(payload+0x30))`, valid only when payload+0x35 is clear. Payload starts at edge+0x20. This is **ActivatedOverlayProperty**, established through named wrappers in `140add310/140adcf50/140add850`, not a matching offset on Workshop::ExtraData. |
| Creation/copy path | `140ad7b80` registers a StoredComponent in manager+0x268; `140add310` registers its Edge in manager+0x300. `140adcfd0` transfers the typed payload. None of these export observations establishes the exact archived wire-to-selected-map correspondence. |
| Residual path | `14077fc20` carries a separate residual triplet. Fresh callers `14078b030/141a20380` and consumer `14077fbc0 -> 14077f900` lead to integer-grid differences, multiplied by 100, and cell traversal/selection. The inspected consumer does not convert the retained fraction into continuous spherical angles. This rejects that particular route as missing subcell ground truth, not all possible continuous consumers. |
| Pair difference path | `14078d2c0` converts two pairs to indices, differences them via `14096f940`, and multiplies by 100. This supports indexed translation between frames, not a continuous spherical metric. |

New exports and all cap/failure flags are identified in [native-exports.csv](durable-center/native-exports.csv). Decompiler pseudo-types such as IMAGE_DOS_HEADER on game objects are artifacts, not accepted structure names. Claims use explicit operands/type provenance and selected call chains. Large `141a20380` and other printed listings have 600-instruction caps; decompiled text and bounded follow-up windows were examined, without claiming exhaustive caller or writer enumeration.

## Save25/26 invariance and terrain frame

Exact selected [invariance table](durable-center/invariance.csv) includes identities, parent/base context, angles, decoded offsets, vector bytes and both deliberately unqualified continuous hypotheses.

| Site/sample | Saved token / parent | Current XYZ | Compensation XYZ | Computed center XYZ |
|---|---|---|---|---|
| SOR-002 / Save25 | 822821 / 822834 | (122.70045471191406,273.0462341308594,18.352506637573242) | (0,0,0) | same |
| SOR-002 / Save26 | 81ab50 / 81762f | same | (0,0,0) | same |
| SOR-003 / Save25 | 84b985 / 84b996 | (356.8204040527344,2459.05859375,-31.89084243774414) | (0,0,0) | same |
| SOR-003 / Save26 | 81ab8f / 81cb3d | (337.85345458984375,2406.418701171875,-35.21407699584961) | (18.966949462890625,52.639892578125,3.3232345581054688) | (356.8204040527344,2459.05859375,-31.89084243774414) |

SOR-003 beacon displacement is `(-18.966949462890625,-52.639892578125,-3.3232345581054688)`, norm **56.05129213936618 native units**. Both compensated centers have component delta `(0,0,0)` and **zero float32 bit errors** across files. SOR-003 center bytes are `0369b243f0b019457220ffc1`; SOR-002 `a266f542eb858843efd19241`. Correspondence uses each unchanged Workshop+0x98 identifier (`0efca066ee4c7b9b` / `f1517de43e171745`), names/base, selective transition and independent captures; it does not assume equal tokens or a universal UUID contract.

Both bodies are Kreet `0003F59F`; SOR-002 site pair `(-0.2211059435912563,-0.5113105421317372)` and SOR-003 `(-0.2197651008318516,-0.5116409319889974)` remain bit-identical. Save25/26 XYZ offsets and delta locations are retained in the CSV; compensation is directly serialized, whereas active-map/frame selection is reconstructed during load and activation. Do not conflate these classes.

Fresh raw [terrain checks](durable-center/terrain-captures.csv) recover mode 2, selected +0xc8 origin, southern tag 1, coarse `(54,110)`, sub `(8,0)`, fine `(0,0)`, giving `(10464,21120)` in **all nine checkpoints**, including move, save, reload and visit to SOR-002. Raw sections are hash-checked, not transcribed from prior summaries. Both beacons' saved XYZ match the corresponding captured reference bytes under the prior independently checked correspondence.

Compensated SOR-003 splits into q `(3,24)`, residual `(56.820404052734375,59.05859375)`; SOR-002 q `(1,2)`, residual `(22.700454711914062,73.04623413085938)`. This reproduces indices `(10467,21144)` / `(10465,21122)` using the observed common origin. **The move stays inside the same 100-unit XY cell even without compensation**, so unchanged site angles alone would not discriminate a durable-center model from current-position quantization. The exact compensated XYZ and explicit native consumer provide the discriminating evidence.

## Cross-outpost challenge and nonempty Workshop resource tables

The new optional resource reader follows `140f50880/140f515a0/1402cef80`: uint32 group count; per group one queued resource reference and uint32 row count; per row two queued references and seventeen body bytes (4+4+1+4+4). References occupy the separate relocation queue. This is a typed modern prefix, **not seventeen contiguous bytes including identities**. Counts and both queues are bounded; following extras and production semantics remain unclassified. The historical zero-resource reader still rejects nonempty tables unless the new callback is explicitly supplied.

This closes the previous specific parser boundary. All 19 mature beacons now yield compensation, all exactly twelve zero bytes. L2C and the manual resource-bearing beacon also decode. Their later +0x98 identifiers are reported within the modern sampled branch, not transferred to older saves.

The [41-row projection ledger](durable-center/projection.csv) includes earlier Kreet controls, Save25/26, L2C, 17 mature direct pairs and three fixed ESM cities. Save3 and Save2/HIST-0245 contain no ordinary beacon under this detector; Save2's freshly extracted player/site pair `(2.2810355988151545,0.7111154993616507)` equals the installed New Atlantis ESM pair exactly; this is a fixed-location control, not a newly located player center. Cydonia/New Atlantis/Akila reproduce with the same chart constants. Feynman V `0005E0DE` has distinct mature indices `(25124,32446)` and `(37536,20928)`, both compensated vectors zero; both reproduce the discrete pairs without fitted corrections. These checks validate the projection and zero-vector interpretation, **not an independent exact center truth** at those sites. Network JSON is never an input to the new derivation.

The prior negative-X counterexample survives the stronger reader: mature token `84ede9`, body `0005E0DB`, XYZ `(-53.4358024597168,58.03339767456055,8.46107006072998)`, compensation zero, initial frame flag `0x2b`, site index `(13152,45120)`. Occupied-cell subtraction gives origin `(13153,45120)`; retained/snapped-site interpretation gives `(13152,45120)`. The disagreement is one fine step. **Workshop compensation cannot explain it in this sample.** Controlled beacon flags are `0x0b`; mature clear examples include `0x2b`, involving native frame handling. This is a concrete reason to require selected overlay/rebase state for generalization, not a rejection of the hemisphere projection.

## Object-transform matrix and orientation

Fresh installed definitions identify static bases `0023AED9` OutpostStorageSolid01Sm (CONT), `0005EF19` OutpostHarvesterSolid_Iron_01 (CONT), `002031E1` OutpostPowerSolarArray03 (ACTI). These agree with the controlled inline direct tokens. Source identity and offsets remain local in `definitions-and-rotation.json`. Mature inspection uses the same specific bases: 53 storage and one extractor references, **zero same-base solar**; this is not absence of other solar definitions.

| Object / transitions | Translation evidence | Rotation / membership status |
|---|---|---|
| Beacon | Own case 5 XYZ; different parent from ordinary objects; Workshop vector yields invariant center for SOR-003 | Controlled shape 0, initial omitted axes restore as zero in the mapped branch. No independent Workshop rotation appears in its center helper. |
| Storage, S2 onward | Own case 5 XYZ `(126.20349884033203,275.5676574707031,18.18954849243164)`; parent 8147fb in S3; retained through all subsequent manual controls | Shape 4 stores only axis 2, float32 bytes `49b4253e` =0.16182054579257965. x/y default zero in this branch. Saved presence is not by itself complete ownership. |
| Extractor, S3–S6C | Own XYZ `(106.12486267089844,279.8920593261719,16.820655822753906)`; same parent 8147fb; absent from selected framed records at S7/S7C | Shape 0. Workshop resource group 4057c7 contains queued pair `(822da9,45ef19)` through S6; group disappears at S7. Strong scoped resource-object association, not universal membership enumeration. |
| Solar, S3–S5C | Own XYZ `(111.92146301269531,269.6281433105469,16.874279022216797)`; same parent 8147fb | Shape 0. No rotation mutation during the recorded move; no workshop resource-table membership inferred from proximity. |
| Solar, S6 onward | Own XYZ `(107.60543060302734,248.40133666992188,15.988268852233887)`; displacement `(-4.316032409667969,-21.226806640625,-0.8860101699829102)` | Same identity/base/parent inside the reported continuous session; subsequent controls retain exact XYZ/rotation bytes. |

All seven action/no-action pairs preserve selected XYZ and present rotation bytes exactly. L2C's same definitions and transform tuples recur under new tokens and a different ordinary-object parent `8147e0`; correspondence is by base/tuple/site/context rather than literal token equality. [Selected object rows](durable-center/object-transforms.csv) include offsets and six mature object checks. No ordinary placed object with these same bases appears in Save25/26 under this predicate, so **beacon relocation while retaining these ordinary objects was not tested**.

Subtracting the manual beacon from the ordinary tuples gives storage `(3.511383056640625,-1.686737060546875,-0.16222381591796875)`, extractor `(-16.56725311279297,2.637664794921875,-1.5311164855957031)`, solar before `(-10.770652770996094,-7.626251220703125,-1.4774932861328125)`. These are useful **frame-unqualified candidate offsets** because the beacon's parent is 822c8d, not 8147fb. Differences among ordinary objects sharing 8147fb are directly same-parent reference differences. Numerically plausible distances do not clear the separate parent alignment requirement.

The best-supported representation is **own parent/world reference transforms with conditional overlay rebasing**, with workshop-relative translation derived after alignment. The studied case 5 prefixes do not require a placement-parent/snap transform to decode their position; case 6 and later attachment extras exist and are outside this conclusion. Rotation is conditional little-endian float32; initial omissions default to zero; radians are supported by the reference setter's2pi modulus. Axis composition order, handedness, snap-chain composition and all final runtime orientation remain OPEN. A separate outpost rotation has not been demonstrated; none is needed for the studied center helper. This is scoped positive data flow, not an absence proof over every Workshop field.

## Competing continuous models and exact stopping boundary

Using the **same observed** Kreet origin and compensated SOR-003 XYZ, two unqualified extensions give:

| Continuous chart phase | Longitude / latitude radians |
|---|---|
| `from_square(tag,(s+.5)/N-.5,(t+.5)/N-.5)` | (-0.21973838091541562,-0.5116797847638825) |
| `from_square(tag,s/N-.5,t/N-.5)` | (-0.21976066051647306,-0.5116457946804763) |

Difference is `(2.227960105743998e-05,-3.3990083406210125e-05)` radians. Both remain exactly invariant across Save25/26 because their compensated input is identical. The separate discrete-grid model reproduces the observed site pairs regardless of which continuous extension is proposed. Neither extension was exercised by a demonstrated continuous consumer; these numbers are **not calibrated planetary coordinates**. Invariance alone cannot select a phase, flat-tile embedding, tangent approximation, or other residual function. Z is retained locally but absent from the studied pair conversion; no radial/altitude interpretation or surface distance is invented.

Generalization additionally requires the exact activated edge selected for a serialized world/parent and occupied cell: payload +8/+0xc/+0x30/+0x35 and its world-key tuple/bounds. Existing captures contain manager origin and world prefixes but do not walk this component edge's payload. The saved unit 6 site association is not that selected translation record. Fresh native work follows registration, copy, selection, save-side subtraction, pair/residual consumers and their callers; it does not close the component wire-restoration path or prove that no such saved information exists.

Smallest next acquisition, **proposal only**: first export the exact ActivatedOverlayProperty component serialization/activation descriptor and identify its restored world-key/bounds/payload mapping in these same archives. If that remains ambiguous, a separately approved bounded read-only capture should read the **selected** component key, bounds, +8/+0xc/+0x30/+0x35, effective origin, same-parent ordinary reference and compensated center at one settled Kreet checkpoint and one `0x2b` mature case. No movement, new save, border test, or native call is needed to answer frame selection. Continuous geography additionally needs the actual residual-to-body consumer (or an independently calibrated subcell fixed point); another quantized Starmap reading would not distinguish the above models. There is no claim that all authorized offline paths are exhausted, and no new live authority follows from this recommendation.

## Prior art and access outcome

SOR-S-0130/0131 revisited on 2026-10-10. [Tinbite Solomon/omaops, Celestial Positioning System — GPS for Starfield](https://www.nexusmods.com/starfield/mods/17020), listing2.2.0, original upload 2026-05-09, update 2026-06-21: description and permissions accessible. It reports Starmap-based planetary readings and separate local XYZ; it supplies no source equation or saved activated-map schema. Its claimed four-decimal display precision is not an independent continuous-position accuracy bound. Upload is prohibited; modification requires permission; assets have stated credit/commercial/donation conditions. These terms are recorded as consultation metadata, **not accepted code/asset reuse authority**. No download, installation or implementation inspection occurred.

Both original Reddit URLs again failed direct access: [Found a perfect example of Starfield's tiling](https://old.reddit.com/r/Starfield/comments/1vqcjk3/found_a_perfect_example_of_starfields_tiling/) and [Observations on Starfield's Tile System](https://old.reddit.com/r/NoSodiumStarfield/comments/1cr7w8t/obervations_on_starfields_tile_system/). Following the user's instruction, Wayback replay requests using `/web/20260000000000/` and a CDX query for `reddit.com/r/NoSodiumStarfield/comments/1cr7w8t/*` were attempted; the web tool returned inaccessible/internal-error responses. Exact-ID searches returned no results. No authenticated archive timestamp, complete text or author was recovered. This is **failed retrieval, not proof of no archived copies**. Earlier authorship UNKNOWN remains UNKNOWN; no inferred permission or reconstructed quotation.

Resource/texture UV mapping, repeated tiles/2×2 features, rotation/mirroring, poles/prime meridian and variable-size components remain source leads in [the prior-art register](planetary-surface-anchor/prior-art-and-leads.md). Native `140accc10` does use definition-dependent extent fields +0x40/+0x44 in one overlay-bound calculation; that is not confirmation of the Reddit 2×2 claim. None of these appearance observations supplies a continuous residual embedding or metric radius. No third-party material incorporated, upstream contact, fork or PR; no permission exception needed.

## Verification and handoff

[Reproduction and checks](durable-center/README.md) identify all changed/new files and the unstaged/untracked-inclusive local review diff. Synthetic tests cover finite/vector errors, float32 cancellation, negative grid floors, rotation truncation, phase ambiguity and independent resource/body queues. Corpus checks assert primary identifier correspondence, exact compensated-center bits, unchanged angles, seven controls and 19 zero mature compensations. They do not validate the unresolved geographic semantics. Original native/capture data remain local; selected authored numbers and reports require scientific and rights/privacy review. No existing finding was silently promoted or replaced. Suggested commit after critical review: `research: investigate durable outpost center and object transforms`.
