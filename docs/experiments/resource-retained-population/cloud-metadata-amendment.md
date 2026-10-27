# D5L diagnostic Cloud metadata amendment

2026-10-28, Australia/Sydney. Offline operational amendment to accepted
[Phase A](report.md) and its proposed [Phase B run card](run-card.md).

`remotecache.vdf` no longer blocks D5L preflight, admission or postflight when
its hash changes. It is diagnostic synchronization metadata under
[SAVE_PROTECTION](../../SAVE_PROTECTION.md). Protected local/remote saves,
independent backups, installed binaries/definitions and other protected inputs
retain their existing gates. Steam Cloud state confirmation remains mandatory.
The card is prepared for separate live authorization; this amendment grants none.

## Maintainer instruction and frozen scope

The maintainer requested a narrow amendment directly in chat and authorized
short corrections without another brief. Its mandatory requirements were:

1. Classify `remotecache.vdf` as diagnostic metadata, not a scientific input.
2. Remove its blocking identity checks from relevant preflight, admission and
   postflight operations, retaining strict protection for scientific inputs.
3. Preserve the historical D5L discrepancy and original failed verdicts.
4. Remove the card's separate exact-hash maintainer exception.
5. Retain Cloud state confirmation and direct protected remote save checks.
6. Update affected tests/schemas and demonstrate metadata drift acceptance,
   protected save failure, other protected-input detection and unchanged science.
7. Deliver this report, focused results, independent review and verified complete
   and task-only diffs. No Phase B, staging, commit or push is authorized.

The assignment forbids Starfield launch/attachment, source-selection research,
new instrumentation, archive maintenance and broad historical preservation
audits. It excludes a repeat of the 27-scenario debugger qualification unless
debugger behavior changes. No such change is made. No gameplay step, selected
source or software-breakpoint site is altered.

## Operational changes

The shared C2B `protection.py` still records the observed metadata hash and
`matches_historical` diagnostic, including a false result. Its new
`scientific_inputs_match` gate compares protected remote saves and other remote
inputs independently of metadata. Missing/unreadable metadata is diagnostic.
`sync_equal` now compares remote path, other inputs and protected save contents
without metadata equality. Historical receipts are not edited.

D5L preparation uses that scientific gate and always records
`OFFLINE_CHECKED_NOT_AUTHORIZED` after successful checks. Admission requires a
fresh `sor-d5l-preflight/2` receipt, current code/policy/card/build pins and Cloud
confirmation. It no longer requires `cloud_metadata_decision` or reads the
metadata file as a guard. Existing main-menu admission remains lightweight:
protected names/sizes, backup/archive and installed metadata. Equal-size content
substitution is checked by full preflight/after-exit hashes; lightweight admission
alone does not establish content identity. No full save scan is added during play.

The card now runs an explicit after-exit receipt comparison through
`preservation_native.py` after repeating full offline preparation. It checks
protected local/remote content, backup records, installed/configuration hashes,
archive guards, policy, source, tool/build/qualification and operational-code
identities. Metadata before/after hashes remain in its diagnostics.

The native build manifest also pins operational Python sources which were not
compiled into the observer. Without a correction, those obsolete operational
pins would prevent the amended card from running. `verify_build_files` permits
only the three amended D5L Python paths (`prepare_native.py`, `collect_native.py`,
`check_admission.py`) to differ, authenticates their original preserved build
snapshots, and binds current hashes in the fresh preflight. Every other build
file remains exact. Native source/binary/tool pins and original qualification
receipts are unchanged; no rebuild is performed. Fresh receipts additionally
pin the shared save-helper Python sources.

Older non-D5L preflight callers which still use `matches_historical` retain
their historical implementation and need prospective review before reuse.
This amendment updates the D5L path and shared comparison semantics, not every
historical run card. No old receipt is promoted to the new schema.

## Preserved historical result

Phase A recorded historical metadata SHA-256
`6aa04109a0f3b2eb73f9cf20cef75bb652a7521f7ea7eba9bfbe6188e4730886`
and then-observed SHA-256
`999aabbc12c48097d0a05f9cdbf329f0b26f6fb9ac9037e101ca80cfb2f12f4f`.
The recorded 2026-10-27 03:07:41 UTC modification time preceded Phase A's
05:21:57 UTC start. Remote protected saves matched in that audit. Original
preflight04 remains `OFFLINE_CHECKED_CLOUD_HOLD`; old-gate FAIL and eleven
original admission controls remain historical. The four excluded-ZIP strict
historical failure also remains untouched. No baseline, archive or old result
is repaired or reclassified by this amendment.

## Focused verification and limits

| Mandatory verification | Result and evidence |
|---|---|
| Changed metadata permits admission/postflight | PASS: disposable actual-file admission controls need no exception; full receipt comparison accepts changed/missing metadata. The shared preflight snapshot accepts metadata drift while retaining false historical comparison. |
| Changed/missing/substituted protected saves fail | PASS: lightweight admission rejects size/name/missing changes in both local and remote namespaces; full snapshot/comparison rejects equal-length substitutions and missing saves. |
| Other protected inputs remain detectable | PASS: backup, archive, installed executable, definition, configuration and code changes are rejected by relevant lightweight guards or full comparisons. Inherited controls reject missing/corrupt backup content and unclassified/new/manual/quicksaves. |
| Observation method/classifications unchanged | PASS: focused integrity receipt compares untouched native sources, site/epoch reducer, native contract and historical qualification against the starting tree; build files retain exact native/tool identities. |
| Cloud state and schema remain enforced | PASS: missing Cloud confirmation and old D5L receipt schema are rejected; remote namespace/non-save differences still fail. |
| Complete reviewed delivery | Exact reviewed hashes, inclusion/exclusion inventory and forward/reverse patch verification are recorded in the local package identified below. |

Run the focused tests from the repository root with installed Python 3.14.3:

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B -m unittest discover -s research/resource-retained-population -p test_preservation.py -v
& $py -B -m unittest discover -s research/resource-carinae-source-context -p test_save_policy.py -v
```

The suites contain 12 amendment tests and 14 inherited policy tests, including
multiple mutation subcases. The inherited disposable archive-policy control now
stubs the archive lookup to an empty synthetic mapping; it does not touch real
archives. Tests create temporary synthetic saves/backups only and remove them.
All approval-shaped dictionaries are synthetic and grant no live authority.
The old 27-scenario Windows qualification is retained, not rerun. No retail
behavior, real postflight or full preservation audit is newly validated.

Primary final results, command logs, immutable-method/build checks, editorial
screen and exact review packages are LOCAL-ONLY under
`.local-work/d5l-cloud-amendment/`. Complete/task-only diffs are under
`.local-work/diffs/` with the `rg2-d5l-cloud-` prefix. The initial tree was clean,
so their path sets and content are identical. Exact final manifests and the
verbatim independent disposition bind the reviewed snapshot without rewriting
the historical D5L delivery. Reviewer acceptance grants no integration or live GO.

Scientific confidence, coverage and publication classifications remain unchanged.
Authored amendments are REVIEW-REQUIRED; private receipts remain LOCAL-ONLY.
No new external code, dependency, permission basis or disclosure is introduced.
Existing maintainer-owned save/operational/export methods are reused under
SOR-P-0002. [Sources](../../SOURCES.md) records that provenance.
