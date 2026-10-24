# D5 validation and reproduction

2026-10-25, Australia/Sydney. [Result](report.md), [contract](contract.md),
[provenance](sources.csv), [independent review](review.md).
Receipts below are under ignored `.local-work/resource-feynman-d5/` unless
otherwise specified. These are actual completed offline checks, except the
explicitly future live qualification/card.

## Prediction freeze and regressions

`build04` freshly verifies the D4E input freeze and installed ESM, recomputes
initialized components and matches every frozen component before selecting
descriptors. It changes only Feynman III BIOM `0x000fd00a`. Its normalized and
expanded corpora are byte-identical to the earlier completed `build02`; the
additional build04 checks do not change predictions. Both code bundles preserve
the original inference and geometry bytes. The new builder consumes no images,
saved extractor outcomes or native selected DNAM as answers.

`validation01/prediction-freeze.json` seals all 17 active-case predictions in
both representations and the Feynman/Carinae control requests before opening
native answers. The inherited control corpus is unchanged. Archimedes controls
use the cohort prediction. Each isolated inference process denies all eight
forbidden-read probes and reports no forbidden inference reads. Full case and
association comparison follows that freeze. `screenshots.csv` was authored only
after the separate visual access receipt; earlier resource knowledge is disclosed.

`validation01/native-comparison.json` has 20 successful comparison rows: both
representations for captures 299, 325, 696, 716 (Feynman V), 1270, 1280, 1301
(Carinae III-a), and 829, 2881, 2941 (Archimedes III). Each has exactly one match
for resource identity, ordered little-endian binary32 XYZW, native sphere-bound
bytes and callback decision. The three Archimedes controls additionally compare
source identity. An attempted all-ten source-context check encountered the older
seven receipts' missing `source_context` field; their additional source identity
is NOT TESTED. No successful geometry match fills that provenance gap.

All 19 recognized cases and 46 saved association rows are reassessed. Two disabled
rows remain excluded; four of the 17 active predictions remain partial for masks.
The remaining 13 are conditional full model predictions, not complete native
inventories. `cases.csv` records paths, supported resources, additional unverified
resources and failures. `associations.csv` preserves D2/D3/D4E beside D5.
`nine-pairs.csv` contains all nine prior indeterminate pairs. Compared with D4E,
two become conditional positives, seven remain indeterminate, and no prior
positive is lost. Zero diagnostic potential false negatives is not an accuracy
claim or proof of terrain absence. Frozen original outputs remain unchanged;
the preservation audit hashes those baselines rather than replacing them.

## Tests, cost and failures

`checks03/checks.json` and test stdout/stderr retain 15 passing tests: eight
descriptor-order controls, five final raster-stage controls and two source-gate
tests with multiple rejection subcases. They discriminate reversed authoring
order, failed eligible candidates, current-RSGD/current-RNAM precedence,
alternate override substitution, wrong-root fallback, duplicate keys, opposite
masks, boundaries, inverted Y, asymmetric raster dimensions, wrong source/frame,
borrowed query and exception invalidation. They do not exercise retail attachment.
The wrapper's `--help` invocation succeeds without a target.

Canonical payload sizes are 221130 → 221494 bytes. `checks03` independently
calculates the 364-byte delta: bodies +364; generation blocks, schema, source
tables, settings and all other fields +0. Every new block reference already
exists. There is no new numeric field, algorithm change or compression study.
The Feynman/Carinae control corpus is reused byte-for-byte, so its increment is 0.

Failures are retained and corrected within this assignment. Initial module
imports lacked inherited search paths; build01 then referenced the inherited
sorter beside the new script. Build02 corrected the explicit paths; build04 adds
full freeze-input and component-recomputation checks and has identical corpus
bytes. The initial input-ledger import similarly needed owned geometry paths.
Final code audit also found the descriptor refactor had omitted the inherited
nonzero Everywhere rejection. Build04 restores that guard, adds its synthetic
discriminator and produces byte-identical normalized/expanded corpora to the
original frozen build02. The restored guard changes no prediction input/output
bytes. Independent image review corrected one missed overlap-error banner;
the observation index and its manual annotation source now agree with the original.
`checks01` wrongly expected a generation-block delta; inspection established
that only the body projection changes, corrected in checks03. The all-source
identity probe's missing legacy field remains a coverage limit, not a repaired
native observation. No failed attempt is recast as scientific success.

## Reproduction commands

Use installed CPython 3.14.3 at the explicit path below. Default `python` resolves
to an inaccessible WindowsApps alias in this session; no installation was made.
The command list records the actual input/output destinations. For an equivalent
rerun, choose fresh unused destinations and update dependent references; existing
evidence is never overwritten. The inputs-v2/targets freeze originally read
build03, before build04's later byte-identical guard requalification.

```powershell
$d5Python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $d5Python -B research/resource-feynman-d5/audit.py before
& ./research/workshop-population/export.ps1 -OutputName d5-mask01 -Addresses '142339340','142339080','ref:14079f860'
& ./research/workshop-population/export.ps1 -OutputName d5-raster02 -Addresses '1423390f0','1423321f0'
& $d5Python -B research/resource-feynman-d5/corpus.py --base .local-work/resource-slot-provenance/build02/normalized.json --freeze .local-work/resource-slot-provenance/freeze01 --output .local-work/resource-feynman-d5/build04
& $d5Python -B research/resource-feynman-d5/inputs.py --corpus .local-work/resource-feynman-d5/build03/normalized.json --output .local-work/resource-feynman-d5/inputs-v2.json --targets .local-work/resource-feynman-d5/targets-v1.json
& $d5Python -B research/resource-feynman-d5/validate.py --output .local-work/resource-feynman-d5/validation01 --build .local-work/resource-feynman-d5/build02 --controls .local-work/resource-slot-provenance/build-controls02
& $d5Python -B research/resource-feynman-d5/intake.py --archive .local-work/screengrabs/screengrabs-feynman.zip --output .local-work/resource-feynman-d5/screenshots01
& $d5Python -B research/resource-feynman-d5/checks.py --output .local-work/resource-feynman-d5/checks03
& $d5Python -B research/resource-feynman-d5/audit.py after
```

The listed commands group reproducible phases, not execution chronology.
Hash/extract intake did not interpret screenshots; actual pixels were opened
after the prediction freeze. Visual annotations in `tables.py` are manual
observations, not an automated image interpreter. `tables.py` exports bounded
authored CSV summaries and per-use hashes after comparison. Native raw outputs,
images, code bundles, corpora and integrity receipts stay local.

## Authority and acceptance matrix

The before/after audit covers 36604 immutable pins, protected saves/backups and
Git HEAD/index. Its exact results and package hashes are recorded in review.
No retail process was launched, attached, terminated or modified. Existing saves,
definitions, native captures and frozen outputs receive no writes. Ghidra runs
read-only with analysis disabled; no symbols/types/comments are edited.
Screenshot source and extracted bytes match their retained hashes.

| Criterion | Implementer status | Evidence and limit |
|---|---|---|
| AC1 | PASS | Before/after audit, original screenshot hashes, unchanged HEAD/index and no live action. |
| AC2 | PASS | Native instruction chain and all mixed-source inputs; historical query unavailable, localized with specific source-bound acquisition. Partial-resolution clause applies. |
| AC3 | PASS | Conditional initialized traversal and explicit failures/first success; historical native component population unobserved. |
| AC4 | PASS | General resolver, unchanged geometry/code, synthetic discriminators and canonical +364-byte accounting. |
| AC5 | PASS | Full 19/17/46 cohort, all nine pairs, ten original geometry controls; additional source identity available for three controls only. |
| AC6 | PASS | All 24 images hashed/read/indexed after freeze; descriptor resolution plus exact query/cache dependency and discriminating source gate/card. |
| AC7 | PASS | Native/source/operand ledgers, tables, failures and complete editorial finalization recorded in editorial.md. |
| AC8 | PASS | Independent review04 ACCEPT, exact 37/36-file patch verification and separately reviewed closure delta; authoritative records are in review.md and local receipts. |

The matrix reports implementer checks; it is not an independent acceptance
certificate. Review disposition, scientific partial resolution and integration
permission remain separate. Seven mask pairs require new evidence under a
separately approved live decision. No image redistribution, publication, staging,
commit, push or production-tool integration is authorized.
