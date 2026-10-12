# Live attempt02: fallback grid reached

2026-10-12; SOR-EXP-0031 / SOR-EV-0039 continuation. The approved Save28 to SOR-003 run reached one fresh generic terrain-grid calculation through a **fallback reference**, with native and frozen component replay agreeing at `[1,10464,21141]`. The existing-reference search returned null. This is a zero-floor `[0,0]` case, not a live test of nonzero offsets, carry or scale. The chosen base was `00007145`, not ordinary beacon base `002C60E9`; selected-reference ancestry was not observed. The capture does not establish an identity-bound SOR-003 workshop result, a saved load map or full native equivalence.

The 778 persisted records are intact. Worker drain and retirement completed with zero loss, health timeouts or depth errors. The original inspector reported `capture_complete=false` because it treats a legitimate Q auxiliary event as an extra boundary record. Separate supplementary analysis establishes complete Q/E lifetimes without rewriting that result. Cleanup passed; all280 frozen pins and all retained save files match. Normal exit rotated one ExitSave, disclosed below.

## Authorization and provenance

The user approved the exact0.4.0 observer and [run card](run-card.md), then approved the [external timing correction](retry-timing-addendum.md) and retry. The user enabled the same approved DLL through Vortex profile `Starfield - SFSE`, launched using the Vortex SFSE button, and reported responsive main menu. Preflight verified280 pins, archive/deployed DLL, game/SFSE/installed prerequisites, process absence,261 save files and both-drive40,000,000,000-byte guards. No configuration, manual deployment, debugger, synthetic native call or manual save was used by Codex.

DLL SHA256 `ca25f05189ff831c84b2eaaf7e139a873578e64aa8a17b349f9882967055e7c3`; ZIP `7cb69d4a968c60cf7b99eb8faae11ff93bd79ac2db47b8390c8dec221624fd2f`; lock `060db14e0000146ed13537c6b59b688eff238132819b0e42f24a94588f69ab6b`. Game SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. The unchanged15 CALL wrappers affect execution/timing and remained resident/inert after STOP until normal exit.

Fresh session `session-36756-82447437`, PID36756. Pre-edit61 and pre-load160 cooperative module entries were READ_OK; normal Windows/Defender, Steam overlay and NVIDIA components were assessed. Post-travel module set and hashes were unchanged. The helper's separate inventory/ACK scans remain non-atomic. Monitor ACK `79dfc077055f4abda10d4e3ea116f003` completed in3.075848 seconds; monitoring remained running through the action, ending without failure or timing warnings. There was no timing-only stop or confirmation warning in this retry.

Before loading, the user transcribed `Kreet - Landing Area; Level 4; 10/12/26; 12:18:28 PM; 2h 58m` and explicitly confirmed Attila Kiraly and the actual Vortex launch method. After loading, they reported Save28/Kreet and the SOR-003 marker, then explicitly reconfirmed Attila Kiraly, level4. After clearance for one trip, they reported `Arrived at SOR-003 Kreet; game is responsive; no build mode active`. This is operator evidence of the action/arrival; no independent selection-time screenshot, exact click timestamp or observed selected-producer scope supplies a stronger native binding. No extra travel was requested. User later reported normal exit, completed Steam sync and plugin disablement.

## Native route and exact evidence

All sequences/invocations below belong to this session, thread17520. Addresses in the design remain pinned-build RVAs; values labelled pointers below are runtime pointers only. [Source/receipt ledger](live02-sources.csv) pins local primary evidence; raw bytes remain untracked.

| Boundary | Invocation / sequences | Direct observation |
|---|---|---|
|Enclosing77FC20|1 /1,778|Normal paired return; parent0; source and known-reference arguments null; no observed selected scope.|
|Eligibility77DEF0|2 /2,3|AL=0.|
|Existing-reference search77F900|3 /4,5|RAX=null.|
|Fallback77E350|4 /6,773|Returned runtime reference `0x211eccfec40`, also chosen owner+18 and grid ref address.|
|Fresh descriptor96EB90|368 /774,775|Normal source production before grid; same descriptor pointer and exact44 produced bytes.|
|Generic grid96F5C0|369 /776,777|Normal pair; valid CALL attribution; before/after descriptor unchanged; native floorXY `[0,0]`.|

Fresh descriptor input and output hex:

```text
01000000360000006e0000000afd21000800000008000000010000001dfd2100c84868400000000009000000
```

Native block setting10 with original read-valid1 and merge2 gives12; landscape resolution256, body `0003F59F`, system88327, body index15. Frozen component replay derives `[1,10464,21141]`, exactly the hierarchy decoded from the native in-place output. RAX at the grid is separately captured and is not its output descriptor. Both chosen-reference samples and the fallback return bind this component to the same live reference. Ordinary-base test is false (`00007145`).

Request angle bytes `33fe6f484321ccbfac01c6cd5c5fe0bf` match the previously documented candidate16/SOR-003 saved-context angle correspondence. Final route/source angles changed to `41018740a425ccbf85e3c02fb15de0bf`. Exact-angle correspondence supplies a scoped input link, not selected-reference ancestry or a save-to-runtime identity map. Translation XYZ bits `f1d54b420667064568cf8040` are route residuals, not Workshop compensation.

Sampled manager world pointer `0x2117fe616c0` differs from chosen reference's exterior-parent world `0x20dac37e440`. Their sampled packed+310 bytes are respectively `feffffffffffffff` and `ffffffffffffffff`; these are unqualified sentinel-like values here, not validated saved source keys. Pointer identity, runtime FormIDs, serialized saved tokens and byte offsets remain distinct domains. Selected-reference events40-49 were absent; no native selection binding is inferred from timing or matching angles.

## Diagnostic correction and completeness

Q entered323 times and returned normally323 times (304 low32 returns1,19 returns0). E entered40 times and returned normally40 times. Each of40 Q invocations has `[7,20,8]`: begin, documented `q_e_entry` auxiliary, normal end; each auxiliary encloses exactly one same-thread normal E `[10,11]` lifetime. No Q/E unwind kind9/12 was recorded.

The frozen inspector's `pair()` requires exactly two records for a Q group and therefore labels those40 valid three-record groups incomplete. Consequently both original inspection files and the original postflight command's nonzero exit remain preserved. That nonzero exit reports the frozen capture-completeness verdict, not cleanup/hash failure. Independent reviewer reproduced this diagnosis from raw records.

[Supplemental reader](../../../research/existing-reference-grid/live02_analysis.py) retains the frozen output and separately validates allowed Q stages, boundary identities/order, auxiliary identity, nested E sequence/QPC windows, E pairing/parent/thread and original worker/retirement/integrity checks. Its derivative reports `supplemented_capture_complete=true`; component replay is qualified separately. Missing/unwound E, duplicate auxiliaries, changed identity/thread and invalid nesting fail controls. Raw/session files, approved code/lock and the original false-negative output are unchanged. Six new offline controls plus36 existing tests passed (42 total). This correction does not make absent selected ancestry complete.

## Frozen predictions and scientific disposition

All23 immutable predictions are enumerated in the [per-row ledger](frozen-predictions-live02.csv), each with sample, saved parent/workshop identity, body, expected cell/center and explicit applicability/frame/compensation/outcome. Every Workshop comparison remains NOT TESTED: no selected/saved load join and no compensated Workshop-center oracle. Frozen predictions SHA256 stays `a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487`.

The generic result differs numerically from the frozen SOR-003 Workshop cell `[1,10467,21144]` and SOR-002 cell `[1,10465,21122]`. Those are different, unjoined computations; this is neither a validated Workshop mismatch nor evidence to retune the model. Strongest supported conclusion: retail fallback-to-generic-grid reachability and one fresh identity-bound **zero-offset component agreement**. SEARCH_SHORTCUT/direct reachability was not observed. Selected SOR-003 binding, persisted authority, saved correspondence, nonzero-offset live behavior and full model equivalence remain unestablished.

## Cleanup and criterion matrix

Postflight recorded target/loader/debugger absence and observer DLL removal,280 exact pins PASS and261 saves before/after. Protected Save25-28/archive inputs remain identical; Save28 SHA256 remains `7360ce427b2a51aa94efb776d09dfaa30654c44ba08c60259b52c639cde2a35c`. Retained save entries have no changed bytes. One ordinary ExitSave rotation occurred for characterD6036588: old sequence000258/timestamp20261012075349 was replaced by new000302/20261012101840. No protected original was overwritten, deleted or repaired by Codex. New ExitSave stays local and untracked.

| Criterion | Result |
|---|---|
|Approved identity, disk, fresh-session admission,15 guarded CALLs/relays|PASS|
|Operator pre-load/post-load identity and ordinary single arrival|PASS on recorded user testimony; native selected ancestry absent|
|Pre/post cooperative module inventories and fresh ACK/continuous monitoring|PASS, race limits retained|
|Durable778 record integrity; zero loss/errors; drain/retirement|PASS|
|Frozen diagnostic-completeness verdict|FAIL: preserved decoder false-negative|
|Supplemented Q/E lifetimes and capture completeness|PASS with separately recorded correction and42 offline controls|
|Fresh fallback reference/grid component|PASS, zero-offset scope only|
|Existing-reference search shortcut/direct path|NOT OBSERVED; search returned null|
|Selected ordinary SOR-003/saved mapping/full frozen-model equivalence|NOT ESTABLISHED / NOT TESTED|
|Normal exit/Steam sync/disablement|User testimony; process/DLL absence corroborated|
|Protected hashes and cleanup|PASS; incidental ExitSave rotation disclosed|

This closes the authorized single run, subject to [critical review](live-attempt-02-review.md). No retry, hook change, new scenario, publication, staging, commit or push follows. A possible next bounded question is an offline trace of the actual route's producer and null search inputs, to explain missing selected ancestry; it is a recommendation, not work started here.
