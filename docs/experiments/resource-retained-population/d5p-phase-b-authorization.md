# D5P Phase B authorization — one conditional session

2026-10-29, Australia/Sydney. [Approved card](run-card-d5p-v1.md),
[accepted Phase A review](d5p-review.md).

The maintainer supplied this instruction in the current chat:

> Thanks Codex. The plugin and phase B run card are approved, subject to successful preflight. I have installed the plugin under the Vortex profile 'Starfield - SFSE'. Steam Cloud saves are disabled for Starfield, and the game has not been launched. Please proceed when you're ready. Finalization tasks must include independent review and diff generation before returning. Do not commit or push changes, thank you.

This approves one session under the unchanged v1 card, conditional on successful
fresh preflight. The maintainer owns launch through `sfse_loader.exe`, gameplay
and Vortex installation/removal or disablement. Codex owns read-only preflight,
plugin-generated evidence/nonce verification, permitted session STOP requests,
offline analysis, postflight, independent review and exact diff delivery.
No save load is cleared until the post-launch READY gate passes.

The approved ZIP SHA-256 is
`6bf7b00f3bbe98f8a1140169d0661c46c9cd6a03462a81c6807cf7d1f650b85a`;
DLL SHA-256 is
`935071691f6325f99d1f8ec99056349d6eb5fee19dba237cffd6e7d7833650cc`.
The exact card hash and verbatim authority are retained in
`.local-work/d5p/phase-b-authorization-v1.json`. The private start receipt is
`.local-work/d5p-phase-b/start.json`.

The operator confirms the profile name, disabled Steam Cloud saves and no prior
launch for this attempt. Profile selection is operator-confirmed, not claimed
as a decoded Vortex database observation. Read-only file checks identify the
same approved DLL in the Vortex staging and game deployment paths and no other
deployed SFSE plugin DLL. All 26 accepted Phase A files matched their reviewed
hashes at task start. The repository now has maintainer-integrated HEAD
`3f2e3481e25b5ef2a4594b424b03e3ee5180694f`; the earlier Phase A HEAD binding
remains historical. The current task began with a clean working tree.

No automatic launch, retry, alternate source/mask/target, forced generation,
cache clearing, console command, save/configuration mutation, exception
suppression, game termination, Vortex change, staging, commit, push, B6 or
publication is authorized. A post-capture crash may leave valid durable evidence;
it does not waive protection or postflight. The original card's NOT AUTHORIZED
label records its prospective Phase A status; this separate conditional approval
does not rewrite that historical document.

## Frozen execution and finalization criteria

| ID | Required outcome |
|---|---|
| B1 | Exact approved card/package/deployed DLL and installed prerequisites, successful fresh protected-input/save/backup preflight, both disk floors and recorded operator Cloud/profile confirmation before launch. |
| B2 | One maintainer-launched SFSE process; fresh plugin identity, eleven-hook READY and nonce ACK accepted before Save52 load; only the approved ordinary target sequence. Failure closes acquisition without automatic retry or game termination. |
| B3 | Authenticate raw/flush evidence and classify complete region chains, partial/contrary/hit-only/bypass results or incomplete acquisition at their actual strength. Positive confirmation is not required; missing coverage cannot establish absence. |
| B4 | After target exit, verify protected inputs and evidence, both disk floors and maintainer removal or reviewed disabled-state evidence for Vortex/deployed paths. Preserve originals and report residue; Codex never removes the plugin. |
| B5 | Retain authority, execution/failure and provenance records, final scientific/engineering/editorial independent dispositions, exact status/inclusion/exclusion manifests and verified complete/task-only diffs. No staging, commit, push or publication. |

During play, health checks read only lightweight startup/ACK/terminal/control
receipts, process identity and disk metadata. No full protected-input scan or
bulk raw decode runs during ordinary gameplay without a specific integrity
incident. The existing reviewed READY command authenticates its initial prefix;
full scientific reduction is offline after exit. Session nonce/STOP writes stay
inside the exact new plugin session. No general 0.7.0/0.8.0 session adapter is
assumed compatible with D5P's distinct protocol.

## Accepted pre-load launch deviation

After the launch instruction, the plugin created startup sessions for original
PID 3424, creation FILETIME `134377114959040017`, and PID 6460, creation FILETIME
`134377115353004155`. The latter exited; the former remained at the operator's
reported main menu with no save loaded. Both authenticated startup prefixes
contain only one READY record and no scientific observations. The maintainer
confirmed: **“I launched the loader more than once.”** The cause of the second
process's exit is not established by those receipts.

Independent review accepted original PID 3424's fresh eleven-hook READY/ACK but
escalated the duplicate launch under the immutable one-process/no-retry card.
The maintainer then explicitly answered **“Accept the deviation and continue only
the original process”** to the narrow continuation request, which expressly
permits no further launch or retry. This accepts the documented pre-load
deviation without rewriting the card or treating the second process as an
admitted scientific target. Continuation is restricted to original PID 3424 and
its exact creation identity after a renewed fresh READY check. If it exits,
there is no authority to select another process.

The exact question/answer and original authority binding are retained in
`.local-work/d5p/phase-b-authorization-v1-continuation.json`. Both startup
records and the historical escalation remain preserved locally.
