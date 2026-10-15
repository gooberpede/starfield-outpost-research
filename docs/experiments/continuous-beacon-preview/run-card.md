# Prospective Save3 continuous beacon-preview resource run

2026-10-15, Australia/Sydney. SOR-EXP-0035 / SOR-EV-0043.
**Offline preparation only. Requires combined maintainer/ChatGPT review and
explicit authorization of the final byte-pinned 0.7.0 package and this card.**
[Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_continuous_beacon_preview_resource_oracle.md),
[native contract](native.md), [qualification](validation.md), [review](review.md).
After that approval and maintainer Vortex deployment, successful machine-side
preflight permits this sequence without another routine approval. Changed hooks,
DLL, control save, gameplay actions or safety contract need review.

## Package and source control

Selected build is `.local-work/continuous-beacon-preview/builds/qualification-06`.
The exact manifest/DLL/ZIP pins are retained in [report](report.md); use only the
reviewed manifest hash from its selected-artifact table. This is a candidate until
all mandatory qualifications and independent review pass. Runtime-required
deployment is solely `Data/SFSE/Plugins/SorNativePositionOracle.dll`. Package
ResearchNotices are not mandatory neighboring deployed files. Windows/MSVC runtime
prerequisites are pinned, with no download/update/install implied.

Ten guarded natural CALL replacements and exact target entries/getter are disclosed
instrumentation. Register/stack observation, process-local reads, synchronous file
backpressure and worker flushing affect timing. It is not non-invasive. Native
model rows are not directly observed rendering. Cross-thread atomicity, cache ABA,
unhooked lifecycle writes and crash-before-flush suffix durability are limited.
No external debugger, engine function invocation, terrain/footprint hook or save
writer is authorized. No crash tolerance or forced recovery is presumed.

Primary protected file (2,096,496 bytes):
`C:/Users/User/Documents/My Games/Starfield/Saves/Save3_D6036588M417474696C61204B6972616C79_000214_20261006013428_3_0_4.sfs`.
SHA256 `d06123ee32bd5b3e244650852fac9714697a19fd6243384966414d1d1f4ffbfe`.
Use this original source's hash-bound mtime, not a copied file's timestamp.

Operator instruction, provided once before loading:

> **Load Attila Kiraly — Kreet - Kreet — Level 3 — 10/6/26, 12:34:27 PM.**

The new save-menu receipt corroborates header/mtime model at UTC+11; it does not
claim a new screenshot verification. The brief supplies earlier load-screen control.
Do not ask for the full label again after providing this instruction unless the
character filter, duplicate label, missing file or screenshot exposes ambiguity.
Mutable menu ordinals and another character's Save3 are not identities.

## Preflight before launch

Run only after combined approval and user Vortex deployment, in repository cwd.
Every output path is fresh. The manifest hash must be the reviewed table value,
never an opportunistically re-pinned changed artifact.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$build = '.local-work/continuous-beacon-preview/builds/qualification-06'
$manifestPin = '20d82ecea1949265778ba2ee1af578baa9a9d2836bb82a23f48a131df7381b2a'
$run = '.local-work/continuous-beacon-preview/run-' + (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssfffZ')
New-Item -ItemType Directory -Path $run -ErrorAction Stop | Out-Null
& $py -B runtime/beacon-resource-070/operate.py preflight --build $build --manifest-sha256 $manifestPin --deployed --out "$run/preflight.json"
if ($LASTEXITCODE -ne 0) { throw 'Preflight failed: do not launch/load.' }
$save3 = 'C:/Users/User/Documents/My Games/Starfield/Saves/Save3_D6036588M417474696C61204B6972616C79_000214_20261006013428_3_0_4.sfs'
& $py -B save-analysis/scripts/save_menu.py $save3 --utc-offset '+11:00' --json "$run/save3-menu.json"
if ($LASTEXITCODE -ne 0) { throw 'Save3 identity/menu conflict: resolve before launch.' }
```

Verify protected saves/archives/prior releases/frozen inputs, exact game/SFSE/DLL/
ZIP/runtime prerequisites and caller-available **40,000,000,000 bytes on each C:
and D:**. Preserve a fresh private save inventory of paths/lengths/mtimes/hashes
before launch so incidental ExitSave rotation is distinct from canonical pins.
Use read-only process metadata to verify no existing Starfield/SFSE process remains;
retain the preflight existing-session list. Pinned SFSE loader SHA256 is
`16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526`.
Verify that existing loader at launch; do not update or repair configuration.

Normal Steam/NVIDIA overlays are accepted and inventoried. Unknown modules do not
trigger a blanket allowlist rejection; assess actual conflicting instrumentation.
Wrong identity, occupied/changed guarded bytes, failed disk query/floor, protection
change, recorder failure or unsafe admission is a hard safety/integrity stop.
Elapsed time, delayed action, routine cadence, count or output size is not a stop.

## Startup and observation

Operator starts the reviewed SFSE/Vortex entry. Identify exactly one new session
under `.local-work/continuous-beacon-preview/live`. Confirm session PID/creation,
module base, game/SFSE/DLL/schema7, sole-thread pre-edit admission, ten installed
sites, target guards, recorder and actual worker health. If startup waits for safe
admission, inspect waiting receipt and use STOP if necessary; do not patch while
multiple threads execute, force termination, or invent an admission timeout.

```powershell
$session = 'EXACT_NEW_SESSION_DIRECTORY'
& $py -B runtime/beacon-resource-070/operate.py request --build $build --manifest-sha256 $manifestPin --session $session --out "$run/ack-request.json"
$nonce = (Get-Content "$run/ack-request.json" -Raw | ConvertFrom-Json).nonce
& $py -B runtime/beacon-resource-070/operate.py status --build $build --manifest-sha256 $manifestPin --session $session --nonce $nonce --out "$run/ready-ack.json"
```

WAITING_FOR_READY_OR_ACK requires waiting and a fresh output name on recheck.
READY_ACK plus matching pins/worker permits Save3 loading. Full protected audits
can be slow; use watch.py for lightweight intermediate health snapshots and fresh
ACKs at meaningful phase boundaries. Stale progress is investigated and disclosed,
not silently relabelled as worker failure or assigned an arbitrary deadline.

1. Load the supplied Save3 instruction. Reach legal beacon placement preview
   without confirming placement. Operator reports Available Resources visible.
2. Mark `PREVIEW_VISIBLE`; record observed labels or screenshot where available.
   Native input must be producer-preview site, captured held ref/base and indexed
   position/frame/domain, with scope/unknowns retained. If selected base/context
   contradicts ordinary beacon preview, preserve evidence and return for diagnosis;
   never silently substitute player XYZ or another save.
3. Capture continuously while operator moves **the proposed beacon**; player may
   remain stationary. Repeated unchanged evaluations are retained. Seek different
   displayed sets if convenient; Fe versus Fe+Alkanes is useful, not required.
   He-3 is an atmospheric control; never hard-code it or make a transition mandatory.
4. Use simple phase labels A/B/C as **displayed set conditions**. C can show the
   earlier set at any position; no exact coordinate return. Native rows and rendered
   labels remain separate evidence channels. Mark useful transitions with labels
   and optional screenshot hash:

```powershell
& $py -B runtime/beacon-resource-070/watch.py $session
& $py -B runtime/beacon-resource-070/mark.py $session --phase A --labels 'Iron' 'Helium-3'
# Labels above are an example; supply only what the operator actually sees.
# --screenshot accepts an already captured local screenshot path, when supplied.
```

Markers record report-receipt time, not exact render time. Preserve operator
transition intervals, screenshot metadata and native QPC/frequency. Compare all
qualified native/UI invocations in the phase interval; unequal or ambiguous epochs
remain unresolved. No nearest-event rule. Actual consumer inputs and completed
row ordinals reconcile independently; producer matching yields correspondence
candidates, not unique queued ancestry. Plugin-qualified label/FormID mappings
must be independently supported; unresolved names/IDs are not empty resources.

No constructed extractor, resource-footprint test, beacon confirmation, console
command, new manual save, gameplay side experiment or alternative save is included.
If Save3 is unsuitable, propose evidence-backed alternatives for review.

## STOP, normal exit, removal and full scientific completion

Cancel preview without placing beacon. Mark `PREVIEW_CANCELLED`. Operator explicit
STOP ends acquisition; Codex requests it using the preallocated control file:

```powershell
& $py -B runtime/beacon-resource-070/operate.py stop --build $build --manifest-sha256 $manifestPin --session $session --out "$run/stop-request.json"
```

Wait for worker drain and accurate retired.json (or preserve failure/emergency
receipt). In-flight calls finish; patches remain resident/inert until normal exit.
Do not unload or hot-unpatch. Ask operator to exit normally, then remove this Vortex
deployment. Verify original PID/creation is gone; no termination or memory/register
change is authorized. On unexpected exit, retain complete prefix/tail/failure;
target survival, evidence integrity and scientific result are separate outcomes.

```powershell
& $py -B runtime/beacon-resource-070/operate.py postflight --build $build --manifest-sha256 $manifestPin --session $session --out "$run/postflight.json"
& $py -B runtime/beacon-resource-070/operate.py seal --build $build --manifest-sha256 $manifestPin --session $session --out "$run/seal.json"
& $py -B runtime/beacon-resource-070/inspect_resources.py $session --out "$run/native-ui-analysis.json"
```

Check exit code and explicit status at each step. Postflight checks all protected
pins and DLL absence; compare pre/post save inventory, disclose incidental automatic
exit-save rotation without restoring/overwriting originals. Seal session files with
length/hash after process exit. Preserve faults/partial tails; no retry/repair/save
mutation follows automatically. Finish scientific report and independent review
before final handoff, even if operator asks for a short postflight-only update.
Report displayed/native agreement, stable/change conditions, unknown IDs, cache/
refresh distinction, overlaps, ambiguity and missing phases; no capture is not
an empty-resource result. Milestone B remains separate and is not a gate for A.
