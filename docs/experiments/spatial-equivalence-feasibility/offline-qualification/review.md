# Offline qualification review package

[Original brief](../../../implementation-briefs/CODEX_BRIEF_SOR_experiment_A_internal_observation_offline_qualification.md),
[report/matrix](report.md), [technical contract](contract.md),
[scientific decision](decision.md), [replay commands](../../../../research/internal-observation-qualification/README.md).
Recommendation: scoped synthetic **PASS**, independently **ACCEPTED**.
No integration, staging, commit, push, observer build or live authorization.

## Mandatory deliverables

| Original requirement | Evidence / current result |
|---|---|
| G1–G3 and honest recommendation | Report gives scoped synthetic PASS, retained full-x87 FAIL and retail/native NOT TESTED. |
| Native contract, harness, fixtures, records and replay | Contract + original native/build/capture/decoder/static-check sources; pinned executable/export checks; local build/decoder receipts. |
| Consequential scientific decision | decision.md retains zero native pairs and separate future implementation/live gates. |
| Independent critical review and corrections | Two preliminary REWORK passes; formal ACCEPT and reporting-delta confirmation below. |
| Provenance and protected-input verification | 132 selected baseline pins; package receipt rechecks exact bytes, HEAD and index; no full save/database audit claimed. |
| Both complete and task-only review patches | Local patch paths, inventories, checks and SHA256s in package.json; source/docs included, binaries/raw material excluded. |
| Prose/link/whitespace audit and commit suggestion | package.py plus manual review of task Markdown; final disposition below. No Git mutation. |

## Independent objections and response

One fresh-context, read-only reviewer was explicitly authorized by the brief.
The first pass returned **REWORK**: generic uses did not identify real consumed
sites, verdicts came from authored booleans, the pending record supplied its own
expected terminal token, duplicate/late/after-close terminal/use operations could
remain complete, mutation/lifetime/STOP tests were weak and MXCSR was invented.
The reviewer also challenged identical SIMD patterns and the x87 classification.

Corrections add a native finite fixed-quad arithmetic fixture consuming actual
recorded use locals, required case-specific use traces, independent closure-token
observation from exception RSI, lifecycle rejection, sampled numeric state,
versioned mid-copy ABA, freed source storage, active-worker STOP, C++ unwinding,
distinct SIMD lanes, two flag patterns and three MXCSR controls. These changes
do not recreate resource generation or native strip logic. All affected native
controls were rebuilt through `native-11`; the 12 frozen Python tests pass.

The second pass returned **REWORK** because only the first Use's provenance was
independently validated. The decoder now verifies every complete Use's exact
64 bytes against independent authored inputs and rejects corrupted provenance
in a later use. It also verifies header centers/radius and fixture identities.
The reviewer agreed a synthetic PASS can be defensible without treating fixed
quads or cooperative versions as proof of retail geometry/coherence. Full-x87
failure and its scope are retained explicitly, not described as irrelevant state.

Formal disposition: **ACCEPT**, for submitted package SHA256
`acf998eb6e2d1bee41bcddc9a4865375a2943cbcec261159b95af47708efd437`.
That exact package/patch snapshot is retained under local `review01/`.
Actual returns are preserved in `reviewer-design-rework-01-verbatim.txt`,
`reviewer-design-rework-02-verbatim.txt` and `reviewer-formal-accept.txt`.
The earlier separately named local summaries remain summaries, not substitute
verbatim evidence. This final reporting delta records the acceptance and commit
suggestion; its independent confirmation is retained in `reviewer-final-delta.txt`.

The reviewer independently checked all 20 complete-file hashes, both patch
hashes, 132 selected preservation pins, 101 evidence-file hashes, HEAD/index,
64 binary frames, all complete point arrays and all 76 complete Use snapshots.
It independently reconstructed both patch contents forward in memory, checked
all 41 changed Markdown relative-link targets and reviewed source/native
boundaries/failures/logs. It did not execute native fixtures, replay/unit tests
or the eight decoder negative controls; those results are receipt-backed and
source-reviewed. Temporary-tree forward/reverse patch application was performed
by the implementer, not independently rerun by the reviewer.

## Preservation and packaging scope

Ignored root `.local-work/internal-observation-qualification/` retains
`preservation-before.json`, `preservation-after.json`, `static-contract.json`,
all failed/successful disposable run directories, `changed-files.json`,
`complete-files.json`, `exclusions.json`, `git-status-short.txt`,
`verification.json`, `evidence-files.json`, `package.json` and `package.sha256`.
The evidence manifest hashes the original local run outputs without including
their binary contents in the review patches. Exact source/tool/generated/output
hashes are also retained inside each run's build.json. Manifest checks prove
integrity, not semantics or publication eligibility.

The 132 baseline pins cover installed executable, selected exports, original
080/evaluator/research sources, historical and supplied briefs, HEAD and index.
They do not cover every save, archive, database or loaded module. None of those
unscanned protected collections was opened or modified by task commands. No
target process operation was performed; target survival/restoration is not
applicable. Only the disposable process ran and its own sites were patched.

The baseline worktree contained only the supplied untracked brief. It remains
unchanged and is included only in the complete patch. Task-authored source/docs
and bounded index/credit/state additions are included in both patches:

- `.local-work/diffs/internal-observation-qualification-task-only.diff`
- `.local-work/diffs/internal-observation-qualification-complete.diff`

`package.py` adapts the project-owned predecessor local checker, whose source
is `.local-work/spatial-equivalence-feasibility/verify-package.py`, SHA256
`ef201ccfc160e1964c709d36cd3f0fa1de20402807243a333c73f0d59c5b1a15`.
The adaptation changes task scope, inventories and synthetic-evidence receipts.
It reads Git HEAD/worktree/index,
selected local inputs and task text; writes ignored receipts/patches; and checks
forward/reverse application in disposable temporary text trees. It does not stage
or mutate refs. It verifies changed-path inventories against tracked/untracked
text, LF/UTF-8/new-file whitespace and changed Markdown relative-link existence.
Manual prose review covers token spacing, numbers/addresses and inline code;
the regex candidate list is advisory, not proof of prose quality or link anchors.

Actual package checks: 19 task-authored paths, 20 complete paths including the
supplied brief, 132 unchanged pins, five unique inherited source pins,
11 inherited instruction assertions plus 12 static-contract assertions and three
PE instruction hashes, 41 changed Markdown link targets, clean tracked/new-text
whitespace and exact forward/reverse reconstruction for both patches. Manual
inspection of Markdown pattern candidates found valid inline code/address text
and no malformed token fusion. Final hashes belong to generated local receipts.
The complete patch excludes ignored
raw/binary/build/receipt material by declared scope, not by pretending those
files do not exist. Prior evidence, 0.8.0 candidate and the frozen evaluator are
unchanged. No third-party reuse/permission issue was found; existing
[source lineage](../../../SOURCES.md) and [credits](../../../../CREDITS.md) apply.

Suggested Conventional Commit subject:
`test(research): qualify internal spatial observation offline`

Maintainer critical review and publication gates remain open. No staging,
commit, push or integration was performed.
