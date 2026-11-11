# D5BT — Save29 Electrical Graph and Display Component Reader Qualification

**Project:** `starfield-outpost-research` · **Type:** bounded engineering and original-evidence verification · **Roadmap:** 5B-1 · **Authority:** maintainer approval in the conversation commissioning this brief · **Publication:** NOT READY / NOT CLEARED

## 1. Purpose and governing decisions

Remove the **two specific portable-reader blockers** identified and independently accepted in D5BR. Deliver independently qualified, reusable *explicit-input, read-only* procedures for (A) the Save29 ordered electrical graph and (B) the HIST-0021 displayed-helmet component relationship. Test the procedures against **only** the exact, already-selected archive members, plus synthetic and bounded negative controls. Do not repeat the wider A1–A6 original-save verification or any scientific mechanism investigation.

The maintainer **expressly authorizes read-only access to the archived original saves necessary for this assignment**: D5BF CORE `B4-F054` (Save29) and D5BF ADDENDUM `B4-F067` (HIST-0021), obtained from the already selected, hash-pinned archives and/or their protected, identity-verified copies. This permission includes narrowly necessary, existing project-owned local reader components and approved provenance receipts after exact source-identity checking. It does **not** authorize reading other archive members for analysis, harvesting active-save directories, modifying saves, transferring or publishing proprietary bytes, accessing game-process memory, running native game code, or broadening the original corpus. If a named prerequisite cannot be located and verified, document the exact barrier; do not substitute another save. The historic helper `authority_probe.py` may be recovered *only* if its exact provenance and safe read/write behavior can be qualified; recovery is not a prerequisite if a new bounded adapter passes.

**Prior decisions:** D5BR accepted 54 of 68 selected evidence routes as READY FOR B6 at the agreed tier, 12 as READY FOR VERIFICATION and these two as BLOCKED. D5BT addresses **only** `S-P1-S29-ORIGINAL` and `S-SD1-H21`, and their immediate method dependencies. Scientific findings, D5BP/D5BQ evidence tiers, D5BD/D5BS and all historical/release restrictions remain unchanged.

## 2. Mandatory source reading and evidence hierarchy

Apply `AGENTS.md`, `WORKFLOW.md`, `THIRD_PARTY_POLICY.md`, `docs/CHARTER.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, `docs/SAVE_PROTECTION.md`, `docs/PUBLICATION.md`, and the B0/B3/B4/B5 release and method contracts. Retrieve and **understand the complete relevant source content by final acceptance**, including truncated outputs; record how it informed decisions. Reading order alone is not an acceptance criterion.

Specifically read:

- `docs/audits/evidence-readiness-d5br/{README.md,readiness.json,execution-plan.md,exceptions.md,review.md}` (Stage 0; A3; A5), and their exact source/reader/member pins;
- `docs/audits/release-assets-d5bf/{README.md,release-assets.json}` and selected F1 member identities; `docs/audits/publication-claims-d5bg/{claims.json,evidence-edges.json,actions.json}`; `docs/audits/publication-decisions-d5bq/README.md`;
- `docs/experiments/power/{save29-authority.md,save29-authority-review.md,save29-test-plan.md}` and relevant `research/p1-power`/`save-analysis` reader sources;
- `docs/experiments/containers-displays/{report.md,methods.md,review.md,sources.csv}` and existing owned `sd1-containers/components_sd1.py`, `extras_sd1.py`, their source precursors and B3-C0115/0124 dispositions; and
- `docs/audits/publication-readiness-b3/method-reproduction.md`, B4/F1 file dispositions and privacy policy, and the B5 creator safety results.

Original published research and review decisions control interpretation; D5BR selects the *verification route*, not a new scientific result. Source names in historical records may refer to ignored `.local-work/` files: locate and hash-check actual files before using them. No fabricated equivalence from similar filenames.

## 3. Controlling questions and required outputs

### D5BT-Q1 — Safe, exact evidence staging

Can the two named original archive members and all necessary owned reader components be supplied from verified provenance without accessing or altering any unselected original, active save, protected artifact or private evidence?

**Required:** Establish container/member identities (basename, member ID, size, SHA-256, compression/framing as applicable), input existence, selected header/build acceptance, Python/dependency versions, and expected read/write effects before real-data execution. Use separate, caller-owned, **exclusive** staging/output directories. Never extract whole archives merely to obtain these two members. Reject traversal/duplicate member names, unsupported archive codec, wrong bytes and selected-member ambiguity. Preserve private absolute paths only in ignored receipts, not publication text. Record original and staged hashes before and after. Reuse safe existing project-owned parsers; inspect imports and top-level effects, particularly historical active-save copy modes.

### D5BT-Q2 — Save29 electrical graph reader

Can a portable, explicit-input method reproduce the *saved* electrical component independently of the unavailable loose `authority_probe.py`?

**Required exact positive oracle, from `save29-authority.md`:** Select **four** typed REFR objects and their complete counted extras with no arbitrary byte-pattern search or winner-driven permutation:

| Role | Saved REFR FormID | Ordered `ExtraCB` targets / words | `Extra9C` word |
| --- | --- | --- | --- |
| Beacon | `ff022778` | `ff022841, ff022917, ff02294d` / `1,1,1` | `0x840` |
| Solar | `ff022841` | `ff022778` / `1` | `0x840` |
| Extractor #1 | `ff022917` | `ff022778` / `1` | `0x840` |
| Extractor #2 | `ff02294d` | `ff022778` / `1` | `0x800` |

Report, and independently challenge, the original **decoded-stream, half-open** REFR/CB/9C offset ranges from the accepted source. Verify selected bases and ordinary conditional calculation inputs using pinned definitions or the accepted separately attributed values: solar output **6**, each extractor demand **5**. The order predicts #1 eligible, #2 rejected under the declared native assumptions; swapping consumer order predicts #2. The *saved powered flag* must stay distinct from an actually observed post-load worker invocation. No three-load runtime replay, authoritatively settled power state, save writer, or new allocation rule is claimed.

Reader contract: Reuse `workshop_inventory.linked_prefix`'s ExtraBC consumption grammar and independently compare the relevant counted-extra end/reference cursor with `saved_instances.extra_view` or an equivalently distinct check; reproduce the source's original positive-subset failure and successful bounded extension rather than hiding a parser gap. Preserve the distinctions between a record's counted-extra termination, whole-record bounds and reference queue exhaustion. Validate full framing in the supported input domain. Reject malformed/truncated BC/CB, invalid count/length/reference resolution, wrong record type, unsupported save header, inconsistent graph or flags, and synthetic order/word mutations. The independent oracle must not simply re-read the implementer's JSON output.

### D5BT-Q3 — HIST-0021 displayed-item reader

Can a portable, explicit-input method inspect the selected displayed helmet **without treating ordinary inventory stock as the entire display state**?

**Required:** Validate the exact ADDENDUM `B4-F067` original. Inspect existing hash-pinned project-owned component and extra readers, including the `pending-dialogue` typed branch and strict section closure. Supply a narrowly scoped portable implementation with a documented allowed component/extra subset. Independently reproduce and locate the **43-section framing/closure where applicable**, fixture identity and ownership, **zero normal inventory count**, positive displayed-helmet slot, the separately serialized item reference and reverse/backlink joins, plus the distinct backpack control and explicit unsupported extra cases. Take concrete expected identities, offsets and item tokens from the accepted SD1 source, receipts and D5BR route record; **do not invent expected field values from this brief**. Preserve the distinctions between typed component ID, section index, raw save token, FormID and decoded-stream offset. An unknown/unsupported variant must fail closed, not be converted to an absent display item.

B3 previously deferred the two local component sources as *public reproducibility inputs*. D5BT may review, adapt and promote the minimal **maintainer-owned** capability only after exact source/provenance and effects checks. Do not silently include unpublished raw component bodies, private paths, Bethesda payloads or broad legacy tooling. The new reader should be executable with tracked approved source plus explicitly supplied lawful save bytes, or report an exact independently reviewed blocker if this cannot be made safe and portable.

### D5BT-Q4 — Qualification, durable integration and handoff

Do independently reviewed positive and negative tests demonstrate that both readers reproduce their *selected saved-state evidence tiers* and are suitable for the later coordinated A1–A6 verification?

Produce small documented reader entry points, supported input/header/schema contracts, deterministic machine-readable **selected-only** output (with separate human summary), strictly bounded effects, synthetic/negative tests and original-byte receipts for Q2/Q3. Provide reproducible clean-copy examples without hidden `.local-work/` dependencies; the actual input saves must be supplied explicitly and never checked into Git. Integrate code only into appropriate existing `research/`/`save-analysis/` locations, with concise durable D5BT audit docs and a follow-on D5BR crosswalk/status note where justified. Never change D5BG scientific statuses or mark first-release asset distribution as cleared solely on a local run. The two D5BR blocks may be recorded as **reader qualified locally / awaiting coordinated 5B original verification and B6**, not READY FOR PUBLICATION.

## 4. Execution boundaries and controls

**Permitted:** read exact `B4-F054` and `B4-F067` from approved archives/protected copies; hash/stream/decompress those selected members into isolated scratch, inspect and adapt verified maintainer-owned reader sources, execute local Python-only offline readers/tests against those copies, use pinned installed definitions *only if directly indispensable to the Save29 conditional definition check and separately justified under existing rights/preservation rules*, write new owned source/tests and compact documentation/receipts, perform Git read-only commands and isolated disposable patch reconstruction. The original read authority is the user's explicit D5BT authorization, not an implied general permission for other archive members.

**Prohibited:** launching or modifying Starfield, SFSE, Ghidra analysis, debugger or native code; scanning additional original saves or whole historical corpora; reading live/active saves; write-back to original archives or existing historical receipts; changing game, settings, registry, analysis databases or Git index/refs; unapproved third-party dependencies or downloads; uploading or externally disclosing evidence; altering scientific dispositions or granting publication, archive, release/tag or visibility authority. The HIST-0021 reader must not take a successful isolated byte parse as evidence of a rendered game state.

**Operational:** Preserve at least **40,000,000,000 caller-available bytes on C: and D:** before and during material writes; calculate bounded peak scratch size. Verify pre/post original, archive, selected dependency, project/index and output identities. Use `-I -B` or appropriately justified installed-Python isolation, assertions enabled, no implicit active-save discovery, exclusive output paths and explicit CLI arguments. For every error, preserve the original failed receipt before correction; a retry cannot overwrite it. Reject silent format fallback. Stop the affected branch on hash mismatch, unsupported build/header, unsafe path/effect, missing material, disk guard failure or unauthorized dependency. Diagnose and correct in-scope engineering failures under this same brief; escalate only genuine terminal authority/input/capability blockers with a smallest corrective proposal.

One optional **read-only specialist** may independently compare the historic parse contracts and narrow negative oracles. **At most one sub-agent active at a time**, confirmed terminated before starting the fresh independent reviewer. The **primary agent alone edits and executes the authorized tests**. No delegated native/game operation.

## 5. Deliverables and acceptance criteria

Deliver, under `docs/audits/reader-qualification-d5bt/` or a similarly explicit durable directory, an answer-first `README.md`, active `investigation-ledger.md`, `review.md`, exact input/reader control and provenance crosswalk, and independent test results. Put detailed paths and original output data only in ignored local receipts. Document a clear 5B-2 handoff showing the two readers' inputs, safe invocations, limits and whether further selected original verification is required. No new evidence ZIP or raw-save derivative is to be published. Deliver a *complete* patch (including the unchanged supplied brief) and *task-only* patch, file/hash/exclusion manifests, exact forward/reverse verification in disposable trees and status evidence; nothing staged, committed or pushed.

- **AC01:** Full relevant mandatory reading understood and applied; original authorization and all prohibitions upheld; active ledger maintained.
- **AC02:** Exact CORE F054 and ADDENDUM F067 container/member provenance, source identities, supported build/header and preservation verified; no unrelated saves read.
- **AC03:** Reader input/output/side-effect contracts are portable, explicit and fail closed; no active-save default or overwrite path.
- **AC04:** Save29 reader reproduces all four typed REFRs, ordered CB lists/words, 9C flags, original decoded ranges and reciprocal graph against original bytes.
- **AC05:** Save29 BC/extras/queue closure has an independently checked oracle; malformed, unsupported and ordering/word negative tests reject.
- **AC06:** Conditional power calculation (6 versus 5+5, swapped-order counterexample) is confirmed without elevating saved flags to historic runtime authority.
- **AC07:** HIST-0021 reader reproduces exact component closure, zero-stock/positive helmet slot and reciprocal joins, with separate backpack and unsupported-extra cases.
- **AC08:** HIST-0021 independent typed/framing and field controls reject truncation, wrong token, missing backlink, malformed section and unsupported variant; no game rendering claim.
- **AC09:** Reader source, transitive imports, approved local-component reuse, licenses, unavailable historical tools and lawful supplied-input requirements are documented; selected public method does not depend on unshipped scratch code.
- **AC10:** Exact pre/post originals and repository protection, error histories, environment and actual invocation/exit receipts prove the bounded execution; no unauthorized files or effects.
- **AC11:** Editorial reading, link/encoding checks, task/complete patch coverage, manifest hashes and byte-exact forward/reverse reconstruction pass; unchanged supplied brief preserved.
- **AC12:** Fresh, distinct, read-only independent reviewer receives original brief, active ledger, original positive/control receipts and all changed source/prose; challenges both parent Qs, missing alternatives, test independence, and exact final snapshot. Only `ACCEPT` with Q1–Q4 COMPLETE and AC01–AC12 PASS is completion. `REWORK` stays within D5BT; evidenced terminal `BLOCKED` requires `ESCALATE` and specific maintainer decision.

**Outcome separation:** scientific result = prior accepted power and SD1 findings unchanged; engineering result = local original-byte reader qualification; target survival = NOT APPLICABLE (no live process); publication = NOT READY / NOT CLEARED. No new release or native-execution permissions follow from successful D5BT.
