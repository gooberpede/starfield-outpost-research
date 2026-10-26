# Cargo routine verification cutover

**ACTIVE for Cargo following separate execution approval, 2026-10-26.** The
[execution report](execution.md) and [active selection](active-baseline.json)
replace the loose 1,051-member routine boundary with archive/index plus three
unchanged holds. Use the selection's pinned qualified `routine_command`; baseline
and journal must agree on COMMITTED. No global or saved-file protection changes.

## Historical proposal

The original proposal below records its implementation-stage authority and
remains preserved. Its inactive label was superseded only for the exact Cargo
transaction documented above, not for another owner, archive version or operation.

**PROPOSED / INACTIVE.** The [brief](../../implementation-briefs/CODEX_BRIEF_SOR_archived_evidence_resolution_cargo_cutover.md)
authorizes a demonstration, not activation. Existing mandatory preservation rules,
save protection and historical failed verdicts remain unchanged.

After separate approval of the exact retirement set and baseline version, replace
the 1,051 Cargo member rows in the proposed routine Cargo boundary with one
externally pinned archive object and its externally pinned central index. Keep
the three unarchived packager holds as individual loose objects. Authenticate
each archive/index once per required pre/post verification boundary; share that
result within the boundary rather than rehashing it per constituent member.
The shadow schema is `sor-preservation-shadow/1`; its prior rows and independent
canonical prior-baseline hash support exact rollback while originals survive.
Existing archive/index rows are matched and replaced once, preventing duplication.

Historical member hashes and original relative paths remain in the authenticated
inventory. Scientific use requires explicit restoration, complete archive/member
verification and rereading the selected working bytes against the original pins.
An ephemeral restoration is never automatically enrolled as permanent history.
Relevant original-save/backup, installed-content, analysis-project and high-risk
live-session protections remain separate, stronger checks under their own briefs.

The 93,334-pin D5G inventory and 12,974-row protected manifest contain no Cargo
member paths. This proposal therefore claims no savings in either inventory and
does not rewrite them. Its measured comparison is the Stage B Cargo boundary:
1,054 loose objects versus three holds plus two archival/control objects. Routine
per-member checks for the proposed retired set fall to zero in that model.
Programme-wide reduction of at least 80% remains a future migration objective;
the earlier preservation-optimization AC4 remains FAIL / REWORK.

Archive hashing detects corruption only in objects actually hashed at that
boundary. It does not prevent later corruption or establish integrity of unrelated
archives. Propose a full archive/member audit after each new archival publication,
before a retirement decision, after a storage incident or suspected corruption,
and at a separately agreed periodic maintenance interval. No automation or period
is activated here. Archive and original-source equality must be checked again
immediately before any separately approved retirement.

No journal is an authority for expected hashes or missing-source absence. Missing,
swapped, truncated or corrupt objects, substituted indices, baseline mismatch,
orphaned membership and ambiguous journal states fail closed. Once originals are
retired, recovery depends on the authenticated archive and any separately approved
replica; the old loose baseline cannot be called verified until exact restored
originals actually exist and pass their pins. One local archive is vulnerable to
drive loss. No off-device backup or second lasting replica is claimed.
