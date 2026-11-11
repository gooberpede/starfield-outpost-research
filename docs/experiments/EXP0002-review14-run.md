# EXP0002 fresh primary run — review 14-settled

2026-10-06 Australia/Sydney. SOR-D-0013 authorizes a fresh primary A0/A0C/A1/A1C/A2/A2R run after review of the [synchronization correction](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/exp0002-settled-correction.md`). The [operator card](EXP0002-operator-card.md) governs actions, bounds, anomaly handling and cleanup. No optional debugger diagnostic. Prior failed-run evidence is not reused as a primary checkpoint.

## Preflight and current status

User reports review 14 ZIP installed/deployed through Vortex profile **Starfield - SFSE**, with SFSE the only other enabled mod and Starfield initially closed. Independently checked deployed DLL/config against the reviewed ZIP, source hashes against build.json, pinned game/SFSE identities, and protected parent/backup size/hash/mtime. All match. Both C:/D: have more than 40 decimal GB available. Save-directory metadata and native/configuration inventory are retained locally; protected save contents were read only for hashing, no semantic parsing.

ZIP SHA-256 `970dce992d665eeda0fcf8fcdbcb4d363016756e02e2e3a9ca4c7eeed4a37ff4`; DLL SHA-256 `9a1636adacdcd0967e7873fcdbc161fed04876d3c368f9e37735f707e9e191ed`; config SHA-256 `e6ada6592dc673d12b920864f7c944b38251fbe9a20e221b9ef551a9c4411185`. Local evidence root `.local-work/exp0002-review14-live/`; preflight.json preserves exact locators and timestamps, LOCAL-ONLY. Runtime profile/winning definitions are not established merely by the file inventory or user-reported mod list.

User-operated launch produced session `session-21888-74608765`, READY `2026-10-06T08:34:30.625Z`, with matching review 14 DLL hash and no failure marker. User explicitly confirmed settled gameplay before A0 and A0C; each request included SETTLED. Both completed and passed native-schema validation with zero optional load notifications. The run was stopped before construction/A1 due to observed execution-thread inconsistency with the main-thread assumption. No debugger, native selected-reference query, commit or push occurred. Cleanup/archive status follows below.

## Captures and controls

| Checkpoint | Capture UTC | Thread ID | Scan entries | Capture ms | Selected roles / terminal |
|---|---|---:|---:|---:|---|
| A0 | 2026-10-06T08:36:08.868Z | 15592 | 2566 | 46 | None / CHECKPOINT_COMPLETE |
| A0C | 2026-10-06T08:37:33.825Z | 21756 | 2572 | 79 | None / CHECKPOINT_COMPLETE |

Both records show optional pre/post counters zero, player FormID 00000014, stored cell FF01480C, worldspace FF014803 and persistent-cell candidate FF01BCE3. Raw player XYZ [120.827057,270.736237,17.5202465] and raw rotation [0,0,0.0381769538] match. Units/frame remain unqualified. Counts describe only the bounded two-cell scan, not universal absence of outposts. Scan-entry variation is observed, not assigned a cause. No selected-reference callback was invoked in either baseline checkpoint. These records exercise zero-message acquisition but do not establish membership, reload behavior or a safe integration point.

The user reports A0 and A0C saved into new manual slots, with no deliberate movement/construction. A0 maps to one newly observed manual filename; A0C's metadata observation occurred after the exit-save appeared, so its original observation correctly records REQUIRES_REVIEW. Final archival correlation must separate the single new manual A0C filename from the incidental exit save using operator confirmation and recorded timestamps; do not silently overwrite the original observation.

## Thread discrepancy and stop before native calls

The captured thread IDs differ. The SFSE loader log reports primary/main thread ID 21756; process-thread metadata independently showed 21756 created at process launch and 15592 created later. Thus A0 was not executed on that OS main thread, while A0C was. The approved header describes AddTask as main-thread execution, which informed the original native-query preparation.

Read-only inspection of pinned SFSE [PluginManager.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/PluginManager.cpp#L51-L56) and [Hooks_Command.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/Hooks_Command.cpp#L21-L39) shows AddTask routed to a queue drained from the command-processing hook, without a thread-ID check in that implementation. Source SOR-S-0119 is credited; no hook implementation was incorporated. This explains why the interface comment alone cannot establish execution-thread affinity. It does not prove the complete installed-binary scheduling model or callback safety on other threads.

The researcher stopped experimental progression before beacon placement/A1 rather than assume the selected-reference callbacks are safe on a different thread. This was an evidence-driven operator stop, not a fabricated observer failure.json or global anomaly stop. The observer's files contained no anomaly or terminal failure at inspection. No A1 request, debugger, thread/context mutation, hook change or automatic retry occurred. A0/A0C evidence remains valid as bounded, non-atomic reads with their actual thread provenance. Before native-query continuation, the main-thread requirement must be explicitly enforced or an alternative execution contract established and reviewed.

## Exit, archive and disposition

User confirms normal exit, Steam sync completion and subsequent Vortex disablement of the observer. Process absence and absence of deployed SorExp0002 DLL/config were independently verified. No researcher deployment/removal, forced termination or debugger attachment occurred. No beacon/storage was placed. A1/A1C/A2/A2R were not requested; no complete-sequence marker exists.

Post-exit inventory contains two new manual saves (A0/A0C), one new incidental exit save, no changed existing save filenames and one missing prior exit-save filename. The missing prior exit save already has a verified copy in the first attempt's archive. Both immutable parent/backup retained size, SHA-256 and mtime. Thirteen exact-byte copies preserve three saves, eight observer/control files and two SFSE logs. Source/copy/source hashes and source metadata agree. No semantic save inspection or comparison was performed.

A0C correlation was resolved without rewriting its original REQUIRES_REVIEW observation: its one new manual filename follows A0C capture and precedes the distinct incidental exit-save timestamp; the user confirmed the new manual slot. This is operator/metadata correlation, not a save-content inference. Actual private locators remain in local post-exit.json.

| Sample / alias | Bytes | SHA-256 |
|---|---:|---|
| SOR-SAMPLE-0002 / A0 | 2082992 | `7d25e02cc0ac4bc81ab7d966a73c84ade0c6c795d154aa625d85b0aaf259fa66` |
| SOR-SAMPLE-0003 / A0C | 2066048 | `875f2e8460d3e5adfdfc15de860a57b991139195905ffff461c43fdf59409d0c` |
| Incidental exit (not a primary checkpoint) | 2074288 | `adaf84c0708214ed2055148fb196c7d461427ba1f8641855eef40f8456d077a1` |

Evidence completeness: **A0/A0C complete; primary A0–A2R sequence incomplete**. Scientific result: **baseline/control observations only; no membership or reload result**. Instrument result: **zero-message acquisition exercised; execution-thread assumption contradicted for A0**. Target outcome: **normal user exit**. [SOR-EV-0004](evidence/exp0002-review14-live/README.md) indexes exact evidence. All raw records/saves remain LOCAL-ONLY. No observer/request code was changed during this live run, no source/save bytes patched, and no staging/commit/push occurred. No new source implementation was incorporated.
