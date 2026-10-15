# Milestone B native evaluation specification and contract

2026-10-15. [Result](report.md), [decisive native evidence](native-provenance.md).
All algorithms are build-specific OBSERVED-INTERNAL; they are not validated
callable mod integration APIs. Executable SHA256 is
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Preferred static image base is `0x140000000`; runtime base in the original capture
is `0x00007ff7ce2f0000`. An RVA is added only to its corresponding base.

## Data flow and spatial decision

The preview CALL at RVA `0x021b42e3` supplies producer `0x021e07d0` with RCX
query state, RDX indexed XYZ/frame/domain, XMM2 query radius, XMM3 separate height
operand. It is the evaluation-time prospective position, not player XYZ.
The producer locks ProcGen and scans every occupied source-table slot; its callback
scans every occupied resource slot within each source. This is a loaded-table scan,
not a proved query-neighborhood index lookup. The callback at RVA `0x021e0f50`
resolves resource candidates, checks native
type `0x9f` (IRES), then examines 48-byte region descriptors and their pointed
16-byte xyz/width point sequences. Query coordinates must be translated by the
**actual invocation's** indexed translation table before comparison. Frame zero
is not itself evidence of a zero translation. The evaluator therefore requires
pretranslated qualified coordinates and never guesses a world/save transform.

1. Compute binary32 `dx=region.x-query.x`, `dy=region.y-query.y`,
   `distance2=f32(f32(dy*dy)+f32(dx*dx))`,
   `reach2=f32(f32(regionRadius+queryRadius)^2)`. Equality passes broadphase.
2. A failing broadphase rejects. Point count zero rejects; count one accepts
   without consuming the point contents. A passing multiple-point region tests
   each consecutive pair, with **no last-to-first closure**.
3. Normalize the pair's 3D direction, rotate with the native fixed-angle
   polynomial result, and offset by each endpoint's independent width to form a
   tapered quad. The native residual cosine is retained; substituting an ideal
   perpendicular changes rounding. [Native ledger](native-provenance.md) pins
   constants, DPPS/scalar grouping and degenerate handling.
4. First accept when all four oriented XY crosses are nonpositive. This branch
   ignores Z. Otherwise accept any vertex with XY distance² <= query radius²
   and vertex Z <= separate height operand. The height is an absolute operand,
   not query Z plus an assumed range. Otherwise accept a closed **quad edge**
   whose 3D segment distance² <= query radius². Reject if every strip fails.
5. Accepted resource pointers feed the spatial population, without duplicate
   resource pointers. Candidate resource identity is distinct from region
   identity, generation definition, actor value, recipe or localized name.

Arithmetic rounds at native binary32 operations. The executable qualifies finite
normal/zero operands and intermediates; overflow, subnormal results and missing
MXCSR-sensitive cases return UNKNOWN rather than assert native equivalence.
Synthetic boundary/degenerate tests qualify the transcription only.

## Atmosphere, biome, special cases and presentation

The producer resolves the world-component atmosphere definition and copies its
resource list. Kreet's actual captured second population is IRES
`Starfield.esm:0057f5`, Helium-3; it remains present while the generated spatial
population switches between Iron (`0057c7`) and Iron plus Alkanes (`0057c9`).
These identities are independently resolved installed definitions, not inferred
from their labels. Effective ATMO reflection/load-context qualification remains
an upstream obligation. See [B2](native-provenance.md).

Spatial BIOM lookup supplies BIOM RNAM → RSGD descriptors → their resource
pointers. This unfiltered third population is not a local spatial set. The
recorded third population contains Iron and Lead (`0057c1`); Lead does not appear
in the UI because only the selected water FormID can pass its special loop.
The existing `biome_rnam_resources` definition projector remains the executable
definition-edge calculation; it performs neither spatial selection nor generation.

The first two populations are merged in order by exact pointer identity.
Selected biome entries are appended by FormID comparison without the common
union's deduplication. Null common entries make no row; a null special entry
with a nonnull selector is invalid. Row order and the mathematical identity set
are distinct outputs. Allocation success is a required condition. Queue delivery
reads shared populations, not an evaluation snapshot. Refresh, content change,
UI application and rendering are separate events; 346 refreshes accompany only
five population changes. No exact render-frame or unique async ancestry claim follows.

X-Tech's PlaceAnywhere/SkipResourceVeinCheck keys belong to a separately scoped
harvester resource-gate exemption. They do not create ordinary region presence,
prove a UI row, or imply a legal extractor footprint. Existing
`harvester_resource_gate` remains separate. No construction-cost or collision
criterion is added to availability.

## Executable input/output version 2

[resource_availability.py](../../../save-analysis/scripts/resource_availability.py)
dispatches both the preserved `sor-resource-ui-input/1` and new
`sor-resource-availability-input/2`. New spatial functions reside in the imported
[resource_spatial.py](../../../save-analysis/scripts/resource_spatial.py), not an
alternative competing evaluator. Pure stdlib, no target or file writes.

| Input | Meaning |
|---|---|
| `schema`, `exe_sha256`, `session`, `evidence` | Version string, pinned executable, nonempty session/lifetime and evidence locator. Syntax cannot certify provenance. |
| `query` | `xyz` length 3, `radius`, `height`, `frame_qualified` boolean. Coordinates already mapped into the actual callback frame. Null/missing operands remain unknown. |
| `candidate_enumeration_complete` | True only when the complete native candidate retrieval result is independently qualified. Null/false cannot justify an absent resource. |
| `regions` | Complete candidate regions, or null if unavailable. Empty array is observed empty. Each has `identity`, `evidence`, `resolved_form_type`, `resource`, `center`, `radius`, `point_count`, `points`. |
| Region identity / resource | Diagnostic region identity and its independently resolved concrete type. Non-IRES candidates are rejected. `resource` uses the existing pointer/FormID/optional plugin-qualified identity contract. |
| Region geometry | Center XYZ and broadphase radius; u32 point count and complete ordered `[x,y,z,width]` sequence. Null points can still qualify count-zero/one branches; multi-point acceptance requires geometry. |
| `atmosphere`, `biome` | Ordered independently qualified definition-resource operands, or null. The biome array is unfiltered, not already selected water. |
| `selector_observed`, `selected_form_id`, `allocations_complete` | Existing version-1 meanings retained. Unknown differs from observed null/empty. |

Result `sor-resource-availability-result/2` preserves provenance and spatial
diagnostics with branch/reason/accepted state. `CONDITIONAL_NATIVE_AVAILABILITY`
requires complete qualified inputs and successful allocation; missing evidence
yields `UNKNOWN`, null `ui_rows`/`ui_form_set`, and named missing inputs. The
`known_spatial_resource_lower_bound` contains only accepted supplied candidates;
it is never labelled a complete availability set. This lower bound also requires
the caller's evidence assertions to be true. `native_equivalence` explicitly says
that executing this model does not establish equivalence. Malformed typed IDs or
provenance raise ValueError; unqualified spatial numeric cases return UNKNOWN.

[Synthetic input](synthetic-input.json) and [output](synthetic-output.json) are
authored controls with fake identities, not extracted game operands. Reproduce:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/resource_availability.py docs/experiments/resource-availability-milestone-b/synthetic-input.json
```

The command reads its explicit JSON and prints JSON. It does not enumerate native
regions, generate terrain, resolve a save to the selected live frame, schedule
UI events or certify extractor placement.
