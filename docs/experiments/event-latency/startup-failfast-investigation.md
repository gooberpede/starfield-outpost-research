# Adapter startup fail-fast — SOR-EXP-0027 / SOR-EV-0035

2026-10-11 Australia/Sydney; SOR-D-0047.
[Authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_adapter_013_startup_failfast_investigation.md`).
Offline analysis and disposable processes only; no Starfield process open, memory
access, launch or attachment in this assignment. Authored results REVIEW-REQUIRED;
private receipts/dumps LOCAL-ONLY.

| Question | Strongest supported answer |
|---|---|
| Why can0.1.3 silently die before READY/root creation? | A startup error enters its outer catch; that catch writes timing before stderr. A missing/unwritable output path throws `profile_write` from the handler, escaping and terminating the executable. PID conversion also occurs outside the protected block. |
| Confidence | PROVEN for the controlled error-handler defect and uncaught-PID paths; STRONG as an explanation of the original incident's phenotype, not a uniquely established original primary error. Proposed classification awaits review. |
| Coverage | Byte-identical approved 0.1.3, existing installed runtime, rejected disposable identities, denied access, invalid inputs, output conditions and launch variants. Corrected 0.1.4 tested independently. No new game run. |
| Decisive evidence | Absent/existing-directory intervention; native `0xC0000409` versus exit 1 with original diagnostic; CDB observes `open:87` then uncaught `profile_write` in the exact original executable. 19 startup controls per version. |
| Original incident limit | No original exception/dump/primary diagnostic was retained. Multiple distinct errors reproduce its identical signature. The precise original initiating error is not recoverable from these receipts. |
| Decision | A narrow0.1.4 diagnostic/argument repair is justified for review. It does not establish live readiness or resolve the separate threaded qualification counterexample described below. |

## Original evidence and preservation

[First attempt](center-smoke-20261011-result.md) remains unchanged. Approved ZIP
SHA-256 `2e29c452b566b992bc504cf0d6e2c4971675aabd47ad4d3408b455268c121efc`;
approved executable SHA-256
`b0751a86655b0a4759932f0b90cfcd7aeb9314f9a03b5a52d4522ba5bd1c1eb3`.
Original PID 8556 launch 02:23:04.1284781Z/exit 02:23:04.4462634Z is
13:23:04 Australia/Sydney (UTC+11). Target PID 17100, original windows/no debugger
postflight, user normal exit/sync and protected-input checks remain observations,
not evidence of a confirmed attachment. No root/READY/WAL was fabricated.

All 116 original incident/review files and approved binary/package inputs are
hash-pinned in `.local-work/adapter-startup/immutable.json` and checked at handoff.
The 0.1.2 baseline/all six controls and original 0.1.3 qualification remain separately
preserved. New builds, failed pilots and tests use distinct ignored directories.

## Exact executable, runtime and startup

The original PE is AMD64/PE32+, Windows console subsystem 3, preferred base
`0x140000000`, entry RVA`0x1F480`, image size`0x32000`. Link timestamp decoded as
UTC is 2026-10-11T01:25:47Z. Compilation receipts pin MSVC19.51.36256/link 14.51,
`/std:c++20 /EHsc /W4 /O2 /MD /DUNICODE /D_UNICODE`, `/INCREMENTAL:NO` and bcrypt.
The generated retail hash/site table matches the approved guards. Original
qualification's source hashes, generated header, build logs, executable hash and
ZIP member/hash provide provenance; timestamps alone do not prove identity.

Dependencies include KERNEL32, bcrypt, MSVCP140, VCRUNTIME140/140_1 and UCRT API
sets. Actual CDB loads resolve UCRT to installed `ucrtbase.dll`10.0.19041.3636.
No SFSE import/deployment is involved. PE has ASLR/high-entropy/NX flags, x64
unwind data, a security-cookie location and CF-instrumented load-config flag with
no function table; do not equate those fields with proof of a fully enabled CFG
policy. No PDB was supplied; static imports/disassembly and runtime throw-object
observations supply the relevant compiled boundaries.

The [fault-path map](startup-fault-map.md) distinguishes compiled/static stages
from observed executions. Entry initializes CRT/cookie/C++ state, then wmain;
normal argument branches precede OpenProcess, image/root/identity/site/module
checks, root creation, evidence directory/WAL, durable session and attachment.
`DebugActiveProcess` is after session flushing. No root-removal path exists in
this source. External deletion/path/reporting error was not traced retrospectively
and cannot be absolutely excluded solely from directory absence.

## Reproduction and causal intervention

Start with the pinned approved executable, not a rebuild. Initial six probes are
retained under `.local-work/adapter-startup/initial-repro`: version exits 0,
missing arguments exit 2; invalid/nonexistent PID and a valid disposable Python
PID with rejected retail identity each silently exit`0xC0000409` with absent root.
Precreating only the output directory changes both cases to exit 1 and preserves
`open:87 attached=0` or `retail_identity:0 attached=0`. The target remains alive;
retail integrity was never bypassed.

Final [original startup matrix](../../../.local-work/adapter-startup/startup-controls-013-final/results.json)
contains 19 controlled cases; [candidate matrix](../../../.local-work/adapter-startup/startup-controls-014-03/results.json)
repeats them against the delivered binary. Inputs include valid disposable PID,
empty process DACL denying new opens (error 5), missing/unknown mode, version,
invalid/overflow/trailing/negative/zero PID, relative path, changed cwd,
space-containing path with correct quoting, hidden redirected Start-Process,
inherited streams/default creation flags, wrong genuine-fixture hash, output
occupied by a protected sentinel file, successful fresh-root fixture startup,
and a timing-write failure after independent retirement. Temporary DACL changes
apply only to the original disposable helper itself and are restored before its
normal exit. No system/security configuration was changed.

0.1.3 reproduces the silent failure under ordinary direct launch as well as the
hidden/redirection shape. Those launch features are not necessary causes. A valid
fresh-root fixture reaches READY and clean retirement: missing output directory
does not itself break successful startup. It breaks the error-reporting path
when an earlier operation rejects. Wrong argc/mode exits 2 rather than fail-fast.
PID conversion outside try is a distinct unhandled-error route; the original
live numeric 17100 argument supplies no positive evidence for that route.

Two harness pilots failed before launching the adapter: inherited environment
contained case-variant Path/PATH entries that Windows PowerShell's Start-Process
dictionary rejected. Final harness canonicalizes environment-key case in its
own child environment, records the launch and preserves the pilots. This is
distinct from the incident, which recorded a real adapter PID and process exit.
No system environment was changed. Current environment/token observations cannot
reconstruct every property of the earlier launch token.

## Instruction/exception evidence

CDB10.0.19041.5609 was launched only against disposable adapter executions, with
an empty local symbol path, inherited symbol paths ignored and no symbol downloads.
The useful trace under `diagnostic-013-throw2` breaks at CxxThrowException and
reads the adapter's own exception object: first `open:87`, then `profile_write`.
The second exception reaches second-chance unhandled C++ EH. Its private dump,
console, command and hashes remain local. Earlier incomplete debugger pilots are
retained and are not labelled successful fault captures.

Original compiled image RVAs: OpenProcess call`0x1BED4`; failed require returns
through`0x16EB4` to`0x1BEFC`; profiler-save throw returns through`0x17B56`;
the outer handler calls profiler-save at`0x21836` and would print the primary
diagnostic only afterward. Thus the source hypothesis is verified in the exact
compiled executable, not merely inferred from a modified build.

Native non-debugged controls exit`0xC0000409`. The debugger exposes the secondary
C++ EH boundary instead of reproducing that final native status; do not present
its dump as the original incident's crash/subcode. Installed UCRT disassembly
shows terminate→abort and abort's `mov ecx,7; int29` path. This corroborates the
fatal-app-exit mechanism, but **neither the original incident's fast-fail parameter
nor its exact fault address was captured**. Microsoft's [fast-fail documentation](https://learn.microsoft.com/en-us/cpp/intrinsics/fastfail?view=msvc-170)
explains why status alone is insufficient, while its [unhandled C++ exception documentation](https://learn.microsoft.com/en-us/cpp/cpp/unhandled-cpp-exceptions?view=msvc-170)
supports the runtime termination chain. SDK 26100 CRT source was consulted only
as explanatory source; it is not assumed byte-identical to OS UCRT19041.

## WER, permissions and remaining original uncertainty

Read-only searches retained in `wer-search.json` and `security-event-search.json`:
Application/System for 02:15–02:35Z; Defender/CodeIntegrity/AppLocker for
02:22:45–02:23:45Z; machine/user WER archive/queue and existing CrashDumps entries
matching adapter/SorEventOracle/PID 8556; current WER/LocalDumps registry values.
Application has 3 entries in the broad interval, none matching the adapter;
System/security intervals return no matching events; WER-Diag channel is absent.
No matching adapter report/dump is found in the searched directories; current
machine LocalDumps key is absent. These negatives are scoped searches, not proof
that no diagnostic ever existed. Unrelated Starfield dumps were not opened.

Candidate initiating errors before first output include full-access process-open
denial, image/root/identity guard rejection, module/ntdll validation and directory
creation failure. Original read-only preflight verifies less than
PROCESS_ALL_ACCESS; it cannot retrospectively prove that full-access open
succeeded. Controlled access denial and identity rejection are counterexamples
to uniquely attributing the phenotype. There is no original stack/throw object,
API result or token/ACL trace to distinguish them. Missing global CRT dependency
or universal static-initializer failure is contradicted by the same executable's
successful version and fixture paths, but per-launch environment faults are not
universally excluded.

Accordingly: original **confirmed startup failure, no confirmed attachment**;
process open could have occurred before rejection; patching requires later
attachment/debug events. Original independent postflight remains the direct
same-survivor evidence of original code/no debugger. No claim of a Starfield
defect, overflow or game-specific trigger follows.

## 0.1.4 correction and separate qualification counterexample

The repair puts PID parsing inside the protected block, validates a full positive
DWORD decimal PID, prints/flushed primary error plus stage/attached state before
optional timing, catches secondary telemetry failures, never creates an error
path to make diagnostics succeed, and guards timing output on both drives.
Stage advances through event-loop/timing/terminal operations. Process handles
are closed on rejection. Existing loop/patch/collector/invocation/WAL bodies are
unchanged apart from event/READY version labels. WAL format remains SOREP013;
decoder receipt version 0.1.3 denotes format, not the emitting adapter version.

[Qualification](startup-014-qualification.md) preserves every attempt. A preliminary
build ran six controls but its end-of-run source-pinning assertion failed because
source was refined while it ran; it is not the delivered qualified build. A second
build's threaded full control reached READY, then received a breakpoint exception
while a center-entry replay was pending, reported restored:true and persisted a
RETIRED terminal before fixture completion. The wrapper did not retain numeric
exit statuses for that failed case. Its WAL is valid, terminal RETIRED, 24 boundaries, 13 actual
center entries and one active scope retired. No exception address was recorded,
so a queued second site trap is a concrete hypothesis, not a proven address match.
This is a retained instrument-safety counterexample, separate from startup and
not caused by the new diagnostic handler according to the unchanged loop diff.
No failure is erased by a later passing sample.

The final harness can finish remaining controls after a failure while retaining
failed status and nonzero overall exit. This improves reporting; it does not
weaken assertions or classify a failed control as passing. The final six-control matrix is 5 PASS/1 FAIL: grid-guard-failure stops with
`suspend_live_thread:5` in the unchanged event loop. Review both retained
counterexamples and the complete case matrix before any decision. Startup repair is useful
even if runtime readiness remains blocked.

## Recommendation

Review the surgical diagnostic correction independently. **Do not authorize a
new live smoke from this package alone.** First investigate the retained pending-
replay/foreign-breakpoint counterexample using disposable processes with exact
exception-address/control-state logging and independently checked continuation.
The old approved run card/checker still pin 0.1.3 and must not silently run 0.1.4.

Once runtime readiness is resolved and reviewed, the most discriminating proposed
live diagnostic would use the corrected primary-error reporting under a separately
authorized card. It is a proposal only: no launch/attachment, deployment, contact,
publication, staging, commit or push follows here. The original initiating error
cannot be recreated offline without either fabricating its state or accessing the
prohibited game process, so this report leaves it explicitly unresolved.
