# Reproducing the D5AQ fixed fixture from local files

**D5BJ is a local Option C checkpoint.** The methods execute the pinned
Starfield instructions for C1 numeric conversion and sampling, complete fixed
ordinary geometry, and bounded queue, service, source and retirement controls.
The [original D5AQ conclusion](../../experiments/resource-retained-population/d5aq-report.md)
composes these kinds of controls with static reasoning about the ordinary
startup and provider path. Native feasibility is separate from retail
occurrence, frequency, effective-input equality and full game determinism.

| Question | D5BJ disposition |
| --- | --- |
| Q1 · Input and method inventory | **INCOMPLETE.** The runnable tiers have explicit inputs. The entire exact fixture still depends on historically qualified component initialization and preparation premises. The public D5AS and D5BI access routes require clearance and hosting. |
| Q2 · Native computation and feasibility | **INCOMPLETE.** C1 numeric, fixed three-resource geometry and the named native transition controls execute locally. Exact reader-input composition of all preparation and source-to-first-miss prerequisites remains open. |
| Q3 · Evidence reuse and independent reader test | **INCOMPLETE.** The local isolated tests supply byte-identical staged D5AS and D5BI candidates. The full fixture and hosted-input test remain conditional. |
| Q4 · Reader contract and policy | **COMPLETE for the authored local checkpoint.** [Publication policy](../../PUBLICATION.md#reader-supplied-game-inputs) and the [run card](../../PUBLICATION_RUN_CARD.md) separate runnable methods from release readiness. |
| Q5 · Feasibility and fallback | **INCOMPLETE for the full exact route.** Bounded native reproduction is feasible. A complete lawful public route for the full fixture remains unqualified. The smallest existing comparison tier reuses D5AS and D5BI without a new derivative. |

The [dependency matrix](dependencies.md), [continuation audit](continuations.md),
[qualification record](qualification.md) and [investigation ledger](investigation-ledger.md)
state which edges were exercised. The release remains **NOT READY / NOT CLEARED**.

## Supply these files

Use your own lawful files for **Starfield 1.16.244.0**. Exact bytes determine
compatibility. The main file is the only definition namespace used by these
fixtures. Effective loaded overrides, plugin state and configuration of a
retail episode require separate evidence. This procedure begins with files
you already have.

| File | Required SHA-256 |
| --- | --- |
| `Starfield.exe` | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| `Starfield.esm` | `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7` |
| `Starfield - PlanetData.ba2` | `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5` |
| D5AS `d5as-feynman-geometry-v1.zip`, for geometry | `d0d35ed2193527dd8215a647178614a5403e814bf14c3f9d1f0a448c53a1043c` |
| D5BI `SOR-D5BI-N2-projected-evidence-v1.zip`, for N2 | `a47bbd302553755d0fe87d746234d0d6c527ee7297cfda2e38915072edb7c3d7` |

The two proposed evidence ZIPs are pending file-specific clearance, approved
transfer and retention, B6 and hosting. This checkout contains their methods
and manifests. The ZIPs are provisioned separately. [D5AS contract](../evidence-access-d5be/d5as.md) ·
[D5BI contract](../evidence-derivative-d5bi/README.md)

The native commands require Windows 10 build 19045 and AMD64 CPython 3.14.3.
They check the interpreter EXE SHA-256
`cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`,
system `ucrtbase.dll` SHA-256
`3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9`,
and AVX, FMA3 and enabled SSE/YMM state. The tested CPU was an Intel Core
i7-10700F. Other OS/CRT/Python builds and non-AMD64 platforms are outside the
native support contract. The N2 join uses CPython 3.14.3 and the standard
library without game inputs. Use an ordinary local directory and file paths
for the native inputs. Keep at least 40,000,000,000 free bytes per involved
volume.

## Run in a clean source tree

From the root of a fresh checkout, replace the placeholders below. Invoke
each native command in its own process. Use a separate caller-owned, empty
directory if you redirect stdout and stderr. The procedures require neither
a Ghidra project nor Steam version retrieval.

```powershell
$py = '<compatible python.exe>'
$exe = '<path to Starfield.exe>'
$esm = '<path to Starfield.esm>'
$ba2 = '<path to Starfield - PlanetData.ba2>'
$d5as = '<path to exact D5AS ZIP>'
$d5bi = '<path to exact D5BI ZIP>'
$src = 'research/resource-retained-population'
$gameInputs = @('--exe', $exe, '--esm', $esm, '--planet-data', $ba2)

& $py -I -B -X faulthandler "$src/d5bj_sampler.py" @gameInputs
& $py -I -B -X faulthandler "$src/d5bj_geometry.py" @gameInputs --d5as $d5as
& $py -I -B -X faulthandler "$src/d5bj_dispatch.py" --exe $exe
& $py -I -B -X faulthandler "$src/d5bj_sources.py" --exe $exe --esm $esm
& $py -I -B "$src/d5bj_n2.py" $d5bi
```

Each program reads explicit inputs and emits JSON on stdout after its checks
pass. A missing file, hash mismatch, unavailable preferred address, incompatible
host or failed comparison stops that process. For an address collision, use
a fresh process. For a hash mismatch, supply exact compatible inputs. A fault
in the private fixture process invalidates that run. Preserve stderr and the
exit code for diagnosis.

The native programs copy a fixed PE page set into their own address space and
execute selected original instructions using the Windows x64 ABI. Pages are
writable during setup and executable after protection changes. Named private
dispatch, import, allocator and callback substitutions are part of the tested
fixture. The subprocess is a boundary for memory lifetime, rather than an OS
sandbox. See the [execution inventory](dependencies.md) before running.

## What success means

- **Sampler.** Each of the two original arithmetic branches checks all 196
  signed C1 Int2 requests against the independent atlas calculation and the
  historical coordinate table. Exact sampled atlas cells are reconstructed
  with encoded synthetic rasters. The authentic raster yields 28 masks
  `0x0` and 168 masks `0x3` per branch. Fine Y +1 changes the sampled mask
  at 14 coordinates.
- **Geometry.** Each run supplies masks computed by both original sampling
  branches to the fixed ordinary stage. It checks 144 native packed cell keys and the full
  three-resource output against the planar model and both canonical D5AS
  reference bodies. Mask 0 produces 74 regions and 193 points. Mask 3
  produces 78 regions and 180 points. The second mask-3 query produces
  identical represented geometry. The emitted digests are receipt identifiers.
  The verification itself compares complete bytes in memory.
- **Service and source controls.** The two queue orders cover all 1,720
  registrations. Direct/shared queue contrasts and private populated command
  controls check service without starting workers. Source controls check the
  static LoadingCells dependency closure, selected C1 corner slots, target
  token low-word uniqueness over 324 admitted sources, and the Grid shift
  and retirement predicates. The [continuation audit](continuations.md)
  separates these executions from the composed first-miss path.
- **N2.** D5BI's exact projected evidence independently supplies 196 density
  and 196 distinct layer allocations at the same coordinates. The sole
  historical sampled constructor is `(-2,11)` with mask `0x3`, sequence
  3962. The other 195 rows retain their conditional interpretation.

Keep the numeric and comparison receipts local until reviewed. The procedures
keep native pages, the decoded raster and the reference comparisons in memory.
Process exit releases the fixture memory. The caller owns any redirected logs
or staged candidate copies. [Reader input and publication policy](../../PUBLICATION.md#reader-supplied-game-inputs)
