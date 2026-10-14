# Durable outpost position resumption â€” SOR-EXP-0030

2026-10-11 Australia/Sydney. SOR-EV-0038. Original
[authorized brief](../implementation-briefs/CODEX_BRIEF_SOR_durable_outpost_position_reconstruction_resumption.md).
Offline results REVIEW-REQUIRED; raw material LOCAL-ONLY. Independent reviewer
returns [ESCALATE](position-resumption/independent-review.md): completed offline
implementation/evidence package, full native-equivalence objective incomplete.

| Element | Supported result |
|---|---|
| Question | Can persisted ordinary Workshop inputs reproduce native body/frame/grid/subcell/compensated-center representation with independent validation? |
| Answer | Version 2 corrects a native packed-origin reflection defect outside the 23 frozen cases, reproduces all 23 unchanged, exposes missing site cells as UNKNOWN, and separates native hierarchy from packed coordinates. Native-order angular diagnostics materially refine the earlier ideal math. Fresh same-invocation native grid equivalence remains NOT TESTED. |
| Confidence | Static instruction/arithmetic claims scoped to pinned retail 1.16.244.0; loaded input bits independently corroborated. No new semantic promotion or native-equivalence PASS. |
| Coverage |23 frozen active inputs: Save25/26 four, S1/S1C two, Save52 seventeen; fresh 23-save decode, all 16 Phase 1 checkpoints/9,412 raw sections, 32 loaded Workshop records, synthetic tags 0â€“3/crossings/quantizer boundaries. No blind native holdout. |
| Evidence | [Algorithm](position-resumption/algorithm.md), [dependency/alternatives ledger](position-resumption/dependencies.md), [review and acceptance matrix](position-resumption/review.md); local verification receipts and selected comparison CSVs in that directory. |
| Limits | Frame 2b requires an upstream qualified site cell; raw-angle SIMD/CRT and floating-environment equivalence, future selected live edge/epoch and fresh native center/grid ownership are not established. 10 matching passive tuples do not close these gaps. |
| Next decision | Independent scrutiny of the residual authority gap, then [narrow observer qualification design](position-resumption/acquisition.md). No live action or external debugger work is authorized. |

## Changes and actual results

[Version 2](../../save-analysis/scripts/durable_position_v2.py) preserves the
original reader/model/observer/fixtures. A specialist traced the packed tag 2/3
unpacker and found that both axes reverse before native hierarchy offsets.
The original model offsets the encoded axes directly. The exact accepted-input
counterexample, instruction locations and corrected dual-domain output are in
the algorithm. This correction changes no frozen expected output.

The new [angular diagnostic](../../save-analysis/scripts/position_quantizer_diagnostic.py)
recovers binary32 normalization, epsilon-zero radicands and nested double
fmod/floor hierarchy operations. It deliberately exposes surrogate trig and is
not wired into missing site-cell handling. Terrain landing snap corner branches
and asset rotations are separate dependencies, not per-case fitted transforms.

The [verification CLI](../../save-analysis/scripts/verify_position_v2.py)
checks all 23 frozen outputs against unchanged expected JSON, fresh decode
provenance/bits, every Phase 1 raw section and all 32 loaded input triples.
Sixteen selected terrain-origin/body/grid comparisons also match the controlled
saved descriptor origin; this corroborates that representation, not the
workshop post-quantization result or an unspecified future frame.
The sixteen native comparisons preserve 10 equal tuples and six unequal ones:
one inactive zero baseline plus five retained prior-site 003 records. All remain
freshness/identity-unqualified. There is no qualified native mismatch, zero
native grid outputs and zero blind native holdouts. Passing hashes establish
integrity, not semantics; recomputing loaded sums is not native execution.

The full save-analysis suite passes 152 tests at this checkpoint (baseline 140,
twelve new). These include all original tests, original complete 23-output equality,
four tags and crossing branches, packed/native inversion, signed remainder,
negative floor, zero copy, unsupported domains, poles/equator and neighboring
double quantizer boundaries. Exact checks use bits/integers, with no fitted
epsilon. Synthetic controls are not retail native observations.

## Experiment authority and integrity

Allowed: protected local saves/archive and receipts read-only; static native
exports with readOnly/noanalysis; original deterministic code/tests/docs and new
ignored receipts. Risks are frame-domain confusion, mixed arithmetic, stale
tuples and accidental input mutation. Stop affected evidence work if integrity
fails, disk query fails or caller-available C/D bytes fall below 40,000,000,000.
Ordinary scientific anomalies stay in the ledger. No target is run or attached;
no game/Vortex/save/configuration/database edits, dependency installation,
network disclosure, staging, commit or push by the agent.

Fresh decoding reused unchanged `research_durable_center.py` and existing bounded
stdlib/project readers. 23 source saves, catalog and ESM preserve their before/
after identities; decoder scratch is cleaned by its existing controlled reader.
Its fresh run is `.local-work/durable-center/position-resumption-01/`.
Phase 1 reinspection and before/after raw hashes are in
`.local-work/position-resumption/verification-04/`. The starting tree and committed
source/output hashes are in `.local-work/position-resumption/baseline.json`.
The maintainer committed prior extractor research during startup; the user
explicitly reported this. The baseline captured HEAD 22df3a71 and clean index,
with only the supplied brief untracked. Earlier staged status is preserved in
the session; no prior task file is reverted or attributed to this task.

## Offline reproduction

From repository root, use the installed CPython 3.14.3 path (no installation):

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
& $py -B save-analysis/scripts/durable_position_v2.py .local-work/engine-oracle/example-input.json
& $py -B save-analysis/scripts/position_quantizer_diagnostic.py -0.2197651008318516 -0.5116409319889974
& $py -B save-analysis/scripts/research_durable_center.py --run NEW-POSITION-RUN
& $py -B save-analysis/scripts/verify_position_v2.py --output .local-work/position-resumption/NEW-VERIFY --session .local-work/beacon-observer-live/session-9236-127079640 --extraction .local-work/durable-center/NEW-POSITION-RUN/results.json
```

Output directories must be new. Pure fixture tests/model need only repository
files and explicit JSON; full archive verification requires preserved local raw
inputs and manifests. `verify_position_v2.py --output NEW` without optional inputs
is a 23-case regression check only. No CLI communicates with the game. Reviewed
changes and precise checks/limitations are in [the review package](position-resumption/review.md).
