# Qualification contract and native boundaries

2026-10-15, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation.
[Authorized brief](../../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_internal_observation_offline_qualification.md`),
[report](report.md), [predecessor boundary inventory](../boundary.md).
Original mandatory G1–G3 criteria are retained; no amendment is adopted.
Authored work is REVIEW-REQUIRED. Native exports and receipts remain LOCAL-ONLY.

## Scope and finite method selection

Read existing exports, installed executable bytes as data, owned source and local
receipts; author/build/run original disposable fixtures; write documents and
review artifacts. No retail code loading/invocation, SFSE observer, package,
deployment, game/debugger action, save/settings change, analysis-project edit,
dependency download or Git mutation. Allowed fixture inputs are authored finite
geometry, register patterns and injected failures. Outputs are owned synthetic
records, text logs, hashes and original source. Risk is confined to the disposable
process and its output directory; unexpected corruption elsewhere is a stop.
Preserve every failed attempt. No automatic cleanup of evidence.

| Candidate | Decision and reason |
|---|---|
| Ordinary CALL replacement | Reject for this question: neither terminal is a CALL; normal ABI volatility is inadequate at an internal edge. |
| Multi-byte inline jump and relocated block | Not selected: entails multiple-instruction relocation, incoming-edge and unwind qualification beyond the smallest terminal test. No decoder/library is imported. |
| One-byte breakpoint, process-local VEH and leaf continuation | Selected for synthetic testing. Only the first byte of one known instruction changes; exception context resumes in an authored equivalent leaf instruction and jumps to the original next instruction. No RIP-relative operand is relocated at the two tested terminals. |
| Hardware traps/external debugger | Not pursued: finite debug-register capacity and separate historical retirement failures offer no advantage for the many required operand-use sites. No debugger execution occurs. |

## Exact static contract

Pinned retail **1.16.244.0**, SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Preferred static VA base `0x140000000`. The following are **RVAs**, not runtime
pointers. Existing P16 export hash is
`3e29f0c813e9a49aa9c53eada6dee052056dfd659979aeea89868fe7c8447aca`.
Primary locators and P15/P17/PS hashes remain in the predecessor inventory.
`static-contract.json` independently checks file bytes and export ordering.

| RVA / next RVA | Observed semantics and preservation obligation |
|---|---|
| `0x021E1060` / `0x021E1063` | Region-entry MOV writes low R8 only. The following instruction has a RIP-relative operand and must not be silently included in a relocated block. Entry replacement is statically inventoried, not executed in the fixture. |
| `0x021E1119` | VSUBPS follows actual broadphase translation; resolved XYZ are on the stack. The fixture does not relocate or claim byte-exact qualification of this instruction. |
| `0x021E174E` / `0x021E1752` | Reject ADD advances RBX by 48 bytes and changes arithmetic flags. Observe region identity first; resume at the following comparison, not at region entry or after that comparison. |
| `0x021E1772` / `0x021E1776` | Accept MOV reads closure+8 into RBX, preserving flags. Observe region identity before it is destroyed; direct count-one and post-cleanup paths join here. |

Broadphase JA at `0x021E1140` rejects; count-one JZ at `0x021E114C` accepts;
zero JZ at `0x021E1154` rejects. Containment/vertex success at
`0x021E145C–0x021E1460` and edge JBE outcomes through `0x021E1714` join cleanup
at `0x021E1761` before acceptance. Source traversal later sets EAX to one at
`0x021E18F2`; it is not the geometric verdict. No preliminary RVA was silently
substituted or treated as a function entry.

Windows x64 internal observation cannot assume volatile registers are dead. The
fixture seeds every GPR except structural RSP/RSI/R15, snapshots those structural
registers too, and compares all live registers including RSP. YMM patterns differ
by register and lane. Both arithmetic-flag patterns and three MXCSR controls are
tested. The handler has compiler-generated ABI stack/shadow space; the probe
retains aligned stack storage and the continuation is a leaf without stack
adjustment. The authored probe has MASM frame directives for its saved GPRs and
stack allocation. This is no proof of retail exception-handler compatibility,
arbitrary unwind/stack walking, dispatch hooks or asynchronous removal.

The full-x87 environment failure is retained, independently of the scoped
SSE/AVX tests. No XSAVE/AVX-512/AMX or whole-machine context claim is made.
The pin describes the native evidence build; it does not make the disposable
binary an execution of Starfield instructions.

## Owned record protocol

Machine definitions are in
[capture.h](../../../../research/internal-observation-qualification/capture.h);
the independent little-endian decoder is
[verify.py](../../../../research/internal-observation-qualification/verify.py).
Each framed record contains a 108-byte packed header, declared copied point
bytes, 64-byte ordered use snapshots and a completion marker. Each point is
four f32 words, ordered XYZ/width, without reconstruction or truncation.

Header fields preserve schema/status/reason, invocation token and parent,
thread/query/source/region identifiers, original admitted count, copied bytes,
use count, independent terminal and verdict, center/radius and sampled MXCSR.
Synthetic identities are authored invocation-scoped identifiers, not persistent
FormIDs or real cache/source objects. A synthetic closure word carries the
invocation token independently into the exception-context RSI ancestry. This
word is fixture instrumentation, not a proposed modification to a retail closure.

Use snapshots retain ordinal/kind, indexed XYZ, actual translation, resolved XYZ,
radius, upper scalar, index and domain. Kinds 1/2/3/4 mean broadphase,
containment, individual vertex resolution and edge resolution. The finite
case-specific trace includes every executed vertex helper and each strip's
resolution. All four edge comparisons share one resolved position, as in P16.
The decoder rejects missing/reordered sites even if the wire frame is complete.
The existing single-query evaluator is eligible only when all consumed resolved
XYZ/radius/upper bits agree. Changing uses remain owned invalid evidence.

Each group owns preallocated storage before returning; the writer never reads a
borrowed pointer. A cooperative source lease covers copying and fixture decision.
Versioned mid-copy ABA mutation is injected and rejected. A successful read or
equal headers cannot prove coherence against an uncooperative unversioned writer;
uncertified sources are rejected before copying. The real native writer contract
is unresolved. The fixed capacity is **8,192 points, 64 uses, 64 records** in this
stress fixture. Capacity violations are sticky instrumentation failures, not
scientific event/session quotas. There is no silent truncation or ring overwrite.

COMPLETE is owned transport completeness; decoder admission additionally checks
use coverage, ancestry, numeric mode and fixture identity. INCOMPLETE preserves
the explicit failure reason and is excluded from comparison; NOT_EVALUATED marks
admission after STOP. No missing terminal becomes false. Duplicate terminals,
late uses, completion after close, read faults, count/use/pool capacity, source
mutation, ancestry mismatch, C++ unwind and STOP preserve prior complete groups.
The fixture writes and fflush/closes all framed groups after capture; it does
not qualify a continuously draining worker, power-loss durability or crash-before-
write evidence retention. Decoder tail-truncation controls retain whole-prefix
groups conceptually but reject the incomplete file as a qualified corpus.

## Mandatory gate criteria

G1 needs concrete state/continuation controls for relevant instruction classes,
both decision edges, concurrency/reentry, interruption and cooperative retirement;
remaining retail assumptions must be explicit. G2 needs independent exact decode
of complete variable geometry and positive/negative ownership tests. G3 needs
actual consumed per-use operands, independently observed terminal ancestry,
representative branch fixtures and unchanged-evaluator replay, with actionable
exclusion of missing or inconsistent inputs. A synthetic PASS never establishes
native spatial equivalence or authorizes further work.
