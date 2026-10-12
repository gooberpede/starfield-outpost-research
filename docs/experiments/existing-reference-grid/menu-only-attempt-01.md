# Menu-only attempt 01 closure

2026-10-12, SOR-EXP-0031 / SOR-EV-0039 continuation. The user approved observer0.4.0 and the original card, deployed it in Vortex profile `Starfield - SFSE`, and selected the Vortex SFSE launch button. They reported a responsive main menu without loading a save, then normal exit and observer disablement.

The menu-only session was `session-9540-81095078`. Admission and cooperative module/ACK checks passed. READY's payload timestamp preceded its startup wait; actual durable READY file time was 09:48:31.958956 UTC. The first external monitor sample was 09:50:37.570208 UTC, 125.611252 seconds later. Codex stopped for exceeding the original 120-second admission budget by 5.611252 seconds. This was an external procedural timing deviation, not evidence of an unhealthy observer or game. No save was loaded. The original attempt and its deviation remain recorded.

Retirement at 09:51:06.307 UTC had zero events, loss, health timeouts or depth errors. Postflight at 09:54:40.643616 UTC passed: game/loader/debugger absent, observer DLL absent, all 280 frozen pins unchanged and all 261 inventoried save files unchanged (zero new, missing or changed files). This includes protected Save25-28 and the frozen archive. Save28 SHA256 remains `7360ce427b2a51aa94efb776d09dfaa30654c44ba08c60259b52c639cde2a35c`.

Local supporting receipts are `.local-work/existing-reference-grid/live-01/` (startup timing, menu inspection, admission, operational stop) and `.local-work/existing-reference-grid/postflight-01/` (audit, save differences and inspection). Raw evidence stays local. Complete retirement and cleanup do not establish native reachability: there are no scientific records and native equivalence remains NOT TESTED.

The user subsequently instructed that a time limit alone must not scuttle a healthy live test and requested confirmation first. The [retry timing addendum](retry-timing-addendum.md) adopts that instruction prospectively. No deployment, game launch, save modification, Git staging, commit or push was performed for this correction.
