# RG2-C1E proposed P3 accepted-region pilot

> **NO LIVE RETAIL TEST IS AUTHORISED BY RG2-C1E; A SEPARATE MAINTAINER GO-AHEAD IS REQUIRED AFTER REVIEW OF THIS CARD.**

2026-10-22 Australia/Sydney. Submitted for human review, **NOT EXECUTED**.
[Authority and AC1–AC8](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_C1E_native_resource_region_ancestry.md`),
[qualified implementation/limits](verification.md), [receipt contract](contract.md),
[analysis](comparison.md). Reviewer acceptance supplies no launch permission.

## Exact proposed target

Only Steam Starfield1.16.244.0, installed
`C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe`, SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
Starfield.esm SHA256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Save52/HIST-0267 archival/master SHA256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`,
Cao Tran, Feynman V “Cu Co Ni IL”, P3. [Saved joins](../resource-geometry-observation/cases.md):
PNDT05e0de, beacon83388f, parent84ec80, Workshop bytes `c3a5866f4cfcf585`;
IL extractor83836b/base06ac8f/IRES Starfield.esm:0057d4; independent Cu
extractor83836a/base06ac95/IRES0057cf. Saved references are not live handles.
Exact source-save filename and backup path are in the locally hash-bound
preflight receipt; select the matching Save52 via the normal load menu.

Propose **one session, one Save52 load and one natural established P3 build-mode
entry**. This is a deliberately small approval request to establish new source
geometry before expanding observations; it is an action/session scope, not an
event/time quota. No automatic retry. A failure diagnosis/new build requires
offline correction, requalification and a new maintainer instruction for another
session. Slow operator response or a late health poll alone does not terminate
a healthy session. No cache reset, forced call, build/delete, travel test, save
command, SFSE/old observer, generator interception or Feynman VIII-b test.

## Before launch, after fresh explicit approval only

1. Confirm target absent. Confirm Steam Cloud disabled for Starfield through
   actual operator/UI inspection and held disabled through postflight; offline
   inventory cannot establish Cloud status. Review game Saves path, OneDrive or
   other redirection/sync, Steam userdata/remote paths and exit/autosave behavior.
   Stop on an unknown write/sync path or sole recoverable copy. Do not change
   configuration or Cloud settings through this collector.
2. Verify full SHA256 inventory of live Saves and separately held C1D protected
   backups outside game/sync paths. Phase A found271 files on each side, equal
   to the prior master. Recheck before launch; changes require a new reviewed
   baseline/verified independent backups, not silent acceptance. `preflight.py`
   copies Save52 only to a new disposable rehearsal and checks restored SHA;
   it never restores active saves. Require >=40,000,000,000 caller-available
   bytes on **both C: and D:** throughout. No prior evidence is deleted.
3. Freshly run these offline-only commands from repository root, with the exact
   installed interpreter `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`.
   The examples below use `python` for that interpreter. Choose fresh names:

   ```powershell
   python -B research/resource-region-ancestry/qualify.py --build .local-work/resource-region-ancestry/build06 --output .local-work/resource-region-ancestry/pilot-qualification01
   python -B research/resource-region-ancestry/preflight.py --build .local-work/resource-region-ancestry/build06 --qualification .local-work/resource-region-ancestry/pilot-qualification01/qualification.json --name pilot-preflight01
   ```

   Check all32 cases PASS, source/binary pins, exact EXE,39 installed definition
   identities/config, site instructions/call destinations, save parity/rehearsal
   and free space. No need to rehash all saves during gameplay. Lightweight
   READY names/sizes checks compare to this hash-bound prelaunch receipt.
4. Retain the fresh human go-ahead verbatim in a new ignored approval JSON
   `.local-work/resource-region-ancestry/pilot-approval01.json`. It must specify
   status `GO_PHASE_B`, `human_instruction`, exact card/build/preflight SHA256s,
   `cloud_disabled_confirmed: true`, `used: false`. These receipt fields record
   actual authority; editing JSON or inventing an instruction cannot grant it.
   The wrapper exclusively creates a consumed side receipt before attaching;
   consumed names cannot be reused. Phase A creates no such approval receipt.

## Launch, attachment and natural trigger

5. Record actual launch UTC; user launches through Steam URI
   `steam://rungameid/1716740` (ordinary Steam, not SFSE). No direct EXE launch.
   At main menu identify the newly started PID, full path/hash and process start
   later than launch. Existing play sessions are ineligible. Use an ordinary
   unrestricted user token if required by the evidenced C1D restricted-token
   barrier; no administrator elevation, privilege enabling or security change.
6. Run the approval-gated wrapper, substituting that actual PID and UTC:

   ```powershell
   python -B research/resource-region-ancestry/collect.py --retail-pilot --approval .local-work/resource-region-ancestry/pilot-approval01.json --preflight .local-work/resource-region-ancestry/pilot-preflight01/preflight.json --build .local-work/resource-region-ancestry/build06 --pid PID --launch-utc UTC --output .local-work/resource-region-ancestry/retail-attempt01
   ```

   Attachment/debug events pause execution. DR0–DR3 execution breakpoints,
   owned DR6 clearing/RF and declared post-evidence process disposal are native
   interventions. They may crash/disrupt the game. No software patch, injection,
   TF stepping, manual suspension, exception suppression or target-memory write.
   Remain attached through exit; never detach with armed traps. Refuse unowned
   debug state, wrong PID/path/hash/guards, instruction/context-readback failure.
   Future retail lifetime safety is untested; fixture success does not prove it.
7. After SESSION/startup readiness, load only the verified Save52. Navigate
   normally to its already established P3 if necessary and enter build mode once.
   No attempt to reproduce resource mutation. The ordinary updater must execute
   naturally. If only retained/no-refresh state is reached, record NOT_EXECUTED;
   do not force refresh or declare absence.

Four static VAs below relocate by measured runtime module base minus preferred
base140000000. Compare16 actual bytes with pinned disk image before arming and
on every hit; exact hex guards are in preflight. True helper CALL targets and
edge encodings are separately checked. All returned thread lifetimes are armed.

| Hardware site | Evidence expected at stop |
|---|---|
| DR0 `1421e07d0` | Actual updater entry/caller/R14 reference, shared state/descriptor checks; new per-thread invocation token/parent. |
| DR1 `1421e1772` | Accepted current RBX region before insertion; saved callback/updater/source frames, source key/ordinal/wrapper, R12 resource slot/R13 IRES, complete ordered points/bounds, retained Qb and closure scalar/descriptor bytes, associated-file evidence. |
| DR2 `1421e174e` | Actual rejected current region before advancement; same data/limits. Short-circuited/unvisited tails are not decisions. |
| DR3 `1421e0bf4` | Pre-install transfer vector; same updater token/frame/temp-set and exact accepted pointer membership. This does not observe completed installation or catalogue. |

Full deep-manager copying is unnecessary. Copy the selected region and its
entire ordered point list at stop; limit individual reads64KiB, total1MiB/stop,
4096 capacities, output1MiB. Snapshot failures/budget refusals preserve partial
evidence/null fields and loss reasons. Required query/descriptor read flags must
pass before useful-success stopping. Full all-use multipoint inputs and generator
context remain UNKNOWN; no broad Stage2 observer is installed by this card.

## Durability, stopping and failures

8. Each SESSION/SAMPLE/END receipt is exclusively written, flushed/fsynced,
   closed, reread, decoded and hashed. An independent parser checks it and ACK
   file bytes before numbered ACK. Event JSONL is flushed/fsynced too. Useful
   stop requires a bound accepted IL region with complete geometry/selected
   ancestry, captured retained Qb/closure/descriptor, main-file qualification,
   then its exact resource pointer in a bound transfer under the same updater
   token. Copper uses identical checks; absent/unvisited Cu is a stated coverage
   limit, not a tuned alternative. Preserve earlier rejected and partial regions.
9. Wrapper sends atomic `ACK n STOP` only after durable verified evidence,
   causing declared controlled disposal at the same stop. Independently audit
   framing, accepted ACK and EXIT/accounting before scientific success. A
   post-capture crash/termination does not erase complete evidence. A crash
   before usable evidence is failed acquisition. Unknown exceptions pass to
   Windows; error cleanup may terminate the admitted disposable process.
10. Explicit STOP file at the attempt output requests disposal; integrity failure,
    wrong identity, actual worker failure or disk protection failure also stops
    safely. Preserve raw partial/crash/LOSS diagnostics, stderr and exact commands.
    A delayed operator/poll alone is a deviation, not worker failure. If no new
    region can be obtained from this natural action, stop after its diagnosed
    result and submit the specific obstacle; no automatic second load/session.

## After every attempt and proposed recovery

11. Confirm Starfield absent, then perform full live/backup hashes and installed
    definition/config checks using the fresh preflight:

    ```powershell
    python -B research/resource-region-ancestry/postflight.py --preflight .local-work/resource-region-ancestry/pilot-preflight01/preflight.json --output .local-work/resource-region-ancestry/postflight-attempt01.json
    python -B research/resource-region-ancestry/analyze.py --receipts .local-work/resource-region-ancestry/retail-attempt01 --output .local-work/resource-region-ancestry/analysis-attempt01.json
    ```

    Postflight writes additions/removals/changes before asserting equality.
    If saves changed: preserve the changed/new versions locally, verify separate
    backup masters, propose exact named restoration, and obtain the documented
    recovery authority before overwriting/removing live files. Rehash restored
    bytes against those masters. Do not restore a corrupt/changed backup or
    expend the sole copy. A failed backup or unexpected corruption outside this
    boundary halts further activity. No automatic restore/cleanup.
12. Independently review native/source/query/region joins and compare frozen
    predictions under [comparison rules](comparison.md). Report consumer-only
    geometry, conditional replay and unknown generation/history separately from
    evidence integrity and target survival. A later all-use or Stage2 plan needs
    its own exact engineering qualification and explicit approval; no new hook
    follows from this card. Preserve all raw bytes local/untracked, B6 on hold.

## Separately gated fallback

Only if a **specific Feynman obstacle** is documented, propose Carinae III-a Rc Fe,
same Save52 SHA but distinct PNDT05e4da, beacon82be17/parent84655c, Workshop
`91bac704da9b1e34`, Iron82bea6/base05ef19/IRES0057c7. Current hardcoded P3
identity/main-resource filters must first receive an offline qualified distinct
case variant and a reviewed card with its own backup/preflight/one-session scope.
No automatic live switch, extra attempt or reuse of P3 binding. Feynman VIII-b
instability is excluded. Stage2 is contingent on Stage1 evidence, not a mandate.
