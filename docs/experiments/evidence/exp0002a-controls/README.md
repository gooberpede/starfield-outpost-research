# SOR-EV-0006 — S0/S1/S2 controls and crash evidence

2026-10-07 Australia/Sydney; SOR-EXP-0002A, SOR-D-0019. Authored index REVIEW-REQUIRED; all raw saves, dumps and debugger logs LOCAL-ONLY and ignored. [Audit](../../../audits/exp0002a-adapter-0.1.3.md), [S0](../../EXP0002A-S0-control.md), [S2 selection review](../../EXP0002A-S2-thread-review.md).

| Control | Project result | Decisive evidence and limits |
|---|---|---|
| S0, no debugger | PROJECT-VERIFIED RUNTIME PASS | Operator normal Steam/Save3/New Save/gameplay/normal exit/sync; independently copied and hashed Save6, SOR-SAMPLE-0004. No retrospective loaded-module assertion or reload/format proof |
| S1, attached without DR0 | PROJECT-VERIFIED RUNTIME PASS | Zero native DR0 owners and no explicit suspensions; pre-click active window; new Save7 last-write inside that window; operator gameplay/delayed responsiveness/normal exit/sync; native detach and15s presence checks. SOR-SAMPLE-0005 |
| S2, one existing window-owner thread | INCOMPLETE_PRE_CAPTURE_TARGET_EXIT | Exactly one owner TID19140; active window before cue; operator click then exit; zero request records; raw deadline NO_HIT then stale-thread retirement failure. No process-exit event reached the handler and no native terminal record. No widening/retry |

Local root: .local-work/exp0002a-adapter-0.1.3/. S0 authoritative archive index is s0-archive/corrected-index.json; the initial overbroad archive manifest is retained as a documented counterexample, with unrelated copies excluded. Exact experimental Save4/5/6 cleanup paths and verified hashes are recorded separately; unrelated original saves were untouched.

S1 native SHA-256: 2155f65faf61ed42d83dac05c5f36636dbc34a78ba061f4d5698fa2285ab5b82. S2 native SHA-256: e204aa3deffb99ce0f81f48e81c0961638d1b0584a4a362209e3d407347299d9. Used build/source identity and four passing disposable lifecycle controls are in build-02/manifest.json, used-source-build-02/ and qualification-01/. These qualify limited mechanics and do not erase the live S2 counterexample.

Post-run collection secured existing filename-PID/time-matched dumps: prior0.1.2 PID10364,152,746,596 bytes, SHA-256ed6d66eab9696aae09b1de5d7edb7a74c449893fe8374c29582a9c152a49ff18; S2 PID15608,152,465,020 bytes, SHA-25635da8e8b7459ec67ec30d9ad7fcb878cee38ac26f445cb603da68bfec9bf23eb. Source/copy/source hashes matched. No dump contents were interpreted. Application1000/1001 query returned no matching records; system WER directories remain partially inaccessible. No handler, ACL, registry or network change.

The full0.1.2 run remains unchanged as INCOMPLETE_PRE_CAPTURE_TARGET_EXIT;383 earlier evidence files were rehashed unchanged. S0/S1/S2 narrow the investigation but do not prove a unique failure cause, a correct initiating thread, arguments, manager instance, naming or completion contract. Stage A remains static; Stage C remains blocked. Current status: stop for review, no additional live run.
