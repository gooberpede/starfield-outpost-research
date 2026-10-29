# D5P v1 proposed Phase B card — NOT AUTHORIZED

2026-10-29, Australia/Sydney. [Brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_SFSE_retained_population_observer.md),
[Phase A report](d5p-report.md), [review](d5p-review.md), [source ledger](d5p-sources.csv).
This card is a proposal. Independent Phase A review and a separate explicit
maintainer GO are required. No command below grants permission by itself.

The candidate is `.local-work/d5p/build14/SorRetainedPopulation-0.1.0-review.zip`.
Its exact ZIP/DLL/build/qualification hashes are in that directory's
`package.json` and the final delivery manifest. Any mismatch stops admission.
Only the maintainer installs, enables, disables or removes it through Vortex.
Only the maintainer starts `sfse_loader.exe`. Ordinary Steam launch does not
test this SFSE plugin. Codex must never install, launch or remove it on their behalf.

## Scope, inputs, effects and stop conditions

One separately approved process and ordinary protected Save52 load/travel target
second Feynman V, source `0:37536:20928:0029d20e`, chart 0, owner FormID
`0x0005e0de`. No alternate target, retry, forced generation, cache clearing,
console command, save write or configuration change is included. Native function
hooks and bounded reads alter execution timing. The method is observation-only
with respect to gameplay state; it is not intervention-free.

The installed baseline is Starfield 1.16.244.0, EXE SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
ESM `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`,
PlanetData `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`.
The actual SFSE runtime DLL is pinned by the build; its inspected file version
is 0.2.21. Loader file metadata reports 1.1.1; this is not the runtime version.
Reverify both installed prerequisites instead of inferring compatibility from
the loader's name or a previous startup report. No CommonLibSF runtime is required.

Both C: and D: must retain at least 40,000,000,000 caller-available bytes.
Identity, hook integrity, unsupported critical reads, capture loss, output failure,
protected-input change, or explicit operator STOP closes the affected acquisition.
No elapsed-time, event-count or evidence-volume scientific cutoff is imposed.
Queue/point/table bounds are engineering capacity controls; exceeding them is
incomplete coverage. Do not weaken a failed guard or silently retry.

A crash after independently verified durable decisive evidence is acceptable.
A pre-evidence crash is incomplete. Clean exit is optional for science. Never
terminate the game automatically, suppress exceptions, restore a save or remove
residue to manufacture a successful result. Preserve raw originals and contrary
observations; a partial or hit-only capture is useful at its actual strength.

## 1. Codex read-only preflight, before installation or launch

Confirm the game is absent. Authenticate the final review, package and source
pins. Verify protected Save52/manual/quicksave/designated saves and independent
backups, the active archive-backed baseline, installed definitions/configuration
and both disk floors. Reliably classified active autosaves/exitsaves are diagnostic;
unclassified saves fail closed. `remotecache.vdf` is diagnostic, not a protected
save hash. Obtain fresh operator confirmation that Steam Cloud saves are disabled.

Record the intended Vortex profile and actual deployment preview. Two profile
directories were present during Phase A; their active/enabled state was not
established. The maintainer must confirm the exact profile in Vortex and identify
any earlier observer or potentially conflicting plugin. Codex may inspect files
and state read-only but must not change that profile.

From the repository root, this executable preparation command reads inputs and
writes only task receipts and a Save52 rehearsal copy:

```powershell
$Python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$Build = 'D:/Projects/starfield-outpost-research/.local-work/d5p/build14'
$ProfileLabel = Read-Host 'Exact intended Vortex profile label, confirmed by maintainer'
& $Python -B runtime/retained-population/operate.py preflight --build $Build --name phase-b-preflight-v1 --profile $ProfileLabel
```

Read the resulting `.local-work/d5p/phase-b-preflight-v1.json`. Existing D5P
presence, a conflicting DLL, failed preservation or missing prerequisite must
be resolved by the maintainer before admission. Phase A does not require a live
installation. Do not substitute an older preflight or a broad retired loose audit.

## 2. Maintainer-only installation and launch, after separate GO

1. Install the exact approved ZIP through Vortex in the confirmed profile. Review
   the archive's `Data` root and file preview: only
   `Data/SFSE/Plugins/SorRetainedPopulation.dll` is runtime-essential. Keep
   `ResearchNotices` with the research package; do not deploy source/build outputs.
2. Enable/deploy the approved candidate through Vortex. Confirm no earlier
   D5P/native experiment is enabled and retain the actual staging/deployed paths.
3. Launch explicitly using the installed `sfse_loader.exe`. Stay at the main
   menu. **Do not load Save52 before the READY gate passes.**

Codex records the actual GO verbatim in a local authorization receipt, including
`phase: "B"`, `explicit_go: true`, fresh `steam_cloud_disabled: true`, approved
`package_sha256` and this exact `card_sha256`. These fields document human
authorization; creating JSON alone is not authorization. The gate must be bound
to the reviewed package and card, not an unreviewed replacement.

## 3. READY before Save52

The plugin must create fresh identity, raw, flush and `ready.json` evidence below
`.local-work/d5p/live/session-<pid>-<tick>/`. No READY is a failed gate, even when
the DLL is installed or a Starfield process exists. Sole-thread installation
availability and actual SFSE load behavior remain retail tests.

With the exact new session and recorded authorization paths:

```powershell
$Session = Read-Host 'Absolute new D5P session directory'
$Authorization = Read-Host 'Absolute reviewed Phase B authorization receipt'
& $Python -B runtime/retained-population/operate.py ready --build $Build --name phase-b-ready-v1 --session $Session --authorization $Authorization
```

The helper checks the exact approved DLL, game/SFSE identity, PID creation time,
eleven installed hooks and a fresh worker nonce ACK. It independently validates
the acknowledged raw prefix. Check the actual `READY_AT_FRESH_ACK` receipt and
absence of terminal/failure/STOP evidence before clearing the maintainer to load.
Installed files, process name and stale startup logs are insufficient. Failure
means no experimental Save52 load; the maintainer exits and removes/disables the
candidate in Vortex. Codex does not attempt another launch.

## 4. Ordinary observation

After READY, the maintainer loads protected Save52 and performs only the agreed
ordinary load/travel sequence to second Feynman V. Retain operator checkpoints
and ordinary observed outcomes. No instrumentation change, regeneration, retry,
alternate mask or target is authorized. The reader reports construction-only,
retention-only, hit-only, bypass, contrary and incomplete results separately.
Source pointer equality alone never proves lifetime; first observed never means
first-ever. A runtime chain makes no persistence claim.

Codex may read session receipts and request fresh worker ACKs under the approved
run. An operator STOP is a `STOP` file in this exact task-owned session. The
worker drains admitted records and leaves inert resident wrappers until exit;
it does not unpatch or unload. No deadline is inferred from a slow operator.

## 5. Exit, maintainer removal, and Codex read-only postflight

The maintainer exits when appropriate, then removes the candidate through Vortex
or disables it and verifies the expected disabled state in that same profile.
This helper's strict absence path assumes removal: verify the staged and deployed
DLL are absent. If a disabled staging copy remains, retain its exact identity and
Vortex disabled-state evidence for explicit review; do not delete it or silently
treat file presence alone as enabled deployment.

```powershell
& $Python -B runtime/retained-population/operate.py postflight --build $Build --name phase-b-postflight-v1 --preflight 'D:/Projects/starfield-outpost-research/.local-work/d5p/phase-b-preflight-v1.json' --session $Session
```

Postflight verifies game absence, protected content/save equality and independent
backups using the same policy, both free-space floors, capture integrity and
known Vortex/deployed-path absence. A residue is a reported postflight issue;
Codex must not remove it. Authentication may retain a decisive verified prefix
after a crash without pretending the whole session completed. Retain relevant
startup and closeout receipts, raw originals and failures locally. No new
archival programme, integration, commit, push, B6 or publication follows.
