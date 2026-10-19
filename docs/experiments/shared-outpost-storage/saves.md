# Historical correspondence and its exact boundary

[Answer](report.md), [native model](shared-inventory.md), [coverage register](corpus.csv),
[source hashes](sources.csv), [methods](methods.md). Raw saves, decoded bytes,
reference queues and bulk receipts remain LOCAL-ONLY. Offsets here are decimal
**decoded logical-stream offsets**, not compressed-file offsets or native VAs.

## Broad search

The frozen 278-entry canonical historical inventory supplied the locator set.
All 255 still-accessible originals matched their recorded SHA-256 before strict
decoding and matched again afterward. Twenty-three canonical paths were missing;
they were not replaced with similarly named files. Reader-supported results:
**147**; unsupported header/build contexts: **108**. Every label and its outcome
is in corpus.csv; per-save receipts retain source and decoded hashes, exact
record/prefix/extra positions, plugin mapping and errors.

The supported inline-base search finds **1,499** records with canonical base
`sfbgs00d.esm:02af77`, in **124** saves. These are repeated historical snapshots,
not 1,499 independent constructions or experiments. Plugin-aware identity
resolution is essential: the raw file-encoded add-on index is not a saved index.
The detector uses typed REFR records and a positively decoded initial base.
It does not cover every default, replaced/inherited or unparsed representation.
Unsupported prefix counts remain in receipts; zero candidates is a bounded
detector result, never proof that a universe contains no shared inventory.

All 1,499 have **NO_INVENTORY_CHANGE_BRANCH** under the ordinary reference
inventory-change mask. This does not mean zero items. It is the expected
counterexample to treating each visible shared fixture as its own saved stock:
the separate native player writer persists the backing inventory. No inference
that a fixture was empty, accessible or successfully used follows.

## Fresh representative joins beyond Save52

joins01.json freshly re-decodes three originals, closes typed record iteration,
resolves each candidate's WorkshopItem edge, and physically identifies every
selected target as the ordinary beacon base `Starfield.esm:2c60e9`.

| Canonical original / SHA-256 | Shared fixtures and owners | Exact positive example |
|---|---|---|
| HIST-0018 / `aff01925cafa2473765512df0ea48dc1f41137ff523668a102406c750f5b011f` | 1 fixture, 1 distinct beacon owner; saved disabled/deleted flags clear | `DYNAMIC:ff0253b5`, record 1644111 -> special base; Extra4C at 1644255 contains `054ba6 -> ff02532b`; owner independently resolves to beacon |
| HIST-0036 / `7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37` | 17 fixtures, 17 distinct beacon owners; all selected flags clear | First fixture `ff01a5a0`, record 3051921; all 17 owner records physically joined in joins01 |
| HIST-0257 / `0435cade6ce089cc029804ae8f77f07cd79ca882886099036351015a03b68004` | 19 fixtures, 19 distinct beacon owners; all selected flags clear | First fixture `ff02404b`, record 7662412; 19 beacon joins rather than proximity/name inference |

HIST-0018 also has HandScannerTarget `22a2b6 = 1` in ExtraBF; that is **not**
OutpostBuildContainer `00f65a`. Its physical fixture has separate ownership
Extra1F referring to player reference `000014`, and a distinct `1c5edd` keyed
relationship. Neither is interchangeable with the WorkshopItem owner. The
re-read original flags are historical state, not current Health, registration
or post-load authority. The three saves are observational examples without an
assumed common chronology, action/control pairing or controlled craft.

## Residence, reconstruction and unresolved saved amounts

The strongest identified mechanism is the **native** player-held global backing
inventory: fixture recognition -> player+1008 substitution -> ordinary inventory
mutation -> player writer's second internal inventory list -> version-gated
loader into the reconstructed backing reference. See exact writer/load windows
in shared-inventory.md. No saved pointer or fixture FormID is needed to maintain
an item once stored in that player-owned list.

The positive saved chain established here is **special base -> actual fixture ->
Workshop edge -> independently identified beacon**, with native correspondence
for the shared-access and writer/loader links. A fully framed field-specific
decode of player+1008's inventory segment is **not yet established**. Consequently
no particular saved backing-item identity/quantity, total stock, empty backing
list or post-load value is claimed. This is a decoder coverage gap, not absent
fixture evidence or evidence of lost contents.

joins01 retains the player actor's complete raw body and resolved queue for each
selected original. A diagnostic scan for complete positive empty-stack-extra
inventory subgrammars returned zero candidates (player-candidates01/02.json).
The first version incorrectly required the trailing byte to be zero; SD1's
positive ammo-box row has byte 254, so the corrected diagnostic removed that
constraint. It still returned zero. Neither scan supplies a field anchor or
handles arbitrary stack extras; both are retained as failed acquisition routes,
not absence tests. A future parser must anchor the PlayerCharacter extension
and its preceding fields rather than promote a plausible byte match.

No source save was loaded or resaved, no controlled craft was performed, and
no remote inventory delta or settled reload was measured. The native mechanism
does not require those observations to distinguish a single backing inventory
from synchronization of many per-fixture stores; exact historical backing
contents and realized consumption remain separate open questions.

## Smallest proposed discriminating live acquisition

Only under a separate approved card: protect/hash an original and controlled
copies; use two existing outposts with recognized fixtures and a bench, and
record player/ship/local ordinary/incoming/outgoing/shared stocks independently.
Deposit a distinctive counted resource stack through fixture A, inspect B, then
craft one known-cost item using a deliberately split-source requirement. Record
before/after exact inventories and selected-source order. Save/reload the
controlled copy, repeat the inspection, and separately test a bench with no
eligible local shared fixture. A last-fixture scrap is an additional separately
specified action if conservation/access recovery is the question.

This would test remote **access**, actual **depletion**, source priority and
loaded reconstruction; it must not assume item transport. Include power/loaded
state and selected ship, finite actions, input protection, failure/stop/cleanup
and evidence flushing in the future card. No observer, live run, deployment,
save write or gameplay action is authorized or executed by SD2.
