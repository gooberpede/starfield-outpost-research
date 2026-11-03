# D5AM ordinary owner-lock caller census

The earlier three-reader-release assumption was insufficient. Fresh offline
analysis found **three more shared releases and two inline writer releases** on
the watched ProcGen lock. The new candidate therefore needs sixteen causal
sites, including six typed shared decrements and the two inline writer
decrements. This is a correction to the earlier coverage proposal, not a new
retail observation or permission to deploy.

All addresses below are preferred-image virtual addresses for the pinned
1.16.244.0 executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
They are neither live ASLR pointers nor FormIDs.

## Method and preservation

The owned D5AI manager census supplied the initial receiver-rooted question.
D5AM actually repeated it on a fresh verified copy of all fifteen pinned
analysis-core files under `D:/tools/sor-d5am-owner-census01`. The original project
was never opened. The first export used `-readOnly -noanalysis`, authenticated
both original and copied core before and after, and retained its full command,
script, output and result. Later exports reauthenticated that same copied core
before and after each read-only invocation. Original preservation from the
first export is an explicit inherited receipt, not an invented postcondition of
each later wrapper.

Reproducible authored methods are
[the fresh-copy exporter](../../../research/resource-retained-population/d5am_owner_census_export.py),
[the copied-core follow-up](../../../research/resource-retained-population/d5am_owner_function_export.py),
[the native exporter](../../../research/resource-retained-population/D5AMOwnerCensus.java),
and [the byte audit](../../../research/resource-retained-population/d5am_owner_census_audit.py).
These adapt maintainer-owned D5AI/D5S methods under SOR-P-0002. Raw instructions,
bytes and analysis-project files remain ignored local data.

The first running exporter was hardened after launch to reject optimization
before imports. Its exact launch source remains
`.local-work/d5am/owner-census01/method-at-launch.py`; the old receipt still pins
those bytes. The subsequent scripts use early ordinary optimization guards,
fresh non-reparse outputs and both free-space floors. Their receipts additionally
pin the interpreter, installed Java executable and Ghidra utility JAR. This
guard-only change does not retroactively rewrite the first execution.

| Fresh local export and audit | Actual inspected scope | Verified instruction bytes |
| --- | --- | --- |
| `owner-census01` | Generic shared/exclusive/release helper references; provider, reset/destructor and area bodies | Imported program identity plus original/copied-core preservation; initial exporter has no per-instruction byte column. |
| `owner-census02`, `owner-census02-audit04.json` | Nine explicit caller windows, including three nearby apparent shared users, reset, point, area and provider | 2,472 unique instructions, 10,257 bytes agree exactly with installed PE. |
| `owner-census03`, `owner-census03-audit04.json` | Eleven ProcGen methods/clients reached from manager `+0x130` | 1,673 unique instructions, 6,688 bytes agree exactly. |
| `owner-census04`, `owner-census04-audit04.json` | Eight remaining nearby shared-helper call windows | 1,808 unique instructions, 9,570 bytes agree exactly. |
| `owner-census05`, `owner-census05-audit04.json` | Union of 392 functions containing direct manager-singleton references and 82 manager-interval functions, with five overlapping functions: 469 total. There are 760 raw singleton references; the interval is `0x140787000..0x140790000` | 164,449 unique instructions, 695,339 bytes agree exactly. This authenticates bytes; it does not assign ProcGen semantics to every unrelated instruction. |
| `owner-census06`, `owner-census06-audit01.json` | Six forwarded receiver/context bodies, including `0x1407a38c0` and `0x1407a3b00` | 2,233 instructions, 9,027 bytes agree exactly. |
| `owner-census07`, `owner-census07-audit01.json` | Four cache/context/iterator bodies | 1,608 instructions, 6,155 bytes agree exactly. |
| `owner-census08`, `owner-census08-audit01.json` | Callback continuation, cache getter, exact-word mutex primitive and map lookup | 277 instructions, 949 bytes agree exactly. |
| `owner-census09`, `owner-census09-audit01.json` | Reference callback continuation and three cache-map primitives | 526 instructions, 2,054 bytes agree exactly. |
| `owner-census10`, `owner-census10-audit01.json` | Exact copy/invoke wrappers for the captured creation functor | Eight instructions, 33 bytes agree exactly. |

The fresh root export identifies the real ProcGen owner through manager
`+0x130`, rather than treating every global lock-helper caller or every nearby
address as that owner. The generic shared helper has 3,393 direct call references
in the retained prelock export; their receivers are not interchangeable. The
applied review follows manager/ProcGen receiver loads, direct method calls,
actual lock operands and paired releases. It excludes stack `+0x130` operands,
other singleton receivers and nested cache locks by their demonstrated bases.

## Material receiver paths and corrected coverage

| Receiver/path | Exact native boundaries | Consequence for the instrument |
| --- | --- | --- |
| Provider ProcGen `+0x40` | Shared call `0x14079fc45`, decrement `0x14079fc85`; exclusive call `0x14079fcb3`, release-helper call `0x14079ffa5` | Existing typed decrement plus generic admission/release bridges. |
| Point consumer ProcGen `+0x40` | Shared call `0x14079df9b`, decrement `0x14079e027` | Existing typed decrement. Other point callers reach this same consumer; their different requests do not create new release sites. |
| Area consumer: manager `+0x130`, then ProcGen `+0x40` | Shared call `0x1421e09ed`, decrement `0x1421e0a87` | Existing typed decrement. |
| ProcGen method `0x1407a50d0` | Separately owns ProcGen `+0xd0`; conditionally acquires shared `+0x40` at `0x1407a5133`; shared decrement `0x1407a51b7` | **Add** reader-release site RVA `0x7a51b7`. The distinct `+0xd0` lock must not be attributed to `+0x40`. |
| ProcGen method `0x1407a5210` | Separately owns `+0xd0`; two branches acquire shared `+0x40` at `0x1407a52c0`/`0x1407a53d9`; decrements `0x1407a5386`/`0x1407a547c` | **Add** both reader-release sites. Branches and releases must remain distinct site identities. |
| Reset `0x14079ddf0` | Exclusive `+0x40` at `0x14079de83`, release `0x14079dec4`; then distinct `+0xd0` at `0x14079ded3` | Generic watched-owner admission/release covers the material first lock without conflating the second. Whole-reset uncertainty fencing remains unchanged. |
| Owner map client `0x140982b70` | Manager `+0x130` then `+0x40`; exclusive call `0x140982b9c`, release `0x140982bc9` | Generic bridges include this user without provider TLS. |
| Owner map client `0x1409829b0` | Manager `+0x130` then `+0x40`; exclusive call `0x140982a16`; final decrement `0x140982a5a`, recursive decrement `0x140982a92` are inline | **Add two inline writer-release bridges**; the generic release helper alone misses them. Preserve incoming ECX delta, returned old ECX and arithmetic flags. |
| ProcGen destructor `0x14079d910` | Existing destructor hazard/epoch boundary; no owner-map lock acquisition | A lifecycle uncertainty fence, not a fabricated release or additional lock holder. |

The three new reader sites have the same original six-byte XADD/MOV sequence as
the existing typed decrement bridge. The new inline writer sites each displace
exactly one five-byte XADD. The following branch destination at
`0x140982a97` remains intact. Native input delta and pre-atomic owner word are
copied and validated; a wrong input is a recorded invalid-operand failure,
not an inferred fixed transition from the site label. The new typed methods
contain no YMM instructions; their relevant native continuations do not consume
a live upper-YMM value across these inline sites. The exact bridge ABI and
unwind tests remain required for the resulting candidate object.

Nearby apparent alternatives were actively checked. Calls at
`0x14079c942` and `0x14079ec1e` use manager `+0x24`;
`0x14079e616` uses a referenced cache object `+0x18`;
`0x1407a2aba` and `0x1407a31de` use nested objects `+0x20`;
`0x1407a6915` and `0x1407a6fe3` use a different singleton `+0x30`;
`0x1407a6c1a` uses a returned cache object `+0xb8`.
These are evidence of different receivers, not extra watched-owner releases.
ProcGen methods reached through the manager field, including
`0x14079da80`, `0x1407a1940`, `0x1407a0fa0`, `0x1407a4cc0`,
`0x1407a4b90` and `0x1407a1f80`, were exported as well; their bodies do not
introduce another direct watched-lock shared decrement in this mapped graph.

## Forwarded receivers and captured contexts

Independent review correctly challenged stopping at a caller with no direct
lock instruction. That is insufficient where it forwards the actual ProcGen
pointer. D5AM followed those aliases through fresh copied exports 06–10:

| Ordinary entry/forwarding chain | Actual owner-pointer use and disposition |
| --- | --- |
| `0x1407a4b90 -> 0x1407a4cc0 -> 0x1407a38c0 -> 0x1407a3b00` | ProcGen is forwarded and then stored as context element zero. The old absence-of-direct-call observation is not used to terminate this chain. |
| `0x1407a3b00` local reference callback | Vtable `0x144b3f1a8`, slot `+0x10`, resolves to `0x1407b1410`; iterator `0x140b1e190` actually invokes that slot. It forwards through `0x1407b1bd0` to `0x1407a4730`. Here the first argument is the larger captured context, not a ProcGen base. Context element zero forwards ProcGen only back into the already inspected `0x1407a3b00` recursion. Other callback arguments are separate placement/reference contexts and actor objects. The iterator's own lock is referenced-object `+0x118`. |
| Creation functor captured by `0x1407a4b90` | Vtable `0x144b3efe8`: `+0x08` copy is `0x1407b0990`, which copies the captured word at `+0x08`; invoke `+0x10` is `0x1407b0980`, a tail jump to `0x1407a6700`. The latter does not load the captured ProcGen member. Its incoming closure argument is only spilled to its ABI home slot, later reused for a scalar key; it does not become a ProcGen receiver. Its two shared locks use the other singleton `+0x30` and returned cache `+0xb8`, already classified above. This discharges the actual unused capture rather than presuming captures harmless. |
| `0x14079da80`, `0x1407a1940`, `0x1407a1f80` | Besides the already covered provider call, forwarded `0x14079e220 -> 0x1407ac4d0` uses ProcGen `+0x130` as an exact-word mutex and `+0xf8` as a cache map. This is a second offset domain: ProcGen `+0x130` is not manager `+0x130`, and neither is the watched `+0x40` lock. Returned cache objects use their own `+0x18` locks. |
| `0x14079ea40 -> 0x1407ad160 -> 0x14079e6d0`; `0x1407a0fa0 -> 0x1407adc60` | The latter explicitly carries ProcGen as context element eight into the same `0x14079e6d0`. Its forwarded cache getter `0x14079e060` uses the same ProcGen `+0x130` mutex and `+0xf8` map. `0x140323460` operates on the exact supplied word, not a parent object recovered through a negative offset. `0x1407aa310/0x1407aa0b0` use that map subobject; `0x1407ab260` ignores its container argument while hashing twelve key bytes. `0x1407aa930` assigns reference-counted cache values. These paths introduce no additional watched-lock decrement. |
| `0x1407a5210 -> 0x1407a6150` | The callee explicitly takes the distinct ProcGen `+0xd0` mutex, including its inline release. Its caller's `+0x40` reader intervals are covered by the two newly added typed release sites. |

The two callback vtables were also read as four little-endian 64-bit words from
the pinned PE at RVAs `0x4b3f1a8` and `0x4b3efe8` using the owned PE reader.
Their 32-byte SHA256 values are respectively
`4cdf8b3fa177a9313e768676897cf1820f1f7efae34a955fa3e7a6b11d347d00`
and `75aef7cc36e619b76338f2e55ab4016752ec338fc8dcea289717f623a8b2fde1`.
Local receipts `owner-forwarding-vtable01.json` and
`owner-forwarding-vtable02.json` retain the four decoded values. The native
LEA, slot call, data references, copy and tail-jump bodies independently anchor
which slots are actually used. These are static analysis facts, not newly added
runtime vtable hooks.

## Scoped sufficiency and remaining trial predicates

The corrected sixteen-site proposal covers the demonstrated ordinary
receiver-rooted lock graph, including non-provider users and inline releases.
This closes an actual missing edge discovered during D5AM, rather than leaving
the census as prospective review paperwork. Its final native, ABI, STOP and
adverse-operand qualification is a separate required gate.

This is not a theorem excluding arbitrary computed replacement clients or
unapproved modifications to the executable. Production guards, ordinary-path
admission and actual trial accounting must still hold. Unjoined tasks,
unsupported owners, unknown initial history, uncertain lifetime snapshots,
unmatched cohorts or unexplained atomic state changes refuse the dependent
ordering conclusion. They do not become absence claims or reasons to discard
an inconvenient but otherwise healthy scientific trial. The final independent
review must assess this scoped source argument together with actual qualified
records; the byte audit alone cannot accept the mechanism.
