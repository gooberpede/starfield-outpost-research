# Fabricator selection, state and production contract

[Report](report.md), [definitions](definitions.md), [reuse](reuse.md),
[saved corroboration](saves.md), [shared native register](../native-availability-map/functions.csv).
All addresses are hexadecimal preferred static VAs, base `0x140000000`;
RVA = VA minus that base. Object offsets are hexadecimal. Build is retail
1.16.244.0, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Aliases describe proposed STRONG / STATIC interpretations, OBSERVED-INTERNAL,
REVIEW-REQUIRED. No callable ABI, safe invocation or integration is qualified.
Decompiler argument types are hypotheses; decisive instructions control them.

`e2/NN` means existing `.local-work/e2-organic/native/NNN.request.tsv`;
`e3/NN` means fresh `.local-work/e3-fabricators/native/NNN.request.tsv`.
E1 source locators retain their original [pins](../inorganic-extractors/arithmetic-sources.csv).
Complete local function exports are the evidence unless an instruction span is
specified. Game-derived native text remains LOCAL-ONLY.

## Catalogue and current configuration

Facility classification has separate layers: CONT class, Builders category
keyword `002731a0`, manufactured resource keyword `0023ceb6`, resource-property
support and positive selected resource AV. Display names and tier labels are
insufficient. `140f7cab0` tests the Builders default-object keyword and excludes
the Workshop itself (existing e2-specialist-01). `1409e8700` enumerates positive
resource AVs; `1409e9700` additionally recognizes recipe-bearing resources with
nonempty input requirements (e2/003, e2/006). Temporary reference setup means the
selector is not a side-effect-free operation to call as a detector.

`140f859d0` (e2/004) receives output vector RCX, Workshop RDX, facility/base R8,
require-known byte R9B. It obtains the base property sheet through `14048eba0`,
constructs a temporary reference to classify recipe capability and reads
OrganicResourceType from AV singleton +4c8. Values 1/2 enter planet/species
branches; **zero enumerates AVIF definitions** through `140593280`, form type
`6d`. That is the ordinary fabricator branch. Do not confuse AVIF form type with
runtime IRES byte `9f` or a saved record type.

Fresh vtable `144c25db0` -> callback `140f8be60` (e3/001-002) closes admission:
AVIF +160 must equal 9 (the caller supplies this category; wildcard 0b is not
used here), +15c bit 1 must be clear, then AVIF +148 supplies its IRES backpointer.
IRES fixup `1409e8570` writes that backpointer (e3/003). The callback calls the
common admission with **knowledge byte 1**. It does not evaluate COBJ conditions,
player skill, research, stock or species knowledge. This is a positive branch
contract, not an absence claim from a name search. The alternate no-recipe
capability branch uses callbacks `1409ea3f0`/`1409ea490` before property admission;
it is separately bounded from ordinary recipe-capable constructed fabricators.

The common admission `140f85f80` (e2/005) requires nonnull IRES, recipe +108,
AV +f8 and presence of that AV in the facility base sheet via `14044b610`.
Presence permits a zero-valued supported property. It appends owned stride-10
entries: knowledge byte +00, IRES pointer +08; duplicates OR the knowledge byte.
Thus catalogue membership and current positive selection are different states.
No recipe name, output display text or current input stock is the identity key.

Some tier 2/3 recipe definitions contain Special Projects conditions. Those bytes
remain in the [recipe table](recipes.csv). Generic admission, ordinary application,
input cap and requested-production paths do not themselves traverse/evaluate
that COBJ condition list; it is not the knowledge flag emitted to this builder UI.
Construction research and recipe-construction skill gates remain separate from
changing an existing producer's selected resource. No universal claim that a perk
can never affect fabricators follows from this scoped negative.

`141582340` (e2/005, e2/008) builds WorkshopBuilderDirectoryData with
require-known false. UI uID is the COBJ FormID from IRES +108, recipe +28.
Model +328 maps uID to resource AV and producer reference; current/highlighted IDs
are +370/+374. Recipe product +88 supplies weight/value; IRES supplies the name.
BuildItemData wrappers and owned vector cleanup are documented in the
[E2 layout](../organic-facilities/native.md#ui-producer-consumer-and-choice-mutation).
These are transient model structures, not saved identifiers or public APIs.

**E2 divergence:** `140f86170` (e2/012) only auto-selects the first known candidate
when OrganicResourceType is 1 or 2 and no candidate has a positive AV. Its
`(type - 1) < 2` guard excludes ordinary fabricators. Constructed fabricator bases
instead provide product-preset AV values; do not generalize organic menu-time
initialization to manufacturing.

## Choice application, timer replacement and persistence

The shared UI sends `WorkshopBuilderMenu_ChangeBuildItem` with COBJ uID.
`141717fd0` parses it, optionally queues `141719040` for the engine thread, then
calls `141583410` (e2/012, e2/005). Both old/new model associations and a resolved
Workshop are required. It sets old AV to 0, calls `140f83900` to deregister old
resource, sets new AV to 1 and calls `140f83b90` to register. Model/current ID and
refresh/event operations are not a transactional public configuration API.
Stale IDs or failed ownership resolution need not produce a completed change.

`140f83b90` -> `140f7dfa0` creates the shared resource-keyed producer row:
handle +00, base FormID +04, bookkeeping +08, ceil(base resource AV) integer
iterations +0c, binary32 remaining +10 and interval +14 initially zero,
cached reason-zero eligibility +18; stride 1c. Successful reconfiguration replaces
the old scheduling registration. The former countdown is not preserved by this
path; zero initialization does not prove immediate accepted output. Other
registrations/failed-path behavior must not be inferred from a successful path.

Selection is a PERSISTED AV configuration channel: reference +70 setter virtual
+20 `140b6d190` -> ExtraBF via `140b6cbe0` -> base-value upsert `1419af7c0`,
with reference change mask `80000000`. Base AV rows have AV pointer +00 and float
+08, stride 10. Serializer `1419aec20` writes reference identities, base-row masks
and nondefault values; loader `1419aeff0` restores values/defaults (e2/019-023).
Producer map save/load `140f50660`, `140f515a0`, `140f50880` separately persists
two remapped reference identities plus 17 row-body bytes. Neither wire channel is
a raw runtime-pointer dump. Native handles, saved FormIDs, COBJ IDs and IRES IDs
remain different domains. Restored effective selection and current eligibility
can be changed/recomputed after load; saved configuration is not current authority.

## Connections and upstream input contract

Shared registry `145916580`, lock `1459165d0`, maps **destination handle to incoming
source handle set**. `140f80af0` reverses that membership query to list a source's
direct outgoing destinations. `140f881c0` starts with the consumer, resolves and
deduplicates incoming sources and repeats transitively (e2/003; E1 link exports).
Loops require visited identities; resolved references and temporary arrays have
native lifetime/cleanup obligations. A direct connection is not an input quantity
or a promise of sustained supply.

For local research, retain every directed edge/path and classify terminals as
LOCAL_PRODUCER_REACHED, STORAGE_BOUNDARY, INCOMING_CARGO_BOUNDARY,
NO_IDENTIFIED_PATH (within qualified graph coverage), or UNKNOWN. A storage
reference can have further local incoming edges; record the buffer boundary even
when tracing onward to a producer. A local cargo container does not supply a
native cross-planet graph edge here. No inventory quantities or remote origins
are evaluated in E3. Saved edges use save-era identity resolution and the
separate serializer; never substitute runtime handles for them.

Selection can prune links. Warning predictor `140f81000` (e2/007, e2/011) checks
incoming compatibility against **proposed COBJ +78 ingredients**. Outgoing
compatibility receives the **whole selector candidate vector**, require-known
false, through `140f841c0`. Registration calls `140f81cc0` (e2/013), with incoming
source acceptance through `140f84470` and the same outgoing candidate-vector
test. It removes at most the **first incompatible outgoing membership** per
invocation through `140f81a90`, then exits (instructions
`140f820b9..140f820ef`, E1 removal export e1-native-09). It is not a complete
outgoing sweep and not solely a check of the newly selected product. Later
refresh/graph consequences and failure atomicity remain conditional. Absence of
an explicit inventory clear in the setter does not prove inventory preservation.

The actual outgoing predicate `140f841c0` (e3/003, e2/013) normalizes each valid
candidate IRES's recipe product (including an IRES-product indirection), requires
an eligible product and a destination CONT, then reads destination base +258
filter list. Null filter accepts; present empty list rejects. A populated list
accepts an exact product pointer or a KYWD tested against the product keyword
interface. A failed valid candidate rejects the catalogue. It is not a link
throughput or current stock test. Incoming builder compatibility in `140f84470`
walks the destination's positive selected resources and their recipe ingredients,
accepting a source that can structurally supply at least one ingredient through
`1409e9960`; additional category and topology checks remain in the full shared
function. Link admission and production's all-ingredients stock test are distinct.

More precisely, source helper `1409e97a0` (e3/005) enumerates positive resources,
selects the first with a nonnull recipe/product, and returns that product or the
IRES members of a component list for the special product kind. `1409e9960`
(e3/004) compares its owned set with an ingredient IRES (or the corresponding
special ingredient component list). This is definition/selection compatibility,
not a count of stored items. First-match behavior must not be generalized to
every hypothetical multi-selected resource state. The final `140f843e0` topology
guard delegates to existing traversal `140f894c0`; it is a separate link-policy
dependency, not a sustained-supply proof or a remote logistics traversal.

## Operating eligibility and actual request

`140f7d120` shares E1's current reason contract: halt/group keyword predicate
`140f7cc70` gives reason 9; applicable missing power gives 5; builder one-cycle
input check `140f7f6f0` returning zero gives 7. Reason zero means current native
eligibility, not accepted output. Powered ExtraFlags type 9c mask 40 is separate
from halt, saved disabled flags and cached row eligibility. No distinct universal
activation Boolean is established. [E1 state evidence](../inorganic-extractors/native.md)
controls exact applicability/locking and remaining reasons.

`140f7f6f0` (existing e2-specialist-01/02) obtains current positive selected IRES
through `1409e8700`, recipes through +108 and ingredient list COBJ +78
(count +00/data +08, ingredient stride 18, form +00, required count +10).
It walks transitive incoming references `140f881c0`, totals each required
ingredient through `140b63d40`/IRES-special `140b6bba0`, and caps requested cycles
by floor(available/required). One short ingredient returns zero. No link-only
eligibility rule exists in this path. With nonnull R8, it allocates consumption
rows (source handle +00, units +04, ingredient pointer +08, stride 10), distributing
requirements across sources in native iteration order. RCX is not assigned a
stable semantic argument from these callers; this is not a qualified ABI.

`140f7d6a0` receives producer RCX, selected IRES RDX, due cycles R8D. For Builders,
it caps cycles and prepares source removals. Source virtual +458 receives removal
requests **before** ordinary insertion; IRES ingredients are converted to their
recipe products where required (e1-native-05). It resolves output from recipe
+88, chooses producer/compatible destination with capacity checking, and sends
requested count to ordinary insertion `140b64fc0`. The ordinary branch has no
COBJ NNAM load/multiply; distinguish recipe NNAM from actual cycle/request count.
All ordinary catalogue recipes' product kinds/counts are checked in definitions.
Leveled output is a different path, not an excuse to assert a universal formula.

Insertion's capacity-fit and bookkeeping can alter realization; production does
not inspect its returned count. Subsequent D8 dispatch, refresh and ItemProduced
event count are not an independently observed inventory delta. Nominal capacity,
conditional effective requests and actual accepted output are three different
claims. No stock accounting or throughput simulator is delivered.

## Shared clock and conditional rate

Fabricator registration reaches the same global `140f7ef20` -> `140f7f1e0`
resource-row traversal, not a manufacturing-specific clock. E1 instruction-backed
caller paths remain applicable: frame `1417cbbe0`/`1417cab70` reads engine elapsed
seconds; wait `141a38ba0` supplies converted skipped-time chunks; travel
`141a27d80` supplies its own converted elapsed. Local displayed day, calendar
scale and wall time are distinct. Registered/resolvable Workshops do not prove
every unloaded reference is simulated. See the exact
[clock arithmetic](../inorganic-extractors/arithmetic-clocks.md).

Resource GLOB +48 hours times binary32 3600 gives base duration via `140f7bd20`.
The same timer folds eligible assigned actors then player through A1 operation 3;
`140f7bf10` also reads positive effective HarvesterRateMult through `140f7c000`,
using 1 if nonpositive. The effective duration therefore depends on actual actor
entries/conditions and actual AV state; raw facility PRPS is not that state.
`140f7bf80` is a nominal per-minute helper feeding shared aggregate refresh/UI,
not a per-fabricator actual output measurement. [Reuse/modifiers](reuse.md) and
[definition examples](definitions.md) separate eligibility from current activity.

At elapsed >= positive interval, scheduler due count is trunc(elapsed/interval),
ignoring remaining countdown. Otherwise it subtracts elapsed and yields one cycle
if remaining becomes nonpositive. It loops registration iterations, rechecks
reason for each, requests capped cycles, then resets interval/remaining using
current timer. Overshoot and failed-reason debt are not generally retained.
Binary32 arithmetic, integer conversion and failed-handle bookkeeping retain
E1's finite-domain limits. These are native operations, not measured live rates.
