# Startup investigation review return — candidate 0.1.4, not live-qualified

2026-10-11 Australia/Sydney; SOR-D-0047 / SOR-EXP-0027 / SOR-EV-0035.

- [Answer-first root-cause report](startup-failfast-investigation.md).
- [Compiled/source startup and fault-path map](startup-fault-map.md).
- [Exact candidate qualification and retained failures](startup-014-qualification.md).
- [Original startup controls/read-write/cleanup contract](../../../debugger/event-startup/README.md).
- [Task-only patch from captured starting tree](../../../.local-work/diffs/adapter-startup-failfast-task-only.diff).
- [Complete HEAD patch, including earlier uncommitted work and supplied brief](../../../.local-work/diffs/adapter-startup-failfast-complete.diff).
- [Status, hashes, path/exclusion/check manifest](../../../.local-work/adapter-startup/review-01/review.json).
- [Versioned local review ZIP](../../../.local-work/adapter-startup/review-01/SorEventOracle-0.1.4.zip).
- [ZIP/member/hash manifest](../../../.local-work/adapter-startup/review-01/package.json).
- [Preservation/input receipts](../../../.local-work/adapter-startup/review-01/preservation.json).

**Proven defect:**0.1.3 writes timing from its outer error handler before stderr;
an unavailable timing path throws another exception, hides the first error and
reproduces silent`0xC0000409`. PID conversion outside try is another unhandled
route. The original live initiating error remains UNKNOWN because its first
diagnostic/dump was lost. Multiple controlled errors have the same signature.

**Narrow change:**0.1.4 protects/validates PID parsing, flushes primary diagnostics
first, names stages, contains secondary timing errors, avoids diagnostic-created
unvalidated directories, closes rejected process handles and checks the existing
both-drive storage guard before timing output. Acquisition loop and native guards
are unchanged apart from event/READY version strings. The qualifier's optional
keep-going mode retains failed controls and returns overall failure, enabling a
complete case matrix instead of aborting at the first failure. 19 startup controls,
12 health and 11 Python tests pass; final established controls are **5 PASS/1 FAIL**.
Two runtime counterexamples remain blockers regardless of passing repeats.

New authored files: two disposable startup scripts and their README; investigation,
fault map, qualification and this review. Modified implementation files: adapter
startup/version code and qualification/version/reporting only. Documentation
supplements update root/state/decision/provenance/source/credit/experiment/evidence/
brief/latency indexes. Supplied brief is retained unchanged and included in the
complete patch as pre-existing supplied input, not task-authored work. No renames
or deletions. Original 0.1.3 architecture README remains unchanged; the new startup
README supplies the candidate supplement.

Actual review checks: preserved original/package/baseline/shared inputs; compiled
runtime-code comparison; source-to-build hashes; both patch path inventories,
reverse applicability and forward exact-byte comparison; tracked/current-task
whitespace, Python syntax and local Markdown file links. Counts/hashes and any
intentional supplied-brief whitespace exclusion are in the manifest. Anchors,
external URLs and scientific semantics are not validated by link existence.

The ZIP is **NOT_LIVE_QUALIFIED**, includes only original authored candidate/source/
docs and selected non-raw review/qualification/preservation receipts. No proprietary
game binary/asset, save, raw memory/WAL, process dump, OS/CRT source/binary, symbol,
analysis database, configuration, credential or bulk event-log payload is included.
Private artifact locations/hashes and omissions are explicit. No upload/disclosure.

No permission issue blocked the performed scope: original project reuse retains
SOR-P-0002/SOR-S-0132; Microsoft SOR-S-0138 consultation and installed separate-tool
execution were within the explicit brief, without copied implementation or new
dependency. No Starfield launch/open/memory/attachment, global security/config
change, save/database mutation, deployment, staging, commit or push.

Review decision requested by the brief: consider the startup repair independently;
retain the live block and pursue disposable thread-control diagnosis before any
separately authorized minimal live diagnostic. Do not silently replace the approved
0.1.3 card/checker/package or treat this report as integration approval.

Suggested subject (not committed):

```text
fix: preserve adapter startup errors and record failed requalification
```
