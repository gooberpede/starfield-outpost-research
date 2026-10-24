# Chlorine 829: serialized SFPT installation defect

2026-10-24, Australia/Sydney. This is the same-assignment correction requested by independent REWORK of review02. [Native pins](sources.csv), [original and corrected validation](validation.md), [review](review.md). No live acquisition was needed to diagnose this discrepancy.

**The existing corpus builder treated serialized SFPT FNAM/GNAM pairs as the runtime array. Native installation transposes that array. Applying the general installation rule selects Chlorine 829's observed SFBK and preserves its exact geometry.** The corrected preparation uses the same installed PNDT, SFTR, SFPT, source coordinates and geometry arithmetic. No observed SFBK is injected into an input table.

## First divergent operation

All VAs are preferred static VAs on the pinned 1.16.244.0 image/base described in [native.md](native.md). Object offsets are bytes; array indices below count entries.

| Boundary | Evidence and result |
|---|---|
| Typed pattern loader | `d4c-patternvtable01.tsv`: `BGSSurface::Pattern` secondary vtable at `0x144b67080` points at `0x14096bf00` for loading. `d4c-patternloader01.tsv` exports the full function. |
| Modern serialized input | `0x14096bf00`, FNAM/EFRM branch through `0x14096cbc2`: read 256 FormIDs and 256 flags, pair them in serialized order, resolve references, then call `0x14096bae0`. FNAM supplies false for the partial-update flag; EFRM supplies true. |
| Installation transpose | `d4c-patterninstall01.tsv`, `0x14096bb20–0x14096bb54`: read input index `inner + 16*outer`, write runtime pattern `+0x38` at index `16*inner + outer`. For FNAM, copy the complete pair including unchanged flag bits. EFRM partial updates are outside the new adapter. |
| Runtime lookup | `d4c-patternvtable01.tsv`, `0x14096be88–0x14096bee4`: for coarse flags below `0x20`, use pattern `+0x38` at `X*16+Y`. The captured coarse flag is `0x08`, so this does not require an orientation-setting assumption or remapped table. |
| Existing extraction defect | D1/D3 builders use `zip(unpack(FNAM), GNAM)` directly as the runtime X-major array. They omit the installation operation between serialization and lookup. Both old corpus representations inherit that omission. |

The pure preparation adapter [source_layout.py](../../../research/resource-owner-root/source_layout.py) implements this transposition for complete modern FNAM/GNAM arrays. Three asymmetric authored-grid tests distinguish transposed and direct indexing, preserve duplicates/flags and reject wrong lengths. They complement the eleven logical map tests. This is a source-backed format correction; the earlier family-to-slot hypothesis remains unvalidated.

## Existing operands resolve the discrepancy

The installed Archimedes PNDT `0x0005de4c` selects SFTR `0x0012c692`. Chart 0, coarse cell (141,187), table index 36283 gives SFPT `0x0023de96`, coarse flag `0x08`. The captured source for 829 independently retains that same pattern, coarse cell, flag and subindices (8,7).

| Read at subindices (8,7) | Input index in serialized arrays | SFBK / block flag |
|---|---:|---|
| Frozen direct-array projection | 135 | `0x002c17d5` / `0x28` |
| Native installation followed by runtime lookup | 120 | `0x002c17d3` / `0xc8` |
| Captured source `+0x54/+0x58` | Not an inferred file offset | `0x002c17d3` / `0xc8` |

The source's first word also names `0x002c17d3`. Both installed SFBKs have raw DNAM dimensions (14,14), giving nominal dimensions (10,10). That equality explains why the original geometric match survived the wrong identity. At Tungsten's subindices (7,7), installation reads the same diagonal entry, so its source remains `0x0028be0d`. Matching geometry alone did not test the missing preparation step.

`source-layout01/source-boundary.json` retains the complete route summary; `preparation.json` retains pattern header offsets and dependency pins. Original framed captures and the earlier failing strict source check remain intact. `source-bound-layout01.json` now verifies all three Archimedes controls against source identity, IRES, ordered binary32 XYZW and the 16-byte native sphere bound. The Tungsten geometry still depends on the separately frozen conditional two-resource map, not a complete native candidate reconstruction. Historical generation/consumer continuity remains UNKNOWN.

## Versioned consequences and storage

The [layout validation driver](../../../research/resource-owner-root/layout_validate.py) checks every retained pattern against fresh pinned serialized ESM fields, rejects EFRM, prepares new normalized/expanded corpora and runs isolated inference. It does not overwrite D1/D2/D3 code, requests, corpora, outputs or classifications. The D1 control corpus is bridged to the existing D3 schema/status vocabulary for a common unchanged inference bundle; this adds 21 authored schema/status bytes, independently of the transpose.

All 17 active D3 requests are rerun with corrected source layout. All 19 original cases remain accounted for; the two disabled cases stay excluded. All 46 saved association rows are reclassified diagnostically, including controls. There are zero changed association classifications and zero resource-availability status changes. Held-out counts remain 25 positive correspondences, one potential false negative, nine indeterminate pairs and four separate alternative-admission Water pairs. These are source-layout diagnostic consequences, not validation of an owner-root correction or native resource absence.

| Case | Source count before → after | Generated paths before → after |
|---|---:|---:|
| `D2-828ee2` | 6 → 6 | 524 → 807 |
| `D2-82a0c0` | 6 → 6 | 493 → 748 |
| `D2-82be17` | 6 → 4 | 1326 → 1144 |
| `D2-830a80` | 4 → 4 | 332 → 604 |
| `D2-832512` | 4 → 4 | 302 → 560 |
| `D2-84ede9` | 4 → 3 | 626 → 535 |

The other eleven active cases retain path/source counts, although source identities can change. Generated paths are not visible patch counts or a complete native population census. Frozen and corrected local outputs both remain available; no old numeric inventory is silently relabeled.

All seven established Feynman/Carinae resource/shape/callback controls still have exactly one match in both normalized and expanded corrected representations. Their historical source-identity coverage is unchanged; no new source identity claim is inferred from those seven shapes. The full frozen D2/D3 replays also remain equal to their historical outputs under their original corpora.

D3's original pretty JSON occupies 738975 bytes. At identical canonical serialization, old and corrected normalized corpora both occupy 220381 bytes: **0 additional retained bytes, 0 new numeric fields** for the source-layout correction. The apparent reduction from pretty to compact JSON is formatting, not a new minimization result. No general owner-root production corpus is supplied; its additional dependency cost remains unmeasured because the actual component projection is unresolved.

This diagnosis closes the offline Chlorine source-selection follow-up. It does not fill the native owner-range keys/slot ancestry or explain the two ordinary Water operands. The [prospective map card](run-card.md) targets that separate remaining gap; it no longer treats Chlorine 829's table-index mismatch as a reason for new live acquisition.
