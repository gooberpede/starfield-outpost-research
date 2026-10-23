# Proposed C2B Phase B: bind the consumed Carinae source frame

2026-10-23, Australia/Sydney. **PROPOSED ONLY — NOT AUTHORIZED.**
[Frozen Phase A contract](contract.md), [qualification](verification.md),
[source pins](sources.csv), [discriminator](comparison.md).
Independent review cannot approve launch, attachment, save recovery or publication.

## Scientific discriminator and identity

In one Workshop-bound evaluation, do the source-key referent, manager owner and
selected frame associated with the accepted Iron, Alkanes and Rothicite geometries
agree with the frozen ordinary Carinae context? Different context localizes an
input mismatch; agreement leaves historical selection/epoch versus algorithm
unresolved. Current source metadata is not historical generation provenance.

Only the installed Steam `Starfield.exe`, retail 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Only Save52/HIST-0267,
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`,
character Cao Tran, outpost **Carinae III-a Rc Fe**. Machine identity is typed
Workshop bytes `91bac704da9b1e34`, with main-file IRES Iron `0x000057c7`,
Alkanes `0x000057c9`, Rothicite `0x00005df1`. Saved beacon token `82be17`
and historical runtime FormID `0xff02b6a8` are contextual records, never inputs
to runtime pointer resolution. Slot 24 is not an expected permanent identity.

Use `.local-work/resource-carinae-source-context/build06`, whose exact build and
controller pins are in [sources.csv](sources.csv). A changed source/tool/binary
requires fresh qualification and independent review before this card is used.
DR0–DR3 retain RVAs `0x021e07d0`, `0x021e1772`, `0x021e174e`, `0x021e0bf4`.
Preflight records exact 16-byte disk preimages and verifies calls at RVAs
`0x021e0a46→0x021e0f50`, `0x021b6931→0x021e07d0`,
`0x021e0bf4→0x012ed2a0`, plus terminal instruction words. Controller rechecks
relocated instruction preimages at arm/hit and records measured module base.
Refuse image/path/hash, startup-thread, unowned debug-register, frame, instruction
or context verification failures. No software breakpoints or code patching.

## Admission before launch

1. Obtain explicit maintainer approval for this exact finalized card and one
   disposable process, including DR/RF intervention and controlled disposal.
   The process may exit before catalogue appearance. No approval receipt is
   created during Phase A.
2. Resolve the already observed historical exitsave discrepancy. The old protected
   live file `Exitsave0_BA75E3CDM43616F205472616E_580748_20261022002200_319_15_4.sfs`
   is absent, and `Exitsave0_BA75E3CDM43616F205472616E_580746_20261023053108_319_15_4.sfs`
   is newly present relative to that historical corpus. Save52 and independent
   backups remain protected. Both corpora contain 271 files; equal counts do
   not establish equal contents. Do not launch under the stale corpus claim. The maintainer must separately approve
   named recovery, or explicitly accept the current corpus while preserving
   the historical backup. No automatic restore or deletion is permitted.
3. For the latter option only, retain the actual explicit instruction in a new
   local integrity-disposition JSON. Required fields: `status` equal to
   `ACCEPT_CURRENT_CORPUS_PRESERVE_BACKUP`, nonempty `human_instruction`, exact
   `card_sha256`, `missing` mapping each absent basename to its original
   `{bytes,sha256}` from the protected backup inventory, `added` mapping every
   new basename to its exact current `{bytes,sha256}`, and
   `restore_authorized:false`. Approval must include copying those additions
   to a new supplemental backup outside game/sync writes before launch. The helper refuses undeclared additions, changed
   existing saves/backups, inaccurate missing entries or a different card. This prospective
   procedure does not presume that acceptance has been given.
4. Confirm game absent. Operator inspects Steam Cloud and confirms it disabled
   through postflight. Verify actual Documents/Saves, reparse/OneDrive ancestors,
   Steam userdata/remote and remotecache write paths, and that pause/travel/wait/
   rest autosaves remain disabled. Unknown active sync/write paths or changed
   settings stop admission; this card does not authorize configuration changes.
   Keep both drives above 40,000,000,000 caller-available bytes throughout.
5. Run fresh offline qualification and preflight, with fresh output names:

   ```powershell
   $c2bPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
   & $c2bPython -B research/resource-carinae-source-context/qualify.py --build .local-work/resource-carinae-source-context/build06 --output .local-work/resource-carinae-source-context/pilot-qualification01
   & $c2bPython -B research/resource-carinae-source-context/preflight.py --build .local-work/resource-carinae-source-context/build06 --qualification .local-work/resource-carinae-source-context/pilot-qualification01/qualification.json --integrity-disposition .local-work/resource-carinae-source-context/integrity-disposition01.json --name pilot-preflight01
   ```

   Require 42 debugger cases and the context-memory unit controls PASS. Preflight
   verifies all pinned source/build bytes, installed definitions/configuration,
   full protected-content hashes, live/backup save content and Steam remote/cache
   hashes. It rehearses Save52 restoration to a fresh ignored scratch file and
   verifies the original hash. Diagnostics persist before corpus assertions.
   The historical backup remains unchanged. Explicitly admitted additions get
   an independent hash-verified supplemental backup; the absent original is
   retained in the historical backup. Repeat full audits before launch if any
   intervening game/save/config activity occurred. Do not perform full scans
   during play unless a specific integrity incident requires one.
6. Retain the verbatim fresh instruction in `pilot-approval01.json`, with
   `status:GO_PHASE_B`, `human_instruction`, `card_sha256`, `build_sha256`,
   `preflight_sha256`, `cloud_disabled_confirmed:true`, `used:false`.
   All hashes bind the actual new receipts. Exclusive `.consumed.json` creation
   before attachment prevents reuse; a JSON file cannot create human authority.

## One finite natural action sequence

7. Record UTC immediately before ordinary Steam URI
   `steam://rungameid/1716740` launch. Record new PID/start UTC at the main menu;
   its start must follow both fresh preflight and dispatch. Ordinary user
   execution only, no elevation or privilege changes. Do not use an existing
   play process or launch the EXE directly. At the main menu, before loading:

   ```powershell
   & $c2bPython -B research/resource-carinae-source-context/collect.py --retail-pilot --approval .local-work/resource-carinae-source-context/pilot-approval01.json --preflight .local-work/resource-carinae-source-context/pilot-preflight01/preflight.json --build .local-work/resource-carinae-source-context/build06 --pid PID --launch-utc UTC --output .local-work/resource-carinae-source-context/retail-attempt01
   ```

   Pass PID and UTC as exact arguments; avoid PowerShell locale timestamp
   coercion. Require SESSION and startup hardware-register readbacks before load.
8. Load exactly Save52 normally, travel directly to the established Carinae
   outpost and enter actual Build Mode once. Scanner alone is insufficient.
   Confirm displayed body/outpost name as context; the machine Workshop-byte
   check controls identity. Do not place, move or delete anything. If useful
   stopping occurs earlier, record later actions as NOT EXECUTED.
9. If no qualifying consumer transfer occurs after that normal evaluation,
   record whether there was no updater, retained state, wrong Workshop,
   incomplete context or only a subset of resources. One exit from Build Mode
   and one re-entry at the same outpost is the only allowed natural fallback:
   it tests another ordinary consumer evaluation without cache manipulation.
   After that evaluation, request STOP regardless of scientific success.
   No reload, retarget, second process or automatic retry. Natural generation
   is welcome incidental context but is not instrumented or required.

The finite action sequence bounds the experiment. No event-count, wall-clock,
capture-size, operator-delay or monitoring-cadence deadline terminates a healthy
run. Engineering bounds remain 4096 source/resource/point capacities, 65536 point
bytes and 1048576 copied bytes per stop, 64 queued rows and 4096 active local
invocation entries. These prevent invalid-memory/unbounded-allocation behavior;
they are not scientific sample quotas.

## Receipt, coherence and stopping

At each decision retain PID/TID/lifetime/sequence, updater token/frame/temporary
set, concrete Workshop evidence, source ordinal/slot/key/wrapper, selected
resource/collection/region, complete ordered XYZW/bound and native decision.
New `source_context` contains full source `0x70` and manager `0x200` byte copies,
owner `+0x80`, eight raw signed source words at `+0x10`, and raw manager
descriptors `+0xc8/+0x1c0`. Verify global pointer stable, manager `+0x130`
equals this callback's ProcGen, and occupied source-map key/wrapper equal the
selected slot before/after. A bad/partial/changing copy is INCOMPLETE, not empty.
The source's `+0x18/+0x1c` words are not assumed effective dimensions.

The all-stop controller pauses execution and changes owned DR/RF state. This
is intervention and can destabilize the disposable process. No injection,
memory/byte patch, stepping, manual suspension, unrelated register modification,
exception suppression, forced native call, cache invalidation, source regeneration,
save command, plugin/config change or observer deployment is permitted.
Unknown exceptions pass to Windows; stay attached through disposal/exit rather
than detach with armed traps.

Each SESSION/SAMPLE/END SRO1 file is flushed/fsynced, closed, decoded and
hash-read back externally before ACK. Events rows are flushed/fsynced in the
still-open events file before ACK. END completeness includes
the new context status. `ACK n STOP` requires all three qualified resources in
one complete Workshop-bound transfer under the same thread lifetime/updater
token. Their contexts need not agree: disagreement is itself evidence, retained
per decision. Shared pointers, copies, digests and timestamps never create a
generation epoch; those fields remain null. Short-circuiting prevents a census.

Operator STOP file, failed disk guard, identity/instruction/integrity failure or
actual worker failure requests controlled disposal. Rejected ACK/fatal failure
may also dispose this admitted process. Use lightweight stderr/health/ACK and
free-space checks during play. A delayed poll or operator action alone is not
worker failure. A pre-evidence crash fails acquisition; complete durable evidence
can remain scientifically useful after disposal/crash. Preserve losses, exceptions,
stderr, incomplete files and exit accounting. No automatic relaunch.

## Offline postflight, analysis and recovery

10. Confirm process absent, then run:

    ```powershell
    & $c2bPython -B research/resource-carinae-source-context/postflight.py --preflight .local-work/resource-carinae-source-context/pilot-preflight01/preflight.json --output .local-work/resource-carinae-source-context/postflight-attempt01.json
    ```

    Require exact pre/post live, historical-backup and supplemental-backup inventories, installed/configuration,
    protected-content and Steam remote/cache equality. Record additions/removals/
    changes before assertions. Preserve any changed file outside active/sync
    paths before a recovery decision. No helper restores or deletes saves.
11. Recovery requires separate explicit permission naming each affected path.
    Verify its independent backup against preflight; preserve changed bytes;
    copy the approved backup to that exact destination; rehash it and both full
    trees. Quarantine additions only if separately named/authorized. A backup
    mismatch stops recovery. Scratch restore was the recoverability rehearsal.
    Keep Cloud disabled until the operator resolves postflight/recovery.
12. Offline analysis first verifies SRO1/ACK sequences and transfer joins. Decode
    source anchor/padding/raw dimensions and manager mode/descriptor using the
    pinned static ledger, compare each resource's context with the four frozen
    requests, and state OBSERVED versus DERIVED versus UNKNOWN per operand.
    Compare exact original geometry separately from conditional frame projections.
    A context disagreement is a discriminator, not proof it caused every path.
    Agreement does not prove historical BIOM/DNAM/masks/settings or epoch.
    Preserve originals, seal a lossless archive with stream-hash verification,
    then obtain independent scientific/editorial review before any next scope.

No-hit mitigation is concrete: this consumer-first capture remains executable
when no producer runs after Save52 load. If the consumer also never evaluates,
the one natural re-entry above is the fallback; retain a scoped failed acquisition.
Any later producer hook or another session requires a new reviewed scope and
explicit authority. B6/publication, integration and Git gates remain closed.
