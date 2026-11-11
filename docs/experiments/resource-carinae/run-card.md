# Proposed C2A Phase B: one Carinae native Iron session

**PHASE B NOT EXECUTED — MAINTAINER APPROVAL REQUIRED.**
2026-10-23, Australia/Sydney. This is an approval-ready procedure, not authority
to execute. [Phase A brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_C2A_carinae_native_iron_region_qualification.md`),
[contract](contract.md), [qualification](verification.md), [comparison](comparison.md).
Reviewer acceptance supplies no launch, attachment, recovery or publication grant.

## Target, inputs and finite scope

Only the installed Steam game at
`C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe`, version
1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Starfield.esm SHA-256 is
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`;
all other installed definitions and configurations must equal the fresh preflight.
Only Save52/HIST-0267, SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Full filename, live path and independent backup path come from that receipt.
Character Cao Tran, named outpost **Carinae III-a Rc Fe**, P4. Workshop bytes
`91bac704da9b1e34`; Iron IRES `0x000057c7`, Alkanes `0x000057c9`,
Rothicite `0x00005df1`, all Starfield.esm-qualified. Saved identities and raw
extractor positions are in the [case contract](contract.md), not runtime IDs.

One fresh Steam process, one Save52 load, ordinary travel directly to that
established Carinae outpost, and one build-mode entry. Collect Alkanes/Rothicite
as naturally available in that evaluation. Do not visit Feynman for a live
control. No automatic second session, reload or retry. No source regeneration,
cache invalidation, forced native call, save command, construction, movement of
equipment, deletion, console intervention, definition/configuration change,
SFSE/old observer or Feynman VIII-b action.

The purpose is a positive Workshop-bound accepted Iron region and same-invocation
pre-install spatial transfer. A cached accepted region is useful evidence even
when no generation occurs. No new generation or complete resource census is
required. Source/frame/generation selection remains UNKNOWN unless actually
witnessed; this four-site card does not add producer instrumentation.

## Before Steam launch

1. Obtain a fresh explicit maintainer instruction approving this exact card and
   one session, including DR/RF debugger intervention and controlled disposal.
   Confirm the Phase A exact-snapshot review and all required tests. Choose fresh
   local receipt names; do not overwrite earlier runs or recycle approval names.
2. Confirm Starfield absent. The operator must inspect Steam Cloud and confirm
   it disabled for Starfield throughout the session/postflight. Identify actual
   Saves, redirection/OneDrive, Steam userdata/remote and autosave write paths.
   The machine inventory alone cannot establish sync status. If any active
   write/sync path is unknown or holds the sole recoverable copy, do not launch.
   Do not change Cloud or game settings through this procedure.
3. Use the existing protected independent C1D backup outside game/sync paths.
   Hash every live and backup file, require exact parity with the protected master,
   and rehearse restoration of Save52 into a new scratch file. A changed baseline
   needs a separately reviewed replacement, not an edited expected hash. Keep
   at least 40,000,000,000 caller-available bytes on both C: and D: throughout.
4. From repository root, use the exact installed Python interpreter. In these
   commands PowerShell variable `$c2aPython` is only a convenience:

   ```powershell
   $c2aPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
   & $c2aPython -B research/resource-carinae/qualify.py --build .local-work/resource-carinae/build05 --output .local-work/resource-carinae/pilot-qualification01
   & $c2aPython -B research/resource-carinae/preflight.py --build .local-work/resource-carinae/build05 --qualification .local-work/resource-carinae/pilot-qualification01/qualification.json --name pilot-preflight01
   ```

   Require all 40 cases PASS, exact source/binary hashes, installed definition
   and configuration inventory, protected-save parity and successful scratch
   restore hash. The Phase A build manifest SHA-256 is
   `42ecda7762331206c80efb650db0c02511673c7baed9e90224d6aa4fe4c0a6fd`;
   retail controller SHA-256 is
   `3efbec07288bcba47df7151feeb5a5c765433d1c135caa1953c76cf195311f50`.
   Any change requires reviewed requalification and refreshed card pins.
5. Retain the actual human instruction verbatim in a new local
   `.local-work/resource-carinae/pilot-approval01.json`. Required fields are
   `status: GO_PHASE_B`, nonempty `human_instruction`, exact `card_sha256`,
   `build_sha256` (the build.json hash), `preflight_sha256`,
   `cloud_disabled_confirmed: true` and `used: false`. Creating this JSON cannot
   grant permission. No such approval file is created during Phase A.

## Steam launch, admission and user actions

6. Record launch UTC immediately before the operator launches ordinary Steam
   URI `steam://rungameid/1716740`. Do not launch the EXE directly. At the main
   menu record PID, process start time and exact image identity; its start must
   follow launch and preflight. No existing play process qualifies. Run as an
   ordinary user if the restricted-token debugger barrier recurs; no administrator
   elevation, privilege enabling or security change is authorized by this card.
7. Substitute the actual integer PID and ISO UTC timestamp below:

   ```powershell
   & $c2aPython -B research/resource-carinae/collect.py --retail-pilot --approval .local-work/resource-carinae/pilot-approval01.json --preflight .local-work/resource-carinae/pilot-preflight01/preflight.json --build .local-work/resource-carinae/build05 --pid PID --launch-utc UTC --output .local-work/resource-carinae/retail-attempt01
   ```

   The wrapper verifies approval/card/build/preflight pins and exclusively creates
   a consumed receipt before attachment. Require SESSION and startup-arm readback
   before loading Save52. The controller compares actual instructions with the
   pinned disk image before arming and at each hit. DR0–DR3 use RVAs
   `0x021e07d0`, `0x021e1772`, `0x021e174e`, `0x021e0bf4`; call-target guards,
   exact 16-byte site words and runtime relocation base are recorded by preflight
   and SESSION. Refuse wrong path/hash/PID, unowned debug state, instruction
   mismatch or context verification failure.
8. Load the hash-identified Save52 through the normal menu, then use ordinary
   map/travel actions directly to Carinae III-a Rc Fe. Independently confirm the
   displayed body/outpost name and existing Iron equipment. This contextual check
   supplements the machine's exact typed BC Workshop-byte join. Saved beacon
   `82be17` and extractor `82bea6` must never be entered as runtime handles.
   If machine Workshop identity disagrees, stop as an identity failure. Enter
   established build mode once and allow that normal evaluation to complete.
   No placement is necessary. Retain naturally occurring control decisions.
   If useful evidence triggers an earlier automatic stop during travel, record
   remaining planned actions as NOT EXECUTED; do not relaunch to complete them.

Attachment and debug events pause execution; hardware execution breakpoints,
owned DR6 clearing, RF changes and controlled process termination affect the
target. They can cause instability. No software byte patch, injection, stepping,
manual suspension, unrelated register mutation, exception suppression or memory
write is permitted. Stay attached through disposal/exit; do not detach with armed
traps. Unknown exceptions pass to Windows. Fixture success is not a guarantee
of retail process survival.

## Durability, loss, no-hit and stopping

Every stop must be copied to external owned bytes, exclusively written as SRO1
SESSION/SAMPLE/END frames, fsynced, closed, independently decoded and hash-read
back before ACK. Events JSONL is flushed/fsynced. Failed or truncated reads and
LOSS records remain evidence; they cannot qualify useful-success stopping.
The finite action sequence is the scientific event budget. There is no arbitrary
event count, capture-size, elapsed-time or operator-delay cutoff. Preserve the
engineering memory/read/frame/queue budgets in the [contract](contract.md).

The wrapper sends `ACK n STOP` only after a complete, bound, main-file-qualified
accepted Iron geometry sample and its exact resource pointer in a complete bound
transfer under the same thread lifetime/updater token. Retained query/closure/
descriptor reads must be complete. The transfer is pre-install; completed cache
installation, final catalogue output and producer history remain unobserved.
Alkanes/Rothicite are useful controls where seen, not mandatory extra live sites
or a reason to tune the useful-stop rule.

Explicit operator STOP, failed disk protection, identity/guard/integrity failure
or actual worker failure ends the attempt safely with diagnostics. The operator
can create `.local-work/resource-carinae/retail-attempt01/STOP`; the wrapper
requests controlled disposal. Rejected ACK or fatal controller failure may also
terminate this admitted disposable process. Poll health without full save rescans
during gameplay. A late poll or slow user action alone is not worker failure.

If the one natural travel/build-mode action yields no qualifying Iron event,
the operator records completion of that action and requests STOP. Distinguish
no updater hit, retained/no-refresh state, unbound Workshop, rejected Iron and
incomplete/lost evidence. No missing event establishes native Iron absence.
Preserve the actual diagnostics. The bounded mitigation is offline classification
of that precise failure and, if justified, a separately reviewed card/authorization
for another natural trigger or additional narrowly guarded site. Do not add a
reload, force refresh or retarget during this session.

A crash before usable durable evidence is failed acquisition. A crash after
externally verified evidence is reported separately from scientific usefulness.
Do not relaunch automatically. Preserve stderr, exception, ACK, exit and accounting
records, including incomplete files and additions caused by the attempt.

## Postflight, recovery and Phase C

9. Confirm the process absent; hash all live/backup saves and installed definitions/
   configurations, recording additions, changes and deletions before assertions:

   ```powershell
   & $c2aPython -B research/resource-carinae/postflight.py --preflight .local-work/resource-carinae/pilot-preflight01/preflight.json --output .local-work/resource-carinae/postflight-attempt01.json
   ```

   Preserve changed files outside game/sync paths before considering recovery.
   No helper automatically restores or deletes saves. For a changed live save,
   stop for the maintainer's explicit recovery decision naming the affected paths:
   verify the independent backup against its preflight hash, copy each approved
   backup file to its exact live counterpart, then rehash it and the full trees.
   Quarantine additions only if separately named/authorized; never discard them
   or overwrite the only recoverable copy. A backup mismatch stops recovery.
   The scratch restoration rehearsal is the prior recoverability test. Keep Cloud
   disabled until postflight/recovery is resolved by the operator.
10. Phase C also requires explicit authorization. Retain it in a local
    `phase-c-approval01.json` with `status: GO_PHASE_C`, actual `human_instruction`,
    this exact `card_sha256` and closed `events_sha256`. Then, and only then:

    ```powershell
    & $c2aPython -B research/resource-carinae/compare.py --receipts .local-work/resource-carinae/retail-attempt01 --phase-c-approval .local-work/resource-carinae/phase-c-approval01.json --output .local-work/resource-carinae/comparison-attempt01.json
    ```

    Audit framing/ACK/EXIT/loss completeness first; compare exact ordered point
    and bound bits against pinned installed geometry, retaining source/frame
    identity, equality, conditional query classification and coverage separately.
    Apply the [decision table](comparison.md). An apparent match cannot supply
    missing source identity. Return primary pins, scoped conclusions, unknowns
    and an independent review package. No fitting, prediction mutation, automatic
    retry, integration, publication or Git mutation follows from Phase C.
