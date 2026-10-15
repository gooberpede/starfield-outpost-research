# Codex implementation brief — SOR live-experiment infrastructure consolidation and evidence archival

**Project:** `D:\Projects\starfield-outpost-research`  
**Assignment:** Bounded, single-agent infrastructure maintenance  
**Starting point:** Latest committed/synced state following the SorNativePositionOracle 0.7.0 beacon-preview live experiment.  
**Next scientific assignment (not included):** Milestone B — reconstruct the native inorganic-resource availability determination algorithm.

## 1. Purpose and completion standard

Reduce routine operator/game idle time during live experiments, reuse the proven operational tooling instead of creating fresh scripts for each observer, and provide verified, lossless compression of sealed evidence. This is **practical maintenance**, not a redesign of the observer architecture or a new scientific investigation.

Deliver a small, working and documented shared workflow that the next approved observer experiment can use for preflight, READY/ACK/STOP coordination, postflight and archival. Investigate existing implementations first. Prefer consolidation and thin adapters over a new large framework. Do not represent partial implementation as COMPLETE; resolve in-scope test failures within this assignment.

**No sub-agents, including no reviewer agent.** The maintainer and ChatGPT will critically review the delivered diff. Do not spawn or delegate to agents. This explicit assignment-specific exception supersedes the routine independent-review requirement.

## 2. First audit what exists

Inventory existing commands, scripts, receipts and contracts across prior live experiments (especially observer 0.5.0, 0.6.0, 0.7.0 and their run cards). Identify which functionality already exists, which is duplicated, which is observer-version-specific and which can safely be shared. Include:

- Prelaunch game/SFSE/runtime and DLL identity, Vortex effective-deployment checks (require **only actual runtime dependencies**; do not require optional README or manifest files in the game plugin directory).
- Protected save, frozen-input and research-source content verification; the **40,000,000,000-byte caller-available free-space guard on both C: and D:**.
- Runtime process identity, observer READY, fresh worker-health ACK, STOP and retirement/exit handling.
- Live health monitoring and evidence integrity; postflight verification and sealing.
- Save-menu identification utility and its concise operator-facing load instruction.
- Common incident/failure classifications and their durable receipts.

Create a concise **reuse/duplication matrix**, identifying the actual existing tool path and what should remain observer-specific. Do not rewrite working components merely for stylistic consistency.

## 3. Phase-aware checks that avoid idle gameplay

Implement or consolidate a minimal shared command/interface (or a few clearly documented commands) supporting:

1. **Offline/prelaunch full preflight:** expensive protected-file hashes, pinned game/DLL/tool identities, save inventory, baseline evidence and sufficient free space. Run **before launching Starfield** when practical. Record immutable hash-bound receipts and the source inventory that was checked.
2. **Lightweight live admission and monitoring:** check the actual process, deployed DLL, native-hook/observer admission evidence, READY/ACK, worker integrity and disk guard. Avoid rescanning thousands of protected files, whole archives, or gigabytes of evidence while the user stands idle in-game. Only re-run a full content audit during live play for a **specific documented integrity incident** requiring it. Distinguish a fresh ACK from an unrelated or stale ACK and preserve established observer-specific semantics.
3. **Offline postflight:** after game exit, independently check original/protected inputs, exit-save rotation, plugin removal, evidence completeness and preservation; then seal and archive evidence.

Do not weaken actual hard stops (hash/instruction identity failures, unsafe patch state, low disk space, confirmed worker/evidence integrity failures, explicit STOP). Ordinary Steam and NVIDIA overlays are accepted as baseline. Do not invent arbitrary hard time limits, polling deadlines, event-count limits or evidence-volume quotas. A noncritical delay calls for an operator update and continuation, not automatic abandonment. Avoid repeated operator confirmations after save identification has already been supplied.

Keep observer-specific hook guards, native schemas, event decoders and scientific analyses in version-specific code. The shared harness should call or consume them through a small clear contract, not rewrite them.

## 4. Verified lossless evidence archiving

Audit whether sealed historical captures are already compressed, duplicated or individually archived. **Do not bulk-convert or delete historical evidence in this assignment.** Implement a reusable offline archival operation for future sessions and prove it against disposable representative evidence.

Required archive flow:

- Require a completed immutable-source sealing/integrity receipt (or explicitly mark the archive `PARTIAL` when preserving a crashed/incomplete capture). Do not silently repair or reinterpret raw evidence.
- Construct a **lossless** compressed archive containing all required raw evidence and companion metadata, with an unambiguous relative-path manifest and original per-file hashes/sizes. Select a format readily supported on the actual machine (ZIP with reliable standard compression is adequate; consider zstd only if already available and demonstrably advantageous, without imposing a new unnecessary dependency).
- Hash the archive itself, verify file inventory, reconstruct the original files in disposable space or stream-verify **every member's decompressed bytes and hash**, and document the verified round trip. Detect corruption, missing files, duplicate paths, truncation and archive-generation errors.
- Preserve the raw originals and archived copy during qualification and first postflight adoption. **Do not automatically delete raw evidence.** Produce a separate explicit, reversible retention recommendation for later maintainer authorization to retire redundant uncompressed copies after verified archival. Ensure archive provenance distinguishes raw captures, derivatives, sensitive/private receipts and publishable reports.
- Respect the C:/D: disk guard during creation and verification; determine temporary-space needs before starting. Do not reduce scientific sampling or discard records to improve compression.
- Allow future analyses to access a necessary subset of evidence without permanently extracting the whole archive if readily supported; otherwise document a safe selective extraction procedure. Do not build an elaborate virtual filesystem.

Report measured before/after sizes and elapsed processing times on actual representative **disposable** or authorized existing local evidence, accurately distinguishing tests from production archival. Compression ratio is informative, not an acceptance threshold.

## 5. Testing and qualification

Use offline/disposable tests, with no game launch or live process contact. At minimum test:

- Preflight receipt creation and reuse versus changed/missing/mismatched protected inputs; mismatch must fail, not be waived.
- Accurate distinction between full prelaunch checks and lightweight live checks; demonstrate the latter does not rescan the entire protected corpus.
- Valid READY/ACK and stale/mismatched ACK; STOP/retirement errors and incomplete evidence as distinct states.
- Free-space guard failure and unavailable drive-space queries.
- Proper handling of expected ExitSave rotation without falsely declaring other originals changed.
- Archive round trip preserving binary bytes/path inventory, duplicate or malicious member paths, missing/corrupted/truncated files and partial capture classification.
- No modification of approved observer DLLs, saves, frozen predictions, sealed raw capture or original verification receipts.

Use existing test infrastructure where appropriate. Do not rerun enormous native-observer fixture suites unless shared-interface modifications actually affect them. Preserve negative test evidence and fix in-scope defects before handoff.

## 6. Required deliverables

1. **Short audit and design record:** inventory of existing operational tools, duplicated behavior, what was reused, what changed, and what deliberately remains version-specific.
2. **Reusable, tested shared tooling:** executable prelaunch/lightweight-live/postflight/archive commands or adapters and documentation sufficient for Codex to use without inventing another run-specific framework.
3. **Archival contract and retention proposal:** format, manifest, round-trip verification, safety checks, treatment of crash tails, no automatic deletion and selective extraction.
4. **Example future run-card fragment:** exact phase sequence and operator handoff, including save-menu label; show how the next observer would use the harness. Do not retroactively change historical run cards or verdicts.
5. **Qualification and measured cost:** test results, prelaunch versus lightweight live workload differences, actual archival timings/compression, limitations and remaining observer-specific steps.
6. **Complete review package:** `-task-only.diff` and `-complete.diff` in `.local-work/diffs/`, incorporating untracked text files, `git status --short`, changed-file and exclusion manifests, and exact forward/reverse patch verification. Keep private raw evidence/binaries/saves outside patches.

Update `WORKFLOW.md` or shared run-card templates only where essential to make the new **phase-aware, reusable** process discoverable; avoid another sweeping policy rewrite. Write normal prose and preserve technical names.

## 7. Boundaries and stopping rule

- **Single primary Codex agent only; no sub-agents.**
- No Starfield/SFSE launch, observer deployment or live experiment.
- No new observer build, native hook changes, debugger revival, new save creation, game setting changes or scientific Milestone B reconstruction.
- No bulk rewriting, deleting, compressing in place or relocating historical protected evidence without authorization.
- No staging, commit or push. The maintainer will review first.
- Treat the project-owned tools as reusable with internal provenance; obey established third-party permission and attribution rules.
- Make this a **bounded infrastructure pass**. Finish when a future live experiment can reuse the proven commands, avoid redundant full audits during gameplay and produce a verified compressed evidence archive after exit. Do not chase perfect generality, unlimited observer compatibility or maximal compression.
- If a genuinely independent authorization or essential external resource is required, identify the precise blocker; do not reclassify ordinary bugs or in-scope integration work as a final handoff.

## 8. Handoff format

Lead with a clear `COMPLETE — PASS` or an evidenced terminal finding; state the actual reusable commands, tests, archival format and verification, performance observations, exclusions, known limitations, and the paths to the review diffs. Explicitly state whether any existing capture was archived, deleted or modified (default: **none**). Suggest a **Conventional Commit** subject, but do not commit.

The next research assignment, **Milestone B inorganic resource-availability algorithm reconstruction**, starts only after this infrastructure pass is reviewed and integrated.
