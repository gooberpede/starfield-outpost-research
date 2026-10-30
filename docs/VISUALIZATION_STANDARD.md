# Prospective research visualization convention

Applies to new research maps from D5U onward. Existing studies/images retain
their historical contracts; this guide does not silently retrofit them.

- Link every figure to machine-readable data, source/build/tool identities and
  deterministic reproduction. Separate original evidence from rendering inputs.
- State the spatial product: query support, generated competition footprint,
  Workshop availability, terrain or another qualified consumer. Do not exchange
  them without proof. Label STATIC, executed, inferred and UNKNOWN coverage.
- Declare origin, axes/orientation, units, transform, extent and scale. Use one
  origin/scale/orientation/extent within variant comparisons. Explain discrete
  query bins separately from continuous geometry; provide labelled ticks or a
  scale bar and verify no meaningful primitive is silently cropped.
- Keep sampled-mask colors stable across sources. Mask colors are not resource
  membership or IRES deposit colors. Show support, proven admissible witnesses,
  proven exclusions and unqualified candidates distinctly. Candidate counts
  are not winner probabilities.
- Use verified IRES TINC or the applicable resource-color field for deposits;
  retain FormID, field/record locator and conversion. Document a fallback and
  why the field was unavailable. Preserve resource colors across panels.
- When depicting an outpost, mark its **native centre** and the **150-native-unit
  radius boundary** in the same coordinate transform. Locate the beacon
  separately if known and different. Source anchor, native centre and beacon
  must never be assumed identical. Establish the translation explicitly.
- If centre/beacon/alignment is unknown, label UNKNOWN and name the missing
  prerequisite; do not invent an overlay. A source-only map may show its anchor
  and footprint, with an explicit statement that it does not locate an outpost.
- An outpost composite must cover the complete relevant source halo, including
  sources outside a comparative census. Keep source IDs stable and give added
  sources separate identities. Show invariant contributions and independent
  variable-source layers without inventing jointly achievable combinations.
- Separate geographic descriptor, saved site/base, native centre, source anchor
  and padded generator origin. Prove forward/inverse transforms against an
  independent numerical control. Recomputing a display origin does not preserve
  frame-dependent procedural seeds. A historical disk on normalized prospective
  geometry is a reference unless the generation-frame equivalence is established.
- Distinguish a fixed research radius from a recovered saved hardware boundary,
  and saved beacon/centre coincidence from a current loaded-state observation.
  Label deliberate zoom clipping; keep the full disk visible and retain full
  geometry outside the viewport in machine-readable data.
- Preserve exact native points/bounds and meaningful metadata. Document boundary
  approximation, clipping and paint rules. Finite point tests do not prove exact
  continuous native boundary equivalence or terrain/UI identity.
- Rasterize with a named local renderer, preserve warnings and inspect labels,
  legends, transformations, scale, clipping and difficult variants. Record the
  actual inspected image inventory, complete manual prose coverage and independent
  final-snapshot review. A checksum or successful rendering alone is insufficient.

The [D5U methods and gallery](experiments/resource-retained-population/d5u-methods.md)
demonstrate this convention with reproducible source/geometry SVGs. Scientific
confidence, completeness, rights eligibility, integration and publication approval
remain separate under the [evidence standard](EVIDENCE_STANDARD.md).

The [C1 outpost composites](experiments/resource-retained-population/d5u/outposts/README.md)
and [coordinate proof](experiments/resource-retained-population/d5u-c1-coordinate-validation.md)
demonstrate the additional outpost/seed-frame requirements. Original accepted
source-only figures remain historical artifacts with their original qualifications.
