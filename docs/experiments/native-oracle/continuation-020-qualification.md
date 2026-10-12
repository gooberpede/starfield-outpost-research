# Native-oracle 0.2.0 offline qualification

2026-10-12. SOR-EXP-0031 / SOR-EV-0039. Final candidate **final-review-04**:
**520 native assertions PASS; 30 Python tests PASS**. Actual production
worker-health helper nonce ACK measured **203ms**, below the15,000ms deadline.
These are disposable engineering/diagnostic results, not Starfield observations.

Primary local evidence: `D:/Projects/starfield-outpost-research/.local-work/native-oracle-020/builds/final-review-04` contains build.json, identity.generated.h,
assemble/plugin/tests command files and complete logs, qualification.txt,
inspection-tests.txt, original fixture raw cases, production-health helper output,
DLL/ZIP and exact package members. ZIP SHA256 `6dfb89713c4d8aedd072170ffdc2b8436509ce634eb037275ef6e78a52a6b0b9`;
DLL SHA256 `00fa1c2d42871a0ba096d49d235f88917f025f9b0f97ec24a7a246c056744201`. Sources and compiler/assembler/linker hashes,
game/SFSE identities,11 guard windows, six protected pins before/after and ZIP
member CRC/uniqueness/exact-byte checks are retained in build.json and release lock.
No download, game/SFSE launch, attachment, deployment or save/config change.

## Acceptance matrix

| Dimension / mandatory criterion | Result and actual evidence | Limit |
|---|---|---|
| Native ABI/forwarding | PASS: real original MASM full-CALL wrappers and vtable dispatch; full EAX Q/E and uint64 C returns; eight GPR/ten XMM sentinels, FP/LastError, C++/SEH propagation. | Modeled observed ABI, not full engine scheduling/game execution. |
| Admission/patch transaction | PASS: nonquiescent and wrong-preimage refusals before writes; six-edit installation, rel32/RX islands, exact installed checks; production relay target/RX drift rejection; actual mid-transaction protection failure, earlier-byte/protection restoration and conservative dirty state. | Actual SFSE accepted-overlay sole-thread admission NOT TESTED. |
| Nested/concurrent identity | PASS: TLS nesting, rejected nesting suppression, four callback producers, non-torn MPSC publication, overflow/loss stop. | Arbitrary game interleavings not exhaustively proved. |
| Diagnostic matrix | PASS: case-0.bin Q0; case-10.bin Q/E0; case-11.bin E/C0; case-12.bin C/grid0; case-positive.bin Q/E/C/center/pre/grid/normal chain. | Explicitly synthetic; no natural positive control claimed. |
| Negative protection | PASS: missing/zero ancestry, missing center/pre/result, abnormal/missing end, wrong order, duplicate sequence, corrupted/truncated records, journal/raw tails. | Partial originals retained; no semantic branch guessed. |
| Independent health/control | PASS: production Health.poll/append durable no-event ACK, one-time nonce, tick success/failure wiring, stale admission closure, writer failure, actual control during sustained backlog. | Whole plugin SFSE worker/lifecycle is source-reviewed; helper fixture is not a game run or full worker host. |
| Operator validation | PASS: atomic nonce publication interleaving, low-disk STOP, stale/wrong/duplicate ACK, wrong identity/loss/depth/timeouts/stopping, recovered QPC stall, counter regression, final entered/journal contradiction. |15s chosen operational deadline; no power-loss durability claim. |
| Retirement/evidence | PASS: stop during in-flight native call, drain/inert forwarding, actual append/flush/hash, final inspector counts/offset/queue/clock validation. | Stuck call/crash/disk failure may prevent terminal receipt; no live hot-unhook. |
| Conditional native replay | PASS: exact synthetic math equality and deliberately mismatching grid; unsupported rounding/subnormal/overflow remain unassessed. | Saved-to-loaded frame reconciliation/full equivalence NOT TESTED. |
| Packaging/provenance | PASS: build source-before/after equality including prepare.py, pinned installed tools, five exact ZIP members and approved notices. | Candidate remains local/review-required; deployment/removal NOT TESTED in this continuation. |
| Scope/preservation | PASS: separate preservation receipt and review exporter, no Git mutation/target operation. | Hashes prove bytes, not semantics. |

## Retained iterations and review-driven rework

All original0.1.0 builds/failures and live attempt01 remain intact. New020 builds
qualification-01/02 and final-review-01/02/03 remain separate superseded candidates;
none is the deployment package. New fixtures retained each negative case instead
of replacing the observed game zero-event journal.

Early review required same-assignment fixes: durable-heartbeat admission wiring;
atomic nonce publication; STOP availability below disk floor; orphan and incomplete
grid-negative rejection; final entered/journal reconciliation; recovered-stall and
counter-regression rejection; direct prepare.py source pin; honest optional module
hash_status; explicit relay provenance/guards and retained CALL-window checks; actual mid-transaction rollback adverse fixture and finite30s operator retirement deadline.
Qualification-02 passed510/27; final-review-01 passed510/28; final-review-02
passed511/30; final-review-03 passed513/30; final-review-04 passed520/30. Earlier successful tests do not
qualify later source edits; this final build pins the current runtime source.

Native and Python fixtures are original project code executing only inside a
fresh disposable process and ignored directories. Disposable patch restoration is
permitted for that quiescent process; it is never a claim of safe live teardown.
Normal overlays are accepted policy, with concrete site/identity checks; actual
compatibility, natural trigger reachability, ordinary reference identity and selected
terrain-frame reconciliation await the approved live card. No scientific confidence,
frozen23 corpus, equivalence or publication eligibility is promoted by these passes.
