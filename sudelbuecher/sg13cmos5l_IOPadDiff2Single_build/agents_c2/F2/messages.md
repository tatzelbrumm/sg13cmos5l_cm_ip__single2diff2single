<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F2: messages

Agent F2 of session C2: assembly from the reviewed P2 / N2 primitives. Model Opus, effort high. Started by the lead on
2026-11-03 at 13:24 CET in the C2 cloud session (Christoph: "On second thought, resume, with my manual comments. You built
the instructions for F2 already. Launch."). Workspace `/home/user/c2/F2/` (`work/`, `out/`); `$D` = the design checkout
(`claude/c2-pad-layout`, 8a72dd8), `$N` = the notes checkout (`claude/c2-pad-layout-sudel`), both read-only for F2.
Brief: `BRIEF.md` here.

## 13:24, launch prompt (verbatim)

> You are agent F2, the floorplan and assembly agent for an analog pad cell on IHP sg13cmos5l. Your whole task is in the brief file `/home/user/c2/F2/BRIEF.md` — read it first and follow it exactly. Paths for this run: `$D` = `/home/user/sg13cmos5l_cm_ip__single2diff2single` (design checkout, branch claude/c2-pad-layout), `$N` = `/home/user/sudel` (notes checkout, branch claude/c2-pad-layout-sudel), `$W` = `/home/user/c2/F2` (your workspace: write only in `$W/work` and `$W/out`). `$D` and `$N` are read-only for you: never write, move or delete anything there, and run no git commands. PDK: `export PDK_ROOT=/foss/pdks` (`$PDK_ROOT/ihp-sg13cmos5l`); IHP's DRC and LVS decks resolve in this container. Do **stage A only**: place the reviewed P2 / N2 primitives and your reworked copies (pd_n, ab_n, moved TGN / TDN / TGP, tap rings where space allows, Christoph's review comments in the brief) bottom-up in the pad context, without routing; check every changed cell (DRC, LVS, sym_check.py); deliver `out/previews/placement_A.png`, the cells and a short note as the brief says. Then reply with a summary of no more than 15 lines and stop — Christoph reviews the placement before stage B.

## about 13:35, from the lead (summary; verbatim text in the session)

Christoph's decision verbatim ("CMA and CMB, symmetric with 2kΩ stage, …"): draw the stage in stage A instead of the
reserve — CMB's gate and CMA's pad-side plate each fed from the pad through rppd 1 × 7.435 µm (≈ 2 kΩ), with dantenna
0.64 × 3.1 to the substrate and dpantenna 0.64 × 4.98 to iovdd at the capacitor-side node; identical (mirrored) stages,
short wide pad feeds, ESD guard / ties, CMA / CMB still separate, the bias tree first; DRC incl. latch-up and antenna, LVS,
in the placement picture, and the sheet change for the backannotation.

## about 13:45, from the lead (summary; verbatim text in the session)

Christoph: "keep CMA and CMB polarity such that capacitance is maximal." Both turned (CMA gate on the pad side behind its
2 kΩ stage, S/D/NW on a; CMB gate on b, S/D/NW on the pad side behind its stage, CMB's well pad-driven with its own
guard ring); still separate; K checks the loop in parallel; list the sheet change.

## about 14:05, F2's stage A reply (summary)

Placement in the pad top, unrouted: bottom row CMA stage | loads | ab_p (+pd_p) | ab_n | pd_n | CMB stage (mirrored); PMOS
column left (casc_p, tails, inputs, bias_tree_p), NMOS / R right (casc_n R90 | sinks R90, rhigh, bias_tree_n). Cells 4931 of
6789 µm², free 1858 µm². Reworked pd_n, ab_n (NMOS twins of pd_p / ab_p), TGN / TDN / TGP moved, ab_p well tap a U, rings
around rhigh, casc_n, sinks; new `d2s_sp2k_f2` (2 kΩ stage). Turning CMA / CMB deferred to stage B. Answer on the sinks' centre
contacts: they carry BN's diode and the twin's ties; removable. Note: `stage_A_note.md`.

## the lead's check of stage A

Rebuild with `run_A.sh` byte-identical (cells and placement); `lead_check.py` on the 9 reworked / new cells: XOR empty, DRC
clean, LVS match, device sums equal (rhigh: series reduction); `sym_check.py`: 0 except sinks 0.0768 µm² (centre PCell, as N2)
and the bias trees (bbox axis shifted by the moved switches; rows unchanged against P2 / N2 per F2's row-window XOR);
run_drc.py on the whole placement clean, 0 exceptions; row check: all bands and rails pass, edges equal IOPadAnalog's.
