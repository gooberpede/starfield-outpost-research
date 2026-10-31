# D5AA figures and sanitized backing data

2026-10-31, Australia/Sydney. [Report](../d5aa-report.md),
[chronology](../d5aa-b1-chronology.md), [native map](../d5aa-gameplay-transition-map.md),
[sources](../d5aa-sources.csv) and [review](../d5aa-review.md).
Authored derivatives are REVIEW-REQUIRED. Raw captures/native exports/saves remain
local; these files do not clear publication.

- [Chronology](chronology.svg): measured QPC points and external checkpoint
  collection intervals; the shaded region starts at the retained admission at
  the sampled first-loss boundary, not a measured dropped-event instant.
- [Causality](causality.svg): native possible/required transitions and distinct
  runtime observations. Row order is schematic, not a historical total order.
- [Source state machine](source-state.svg): visited hit, unvisited map hit/miss,
  generation/sample, reserve success/failure and reset/retirement. Static token
  storage semantics are known; B1 append occurrence remains unknown.

## Data interpretation

`events.csv` retains 451 sanitized records selected from the full local
19,780-row derivative. `raw_frame_offset` is an original-file byte offset;
QPC is absolute monotonic host ticks at 10,000,000 Hz. Relative seconds subtract
2,619,875,036,404. Event UTC is not observed. `P` labels preserve pointer equality
only; no allocation lifetime, stable geography or cross-session identity is
implied. Copied source keys appear only on records that actually carry bytes.
No proprietary source buffers, executable bytes, raw pointers or save payloads
are included. Status/hazard fields remain visible. The schema's branch operand
is meaningful only for its documented event kind.

`paths.csv` audits all 24 copied map decisions in lookup-sequence order.
`partial-chains.csv` audits later same-epoch pointer-compatible visited hits:
23 rows are positive and lookup 1227 has zero. These are conditional joins,
not authenticated full chains; an equal-pointer bypass across epochs is excluded.
`conditional.csv` preserves all 119 D5Y target-compatible pairs and their
attribution qualification. Its original D5Y `P20` alias namespace differs from
the new event ledger's labels; do not join alias text between the two tables.
Join explicit record sequences instead.

`checkpoints.csv` preserves request/ACK/STOP annotation QPC/UTC, not native action
instants. `chronology-points.csv` selects the plotted points; `graph-data.json`,
`transitions.csv` and `state-edges.csv` supply authored causal labels and evidence
classes. `summary.json` records scope/counts/provenance and missing witnesses.
`capacity-sensitivity.csv` is a serial admitted-input sensitivity model with
ideal drain snapshots, not a changed observer or a future qualification.

## Reproduction

Use the installed CPython executable if `python` resolves to the unavailable
WindowsApps alias. All scripts use stdlib and refuse existing output directories.
From the repository root, replace `FRESH` labels with unused names:

```powershell
python -B research/resource-retained-population/d5y_forensics.py d5aa-FRESH
python -B research/resource-retained-population/d5aa_chronology.py .local-work/d5y/d5aa-FRESH .local-work/d5aa/chronology-FRESH
python -B research/resource-retained-population/d5z_b1.py .local-work/d5y/d5aa-FRESH .local-work/d5aa/reset-FRESH
python -B research/resource-retained-population/d5aa_backing.py .local-work/d5aa/chronology-FRESH .local-work/d5aa/backing-FRESH
python -B research/resource-retained-population/d5aa_checks.py .local-work/d5y/d5aa-FRESH .local-work/d5aa/checks-FRESH
python -B research/resource-retained-population/d5aa_figures.py .local-work/d5aa/backing-FRESH .local-work/d5aa/figures-FRESH
python -B research/resource-retained-population/d5aa_verify.py verify-FRESH
```

The verification method intentionally uses the retained `d5aa-auth01` inventory
and seven pinned export paths as prerequisites, rather than silently rebasing
them onto new files. The fresh authenticator supplies the same original native
and archive inputs; its HEAD/free-space values are run-specific. Commands do not
download missing private evidence. Native-export reproduction uses
`d5aa_native.py LABEL ADDRESS...` with the exact explicit address sets from
`.local-work/d5aa/export01..07/command.json`, retaining `-readOnly -noanalysis`.
The source ledger pins original exports, inherited owned reader and methods;
export caches/logs stay in a fresh local directory. This is not a portable public
checkout with proprietary native evidence included.

Executed checks and their limits appear in the report/review. Local PNG previews
were rendered with existing standalone sharp/libvips and visually inspected;
no renderer code or dependency is incorporated. The font cache was unwritable,
but PNG outputs were produced and inspected. No external image is used.
