# SOR-EXP-0002 — Outpost membership, reload and location

**2026-10-06, Australia/Sydney. Gate A: OFFLINE IMPLEMENTATION/BUILD PREPARED FOR REVIEW; live qualification unperformed. Critical review required.**

Authority: user explicitly invoked the [brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_SOR-EXP-0002_outpost_membership_reload_location.md`); SOR-D-0010. Publication: authored notes/code REVIEW-REQUIRED; saves, local paths, binary/source exports, synthetic outputs and profile data LOCAL-ONLY. An installable observer and executable diagnostic are built locally, not deployed or live-qualified. SOR-D-0011 / SOR-P-0001 record continued authority and exact header approval. This report does not authorize Gate B.

## Question

What does GetWorkshop return for the beacon and one ordinary storage reference, and how do distinct identities, membership and spatial values compare across A2 reload? SOR-H-0001 remains provisional. Persistent membership, reconstructed membership, an intermediate owner and cached/location-derived membership remain competing explanations. No semantic save analysis is in this preparation.

## Baseline

SOR-ENV-0002 rechecks SOR-ENV-0001: both installed/pinned game and CK, installed SFSE loader/DLL and development archive match the earlier sizes/hashes. Game/CK 1.16.244.0; preferred PE base 0x140000000 is not an ASLR base. Python 3.14.3 executed only original offline helpers. Existing Ghidra reader executed with read-only/no-analysis flags; no new analysis, renaming or type edits. Evidence and final preservation checks: [SOR-EV-0002](evidence/exp0002-preparation/README.md).

Runtime module/plugin profile is UNKNOWN. Prior static inventory is not a runtime profile or proof of an unmodded game. The expected resource budget and disabled autosave settings in the supplied brief remain USER-REPORTED; no settings were changed. Original untracked brief was retained unchanged and contains private paths/filename: it requires separate redaction/publication review before any disclosure.

## Protected parent sample

SOR-SAMPLE-0001 is the immutable pre-outpost parent identified as Save3 by the user. Original and backup are 2,096,496 bytes; SHA-256 `d06123ee32bd5b3e244650852fac9714697a19fd6243384966414d1d1f4ffbfe`. Direct streaming comparison confirmed equality. Local integrity manifests record both exact paths, filename and timestamps; these differ in last-write time, not bytes. Parent and backup were only hashed/byte-compared, never semantically parsed, loaded, copied anew or modified.

Kreet, no outpost, buildable-site position and sufficient materials are USER-REPORTED until live confirmation. Save's originating game version, runtime profile and format are UNKNOWN; matching the installed build does not establish the save's creation build. Raw sample is LOCAL-ONLY.

## Checkpoint/sample plan

Logical aliases below follow the explicit brief; only SOR-SAMPLE-0001 currently exists as a registered sample. Planned checkpoint aliases are not allocated evidence of existing saves. Canonical actual-sample records may be assigned sequential numeric IDs when created while retaining these aliases.

| Checkpoint / planned alias suffix | Parent checkpoint | Required action | Planned artifact |
|---|---|---|---|
| A0 | SOR-SAMPLE-0001 | Load parent, build nothing, settle | Ordinary new manual/menu save |
| A0C | A0 | Matched no-action interval, build nothing | Ordinary new manual/menu save |
| A1 | A0C | Place exactly one beacon, settle, capture | Ordinary new manual/menu save |
| A1C | A1 | Matched no-action interval, capture | Ordinary new manual/menu save |
| A2 | A1C | Place one ordinary small solid storage, settle, capture | Ordinary new manual/menu save |
| A2R | A2 | Reload A2 normally, settle, repeat capture; rebuild nothing | Runtime checkpoint ONLY; no new save by default |

Aliases are `SOR-SAMPLE-EXP0002-<checkpoint>`. A2R's alias is a logical runtime checkpoint, not a claim that a seventh save exists. If a post-reload save is later agreed, explicitly register it with A2 parent and its actual filename. A3/A4, extractor, solar array, output links, crew, cargo and other objects remain deferred.

## Observer design

Implemented original [SFSE observer, build/request helpers, validator and bounded debugger](../../runtime/exp0002/README.md), using only the explicitly approved MIT SFSE interface header. SFSE runtime stays external; no CommonLib/Address Library linkage or sibling observer adaptation. [Static contract](../../runtime/exp0002/STATIC-CONTRACT.md) traces independent operand checks and credits source-informed leads.

One explicit SFSE main-thread task reacquires candidates from the player's stored exterior cell and its worldspace's persistent-cell candidate: at most 4096 entries each, exact role counts for query selection; ambiguity/count mismatch yields bounded anomaly evidence without target calls, no checkpoint pointer reuse. Beacon stored base 002C60E9; storage 0023AED9 / recipe 00299547. This is not exhaustive membership enumeration. No placement-event subscription. Repeated byte views do not retain engine ownership or make the snapshot atomic.

Load guards require exact game/SFSE DLL hashes/version and 18 loaded native code hashes. Output is confined to the ignored experiment root. Control-file polling never polls world state. Main-thread callbacks use independently inspected R8 operands; query/cache effects are interventions. Actual lifetime/ABI/query safety remain live assumptions. Session duration, fixed outputs and cooperative budgets are detailed in the native README; synchronous engine calls cannot be forcibly cancelled safely.

Historical correction: initial handoff prematurely stopped at missing ABI/dependency information. User requested continuing; independent static inspection, exact header approval and original implementation closed the offline package gap. The initial report is retained locally as pre-continuation-report.md and its audit is explicitly historical.

## Identity fields

Native schema `SOR-EXP-0002-native-v1` records UTC, declared timezone, game/hash, module base, observer/profile hashes, thread/load generation, elapsed real time, unavailable game time and non-atomic snapshot status. Role identities distinguish pointer, FormID, stored base, candidate native identifier (not a validated handle), extras, stored cell and separately queried location/worldspace. Raw reference XYZ/rotation are retained; loaded-3D, resolved handles and derived coordinate domains are unavailable. Failed reads differ from null queries.

[Native validation](../../runtime/exp0002/validate.py) checks structure/correlation, not engine truth. Its schema differs from the earlier capture_contract.py design. Production serialization is exercised with synthetic memory. CHECKPOINT_COMPLETE is acquisition completion, not scientific success or persistence proof.

## Workshop query plan

A0/A0C verify no selected candidates and capture player/context only. A1/A1C query beacon once; A2/A2R query beacon then storage once each. Per role: GetWorkshop, GetCurrentLocation, GetWorldSpace, with ordered/time-stamped pre/post flushed records and read-validated result identity or explicit null. No owner/resource-subset calls, general world dump or background game polling. Successfully observed load/identity changes, scope/count mismatch and cooperative time limits abort only that attempt and persist anomaly evidence; actual unsafe reads, failed persistence, invalid requests/permissions, wrong build/site and low/unknown disk space remain terminal. An anomalous checkpoint is consumed, not retried; the next explicit request requires acknowledgment of prior anomalies. Added native calls may affect caches/scheduling.

## Coordinate-domain plan

Required static work was performed, bounded to position/location interfaces and lat/long leads. Sources: Bethesda inputs SOR-S-0104; Ghidra interpretation SOR-S-0105. SOR-F-0005 retains coordinate-name evidence; SOR-F-0006 adds prepared raw operand capture without live validation.

| Domain | Static evidence / preparation | Future capture and limitation |
|---|---|---|
| Reference XYZ / rotation | ObjectReference.psc: 523/526/529 and 372/375/378 | Record raw query triplets, API names, units/frame UNKNOWN until qualified |
| Location, cell, worldspace | ObjectReference.psc: 405/517/640; Is3DLoaded: 705 | Identity/context fields separately; do not infer equivalent coordinate frames |
| Cell-local / worldspace XYZ | No conversion demonstrated | UNAVAILABLE; do not relabel reference XYZ |
| Body-relative XYZ / surface-map | No selected-reference conversion established | UNAVAILABLE; no speculative spherical transform |
| Latitude/longitude | CK labels and game name-binding sites found | Candidate only; object type, units, handedness, range, body and outpost association UNKNOWN |

Game static strings latitude at 0x144c92618 and longitude at 0x144c92948 have xrefs in 0x14167f7e0 and 0x14341c0a0. At 0x14167f82f/843, addresses of object-relative +0x68/+0x88 are passed with those names to an indirect call. This is **not** proof of two raw floats at those offsets; the surrounding named properties support a UI/property-binding interpretation. Decompiler labels include markerHandleBits and hasOutpost, but their semantics and object link remain unvalidated. No traversal into planetary generation was undertaken.

CK labels `Location: Longitude` / `Location: Latitude` at 0x148aa1b60/178 reference function 0x142b96190; spinbox names at 0x148b7d268/298 reference 0x1432018b0. This corroborates label presence behind the user's recollection, not an operational CK UI workflow or retail runtime field. CK addresses never transfer to the game.

Broad binary scan capped at 80 matches per encoding; focused scan excludes noisy worldspace/biome terms and retains explicit cap status. No absence claim from search failure. Six installed source entries were searched by exact archive path. At A1/A2/A2R, compare beacon and storage positions in the same confirmed frame; only then calculate storage-minus-beacon displacement. Stable values across reload can be reconstructed/derived, not necessarily PERSISTED.

## No-action controls

A0/A0C and A1/A1C mandatory. Proposed matched settling rule: observer ready, player stationary, build menu closed, no console, no combat/dialogue/loading transition; wait 5 real seconds with no deliberate game waiting/sleep/travel. Start each interval after returning to normal view. Record real elapsed time, game time when available, UI activity, unavoidable movement and any save-related elapsed time. Identical query order at matched control checkpoints; before the outpost exists record session/player only. Controls characterize background variation, not bitwise determinism. Five seconds is a procedural control, not proof the engine has settled.

## Debugger fallback plan

Prepared original [trace.cpp / trace.py](../../runtime/exp0002/README.md) and [declarative review plan](../../research/exp0002/debugger-plan.json). Separate optional authority only after A2R. Callback RVA 0x02073cf0, tail 0x00517d60, key global 0x05f0b3d8. Resolve ASLR from module snapshot, verify executable/loaded code, select A2R main thread/storage, refuse occupied debug registers and restrict selected return provenance to observer DLL.

DR0 callback, DR1 tail, DR2 return capture entry R8, RCX/RDX/R8/R9/RSP/RIP, selected extras/global, return site and RAX. Return requires same thread/entry stack at tail and RSP+8 at return. Native validator checks operand/stack correlation. Returned form identity comes from paired observer TRACE output; key form/symbol and validated handles remain unavailable. No broad dump.

Attachment pauses execution and Windows emits an initial breakpoint. Hardware registers and RF/DR6 resume state are explicit debugger-control interventions requiring review, not non-invasive observation. No custom INT3 patch, gameplay register edits, exception suppression, long stepping or forced termination. Restore original selected-thread debug registers, resume and detach with kill-on-exit disabled. Failures require operator recovery. Attach/context/cleanup remain untested against Starfield.

## Crash-tolerant outcome model

One selected operation OR 100 callback hits OR 5 seconds armed, whichever first; 5 s setup, 1000 debug events, <=300 records at <=4096 bytes and <=1,250,000 total bytes; zero retries. Independent 50 ms waits enforce zero-hit timeout. OS scheduling, flushing and cleanup may overshoot nominal time; no hard real-time guarantee. Primary observer has fixed output/count limits and cooperative 1 s selection / 2 s post-query checks; no forced interruption inside engine calls.

Flush events before continuation. Missing/truncated terminal files are incomplete; tested write/readback is not a crash/power-loss durability test. Evidence completeness, scientific result and target outcome stay separate. COMPLETE/SUCCESS/CRASHED is possible only with complete scientifically assessed evidence. Initial trace result is UNASSESSED. Pre-flush crash or missing A2R cannot answer reload. Corruption, restoration/detach failure stops with preservation/recovery; never automatic kill, relaunch, retry or evidence deletion.

## Save-copy/hash plan

Prepared local machine-readable manifest includes sample alias, logical checkpoint, parent, actual filename, timestamp, size/hash, game build/profile, body/location, observer IDs, actions, incidental artifacts and publication class. All future actual artifact fields are null, not invented. No copy helper was executed or supplied that silently enables Gate B.

After separately authorized live work and known exit/crash state, inventory new source saves against pre-session metadata; correlate each using operator action times and menu observations, not filename guesses alone. Stop if ambiguous. Hash source; copy to a new ignored session/checkpoint directory using create-new/no-overwrite; hash copy and rehash source; require equality and unchanged source metadata. Record both locators locally. Never move/delete originals or overwrite either protected parent. Rehash parent/backup before/after the future session. Save-content comparisons remain a later phase and cannot infer semantics from changing bytes alone.

## Exit-save treatment

Record autosaves, accidental saves and exit saves separately with session/checkpoint context. Never rename one into a primary checkpoint or treat it as a no-action control without later justification. Preserve originals; do not delete files to make an inventory tidy. Report autosave despite reported settings without changing configuration.

## Console exclusion / later follow-up

Primary experiment uses ordinary menu saves only, with external logical aliases. Never open the console, force filenames, change Developer Mode/achievement state or patch saves. Backlog only: a separate experiment branching from pristine SOR-SAMPLE-0001 should distinguish never-opened console, opened/closed without command, and command executed. None of those branches was executed here.

## Operator run card

**Vortex exclusively owns deployment and retirement.** After separate Gate B approval the user manually installs/deploys/retires the exact reviewed ZIP through Vortex. Codex never directly copies/removes game DLL/config files or uses a parallel manual deployment path. Record ZIP/Vortex profile/deployed identities and preserve evidence. This supersedes the earlier temporary manual deployment proposal, which was never executed.

The exact [future operator card](EXP0002-operator-card.md) specifies package/profile preflight, approved install/launch path, protected parent selection, READY/session checks, command trigger, six construction/capture/menu-save steps, A2R runtime-only reload, completion checks, optional diagnostic, exit/archive and stop/cleanup. Researcher runs helpers; user uses ordinary game UI. No pointer/register transcription or console. Gate B remains unauthorized; UI labels/profile/menu identification and live safety are untested.

## Risks and stop conditions

Hard-stop instrument acquisition for changed parent/build/site, profile mismatch, unsafe structural reads, unapproved dependency/permission or invalid request, unbounded acquisition, output failure, C: or D: available space below 40 decimal GB (or unreadable), unsupported debug-context intervention or corruption. Ambiguity/count mismatch, successfully read collection/identity/player changes and observation-time overruns instead persist bounded anomalies and leave the instrument available for a fresh next explicit checkpoint; no target is guessed. Report accidental save/movement/placement, material shortage, NPC/combat, wrong object, observer failure, crash and UI anomaly. Do not silently fix any. Source semantics, UI actions, callbacks and timing are not qualified by offline tests. No cleanup removes evidence; synthetic temporary fixtures alone are automatically cleaned.

## Offline validation

Nine original Python tests pass. Native synthetic tests cover bounded selection/ambiguity/duplicate-cell and collection-change handling, finite identities, exact requests, ASLR arithmetic, write/flush/readback/overwrite/size guards, actual DLL rejection of wrong version/non-game hash, and debugger correlation/zero-hit/hit bounds. Python validates production serializer bytes and rejects invalid roles/order/read/coordinate/terminal/evidence kind. Final counts, compiler/package identities, preservation and repository checks appear in the [audit](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/exp0002-preparation-validation.md`).

No live query safety, reference ownership, full plugin profile, crash durability, debugger attach/restoration or coordinate semantics was tested. Header task contracts are source-reported; operand evidence is static. No game/SFSE launch, deployment or semantic save inspection.

## Live execution gate

**Current update, 2026-10-06:** SOR-D-0012 authorizes the six primary Gate B checkpoints. The [Gate B run record](EXP0002-gate-b-run.md) supersedes the earlier unauthorized status below and records preflight, the configuration/package correction and pending operator handoff. The optional debugger remains unauthorized. Earlier preparation statements are historical; no live success is implied.

Offline implementation and review package are prepared. Critical review must assess selection/lifetime/ABI assumptions and optional debugger context intervention; compilation is not live qualification. Separate user approval must accept exact package/config/profile/sequence and first-run risks. Default is primary six checkpoints; optional diagnostic needs a separate decision after those are secure. Material changes are surfaced before execution. SOR-P-0001 satisfies the exact header use, not broader reuse.

LIVE EXECUTION NOT YET PERFORMED
DEPLOYMENT NOT YET PERFORMED
SAVE3 NOT LOADED OR MODIFIED
DEBUGGER NOT ATTACHED

## Expected discriminating outcomes

Stable logical relationship with changed pointers supports restored/reconstructed membership, not direct persistence proof. Different workshop results with unchanged placement challenge direct-beacon ownership. Owner/resource subset omissions, if later queried, refute exhaustive use of those APIs. Stable positions require matched body/cell/frame before comparison; changed coordinates may mean a frame transition. No-action differences bound background variation but do not label saved bytes. Independent repetition on another pair remains necessary before generalizing beyond this one site. Missing/ambiguous observations narrow no hypothesis and must remain failures/unknowns.

## Accepted correction: Vortex ownership and anomaly handling

2026-10-06 user instruction supersedes the earlier terminal-on-unexpected-observation behavior and temporary manual deployment proposal. No deployment or live authority is added. [Native policy table](../../runtime/exp0002/README.md) reviews collection_changed, unstable_identity, player_or_load_changed and time-budget cases separately. Anomalies retain up to 16 safely copied candidates, expected/observed role counts, completeness/truncation and completed-query evidence; ambiguous/unqualified selection invokes no selected-reference query. A persist failure becomes terminal. Count completeness concerns only the bounded scan, not universal outpost membership.

Six explicit checkpoint slots and the 45-minute lifetime remain unchanged. ANOMALY_RECORDED consumes a slot without promoting it to success; request.ps1 requires -AcknowledgePriorAnomalies for subsequent requests. Sequence outcome with any anomaly is CHECKPOINT_SEQUENCE_RECORDED_WITH_ANOMALIES, and the optional debugger diagnostic still requires six successful checkpoints. Safety checks enforce at least 40,000,000,000 available bytes on both C: and D: at startup, polling, evidence writes and queries. They cannot interrupt an engine call already in flight. No research finding, saved-state claim or integration-safety claim is strengthened.


## Accepted correction: operator-settled acquisition

2026-10-06: the user authorizes an offline correction following the first A0 load-notification anomaly. The [run record](EXP0002-gate-b-run.md) preserves that attempt and states the replacement synchronization model. PreLoadGame/PostLoadGame are optional telemetry, never required or correctness-controlling. Explicit operator confirmation plus fresh player/cell/world/collection/reference consistency checks gate each request. A2R requires a new reloaded-and-settled confirmation and fresh acquisition, without pre-reload selected pointers/handles. New output records declare operator_settled_fresh_state_v1 and optional notification counters rather than treating counters as a verified load generation. Review the fresh build before any deployment/rerun; debugger remains excluded. No new scientific claim is established by the correction.
