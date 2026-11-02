# D5AE offline methods and tests

2026-11-02. [Contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AE_GC10_construction_winner_scheduling.md),
[ledger](d5ae-investigation-ledger.md), [sources](d5ae-sources.csv).
Raw evidence, native bytes/exports and private receipts remain LOCAL-ONLY.

## Experiment boundary

Allowed actions are read-only existing evidence/binary analysis, exports from
the verified disposable Ghidra copy, owned offline models and disposable native
instruction fixtures. Inputs are the pinned installed executable/content,
selected original/copy core hashes, protected Save52 research copy and B1/B2
evidence. Outputs are fresh ignored receipts, local exports and authored text.

Risks are wrong alias/control-flow inference, ABI faults inside disposable
fixture processes, accidental original-project access, disclosure and scratch
growth. Stop affected work on identity/ABI/oracle failure, failed disk query or
caller-available free space below 40,000,000,000 bytes on either C: or D:.
No elapsed-time or evidence-volume cutoff is used. No live process is attached,
launched or terminated. No protected input/configuration/database is edited.
Native process exit frees fixture memory; original captures and failed receipts
remain retained. The review exporter removes only its verified owned temporary
application tree under `.local-work/review-patches`.

## Reproduction

Use installed CPython with `-E -B`; the Windows application alias failed before
execution. The working interpreter is
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, whose exact
version/hash is recorded in `inputs01.json`. All outputs below must be new.
Commands are relative to the repository root and require retained local inputs.

```text
research/resource-retained-population/d5ae_baseline.py NEW-INPUTS.json
research/resource-retained-population/d5ac_reconstruct.py .local-work/d5ac/NEW-AE-RAW
research/resource-retained-population/d5s_controls.py replay --output .local-work/d5ae/NEW-SCHEDULER
research/resource-retained-population/d5w_native.py .local-work/d5ae/NEW-INCREMENTAL.json
research/resource-retained-population/d5ad_readiness_control.py .local-work/d5ae/NEW-READINESS
research/resource-retained-population/d5z_append_control.py .local-work/d5ae/NEW-APPEND
research/resource-retained-population/d5ae_controls.py .local-work/d5ae/NEW-PREDICATES
research/resource-retained-population/d5ae_rank_control.py .local-work/d5ae/NEW-RANK
research/resource-retained-population/d5ae_export.py NEW-EXPORT EXISTING_STATIC_FUNCTION_VA
research/resource-retained-population/d5ae_sources.py .local-work/d5ae/NEW-SOURCES
```

The final source command regenerates the authored locator CSV as well as writing
its local receipt. Its implementation pins inherited source rows and refuses a
missing function or mismatched export. The export command passes only
`D:/tools/sor-d5ad-ghidra-project` to Ghidra, with `-readOnly -noanalysis` and
isolated cache/log/temp directories. It hashes original and disposable core files
before/after. Temporary Ghidra housekeeping is confined to the disposable copy;
no symbol, type or comment edits are performed. Ghidra/JDK are separate installed
tools, not incorporated dependencies.

## Results and limitations

| Test | Result | Exact evidence and scientific limit |
|---|---|---|
| Initial baseline | PASS after correction | `.local-work/d5ae/baseline.json` freezes clean HEAD/index plus supplied brief. First adapted selected-input run used a wrong brief basename and failed before receipt creation; corrected `inputs01.json` authenticates 54 selected inputs. This is not a full active-save preflight. |
| B2 authentication | PASS | `.local-work/d5ac/d5ae-reconstruction01`: all 32,141 frames, fixed-offset/owned-decoder agreement, CRC/sequence, unchanged reader equality, exact target/epoch joins. Three damaged input controls reject. Zero qualified cold chains and 97 adjacent admission/QPC inversions remain. |
| Native scheduler/generation replay | PASS | `.local-work/d5ae/d5s-replay01/replay.json`: eleven retained methods rerun in separate processes and agree numerically with originals. Includes registration, actual queue/dispatch, query conversion, first-resource geometry, spatial and retirement controls. This is not execution of every full engine node. |
| Incremental queue challenge | PASS | `incremental01.json`: twelve native dispatcher/claim cases across six activation batches and owner/peer routes. Batch 1 agrees on `(-2,11)`; full batch gives `(10,11)` versus `(-2,-2)`; owner batch 875 gives `(-2,-2)`. Successful allocator/TLS/five empty context fixtures and callback tokens substitute for full engine state. |
| Readiness helper | PASS | `readiness01/control.json`: six original `0x1427d4be0` uncontended entry-state cases. No waiting loader, stream decode or real concurrent file load executes. |
| Visited reserve helper | PASS | `append01/control.json`: six original `0x1422cc0d0` index/count/sentinel cases, including failed initialize/grow callbacks. No full engine allocator/OOM recovery is claimed. |
| Arbitration predicates | PASS | `controls03/controls.json`: seventeen synthetic source cases, six node predicate cases and fourteen raw B2 boundaries. Reverse map acquisition, pending A, startup admission suppression, missing metadata/raster refusal, post-authority delay, populated cache, failed reserve, returned-empty generation, Grid versus broad reset, other owner/pointer/token and aggregate reuse are explicit. These are branch/state controls, not executed native concurrent arbitration. |
| Rank/serial bound searches | PASS | `rank01/control.json`: 42 original native helper cases with empty/nonempty arrays, equal-rank serial ties, mixed ranks and unsigned maximum operands. Independent Python tuple-order indices agree; inputs remain unchanged. These execute the comparison helpers, not the whole tree or scheduler. |
| B1/B2 chronology cross-check | PASS | `.local-work/d5ad/d5ae-chronology01/chronology.json` authenticates both historical captures/checkpoints and nine adverse chronology cases. B1 losses and unrecorded caller/readiness fields remain limits. |
| Source lifetime | PASS within inherited fixture | D5S replay preserves 37 small shifts and retires on shift 38 with Grid refcount 2. Terminal free is a fixture recording callback; actual erase/unlock/free is static. This is not an observed retail dangling-pointer crash. |

Map-holder allocation failure is explicitly outside successful-allocation
controls: the native branch can continue with a null wrapper toward a later
dereference, so safe retry is not inferred. Failed/partial geometry does not
prove failure of holder insertion or visited append. The source-informed
predicate model keeps these distinctions and makes no probability claim.

Method lineage is maintainer-owned D5S/W/Z/V/AA/AC/AD under SOR-P-0002.
Bethesda native bytes/content and B1/B2 observations remain attributed primary
inputs; existing third-party notices are unchanged. No new implementation,
licence basis, dependency, external contact or publication permission is used.


## Preserved diagnostic failures

Export04's launcher returned zero but its script failed on an undefined getter
function; the missing terminal END caused the owned exporter to refuse success.
Completed export05 repeats the preceding consumer windows. Getter bytes and
priority vtable slots are verified directly through the owned PE reader without
creating a database function. Preliminary source-locator runs refused missing
entries because a getter was data rather than a defined function and D5AA used
its `locator` column instead of `static_va`. The corrected source method handles
both explicitly; no failed source inventory is called complete.

Controls01 predates node cases; controls02 predates the explicit sample/map-key/
token-store assertions. Controls03 is the final qualified method. Earlier outputs
remain retained with their actual script hashes. The constructor-rank/count
misinterpretation was corrected from new primary exports; it is preserved in
the active ledger rather than hidden in the final synthesis.
