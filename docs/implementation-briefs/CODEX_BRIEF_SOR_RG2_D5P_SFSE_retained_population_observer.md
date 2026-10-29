# RG2-D5P — SFSE Retained-Population Observer: Feasibility, Implementation and Qualification

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Phase A only — offline native investigation, implementation, disposable-process qualification and Phase B preparation  
**Phase B:** **NOT AUTHORIZED**. Only the maintainer may install the plugin through Vortex and start Starfield using **`sfse_loader.exe`**. Do not launch through Steam as an SFSE test: ordinary Steam launch bypasses the requested loader path.  
**Status:** Implementation brief; freeze AC1–AC8 before work begins.  
**Publication/B6:** ON HOLD.

## 1. Scientific purpose and completion contract

**Scientific question:** Does the first successful resource-source construction query select the resource population retained by the ProcGen manager, and does a later request reuse that same completed population within a qualified source lifetime?

Develop and independently qualify an **in-process SFSE observer** capable of yielding evidence for that question. The instrument must not be a mechanical translation of the D5L–D5O fourteen-breakpoint external debugger. Prefer the smallest effective native observation interfaces, function hooks or targeted detours. A construction-only witness, hit-only witness, or contradictory observation is scientifically useful but must be classified at its actual evidence strength; it must not be represented as a complete chain.

**Phase A engineering completion:** functioning version-pinned plugin, evidence contract, reproducible relevant synthetic tests, valid post-crash evidence handling, independently reviewed frozen deployment artifact and executable Phase B card. Positive confirmation of the scientific hypothesis is **not** an acceptance criterion. Actual runtime Starfield reliability and scientific outcomes remain untested until separately authorized Phase B.

**Scoped negative/feasibility outcome:** If credible in-process observation cannot be implemented safely, identify precisely the inaccessible native boundary, tested options, failed controls and smallest missing capability; return an honest REWORK/ESCALATE rather than weakening the scientific contract or claiming completion. Diagnose and fix in-scope implementation failures under this assignment rather than stopping at the first failed test.

## 2. Existing research and plugin implementations — inspect before design

**Start with the actual local repository tree and existing working examples**, including both:

- `D:\Projects\starfield-outpost-research\` — prior SFSE observers, experiments, build scripts, plugin load/version checks and native field/receipt methods.
- `D:\Projects\starfield-reference-handles\` — prior functioning SFSE observer plugin(s), their deployment/verification instructions, recorder and lifetime/identity patterns.

Do not assume a particular source file exists or that past observer code is correct merely because it previously loaded. Locate the actual implementations and inspect their source, toolchain, build metadata, compatibility pins, logs and known limitations. Report which designs are reused, adapted or rejected and why. Prefer reusing tested plugin initialization, safe logging, native function registration, address relocation, threading and evidence-transport patterns. Preserve provenance and relevant third-party licensing and avoid unnecessary new dependencies.

Read the applicable `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, the existing D5C–D5O native/source ledgers and the D5L–D5O failed-run reports and review records. Relevant science includes D5C's source-pointer-keyed retained map and distinct visited guard, D5H/D5I's qualified variable-mask paths, and D5L's difference between inserted wrapper and successfully copied region. The D5L/D5M INT3 and D5N/D5O DR0 retail failures are evidence against assuming debugger traps will deliver reliably; in-process instrumentation must justify its own assumptions.

Pinned research baseline (reverify from installed sources before using): Starfield **1.16.244.0**, `Starfield.exe` SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; `Starfield.esm` SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`; PlanetData SHA-256 `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`. Verify the installed SFSE/CommonLibSF versions and actual compatibility rather than importing assumptions from online version tables.

## 3. Minimum observation contract

For the selected source, a *complete witnessed-region chain* needs:

1. **Source demand:** original initiating query/coordinate and effective manager/frame context, source descriptor and manager lifetime; distinguish source geographic identity from native pointer identity.
2. **Decision:** positively observed visited-source guard outcome and source-map hit/miss. A visited bypass does not certify map lookup or a complete population.
3. **Generation inputs:** direct sampled ordinary resource mask and effective resource/descriptor inputs, correlated with the source-specific construction invocation.
4. **Successful geometry:** at least one fully formed resource region with exact ordered native point words and bounds, correctly copied into a retained collection; wrapper allocation, map insertion or visited marking alone do not establish this.
5. **Retention:** the region belongs to the final owned wrapper, resource map and source in a qualified lifetime.
6. **Reuse:** a subsequent qualified map hit or equivalent provable retrieval of the same completed population, with matching region identity/bytes and no intervening relevant reset, destruction, replacement or alias ambiguity.

Prefer checking completed state at a safe later function boundary rather than hooking every inner point-copy operation, **only if** equivalence of ownership, completeness and ancestry is demonstrated. A full resource census and downstream Workshop consumer linkage are optional, not prerequisites to a one-region chain. Retain construction-only, retention-only, hit-only, bypass and incomplete-coverage results separately. Do not infer first-ever construction from first-observed construction or promote source pointer equality alone to lifetime proof. Never choose a mask to match prior geometry.

**Primary live candidate (unchanged):** second Feynman V source `0:37536:20928:0029d20e`, chart 0, owner FormID `0x0005e0de`, protected Save52. D5B observed three regions matching frozen conditional mask 3; D5H/D5I establish qualified mask 0/3 alternatives. These are held-out context, not inputs used to fit the new observer.

## 4. Architecture and implementation

Before major coding, produce a small decision record comparing: existing SFSE interfaces, function-entry/exit hooks and narrowly targeted detours for the required boundaries. Select the least intrusive architecture that can preserve the causal chain. Only introduce extra hooks when their incremental evidentiary value is specified. Do not recreate the external debugger's fourteen hooks by default.

Required implementation safeguards:

- Exact executable/module/plugin identity, relocation and instruction/prologue validation before any native patch or callback installation. Refuse mismatched versions and unsupported function shapes.
- Correct ABI, stack/register preservation, trampoline relocation and original-call semantics where hooks are used. Handle nested and concurrent invocations and recursion without conflating events.
- Source/manager lifetime and generation-epoch tokens or an equivalently qualified ancestry mechanism; demonstrate how pointer reuse and reset invalidate joins.
- **Lightweight hook hot path**: bounded copying and validated native reads; avoid expensive formatting, hashing, filesystem I/O and blocking work inside the intercepted function. Explicit capacity/drop/failure reporting and backpressure policy, with no silent eviction of decisive evidence.
- Durable append-only capture transport with framing, sequence numbers, identity, CRC/hash or equivalent validation, flush/ack state and independent offline reader. Distinguish enqueued, written, flushed and independently verified observations. Crash after decisive durable capture is acceptable; clean game shutdown is optional. Crash before durable decisive evidence is an incomplete acquisition.
- Unsupported native state or incomplete reads fail closed for that claim, not by inventing zero values or inferring absence. Unexpected observations and contradictory geometry are preserved.
- All plugin functionality is research-only, with no gameplay mutations, forced generation, cache clearing, console commands, save modification, or automatic change to source/population state.
- Minimize persistent installed files: source/build/test artifacts remain project-local; output directories under task-owned ignored scratch. Only reviewed release/deployment bundle is to be handed to maintainer.

## 5. Phase A verification

Use real disposable Windows native fixtures and/or an isolated host sufficient to exercise the **actual built plugin hooks and recorder**, not just mock JSON reducers. Qualify:

- plugin load/version rejection and exact hook site identity;
- correct query/mask/source/manager correlation for concurrent and nested requests;
- successful region copy/retention and later hit with exact native point/bounds equality;
- partial or failed generation, wrapper inserted before population, and visited bypass;
- manager reset, source retirement, allocator address reuse and ABA rejection;
- incomplete/corrupt/torn records, dropped capture, output failures and crash before/after durable decisive evidence;
- safe deactivation/teardown where supported, without requiring clean exit as a scientific success condition;
- counterexamples and unexpected outcomes not rewritten to confirm the model.

Verify representative retained scientific controls and native pin identities **proportionately**; don't rerun full geometry research merely because observer code changes. If an SFSE plugin cannot realistically execute inside a synthetic host, qualify exact built native hooks in a justified alternative fixture and disclose the untested retail integration boundary. Synthetic green tests must not be described as proof of retail reliability.

## 6. Maintainer-owned Phase B deployment and operation — proposal only

**Codex must not install, enable or remove the plugin in Vortex; must not run `sfse_loader.exe`, Steam or Starfield; and must not change Vortex profiles, plugins, saves or installed game files in Phase A.** The maintainer owns installation through Vortex and launch **via `sfse_loader.exe`**, not through ordinary Steam launch. Codex may inspect existing installed SFSE/toolchain state read-only, prepare a deployment package and write explicit operator instructions.

The proposed Phase B run card must distinguish:

1. **Preflight (Codex, read-only):** verify installed game/version/SFSE prerequisites, protected save/backup/content identities, disk free-space floors of **40,000,000,000 bytes on C: and D:**, expected plugin package and intended Vortex deployment paths/profile. Record existing plugin presence/absence and any potentially conflicting version. Do not require live install to complete Phase A.
2. **Maintainer action:** install/enable the approved package in Vortex, then launch through SFSE loader and perform the agreed ordinary Save52 load/travel sequence. No script should silently install or launch on the maintainer's behalf.
3. **Ready gate:** after launch, verify from plugin-generated startup evidence that the exact approved DLL loaded, attached required native hooks, and completed their own identity/coverage checks **before the operator loads Save52**. Installed files or a process name alone do not prove hook readiness. If READY fails, do not load the save for the experiment.
4. **Observe:** second Feynman V, source above; no forced regeneration, no gameplay instrumentation changes, no retries or alternate targets without approval. Preserve partial findings and decisive complete chains separately.
5. **Postflight (Codex, read-only):** authenticate evidence, compare protected inputs and configuration, confirm plugin **removal/disablement in Vortex** after the maintainer removes it, and record both Vortex/deployed-path absence or expected disabled state and relevant startup/closeout evidence. Do **not** remove the plugin itself. An unexpected deployment residue is a postflight issue, not permission for Codex to delete it.

Give the maintainer a concise installation/launch/removal checklist and an executable, exact-pinned run card. The live run remains **NOT AUTHORIZED** until separate explicit GO after Phase A review. Steam Cloud state confirmation remains necessary; `remotecache.vdf` changes are diagnostic, not protected-save hash failures. Preserve the user's decision that a crash after verified decisive evidence is acceptable. No clean shutdown requirement, automatic retry, or archival programme.

## 7. Research workspace and preservation discipline

Read-only scientific research means original protected inputs and accepted decisive evidence must not change. It does **not** require preserving every `.py`, `.json`, fixture log, failed build or derivative generated in `.local-work/`. Codex may replace/remove task-owned disposable intermediates freely. Retain only the final source/build method, essential failed counterexamples, decisive evidence, bounded qualification summary, review package and necessary reproducibility identifiers. Don't silently delete historical primary observations or evidence accepted in earlier tasks. Use the active archive-backed baseline, no old 93,334-file loose audit, and no unrelated archive/housekeeping work. Keep any proprietary decompilation or raw native dumps local-only and outside tracked paths.

## 8. Frozen acceptance criteria

| ID | Mandatory outcome |
|---|---|
| **AC1 — Authority and protection** | No live game operation, plugin installation/removal, Vortex or save/config mutation. Pinned inputs and protected evidence unchanged; 40 GB disk floors observed where applicable. |
| **AC2 — Prior methods and feasibility** | Inspect both projects' actual working SFSE observers, compare native observation options, justify selected minimal hooks and document reused design/provenance. |
| **AC3 — Native evidence contract** | Trace and qualify query, mask, source/manager lifetime, completed region ownership and reuse; no false first-ever, wrapper-only or pointer-only claims. |
| **AC4 — Implemented observer** | Build a version-pinned SFSE observer plugin with relevant native instrumentation and a verified, independently consumable evidence format. |
| **AC5 — Qualification and scientific discrimination** | Demonstrate the complete witnessed-region chain and adversarial/negative cases on disposable Windows/isolated native fixtures; authentic contrary evidence must survive. State retail limitations. |
| **AC6 — Phase B operational readiness** | Exact deployment package, maintainer-only Vortex installation and SFSE launch/enable/disable/removal instructions, preflight READY and postflight absence checks, protection/STOP/crash rules, complete proposed run card marked NOT AUTHORIZED. |
| **AC7 — Focused durability and editorial completion** | Concise reproducible evidence, hashes, outcomes and failures; task-owned scratch disposable; current preservation policy and editorial standard followed; no irrelevant full audits. |
| **AC8 — Independent review and exact delivery** | Independent scientific, engineering and editorial dispositions against AC1–AC8, corrective rework within scope, frozen final hashes, verified complete/task-only diffs, explicit status/exclusions. No staging, commit, push, integration, B6 or publication. |

## 9. Deliverables

- `docs/experiments/resource-retained-population/d5p-report.md`: concise architecture, what was actually implemented, qualification results, scientific limits and exact missing capabilities.
- `docs/experiments/resource-retained-population/d5p-review.md`: frozen AC1–AC8 matrix, independent dispositions and editorial completion.
- `docs/experiments/resource-retained-population/run-card-d5p-v1.md`: proposed Phase B steps, preflight/READY, **maintainer-only** Vortex/SFSE actions, postflight confirmation and separate GO.
- Task-owned plugin source/build tooling and a **single reviewed deployment package**, with identity and compatibility manifest. Reuse repo conventions where practical.
- Compact source/provenance ledger and relevant tests/qualification summary; decisive raw receipts may remain local-only.
- Complete and task-only diffs with exact hashes, inventory/status and bounded exclusions. Do not stage/commit/push.

If a particular path conflicts with existing repository conventions, follow the established layout and document the change. Keep the deliverables focused; avoid creating redundant per-experiment manifests and huge persistent scratch collections.

**No result from Phase A authorizes Phase B.**
