# D5X architecture decision before implementation

2026-10-30, Australia/Sydney. Status: proposed implementation choice, offline only.
[Contract and live ledger](d5x-investigation-ledger.md). No retail GO.

Choose a purpose-built narrow witness, conceptually reusing the maintainer-owned
D5P-R1 transport and patch admission. Do not retain geometry capture, wrapper
enumeration or ordinary-Grid membership. Hook count alone is not an overhead
measure: the necessary selection and invocation witnesses can increase site
count while removing point arrays and all container traversals.

| Route | Evidence and coverage | Cost, safety and diagnostic yield |
|---|---|---|
| Narrow D5P-R1 | Existing durable-prefix transport, lookup/sampler wrappers and five lifecycle fences are useful. Its current invocation starts at visited, its source validation scans mutable Grid storage, and it captures region geometry. | Reusing it unchanged cannot establish original provider entry or all selected sources. Removing its scientific reducer is effectively a new contract. Keep R1 unchanged and reuse only explicitly identified owned methods. |
| Purpose-built witness | Provider entry/return, selected cursor load, visited branch, protected lookup result, actual converter descriptor, generator scope, direct sampler result, reset/destruction/erase/clear/retire witnesses. | Bounded fixed records, no native helper calls for identity, no locks acquired by observer, no source dereference at selection. Protected lookup copies bounded source bytes; converter copies actual descriptor. Per-thread stack scopes prevent nested joins. Native calls/arguments/results are forwarded unchanged. More sites than an entry-only design, much lower payload than geometry tracing; actual pressure must be measured. |
| Generator/sampler only | Exact mask and generator source but no original-request provenance, visited/hit distinction, selection-only failure or cold evidence. | Smallest instrumentation, insufficient identical claim. Adding stack guesses recreates unqualified joins. Reject as scientific candidate; retain as a diagnostic weaker outcome. |

The provider entry first seven bytes are non-RIP-relative MOV instructions;
relocate only that checked prefix. CALL wrappers preserve the Microsoft x64 ABI.
Inline selection and visited bridges must preserve volatile registers, vector
registers and flags and replay the exact displaced instructions. Reject any
build/site guard mismatch before writing. Sole-thread installation is required;
general asynchronous exception unwinding remains a separate qualification risk.

Source pointer is recorded at selection without following it. At lookup return,
the original engine exclusive interval is active. Copy bounded source descriptor
only when no lifecycle hazard or epoch transition overlaps the invocation.
Geographic key and pointer lifetime are distinct. No descriptor collision may
merge allocations. Reset, retirement, destruction, erase or Grid clear invalidates
continuity; ordinary queue loss does likewise without disabling acquisition.

Cold evidence requires a completely witnessed broad reset of the actual ProcGen,
not READY or Save52 loading. The independent native review identified the stronger
anchor: wrap the unlock CALL at preferred static VA `0x14079dec4`, after map and
visited clearing and before releasing that same exclusive lock. Preserve all
lookup attempts around reset and reject overlapping lifecycle hazards. Reducer must
account for earlier misses even when their own context is invalid; otherwise a
later valid miss could be falsely promoted. Fresh first construction after loss
requires a new qualified reset; post-loss acquisition itself continues.

The planned witness deliberately excludes later cache retention, source population,
resource membership and frequency claims. Both ordinary Mask 0 and Mask 3 are
valid observations. Production hook code and independent reader must be exercised
together in a disposable native host before claiming any qualified candidate.

Permission remains pending for extending the pinned SFSE header to a new D5X
plugin. Native host work and static verification do not depend on that permission.
No substitute interface derived from that header will be used to evade the gate.

That paragraph records the initial permission gate. The maintainer subsequently
approved the exact extension, recorded in ledger checkpoint 3 and
[PERMISSIONS](../../PERMISSIONS.md#d5x-pinned-sfse-header-extension--2026-10-30).

The review also identified a sampler-only stack witness. Fixed saved-frame and
return-address checks could recover original inputs at one positive boundary.
It still needs lifecycle/cold observation and cannot distinguish provider absent,
selection-only, visited bypass, map hit or skipped sampling. Those are mandatory
diagnostics, so it cannot replace the proposed checkpoints for Q2/Q3. It also
adds fragile stack arithmetic that the explicit provider scope avoids.

## Consumed-descriptor correction before final qualification

Independent static challenge found that a pre-converter copy of mutable manager
storage cannot prove which words the engine consumed. Converter
`0x14078d660` copies fields into its own stack at `0x14078d68e..0x14078d6e1`;
temporary descriptor writes at `0x14078c82a..0x14078c88e` are not covered by the
five original lifecycle fences. Known ordinary writes often copy unchanged
values, but that is not a runtime stable-copy certificate.

Adopt one additional CALL wrapper at preferred static VA `0x14078d6f4`, targeting
normalizer `0x14096f5c0`. Capture its actual engine-local descriptor in RDX and
copied original Int2 in R8, only while the provider's converter wrapper owns a
matching thread-local conversion scope. Forward the native call unchanged.
This supplies the actual consumed frame with no writer census, extra native
lock, engine identity helper or mutable Grid scan. Unrelated conversions pass
through without emitting. The final candidate therefore has fourteen sites.

Descriptor padding bytes `+0x01..+0x03` are raw/uninitialized engine-local bytes;
preserve them but exclude them from semantic comparisons. The meaningful chart
and `+0x04..+0x2b` fields are captured before original normalization. Source
local anchors can also change in the inspected shift loop; copied geographic
fields remain separate. Do not call the entire source prefix immutable or an
observed generator-origin snapshot.

Version the corrected contract as observer 0.2.0, schema `sor-d5x/2`; preserve
all schema-1 development binaries/readers/receipts. This changes implementation,
not the frozen questions or acceptance criteria. Requalify the exact final
package, including a controlled input that changes and restores manager storage
around the engine-local copy, plus the 64-bit sequence and ABI boundary controls.
