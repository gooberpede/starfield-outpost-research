# Reproduction, chronology and check limits

2026-10-24, Australia/Sydney. [Report](report.md), [sources](sources.csv).
Receipts below are relative to ignored `.local-work/resource-save52/`.
The installed interpreter is
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, CPython 3.14.
No dependency was downloaded or installed. Existing Git performs read-only
identity/diff checks and applies patches only to disposable comparison trees.

## Original execution and failure history

1. `save52.py inventory` wrote the protected audit and `inventory-v1.json`.
   It recognized 19 cases but correctly rejected all site-relative frames on
   the initial source-frame-only adapter. This was an adapter limitation,
   not evidence of unsupported planetary geography or absent outposts.
2. `save52.py qualify` used the established site-centre/frame route, independently
   checked framing/detection and wrote `inventory-v2.json`. All 17 eligible
   cases have supported static interior inputs. The original inventory remains.
3. A one-line projection command wrote `requests-v1.json`: only case ID, control
   flag and exact D1 request. The final equivalent `requests` stage additionally
   writes a separate inventory/roster hash receipt for future runs; that receipt
   did not exist for the original run and is not retroactively claimed.
4. `save52_corpus.py` wrote `build-v1`. The immutable corpus file SHA-256 is
   `c0002efbf174094d942a96f154b1ff6c4170a5732277bf43396814172777dade`.
   Preparation added no new schema field or numerical rule. All field lineage
   and original builder/owned-selection pins are in its manifest.
5. `save52.py predict` launched 17 fresh `-I -S -B` processes through the unchanged
   D1 isolation helper. Every request, stdout, audit and freeze remains local.
   Input freeze precedes prediction; final freeze time is
   `2026-10-23T23:16:06.777525+00:00`. Each run has eight denied probes and zero
   forbidden inference accesses. Current source EXE/ESM, raw saves, caches,
   native answers and expected geometry were unavailable to inference.
6. `comparison-v1/answer-access.json` records first comparator launch at
   `2026-10-23T23:17:01.458433+00:00`. That attempt failed with `KeyError:
   saved_reference`: the adapter used the wrong owner-summary key. It produced
   no comparison verdict. The owner field was corrected to `owner_identity`.
7. `comparison-v2` completed. `comparison-v3` then added exact equality between
   inventory-derived case/control/requests and the frozen roster. Counts are
   unchanged: 16 positive, one candidate, 18 indeterminate and four alternative
   held-out pairs. No predictor rerun or answer-informed input change occurred.
8. `diagnostics-v1` independently checked seven native paths, full control
   geometry and manual membership. `diagnostics-v2` added source-class details;
   its property-value list was mistakenly empty because a diagnostic tag was
   compared as text instead of bytes. `diagnostics-v3` corrects that ancillary
   read and records both Water-base atmosphere values as 1.0. The comparator
   already used the correct decoded string-tag definitions; no outcome changed.
9. Wrapper CLI options and the equivalent request-projection stage were added
   after science for reproducibility. They do not modify the copied D1 predictor
   or frozen results. The original corpus-builder manifest pins its executed
   source version; the final source ledger/delivery manifest pin current code.

All earlier incomplete/failed outputs remain. Interactive diagnostic commands
also exposed one console encoding error while displaying installed metadata
and one unsuccessful lookup for a nonexistent no-family example. Neither wrote
predictions, altered evidence or supplied a scientific verdict.

## Repeat on a fresh ignored root

These commands reproduce the final equivalent pipeline. Use a root that does
not already exist, from the repository root; defaults refer to the original
immutable run and therefore refuse existing outputs. Installed data and existing
protected fixtures must match the source pins. Outputs stay local; temporary
decoded scratch is cleaned by the existing mapped decoder. The offline decoder
uses an infinite time deadline while retaining bounded framing/allocation and
both-drive free-space protection. No scientific event/time quota is introduced.

```powershell
$d2Python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$d2Root = '.local-work/resource-save52-reproduction'
& $d2Python -B research/resource-standalone/save52.py inventory --root $d2Root
& $d2Python -B research/resource-standalone/save52.py qualify --root $d2Root
& $d2Python -B research/resource-standalone/save52.py requests --root $d2Root
& $d2Python -B research/resource-standalone/save52_corpus.py --root $d2Root
& $d2Python -B research/resource-standalone/save52.py predict --root $d2Root
& $d2Python -B research/resource-standalone/save52_compare.py --root $d2Root --run comparison-v3
& $d2Python -B research/resource-standalone/save52_diagnostics.py --root $d2Root
& $d2Python -B -m unittest discover -s research/resource-standalone -v
```

The seven native captures are independently parsed with sequence, digest and
ACK validation, not accepted from an old summary. Their resource identities,
native bound bytes and ordered XYZW bytes each match exactly one predicted path.
All 1429 control path identities/geometries equal the original D1 output order.
This is deterministic fixture regression, not new native sampling, native census
or proof that all additional paths are correct. Callback/placement/throughput
equivalence outside D1's previous checks is not newly asserted.

The 23-test suite contains the unchanged 16 D1 tests and seven D2 boundary tests.
`tests-final.txt` retains the actual final run. These synthetic tests cover
taxonomy and label-dropping mechanics; primary Save52 scans and native byte
comparisons provide the real-data checks. No test turns a plausible output into
an exhaustive availability oracle.

## Preservation and delivery

The initial and final broad protection audits apply the existing prospective
save policy. Reliably classified active autosaves/exitsaves are diagnostic;
designated research/manual/quicksaves, historical archives, backups and
unclassified files remain strict. Old manifests and historical discrepancies
were not rebaselined. `protected-before.json` and `protected-after.json` retain
the actual inventories. The separate 21,857-file frozen-evidence inventory was
verified against its original pins before comparison and checked again after
science; see `frozen-verified-before-comparison.json` and `frozen-after.json`.
Both broad audits covered 12,974 entries and reported zero current protected
changes. All 21,857 frozen files matched before and after the comparison/tests.

The protection audit does not establish game semantics. Final HEAD/index/status,
complete and task-only patch hashes, inclusion/exclusion inventory and exact
forward/reverse reconstruction checks are in the [review package](review.md).
No staging was used to export untracked text. Raw saves, full generated payloads,
memory/native captures, analysis databases, private network data and ignored
receipts are excluded from the text patches; exclusions are not publication
clearance. Full corpus/raw-source reproducibility requires authorized local access.
