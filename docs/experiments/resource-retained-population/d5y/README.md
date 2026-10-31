# D5Y diagnostic figures and aggregate data

All figures describe one retained B1 retail capture. They are REVIEW-REQUIRED;
publication remains ON HOLD. [Report](../d5y-report.md),
[decision](../d5y-decision.md), [sources](../d5y-sources.csv).

| Figure | Backing data and interpretation |
|---|---|
| [chronology.svg](chronology.svg) | `chronology.csv`, `checkpoints.json`, `summary.json`: admitted records in one-second QPC bins; checkpoint collection bounds, not exact gameplay transition times. Empty bins do not prove native inactivity. Red shading uses admission-boundary proxies, not measured loss-time containment. |
| [writer-progress.svg](writer-progress.svg) | `writer-progress.csv`: cumulative counts versus flush-ledger ordinal; endpoint-event seconds are deliberately not used as flush times. Maximum flush duration combines raw and ACK calls. |
| [target-depth.svg](target-depth.svg) | `source-depth.csv`, `pointer-envelopes.csv`, `conditional-target.csv`, `spatial-controls.json`: copied source identity differs from conditional installed-support attribution. Pointer labels are first-selection-order aliases, not persistent source IDs. |

`requests.csv` lists valid original local Int2 requests. No unqualified absolute
native-coordinate transform is applied. `replay.json` and `isolated-pauses.json`
describe synthetic serial-capacity sensitivity controls, using only retained
arrival QPCs. They do not reconstruct dropped arrivals, actual transport I/O or
the engine scheduler. Per-kind/thread/epoch strata and raw pointer mappings
remain local in `.local-work/d5y/analysis03/`.

The `kinds` field in `source-depth.csv` is a semicolon-delimited list of exact
machine event tokens. Its compact separators are intentional; punctuation-space
screen warnings on those nineteen data rows do not indicate joined prose.

Reproduce SVGs using `d5y_figures.py` and the report's fresh-output command.
`figures.json` pins its generator, authenticated analysis receipt and every
generated data/graphic input. This README is authored explanatory material,
not a generated input. Native source bytes, memory addresses and proprietary
exports are excluded. Rendered PNGs are local QA artifacts, not delivery assets.
