# Construction Winner package name

2026-11-01. The maintainer requests an instrument name and version for the ZIP
shown in Vortex. The operator-facing archive is now
**`SorConstructionWinner-0.4.0.zip`** at
[the versioned package location](../../../.local-work/d5ab/p4-versioned-package01/SorConstructionWinner-0.4.0.zip).

This follows the existing `SorBeaconObserver-0.1.1.zip` and
`SorNativePositionOracle-0.7.0.zip` naming convention. Construction Winner's
existing `SFSEPlugin_Version` value is `0x00040000`, corresponding to 0.4.0;
the name therefore reflects the instrument's existing version. It does not
renumber or rebuild the DLL. Future instrument patches should advance that
instrument version and archive name together.

The named ZIP is a byte-for-byte copy of the qualified Package02 archive,
not a rebuilt archive. Its SHA-256 remains
`9c7a4a4d220948b3dac877b783487abc8ec65be026117158e1e883c35592d2cf`.
The retained naming receipt records source/destination identities, ZIP member
hashes, DLL identity and the original package/plan hashes at
`.local-work/d5ab/p4-versioned-package01/naming-receipt.json`.

The original qualified staging directory, ZIP, plan, manifest and helper-source
pins remain unchanged. Canonical operations still use the exact plan and tools
in the [B2 card](run-card-d5x-b2.md); this ZIP contains the install files, not
the Python controller/helper bundle. The [corrected readiness assessment](d5ab-p4-optimization-correction.md)
and its authorization limits remain in force. Naming does not authorize
deployment, Starfield launch or B2, and does not alter Vortex's existing state.
