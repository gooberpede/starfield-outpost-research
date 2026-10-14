# Existing-reference grid acquisition: offline engineering result

2026-10-12; SOR-EXP-0031 / SOR-EV-0039 continuation. Authority is the
[integrated brief](../../implementation-briefs/CODEX_BRIEF_SOR_existing_reference_grid_oracle_integrated.md).

The pinned native route can calculate a generic terrain grid after either an
existing-reference search or a fallback reference, and can resolve a supplied
reference directly without Q. Observer 0.4.0 distinguishes these paths, captures
fresh descriptor/grid inputs and in-place outputs, and binds them to synchronous
selected-travel ancestry where observed. Disposable engineering controls pass.
Retail reachability, saved-to-loaded reference mapping and full frozen-model
equivalence remain **NOT TESTED**. No game launch, deployment or live capture occurred.

This is a conditional acquisition candidate, not a finding that Save28 travel
will take the shortcut. The [run card](run-card.md) and exact candidate must receive
joint maintainer approval before use. [Review](review.md) controls disposition.

## Native source and minimum observation decision

Direct observations below are of pinned executable bytes and retained static
exports, not live execution. Preferred image base is 0x140000000; all following
addresses are **RVAs**, not runtime pointers or file offsets. Executable SHA-256:
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The build receipt maps each RVA to a file offset and hashes 32-byte guards and
callee entries. Startup checks loaded identity and original bytes before edits.
See [source ledger](sources.csv), [prior matching-source result](../matching-source-qualification.md)
and [Q/E reconstruction](../q-to-e-control-flow.md).

| CALL RVA → callee RVA | Native contract / observation purpose |
|---|---|
|78B877 →77FC20|Enclosing route: RCX owner, RDX output angles, R8 request, R9 source reference, stack known reference, context, adjust flag. RAX output-angle pointer (MOV RAX,RSI at 780052); owner+18 chosen reference, +20/+24/+28 residual XYZ.|
|7800A6 →77DEF0|Eligibility predicate, AL result.|
|7801B3 →77F900|Six arguments, fifth points to XYZ output; RAX search reference.|
|780264 →77E350|Five arguments; RAX fallback reference. Non-null fallback can also reach grid.|
|77FE91 →96EB90|Fresh 44-byte descriptor from current route angles.|
|77FEC0 →96F5C0|RCX landscape, RDX mutable 44-byte hierarchy, R8 signed floorXY8. Output is modified hierarchy, not RAX.|
|77FD45 /780132 →96F940|Direct/eligible displacement paths, separate attribution.|
|77FCE9 /7800D6 →AD3B20|Direct-supplied/eligible reference-angle extraction, separate tags 45/46 versus 37/38.|
|AD93FA →AD08D0; AD0AB5 →B1E190|Secondary Q/E diagnostics only.|
|17DF421 →17DFDF0|Sentinel-body selection: selected RCX, synchronous parent scope.|
|17DF48D →AD3B20|Explicit-body selected-reference angle extraction.|
|17DF4E2 →78B030|Explicit producer: native four arguments; proven selected RDI and operation RSI captured by unwind-described assembly bridge.|

Static direct path 77FCAD→77FCBA→77FCE9→77FD96 bypasses the eligibility,
search and fallback calls. RBX becomes floorX before grid, so reading it as a
reference there would be wrong. Explicit producer request clears+20/+28/+30;
selected identity therefore comes from the producer's RDI, not an assumed
nonzero request reference. Sentinel scope calls 78B030 at 17DFF60. TLS scopes
retain nested/reentrant ancestry, thread and invocation IDs.

Decision: fifteen complete-CALL wrappers are the minimum sufficient set for
this implementation's branch/selected-lineage question plus retained Q/E
diagnostics. A grid-only hook loses path and reference identity; Q/E-only misses
the shortcut; route-only loses fresh native calculation; one angle site misses
the direct branch; explicit-body angle extraction alone loses the subsequent
producer link. Entry detours, external debugger, synthetic game calls, key
insertion and center-hook expansion were rejected. These wrappers change timing
and execution and are not non-invasive. No Ghidra state was modified.

## Scientific coverage and reconciliation

Native observations are independent of the model: hooks copy native buffers
before/after the natural invocation and never call the model. Offline decoding
replays the frozen implementation afterward. Fixture arithmetic is original
synthetic control data and proves transport, not retail terrain semantics.

| Per-invocation evidence | Required interpretation / missing case |
|---|---|
|Selection 40/41 or producer 48/49, route 22/23, same TLS parent/thread|Record selected-reference binding separately. Unpaired or unwound scopes remain diagnostics.|
|Eligibility 25/26, search 27/28, fallback 29/30, direct 45/46|Classify search shortcut, fallback reference/no reference, supplied reference or direct supplied reference. No event is no observation, not a false predicate.|
|Owner reference, raw reference/base/cell/Extra-bc, current and reference-parent world|Distinguish reference, body, frame, source and residual displacement. Pointer equality alone is not persistent identity.|
|Source 31/32 then grid 33/34 in route, exact descriptor pointer/44 bytes|Fresh native source must precede the paired grid. Record landscape resolution/body/system/index and signed floorXY plus before/after hierarchy.|
|Journal sequence/hash/offset, record pairs, worker identity and retirement|Capture integrity and scientific completeness are separate; retain orphan/unpaired/unreadable records.|
|Component replay and untouched 23 predictions|Report exact values and agreement/disagreement per qualified frame; no tolerance/model retuning. Generic grid is distinct from compensated Workshop center.|

Decoder field `scientific_complete` means a paired, identity-bound **component
replay** only. It does not require `selected_reference_bound` or `saved_join` and
does not establish full model equivalence. Report these independently. Raw
unreadable scientific blobs do not kill acquisition; no guessed defaults become
valid data. A complete capture can contain no qualifying grid calls.

Candidate 16 is SOR-003's saved context; candidate 15 is SOR-002's, following the
prior eight saved joins. Exact angle bytes for 16:
`33fe6f484321ccbfac01c6cd5c5fe0bf`; for 15:
`3e7c5616334dccbf74c911eda75ce0bf`. Shared saved origin packed
`02b20e79528028e0`, source coarse 54,110 / sub8,0 / fine 0,0. Save28's current
active landing context differs, so shortcut eligibility is uncertain. Save28
SOR-003 parent 81cb2b/beacon 81ab9a and secondary 8147ef are serialized tokens,
not proven runtime FormIDs or handles. Angle correspondence narrows candidates
but does not prove a load map. Kreet PNDT0003F59F/system 88327/index 15 is a
body check, not proof of selected-site identity. SOR-002 is not in the default run.

Frozen Workshop predictions for SOR-003 include cell[1,10467,21144] and center
`0369b243f0b019457220ffc1`; SOR-002 cell[1,10465,21122], center
`a266f542eb858843efd19241`. A generic grid result cannot be declared equal to
these without recovered frame identity and compensation. The live analysis must
list all 23 immutable predictions, identify applicable rows or explicitly mark
them unassessed, and preserve mismatches and absent transitions.

## Exact engineering candidate and acceptance matrix

Candidate `.local-work/native-oracle-040/builds/qualification-08/`:

- ZIP `SorNativePositionOracle-0.4.0.zip`: SHA-256 `7cb69d4a968c60cf7b99eb8faae11ff93bd79ac2db47b8390c8dec221624fd2f`.
- DLL: SHA-256 `ca25f05189ff831c84b2eaaf7e139a873578e64aa8a17b349f9882967055e7c3`.
- build.json: SHA-256 `918625105e6b2006abcf97109f7130264b0914aa1584ed27f48e28d326567ecd`.
- schema.md: SHA-256 `e71685c1a803e2694801e3442cfad795e6fc324fd2243afad4ba9c4f9405194c`.

| Mandatory offline criterion | Result / retained evidence |
|---|---|
|Shortcut/direct/fallback positive and negative cases; reference/frame/coordinate changes|PASS: route native 158 checks and decoder 23 tests, qualification 08 route receipts.|
|Nested/concurrent/unpaired/out-of-order paths; incomplete roots/Q/E/selection|PASS: native route and decoder adversarial controls; missing scopes prevent complete capture.|
|CALL/return arguments, integer/SIMD/FP effects, SEH/C++ unwind, explicit producer bridge|PASS: generic 520, branch 240 and route 158 native checks. Native x87/MXCSR effects propagate; observer copies preserve environment.|
|Guard rejection, rollback, queue/backpressure, disk and zero-event worker STOP/failure|PASS: generic qualification and inspection 30 tests. Startup null/version/interface/wrong-host refusal PASS in disposable Python loading own DLL only.|
|Journal durability/hash/sequence and incomplete-tail recovery|PASS: inspect 30 and route 23 tests; truncated last record/raw tail recover, complete corrupt record fails.|
|Independent Q/E regression|PASS: branch inspection 6 tests and 12 native decoder cases.|
|DLL-only Vortex payload; archive/installed mismatch, optional text variation, unfamiliar modules|PASS: procedure/inventory 29 tests. Required module read failure rejects; unreadable nonessential module remains assessment.|
|Protected data and frozen model|PASS: supplemental 310 historical pins before/after; 162 save tests; 23 frozen replay PASS with zero fresh native oracles.|
|Final source/build/lock and review patch consistency|Required package checks and independent disposition in [review](review.md).|
|Starfield shortcut reachability, saved load-map, fresh native/full equivalence|NOT TESTED; outside current live authority.|

Primary logs are retained in qualification 08, supplement-04 and frozen-replay-01
under ignored `.local-work/`. Qualification 01–07 are superseded, retained and not
the deployment candidate. The first procedure run failed required-module unreadable
handling; corrected by requiring READ_OK for the three mandatory identities.
The initial reviewer identified missing direct attribution, lost selected TLS
ancestry, omitted incomplete outer scopes and an overly broad plugin gate. All
were corrected and requalified; final review remains independently controlled.
Compiler C4324 alignment and fixture C4389 signed-comparison warnings remain
recorded; no build errors.

DLL uses established dynamic /MD linkage, importing Windows bcrypt/KERNEL32,
MSVCP140, VCRUNTIME140, VCRUNTIME140_1 and six UCRT API-set contracts (actual
dumpbin list retained in dependencies.txt). Existing installed System32 runtime
prerequisites are pinned in build.json and the release lock and required by
loaded cooperative inventory with exact hash/READ_OK. UCRT API-set resolution is
provided by the installed Windows system. Disposable own-DLL LoadLibrary plus
startup refusals exercises dependency resolution; no runtime redistributable is
bundled, downloaded or installed. Only
`Data/SFSE/Plugins/SorNativePositionOracle.dll` is runtime-essential **deployed
payload**. This is separate from installed system prerequisites. ZIP notices
remain distributed review/legal material; Vortex need not deploy those texts.
Earlier /MT candidates are unapproved incorporations, retained locally and
excluded as documented in review; no new rights approval was inferred.

Queue 4096 bounds memory, not scientific event count. Overflow stops admission
and is failure evidence. Both drives require 40,000,000,000 caller-available bytes;
worker retains 1 MiB write reserve. External monitoring nominal 3 s, maximum gap 10 s;
worker health deadline 15 s, fresh initial nonce ACK 15 s, monitored interval 20 min and
2 GiB output threshold bound operational exposure without a hit quota. STOP
drains admitted work and leaves inert CALL edits/relays resident until normal
exit; it does not promise unpatching or target survival.

Reuse is maintainer-owned 030 and existing project helpers under SOR-P-0002;
existing SFSE header/MIT notice under SOR-P-0001 unchanged. No new dependency,
third-party source, network download, publication or upstream contact. Protected
binaries, raw saves, static exports and fixture outputs remain local and untracked.

Final review also corrected unreadable native setting validity and unwind-tag
collisions; explicit 16-byte child contract and adversarial controls are documented
in the schema and review. Candidate 06 failed compilation during correction and
is retained in plugin.txt; corrected 07 passed engineering; 08 resolves the permission boundary. Earlier 05
passed prior controls but predates these two review fixes. No frozen input changed.
