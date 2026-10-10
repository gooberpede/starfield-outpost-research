# Phase1 Save25/Save26 operator run card — observer0.1.1

**Approved for this live session, 2026-10-10:** User explicitly approves the
preflight/card and authorizes Phase1 with the deployed0.1.1 instrument. The
review/authorization gate below is satisfied for this bounded sequence. User
retains launch/gameplay/load/exit control. [Live ledger](Phase1-live-session.md).

2026-10-10 Australia/Sydney. SOR-EXP-0022 / SOR-EV-0030 / SOR-D-0041.
**PROPOSED / REVIEW-REQUIRED. Do not begin the scientific session until reviewed
and separately authorized.** Deployment and the smoke test are complete; this
card grants no new live authority. [Actual installed preflight](../../audits/observer-011-post-deployment-preflight.md)
passes. [Frozen comparisons](validation-protocol.md) and
[native oracle contract](oracle-contract.md) remain the scientific basis.

## Question and exact instrument

Does the engine's **stored native workshop center/radius** become fresh for the
currently selected workshop when build mode opens, remain stable without action,
change appropriately when switching002/003, and preserve durable center across
Save25→Save26's already-saved beacon relocation? Phase1 captures this independent
stored output, not a plugin calculation of XYZ+compensation. It does not capture
the complementary breakpoint/grid oracle or validate all planetary placement.

Use the already deployed approved package only:

```text
D:\Projects\starfield-outpost-research\.local-work\beacon-observer-builds\engine-oracle-011-02\SorBeaconObserver-0.1.1.zip
SHA256 9570c9da1b206c6b611e31273e71b5cf84b10e10b6b7fc2e479e7aa1fd445023
DLL 0.1.1 / SFSE export 0x00010001
DLL SHA256 4ae2a1e329a498b12352f4145db546fdb1317048dced5dede8c16f3fabe30504
Config SHA256 edf6c20d8bff667783467d8ac6094b331355c07adf4c5ee323e923e407033177
```

Config points to
`D:\Projects\starfield-outpost-research\.local-work\beacon-observer-live`.
Vortex profile `Starfield - SFSE` is user-reported; user verifies that profile
and the intended0.1.1 mod before launch. Vortex exclusively manages deployment.
Do not rebuild/replace the DLL/config or enable a second observer version.

## Inputs, actions and safety

User retains launch/load/gameplay/travel/build-mode/exit control. Agent control
commands, once the live session is authorized, only request settled snapshots
and cooperative observer STOP. No debugger, hooks, native calls, native-save
automation, console mutations, placement/move/delete, configuration edits or
forced game termination. No new outpost, POI trip or Save52 deployment is required.

Select the exact Save25/26 entries below; protect originals and frozen archives.
No manual save or overwrite is needed: Save26 already contains the relocation.
If a separately identified controlled copy is needed, create/archive/hash it
before loading under the reviewed session scope; do not silently select another
save or copy over an active playthrough. Incidental new autosave/exit-save files
are separate provenance and not substitutes for the inputs; no settings change.

| Input | Exact filename | SHA-256 |
|---|---|---|
| Save25, before relocation | `Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs` | `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5` |
| Save26, after relocation/save | `Save26_D6036588M417474696C61204B6972616C79_000241_20261010012454_4_0_4.sfs` | `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104` |

Actual installed save directory:
`C:\Users\User\Documents\My Games\Starfield\Saves`.
Immutable archives remain under `.local-work/savegames/two-outpost-anchor/exact-beacon-01/`
and `.local-work/savegames/beacon-observer/initial-01/` respectively.
Recheck hashes before and after Phase1 and preserve session output locally.

Maintain **40,000,000,000 available-to-caller bytes on both C: and D:**.
Recheck immediately before launch; automatic guards continue during collection.
Terminal: code/version/hash/target identity mismatch, genuine writer/integrity or
runaway-output failure, failed disk query or below-threshold capacity. Preserve
flushed evidence and stop acquisition; do not force-kill or hot-unload the plugin.
Unreadable/changed/stale optional fields, CAPTURE_PARTIAL and unexpected scientific
values are recorded and do not automatically terminate independent collectors.
Repeated inability to acquire the **primary** native result means Phase1 is
inconclusive; return for review rather than expanding scope to force a result.

## Fresh-session readiness, then serial acquisition

1. After review/authorization, user launches through the SFSE Vortex profile.
   At main menu identify the newly created `session-<PID>-<tick>` in the configured
   root. Verify `ready.json`, startup `STARTUP_RECORDED`, current live PID/process
   creation, version0.1.1 and the exact game/SFSE/DLL hashes from the preflight.
   Startup module inventory and loaded code guards must be healthy. Do not reuse
   smoke `session-6936-125088390`, old0.1.0 session17596 or their pointers/PIDs.
   If READY is absent or mismatched, pause for readiness diagnosis before science.
2. User loads exact Save25; reported starting site is **SOR-003**. Wait for normal
   loading/terrain settling and record how long. Confirm actual site/build-mode
   state rather than assume the menu selection proves it. Avoid intentional
   movement while each finite snapshot runs. SETTLED is operator attestation,
   not an engine synchronization or atomicity guarantee.
3. Perform the rows below serially. For each request record save/site, UTC/local
   time, build open/closed, loaded/unloaded state, travel/loading route, time state
   and deliberate actions. Open build mode through normal UI without modifying
   anything. For `control`, remain in the same build state with no deliberate
   action. On closing, settle again before `closed-after`.
4. Wait for that label's `complete.json` and final metrics, or a documented partial/
   failure state, before the next deliberate action/request. Validate raw referenced
   hashes using the inspector; integrity success alone is not semantic success.
   Do not race travel/load against acquisition. A missing marker is not a pass;
   retain the journal/partial files and diagnose instrument health.

| Load/site condition | Closed | Open build mode | No-action open control | Closed again |
|---|---|---|---|---|
| Save25 SOR-003 | `p1-25-003-closed` | `p1-25-003-open` | `p1-25-003-control` | `p1-25-003-closed-after` |
| Save25 SOR-002 | `p1-25-002-closed` | `p1-25-002-open` | `p1-25-002-control` | `p1-25-002-closed-after` |
| Save26 SOR-003 | `p1-26-003-closed` | `p1-26-003-open` | `p1-26-003-control` | `p1-26-003-closed-after` |
| Save26 SOR-002 | `p1-26-002-closed` | `p1-26-002-open` | `p1-26-002-control` | `p1-26-002-closed-after` |

After the first row, user travels to002 using an agreed route (on foot or fast
travel); record any loading/frame change. Travel is a separate condition, not
a no-action control. Then user loads exact Save26, confirms003 location, settles
and repeats; loading reacquires all roots/associations even if addresses coincide.
Finally visit002 for the cross-save distinction control. These16 checkpoints are
chosen state/identity/load controls on **two existing** outposts, not an arbitrary
outpost-count target or a requirement to manufacture additional samples.

Use the unchanged helper with the **fresh verified session path**. Examples
are prospective, not executed by this preflight:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B 'D:/Projects/starfield-outpost-research/runtime/beacon-observer/request.py' '<fresh-session>' p1-25-003-closed --settled
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B 'D:/Projects/starfield-outpost-research/runtime/beacon-observer/request.py' '<fresh-session>' p1-25-003-open --settled
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B 'D:/Projects/starfield-outpost-research/runtime/beacon-observer/request.py' '<fresh-session>' p1-25-003-control --settled
```

Use each subsequent label from the table once, after its operator condition.
Do not submit all requests as a batch. If a repeat is scientifically useful,
record its reason and use a new label; no arbitrary tiny error/hit/volume quota.
If a restart is required, verify a new session and retain the prior partial run.

Offline inspection after each durable checkpoint, to a NEW ignored receipt path:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B 'D:/Projects/starfield-outpost-research/runtime/beacon-observer/inspect_capture.py' '<fresh-session>/p1-25-003-open' --output '<new-local-inspection-file.json>'
```

## Observables and precommitted interpretation

Retain raw before/after native output prefix, its pointer provenance, center12
bytes, radius4 bytes, flags e8/e9/ea; fresh terrain/body/origin/grid state; current
context diagnostic pointer; both ordinary beacon transforms/Workshop compensation/
identifier98 where present; worker thread, timestamps and loaded-module identity.
Missing/unloaded references are NOT_OBSERVED, not proof of no outpost. Saved
tokens are not runtime FormIDs/handles. Associate using body/base/transform/
Workshop identifier and operator condition; preserve ambiguity and pointer churn.

| Site, both saves | Workshop identifier98 LE hex | Expected same-frame native center LE binary32 hex | Saved-frame cell |
|---|---|---|---|
| SOR-002 / Kreet0003F59F | `f1517de43e171745` | `a266f542eb858843efd19241` | [1,10465,21122] |
| SOR-003 / Kreet0003F59F | `0efca066ee4c7b9b` | `0369b243f0b019457220ffc1` | [1,10467,21144] |

Before counting an exact center pass, demonstrate native output freshness,
active-workshop association and common coordinate frame from open/control and
site-switch evidence. Identical brackets can both be stale. Closed-mode samples
are freshness negatives, not prescribed expected zeros; native reset may zero
radius while retaining old center. Flags alone do not establish authority.
Do not use matching center as the only evidence for its own association.
If the captured evidence cannot independently establish association/frame, report
CONDITIONAL_MATCH/UNASSESSED rather than claiming full oracle validation.

Same-frame comparison requires **exact12-byte equality**, no posthoc epsilon or
per-case offsets. Ordinary active radius150 is a conditional existing expectation,
not a fitted result. SOR-003 raw beacon position should differ Save25/26 while
its durable center remains invariant;002 is unchanged and distinct. Preserve
unexpected values as counterexamples after identity/frame checks.

The saved-frame cells/residuals are frozen model predictions, **not newly acquired
native grid outputs in Phase1**. A current rebase may change local coordinates;
frame equivalence needs a demonstrated transform. This passive run does not
capture the callback's post-quantization hierarchy. No matching local center
alone proves planetary-grid/full-algorithm equivalence or continuous geography.
Return stale/partial/inconclusive outcomes as useful evidence; any further native
trace/query/instrument change requires its own review and authorization.

## Finish and review return

After the last requested checkpoint is durable and its metrics/partial outcome
recorded, send cooperative STOP to the verified current session:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B 'D:/Projects/starfield-outpost-research/runtime/beacon-observer/request.py' '<fresh-session>' STOP
```

Confirm `retired.json` when space/instrument health permits; STOP can interrupt
an in-progress capture, so preserve its partial journal. DLL stays resident.
User exits normally and disables through Vortex; verify process absence, original/
archive save hashes, instrument hashes and all referenced raw hashes. Record
incidental new saves separately, without deleting or overwriting inputs.
Report evidence completeness, scientific comparison and target survival separately.
Return the full checkpoint/condition ledger, raw integrity receipts, exact/conditional/
stale/mismatch results, unknowns and deviations for critical review. No staging,
commit, push, publication, POI experiment or automatic next phase follows.
