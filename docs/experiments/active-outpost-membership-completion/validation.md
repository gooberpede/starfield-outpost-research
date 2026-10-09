# SOR-EXP-0010 validation and review inventory

2026-10-09. SOR-EV-0016. [Report](../active-outpost-membership-completion.md). This is a partial handoff for critical review, not approval to integrate, publish or expand scope. User-deferred quest-state work and incomplete offline reconstruction remain explicit.

## Actual checks and their limits

- Nine new synthetic methods pass in `test_outpost_membership.py`: reference tags/one-based bounds, cases4–7, omitted flags, disabled/deleted distinction, transform-conditioned offsets and self-queue rejection, promoted-player-reference ownership decoy, buffer-version/empty-array behavior, extra boundary/unknown stops, and ESM subrecord/XXXX bounds. Six existing `test_outpost_record_framing.py` methods also pass. These tests establish decoder behavior, not runtime membership semantics. No third-party fixture or dependency is used.
- Fresh corpus challenge: 412 labels / 389 source hashes; 409 exact R3 closures / 48,863,625 records; three decoded-size limits (HIST-0252/0256/0257). 1,804 case5 diagnostics plus 21 conditional case6 leads. No IsDeleted-set diagnostic; 21 unknown flags. All 412 semantic results INDETERMINATE. Selected ledgers contain 412 manifest rows, 62 exact record rows and four definition rows.
- Frozen feature extraction precedes per-file old-observation comparison. All 409 comparable inline counts match the prior frozen observation ledger; new R1/definition leads add coverage rather than establish active false negatives. Only 24 labels have independent operator/network ground truth (three zero, 20 one, one network17); 388 are unlabelled. Existing familiarity prevents a fully blind claim. The semantic classifier abstains on every file: no claimed semantic sensitivity/specificity.
- Installed definition reader completes two bounded header/group walks per selected ESM, with source SHA-256/stat identity checks before/after. ACTI EDID prefix selection does not cover arbitrary keyword-bearing definitions, plugin overrides or historical content snapshots. Payload decompression and subrecord bounds are checked; a matching output is not evidence of ownership.
- Ghidra runs use existing analysis only with `-readOnly -noanalysis`, no project edits or imports. The final bounded instruction search records 748 exact non-stack `+0x298` operand matches inside `[0x140001000,0x143400000)` and `CANCELLED false`, with no1000-hit cap. Matching offsets do not establish the same structure or exhaustive semantics. One global-reference query hits the existing24-xref cap; the exclusion-global query returns one xref. These are bounded discovery results. No full native writer/registration/keyword proof follows.
- Exact input hashes are in [manifest.csv](manifest.csv); definition hashes are in [definitions.csv](definitions.csv). Decoded offsets and omission states are in [records.csv](records.csv). Full private source/copy locators, timestamps and every before/after identity are local. No raw save, decoded payload, native code or substantial proprietary script data is included.

## Preservation, failed attempts and deviations

The ignored bundle `.local-work/membership-completion/` contains `challenge-01/` and the final `challenge-final/`, definition receipts, hashed exploratory scripts, copy archives, quest/PEX leads and a contemporaneous `ghidra-before.json` / final `ghidra-after.json`. Fifteen existing Ghidra-project files match by size and SHA-256. Two installed ESMs, the BA2 and ten selected local PEX copies match their recorded identities at final static verification. Settings/cache/log writes are outside the analysis database and disclosed. Source-save original/copy identities are checked individually before/after each challenge read; access-time behavior is uncontrolled. The original donor archive is not extracted or used again by this task; donor members remain subject to SOR-P-0003's local-only limits.

**Copy-handling deviation:** early ignored `probe.py` imported the prior `specs()` helper, whose HIST copy locator is the original path. It therefore parsed selected original historical saves instead of verified ignored copies. No write was made; subsequent challenge source hashes match the frozen manifests. This does not retroactively make the probe copy-only. The corpus runner locates archived copies by hash and creates an exclusive missing copy before parsing; source reads are restricted to copying/integrity. Missing historical copies add approximately2.36GB, guarded on C/D. The user was informed of the deviation. No original save was modified or deleted.

**Provenance repair:** the first complete challenge began before the final runner's tool-identity receipt/1800s guard was added. Those checks are not attributed to that first run. During that run a display-only coverage list was extended to mention already-supported empty extras0x4c/0x80; semantic code was unchanged. A fresh full final run uses the completed scripts, captures tool/definition/runtime identities before/after and compares all candidate/state measurements against the earlier frozen features. Final public ledgers must match that final run. Initial exploratory ESM probes reused/overwrote their own local output; reproducible `definitions-01` is the retained exclusive definition authority, not the overwritten probe output.

**Preserved failures:** direct Java startup without the configured VM arguments failed; the existing wrapper recovered it. Unquoted numeric addresses containing `e` were converted by PowerShell and caused partial/error exports in static06/07; correctly quoted static08 recovered the intended targets. A concurrent project-open attempt static11 hit a lock and produced no successful export; static12 reran sequentially. The initial PEX string probe stopped on an incorrect identifier spelling, corrected in a separate run; the attempted general VMAD property reader stopped on unsupported type17 and was abandoned when quest decoding was deferred. `NO_FUNCTION_AT 140f31a00` in static14 is a missed exact function address, not absence of code. No failed/capped scan is used as negative semantic evidence. Native exports and logs remain ignored under `.local-work/recon/membership-*`.

## Tool and source identity receipts

`challenge-final/tools.json` records the installed Python executable, definitions JSON, all project Python script identities and command line before/after. `static-preservation.json` records installed content hashes, native export/log hashes and exploratory script identities; the unchanged pinned executable hash is embedded in the Ghidra exports. SOR-S-0127/0128 credit installed Bethesda evidence; SOR-S-0124 credits project methods; SOR-S-0113 credits separately installed Python/stdlib; existing Ghidra/JDK and donor credits remain. No new install, copied parser, outside consultation/contact, upstream issue/PR, permission correspondence or external disclosure.

## Changed-file inventory

New authored files:

- `docs/experiments/active-outpost-membership-completion.md`
- `docs/experiments/active-outpost-membership-completion/manifest.csv`
- `docs/experiments/active-outpost-membership-completion/records.csv`
- `docs/experiments/active-outpost-membership-completion/definitions.csv`
- `docs/experiments/active-outpost-membership-completion/validation.md`
- `save-analysis/scripts/outpost_membership.py`
- `save-analysis/scripts/inspect_outpost_definitions.py`
- `save-analysis/scripts/challenge_outpost_membership.py`
- `save-analysis/scripts/test_outpost_membership.py`
- `ghidra/scripts/OutpostMembershipRefs.java`

The supplied, initially untracked `docs/implementation-briefs/CODEX_RESEARCH_BRIEF_active_outpost_membership_completion.md` is retained unchanged and included in the review diff; it was not authored by this task.

Modified existing files: `CREDITS.md`; `docs/DECISIONS.md`; `docs/PROVENANCE.md`; `docs/RESEARCH_STATE.md`; `docs/SOURCES.md`; `docs/experiments/README.md`; `docs/experiments/evidence/README.md`; `docs/function-register.md`; `docs/hypotheses.md`; `docs/implementation-briefs/README.md`; `docs/known-facts.md`; `docs/state-register.md`; `docs/subsystems/initial-map.md`; `ghidra/scripts/Invoke-OutpostRecon.ps1`; `ghidra/scripts/README.md`; `save-analysis/scripts/README.md`.

The wrapper change only permits selecting the new original read-only reader. Other modifications record the new evidence, partial state, IsDeleted priority, maintainer correction, edge-case deferral and reproducible interfaces. Existing historical findings are preserved.

## Final repository checks and review artifact

The final repository-check receipt and complete binary-capable review patch are retained locally under `.local-work/membership-completion/review/`. The patch includes tracked changes plus every non-ignored new file, including the unchanged supplied brief; no staging is used. `files.json` supplies actual file/status/size/hash identities, including the patch hash in `checks.json`. No patch self-hash is embedded into a tracked file. Internal-link checking covers relative file targets in all changed Markdown; anchor correctness is separately reviewed for the new cross-report link, not a general Markdown renderer audit. `git diff --check` plus new-file whitespace checks and tracked raw-artifact inventory are required to pass. The staged diff remains empty; HEAD remains unchanged. Final status is preserved verbatim in the local package. No commit, push, remote change, branch publication, live experiment or publication has occurred.

Remaining unknowns: inherited form types, complete R1 created-reference/template mapping, save-era content/overrides, ExtraFlags buffer version, nonempty extras/ExtraWorkshop, resolved exclusion keyword/property and complete registration/ownership restoration; the user has deferred faction quest-status decoding. These prevent complete active-player classification. No approval or semantic promotion is implied by this handoff.
