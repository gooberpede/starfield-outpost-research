# Disposable qualification and measurement limits

[Methods](../../../research/preservation-verification/README.md),
[report](report.md), [full trial table](measurements.csv), [base tests](tests.csv).
Every mutated file was generated under the ignored task workspace. No original
save, backup, capture, installed input or analysis database served as a fixture.

## Execution and preserved attempts

The unchanged protection helper completed before the experimental fixture work.
Task source pins were recorded and checked before reconstruction; D5G's audit
receipt matches the digest printed in its historical reviewed completion record.
The reconstruction compares expected mappings without rehashing their payloads.
Current file sizes and IDs are a separate metadata-only observation.

- `run01/` retains the initial frozen setup attempt. Generic-read volume access
  returned access denied before a performance measurement was emitted.
- `run02/` retains a zero-access volume-handle attempt; the query returned
  incorrect function. A direct privileged journal-read probe also returned
  access denied. No elevation or policy/volume change was requested.
- The existing Windows SDK interface declarations identified the unprivileged
  journal operation. Read-only probes established that a root-directory handle
  supports query and unprivileged reading here. No SDK implementation was copied.
- `run03/` retains all 25 performance records, 50 declared test results and the
  modeled corruption counterexample from the first successful version. Independent
  review then identified a baseline-construction race and the per-category scan
  ordering weakness. Its zero test failures were insufficient validation.
- The corrected method captures a cursor before baseline hashing and refuses
  historical activity during construction. It retains that initial cursor.
  Before/after passes now surround the complete scientific/critical verification
  sequence. `run04/` freezes the same workload sizes, metrics and trial count;
  its method hashes bind the corrected implementation. It supplies final results.

No failure was retrospectively turned into a pass or erased. The original
denominator and 80% requirement remain unchanged after correction.

## Detection controls

The base suite declares expected outcomes before execution and runs each case in
full and conditional modes. Actual filesystem operations cover content edits,
same-size substitution, timestamp-preserving substitution, deletion, rename,
same-byte replacement, unexpected additions, root-directory replacement and a
hardlink alias write. Fresh scientific and critical checks cover a changed
scientific file, protected original stand-in, EXE and ESM. Truncated scientific
ZIP and corrupt/tampered manifest tests fail, rather than adopting new hashes.

Negative control and authorized output creation allow admission. The real
permission-denial case uses `icacls` to deny read access on a newly generated
scientific file and removes only that deny ACE in `finally`. It produces an
actual Windows permission error. I/O failure and interruption are explicitly
injected exceptions, not claims of hardware faults. Journal reset/gap and corrupt
page controls inject metadata into the actual parser/continuity checker; no
volume journal is reset or truncated. Full mode correctly ignores injected
journal failures because it has no journal dependency. Conditional mode refuses.

The supplementary suite freezes additional expectations in
`supplement01/freeze.json`: a foreign but correctly hashed baseline/root;
interrupted full scan; a historical write during scientific hashing; unavailable
journal followed by non-destructive full fallback; unsupported journal record;
and a mutation between a baseline leaf hash and cursor finalization. Actual
authorized tracked Git changes provide the benign output context, while scanners
remain confined to synthetic protected roots. This shows boundary allowance,
not a deployed Git-policy enforcement implementation.

The modeled unjournaled-mutation control deliberately suppresses the journal
adapter's events after an ordinary real write. Conditional mode admits; full
mode detects changed bytes. The write was actually journaled: this is a model
counterexample to dependence on journal observations, not an experiment that
corrupted NTFS below its journal. It supports the precise coverage gap in AC4.

## Reproducibility and performance scope

Use a fresh alphanumeric label with the commands in the method README. The
scripts refuse overwriting receipts/manifests and do not advance checkpoints or
repair fixtures. Both-drive free space is checked; every W2 arm checks it before
and after. Independent reviewers may execute separately authorized fresh
disposable controls; their actual return is bound by [review](review.md).

All fresh measurements are logical application-level reads/hash calls and
wall/process-CPU time. No claim is made about device I/O, cold-cache speed,
peak memory or exact physical scratch allocation. Manifest/control bytes and
journal reads are charged separately from payload work. Namespace entries and
logical pin visits are distinct. Selected ZIP validation adds identical archive
read work to all W1 arms; it is included in wall time but not payload SHA bytes.
The full input population and its before/after hashes are retained; no critical
class was moved into the historical denominator to improve the ratio.

W1 compares a scaled operation model, not an exact replay of D5G's data and
parallelism. The historical eight-worker after branch is documented but not
recreated as a claim about its original throughput. W2 is a risk-control
simulation and is intentionally not optimized. Full scans and journal gates
still have finite observation windows; neither is a transactional snapshot.

The final task preservation run rehashes actual consumed source receipts and
the unchanged protected-save/content scope. Its costs remain separate from
synthetic W1/W2 performance and from historical reconstruction.
