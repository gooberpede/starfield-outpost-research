# Prospective operator run card — review required

**No live/deployment authority is granted by this card.** EXP0021 prepares
SorBeaconObserver0.1.1; exact package/manifest/hashes and offline checks are in
the [review receipts](review.md). User controls Vortex and gameplay. No manual
DLL copy, native game call, native-save automation or debugger retry is included
in the passive session. Source saves stay protected; use separately archived
controlled copies and retain provenance. No overwrite of originals/active playthrough.

## Review and preflight

Review [contract](oracle-contract.md), [predictions](validation-protocol.md),
capture layout and package manifest. Separately authorize installation/load and
this finite operator sequence. User installs/enables the exact ZIP through
Vortex; ensure only the intended observer version is enabled. Confirm retail
hash, actual DLL/SFSE/module identities and output root on startup. Keep at least
40,000,000,000 available bytes on C: and D:; guard query failures stop output.
Disk/writer/integrity/runaway failures stop acquisition, preserving flushed files.
Partial/changed/unreadable components remain recorded and other collectors continue.

The extension performs no hooks/breakpoints or calls, but reads are non-atomic
and object lifetime unpinned. A scene change during census can yield mixed epochs.
Operator SETTLED is an attestation, not synchronization. Do not compare saved
frame against current terrain blindly. Record location, build-mode state,
travel/loading route, time state and deliberate actions for every label.

## Proposed first session

1. User loads controlled Save25 copy (starts at SOR-003). Await normal settling.
   Capture unique `oracle25-003-closed` outside build mode. Open build mode
   without placement, move, delete or edits; capture `oracle25-003-open` and
   a no-action `oracle25-003-control`. Close build mode; capture
   `oracle25-003-closed-after`. Wait for each complete/partial marker before
   another action. Preserve reset/inactive/stale flags instead of discarding them.
2. User travels to SOR-002 using an agreed route; log loading/frame changes.
   Repeat closed/open/control/closed-after with unique 002 labels. The switch
   tests which outpost supplies the stored center. Travel is a changed condition.
3. User loads controlled Save26 copy; reacquire all roots and associations after
   settling. Repeat SOR-003 and, if needed for identity control, SOR-002.
   This compares existing saved relocation; no new relocation or save is required.
4. Inspect raw hashes, classify before/after and freshness, then perform the frozen
   comparisons. If no usable stored output exists, report NOT_OBSERVED/STALE with
   supporting bytes. Do not expand into new gameplay or call queries automatically.
5. Request STOP, allow normal user exit, disable via Vortex; preserve session files
   and report game survival separately from evidence completeness. No process kill
   or source save cleanup is authorized. Critical review precedes any next round.

Example after the ready marker supplies the actual local session path:

```powershell
python -B runtime/beacon-observer/request.py '<session>' oracle25-003-open --settled
python -B runtime/beacon-observer/request.py '<session>' oracle25-003-control --settled
python -B runtime/beacon-observer/request.py '<session>' STOP
```

## Complementary trace, only if separately reviewed and authorized

The disposable adapter 0.1.0 has **no live mode**. A future live implementation
must verify executable/module/site bytes, attach only the independently identified
target, set one post-result INT3 at RVA ad0d3b, retain the contract's raw inputs/
output with thread/time provenance, auto-continue natural hits, and flush each
record. It must qualify code restoration, independent detach verification,
zero-hit/partial cleanup and target survival, and provide a tested recovery policy.
Use one finite agreed terrain/site scene sequence, not an arbitrary tiny hit quota.
No unreviewed function calls, memory/register changes, forced placement, native
saving or process termination. Breakpoint/attach effects must be disclosed.
Do not run it merely because the passive output differs: resolve identity/frame
first. The natural callback might never execute in the agreed scene. A complete
zero-hit record is useful reachability evidence, not an algorithm validation.
