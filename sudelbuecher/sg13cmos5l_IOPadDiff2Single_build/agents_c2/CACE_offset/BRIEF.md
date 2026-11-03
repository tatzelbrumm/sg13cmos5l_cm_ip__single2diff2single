<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief (proposal, not yet run): loop gain of the IOPadDiff2Single driver over the output swing in CACE

Prepared 2026-11-03 by the C2 lead at Christoph's request ("prepare the proposal for an agentic claude run"). For a
later agent run; in C2 itself the swing-end check is folded into the short simulation sanity check.

## Why

CACE's loop groups of the pad driver (`macros/sg13cmos5l_IOPadDiff2Single/verification/cace/d2s_mpdda_pd_sel.yaml`:
`loop_params`, `loop_load_params`, `loop_1nF_params`, `loop_sel_params`) sweep only `cload`, `rload` (and `sel`). The
pad output always sits at vref (1.65 V). Agent K of C2 (`agents_c2/K/report.md`, stages 4 and 6) swept the pad over
0.94–2.29 V and found the loop changes with the output voltage, worst at the top (sourcing half, OP dominant):
- gain margin 16.8 dB at pad 2.29 V (limit 15);
- phase margin 39.7° at 300 pF unloaded, pad 2.29 V (limit 40; 42.2° at mid-rail).
CACE sees neither. Christoph (2026-11-02): "The small signal poles and zeros depend on output voltage, and the
consequences may get overlooked by just standard AC analysis at output voltage=output reference voltage".

## The change

1. **Template** `verification/cace/templates/d2s_mpdda_pd_sel_tb_loop.sch`, block SOURCES. Today the differential
   input is zero:
   ```
   Vic vic 0 CACE\{vicm=1.65\}
   Ep vinp vic 0 0 0.5
   En vinn vic 0 0 -0.5
   ```
   Add a differential input `vd` and drive the two E sources from it:
   ```
   Vd vd 0 CACE\{vd=0\}
   Ep vinp vic vd 0 0.5
   En vinn vic vd 0 -0.5
   ```
   (pad − vref = vd / 2 in closed loop; the loop is opened at vfb through Lb 1 GH / Cb 1 F, so the DC operating point
   still follows the closed loop.) Pick device names that differ from every existing one by more than case (ngspice-47
   stops on `XRP1` / `XRp1`-type clashes).
2. **yaml:** add `vd: enumerate: [-1.3, 0, 1.3]` to the `conditions` of `loop_params` and `loop_load_params` (pad ≈ 1.0 /
   1.65 / 2.3 V), keep the limits (PM ≥ 40 under load, GM ≥ 15, fc ≥ 0.8 MHz), and add a `PM_vs_vd` plot. Leave
   `loop_1nF_params` (report only) and `loop_sel_params` unchanged unless the run time allows.
3. Results to `verification/cace/results/d2s_mpdda_pd_sel/` as the Makefile's `sim-cace` writes them (CSV + summary).

## How to run and check

- Environment: Claude Code cloud environment `sg13cmos5l` (claude-cloud-config). `/foss/setup.log` needs `CACE_OK`,
  `OSDI_OK`; `export PDK_ROOT=/foss/pdks; source .designinit`.
- Run the **unchanged** template once first (`cace d2s_mpdda_pd_sel.yaml -s schematic -p loop_load_params`) and compare
  with the committed CSV; then the changed one. Always `-s schematic` (CLAUDE.md traps).
- Grep every ngspice log for `Transient op started` and `Timestep too small` (C1: a failed op falls back to a transient
  op, gives plausible wrong numbers, and CACE still reports pass).
- Expected with the sheet of `toplevel` 8a72dd8 (K's deck 13, not CACE): PM ≈ 39.7° at 300 pF, vd = +1.3 — a FAIL that
  is the point of the change. With the C2 backannotation (CMA / CMB turned, symmetric 2 kΩ stages, if adopted) the
  numbers move; run after that integration and say which sheet was used.
- Report: a table of fc / PM / GM per (cload, rload, vd), against K's numbers; any FAIL stated plainly.

## Scope and git

- Files: the template and the yaml above, the new results; nothing else.
- Branch: the C2 design branch `claude/c2-pad-layout` (or a branch Christoph names); commit and push; no pull request.
- Model: Sonnet, effort medium, is enough (a small, mechanical change plus one CACE run); Opus if the run needs
  convergence work.
