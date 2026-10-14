# EXP0002A adapter 0.1.1 — fixed thread population and capture-first recovery

2026-10-07, user-directed correction, SOR-D-0017. PID 16100 was manually terminated by the user after review; this is USER-REPORTED and requires no further cleanup action. Preserve all 0.1.0 source/build/evidence receipts as a **failed dynamic-new-thread retirement test**. Do not rewrite its result after changing the experiment.

Implement adapter 0.1.1 for the next reviewed attempt. Arm only REQUEST_ENTRY on threads existing at the ARMED boundary. Record that population and subsequent CREATE_THREAD events, but do not install DR0 on post-ARMED threads or expand ownership during capture. A request executing only on an unarmed new thread may yield bounded NO_HIT; retain new-thread provenance and do not infer the cause from absence alone.

Retain ordinary Steam without SFSE, explicit SFSE/SorExp0002 loaded-module absence, disposable Save3-derived state, Pause > Save > New Save highlighted without confirmation, operator ready before attach, and ARMED before the user confirms. Setup/coordination/capture remain distinct. No Starfield launch or attachment is authorized now.

Scientific evidence has priority over tidy disengagement. Flush the required complete request record durably first, attempt bounded clean retirement, and if clean retirement cannot be established permit termination of **only the exact verified experimental target**. Verify retained handle, PID, creation time, full image path and hash. Do not force-kill before complete capture has been flushed except for an independent machine-safety condition such as measured low disk. Evidence completeness, scientific interpretation, cleanup result and target survival are separate; cleanup failure never downgrades complete captured evidence. This supersedes the prior no-kill policy for this precisely gated recovery only.

Fresh qualification is limited to the changed contract:

1. Already-running disposable target; arm existing threads, create additional unarmed threads after ARMED, request on an armed existing thread, retain one hit, durable flush and attempted retirement, delayed worker health.
2. New-thread-only request control: bounded NO_HIT, recorded unarmed thread provenance and no widening.
3. Disposable-only retirement fault after durable capture: attempt retirement, inject failure before detach, verify exact retained-handle termination, and independently verify preserved complete request evidence.

The third case is a recovery-policy control, not a natural failure or Starfield trial. Offline gate checks must reject pre-flush termination without machine safety and reject missing identity. No broad stress matrix, dynamic-new-thread arming retry, download, deployment, save modification, staging, commit, push or external disclosure. Preserve protected parents and Stage-A mapping. Observer 0.1.0 remains a separate unbuilt Stage-C reservation; adapter 0.1.1 is not an SFSE plugin. Return source/build provenance, actual checks and limits, complete diffs including new files, and Git status for review.
