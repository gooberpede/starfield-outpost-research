# SOR-EXP-0017 — Workshop origin, beacon relocation, persistence and radius

2026-10-10, Australia/Sydney. ANALYZED; SOR-EV-0025 / SOR-F-0021–0022. [Authorized brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_workshop_origin_beacon_relocation_persistence.md`), SOR-D-0036. [Review package, selected evidence and reproduction](workshop-origin/README.md). Authored interpretation REVIEW-REQUIRED; original saves, captures, full native exports and private receipts LOCAL-ONLY. Critical review is pending. No live work, staging, commit or push.

## Answers and coverage

| Question | Best-supported answer | Confidence and coverage | Concrete remaining limit |
|---|---|---|---|
| What is workshop +0x60? | Three float32 components in **Workshop::ExtraData**, extra type 0xbc, that compensate the reference position. The center helper explicitly adds them to current reference XYZ. | PROVEN bytes/arithmetic and selected STATIC data flow; **scoped STRONG semantics proposed** for SOR-003 relocation, with unchanged SOR-002 control. | No universal immutable birth-position claim. A creation/finalization path resets the vector, and float32 accumulation can round. |
| How does it return after reload? | **Direct serialization**, not merely an unlocated reconstruction hypothesis: the native saver writes +0x60/+0x68 as 12 body bytes, the native loader reads 12 bytes back, and the framed Save26 Workshop payload contains exactly the captured vector. | PROVEN selected save bytes/static copy operations; **STRONG cross-validated persistence chain proposed** for two beacons in Save25/26, one recorded reload. | The actual serializer/loader was not traced live. The research reader covers the modern zero-resource Workshop prefix, not every extra or version. |
| Does the center move with this beacon? | `float32(current XYZ + delta)` recovers the pre-move center exactly in all nine snapshots. Native border drawing uses that compensated center. | PROVEN arithmetic; **STRONG original-center/border relationship proposed**, matching the operator's no-visible-shift report. | Effective placement descriptor was not captured; arbitrary region/volume bounds and every permission rejection are not reduced to one circle. |
| What is the radius? | The installed ordinary beacon definition sets **OutpostBuildAreaRadius = 150.0 native coordinate units** (diameter 300 for the circular branch). A separate native fallback is **71.40000152587890625** units. | PROVEN installed definition/constants, STATIC conditional getter and geometric consumers; **STRONG ordinary-default interpretation proposed**. | No live effective-radius measurement, all-load-order override merge, skill/type universality or independently defensible metre conversion. Do not substitute the user's 100 m estimate. |
| Does the offset matter geographically? | A terrain/overlay consumer uses the compensated center plus its frame translation before converting to discrete terrain indices and angular coverage. Both saved site-angle pairs stay bit-identical during relocation. | PROVEN selected pair bytes and STATIC center-to-terrain data flow. | This is an overlay/coverage path, not a validated continuous planetary position of the moved beacon. World authority and fractional embedding remain open. |

Confidence, coverage, completeness and publication eligibility are separate. This pass identifies concrete consumers and the saved field; it does not claim all writers/consumers or all outpost bounds are enumerated.

## Experiment, inputs and preservation

Question: explain the relocation vector and its persisted representation, then follow direct center/bounds/terrain consumers. Authorized operations were read-only archived-save/capture/ESM/PE analysis and existing Ghidra `-readOnly -noanalysis` exports, plus original scripts, tests, local scratch and authored records. No process/game/configuration/database mutation, download, external communication or upload was performed. Risks were misidentifying an offset/type, mistaking a literal for a serializer, confusing remapped tokens, interpreting background churn as causality, and excessive scratch. Stop conditions: actual evidence corruption, untrusted input identity, uncontrolled output or available space below 40,000,000,000 bytes on C:/D:. Temporary decoded mappings close and scratch files are removed automatically; ignored receipts/exports are retained for review.

Pinned executable SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, version 1.16.244.0, static image base `0x140000000`. Static addresses below belong only to this image; **RVA = static VA − 0x140000000**. The prior session's actual module base was `0x00007ff73b380000`; raw workshop vtables minus that base equal RVA `0x4c24e60` in all 18 selected object observations. Runtime reference/extra pointers, FormIDs, saved tokens and decoded offsets remain separate domains.

| Input | Original bytes / SHA-256 | Decoded bytes / SHA-256 |
|---|---|---|
| SOR-SAMPLE-0030 / Save25 | 2,403,744 / `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5` | 6,553,789 / `0c27c10c1f07d5a480da4f857072cafc17e198b981350e01de2fa6b09f972cfd` |
| SOR-SAMPLE-0031 / Save26 | 2,409,024 / `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104` | 6,534,763 / `bb07dd976e369349a602c40461a4017b51aed88b81cc0acc5483220d9fcb6160` |

Save26 is resolved from the prior session's `final-summary.json` exact `save.archive`/hash entry, not a filename glob. Save25 is resolved from its protected archive entry in the same manifest. Exact filenames are in the retained brief and local receipts. All 5,265 files in the session manifest are freshly hashed against that manifest, covering all nine journals and 5,233 raw sections. Captures are guarded, non-atomic worker reads from the already completed observer session; this task did not run the observer. The archived journal acquisition method and operator conditions remain [SOR-EV-0024](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/beacon-observer-initial-live-results.md`).

The installed ESM/catalog and executable, exact archived saves and database-file inventory are hashed before/after fresh offline passes. The first new native export preceded this task's contemporaneous database snapshot: the snapshot directly brackets subsequent work, not the first exports. All native invocations used read-only/no-analysis, and no database edits were requested. Final preservation receipts retain that timing limit. Original capture content is independently checked against the earlier frozen manifest. Tool and project-script identities are local. No new originating-game baseline is inferred for historical controls.

## Reproduced runtime field arithmetic

Current position lives at **reference +0x8c**, compensation at **Workshop::ExtraData +0x60**. For moved reference `FF01AB8F`:

| State | XYZ float32 LE hex | Exact decoded XYZ |
|---|---|---|
| baseline/control/premove | `0369b243f0b019457220ffc1` | (356.820404052734375, 2459.05859375, −31.890842437744140625) |
| moved/save/reload/reload-control/visit/control | `3eeda843b366164537db0cc2` | (337.85345458984375, 2406.418701171875, −35.214076995849609375) |
| compensation after move | `50bc9741408f5242e0af5440` | (18.966949462890625, 52.639892578125, 3.32323455810546875) |

Each subtraction and addition is rounded to float32 separately. All nine snapshots satisfy both byte equalities: delta = rounded(original − current); original = rounded(current + delta). Control `FF01AB50` keeps XYZ `a266f542eb858843efd19241` and zero compensation. [Selected capture ledger](workshop-origin/captures.csv) records exact UTC read timestamps, root/file/hash locators, identities, float bits and the corresponding raw workshop section. Full runtime pointers stay in local evidence. Different reference and workshop reads are not atomic; the exact stable matches do not change that acquisition limit. Both workshop pointers change on reload; their type/vtable and persisted fields are reacquired and checked.

## Concrete native type, writers and consumers

Full original disassembly/decompilation stays under ignored `.local-work/recon/workshop-origin-*`. [Native mapping](workshop-origin/native-map.csv) gives static VA/RVA, decisive call sites, export names and hashes; local PE receipts give original-file offsets and instruction bytes. Descriptive roles below are research aliases, not renamed Ghidra symbols or established public APIs.

| Static function / decisive sites | Established data flow and limit |
|---|---|
| `140f4ffc0`, `14053dd30`, `140f51350` | Constructor writes type byte 0xbc at +0x12 and `Workshop::ExtraData` vtable `144c24e60`; initializes +0x60/+0x68 from a verified all-zero constant. The allocator requests 0xa0 bytes; REFR accessor checks activator type/keyword and reads reference+0xc8's extra list. This closes the same-object-type requirement, rather than relying on offset text. |
| `1421b11a0`, `1421b131d–1421b1421` | Gated ordinary-activator/keyword path obtains **type 0xbc** from the workshop-owning reference at operation-context +0x608. It resolves references from operation endpoints +0x278 and +0x268 and computes `delta += endpoint278.XYZ − endpoint268.XYZ`, independently per component with scalar float32 arithmetic. Stores at `1421b140d/1417/1421`. Calls from `1421b1450` and `1421b44b0` include endpoint swapping; the resolved old/new labels are inferred from the observed move and operation context, while the subtraction order is directly proven. No rotation matrix appears in this update. |
| `1421b2e20`, window around `1421b3ee7` | Creation/finalization path obtains Workshop via the create-enabled accessor and resets +0x60/+0x68 to zero before registration/update. This is a counterexample to treating the field as an immutable lifetime origin or every write as relocation. |
| `140f50660`, `140f50825/50832` | Saver appends exactly 8+4 bytes from +0x60/+0x68 after +0x78, before +0x98. Separate handle and string queues carry references/names. |
| `140521620` case 0xbc, `140f50880`, `140f51164–140f51171` | Extra dispatch allocates/finds this concrete type and loads 12 bytes directly into +0x60 via `141865020` (bounded buffer memcpy). +0x98 is read only for buffer version ≥0x89; earlier versions call its generator. This is why the reader must not transfer modern wire positions to older saves. |
| `140f4ab80`, `140f4abdc–140f4ac3f` | Copies reference XYZ, obtains extra type 0xbc, reads +0x60/+0x68, and adds nonzero components. No planetary projection or rotation occurs here. Exact zero bypasses addition. |
| `140f4a140`, `140f49440`, `140f49c50` | Descriptor construction and named `WorkshopBorderRegion`/`WorkshopBorderRadius` drawing use `140f4ab80`. The circular path consumes the selected radius; height placement has separate offsets/terrain sampling. Visible border construction and the position helper are directly linked. |
| `140f4a910`, `140f4ac50`, `140f4aab0` | Descriptor dispatch distinguishes region, volume, circle and permissive branches. Circle predicate checks **XY squared distance ≤ radius² AND point.Z ≤ supplied ceiling**; indexed centers can receive frame-origin translation. It is not a sphere or a symmetric ±Z bound. A separate wrapper qualifies parent/world identity. Full gameplay permission additionally has other consumers/conditions. |
| `1421bb860` | Uses compensated active-workshop center and radius to clamp a point outside the XY circle; preserves the input Z. This independently confirms horizontal circle semantics for this consumer, not every build rule. |
| `1421b2570` | Supplies compensated XYZ plus radius to another loaded-state consumer. Geometry's downstream authority is not fully mapped. |
| `140ad0b90`, `140ad0c36/140ad0c48` | Uses compensated center and radius in a terrain/overlay coverage computation; see geographic section. |

The broad instruction inventory examined **13,986,298 existing instructions**, selecting 47,888 non-RSP/RBP textual +0x60/+0x68 operands in static `[140000000,143800000)`. It helped identify the actual accumulating writer. It is an exploratory candidate inventory, not type analysis or an exhaustive writer proof: other offsets, pointer arithmetic, stack aliases, undefined code, indirect calls and code beyond that range are not covered. Only candidates with established concrete type/data flow are classified above. Some large-function exports reach the existing 600-instruction printing limit; full decompilation and separate decisive instruction windows are retained. No absence claim is based on those limits.

## Save25 → Save26: record-aware persistence

Cross-file tokens are **not equal**. Workshop +0x98's generated 64-bit identifier remains equal across matched saved records and runtime captures, along with name/base, the expected selective XYZ transition, neighboring Workshop fields and unchanged control. That supports a strong scoped correspondence, not a universal globally unique ID contract. Save26's dynamic saved tokens also correspond numerically to the captured `FF01AB50/FF01AB8F` under the existing tagged-token rule; Save25 is subject to load remapping.

All offsets in this table are **decoded-stream byte offsets**, never compressed-file or runtime offsets:

| Beacon/sample | Record [start,end) | Saved token / parent | XYZ start | Workshop type-byte start | Delta start / within body |
|---|---|---|---|---|---|
| SOR-002 Save25 | [1344506,1344824) | 822821 / 822834 | 1344574 | 1344609 | 1344620 / +47 |
| SOR-002 Save26 | [1359542,1359860) | 81ab50 / 81762f | 1359610 | 1359645 | 1359656 / +47 |
| SOR-003 Save25 | [1474148,1474483) | 84b985 / 84b996 | 1474225 | 1474260 | 1474271 / +47 |
| SOR-003 Save26 | [1361639,1361970) | 81ab8f / 81cb3d | 1361713 | 1361748 | 1361759 / +47 |

The bounded reader walks the framed case-5 initial/general prefix, leading modern extras 0x9c/0xda/0x4c, then 0xbc, with **separate reference and string cursors**. It does not locate the field by searching for the expected vector. These four Workshop payloads have zero resource-table entries, one queued handle, one +0x94 byte, one queued name, four +0x78 bytes, twelve compensation bytes, and eight +0x98 bytes. For these samples the displacement is Workshop-type-byte +11, but that is **not a general wire offset**: variable table/handle grammar can move it. Following extras are deliberately left undecoded.

The +0x78 words remain 1 for SOR-002 and 2 for SOR-003 (unassigned meaning); +0x94 remains zero. Workshop +0x98 bytes remain `f1517de43e171745` and `0efca066ee4c7b9b`, respectively. All four selected fields, plus XYZ, exactly match the appropriate baseline/saved/reloaded raw captures. After relocation, the literal displacement occurs once in the entire decoded Save26, inside SOR-003's correctly framed Workshop prefix; it occurs zero times in Save25. Those search counts are cross-checks, not the field parser's premise.

The resulting chain is:

`typed relocation update → Workshop +0x60 → native saver 8+4 body bytes → Save26 framed extra 0xbc → native loader 12-byte copy → reacquired Workshop +0x60 → compensated center helper`.

The actual runtime invocation of those native functions was not instrumented; direct serialization is nonetheless substantially supported by explicit matching saver/loader type flow and exact record/runtime values. A model in which the field is *only* recomputed from two saved absolute positions is displaced within this modern sample scope. Other reconstruction/rebase paths are not excluded. No save was edited to establish load authority.

Saved parent tokens and cached source-world tokens remap. Direct body IDs remain Kreet `0003F59F`, and both 16-byte site-angle pairs remain identical: SOR-002 `3e7c5616334dccbf74c911eda75ce0bf`; SOR-003 `33fe6f484321ccbfac01c6cd5c5fe0bf`. The previous Save25 unframed Uranus-shaped cache lead is retained; Save26 has only the matching Kreet-shaped cache hit for this candidate. This illustrates why unframed cache matches are not authoritative body evidence. Runtime terrain origin/resolution fields remain equal in the existing move/reload/site captures; this does not prove every saved overlay/map field is unchanged.

Save25/26 are separated by loading, movement/UI activity, elapsed time and a save, without a same-session no-action **save pair**. Runtime controls exist, but they cannot classify every unrelated saved change. SOR-003's saved form flags also change `0x00400409 → 0x00400408`; declared extra count stays eight, but record size changes 335→331 as its reference queue loses an entry. SOR-002 retains its 318-byte framed length and flags. Reordering/remapping and the whole decoded-size change are not assigned to the beacon move. Entire parent/overlay schemas and all background churn are not decoded here.

## Radius, boundaries and units

Independent fresh ESM parsing reproduces the older xEdit observation at [SOR-S-0103](../SOURCES.md): ordinary ACTI `002C60E9`, PRPS entry bytes `c53f06000000164300000000`, associate AVIF `00063FC5` **OutpostBuildAreaRadius** with float32 `0x43160000 = 150.0`. ESM original record offset 3,761,304; the record is compressed, so a decompressed subrecord offset must not be called an original-file PRPS offset. AVIF's own default is zero; the ordinary beacon's property supplies 150. DFOB `00063FC6` **WorkshopBuildRadiusAV** points to `00063FC5`. Native initializer `140157cc0` constructs the named default-object binding; radius getter `140f38e30` consumes its resolved +0x48 pointer at `145f0ba28`.

The getter obtains the relevant current workshop/object property context, searches its property collection via `14044b670`, and, if zero, can search linked objects; it falls back to INI setting value at `145f0b320`. Initializer `140157700` binds that setting as **fItemPlacementRadius:Workshop**, using float32 bytes `cdcc8e42` at static `144f04c5c` (RVA `4f04c5c`, original PE file offset 82,854,492), exactly **71.40000152587890625**. Zero/missing property and current-workshop context are material conditions. This is a configurable fallback, not another proof of the ordinary 150-unit radius. Unbacked PE global reads were recorded as such, then followed to their initializer rather than interpreted as zero-valued file data.

The circular descriptor stores the radius at +0x28 and compensated center at +0x00; center selection can encode a frame index at +0x0c. Its caller passes that radius to `140f4ac50`. The visual radius path and clamp use the same getter. Region/volume/interior branches, vertical ceiling offsets and restricted-build areas remain separate. **WorkshopRestrictedBuildRadius**, AVIF `0006CA31`, and DFOB `0006CE60` are a different property/binding; this pass does not conflate their exclusion/ownership rules with the ordinary outpost circle. Snap/connection query ranges are secondary leads, not candidate substitutes for the circle.

Radius and local XYZ are dimensionally shared by the distance comparisons; this establishes native coordinate-unit compatibility. No independent physical calibration was found or executed. In particular the terrain code's 100-unit indexing and the operator's approximate movement/distance descriptions do not establish a metre conversion. Report **150 native units / conditional circular diameter 300 native units**. Effective live radius, configuration/skill/quest variation and a complete authoritative build permission predicate remain unmeasured. The default radius is definition-derived; runtime modifications and any saved actor-value overrides require separate decoding. No explicit radius word is identified in the decoded Workshop prefix, and this is not an absence proof for the whole save.

## Geographic connection and alternatives

`140ad0b90` first qualifies the beacon's concrete ordinary type/keyword, then calls the compensated-center helper at `140ad0c36` and radius getter at `140ad0c48`. It adds a separate frame translation to center XY, multiplies by a native constant, floors the result, and calls the terrain-index helper `14096f5c0`; radius similarly bounds an index neighborhood with an additional buffer. It normalizes selected indices with the established terrain resolution/subdivision terms and converts them through the body chart. This is a direct **workshop center → translated terrain/grid coverage** connection. It explains why retaining the center can matter beyond a drawn border. Exact buffer/coverage authority is a secondary lead; no generic terrain-generation model was built.

Six distinct quantities remain explicit: body identity; saved overlay/site lon/lat; terrain frame/origin; compensated workshop center; current reference XYZ; exact planetary beacon position. For SOR-003 the current reference moves while the first four tested quantities remain compatible with a fixed original workshop/site center. The existing discrete 49,152-grid result is not extended into an unvalidated continuous coordinate formula. A compensated-center consumer does not mean every reference-position consumer should add the offset: doing so to locate the **current beacon** would return its former position in this sample.

| Explanation/prediction | Test and outcome |
|---|---|
| +0x60 belongs to an unrelated structure | Rejected for selected objects: runtime vtable RVA/type match constructor and explicit typed lookup in producer/consumer/load dispatch. |
| Offset is only a geographic or boundary-independent cache | Narrowed: explicit center helper feeds named border geometry, circular descriptor/clamp and terrain coverage. Other uses remain possible. |
| Reload merely reconstructs the vector from unrelated positions | Displaced as the sole explanation here: framed field and direct native saver/loader match all 12 bytes. A live loader trace is still absent. |
| Vector always equals birth position minus current position | Too broad: a separate finalization path resets it. Accumulation predicts preserved center over repeated relocations only while that path/frame applies, subject to float rounding. |
| All outposts have a 150-unit spherical bound | Unsupported: radius getter is conditional/configurable; circle predicate is XY plus upper ceiling and descriptor dispatch has other geometries. |
| Saved site pair is current beacon's exact planetary position | Contradicted within this relocation: site pairs remain bit-identical while current XYZ changes. Exact frame/residual embedding is still open. |

## Recommended follow-up and review boundary

Highest-information new live test, **proposal only**: on a protected disposable successor, capture the active radius property's resolved object/value, selected boundary descriptor (mode, translated center, radius, ceiling) and current reference/workshop fields before a second finite relocation, after it, and after one reload. Record one just-inside and one just-outside horizontal permission result at measured native offsets, plus one vertical comparison. This tests accumulation, active branch/default, and whether the geometric predicate matches actual permission. Require a separate exact live brief for input/build hashes, capture method, permitted actions/hooks/native calls, finite bounds, protected originals, evidence flushing and exit/recovery. This proposal authorizes no launch, deployment, attachment, move or save.

Before integration, critically review the typed field/prefix grammar, +0x98 correspondence limits, inferred old/new endpoint roles, conditional radius and geometry claims, geographic coverage role, preservation timing and publication eligibility. No safe mod integration point or completed general planetary transform is claimed.

## Provenance and checks

Bethesda's installed native/content and user-controlled saves/captures supply source material (SOR-S-0127/0128/0132 and original SOR-EV-0024). Ghidra/JDK and installed CPython/stdlib/zlib are separately executed existing tools (SOR-S-0105/0113); earlier project framing/association methods retain SOR-S-0124 provenance. Original new readers are source-informed by the actual native operations, not claimed clean-room work. No outside implementation, dependency, fork, PR, upstream contact or external source consultation was added. [Credits](../../CREDITS.md) and [sources](../SOURCES.md) are updated.

Actual checks, limits, preservation receipts and the full unstaged/untracked review diff are indexed in [the review package](workshop-origin/README.md). Raw proprietary or private artifacts remain ignored and untracked. Suggested commit after critical approval: `research: trace workshop relocation offset and outpost bounds`.

## Independent archive challenges and final checks

Fresh hash-pinned S1/S1C decodes each yield one supported Workshop prefix, with identical zero compensation. The mature HIST-0267 archive yields 19 ordinary candidates: two zero-resource prefixes decode with zero compensation; 17 explicitly stop at nonempty Workshop resource tables. L2C likewise stops at a nonempty table. These challenges confirm useful prefix behavior and its real coverage boundary; they do not establish a mature population-wide zero-vector result or historical grammar. [Selected control ledger](workshop-origin/independent-controls.csv), full local `final-03/independent-controls.json`. All control original/decoded hashes match the prior frozen corpus and archived inputs remain unchanged.

Final local preservation rechecks all 20 snapshotted protected archive/catalog/ESM/executable/database files and the two available original Save25/Save26 files. Instruction bytes at decisive static windows are independently re-read through PE mapping into local `instruction-bytes.json`; [native export identities](workshop-origin/native-exports.csv) retain the full read-only exports and failed lock-attempt log. A project-lock rejection produced no successful export and was retried after the other read-only scan completed. Optional unbacked PE reads were retained as errors. Neither is presented as scientific negative evidence. The baseline timing limitation above still applies.

The full existing Python test suite passes 83 tests, including six new synthetic prefix-boundary tests. Those tests establish parser behavior, not game semantics. Fresh source/capture/save/native evidence establishes the scoped results. Full final diff/link/encoding/status receipts are described in the [review package](workshop-origin/README.md).
