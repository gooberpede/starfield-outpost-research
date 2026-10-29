# D5P Phase B — capture loss and unqualified native context

2026-10-29, Australia/Sydney. [Authority and accepted deviation](d5p-phase-b-authorization.md),
[approved historical card](run-card-d5p-v1.md), [independent review](d5p-phase-b-review.md),
[source/evidence ledger](d5p-phase-b-sources.csv).

**The observer loaded and passed READY, but acquisition failed after one reported
producer-admission drop. All 1,592 admitted records were flushed and authenticated.
None qualifies the selected source's construction or reuse. Native context
qualification also failed on all 319 recorded source-demand events. The game
survived through operator-reported arrival and subsequent exit; protected-input
postflight passed. Further retail use of this candidate is NO-GO.**

| Element | Supported result |
|---|---|
| Question | Can the approved observer witness construction, completed retained geometry and later reuse for second Feynman V source `0:37536:20928:0029d20e`, owner FormID `0x0005e0de`? |
| Answer | Not established. No qualified selected-source decision or region chain survived; acquisition is INCOMPLETE, not a qualified non-hit or hypothesis falsification. |
| Confidence/basis | PROVEN / RUNTIME for authenticated startup/ACK/terminal and captured diagnostic words. Individual context-guard failure and full-queue versus contention failure branch remain UNKNOWN. |
| Coverage | Two observed pre-load startup streams; only original PID 3424 admitted for the ordinary Save52 sequence after an explicit duplicate-launch disposition. The operator reports arrival, then exit and disablement. |
| Completeness | Exactly 1,592 acknowledged primary records and one acknowledged duplicate-startup record are authenticated. This does not establish complete execution coverage, source absence or the number of unrecorded events after capture closed. |
| Publication | Authored account REVIEW-REQUIRED; native records, private receipts, binary package and protected-save copies LOCAL-ONLY. B6/publication holds remain unchanged. |

## Admission and operator actions

The task began clean at maintainer-integrated HEAD
`3f2e3481e25b5ef2a4594b424b03e3ee5180694f`. At admission, all 26 accepted
Phase A files and the build14 DLL, ZIP, qualification and card matched their
approved hashes. The executable sources and deployed artifact were unchanged. The
maintainer installed the package in Vortex profile **Starfield - SFSE** and
confirmed disabled Steam Cloud saves and no launch before this attempt.
The staged and deployed DLLs both match SHA-256
`935071691f6325f99d1f8ec99056349d6eb5fee19dba237cffd6e7d7833650cc`.
Only that DLL was deployed under `Data/SFSE/Plugins`.

Fresh preflight authenticated the active archive-backed selection, 91,933
historical archive references and 1,401 surviving loose hashes, 98 protected
save names with independent backups, Save52 rehearsal copy, installed
EXE/ESM/PlanetData/SFSE/loader, definitions and configuration. Both 40,000,000,000-byte
caller-available disk floors passed. The old strict four-ZIP failure remains
historical. Independent review accepted the preflight before launch instruction.

Two startup identities appeared after that instruction:

| Process | Creation FILETIME | Observed disposition |
|---|---|---|
| Original PID 3424 | `134377114959040017` | Remained running; operator reported main menu with no save loaded. Admitted for science only after fresh READY and the deviation decision. |
| PID 6460 | `134377115353004155` | Exited before scientific admission. Its one acknowledged record is READY only. Exit cause is not established. |

The operator confirmed launching the loader more than once. Independent review
accepted original PID 3424's technical READY but escalated the one-process/card
deviation. The maintainer explicitly accepted that deviation and continuation
**only in the original process**, with no further launch/retry. Both startup
records and the historical escalation are retained. No exact count of all
possible loader invocations is inferred from two observed plugin streams.

A renewed fresh nonce ACK bound the approved DLL, original PID/creation,
eleven intact hooks, active capture and zero reported drops before Save52.
Lightweight admission checked all 98 protected local and 95 protected remote
save names/sizes without a full live rescan. `Plugins.txt` had only a changed
timestamp; its 480-byte content retained SHA-256
`8dac50493405250ab92feea55701a1ecb6fdf333703d9c152042262e5c26db33`.
That specific guard change was checked by hashing only the small changed file.
Independent continuation review accepted those gates before loading was cleared.

The maintainer then reported arrival at the second Feynman V outpost. The first
post-load health check found the recorder already retired with failure. Exact
failure timing relative to load/travel/arrival is not established: event records
have sequence numbers but no per-event wall clock, and no arrival ACK was issued
after the terminal file was discovered. The maintainer exited and disabled the
plugin through Vortex. Codex never launched, terminated, installed, enabled,
disabled or removed the game/plugin, and issued no gameplay/console/save command.

## Authenticated failure and scientific discrimination

The original terminal receipt reports `enqueued = written = flushed = 1592`,
`drops = 1`, `failed = true`, and resident inactive wrappers. Every admitted
record passes framing, sequence, payload CRC, identity and cumulative flush
receipt validation. The independent reader appropriately reports
`terminal loss/failure` and INCOMPLETE acquisition. That diagnostic does not mean
the retained bytes are corrupt. One reported drop is a lower bound on lost
coverage; subsequent disabled observations were not admitted or counted.

The bounded `emit` implementation uses the same drop counter for a full queue
and exhausted bounded CAS contention retries. The terminal record does not
identify which branch fired. Queue overflow is plausible, not uniquely proven.
The earlier [Phase A build13 overflow](d5p-report.md#preserved-failures-and-corrections)
shows a possible capacity failure, not the historical cause of this retail run.

| Captured kind/status | Count | Meaning within this record |
|---|---:|---|
| READY, status 0 | 1 | Startup transport record. |
| Lifetime fence, status 0 | 104 | Conservative invalidation events; not an exhaustive lifetime census. |
| Visited/source demand, status 1 | 319 | Every demand failed the read/context-invariant guard. |
| Lookup, status 3 | 11 | Context failure plus unavailable/unqualified pending context. Four raw lookup outputs differ from captured capacity; none is a source/lifetime-qualified hit. |
| Query / mask / completed, status 3 | 7 / 7 / 6 | Unqualified context persists. All seven raw mask bytes are 3; they do not establish the selected source's mask. |
| Temporary / append result, status 3 | 569 / 568 | Raw geometry observations remain unqualified. The last admitted record is an unmatched temporary record. |

Status 1 pools read, manager/type, Grid extent and membership checks. Individual
predicate operands and the first failed predicate are absent from this schema.
The existing bytes therefore cannot identify the exact native boundary that
failed qualification. This context failure is an independent limitation even
if admission loss were repaired. The reader's raw counters of four hit outputs
and 305 visited-positive observations must not be promoted to qualified hit-only
or selected-source bypass findings.

The bounded [offline analysis](../../../research/resource-retained-population/d5p_phase_b_analysis.py)
reuses the owned D5L/D5B chart-0 decoder, including manager-frame translation;
local source anchor words are not compared directly to geographic coordinates.
It finds seven raw geographic descriptor candidate groups, all with recorded
owner `0x0005e0de` and context failure. None matches the selected geographic/SFBK
key. These are diagnostic groupings, not certified source lifetimes. Missing
qualified target evidence plus failed coverage cannot establish target absence,
which query originally populated it, or whether a later request reused it.
No frozen mask, geometry, persistence or first-ever construction claim changes.

## Protection and cleanup

Full offline postflight passed thirteen explicit comparisons: policy content and
hash, protected local saves, Save52 identity, backups, archive guards,
definitions, configuration, installed inputs, restoration-copy identity,
protected remote inputs, target absence and deployed-DLL absence. The same
prospective policy treats active classified autosaves/exitsaves and
`remotecache.vdf` as diagnostic. No original was restored or overwritten.

The deployed DLL is absent and no Starfield process remained at the postflight
check. The approved DLL remains in Vortex staging, as expected after disablement.
The maintainer explicitly reports disablement in the same profile. An attempted
read-only Vortex UI inspection using the bundled computer-use/Sky tool exposed
only generic panes; screenshot capture timed out and the one allowed recovery
also timed out. Disabled UI state is therefore **operator-confirmed**, while
deployment absence and staging identity are directly verified. No Vortex setting
or file was changed by Codex; only a read-only window observation/activation was
attempted. The strict helper's removal-only absence branch was not falsely marked
passed; this uses the card's explicit reviewed disabled-state path.

## Outcome and remaining boundary

Scientific result: no answer to the selected-source hypothesis. Instrumentation
result: retail acquisition FAILED with a reported admission drop and unqualified
native context. Target outcome: operator-reported successful arrival and exit;
Codex observed process absence afterward. Protection/cleanup: PASS within the
stated direct-file and operator-confirmed disabled-state evidence. The duplicate
pre-load launch is an explicitly accepted deviation, not erased history.

The highest-information next work would record precise failing context operands
and per-admission failure reasons, then qualify sustained producer/worker behavior
before proposing another retail trial. That is a recommendation, not a new
implementation or launch authorization. The current approval is consumed;
no further live run, replacement observer, retry, integration, commit, push,
B6 or publication is authorized. [Independent review and exact delivery](d5p-phase-b-review.md)
govern acceptance of this faithful failed-run record, not acceptance of retail
reliability or the scientific hypothesis.
