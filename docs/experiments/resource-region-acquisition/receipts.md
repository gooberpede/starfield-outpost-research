# Prospective raw receipts and negative-result semantics

[Plan](plan.md). Schema `sor-rg2c1a-manual/1`; never fabricate a live example.
Raw receipts and pixels stay local. Unique session/sample IDs are task-local,
not new global SOR evidence IDs. Original video plus operator log is primary;
an extracted JSON is an authored derivative, linked by hashes and frame ranges.

| Record | Required fields / domain |
|---|---|
| Session | session_id; authority/run-card hash; EXE version/hash; actual plugin/load-order/settings manifest hashes; source and working save hashes; protected-input manifest; UTC and local offset, monotonic/video time basis; capture software/version/settings; frame size/FOV/camera; operator; load/travel/pause/menu/exit log; disk and isolation test receipts |
| Identity | body plugin/FormID, Workshop bytes, saved beacon/parent/extractor tokens, base and IRES with plugin qualification; save record offset/domain; offline join receipt hash; visual-map and continuous identity frames; operator confirmation; status EXACT_SAVED_JOIN_AND_VISUAL / SITE_ONLY / UNKNOWN. Runtime handles/pointers remain null/unobserved |
| Sample | sample_id; session_id; case_id C1-IL/C1-CU/C1-FE; epoch_label PRE/NO_ACTION/POST_RELOAD; action sequence number; monotonic start/end; wall UTC; video hash/frame span; still hashes; UI mode; selected resource/base label; body/site/extractor evidence references |
| Geometry registration | saved anchor XYZ/chart with provenance; original screen landmark feature definitions and before/after pixel pairs, resolution, direct per-feature pixel displacements without warping/fitting, independent reader check; same-view status; query_world_xyz=null unless independently measured; positional_uncertainty_native=null; source_frame/actual_radius/upper=null unless measured. Null means UNOBSERVED, never zero |
| Observation | list PRESENT / NOT_LISTED / UNREADABLE; ground PRESENT / NOT_DETECTED / UNREADABLE / NOT_TESTED; preview ACCEPTABLE / BLOCKED / UNREADABLE / NOT_TESTED; all rejection text, resource label, card and visible color references; occlusion and region-of-interest coverage. NOT_DETECTED applies only to that visible ROI and mode, never the whole site |
| Transition | pair_id; before/after sample IDs; stationary control IDs; declared reload/save/travel sequence with hashes; state of player/menu/loading/time/weather; known confounders; native_population_epoch=null. A reload label is an observed action epoch, not a native cache epoch |
| Integrity | ordered chunk/frame ranges, per-file hash/size, dropped-frame and gap ranges including UNKNOWN loss, flush/close state, operator deviations, abort reason and postflight; completeness is separate from target survival |

Successful negative: “IL NOT_LISTED in this fully scrolled readable menu at P3
in sample X” or “no IL ground overlay detected in this unobscured ROI under
the selected mode”. It requires a matched visible resource label/mode, complete
stated ROI, positive Cu procedure control and integrity/identity receipts.
It never means no IL at P3 or no serialized/native IL. BLOCKED is neither negative
resource nor ACCEPTABLE. ACCEPTABLE is a displayed preview, not a captured native
return or successful construction. A displayed hourly rate is not measured output.

Preview NOT_TESTED, clipped/occluded pixels, missing frames, unreadable labels,
identity ambiguity, unregistered views or loss during a transition are retained.
The affected comparison is UNKNOWN. A surviving complete earlier group remains
evidence, even if a later capture fails. Keep operation loss distinct from a
native empty set or loop exhaustion; no native loop was observed in this route.

The [offline prototype](../../../research/resource-region-acquisition/receipt_gate.py)
checks an intentionally smaller **classification envelope**, not this entire raw
schema. Its synthetic fixtures test refusal to convert blocked/missing/wrong-site
observations into absence, and refusal to compare an unregistered reload pair.
It does not authenticate video, verify hashes against files, establish scientific
identity or implement the live capture. Raw-to-envelope derivation requires human
review of the above primary records. No PASS from it certifies game safety.
