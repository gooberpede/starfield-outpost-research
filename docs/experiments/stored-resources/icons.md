# Resource icon provenance

[Answer](report.md), [row contract](provider.md), [methods/source hashes](methods.md).
These are STATIC installed-definition and compiled-asset joins, not a new rendered
game observation. No raw artwork is included in tracked documentation.

## Item -> resource metadata -> icon

Physical item association reaches an **IRES** resource (`141350b10`, n017).
**141351790** (n015/n016) constructs its metadata:

| Native source | Meaning in the bound row | Installed loader support |
|---|---|---|
| IRES+28 | uResourceID | Resource form identity, distinct from physical MISC |
| IRES+38 full-name interface | sResourceName | Resource FULL/localized label |
| IRES+d0 via 14064a770 | sSymbol | NNAM localized symbol; helper strips an initial `<ID=` localization wrapper |
| IRES+d8 | sArtName | GNAM selector string |
| IRES+110, only values below 5 retained | uRarity | SNAM low byte; otherwise metadata rarity defaults to 0 |
| Symbol nonempty -> 1409e7890 -> packed color | uResourceColor | TINC RGB channels at +e0/e4/e8; all-zero channels use rarity palette |

**1409e7900** (n026) is the IRES loader: GNAM writes +d8, NNAM loads the
localized string at +d0, SNAM sets +110, and TINC expands the packed channel
bytes into floats. **141350a00** carries these into the metadata structure;
**14135d210** binds their exact field names (n018/n019). The game does not choose
this icon from a physical item's MODL mesh or dynamically render its inventory
portrait. Category keywords alone do not select the clip.

ABC **1288 SetupStoredResourceIcon** uses `uResourceColor == 0` to select the
OrganicIcon branch, including manufactured resources. It requests `sArtName`,
or **Generic** if the selector is empty. Otherwise it passes sSymbol/color/rarity
to **PlanetInfoResourceIcon.SetResource**, ABC **910**, which draws the localized
symbol, transforms its background color, and applies rarity/tracked indicators.
The branch name OrganicIcon therefore does not prove the item is organic.

## Exact installed joins

Both movies below are members of the freshly pinned installed
**Data/Starfield - Interface.ba2**. See ui-source01/assets01/planet-assets01 and
localization01 under the local evidence root; [sources.csv](sources.csv) binds
their hashes. FormIDs here are local to Starfield.esm.

| Physical item -> IRES | Selector | Referenced installed asset / reproducible metadata |
|---|---|---|
| Iron `00556e -> 0057c7` | NNAM string `000081f7` = **Fe**; TINC bytes `75403a00`, nonempty symbol -> color branch | **interface/planetinfocard.swf**, SymbolClass **Components.PlanetInfoCard.PlanetInfoResourceIcon**, character **18**; text/background/rarity composite, not unique Iron texture |
| Adhesive `0055b1 -> 077828` | GNAM **Adhesive**, empty symbol -> zero resource-color branch | **interface/organicicons.swf**, SymbolClass **Adhesive**, character **174** |
| Amino Acids `0055cd -> 07782a` | GNAM **AminoAcids**, empty symbol | Same movie, SymbolClass **AminoAcids**, character **107** |
| Adaptive Frame `246b6a -> 245775` | GNAM **StructuralFrame**, empty symbol | Same movie, SymbolClass **StructuralFrame**, character **141** |
| Empty art selector in zero-color branch | **Generic** | Same movie, SymbolClass **Generic**, character **15** |

The actual Locations movie imports **PlanetInfoCard.swf** through ImportAssets2
at decompressed movie offset **4512**. Its PlaceObject3 at **10487** creates
`Components.PlanetInfoCard.PlanetInfoResourceIcon` with instance name
**InorganicIcon_mc**; the companion **OrganicIcon_mc** uses local character 117
in the same row sprite 118. This is icon linkage metadata, not a layout analysis.
The complete Locations SWF is 90,354 bytes, SHA-256
`3977612bf4f8285ac6dfed149a8ce01c23ac8ccc5e8c1673be40434978c4998d`.

ABC **1254** owns an OrganicIcons shared library. **148 LibraryLoaderConfig**
selects library name **OrganicIcons** and default clip **Generic**;
**483 LibraryLoader** appends `.swf`. **487 LoadClip** asks that loaded movie's
application domain for the named class and instantiates it. **1222/1225** manage
the row clip and completion. These are vector/timeline symbols in compiled SWFs,
not an atlas of per-item PNGs or BA2 texture filenames.

## Fallback boundaries

Empty sArtName explicitly requests Generic. The loader also contains null-class,
alternate-name and configured-default branches; a library not loaded returns no
clip until its completion path. **No exception handler is present in ABC 487**
(02.json preserves exception tables). Consequently a nonexistent named definition
must not be promised to reach Generic if getDefinition throws; runtime exception
behavior was not executed. The provider restricts ordinary rows to associated
IRES data, so unsupported physical item classes ordinarily fail before icon
selection. Zero/nonempty-symbol color anomalies remain conditional on the
actual native metadata, not a guessed category fallback.

The screenshots show Fe/Iron and mixed resources consistent with this contract.
Their build, localization configuration, underlying inventories and epochs are
unpaired; they do not validate exact current assets, totals or fallback execution.
