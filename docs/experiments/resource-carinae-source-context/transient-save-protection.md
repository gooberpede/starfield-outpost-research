# C2B transient-save operational amendment

2026-10-23, Australia/Sydney. [Invoked amendment](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_AMENDMENT_SOR_C2B_transient_save_protection.md`),
[durable policy](../../SAVE_PROTECTION.md), [amended card](run-card.md),
[current source/evidence pins](transient-sources.csv).
**Phase B: PENDING MAINTAINER APPROVAL. No Carinae live test was performed.**

Active exitsave/autosave churn is now excluded consistently from preservation
gates. Protected research/manual/quicksaves, all historical backup records and
raw research evidence remain strict. Ambiguous saves fail closed. The old
exitsave discrepancy remains preserved evidence but no longer requires corpus
acceptance, restoration or a supplemental transient backup.

## Classification and operational paths

`save_policy.py` validates the complete native-generated filename structure,
including kind/slot, profile/flags/encoded-name, elapsed and UTC fields, numeric
bounds and final marker. It uses existing retail 1.16.244.0 formatter evidence at
preferred static VA `0x14184eec0` and its complete decompilation; the export's
instruction-list limit is not represented as complete instruction coverage.
This is a native-bound naming model, not a save-header kind decoder. Partial
names, malformed fields, nested names and case collisions cannot be silently
excluded. Unsupported cases need explicit documented qualification/designation.

The tracked JSON contains exact research designations and their pins. Save52
remains the primary protected input. Initial enumeration also found one
BCPS-signature save file, `funclist.sfs`, with an unsupported name. The maintainer directly
answered “Designate it as protected (Recommended)”. The exact designation and
original byte/hash identity are retained locally and in the policy; its nominal
kind remains UNKNOWN. No filename or original/backup bytes were altered.

| Code path | Prospective behavior |
|---|---|
| `save_policy.py` / JSON | One deterministic classifier and canonical policy hash. Explicit research designations win over nominal kind. Manual/quicksaves are protected; active auto/exit files transient; ambiguity blocks. Every designation needs exact live and independently verified backup pins. |
| `admission.py` | Uses the shared protected-save gate. Historical backup equality remains exact for every record. Removed the old per-rotation corpus-disposition exception. New/changed/missing protected live saves still fail. |
| `preflight.py` | Full protected input/installed/config/Steam audits, classified live inventory and strict historical backup validation; persists diagnostics before admission assertions. Rehearses Save52 restoration into a new local scratch file. Schema 2 binds exact policy/classifications; no live permission inferred. |
| `protection.py` | Reads the old immutable manifest through the new policy. Only exact active Documents/Saves paths get transient exclusion; archived raw/backup paths retain strict pins. Enumerates current active additions/unclassified files. Steam save comparison is filtered; Cloud metadata/cache and non-save files remain strict. |
| `collect.py` | Requires schema 2 and unchanged policy/build/code pins. Existing lightweight launch names/sizes checks compare protected live files and every backup record, excluding active transient races. Scientific capture/three-resource STOP logic is unchanged. Not executed against retail. |
| `postflight.py` | Uses the same receipt-bound policy, compares protected live content and every backup record, retains full transient diagnostics, and checks EXE/definitions/config/source evidence/Cloud metadata separately. No whole diagnostic sync-map equality or live restoration. |
| `build.py` | Includes the JSON policy in source pins. New build and fresh synthetic qualification replace no old build/receipt. C++/ASM collector code is unchanged. |

Live transient read/disappearance races produce diagnostic entries; protected
read failures remain failures. Active namespace/root/ancestor reparse checks are
retained. A changed policy invalidates launch/postflight admission rather than
silently reclassifying a session. Non-save Steam metadata changes remain an
independent guard failure, even if transient files also change.

## Historical reconciliation

The former old exitsave ending `20261022002200_319_15_4.sfs` was absent, while
the newer exitsave ending `20261023053108_319_15_4.sfs` was present. Both complete
names satisfy the native-bound Exit/slot-zero grammar. This is transient
rotation for prospective preservation purposes; timing and cause are not newly
inferred from filenames. The old refusal receipt and its recorded failure remain
unchanged. All old manifests/hashes, archived copies, frozen predictions, native
captures and acceptance records retain their original scope.

The immutable historical backup includes all 271 old records, including old
transient copies. Their hashes and names remain strict archive checks; the
current live transient population need not equal them. This keeps archival
preservation independent of active-save churn. The prospectively protected
live subset contains manual/quicksaves plus explicit designations; total counts
are diagnostic and never an integrity oracle.

## Reproduction and qualification

Use installed CPython 3.14 with `-B`, never `-O`, from repository root. Commands
write only new ignored builds/receipts/scratch; choose fresh output names on
reproduction. No original save or backup is written or restored.

```powershell
$c2bPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $c2bPython -B -m unittest discover -s research/resource-carinae-source-context -v
& $c2bPython -B research/resource-carinae-source-context/build.py --name transient-build01
& $c2bPython -B research/resource-carinae-source-context/qualify.py --build .local-work/resource-carinae-source-context/transient-build01 --output .local-work/resource-carinae-source-context/transient-qualification01
& $c2bPython -B research/resource-carinae-source-context/preflight.py --build .local-work/resource-carinae-source-context/transient-build01 --qualification .local-work/resource-carinae-source-context/transient-qualification01/qualification.json --name transient-offline-preflight01
& $c2bPython -B research/resource-carinae-source-context/postflight.py --preflight .local-work/resource-carinae-source-context/transient-offline-preflight01/preflight.json --output .local-work/resource-carinae-source-context/transient-offline-postflight01.json
& $c2bPython -B research/editorial/screen.py --changed
```

Seventeen unit tests PASS: fourteen save-policy tests and three unchanged
geometry/transfer/receipt contract controls. Subcases cover exitsave creation,
removal, replacement and rotation; autosave churn; Save52 modification/removal;
new/changed/missing manual saves; quicksaves; missing/corrupt backups including
archived transients; ambiguous names/kinds; explicit transient designations;
mixed protected/transient changes; whole-manifest namespace boundaries;
transient/protected read races; root reparse rejection; and independent Steam
cache integrity. The preflight/admission and postflight core functions are both
exercised. A later new designation without its own verified backup is rejected.

The refreshed debugger suite passes all 42 disposable-target cases and the
source-context memory controls. It qualifies the rebuilt source bundle without
new retail execution or changes to the capture's scientific discriminator.
The unchanged C++/ASM source hashes and frozen scientific evidence are retained.

Actual offline preflight PASS: 271 live files comprise 98 protected and 173
transient files, with zero unclassified files; all 271 historical backup records
agree. The old/new exitsave names appear only in transient diagnostics. The
12974-entry broad audit excludes 173 active transient entries and reports zero
protected changes. Save52 scratch restoration reproduces its original hash.
Matching offline postflight PASS: no live/backup/installed/configuration or
protected-evidence changes; Steam metadata/cache is unchanged. The final strict
12974-entry before/after integrity check also passed, including exact historical
records, with HEAD/index unchanged. No gameplay is used to simulate transient churn; synthetic file fixtures reside only under new
temporary children of `.local-work/resource-carinae-transient-saves/`.

## Frozen amendment acceptance and review

| Condition from the amendment | Disposition and evidence |
|---|---|
| Transient churn nonblocking without suppressing protected failures | PASS: shared pre/post classifier gates, mixed-change regressions and broader audit namespace tests. |
| Deterministic, auditable, fail-closed classification; designation precedence | PASS: native-bound full grammar, tracked policy/pins and documented direct maintainer designation; ambiguity and late unbacked designation controls. |
| Earlier exitsave discrepancy explained and no longer an admission blocker | PASS: actual offline preflight admits the original rotation with zero protected/backup changes; no corpus exception supplied. Historical manifests/refusal remain immutable. |
| Required regressions and independent exact-snapshot sign-off | PASS: tests and independent exact-snapshot review ACCEPT; closure-only delivery delta receives separate review. |
| Original saves/backups/frozen predictions/native evidence unchanged; no live execution | PASS: 12974-entry strict before/after receipt has zero changes; actual offline postflight and unchanged HEAD/index verified. No game launch/attachment/save mutation. |

Earlier incomplete-design defects found during review are preserved in the local
check history: root reparse coverage, exact elapsed/name validation and backup
readiness for later designations. They were corrected before final qualification;
no source/save baseline was refreshed to mask a failure. The initial policy
enumeration correctly left `funclist.sfs` unclassified until the direct maintainer
designation. Historical tests/refusal artifacts are not deleted or rewritten.

Editorial finalization follows the project standard: automatic changed-text
screen, complete manual changed-prose/comment/label reading, independent review
of the exact final snapshot, then verified delivery. Original receipt/input
hashes and the final changed-file inventory are retained in the source ledger
and delivery manifest. Any substantive later edit needs independent delta review.
Complete/task-only diffs, exclusions and byte-exact forward/reverse application
checks remain local; raw saves, native exports, binaries and private receipts are
excluded from deliverable patches. No staging, commit, push or publication.

## Independent disposition and delivery closure

Independent review returned **ACCEPT** for all amendment requirements on the
26-file `rg2-c2b-transient-review01.json` snapshot (manifest SHA-256
`a5b857f2e48d2dc7f2e913ed77d77a2ce06fdca46dea0b46daa6fa1515c2c9b8`).
The verbatim return is retained in
`.local-work/resource-carinae-transient-saves/review01-independent.txt`.
Editorial disposition is PASS; all 56 source pins and exact file/Git identities
were independently verified. Exporter receipts prove byte-exact forward/reverse
reconstruction; the reviewer separately checked actual-tree reverse applicability.

The reviewer disclosed a scope deviation: one selected receipt-control test
created a disposable `contract-*` directory under the ignored C2B scratch root,
contrary to the stricter no-temporary-test review instruction. It self-cleaned;
subsequent inspection found no remaining temporary directory and all frozen
file/HEAD/index identities remained exact. No original save, backup, game, code
or Git content changed. This disclosure does not waive that instruction; no
further mutating reviewer tests were run. No reviewer code corrections were
incorporated.

The closure changes only this report's acceptance/delivery text and one grammar
correction. The final changed/new-file inventory and both verified patches are
in `.local-work/review-deliveries/rg2-c2b-transient-final01.json`; the complete
patch includes the supplied amendment, while task-only excludes it. Local raw
artifacts are excluded from both. The scoped final delta return is retained in
`.local-work/resource-carinae-transient-saves/review02-delta.txt` after review.
No code, policy, build, qualification or scientific input changed during closure.
**Phase B remains PENDING MAINTAINER APPROVAL.** Reviewer acceptance grants no
live execution, integration, staging, commit, push or publication authority.
