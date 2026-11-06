# D5AS aggregate analysis protocol

Use the pinned Windows CPython 3.14.3 with `-E -B` from the repository root
after the proposed series receives separate authorization. The tool opens
only the dedicated capture directory and local evidence. Its outputs go in
`.local-work/d5as/` outside the capture directory. Do not put receipts in the
capture directory. Keep Starfield closed during aggregate analysis.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$series = 'research/resource-retained-population/d5as_series.py'
$prepare = 'research/resource-retained-population/d5as_prepare.py'
```

## Inventory and qualification

Run `& $py -E -B $series inventory .local-work/d5as/attempts-01.json` using the
[analyzer](../../../research/resource-retained-population/d5as_series.py).
This is the first step after the initial 30 attempts and after each batch of
replacements. Use a fresh output name for every pass.

The ledger inventories every immediate artifact and keeps its filename, byte
count, SHA-256 or read failure. It groups capture artifacts by session UUID and
capture UUID. The filename timestamp and IDs must match a sealed and exactly
encoded final snapshot. A partial stays invalid even when its checksum and
process identity can be recovered. Unknown artifacts remain in the file ledger.
Producer-reported refusals keep their original reasons. Startup records bind
the same session and process to the selected DLL, game, SFSE, source lock and
series sidecar. Three finalized startup stages are required for the eligible
retail command path. Identity fields and integrity hashes establish internal
consistency within the retained evidence. A copied or fabricated self-reported
JSON object has no independent provenance by itself.

Multiple capture identities in one session, repeated capture UUIDs across
sessions and multiple sessions tied to the same PID and creation FILETIME
invalidate the affected attempts. PID reuse with a different creation FILETIME
is allowed. A startup-only session shows launch evidence and an unverified
capture attempt. It contributes to the separate launch-only tally. A launch
without an attributable file remains unknown unless separately documented.
The analyzer never invents the difference between 30 and the number observed.

At aggregate review, obtain one maintainer account of adherence and known
deviations. The capture cannot verify the save or route directly. If known
deviations affect identifiable attempts, rerun inventory with `--deviations FILE`
and pass the same option to archive and freeze. Use a JSON object with schema
`sor-d5as-documented-deviations/1` and a `deviations` list. Each entry has the
observed `session_id`, `capture_id`, evidence location or account in `evidence`,
and a `code` from the analyzer's prespecified deviation codes. These cover
wrong save, route, package or profile, extra gameplay or trigger, a repeated
process, or operator STOP during the attempt. Evidence review resolves
uncertain or unassignable departures before freeze. Preserve independently
documented no-file attempts with the review as launch or attempt evidence,
separate from the observed capture-artifact count.

An attempt row contains its identities, file links, original copy status,
startup link, selected source and geometry admission, and an eligibility flag
with all reasons. The geometry gate never uses reference equivalence. The
summary has observed attempt, qualified, invalid and launch-only counts, plus
a histogram of reasons. One invalid attempt can have several reasons.

When the ledger reports `PROVISIONAL_NEEDS_REPLACEMENTS`, keep it and every
input. Collect the reported number of additional eligible observations with
fresh processes under the same procedure. Record later attempts under their
new IDs. Additional invalid captures can require further replacements. This
state supplies no final roster or binomial result.

## Candidate, archive and freeze

Order eligible observations by ascending numeric process creation FILETIME,
then invocation UTC, session UUID and capture UUID. This is the prespecified
timestamp-based ordering. Local clock adjustment can affect apparent elapsed
time and order, so retain raw times and any diagnostics. Select the first 30.
Keep every later eligible attempt and every invalid attempt in the ledger and
archive. Independently investigate material integrity or procedure deviations
before freeze. Do not replace or remove a qualified capture based on its shape.

Run the one aggregate content comparison with
`& $py -E -B $prepare protect --output .local-work/d5as/protection-after01 --baseline BEFORE`.
Use the exact successful D5AS baseline receipt from the handoff as `BEFORE`.
The operation checks current protected originals and backup/restoration inputs,
Steam remote content, guarded files, and both disk floors. Timestamp differences
alone are diagnostic. A content or protected namespace change stops freeze and
calls for maintainer review. No original is restored automatically.

Run `& $py -E -B $series archive .local-work/d5as/corpus.zip --ledger LEDGER`.
The tool rereads and hash-checks every inventoried file and stream-verifies
every ZIP member. Keep the loose originals. An independent reviewer must check
the exact earliest 30, later and invalid attempts, producer and reference pins,
route and protection evidence, archive and actual maintainer decision before
accepting freeze. Preserve evidence for documented departures or invisible
attempts with the review. Reviewer and maintainer records are external human
attestations. The offline code verifies their declared bindings.

Use a local authorization JSON with schema `sor-d5as-series-authorization/1`,
decision `AUTHORIZED_BY_MAINTAINER`, `maintainer_record` identifying the actual
approval, `package_sha256`, exact ledger `method_pins`, and `before_sha256`.
Include exact ledger `reference_pins`. Confirm the approved route and card in
the underlying maintainer decision.
Use a review JSON with schema `sor-d5as-independent-freeze-review/1`, decision
`ACCEPT`, identified `reviewer`, `review_record` and `pins` mapping
`ledger`, `archive`, `authorization`, `before` and `after` to their file
SHA-256 values. No such approval or series review is issued by this assignment.

```powershell
& $py -E -B $series freeze .local-work/d5as/frozen-corpus.json --ledger LEDGER --archive ARCHIVE --before BEFORE --after AFTER --authorization AUTHORIZATION --review REVIEW
```

The canonical freeze file binds roster identities, exact method and package
pins, archive, protection and independent decision. The tool rechecks the
current ledger and archive and publishes a single exclusive manifest containing
the prespecified statistics after review. Keep this file and its cited evidence.
Later files never replace a frozen sample.

## Prespecified analysis

Use the complete canonical body under the pinned source and frame. Compare
all bytes with the two references. Retain `MATCH_MASK0_REFERENCE`,
`MATCH_MASK3_REFERENCE`, and `OTHER_QUALIFIED_GEOMETRY` as separate classes.
For novel observations the frozen roster retains full canonical bytes and
first differences against both references. The archive retains all raw bytes.

Report counts and fractions out of 30 plus 95% equal-tailed exact marginal
binomial intervals under an IID sampling model. These are marginal intervals,
with no simultaneous coverage claim. They do not measure uncertainty due to
capture failures, dependence or procedure deviations.

If the 30 qualified observations all fall in the two fixed reference classes,
set K to the number of mask-0-reference matches. Conditionally on IID
observations, the fixed reference assumptions and a binary proxy model, compare
K to the hypothetical binomial null with 30 trials and p = 1/7. Report both
inclusive tails and the exact probability-ordered two-sided tail, summing the
masses no greater than the observed count's mass. Prespecify the all-mask3
probability as (6/7)^30, about 0.00980836 under that null. Any other qualified
geometry makes the binary proxy test **INCONCLUSIVE**. Retain the three-class
counts and intervals. The 28/196 conditional coordinate census does not supply
a measured game winner probability. Fresh processes do not establish IID, and
geometry equivalence supplies no direct mask read.
