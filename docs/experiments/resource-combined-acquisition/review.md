# D5B qualification, preservation and review

2026-10-25, Australia/Sydney. [Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5B_combined_construction_mask_consumer_acquisition.md), [frozen contract](contract.md), [report](report.md), [native map](native.md), [proposed card](run-card.md), [source ledger](sources.csv).

**Phase A scientific scope is source-bound synthetic construction and separately bound current consumption. Native producer-to-consumer epoch and historical construction inputs remain UNKNOWN. Phase B has not been executed and is not authorized.** Independent review returned ACCEPT for scientific, engineering and editorial conformance on the exact review02 snapshot; the disposition and its limits are recorded below.

## Actual execution and reproducibility

Task raw/build/verification outputs are ignored and local under `.local-work/resource-combined-acquisition/`; inherited reruns also use the fresh directories listed below. The supplied untracked brief was the only initial worktree change. HEAD/index are protected and no staging, commit or push occurs. Installed tools are CPython 3.14.3, Windows debugging APIs, MSVC compiler 19.51.36256.0 and linker 14.51.36256.0; exact setup/source/binary hashes and tool output are in each build manifest/log.

The final build is `build15/`. Its manifest pins the complete authored source set and transitive inherited debugger/decoder/transport inputs. Both the retail controller and disposable fixture/controller are built; only the fixtures are executed in Phase A. `qualification13/` executes the required 37-case roster, with 316 independently readback-verified SRO1 samples. Its summary records the actual final receipt count.

Coverage includes differing initial Int2/geographic operands yielding masks 0 and 3 on the same source; conflicting invocations; construction without consumption; cached Workshop consumption; one fixture-only linked population; same-address lifetime replacement/reset; wrong Workshop/body/source/resource/transfer; nested/concurrent events; slot-switch gaps; unavailable context and partial pages; complete XYZ/width/bounds and corrupt arrays; crashes, pre-ACK target termination and durable evidence; STOP with 96 waiting threads; observed zero calls/empty transfer and refused final construction ACK. A nested producer that loses its rotating stages is PARTIAL, not an invented complete construction. Concurrent scheduling does not establish universal loss-free event coverage.

The fixture-only positive linkage relies on the pinned sole-writer path and stack lifetime, plus copied actual target witness, wrapper, source and geometry. Synthetic epoch words are compiled out of retail. Replacement/reset variants refuse the link; matching bytes/pointers alone are not a retail lifetime proof. Reducer defaults supply no synthetic proof. The [machine schema](../../../research/resource-combined-acquisition/receipt.schema.json) and [target contract](../../../research/resource-combined-acquisition/target.json) preserve these distinctions.

`checks04/` is the final comparator/operational verification root. It compares every fresh case against **both** unchanged D5A alternatives, tests corrupt/truncated controlled copies, exercises the shared actual operational pump on construction-only ACK STOP, combined-unlinked, cached-consumer and unrelated-source cases, and refuses a denied retail gate before any process query/attachment. All 44 final comparisons and operational/admission checks pass in `checks04/`; `checks01/`, `checks02/` and `checks03/` retain their earlier 44-check successful snapshots. Synthetic geometry/candidate ordering intentionally differs from the retail predictions; recorded mismatches are not fitted away. The operational pump receives no synthetic lifetime proof.

The inherited executions are actual reruns, not copied historical reports:

| Suite | Fresh local evidence | Cases |
|---|---|---:|
| C1C collector | `resource-oracle-collector/d5b-inherited01/qualification.json` | 19 |
| C1D retail adapter on fixtures | `resource-oracle-retail/d5b-inherited01/qualification.json` | 13 |
| C1E region ancestry | `resource-region-ancestry/d5b-inherited01/qualification.json` | 32 |
| C1G selection operands | `resource-selection-operands/d5b-inherited01/qualification.json` | 27 |
| D4 full selection context | `resource-selection-context/d5b-inherited01/qualification.json` | 34 |
| D4A repaired consumer/diagnostics | `resource-tungsten-acquisition/d5b-inherited01/summary.json` | 46 |
| C2B amended source-context build | `resource-carinae-source-context/d5b-qualification01/qualification.json` | 42 |
| D4B terminal retirement | `resource-combined-acquisition/inherited01/terminal/summary.json` | 12 |
| D4D ordered construction | `resource-owner-acquisition/d5b-qualification01/summary.json` | 25 |

These 250 inherited cases are disposable Windows targets. Intentional controller failures remain separate from harness PASS. The historical D4A `win32=31` timing is not asserted reproduced. The new combined STOP tests and inherited terminal controls establish no-late-rearm on the actual observed exits, not universal future retail safety.

`inherited01/geometry/` freshly executes all 17 active Save52 requests in both normalized and expanded representations and all ten exact native geometry controls. It accounts for all 19 cases and 46 associations. Ordered binary32 XYZ/width, native bounds, resource and callback agree for every control; Archimedes also checks source identity. The three differences relative to D3 are already inherited D4E Tungsten and D5 Uranium/Vanadium correspondences, not D5B reclassification. `checks04/frozen-d5a-equality.json` compares all 38 new prediction outputs semantically to the unchanged D5A originals. `legacy-regression01/` independently reruns all 34 frozen D2/D3 requests and the seven original controls in both representations with exact semantic equality and eight denied inference-read probes. Frozen predictions, source/case/screenshot bytes and original native captures remain unchanged.

Actual principal commands, from repository root, are:

```powershell
$d5bPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $d5bPython -B research/resource-combined-acquisition/audit.py before
& $d5bPython -B research/resource-combined-acquisition/build.py --name build15
& $d5bPython -B research/resource-combined-acquisition/qualify.py --build .local-work/resource-combined-acquisition/build15 --output .local-work/resource-combined-acquisition/qualification13
& $d5bPython -B research/resource-combined-acquisition/checks.py --qualification .local-work/resource-combined-acquisition/qualification13 --name checks04
& $d5bPython -B research/resource-combined-acquisition/inherited.py --name inherited01
& $d5bPython -B research/resource-carinae-source-context/qualify.py --build .local-work/resource-carinae-source-context/transient-build01 --output .local-work/resource-carinae-source-context/d5b-qualification01
& $d5bPython -B research/resource-owner-acquisition/qualify.py --build .local-work/resource-owner-acquisition/build15 --output .local-work/resource-owner-acquisition/d5b-qualification01
& $d5bPython -B research/resource-combined-acquisition/legacy_regression.py
& $d5bPython -B research/resource-combined-acquisition/preflight.py --build .local-work/resource-combined-acquisition/build15 --qualification .local-work/resource-combined-acquisition/qualification13/summary.json --name offline-preflight03
& $d5bPython -B research/resource-combined-acquisition/postflight.py --preflight .local-work/resource-combined-acquisition/offline-preflight03/preflight.json --output .local-work/resource-combined-acquisition/offline-postflight01.json
& $d5bPython -B research/resource-combined-acquisition/audit.py after
& $d5bPython -B research/editorial/screen.py --changed
& $d5bPython -B research/resource-combined-acquisition/package.py --label review03
```

Fresh output names are mandatory; reruns do not overwrite prior evidence. `inherited01/summary.json` records exact subprocess commands and exit codes. The dedicated C2B/D4D commands above and legacy replay preserve their own primary receipts. The comparator writes INVALID for malformed receipt copies and retains both untested alternatives. It never treats an observed zero population as missing evidence.

Both preservation audits rehash the same 36892 initial pins with zero protected changes and unchanged HEAD/index. The final `offline-preflight03/` audits 271 live/backup saves and 39 installed definitions, verifies 98 fresh protected master copies and scratch-only Save52 restoration. `offline-postflight01.json` passes full no-session live/backup/master/content/configuration comparisons with no changes; this rehearsal is not a retail session. Steam Cloud remains UNKNOWN and requires fresh operator confirmation before any future live approval.

## Preserved failures and corrections

The normal `python` alias was unavailable; execution uses the explicit installed CPython path. Build01 failed because C++ object names collided with assembly object names. Build02 failed on duplicate inherited decoder definitions. Both logs remain local; separate assembly names and one decoder domain corrected those failures.

Qualification02 incorrectly required no valid current consumption after a source-slot reuse that occurred after an earlier valid ACCEPT. It preserved a legitimate consumer-only observation, with no lifetime join; the oracle was corrected. Qualification05 incorrectly expected a controller error on pre-ACK target termination; Windows could drain that exit cleanly. The corrected test checks the actual target exit, receipt durability and absence of scientific promotion, accepting a clean drain or an explicit failure. The earlier failed verdicts are unchanged.

A transient qualifier indentation error prevented dispatch and was corrected before its rerun. One mistyped executable path failed before dispatch. A Windows default-code-page read damaged the new card and two shared documentation bodies; diff/editorial review caught the damage, restored the shared bodies exactly from HEAD and retained only the intended D5B entries. Explicit UTF-8 reads now apply to every authored Python module. The final manual pass also corrected a script docstring that had omitted its newly added synthetic subprocess effects; a fresh build and qualification bind that correction. Later source changes always received a new build manifest and fresh qualification. Context-unavailable and intentionally refused/corrupt cases remain negative evidence, not successful native science. No failure was repaired by changing protected inputs, fitting predictions or granting live authority.

Independent primary review caught one reduced metadata defect: the return row lacks a provider token even though the raw entry retains it. The corrected reducer preserves the entry token, requires equality with the original and upstream tokens, and qualifies a nonzero integer in both schema and fixture assertions. Receipt comparison also rejects cross-session envelopes. Build15 and its fresh qualification supersede earlier reductions; raw first-query/mask evidence was intact. Offline preflight01/02 are retained but cannot serve as gates for the corrected final build.

## Criterion matrix and separate outcomes

The independent reviewer accepted the following accounting against the exact review02 snapshot. AC1–AC8 remain exactly as frozen in the brief; only the review closure changes afterward.

| Criterion | Status | Primary evidence and limits |
|---|---|---|
| AC1 | PASS | `audit-before.json`/`audit-after.json`, protected-save receipts, no retail operation; original inputs and HEAD/index equality. New test outputs are additions, not changes to the initial protected inventory. |
| AC2 | PASS, scoped STATIC/fixture | native.md, source pins, exact saved case and raw boundary operands. Native lifetime/alias fence and historical epoch remain unknown. |
| AC3 | PASS, synthetic | actual combined hardware controller, cross-process reads, shared operational pump, independent SRO1 readback and ACK/STOP. Retail execution is NOT TESTED. |
| AC4 | PASS, scoped synthetic | exact-key discrimination, current Workshop transfer, conflicting masks, fixture-only positive lifetime and replacement/reset refusals. No native epoch promotion. |
| AC5 | PASS | fixed mask-0/mask-3 comparisons, explicit first-query prediction unknown, negative/partial/corrupt-copy cases and unchanged frozen hash. |
| AC6 | PASS, proposal only | complete one-case run-card.md with strict preflight, construction-only STOP, no-hit/cache paths, backups/postflight and separate approval. VI-b remains gated. |
| AC7 | PASS | fresh 37 cases, 250 inherited cases, actual operational pump, ten native controls, 34 D2/D3 requests, 38 D5A equal outputs, source/protection/build/command receipts. |
| AC8 | PASS | independent scientific/engineering/editorial ACCEPT on review02; exact patches, manifests, exclusions, screen/manual coverage and forward/reverse checks verified. The final closure receives narrow delta review. |

Science: synthetic construction and consumption ancestry qualified; no new retail query, mask or region measured. Engineering: actual executed coverage only, with incomplete nested producer stages and possible slot-switch loss disclosed. Evidence integrity: independent framing/readback and original-input hashes; checksums do not prove semantics. Target outcomes: intentional disposable fixture crashes/termination, final PID absence checked; no retail survival/recovery claim. Rights: owned adaptations only; raw evidence LOCAL-ONLY and authored work REVIEW-REQUIRED. No integration or publication clearance.

## Editorial and exact delivery

The final changed-text screen covers every changed authored Markdown/CSV label and Python comment/docstring; manual reading also covers C++/assembly explanatory text, JSON schema labels, the complete changed prose and scientific qualifications. Native domains, binary32 bits, source/site distinction, pointer/lifetime limits, direct/derived evidence and proposal/authority wording receive contextual review. A clean screen alone is insufficient. The complete brief is supplied unchanged and is governing input, not task-authored prose.

The exporter writes complete and task-only patches in `.local-work/diffs/rg2-d5b-review03-*.diff`. Complete includes the supplied brief; task-only excludes it. It inventories tracked and untracked text, validates exact forward/reverse application against HEAD in isolated scratch trees, checks whitespace/links, and preserves changed-file hashes, status and local-only exclusions. The entire raw corpus, built executables, proprietary bytes, saves, analysis databases and prior failure logs remain excluded/local. The supplemental `inherited-exclusions.json` inventories all 3583 new inherited raw artifacts outside the task root; `integrity-final01.json` verifies unchanged original pins, current build pins and HEAD/index. Nothing is staged for export.

Independent review returned **ACCEPT** for AC1–AC8, with separate scientific, engineering and editorial ACCEPT on review02. The complete actual return is retained at `.local-work/resource-combined-acquisition/independent-review01.md`.

The reviewer independently decoded all 316 final captures, checked SRO1 digests/sidecars/events/SESSION envelopes/PIDs and post-STOP discipline, verified all 13 acknowledged provider tokens, all ten native controls in both representations, 38 D5A equal outputs, 101 build pins, 54 provenance pins and 3583 inherited exclusions. All 38 file hashes and both patch reconstructions agreed; reverse scratch states matched HEAD or absent new files. The reviewer inspected executed tests and performed separate read-only checks; they did not rerun targets or rehash every protected original. Those limits remain explicit.

Accepted review02 package SHA-256 is `2afebc7793f57ddeb4427ef8084dafb5ff10393ed50b4c924544f0238729883e`; its changed-file manifest is `12c6eba3519800aa462655860a1de510656010b9073d7e6fe850307985332aaf`. Both full protection audits hash to `655e869bc17c4f607907d08d27e100114f4eb9e70e30f4a6336494a2bfcd3908`. HEAD remains `0d03262e2cc05c01a992f8eddee183a9d8ab0d32`; index SHA-256 remains `6af6672613fc894ab677bd7cf78bd441f2093f33bd5456593dc049a47c79e8be`.

Only this self-describing review closure changes after acceptance. Final package review03 refreshes exact complete/task-only patches and manifests; `independent-delta01.md` retains the required narrow delta decision. The final local `delivery.json` binds the actual independent returns and final package hashes. No acceptance supplies Phase B, integration, staging, commit, push, release or publication authority.
