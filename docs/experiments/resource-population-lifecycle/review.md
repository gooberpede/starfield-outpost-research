# D5C completion and review package

2026-10-25, Australia/Sydney. [Original frozen AC1–AC8](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5C_resource_source_population_lifecycle.md`), [report](report.md), [native claims](native.md), [pins](sources.csv).
Task type: bounded offline native research. No amendments to mandatory criteria.
An honest unjoined Save52 timing/serialization result is permitted by AC5; missing
engineering verification or independent review is not a scientific negative.

## Baseline and actual method

Branch `main`, HEAD `c8678e80ecf6a309816da60de4234105848aec0e`. Initial status
contained only the supplied untracked D5C brief. It is preserved unchanged and
included in complete coverage, separately from task-authored text. No unrelated
working-tree changes were present. HEAD/index are hash-protected; no staging,
commit, push, branch/remote change, external disclosure or publication occurs.

The actual primary native inputs are the 1.16.244.0 executable (hash verified),
existing export bodies listed in [native.csv](native.csv), and three fresh
read-only/no-analysis exports: `d5c-lifecycle01`, `d5c-load02`, `d5c-init03` under
`.local-work/workshop-population-rework/specialist/`. Full instructions,
decompilation, xrefs and the six-entry ProcGen table remain LOCAL-ONLY. The
exports end with END and their logs record completion without script errors.
The static VA/RVA/member domains and each decisive branch are recorded; inferred
roles and unknown lifetime/event bindings remain qualified.

The principal routes considered were existing primary export inspection, bounded
new function/xref export for missing exact lookup and load/init edges, and
disposable synthetic modeling. Existing/new native bodies directly answer the
retention question with less infrastructure. Another synthetic cache model would
only reproduce an assumed rule, so no synthetic fixture or native experiment was
added. No predictor or collector was changed or executed. No resources were
regenerated and no new game measurement was made.

## Checks and reproduction

Use `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe` with `-B`.
The [helper documentation](../../../research/resource-population-lifecycle/README.md)
states reads/writes/dependencies/prerequisites and target effects. Local
`commands.json` preserves exact export selectors and command forms; export logs
give the executed argument vectors, not merely a proposed method.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-population-lifecycle/audit.py before
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-population-lifecycle/checks.py --label checks02
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-population-lifecycle/audit.py after
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/editorial/screen.py --changed
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-population-lifecycle/package.py --label review01
```

The first integrity check verifies 64 source pins, including 30 independent
historical register crosschecks. It confirms the original ten native-control
identities across 20 normalized/expanded comparison rows, and the frozen
conditional-result digest
`1c7420c884d5260b6d67f9ffe3f7ccd2f36f903501431feba2f2f85abddf8644`.
The final `checks02.json` adds the explicit Workshop row-iterator register entry.
These are unchanged-result integrity checks, **not a rerun** of the ten native
geometry controls. Geometry/predictor inputs were not touched. D2–D5 alternatives,
all seven indeterminate associations, original captures and sealed D5B evidence
remain protected. Receipt hashes are retained in the final local delivery index.

Protected-save verification uses the existing 12,974-row historical manifest and
prospective classification policy. Qualified active transient files remain
diagnostic exclusions; archives, designated research saves, manual saves and
quicksaves remain strict. Original historical discrepancies are retained rather
than rebaselined. The dedicated native before/after receipt compares all 15
analysis-project files and the complete file inventory. No analysis content is
written; tool cache/settings/logs are outside that inventory and stay local.

Both full audits pass with identical 77,893-pin maps and unchanged HEAD/index.
Both protected receipts are byte-identical, with zero new changes. Full audit
SHA-256 is `f622ffc3025fef057fd22af6e337987d55a820ad06948e7f476b076606c58f28`;
protected-receipt SHA-256 is
`318a5b51a28423e4ba7da8d88fb679d19122bf6598553975abcb10b6fab24bed`.
Final receipt/file/patch hashes are bound by the local `delivery.json`.

## Acceptance accounting

The independent reviewer accepted the following mapping against exact review01.
PASS means the frozen bounded criterion is met, including its stated unknowns;
it does not turn an unobserved historical event into a measurement.

| Criterion | Result | Evidence and bounded completion result |
|---|---|---|
| AC1 | PASS | `protected-before/after.json`, `audit-before/after.json`, `native-before/after.json`, unchanged HEAD/index; offline operations only. Protected inputs are equal; no unauthorized operation occurred. |
| AC2 | PASS | [N01–N03, N06–N08, N12–N14](native.csv): allocation, retained map/collection holders, deep points and final release; source definitions and Workshop result separated. External owner fence/aliases unknown. |
| AC3 | PASS | [N03–N05, N16](native.csv): exact source-pointer hash/equality, capacity sentinel, visited skip and generator bypass; implicit complete-context invariants unknown. |
| AC4 | PASS | [Lifecycle matrix](lifecycle.csv): insertion, defensive replacement, rehash, reset, teardown and operation refresh; first-query hypothesis conditional, no observed retail history dependence. |
| AC5 | PASS | [Bounded search](native.md#save-and-initialization-scope), N10/N11/N17/N18, direct provider callers and guarded bootstrap. Population serialization and Save52 timing UNRESOLVED with a discriminating [draft](next-run-draft.md). |
| AC6 | PASS | [Propositions](propositions.md): all requested claims, falsifiers, exact D5B mask-3 geometry and unknown historical mask/epoch preserved; no Save52 reclassification. |
| AC7 | PASS | [Pins](sources.csv), `checks02.json`, unchanged controls/frozen outputs, full protection receipts; screen/manual reading and exact export checks. Integrity does not prove semantics. |
| AC8 | PASS | Exact file inventory, complete/task-only patches/manifests, protection receipts and independent scientific/engineering/editorial ACCEPT. Final closure receives narrow independent delta review. |

## Editorial and delivery scope

The final prose inventory includes every changed Markdown paragraph/table, CSV
label/claim, Python comment/docstring and seven navigation/provenance edits.
The bounded changed-text screen returned zero diagnostics, followed by actual
manual reading of the entire authored set before independent assessment. Local
`manual-editorial01.json` binds that coverage to review01. No screen exception
or automatic legacy prose cleanup is adopted. Hashes/identifiers are checked for
identity; mask-versus-geometry, pointer-versus-epoch, source-versus-Workshop and
static-versus-runtime qualifications receive explicit contextual review.

Review artifacts live under `.local-work/resource-population-lifecycle/review01/`;
patches under `.local-work/diffs/rg2-d5c-review01-complete.diff` and
`rg2-d5c-review01-task-only.diff`. Separate machine-readable complete/task-only
manifests, changed-file hashes, status, exclusions and package checks distinguish
the supplied brief. Both patches are reconstructed byte-for-byte from HEAD in
isolated forward/reverse scratch trees; inventory comparison covers untracked
text, not merely ordinary Git diff. Whitespace, UTF-8/LF and local evidence links
are checked. Raw inputs, saves, binary/assets, analysis databases and ignored
receipts/exports are excluded and identified with local locations and hashes or
inherited immutable inventories. Nothing is staged to make the package.

Initial locator attempts for nonexistent `source-register.md`, `regressions.md`
and `native.md` paths produced read errors; the actual source CSVs and linked
native ledgers were then used. One broad export search ran slowly and completed;
it was not treated as absence evidence. The first checks receipt preceded the
explicit row-iterator register addition and is retained, with a separately named
final check. No failed scientific experiment, native mutation or protection
exception was concealed or converted into a pass.

Science: positive scoped native retention/reuse, unresolved historical/load/save
questions. Engineering: offline metadata/integrity/export verification only;
no new collector or retail safety qualification. Target survival/cleanup: not
applicable because no target was launched or attached. Publication: authored
REVIEW-REQUIRED, raw LOCAL-ONLY, B6 on hold. Independent acceptance does not supply
maintainer integration, live execution, staging, commit, push or publication approval.

## Independent disposition

The independent reviewer returned **ACCEPT for scientific, engineering and
editorial conformance; AC1–AC8 PASS** on exact review01. The verbatim return is
`.local-work/resource-population-lifecycle/independent-review01.md`. The reviewer
inspected decisive primary native bodies, all 64 source pins, all 20 changed
hashes, the complete authored prose, both exact patch reconstructions/reverse
scratch states, all 14 listed task-local exclusions, executable/database hashes,
control ledger and preservation-receipt equality. They did not independently
rehash the entire 77,893-input corpus or rerun geometry controls.

Only this self-describing completion record changes after that acceptance.
Final `review02/` refreshes the complete/task-only manifests and patches at
`.local-work/diffs/rg2-d5c-review02-complete.diff` and
`rg2-d5c-review02-task-only.diff`. The narrow delta return is retained in
`independent-delta01.md`; final `delivery.json` binds both actual returns, all
final file/patch hashes, integrity receipts and unchanged HEAD/index. No
acceptance supplies integration or further execution authority.
