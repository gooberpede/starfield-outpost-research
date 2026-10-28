# D5L Phase B: incomplete acquisition and breakpoint failure

2026-10-28, Australia/Sydney. [Authority](phase-b-authorization.md),
[executed card](run-card.md), [post-mortem and prevention plan](phase-b-postmortem.md),
[receipt ledger](phase-b-sources.csv). Original Phase A findings and qualification
remain historical.

**Neither authorized process captured a target construction–retention–reuse
chain. The ordinary-user retry attached successfully and preserved 493 verified
receipts, but exited during the reported fast-travel sequence. Windows crash
records locate the breakpoint failure at the observer's Grid-clear probe.**

| Evidence dimension | Result |
|---|---|
| Scientific question | Does a witnessed first successful construction produce a retained region subsequently reused by the selected source? |
| Best-supported answer | Unresolved. No selected-source decision, completed construction or reuse chain was captured. |
| Confidence and basis | PROVEN / RUNTIME for recorded barrier, copied lifecycle events and receipt correspondence. STRONG observer-associated breakpoint failure from runtime/Windows crash correlation; precise mechanism UNKNOWN. |
| Coverage | Two explicitly authorized processes; the first failed before attachment. The retry covers main-menu arming and partial Save52/travel activity, ending before reported arrival. |
| Completeness | All 493 retry receipts and ACKs bind to the journal. Scientific acquisition is incomplete; first-ever construction and intended population completeness remain UNKNOWN/unproved. |
| Publication | Raw captures/Windows records/archives LOCAL-ONLY; authored synthesis REVIEW-REQUIRED. No B6 or publication clearance. |

This is not a completed negative result about construction or retention. The
operator's bounded travel sequence did not finish, and the terminal journal
contains an unexpected-exit GAP. The older D5B consumer geometry and all frozen
query predictions retain their prior classifications.

## Two separately authorized opportunities

The first full preflight passed before launch: 98 protected save names with
verified independent backups, 39 installed definitions, installed executable and
PlanetData pins, configuration, active archive-backed scientific inputs, disk
floors and scratch-only Save52 restoration rehearsal. Steam Cloud disabled and
main-menu/no-save-loaded state were direct operator reports.

The first collector invocation stopped before consumption/attachment because
normal launch rewrote only `Plugins.txt`'s timestamp. Its size remained 480 bytes
and its original scientific SHA-256 remained
`8dac50493405250ab92feea55701a1ecb6fdf333703d9c152042262e5c26db33`.
A separately written derivative refreshed that one metadata guard, preserved all
content expectations and the original prelaunch timestamp, and recorded its
provenance. Independent incident review accepted that exact bridge. No original
receipt or configuration was changed.

The subsequent invocation consumed admission02 for PID 13276, creation FILETIME
`134376171120172056`. `DebugActiveProcess` returned Windows error 5. No SESSION,
barrier or scientific receipt was produced. The controller's approved failure
cleanup requested termination; independent process absence and the operator's
“Game exited.” report followed. The cleanup did not observe an EXIT debug event.
Full offline postflight and protected-input comparison passed before any retry.

The collector had run under `typhon\codexsandboxoffline`, while Steam belonged
to `TYPHON\User`. Neither inspected token carried `SeDebugPrivilege`; its absence
alone does not establish the cause. Windows requires fuller debugger access than
the controller's earlier query/read/termination handle. See
[Microsoft DebugActiveProcess](https://learn.microsoft.com/windows/win32/api/debugapi/nf-debugapi-debugactiveprocess).
The account boundary is the best-supported access diagnosis; the original target
DACL and complete security state were not captured.

The maintainer then explicitly authorized a fresh ordinary-user retry. A new
full preflight passed before PID 8352, creation FILETIME `134376178118454456`,
was launched. The same timestamp-only Plugins rewrite was independently reviewed
again against the exact original content hash, with a separate derivative.
Admission03 and the reviewed wrapper bound that process, original card/build and
actual `typhon\user` caller. No privilege, observer source, site or binary changed.

## Retry observations and exit

The retry SESSION records the pinned retail executable, actual module base
`0x7ff620be0000` and all fourteen relocated probes. The durable barrier covered
93 known threads. Independent SRO1/ACK decoding verified it before the load
instruction was issued. The operator was told to load only the hash-bound Save52
menu entry, travel normally to the second Feynman V outpost, and avoid saves,
Build Mode and outpost modification.

The operator first reported “Still loading or travelling”, then:

> Save52 loaded. Game exited after selecting second Feynman V outpost and initiating fast-travel.

These are operator reports, not screenshot-derived locations or precise action
times. Exact load and travel-start times remain UNKNOWN. No automated gameplay
input or additional runtime observer was used. Live monitoring stayed within
small health/identity/file-metadata checks; no full save audit or scientific raw
reduction was performed during play.

| Retained retry event | Count |
|---|---:|
| Durable barrier | 1 |
| Reset sample | 1 |
| Grid initialization samples | 55 |
| Source initialization samples | 383 |
| Grid-clear samples | 53 |
| Total native samples | 492 |
| Selected-source decisions / complete chains | 0 / 0 |

The unchanged reviewer binds all 493 SRO1 files and ACKs to the journal and
reproduces zero decisions/chains. The terminal record is `GAP: unexpected_exit`
followed by EXIT code `0x80000003`. Controller exit 0 describes its completed
event loop, not successful target execution; `requested_stop` is false. There is
no recorded TARGET_EXCEPTION, STOP, fatal or failure-cleanup event in this retry.

Windows Application Error 1000 and its WER companion identify the same PID and
creation time, Starfield.exe 1.16.244.0, exception `0x80000003` and module-relative
fault offset `0x9829b0`. That equals probe 10, `native_grid_clear`, at runtime VA
`0x7ff6215629b0`. This strongly associates the failure with the armed breakpoint;
the precise delivery/continuation mechanism is not established. The final sample
492 is source initialization, not the faulting Grid-clear event. Its timestamp is
23:42:04.472532 UTC; the Application Error record time is 23:42:54.7795942 UTC,
which is not necessarily the exact trap time. No crash dump was opened.

## Preservation, evidence and completion accounting

Both complete after-exit preparations and protected-input comparisons passed.
All 98 protected save names and their independent backups, installed inputs and
configuration hashes remain equal. Transient saves and `remotecache.vdf` retain
their prospective diagnostic treatment. The historical Cloud discrepancy and
four-ZIP strict failure remain recorded; no historical baseline was repaired.
The two postflight bridges are deliberately `PARTIAL_POSTFLIGHT` despite
preservation PASS because the scientific captures failed/incomplete.

The existing archive utility sealed both raw attempts and their companion
receipts as PARTIAL, retained raw originals, and stream-verified all 1,065 members.
The ZIP SHA-256 is
`609efea5642ec4d225ad2381abdf658abf8da9d986b98c5275a3472724548a0b`.
The seal and archive receipts are outside every sealed root. Later review/delivery
records reside separately in `.local-work/d5l-phase-b-final/`; they are not claimed
as members of that earlier sealed evidence set.

| Required outcome | Disposition |
|---|---|
| Authorization, fresh preflight and Cloud confirmation | PASS for each authorized opportunity. |
| Correct retry account and verified pre-load barrier | PASS; actual ordinary-user caller and fourteen-site/93-thread barrier recorded. |
| Protected Save52 load and travel completion | PARTIAL operator report: load and travel initiation, no completed arrival. |
| Construction–retention–reuse witness | NOT ACQUIRED; zero decisions/chains. The research question remains open. |
| Receipt integrity | PASS for the complete retained retry prefix and terminal journal. |
| Target survival | FAIL: first approved cleanup disposed the process; retry exited unexpectedly at an armed breakpoint. |
| Offline preservation and archival | PASS, with partial-capture classification retained. |
| Independent final review and exact diffs | Bound by the separate final delivery manifest and verbatim review returns. Acceptance of this record does not qualify the observer for reuse. |

All 32 original D5L method/history files and the accepted native build identities
remain unchanged. The 27-scenario debugger qualification was not rerun. The
post-mortem recommends specific repairs/requalification; none was implemented
and no further retail process was launched. No staging, commit, push or external
evidence disclosure occurred. Further live use is on hold pending the applicable
engineering review, qualification and new explicit authorization.
