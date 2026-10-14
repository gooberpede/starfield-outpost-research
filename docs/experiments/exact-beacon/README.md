# SOR-EXP-0015 review package

2026-10-09. **Critical review required; exact continuous beacon coordinates remain OPEN.** [Answer, formula, data flow, hypothesis tests, counterexample, prior art and next discriminator](../exact-beacon-planetary-coordinates.md). SOR-EV-0021 / SOR-F-0020 / SOR-H-0009 / SOR-ST-0020. Scientific confidence and publication eligibility remain separate.

Recovered native/default grid projection reproduces 22 beacon-associated angular pairs and three fixed cities; controlled Save25/S1 differences give the same candidate grid origin without fitting. World/cached-frame selection and fractional XYZ embedding remain unvalidated. Full requested Reddit reading was blocked by primary-source access errors. No live work, staging, commit, push, external disclosure or automatic integration approval.

## Files and evidence

- [Validation matrix](matrix.csv): 22 beacon/site pair rows and three fixed ESM rows; body/token identities, half-integer residuals, angular errors, local split and explicitly **candidate** origins. Not exact beacon coordinates.
- [Initial flags](initial-flags.csv): 22 selected records across Save25, S1 and all 19 Save52 candidates, including two disabled-set records without direct pairs. Shape/flag offsets are decoded logical offsets. This flag ledger has different coverage from the angular matrix.
- [Native export hashes/caps](native-exports.csv): 17 batches, exact function/window VAs, export/log hashes, incomplete-function/cap diagnostics. Raw exports/logs under `.local-work/recon/`, LOCAL-ONLY. Batch 04 failed after two setting initializers because PowerShell parsed an unquoted address as scientific notation; batch 05 quoted retry recovered the intended functions. Batch 12 completed its nine function exports but failed at an invalid instruction-window centre; batch 17 recovered windows at verified existing call instructions `141834c0a/141833eb3`. Batch 15 large decompilation cap retained. Ordinary 24-xref caps are not exhaustive; batch 16 explicit `refall` projection inventory avoids that cap but includes only references already in the database.
- [Local receipts/helper hashes](local-artifacts.csv): ignored extraction, numerical, preservation and inspection materials. The selected ledger contains locators/hashes, not proprietary raw text.
- [Exact changed-file inventory](changed-files.csv): task outputs plus the supplied pre-existing brief, with content hashes. The inventory excludes its own hash to avoid self-reference; it is itself included in diffs/status.
- Original [projection model](../../../save-analysis/scripts/beacon_terrain_projection.py), [receipt audit runner](../../../save-analysis/scripts/audit_beacon_projection.py), [analytical tests](../../../save-analysis/scripts/test_beacon_terrain_projection.py); small existing Ghidra reader `refall` extension. Source-informed mathematics, not copied native source/decompiler text or an exact-beacon API.
- Durable finding/hypothesis/state/function/source/provenance/decision/subsystem and script/brief/experiment indexes updated; prior evidence/history retained. Supplied brief retained unchanged. No third-party implementation or new dependency incorporated.

## Actual checks and their limits

`python -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'`: **77 tests pass**, including five new mathematical tests (36 sphere-roundtrip cases, explicit axes/tags, grid quantization, negative/boundary float split, invalid inputs). These check numerical implementation and existing analysis behavior; they do not validate runtime frame authority, all native rounding, saved wire semantics or continuous residual embedding.

Fresh `research_two_outpost_anchors.py --run exact-beacon-01` extraction yields Save3 zero, Save25 two, S1/S1C/L2C one each, Save2 zero ordinary candidates, Save52 nineteen (17 clear/two set). The existing independently authored arithmetic/framing checks and frozen decoded identities in that runner pass. Mature network JSON body/system cross-check passes 17/17 **after** save extraction; it is not a coordinate source. New projection audit runs01/02 agree numerically; run 02 only changes CSV line endings. All 25 available pairs reproduce; two set records without pairs remain missing coverage. New runner input SHA-256 values equal before/after. Fixed ESM numeric controls are from prior qualified exports and fresh existing extraction comparisons; no fresh full xEdit session is claimed.

Final source/content/archive checks: **16 recorded input identities match** size/hash/mtime; includes Save25 original/copy, available source/control archives, executable, ESM, catalog/frozen receipts and manually maintained network. S1/S1C/L2C original files are absent at frozen paths; archived hashes and decoded identities match their manifests instead. Access-time preservation and complete historical configuration are unproven. The audit also preserves its two receipt/CSV inputs. No original save is written.

**15 Ghidra project-file hashes/sizes unchanged** against the task snapshot; all 15 also match the earlier EXP0013 preservation manifest. Snapshot was taken after batch 01 began, so it alone cannot establish pre-batch 01 preservation. The earlier matching manifest supplies an additional historical reference, not an invented task-start snapshot. Launches use `-readOnly -noanalysis`; no symbols/types/comments/bytes edited. Logs and partial exports retained. Initial and final disk free space exceeds 40 GB on C/D.

Final `git diff --check` and equivalent untracked-file checks: PASS. Local Markdown file/heading link checks: **382 targets, zero errors** for changed/new docs; baseline 342 targets also zero errors. These validate resolvable local targets, not internet availability or case-sensitive portability of untouched historical links. Inventory covers 26 files (25 task outputs plus supplied unchanged brief). Changed-file contents were inspected for raw/proprietary payloads: selected authored numbers/docs/scripts only; raw saves, decompressed streams, native text and DBs remain ignored/local. No network-enabled CI/upload executed.

## Review artifacts and script effects

Ignored downloadable review artifacts, recreated against the final working tree:

- `.local-work/exact-beacon/task-only.diff`: all task modifications/new files, excludes supplied unchanged brief.
- `.local-work/exact-beacon/complete.diff`: includes supplied pre-existing brief and all working-tree changes, including untracked files. No staging/index manipulation used.
- `.local-work/exact-beacon/git-status.txt`, `diff-check.json`, `links.json`: actual status/whitespace/local link results.
- `.local-work/exact-beacon/final-input-preservation.json`, `database-final.json`, `previous-database-comparison.json`: exact local integrity receipts.
- `.local-work/exact-beacon/audit-02/summary.json` and `matrix.csv`: fixed native-derived N, actual maxima and input hashes.

Local original inspection helpers retained with hashes: `probe.py` reads installed PE sections/constants, writes its own numeric/byte receipt; `frames.py` reads verified archives with disk-backed decoder, hashes before/after, writes local initial flags/cache context, and cleans only decoder scratch; `numeric.py` reads extraction JSON and mathematical module, writes its own local numerical receipt. `package.py` reads Git/files/receipts, hashes source/database content and writes selected ledgers plus ignored review diffs/checks; no index/commit/network/target/database write. All use existing CPython stdlib and project-owned readers; no dependency acquisition. Raw helper outputs containing neighboring save/native bytes are LOCAL-ONLY. Model has no I/O; public audit reads only two authored/extraction receipts and writes a new directory after 40 GB guard. Existing protected-copy extraction tool effects remain documented in its source/README.

Publication gates: all authored output REVIEW-REQUIRED. Full native evidence/local raw data cannot be staged/disclosed merely because hashes/summary pass. No rights-holder contact, PR, fork or permission request; inaccessible source authors are not invented. Critical review must decide semantic integration and whether further offline decoder work or a separately approved live discriminator is warranted.

Suggested commit message **after review**, reflecting the incomplete exact-coordinate result:

```text
research: recover beacon terrain projection and bound exact coordinates
```
