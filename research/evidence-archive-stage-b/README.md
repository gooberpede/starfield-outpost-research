# Cargo evidence archival pilot

The [invoked brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_consolidated_evidence_archival_stage_b_pilot.md`)
authorizes offline packaging, synthetic fault tests and disposable restoration.
It does not authorize retirement of real files. Use the existing CPython 3.14
executable with `-B`, from the repository root. No installation or network is used.

| Method | Inputs and prerequisites | Outputs and effects |
|---|---|---|
| `engine.py` | Explicit expected index/manifest digests, canonical Windows paths, source hashes, exclusive ownership of ancestor directories | Fresh archives and restores, flushed journals and write-through publication; optional separately approved exact-file retirement |
| `qualify.py` | Existing Python/stdlib, three hash-pinned packager sources and Stage A version metadata | Fresh synthetic fixtures only; intentionally corrupts and deletes its own files; leaves failures and malicious test nodes for diagnosis |
| `pilot.py --build` | Exact Stage A cargo set and historical ledgers, original non-save files, both-drive 40 GB guards | Fresh final archive, central index, complete disposable restore, dry-run proposal and measurements; no original changes |
| `audit.py --label NAME --index-sha256 DIGEST` | Authenticated final archive, exact original members and baseline | Fresh local source/read/allocation/exclusion receipts; skips synthetic reparse nodes and never deletes files |

Do not rerun `pilot.py --build` over an existing transaction. Its exclusive outputs
deliberately refuse replacement. Diagnose interrupted work, authenticate it with
an independently retained digest, then use a newly named transaction for a retry.
Synthetic qualification may be repeated because it allocates a fresh UUID root.
Do not delete or traverse its junction and hardlink fixtures as ordinary evidence.

The final central index is `.local-work/research-archives/index.json`. Its schema
maps each archive owner to its manifest and each overlapping consumer to that
owner. Each original has one physical owner. The cargo archive embeds the exact
member manifest; the central index authenticates its digest and every payload.
The independent expected index digest belongs in the durable decision card and
review package. A hash stored only beside a replaceable index is not a trust root.
This does not provide an off-device or adversary-proof root of trust.

For a future read, use `engine.py restore --index PATH --index-sha256 DIGEST
--destination FRESH_PATH`. Destination must be within the task output root.
The full original relative paths appear beneath that destination. Recheck the
specific scientific input's original hash before use; a journal or archive hash
does not establish scientific meaning. Historical scripts may be inspected there,
but no acquisition, game, save or retired packaging script is authorized to run.

Windows read handles deny concurrent write/delete sharing. Regular-file, hardlink,
stream and ancestor checks reject hazardous inputs. Directory ancestry must remain
under exclusive operator control; this is not a defense against a hostile kernel
or an attacker replacing ancestor directories during an operation. Restoration
creates regular files with newly assigned metadata and never imports executable
permissions, alternate streams, links, ownership or timestamps from the container.

File data is flushed before `MoveFileExW` with `MOVEFILE_WRITE_THROUGH`. Tests cover
software interruption and abrupt process exit; real power loss and controller
honesty are untested. A published archive without an authenticated index remains
quarantined. A verified index without the final human approval cannot trigger
retirement automatically. Journals distinguish preparation, verification,
restoration test, awaiting approval, retirement and completion. They record progress
but never replace fresh source/archive verification.

The retirement executor checks the exact externally approved manifest identity,
its index binding, full archive/member integrity and all sources before removal.
It reauthenticates archive/index and the locked source immediately before each
individual deletion. Deletion uses the same Windows handle whose bytes were
hashed. There is no multi-file atomicity. Missing or changed files stop a retry;
partial removal requires controlled restoration and a new operator decision.
The [continuation card](../../docs/experiments/evidence-archive-stage-b/continuation.md)
contains the exact unexecuted command and recovery procedure.

The strict tar/path decoder and space guard come from the project-owned
Stage A prototype. Export verification uses the current owned
`research/review_package.py`. Reuse follows SOR-P-0002; source hashes and failed
executed versions are retained locally. CPython's stdlib and Windows APIs are
execution facilities. No outside code, new dependency or licence basis is added.
