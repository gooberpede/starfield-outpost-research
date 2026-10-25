# PROPOSED / NOT EFFECTIVE: preservation workflow amendment

No policy amendment or activation is performed by this document. The
[report](report.md) returns AC4 FAIL and REWORK. The maintainer must separately
approve any adoption, scope/guarantee change and controlling-policy amendments.
The current rules, broad helpers and historical verdicts remain in force.

## Proposed exact text changes

The following is a reviewable policy diff, **not an applied patch**. Its
conditional entry point must stay unavailable unless the activation prerequisites
below have passed. It does not approve a reduced corruption-detection guarantee.

```diff
diff --git a/WORKFLOW.md b/WORKFLOW.md
--- a/WORKFLOW.md
+++ b/WORKFLOW.md
@@
 ## Scientific experiment continuation and health
+
+For an expressly approved ordinary offline verification scope, distinguish
+fresh scientific-input verification, critical-original/content protection and
+historical-store maintenance. Verify every actual scientific input against an
+independently bound expected digest at intake and applicable reuse. This applies
+equally to tracked, untracked and ignored inputs. A prior audit PASS is never
+an expected identity or proof of current bytes.
+
+Historical skipping is unavailable unless an independently reviewed storage
+contract preserves the approved detection guarantee, authentic baseline/root
+identity, namespace coverage and change-history continuity. Missing or changed
+trust, a suspected integrity incident, migration or an explicit release gate
+requires a full historical re-audit. Journal-only quietness does not establish
+current readable-byte equality. Without qualified equivalent protection, use
+the existing broad fallback. No file is reclassified from its prior status.
+
+For game/save-handling or other high-risk work, retain full protected-save and
+backup before/after checks, installed input identities, namespace/reparse guards,
+restoration readiness and both-drive free-space guards. Do not apply an offline
+historical optimization to live operation by inference.
diff --git a/docs/RESEARCH_EXECUTION_PROTOCOL.md b/docs/RESEARCH_EXECUTION_PROTOCOL.md
--- a/docs/RESEARCH_EXECUTION_PROTOCOL.md
+++ b/docs/RESEARCH_EXECUTION_PROTOCOL.md
@@
 ## Completion accounting and evidence
+
+An approved preservation receipt must separately report selected scientific
+inputs, critical protection, historical-store checks and trust prerequisites.
+Measure enumeration, unique files, payload/control bytes, hash calls, elapsed
+time and setup amortization; preserve UNKNOWN physical I/O and coverage gaps.
+A skipped historical payload check cannot be reported as a current-byte PASS.
+Failure or interrupted verification emits no success/admission receipt, does
+not refresh expected hashes, and requires explicit full fallback or recovery.
diff --git a/docs/SAVE_PROTECTION.md b/docs/SAVE_PROTECTION.md
--- a/docs/SAVE_PROTECTION.md
+++ b/docs/SAVE_PROTECTION.md
@@
 ## Namespace and evidence boundaries
+
+Offline historical-verification proposals do not amend these active-save,
+historical-original, independent-backup or installed-content protections.
+Task-used save/native bytes always receive explicit expected-identity checks.
+A historical change-journal receipt is not protected-save backup readiness,
+permission to restore, or authorization to launch, attach or alter a save.
```

These context snippets specify insertion points and complete added text. They
are not intended for unattended `git apply` or automatic activation. A future
adoption package must use the then-current file context and exact reviewed
implementation; the current prototype is not that implementation.

## Required tool contract before adoption

1. An admission wrapper accepts an approved scope identifier, independently
   bound expected manifest digest, original HEAD/index, exact task input paths
   and protected roots. It refuses unknown classes, reparse ancestors, changed
   trust roots, missing backups or missing disk queries.
2. Default and high-risk modes use existing full protection. A conditional
   historical mode is unavailable until a separate qualified storage contract
   establishes the agreed detection guarantee. No automatic “fast” switch follows
   from file age, suffix, size/mtime or an earlier PASS.
3. Receipt schema separates selected-byte PASS, namespace state, historical
   readable-byte coverage, journal continuity and storage trust. Any failed stage
   prevents an admission result. Recovery never overwrites an original or
   rewrites an old verdict.
4. Preserve the broad scripts at their original versions and keep a full scanner
   available. A future ordinary full-pass consolidation may reduce duplicate
   hashes, but must not use current observations as replacement expected pins.

The prototype supplies disposable measurement and detection functions only.
It intentionally does not implement or install that project-wide wrapper.

## Migration, triggering and rollback

First review the detection contract: must every historical readable byte be
reverified on every ordinary task, or can separately verified immutable storage
supply comparable protection? The current journal-only design does not resolve
that choice. Any decision to tolerate delayed detection is a material contract
change, not approval of this assignment's AC4.

Before a future migration, inventory and classify scope with unresolved classes
held strict. Verify original expected hashes and namespaces using the old method;
preserve the actual methods, failures and receipts. Establish the authentic
out-of-tree root and storage integrity independently. No historical data need be
deleted, normalized, repacked or altered; any required storage migration needs
its own approved inputs, writes, copy verification and rollback boundary.

Shadow the candidate beside the old verifier on controlled copies and compare
all detection duties, including concurrent changes and scanner failure. Re-run
the frozen efficiency contract on representative data, charge initial setup and
periodic/full recovery, and obtain independent review of the exact final version.
Only a separate maintainer decision activates new controlling text or scripts.

On journal gap/reset, baseline identity change, unsupported records, inaccessible
storage, suspected corruption, archive migration, protection incident or explicit
release/publication gate, halt admission and retain diagnostics. Use full
historical verification against the original independently bound expectations;
do not bless changed bytes as a new baseline. An authorized incident review
decides recovery or a new baseline. Ordinary new task outputs outside protected
roots do not by themselves trigger historical re-audit.

Rollback disables the new admission entry point and selects the unchanged old
full verification path. Keep both old and candidate receipts and the previous
trust root; no data restoration or overwrite follows automatically. Because
nothing is activated here, current rollback is simply to continue the existing
rules. No installation, live action, publication, staging, commit or push is part
of this proposal.
