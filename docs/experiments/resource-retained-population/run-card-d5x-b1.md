# D5X-B1 instrumentation validation — NOT AUTHORIZED

2026-10-30, Australia/Sydney. This is a proposed single visit, not a retail GO.
Separate explicit authorization must bind this card, the final reviewed
DLL/package/build/reader hashes and the exact actions below. B1 does not authorize
B2, a scientific winner claim, another launch or an automatic retry.

## Identity and ownership

Use the final D5X compatibility manifest named in [the report](d5x-report.md),
not a development build or an old D5P ZIP. Required baseline: Starfield
1.16.244.0, SFSE runtime 0.2.21. Exact locally reverified pins are in
`.local-work/d5x/identity04/identity.json` and the final build manifest:

| Input | SHA-256 |
|---|---|
| Starfield.exe | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Starfield.esm | `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7` |
| Starfield - PlanetData.ba2 | `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5` |
| sfse_1_16_244.dll | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` |

The loader was rehashed offline in `identity03` and matched
`16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526`
at the installed game-root path. Rehash it before approval and retain its exact
actual path/hash. No address transfers to another build are allowed.

The maintainer alone installs/enables/deploys the exact package through Vortex,
launches once through `sfse_loader.exe`, performs gameplay, exits, and disables or
removes the observer through Vortex. Codex verifies bytes, receipts and evidence,
records checkpoints and performs only the separately authorized session-control
file writes. Codex never launches the game, installs/removes plugins, patches
saves, changes configuration, forces generation or terminates the game.

## Proposed sequence

1. **Offline preflight:** with Starfield absent, authenticate final source,
   build, DLL, package, reader, card and tool pins. Recheck installed inputs and
   all fourteen site/target guards. Apply [current save protection](../../SAVE_PROTECTION.md)
   to all designated research/manual/quick saves and independent backups,
   including exact Save52 length/hash and a verified scratch restoration COPY.
   Audit protected remote saves, configuration, definitions and relevant content.
   Enumerate namespaces; unknown saves fail closed. Reliably classified active
   autosaves/exitsaves and `remotecache.vdf` remain diagnostics. No original is
   overwritten. Use the current archive-backed preservation method, not obsolete
   loose Cargo/evidence requirements. Verify at least **40,000,000,000
   caller-available bytes on both C: and D:**; unavailable queries fail closed.
2. **Operator confirmation and install:** record fresh confirmation of Steam
   Cloud disabled where applicable, Vortex profile `Starfield - SFSE`, exact
   Save52 choice, no competing deployed SOR observer and no prior attempt.
   Maintainer uses Vortex Install From File, enables and deploys the approved
   ZIP. Codex hashes the effective
   `Data/SFSE/Plugins/SorConstructionWinner.dll`, records actual staging paths
   and checks competing observer DLL absence. A UI checkbox alone is insufficient.
3. **Main-menu gate:** maintainer launches once via the pinned loader and stays
   at the main menu. Codex selects only the new `.local-work/d5x/live/session-*`
   identity, checks actual PID/creation time, retail flag, module base,
   game/SFSE/DLL hashes, startup nonce, all fourteen installed sites and worker
   health. Fixture-host receipts are forbidden. Missing READY is a startup
   uncertainty/failure, never permission to load a save.
4. **Fresh challenge before Save52:** under the future explicit session-control
   authority, Codex generates a new 32-character lowercase hexadecimal challenge,
   writes exactly those bytes to a sibling temporary file, flushes it and
   atomically replaces `request.txt`. Read `ack-CHALLENGE.json` only after its
   durable completion. Require unchanged startup `nonce`, matching
   `request_nonce`, process/DLL identity, `hooks_intact`, `capture_active`, current
   loss counters and an authenticated flushed prefix. Do not reuse a prior ACK.
   The [schema](d5x-schema.md) defines the protocol. The 070/080 shared adapters
   do not support D5X; do not pass them a fabricated adapter ID.
5. **Exact save-load gate:** exercising native construction boundaries may
   require loading **Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs**
   and ordinary travel to second Feynman V. That exact load/travel must be named
   in the separate B1 approval. After fresh READY/ACK, maintainer loads it,
   records load-complete, travels ordinarily once to Feynman V Cu IL F and
   records arrival. Loading is not proof of cold state. No resave, forced cache
   clear, sleep/wait experiment, repeated trip or automatic retry is included.
6. **Boundary validation endpoint:** after that one arrival and a fresh health
   challenge, operator issues STOP and exits normally. B1 seeks native provider,
   selection, visited/map and sampler receipts when those branches actually
   occur; READY alone cannot pass them. Record the first missing boundary or
   explicit uncertainty. A hit/bypass/no-call visit may validate only a subset
   and must not be called full instrumentation qualification. No arbitrary
   time/record/byte quota terminates a healthy session; this finite ordinary
   gameplay endpoint controls the visit.
7. **Postflight:** after confirmed process exit, maintainer disables/removes
   through Vortex. Codex checks effective deployed-DLL absence and actual staging
   disposition separately, both disk floors, protected saves/backups/content and
   configuration against preflight, and fresh Cloud status where applicable.
   Preserve all original receipts, even failed trials. Reduce only offline with
   the pinned reader, seal a lossless archive and stream-verify it while keeping
   raw originals. Obtain independent B1 review before considering B2.

## STOP, failure and recovery

Explicit operator STOP, disk query/floor failure, identity/site/relay/target guard
failure, genuine worker/output failure or protected-input incident supersedes
continued capture. Codex may create only this session's STOP file under future
approval; no hot unload, exception suppression, process kill or automatic restore.
Hooks affect execution and may contribute to a crash. Keep authenticated durable
prefixes and mark uncertain tails. A pre-evidence crash is not validation success;
post-evidence survival and evidence completeness are separate. Unexpected save or
content corruption requires a maintainer recovery decision; never overwrite from
backup automatically. Delayed operator action or a routine late poll alone is
not failure and does not trigger termination.

This card remains **NOT AUTHORIZED**, including its control-file writes.
