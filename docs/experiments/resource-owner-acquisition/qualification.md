# D4D qualification and reproduction

Run from the repository root with installed CPython
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`.
No downloads or new dependencies are required. Build outputs and raw evidence
are exclusively created under `.local-work`; old attempts are preserved.

| Check | Actual evidence and result |
|---|---|
| Candidate build | `build15/build.json`, exit 0, installed MSVC 19.51.36256.0. The intentional per-thread `rvas` alias produces a shadowing warning, not a failed build. |
| Native map fixtures | `qualification12/summary.json`: 25 real Windows attachment cases, all semantic expectations pass. Target arrays belong to the independently executing fixture. |
| Terminal transport/STOP | `terminal06/summary.json`: all 12 expectations pass, including 96 worker-thread exits, pending STOP, missing/partial/refused ACK, crash before/after evidence and genuine invalid-handle/continuation probes. Deliberate controller errors remain exit 2. |
| Adversarial comparison | `comparison06/summary.json`: 14 checks pass. Removing all CALLs or cleanup is rejected; a contradictory map is retained at its first boundary; corrupted copied receipt is refused by independent digest verification. |
| Operational wrapper admission | `wrapper02.json`: exact-path D4D selector import and four receipt regressions pass. Cache-only, wrong source and wrong Workshop do not stop; complete bound construction does. This imports the real wrapper without executing its retail main. |
| Inherited debugger suites | `inherited01/summary.json` and each suite's `d4d-inherited01` receipt directory. D4A, D4, C1G, C1E, C1D and C1C remain separately scoped synthetic qualifications. |
| Geometry/predictions | `regressions01/roster.json` reruns frozen D2/D3 requests; its `seven-controls` retains both D1 representations. `inherited01/archimedes/summary.json` reruns the three receipt-informed D4B controls. No fitting or frozen-output replacement. |
| Python/transport | `python-checks01/summary.json` retains standalone/selector tests and the inherited SRO1 self-test. |
| Protected inputs | `audit-before.json`, `audit-after.json` and `protected-before/after.json` rehash the exact immutable baseline and adopted save/content policy. HEAD/index are independently compared. |

Paths in the table are relative to `.local-work/resource-owner-acquisition/`, except
the inherited debugger suite directories, which remain under their own local
subsystem roots. The final delivery manifest supplies exact hashes and outcomes;
no earlier diagnostic snapshot is substituted for a current qualification.

The 25 cases cover direct supply; equal-final-map exchange; distinct order; null
slots; duplicate root/empty replacement; empty range; malformed and incomplete
node reads; corruption; nested calls; source-content reuse; wrapper reuse; unrelated
same-planet source; cache hit without construction; crash before and after;
wrong owner/type/range; positive source plus Workshop; wrong source; wrong Workshop;
sequential thread lifetimes; and deterministically overlapping construction. The descriptor-bypass case completes construction with candidate/CALL coverage UNKNOWN and no scientific STOP. All six slot positions
and full raw headers are checked, not a resource multiset alone.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-owner-acquisition/audit.py before
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-owner-acquisition/build.py --name build15
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-owner-acquisition/qualify.py --build .local-work/resource-owner-acquisition/build15 --output .local-work/resource-owner-acquisition/qualification12
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-owner-acquisition/teardown.py --build .local-work/resource-owner-acquisition/build15 --output .local-work/resource-owner-acquisition/terminal06
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-owner-acquisition/test_comparison.py --qualification .local-work/resource-owner-acquisition/qualification12 --output .local-work/resource-owner-acquisition/comparison06 --d4c-model .local-work/resource-owner-root/freeze01/inputs-v1.json
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-owner-acquisition/inherited.py --name inherited01
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-owner-acquisition/audit.py after
```

These are the executed names; repeat runs require fresh names and destination
adjustments in the fixed-output regression helpers. Exclusive creation prevents
overwriting prior failures. `build01` preserves an assembly label-size error;
`build02` preserves an object-name collision. `qualification01` preserves the
fixture argument-home overwrite crash. `qualification02/03` preserve the wrong
candidate-header diagnostic and its subsequently failing semantic assertion.
Later builds/runs remain retained even when superseded. A zero controller exit
was never sufficient to qualify the failed acquisition. Historical D4A teardown
failure and D4C ESCALATE are unchanged.

Final review of the earlier build14 snapshot found an operational import defect:
the wrapper resolved the old D4A admission module after qualification changed
the Python search path. That selector falsely stopped on cached-only capture 3
with zero construction rows. The actual independent REWORK is preserved in
`independent-review01.md` locally. The corrected wrapper loads its D4D selector
by exact source path; `test_wrapper.py` checks that actual import and all four
positive/negative receipt cases. New build/qualification/preflight supersede the
defective snapshot; its patches, manifest and counterexample remain retained.
