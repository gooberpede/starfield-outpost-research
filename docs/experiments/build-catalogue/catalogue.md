# Catalogue discovery, grouping and selection

[Answer](report.md), [methods and source domains](methods.md),
[definition controls](definitions.csv), [category inventory](categories.csv).
`nNNN` means `.local-work/build-catalogue/native/NNN.request.tsv`.
Addresses are hexadecimal preferred static VAs, image base `140000000`, on the
freshly hashed retail 1.16.244.0 executable. Object offsets are hexadecimal;
physical ESM offsets in CSVs are decimal. FormIDs below are main-file identities.

## Definition to category map

| Stage | Installed source and consumer | Consequence |
|---|---|---|
| Configure menu | DFOB `00058607`, WorkshopAllCategoryList_DO -> FLST `00058606`, OutpostRecipeCategories | Ordered list of 15 keyword positions; this is not a constant compiled array of 15 allowed categories. |
| Bind root | `140156700` and `1409e6c20`, n015/n016 | Default-object descriptor `145f09e60`, resolved-value slot +48 = `145f09ea8`. |
| Build/rebuild map | `1421ad290 -> 140f35940 -> 140f4d630`, n007/n006/n004 | Clear prior maps; walk loaded DataHandler's COBJ pointer vector (+ea8 count/+eb0 data under its lock). Require COBJ runtime type `97` and clear flag `20`. |
| Admit category | COBJ FNAM loader `140a02160`, n006 at `140a0239b..140a023a7`; map builder n004 | FNAM populates vector +150/+158. Only its first keyword is used here, and must be a member of the configured root list. BNAM is not a substitute for this test. |
| Construct node | `140f4cc70/ccf0/cf60/4d080`, n008 | Follow CNAM at +88. FLST runtime type `69`, nested COBJ `97` and leveled-list `3f` have distinct dispatches; ordinary buildable leaves must pass their form virtual predicate. |
| Populate tabs | `141578e50 -> 1421f6e40/6dc0`, n010/n006/n011 | Iterate configured category order and publish only categories with qualifying entries; current category is separately rebound. |
| Populate selected grid | `1415795f0 -> 141579fc0`, n001 | Resolve selected category's nodes, apply specialized/contextual and condition gates, build ordinary and unearned preview rows. |
| Expand prospective options | `14157eb30`, `14157a1c0`, `14157a740`, n002/n003 | Walk eligible list leaves/child recipes in order and append variant descriptors; select an actual leaf FormID. |
| Select and preview | `14171a050/a140`, `14171a1a0/a290`, `14171a2f0/a3e0`, n012–n016 | Grid selection, tab selection and variant cycling have separate callbacks; `1421bab50` queues NewItemEvent with node and selected form. |
| Request construction | Compiled ConfirmAction -> AttemptBuild -> `141719fb0 -> 1421f4ed0 -> 1421bb3d0` | Accepted global placement state produces CommitEvent. State handlers still require frame status 2; [UI](ui.md) and L1–L3 control the handoff. |

The freshly measured 546 BNAM-qualified COBJ records are a useful broad comparison
population, preserved in local survey.json, not the discovery count. Applying the
actual first-FNAM rule gives **204 physical root recipes**, including test and
ship-context definitions before filtering. Recursive CNAM/FLST traversal reaches
545 COBJ records. These counts have different inclusion criteria; neither is an
actual menu size or an exhaustive unlock inventory. [Methods](methods.md) records
the selected-type terminal boundary and the correction from BNAM reconnaissance.

## Concrete sub-item controls

| Root recipe -> ordered target list | Physical list entries | Demonstrated distinction |
|---|---:|---|
| Chair `00296338` -> FLST `00296339` | 35 | Root flag `04000000`; first direct FURN `0002f42d`, later child COBJ `00100c57` -> FURN `0012a735`. Child has BNAM Furniture but no FNAM, so is not separately admitted by first-FNAM discovery. |
| Sleeping bags `002951f9` -> FLST `00259f5c` | 4 | Four prospective FURN forms, beginning `000e03f5`; root remains one grouped icon. |
| Small tables `00293ad1` -> FLST `00293ae0` | 27 | Mix of direct forms and child recipes; root flag preserves list as variants. |
| Small solid storage `00299547` -> CONT `0023aed9` | One direct target | No recipe CTDA/RQPK/JNAM; it still needs materials and valid placement. |
| Four Wall Hab's construction and BM1 wall STBH `001e8d95` | Different graph | Constructing a root PKIN and cycling a placed component's Snap Behavior are separate operations. |

With `04000000` set on the owning recipe, `140f4ccf0`/`140f4cf60` allocates a
single WorkshopMenuNodeBuildableObject for a list. Without it, the helper descends
the list and builds separate nodes, evaluating per-index condition entries where
present. Nested COBJ follows its own target; direct leaves retain the enclosing
recipe's costs/conditions. `14157eb30` checks list-index condition maps and child
recipe conditions before admitting a concrete option. There is no need to invent
a furniture-specific hardcoded bed/chair/table submenu.

`141579fc0` uses the list's FormID as icon/group identity, while variants have
concrete leaf FormIDs. `14157a740` supplies each leaf's name, image, requirement
booleans and ordinal/count text. `1421a6810` stores the current leaf; changing
direction wraps its index within the eligible variant count. These transient
selection IDs are not saved reference handles. See ui.md for the exact compiled
consumer and callbacks.

Category order comes from the root list. Within a category, `140f4e7f0` records
original positions and `140f4ecd0`/`140f4e760` compare recipe +94 binary32 sort
values, resolving equal keys with those recorded positions. This is not an
alphabetical sort. Ordinary list leaves retain the traversed list order subject
to conditions. Actual equal-key order depends on the loaded registration vector;
a physical file traversal is not a reconstructed load-order merge. The sort
consumer is established independently of a universal editor-field interpretation.

## Structural limits and the 1,000/2,000 question

| Population | Inspected representation/consumer | Supported limit statement |
|---|---|---|
| Categories | FLST +38 u32 count/+40 pointer; provider loops to that count | Definition length and dynamic publication; 15 is the installed sample, not a fixed compiled maximum. |
| Category buckets | Hash slots stride `18`; node list u32 count/capacity/data | Dynamic insertion, no detected 1,000/2,000 cutoff. |
| Native nodes | Allocated `30`-byte buildable node; eight-byte pointer list | `1422cc0d0` grows through allocator callbacks and returns `ffffffff` on failure; not an unbounded append promise. |
| Published grid/variant arrays | Owned begin/end/capacity vectors; preview stride `130`; variant data is nested | Explicit growth helpers, no detected small fixed population cap in the mapped provider. |
| Current variant | u32 count/index helpers and wrap logic | Finite representation; width alone is not a supported numerical menu ceiling. |
| Compiled interface | BuildPopupContainer iterates `aCategories`/`aPreviewIcons`; WorkshopUtils walks `aObjectVariants` | Data-driven loops, not a 1,000-entry hardcoded table. Viewport size and card skill/description limits concern presentation, not catalogue population. |

Leveled-list dispatch reads a byte-sized entry count in its own structure. That
does not limit an ordinary FLST furniture catalogue to that width. Likewise the
event factory's template parameter 512 describes event registration machinery,
not the number of construction candidates. Neither is a demonstrated menu cap.
Allocator growth, finite arithmetic, recursion/cycles and practical UI/assets
remain bounded; no stress test or maximum safe count is claimed.
