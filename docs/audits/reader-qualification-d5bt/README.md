# D5BT selected save reader qualification

Both explicit-input readers reproduced their selected saved-state evidence on the
pinned originals and in a source-only copy. Save29 reproduced the four typed
REFRs, ordered reciprocal ExtraCB graph and four Extra9C words. HIST-0021
reproduced the 43-section component closure, the empty helmet fixture inventory
with a positive displayed-item reference, and the separate backpack witness.
Independent acceptance is recorded separately in [review](review.md).
Publication is **NOT READY / NOT CLEARED**.

| D5BR route | Local result | 5B-2 handoff |
| --- | --- | --- |
| `S-P1-S29-ORIGINAL` · A3 | Reader passed locally on CORE `B4-F054`. The two extra walks agree on each counted end and reference cursor. | Restage or reuse an identity-verified immutable copy of the exact member. Rerun the selected reader and its controls in the coordinated original verification. |
| `S-SD1-H21` · A5 | Reader passed locally on ADDENDUM `B4-F067`. Nested, stock, item REFR, Extra36 and keyed reverse joins agree for both selected fixtures. | Restage or reuse an identity-verified immutable copy of the exact member. Rerun the selected reader and its controls in the coordinated original verification. |

The [D5BR crosswalk](../evidence-readiness-d5br/readiness.json) retains its
historical dispositions. The [Save29 authority report](../../experiments/power/save29-authority.md)
and [SD1 saved evidence](../../experiments/containers-displays/saves.md) still
govern the scientific interpretation. Saved power mask `0x40` and observed
post-load allocation are separate questions. The attributed ordinary base
values of 6 supply and 5 demand each predict only extractor #1 under the
declared native eligibility, resolution and effective-state conditions. Reversing
the consumer order predicts only #2. Display joins establish serialized state.
Rendered restoration and historic worker invocation remain unmeasured here.

## Reproduce from a clean source copy

Use CPython 3.14.3 on Windows with stdlib and the source paths in
[provenance](provenance.md). Run from the repository root or a source-only
copy preserving that layout. Supply lawful, immutable staged copies of the
two original SFS members. Use existing caller-owned parent directories and
choose previously nonexistent child output directories outside the source tree.
Keep the outputs local. These examples assume PowerShell variables pointing to
the executable and caller-owned locations.

```powershell
& $python -I -B save-analysis/scripts/d5bt_reader.py save29 --save $save29 --output-directory $powerOutput
& $python -I -B save-analysis/scripts/d5bt_reader.py hist-0021 --save $hist0021 --output-directory $displayOutput
& $python -I -B save-analysis/scripts/test_d5bt_reader.py
& $python -I -B save-analysis/scripts/test_d5bt_reader.py --save29 $save29 --hist-0021 $hist0021 --scratch $controlsScratch
```

Each reader checks the compressed size and SHA-256, BCPS1/zlib framing,
decoded length and SHA-256, save format 27, buffer version 153 and both
1.16.244.0 build strings. It walks the declared R3 region to closure and
selects only the four designated case-5 REFRs using the footer types.
Exit 0 writes deterministic `d5bt-selected/1` JSON and prints a human summary.
The output identifies the witness, pins, header, R3 count and selected rows.
Locations are decimal half-open decoded-stream ranges. Hex strings represent
FormIDs or raw tokens as labelled. Section, row and typed indices are
zero-based and have distinct meanings. Failures after directory creation
write an exclusive diagnostic. A path collision fails before output is opened.

The Save29 grammar covers the observed counted extra tags `9C DA 4C BC 84 BF
80 CA CB 1F` in the four selected records. The extra cursor can stop before
the REFR end and before queue exhaustion. HIST-0021 admits the pinned type-6
and CTName layout with the typed pending-dialogue extension. Its selected fixture
extras are `84 BF 9C 4C 1F` and its item extras are `33 96 BF 1F 36 4C 84`.
The `96` subset requires zero flags, and `33` admits only its two documented
mask bits. Unsupported variants fail closed. The display reader checks zero
normal inventory count and retains the one-byte record tail beyond the helmet
and backpack counted item extras as outside that counted list. Neither CLI
accepts another save as a fallback or scans a save directory. The pinned
definition results are attributed from the prior work, so the commands require
no game install or ESM.
