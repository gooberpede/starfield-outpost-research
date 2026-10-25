# Stage A evidence archive research

[Report](../../docs/experiments/evidence-archive-discovery/report.md),
[accepted save-file hold](../../docs/experiments/evidence-archive-discovery/scope-amendment.md).
These are task-bound research helpers, not an activated production archiver.
No original evidence is migrated, deleted, normalized, uploaded or repaired.

Use the already installed Windows CPython 3.14.3, stdlib Zstandard/SQLite and Git.
No installation or network is required. `python` below denotes that interpreter;
it is not a request to change aliases. Fresh labels are required; original
receipts and failed attempts are retained under `.local-work/evidence-archive-discovery/`.

## Reads, writes and reproduction

| Helper | Reads | Writes / effects |
|---|---|---|
| `inventory.py --label FRESH` | Entire `.local-work/` namespace metadata and authenticated old pin receipt | New SQLite/summary and refreshed aggregate CSVs; no population payload hash |
| `discover.py --label FRESH` | Recorded inventory03, authored tracked/initial-untracked source text and source ledgers | Candidate owner index, local complete mention ledger, compact research-area/dependency/option tables |
| `retention.py` | Pinned prior deterministic stand-in builder/fixture and cargo candidate bytes | Reproduction proof and two-pass fresh pilot identities; no original writes or retirement |
| `scope.py --label FRESH` | Frozen metadata/owner tables and reproduction proof only | Non-save/held reconciliation and current proposed roster/retention tables; never reads save/container payloads |
| `benchmark.py --label FRESH --candidate-pin EXPECTED_SHA256` | Prior-pinned non-save actual sources and recorded expected-pin cache | Authenticated disposable copies, tar.zst/ZIP, verified restores and phase receipts; no source modification |
| `check_admission.py` | Injected disk readings and entrypoint guards only | Local eight-control receipt; no original payload reads or archive writes |
| `qualify.py --label FRESH` | New generated synthetic inputs and its own indexes/archives | Fault vectors, partials and successful disposable restores; creates one internal junction test, never an escape write |
| `model.py --label FRESH` | Scoped metadata, benchmark results and pilot/source ledgers | Transfer scenarios, candidate pilot and explicitly synthetic full-cardinality index; no real archive payload or production manifest |
| `deliver.py` | Exact authored tree, baseline copies, receipts, Git and method identities | Source ledger/preparation or fresh review patches/manifests and bounded scratch application trees; no staging/ref write |

Discovery/model helpers deliberately refer to this task's frozen inventory03,
discovery03 and scope02 inputs. They are reproducible against the preserved
receipts; a new inventory requires explicit input configuration and a new freeze,
not overwriting an old receipt. Do not run all discovery steps as a default
preservation ritual. The current benchmark driver removes the saved-file sample.
Saved-work helpers/derivatives are suspended locally and are outside this plan.

```powershell
python -B research/evidence-archive-discovery/qualify.py --label NEWTEST
python -B research/evidence-archive-discovery/benchmark.py --label NEWSAMPLE --candidate-pin EXPECTED_SHA256
```

The expected cache identity is recorded in the source ledger/preparation receipt.
Actual inputs must match the pre-existing source expectations before analysis;
do not calculate a new digest of changed bytes and call that an expected identity.
Metadata/derived-input hashes and current source versions are checked separately.

## Format and safety contract

`archive.py` only accepts marked copied/synthetic trees inside the Stage A
workspace. It writes exclusive partial archives, compares streamed member hashes
to authenticated intake, hashes the encoded archive and registers it in the test
index. Restore validates the index root, archive identity, bounded members and
fresh restored bytes before renaming a new partial tree. Existing destinations,
unsafe paths, special files, reparse ancestors, extra/missing/substituted members,
unsupported schema and broken data fail closed.

One logical SQLite master has archive/member identities, canonical original
relative paths, aliases and cross-system locators. Schema 0 benchmark indexes
are supported read-only; schema 2 qualifies explicit same-byte aliases. Version
roots must be supplied independently. Fixture indexes are separate instances
for tests, not a production sidecar per experiment. Member/index caps, strictly
bounded PAX path support and ZIP's sample-scale limit are documented in
[security](../../docs/experiments/evidence-archive-discovery/security.md).

Current helpers preserve both-drive 40,000,000,000-byte guards with phase
reservations. Metadata helpers reserve 1 GiB for the frozen observed workloads;
JSON writers additionally admit exact serialized bytes plus a metadata margin,
and aggregate CSV writes reserve 64 MiB. Different input scales require a new
measured reservation; these are task-bound budgets, not unbounded tools.
Current packaging reserves conservative expansion,
member overhead and 512 MiB for bounded index/journal work. Restore reserves
payload and directory/file cluster overhead. Stop on identity/integrity failure,
failed I/O/space protection, unexpected writes outside the disposable boundary
or explicit operator STOP. No elapsed-time/event quota terminates a healthy run.

Power-loss durability, atomic source snapshots, off-device backup and operational
consumer adaptation are not supplied by the prototype. Failed outputs remain
quarantined; no automatic source repair, baseline refresh or original cleanup.
The future Stage B brief must authorize and qualify those boundaries separately.

## Provenance

The implementation uses original stdlib code with source-informed adaptation of
the maintainer's `runtime/session-tools/archive.py` name/integrity safety method
and review-export `diff`/Git helpers under SOR-P-0002. Precise input/executed-method
identities are in the [source ledger](../../docs/experiments/evidence-archive-discovery/sources.csv).
The exact benchmark sources are retained in `benchmark01/methods/`; later safety
and alias changes are separately qualified, not assigned old timing receipts.
No third-party implementation, dependency download or external communication is
introduced. Raw native/proprietary evidence stays local and untracked.
