# D5AF methods and checks

2026-11-02. [Frozen contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AF_construction_winner_stabilization.md),
[report](d5af-report.md), [source pins](d5af-sources.csv).

## Execution boundary

Inputs are the pinned installed 1.16.244.0 executable/definitions/PlanetData,
existing source exports and owned methods, verified disposable Ghidra copy,
protected Save52 research copy and B2 session/notes. Allowed actions are offline
hashing/decoding, targeted no-analysis read-only exports from the disposable copy,
owned private-page native controls and authored synthesis. Outputs are fresh
ignored receipts/exports/scratch and reviewable text. Original databases are
hashed as files but never passed to Ghidra. No game, deployment, target attach,
save/configuration mutation, network or Git integration occurs.

Risks include alias/ABI/interpretation mistakes and accidental original-project
access. Stop affected work on identity, callback, oracle, project-path or disk
failure. Both drives retain the 40,000,000,000-byte caller-available floor.
Native mappings and controlled wait/release callbacks exist only inside their
disposable host process; exit frees its mappings. Exports may create housekeeping
only in the disposable project. Preserve original evidence and failed attempts.
Review apply trees stay under `.local-work/review-patches/`, with parent Git
discovery stopped at `.local-work/`; patches stay under `.local-work/diffs/`.

## Reproduction and provenance

Use `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -E -B`.
The fresh input receipt pins CPython 3.14.3 and its executable. Windows PATH's
application alias failed before execution. Commands below require authenticated
local proprietary evidence and fresh output names; they do not download inputs.

```text
research/resource-retained-population/d5af_baseline.py --inputs NEW-INPUTS.json
research/resource-retained-population/d5ac_reconstruct.py .local-work/d5ac/NEW-AF
research/resource-retained-population/d5w_native.py .local-work/d5af/NEW-QUEUE.json
research/resource-retained-population/d5af_controls.py .local-work/d5af/NEW-CONTROLS
research/resource-retained-population/d5af_lock_control.py NEW-LOCK
research/resource-retained-population/d5af_geometry.py .local-work/d5af/NEW-GEOMETRY .local-work/d5af/geometry-metadata
research/resource-retained-population/d5af_extra_inputs.py NEW-EXTRA-INPUTS.json
research/resource-retained-population/d5af_export.py NEW-EXPORT EXISTING_STATIC_FUNCTION_VA
research/resource-retained-population/d5af_sources.py .local-work/d5af/NEW-SOURCES
research/resource-retained-population/d5af_package.py NEW-PACKAGE
```

The initial `d5af_baseline.py` invocation freezes repository files exactly once;
its `--inputs` route adapts owned D5AE baseline checks by changing only output
namespace and governing brief basename. The first stdin adaptation had a wrong
`__file__` root and refused before input access; the corrected initial receipt
is `inputs01.json`. `inputs02.json` uses the durable wrapper and records original,
transformed and wrapper method hashes. This is a selected-input preservation
check, not a full active-save preflight.

The exporter adapts D5AE/D5S, enforcing `-readOnly -noanalysis` and passing only
`D:/tools/sor-d5ad-ghidra-project`. Core pins are checked before/after. The lock
method relocates only imported call addresses in copied native helper bytes;
its wait callback performs a declared external release and wake callbacks record
destinations. It exercises helper predicates, not actual OS blocking/fairness.
The geometry method extends owned D5S/RG1 methods; D5T already established the
two complete ordinary outcomes. Metadata from the completed targeted exports
binds native math dependencies. Native buffers/allocators and collection getters
are explicit fixture substitutions. No implementation from outside this project
is incorporated; installed Ghidra/JDK/CRT/CPython/Git are separate tools.

## Performed results

| Check | Result | Evidence and limit |
|---|---|---|
| Repository freeze | PASS | Baseline HEAD `53d6c69d4d88a9de9b514f224c5cf45f6881e74b`, index hash and 3,168 byte copies; existing D5AE work and supplied briefs distinguished from D5AF. |
| Selected-input authentication | PASS | inputs01/02 each authenticate 54 pinned selected inputs and both disk floors; executable file/product version read directly as 1.16.244.0. |
| Fresh B2 reconstruction | PASS | `.local-work/d5ac/d5af-reconstruction01`: 32,141 records, exact reader equality, three damaged-input refusals, 224 increments, 97 admission/QPC inversions, zero qualified cold chains. |
| Native queue contrast | PASS | `incremental01.json`: twelve original dispatcher/claim activation and locality cases; callback tokens substitute for whole engine nodes. |
| Arbitration/failure predicates | PASS | `controls01/controls.json`: seventeen inherited synthetic state cases, seven new schedule/readiness/observation-equivalence cases and eight same-owner protected lookup joins. No synthetic schedule is a retail probability. |
| Native lock admission | PASS | `lock02/control.json`: eleven original helper cases, including pending-writer barging, incoming reader, recursion and both wake branches. Earlier specialist `prelock-native01` is retained with its exact method pin. |
| Disposable native exports | PASS | prelock-export01 and geometry-export01/02 complete with terminal END, original/copy core preservation and exact receipts. |
| Complete fixed geometry | PASS at fixed-input scope | Final geometry receipts compare all resource keys, regions, headers, point counts/bytes and native bounds with independent arithmetic and cold repetition. See geometry report for final receipt/version names and full-generator/retail boundary. |
| Fixed-source extra-pass applicability | PASS | `extra-inputs03.json` freshly reconstructs pinned installed ESM and component slots; Special/Everywhere are absent under the fixed main-file contract. This is not B2's effective runtime state. |
| Normal-retail preference and complete-geometry repetition | NOT TESTED | No new live operation is authorized. Existing recordings lack the essential admission/readiness and complete-population operands. This is a mandatory scientific gap, not a passing test. |
| Pre-work required-reading sequence | FAIL | Initial concatenated read was truncated; targeted reading and relevant D5T reconciliation occurred during investigation. No retroactive compliance claim. |

Editorial screening, complete manual changed-prose reading, independent review,
final source/HEAD/index preservation and forward/reverse patch-byte verification
are recorded in [the review record](d5af-review.md) and local package manifests.
Their success cannot replace the unanswered scientific contract.
