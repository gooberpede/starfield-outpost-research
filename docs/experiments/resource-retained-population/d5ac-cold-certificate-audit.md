# D5AC cold-certificate audit

**The unchanged schema-4 contract is conservative, and B2's target remains
unqualified for firstness.** A native empty state can exist without a same-epoch
reset certificate. B2 provides a scoped carried-empty example, but its earlier
target decision still defeats constructing-first attribution. D5R OPEN.
[Report](d5ac-report.md), [sources](d5ac-sources.md), [controls](d5ac-tests.md).

## Four separate verdicts

| Layer | Verdict and scope |
|---|---|
| Native behaviour | Constructor initializes empty map/visited storage. Broad reset clears both under ordinary structure invariants. Grid clear/retirement can remove map entries while retaining visited. These are different state transitions. |
| Instrumentation coverage | Eighteen installed sites cover the reviewed ordinary source-lifetime, provider, reset and erasure boundaries. There is no ProcGen constructor-completion/publication witness, explicit map-insertion event or exact lock-acquisition witness. Zero reported loss does not close those coverage gaps. |
| Schema/reducer rule | Sound sufficient witness within the qualified native graph, with deliberate global epoch and reset-only conservatism. It is not a necessary-and-sufficient classifier of every native cold state. No change to installed or production source. |
| Historical B2 sufficiency | Direct target query `[5,0]`, mask `0x3` and token store supported. Same-epoch reset certificate absent. Empty-state continuity is separately derived from reset 113, but earlier eligible decision 8006 precedes constructing decision 8020. Cold-first remains unproved. |

## Current predicate in executable order

The following is a reading of the unchanged source, not a replacement oracle.
`reduce_v4.reduce` wraps the legacy sample-prefix reducer and adds lifetime,
native-order, append and firstness requirements. The full pin and line locators
are in the source ledger.

1. Require unique, contiguous record sequences. Index entries, returns,
   selections, births, publications and lifecycle spans. QPC ties across threads
   are unordered; same-thread callback order can disambiguate a tie.
2. Collect reset begin (kind 10, reason 0), protected Cold (kind 12) and normal
   reset end (kind 11, reason 0), keyed by ProcGen and epoch. Require exactly one
   of each, same thread, status zero, hazards `[1,1,0]`, Cold visited control/data
   zero, admission order begin < Cold < end and valid native order.
3. Qualify each visited identity from one Entry/Selected/Visited context. Require
   zero status/hazards, valid native order, matching owner/request/thread/parent/
   invocation/epoch and matching selected source/frame/selection. Find the most
   recent preceding private birth for that pointer, unique nonzero allocation,
   matching consumed token and loss generation, without reuse through decision.
   Require same birth/entry/visited epoch and one correctly ordered actual
   publication on the birth's Grid/thread. Lifecycle spans, loss bounds and
   unordered native retirement refuse allocation continuity.
4. For Lookup, requalify identity through lookup time, require zero source-copy
   payload, and supply the qualified private birth semantics to the legacy
   reducer. This is an offline join, not a second source-memory snapshot.
5. The legacy prefix requires original request, consistent context and selected
   source; unvisited; one protected map miss (`a == b`); consumed descriptor
   input equal to holder `+0xc8`; one generator/sample with matching geographic
   argument and mask within the low nibble. It requires a same-owner/same-epoch
   reset anchor before Entry, complete earlier activity, first map access/miss
   for that pointer, no geographic collision and boundary admission order.
6. Schema 4 additionally requires the exact valid triad to finish before Entry
   in native order, a unique complete selection path, qualified semantic source
   identity, one Generated/Reserve/Stored outcome and a consistent return. It
   checks native callback order, context, count/capacity/index, exact store
   destination/token, loss continuity, retirement through store and token/
   allocation collision exclusions.
7. Reject prior eligible or unordered decisions for the same geographic key or
   token, and prior unqualified selections over the cold-to-store interval.
   Later bypass is optional corroboration and must follow the store in native
   time for the same qualified allocation and owner/epoch.
8. The enclosing reader authenticates frame/prefix/session identity and terminal
   accounting. Loss, damaged/faulted or unfinished history cannot become an
   unconditional retail firstness claim. Conditional reset-scoped evidence stays
   separately labelled; operational retirement/inert wrappers do not establish
   scientific source lifetime or successful geometry.

## Native sites and different meanings of empty

| Native site, preferred static VA | Schema role | State meaning / limitation |
|---|---|---|
| `0x14079ddf0`, unlock `0x14079dec4` | Fence 0 and Cold | Both stores cleared before protected unlock; complete normal end required. Null-data/nonzero-count corruption is outside valid structure invariants. |
| `0x14079d910` | Fence 1 | ProcGen destruction; cannot be used as an empty live owner. |
| `0x140975030` | Fence 2 | Pointer-map erasure; does not certify visited emptiness. |
| `0x1409829b0` | Fence 3 | Grid clear with optional per-source map erasure and free; does not clear visited. Receiver field is a Grid. |
| `0x140982b70` | Fence 4 | Single-source retirement; visited survives. Receiver field is a source. |
| `0x1409830cd`, `0x140983177` | Birth / Published | Geographic-source private identity and actual Grid publication, not ProcGen initialization. |
| `0x14079f860`, selected `0x14079fa90`, visited `0x14079fca3` | Entry / Selected / Visited | Original request and actual source/token decision; actual consumed-token load precedes the visited capture. |
| Lookup call `0x14079fccb` | Lookup | Pointer-map result and current epoch while exclusive lock held; no lease of source memory. |
| `0x14079feaf`, `0x14079ff18`, `0x14079b8e8` | Descriptor / Generating / Sample | Descriptor conversion, generator and sampler CALL sites; actual consumed normalization also uses `0x14078d6f4`. No full geometry capture. |
| `0x14079ff3e`, `0x14079ff59` | Reserve / Stored | Reserve call and executed token-store bridge; failed reserve cannot be a successful append. |
| `0x14079d660` | Not instrumented | ProcGen constructor initializes empty stores. No observed historical completion/publication anchor. |

Site VAs above identify installed or relevant native boundaries on the pinned
build. They are not runtime pointers. Function entry versus CALL/midfunction
capture semantics are preserved by the source/guard ledger. Owner/context
replacement is handled through the reviewed reset/destruction and source-owner
graph; same owner FormID alone is insufficient to prove object continuity.

## Equivalent anchors and completeness

A new provably initialized ProcGen is mechanically an empty native origin.
Qualifying it would require constructor completion, actual owner publication,
an unambiguous owner generation and full intervening writer/lifetime history.
Ready, process startup, geographic Birth and a reset of a different owner cannot
supply those facts. The constructor-only adverse fixture correctly refuses a
production firstness chain. No historical constructor anchor is claimed.

B2 offers a different equivalent proof: reset end 883 is for the target ProcGen;
the interval before first Entry 2470 contains 47 Grid clears but no provider or
append and no destructor/reset/replacement fence. The audited ordinary native
mutation graph establishes that Grid clears can only remove population entries
and do not add visited tokens; private source births/publications do neither.
Both stores therefore remain empty at the end of the last clear in epoch 207,
under that scoped graph. This proof needs no hypothetical new constructor.
The local `carried-empty-oracle.json` records the evidence interval, not a new
schema-4 chain. Other sources populate the map after demand begins.

This separates an instrumentation/representation completeness gap from a false
positive defect. The production rule loses useful state continuity through
global lifecycle fences, even when a particular source is born after the last
fence. Preserving allocation invalidation remains essential: an empty ProcGen
does not make retired geographic pointers safe. A future rule must track these
two propositions independently and must not relabel epoch 207 cold by fiat.

## Defect and remedy decision

**NO-CHANGE for production under this brief.** The conservative coverage gap is
documented; there is no demonstrated false-positive target qualification.
If separately amended, add an analysis-only native-state continuity proof that
carries an authenticated same-owner reset across removal-only operations while
retaining independent geographic allocation fences. Tests must include unknown
mutators, omitted lifecycle observations, wrong owner/generation, pre-arming
initialization, delayed admission, concurrent reset, source reuse/collision,
earlier decisions and loss/fault intervals. Such a correction still cannot make
8020 earlier than 8006. A ProcGen-constructor witness is a separate optional
design requiring native qualification and deployment authority, not a prerequisite
to explain this B2 episode.
