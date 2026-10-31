# Netlist changes implied by the layout (agent F; started at stage 2, 2026-10-31 17:50 CET)

For the lead's backannotation. "Proposal" = a sheet that stays unchanged in this task (rule 4).

1. **unit_r2's resistor (units.spice, `XR sa sb vss rhigh w=0.5u l={rl}`, rl = 50.6u).**
   - Drawn as 4 series rhigh segments of w 0.5 × l 12.65 µm per unit, in d2s_rhigh, map of layout_primitives §5.
   - Total length 50.6 µm, as in the sheet. Each segment has its own two heads, so R is a little above one 50.6 µm
     device (same in all four units, gain unaffected) [r].
   - Backannotate as a chain `XR[3:0]` (xschem vector instance) with nodes sa, R_1, R_2, R_3, sb.
   - Two dummy segments, both ends on vss: `XRdummy[1:0] vss vss vss rhigh w=0.5u l=12.65u`.
2. **bias_tree_pd (proposal, sheet unchanged).** Remove `Xd ... bias_diodes` from the sheet. BP / BN / BPC / BNC are
   drawn in the tails, sinks and cascode cells (lead's decision 17:01), so they move to d2s_mpdda_pd (layout_primitives
   §7 decision 4). The library dummies become devices of the tree:
   - `MNdummy vss ni vss vss sg13_hv_nmos w=2.4u l=6u`
   - `MPdummy vdd vbp vdd vdd sg13_hv_pmos w=2u l=6u`
3. **CMA / CMB** (sg13cmos5l_IOPadDiff2Single.spice): unchanged, `w=7.96u l=32.16u ng=1`, one unit each.
   - CMA keeps its own region, now inside a p+ ring (iovss); there is no new device for the ring.
4. **XSB's bulk** (d2s_mpdda_pd): vsso → vss (one substrate; lead's decision 17:45).
   **XSA's bulk**: vddo → vdd, if P draws SA in the shared iovdd NWell.
   - SB's source stays on vsso, SA's on vddo.
