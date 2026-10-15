# Single proposed operator card — 0.8.0 local availability

**WITHDRAWN FROM LIVE CONSIDERATION — NO-GO.** The plugin and this card are not approved. The [reassessment](scientific-value-reassessment.md) supersedes the earlier ACCEPT. The conditional procedure below is preserved historical material, not a current request for deployment or launch; any future work requires a separate brief and authorization.

**Historical approval premise (superseded):** this card and its
[release identity](release.md) were submitted for integrated review before any
deployment or launch. Approval never occurred. The proposed procedure below is
retained to define exactly what the reassessment rejected.
[Scope/hypotheses](contract.md), [schema/limits](schema.md), [processing](processing.md).

Initial scope: one Kreet unplaced-beacon preview from protected Save3. Seek the
already evidenced A/B/C displayed sets naturally; no exact numeric return to A,
minimum event count, elapsed quota, capture-volume quota or ACK cutoff. Normal
beacon motion is the controlled action; neither outpost construction nor an
extractor is needed. Established-Workshop and player-displacement scenarios are
omitted from this initial card: they add context transitions without a guaranteed
natural refresh, and are optional under the brief. Init/operation calls remain
separately classified if they occur naturally during the selected scenario.

Before loading, give this verified instruction once:

**Load Attila Kiraly Save3 — Kreet - Kreet — Level 3 — 10/6/26, 12:34:27 PM.**

The save-menu utility freshly regenerated this from controlled-mapping/run-04
using original metadata/hash and fixed UTC+11, matching the prior screenshot
control. Private receipt `.local-work/local-readiness/save-menu.json` retains
exact path/hash/metadata; research ID Save3 need not appear in the game's menu.
Do not choose by ordinal or copy timestamp. If missing/ambiguous/different,
resolve the actual menu offset and selected original once before continuing.

## Approval and offline preflight

The approval must cover the exact DLL/package/source/adapter identities in
release.md, thirteen guarded CALL replacements, bounded RPM reads, lock-free
4096-record queue, 256-member/row snapshot capacity, sticky failure behavior,
resident inert retirement and normal-exit policy. Instrumentation affects timing;
this is passive observation of natural calls, not zero-interference execution.
No arbitrary native invocation, cache mutation, prefetch or generation request.

After that approval, import the exact ZIP into **Vortex**, enable/deploy it there,
and verify the effective DLL. Do not copy DLLs manually. Only the DLL belongs in
Data/SFSE/Plugins; package notices are not runtime payload. Confirm no competing
SOR observer, original saves intact, executable/SFSE/dependencies and every
protected pin match. Known normal Steam/NVIDIA overlays are accepted. Vortex's
deployment may expose an additional effective DLL path: add that concrete removal
path to a new pinned plan before launch, never silently alter an approved receipt.

Use installed Python and the private reviewed plan named in release.md. PLAN_HASH
is the plan's actual SHA256, obtained with Get-FileHash. Every output is a fresh
exclusive path under a new `.local-work/local-readiness/approved-run-N/` directory.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$plan = 'D:/Projects/starfield-outpost-research/.local-work/local-readiness/plan.json'
$planPin = (Get-FileHash -Algorithm SHA256 -LiteralPath $plan).Hash.ToLowerInvariant()
$run = 'D:/Projects/starfield-outpost-research/.local-work/local-readiness/approved-run-N'
& $py -B runtime/session-tools/session.py prelaunch --input $plan --sha256 $planPin --out "$run/prelaunch.json"
```

Require PASS_PRELAUNCH with `deployed:true` and `adapter: "080"`; a planning audit with
deployed:false is not launch clearance. Full save/protected audits happen here
and after exit, not repeatedly during player-controlled gameplay. Preserve at
least 40,000,000,000 caller-available bytes on both C: and D:. Original save hashes
must never be replaced with changed values to bypass a failure.

Launch the pinned installed `sfse_loader.exe` once only under that approval.
Record actual launcher path/hash, local time, PID/creation and operator notice.
Do not inject or attach a debugger. The plugin admits edits only during qualified
sole-thread startup and verifies original/installed instruction guards. If it
waits, inspect admission state; no elapsed deadline justifies force-patching.

## READY, action and STOP

Select the exact newly created directory under
`.local-work/local-readiness/live/session-PID-TICK`; never select an old session.
Bind it to the original PID/creation, schema 8, executable/SFSE/DLL and site guards.
Then use the shared commands (PRELAUNCH_HASH is actual receipt hash):

```text
session.py request --input PRELAUNCH --sha256 PRELAUNCH_HASH --session EXACT_NEW_SESSION --out REQUEST
session.py live --input PRELAUNCH --sha256 PRELAUNCH_HASH --session EXACT_NEW_SESSION --request REQUEST --request-sha256 REQUEST_HASH --out READY_RECEIPT
```

Require READY_ACK before asking for the Save3 load. WAITING_READY/ACK/FRESH_ACK
means report progress and continue appropriately; never reuse an old nonce or
invent a response cutoff. Inspect actual worker health, instructions, both-drive
space and error/overflow/queued counters with lightweight `live`, using fresh
outputs and ACKs at meaningful phase boundaries. Compare health serial progress;
a delayed routine poll alone is a disclosed deviation, not a hard stop. Do not
decode the full raw stream or hash the corpus while the user stands in-game.

1. User loads the supplied Save3 label and enters normal outpost-beacon placement
   preview without confirming placement. User reports Available Resources visible.
   Mark that report with a separate local UTC/QPC-receipt note; it is not an exact
   rendering timestamp. Keep labels/screenshots local with origin preserved.
2. User moves the proposed beacon normally to observe **A: Iron + Helium-3**,
   **B: Iron + Alkanes + Helium-3**, and **C: Iron + Helium-3** if conveniently
   reachable. Report each actual list. Repeated or other sets are evidence, not
   failures. No mandatory distance, coordinates or travel; no console/spawn/save.
3. Codex checks lightweight worker health and a fresh ACK at phase boundaries.
   Native producer descriptors, scan children and UI rows are analyzed offline;
   do not promise the UI change guarantees an upstream source event.
4. User signals **STOP** when the available natural comparison is complete, the
   panel/action is impractical, or they wish to stop. No arbitrary event quota.

Actual instruction/identity/protected-input/integrity/worker failure, exhausted
queue/snapshot capacity, or failed caller-available disk query/floor is a hard
stop. Preserve the partial capture and use the shared STOP immediately while
safe; do not terminate the process, retry in-place, change target state or waive
the failure. A partial result is not successful full capture.

```text
session.py stop --input PRELAUNCH --sha256 PRELAUNCH_HASH --session EXACT_NEW_SESSION --out STOP_RECEIPT
session.py live --input PRELAUNCH --sha256 PRELAUNCH_HASH --session EXACT_NEW_SESSION --out RETIREMENT_RECEIPT
```

STOP is idempotent and preallocated; it remains available during disk/protection
failure. If a changed shared-tool pin blocks it, use the version-specific
`runtime/local-readiness-080/operate.py stop --build REVIEWED_BUILD
--manifest-sha256 MANIFEST_HASH --session EXACT_NEW_SESSION --out FRESH_RECEIPT`
with the original reviewed pins. Do not edit those pins. Require RETIRED with
active=0, queued=0, losses=0, failed=0 and attempted=captured=durable; otherwise retain
the explicit failure/partial state. Resident wrappers stay inert until normal
exit; do not hot-unpatch/unload. If a native call remains active, preserve state
and consult the operator; never invent a retirement timeout or force termination.

## Normal exit, removal and evidence

User exits normally. Record exit and any automatic ExitSave rotation separately;
no manual save or original-save overwrite is permitted. Disable/undeploy through
Vortex and verify all effective observer DLL paths absent. Confirm the original
PID/creation is gone, not merely an application-window change.

```text
session.py postflight --input PRELAUNCH --sha256 PRELAUNCH_HASH --session EXACT_NEW_SESSION --out POSTFLIGHT
archive.py seal --input ROOTS --sha256 ROOTS_HASH --postflight POSTFLIGHT --postflight-sha256 POSTFLIGHT_HASH --out SEAL
archive.py create --input SEAL --sha256 SEAL_HASH --archive NEW_ZIP --out ARCHIVE_RECEIPT
archive.py verify --input SEAL --sha256 SEAL_HASH --archive ZIP --archive-sha256 ZIP_HASH --out VERIFY_RECEIPT
```

All scripts above live in runtime/session-tools. ROOTS maps aliases to absolute
raw-capture/private-receipt/derivative directories per its README. Finish companion
receipts first; include the postflight and operator notes. Seal/ZIP/verification
outputs stay outside sealed roots. Expected raw artifacts: session/admission/
patch/module identity files, READY/ACK/control/STOP, health, emergency/terminal,
events.bin and records.jsonl. Include failed/partial tails; never repair originals.

PASS_POSTFLIGHT requires unchanged protected/save inputs, verified removal and
complete byte/record integrity. For PARTIAL_POSTFLIGHT, use explicit
`--partial-reason` when sealing; full member hashes and ZIP hash still must verify.
Compression failure remains failed/unverified output. Preserve raw, seal and
verified archive; no deletion, overwrite, automatic old-run archival or upload.
Source quiescence/exit must be established before sealing. Final interpretation
must distinguish science, instrument integrity, target outcome and authorization.
