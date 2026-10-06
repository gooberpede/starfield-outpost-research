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

Initial reconnaissance (2026-10-06) uses installed xEdit/Ghidra as separate tools and Bethesda development scripts/game data as local research inputs, under the invoked brief. That reconnaissance added original helpers and factual notes, not those tools, dependencies, scripts or raw exports. Game-derived outputs remain LOCAL-ONLY; authored summaries/identifiers remain subject to publication review. Source-reported mod behavior and documentation are attributed without incorporating implementations. See SOR-S-0101–0112 in [SOURCES.md](docs/SOURCES.md). No third-party code reuse decision was granted for that initial reconnaissance; the later header exception is recorded above.

Before adding outside material, record its origin, exact version, rights-holder permission, user approval, obligations, and publication status in [PERMISSIONS.md](docs/PERMISSIONS.md). Add applicable notices here without removing upstream notices.

Keep proprietary executables/DLLs, assets, raw saves, decompressed saves, imported analysis databases, memory dumps, private correspondence, and unreviewed bulk traces outside Git. Targeted game-derived evidence also needs a rights/privacy review; small size or local generation is not automatic clearance. Do not assert rightsholder approval unless it was actually obtained and its scope recorded.
