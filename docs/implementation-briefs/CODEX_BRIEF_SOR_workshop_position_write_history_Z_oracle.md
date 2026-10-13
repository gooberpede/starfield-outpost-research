# Codex implementation brief — SOR Native Workshop Position-Write History and Z Restoration Oracle

**Assignment:** Integrated offline implementation, qualification, Vortex packaging, and a prospective live run card. **Do not launch or attach to Starfield in this assignment.** Continue in `D:\Projects\starfield-outpost-research` from the latest committed/synced state. Comply with `WORKFLOW.md`, the Research Execution and Completion Protocol, evidence/provenance rules, and existing repository documentation. This brief authorizes implementation and disposable testing, **not** live deployment or execution.

## 1. Purpose and scientific baseline

The 0.5.0 observer provided 40 fresh Workshop grid observations, 20 each for SOR-002 and SOR-003, with identity-associated XY grid agreement against frozen Save25/26 controls, including nonzero translations and the SOR-003 hierarchy carry. Subsequent analysis recovered the 2D source-frame key `0x02b20e79528028e0`. Full saved-to-loaded XYZ equivalence remains unvalidated because the native Workshop center Z differs from saved Z:

| Workshop | Saved Z (approx.) | Live native center Z (approx.) | Saved minus live |
|---|---:|---:|---:|
| SOR-002 | +18.352507 | +3.643147 | +14.709359 |
| SOR-003 | −31.890842 | −9.516418 | −22.374424 |

These are *diagnostic differences*, not preapproved correction vectors. Existing captures show zero Workshop relocation compensation for these cases, with native reference Z agreeing with returned center Z; do not infer a terrain-height datum or invent a Z translation. The grid translation operand is **XY only**—an adjacent stack word was previously misread as a third component.

The latest offline research identifies reference construction/replacement via `B4E410`, ordinary frame conversion `B734C0 → B73310` (including a signed XYZ application), `+0xD3` reference frame state, and native Workshop-center calculation `F4AB80`. Source addresses/RVAs and ABI interpretations must be reverified against the installed and pinned retail executable before building hooks. The saved ordinary created-reference path reportedly bypasses alternative edge-addition branches at initial load; investigate without presupposing that any one writer explains the observed Z discrepancy.

**Primary question:** What sequence of native position writes and frame-state transitions takes each identified Workshop reference from its serialized position to its observed live position and center Z? Obtain enough history and identity evidence to reconcile the discrepancy, or demonstrate exactly where writer/epoch/identity coverage is incomplete. Generic terrain generation and ship-landing reconstruction are not principal deliverables.

## 2. Required preliminary static audit

Before choosing instrumentation, reconstruct the relevant writer coverage from the most recent native-code and save evidence. Explicitly investigate:

1. `B4E410`: callers, initial creation versus replacement roles, reference pointer/handle lifetime, argument provenance, value type, in-place effects and possible wrappers or bypasses.
2. `B734C0 → B73310`: conditions, signed vector producer, deferred/queued application, `+0xD3` before/after, thread and object ownership, effects on all XYZ components.
3. `F4AB80`: fresh reference position, full `ExtraWorkshop +0x60` compensation vector, center output, own-parent/world identity distinct from the enclosing query/source frame.
4. Other *plausible actual XYZ writers* that could affect these references between saved-record reconstruction and center observation, including direct stores, dispatch through virtual methods and deferred application. Produce a writer-coverage table with evidenced sites, exclusions, and unresolved routes. Do **not** claim an exhaustive write set simply by enumerating hooked functions.
5. Identity/remapping lifecycle: the earliest point at which a reference can be linked to SOR-002/SOR-003; dynamic/static ID namespaces, parent and epoch changes, pointer reuse, and how early generic writes can later be associated with a Workshop.

Distinguish proven code paths, possible paths, and observed live behavior. Permit the specialist sub-agent to independently audit writer/ABI/identity coverage and identify counterexamples before design freezes.

## 3. Instrumentation: lossless capture is mandatory

Develop a versioned SFSE in-process observer building on the qualified 0.5.0 architecture where appropriate. **Do not revive the closed external-debugger/INT3 path.** Select the narrowest qualified native mechanism that can acquire authentic naturally executed writes and pair them to individual reference lifetimes, without fabricating calls or changing application semantics.

Required scientific fields where available:

- Native event identity, thread, monotonically ordered sequence, producer/caller ancestry, invocation/queue identity, game/SFSE/plugin version and native site guards.
- Before/after reference XYZ as raw binary32 bytes and decoded values; operand XYZ/vector or replacement input as raw bytes; relevant `+0xD3` state before/after and flags/metadata relevant to operation applicability.
- Raw reference pointer and any legitimate reference/form/handle/parent/world/base/workshop identity available at that moment, with validity, source and epoch; never silently equate pointer to durable ID.
- Initial construction event, conversion event, replacement event, deferred producer/application relationship, and center invocation with reference XYZ, compensation XYZ and returned center, distinguishable by record type.
- Validity/error states for unavailable optional fields; unpaired or unfinished calls and object-lifetime uncertainty preserved, not replaced with zero or guessed joins.

**Lossless design:** Do not rely on early filtering to named Workshops if that can discard writes before their identities become known. Capture enough of the relevant generic write population, with durable raw provenance, to perform *retrospective* identity/lifetime joins. Do not silently drop events under high rates or queue saturation; use a correctly qualified backpressure/spooling strategy. A genuine inability to preserve data must be surfaced as an instrumentation-integrity condition with full counts and last durable sequence, not mislabeled as a scientific negative. Treat producer/application ancestry and thread interaction as testable requirements. Preserve exact original bytes, meaningful ordering and failure traces. Do not assert history completeness from absence of events or from hooks merely being installed.

The observer must distinguish:

- **Complete history within a demonstrably covered writer set and reference lifetime**;
- **Partial observed history**, with missing identity, producers, writers or periods named;
- **Scoped no-write observations**, justified by a specific proven coverage interval;
- **Unusable/missing evidence**, with reason.

A native center match by itself is not a complete restored-position model; if no direct history is recovered, the results must still isolate the deepest operation observed and the precise gap.

## 4. Durable transport, safety, deployment

Retain proven SFSE/Vortex deployment conventions. Explicit runtime payload checks must require **only** `Data\SFSE\Plugins\SorNativePositionOracle.dll` plus separately justified essential runtime dependencies. Documentation, manifests, README and research text files are *not* deployed-file admission requirements. Preserve versioned build/archive/DLL hashes, actual module inventory and pinned native instruction preimages. Expected Steam and NVIDIA overlays are baseline, not automatic refusal conditions; credible conflicting instrumentation should be addressed explicitly.

Retain:

- Absolute **40,000,000,000 caller-available bytes** free on **both C: and D:** as mandatory guard; failed disk queries stop acquisition safely.
- Protected Save25/26 and other canonical saves, archives, fixed predictions and previous sealed sessions unchanged; use read-only checks, immutable new experiment evidence and hashes. Do not stage raw `.sfs`, dumps, proprietary binaries or sensitive local material.
- Durable, inspectable, integrity-checked raw event data; journal and postflight accounting sufficient to distinguish captured events, loss, partially committed records, worker health, and legitimate operator retirement. No data rewriting to make validation pass.
- Continue healthy acquisition through odd scientific values, optional unreadable fields and delayed actions; only real safety, data-integrity or instrumentation failures or operator STOP are hard stop conditions.
- **No arbitrary wall-clock, monitoring-cadence, operator-response, event-count or evidence-size hard cutoffs.** A proposed additional hard limit requires a demonstrated necessity and advance maintainer authorization; warnings do not silently turn into STOP. Respect existing workflow policy.
- Hooks may remain resident until normal game exit only if safe/qualified and explicitly described; STOP/retirement semantics must be accurate, especially during writes or pending invocations.

Do not overfit the design to exactly two Z differences or introduce a guessed adjustment into frozen production models. Capture is the priority.

## 5. Disposable qualification and independent audit

Provide reproducible native fixtures and offline tests for original-instruction preservation, call/return ABI and floating-point state, all three components of write semantics, nested/reentrant/concurrent calls, pointer reuse and identity-late-binding, producer/application timing, queue/backpressure and genuine write failure, worker STOP and retirement, crash-after-flush recovery, absent/invalid memory, guard mismatch and protected-input preservation. Include a high-event-rate fixture and a non-Workshop early-write fixture that later acquires identity; assert **zero silent data loss** and correct retrospective association.

Where no finite fixture can establish global writer coverage, explicitly state the scoped proof and limitations. Correct all in-scope failing tests and reviewer objections under the **same assignment**, not in a new handoff. The independent reviewer receives the original acceptance contract, source/diff, primary fixture artifacts and actual pass/fail records; it may require REWORK. At most **two concurrent sub-agents** (reviewer plus optional specialist); primary Codex agent does not count. Track the specialist's *distinct technical contribution* concisely; no further routine effectiveness audit of the reviewer is required.

## 6. Integrated prospective Save25 live run card

Deliver the **complete run card with the qualified Vortex package in this same assignment**, for joint maintainer review/authorization. Do not execute now. The prospective operator sequence is:

1. User deploys the approved plugin with Vortex. Codex verifies exact DLL/game/SFSE/preimage identities, protected inputs, 40 GB guards, readiness and durable evidence health **before** save loading.
2. Give one exact upfront save instruction, without repeated confirmations: **“Load Attila Kiraly Save25 — Kreet - Outpost, 10/9/26 at 9:22:22 PM (Level 4).”** Use the already recorded screenshot mapping. Ask for another screenshot only if a real ambiguity or conflict arises; never guess by mutable list ordinal.
3. Observe scene settling at SOR-003. If the run-card logic requires loading SOR-002, direct one ordinary travel to SOR-002 and, where justified, back to SOR-003. The operator reports actual visible state; no new landing, construction, beacon move, console commands, or new save is included.
4. Preserve early generic writes from the load epoch and later Workshop/center observations with event/lifetime joins. Do not presume that loading both Workshops proves a complete write history.
5. On agreed completion or explicit operator STOP, safely retire, allow normal game exit, independently verify postflight, seals, session inventories, and original protected hashes, then analyze the native XYZ histories against the *unchanged* saved/frozen comparisons.

The run card must specify exact step-by-step machine/operator coordination, identity and guard verification, STOP before/after READY, error recovery, sealed evidence procedures and **prospective** scientific interpretations. Successful preflight after our single combined approval authorizes the reviewed live run without another routine review. Any changed hook/DLL, new live action, materially different safety contract or further experiment requires separate approval.

Avoid arbitrary confirmation cycles and do not end the assignment at postflight sealing: the **subsequent authorized live run's** normal final handoff includes scientific reconciliation and independent review as well as cleanup, unless the operator expressly requests only an intermediate operational checkpoint.

## 7. Deliverables, acceptance matrix and stopping rules

Return together:

1. Versioned observer source, build provenance and reproducible binary/package with pinned hashes; Vortex deployment contract.
2. Static writer coverage and identity/lifetime report with named native-code evidence, hypotheses, negative leads and risks.
3. Disposable fixture/tests and recorded actual results; independent reviewer findings and completed rework ledger.
4. Event schema, reliable decoder/inspector and retrospective Workshop association mechanism. Inspector must differentiate observational completeness and scientific equivalence.
5. Complete, ready-for-review live run card with precise Save25 instruction, no extra routine approvals, and genuine safety rules only.
6. Durable docs (decision, evidence, source/provenance and research indexes as appropriate), `git status --short`, changed/excluded file manifests, path/hashes and **complete plus task-only** review diffs under `.local-work/diffs/` including newly created text files. No staging/commit/push.

An implementation result may be returned as **COMPLETE — PASS** only if the agreed offline functionality, qualification, scientific acquisition feasibility and integrated run-card requirements are met. A **complete evidence-bound feasibility failure** requires primary evidence for an actual blocker, attempts to resolve feasible in-scope causes, and an independent review; do not present a failing mandatory fixture as a qualified plugin or relabel unfinished work as completion. Do not require live native equivalence to PASS this offline assignment, and do not claim it before actual independently associated live results.

**Authority boundary:** No Starfield game execution, attachment, deployment, Vortex modification, live input, new saves, external publication, staged Git changes, commit or push in this brief. Return the package for combined critical review and explicit maintainer authorization first.
