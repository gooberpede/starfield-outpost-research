# Live-experiment infrastructure consolidation

**COMPLETE — PASS (offline engineering); critical review pending.**
2026-10-15, Australia/Sydney. This single-agent assignment follows the
[authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_live_experiment_infrastructure_consolidation.md).
The explicit no-sub-agent exception replaces routine independent-agent review;
the maintainer and ChatGPT review this package. No self-summary grants integration.

The reusable commands are `runtime/session-tools/session.py`:
`prelaunch`, `reuse-full`, `request`, `live`, `stop`, `postflight`; and
`runtime/session-tools/archive.py`: `seal`, `create`, `verify`.
The [tool instructions](../../../runtime/session-tools/README.md) specify inputs,
effects, dependencies, incident states, archive contract and retention proposal.
The [future run-card fragment](future-run-card.md) supplies the exact phase and
operator handoff sequence. Only the 070 adapter is qualified; live adoption is
**NOT TESTED**. Milestone B scientific reconstruction has not started.

## Audit and reuse decisions

The source baseline is project HEAD
`0d443482f82c8f1a3750461c6bfec96bd0a6e56e`. All following repository paths are
maintainer-owned internal provenance under SOR-P-0002. Exact existing pins and
qualification receipts remain in `.local-work/session-tools/qualification-01/`;
the review package hashes all new authored files. No outside implementation,
new dependency, licence basis, contact or disclosure was introduced.

| Existing implementation | Duplicated or useful behavior | Shared disposition / version-specific remainder |
|---|---|---|
| `runtime/native-oracle-050/operate.py` | Full file/module/save preflight; process-name/PID metadata; cooperative challenge, health and STOP; DLL-only effective deployment. | Directly reuse `processes()` in the new adapter. The old challenge publication, inventory/health schema and session root remain 050-specific. |
| `runtime/native-oracle-060/operate.py` | Full manifest/protected/runtime audit precedes routine request/status/postflight/seal; PID/creation query; admission/site guards; preallocated STOP. | Compare with 070, retain historical code. Its schema6 decoder and native guards stay local to 060. No claim that the new 070 adapter operates 060. |
| `runtime/beacon-resource-070/operate.py` | Nearly identical 060 lifecycle, adding operational-source pins and schema7 identity. Routine request/status reruns full pins. | Directly call `manifest`, `audit_deployed`, `session_path`, `session_identity`, `admission`, `process_state`, `stop_control`, and existing decoder through `adapter070.py`. Full manifest only in offline phases. |
| `runtime/beacon-resource-070/watch.py` | Lightweight own-session/disk/process health suffix; distinguishes partial current health line and delay. | Conceptually reuse its bounded suffix read in the adapter, adding strict latest-complete-line parsing, worker identity and request-bound ACK. Historical watcher unchanged. |
| `.local-work/continuous-beacon-preview/run-20261014T233433728771Z/prelaunch-audit.py` and `post-exit-audit.py` | Run-local loader/PE-guard/save inventory and ExitSave comparison fill gaps in the general helpers. Earlier 050/060 cards also repeat save hashing and sealing snippets. | Consolidate save content/mtime inventory, loader extra pins and ExitSave/metadata distinctions into shared commands. Whole game SHA establishes the reviewed disk image; runtime instruction/relay checks remain native. Do not copy private run receipts into Git. |
| `runtime/beacon-resource-070/inspect_resources.py`, `runtime/native-oracle-060/inspect_history.py`, `runtime/native-oracle-050/inspect_capture.py` | Transport completeness, native schemas, semantic analyses. | Keep version-specific. Shared 070 postflight consumes a compact decoder result, omitting large evaluation/UI arrays. No native decoder or DLL changes. |
| `save-analysis/scripts/save_menu.py` and `docs/experiments/save-menu-identification.md` | Header/original-mtime identity and concise character/date/time load instruction. | Reuse unchanged before launch. Deliver label once; only material ambiguity prompts another targeted check. No new save parser. |
| 050/060/070 run cards and existing seal receipts | Actual lifecycle, protected pins, disk guards, failure/retirement evidence, manifests. | Read as provenance and preserve historical verdicts. A new prospective fragment calls the shared interface. Original cards/seals remain unchanged. |

The new prelaunch receipt contains the full checked source inventory and hashes,
game/SFSE/runtime/build identity, explicit loader/tool pins, save inventory and
existing-session names. Reuse binds the manifest and shared tools. Effective DLL
and installed SFSE checks require actual runtime payload only; optional deployed
README/notices/manifests are not dependencies. Vortex's database is not edited or
treated as proof of effective deployment. Configured alternate removal paths can
cover an actual Vortex notice path without inventing required sidecar files.

Lightweight live operations read the pinned prelaunch receipt, shared tools and
small build manifest, deployed DLL/SFSE, own session identity/admission/READY,
fresh request's ACK and a 64 KiB health suffix. They neither hash protected
corpora nor decode raw event history. PID/creation metadata is observational;
native worker admission and ongoing guard verification remain the established
070 semantics. A nonce is fresh for its new request, not indefinitely fresh:
issue a new challenge at each meaningful phase and compare health progress.

The durable classifications distinguish waiting, STOP pending, clean retirement,
retirement error, worker failure, check error and partial postflight. Noncritical
delay calls for an update and continuation, with no new time/count/volume quota.
Actual integrity/identity/instruction/disk/worker failures and explicit STOP retain
their stops. Both C:/D: caller-available space must exceed 40 billion bytes;
unavailable queries fail closed. STOP retains the preallocated emergency path.

## Historical evidence archival audit

The metadata audit at `.local-work/session-tools/historical-audit-02/` inspects
five scopes: 050 build packages, shared 020–050 live sessions, 050 run receipts,
060 and 070 trees. It finds 14 ZIPs; their central-directory inventories contain
no `events.bin` or `records.jsonl` members. These are existing packages, not
verified compressed raw-session archives. No `.7z`, `.zst` or `.gz` evidence
archive was found in those scopes. This is a bounded inventory, not a search of
every disk directory or a round-trip validation of historical packages.

Metadata raw/fixture totals are 8,335,663 bytes in 050 builds, 38,561,772 in shared
020–050 sessions, 2,394,675,639 in the 060 tree and 3,660,496,622 in the 070 tree.
These include fixtures and repeated builds, and are not scientific capture totals.
The actual 070 session separately has 2,036,489,728-byte events and 79,105,401-byte
journal. Its run also retains a 107,380,337-byte decoded postflight and
112,124,180-byte console output: substantial derived repetition, not byte-identical
raw copies. Compact new postflight summaries avoid generating that duplication.

Within 648 audited raw/journal pin entries, 62 repeated hash groups include empty
files and repeated fixtures. No nonempty equal-hash group joins two retained live
session paths in that pin inventory. Detailed groups stay in the private audit
receipt. This neither proves that all historical evidence is unique nor authorizes
deduplication. **No existing capture was archived, moved, deleted or modified.**

## Qualification and measured costs

Local receipts: `.local-work/session-tools/qualification-01/{summary.json,tests.txt,protected-before.json,protected-after.json,archive-receipt.json,verify-receipt.json,negative-receipts.json}`.
The initial full historical audit was expanded with the metadata-only command
to include 050 build/shared live roots and inspect ZIP inventories; that corrected
coverage is retained separately in `historical-audit-02`, without repeating the
large byte audits. Final focused tests are recorded in the review package.

| Mandatory criterion | Result and actual evidence |
|---|---|
| Prelaunch receipt creation/full reuse, changed/missing/mismatched pins | PASS: disposable receipt creation/reuse and missing/changed input refusal; receipt and manifest/tool identity checks. Actual reviewed existing full checker also passed offline. |
| Full versus lightweight phase distinction | PASS: trap test rejects any full audit or corpus inventory in `live`; a synthetic protected input is removed and lightweight operation still reads only its defined scope. Unseen protected drift is detected by full postflight, not falsely certified during live. |
| READY/admission/fresh ACK versus stale/mismatched ACK | PASS: real 070 admission receipt checker with disposable site/preimage data; wrong identity/nonce, unrelated prior ACK and absent READY/ACK controls. No real process contact. |
| STOP/retirement/worker/incomplete evidence distinction | PASS: preallocated STOP below failed disk query, invalid flag, pending STOP, retired count mismatch, clean retirement, worker failure and partial decoder result. |
| Disk failure/unavailable queries and temporary-space planning | PASS: both-drive low-space controls, query exception, reservation failure. Actual qualification had caller-available C: 93,507,452,928 / D: 118,020,857,856 bytes at archival admission. |
| ExitSave rotation versus originals/new saves/metadata | PASS: expected prefix rotations separated from original content changes, unexpected new save and same-byte mtime changes. No restore/write to originals. |
| Lossless binary/path inventory round trip | PASS: actual disposable CLI seal/create/verify; every member size/CRC/hash verified. Synthetic binary all-byte fixture also passes. |
| Corrupt/missing/truncated/duplicate/malicious paths and generation errors | PASS: 51 final focused controls include same-length wrong bytes, CRC corruption, missing member/source, truncation, case collision, traversal/Windows paths, symlink member and injected writer failure; original disposable raw hashes preserved. Durable expected-refusal receipts retained. |
| Partial capture classification | PASS: missing retirement/incomplete decoder yields partial postflight; incomplete seal requires an explicit reason; ZIP verification preserves PARTIAL. No raw tail repair. |
| Original/approved input preservation | PASS: 6,895 pinned entries, 9,989,677,927 summed bytes, zero mismatches before and after. Includes 6,847 existing protected pins, approved sources/runtime/DLL/package, original seal and all sealed 070 raw members. No new native build/fixture suite. |
| Review package and scope | PASS: complete/task-only patches include untracked text, exact path/content inventories, forward/reverse checks and exclusions. Single agent, no launch/deployment/process contact, staging/commit/push or Milestone B. |

The initial 43 focused tests took 0.853 s in the main qualification and 0.817 s
in a subsequent run. Seven added boundary/integration controls passed as a
50-test suite in 1.149 s. Final self-review added rejection of absent/malformed
worker integrity fields rather than accepting missing values as false; the final
suite has 51 tests and review receipts carry its final invocation. The
existing full manifest checker took **79.85 s**. Expanded before/after pin audits
took **100.18 / 100.98 s**. These are measured offline content costs, not projected
live latency. Lightweight checks perform **zero protected-corpus hashes** by
contract and trap test; real process/deployment latency remains NOT TESTED.

The representative disposable sample contains 16 MiB of actual 070 event prefix,
4 MiB of journal prefix, its 663,226-byte health file and two companion metadata
files. These deliberately incomplete copied prefixes are qualification derivatives,
not a production session or semantic replay. The seal and archive are `PARTIAL`.

| Measurement | Actual disposable result |
|---|---:|
| Original member bytes | 21,636,455 |
| ZIP bytes | 1,742,542 |
| Remaining size | 8.05% (about 12.42:1) |
| Source-check time | 0.0495 s |
| Compression time | 0.1067 s |
| Verification plus source-recheck time | 0.1231 s |
| Total operation | 0.2793 s |
| Temporary reservation above floor | 38,651,938 bytes on D:; no full extraction |
| ZIP SHA256 | `6c7a807a80f7fbc8c2f79b76e5af05b9e68debe696065074c3ccc88162327a53` |

Standard-library ZIP Deflate level 6/ZIP64 is available on the actual machine
and adequate here. No zstd dependency was sought or installed; maximum compression
is not an acceptance criterion. Ratios/timings of this prefix sample do not predict
whole-session compressibility or cold-disk performance. Keep both copies at first
adoption. The documented later retention proposal is reversible quarantine after
maintainer authorization, never automatic deletion.

## Review boundary and limits

Review files are `.local-work/diffs/session-infrastructure-task-only.diff` and
`.local-work/diffs/session-infrastructure-complete.diff`; the accompanying package
manifest and status are in `.local-work/session-tools/review-01/`. Task-only
excludes the supplied unchanged brief; complete includes it. Private raw/ZIP
qualification samples, native evidence, original saves/archives, DLLs and other
ignored bulk artifacts are excluded and identified with local hash receipts.

The 070 adapter is tested against synthetic lifecycle receipts and the actual
read-only full checker; no new runtime compatibility, scientific semantics or
native hook validation is claimed. Future observers retain their own guards,
schemas, analyses, authorized gameplay and exit policy. The large native fixture
suites were not rerun because no native/schema implementation changed. No original
verification receipt was modified. Authored code/reports are REVIEW-REQUIRED;
private captures/receipts remain LOCAL-ONLY. Scientific evidence state and prior
milestones/verdicts are unchanged. No permission issue or independent resource
blocker remains; maintainer/ChatGPT critical review and separately authorized
future live adoption remain required.
