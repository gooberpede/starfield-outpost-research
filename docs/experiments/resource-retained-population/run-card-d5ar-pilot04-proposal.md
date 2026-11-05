# D5AR Pilot04 operator card

Status **OFFLINE PREPARATION ONLY**. One separately approved smoke test on
Starfield 1.16.244.0 and SFSE 0.2.21. Can one command after normal arrival
finalize a protected resident geometry copy in the retail process?

Use the package `SorOutpostGeometrySnapshot-0.2.0-D5AR-Vortex-Pilot04-REWORK01-NOT-AUTHORIZED.zip`
and its sibling `packaging.json` in `.local-work/d5ar/pilot-vortex04-rework01`. The
receipt pins the archive, DLL, source lock, sidecar, both build receipts and
operator cards. The ZIP holds the DLL and UTF-8 LF sidecar together under
`Data/SFSE/Plugins`, with the project license and full Ian Patterson MIT
notice. The source and offline controls are retained in the local build
handoff. The [Pilot03 card](run-card-d5ar-pilot-proposal.md) supplies the
inherited preservation and fresh Preload gates. Use the sequence here for
trigger, evidence and success criteria.

## Operator sequence after separate approval

1. With Starfield closed, verify the approved `Starfield - SFSE` Vortex
   profile, Steam Cloud disabled, exact effective native load set and fresh
   SFSE Preload route. Verify exact Save52 and the protected originals,
   independently verified backup and rehearsal restore copy. Run the full
   [protected preflight](../../SAVE_PROTECTION.md) and require both
   caller-available drive floors of 40,000,000,000 bytes. With earlier SOR
   packages disabled, import this ZIP via **Install From File** and deploy
   through Vortex. Have the operator verify deployment before launch.

   ```powershell
   & 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -E -B 'D:/Projects/starfield-outpost-research/research/resource-retained-population/d5ar_direct_package.py' check-deployed
   ```

   Require `PASS_DEPLOYED_FILES_ONLY`. This checks archive and deployed
   members, duplicates, target hashes, disk floors and an empty capture
   directory. Separately verify the effective load set and protected files.
   Keep the deployment and sidecar fixed until Starfield exits.
2. Launch one fresh process through the approved SFSE route. At the main menu,
   before console input or loading a save, require a finalized
   `COMMAND_READY` startup receipt with evidence basis `UNQUALIFIED_NATIVE`, PID and process
   creation FILETIME matching the fresh process. Compare game, SFSE runtime,
   DLL, source lock and configuration SHA-256 with `packaging.json`. Require
   observed, complete startup stack admission. Preserve the other startup
   receipts. On a startup refusal, use the STOP procedure below.

   ```powershell
   $capture = 'D:/Projects/starfield-outpost-research/.local-work/d5ar/pilot-vortex04-rework01/capture'
   Get-Process -Name Starfield | Select-Object Id,@{n='creation_filetime';e={$_.StartTime.ToUniversalTime().ToFileTimeUtc()}}
   Get-ChildItem -LiteralPath $capture -Filter '*.startup.json' | ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json }
   ```

3. Load protected Save52 once, at the Lodge, and travel directly to
   **Feynman V Cu IL F**. Wait for ordinary gameplay to settle. Record arrival
   and location as operator evidence. Stay in ordinary gameplay. Avoid
   Build Mode, edits, detours, forced refreshes and deliberate saves.
4. Enter `SORSnapshot` once. Record the `ARMED` capture UUID and output path
   and close the console. Require the displayed path to match
   `capture_directory` in `packaging.json`. A mismatch triggers STOP and
   protected closeout. The command queues one attempt immediately.
   Observe the private output directory while remaining at the outpost. Use
   the file as the completion signal. Keep any refusal or partial and end
   the attempt without retrying, reloading or substituting a trigger.
5. Exit Starfield normally without making a deliberate save. Verify the
   exact process exited. Disable Pilot04 in Vortex, deploy the removal and
   independently check effective absence. Run full protected postflight,
   including protected-content comparison, backup identity and rehearsal
   verification. Preserve loose originals and a lossless local evidence
   archive. Verify every archive member. Compare the capture UUID, session,
   PID and creation FILETIME to the console/startup evidence and independently
   decode the terminal artifact offline. Use the raw decoder in the
   source-locked build copy. Verify its SHA-256 against the entry for
   `research/resource-retained-population/d5ar_snapshot.py` in
   `source-lock.json` before invoking it. Require exactly one snapshot.

   ```powershell
   $pilot = 'D:/Projects/starfield-outpost-research/.local-work/d5ar/pilot-vortex04-rework01'
   $build = 'D:/Projects/starfield-outpost-research/.local-work/d5ar/direct-worker-rework03'
   $method = 'research/resource-retained-population/d5ar_snapshot.py'
   $decoder = Join-Path (Join-Path $build 'sources') $method
   $lockPath = Join-Path $build 'source-lock.json'
   $pins = Get-Content -LiteralPath (Join-Path $pilot 'packaging.json') -Raw | ConvertFrom-Json
   if ((Get-FileHash -LiteralPath $lockPath).Hash -ne $pins.artifacts.'source-lock.json') { throw 'Source lock differs' }
   $lock = Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
   if ((Get-FileHash -LiteralPath $decoder).Hash -ne $lock.files.PSObject.Properties[$method].Value) { throw 'Decoder identity differs' }
   $snapshots = @(Get-ChildItem -LiteralPath (Join-Path $pilot 'capture') -Filter '*.snapshot.json' -File)
   if ($snapshots.Count -ne 1) { throw 'Expected one finalized snapshot' }
   $summary = Join-Path $pilot 'raw-decoder-receipt.json'
   & 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -E -B $decoder $snapshots[0].FullName --out $summary
   if ($LASTEXITCODE -ne 0) { throw 'Raw decoder refused' }
   Get-Content -LiteralPath $summary -Raw
   ```

## STOP and acceptance

On operator STOP, unexpected game/observer behavior, disk/protected-content
failure or a stalled attempt, create plain `STOP` in the capture directory
(`STARTUP_STOP` during startup). Preserve artifacts and follow the normal exit
and protected closeout above. One copy is bounded by validated sizes, memory
availability and per-read cancellation. Copy-time STOP may finalize a refusal.
Publication checks STOP around serialization, during output and readback, and
just before rename. An in-progress allocation or I/O call may have to return
before a check runs. STOP after the last check can race rename. Retain any
result from that race and classify the interrupted attempt as incomplete.
The writer checks available output space for remaining encoded bytes above the
disk floor. This check cannot reserve space against other processes, and the
copy memory budget excludes JSON serialization. An early STOP or I/O failure
can leave no finalized result. Avoid
forced termination, automatic restoration and hot unload. An unexpected
original native exception retains its original propagation.

The instrument patches five lifecycle and two source-ending sites (35 native
bytes, 28 KiB relay pages) during guarded startup. The worker writes the native
reader count and can briefly delay a writer. The worker and STOP timer also
affect scheduling. A busy word, missing owner/attachment, empty map or
lifetime refusal ends the attempt. These results do not establish that the
outpost has no resources. The worker does not call a generator or force a
refresh. Unknown native failures can leave an incomplete attempt.

Technical success requires raw decoder status `REPRESENTATION_VALID_UNQUALIFIED`,
`capture_status` of `COPIED_UNQUALIFIED`, positive `geometry_entries` and
`represented_points`, matching startup, package and capture identities,
no operator STOP, and passing protected closeout. Empty or unavailable
holder rows count toward `represented_entries`. Preserve them even when
they supply no points. A refusal, partial-only result, absent result or
zero represented points leaves retail capture incomplete. The raw schema
and encoding are shared with 0.1.0. Outpost attribution and physical area
association remain UNKNOWN in this route. Pilot04 cannot enter the existing
0.1.0 scientific source profile or count toward the 30-sample series. GC-10,
GC-31, D5R and study qualification remain open.
