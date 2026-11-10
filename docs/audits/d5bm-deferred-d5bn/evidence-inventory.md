# Evidence inventory and custody

The [machine-readable inventory](inventory.json) gives the entry Git
identity, current D5BM source pins, the exact r3 review and permits,
and five records for each started attempt. Paths identify local files
relative to the repository. The streams, staged sources and protected
path inventory remain local.

| Evidence | Locator and classification |
| --- | --- |
| Current and reviewed bytes | The 23 D5BM worktree files match the frozen r3 manifest at `.local-work/d5bm/correction-delivery-r3/manifest.json`. The exact independent return is `correction-admission-review-r3.md` in the same D5BM root. The manifest records earlier review and patch identities. |
| Normal, pending and missing peer | `.local-work/d5bm/admission-attempts/` contains `r3-pump-normal03`, `r3-pump-pending01` and `r3-pump-missing01`. Each retains `admission.json`, `owner.json`, `stdout.json`, `stderr.txt`, `postflight.json` and seven exact source members. The admission argv, permit/source and runtime identities, PID/token join, streams and postflight all match. Exits in execution order are 0, 1 and 0. |
| Pre-child normal refusals | `r3-pump-normal01` and `r3-pump-normal02` produced no attempt directory or child receipt. The session reported `Reviewed CPython runtime differs: vcruntime140.dll` then `Reviewed CPython runtime differs: DLLs/_bz2.pyd`. The actual JSON keys were case sensitive. The original, intermediate and corrected `r3-review-pump*.json` records and `correction-ledger.md` remain local. No standalone error stream files are known for these refusals. |
| Unrun r3 controls | The `fault` and `tags` cases have source and static review, plus an applicable permit. There is no corresponding attempt directory, child identity or native output. The shared host also has no admitted execution. |
| Earlier native D5BM | See the continuation checkpoint under Source locators below. The local `resume/` tree retains the original server, pool and file receipts, their exports, and earlier refusals and access violation. `reconcile-20261110.stdout.json` records the earlier identity checks. |
| Original and staged assets | The D5BL copy manifest names each original and staged variant independently. The D5AS and D5BI original candidate ZIPs match their retained copies and have readable members. D5AS canonical geometry bodies and D5BI projected N2 event records retain their distinct provenance. Access and hosting remain held. |
| Protected inputs | Historical `.local-work/d5bm/postflight.json` enumerates 18 exact protected and host files. The r3 supervisor bound that inventory and each attempt rechecked all 18. D5BN relies on those historic postflights for the run-time preservation claim. |
| Missing or unknown | Pending stdout is an authentic empty file. No separate event trace identifies which part of marker verification failed. D5BL's exact-final D5BJ receipt search remains NOT LOCATED. The current incident trigger and feedback outcome have no verified record. |

## Frozen briefs and exact source

- Frozen contract and closure authority under `docs/implementation-briefs/`:
  `CODEX_BRIEF_SOR_RG2_D5BM_Native_Completion_to_Density_Eligibility_Qualification.md`
  and `CODEX_BRIEF_SOR_RG2_D5BN_D5BM_Deferral_Closure_and_Resumption_Dossier.md`.
- Ownership, source and prior run reconciliation under
  `docs/audits/d5bm-completion-eligibility/`, especially
  `admission-corrections.md`, `contract.md` and `continuation-2026-11-10.md`.
- The exact gate, probe, tags and supervisor under
  `research/resource-retained-population/`, named
  `d5bm_pump_gate.py`, `d5bm_pump_probe.py`, `d5bm_tags.py` and
  `d5bm_admit_component.ps1`. Match the [source pins](inventory.json).
  For the three executed snapshots, start in each attempt's `source/`.

These locators refer to the full local checkout and private copy.
The proposed documentation WIP keeps the historical fixture files separate.

## Recheck and local copy

From the repository root, `python -I -S -B docs/audits/d5bm-deferred-d5bn/inventory.py`
reads metadata, hashes bytes, checks retained source and stream joins, and
verifies the D5BL original/copy set and candidate archive members. It uses
the standard library and read-only Git commands. It does not import or
run any fixture. With `--full`, keep the expanded ignored-file index in
`.local-work/d5bn/`. The entry full index covers all 44,233 files in
the D5BM scratch tree, totaling 1,132,479,415 bytes. It includes nested baseline exports, historical
reviews and run snapshots. A missing or mismatched indispensable file refuses
with a diagnostic. The old inventories and working copies stay intact.

D5BN preserved a scoped private copy of 77 files totaling 1,355,174
bytes. It includes the latest attempt records,
their staged sources, the r3 review and permits, and the exact
D5BM working files. The local `.local-work/d5bn/custody.json` identifies
each original and copy member. All 18 protected files also matched
their retained sizes and hashes in the read-only current check.
The 360-file, 35,770,957-byte D5BL
copy was reverified against its source and destination pins. These
are same-volume working copies. They do not protect against disk
loss or common deletion. D5AW allows disposal of `.local-work/`
after publication. A public reader route must survive its removal.
[D5BL custody](../d5bj-preservation-d5bl/inventory-and-backup.md) ·
[D5AW disposition](../deferred-work-d5aw/README.md)
