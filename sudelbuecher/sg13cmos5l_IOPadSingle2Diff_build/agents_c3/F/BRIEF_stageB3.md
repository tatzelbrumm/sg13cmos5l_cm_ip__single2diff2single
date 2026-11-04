<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief F, stage B3: one M1.f in the abutted row (C3, 2026-11-04, lead)

`BRIEF.md`, `BRIEF_stageB.md` and `BRIEF_stageB2.md` still apply. Christoph accepted B2 as "good enough to proceed
to phase 4". The lead's phase 4 found one rule violation that only shows when the cell is abutted.

## Finding [M]

- **Setup:** IHP `run_drc.py --no_density --mp=4` on the row from C2's `row_check.py`: Filler1000 | IOPadAnalog |
  PAD | Filler200 | IOPadIOVdd | PAD | Filler1000.
- **Result:** 1 item, **M1.f** (Metal1 space 0.6 µm when one line is wider than 10 µm with a parallel run over
  10 µm), in `s2d_block`.
- **The two edges:**
  - the template's left edge stub, Metal1 x 0–1.20, y 84–140.17 (global; cell `edge_stubs`);
  - a router Metal1 jumper of `s2d_block`, global polygon (1.47,117.92; 1.47,140.575; 0.66,140.575;
    0.66,140.865; 1.76,140.865; 1.76,117.92), Via1 at both ends (1.52,117.97) and (0.71,140.625).
- **Spacing:** 0.27 µm, with a 22.7 µm parallel run.
- **Why only in the row:** alone, the stub is 1.2 µm wide. Abutted, it merges with IOPadAnalog's (or a filler's)
  edge Metal1 into a line wider than 10 µm, so M1.f applies.
- **The cell itself:** DRC is clean on both decks, and the row's maximal deck with latch-up shows 0 (it has no M1.f
  check at this level).
- The right edge has no item.

## What to change

1. Take that jumper off Metal1 next to the stub. Rule for the whole cell: no buffer Metal1 within 0.6 µm of any
   edge-stub Metal1 band (x 0–1.2 and 78.8–80), over a parallel run of more than 10 µm.
   - x 1.8–4.3 / 75.7–78.2 stays free of Metal1 (the reserve).
   - So the net needs another path: Metal2, which is allowed in the reserve, or another route.
   - Say which net it is.
2. Add a row DRC to `src/checks_B.sh`: C2's `row_check.py` builds `row/row.gds`, then `run_drc.py --no_density` on
   it (top cell `row`) and the maximal deck with latch-up. Both must be 0. The script is at
   `/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/row_check.py`
   (read-only; usage in its docstring).
3. Leave everything else as routed. The B2 pad line, shields, vbp and vbnc stay, and so does the `pwr_f` iovdd rail
   tie: the lead moves it into its own cell after you.

## Checks and deliverables

- Every stage B2 check, plus the row DRC (both decks).
- The before / after lengths of the net you move.

Overwrite `pad_candidate.gds` / `.cdl` (the CDL should not change: say so), and keep B2 as `out/stageB2_v1/`. Write
`stage_B3_note.md` (under ~40 lines; the harness may refuse names starting with `report`). Reply with at most 10 lines
and the file list with sha256, and stop.
