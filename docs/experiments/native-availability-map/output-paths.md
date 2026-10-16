# Prospective and established output association

2026-10-16. [Build and output contract](output-contract.md),
[existing function register](functions.csv), [assessment](completion-assessment.md).
All entry points are RVAs for the pinned 1.16.244.0 executable. Windows register
roles come from actual call instructions, not inferred decompiler prototypes.

| Stage | Prospective preview | Established Workshop |
|---|---|---|
| Caller/reference | N02 `0x021b41f0` resolves the selected reference from operation+268; held RBX reference is converted by N06 `0x00b4cee0`. | N03 `0x021b2570`, context+630==0, resolves Workshop via `0x00f3df70` from +268 and calls N05 `0x00f4a140`. N04 `0x021b64c0` supplies another descriptor/transition path. |
| Area construction | Indexed binary32 XYZ/index/domain; converter qualifies domain types 49/56 or sentinel and has precision/global branches. Radius and upper are operation+360/+364. | Builder derives center through `0x00f4ab80`, radius through `0x00f38e30` to descriptor+28, upper through height+setting to +2c, with component-top override. Status/early returns can preserve initialized defaults. Lower +30 is separate and is not an updater operand. |
| State | Initialized operation owns S=operation+520; constructor and caller state predicates apply. The function takes prior caches as well as area operands. | Same S layout and caller lifecycle prerequisites. Descriptor stored at operation+338..36c; independent area bounds are not implied by matching centers. |
| Convergence | ui15 `1421b42d1..42e3`: RCX=S, RDX=indexed descriptor, XMM2=radius, XMM3=upper → `0x021e07d0`. | ui15 `1421b26a8..26bc`: RCX=S, RDX=descriptor, XMM2=descriptor+28, XMM3=+2c → same updater. Transition call at `1421b6931` is separately mapped. |
| Output/consumer | Three mutable populations; refresh event 7 requests model command; UI later reads shared ranges and constructs rows. | Same statically mapped operation storage and shared UI consumer; no separately returned per-Workshop durable result or keyed output archive is established. |
| Runtime support | 35,573 natural preview calls. Held reference base was `Starfield.esm:015804`, `OutpostGroupPackinDummy`, not a placed beacon. Proposed position was captured; player XYZ was not substituted. | One initialization-site evaluation was captured; its call-site label alone does not prove an established selected Workshop or equality with a preview/loaded save. Established-Workshop descriptor/state/output equality is NOT TESTED. |

Primary locations: ui15 caller windows above and complete caller decompilation;
`workshop-origin-03.tsv:140f4a1ba..2eb`, `140f4a41b..43e` for radius/upper;
ui17 N06 for indexed conversion; ui08/09 for shared UI consumption. Exact hashes
are in [sources.csv](sources.csv). The original
[dataflow](dataflow.md#1-caller-supplied-and-derived-operands) records instruction
roles and descriptor offsets. The
[070 report](../continuous-beacon-preview/live-scientific-report.md) controls the
observed actor and capture scope.

**Assessment:** static convergence is sufficient for the limited research
endpoint. A reader can follow the established reference and descriptor to the
same output-storage schema and consumer. Missing established runtime observation
limits claims about actual descriptor values, selected-Workshop association,
readiness, after-load freshness and equality; it does not leave an unidentified
essential function or result representation. No per-site authority is claimed.
The UI command has no evaluation/position snapshot, so association cannot be
repaired by nearby timestamps, matching centers or equal sets. No additional
experiment is required solely to make the two columns symmetric.

The updater reads current-manager resident geometry, atmosphere and spatial
biome internally; it does not synchronously request full generation at this
boundary. [Provider/lifecycle](region-lifecycle.md) and
[requirements](region-requirements.md) distinguish source residency, attempted
construction, completion, player presence and freshness. Independent remote
context preparation and freely invoking the operation remain unknown, separately
from the static established caller mapping.
