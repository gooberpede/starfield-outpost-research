# Codex follow-up amendment — transient-save protection for RG2-C2B

**Project:** `D:\Projects\starfield-outpost-research`  
**Scope:** Narrow operational correction to the committed RG2-C2B Phase A save protection/preflight and Phase B run card. **No Carinae live test is authorized by this amendment.**

## Purpose and governing rule

Our research does not use Starfield **exitsaves** or **autosaves** as test inputs. Starfield ordinarily creates/replaces exitsaves when the game closes. Their churn must **not** cause preflight or postflight failure, trigger restoration, or block Phase B authorization. Conversely, user-designated research saves (including Save52 and named controlled saves), protected manual saves and their independently verified backups remain subject to strict preservation.

Implement a consistent, prospective policy across save enumeration, admission, baseline comparisons, protected-input manifests and postflight checks. Classify by **reliably identified save kind / explicit designation**, not fragile filename substring matches. Ambiguous or unclassified saves must not be silently excluded: fail closed or require a documented maintainer classification. A save expressly designated as research evidence remains protected regardless of its nominal save kind; do not discard or silently reclassify historical evidence.

## Required changes

1. **Durable policy:** Update the relevant permissions/workflow/save-protection documentation with three explicit classes: (a) protected designated research and manual saves, (b) transient exitsaves/autosaves excluded from preservation/equality gates, and (c) ambiguous/unclassified saves requiring qualification. State that quicksaves are **not** automatically excluded and that a later user-designated transient save becomes protected prospectively.
2. **Implementation:** Identify and amend all relevant code paths, including `preflight.py`, `protection.py`, save-corpus admission and postflight comparison. Ensure transient files are excluded consistently from strict protected-file hash/absence/addition checks; an unchanged count of all saves is **not** a sufficient check. Keep transient creation/replacement/removal visible in an optional diagnostic inventory, not a failure. Protect backup records and verify protected-save backup hashes, names/identities and restoration readiness as before. Do not weaken unrelated EXE, ESM, installed-definition, configuration, source-evidence, Steam Cloud or Git integrity checks.
3. **Historical reconciliation:** Preserve existing historical manifests, hashes and the observed exitsave rotation as immutable records. Explain the earlier discrepancy under the new policy; do **not** rewrite old baseline data, erase the failure history, rename files, alter live saves/backups or quietly refresh expected hashes.
4. **Regression qualification:** Cover normal exitsave creation, removal, replacement and rotation; autosave churn; protected Save52 modification and removal; corrupted/missing protected backup; new/changed protected manual save; quicksave treatment; ambiguous names/kinds; explicitly protected nominal exitsave/autosave; mixed transient and protected changes. Verify both preflight and postflight and consistent handling in the broader protected-input audit. A change to protected evidence must still fail even when transient churn occurs simultaneously.
5. **Phase B card:** Update the existing RG2-C2B run card and preflight commands to apply the revised policy, preserving the exact scientific scope, one-session limitations, approval requirement, explicit stop conditions and postflight procedure. A successful amended preflight **does not itself authorize launching or attaching to Starfield**.
6. **Finalization and delivery:** Follow `docs/EDITORIAL_STANDARD.md` and the current research completion protocol: automated changed-text screening, manual editorial reading, independent critical review of code/tests/semantics and the **exact final snapshot**, with scoped delta review for any post-acceptance edits. Supply test commands/results, protected-input integrity records, changed/new-file manifest and verified complete/task-only diffs. Do not stage, commit or push.

## Acceptance conditions

- Transient exitsave/autosave churn is nonblocking **without** suppressing protected-save integrity failures.
- Classification is deterministic, auditable and fail-closed for ambiguous cases; explicit evidence designation takes precedence.
- The previously recorded exitsave discrepancy is explained and no longer blocks an otherwise valid prospective admission.
- All required regression cases pass, and the independent reviewer signs off on the exact delivered snapshot.
- Original saves, backups, frozen predictions and native evidence remain unchanged; **no live game execution**.

**Return:** a concise summary of revised classification, code paths, regression results, preserved prior discrepancy, updated run card and review decision. Phase B remains **PENDING MAINTAINER APPROVAL**.
