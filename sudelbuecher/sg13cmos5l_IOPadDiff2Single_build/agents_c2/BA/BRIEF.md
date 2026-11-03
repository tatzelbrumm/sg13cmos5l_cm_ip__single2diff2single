# Brief BA: backannotation of the drawn `sg13cmos5l_IOPadDiff2Single` pad cell (C2, 2026-11-03)

Workspace (yours only): `/home/user/c2/BA/` — `work/` is a full copy of the design repository (branch
`claude/c2-pad-layout`, with the new pad layout already in `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/`), which
you edit; `inputs/` read-only; `out/` your notes, checks and renders. The lead copies your changed files into the real
repository after checking them. No git commands. American English in everything you write.

## Goal (Christoph, verbatim)

"sg13cmos5_IOPadDiff2Single should correspond to the actual layout within the pad outline. backannotation of xschem
schematics, symbols, and CACE harnesses is to be expected."

So: the xschem sheet, the symbol and the source netlist of `sg13cmos5l_IOPadDiff2Single` describe exactly the drawn
cell — every drawn device, dummies included, and its ports — and everything that instantiates it is updated to keep
working with the old function.

## The truth to match

`inputs/pad_candidate.cdl` (subckt `sg13cmos5l_IOPadDiff2Single`): the reference netlist the layout passed IHP LVS
against, device for device (hierarchy of the layout cells, not of the sheets). The lead verified it equals the circuit
(the source netlists + Christoph's decisions) except for the added dummies. `inputs/netlist_changes.md` (agent F2) lists
what changed and why; `inputs/report_stageB.md` is F2's report; `inputs/decisions.md` holds Christoph's decisions.

## Changes

1. **Pad cell `macros/sg13cmos5l_IOPadDiff2Single/schematic/xschem/sg13cmos5l_IOPadDiff2Single.sch` / `.sym`:**
   - ports, in this order: `iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b` (the old `ibias en_1v2
     sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense` go; `iref` comes in);
   - remove `xc` (`en_ctrl_3v3`) and `xg` (`bias_gen_pd`); keep `xt` (`bias_tree_pd`, its sheet unchanged), `xd`, `xfp`,
     `xfn`, `DN`, `DP`;
   - **CMA / CMB (v8):** `CMA` gate `a`, D / S / bulk on new net `pa`; `CMB` gate on new net `pb`, D / S / bulk `b`;
     between `pad` and `pa`, and between `pad` and `pb`, an identical secondary stage: rppd `w=1u l=7.435u` (pad → node),
     `dantenna` `w=0.64u l=3.1u` (anode iovss, cathode node), `dpantenna` `w=0.64u l=4.98u` (anode node, cathode iovdd).
     Draw the stage once as its own sheet / symbol (e.g. `d2s_sp2k`) in the pad macro and instantiate it twice;
   - the dummies of the bias tree's layout (see the CDL: `bias_tree_n_f2`, `bias_tree_p_f2`) are devices of the pad sheet
     (rule: `bias_tree_pd`'s sheet stays unchanged in this task);
   - keep the drawing readable (the xschem-analog-schematic skill's style if you know it: no overlapping wires, labels
     instead of long wires).
2. **`d2s_mpdda_pd.sch` / `d2s_mpdda_pd.spice`:** finger counts and `ng` as drawn (SX / SY `w=36u ng=6`, PL / PR as 4
   fingers, PCL / PCR / CX / CY as 2, …); every dummy of the d2s cells as a device (tubs, tails, loads, casc_p, casc_n,
   sinks, ab_p, ab_n — from the CDL); XSA bulk `vdd`, XSB bulk `vss` (decided 2026-10-31); the two dummy rhigh strips
   (`vss vss vss rhigh w=0.5u l=12.65u`). The four bias diodes BP / BN / BPC / BNC stay in `bias_tree_pd` (flat LVS is the
   same either way; moving them is only a proposal).
3. **`unit_r2.sch` / `units.spice`:** the resistor as a chain of 4 rhigh segments `w=0.5u l=12.65u` as an xschem vector
   instance `XR[3:0]` (sa → n1 → n2 → n3 → sb), body vss — as drawn in `d2s_rhigh_f2`. Keep `rl` usable if the sheet
   parameterizes it; say what you did.
4. **Source netlists `macros/sg13cmos5l_IOPadDiff2Single/netlist/source/*.spice`:** the same changes, so that the
   sources and the sheets agree.
5. **Users of the pad symbol** (keep the old function by placing what left the cell next to it):
   - the 8 CACE templates `macros/sg13cmos5l_IOPadDiff2Single/verification/cace/templates/sg13cmos5l_IOPadDiff2Single_tb_*.sch`:
     add `en_ctrl_3v3` and `bias_gen_pd` instances wired as the old pad sheet wired them (ibias, en_1v2, sel0_1v2,
     sel1_1v2, vdd1v2_sense, vdd3v3_sense → en_3v3, en_3v3_b, sel*_3v3, iref), and the yaml's `pins:` section to the new
     ports (keep the template sources that drive the old pins, now driving the added instances);
   - `macros/slot/schematic/xschem/slot.sch` (`xd2s`) and the project top
     `schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sch` (`xoutbuf`): the same, minimal edits.
   - `d2s_mpdda_pd_sel.sch` (the loop fixture) uses `d2s_mpdda_pd` only: it changes only through change 2; check it still
     netlists.

## Checks (all measured, logs in `out/`)

- xschem netlists every changed sheet without errors (PDK xschemrc + the repo's; `export PDK_ROOT=/foss/pdks; source
  .designinit` in `work/`).
- **Pad sheet vs layout reference:** netlist `sg13cmos5l_IOPadDiff2Single.sch` (as LVS CDL: `make -C
  macros/sg13cmos5l_IOPadDiff2Single klayout-lvs-netlist`), then `python3 inputs/circuit_vs_cdl.py` comparing it with
  `inputs/pad_candidate.cdl` — flatten both (you may need to adapt the call: both sides are CDLs here; the script's
  "circuit" side takes SPICE top lines; or write a 20-line comparison of your own) — must agree device for device,
  dummies included (W per (model, L, D/S, G, B), diodes, resistors series-reduced).
- **Sheets vs source netlists:** each changed sheet's netlist against its source subckt (topology).
- **Users, before vs after:** `python3 scripts/xschem/sheet_equiv.py <old root> work` for slot.sch, the top sheet and the
  8 templates, with the old root = an untouched copy (`inputs/` has none: make one with `cp -a` of `work` before you edit,
  or use `/home/user/sg13cmos5l_cm_ip__single2diff2single` read-only — it holds the old sheets). Expected differences:
  only the intended ones (dummies, the two stages, CMA / CMB on pa / pb, the rhigh chain); list and explain each.
- Renders (PNG) of every changed sheet and symbol in `out/renders/`.
- Copies of every file you replace, as it was, in `out/macro_before/` (same relative paths).

## Deliverables

`out/changed_files.txt` (every file you changed or added, relative to the repo root), the checks above, `out/report.md`
(under ~100 lines; if the harness refuses to write it, put its text in your reply). Reply with a summary of no more than
12 lines. Do not report success you have not checked.

## Hard rules

Write only in `/home/user/c2/BA/`. No git, no web searches. Background commands under 2 h; kill by PID, never `pkill -f`.
