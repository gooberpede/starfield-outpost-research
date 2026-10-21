# B5-A storage, retention and scratch lifecycle

2026-10-21, Australia/Sydney. **B5-B is deferred until after release.** No deletion
is authorized. Publication remains NOT CLEARED under its separate gates.
The [maintainer correction](delivery-correction.md) amends the
[original brief](../../implementation-briefs/CODEX_BRIEF_SOR_B5_A_local_work_inventory_scratch_lifecycle.md).

The completed inventory measured **33,963,351,165 logical bytes (33.96 GB),
90,914 files and 12,951 directories**. The recorded proposal covers **7,657
duplicate review-copy files totaling 192,761,272 bytes (192.76 MB)**:
180,674,816 bytes had no exact reference hit in the original audit scope;
12,086,456 bytes were reference-blocked. Another 29 empty Temp trees contain
zero file bytes. These are historical conditional estimates, not current deletion
clearance or guaranteed reclaimed disk space. **No pre-existing files were deleted.**

Large retained consumers include the 12.31 GB Workshop inventory, 3.94 GB preview
research, 2.58 GB position-write history, 2.36 GB membership archive and 2.05 GB
robot research. They contain original WALs/captures, distinct failed/corrected
analyses, saved-state archives and historical methods useful for follow-up.
Newer summaries do not replace those inputs. The broad 1.78 GB robot acquisition
preserves different coverage from its narrower final acquisition. Original crash
collection evidence, donor material, B3 historical source and B4-F1 assets and
constituents remain retained; installed tools/game and external analysis are
outside cleanup scope.

All four protected roots remain: `diffs/` (172,744,709 bytes), `scratch/`
(228,626 bytes), `screengrabs/` (15,749,839 bytes) and `savegames/`
(199,457,731 bytes, 54 files), under `.local-work/`. None of their contents was
proposed for removal. Their usable local scaffolding must also survive any
later approved cleanup. Exact object comparison found 450 objects / 446 hashes;
the four equal pairs preserve original candidate/frozen-control contexts.
No build object is proposed for deletion.

## Retained audit and verification

- [Retention ledger](retention-ledger.csv), [HOLD inventory](hold-inventory.csv),
  [large duplicate groups](large-duplicates.csv), [build accounting](build-output-accounting.csv)
  and [proposal totals](reclamation-ranked.csv) retain the substantive audit.
- [Reference impact](reference-impact.md) preserves the bounded dependency study:
  41,839 text files / 19,755,517,096 bytes, 10,868 candidate-path hits, all hits
  blocked. Dynamic-path and encoding limits remain explicit.
- [Scratch lifecycle](scratch-lifecycle.md), [creator inventory](creator-inventory.csv)
  and [frozen creators](frozen-creators.csv) document ten exporter repairs and
  historical entrypoint retirement. The original twenty normal/exception scratch
  cases and four successor control-flow cases passed; their results remain
  preserved. [Test sources](test_scratch.py) and [successor tests](test_successor.py)
  are retained. No inventory, candidate assessment or synthetic execution was
  repeated for this delivery correction.
- [Review](review.md) preserves the original AC1–AC8 ACCEPT and its coverage
  limits: all initial metadata and 167 selected protected pins checked, exact
  source identities preserved, no second whole-workspace byte rehash or live
  validation claimed. [Owned local methods](local-methods.csv) retain provenance.

## Local-only proposal and deferred B5-B

The detailed manifest is **temporary local working material**, retained unchanged
at `.local-work/b5/deletion-candidates.json` (24,999,423 bytes), SHA-256
`e44336fadbe7d95a15180b4e06b73bcf680d320a426980af795a67d582d8b9e0`. It is excluded from the proposed tracked tree, review diffs and
public checkout; no public download is promised. [The optional validator](check.py)
requires that local file and is not a checkout-only reproduction path.
The tracked proposal ledger supplies totals rather than enumerating candidate IDs.

**B5-B is deferred until after release**, and release itself grants no deletion
authority. Any later cleanup needs a fresh bounded proposal, current identity,
reference, recovery, reparse and C:/D: space-guard checks, independent review and
new explicit maintainer approval. The old local manifest is provenance, not a
ready-to-execute cleanup list. [Deferred safety conditions](b5-b-plan.md) remain.

## Corrected delivery

Corrected complete/task-only patches are
`.local-work/diffs/b5-corrected-complete.diff` and `b5-corrected-task-only.diff`.
Their file hashes, included/excluded inventory, exact forward/reverse checks and
status are in `.local-work/review-deliveries/b5-corrected.json`. Both exclude the
local manifest. Complete includes the unchanged supplied brief; task-only covers
the combined B5-A work and this correction, excluding that brief. Earlier review
packages remain historical local receipts, not the proposed release contents.
The focused correction review is retained locally as
`.local-work/b5/independent-review-corrected.md`; integration remains separate.

Suggested commit: `chore: audit local-work retention and fix review scratch lifecycles`
