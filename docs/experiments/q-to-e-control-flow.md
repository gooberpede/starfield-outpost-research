# Candidate-query control flow and oracle reachability

2026-10-12, Australia/Sydney. Continuation of SOR-EXP-0031 / SOR-EV-0039;
no new runtime experiment. [Authorized brief](../implementation-briefs/CODEX_BRIEF_SOR_Q_to_E_control_flow_and_oracle_reachability.md).
Authored interpretation REVIEW-REQUIRED; raw evidence LOCAL-ONLY.

| Element | Answer |
|---|---|
| Question | Why did 18 natural Q calls return 1 without instrumented E, and what oracle acquisition follows? |
| Best-supported answer | Q returns a shared Boolean **continue predicate**. Early unresolved-state exits preserve it; hierarchy/flag shortcuts skip E but still test an overlay rectangle. E is optional, and Q1 is compatible with legitimate nonoverlap. The captured packed source key is recoverable. Under explicit baseline geometry assumptions, all 18 candidates differ from that source, supporting a hierarchy shortcut explanation; exact executed predicates remain unrecorded. |
| Confidence | PROVEN/STATIC for this pinned CFG/return normalization; PROVEN/RUNTIME for recorded pairs and bytes; conditional MODEL-PREDICTED for geometric shortcut assessment. Proposed interpretation awaits review. |
| Coverage | Entire Q function, its candidate iterator, resolver/overlay dependencies, both E dispatch branches and C exits; all 18 original invocation pairs and Save25/26 negative phases. One build/landing; no universal no-enumeration or outpost-count claim. |
| Evidence | [Source ledger](q-to-e/sources.csv), [18-call index](q-to-e/invocations.csv), ignored full ledger `.local-work/q-to-e/reconcile-03/ledger.json`, fresh read-only native exports and saved-angle correspondence below. |
| Limits | No actual helper return values, active-landscape/hierarchy buffers, overlay flag/rectangle or final angular-source pointee. No independent native center/grid outputs. |
| Next step | [Ranked acquisition assessment](q-to-e/acquisition.md); bounded additional observation requires separate authority. |

## Authority, provenance and preservation

Offline original Python/stdlib/project readers and existing read-only Ghidra/JDK
export workflow only. No game/process access, plugin modification, deployment,
new saves, configuration edits, network, staging, commit or push. The external
debugger path remains closed. Risks were address-domain confusion, stale state,
surrogate arithmetic and accidental input changes. Stop conditions: any failed
input pin, unavailable disk query or C:/D: caller-available bytes below 40 billion.
Decoder scratch cleans itself; immutable working save copies and receipts remain
ignored. No original was overwritten.

Starting HEAD/index and all tracked-file hashes are in
`.local-work/q-to-e/baseline.json`: tracked tree/index clean, supplied brief alone
untracked. That brief is preserved separately from task-authored changes.
`reconcile-03/receipt.json` verifies 238 input pins before/after, including all 127
prior live-evidence manifest members, original session files, native observer
sources, protected Save25/26 originals/archive copies, Save27/28, executable,
installed ESM/catalog and frozen predictions. Save27/28 hashes are respectively
`9615df728ab073bd24661fdc8abc65e0d0196b5abe532ab1b611bbe7ef7fc66c` and
`7360ce427b2a51aa94efb776d09dfaa30654c44ba08c60259b52c639cde2a35c`.
Their controlled lineage/actions remain [operator-attested](native-oracle/continuation-020-live-attempt-02.md),
not proved by filenames or hashes. Save25/26 frozen inputs remain unchanged.

All native instruction addresses below are **RVAs** for retail 1.16.244.0,
SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Static VA=RVA+`0x140000000`; attempt 02 runtime VA=RVA+`0x7ff6191f0000`.
Structure offsets are runtime member offsets, never save/file offsets.
Fresh Q/E CALL guards are existing pinned evidence; no runtime sites were read.
Fresh exports `q-to-e-specialist-01/02.tsv` extend already available analysis
without changing symbols/types/comments. Complete analysis-database hashes match
before/after in `.local-work/q-to-e/native-db-{before,after}.json`.

## Decision tree and return semantics

Primary instruction sources: `engine-oracle-02.tsv:48–213` (Q),
`engine-oracle-04.tsv:6–111` (caller), fresh specialist exports (helpers),
`exp0002-selection-sites.tsv:827–917` and fresh full E export,
`engine-oracle-01.tsv:6–195` (C). These are local proprietary exports, not copied
into this report; hashes and locators are in the source ledger.

Caller AD92E0 initializes one byte to 1 at AD933D **before** its candidate loop.
It constructs context `(owner-slot pointer, byte pointer, world pointer,
query-rectangle pointer, angular-source pointer)`. Context+0 is a pointer to a
stack owner slot, not the owner itself. At AD93FA it calls Q AD08D0 with RCX=context,
RDX=24-byte candidate descriptor. AD93FF compares full EAX with 1:1 advances the
iterator; 0 exits. The latch persists within one caller invocation. Shared stack
addresses across observed Q scopes are compatible with this loop but do not
record an outer caller invocation identity.

| Q RVA / predicate | Outcome / next dependency |
|---|---|
| AD08F2: AD5760(world,candidate+10,candidate) | Attempts candidate form resolution, with cached/generated-name alternatives. |
| AD08FA–0918: null result | Fallback 5DE3B0(candidate+10); null or type+2E !=56 returns unchanged latch. Non-null primary result proceeds; its helper already checks type 56. |
| AD092C–0937: ACCAD0(owner-slot,resolved) null | Returns unchanged latch. |
| AD093D–0956: global 5FD9C30→+120→+58 landscape null | Returns unchanged latch. Global/intermediate dereferences themselves are not null-guarded here. |
| AD0976 / AD0986 | A=96EFB0(landscape,candidate angles); B=96FB40(landscape,world+310 **value**). |
| AD098B–0A0C: any A/B field differs | Skip E to AD0ABA. Ordered offsets: byte 0,dword 4,dword 8,byte 10,dwordC,dword 14,dword 18,byte 20,dword 1C,dword 24,dword 28. This includes handle data, beyond geometric indices. |
| AD0A12: overlay+20 bit 0 clear | Skip E to AD0ABA. |
| AD0A28–0AB5: all preceding gates pass | Recompute candidate hierarchy with 96EB90; 96F940 yields XY delta; multiply 100→binary32 translation. E B1E190 receives resolved+ D8 collection, stack callback object, optionR8B=0. |
| AD0ABA–0AC1: latch already 0 | Exit without final rectangle work. |
| AD0AE5 / AD0AF4 / AD0B08: latch nonzero | Compute source from context[4] angular pointee and candidate with 96EB90, then 96F940 delta; translate overlay signed rectangle. This runs after **either** E or hierarchy/flag skip. |
| AD0B42–0B62 | Write 1 iff query rectangle and translated overlay rectangle are disjoint; write 0 on inclusive overlap. |
| AD0B74–0B8B: every normal return | Zero EAX, compare latch against 0, SETNZ AL. Exactly 0 or 1; no status 2 or sentinel semantics. |

For query rectangle `(qx0,qx1,qy0,qy1)`, overlay rectangle
`(x0,x1,y0,y1)` and 96F940 delta `(dx,dy)`, final return is 1 iff
`qx0 > x1+dx || x0+dx > qx1 || qy0 > y1+dy || y0+dy > qy1`, with
wrapping 32-bit additions and signed comparisons. Touching counts as overlap.
[Executable probe](../../save-analysis/scripts/reconcile_q_calls.py) tests this,
including wrap and four separating axes. This is a static deduction, not the
observed path assigned to any particular call.

AD5760 first consults 5DE3B0's live global form table and type 56, obtains cached
AD36D0 state, and keeps the initial form only with cache plus form+20 bit 2 or
form+388 nonnull. Otherwise AD55B0/AD01D0 generate an angle-derived name and
5AFA50 consults the name registry. A null transformed lookup can fall back to
the original key in Q. ACCAD0 obtains 4595C0 context, tries 5DDB20, then uses
461F10 or 461EB0 depending on global 16-bit 61DD7EC. The deeper helpers consume live
context maps/table entries. Static ESM existence supplies neither table membership
nor these returned pointers. Following these helpers closes the static alternatives,
without manufacturing their absent runtime state.

E's option 0 reverse collection loop filters null references, conditional ref+20
bit 3 and nonnull base+98, then dispatches callback vtable+10 at B1E33C. Option
nonzero uses a separate cell-filtered dispatch B1E2C0; Q supplies 0. Full E export
confirms both. Callback slots 4B916F0/4B916F8 target thunk AD8EC0, which dereferences
the reference slot and tail-jumps C AD0B90. Ineligible C (null ref/base, wrong type 1E,
missing/incorrect Workshop keyword or 47FCE0 predicate) returns 1. Eligible C calls
center F4AB80 at AD0C36 and grid 96F5C0 at AD0D36, writes its footprint-overlap latch,
and returns 0 **regardless of overlap** at AD0E79–0E8D. E thus stops on first eligible
C, while Q ignores E's return and consumes the shared byte. No alternate dispatch
inside this Q CFG bypasses the E boundary. Separate enumeration/helper callers
elsewhere remain possible; E0 is scoped to the instrumented CALL, never global absence.

## Recoverable packed source and meaningful variation

The stage-Q collector in `runtime/native-oracle-020/core.h:136–139` captures 40-byte
context, 24-byte candidate, 1-byte latch, 16-byte rectangle and 0x390-byte world prefix.
It then erroneously attempts a pointer read using world+310. Native AD096F/0983
passes the loaded uint64 directly to 96FB40. Thus unreadable `source` means an
unsuitable observer read, **not** missing packed-source bits. No plugin was changed.
The prior [attempt 02 report](native-oracle/continuation-020-live-attempt-02.md)'s
source-availability interpretation is superseded here; original evidence is retained.

All 36 world prefixes contain packed key`0x02b20e7843e090c0`: system 88327, body-index 15,
tag 0, encoded XY37056/17376.96FB40 first calls 2332EA0(system,body-index) and compares
its output with landscape+54. Mismatch leaves the initialized 44-byte hierarchy zero.
Match splits/reflection depend on landscape+50 and globals 5EA66F0+5EA6770; tags 2/3
reflect both full axes. Coarse/sub/fine use signed division. Table lookup fills
fields+C/+10; resolved typeB5 pattern fills+1C/+20. Those fields participate in Q's
comparison; mathematical XY equality alone is insufficient.

96EFB0 starts with angular 96ECB0, snaps subcoordinates to 0/8 with coarse/hemisphere
crossings at sub>=12, zeros fine fields, and fills landscape handle fields.
Under **assumed**, unrecorded-at-Q resolution 256, block+merge 12 and component match,
the captured source geometry is `(tag0, coarse193/90, sub0/8, fine0/0)`.
The [conditional diagnostic](../../save-analysis/scripts/q_hierarchy_diagnostic.py)
evaluates both previously recovered AVX/FMA paths with surrogate scalar cos:

| Invocations | Predicted snapped candidate geometry | Consequence under assumptions |
|---|---|---|
|1,13|tag 0, coarse 74/66, sub8/8, fine 0/0|First geometric disagreement at coarseX. |
|2–12,14–16,18|tag 1, coarse 54/110, sub8/0, fine 0/0|Tag disagrees immediately. |
|17|tag 0, coarse 186/189, sub0/0, fine 0/0|First geometric disagreement at coarseX. |

Both modes agree for all 18, but are predictions, not native branch observations.
This is useful positive support for a legitimate hierarchy shortcut and refutes
the notion that the 18 descriptors are identical. Source fine values modulo 12
are 0/0, so fine disagreement alone cannot prove the branch. If component comparison
fails, source is zero instead; if an earlier helper fails, hierarchy code never runs.
Missing actual landscape/global/handle state prevents selecting among these paths.

The header captures MXCSR`0x9fbf` for each Q boundary: round-to-nearest, FTZ set,
DAZ clear. We evaluate these bits rather than call the entire environment absent.
CPU math dispatch, native scalar cos/x87 behavior and within-helper environment
preservation remain unobserved. No frozen prediction or native float bit was retuned.

## All 18 invocation reconciliation and controls

The complete raw-grounded JSON/CSV ledger retains argument register values,
context pointer fields, both bounded snapshots, journal offsets/hashes, QPC,
return bytes, candidate identity/angles, decoded source bits, evaluable predicates,
unknown predicates, mutations and linked event status. It is local because it
contains raw memory/runtime pointers. [Reviewable index](q-to-e/invocations.csv)
contains 18 rows and decisive per-call source locations/hashes without bulk memory.

Every pair is a normally completed root Q, parent 0/thread 23796, adjacent
sequences 1/2 through 35/36. Returns are`01 00 00 00`; latch 01 before/after.
Context/candidate/world/rectangle/latch snapshots show no byte changes at their
boundaries; that does not exclude intermediate writes or uncaptured changes.
No E/C/center/grid child is recorded under actual invocation ancestry. No join is
made from nearby times or matching numerical values.

Candidate 1's static FormID 00325868 resolves in the pinned installed ESM catalog
to WRLD `LC003KreetBase`; 17 other captured keys have FF prefixes and no static
catalog entry. They remain runtime candidate identities, not claimed ordinary
beacons or saved IDs. All 18 exact 16-byte angle pairs occur **once each** within
both Save27 and Save28 global unit 6. The
[saved-correspondence probe](../../save-analysis/scripts/probe_q_saved_correspondence.py)
archives immutable copies before bounded decoding and records decoded-stream
offsets in `.local-work/q-to-e/saved-correspondence-04/receipt.json` and the index.
This independently demonstrates pre-existing saved angle correspondence; it does
not prove runtime FormID remapping, record semantics, or selected active frame.
At each angle pair, preceding/repeated saved tagged identity agrees with the
candidate's proposed numeric domain conversion. Saved neighboring kind bytes
are 0000 for 1,0100 for 2–14,0200 for 15/16,0300 for 17/18. These are saved fields,
not Q flags or a claimed count of outposts. Correct little-endian tagged-ID
search finds no matching record starts in the bounded R3 grammar in either save;
the actual positive identity/angle evidence is in global unit 6. This scoped
record search cannot establish absence of dynamic worlds or live form-table
entries. Persistence corroborates candidate correspondence but does not contain
the contemporaneous resolver/cache/overlay results or active-landscape handles.

Ten Save25/26 checkpoint receipts (five per save: 003 closed/open, 002 closed/open,
003 return) all have entered[0,0,0], flushed 0, fresh successful health/nonce checks.
N1 map QPC 504643132186 remains 0; landing QPC 505365604345 has 18/0/0 and 36 records.
Q batch QPC 504757987789 through 504757991146 lies between them, spanning0.3357 ms.
Action association follows preserved phase chronology/operator testimony; it is
not a body/Workshop/native-parent join. Save27 baseline and fauna combat interruption
precede landing; the intervening combat is not erased or treated as a control.
Existing-site search can bypass Q, but no upstream branch capture proves that
specific explanation for the Save25/26 zeroes.

All 36 journal hashes/extents, complete scopes, final entered/flushed counters,
639648 bytes, zero loss/depth/watchdog counters and drained retirement reconcile.
1973 health rows have maximum QPC gap 4.6063803 s, below 15 s. 1709 external-monitor
rows have maximum UTC gap 2.792511 s: strict one-second cadence remains **FAIL**.
Capture integrity and procedural timing are separate. No claim of native
position/grid equivalence follows from either.

## Evidence closure and exhausted alternatives

| Missing exact operand | Why existing offline material cannot substitute |
|---|---|
| AD5760/fallback 5DE3B0 actual returned pointer/type | Live form/name/cache registries and selected result were not copied. Static form 1 and saved angle matches do not establish live lookup membership. |
| ACCAD0 overlay result and overlay+20/+24..30 | Live map lookup outcome, flag and rectangle were not captured anywhere in these Q snapshots. |
| Actual landscape pointer/+50/+54, tables and block/merge globals | Q world is a different object. Prior sessions/settings cannot be assigned to this invocation; hierarchy helpers consume this live state. |
|44-byte A/B hierarchy results, including compared handles | Geometry can be predicted conditionally, but zero-on-component-mismatch, current cell/pattern handles and actual angular outputs remain unrecorded. |
| context[4] angular-source **pointee** / final 96F940 delta | Its pointer is captured; its bytes are not. It is a separate input from world+310 packed source. Needed for final rectangle path. |

Original journals/health/raw world prefixes were redecoded rather than relying on
old null placeholders; all available packed-source operands were recovered.
Full resolver/overlay CFG, both E branches, C returns and hierarchy helper branches
were traced using existing and fresh read-only exports. Static installed form
lookup, both angular dispatch hypotheses, exact saved-angle correspondence,
23 frozen outputs and prior passive capture alternatives were examined. None
records the missing live results or same-operation grid output. Reading more saved
angles cannot recover a transient lookup/table selected during this call. There
is no remaining readily available captured predicate left unevaluated.

Competing explanations still compatible with the actual 18 pairs are: unchanged
latch on an early resolver/overlay/landscape exit; or hierarchy/flag shortcut followed
by a disjoint rectangle. Conditional geometry makes the hierarchy shortcut a
source-supported explanation, without proving it executed. A minimal discriminating
observation records stage outcomes at those specific branches and final rectangle
operands, bound to Q invocation; the separate acquisition assessment specifies it.
These are data gaps, not a universal impossibility proof or permission to observe.

## Checks, review and reproduction

**COMPLETE — EVIDENCE GAP / ESCALATE.** Independent reviewer accepts offline
evidence closure with verdict ESCALATE; no remaining in-scope REWORK blocker.
Exact live branches/full native equivalence remain unresolved.

[Acceptance matrix and independent disposition](q-to-e/review.md) separate offline
completion, live unknowns and the earlier cadence failure. Original
specialist `/root/native_cfg` and independent `/root/completion_review` actually ran.
Reviewer challenged packed-source availability, captured MXCSR versus unknown
within-helper environment, unrecorded B12/res256 assumptions, and meaningful
descriptor variation; each challenge is addressed above and in the code/receipts.

Use installed CPython 3.14.3, no installations. From repository root:

```powershell
$py='C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B save-analysis/scripts/reconcile_q_calls.py --session .local-work/native-oracle-live/session-19908-48616078 --output .local-work/q-to-e/NEW-LEDGER
& $py -B save-analysis/scripts/q_hierarchy_diagnostic.py .local-work/q-to-e/NEW-LEDGER/ledger.json .local-work/q-to-e/NEW-GEOMETRY.json
& $py -B save-analysis/scripts/probe_q_saved_correspondence.py --ledger .local-work/q-to-e/NEW-LEDGER/ledger.json --output .local-work/q-to-e/NEW-SAVED
& $py -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
```

Output paths must be new. Full reproduction needs retained private inputs;
pure arithmetic tests require only repository source. Original and repeated
source-to-output checks, test logs, before/after protected pins, link/whitespace
and forward-applied exact-byte patch receipts are under `.local-work/q-to-e/`.
The actual save-analysis suite passes 162 tests, including 10 new arithmetic,
wire-endian and conditional seam controls. All 23 frozen outputs reproduce
unchanged; this rerun supplies no fresh native output or archive revalidation.
No native-engine test is claimed. Initial inspector invocation incorrectly used
unittest discovery against a script that requires a fixture-directory argument;
24 path errors were preserved, then corrected using disposable copies of existing
fixtures (30 PASS). No production observer source was changed to fix that invocation.
Reviewer also caught an endian error in the first saved-token search: numeric
hex was compared with wire-order token strings. Corrected to three-byte
little-endian encoding, added an independent regression and reran; the earlier
failed derivative remains under `saved-correspondence-02/`, superseded by 03/04.

Review patches: `.local-work/diffs/q-to-e-task-only.diff` and
`.local-work/diffs/q-to-e-complete.diff`. Complete includes the unchanged supplied
brief. Raw journals, memory, saves, proprietary exports/binaries/databases and
private bulk receipts are excluded explicitly in the package manifest.
Existing Bethesda/SFSE/tool and maintainer evidence provenance is extended in
[SOURCES](../SOURCES.md) and [CREDITS](../../CREDITS.md). No new third-party code,
permission basis or publication clearance was introduced.
