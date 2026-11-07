# Logistics claim and evidence crosswalk

[Brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BB_Logistics_and_Storage_Guides_and_References.md) · [Verification and handoff](README.md)

STATIC refers to the pinned installed retail 1.16.244.0 executable and main ESM,
with the installed scripts for C2/C3 and the add-on for SD2 where identified by
the linked reports. SAVE refers to the named historical sample and reader
grammar. Derived examples calculate from explicit operands. D5BB adds no
RUNTIME capture. Original runtime behavior and currently effective operands
remain unmeasured where the sources say so.

| ID and scoped claim | Basis and primary locator | Review and challenge | Access tier |
| --- | --- | --- | --- |
| Q1a. Ordinary stores filter item categories on mapped routes and use effective weight. 75/150/300, 200 and 300 are base definition values for their respective qualified stores. | STATIC [catalogue](../../experiments/storage/catalogue.csv), [capacity and gates](../../experiments/storage/native.md#owner-weight-and-capacity), [capacity examples](../../experiments/storage/capacity-examples.csv) | [S1](../../experiments/storage/review.md) and [capacity follow-up](../../experiments/storage/capacity-review.md). Effective overrides and native chest prohibitions defeat a UI-only classification. | Tracked inspection and selected arithmetic. Exact native validation depends on pinned lawful inputs and the qualified method. |
| Q1b. Stacks and links have separate owners/channels. Ordinary cargo compartments are separate references. | STATIC + SAVE [storage joins](../../experiments/storage/saves.md#object-level-evidence), [link joins](../../experiments/local-output-links/saves.md) | [S1](../../experiments/storage/review.md), [S2](../../experiments/local-output-links/review.md). Omitted or unsupported inventory branches cannot establish empty stock. | Tracked inspection. Historical originals need approved access. |
| Q1c. Redistribution traverses forward, can bypass intermediates and split a source row. Production can request a whole batch into one receiver. | STATIC + derived [movement](../../experiments/local-output-links/native.md#existing-stock-planning-and-mutation), [worked traces](../../experiments/local-output-links/traces.md) | [S2 correction](../../experiments/local-output-links/review.md#retained-failures-and-corrections). The multi-item exclusion test defeats an aggregate reservation guarantee. | Tracked inspection and operand recomputation. |
| Q1d. Producer work can run for a registered, resolvable outpost without graphics. Missing references, ineligibility and elapsed-update handling are different branches. | STATIC + SAVE [lifecycle](../../experiments/local-output-links/lifecycle.md#state-by-state-result), [producer/link joins](../../experiments/local-output-links/saves.md) | [S2](../../experiments/local-output-links/review.md). Unresolved producer sentinel and Workshop failure defeat general catch-up. | Tracked inspection. Original exports and historical saves are local or provisionally selected. |
| Q2a. Reciprocal markers and one ship enable alternating unload/load legs. Refused stock remains aboard and can return to the origin's incoming child. | STATIC + SAVE + derived [configuration](../../experiments/cargo-links/configuration-ui/native.md#terminal-eligibility-and-pairing), [cycle](../../experiments/cargo-links/transport/cycle.md#roles-and-authoritative-transitions), [transfer](../../experiments/cargo-links/transport/inventory.md#returned-cargo-discrimination), [Save52 joins](../../experiments/cargo-links/transport/saves.md) | [C1](../../experiments/cargo-links/configuration-ui/review.md), [C2](../../experiments/cargo-links/transport/review.md). Full destination/empty outgoing do not bar departure, and a static origin-incoming stack cannot identify a historical return. | Tracked inspection and model recomputation. Save52 is a provisional F1 input. |
| Q2b. Dock deadlines, VM dispatch and native travel have separate clocks. Clearing can recover held items to home ship then player. | STATIC [timing](../../experiments/cargo-links/transport/timing.md#script-authority-and-native-deadline), [lifecycle](../../experiments/cargo-links/transport/lifecycle.md#distinct-operating-and-failure-states), [transit follow-up](../../experiments/cargo-links/transport/transit.md#answer-and-claim-scope) | [C2](../../experiments/cargo-links/transport/review.md), [transit continuation ACCEPT](../../experiments/cargo-links/transport/transit-review.md#mandatory-criterion-ledger). Wait/sleep suppresses delivery during the mapped gate and supplies no replay guarantee. | Tracked inspection/recomputation. Exact primary EXE/PEX/definition inspection is conditional on lawful pinned inputs and qualified method. |
| Q2c. Inter-system fuel is an upstream recipe of five He-3 per accepted producer cycle at 108 base scheduler seconds. Either eligible non-mission endpoint can admit the next leg. | STATIC + SAVE [definitions and chain](../../experiments/cargo-links/fuel/native.md), [stages](../../experiments/cargo-links/fuel/stages.md), [Save52 fuel sources](../../experiments/cargo-links/fuel/saves.md) | [C3 receipt-controlled](../../experiments/cargo-links/fuel/review.md). Charged mode 0 can pass despite fewer than five accessible units. A query can also pass before any withdrawal. | Tracked inspection and arithmetic. Historical charge/stock joins require original access. |
| Q3a. The recognized add-on fixture exposes a player-held inventory. The player serializer owns the inventory channel, while fixture records can show ownership without stock. | STATIC + SAVE [recognition/residence](../../experiments/shared-outpost-storage/shared-inventory.md#recognition-and-residence), [construction](../../experiments/shared-outpost-storage/prerequisites.md), [historical saves](../../experiments/shared-outpost-storage/saves.md) | [SD2 ACCEPT](../../experiments/shared-outpost-storage/review.md). Exact saved backing quantities remain unparsed despite positive fixture/owner joins. | Tracked inspection and census recomputation. Fixture witness access is provisional or local. |
| Q3b. Counting uses a temporary copy. Actual spending follows an eligible source vector and separate removal calls. | STATIC [entry points](../../experiments/shared-outpost-storage/consumers.md#entry-points-and-actual-source-lists), [depletion](../../experiments/shared-outpost-storage/consumers.md#counts-ingredient-plans-and-actual-depletion) | [SD2 ACCEPT](../../experiments/shared-outpost-storage/review.md). Outgoing cargo can fail the build-container gate while a link-prohibited chest passes. | Tracked inspection. Exact primary native comparison is conditional on lawful pinned inputs and qualified method. |
| Q4a. The Locations entry uses registered Workshop members with effective container/build gates and shared-reference substitution. It emits per-outpost arrays. | STATIC [provider](../../experiments/stored-resources/provider.md#source-inventories-to-selected-row), [membership](../../experiments/stored-resources/membership.md), [freshness](../../experiments/stored-resources/aggregation.md#three-separate-freshness-boundaries) | [SD3 review02 ACCEPT](../../experiments/stored-resources/review.md). A UI repaint cannot establish a new inventory collection. | Tracked inspection. Exact native/UI verification depends on pinned lawful inputs and qualified method. |
| Q4b. Qualified item instances group by associated IRES and contribute stack units. HIST-0036 gives conditional mixed-source examples. | STATIC + SAVE + derived [aggregation](../../experiments/stored-resources/aggregation.md#item-admission-and-grouping), [icon joins](../../experiments/stored-resources/icons.md#exact-installed-joins), [HIST-0036](../../experiments/stored-resources/saves.md#positive-mature-mixed-source-witness) | [SD3 review01 correction and review02 ACCEPT](../../experiments/stored-resources/review.md). Default-entry zero preparation differs from exceptional stack counts. Screenshots lack an epoch join. | Tracked inspection and arithmetic. HIST-0036 is provisional, with no approved witness URL. |

## Evidence access and review status

**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING** for independent inspection
of indispensable original witnesses behind the selected historical claims.
The HIST-0036 stock, membership and aggregation joins (F1 candidate
B4-F064) and C2/C3 Save52 endpoint, hold and producer joins (B4-F040)
need their exact approved original or a
sufficient cleared derivative, with a qualified reader. H18/H257 fixture
joins and the full SD2 corpus need separate witness coverage if retained at
the original-verification tier. The tracked summaries and row counts remain
inspectable and their bounded arithmetic can be recomputed. The
[F1 candidate members](../publication-readiness-b4/f1/members.csv) and
[D5AX access assessment](../publication-architecture-d5ax/evidence-access.md#f1-continuity)
describe provisional selections. No current download is promised.

Exact primary native/script verification needs the installed executable,
definitions, shipped PEX or UI assets named by each source ledger, plus a
qualified selected method. No raw exports or decompilation artifacts are
included here. The original S1 and corrected S2 local ACCEPT receipts
were readable at the paths named by their tracked reviews. The C3
final review, seal and package are indexed as retired members of the
active LOCAL-ONLY Cargo archive. The index and retirement allowlist
match the tracked hashes. D5BB inspected that metadata only, so the
historical C3 final verdict stays receipt-controlled and unverified here.
C2 and its transit continuation retain their separate accepted reviews.
[Active archive baseline](../../experiments/cargo-evidence-cutover/active-baseline.json) · [Retirement record](../../experiments/cargo-evidence-cutover/execution.md) · [Original evidence tiers](../publication-architecture-d5ax/evidence-access.md).
