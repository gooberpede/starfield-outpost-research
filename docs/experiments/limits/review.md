# L1 completion and review package

2026-10-19, Australia/Sydney. SOR-EXP-0051 / SOR-EV-0059.
[Original brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_L1_numerical_perk_limits.md`),
[frozen plan](plan.md), [answer/matrix](report.md), [native chain](native.md),
[saved coverage](saves.md). No criterion was amended.

| Original mandatory criterion | Implementer result | Primary evidence and limit |
|---|---|---|
| 1. Answer-first exact limits matrix | PASS | report.md; all nine physical recipe-global groups, deployment and environmental rules; uncertain current state and availability explicit |
| 2. Outpost count admission/skills | PASS | native.md; n003–011, player PRPS 8, actual PEX 12/16/20/24; effective remaining AV, entry/confirmation and accepted-action -1/removal +1; no atomic low-level recheck claim |
| 3. Regular/inter-system cargo count/modifiers | PASS | Both COBJ JNAM identities, stage 701 PEX and installed cargo-specific VMAD 3, shared count/card/status/action chain; 53 supported saved pad roots |
| 4. Turret construction categories/modifiers | PASS | Seven shared-global recipes, native G chain, full named threshold source census; two actual saved turret actors with explicit owner-join gap |
| 5. Bounded other-limits census, crew/robot reuse | PASS | All 3,009 COBJ, 576 name candidates, 51 JNAM; recipes.csv/categories.csv; CR1/R1 reused; scope excludes a claim that every candidate is ordinarily playable |
| 6. Planetary Habitation and L3 boundary | PASS | Actual scanner -> installed DFOB/CNDF -> nested four groups -> BodyHasKeyword/GetPerkRank; resolved body/default keyword inputs, environmental and local dispatch separated |
| 7. Saved interpretation/examples/registers/roadmap | PASS | Six freshly scanned saves, positive/negative population contrasts, 76 physical limited-root checks, 18 saved-body/default environment rows, functions/sources, durable L1/L2/L3 decisions/indexes |
| 8. Verification/protection/diffs/independent ACCEPT | Technical checks PASS; independent result controls accepted completion | verification-second.json: 1,510 checks, 623 physical ESM records, 76 Save52 limited roots; package-review01.json and preservation-review01.json; actual independent verdict retained separately below |

Scientific outcome: proposed **STRONG ordinary causal STATIC explanation** with
scoped SAVE corroboration. The complete physical COBJ/JNAM census is a bounded
definition result, not complete playable-object or save membership enumeration.
Loaded allowance, actual same-frame refresh, historical perk ranks, universal
destroy/disable cleanup, exceptional scripted over-limit load behaviour and safe
integration remain unmeasured. The positive native model does not depend on
inventing a mandatory serialized limit field. Task completion, scientific
confidence, runtime validation, publication and integration are separate.

Engineering/integrity: executed correspondence checks, source pins, scratch
cleanup, both-drive guard and exact patch reconstruction. No target was launched;
game survival/restoration is not applicable. Existing game/save/configuration,
persistent Ghidra content and HEAD/index must match baseline. Ordinary Ghidra
read-only housekeeping metadata is not disguised as source alteration. No new
third-party code, licence basis, download, outside contact or disclosure occurred.
Owned methods use SOR-P-0002 with source hashes; existing Bethesda/tool credits apply.

## Retained failures and corrections

- Some initial combined required-reading output was truncated. Focused policy,
  prior mechanism and source reads followed. Guessed research helper/document
  paths, a `form_id` versus `formid` diagnostic and an rg option typo failed;
  they are locator mistakes, not scientific negative evidence.
- The first player-property diagnostic assumed 8-byte PRPS stride and failed at
  the end of its 300-byte payload. The verified 12-byte entries correctly locate
  OutpostMaxDeployed 8 at payload+90. No original bytes were changed.
- Native request 013 contained an invalid exploratory `refall:144bca?0` selector;
  null-address handling failed and the first owned read-only worker exited.
  Its partial TSV, error log and FAILED done receipt are preserved. Earlier
  guessed description addresses had zero xrefs and were not used as findings.
  Correct PE/string mapping and bounded actual command registration windows
  supplied the later evidence. A new owned worker completed requests 014–020;
  no game process was touched. A guessed non-entry `140e47350` returned
  NO_FUNCTION_AT; no conclusion relies on it.
- First verification stopped at an over-specific decompiler text predicate:
  expected `longlong *` where the actual cast is `longlong **` at PNDT+1c8.
  The condition mechanism was unchanged. Corrected verification-second.json
  passes all 1,510 assertions; the original diagnostic is retained locally.
- The R1 actor-link reader reaches unsupported leading E6 in the two real
  turrets. No byte scan skips to a later apparent 4C. The saved owner join stays
  OPEN. Player E7/96 similarly prevents a claimed exact saved effective AV.
- Some native exports have instruction/decompilation caps or type warnings;
  functions.csv reports them. Exact selected instruction windows ground the
  deployment mutations that lie beyond the large handler's initial listing cap.
- The final worker was stopped by its sentinel and its recorded PID is absent.
  Detached launch does not retain a numeric exit code, and the log has no final
  processing receipt. Used successful request receipts/content and persistent
  database hashes are independently checked; process absence is not exit-0 proof.

## Review artifacts and independent disposition

Local root: `.local-work/l1-limits/`. Review diffs:
`.local-work/diffs/l1-limits-review01-task-only.diff` and
`.local-work/diffs/l1-limits-review01-complete.diff`.
The supplied initially untracked L1 brief is preserved unchanged, included in
complete and excluded from task-only. No other initial changes existed.

`package-review01.json` binds exact changed/untracked authored-text hashes,
status, inclusion/exclusions, UTF-8/no-BOM/LF, whitespace and internal links.
Both patches must reconstruct exact bytes forward/reverse in disposable .local-work/review-patches
trees and reverse-check against the actual tree. No staging or workspace apply
is used. Raw/native/save/database payloads remain excluded/local. Source ledger
pins the original protection baseline, source methods and primary exports;
package manifests bind the final authored tree independently.

The independent reviewer follows [the repository procedure](../../reviewers/research-completion-reviewer.md)
against the original brief, primary receipts, patches and actual tree. Its actual
verbatim decision is retained as `.local-work/l1-limits/independent-review01.md`
(or a subsequent numbered re-review after REWORK). This report does not assign
its own ACCEPT. Accepted completion requires the actual independent ACCEPT and
unchanged reviewed snapshot; missing review remains NOT REVIEWED. Reviewer
acceptance supplies no staging, commit, push, live, publication or integration
authority. The maintainer's critical integration review remains required.
