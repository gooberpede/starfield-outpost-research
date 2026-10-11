# Codex Implementation Brief — SOR Event-Associated Workshop and Terrain-Grid Oracle Instrumentation

**Project:** `D:\Projects\starfield-outpost-research`  
**Status:** Authorized implementation and offline/disposable qualification; **live Starfield deployment and execution require separate review**.  
**Proposed observer version:** `0.1.2` (successor to reviewed `0.1.1`).

## 1. Mission and success criteria

Build qualified instrumentation that records **native function invocations** instead of polling retained output storage. The scientific objective is independent engine-oracle validation of the existing deterministic offline outpost-position model, using the frozen Save25/Save26 predictions. This is not native-save automation, a general debugger framework, or a return to the deferred continuous latitude/longitude problem.

Two independently reportable milestones:

- **A — Mandatory workshop-center oracle:** capture fresh per-invocation native center results, actual input reference/workshop identity, thread and calling context; pair entry and exit from the *same invocation*. Obtain sufficiently complete evidence to test the frozen predicted durable centers for SOR-002 and SOR-003, including the relocated-beacon case.
- **B — Terrain-grid oracle:** capture the native selected reference/world/frame, translation, quantized grid result and relevant intermediate values for comparison with the saved-frame reconstruction. Implement and independently qualify this in the same cycle **if technically supportable**. Do not let difficulties with B jeopardize A. If B cannot be qualified, provide a concrete engineering obstacle, attempted tests, and a direct path to resolution—not a generic complexity objection.

Passing disposable tests is **not** claiming that either oracle was exercised in Starfield. No full-algorithm equivalence or native grid-oracle validation may be claimed until live, independently associated results exist.

## 2. Authoritative research inputs

Read the project's current `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, research-state and decision records before editing. Use the latest committed event-oracle investigation and its ranked acquisition design as the primary technical basis, together with:

- `docs/experiments/event-associated-position-oracle-and-build-mode.md` and `docs/experiments/event-oracle/acquisition-design.md` (verify actual paths against the repository);
- durable-position reproducer, oracle contracts, frozen predictions and Phase 1 Save25/Save26 results;
- observer `0.1.0` and `0.1.1` implementation, evidence and deployment history;
- the reference-handle project and, as methodological precedent, the maintainer's `starfield-resource-research` and `starfield-resource-reproducer` repositories.

Pinned current Starfield build: **1.16.244.0**; SFSE **0.2.21**. Verify exact module hashes, relocated addresses and bytes from the project's pinned evidence instead of treating the addresses below as executable without checks. Known native candidates from prior research:

- workshop-center helper: static `0x140F4AB80` (RVA `0x00F4AB80`);
- terrain-grid selection: static `0x140AD0D3B` (RVA `0x00AD0D3B`);
- shared ProcGen output is **not** an authoritative per-workshop oracle: it can retain prior XYZ while radius is cleared.

These addresses are leads, not authorization to patch unverified bytes or assume entry/exit calling contracts. Recover the exact instruction boundaries, ABI, relevant callers, outputs and triggering conditions from durable static findings and independently verify against the pinned executable.

## 3. Acquisition architecture — engineering discretion with mandatory proof

Choose the least fragile method that provides event-associated data. In-process SFSE hooks/trampolines are preferred where supportable, but a qualified debugger/breakpoint or another technique is allowed. Earlier DR0/debugger failures are relevant negative evidence, **not a blanket ban**. Record the alternatives assessed, selected design and why it fits each function's actual control flow.

For **every recorded invocation**, preserve at least:

- monotonic event/invocation identity; function/site identity and verified build/RVA;
- OS thread ID, nesting/reentrancy information, bounded caller/return provenance;
- original arguments and input-reference/workshop identity, including form/base/world/cell or workshop identifiers where obtainable;
- raw relevant argument memory (when safely readable), register/stack context at the suitable boundary;
- actual *native-produced* output or return, not an observer-side recomputation;
- entry/exit pairing status and failure classification; timestamps and capture provenance.

Design explicitly for parallel/reentrant invocations, multiple returns, unwinding/exceptional exits and missing exit partners. An unpaired event is **partial evidence**, not automatically terminal. Event identity must prevent attaching SOR-003's result to SOR-002 after a site switch. Frame compatibility and freshness must be demonstrable before promoting a numerical match to oracle agreement.

If patching code, demonstrate safe instruction relocation, control-flow integrity, trampoline reachability, register preservation (including SIMD/nonvolatile state where applicable), stack alignment and unwind behavior. Specify how hooks are installed, made visible to other threads, and retired. Do not assume five-byte jumps or universal epilogues are safe without proving them for these sites. Do not invoke native saving.

## 4. Independent oracle branches

### A. Workshop center — mandatory

Instrument the *producing invocation* of the native center helper, not a polling read of `BGSPlanet::ProcGen`'s shared four-float buffer. Determine precisely where output becomes valid (the actual output pointer, local/return value or caller-consumed result). Capture input identity and produced XYZ; capture radius/validity only where part of the same qualified contract.

Specifically test the zero-relocation branch as well as nonzero compensation. Prior static findings show a zero vector can bypass the addition without bypassing center production. Do not assume every build-mode entry executes the helper. Investigate the trigger and relevant callers sufficiently to propose a workable operator action.

### B. Terrain grid — conditional, independently isolated

Instrument the native grid calculation/selection only if the site, invocation contract and event timing can be independently qualified. Aim to record selected source world, owning reference, effective terrain-frame base/translation, intermediate translated position, floor/quantization outputs and final grid hierarchy where actually produced. Associate the grid event with an outpost/workshop independently of output numerics. Identify whether it is reached via build mode, terrain updates, movement, loading or a separate path.

Do not force both oracles to fire on the same gameplay action. B must be independently disableable and must not destabilize A. If B is deferred, document the exact blocker and preserve A as a usable instrument.

## 5. Observer build, evidence, operational policy

Extend the existing observer to **version 0.1.2** if that is the selected architecture. Maintain consistent identity across SFSE export (`0x00010002` if using the established packed convention), filenames, ZIP, manifest, emitted evidence and inspection tools. Do not retroactively rename historical packages or modify earlier evidence. Build a Vortex-installable ZIP with only the approved payload and required notices; **Vortex is the sole deployment owner**.

Capture raw event evidence alongside interpretations, durable manifests and per-section hashes. Preserve independent streams as they are flushed. Prefer broad, useful acquisition during one or two sessions over numerous narrowly tuned experiments. **Do not inherit arbitrary small event counts, file-size, duration or hit limits**. Cyclic traversal protection, safe memory checks and avoidance of repeated identical failed operations remain correctness requirements.

**Hard guard:** a failed free-space query or fewer than **40,000,000,000 caller-available bytes on either C: or D:** must stop acquisition; likewise a genuine runaway writer, broken evidence integrity or compromised instrumentation safety. Optional unreadable pointers, unexpected values, unmatched events, absent calls and individual failed collectors are recorded as partial evidence, not global abort conditions. Separate (a) scientific completeness, (b) instrument health, and (c) process survival. A post-capture crash does not negate durably flushed, interpretable evidence.

Do not call target-native methods from an unproven OS thread. The SFSE task queue's documentation is not proof of actual Windows thread affinity. Do not perform unqualified intrusive calls merely to trigger the oracle.

## 6. Qualification before any Starfield experiment

Build suitable disposable fixture(s) that reproduce relevant ABI and call control flow. At minimum exercise:

- entry/exit pairing; overlapping calls on multiple threads; nested/reentrant calls;
- alternate exits, early returns, exceptions/unwinding and missing exit events;
- exact captured arguments and native outputs, including zero and nonzero relocation;
- register/SIMD/nonvolatile preservation, stack and instruction relocation where relevant;
- concurrent install/retire behavior, benign no-hit operation and safe output flush;
- branch independence: disabling/failing terrain-grid acquisition must leave center acquisition healthy;
- reader/writer failures, disk guard boundaries, recoverable partial evidence and cleanup;
- version/package/config consistency and unchanged pinned game inputs.

Tests must evaluate scientific accuracy and instrumentation health separately. Do not substitute synthetic success for Starfield runtime qualification. Preserve hashes and diagnostic output of failed tests; rectify defects before seeking deployment authorization.

## 7. Precommitted comparison and prospective operator workflow

Use the **already frozen** offline predictions, never retune the model to each native result. Primary controlled cases:

- Save25 SOR-002 (unmoved);
- Save25 SOR-003 (pre-relocation);
- Save26 SOR-003 (moved beacon but invariant durable center);
- Save26 SOR-002 (control).

Require explicit native reference/workshop association and common-frame qualification for any exact byte comparison. Report exact float32 result where applicable, actual numerical differences and any justified rounding differences. Do not adjust tolerance after observing results. Distinguish workshop-center validation from terrain-grid/full-model validation.

Prepare a **prospective** operator card with realistic call triggers and broad capture, but **do not launch Starfield, deploy the ZIP, attach a live debugger or conduct a live capture in this task**. After review, the established workflow remains: user deploys through Vortex → user smoke-tests → Codex performs **post-deployment** preflight and prepares/refines run card → review/authorization → scientific run. If the acquisition strategy requires a different sequence, explicitly justify it and request review.

## 8. Standing review-diff convention — update WORKFLOW.md

Add a durable instruction to `WORKFLOW.md` (and reference it from `AGENTS.md` only if needed) applying to **all future implementation, audit, documentation and research reviews**:

- Place review patch files under `D:\Projects\starfield-outpost-research\.local-work\diffs\`.
- Task-scoped file suffix: **`-task-only.diff`** — changes attributable to the current task.
- Cumulative file suffix: **`-complete.diff`** — **all uncommitted** changes since the last commit/HEAD, including **untracked text files**.
- Use a consistent descriptive task prefix; avoid ambiguous `review.diff`/`cumulative.diff` names without coverage labels.
- When there is prior uncommitted work, provide both; otherwise at least `-complete.diff`.
- Ordinary `git diff` omits untracked files: construct valid Git-style new-file patches for untracked *text* files or otherwise include them faithfully in the complete patch. Do not stage files merely to build diffs.
- Supply `git status --short`, changed-file manifest, exclusions manifest for ignored/binary/raw artifacts, and a completeness/applicability verification against the actual working tree.
- Identify renames, deletions and newly generated scripts/docs distinctly; verify `git diff --check` and internal links.
- Keep raw saves, captured memory, game binaries and other excluded artifacts out of Git and out of patch payloads; report their locations/hashes instead.

Treat this convention as a standing order, not a one-off deliverable.

## 9. Provenance, permissions and research boundaries

The `gooberpede` maintainer-owned-repository reuse exception applies: authorial permission and self-credit are not required for maintainer-authored code; **provenance remains mandatory**, identifying repository, path, revision/hash and reuse method. Embedded third-party material is not automatically covered. SFSE and other third-party licence/notice requirements remain separately applicable.

Do not alter or invalidate existing oracle predictions, historical snapshots, Save25/Save26 originals, archived saves, Ghidra source binaries or evidence. Preserve pre/post hashes. Prefer existing pinned builds/tools. Any discovered build/version drift must be reported rather than silently patched around. Do not investigate deferred build-mode spinner behavior except where required to instrument an identified native trigger; do not expand to native-save automation or continuous geographic lat/long interpolation.

## 10. Required review deliverables and completion contract

Return:

1. Answer-first status for milestones A and B, with confidence, coverage and what is still unknown.
2. Verified native sites, exact ABI/entry/output contracts, trigger conditions and chosen acquisition methods.
3. Entry/exit pairing design and concurrent/reentrant behavior.
4. Complete implementation/source change inventory, reproducible build steps and versioned ZIP path/SHA-256/member manifest.
5. Disposable qualification results, including negative/failure tests and preserved receipts.
6. Evidence format/inspector behavior and the disk/continuation policy.
7. Frozen-model comparison plan and a proposed live operator card, explicitly separated by oracle.
8. Specific reason for any deferred terrain-grid instrumentation and highest-value remedial step.
9. Provenance/permissions record and preserved-input checks.
10. `WORKFLOW.md` diff-convention update and examples of the actual generated review patches.
11. Review files under `.local-work/diffs/` named `...-complete.diff` and, where applicable, `...-task-only.diff`; `git status --short`; changed-file and exclusion manifests; validation receipts.

**Mandatory completion bar:** A must reach an offline/disposable-qualified, reviewable live candidate, or Codex must demonstrate a specific blocking technical incompatibility after pursuing available engineering approaches. B must either reach independent qualification or have an equally concrete disposition. “Difficult”, “possibly unsafe” or a generic “strong partial” is not sufficient to silently drop the grid oracle. Do not claim successful live execution before it occurs.

**No staging, commit, push, Vortex deployment, Starfield launch or live debugger attachment.** All implementation and documentation changes remain uncommitted pending critical review.

Suggested commit subject only if later approved:

```text
research: implement event-associated workshop and terrain-grid oracles
```
