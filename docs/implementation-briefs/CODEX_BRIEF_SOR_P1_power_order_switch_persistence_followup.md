# Codex research brief — P1 follow-up: Power allocation order and switch-state persistence

**Project:** Starfield Outpost Research (`starfield-outpost-research`)  
**Type:** Focused offline research, documentation and verification follow-up to the *uncommitted* P1 power package  
**Authority:** No game launch, observer construction, injection, deployment, save restoration/modification, staging, committing or pushing. Maintain existing P1 changes and review them together with this follow-up.

## Purpose and scientific questions

Resolve two specific gaps in the P1 native power reference before considering P1 complete for commit:

1. **Allocation order.** The mapped allocation function is order-sensitive. Exactly how are graph traversal roots selected, neighbors ordered, and consumers presented to the allocator? Can a particular order be derived from serialized save data and matching game definitions, and which elements (if any) depend on runtime reconstruction?
2. **Switch persistence.** The engine uses an activation-state predicate for switches. Where does that state originate, how is it altered, saved and restored, and can the state of a specific switch be recovered from a save without confusing activation with powered status?

Also perform a **small, explicitly bounded confirmation** of the Fueled Generator's one-Helium-3-per-cycle input check versus its independent charged/uncharged state. Do not broaden this into fuel-network or inventory simulation.

These are native-function and data-representation questions. Do not implement a power calculator or mod. Do not assume that connection sequence alone fixes traversal order, that construction order is priority, or that a saved powered flag represents a switch's On/Off state.

## Required starting evidence

Read the current uncommitted P1 documentation and code, notably `docs/experiments/power/` (report, native mapping, saved representations, contracts, fuel, uncertainties and review), plus the earlier E1 powered-state mapping and save-analysis materials. Reuse the pinned executable/native export evidence, exact existing RVA identities, protected original save corpus, and the existing save reader and source-verification conventions.

Prior P1 claims to examine and verify rather than simply repeat:

- Power allocation around RVA `0x0066B100` is order-sensitive and uses cumulative demand.
- Neighbor enumeration around RVA `0x006779E0` and enqueue around `0x00677C50` are implicated in traversal; the native setting `bWorkshopPowerNonRecursiveTraversal` may select different traversal modes.
- `ExtraPowerLinks` (extra-data type `0xCB`) contains ordered linked-reference records and connection words; save order may not equal final consumer assessment order.
- Activation state is queried via a native helper around RVA `0x005CDC70`; `Extra0D` and script/animation state may be relevant but **not yet demonstrated** as the complete saved switch-state contract.
- The powered bit in `ExtraFlags` is not necessarily switch activation state.
- The fueled-generator definition appears to request one Helium-3 per fuel cycle at a nominal 36 engine-elapsed-second interval, with separate charged/uncharged behavior.

Reverify address/version pins and correct inaccurate preliminary interpretations when evidence demands it.

## Workstream A — Native allocation-order contract

Trace the specific call chain from Workshop electrical graph construction through root selection, visited-set handling, neighbor iteration, connection-type filtering, switch gating, queue/recursive traversal, consumer collection and the cumulative-demand allocator. Establish, wherever static evidence permits:

- What identifies traversal root(s), and whether the roots themselves have a defined order.
- Exactly which containers determine neighbor and consumer iteration order: ordered arrays, maps, sets, pointer/handle iteration or runtime registration order.
- How connection words and graph membership influence reachability, and whether powered, unpowered, switch and relay nodes change the walk.
- What the recursive/nonrecursive setting changes; do not claim equivalent sequences without evidence.
- Whether the allocation changes with graph insertion, handle restoration or rebuild, and what is or is not guaranteed stable.
- Whether a save contains sufficient data to reconstruct the **actual runtime assessment order**, rather than merely a plausible topology or a local neighbor order.

Use a small selection of suitable existing saved power networks as examples, not fabricated data. Recover saved ordered link records, qualify reference resolution and record *which part* of the traversal can actually be reproduced. Where possible, create a deterministic, non-mutating offline replay or fixture that exercises the verified algorithm and identifies unresolved runtime inputs; do not present synthetic agreement as live validation. If full order reconstruction is impossible from saved data, name the missing state precisely and identify the minimum achievable method of obtaining or falsifying it.

A final result may be **fully reconstructable**, **conditionally reconstructable**, or **not established**, supported by explicit native evidence—not speculation about a hidden priority list.

## Workstream B — Switch activation-state persistence

Follow the native switch-state getter to the *actual* fields, helpers and flags it consumes; map representative switch definition(s), construction/activation transitions and native save/load paths. Distinguish:

1. Switch activation (On/Off or the native equivalent).
2. Whether the switch itself is powered.
3. Whether downstream consumers are powered through graph traversal.
4. Animation, script and extra-data state that may encode, reconstruct or override activation.

Identify the authoritative persistence mechanism if available: relevant extra-data record types and fields, Papyrus/script instance properties, animation persistence, initialization defaults or post-load recalculation. Verify the field interpretation on saved examples only when actual switch identity/state can be grounded. Never infer an On/Off value solely from the powered flag or downstream state. A result that state is recoverable **only by native load-time reconstruction** is valid if proven and the dependencies are enumerated.

If the exact saved representation remains inaccessible, document the closest native contract and a *specific achievable* discriminating test (e.g. paired save snapshots of the same identified switch before and after toggling, examined offline, or a narrowly defined live observation proposed separately). **Do not perform such an experiment in this task.**

## Workstream C — Small fuel-threshold confirmation

Recheck the Fueled Generator's associated fuel recipe, input-check function and charged/uncharged state path. State precisely whether **one available He-3 unit satisfies one ordinary fuel-cycle input check**, whether any additional reserve threshold is imposed along that checked path, and which other independent state conditions might prevent immediate output. Do not claim one unit guarantees continuous running, and do not trace full inventory, storage or inter-outpost logistics.

## Documentation and evidence contract

Integrate results into the *existing* `docs/experiments/power/` references, with a compact follow-up report and updates to existing function-register/native/saved/uncertainty material. Do not create a competing native register. For each consequential claim provide exact pinned RVA / executable version, evidence source and relevant path or instruction provenance, plus separate qualifiers for static, definition-backed, save-corroborated and runtime-untested findings.

Include an explicit **save versus runtime availability table** for traversal order and switch activation: raw persisted data, derived values, missing runtime inputs, and which claims have actually been verified. Include representative saved objects or honest coverage limitations.

Preserve the pre-follow-up P1 scientific claims except where corrections are evidence-backed. Integrate findings and review history without silently rewriting earlier provisional statements as if always established.

## Completion and stopping rules

Use the revised classification **COMPLETE / INCOMPLETE / BLOCKED**, with evidence confidence independent of completion status; do not downgrade simply because the assignment is offline. Completion means the authorized questions have been thoroughly answered *to the extent justified by available evidence* and material unresolved dependencies are specifically identified. A consequential uninvestigated in-scope native path precludes COMPLETE; a properly exhausted evidential boundary may be documented without inventing further work.

No broad return to P1 generation, day/night, arbitrary power networks, storage logistics, remote cargo, or experiment implementation. Do not start a sequence of speculative fixes or indefinite further analysis. Any proposed future test must be feasible and discriminating, not an appeal to unavailable perfect observability.

## Review and deliverables

- Primary agent conducts the focused investigation; independent reviewer required under the project's `WORKFLOW.md`. Follow ordinary permitted specialist/concurrency limits.
- Reviewer checks the exact derivation of allocation sequence and the distinction between switch activation and powered status, save proof versus static inference, fuel threshold wording and scope discipline. Address substantive findings within this single assignment.
- Run appropriate focused native/source verification and existing regression tests; inspect actual saved samples where available; preserve all originals and compare protected input hashes in accordance with project practice.
- Mandatory prose-quality audit of **all newly authored or modified documentation** for fused words, malformed version identifiers, missing spaces adjacent to RVAs, counts or hexadecimal offsets, and corrupted encoding. Report examples checked and corrections performed.
- Deliver a consolidated report, updated P1 technical reference and uncertainty table, independent review record, commands and test receipts, preservation checks, and a suggested Conventional Commit subject covering **the combined still-uncommitted P1 changes**.
- Deliver `.local-work/diffs/` task-only and complete diffs, including untracked new textual files, with exact forward/reverse patch-reconstruction checks and a hash-bound output manifest. Do not include raw proprietary evidence, binaries or saves in review diffs.
- **Do not stage, commit or push.** The maintainer will review the combined package before committing.

## Success criterion

Another researcher should be able to understand **how the game determines consumer assessment order**, what of that order is serialized or reproducible offline, and **how a switch's native On/Off state is determined and persists**, with the precise remaining uncertainties stated if complete save-to-runtime equivalence cannot be proven. The fuel conclusion must be accurately bounded to the verified cycle-input requirement.
