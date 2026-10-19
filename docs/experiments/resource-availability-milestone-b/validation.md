# Capture coverage, controls and validation

2026-10-15. [Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_inorganic_resource_availability_milestone_B.md),
[report](report.md), [independent disposition](review.md).

## Original mandatory criteria

PASS below means a specified offline deliverable is present; it does not convert
an unobserved spatial comparison into native equivalence.

| Criterion | Result | Evidence and limits |
|---|---|---|
| Input/capture/tool inventory and preservation | PASS | Local preservation-before/after receipts: 6,868 checked pins (6,847 inherited plus seal and 20 sealed files), all equal; HEAD/index unchanged. Prior reports/readers/definition receipts and 23 frozen position predictions retained. |
| All relevant 0.7.0 populations, bounded memory and repetition | PASS | `coverage01/coverage.json` and SQLite uniqueness index; every 611,926 WAL/raw record verified, all statuses zero, no unpaired invocations. At most two active invocations held; uniqueness uses disk-backed SQLite with 2 MiB cache. |
| B1 query/ABI/frame and spatial rules | PASS STATIC implementation; native equivalence NOT TESTED | Exact producer CALL argument ABI, broadphase, zero/one/multiple point branches, consecutive tapered quads, vertex-height and 3D edge predicates; [native ledger](native-provenance.md). Actual callback points/frame translation table not captured by 070. |
| B1 identity/atmosphere/biome/water/union/order/X-Tech | PASS within stated conditions | Existing installed IRES/BIOM/RSGD/ATMO evidence, fresh full consumer/row replay, explicit special filtering and bypass distinction. No extractor placement criterion introduced. |
| Executable versioned evaluator, typed unknowns and controls | PASS | Version 2 integration, spatial helper, preserved version 1; synthetic samples, 80 passing focused/regression tests. Numeric domain explicitly restricted; malformed or unavailable inputs do not become empty observations. |
| Independent A/B/C and atmospheric/transition/UI tests | PASS final-fold channel; spatial-input comparison NOT TESTED | All 346 exact ordered-row/set comparisons agree from actual common-consumer and constructor/census evidence. Operator receipt intervals A/B/C agree. No exact rendering or unique asynchronous ancestry claim. |
| Substantive B2 input production and save investigation | PASS scoped | Fresh native producer/source-table/generator/descriptor/competition tracing; installed definition edges; fresh 29-save/63-extractor positive replay. Missing full source arrays, generation context and native region operands distinguished from available scalar keys and definitions. No universal whole-save absence claim. |
| Outcome A or completed evidence-bounded Outcome B | PASS — independently ACCEPTED Outcome B | Spatial evaluator is executable beyond set union; [acquisition](acquisition.md) specifies indispensable missing operands and competing explanations. Outcome A NOT TESTED. Independent disposition controls acceptance. |
| Indexes, durable state, backlog and permission/provenance | PASS subject to review | Linked continuation records preserve deferred Z/geography/Hab topics; no new external code, dependency, permissions basis or disclosure. |
| Independent review and complete/task patches | PASS — ACCEPT; see [review](review.md) | Exact original-criterion review, independent raw replay and byte-exact patch reconstruction. No self-acceptance or integration authority. |

## Native population and repetition census

Private receipt root `.local-work/resource-availability-milestone-b/`.
Raw input `.local-work/continuous-beacon-preview/live/session-24552-88395531/`.
The original [seal and source ledger](../continuous-beacon-preview/live-scientific-report.md)
remain authoritative identities. Raw `events.bin` is 2,036,489,728 bytes, SHA256
`33bc0ec5191184b8942f6b47db184465baf5f40ddac4184d428d5cf797ed59ee`;
WAL SHA256 `8112881390d1edded492da3212ac5c7629d95f051105ca077035636cb64bb677`.
The audit verifies per-record ordering/hash and matching retired terminal counts,
not just the file hash. Both C:/D: disk guards exceed 40,000,000,000 bytes before
substantial operations and in final preservation receipts.

| Quantity | Whole capture |
|---|---:|
| Evaluation calls | 35,574 (35,573 preview; one initialization) |
| Distinct indexed argument XYZ/frame/domain tuples | 11,128 |
| Distinct tuples including radius/height bits | 11,128 |
| Once-only tuples / repeated tuples | 11,072 / 56 |
| Largest repetition count | 13,836 |
| Qualified captured region geometries / identities | 0 recovered; actual total UNKNOWN |
| Independent spatial operand/result comparisons | 0; NOT TESTED |
| Refresh 1 with change / without change | 5 / 341 |
| Refresh 0, unchanged | 35,228 |
| Iron-only spatial population / Iron+Alkanes | 20,754 / 14,820 |
| Helium-3 atmosphere / Iron+Lead unfiltered biome | 35,574 each |
| Exact ordered-row/set native comparisons | 346 / 346 agree |

The six constant-population runs contain 10,603, 86, 253, 18,397, 3,964 and
2,271 evaluations, respectively. Their UI counts are 315, 2, 14, 3, 10 and 2.
The first includes the initialization evaluation, unlike the original preview-only
count of 10,602; this is accounting scope, not a counterexample. Operator A/B/C
receipt markers fall within runs four/five/six. They are manual reports, not
native render timestamps. The generated resource population switches five times;
candidate **region** transitions cannot be counted from final populations.

| Branch/control | Synthetic | Independent native operand/result coverage |
|---|---|---|
| Broadphase outside/tangent, point-count 0/1 | PASS | UNKNOWN point counts/regions |
| Multi-point XY containment ignoring Z | PASS | NOT TESTED |
| Vertex XY radius and absolute height | PASS | NOT TESTED |
| Closed quad 3D edge, segment endpoints/interior | PASS | NOT TESTED |
| Consecutive strips without path closure; repeated points | PASS | NOT TESTED |
| Binary32 rounding residual, overflow/subnormal rejection | PASS | Native arithmetic transcription only; MXCSR-sensitive domain excluded |
| Pointer duplicates vs FormID duplicates, null/missing, allocation failure | PASS | 346 final folds sampled; no selected special append observed |
| Water filter/duplicates, X-Tech property bypass | PASS conditional existing controls | No actual water/X-Tech UI branch in this session |
| Reflected/translated coordinates | PASS explicit common-frame translation and reflected ordered-strip controls; no implicit transform | Actual translation table not recorded; arbitrary frame equivalence NOT TESTED |
| Cache repeats and changed/unchanged refresh | Input handling PASS | Captured full census above; branch-specific cache causal history UNKNOWN |

## Reproduction and actual checks

Installed CPython 3.14.3 at the explicit path below, stdlib and owned project
modules only. No downloads or new outside implementations. Commands read
original evidence and write exclusive ignored derivatives; no target/analysis DB,
save/configuration or Git mutation. Do not reuse existing output names.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability-milestone-b/coverage.py --session .local-work/continuous-beacon-preview/live/session-24552-88395531 --out .local-work/resource-availability-milestone-b/coverage-fresh
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability-milestone-b/checks.py --run fresh
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/verify_resource_availability.py --run .local-work/resource-availability/saves01 --extra .local-work/resource-availability/extra01 --output .local-work/resource-availability/milestone-b-checks-fresh
```

`tests-03.json` records 45 availability, 12 spatial, 11 extractor, six Workshop
origin and six framing tests, all PASS (80). Fresh saved-registry replay in
`.local-work/resource-availability/milestone-b-checks01/checks.json` reproduces
29 audit objects/decoded hashes, 848 supported roots, 63 positive extractor joins
and 114 mature registry rows. This verifies reproducibility/producer controls,
not complete availability. Native module test fixtures are original synthetic
controls, never independent retail execution.

Preserved execution failures: an initial shell-quoted inline packaging command
failed Python parsing before writes. First test runner mistakenly named
`test_record_framing.py` and ran zero tests in that group; `tests01.json` retains
the nonzero result. Corrected discovery uses `test_outpost_record_framing.py`;
`tests-02.json` records the actual six passes. Specialist export selector failures
are retained in its ledger. No failed run is presented as a pass.

Independent review also identified a version-2 exception-domain mismatch:
nonfinite/subnormal/overflowing query inputs initially raised ValueError instead
of the promised UNKNOWN. The implementer corrected the integrated query path,
added an adversarial control, and reran all groups in `tests-03.json`. Three
coordinate/rounding controls and explicit hex byte-count notation address the
reviewer's additional gaps. [Review](review.md) records disposition and recheck.

Offline experiment actions are file reads, owned evaluator/test execution,
read-only/no-analysis existing Ghidra exports, and exclusive local derivatives.
Inputs are the pinned capture, executable/definitions, protected save corpus and
existing source/export records. Risks are disk pressure, derivative confusion and
numeric/source misinterpretation; stop affected operations on pin mismatch, guard
failure, unreadable input or malformed evidence. Retain originals and failed
receipts; decoder scratch is cleaned by existing owned readers and review apply
trees remain disclosed under .local-work/review-patches. No target runtime effects are authorized.

Publication eligibility is separate: authored algorithms/interpretations require
review; raw game/native exports, saves, large receipts and runtime pointers stay
LOCAL-ONLY. Passing hashes establish preservation, not scientific semantics.
