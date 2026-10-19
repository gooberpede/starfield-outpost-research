# Output-contract review and verification package

2026-10-16, Australia/Sydney. [Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_native_availability_output_contracts_completion.md),
[mandatory matrix](completion-assessment.md#frozen-mandatory-criterion-matrix),
[native reference](output-contract.md), [path assessment](output-paths.md).
Scientific assessment: **CONDITIONALLY COMPLETE** within the stated research
endpoint. Integration/publication require separate maintainer review.

## Verification and preservation

Task baseline HEAD `2ae9c1b8a0932a0a18aaee8718c2318d2d7e2f49`, index SHA256
`be84d122acbade6977ca36123ca08d90fcf4e6ea8bfece2cf37925b3ad4d6a9b`.
Only the supplied brief was initially untracked; its unchanged SHA256 is
`e9239a4db01580363a8940e18d5b8c3a5683de304bc48f750023af79dfa2fcc9`.
The complete patch includes that brief; task-only excludes it.

Installed CPython 3.14.3, stdlib, existing owned tests and installed Git only.
Commands below were run from repository root; all receipts are ignored/local.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/native-output-contracts/preserve.py --phase before
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/native-availability-map/verify.py --run output-contracts01
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/native-availability-map/verify-region-dependencies.py --run output-contracts01
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/native-output-contracts/preserve.py --phase after
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/native-output-contracts/check.py final01
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/native-output-contracts/export.py --run final01
git diff --check
```

Existing verifier: **70 register entries / 27 export pins / 16 instruction
contracts PASS**, installed executable hash verified; **45 availability + 12
spatial tests PASS**. Receipt `.local-work/native-availability-map/output-contracts01.json`.
Lifecycle verifier: **eight assertion groups / 12 additional source pins PASS**;
`.local-work/resource-region-dependencies/output-contracts01.json`.
These exercise static transcriptions and synthetic evaluator controls, not new
native spatial equality, source readiness or retail safety.

Task-local `check.py` checks eight output-specific instruction groups (absolute
ranges, water filter, pointer union, spatial materialization, biome append,
teardown call/free and direct end resets), pins unchanged 070 capture source and
records tools/scripts/brief hashes in `checks-final01.json` under the task-local
receipt directory. It also checks authored UTF-8/LF encoding and
targeted code/text spacing. The existing full 611,926-record / 35,574-evaluation /
346-fold census is inherited from the qualified original and subsequent complete
replays, rather than rerun here. Preservation rehashes its sealed input bytes.

Local `preservation-before.json` and `preservation-after.json` both verify
**6,868 inherited protected/capture pins**, matching exactly including HEAD/index.
After-check available bytes: C: 93,113,589,760; D: 117,576,925,184. The scope is the
inherited 070 baseline plus session seal, not every file on disk or every current
Ghidra database. No Ghidra execution or project write was performed. Source export
pins are checked separately by the verifiers above. Both C:/D: caller-available
space guards remain 40,000,000,000 bytes; initial values were 93,115,912,192 and
117,579,485,184 respectively. No original save, raw capture, binary, observer,
evaluator, frozen output or protected input is changed by this task.

Local helper provenance: original documentation author/checker, owned preservation
method adapted from `.local-work/native-availability-map/preserve.py`, owned review
exporter adapted from `.local-work/resource-region-dependencies/export.py` at the
baseline HEAD. Helpers read existing inputs/Git and create ignored receipts,
patches and disposable apply trees under .local-work/review-patches; only `author.py` writes the
listed authored documentation. No target/process/database/network effects or new
dependency. Source/script hashes are in the task check receipt; native payloads
remain local and are not embedded in patches.

## Prose audit and actual failures

All newly authored prose and changed navigation are reviewed for readable spacing,
version numbers, RVAs, filenames and code/text boundaries. No broad hexadecimal
or historical prose substitution is used. Historical malformed spacing outside
changed assertions is preserved rather than silently rewriting prior evidence.
An intermediate default-encoding read corrupted punctuation in the function
navigation; the diff caught it, the one affected file was decoded correctly and
its current register count corrected before review. The local author helper was
also corrected to specify UTF-8. Earlier local attempts to read wildcard Windows
paths or guessed filenames failed harmlessly; corrected bounded paths were used.
The initial encoding audit also flagged pre-existing CREDITS punctuation defects;
comparison with HEAD confirmed unchanged counts. A subsequent spacing-regex
check falsely paired adjacent code spans; sequential span checking corrected it.
Failed checker invocations wrote no success receipt; `review03` is the first
successful task-local check. The checker now rejects added
defects while preserving that historical text. The reviewer caught reset stores
attributed to an adjacent caller; the paragraph now identifies the separate
`0x021b6a10` routine. Reviewer taxonomy feedback also separated STATIC/OBSERVED evidence basis from
PROVEN scoped observations and proposed STRONG semantic confidence in the
reference and assessment. No input or scientific result was changed to pass a check.

## Independent review

Independent reviewer `output_contract_review` returned **ACCEPT** against review04
after correction of reset attribution, successful checker command and confidence
taxonomy. It accepted CONDITIONALLY COMPLETE for the original bounded endpoint
and challenged both unsupported safe-copy claims and inflated requirements for
geometry, remote generation or independent invocation. Actual return is retained
at `.local-work/native-output-contracts/reviewer-review04-verbatim.md`.

Reviewed package SHA256
`8f69cbb2a9b382fd79e49f204c7ab9d3974c364b1a3f1eb1d5d5821d01278392`;
complete patch `925e69823bdc4d376fb1b781a86b207fa297d6c54d9a78da7529ec572afc7fbf`;
task-only patch `e30a35e94ef622b6a8a83329488aa587c1f014c14fd0cb0c00c18c4d86eedb63`.
The reviewer independently checked seven source hashes, all 17 working-tree
hashes, both patch hashes, reverse applicability, unchanged HEAD/index and
`git diff --check`. It independently hash-verified/decoded the first 350 raw 070
records, including two three-row UI callbacks. Full capture replay, 346 folds,
57 regression tests and 6,868 preservation checks were inspected through receipts,
not independently rerun. Final01 records this disposition and requires a final
administrative snapshot recheck. No review decision authorizes integration or
live work.

## Review artifacts and coverage

Final task-local artifacts are
`.local-work/diffs/native-output-contracts-final01-task-only.diff` and
`native-output-contracts-final01-complete.diff`, plus
`.local-work/native-output-contracts/package-final01.json` and `status-final01.txt`.
The JSON identifies exact patch hashes, per-file hashes, changed/new manifest,
exclusions, HEAD/index, link/whitespace checks and separate disposable forward
and reverse exact-byte patch applications. No staging is used. Complete inventory
is compared to Git's changed and untracked text paths; supplied brief is separate.
Existing missing links, if encountered, are disclosed in that manifest; no new
missing file target is accepted. External URLs are not checked.

Final packaging covers 17 complete text paths / 16 task paths, with successful
forward/reverse exact-byte reconstruction and file-target checks. A separate
`anchor-check.json` verifies four heading anchors in the new reference/review
documents; it is not a whole-repository anchor audit. The final manifest holds
the final patch hashes, avoiding a self-referential patch-hash claim in this file.

Excluded: all pre-existing ignored/raw/native/proprietary/save/memory/database/
build artifacts, local helpers, receipts, review patches and disposable trees.
Their exclusion is a publication boundary, not a claim of research completeness
or rights clearance. Authored changes are REVIEW-REQUIRED; no new permission
issue, third-party incorporation or external disclosure occurred. Target outcome
and cleanup are N/A because no target was accessed. No stage, commit or push.
