# Netlist changes the layout implies (agent F, C2 2026-10-31, final at stage 3, 18:45 CET)

For the lead's backannotation.
- "Proposal" marks a change to a sheet that stays unchanged in this task (rule 4).
- The reference that LVS matched is `cells/d2s_block.cdl` and `pad_candidate.cdl`, one line per drawn device.
- Items 1–5 come from P's and N's reports (their cells are used unchanged); items 6–10 are F's.

## d2s_mpdda_pd (sheet `d2s_mpdda_pd.sch`, `d2s_mpdda_pd.spice`)

1. **Tails (P):**
   - New dummies, all with D = S = vdd and G = vbp: 2 × 0.3/6 and 1 × 5/6. The library had 3 × 5/6.
   - BP is now the right end of row 2.
   - Unit A's two tails see different row ends (a narrow dummy on one side, BP on the other). Unit B is the mirror
     image (P, [r]).
2. **Input tubs (P):**
   - The 4 dummy tubs are 10/1 ng=1, with G = D = S = well = vdd.
   - The real tubs are unchanged (20/1 ng=2).
3. **casc_p (P):**
   - PCL and PCR are each 2 × 15/3 stacked in one column (same W 30 / L 3). The interleave was dropped (P6).
   - BPC 1/4 plus a 1/4 dummy with its gate on vbpc.
4. **Sinks and casc_n (N):**
   - XSX / XSY: `w=36u l=6u ng=4` becomes 6 fingers of 6/6 each (layout_primitives §7 decision 1).
   - Sink dummies: 3 × 2/6 (D = S = vss, G = vbn); the library had 3 × 6/6.
   - BN is one 6/6 finger in the sink column.
   - casc_n: CX CX | CY CY replaces the cross map; devices unchanged (CX / CY 2 × 15/3, BNC 1/8).
5. **Class AB and power-down (P, N):**
   - RP1 / RN1 are not in d2s_mpdda_pd; they are in the clamp frames (d2s_out.spice).
   - Disable switches:
     - XSA: source on vddo, **bulk vddo → vdd**.
     - XSB: source on vsso, **bulk vsso → vss**.
     - XSABP / XSABN: sources on vdd / vss.
     - Lead's decisions of 17:45 and 17:57.
6. **unit_r2's resistor** (`XR sa sb vss rhigh w=0.5u l={rl}`, rl = 50.6u):
   - Drawn as 4 series segments of rhigh w 0.5 × l 12.65 µm in `d2s_rhigh`, map of §5. Total length 50.6 µm, as in the
     sheet.
   - Every segment has its own two heads, so R is a little above one 50.6 µm device. It is the same in all four units,
     so the gain is unaffected [r]. Re-simulate Gm.
   - Backannotate as a chain `XR[3:0]` with nodes sa, R_1, R_2, R_3, sb.
   - Plus two dummy segments with both ends on vss: `XRdummy[1:0] vss vss vss rhigh w=0.5u l=12.65u`.
   - Magic PEX (EXT_MODE=2) finds 18 capacitor-only nodes, one per segment. Use `pex_for_sim.py --tie` for simulations.
7. **Bias diodes in the front end:** BP (tails), BN (sinks), BPC (casc_p) and BNC (casc_n) become devices of
   d2s_mpdda_pd. layout_primitives §7 decision 4; this is the counterpart of item 8.

## bias_tree_pd (proposal; sheet unchanged)

8. **Remove `Xd ... bias_diodes`** from the bias_tree_pd sheet; they are in the front end (item 7). Add the library
   dummies as devices:
   - `MNdummy vss ni vss vss sg13_hv_nmos w=2.4u l=6u`
   - `MPdummy vdd vbp vdd vdd sg13_hv_pmos w=2u l=6u`
   - Until the sheets change, the pad's flat LVS sees the same devices and connections as the present sheets (lead's
     decision).

## Pad level (sg13cmos5l_IOPadDiff2Single.spice / .sch)

9. **CMA / CMB:** `w=7.96u l=32.16u ng=1`, one unit each, unchanged.
   - CMB's gate is fed from one P-comb pad line (x 72.465) instead of eleven. The circuit is unchanged.
   - The CMB-stage reserve (report §6) is not drawn and changes nothing yet.
10. **Ports as in C2 phase 1 §1.7** (`iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b`; Xc / Xg in the
    slot).
    - vfb = pad, as a Kelvin line from the junction.
    - The pad-level reference the layout matched is `pad_candidate.cdl`. Diodes are written as IHP's LVS extracts the
      DCN / DCP PCells: dantenna / dpantenna, m = 2, A / P as drawn by A1.
