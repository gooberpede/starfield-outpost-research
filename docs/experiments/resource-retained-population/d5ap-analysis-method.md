# D5AP analysis method and qualification

2026-11-04, Australia/Sydney. The interrupted eager writer-pair scan is replaced
by a complete queryable index and lazy witness expansion. Original raw readers
and sealed evidence remain unchanged. The [report](d5ap-report.md) states the
scientific scope; this method does not self-certify universal native coverage.

## Inputs, preservation and reproducibility

Use installed CPython 3.14.3,
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, SHA-256
`cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`,
with `-E -B`. Every new Python module refuses optimization before project or
sensitive imports; `-O`, `-OO` and inherited optimization are separately checked.
No dependency install, target process, database or network access is needed.
The scripts write exclusively new paths under `.local-work/d5ap`, reject
reparse outputs and enforce caller-available 40,000,000,000-byte floors on C:/D:.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -E -B research/resource-retained-population/d5ap_analyze.py --out .local-work/d5ap/NEW-analysis
& $py -E -B research/resource-retained-population/d5ap_windows_controls.py --postflight .local-work/d5ao/n2-live01/postflight02/receipt.json --out .local-work/d5ap/NEW-window-controls.json
& $py -E -B research/resource-retained-population/d5ap_competition.py --analysis .local-work/d5ap/analysis04 --summary-sha256 0228f06e75e879658ed2fc4e85469b4cd43175d0867ba0c2a7a36d3586587968 --out .local-work/d5ap/NEW-competition
& $py -E -B research/resource-retained-population/d5ap_native_controls.py --analysis .local-work/d5ap/analysis04 --summary-sha256 0228f06e75e879658ed2fc4e85469b4cd43175d0867ba0c2a7a36d3586587968 --out .local-work/d5ap/NEW-native-controls.json
```

Replace NEW names with unused names. A new analyzer run has a different summary
hash because disk-floor and timing observations differ; subsequent commands
must bind its actual hash, not copy the example hash onto different bytes.

The analyzer authenticates seal SHA-256
`99360972df120f7ba331bd56593b930fc881f78b6c6938230b20a3956986a3b5`,
archive SHA-256
`d7d48edf884b796865ed56ef5d5e467f381ce51ac6e6229e980a3e267cbc78af`,
all 174 evidence payloads both loose and inside the archive, the sealed reviewed
plan and all 484 source-lock inputs. The operational source-lock SHA-256 is
`acee73650465cd38dbc18ff4aafa17a573b88c5849355a161feb10d6c7f736b1`.
The seal supplies full source locators; no remembered session path is accepted.

Original core, D5AN causal/counter, D5AM scheduler, D5AI geometry/lifetime and
D5AJ source-Grid readers rerun their validation. The only replacement seam is
the pure `registration_windows` enrichment callback in the imported causal
reader; every raw validation, accounting and history predicate remains intact.
This is an identified new offline analysis, not a change to the original live
source lock or its interrupted/omitted historical outputs.

## Index and relationship semantics

[d5ap_windows.py](../../../research/resource-retained-population/d5ap_windows.py)
adapts the owned D5AM method under SOR-P-0002. Algorithm
`owner-context-index-and-lifecycle-bisection/1`, schema
`sor-d5ap-causal-index/1`, indexes one lock/generation by sequence, thread,
context `(thread, invocation, selection, source)` and QPC. Reset/retirement
boundaries are separately sorted for interval bisection. Source allocation and
task lifetime are joined in the extraction layer, not inferred from a source
pointer in an unscoped generic event.

Construction costs O(E log E) time and O(E + W) memory for E events and W calls.
A writer-pair query costs O(log L + K), for L lifecycle boundaries and K returned
invalidators. Expanding every requested pair still requires O(W²) visits, but
never scans all E rows for each pair or retains the Cartesian result. Every
original call, event ID, context and invalidator is retained in the export and
raw validated derivative. `iter_legacy` exactly preserves the original rules
and ordering, including conditional and uncertain outcomes.

The exported reader enrichment intentionally has `qualified=false`: it is
created before final channel and native/source coverage adjudication. Consumers
may instantiate `HistoryIndex(rows, issues, qualified=True)` only after those
prerequisites; otherwise `pair`/`event_pair` return outside-qualified-coverage.
No field silently promotes bytes to native-semantic acceptance.

| Relationship | Meaning and limit |
| --- | --- |
| DEFINITELY_PRECEDES / DEFINITELY_FOLLOWS | Same-thread recorded program order, or the explicitly named native endpoint edge from disjoint qualified approach/pending/acquired bounds. Inspect `native_edges`; this does not order every atomic in the two calls. |
| OVERLAPS_OR_INDETERMINATE | No supplied bounds decide the named native order; equal ticks remain ambiguous. |
| NOT_COMPARABLE | Self or unrelated cross-thread events without positive native ordering evidence. Shared lock identity alone does not supply a happens-before edge. |
| OUTSIDE_QUALIFIED_COVERAGE | Missing admission/qualification, history issue, status/hazard or crossed relevant lifetime boundary. |

The original legacy categories remain conditional even when the index is fully
computed. All-history completeness is computational coverage, not a claim that
reset-crossing pairs are scientifically comparable. `interval` returns callback
witnesses, not held-lock intervals. Reader/recursive events remain queryable;
writer-window rules are not applied to them as invented exclusive calls.

## Independent oracles and adverse controls

[d5ap_windows_controls.py](../../../research/resource-retained-population/d5ap_windows_controls.py)
implements a separate exhaustive bounded reference using direct pair and
invalidator scans. Twenty-four named groups include 150 seeded histories,
positive/negative/ambiguous pairs, equal ticks, same-thread versus cross-thread,
unrelated source on the same lock, recursive/readers, ABA/context reuse,
reset/retirement, missing registrations and incomplete/loss coverage. The tests
of missing/loss prefixes verify refusal qualification; they do not replace raw
wire-validation tests or invent a lossless record from a partial prefix.

Actual N2's deterministic 67-event focus covers acquisitions 1827, 2536, 2925,
2950, 2999, 3548 and 4405. Its full focused output agrees with the independent
exhaustive oracle AND unmodified original D5AM enrichment. Every actual writer
pair is then streamed to counts and a digest. The full stream SHA-256 is
`b5ca59a41627c14986f0805bd4036eb078f4959729f47d3148b47f9629c88e5e`.

[d5ap_native_controls.py](../../../research/resource-retained-population/d5ap_native_controls.py)
adds an independent packed-state oracle. It enumerates operand-compatible
atomic continuations without QPC sorting and reconstructs the five-reader
cohort, including equal-tick 2941 before 2940. Contradictory CAS and missing
reader-release copies produce no complete continuation. Ten direct native
predicate checks include mixed readers/writers, incoming readers with pending
writers, exclusive blocking, same-owner recursion/depth and final release.
These are original semantic controls, not copied or executed proprietary code.
Actual N2 has zero recursive acquisitions; no fixture is misreported as one.

The same file validates two observer/native delay continuations across the
actual peer gap, checks all four timestamped channels and pins the exact
retained 0.9.3 emitter. Its complete 196-coordinate enumeration comparison
independently challenges the upstream-frontier account. It does not promote
the D5S normalized root rectangle into N2's unrecorded ingress operands.

## Actual resource use and result identity

`window-controls03.json` records 79,952 events, 518 writer calls and all 72,015
conditional pairs in 0.701 seconds to index plus 2.921 seconds to stream, with
22,969,659 bytes of additional Python allocations measured by tracemalloc.
This excludes already decoded input objects, interpreter/native allocations
and input JSON loading; it is not whole-process peak RSS. The implementation
retains linear-size decoded histories rather than claiming streaming raw decode.
`analysis04` completes full authentication, original readers, source attribution,
extraction and pair counts in about 20 seconds on this machine. No scientific
row quota or historical-event limit is imposed.

`analysis04/summary.json` locks all generated input/result hashes;
`competition05/competition.json` locks the participant table, graph and interval
fixtures. `native-controls04.json` locks independent controls and the exact
retained emitter. `window-controls03.json` locks the final index and oracle
sources. The final delivery manifest additionally binds every authored source
and local receipt. Independent reviewer reruns of raw authentication, source
attribution and oracles are retained separately; their exact scope is in
[the review](d5ap-review.md).
