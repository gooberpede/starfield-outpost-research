# Visibility, locks and construction admission

[Answer](report.md), [catalogue](catalogue.md), [SD2 prerequisites](../shared-outpost-storage/prerequisites.md).
Addresses/`nNNN` use the pinned static domain in [methods](methods.md).
This taxonomy describes evaluated mechanisms, not an exhaustive item-unlock list.

## Four distinct outcomes

| Outcome | Native/compiled distinction |
|---|---|
| Absent/hidden | Recipe never enters a category node, specialized category gate fails, list-index/child conditions fail, or ordinary recipe conditions fail and the restricted retry also fails. A category with no qualifying entries can itself be omitted. |
| Visible, unavailable | `1415795f0` retries a failed recipe through `1421f66c0` filtering HasPerk, GetPerkRank and IsResearchComplete command IDs `11c0/11fb/136a`; a surviving candidate is appended as unearned. Leaf descriptors independently carry build/skill requirement booleans. |
| Selected, rejected | Selecting a leaf creates the prospective item/preview, but ingredient, prerequisite, quota, budget and placement status can reject it. Card or grid visibility is not successful admission. |
| Constructed | Ordinary CommitEvent state handler requires accepted frame status 2, then enters the established Workshop creation/accounting path. This is static reachability, not a newly observed construction. |

`1421f6f00` builds condition context with **player subject** and selected Workshop
target. Each CTDA run-on controls which object is actually queried; run-on 2 can
name explicit player `00000014`. `140e466f0` ORs entries whose flag bit 1 is set
and ANDs completed groups with short circuiting; SD2's reviewed direct trace is
reused. Empty lists pass. Function indices in physical CTDA are u16 at +8;
the executable registration command adds `1000`. Adjacent padding bytes are not
part of the index. Flag bit 2 can make the comparison operand a GLOB identity,
so its bytes must not be interpreted as a numeric float threshold.

## Positive mechanisms and controls

| Mechanism | Real installed control and context | Consequence / precise limit |
|---|---|---|
| Discovery/menu suppression | FNAM absent on chair child COBJ `00100c57`; first-FNAM membership and recipe deleted flag test in `140f4d630` | Not a separately discovered root; it remains reachable inside the chair FLST. Root-list omission is separate from a failed condition. |
| Perks, ranks and compound AND | SD2 add-on local COBJ `02af79`: Management `23826f` ==4 AND Engineering `2c59e0` ==4, plus LocationOrParentHasKeyword `319847` ==0 | All three CTDA flags are zero. RQPK provides explicit rank requirements for UI/preview. Specific skill failure can be retained locked; location failure is not rescued by the perk/research filter. File-encoded add-on IDs are not universal runtime IDs. |
| Completed research | Large storage COBJ `002331e3`: IsResearchComplete `00389f13` ==1; chair child `00100c4c`: project `00100b8a` | Actual construction research gates, separate from automated-fabricator product selection. Filtered retry can retain unmet research while later prerequisite admission still fails. |
| Quest completion | Space Frog posters COBJ `000636e8`: GetQuestCompleted `0023f810` ==1 | Quest failure is outside the three-predicate retry: hidden under the mapped ordinary provider, not presented as a material shortage. |
| Quest stages / OR | Armillary mount COBJ `0023baa6`: GetStageDone on `002c6d74`, stage 510; `0024ef9c`, stage 10; `0006cd98`, stage 110 | Three entries carry OR bit 1. This supplies a real alternative-stage group; other Armillary state remains governed by its existing DA1 study. No universal quest scripting catalogue API is inferred. |
| Global state | Landing-pad COBJ `0006d72e`: GetGlobalValue `0006d73d` ==1 | Actual global condition, not a skill tooltip. Script changes to an operand may alter its next evaluation; no immediate synchronous menu refresh is promised. |
| Body/environment | Wind COBJ `0003023d`: BodyHasKeyword `00295eaa` ==0; nested P1 generator alternatives use body-conditioned selection | Ordinary wind visibility and variant choice are context-dependent. Separate L1 Planetary Habitation checks govern new beacon deployment; they are not this recipe's ingredient check. |
| House/ship context | Generic-case COBJ `00006d8e`: IsInSpaceship ==0, explicit player run-on; ship counterpart `002ef044` ==1 | Same category vocabulary can contain mutually contextual definitions. A physical recipe census includes both; it is not an exterior outpost menu snapshot. |
| Harvester availability | `1421f68f0`, n001; category default equality, resolved resource properties and selected-context availability arrays | Genuine native specialized gate, reused from the accepted availability map. A definition's presence does not establish currently obtainable local resources. |
| Organic facility feasibility | `1421f6bd0`, n001, and E2 `140f86060` | Builder-category candidates can be omitted by planet/species capability. Existing facility product-choice knowledge and construction gates remain distinct. |
| Materials | `1421f4c60`, candidate `1421dcb10`, SD2 source vectors/spending | Build requirement sufficiency is distinct from definition unlocks. Player/local/eligible shared inventory and consumer cost modifiers matter; arbitrary stock shortage is not a research lock. |
| Category quota | COBJ JNAM -> GLOB; L1 `140f3b170`; Transfer Container `002ce193` versus unquotaed small storage | Count matching construction representatives in the selected Workshop set, not all menu category peers. Status `1f`. |
| Build budget | L2 cached candidate charge plus effective used/allowed budget | Independent status `1e`, with scalar accounting rather than a catalogue-size cap. |
| Territory/support/collision | L3 current proposed position, world/location and physics/clearing | Territorial status `16` and intersection `04` are distinct; successful recipe conditions do not bypass either. |

The 204 first-FNAM roots reach 545 COBJ records through definition list/recipe
edges. Their direct CTDA vocabulary has six wire indices: `003b`, `004a`, `021f`,
`0338`, `035a`, `036a`. No direct faction predicate occurs in that bounded recipe
closure; no main-file direct rank predicate occurs there either. SD2's separately
pinned add-on is the positive multi-perk control. This says nothing universal
about faction-sensitive quests, general condition capability, other plugins,
non-COBJ list-index conditions or scripts. Native generic evaluator capability
without a qualifying installed example is not advertised as a new ordinary
catalogue mechanism.

Prerequisite construction/current Workshop state is positively supported by the
quota/member-set and ingredient-source consumers. A general installed
“build object X before furniture Y” recipe gate was not established by the
bounded CTDA closure. Crew stations can affect other state/capacity without
establishing such a catalogue prerequisite. Scripts can set globals, quest stages,
AVs or progression that consumers read, but are not thereby a native menu-edit API.

## Preview versus transaction

`1421dcb10` independently records ingredient sufficiency at frame +61d,
prerequisites at +61e and quota at +61f; L2 supplies the budget comparison.
`140f3f9a0` reduces these with preceding placement gates: unmet prerequisites
`1d`, ingredients `18`, quota `1f`, budget `1e`. Error precedence matters.
`1421b2360`/`1421b2e20` require status 2 before ordinary commit.
No atomic recheck inside every low-level creation or script interface is proven.
No actual perk-loss, stale-frame, failed-placement or unlock interaction ran here.
