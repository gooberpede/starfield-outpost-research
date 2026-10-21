# B5-A contract, checks and independent review

2026-10-21, Australia/Sydney. [Original AC1–AC8](../../implementation-briefs/CODEX_BRIEF_SOR_B5_A_local_work_inventory_scratch_lifecycle.md)
govern the original execution. The later [maintainer delivery correction](delivery-correction.md)
amends only tracked/local delivery and defers B5-B until after release. No
scientific/protection criterion was dropped and no reclamation quota added.
Publication remains **NOT CLEARED**. Independent review does not approve B5-B,
integration, staging, commit, push or external disclosure.

The initial tree contained only the supplied untracked brief. HEAD was
`1c7758c484d13aa7cb4ebddf5aee219a9bbd35b4`; index SHA-256 was
`20dca3940af5a1a5b7d2b408e9629d747eaf818f7a40f29de470b9904dfcc2a9`.
The [report](report.md) and deliverables carry the reviewed scope; local primary
receipts live in `.local-work/b5/`. Their paths/hashes are supplied with the
complete review delivery. No pre-existing ignored artifact was deleted/moved.

## Actual checks and preserved failures

- The WindowsApps `python` alias was inaccessible before Python execution.
  All successful Python commands use the explicit installed CPython 3.14.3
  executable recorded in `start.json`; no dependency installation occurred.
- Metadata scan visited 90,914 regular files and 12,951 directories without
  following reparse points; zero scan errors. Every initial file was SHA-256
  hashed. Size measurements are logical lengths, not NTFS allocated clusters.
- Twenty actual repaired scratch-block cases passed: ten normal and ten
  injected first-apply exceptions. An earlier nine-exporter pass was superseded
  after broader discovery identified `runtime/session-tools/export_review.py`.
  No existing experiment prologue or native test suite ran.
- Initial harness byte comparison failed because the test Git invocation omitted
  `core.autocrlf=false`; correcting the harness aligned its byte behavior with
  actual exporters. A subsequent missing `pathlib` synthetic binding failed
  before completing the last case; the final twenty-case pass includes it.
  Neither harness failure establishes a scientific-method defect.
- The successor's full synthetic control flow passed normal export, injected
  apply failure with retained completed patch, prior-work rejection and existing
  output preservation. Synthetic Git discovery responses isolate the test;
  real Git diff/apply verifies the patch bytes. Actual B5 delivery separately
  verifies real HEAD/index and current-tree coverage.
- Some exploratory `rg` invocations with Windows wildcard path arguments were
  rejected before searching; corrected explicit roots/`--glob` and inventoried
  file lists drive the final reference checks. Large result payload exclusions
  and dynamic-reference limits are explicit in [reference impact](reference-impact.md).
- The first exact-reference pass stopped on ripgrep's default compiled-regex
  size limit before producing a candidate manifest. A larger ASCII compilation
  allowance still caused repeated large compilations (an observed child reached
  2,270,838,784 working-set bytes). The implementer stopped only its own identified
  read-only Python query worker, PID 70464 / installed Python / start 17:43:02,
  and superseded this method with a literal-prefix trie. No scientific capture
  or game process was stopped. Its failed source version remains local.
- The final literal pass includes all 262 large text files omitted from initial
  discovery. Six synthetic separator/case/absolute/JSON format controls and two
  negative controls passed using actual matcher AST blocks. Complete final scope
  and hit receipts supersede the incomplete regex search; no absence conclusion
  was drawn from that search.
- First postflight rejected trailing whitespace in a generated local-method
  description field. Trimming that authored field before CSV serialization
  corrected it; the unchanged-input preservation checks had already passed.
- Independent review found one actual UTF-8 mojibake occurrence in this new
  document's AC1–AC8 link label. The matrix helper had decoded the earlier text
  with the Windows locale default. Explicit UTF-8 decoding and that exact label
  correction resolve it; historical documents/evidence were not normalized.

The initial independent pass returned **REWORK / incomplete submission** because
reports/manifests/protection receipts were pending. It independently checked all
18 then-current source pins and absent scratch paths, and requested successor
qualification and explicit prior-work/whitespace/link handling. Those requests
were implemented under the same brief; the final scratch scope is twenty cases.
The implementer did not treat preliminary lifecycle checks as final ACCEPT.

## Outcome dimensions

Scientific conclusions, confidence and publication classifications are unchanged.
Current exporter lifecycle qualification is synthetic; historical acquisition
pipelines, native equivalence, retail safety, target survival and live cleanup
are **NOT TESTED / NOT APPLICABLE** to this offline assignment. Preserving byte
identity is not validation of scientific semantics. Installed tools/game and
external analysis projects were not modified or executed.

Exact candidate paths, byte estimates and reference blocks remain proposals.
The B5-B plan requires fresh identity/ancestor/reparse/reference/protection and
space checks plus new explicit maintainer approval. Zero original file bytes
were reclaimed by B5-A; disposable newly created test/apply fixtures self-clean.

## Mandatory criterion matrix

| Criterion | Result | Primary evidence and limits |
|---|---|---|
| AC1 scope/protection | PASS | `start.json`, `protected-before.json`, `postflight.json`: HEAD/index unchanged; 167 selected pins rehashed; all 90,914 initial file metadata identities unchanged; four roots present. |
| AC2 meaningful accounting | PASS | `inventory.json`, all-file `hashes.json`, retention ledger/ranked IDs: 33,963,351,165 bytes, 90,914 files; top-level arithmetic checked independently by check.py; major retained consumers explicitly explained. |
| AC3 retention/recoverability | PASS | Exact candidate/recovery hashes and per-file roles; HOLD inventory and large-duplicate ledger; original saves/captures/source/failed evidence retained. Unknown exact creator invocation is disclosed. |
| AC4 reference closure | PASS | Full literal scan of 41,839 text files / 19,755,517,096 bytes, including 262 large files; exact hit rows in candidate-references.json; every hit blocks deletion. Dynamic-reference/UTF-8-text limits and current versus historical dependencies disclosed. |
| AC5 lifecycles | PASS | Ten current tracked repairs, twenty normal/exception block cases, four successor control-flow cases; source hashes and surviving receipts checked; 64 local packaging leads prospectively retired with preserved bytes and successor; 70 frozen external-creator copies retained. No historical experiment prologue/native suite executed. |
| AC6 exact proposal | PASS | 7,657 duplicate-file IDs and 29 enumerated empty trees; exact identity/recovery/reference/risk/approval fields; B5-B fails closed with both 40 GB guards/reparse/out-of-root checks. No existing deletion. |
| AC7 durable reporting | PASS | Linked reports, CSV/JSON registers, owned local-method provenance, preserved failures and no historical/scientific rewrites; whitespace/syntax/portable file-link checks in postflight.json. |
| AC8 review/delivery | PASS | Independent reviewer ACCEPT of review02: all 33 visible and 42 local input pins verified; complete/task-only payloads independently reconstructed in memory for 33/32 files and matched actual bytes; real-tree reverse checks pass. Final record/package receives affected confirmation below. |

All AC1–AC8 are PASS under the independent review02 decision below. The reviewer
independently checked all initial metadata, all selected protected hashes,
candidate/recovery hashes and reference-count/HOLD consistency. Synthetic runs
and the full reference traversal were inspected through source/primary receipts,
not independently rerun. No live or second all-workspace byte rehash is claimed.

## Delivery and exclusions

Complete/task-only patches include all current nonignored text, including the
supplied brief only in complete. Their package receipt enumerates every changed
file with SHA-256/bytes and supplies exact forward/reverse reconstruction,
path-inventory equality and reverse applicability to the actual working tree.
Ignored audit helpers/receipts are individually identified in local-methods.csv
and the local review input snapshot; private/raw/binary evidence stays local.
The physical starting tree was clean except that brief, so task-only attribution
is unambiguous. No staging was used to construct either patch.

## Historical independent final disposition

**ACCEPT**, reviewer `/root/b5_reviewer`, for fixed snapshot
`.local-work/b5/b5-review02-review-inputs.json`, SHA-256
`1929ed6dfd525f830195737cc35cb7940ede6baef669ceae2694f4c2a0cafc5d`.
The actual criterion-by-criterion return is retained verbatim at
`.local-work/b5/independent-review02.md`. Initial incomplete-submission REWORK and
the AC7 encoding correction were addressed under the same brief, without any
acceptance-criterion waiver. The reviewer authored no implementation changes.

Reviewer diagnostics are separate from implementation failures: an initial
checker used `package` instead of snapshot key `delivery`, one comparison
overlapped the authorized correction, and two label checks used the Windows
default decoding. Corrected checks against the frozen review02 snapshot passed.

The affected confirmation of this final verdict record and `b5-final` package
belongs in `.local-work/b5/independent-review-final.md`, with actual final input
and patch hashes. Final delivery is complete only with that ACCEPT confirmation;
it does not authorize integration, deletion, staging, commit, push or publication.
The final package/snapshot is `.local-work/review-deliveries/b5-final.json` and
`.local-work/b5/b5-final-review-inputs.json`. Original protection/source/scientific
inputs remain fixed through these verdict-record changes.

## Corrected delivery scope

The preceding ACCEPT and `b5-final` hashes describe the original delivery, not
the corrected publication surface. The detailed manifest is now temporary
local-only material; its unchanged hash and location are in [report](report.md).
It is absent from the proposed tracked tree and both corrected diffs. The
tracked summary retains totals/retention findings; B5-B is deferred until after
release and requires fresh review and explicit approval. Original inventory,
candidate decisions, ten exporter repairs and verification receipts are unchanged.

Corrected coverage/application receipts are
`.local-work/review-deliveries/b5-corrected.json`. The focused independent return
at `.local-work/b5/independent-review-corrected.md` binds that corrected snapshot;
delivery requires its ACCEPT. No new filesystem inventory or candidate review
was performed. Historical packages remain ignored/local and are not public
artifact promises. No staging, commit or push.
