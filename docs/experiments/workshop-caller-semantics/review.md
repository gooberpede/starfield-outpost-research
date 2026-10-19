# Acceptance and independent review package

2026-10-13, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039 continuation.
[Original frozen brief](../../implementation-briefs/CODEX_BRIEF_SOR_workshop_center_caller_semantics_idle_camera.md),
[report](report.md), [native ledger](native-ledger.md), [chronology](chronology.md),
[state/acquisition](state-and-acquisition.md), [source hashes](sources.csv).

Scientific outcome: **B, independently ACCEPTED**, evidence-bound result; full native XYZ
equivalence NOT TESTED. Engineering: offline decoding and timing checks pass.
Target outcome: NOT APPLICABLE, no target execution. Authority: offline only;
no observer implementation/build/deployment, game/process/save/configuration or
Git mutation. Authored work REVIEW-REQUIRED; raw/native/private inputs LOCAL-ONLY.

| Mandatory original deliverable | Status | Exact evidence and limit |
|---|---|---|
| Scientific report and fair alternative hypotheses | PASS for B | report.md and state-and-acquisition.md; helper arithmetic/selection established, historical producer and idle-camera activation unknown |
| Native caller/dependency ledger | PASS for B | native-ledger.md; six fresh read-only native exports, eleven descriptor callers, actual camera dependencies and indexed contract; two instruction caps disclosed with complete decompilation |
| Cross-session chronology/frequency and idle-camera test | PASS | chronology-02/events.csv, bins.csv, summary.json; chronology.md and frequency.csv. Raw journal checked; no 060 UTC calibration or input-idle trace invented |
| Matched-state and observer interference | PASS for B | Fresh replay-01/ledger.json and summary.json; state-and-acquisition.md; four pairs quarantined, sampling/timing/semantic effects separated |
| Decision-ready smallest next acquisition | PASS, proposal only | state-and-acquisition.md; same-trigger AD0C36 identity/frame plus producing edge/vector; not another broad descriptor run |
| Tests, input protection, specialist/reviewer and provenance | PASS |16 adverse/timing controls; 23 frozen regressions; 81 sealed files/61 source pins and saves replayed; 203 source ledger pins; independent decision below |
| Complete/task-only patches, manifests/status and verification | PASS | Local package.json and named diffs below include supplied brief and untracked text; 19 complete/18 task paths forward-applied and compared exactly |
| Independent original-contract/evidence review | PASS | /root/independent_review ACCEPT of frozen outcome-B candidate; actual return and final snapshot confirmation retained locally |

## Actual checks and their limits

Local receipt root: `.local-work/workshop-caller-semantics/`.

- `replay-01/`: actual 1,194/562,326 record hashes/extent/pair validation;
  saved 25/26 archived and decompressed hashes, independent selected offsets,
  original 81 sealed files and 61 observer build-source pins plus executable.
- `chronology-02/`: all center metadata, per-thread and pooled interval/bracket
  distributions, five-second bins, action/ACK receipt hashes and counts. The new
  timing tool imports the pinned independent cross-session decoder; it is not
  represented as a separately written parser.
- `workshop-caller-semantics-tests.txt`, `cross-session-center-tests.txt`:
  actual 4 timing controls and 12 retained schema/identity/frame/ancestry controls.
- `frozen-01/`: actual 23 frozen model regressions PASS, with protected hashes;
  zero new native oracles, native equivalence NOT TESTED. Save/ESM/raw inputs
  are read-only; the earlier 6563 postflight receipt is historical, not a newly
  repeated 6563-file audit. Current checks are explicitly scoped above.
- `determinism.json`: independently executed chronology-02/03 event CSV and bins
  byte-identical; summary identical excluding changing disk readings. Specialist
  before/after inventories independently show all 15 analysis-project files
  unchanged. Native source was exported read-only/no-analysis, with no symbols,
  types or comments edited. Two 600-instruction export caps are disclosed in the
  native ledger; decisive claims use included instructions and full decompilation.
- `package.json`, `status.txt`: final changed-file manifest, HEAD/index hashes,
  exclusions, link/whitespace checks, complete/task-only patch inventories and
  exact forward application into disposable plain .local-work/review-patches trees.

The supplied brief was the only pre-existing untracked file; no prior tracked
edits existed. It remains byte-identical, included complete and excluded task-only.
Exports are `.local-work/diffs/workshop-caller-semantics-complete.diff` and
`.local-work/diffs/workshop-caller-semantics-task-only.diff`. Raw saves, memory,
native disassembly/decompilation, binaries, databases and private receipts remain
excluded/local, with hashes and locations disclosed. No staging is used to export.
These checks establish artifact integrity and stated numeric observations; they
do not prove native semantics, lifetime completeness or behavioral noninterference.

## Specialist contribution

The separate specialist independently traced shared descriptor membership,
collision and border ancestry, challenged the camera inference, and reread the
indexed frame contract. That contract was already recorded in EXP0023/24 and is
credited as independent verification, not new discovery. Fresh dependency exports
and the detailed contribution/boundary are in native-ledger.md. The primary owns
chronology, saved/native reconciliation, deterministic checks and synthesis.

## Independent decision

**ACCEPT**, reviewer `/root/independent_review`, against candidate manifest
SHA256 `df2cd551c94014e1ac762d4f414b5a47a33f1c5db0b3d091459babda194bcda7`.
Candidate complete patch SHA256
`bd43d8a8084eee3c3e1d88d18f2717b46ccca77ecedaa5802d410a9a9ff65f2f`;
task-only `50d2b5dc5c4e97c3786bc99a44008b6c3ae7aa8925e2b962e34c69fe88f6cc42`.
The actual return is preserved in local `independent-review.txt`.

Reviewer independently decoded raw structs without importing the decoder,
reproduced counts/fields/timing, executed fresh full verifier and chronology
replays, ran 16 controls, rehashed 203 source pins, checked native instructions and
all 19 manifest files, and checked patch path inventories/hashes/exact replay
bytes and Git whitespace. Initial reviewer patch inspection failed on Windows
default text encoding; explicit UTF-8 resolved that diagnostic without changing
the candidate. No scientific or engineering REWORK was requested.

Reviewer did not rerun native fixtures, Ghidra exports or the 23-case model
regression; those execution receipts were inspected, with frozen input/model
hashes independently verified. Historical producer/lifetime, actual idle-camera
activation and full native XYZ equivalence remain unresolved. Post-candidate
changes only insert this verdict/status and the report/research-state ACCEPT
labels; regenerated final patches receive administrative snapshot confirmation.
Acceptance supplies no integration, publication or live authority.
