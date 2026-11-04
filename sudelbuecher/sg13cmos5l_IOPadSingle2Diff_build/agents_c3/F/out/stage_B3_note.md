# Stage B3 note: net y off the left edge stub (F, C3, 2026-11-04)

[M] = measured in this run; everything else is reasoning.

**The net is y.** In stage B2 its left detour ran M2 up x 3.09–3.38 to y 149.46, left to x 0.66, down to 140.6, then
a Metal1 jumper x 1.47–1.76 from 140.865 down to 117.92 (Via1 at 0.71,140.625 and 1.52,117.97), then M2 down x
1.47–1.76 to 104.96. That jumper ran 0.27 µm from the edge-stub M1 (x 0–1.20) over 22.7 µm [M].

**Change.** I removed the jumper and both Via1s and the M2 piece at x 0.66–0.95. The descent is now one Metal2
column, x 1.81–2.07 (0.26 wide), y 117.92–149.46, inside the left reserve, where M2 is allowed. It meets the
unchanged lower M2 with a jog at y 117.92–118.21. It is 0.21 µm (M2.b) from the template M2 strip at x 1.30–1.60,
and 0.21 µm from the M2 at x 2.28. So y has no Metal1 left of x 4.3 now. The template M2 strip (x 1.30–1.60,
y 118.55–148.8) is why y used Metal1 here: it blocks the old M2 track at x 1.47.

**How.** Rerouting would not do. I added the edge keep-out (no router M1 at x < 1.8 / > 78.2) and tried a full
reroute, then incremental reroutes with B2's wiring fixed and 1 to 18 nets ripped. Each one left 1 to 7 nets
unrouted [M]. So `src/patch_y.py` edits stage B2's routed `s2d_block` directly. `src/run_B3.sh` rebuilds the pad
from `stageB2_v1/` (patch, then fix_block, build_pad, compose_cdl). XOR of the pad against stage B2 [M]: only
Metal1, Via1 and Metal2 differ, all inside x 0.66–2.07, y 117.92–149.46. Everything else is as routed in B2,
including the pad line, the shields, vbp, vbnc and the pwr_f iovdd rail tie.

**Lengths of y** (`logs/y_B3.md`, net_metrics) [M]:

| | M1 | M2 | total |
|---|---:|---:|---:|
| B2 | 44.7 µm | 101.2 µm | 145.9 µm |
| B3 | 21.0 µm | 122.8 µm | 143.8 µm |

**Checks** (`logs/summary_B.txt`) [M]. Every B2 line is unchanged:
- Cells: DRC, maximal, LVS and XOR as in B2.
- Pad: run_drc.py found no violations (30 tables, 0 exception lines); the maximal deck plus latch-up has 0 errors.
- Deep LVS matches. The circuit check is EQUAL. The reserve holds 0 µm² of buffer device layers or M1.
- Template unchanged. row_check passes 25 of 25 with 0 edges DIFFERENT. PEX has 28 capacitor-only nodes, as in B2.

New row DRC on `row/row.gds`, top cell `row`, added to `src/checks_B.sh` [M]:
- run_drc.py --no_density: "No DRC violations detected", 0 exception lines.
- Maximal deck with latch-up: 0 errors.

A geometry check finds no buffer M1 within 0.6 µm of either edge-stub M1 band. B2 had the jumper there; B3 has
nothing [M].

**CDL unchanged.** `pad_candidate.cdl` is byte-identical to B2, sha256 ec55fc18348d… [M]. See netlist_changes.md §6.

**Kept.** Stage B2 is kept as `out/stageB2_v1/`. In `messages.md`, point 14 explains why I hand-edited instead of
rerouting.
