<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Notes for the assembly agent F (pad_ref_rb), collected by the lead

To be folded into F's brief, after the rule sections copied verbatim from C3's F brief.

1. **rb_tree_n's switches** (Christoph, 2026-11-07): "F may decide to move the small rb_tree_n transistors out of the
   guard ring to save area. Then again, there's plenty of room on the slot7 bottom. But it's still good (and
   consistent) practice to keep layout compact, if only for matching purposes."
   - TGN and TDN (1u/0.45u) sit inside rb_tree_n's ring at its two ends (as TGN / TDN in the pad's tree row).
   - TGP is in rb_tree_p, at the end of the PMOS tree row.
2. **Compactness counts** for matching, not only for area. Report each assembled block's area against the row sum
   (N 3953 µm², P rows, rb_avg 120 µm²) and against the 85 × 85 µm estimate.
3. **rb_avg** (P3): two wells, translated rows; pins gh (top), m (both sides), xp (bottom); no vdd.
4. **rb_casc stays as drawn (A)** (Christoph, 2026-11-07, after the sketches of alternatives B / C in
   `lead/rb_casc_alternatives.png`): "keep A for matching. On slot7, we have area to waste." The pad's 8-slot block with
   BNC in the middle, 3 spare 15/3 dummies and the 2/3 end dummies, band tracks as dummies on vdd. Do not trim it.
5. **Christoph's answers before launch** (2026-11-07, verbatim): "Might be a good idea to move the small transistors
   in rb_tree_n and rb_tree_p out of the main transistors' guard ring. Not a must." / "Look at where the voltages
   are needed by the custom pads. The replica bias block should end up close, and routing should be easy." / "Try
   to reproduce the connection sequence of the slot7 boundary to the custom pads." / "Don't stretch the connections
   out unnecessarily to match the slot-to-custom-pads boundaries." / "Pin names vddh and vssh, to they can be
   connected without conflict either way." / "Pad structures are only routed M1/M2. Let's keep it that way for
   consistency." Folded into BRIEF_F.md rules 5, 6, 9.
6. **Stage A is a throwaway** (Christoph, 2026-11-07, while F ran stage A): "Expect to COMPLETELY throw away stage A
   placement and do routing driven placement." F was told to keep stage A light (no row compaction, a quick placement
   and the context picture) and to deliver what a routing-driven placement needs: a pin map per cell, the net list
   with fan-out and sensitive lines, the facing edges per net, and a routing-order / layer-direction / channel
   proposal for stage B.
7. **No distinct stages** (Christoph, 2026-11-07, right after 6): "THERE ARE NO DISTINCT STAGES." Supersedes the
   stage A / B split of BRIEF_F.md and note 6. F was told to place and route as one process, routing driving the
   placement, to a routed pad_ref_rb (M1 / M2, DRC and flat LVS clean against the circuit with every dummy, vddh /
   vssh), with progress lines in `reports/F_progress.md`.
8. **Freedom to rework the rows** (Christoph, 2026-11-07): "F has the freedom to tweak the inputs from the specialist
   agents as compact placement and routing requires, within good circuit layout judgment as has been demonstrated
   with the oa and bg cores, and the custom diff2single and single2diff pads." Passed to F with the four layouts as
   precedent (oa_core_pd, bg_core_pd, both pad cells). The lead kept one standing decision: rb_casc's 8-slot
   structure ("keep A for matching"); its ring, pins, straps and band may change. Every device added, removed or
   re-tied goes into F's CDL and note for backannotation.
9. **"The inputs" = layout primitives** (Christoph, 2026-11-07): "where 'the inputs' means layout primitives. Could be
   confused with input pins. They can be moved within reason, too, but the overall connectivity and I/O and power
   pins of the entire macro must be preserved." Passed to F: the macro keeps exactly vddh, vssh, vref, vcm, en_3v3,
   en_3v3_b, iref (names, directions, boundary order); pins may move within reason; connectivity checked by flat LVS.
10. **Review of F's first routed cell** (Christoph, 2026-11-07, verbatim): "There's ABSOLUTELY NO GOOD REASON to bring
    the terminal lines close together and not route them straight out, given that the distance of the pad
    connections is further apart. There's also ABSOLUTELY NO GOOD REASON to place the replica bias generator next to
    the VSS1V2 pin at the bottom right. This building block should be near the top right, where we need to sort out
    how to place it relative to the bias sources and the (to be laid out) bias_dist_pd network that connects these
    blocks together. And yes, the layout should be MUCH more compact." Both the bunched pins (1.08 µm pitch) and the
    bottom-right position came from the lead's brief (rule 5), not from F. Next: position decided with Christoph
    (`lead/slot_right_options.png`), then F reworks the cell.
