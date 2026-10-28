# D5M Phase B: incomplete acquisition and repeated breakpoint exit

2026-10-28, Australia/Sydney. [Authorization and execution contract](d5m-phase-b-authorization.md),
[accepted card](run-card-d5m-v1.md), [post-mortem](d5m-phase-b-postmortem.md),
[source and receipt ledger](d5m-phase-b-sources.csv).

**The approved process armed successfully, retained 493 verified receipts and
then exited during reported fast-travel. No selected-source decision or complete
construction–retention–reuse chain was captured. Full protected-input postflight
passed. Further retail use of this observer is NO-GO pending engineering work.**

| Dimension | Scoped result |
|---|---|
| Question | Can the repaired observer witness construction, retained geometry and later reuse for the selected second Feynman V source? |
| Answer | Not established. The process faulted at the armed Grid-clear breakpoint before reported arrival. |
| Confidence/basis | PROVEN / RUNTIME for persisted events, receipt correspondence, recorded API results and matching dump state; STRONG observer-associated breakpoint failure. Initiating delivery mechanism UNKNOWN. |
| Coverage | One ordinary-user process; verified pre-load barrier, operator-reported Save52 load and travel initiation. No completed target visit or qualified negative construction result. |
| Completeness | All 493 receipts/ACKs bind to the 680-row journal; terminal GAP remains. Preserved-byte completeness does not imply complete scientific acquisition. |
| Publication | Raw capture, dump, Windows records and archive LOCAL-ONLY. Authored synthesis/code REVIEW-REQUIRED. B6/publication remain on hold. |

## Admission and operator sequence

The current task started with a clean tree at HEAD
`84ff4f758a2cd45496512d21a084c0b90df4ab8d`, index SHA-256
`534ac32c1270b7209525893c5738785cc128756a8d44f283e7d4eec5fa28dac5`.
The maintainer approved the accepted card, confirmed Steam Cloud disabled and
made unchanged-content Plugins.txt timestamps diagnostic. Those instructions
are preserved verbatim in the authorization record; historical Phase A and D5L
records retain their original wording.

Fresh full preflight authenticated the active archive/index and surviving inputs,
all 98 protected save names with independent backups, scratch Save52 restoration,
installed definitions/configuration and pinned EXE/ESM/PlanetData. Both drive
floors passed. Historical excluded ZIP failures remain historical; no obsolete
loose-payload audit or baseline repair was performed.

The accepted build13 manifest SHA-256 remains
`6b82b0c27d860af0e130d3100a4c484183f061f0b266f7885eff0af72f9c91ea`;
all 51 pins match. The exact card is
`49d724a3d2227bd4c88873bb451760eb41bd7a20acd0e78ea58a45c16a4ef7ed`.
The unchanged 42-case final07 qualification supplied readiness, not proof of
retail reliability. No native/controller/collector code changed for this run.

One normal Steam launch used installed app ID 1716740. PID 11600 has creation
FILETIME `134376320324677621`; caller and target were `TYPHON\User`, unelevated,
Windows session 1. Python and native admission both enforced account/lifetime
identity. There was no sandbox attachment attempt or privilege/security change.

Steam and game window capture timed out, including one recovery attempt for
each. No automated menu/gameplay input followed. The operator confirmed the
main menu with no save loaded, then performed gameplay. Window activation does
not establish menu/loading state; the state/action statements here are operator
reports, not screenshot observations.

Normal launch changed only Plugins.txt's mtime. Its 480-byte contents and SHA-256
`8dac50493405250ab92feea55701a1ecb6fdf333703d9c152042262e5c26db33`
remained identical. The accepted helper retained the original preflight and
chronology and produced one narrow derivative. Independent review accepted the
exact original/derivative hashes before admission. This implemented the user's
timestamp amendment without aborting, rewriting configuration or widening guards.

| UTC observation/record | Event and evidence boundary |
|---|---|
| 03:33:56 | Ordinary-user identity receipt records PID 11600 and exact creation time. |
| 03:35:33 | Main-menu confirmation recorded; Plugins.txt content identity checked. |
| 03:38:40 | Independent barrier verification: fourteen sites, 89 known threads, SRO1/ACK/READY/admission bound before load instruction. |
| 03:42 onward | Operator first reported loading/travelling. Exact input and transition times are UNKNOWN. |
| 03:43:18 | Report recorded: “Save52 loaded. About to fast-travel to Feynman V outpost 2”. |
| 03:43:36.772 | Matching Application Error record identifies the breakpoint fault. |
| 03:44:16 | Independent process query finds no Starfield process; 493 receipts/ACKs remain. |

The operator subsequently reported exit after fast-travel initiation. No arrival,
save write, Build Mode, reset, forced generation or alternate target was reported
or requested. Monitoring used only process lifetime, file metadata, disk guards
and at most 64 KiB of control tail. Full reduction/audits ran after exit. There
was no explicit STOP, elapsed-time cutoff, evidence quota, automatic retry or
second game process. A pre-READY verification attempt merely found the receipt
not yet present; the later successful independent barrier check preceded load.

## Evidence and separate outcomes

| Retained observation | Count/result |
|---|---:|
| Barrier / native samples | 1 / 492 |
| Reset / completed Grid init / source init / Grid clear | 1 / 55 / 383 / 53 |
| Selected-source decisions / complete chains | 0 / 0 |
| Control rows / received debug events | 142,604 / 1,330 |
| Matched continuation intent/results | 1,330; all recorded calls succeeded |
| Registered-handle closes / final owners | 254 / zero |
| Target exit | Unexpected `0x80000003`, with GAP |
| Controller exit / requested STOP | 0 / false |

The controller's zero return describes its event-loop cleanup, not a successful
target session. The [post-mortem](d5m-phase-b-postmortem.md) preserves the one
handled suspend error and the missing fault-thread exception delivery. No claim
that every API operation succeeded is made.

Full postflight and protected-input comparison pass: local/remote protected
saves, independent backups, installed identities, definitions, configuration
contents, archive guards and original restoration hash match. Plugins.txt's
mtime is diagnostic under the explicit amendment; all configuration contents
match. Steam synchronization metadata remains separately diagnostic. HEAD/index
are unchanged. The game is gone; no manual restoration or cleanup of protected
inputs was performed.

The lossless archive contains all 1,024 inventoried capture/companion members,
including a verified copy of the existing matching dump. Raw originals remain.
Source bytes total 205,275,368; archive size is 55,666,435 bytes. Archive SHA-256:
`5c16414e89c9550c99a7c4b2eae808738c8b1fe24aafab8aa2db317cf6ada586`.
Its classification is PARTIAL because acquisition failed; every archived byte
still passes streaming inventory/size/CRC/SHA verification. Archival checks found
C: 75,055,333,376 and D: 87,139,569,664 free bytes, both above 40,000,000,000.

## Execution contract and review

| Criterion | Reviewed execution-record assessment |
|---|---|
| B1 authority/admission | PASS: explicit approval, fresh preflight, ordinary identity, exact derivative review, one-use admission and verified pre-load barrier. |
| B2 bounded execution | PASS for scope compliance; scientific acquisition and retail instrumentation FAILED. The one process exited unexpectedly; no retry followed. |
| B3 evidence/science | PASS for faithful evidence/reporting: all receipts decoded, uncertainty and terminal GAP retained; scientific answer remains incomplete. |
| B4 protection/cleanup | PASS: full protected comparison, process absence, disk floors and verified lossless archive with originals retained. |
| B5 review/delivery | PASS with final closure gate: both independent reviews ACCEPT the failed-execution record; delivery requires accepted closure deltas and matching final hashes. |

The maintainer added the following instruction after the target exited:

> Thank you. Please complete a post-mortem after postflight. Use the ordinary user to access crash dumps and Windows error logs if required.

Full postflight preceded completion of the post-mortem. Only existing crash
artifacts and Windows logs were read under that authority; no dump was requested,
security setting changed or live retry performed.

Independent engineering and scientific reviewers both ACCEPT `review02`, whose
complete/task-only patch SHA-256 is
`31bd4dcb1f3191c929c08ac5b5ba7a71ba6dc20b1506dd96f961097ffb3c948d`.
Both independently decoded all 493 receipts/ACKs, reproduced the reduction and
forensic summary, and verified every inventoried archive member against retained
originals. Full protected-input audits and exact forward/reverse application
results remain supplied primary records; engineering also performed independent
read-only patch application checks. Actual criterion matrices and editorial
dispositions are retained as `engineering-final-review.md` and
`scientific-final-review.md` under `.local-work/d5m-phase-b/`.

Only this closure text and the research-state acceptance sentence change after
that snapshot. Final delivery requires both `engineering-closure-review.md` and
`scientific-closure-review.md` to ACCEPT the delta and an external
`final-delivery.json` binding final file/patch/manifests/exclusion/review hashes.
The independent acceptance concerns this failed-execution account; retail
instrumentation remains REWORK/NO-GO and acquisition remains incomplete.

The scientific capture is incomplete and the observer requires engineering REWORK
before further retail use. Acceptance of this execution record is distinct from
acceptance of the instrument for another run. Final reviewer returns, editorial
inventory, exact patches, exclusions and hashes are retained under
`.local-work/d5m-phase-b/`. No staging, commit, push, integration or publication
is authorized or performed.
