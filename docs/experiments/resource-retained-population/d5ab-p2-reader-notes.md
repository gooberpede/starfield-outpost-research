# P2 reader and reducer investigation

2026-11-01, Australia/Sydney. This is the specialist working ledger for P2-Q3
and P2-AC04. The [P2 contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P2_controller_reducer_transport_qualification.md)
and primary active ledger govern completion. D5AB remains INCOMPLETE; D5R OPEN;
B2 NOT AUTHORIZED. Source-lifetime joins remain conditional pending P1/P3.

## Checkpoint 1 — baseline inspection

The schema-3 reader accepts duplicate and regressing ACK lines, because it uses
the maximum observed record count. It can expose prefix chains despite a
damaged tail or incomplete finalization. Its existing `complete_session` flag
already distinguishes finalization; P2 additionally requires the chain API to
separate prefix candidates from the stronger finalized-session claim.
Schema 2 must retain its separately tested historical interpretation.

C2 identifies Build08's packaged reducer as
`f0b1f2d409f1baa5300d6ea18daa832ba4c6ddfd39cc21a660318df137699081` and the
later frozen reducer as
`c3226c3050d5d41143c92ee736e23e6474b77018b845f1f3613790e4444322c3`.
The later version adds zero/duplicate allocation and low-pointer refusals.
Historical receipts are preserved. New tests will bind the final producer and
both final consumers rather than overwrite those receipts.

Plan: preserve authenticated prefix candidates and diagnostics, suppress final
schema-3 chains on integrity/finalization/loss defects, reject malformed ACK
types and nonmonotonic cumulative prefixes, and retain explicit native-lifetime
qualification limits. Reproduce old B1 separately. Add disposable derivatives
without modifying original captures. No target process or proprietary source
analysis is needed by these consumer-only controls.

## Checkpoint 2 — consumer fixes and development tests

The final consumer implementation rejects duplicate/regressing and malformed ACK
counts, checks terminal accounting, and keeps prefix candidates while suppressing
final chains for damage, incomplete finalization or counted losses. A complete
no-bypass positive still qualifies the offline witness logic. Native/scientific
source-lifetime qualification is explicitly false. The reducer rejects repeated
entry/selection identities and reversed native timestamps through append.

Development runs against preserved Build08 are not final combined qualification:
`p2-reader02/receipt.json` records 175 passing checks; `p2-reader03/receipt.json`
records 183 after additional telemetry/accounting and retained-prefix controls.
Both are under `.local-work/d5ab/` and explicitly report a packaged-consumer
mismatch. The first `p2-reader01` stopped after its malformed-ACK check because
the new harness tried to parse multi-line JSONL with the single-object helper.
Its progress and partial derivatives remain preserved. The corrected helper
mutates one ACK line, and the complete reruns pass. This was a harness defect,
not a producer failure. Final qualification requires packaged-consumer equality;
`--development` explicitly permits the interim mismatch.

The separately retained baseline probe
`.local-work/d5ab/p2-reader-baseline-counterexamples.json` reproduces five old API
outcomes with the exact historical reader: duplicate ACK, regressing ACK,
damaged trailing bytes, missing terminal and late terminal loss each preserve one
prefix chain. Those outputs are comparisons with the new P2 contract, not
retroactive edits to historical verdicts. The new API preserves that candidate
as lower-level evidence and suppresses the final chain. B1 schema 2 remains an
exact full-result comparison against its frozen reader.

Next: repeat on the final native build, require exact producer/consumer hashes,
and obtain primary integration review plus independent final-snapshot review.

## Checkpoint 3 — telemetry consistency and controller challenge

The `p2-reader04` development run passes 184 checks. A new discriminating control
reports ACK loss with zero sampled bounds and a terminal receipt denying that
loss. The reader now accumulates durable ACK loss counts, checks their monotonic
progress and cause totals, and refuses terminal accounting below the admitted
ACK loss count. Final firstness suppression consults sampled ranges and counts
independently. A terminal-only sampled interval is conservatively refused too.

Technical review of the primary controller found that its active-prefix helper
ignores bytes after the requested prefix, which is correct during recording but
insufficient for closed evidence. Recommended exact stopped-session reader
reconciliation and damaged-tail controls to the primary implementer. This
specialist review is advisory and cannot substitute for independent acceptance.

## Checkpoint 4 — independent review counterexamples and remedies

The independent reviewer identified missing READY and contradictory clean/faulted
terminal states. Before correction, each retained one chain and reported a
complete session. The three failing derivative cases and hashes are preserved in
`.local-work/d5ab/p2-reader-review-baseline01/receipt.json`. Schema 3 now requires
READY for finalization and a clean terminal output-fault count and name. Valid
prefix candidates and durable counts remain available when these checks fail.

The reviewer also identified unchecked Generated-event context. Nine separate
mutations of status, hazards, epoch, owner, source, thread, request, frame and
parent each incorrectly retained a chain. The original failures are preserved in
`generated-receipt.json` beside that baseline receipt. Generated now participates
in the same status, hazard and append-context checks as reserve/store.

A synthetic cross-thread retirement record timestamped between visited/store,
but admitted after store, and a cross-thread timestamp tie both initially retained
chains. `retirement-receipt.json` preserves those failures plus a passing positive
whose lifecycle interval begins entirely after store. The reducer now applies
its partial-order lifecycle spans through the store, rather than stopping at
visited and then relying only on admission sequence. This is a conservative
ambiguity test; feasibility of that exact producer schedule is unproved. No
native hook or identity acquisition changed, and P1/P3 lifetime obligations remain.

The first two new development invocations stopped at provenance checks: native04
had no final build receipt yet, and native03 reported changed source. Their fresh
output directories remain preserved. A complete Build08 development rerun then
passed 199 checks before the retirement controls were added. These interim
results do not qualify the final combined package. Final rerun and independent
delta review remain required.

The corrected complete development suite passes 202 checks in
`.local-work/d5ab/p2-reader-review-dev04/receipt.json`, including both adverse
retirement orders and the after-store positive. The exact schema-2 B1 full-result
comparison still passes. Explicit-file editorial screening and whitespace checks
pass after manual reading of the changed prose and explanatory comments.
