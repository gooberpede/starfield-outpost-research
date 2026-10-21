# Third-Party Notices

This is an independent, unofficial research project. It is not affiliated with, endorsed by, or sponsored by Bethesda Game Studios, Bethesda Softworks, ZeniMax, Microsoft, or the authors of any tools or research it references. Names and marks remain with their respective rights holders.

The [project GPL grant](LICENSING.md) is limited to material the relevant project contributors have authority to license. It does not relicense Starfield/game-derived material, other people's implementations, private communications, or third-party software and marks.

## Material included at scaffold creation

- **GNU General Public License, version 3:** Copyright (C) 2007 Free Software Foundation, Inc. The complete licence document is included verbatim as [LICENSE](LICENSE), under its stated permission to distribute verbatim copies. See source `SOR-S-0002` in [SOURCES.md](docs/SOURCES.md).
- **User-supplied reference scaffold:** organizational reference for this requested scaffold, credited in [CREDITS.md](CREDITS.md). The old archive, engine-specific findings, proprietary content, and environment baseline are not redistributed here.

At scaffold creation no third-party implementation was bundled. The following later, narrowly approved incorporation supersedes that initial state.

## SOR-EXP-0002 approved SFSE interface header

[PluginAPI.h](runtime/exp0002/third_party/sfse/PluginAPI.h), copyright (c) 2023 Ian Patterson, from SFSE commit `48535cc4306ab345252bf740c20a1c6194929b0e`, is included under its explicit header-only MIT grant. The complete upstream [notice/licence](runtime/exp0002/third_party/sfse/LICENSE.txt) is retained and included in the local test package. User accepted this exact use on 2026-10-06; see SOR-P-0001 and SOR-S-0114. Header text is unmodified apart from LF normalization. This grant does not cover the SFSE runtime or other source. No SFSE DLL/loader, CommonLib code, Address Library database, sibling observer implementation, game content or compiler runtime is bundled.

## Future evidence and incorporations

SOR-EXP-0016 continues use of that exact unchanged SFSE public interface for the resumed research observer and includes its notice in the versioned package. Maintainer-authored sibling census/association patterns are adapted under the standing SOR-P-0002 exception, with [exact source provenance](docs/audits/live-beacon-observer.md) and SOR-S-0132. Embedded third-party sibling code/dependencies remain excluded. This does not incorporate SFSE runtime, CommonLib, Address Library, game bytes or compiler runtime binaries, or authorize publication.

Initial reconnaissance (2026-10-06) uses installed xEdit/Ghidra as separate tools and Bethesda development scripts/game data as local research inputs, under the invoked brief. That reconnaissance added original helpers and factual notes, not those tools, dependencies, scripts or raw exports. Game-derived outputs remain LOCAL-ONLY; authored summaries/identifiers remain subject to publication review. Source-reported mod behavior and documentation are attributed without incorporating implementations. See SOR-S-0101–0112 in [SOURCES.md](docs/SOURCES.md). No third-party code reuse decision was granted for that initial reconnaissance; the later header exception is recorded above.

Before adding outside material, record its origin, exact version, rights-holder permission, user approval, obligations, and publication status in [PERMISSIONS.md](docs/PERMISSIONS.md). Add applicable notices here without removing upstream notices.

Keep proprietary executables/DLLs, assets, raw saves, decompressed saves, imported analysis databases, memory dumps, private correspondence, and unreviewed bulk traces outside Git. Targeted game-derived evidence also needs a rights/privacy review; small size or local generation is not automatic clearance. Do not assert rightsholder approval unless it was actually obtained and its scope recorded.

## Conditional first-party evidence assets (B4)

**B4-F1 clarification, 2026-10-21:** first-party research saves/screenshots are
eligible under the maintainer's policy decision, informed by community practice;
this is not an express Bethesda/ZeniMax licence or assurance of no legal risk.
Missing individual written permission alone is not a first-party hold. Exact
provenance/privacy/utility checks govern local provisional preparation; final
membership and publication authorization remain separate. Character names and
historical workstation profile `User` are acceptable. The
[F1 policy and proposed assets](docs/audits/publication-readiness-b4/f1/README.md)
prospectively qualify the prior conditional text below, without granting rights
in underlying game content or relaxing donor/game-install/Git exclusions.

Raw saves remain outside Git. Only selected unchanged first-party originals may
be proposed as supplementary GitHub Release evidence after file-specific
privacy, underlying-content rights and maintainer selection approval, followed
by separate publication authorization. Save bytes may not be sanitized,
redacted, patched, rewritten or resaved; lossless archive compression preserves
original names/hashes and requires byte-exact reconstruction checks. Character
names alone do not disqualify a candidate. Donor originals remain excluded under
existing permissions. This narrow [policy integration](docs/PUBLICATION.md#conditional-first-party-original-save-evidence)
clears no file and grants no rights in Bethesda content. Publication NOT CLEARED.
