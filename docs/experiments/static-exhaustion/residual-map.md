# EXP0020 — Residual map and identifiability boundary

[Report](../activated-overlay-static-exhaustion.md) · [Ledger](dependency-ledger.md).
Addresses are static VAs, retail1.16.244.0/base140000000. Authored interpretation
and selected numbers: REVIEW-REQUIRED. This is a bounded graph conclusion, not
a proof that no other function exists in the executable.

## What is reconstructed

For a qualified saved beacon, form the durable center
`C = f32(f32(P) + f32(workshop_delta))`, componentwise. Join its saved parent
to the typed unit-6 world component, its secondary world to the unit-3 descriptor,
and system/body-index to installed PNDT GNAM. Keep the saved initial frame byte.
For the studied active cases, use the descriptor's encoded origin when mask20 is
clear, or the saved site anchor when mask20 is set. Split each center axis using
`q=floor(f32(f32(C)*f32(.01)))`, `r=f32(C-f32(100*q))`, and apply native integer
offset/wrap `14096f5c0` to the selected base. Retain Z in its saved local frame.
Implementation: `audit_saved_center_frame.py`; result [table](saved-center-frame.csv).

This gives body, chart/tag, integer cell, XY residual, local Z and a recoverable
saved frame. It does **not** identify the residual's spherical embedding. Nor
does it predict an arbitrary future loaded terrain epoch or bit-exact XYZ after
float32 translations into that epoch.

## Producer-to-consumer closure

| Branch | Actual dataflow | Terminal relevance |
|---|---|---|
| `14077fc20` existing-reference branch | Site/request integer pair difference ×100 plus reference XYZ; split into floor and residual; residual kept in placement state+20/+24/+28. Returned pair is requantized. | RESOLVED local placement split; no residual input to returned angular pair. |
| `14077f900` →144b3dc10→`140780a50` →144b3dbf0→`140780aa0 →140781390` | Enumerates cells/references, selects eligible existing reference, compares local XY squared distances and copies its XYZ plus integer displacement. `14077def0` supplies eligibility, not coordinates. | RESOLVED alternative fractional producer. All coordinates come from existing reference/local translation. |
| `14077e350` →144b3dc70→`140780710 →14077f6e0` | Searches integer candidate cells; checks `14078d2c0` integer-pair displacement; creates/selects overlay and calls the same reference search. | RESOLVED fallback; no continuous inverse projection. |
| `14078b030/14078af30/14078bc30` and player transfer callers | Placement-state fields transferred to local player/reference/cell state. `14078d370` returns100×integer pair delta and local height. | RESOLVED local placement consumers; preservation of XYZ does not supply a body direction. |
| `14078d1f0 →14078d660 →142332410` | Floors float32 XY×.01, offsets indexed origin, evaluates normalized `(i+.5)/49152-.5`. | RESOLVED exact studied discrete map; many local positions share its result. |
| `140910690` / ExtraLocation81 | Cached pair or site pair, otherwise the same floored conversion. `14051ea30`/`140546580` write/read raw pair. Eight setter callers and request enumeration traced. `14076a340` likewise floors offset XY. | RESOLVED cache provenance; no independent continuous center oracle. |
| `1407bcfb0` / celestial consumers | Player XY plus indexed offset, floor, cell-center projection, sin/cos, body orientation/normalization/scale/translation. | FALSIFIED_OR_IRRELEVANT as residual transform: fractions and Z are discarded before body geometry. The body's orientation/scale cannot restore discarded XY. |
| `14076de40 →14076db70 →14076d500` | Dense local samples still floor before planetary location-predicate lookup. | FALSIFIED_OR_IRRELEVANT as off-grid angular evidence. |
| `14099ff50 →1409a0f20/1409a02b0` | Fractional XY interpolates local height samples to a scalar Z. | RESOLVED local geometry; it supplies no body-oriented direction or chart Jacobian. Following every caller of a scalar height routine is not required to identify this output. |
| Additional `14078d370` caller `14141ccd0` / `14141dc70` | Reads manager requested pair+98/+a0; takes only returned Z as height baseline. Camera rays intersect a local Z plane; local bounds/cells feed a sampled height calculation. | FALSIFIED_OR_IRRELEVANT as residual-to-body mapping: no center residual reaches a spherical output through this call. Camera/world ray geometry is not a planetary chart. |
| `14096be70/14096bba0 →140851d20` | Pattern-entry lookup, centered integer rotation/reflection and installed subdivision spans. | RESOLVED footprint/index role; these transform pattern selection, not surviving fractional beacon XY into a body point. |

Exports62–68 recover both formerly indirect placement helpers and the additional
pair-to-local caller. They close these graph branches rather than relying solely
on a list of direct projection callers. Height/eligibility/resource-allocation
callees are excluded by the inspected typed output and call-site dataflow; this
does not classify all uses of their types elsewhere in the game.

## Exact missing relationship and countermodels

The necessary unknown is a source-qualified mapping
`E(body, tag, indexed_cell, residual_XY, local_Z) → continuous body direction`
(or a geometrically equivalent embedding). None of the closed branches above
supplies its off-grid phase/Jacobian/curvature. No unknown compensation byte or
unresolved body ID is being substituted for this relationship.

The existing center/corner candidate difference already demonstrates phase
ambiguity, but choosing a center phase is insufficient. Let `F(tag,u,v)` be the
recovered inverse square projection, `N=49152`, and `s=r/100`. Two same-phase
extensions in the chart interior are:

```
E0 = F(tag, (i+.5+sx)/N-.5, (j+.5+sy)/N-.5)
E1 = F(tag, (i+.5+sx+.05*sin(2*pi*sx))/N-.5,
            (j+.5+sy+.05*sin(2*pi*sy))/N-.5)
```

Both agree at every integer sample, use the same orientation and100-unit step,
are smooth and monotone inside each chart axis, and are invariant under opposite
integer origin/local translations. They differ for the actual nonzero SOR-003
residual. Four independent tests exercise these properties in
`test_residual_ambiguity.py`. They are **countermodels, not proposed engine
implementations or uncertainty bounds**. The arbitrary.05 is one global
mathematical counterexample parameter, not a per-outpost fit. No seam extension
or physical metre scale is claimed for either model.

The studied pair→local placement is itself quantized, so it does not justify
demanding an exact inverse on every off-grid input. Conversely, the local→pair
consumer drops the residual, so it cannot discriminate E0 from E1. Local height,
pattern orientation and the celestial transform likewise add no observation of
the missing relationship. Save25/26 invariance and independent body checks hold
for both; they cannot validate one continuous extension. This is why the lack
of a named native latitude API alone is **not** the blocking argument: equivalent
transforms were considered and shown non-unique under the recovered constraints.

## What could discriminate, and what cannot

Smallest useful new evidence: one settled, known-body local frame with a nonzero
XY residual, an independently qualified native consumer receiving that position
and returning a body-oriented direction/continuous chart coordinate, and its
input/output at an interior location where E0/E1 predict different results.
Two non-collinear offsets are preferable to distinguish both axes; include a
local-Z change if a radial/tangent interpretation is proposed. Capture the frame
key, selected edge validity/shift, origin and rebase mode at the same instant.
A recorded call returning the already studied floored pair will not suffice.

This is a proposed separate experiment, **not execution authority or a promise
that such a consumer exists**. Its prerequisite is a defensible independent
geometric observable. If no such observable/convention exists, an exact
off-grid longitude/latitude is not defined by these engine paths; a documented
application-chosen approximation would be a separate decision. New local
movement/save pairs alone merely provide additional residuals and do not choose
an embedding. A future live brief must pin build/protected source copies,
consumer/breakpoint scope, finite captures, induced-execution risks, evidence
flushing, stop/exit/recovery/cleanup terms. No live action occurred here.

Further repetition of the same static integer/cache/height paths cannot choose
between these interpretations. A newly identified source linking fractional XYZ
to global geometry would reopen this scoped exhaustion; no universal negative
about all executable functions, plugins or asset representations is asserted.
