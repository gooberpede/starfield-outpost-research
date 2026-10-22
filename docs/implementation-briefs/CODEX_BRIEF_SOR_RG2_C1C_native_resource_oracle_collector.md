# Codex implementation brief — RG2-C1C: Native resource-oracle collector implementation and synthetic qualification

**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Authority:** Implementation, instrumentation engineering and **synthetic-target execution only**. No attachment to, launch of, or modification of `Starfield.exe` in this task. No live gameplay, save production, publication, staging, commit or push.  
**Research baseline:** RG2-C1, C1A and C1B are committed. Treat their archived native maps, evidence and limitations as authoritative starting points; verify actual repository state before changes. Current pinned retail target for future work: `Starfield.exe` 1.16.244.0, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Do not infer live addresses from static VAs without module-base and instruction checks.

## Objective

**Implement and demonstrate a working external Windows debugger collector**, not another feasibility-only report. Against a disposable **separate synthetic Windows target**, the collector must use actual OS debugging facilities to observe naturally executing events, independently read target-owned resource-like structures and filter outcomes, and produce independently verifiable durable receipts. Hardware execution breakpoints are the preferred architecture from RG2-C1B. A different architecture is permitted only with documented evidence of a concrete blocker, explicit safety/evidence trade-offs and a comparably actionable implementation.

The eventual scientific aim remains native resource-list provenance at Feynman V (Ionic Liquids versus Copper), then Carinae III-a Iron. The retail pilot belongs to a **later separately authorized brief**. The collector must not be represented as already qualified for retail or as proof of geometry equality.

## Source and workflow orientation

First read `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, and `docs/templates/completion-contract.md`; locate RG2-C1B's report, native lineage, acquisition contract, receipt prototype/tests and reviewer conclusions, plus `docs/experiments/native-availability-map/output-contract.md` and RG2-C1 native contract. Reuse existing identifiers, schema and transport code rather than independently inventing conflicting formats. Record exact source paths and provenance. The old observer's **NO-GO** still prohibits reusing it unchanged: the new controller is independently implemented and qualified. Do not import third-party proprietary code or redistribute protected source/native dumps.

At intake, record branch/HEAD/index/worktree, exact relevant inputs and permitted scratch locations. Preserve already-committed research and frozen RG1/RG2 predictions. If anything is ambiguous, pursue a bounded evidence-backed resolution and document it rather than making up addresses or types.

## Implemented components

1. **Disposable native test target** under project-owned source: resource-like spatial/atmosphere/biome populations, a catalogue-style filter, refresh versus retained branches, deterministic case markers, and one or more naturally executed sampling boundaries. Target-owned memory must actually contain the arrays and relevant decision operands. Ground truth should be written independently or generated reproducibly for test comparison; the collector must *not* receive population contents through a convenient cooperation API masquerading as native observation. The harness is an analogue for debugging mechanics, **not** evidence that retail memory layouts match.
2. **External controller** using real Windows debugging APIs and, preferably, per-thread hardware execution breakpoints. Discover target process and module identities; handle initial stops, exception status, register/DR ownership, thread creation/exit, breakpoint installation/rearming, nested/repeated events, and process exit without silently losing observations. Any architecture relying on instruction patches, thread suspension or other intrusive measures must specify exactly how target state is affected, and the synthetic qualification must exercise those effects. Never attach to Starfield under this brief.
3. **Bounded foreign-memory acquisition**: read source- and population-tagged resource entries and actual filter decisions from target process memory at a stop; preserve process/thread/event identities and ordering. Validate count/capacity/pointer arithmetic before reads, impose documented memory/time/output budgets, reject partial or inconsistent groups with explicit `INCOMPLETE`/`LOSS` rather than reporting an observed empty list. The collector need not copy full vein-region geometry at this milestone; do not claim that it does.
4. **Durable receipt pipeline**: reuse/extend RG2-C1B's receipt contract, persist raw relevant values and normalized provenance with schema/version, source executable identity, event/branch labels, source/population and extractor-filter association, read status, hashes, and verified acknowledgement/readback **before** considering a capture successful or deliberately ending the session. Separate native observed values, synthetic ground truth and analyst inferences; distinguish unchanged retained collection from freshly acquired payload.
5. **CLI and operator controls**: support deterministic synthetic runs, selection of the disposable target, explicit `--synthetic-only`/allowlist or equivalent guard that prevents accidental retail attach, bounded event capture, stopping/terminating the disposable process, exit codes, receipts and diagnostic logs. Document precise build and execution commands, dependencies and where outputs are stored. Failure states must be intelligible without reading a debugger trace manually.

## Mandatory synthetic qualification

Execute the implementation against the **real disposable Windows test process**, not only mocks or parser fixtures. Include a test matrix covering:

- Actual breakpoint hit and correct process/thread/module-site identity; real independent reads of target-owned arrays; correct resource population origin and catalogue-style filter result against an independent oracle.
- A spatial refresh followed by a retained-list event; multiple callbacks/decisions; repeat visits without event mix-ups; target thread creation and exit, including new-thread breakpoint coverage where relevant.
- Zero-entry population versus read failure; corrupt pointers/count-capacity overflow; truncated records; event loss and interrupted copy; malformed receipt or failed durable acknowledgement.
- Termination/crash **after** a successfully flushed/read-back receipt, preserving usable evidence; crash/termination **before** such acknowledgement must not be graded as acquisition success.
- Safe isolation from existing project inputs, saves, binaries and the repository index, and verified no uncontrolled writes beyond approved scratch or new project outputs.

Test the implementation's actual Windows event mechanics and record commands, output receipts, hashes, observed results and unsupported/untested cases. A native executable/controller may rely on toolchains available in the local environment; if a required toolchain is unavailable, document the specific blocker and demonstrate as much of the real mechanism as possible using an available alternative, with executable qualification steps and an objective gate to finish. Do **not** substitute more conceptual architecture prose for a working collector while marking acquisition PASS.

## Future retail pilot — design only, not authority

Deliver a small, explicit retail-readiness checklist and first-pilot run card, grounded in C1B's catalog lineage (`FUN_1415795f0` → `FUN_1421f68f0`) and resource-population refresh boundary, with Feynman IL and Copper first and Carinae Iron subsequently. Require correct runtime module base, pinned EXE identity/instruction bytes, relevant reference/Workshop binding, target thread coverage, captured spatial/atmosphere/biome populations, filter outcome and refresh/retention state. Do not assert that native rows are vein geometry or that a catalogue eligibility test proves successful placement. Feynman VIII-b Au/Sb/Cu remains optional for later runtime-input stability discrimination, not a bug-reproduction requirement.

### Save protection policy for any *future separately approved live test*

**Backed-up, hash-verified saves are permitted some live-test exposure; zero theoretical write risk is not required.** The mandatory preflight is to inventory the exact saves implicated, locate all live save paths and cloud/autosave destinations, verify that independent recoverable backup copies exist, and compute/compare hashes of each protected live save and its intended baseline backup. Confirm the backups are **outside the game's write/synchronization path** and accessible for restoration. If a live save is deliberately different from its backup, document that fact and select an explicit known-good baseline; do not assert they match. Confirm backup readability/copy integrity and a tested or clearly rehearsed restore path. Isolate or control autosave/cloud synchronization where required. If any identity/backup/hash precondition fails, **NO-GO before launch**.

Postflight: inventory newly created/modified saves, hash both live and backup copies, compare against the frozen preflight baseline, disclose all deltas, and restore the baseline from the verified backup **if required**, followed by another hash verification. New controlled or ordinary saves may be created under a future brief, but label/retain them separately and do not overwrite the baseline accidentally. A game crash or unstable disposable session **after** a complete externally acknowledged capture may be acceptable; damage to recoverable live copies is manageable by restoration, but loss or corruption of the sole usable protected copy is not. Receipt integrity and operator awareness remain mandatory. Do not perform these retail operations in C1C.

## Frozen acceptance criteria

**AC1 — Authority, intake and preservation.** Policy and scope verified; only synthetic process execution; protected bytes, HEAD and index preserved. Explicitly no retail attach.

**AC2 — Working debugger controller.** Actual externally executed Windows debugging with a documented event and breakpoint lifecycle; hardware execution breakpoints preferred or evidence-backed alternative.

**AC3 — Independent native-memory acquisition.** Controller reads target-owned resource populations, provenance and filter outcomes at real execution stops; independently verified against synthetic ground truth. Mock-only demonstrations fail this criterion.

**AC4 — Identity, coherence and loss.** Process/thread/site/evaluation labels, refresh versus retained, resource-population provenance, bounds checks and loss classification are demonstrably correct within defined limits.

**AC5 — Durable evidence under failure.** Receipt written, read back and verified; positive post-capture target crash case and negative pre-ack failure case produce correct classifications.

**AC6 — Executed qualification.** Real disposable target tests cover the listed thread/event/memory/termination scenarios; failures and unsupported cases honestly recorded and corrected or made explicit blockers. No unsupported retail safety claim.

**AC7 — Retail pilot handoff.** Concrete future run card with objective GO/NO-GO conditions, independent native information gained, remaining retail-specific engineering gates and the exact preflight/postflight hash-and-restore save policy; no retail execution.

**AC8 — Independent review and exact delivery.** Independent adversarial reviewer checks all ACs, challenges authenticity of foreign-process reading, race/breakpoint coverage and durability, verifies preservation and inspectable receipts, and approves the **exact final snapshot**. Provide complete and task-only forward/reverse verified unified diffs, manifests/inclusions/exclusions, hashes, command/result ledger, and an explicit final disposition. Do not stage, commit or push.

## Reporting and handoff

Create a bounded experiment directory following project conventions with: report, architecture/native-to-synthetic mapping, reproducible build/run guide, qualification matrix with actual outcomes, receipt examples or references, preservation verification, final review and first retail pilot run card. Keep executable binaries, logs, raw memory dumps, screenshots, saves, large receipts and third-party/proprietary artifacts in appropriate ignored local evidence paths; authored code and small synthetic fixtures may be versioned according to repo standards. Maintain original failures in the audit history rather than rewriting them away. No premature claim that a synthetic controller is production-safe, that a UI filter is the vein generator, or that the IL/Iron contradiction has been resolved.

Suggested eventual commit message (maintainer only): `feat(research): implement synthetic native resource oracle collector`.
