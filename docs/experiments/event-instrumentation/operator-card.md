# Prospective operator card — no execution authority

SOR-EXP-0025; review required. External adapter0.1.2; observer0.1.1 unchanged.
This task did **not** run this card. Its reviewed successor must record the exact
tool SHA, target/SFSE/load-order identity, protected paths/hashes, allowed actions,
source-save handling, session boundaries, crash/recovery policy and timing risk.

## Proposed different sequence for review

The brief permits a debugger architecture. It has no plugin to deploy or install
through Vortex, so the usual “Vortex deployment → user smoke → installed preflight
→ review → scientific run” needs an explicitly reviewed variation:

1. Critically review the external adapter/source/ZIP, qualification and latency.
   Decide whether the all-stop pauses are acceptable for a bounded smoke test.
2. Separately authorize the exact live smoke/preflight card, including attachment,
   seven or two INT3 sites, owned single stepping, other-thread suspension and
   an OS break-in thread for STOP. User retains launch/load/actions/normal exit.
   Vortex remains sole owner of any existing SFSE/plugin deployment. No direct
   copying of DLLs or configuration to the game directory is proposed.
3. User launches the approved game/SFSE profile; preflight independently verifies
   executable/module identity, tool hash, free space, original loaded site bytes,
   protected Save25/26 copies and fresh session identity. No second debugger,
   conflicting site patch or unreviewed plugin change may be silently accepted.
4. Conduct the separately authorized smoke with center acquisition, then retire,
   verify code/detach and normal exit. Readiness is not scientific agreement.
5. Refine the scientific card with actual observed trigger/caller/latency evidence;
   return for review and explicit authorization before the scientific session.

No command below is executed in this task. Prospective adapter syntax after
approval is `adapter.exe --reviewed-retail PID ABSOLUTE_SESSION_ROOT GAME_SHA
--center-only` or `--center-and-grid`. Root must be a new session beneath ignored
`.local-work/event-oracle-live/`. Tool verifies the pinned game hash and loaded
32-byte guards. A fresh `READY` identifies installation, not sample authority.

## A — Center producing invocations

Protect original/archive Save25/26 as in Phase1; use reviewed controlled copies
and never overwrite original saves. Preserve baseline save inventory and hashes.
No native saving, new construction, beacon movement/deletion or forced native
query is allowed by this proposal. The moved003 case already exists in Save26.

Capture natural closed/open/settled/closed-after conditions for Save25/003 then
002 and Save26/003 then002, with positive workshop/base/body/frame association
and loading/travel/time-state notes. Keep recording across site switches so both
prior retained003 and refreshed002 conditions remain visible. Natural build
entry, border/descriptor updates and camera/clamp activity are plausible triggers
from the seven direct callers; build-open does not guarantee a call. Ordinary
view/camera changes within the reviewed movement scope may expose different
callers. No repeated intrusive native call is proposed to force a hit. Zero hits
remain NOT_OBSERVED and are useful trigger evidence.

Acquire broadly for the reviewed scene phases, not a small hit/file quota. One
or two sessions are preferred if the independently reviewed smoke supports the
method. Delineate finite operator phases by action completion and safe retirement;
this is not permission for indefinite unattended live collection.

## B — Grid callback, independently enabled

Enable only after the same tool/preimage/latency checks, separately from A.
Natural chain14077E350 →140AD92E0 →140AD08D0 →140B1E190 →140AD8EC0 →140AD0B90
is terrain/site candidate processing. Reviewed loading or travel among the two
existing sites is a plausible trigger; opening a workshop alone may never enter
it. Preserve callback entry/exit even when early return yields no grid result.
Do not place a new outpost, widen travel scope or invoke the callback artificially
to obtain a hit. If absent, report NOT_OBSERVED and propose the next specific
natural trigger for separate review. Center remains reportable independently.

## Frozen comparisons and classifications

Use the unchanged [frozen protocol](../engine-oracle/validation-protocol.md),
[inputs](../engine-oracle/inputs.json) and [predictions](../engine-oracle/predictions.json).
Inputs SHA9fe2924ff7bc444714fbab685893b8d8e0572dc2c7aad96cbd06de8aac93ad91;
predictions SHAa8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487.
The [contract correction](contract.md#correction-to-the-earlier-grid-acquisition-wording)
changes capture labels, not the predicted arithmetic or comparison tolerances.

| Cases | Expected center12 LE hex | Expected saved-frame cell |
|---|---|---|
| Save25/26 SOR-002 | a266f542eb858843efd19241 | [1,10465,21122] |
| Save25/26 SOR-003 | 0369b243f0b019457220ffc1 | [1,10467,21144] |

For A, require an actual paired invocation, ordinary base, concrete workshop
identifier and independently qualified Kreet/body/common frame. Decode native
binary32 XYZ and report per-axis exact bits and numerical differences from the
frozen case. Require all12 bytes equal; no epsilon or adjusted offsets. Save26/003
raw reference XYZ differs while native durable center is predicted invariant.
Missing identity/output is PARTIAL; unknown frame is UNASSESSED. Keep every
mismatch and distinct002/003 result; repeated equal calls are not new independent
samples. Radius is not a center-helper output and is not inferred here.

For B, independently associate the callback and its center child by scope, then
qualify captured source hierarchy, translation, body, resolution256 and settings
block12. Compare actual translated X/Y bits, native floor integers and final
hierarchy/tag/cell to the model replay of **captured native inputs**, in its fixed
float32 order. Z/local center remains separately labelled. Preserve opaque asset
handles; residual derived from captured intermediates is not a native output.
Only after saved-frame/current-frame reconciliation may a final cell be called
end-to-end saved-model agreement. Exact native-input replay, center agreement,
saved-frame grid equivalence and full-model validation are separate results.

## Stop, evidence and cleanup

STOP on user request, instrument safety/patch conflict, failed storage query,
caller-available space below40,000,000,000 bytes on either drive, genuine runaway
writer or broken evidence integrity. Optional unreadable science fields, unknown
values, absent calls, exceptions outside replay and missing partners continue as
partial evidence. Preserve every flushed stream and raw-section hash. At STOP
restore/verify original windows at a debug stop, clear owned TF, undo only owned
suspensions, detach independently, and let the user exit normally. Do not
terminate Starfield, suppress its exceptions or mutate saves. A post-capture
target crash and a pre-evidence crash have different scientific outcomes, but
both require disclosure. Record any debugger-induced failure and return for
review; no retry is automatic. Rehash protected inputs and frozen files after
exit; keep proprietary/raw data local.
