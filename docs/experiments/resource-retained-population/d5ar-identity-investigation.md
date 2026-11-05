# D5AR source and outpost identity investigation

2026-11-05, Australia/Sydney. **Resident geometry, source allocation and current
outpost are separate identities.** A checked raw-source observation can preserve
useful diagnostics without certifying any of them. D5AR-Q2 remains INCOMPLETE
while the native association branches below are pursued; GC-10, GC-31 and D5R
remain OPEN. Authored synthesis and helper sources are REVIEW-REQUIRED; original
native instructions and full receipts remain LOCAL-ONLY.

| Element | Supported result and boundary |
| --- | --- |
| Question | Can a protected on-demand resident-map capture identify its geographic sources and current outpost without a Feynman-specific key or historical construction hooks? |
| Best-supported answer | The exact established operation supplies a selected registry reference copied while its native local lease is live, with operation scope and command-generation binding. This identifies the selected reference at resolution, without claiming unique player ownership or physical area. Source fields and a recoverable native planar basis are supported separately; allocation admission additionally requires permanent ending history and a gated copy, because map membership alone is insufficient. |
| Confidence / basis | STATIC for original instruction edges; CONTROLLED for the separately pinned helper, original lease/retirement/rehash and ABI controls below. Integrated method/source-lock admission and original scientific comparison gates remain subject to independent review. |
| Coverage | Starfield 1.16.244.0, executable SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; preferred static image base `0x140000000`. Every address below is a preferred static VA; member offsets are bytes. |
| Exclusions | No current-outpost census, construction-frame reconstruction, body-owner certificate, geographical absence or retail operation follows from a raw pointer/scalar match. |
| Next action | Review exact ending-history and operation-scope integration; finish effective non-mask generation-input reconstruction and saved-component closure. Per-use indexed translation remains a separate physical-area barrier and is not required for raw source-planar equality. |

## Applied reading and experiment boundary

The complete D5AR brief, AGENTS, README, third-party policy and charter were
read. WORKFLOW's completion/continuation, required-reading and healthy-run rules,
the evidence standard's confidence/coverage/identity rules, D5AI complete source
ownership/frame contract, D5AB P1 identity/lifetime matrix and owner-context
rework govern this investigation. Their concrete effects are to preserve original
Q2, separate raw observation from source leases, retain old source-retirement
counterexamples, continue native callers across subsystem boundaries, and avoid
claiming current manager equality supplies a historical construction frame.

Only existing source/native records, installed PE bytes and a hash-verified
disposable Ghidra copy are read. The new diagnostic fixture uses owned arrays
and the installed compiler. Separately declared native controls below execute
pinned original instruction ranges against owned arrays in disposable Python
children; none opens a game process.
No save, original database, configuration, installation, Git index/ref or remote
is changed. Both caller-available drive floors are checked before/after output.
Failure preserves local logs/partials. SOR-P-0002 covers the project-owned
export/field-research methods; no new third-party implementation is incorporated.

## Exact source fields and their limitation

[D5AB P1](d5ab-p1-source-identity-lifetime.md), especially L02/L06, positively
traces the immutable selected scalar family initialized by constructor
`0x140982d90`: terrain FormID at source `+0x00`, chart byte `+0x38`, and six
coordinate words at `+0x3c`, `+0x40`, `+0x4c`, `+0x50`, `+0x5c`, `+0x60`.
The separately consumed visited token is `+0x68`. Padding, the additional descriptor
words, dimension operands and later `+0x178` metadata are excluded from this
29-byte projection; later diagnostic groups retain the complete descriptor and
proven origin inputs separately.
Original constructor stores include `0x14098301b`, `0x140983085`,
`0x14098308d`, `0x140983095`, `0x1409830a5`, `0x1409830ad`,
`0x1409830bd`, `0x1409830c5` and `0x1409830c9`.

The [new helper](../../../runtime/outpost-geometry-snapshot/identity.h) reads
exactly 29 selected bytes in that order and separately reads the u64 visited
token, exclusively through a checked reader. SOURCE_BYTES_UNQUALIFIED means
only that every requested read completed. READ_FAILED means no scalar payload
is emitted. Neither status proves that an address still designates the original
source allocation. A reused address can contain unrelated bytes; matching those
bytes cannot supply allocation history, current body or geometry coordinates.

The helper now independently preserves four origin-input words `+0x10`, `+0x14`,
`+0x20`, `+0x24` as a separate 16-byte group. Original provider
`0x14079fab8..0x14079fad6` computes binary32 origin from integer differences
`100*(source[+0x10]-source[+0x20])` and
`100*(source[+0x14]-source[+0x24])`. Constructor stores `0x14098303f/0x140983046`
copy the incoming R8 anchor; `0x14098305a/0x140983061` copy the incoming R9 pair.
These four words are distinct from mutable dimension words `+0x18/+0x1c`.
Their later writer/ordinary Grid-shift closure is an active branch; omission
from P1's geography schema did not itself establish their mutability.
SOURCE_ORIGIN_WORDS_UNQUALIFIED is raw observed input, not an origin/frame
certificate. Its READ_FAILED result zeros that group's owned buffer; failure
of either diagnostic group does not discard the other successfully read group
or the protected geometry. No full-source dump or invented source `+0x08`
Grid relation was added.

The full raw constructor descriptor is also copied independently as 44 bytes
from `+0x38` through `+0x63`, with descriptor_bytes, descriptor_complete and
descriptor_status. SOURCE_DESCRIPTOR_UNQUALIFIED preserves padding and the
otherwise unselected words at `+0x44..+0x4b` and `+0x54..+0x5b`; it certifies
no frame. Its failed read does not erase the other successful groups. Source
`+0x64..+0x67` is outside that descriptor and is not copied. Semantic projection
of padding requires the separate native converter contract.

The actual Grid clear `0x1409829b0` and standalone retirement `0x140982b70`
load the **current singleton manager's ProcGen**, erase the matching full source
pointer key under that ProcGen's exclusive lock, release the lock and then free
the source. See [D5AI-OWN-13/14](d5ai-ownership-sources.csv) and
[D5AJ's exact positive ownership proof](d5aj-invalidation-matrix.md).
Consequently an occupied entry under a reader in a different old ProcGen map
does not automatically fence this free. The old source-lifetime warning cannot
be dropped merely because a map traversal is protected. Checked RPM reads remain
fault-safe diagnostics; native source membership remains a separate question.

## Singleton and ProcGen pointer writers examined

The retained original owner census is
`.local-work/d5ai-ownership/owner-census01/native.tsv`, SHA-256
`6cc620abbc789284f60c62e18b6a62a13f61c88e899e14a9bb1ff55722d21914`.
Its exact root-reference inventory contains five singleton WRITE entries.

| Writer | Positive original instruction effect |
| --- | --- |
| `0x140787867` | Constructor publishes its receiver into singleton `0x145fd9c30` before completing field/module initialization. Publication alone does not certify a complete manager. |
| `0x141881f56` | Initialization calls that constructor at `0x141881f51` only after a null-singleton test at `0x141881f3d`; then stores the returned manager into the same singleton. |
| `0x140788e53` | Derived manager destructor clears the singleton after ProcGen destruction/free. |
| `0x14076b4f6` | Shutdown path clears the singleton after invoking the current manager's virtual destructor at `0x14076b4f4`. |
| `0x14078f816` | Base deleting-destructor body writes null to the singleton; this base body alone does not identify an initialized ProcGen lifetime. |

Within the manager method region, constructor `0x140787830` zeroes its
`+0x130` field at `0x1407879eb`, constructs ProcGen through `0x14079d660`,
and forms the field address at `0x1407886f1`. The actual alias store is
`0x140788703`; an old value is destroyed at `0x14078870e` and freed at
`0x140788716`. Constructor cleanup `0x14078f670` and manager destruction
`0x140788d5e` are separate destruction ingresses. A store can precede its
destructor fence, so a snapshot must compare the actual current binding again
after copying rather than assuming the fence precedes every pointer change.

This is positive writer evidence and a promising ordinary-graph binding route,
not yet a completed global alias proof. The candidate composition is: genuine
native foreign reader; unchanged entry/copy/exit destructor epoch and no hazard;
the same current manager/ProcGen binding before and after source reads; then the
ordinary retirement's same-current-map erase must wait behind that reader.
Manager/body/frame and current outpost still need separate proofs. An admitted
destructor between point-consumer entry and the callback must be rejected even
when it completed before the copier sampled its own starting epoch.

## Actual point callers, not an unrelated reader wrapper

The original point reader `0x14079df70` acquires ProcGen `+0x40` shared at
`0x14079df9b`, calls the collection callback at `0x14079dff2` and releases at
`0x14079e027`. [D5V export04](d5ai-ownership-sources.csv), lines 2 through 140,
records six direct caller sites: `0x1405e6aec`, `0x1408691af`,
`0x140c09409`, `0x140c5c655`, `0x140f7c408`, `0x1415a4647`.

The manager methods `0x14079c900` and `0x14079ebe0` really acquire manager
`+0x24` shared, but they are **not those direct point-reader callers**. Their
reader proof cannot be borrowed merely by nearby function address. The original
extractor path loads current manager `+0x130` at `0x140f7c3f4`; the other
candidate path does so at `0x1415a4633`. These positive pointer origins do not
themselves establish an outer manager reader or player-outpost membership.
Fresh exact exports of all six actual caller functions are complete at
`.local-work/d5am/d5ar-identity01/native.tsv`, SHA-256
`4330dc17c29680a610e428bfbaab39f2d5771bc2591076351f2a005db3c53686`.
Their native source/argument edges are:

| Point call | Current ProcGen input and local protection |
| --- | --- |
| `0x1405e6aec` | Loads singleton at `0x1405e6ad6`, then `+0x130` at `0x1405e6ae5`; no manager `+0x24` admission in this function. |
| `0x1408691af` | Loads singleton at `0x140869182`, then `+0x130` at `0x140869189`; no manager reader in this function. |
| `0x140c09409` | Loads singleton at `0x140c093b9`, checks owner/body and passes `+0x130` from `0x140c093e7`; no manager reader. |
| `0x140c5c655` | Loads singleton at `0x140c5c608`, checks owner/body and passes `+0x130` from `0x140c5c633`; no manager reader. |
| `0x140f7c408` | Passes `+0x130` from the manager retained in RDI, loaded at `0x140f7c310`; no manager reader. |
| `0x1415a4647` | Loads singleton at `0x1415a45ce`, then `+0x130` at `0x1415a4633`. Earlier shared admission `0x1415a450b` protects another object at global `0x1461e2318` plus `0x50`, and is released before this point call. It is not an enclosing manager reader. |

These are positive current-singleton origins at each native call, not proof
that a pointer remains the current binding for the whole consumer. The actual
callback method must check its current binding and lifetime interval separately.

## Current outpost and area branch

The established operation path `0x1421b2570` reads state `+0x630`; its zero
branch loads interface `+0x268` at `0x1421b25d1`, invokes resolver
`0x140f3df70` at `0x1421b25d8`, and obtains a descriptor from
`0x140f4a140` at `0x1421b2640`. Fresh original bodies are preserved in
`.local-work/d5am/d5ar-native02/native.tsv`, lines 26082 through 28196, SHA-256
`dcbc1815e61734da4e4749a5cd89812c6c87a92e1bc09865bac3d94ed471c46d`.

The resolver calls interface virtual `+0x08` to get a handle span, resolves
each candidate through the handle service at `0x140f3dff0`, checks its base
type at `0x140f3e022`, and tests the keyed relation via reference `+0x68`
virtual `+0x08` at `0x140f3e054`. It returns the first matching reference,
or null. This is a useful positive operation-context outpost candidate; it is
not a direct `GetWorkshop(player)` call or proof that every matching candidate
has been counted. Duplicate/multiple candidates and lifetime ownership must
be examined before it can certify unique current player membership.
In particular, the resolver's success branch calls `0x140384600` at
`0x140f3e0c2` **before** returning the reference pointer. The fresh original
`0x140384600` body at identity export lines 6760 through 6878 starts with a locked
decrement of reference `+0x08` at `0x14038461c`, with final-release services.
The returned R14 pointer is therefore not, by itself, a locally retained lease.
Native ordinary use may have an enclosing owner, but a console observer cannot
invent that owner from register placement.

An independent point-only capture does not traverse that established operation
path, so an arbitrary point callback cannot inherit its reference or descriptor.
Preview operations use a different path and must remain distinct. A possible
extension, implemented as the isolated operation helper below, observes the actual established operation's existing reference and
area operands at their native call site; invoking the resolver from the console
or forcing the cached area updater is not justified by these observations.
The area callback tests region geometry in a translated indexed frame; that
requires the real descriptor/translation/height/radius, not a hardcoded research
disk or region broadphase alone. [D5V's coordinate contract](d5v-coordinate-contract.md)
preserves those distinctions and the historical/current-frame boundary.

## Executed diagnostic controls and open branches

`identity-controls02/qualification.json` under `.local-work/d5ar/` passes
fifteen owned native C++ checks: exact nine-read layout/token order, explicit
unqualified status, every partial-read position, reader exception, overflow,
invalid address and absent reader. The
[guarded driver](../../../research/resource-retained-population/d5ar_identity_controls.py)
builds with installed MSVC `/W4 /WX`, then checks the exact result and source
hashes. These tests validate the helper; they do not execute source retirement,
manager replacement, outpost resolution or retail code.

The first diagnostic version copied only four bytes of the visited token, after
the parent implementation request specified u32. Original P1/native evidence
shows a u64 token at `+0x68`; this was corrected before final qualification.
The old `identity-controls01` receipt remains a passing test of that incomplete
earlier helper, not acceptance of its token width. Final `identity-controls02`
independently expects all eight original token bytes.

The current `identity-controls03/qualification.json` supersedes those helper
receipts with twenty-two passing `/W4 /WX` controls, including exact thirteen-
read offset order, the high u64 token bytes, each of nine geography failures
preserving healthy origin diagnostics, each of four origin failures preserving
healthy geography, independent exceptions and pre-read invalid-address checks.
`identity-controls04/qualification.json` is the current helper qualification:
twenty-five controls additionally verify all 44 raw bytes, descriptor failure/
exception isolation and the exact fourteen-read order. The earlier 22-control
receipt remains valid for its older helper rather than final source acceptance.

`source-lifetime06.json` passes five **original-instruction** controls using
`0x140982b70`, full chained pointer lookup `0x1403499f0`, exclusive helper
`0x1422cc3d0` and unlock leaf `0x1402c45a0`. In an owned current map, an actual
native exclusive wait blocks source retirement while a foreign reader remains;
the original routine reaches source free only after explicit reader release.
With a reader in a distinct old map and the singleton selecting the new map,
the same original routine reaches free while the old reader word remains 1.
This directly tests the current-map dependency. Three additional populated-map
controls execute native erase `0x140975030`, slot release `0x1407ab6a0`, resource
map clear `0x1407aab10` and collection clear `0x1407ac260`. An external holder
reference preserves nested storage after erase; a remaining collection reference
preserves region/point storage after final holder release; final nested release
records point, region, collection, resource backing, holder and source releases
in native order, with native fields zeroed. Source definition release is a RET
stand-in; heap/sized free loggers retain Python backing rather than freeing it.
Actual Windows wait/wake services execute. No game or source lease is supplied.

The retained first retirement fixture failed before native execution because
the leaf unlock helper has no runtime-function entry. The second failed after
mapping an incomplete pointer-lookup function fragment. The final loader follows
original CHAININFO metadata for every chained function range and uses the
authenticated D5AF 81-byte unlock-leaf range. `source-lifetime01.failure.json`
and `source-lifetime02.failure.json` retain both failures; receipts 03/04 retain
the corrected repeated result. The bounded child timeout is a fixture fault
guard, with exclusive failure-receipt handling, not a healthy-capture limit.

At the earlier operation prototype, `operation-controls02/qualification.json`
passed nineteen owned C++ controls. This prototype is superseded. The
[final lifetime record](d5ar-lifetime-admission.md) and final
[operation.h](../../../runtime/outpost-geometry-snapshot/operation.h) restrict
the copied operands and move selected-reference reads under the native lease.
The exact established call return `0x1421b26c1` gates R14 reference diagnostics,
the supplied indexed descriptor's complete 24 bytes and radius/upper words.
The prototype read previously verified EXP0002 reference fields (`+0x28`,
`+0x2e`, `+0x98`, `+0xb0`). ACTIVE_ESTABLISHED_OPERATION_REFERENCE identified this
actual operation relation, with no unique-player membership or reference lease
claim. Translation observations remain OBSERVED_UNQUALIFIED even when repeated
binding samples match. Controls include a nonzero row at index zero, changed
binding, out-of-range index, failed reads, preview-call refusal and preservation
of caller inputs. The initial compile's unsigned-negation warning remains in
`operation-controls01`; the corrected fixture passes `/W4 /WX`.

`area-native03.json` and its qualification receipt repeat fourteen owned
original-predicate controls through
[d5ar_area_controls.py](../../../research/resource-retained-population/d5ar_area_controls.py).
The pinned D5V method supplies original area/containment/point/edge instructions;
resolver and temporary allocator dependencies are explicitly substituted. All
inherited assertion nodes become ordinary runtime checks before execution.
Controls distinguish supplied translated query contexts, equal-count moved
geometry, empty points, tangency, height and strip interior/edge/vertex cases.
They qualify arithmetic on supplied frozen operands, not a retail outpost or
actual-consumer frame. `area-native01.failure.json` preserves an initially
invalid moved fixture; its points were moved beyond unchanged supplied bounds.
The corrected case moves the complete region consistently. Receipt 02 passes
before the added owned-child timeout failure receipt; receipt 03 passes after it.

## Translation frame investigation and preserved counterexample

The relevant prior [caller ledger](../workshop-caller-semantics/native-ledger.md)
and complete geometry-lifetime [ownership](../spatial-equivalence-feasibility/geometry-lifetime/ownership.md)
and [operand map](../spatial-equivalence-feasibility/geometry-lifetime/operands.md)
were recovered. They materially tighten this implementation: `0x140f4a140`
assigns descriptor index from the **then-current** count `0x1461fae80` for the
matching world, or `ffffffff`. Later consumers compare with the current count.
Count growth can make a previously untranslated descriptor eligible. The actual
area predicate resolves Qb, each strip's Qc, each executed vertex Qv and edge Qe
separately. An entry table sample or a later equal sample cannot certify these
consumed coordinates or exclude table ABA. No frame status is promoted from
the operation helper's table diagnostics.

Fresh readOnly/no-analysis copied-database exports preserve all 2,254 direct
count references and all 1,838 direct pointer references. Their only direct
writes are `0x14387e05a` and `0x14387e053` in cleanup `0x14387e030`, which frees
the table then zeros pointer and count/capacity. No exact-root native LEA was
found. A separate 256-byte neighboring-root inventory exports 260 writer/LEA
function bodies, including the unrelated `0x1461fae78` debug singleton and the
`0x1461fae94` fallback position. These are bounded existing-analysis inventories;
computed or wider-object aliases remain unresolved.

`translation-inventory01.json` pins the complete count/pointer exports, reports
zero initial PE header bytes from PE zero-fill, and finds no full-VA u64 or RVA
u32 address literal targeting any byte of `0x1461fae80..0x1461fae8f`. The
[method](../../../research/resource-retained-population/d5ar_translation_inventory.py)
explicitly records `index_zero_immutable_proven: false`. Initial zero state and
absence of these encodings do not prove runtime count or row-zero immutability.
The initial broad root export `translation-count01` exceeded its function-body
bound; its partial references and failure logs remain local, and are not used
as a complete native-body export. Writer-only and neighboring-root exports
completed their fifteen copied-core pre/post checks.

A0's archived Raw2 header has indexed query index zero and current semantic
descriptor equal to its independently qualified consumed generation descriptor.
It lacks the actual translation count/pointer/selected row and per-use resolved
positions. The equality is a positive diagnostic, not a replacement for this
missing consumer-frame evidence. New actual-consumer interpretation remains a
distinct possible contract from historical construction-frame reconstruction;
neither has been established by the bounded table inventory.

The wider encoded-address alternative was then pursued rather than closing Q2
from this narrow inventory. `translation-literals02.json` scans the entire pinned
PE for full-VA u64 and RVA u32 byte encodings targeting the 8 KiB neighborhood
`[0x1461f9e80,0x1461fbe80)`, preserving surrounding bytes and mapped sections.
It finds no full-VA literal and fifteen raw RVA candidates. Four text candidates
are rejected by exact original boundaries in
`.local-work/d5am/d5ar-near-formations01/native.tsv` (SHA-256
`6e42306ba290cd76af018c70ae93fb3987fbcefa47200d08d4e15da6ca74636a`):
`0x1425fadf9` is a CALL opcode, while the other three occurrences overlap MOV/
LEA instructions at `0x1438a27ab`, `0x1438a27be`, `0x1438a27d9` targeting
unrelated globals. The seven rdata, three bind and one unmapped occurrences
remain byte candidates, not pointer or instruction claims.

`translation-formations01` scans all 14,392,004 existing executable instruction
boundaries in the verified copied analysis state. It records 1,279 LEA reference
rows to that neighborhood before its containing-body phase refuses the existing
500-function bound. Its complete root list is useful diagnostics, but its partial
native export is not presented as a completed function-body export. The corrected
method retains every wider root while selecting bodies only for the nearest
previously unexamined lower bases `[0x1461fad80,0x1461fae00)`; its second export
completes as `translation-formations02`, SHA-256
`b040c7b1efb58ff306c36ce14b5439064b0cfdf451f911df9145650d5ff27c91`,
with all wider roots, six selected bodies and fifteen copied-core hashes
unchanged. No analysis or new boundary creation occurs.

The particularly plausible `0x143a31214 -> 0x1461fadf0` alternative was followed
into original caller `0x142b9d430`. It is a local qword reference plus a separate
initialization guard at `0x1461fadf8`: the branch zeroes only the qword, calls
`0x1428cba80` on its address, and registers `0x143a31210`. That latter function
passes the same address to release helper `0x1428caea0`. This is positive
evidence against treating the nearby LEA as a demonstrated translation-vector
container whose `+0x90` is the header. Other newly examined closest lower roots
are a byte at ada0, a word at adc0, a caller output at add0 and another qword/
guard pair at ade0/ade8. No table store or header receiver is established there.
Further generic-callee alias exclusion remains a distinct proof obligation.

Fresh original-callee export `.local-work/d5am/d5ar-world-frame01/native.tsv`
(SHA-256 `8a54e33aa4e0cf789aeca863f48bfe30936b9187a01eb786fa306e25fcdc815b`)
closes that particular adf0 receiver route more strongly: `0x1428cba80` hashes
a NUL-terminated string into a pool, and writes only the resulting qword to the
original caller receiver at `0x1428cbf8f`; `0x1428caea0` releases the pool entry
and zeros only the receiver qword at `0x1428cb007`. The nearby local is an
interned-string holder, not a demonstrated translation-vector container.

The cleanup's inverse data reference `0x140001210` was also followed. It has no
defined function in the existing analysis state, so the first function exporter
refused it (`d5ar-table-crt01`); no function was created. The guarded existing-
instruction export `table-crt-range01` proves exactly LEA RCX of `0x14387e030`
at `0x140001210`, then JMP `0x14365d408` at `0x140001217`. This registration
thunk does not initialize or modify the table header. A separate earlier attempt
to export text candidates concurrently was refused by the copied project's lock
(`d5ar-literal-text01`); subsequent database reads are serial. Both failures and
their partial logs remain local.

## Positive origin-event and source-local-basis branches

An exact pinned-PE frame/origin registration-name search in `frame-strings02`
finds actual `BSWorldOriginShiftEvent` RTTI. The `BSPosition` matches instead
identify LegacyNif `BSPositionData`; the `OriginOffset` match is a Camera setting.
Neither name was silently promoted into the consumer-frame producer. A bounded
original RTTI layout decoder (`origin-rtti02`) checks COL signature/self RVA,
file-backed type/hierarchy/base-array bounds and member displacements, then
nominates concrete original virtual tables for verification. Existing read-only
analysis references independently locate the corresponding type descriptors.
This supplies a positive new native event branch rather than an absence claim.

The world-origin event source vtable `0x144b35e38` has its original constructor
reference at `0x1406915f1` inside getter `0x140691580`, which initializes the
global at `0x1461e08d0`. Matching sink member displacements nominate navigation
manager `+0x118`/`0x140690030`, audio manager `+0x10`/`0x140f19020`, and player
camera `+0x88`/`0x141e8c6d0`. Actual event sender/receiver bodies and their
relation to the indexed translation header remain under examination. RTTI labels
alone do not establish that the event changes those globals.

The separate source-local-basis branch follows the actual constructor's four
origin words and the provider's consumed origin, then checks ordinary source
writers and Grid shifts. A0's full raw birth record may preserve these words
even though its P1 semantic identity projection excludes them. The parent is
authenticating that original archive join. Any resulting comparison basis must
prove source/holder continuity, later writer exclusion, complete construction
coordinate transformations and the relationship to the geographic descriptor;
it must preserve historical mask/sampler uncertainty. Equal raw words or equal
region bytes alone do not supply that proof.

The full Grid-shift tail reveals a necessary adverse branch that an ordinary
zero-rebase fixture alone would miss. `0x140986da0`'s third argument is an
anchor-rebase pair. If nonzero, it loops the Grid's source array and subtracts
its words from source `+0x10/+0x14` at `0x140987048/0x14098704c`, before source filtering.
This primitive supports source-anchor mutation. Its only defined native code
callers are `0x14078572e/0x140785746` inside `0x1407856b0`; they pass the current
manager's `+0x1ec/+0x1f0` pair. The authenticated owner-census manager-method
graph initializes this triple to zero at `0x140787ab4/0x140787abb` and otherwise copies
the file-backed zero constant `0x144da97a8..0x144da97b3` at
`0x14078c2e8/0x14078c2f6`, `0x14078c438/0x14078c446` and `0x14078c89c/0x14078c8aa`. The nearby
`0x14078b8d7` LEA of RBP+0x1ec is a stack local, not a manager field escape.
Thus the mapped ordinary caller has positive zero-rebase evidence, while
full receiver/alias closure must precede a general origin-immutability claim.
The four origin words are not declared immutable merely by a passing repeated
read. The full population routine `0x1409832e0` reads the selected source in
R14 without directly storing through it; its cells/auxiliary outputs are distinct
objects. Ordinary Grid movement moves/deletes cells and filters sources; the
nonzero rebase branch remains explicitly accounted for.

The native generator supplies a narrower promising comparison basis. Provider
origin is rounded/converted into the Int2 passed at `0x14079ff0f`; constructor
`0x14079b520` retains that pointer at its local traversal context `+0x00`
(`0x14079b86f`). Traversal passes it as generator R8 at `0x14079c4e0`.
The first point uses integer origin plus cell*100 plus local random XY at
`0x14079a7c5..0x14079a848`, with Z explicitly zero at `0x14079a84e`.
Later points use a sin/cos XY direction formed from VEX scalar loads whose
upper lanes are zero; `0x14079a954` adds distance times that zero Z component
to previous Z. For qualified finite inputs this preserves planar Z=0. The
owned XYZ-width vector is copied at `0x14079ab21` and the completed region is
deep-copied at `0x14079aced`, without an intervening terrain-height or descriptor
coordinate conversion in this path. The descriptor-dependent `0x14078d7b0`
call supplies the seed/key, affecting generated shape rather than converting
the stored coordinate axes. Collision-helper callback and remaining source
writer closure remain under examination. This prospective source-local
representation basis does not identify the historical sampled geography/mask,
or qualify the separately indexed current outpost query frame.

| Branch | Disposition / next discriminating action |
| --- | --- |
| Exact scalar layout and lossless diagnostics | Implemented and owned-fixture tested; independent final repetition still required. |
| Current singleton / ProcGen binding | Positive writer graph above; complete alias/caller review and adverse replacement/retirement controls remain open. |
| Historical construction frame | Current manager bytes remain diagnostic. Actual generation-frame equivalence is not recovered merely from present map residence or equal geometry. |
| Current established outpost | Actual established-operation callsite/operand helper and nineteen owned controls implemented. Resolver returns a released reference; unique current-player membership and independent reference lifetime remain unqualified. |
| Area membership and missing/nonresident sources | Preserve resident census and UNKNOWN association until all native frame/area premises qualify. Empty callback silence proves no geographical absence. |

No terminal barrier or impossibility conclusion is claimed. These are material
authorized offline leads within the original Q2, not optional future work.


## Selected-reference lease follow-through

The original handle registry `0x1428ccc40` admits a shared slot, checks handle
index/generation and invokes callback vtable `0x144af3d50 +0x10`. Pinned original
PE data resolves that slot to `0x1402b7070`. Fresh read-only/no-analysis export
`.local-work/d5ar/selected-lease-callback01/native.tsv` retains its complete body:
`0x1402b7074` compares native handle generation, `0x1402b707f` rejects zero low
reference count, `0x1402b7098` atomically adds `0x80000200001` to reference `+0x08`,
and `0x1402b70a1` publishes the resolved slot. An existing slot is balanced by
original release `0x140384600`. Thus the successful resolver's local reference
is actually held until its success release CALL at `0x140f3e0c2`; copying immutable
FormID `+0x28` and type `+0x2e` immediately before that call needs no added native
reference, query or ownership mutation.

Six owned native controls execute unchanged callback and full release bytes
(`d5ar_selection_native_controls.py`, local `selection-native02.json`). They
exercise exact acquisition/release balance, stale-handle generation refusal,
zero-low-reference-count refusal, same-slot idempotence, replacement-slot release
and an equal-pointer/equal-FormID recycling counterexample. Initial low count2
keeps final-free/virtual-destruction branches outside this fixture. This is not
full resolver enumeration or proof of a later lease. The initial fixture01
string-escaping failure remains local with its failure receipt.

The proposed integrated method scopes TLS around complete established operation
`0x1421b2570`, with finally cleanup, nesting refusal and the current arm-generation
and invocation tokens. A pre-release CALL relay observes the original return
`0x140f3e0c7`. At that exact original release entry, resolver's six pushes and
`SUB RSP,0x58` place its caller return at `RSP+0x90`; it must equal established
resolver return `0x1421b25dd`. Later area return `0x1421b26c1` and R14 operand
must match the same active invocation and captured pointer. The helper deliberately
calls the result `SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME`. It never claims
allocation continuity after release, unique current-player ownership, every
matching workshop, or an independently qualified physical query frame.

The isolated `selection.h` helper and 21 owned controls test both partial reads,
exceptions, absent/early/ended scopes, unarmed scope, nested/multiple candidates,
exact native call gates, epoch/invocation/command/operand mismatch and recycling
limits. Whole-operation native integration and exception/finally cleanup require
separate actual DLL controls. The original operation has seven pushes plus
`SUB RSP,0x140` (total `0x178`), RBP=entryRSP-`0x78`, no incoming fifth stack or
SSE argument use, and no R11 operand. Its first five bytes include MOV RAX,RSP
and two pushes; trampoline unwind must describe that exact shape.

Independent `d5ar_r11_liveness.py` checks nine existing hook entries. Seven complete
native bodies contain no R11 operands. The whole area defines it in its epilogue;
the callback's 579-instruction direct CFG proves `0x1421e13a0` dominates both R11D
comparisons and `0x1421e18f7` dominates all epilogue reads. No indirect/escaping
callback branch is assumed away. This supports the revised trampoline continuation
needed by actual OS unwind controls; it does not substitute for those controls.

Q2 remains visible: the selected native operation can identify the reference
at actual resolution time with explicit lease-time scope. Its later raw pointer
is not a continuously held allocation. Physical area membership, missing or
nonresident sources and global unique player ownership remain UNKNOWN. The
resident census and source-planar representation comparison are independent of
those unqualified physical-area claims. Review must decide original contract
coverage using these actual scoped outputs, not synthetic contexts alone.


## Actual growth, collision relocation and reused-key controls

`d5ar_rehash_controls.py` supplies the previously missing executed growth case.
Local `rehash-native04.json` passes five scoped controls against unchanged original
outer rehash `0x1407abaf0`, resource rehash `0x1407abc90`, collision helpers
`0x1407ab510`/`0x1407ab730`, erase `0x140975030`, reservation `0x1407aa5f0`,
exclusive admission `0x1422cc3d0` and unlock `0x1402c45a0`. It uses original
pointer hash code/constants and verifies actual native collision metadata, not
only successful relocation. Both capacities grow from 4 to 8; all keys/pointee
identities, holder/resource/collection/region/point bytes and reference counts
survive; physical slots move and the old slot allocation is released through an
explicit heap-free logger. No Python backing allocation is actually freed.

A foreign thread executes the original exclusive-admission/rehash/unlock sequence.
Actual `WaitOnAddress` is observed while the owned native reader count is 1; the
map remains unchanged until that reader exits, then rehash completes and lock
words return to zero. The enclosing caller sequence and pre-existing reader count
are fixture inputs; this is not execution of a full game consumer or scheduler.

The same fixture then executes native erase, verifies the previous holder's
reference decremented while externally retained, reserves the same source-pointer
key through original `0x1407aa5f0`, and publishes a distinct holder using the exact
unchanged original stores from `0x14079fe14`/`0x14079fe18` in a register-adapting
owned micro-harness. Source bytes are deliberately overwritten in owned memory;
no original source constructor, allocation/free or historical birth certificate is
claimed. A subsequent equal-key/equal-holder overwrite counterexample separately
shows why successful rehash/lookup cannot supply allocation birth identity.
The protected invocation-local current-map theorem does not require a historical
source-allocation certificate after its owned bytes have been copied.

Heap allocation returns owned retained buffers, heap free records pointers, and
owned heap-initialization state is set 2. Original map/hash/lock instructions remain
unchanged. The initial01 Python-generated-byte-literal failure is preserved;
Versions 02 and 03 passed progressively stronger fixtures before the final native erase/
reservation/publication case. No game, save, configuration, installed plugin or
analysis database was mutated. Final receipt SHA-256: `afac12a08048fbeadf24d9fe3b201730ed1bd94d70138af277665da6514fee22`.

Incoming-register closure now also includes the whole established-operation
entry: `r11-liveness03.json` passes ten original entry targets. The final plugin
may remove point entry/callback hooks, but this larger explicit coverage remains
valid evidence for every retained entry detour; a release CALL relay uses no
clobbering original-prologue trampoline.


## Ordinary established-operation trigger scope

Removing the generic point detours narrows the final command to the established
operation's exact `+0x630==0` branch and area caller `0x1421b26c1`. Fresh preserved
read-only caller export `.local-work/d5ar/operation-transition01/native.tsv`
(SHA-256 `34aa38ce46f5b9824e2a84de0e76113c04a56451c9bf0099bd6dcb7efe8de3f9`)
confirms `0x1421be130` selects singleton `0x14597a9c8`, writes operation-state
`+0x210` and dispatches its entry. It is reached at `0x1421b30a6` from a
state/selection branch, at `0x1421b5072` after a displacement/threshold branch,
and by tail jump `0x1421b2357` from an event method. These are positive ordinary
transition paths, not a claim that every frame or every open repeats entry.

Pinned original RTTI identifies operation vtable `0x144d49c80` through COL
`0x1452b3028` as `WorkshopEngine::StateUpdatePlacement`. The long table whose COL
pointer is at `0x144d49030` (COL `0x1452b3050`) identifies
`WorkshopEngine::StateSetupReferences`; its method `0x1421b5e70` completes setup
by selecting the placement singleton except when context `+0x630==6`, where it
selects the other state `0x14597a9f0`. The event method `0x1421b22e0` belongs to
`StateUpdateAutoFoundation` (COL pointer `0x144d4b020`, COL `0x1452b3500`). Names
support the typed graph; they do not prove UI-open timing or player ownership.

Earlier native-availability evidence observed one established initialization and
35,573 preview calls. The preserved event-oracle ledger explicitly lacks the
runtime transition sequence and rejects selection-as-every-build-open. No exact
BuildMode-closed predicate is established in the bounded bodies above. Therefore
the supported card instruction is to arm before the ordinary established-outpost
placement setup/initialization and require the actual zero-state operation and
protected area reader to occur. If they do not occur, the command remains armed
or yields NOT_OBSERVED under its explicit cancellation/exit policy; it must not
force a native query or silently classify absence as an empty population. A
universal deterministic every-open trigger remains unproven, separate from the
instrument's exact native admission and owned-control qualification.


## Mandatory non-mask input follow-through

[The effective-input gate](d5ar-effective-input-gate.md) records the strongest
current scoped results. Authenticated Birth sequence 2082 gives native origin
`[-200,-200]`; all three original constructor caller families now reconstruct
final dimensions `[10,10]` from the captured definition/padding operands. Pinned
stitching initialization/config evidence, the ordinary GMST DATA/reset/reload
closure and the complete 339-record Feynman resource dependency audit materially
advance reconstruction. Conditional native-backed component controls reproduce
the C1 candidates and DNAM supplier; no shape-equality metadata assignment is
used. Actual historical atmosphere/reflection, ordinary initialized-component
and per-use setting/descriptor premises still require their own closure.

[Source-ending history](d5ar-source-ending-proof.md) separately addresses the
late raw-source selection/publication interval. Current-map admission alone is
insufficient. Final source diagnostics need the reviewed pre-owner installation,
complete source-ending CALL coverage, permanent tombstones and shared copy gate,
as well as actual manager/body and geometry-reader premises. The final native
source lock and independent controls must admit that method before a qualified
profile is registered. The narrower source-planar theorem does not itself close
Q3 / AC05 or qualify a future 30-episode causal study from matching content.


### Current effective-input follow-through

The [effective-input investigation](d5ar-effective-input-gate.md) now recovers
final dimensions `[10,10]` from actual A0 retained definition dimensions and
padding through all three ordinary constructor caller families; closes all 339
relevant main definitions against the exact 39-file A0 roster; finds no stitching
keys in the 23 pinned config files; and proves ordinary GMST reset is followed
by definition reload on all examined normal return paths. These replace generic
"not recorded" objections with concrete conditional native reconstruction.

The atmospheric branch now resolves the normal pinned C19B definition route.
Original parent postlink/copy precedes the child DIFF; native reflected names
and field indices bind the zero-count LIST to `Settings.Misc.InorganicResources`.
Three owned original array controls corroborate its clear. A separate sensitivity
control covering every byte alignment of literal IRES candidates finds only
Water; both empty and Water cases yield identical three-biome projections and
ordinary candidate order. That diagnostic domain is not generalized to arbitrary
reference/default paths. The examined Save52 type-3 tail is positively a
different GameDaysPassed component. The PerBiomeData copy factory does preserve
resource slots, so initial population cannot silently stand in for loaded
component state. The [saved-component challenge](d5ar-saved-components-proof.md)
now identifies the actual unit 6 erased-ID/NameComponent and distinct typed
restore paths and PNDT generic flags. These are positive scoped exclusions of
slot-image restoration; historical selected biome/context and per-use inputs
remain separate. No geometry equality, external exporter heuristic or invented
Papyrus GMST setter supplies those operands.
