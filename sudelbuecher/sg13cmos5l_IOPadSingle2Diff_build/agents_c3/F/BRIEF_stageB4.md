<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief F, stage B4: P's input band with vfbp / vdd swapped (C3, 2026-11-04, lead)

`BRIEF.md`, `BRIEF_stageB.md`, `BRIEF_stageB2.md` and `BRIEF_stageB3.md` still apply. B3 is now the macro cell
(design commit bba4aba).

## What changed in P's cell

- **Who and why:** Christoph, 2026-11-04: "go ahead with the vin/vdd track swap". In stage B2's PEX, vin coupled
  5.7 fF to vfbp, the output.
- **The change:** the lead changed one line of P's `build_s2d_p3.py` (`yb`, the gate-band order of `s2d_inputs_c3`).
  Bottom to top it is now `vref vfbn vcm vfbp vdd vin`; before, it was `vref vfbn vcm vdd vfbp vin`.
- **The new files:** `inputs_B4/P/s2d_p3_cells.gds` / `.cdl` / `build_s2d_p3.py`.
- **Lead checks of the cell** [M]:
  - only `s2d_inputs_c3` differs (M1 gate tabs and Via1); every other cell has XOR 0;
  - the CDL is byte-identical;
  - DRC 0 (run_drc.py, and maximal with latch-up), deep LVS PASS, sym_check SYMMETRIC;
  - PEX of the cell alone: vin – vfbp 5.65 → 0.29 fF, vin – vdd 0.50 → 5.86 fF.
- **Pins:** in cell coordinates, the vfbp pin is now M2 (0, 13.31; 0.5, 13.57) and vdd is (0, 13.79; 0.5, 14.05). They
  were the other way round. All six tracks still run the full band width. Every other pin is unchanged.

## What to do

1. Rebuild with `inputs_B4/P` in place of `inputs/P`, and keep everything of B3 that the swap does not touch. The
   pad line still lands on the vin track, which has not moved.
2. Reconnect vfbp and vdd to their swapped tracks. Choose the method: a local patch as in B3, or a reroute of only
   these nets. Report the before / after lengths of vfbp, vdd and outp.
3. Nothing else moves: placement, the pad line and shields, vbp, vbnc, the y detour of B3, the reserve, and the
   `pwr_f` rail tie.
4. **Coupling check on the result:** in the PEX you already run, vin – vfbp (outp) must stay ≤ 1 fF at the pad
   level, and nothing new beside the pad line.

## Checks and deliverables

- Every stage B3 check, including the row DRC.
- The CDL changes only if the cell CDL changed (it did not), so say "unchanged".

Overwrite `pad_candidate.gds` / `.cdl`, and keep B3 as `out/stageB3_v1/`. Write `stage_B4_note.md` (≤ 40 lines).
Reply with at most 10 lines and the file list with sha256, and stop.
