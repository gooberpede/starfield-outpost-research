# Completion matrix and reproducible checks

2026-10-15. [Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_local_inorganic_availability_native_mapping_corrected.md),
[report](report.md), [review](review.md). PASS for an offline artifact does not
mean independent native spatial equivalence. Receipts stay ignored under
`.local-work/native-availability-map/`.

| Original criterion | Result | Decisive evidence / limit |
|---|---|---|
| A: actual source-linked native register | PASS |34 entries in functions.csv; original function declarations/build/base/RVAs rechecked against14 exact-hashed primary exports; explicit input/output/precondition/effect/edge/limit fields |
| B: native dependency/dataflow specification | PASS |dataflow.md distinguishes caller operands, native loaded maps, generation misses, synchronous population writes and asynchronous UI; exact null/same-source retention branches |
| C: minimum sufficient input assessment | PASS evidence-bound |minimum-inputs.md separates inner callback, loaded updater, prospective/established context derivation, provider and final fold; arbitrary invocation and established runtime equivalence NOT TESTED |
| D: existing executable evaluator/capture reused | PASS scoped |checks01.json:45 availability and12 spatial tests pass;16 exact instruction dependency assertions, installed executable pin and14 native-export pins verified. Full raw/WAL census in coverage01/coverage.json; source geometry equivalence NOT TESTED |
| E: neutral reference and uncertainty/disposition | PASS |report/dataflow/minimum-inputs/uncertainty; concrete missing pointees and discriminating outcomes, no mod feature gap analysis or extractor-fit criterion |
| Relevant authorized dependency tracing / Outcome B | PASS independently ACCEPTED |Caller builders, loaded retrieval and cache branches, region predicate, component/descriptor/generation/provider lifecycle, definition and UI sources examined. Missing same-evaluation region/frame/cache operands demonstrated; not whole-engine exhaustion |
| Frozen evidence/provenance and boundaries | PASS |preservation-before.json and preservation-after.json verify6,868 inherited pins including capture/protected inputs; original evidence/predictions/evaluator unchanged; HEAD/index checked |
| Independent review | PASS — ACCEPT |Original-brief and primary-evidence review; execution-language REWORK corrected and final02 independently accepted; see review.md |
| Review manifests/complete and task-only diffs | PASS |Exporter and independent reviewer check Git path inventory, exact forward/reverse reconstruction, links and whitespace; supplied brief complete-only |

## Actual verification versus observed engine behavior

The source assertions check retained-list control flow, updater register roles,
internal manager/ProcGen retrieval and lock, source callback call, three caller
sites and descriptor-derived bounds. They are deliberately **static** evidence
checks; they do not simulate a native cache epoch or execute the retail function.
The57 passing tests exercise the existing evaluator's recovered arithmetic,
UNKNOWN behavior and final pointer fold with original synthetic controls.
No new evaluator or invented cache/query API was introduced.

Fresh full-capture replay verifies every 611,926 WAL/raw record and all 35,574
evaluation pairs,11,128 distinct argument descriptors and346 exact ordered native
UI comparisons. Disk-backed uniqueness preserves bounded memory. These numbers
are scoped to argument/population observations, not independent geometries.
No native spatial input/output pairs are available. Previously reported failures
and counterexamples remain in the original Milestone B records; this run does
not retroactively turn them into passes.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/native-availability-map/verify.py --run FRESH-CHECKS
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-availability-milestone-b/coverage.py --session .local-work/continuous-beacon-preview/live/session-24552-88395531 --out .local-work/native-availability-map/FRESH-COVERAGE
```

Use fresh output names. Scripts read protected inputs without modifying them,
enforce caller-available C:/D: free space>=40,000,000,000 bytes, and write exclusive
local receipts (plus SQLite uniqueness for census). No dependencies/downloads,
process access, save/configuration/analysis-project writes or network.

The initial git status contained only the supplied untracked brief. The long
protection hash audit finished after the first two task-authored files were
created; its raw untracked baseline therefore also recorded those files.
`baseline-raw.json` preserves that audit output. The packaging baseline is
corrected to the initial status (supplied brief only), so both authored files
are included in task-only.diff. The before/after protected-input equality
claim concerns unchanged inputs, not a falsely bracketed snapshot of authored
text. `baseline-correction.json` records the correction and hashes.

Target survival/cleanup is N/A: no target was launched or accessed. Instrument
qualification is unchanged. Scientific spatial equivalence and established
runtime equality remain NOT TESTED; successful static checks and preservation
are separate outcomes. No permission issue, staging, commit, push or disclosure
is introduced.

Actual packaging failures retained: an initial reporting patch had an unmatched
context and applied no changes. An overly broad editorial spacing substitution
altered hexadecimal text in intermediate final01; it was caught by primary
inspection before submission, and all six new documents were restored from the
exact independently reviewed review01 patch. Intended CPython/reporting edits
were reapplied explicitly. Intermediate patches remain local failure evidence;
final02 supersedes them; final03 records the actual independent ACCEPT verdict.
No native/source/evaluator/raw input changed.
