# Offline qualification and its limits

**Historical engineering evidence, not current scientific approval.** [Reassessment](scientific-value-reassessment.md) recommends **NO-GO**. Counts and receipts below describe the earlier qualification; no test, build or corpus audit was rerun for this documentation-only correction. Reproduction recipes are preserved descriptions, not instructions to execute during this task.

[Original contract](contract.md), [review](review.md), [release](release.md).
No fixture loads SFSE or executes any retail target function. Compiler, MASM,
Python and Windows APIs run only the owned disposable programs/files.

| Check | Evidence and limit |
|---|---|
| Build identity, exact CALL bytes/signatures, dependencies, DLL-only runtime ZIP | PASS — qualification-03/build.json and identity.generated.h; thirteen sites and target entry 32-byte windows; actual dependency inventory. All 6,847 inherited pins verified before/after native qualification and package generation; separate offline operational preflight PASS_OFFLINE_PINS also completed. |
| Native producer/UI/row/mixed-float ABI, exception/unwind and failed memory reads | qualification-03/qualification.txt plus native fixture. Native return/LastError/FP state and row fast/growth channels tested synthetically; not a retail timing test. |
| Source/provider forwarding, actual parent, cached-versus-source-child, retired no-read | readiness-tests.txt and readiness-fixtures; macro-only read counter absent from production. No constructor invocation or synthetic retail query. |
| Bounded queue, concurrent worker publication, snapshot limit | 4096 accepted then overflow explicitly fails; 1,000 concurrent records stream-verify exact writer sequence; a 257-member collection fails before member traversal. Integrity bounds are not scientific session quotas. |
| Decoder | Ten inherited plus five focused Python tests pass; damaged WAL/tails, partial reads, uncertain resource IDs, mismatched phase, ordered source/pointer/duplicate signatures, retained versus changed populations, actual parent and failure records. No independent native geometry pairs. |
| Synthetic patch admission/rollback | patch-qualification.txt: quiescence refusal, all-preimage refusal before writes, injected second-write failure restores first patch, all-edit installation/restore and rel32 bounds. Does not guarantee recovery from arbitrary OS corruption. |
| Real worker in disposable executable | normal nonce/ACK/STOP, in-flight STOP, before-READY STOP, guard failure, writer failure, disk-query failure and terminal-writer failure. Active scopes drain; resident patches retained; error/emergency receipts preserve failure. |
| Shared infrastructure | checks-01/session.txt: 55 tests pass, including 0.8.0 version isolation and receipt selection plus existing ACK/STOP, phase separation, full/light audits and archive full-member/hash/corruption/writer-failure controls. Process/deployment contacts mocked; no live controls run. |
| Existing evaluator | checks-01/availability.txt: 45 PASS; spatial.txt: 12 PASS. Tests qualify transcriptions and unknown categories, not new native equivalence. |
| Primary sources | checks-01/qualification.json: 26 existing native-export hashes verify against both pinned source ledgers; installed executable/SFSE and all guarded sites checked by build. No analysis DB changes or new exports. |
| Actual 0.7.0 reference replay | reference-070/coverage.json: 611,926 records, 35,574 evaluations, 11,128 distinct descriptors, 346 exact ordered UI folds. Region operands still missing; spatial oracle comparisons: 0. |
| Save-menu selection | save-menu.json freshly regenerated from controlled original metadata at UTC+11; Save3 date/time/location/level matches retained control. No menu/game opened and no save changed. |
| Protected content and Git | PASS — build checks 6,847 inherited protected pins before/after; subsequent offline-preflight.json and operational-results.json confirm all seven operational checks. Source manifest and unchanged HEAD/index verified by build/export checks. No staging or commits. |

All receipt paths above are relative to ignored `.local-work/local-readiness/`,
with build paths under `builds/qualification-03/`. Earlier failed qualification-01
and qualification-02 remain as described in review.md; successful later checks do not rewrite
them. Original raw captures, saves, fixture WALs, DLL/ZIP and full local path/
hash manifests are excluded from Git/review patch payloads.

Reproduction: run `runtime/local-readiness-080/build.py --name FRESH` with the
installed CPython path from its README, then
`research/local-readiness/qualify.py --out FRESH-IGNORED-RECEIPT-DIRECTORY`.
The existing owned Milestone B coverage command in its validation document
replays the 0.7.0 reference. Each recipe documents reads/writes and does no downloads,
deployment, native target invocation, save/database/Git mutation or network I/O.
Both-drive caller-available 40,000,000,000-byte guard stays fail-closed.
