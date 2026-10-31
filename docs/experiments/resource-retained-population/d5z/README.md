# D5Z causal figures and checklist audit

These non-spatial diagrams show conditional native paths and evidence coverage.
They have no geographic coordinate axes or implied duration scale. Native VAs
refer to Starfield 1.16.244.0 at preferred image base `0x140000000`.

- [Visited-state lifecycle](visited-lifecycle.svg): construction/empty state, source-token lookup, pointer-map relationship, generation/append attempt, retirement, reset and separately restored persistent inputs.
- [Reset causes and effects](reset-causes.svg): actual module reset path, context/load/teardown conditions, inferred lifecycle purpose, the audited absence of a dedicated size/pressure policy and contradicted retirement equivalence.
- [Save-load and streaming](load-streaming.svg): conditional native order beside B1 checkpoint/admission windows; unresolved historical connection remains visibly separate.

[Backing data](graph-data.json) records each node/edge's evidence class,
claim, relative evidence link and display route. Solid blue is a compiled
conditional operation, green is a retained B1 witness, dashed amber is inference,
dashed rose marks the historical gap and brown marks a scoped contradicted claim.
Arrow crossings are display layout, never a new native dependency.

Reproduce exact SVG bytes with the owned
[renderer](../../../../research/resource-retained-population/d5z_figures.py)
and a fresh output directory. Existing standalone sharp/libvips supplies local
PNG previews for visual inspection; no renderer implementation is incorporated.
Local previews and tool hashes belong in the review package. Labels/evidence
strength require manual and independent review in addition to byte regeneration.

[Checklist audit](checklist-audit.csv) pairs all 31 original supplied operations
with their corrected durable wording. No unchecked source item becomes checked.
The original Desktop file is preserved and pinned in the source ledger.
The [durable checklist](../resource-generation-gameplay-checklist.md) controls
navigation; this correspondence is not independent proof of native semantics.

All authored figures/data remain REVIEW-REQUIRED. Raw native exports, saves,
private capture/receipt fields and analysis databases remain local-only; the
diagram package supplies no integration, retail or publication permission.
