# Workshop relocation, persistence and bounds — review package

SOR-EXP-0017 / SOR-EV-0025, 2026-10-10. **Critical review pending.** [Answer-first report](../workshop-origin-beacon-relocation-persistence.md), [invoked brief](../../implementation-briefs/CODEX_BRIEF_SOR_workshop_origin_beacon_relocation_persistence.md), SOR-D-0036. Authored interpretation/selected evidence REVIEW-REQUIRED; original captures/saves/decoded buffers/full native exports LOCAL-ONLY. No staging, commit, push, launch, deployment or debugger actions performed.

The strongest result is the sampled typed compensation/serialization chain: Workshop::ExtraData +0x60 is a three-float delta, explicit native saver/loader carries its 12 bytes, framed Save26 and reacquired captured state agree, and the compensated center feeds border/terrain consumers. STRONG scoped semantics proposed, with PROVEN selected bytes/arithmetic. Ordinary beacon definition radius is 150 native units; 71.40000152587890625 is a separate configurable fallback. Effective live radius, metre conversion, universal authority/coverage and exact planetary beacon position remain open.

## Selected reviewable evidence

- [Capture ledger](captures.csv): 18 observations / nine snapshots, exact UTC read times, reference identities, raw roots/file/hash locators, float bits, type/vtable and stable fields. Resolve files under ignored `.local-work/beacon-observer-live/session-17596-91165828/LABEL/`; runtime pointers remain in local receipts. Guarded reads are non-atomic.
- [Native map](native-map.csv): typed data flow, decisive static VA sites, roles and limits. Static base 0x140000000; subtract it for RVA. No cross-build addresses or callable integration claim.
- [Save transitions](transitions.json): selected framed Save25/26 token/parent/XYZ/Workshop offsets and exact field changes. Offsets are decoded-stream bytes; runtime offsets and compressed offsets differ.
- [Independent controls](independent-controls.csv): original/decoded identities, actual supported zero-resource results and unsupported resource-bearing records.
- [Native exports](native-exports.csv): identities of ignored full exports/logs, including failed project-lock attempt and successful retry. Inventory is exploratory, not exhaustive typed analysis.

## Reproduction and local receipts

From repository root, using installed CPython 3.14.3 (no new dependencies):

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_workshop_origin.py --run REVIEW-UNIQUE
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_workshop_bounds.py 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe' 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm' '.local-work/workshop-origin/REVIEW-UNIQUE/bounds.json'
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
```

Use a new alphanumeric/hyphen run name. Exact local archived Save25/26 are resolved from `.local-work/beacon-observer-live-review/initial-01/final-summary.json`; this also locates pinned source identities. Session/raw manifest, installed sources, existing Ghidra project and `.local-work/save-capacity-location/esm-index-verified.json` are prerequisites. Run without `-O`: assertions enforce evidence checks. Decoder creates/removes temporary disk-backed scratch; 40,000,000,000-byte C:/D: floor enforced. JSON/raw definitions stay ignored. Unsupported variable Workshop resource tables are reported, never guessed. The prefix reader does not decode following extras or prove complete save semantics.

Actual principal receipts: `.local-work/workshop-origin/final-03/{before,captures,saves,transition,preservation,tools,independent-controls,instruction-bytes,final-preservation}.json`; exact radius evidence `.local-work/workshop-origin/run-02/bounds-final.json`. Retained task-local original scripts `finish_evidence.py`, `update_records.py`, `package_review.py` and `final_checks.py` under `.local-work/workshop-origin/` reproduce packaging, archive challenges and review checks; their hashes are in the final local file inventory. Earlier exploratory run-01/run-02 remain local and are not substituted for final evidence.

Read-only native inventory can be reproduced serially (never concurrently against the same Ghidra project):

```powershell
./ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -Reader WorkshopOriginRefs.java -OutputName workshop-origin-review-unique.tsv -Addresses @('140000000','143800000')
```

Existing `OutpostRecon.java` exported identified functions/call sites using the wrapper's address/full-function syntax. Full exports/local commands and logs remain private; the report identifies decisive functions and separate instruction windows. Existing 600-instruction display limits on some large functions are disclosed; full decompilation and cap-free decisive windows support the positive claims. Project DB preservation baseline was taken after the first new export, so it cannot retrospectively bracket that first export. No analysis state was edited.

## Checks and change set

83 Python tests pass (six new parser scope/error tests). Fresh nine-snapshot arithmetic, 5,265 session-file hashes, four Workshop prefixes, original/decoded Save25/26 identities, independent archived controls, installed ESM/PE constants and decisive instruction-byte reads pass. Twenty protected baseline files and both available original saves pass final preservation. No full-record/whole-format completeness or live effective-radius check is implied.

Local `.local-work/workshop-origin/final-03/review/` contains **complete.diff** (all tracked modifications and every untracked deliverable, including the supplied brief), **task.diff** (excludes the unchanged supplied brief), file inventory, validation receipts and final `git-status.txt`. Diffs include unstaged/untracked content without staging. Raw saves, memory, binaries, analysis DBs, full native exports and scratch are excluded. Final Markdown local-link, UTF-8/LF, Python syntax, `git diff --check`, HEAD/index/status and deliverable-extension checks are recorded there.

Changed source: two original Python research probes, six synthetic tests, original Ghidra instruction inventory and wrapper allow-list. Durable records: report and this selected-evidence package; README/research/subsystem state; decision/provenance/source/credits; facts/state/functions/hypotheses; experiment/evidence/brief indexes and script documentation. The supplied brief is retained without edits. No external reuse/permission issue arose; existing separate-tool and observer lineage credits remain mandatory and recorded.

Recommended next step is critical review of this package. If approved and separately authorized, the report proposes a bounded live observation of the effective descriptor/getter values and coordinate frames; no live action follows from this handoff.

Suggested commit after review:

```text
research: trace workshop relocation offset and outpost bounds
```
