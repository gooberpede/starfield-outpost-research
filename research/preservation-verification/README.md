# Disposable preservation-verification research

[Contract and report](../../docs/experiments/preservation-verification-optimization/report.md).
This is an isolated prototype, not a project protection/admission replacement.
Default verification reads every fixture payload. The conditional journal mode
has a documented readable-byte coverage gap and does not satisfy AC4.

Run from the repository root using the existing CPython executable. `python`
below means that interpreter, not a request to install or change aliases.
Windows NTFS, visible unprivileged USN records, the existing Git executable and
the current project save-protection inputs are prerequisites. No network or
third-party dependency is needed.

```powershell
python -B research/preservation-verification/reconstruct.py intake
python -B research/preservation-verification/reconstruct.py reconstruct
python -B research/preservation-verification/qualify.py --label FRESH01
```

`intake` is a once-only task-start command: it writes new ignored source pins,
HEAD/index/status and unchanged-helper protection receipts. `reconstruct` reads
those pins and the historical receipts, stats their fixed D5G paths, and writes
new aggregate tables. It does not rehash the broad historical payload corpus.
The actual task used these commands before any policy/navigation edits.

`qualify.py` creates a fresh ignored fixture subtree under
`.local-work/preservation-verification/`; an existing label is refused. It freezes
W1/W2, expectations, metrics, trial order and method hashes before performance
evaluation, constructs synthetic payloads, runs five paired trials and executes
50 base controls. Results and CSVs stay in the new labeled subtree. It briefly
changes the ACL only on its own synthetic permission-denial fixture and removes
that deny ACE in `finally`. Interrupted permission tests require inspection of
that exact disposable fixture, never a broad ACL reset.

The task-specific `additional.py` writes only a fresh `supplement01/`, freezes
supplementary expectations and exercises race, foreign-baseline, interruption
and fallback cases. It expects authorized tracked navigation changes to exist
as its normal-Git-output context. It does not alter Git state or verify original
evidence with the conditional prototype.

`journal.py` reads root/file identities and the visible drive journal through
Windows APIs. It rejects reparse nodes, malformed/unsupported records and broken
cursor continuity. `prototype.py` writes a manifest only during baseline creation;
verification has no write, repair or automatic checkpoint operation. It requires
an explicit disposable marker, an externally supplied expected manifest hash and
the original fixture-root identity. Full scans use global before/after ordering;
the journal mode gates the interval and freshly hashes every scientific/critical
fixture input twice. These remain finite observation windows, not snapshots.

`summarize.py` is a one-time task report generator over selected frozen receipts.
It writes exclusive local cost/input receipts and refreshes task-authored CSVs
from the selected frozen run04. The export baseline states its actual origin. Final
method/result identities are additionally bound in the delivery manifest.
`reconstruct.py reuse` checks actual consumed source identities, original
HEAD/index and the unchanged save/content scope again. Its only allowed source
exception is the task's navigation addition to research state: original bytes
are checked from HEAD, and changed output bytes are bound in delivery.

Use the existing `research/editorial/screen.py --changed` and
`research/review_package.py` for exact final review exports. Their original
sources are pinned, rather than copied into this prototype. Review patches and
scratch applicability trees remain under the repository's ignored local paths.
`deliver.py --label FRESH02` runs the screen, syntax parsing and that exporter,
then records exact changed-file identities, local exclusions and environment
facts in a new ignored directory. It refuses label reuse and never stages files.

Risks are local fixture disk use, CPU/read load, journal visibility and a
temporary fixture ACL denial. Enforce the existing 40,000,000,000-byte free-space
guard on both C: and D:. Stop on integrity/identity mismatch, worker failure,
unexpected writes outside the declared disposable boundary or explicit operator
STOP. Do not stop a healthy run merely for elapsed time. Preserve failed runs;
there is no automatic deletion, historical repacking or source-evidence cleanup.

No game launch/attachment, debugger, save operation, installed configuration,
analysis edit, deployment, policy activation, staging, commit, push, publication
or external disclosure is performed or authorized by these helpers.
