# EXP0002A — S1/S2 operator handoff, adapter 0.1.3

**STOP: the authorized S1/S2 sequence is complete. S1 passed; S2 exited without capture. Do not repeat or widen. The instructions below are the completed run card, retained for review.**


Authority SOR-D-0019, [brief](../implementation-briefs/EXP0002A-adapter-0.1.3.md), [audit](../audits/exp0002a-adapter-0.1.3.md). S0 already passed; do not repeat it. Preserve 0.1.2 unchanged. Do not use the historical 92-thread or x64dbg modes.

1. Codex verifies protected Save3 and backup hashes, pinned game/build, adapter/source hashes, C:/D: each >=40GB, and fresh local evidence paths. Operator launches normally via Steam without SFSE, loads Save3, opens Pause > Save, highlights New Save and does not confirm. Report ready.
2. S1 attaches with --starfield-s1 and installs no research DR0. Validate loaded SFSE/SorExp0002 absence, base/site hashes, debugger state and complete thread inventory. The UI pause is distinct from debugger stops. Setup has its own 300s bound. Report ARMED only after readiness; **ARMED is not permission to click**.
3. Operator confirms readiness to act immediately. Codex activates the native window using activate_capture.py. The native capture_started record is flushed before active acknowledgement. Only after acknowledgement, and while the deadline is still live, Codex reports **CLICK NOW**. Confirm New Save exactly once immediately. Do not wait to reply before clicking; promptly report whether the game returned to gameplay or exited.
4. The active window is 10s including cue delivery/reaction time. Confirmation is later correlation and never starts/resets it. A late/missing click makes the control inconclusive, not a pass. Native S1 terminal status requires separate operator/save-file validation. No second click or automatic retry.
5. On exit, record code, continue the event and emit terminal evidence without dead-target recovery. Collect matching Windows/WER and existing dumps locally after the run; no crash-handler installation. If S1 crashes, stop before S2. On survival, verify detach, delayed UI health, new manual-save presence, normal exit and sync, then archive evidence.
6. Only if S1 passes, review the best single existing thread for S2 with explicit TID/creation identity and rationale. S2 uses --starfield-s2 with that TID, REQUEST_ENTRY only at fresh base +0x0183c590. All other/new threads remain unarmed. One owned hit or 10s; preserve bounded no-hit without guessing the cause. No widening without subsequent results/review.

Both controls affect execution through debugger stops; S2 additionally changes owned debug registers/RF and uses balanced suspensions. Capture-first destructive recovery remains limited to exact verified experimental target after durable required capture (or independent machine safety). No pre-evidence forced game termination merely for cleanup. Original/backup Save3 remain protected. No Stage C/plugin-triggered saves; Vortex/SFSE observer 0.1.0 remains a separate future Stage-C gate. No deployment, staging, commit or push.

## Superseding final attempt — SOR-D-0021

The S1/S2 card above is historical. Current authority is the [final software attempt](../implementation-briefs/EXP0002A-final-software-attempt.md): ordinary Steam, no SFSE/SorExp0002, pristine Save3; Pause→Save→highlight New Save without confirming; report ready. Researcher attaches existing dbgeng/CDB, verifies process/build/base/site and exactly one one-shot software breakpoint. Wait for ARMED / CLICK NOW after the10-second capture window is active, then confirm once. No hardware breakpoint, S1.5 or repeat. Report game outcome; on survival exit normally/sync when requested. Capture completeness and cleanup outcome are separate. No automatic Stage C or beacon construction under this handoff.


**FINAL ATTEMPT COMPLETE — DO NOT RUN THIS CARD AGAIN.** No material request capture; native saving deferred under SOR-D-0021. Target survived, normal exit/sync confirmed. [Actual outcome and limits](../audits/exp0002a-final-software-attempt.md). Resume planning outpost/manual-save checkpoints; no S1.5 or backend retry.
