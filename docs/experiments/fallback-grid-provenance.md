# Fallback-grid provenance and identity boundary

2026-10-12, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039 continuation.
[Authorized brief](../implementation-briefs/CODEX_BRIEF_SOR_fallback_grid_provenance_and_workflow_policy.md).
Authored interpretation REVIEW-REQUIRED; raw/native/save material LOCAL-ONLY.

| Element | Answer |
|---|---|
|Question|What does the actual captured fallback grid position, and can it independently validate a saved SOR-003 Workshop?|
|Best-supported answer|It positions a fallback ship landing marker's route on Kreet. Installed Starfield.esm base 00007145 is FURN `ShipLandingMarker_80m_Large`; sampled runtime reference FF02380F is distinct from the ordinary beacon. Null known-reference input forces eligibility false; existing-overlay search fails, then fallback changes the requested angles, supplies the marker and local XYZ, and fresh descriptor/grid calculations produce[1,10464,21141]. No saved Workshop identity is established.|
|Confidence|PROVEN for captured bytes, integer tuple, reference/base/cell samples, definition identity and scoped negative controls; STATIC for code dependencies; conditional interpretation for unobserved internal branch choices. These are proposals for maintainer review, not automatic promotion of earlier findings.|
|Coverage|One natural 0.4.0 route, 778 intact records; zero-offset grid only. Static branch coverage and synthetic nonzero/carry/reflection tests are separate from retail observations.|
|Evidence|Raw sequence ledger and hashes in [source ledger](fallback-grid/sources.csv); reproducible [audit](../../research/existing-reference-grid/fallback_provenance.py), `.local-work/fallback-grid/analysis-04.json`, static addresses below and installed definition receipt.|
|Limits|Missing selection producer/caller state, inner overlay-search result/callback identities and save-load map prevent a persistent selected-reference/Workshop join. Component agreement is not full descriptor, Workshop-center or complete model equivalence.|
|Disposition|COMPLETE — EVIDENCE-BOUND NEGATIVE for the saved-instance/selected-Workshop join; independent reviewer ACCEPT. Marker provenance and zero-offset component agreement are supported. Maintainer critical review remains required.|
|Next step|Ranked code-supported acquisition routes below; none is execution authority. Existing external-debugger abandonment remains closed.|

## Authority, inputs and preservation

Starting HEAD `ee17a9397232d1bbc125a005d57f1523db3cb2fe`; the only initial
untracked file was the supplied brief. Initial inventory/index/files are retained
in `.local-work/fallback-grid/baseline.json`. No stage, commit, push, game
launch/attachment, SFSE change, Vortex deployment, new save or save edit occurred.
Existing installed Ghidra/JDK exports use readOnly/noanalysis only, with database
preservation receipts; they do not change symbols, types or comments. New tools
write only new ignored derivatives; original captures, decoder failure,
correction, predictions, observer and prior reports remain intact.

Pinned retail executable1.16.244.0 SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
static preferred image base `0x140000000`. Addresses below beginning140/142
are **static virtual addresses** in that build. Runtime pointers are session-only;
ESM locators are original file offsets; save locators are decoded-stream offsets.
None is interchangeable. The 23 frozen predictions retain SHA256
`a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487`.

## Actual chain and predicate ledger

All captured route boundaries are session `session-36756-82447437`, thread 17520.
The audit reconciles every record, not only the last grid pair. The existing
supplemental Q/E correction is reused with provenance; its original false-negative
outputs are not overwritten.

| Link | Concrete dependency / predicate | Evidence class and location |
|---|---|---|
|Producing caller 78B030|CALL 14078B877 invokes 77FC20 when request+38 is 1; loads request+20 source, +28 known reference, +30 context; boolean adjustment derives from context+9. Returned angles are stored in producer+98/+a0, then 78D4B0 derives producer+190/+198 location state.|STATIC: exact-beacon-05.tsv instructions around 14078B839..14078B8DB and decompilation lines 2246–2272. Actual CALL attributed by guarded wrapper; upstream selected object not captured.|
|Route entry|Invocation 1 sequences 1/778, parent 0. Seven slots: owner 0x21180630aa0, output 0x9afd8ff2f0, request 0x9afd8ff4d0, source 0, known 0, context 0x211a9f71500, low adjustment byte 0. Upper bits of the final slot are not a pointer argument to the boolean operation.|DIRECTLY CAPTURED: kinds 22/23, input_hierarchy; request source bytes. Parent 0 means no observed synchronous selected scope, not proof no selection operation occurred.|
|Direct path bypass|Context nonnull selects 14078008E→21159B0→140780096 rather than direct configuration path 14077FCAD. This is distinct from shortcut eligibility.|STATIC+captured context. volatile helper return is context-derived, not a saved identity.|
|Eligibility|At 1407800A6 RCX=known reference 0; 77DEF0 sets SIL0, tests RCX at 14077DF18, branches straight to return 14077E11B. Captured AL0 at sequence 3 confirms it; no Workshop/type/keyword test is reached on this invocation.|DIRECTLY CAPTURED + STATIC: static-exhaustion-68.tsv lines 6–190. Null source alone is not the explanation.|
|Existing search|1407801B3 invokes 77F900 with aliased input/output angle buffer0x9afd8feec0, context 0x211a9f71500, XYZout0x9afd8feeb0, flag 0. Returns 0 at sequence 5. Captured first slot 0x29962f15de300000 is volatile residue, not a meaningful reference: 77F900 saves but never consumes that incoming RCX before replacing it.|DIRECTLY CAPTURED + STATIC: durable-center-03.tsv lines 50–340. Corrects an overbroad reading of “null search arguments”: nulls are route source/known slots, not every search register.|
|Search subcause|77F900 obtains an overlay lookup via 798D50(manager+140,angles); zero result ID exits; otherwise 5DE3B0 must resolve required type 56 for flag 0, then BB7F80/callback must locate a qualifying reference. Exact result/type/callback rejection was not recorded.|STATIC alternatives, actual discriminator UNKNOWN. No Q event absence proves any of these branches.|
|Fallback|Null search branches1407801BE→1407801C4. Adjustment low byte 0 skips the optional 3A5990 adjustment. CALL 140780264→77E350 takes the same angle buffer and context, owner and XYZout. Invocation 4 sequences 6/773 returns 0x211eccfec40 after candidate probing.|DIRECTLY CAPTURED + STATIC. All 323 Q and 40 E scopes lie inside this fallback window; they are not evidence that the original search succeeded.|
|Chosen reference and local position|Fallback end ref+28=FF02380F; its XYZ at+8c is(50.958927154541016,50.43891143798828,4.025318145751953), byte-identical to fallback XYZ output. Later sampled base+28=00007145. Owner+18 and all grid reference samples equal fallback return.|DIRECTLY CAPTURED and independently reconciled across kinds 30–34/23. Native handle/persistent identity not captured.|
|Route frame conversion|14077FD96 floors local XY after binary32*.01; both floor operands0. 78D370 supplies manager-relative translation; owner+20 result is(50.958927154541016,2150.43896484375,4.025318145751953). This is not the fallback local Y and not Workshop compensation.|DIRECTLY CAPTURED operands/results + STATIC 14077FD96..14077FE68. Intermediate 78D370 output is inferred from code/results, not separately captured.|
|Fresh source|CALL 14077FE91→96EB90 receives landscape 0x211c935a8c0, mutable descriptor 0x9afd8feee0 and the exact fallback angle buffer. Sequences 774/775 produce 44 bytes from final fallback angles.|DIRECTLY CAPTURED; source freshness, pointer equality and bytes checked. Unhooked later source calls are not excluded.|
|Grid|CALL 14077FEC0→96F5C0 takes the same landscape/descriptor and floor[0,0]. Sequences 776/777 preserve every descriptor byte. Landscape+50 resolution 256, +54 PNDT0003F59F, +58 system 88327, +5c index 15. Block10+merge2=12 with valid setting read.|DIRECTLY CAPTURED. Output is in place; captured RAX110 is incidental, not descriptor output.|
|Downstream meaning|14077FEC5..14077FF76 decomposes the output hierarchy into square cell-center coordinates, calls 142332410 to angles, and writes output. 14077FF9E..140780045 reprojects/recenters before returning output pointer. Final route angle bytes equal fallback output; producer stores them as its destination state.|STATIC consumers + directly captured final output. This positions the landing route, not a call to compensated-center helper F4AB80.|

The request angles `33fe6f484321ccbfac01c6cd5c5fe0bf` enter fallback unchanged;
fallback output/final angles are `41018740a425ccbf85e3c02fb15de0bf`.
Matching request bytes to candidate 16/SOR-003 saved context is a supported input
correspondence from [matching-source research](matching-source-qualification.md),
not a selected-reference identity. The route deliberately returns a different
landing location. No retuning or retroactive SOR-003 assignment is warranted.

### Immediate producers, fallback selection and lifetime

Fresh read-only exports `fallback-identity-01.tsv` lines 6–20 enumerate 77E350's
single existing CALL 780264 and 77FC20's callers 78B877/1A22D58. The captured
guard fixes 78B030 as immediate producer, excluding the alternative 1A20380 call
for this invocation. Four existing 78B030 callers are 78AFB3(78AF30),
17DEE5B(17DEC70),17DF4E2(17DF210) and 17DFF60(17DFDF0). Observer 0.4.0 selected
scopes cover only the latter two. Unhooked78AF30/17DEC70 are therefore substantive
alternatives to assuming lost selection events.

`static-exhaustion-23.tsv` lines 2889 onward shows 78AF30 building a request with
zero+20/+28/+30, calling 78B030 then 78BC30.17DEC70 builds from its angle input,
clears+20/+28, supplies local context+30 and enables+38 with+39 conditional on
param6==2. Its shape is compatible with the captured null source/known and
nonnull context, but shape alone cannot select this caller. Fresh
`fallback-identity-02.tsv` lines 223 onward follows their immediate callers;
none supplies a recorded historical producer identity. Absent selected events
do not mean no gameplay selection occurred.

`matching-source-specialist-05.tsv` lines 6–1581 follows 77E350:78D4B0 converts
request to manager-relative cells; spiral rings test candidate overlay 18B0920
or TestLandingOverlay, bounds AD36D0, biome/admission/exclusion849080 and
AD92E0 queries. First admitted candidate supplies 78D660 angles. It may reuse
an overlay through 77F6E0 (type 56, overlay bit 1, geometry/distance and a successful
77F900 search) or call AD0650 if reuse fails. AD0650 builds name/source identities,
calls AD0400 and registers overlay IDs in manager+140/owner+40.77E350 then
calls 77F900 at 77F5BB to select a placed reference. The returned overlay-world
pointer from AD0650 is a different object from the final marker pointer.

AD0400 (`static-exhaustion-17.tsv` lines 1194–1481) first tries named-object 5AFA50
reuse admitted by BC3360, otherwise BB8C20 produces an object. Retain/release
operations and overlay updates are visible. AD0650 releases temporary ownership
through 3846F0 while its registration records retain identity state. This is not
proof that the captured route created a new overlay: either reuse/creation route
can converge on the same final marker. No inner reuse flag or allocation result
was captured. 77E350 returns a raw marker pointer; 77FC20 stores owner+18 with no
retain at that store. Recorded scope-local pointer stability is demonstrated;
post-return marker ownership/lifetime and safe integration remain UNKNOWN.

Search callbacks are also followed:BB7F80→780A50→B1E190→780AA0→781390.
`static-exhaustion-67.tsv` lines 6–157 shows per-reference 77DEF0 eligibility,
optional source-location checks and nearest eligible squared-XY-distance
selection. Inner eligibility can succeed on concrete references even though
the outer known-reference eligibility failed on null. Fresh 798D50 export
(`fallback-identity-02.tsv` lines 18–221) initializes output ID0 and iterates
24-byte active overlay entries; descriptor displacement, bounds and admission
govern which supplies the ID. The historical list/returned ID and callback
outcomes are absent. This demonstrates the exact alternatives to the initial
null search, rather than blaming a nominal null/garbage unused RCX argument.

## Identity domains and joins

| Domain | Captured / established value | Join status |
|---|---|---|
|Runtime reference pointer|0x211eccfec40|Fallback→owner+18→grid reference directly demonstrated for this lifetime only.|
|Runtime dynamic reference FormID|FF02380F from ref+28|A sampled FormID, not a native handle or serialized save token.|
|Native reference handle|Not captured|Cannot derive it from pointer or low FormID bits.|
|Base-object FormID|00007145, namespace 00; sampled base type 2f|Installed Starfield.esm FURN ShipLandingMarker_80m_Large; independent definition corroboration. No runtime EDID string or arbitrary winning-override guarantee.|
|Exterior cell / parent world|FF02380A / FF023809; cell pointer0x2117fecda40, world 0x20dac37e440|Observed runtime reference ancestry to exterior parent; no persisted world-key mapping demonstrated.|
|Manager current world|0x2117fe616c0|Different pointer from reference parent world. Packed+310 feffffffffffffff versus ffffffffffffffff are unqualified sentinels, not interchangeable valid saved keys.|
|Terrain/body|0003F59F /88327 /15; grid[1,10464,21141]|Kreet generic calculation established. Body agreement does not establish landing/site/Workshop ownership.|
|Saved site / beacon|SOR-003 parent 81cb2b/beacon 81ab9a; SOR-002 separate parent/context|Existing serialized-token associations retained. Matching request angles narrows source context, but no captured restoration/remapping edge binds them to FF02380F.|
|Workshop identity / compensated center|No capture|Base 7145 is not ordinary beacon 2C60E9; no Workshop pointer or helper-center result binds this grid to frozen Workshop expectations.|

Definition evidence: full installed Starfield.esm header walk finds 00007145 at
original file offset 20108691, EDID ShipLandingMarker_80m_Large,
model Ships\Discovery\ShipLandingMarker.nif, marker
Markers\InvisibleGeneric01.nif and VMAD LandingPadBlastShields. These selected
identity fields support a landing marker interpretation. Raw proprietary record
payload is retained locally, not incorporated into this report.

### Saved representations and investigated failed joins

The specialist's original read-only probe and receipts are retained under
`.local-work/fallback-grid-specialist/`; full file/source hashes are in the
source ledger. Complete header/group walks of 38 installed ESMs cover 7,717,438
records; only Starfield.esm has exact record ID7145. This does not independently
reconstruct an arbitrary runtime override/load order. Qualified saved plugin
tables identify Starfield as full namespace 00 in each Save25–28.

Archived controlled Save25/26/27/28 decode and exact R3 closure pass with
25976/25992/24875/22902 records. No R3 self ID, form-array entry or untyped
little-endian u32 whole-logical-stream occurrence equalsFF02380F/0A/09. No
landing-marker candidate occurs under the **conditional dynamic case 5 inline**
scan (tag 2 self token, at least 3 queued refs, flag 8000 clear, refs[1] base 7145).
This is not a complete scan of every saved marker representation, nor proof of
absence/remapping. Save28 precedes this travel; a subsequently generated instance
is compatible with the missing numerical values. Raw numerical equality would
also be insufficient without domain/restoration mapping.

The initially tempting alternative was 14 records per save with queued
token 407145 references. Correct token resolution identifies **six static owners
and eight dynamic owners** per save. The six static identities were pursued
into Starfield.esm: all are REFR, **none has NAME/base 7145**. For example Save28 ordinal 1879,
token 43f7e8, decoded offset 588367, queue 197 resolves 0003F7E8
Frontier_ModularREF, base 0000B730 at ESM offset 843584177. Ordinal 1881,
token 45421b, decoded 592421, queue 67 resolves 0005421B PirateShip_ModularREF,
base 00229424 at 843584277. Token 53d13c resolves 0013D13C KreetPirateShip02,
base 000B1374 at 1218137536. Thus queued 7145 in these six static owners is ship-content/definition
reference evidence, not six independently identified placed landing markers.
The other three static bases likewise differ; exact identities/group labels are
in `.local-work/fallback-grid/identity-repro-02/saved-marker-static-records.json`.

The specialist initially masked all 14 owner tokens into static IDs, producing
eight false static lookups from dynamic tokens. Its original 14-row receipt and
interpretation are retained as **INVALID_DOMAIN_JOIN**, not supporting evidence.
Primary reproduction caught this; the promoted tool resolves saved FormIDs first
and selects only qualified namespace 00 definitions. A regression control covers
inline/form-array static IDs, dynamic IDs and other-plugin namespaces. Dynamic
owners were investigated separately; neither masking low bits nor assigning
the same base makes them the captured runtime instance.

All eight dynamic owners in each save were followed through conditional prefix
selectors and queued references. In Save28, five case 5 prefixes resolve to GBFM
ship definitions: FF016B91/FF016B97/FF016BA2 to 00050A66
`LvlShip_RandomCitizen_Cargo`, FF019ADD to 0005C72F
`OE_EncShip_Varuun_Small_Litany`, and FF01C6F6 to 0005D1F8
`OE_LvlShip_Generic_Small_Mixed`. Three case 7 owners
FF01469A/FF0149B4/FF0193F0 carry initial-reference IDs
FF01C6A2/FF01C9FA/FF01C9FA rather than an inline base. Their matching R3
records are short self-only records with flags 40008000; following those records
does not yield a base or parent/world restoration map. Numerical occurrences
elsewhere in the streams remain untyped leads. Static conditional prefix
diagnostics are not proof of inline-base grammar; two static owners fail the
self-reference predicate. The installed definitions independently establish the
six static owners' bases. Reproduction 03 resolves all six owners and five
conditional base definitions (11/11) without collapsing dynamic IDs.

An additional apparent corroboration fails an identity counterexample:
Frontier's conditional saved local X/Y bytes `f1d54b4272c14942` equal the fallback
marker X/Y in **all four saves**, while parent tokens change through 8147f7,
8147bb, 8147ee, 83b098. Its Z is 9.079792022705078 in the earlier three and
8.828018188476562 in Save28, differing from the marker Z4.025318145751953.
Qualified unit 6 parent association predicates find no direct body/cache point
for any of these Frontier parents. No site tuple is established. This shared
historical local placement cannot uniquely select the captured landing site.
Corrected owner, case 7 and Frontier receipts and reader sources are retained
and hashed in the source ledger; original failed interpretations remain intact.

Save28 untyped LE-u327145 matches at decoded 2229198,2229772,2303274,2314223
are retained as numerical leads. No established field/instance boundaries tie
them to the returned marker. Nested modular-ship changed-form bodies and their
load-time marker instantiation are not fully decoded. Even a complete list of
such template occurrences would not select which historical runtime allocation,
cell/world or loaded overlay produced FF02380F without the missing instantiation/
remapping observation. The exact missing join is **saved reference/template
instance→loaded marker identity with parent world and activation epoch**.
Neither existing source save nor raw route capture records that edge. These
counterexamples bound the negative; they do not assert that the marker is
transient, absent from every save, or impossible to recover in a future capture.

## Arithmetic, coverage and counterexamples

Native descriptor hex is unchanged before/after:

```text
01000000360000006e0000000afd21000800000008000000010000001dfd2100c84868400000000009000000
```

With B12, descriptor coarse 54/110, sub8/8 and fine 0/9 decode as
X=54*192+8*12+0=10464, Y=110*192+8*12+9=21141, tag 1.
The frozen component implementation applied to these inputs/floor 0 reproduces
the independent native output. It is **not one of 23 identity-bound Workshop
comparisons**. Frozen SOR-003 Workshop cell[1,10467,21144] and SOR-002
[1,10465,21122] differ numerically; differing computations without a shared
identity do not falsify or validate their predictions. All 23 rows retain
[NOT TESTED outcomes](existing-reference-grid/frozen-predictions-live02.csv).

Static 96F5C0 (activated-grid-01.tsv, function at static 14096F5C0) first applies
signed IDIV remainder moduloN=49152 to displacement; each axis wraps once.
X crossing toggles tag xor1, Y xor3, both xor2. Full multiples of N are discarded
before crossing. It decomposes into coarse/sub/fine at 192/12 scales. Crossing
coarse/tag can update descriptor+0c through landscape tables, reflected lookup
for tags 2/3 uses R-1-coarse coordinates; a sub change can update+1c through
pattern/block resolution. Fine-only or unchanged hierarchy returns early without
those lookups. Therefore the numeric model does **not** validate opaque handles,
new table selection or all 44 descriptor bytes on a nonzero invocation.

New literal synthetic cases cover zero, interior both-sign offsets, fine→sub
and sub→coarse carry, positive/negative X/Y/both seams, whole-N and N+1 signed
remainders, reflected packed/native domain and invalid tag/index rejection.
Missing source, duplicate grid and changed thread controls fail qualification.
These expectations are hand-worked/static, not generated by the implementation
under test, and are not an independent retail nonzero oracle. Existing v2
coverage additionally checks all tag/crossing combinations and signed-zero/floor
preconditions. Native angular quantization, landing 96-step snapping and packed
reflection are separate mechanisms; no visual units or geographic calibration
is inferred from this tuple.

The retained-session census verifies raw transport for 020(36 records),
030(144 and 0),040(778 and 0): no other center/grid native records occur in those
qualified schemas. The 0.1.0 receipt lacks a schema and is explicitly excluded
from cross-version decoding; its raw events file is empty. The older
[Phase 1 center study](engine-oracle/Phase1-results.md) retains a stale-site
counterexample and no qualified generic-grid oracle. Thus current independent
native nonzero-offset coverage is NOT TESTED, not a negative algorithm result.

## Validation matrix

| Scientific dimension | Result | Meaning |
|---|---|---|
|Generic grid-component agreement|PASS|One fresh bound zero-offset reference component, exact tuple and descriptor bytes.|
|Selected-reference identity|PARTIAL / NOT ESTABLISHED|Returned runtime reference/base identified; upstream selected SOR-003 reference not captured.|
|Saved-site linkage|NOT ESTABLISHED|Exact request-angle correspondence; missing persistent reference/load-map join.|
|Nonzero-offset native branch coverage|NOT TESTED|Static recovery and synthetic controls pass; native carry/table effects unobserved.|
|Compensated Workshop-center equivalence|NOT TESTED|No fresh helper/Workshop identity-bound observation.|
|Complete durable-position equivalence|NOT TESTED|Component result cannot supply missing upstream frame/site/Workshop joins.|

## Decision-ready acquisition ranking

These are proposals requiring separate live/save authority, not instructions to
deploy another observer. Prefer preserving identity in the producing request
over trying to force a historically chosen Q function.

| Rank / route | Missing value and source-supported trigger | Positive / negative discriminator; save value | Intervention / validation scope |
|---|---|---|---|
|1. Bind producing travel request to landing marker/overlay|Capture selected-reference identity where request is created, its carried+20/+28/+30 fields, and the resolved overlay/marker ID from 798D50/77F900. Actual Save28 travel demonstrably reaches 78B877→77FC20 and fallback.|Positive establishes which selected context produced destination and whether original search lacked overlay versus marker/type. Negative still distinguishes asynchronous/unobserved producer from intentional null reference fields if request provenance is retained. A controlled post-arrival save plus matching loaded-map observation could join newly generated overlay/marker, but a save alone cannot reconstruct pointer identity.|Natural-boundary instrumentation changes timing and needs review; no external debugger. Validates selected landing/site identity and generic component, not Workshop center by itself.|
|2. Same-object Workshop helper plus grid consumer|Natural callback AD0B90/F4AB80 center and associated native grid, with actual ordinary beacon and qualified loaded parent/site frame. Existing Phase 1 build-mode transitions support fresh center possibilities but show stale-site counterexample.|Positive same invocation/object binds compensated center, frame and grid to frozen row. Negative bypass/retained center must be reported with predicate/active identity, not mismatched model. Additional movement/no-action saves can distinguish compensation persistence, provided runtime load join is also captured.|More dependent native observations; previously qualified observer scope insufficient for arbitrary center consumers. Tests Workshop-center and, with complete frame/source linkage, durable model equivalence.|
|3. Nonzero natural generic-route offset|Observe direct/supplied or search-success 77FC20 branch where local reference XY floor(*.01) is nonzero; source 96EB90 and in-place 96F5C0 retain fresh before/after.|Positive interior/sub/coarse/seam case tests numeric offset and appropriate table effects independently. Zero remains valid evidence, not failure or reason to force more actions. Controlled saves help select nonzero local XYZ but do not guarantee runtime frame/eligibility.|Natural call observation only after approved trigger/pins. Generic grid validation; a landing marker result still cannot validate a Workshop.|
|4. Controlled save/load restoration join|Record serialized marker/parent identity and its native load remapping/handle-resolution result for the same archived/loaded sample.|Positive establishes stable saved→runtime identity and lifetime; negative can expose transient/recreated marker or alternate initial-data representation. Additional saves before/after landing and reload directly help, unlike more unrelated mature saves.|New save generation/load capture needs explicit authority and protected originals. Validates persistence/site identity; arithmetic and compensated center require separate same-object observations.|

The highest-information next action is to design, for review, route 1's producing
request/overlay identity acquisition against the newly established marker chain.
No implementation/deployment is started. Routes2/3 remain valuable independent
questions; route 1 is not an arbitrary prerequisite for every generic-grid test.

## Workflow correction, checks and review

[WORKFLOW](../../WORKFLOW.md#scientific-experiment-continuation-and-health),
the experiment/completion templates and protocol now prohibit arbitrary healthy
run time/volume/delay/cadence cutoffs, preserve both-drive 40 GB and all integrity
controls, and require pre-run maintainer approval for justified essential extra
hard limits. Historical card 20 min/2 GiB criteria, retry monitor limits and their
results remain unchanged. Operational helpers must be prospectively reviewed
before reuse; this assignment does not silently change the approved DLL/helpers.

New audit/regression suite: 47 tests PASS, including 5 new test methods and 42
existing controls; 16 existing arithmetic/quantizer tests also PASS. Frozen replay
passes 23 unchanged cases with zero fresh native oracles. Analysis 01 passed;
expanded inventory 02 failed on missing older schema and is retained. Analysis 03
discloses the excluded schema and passes. Reviewer caught a transcribed cell
pointer typo and an inherited broad `scientific_complete` field; the report
corrects the pointer, and analysis 04 emits `generic_component_qualified` instead,
preserving the original inspector failure separately. The default WindowsApps
python alias could not execute; explicit pinned
CPython succeeded without installation or configuration changes.

Review package paths, exact patch/whitespace/link checks, exclusions and
independent challenges/disposition are recorded in [review](fallback-grid/review.md).
Scientific interpretation and future acquisition remain distinct from
engineering checks and authorization. No new third-party code, external
consultation/contact, permission basis, publication or integration occurred.
