# EXP0021 review receipts and handoff

Authored work REVIEW-REQUIRED; raw game/save/memory/analysis evidence LOCAL-ONLY.
[Answer-first report](../durable-position-engine-oracle.md),
[retained authorization](../../implementation-briefs/CODEX_BRIEF_SOR_durable_position_engine_oracle_algorithm_reconstruction.md).
This package is offline preparation; no independent retail oracle result exists.

## New and changed work

- Original saved-position model, input adapter and eight tests under
  `save-analysis/scripts/`; selected23 inputs/predictions and algorithm specification.
- Native typed contracts, dependency ledger, sibling methods/revisions,
  validation protocol and prospective operator card in this directory.
- Observer0.1.1 adds native stored center/radius/flags acquisition and inspection,
  independent sentinel fixture and build guards; prior0.1.0 records unchanged.
- Original disposable natural-output contract/fixture/qualifier and three decoder
  tests under `debugger/engine-oracle/`; two-thread and zero-hit controls.
- Research state, sources/credits/provenance, decision0040, finding0028,
  function0054/55, state0026 and subsystem/index links updated. Existing classifications
  retained. The supplied brief remains unchanged and is excluded from authored diff.

Complete exact changed-file inventory, SHA-256 manifest, all tracked **and new**
authored diffs and Git status are in local ignored
`.local-work/engine-oracle/review.json`, `complete.diff`, `status.txt`.
Final review covers37 authored files and490 internal relative file links, with
zero reported issues. A local `review-package.zip` bundles these sources, the
unchanged supplied brief, GPL text and selected review/test/build receipts;
it excludes game binaries, saves, Ghidra exports/databases and runtime memory.
`review_work.py` is the original local receipt builder (stdlib/Git only): reads
sources/protected inputs/Git and writes these ignored receipts; no staging,
target access or network. Consulted sibling file hashes and normalized committed
content equality are in `sources.json`; native export hashes are in `review.json`.

## Actual qualification

Installed CPython3.14 standard library and existing project arithmetic only:
`python -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'`
passes **129 tests** (121 existing plus eight new).
`python -B -m unittest discover -s debugger/engine-oracle -p 'test_*.py'`
passes **three**. Transcripts: `save-tests.txt`, `contract-tests.txt` under the
local receipt root. Frozen predictions are freshly regenerated in-memory from
selected inputs and compared exactly; real CLI example output is also checked.
All23 center bits/cells/floor/residualXY also match EXP0020's separate prior
table. These are model/decoder regressions, not independent oracle comparisons.
Frozen input SHA-256:
`9fe2924ff7bc444714fbab685893b8d8e0572dc2c7aad96cbd06de8aac93ad91`;
prediction SHA-256:
`a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487`.

Observer build `.local-work/beacon-observer-builds/engine-oracle-011-02/build.json`
records exact sources/toolchain/pinned executable/SFSE/guard windows and package
members. **0.1.1 DLL SHA-256**:
`4ae2a1e329a498b12352f4145db546fdb1317048dced5dede8c16f3fabe30504`.
**SorBeaconObserver-0.1.1.zip SHA-256**:
`9570c9da1b206c6b611e31273e71b5cf84b10e10b6b7fc2e479e7aa1fd445023`.
565 fixture JSON rows; raw hashes, partial/recovery, request controls, independent
native stored-output copying, offline inspection and decoded-fields/corruption
checks PASS. Package is prepared only, not deployed or retail-qualified. Earlier
011-01 build is retained historically; 011-02 includes the final observer README.

Disposable debugger0.1.0 current-source receipts:
`.local-work/engine-oracle/qualification-03/result.json` and
`qualification-zero-02/result.json`: PASS, two different threads versus zero hits,
32 original site bytes restored, detach independently verified, normal fixture
exit0. Raw transport logs flush durably. Existing x64dbg/MSVC run separately;
no third-party code is embedded. This tests sentinel capture transport and
cleanup, not the real game's layout/ABI, reachability, timing or equivalence.
Earlier qualification-01 did not verify restoration before target exit; it is
retained as an incomplete control, superseded by02/03, not counted as sufficient.

## Preservation and validation limits

Original41-file protected snapshot is freshly rehashed before/after task in
`before.json`/`preservation.json` (hash, size and mtime), including PE/ESM/saves/
Ghidra persistent files. All41 content hashes/sizes agree. Four Ghidra `~index.dat`
and `~index.bak` files (idata/versioned) have refreshed modification timestamps;
their bytes are unchanged. Timestamp differences are retained, not silently
normalized or reported as full metadata equality. Save25 original SHA-256
`d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`;
Save26 original `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104`.
Fresh original `research_workshop_origin.py --run engine-oracle-preservation-02`
verifies **5,265 prior observer-session files**, re-extracts the two protected
saves with identical decoded hashes and matches18 beacon observations across
the nine old captures. Receipt remains in
`.local-work/workshop-origin/engine-oracle-preservation-02/`;
console transcript is `preservation-run.txt` in the engine-oracle receipt root.

The first preservation rerun overlapped a read-only Ghidra export and failed
because a transient database `tmp14845426821272294856.ps` disappeared between
enumeration and rehash. That incomplete run is retained as
`engine-oracle-preservation-01`; it is not a successful preservation check.
The successful rerun waited until Ghidra exports closed; persistent-file equality
is checked independently against the pre-task snapshot. Read-only exports do not
authorize symbol/type/comment changes. Free space remains above40,000,000,000
on C: and D:; exact final values are retained in review/build receipts.

Git diff whitespace, authored-file trailing whitespace/UTF-8, internal relative
file links, ignored raw/build artifacts and unchanged HEAD/index are checked by
the receipt builder. Link checks cover path existence, not remote URLs or Markdown
anchor semantics. No network-enabled CI, download, install, Starfield launch,
live attachment, save/config mutation, stage, commit, push or external disclosure.
No third-party permission issue blocks this offline package: maintainer-owned
conceptual methods use SOR-P0002; approved SFSE interface/notices remain unchanged.
Publication review remains separate from confidence and is not granted here.

## Remaining work and proposed commits

Critical review must assess stored output freshness/active identity and the frame
comparison before authorizing the passive run card. Raw-angle bit-exact site
quantization, future activation/rebase prediction and natural callback live
reachability remain explicit dependencies. A center-only pass cannot validate
the planetary grid or universal placement. No task expansion follows automatically.

Suggested commits after review (none created):

```text
research: reconstruct saved outpost position and specify native engine oracles
feat(observer): capture native stored workshop center and qualify acquisition
```

Alternatively combine as `research: reconstruct durable outpost positioning and prepare engine oracle`.
