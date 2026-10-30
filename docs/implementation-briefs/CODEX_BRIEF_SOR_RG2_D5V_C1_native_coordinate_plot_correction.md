# RG2-D5V-C1 — Native-Coordinate Plot Correction and Independent Visual Acceptance

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Correct the D5V spatial plots and coordinate-presentation claims under the existing D5V assignment. No new scientific investigation or new retail authority.  
**Status:** Correction / REWORK of D5V-AC6 and D5V-AC7 only, with necessary dependent documentation and review updates. D5P retail remains **NO-GO**; B6/publication remains **ON HOLD**.

## 1. Defect and controlling requirement

The D5V plots for `D2-83388f` (**Feynman V Cu Co Ni IL**) and `D2-84e101` (**Feynman V Cu IL F**) label their historical native centres but display axes as displacement from the outpost centre. In the plotting source, `d5v_maps.py` passes `[0,0]` to `panel()` and calls `shifted(v, ref['center'])` for every geometry layer. The plot text explicitly calls the axes “native displacements.” This is a valid *relative* visualization, but it does **not** satisfy the maintainer's request that the plotted coordinate axes correspond to the actual native coordinate domain rather than an outpost-centred coordinate system imposed for display.

**Controlling correction question (D5V-C1-Q1):** Can the two D5V outpost figures present the qualified historical **native descriptor-frame X/Y coordinates directly**—for axes, plotted data, outpost centre, beacon and boundary—while retaining the established geometry, native-consumer findings and reproducibility? The answer must be demonstrated in rendered output, not merely asserted from transform equations.

The qualified native centres in the prior D5V record are approximately:
- `D2-83388f`: `(-2716.539306640625, -132.11228942871094)`
- `D2-84e101`: `(81.1907, 90.2775)`; use the exact authenticated values in the backing data, not these rounded display examples.

The centre marker must be **labelled and positioned at its native coordinate**, not assigned a data-coordinate origin of `(0,0)`. The native 150-unit circle is centred at the same verified coordinate. A source anchor, beacon, saved site-local location, generator origin and consumer coordinate must not be silently treated as interchangeable.

## 2. Required implementation

1. **Inspect and reuse the established coordinate contract** (`d5v-coordinate-contract.md`, D5U-C1 saved-centre/frame proofs, and the supplied C1 geometry JSON) before editing. Identify the exact native domain used by every mapped layer, including any conversion already applied to the historical-frame inputs. Confirm that both maps' native geometry and saved centre are actually in a common qualified frame. If not, establish the requisite join first; do not conceal an unresolved mismatch by relabelling ticks.
2. **Correct both SVG figures and their generator.** Plot native descriptor-frame X/Y values as the public data coordinates. Viewport centring, screen scaling, SVG Y inversion and numerical subtraction of a viewport origin inside the renderer remain permitted implementation details, provided that the plotted native coordinates, tick/grid labels, centre marker, beacon and boundary are correct and do not falsely show the native centre as `(0,0)`.
3. **Preserve the historical centre and 150-native-unit circle**, the recorded beacon relationship (only where actually qualified), the resource shapes, IRES colors, panel comparison meaning and native area-consumer classifications. Do not regenerate native geometry, substitute normalized prospective geometry or change resource-region inputs to make a graphic look similar.
4. **Use unambiguous labels.** Each plot must identify its coordinate domain as historical native descriptor-frame XY, state any restricted frame/epoch assumptions, use meaningful absolute native axis ticks with legible precision and units, and mark the centre at the actual coordinate. Do not imply planetary global XYZ, compass orientation, metres or a live loaded epoch if those are not established. Relative displacement grids may be provided only as a clearly labelled *secondary* convenience, not as the sole coordinate system or the nominal native values.
5. **Audit adjacent spatial figures and narrative** (including `coordinates.svg`, the D5V gallery README, coordinate contract, spatial backing data, report and review) for contradictory wording or misleading captions. Only change them where needed for a consistent truthful coordinate presentation. Preserve lifecycle schematic semantics and historical scientific claims; do not broaden the scientific study.
6. **Retain exact spatial provenance.** Use source geometry and reference metadata as canonical inputs. Keep reversible and documented native-to-pixel mapping and its inverse. Display rounding must not silently replace underlying binary32 native values. Geometry, resource membership, masks and accepted native consumer results must not change.

## 3. Required verification and independent review

- Numerically prove, for **both** figures, native→pixel→native round trips for actual centre, beacon (where qualified), cardinal radius points, plot corners and representative deposit point/bound coordinates. Establish explicit tolerances for display/pixel rounding. Verify the 150-unit circle is centred correctly and has correct native scale.
- Verify machine-readable/native geometry and native-consumer outputs remain unchanged, or document any strictly presentational schema change separately with byte/hash comparisons of scientific input and output fields.
- Reproduce all affected SVGs byte-for-byte from the delivered plotting source and input data. Parse SVG, check axes/ticks and preserve common native coordinate-domain semantics across comparison panels; **do not** require separate outposts to share one viewport extent when their native centres differ.
- **Render and actually inspect** both final outpost SVGs independently of the generator. Check readable native axis labels, correct centre marker/beacon, full boundary, unclipped deposits, legends and panel comparability. Reviewers must inspect the rendered visual result, not simply approve XML validity, formula arithmetic or self-reported QA. If automated browser viewing fails, use an offline renderer and preserve review images/receipts.
- Independent scientific/engineering completeness reviewer must compare original D5V-AC6/AC7 intent with the *visible* corrected plots and the numerical coordinate evidence. Editorial reviewer must independently verify captions, scales, legends and consistency across documentation. Return **REWORK** if the only axes are still centre-relative or if the actual native frame remains unqualified. A reviewer cannot turn a failed mandatory requirement into ACCEPT by documenting a caveat.

## 4. Acceptance criteria (frozen)

| ID | Mandatory outcome |
|---|---|
| **C1-AC1 — Authority/preservation** | Exact pinned inputs and task boundaries verified; no live game/SFSE, Vortex, save/config/analysis-DB mutation, external disclosure, staging, commit, push or publication. |
| **C1-AC2 — Frame qualification** | Each mapped layer and centre/beacon is joined to the same evidenced native descriptor-frame domain; unknown frame relationships remain explicitly unplotted, not guessed. |
| **C1-AC3 — Native coordinate presentation** | Both outpost SVGs show absolute native X/Y coordinates and place/label the native centre at its genuine value, not data origin `(0,0)`. SVG internal viewport transforms are documented separately. |
| **C1-AC4 — Boundary and scientific fidelity** | Full 150-native-unit boundary and qualified beacon marker are correctly positioned; geometry, masks, resource identities, colors, consumer comparisons and historical/prospective distinctions are preserved. |
| **C1-AC5 — Numerical and reproducibility controls** | Relevant round-trip, cardinal-radius, representative-point, unchanged-scientific-data and deterministic SVG regeneration controls pass; tolerances and limits are explicit. |
| **C1-AC6 — Rendered visual QA** | Both final outpost SVGs are rendered and independently visually examined for genuinely native axes, legibility, clipping, legends and correct overlays; evidence is retained. |
| **C1-AC7 — Documentation consistency** | D5V spatial data/README/contract/report and affected review text make no conflicting claims about native versus relative coordinates; superseded statements are corrected without rewriting historical scientific evidence. |
| **C1-AC8 — Independent completion review** | Separate scientific/engineering and editorial acceptance covers the actual plotted output, original failed D5V-AC6/AC7 and exact final snapshot; REWORK is mandatory if native axes are missing. |
| **C1-AC9 — Exact delivery** | Focused report, updated generator/SVGs and necessary supporting documents, verified exact-hash manifest, task-only and complete patches, status/inclusion/exclusion inventory and independent returns; no staging/commit/push. |

## 5. Continuation, blockers and delivery

Apply current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md` and save protection. Start an active, concise correction ledger; continue authorized investigation/correction/requalification under this same assignment until **COMPLETE** or a rigorously evidenced **BLOCKED** escalation. “Axes are a display convenience” is not closure. Do not silently narrow C1-Q1.

Expected report: the exact defect/root cause, the native coordinate-domain and pixel-transform contract, old-versus-new visual semantics, numerical QA, unchanged scientific outputs, and any genuine remaining boundaries. Supply corrected figures and a short human-readable note explaining that native data values are preserved even though a renderer necessarily maps them to SVG pixels. Keep proprietary evidence and temporary renderings in appropriate ignored local paths; retain reproducible authored SVGs in the existing D5V gallery.

**Integration remains the maintainer's decision after critical diff review.** This correction does not itself authorize retail testing or amend the D5V lifecycle/consumer scientific conclusions.
