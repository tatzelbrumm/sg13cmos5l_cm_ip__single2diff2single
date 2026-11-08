<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief R: survey of row-closing cells (fill / decap / endcap / tap) and 3.3 V logic and switch cells (cloud session C4, 2026-11-08)

You are agent R, a research agent. Diligence, not creativity: find, list, measure and cite. Change no design file.

## Why

bias_dist_pd (`/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/bias_dist_pd/`, layout
`layout/klayout/bias_dist_pd.klay.gds`, README "Layout") has a "switch row": one standard-cell-like row of 3.3 V (hv,
thick-oxide) nand2 / inverter / transmission-gate slices between two tie strips (p+ to vssh at the bottom, n+ in the
NWell to vddh at the top), open at both row ends. Christoph, the designer: "Are you aware of some standard cell capacitor
fill cells and endcap cells? So far, the well and substrate strips of the row of logic and transmission gates look quite
good, but if we want something like closed guards around the stripes, it might make sense to look into them." The
project's layout rules ask for "taps as rings where space allows". Find what already exists that could close the row
(endcaps, tap cells), fill its gaps (fill / decap cells), or replace our hand-drawn hv gates.

## Sources (read only)

1. **The PDK:** `/foss/pdks/ihp-sg13cmos5l/libs.ref/` (`sg13cmos5l_stdcell`: gds, lef, cdl, doc; `sg13cmos5l_io`)
   and `/foss/pdks/ihp-sg13cmos5l/libs.tech/`. The stdcell LEF has `sg13cmos5l_decap_4/8`, `fill_1/2/4/8`,
   `antennanp`, `tiehi/lo`: find out their device type (1.2 V lv or 3.3 V hv), size, row height, how wells and
   substrate are tied (in the cells, by tap cells, or not at all), and whether the PDK has endcap or tap cells or a
   rule (deck / document) that asks for them. Same questions for the IO library's filler / spacer cells.
2. **The Chipalooza harness:** `/home/user/rtimothyedwards/sg13cmos5l_ocd_chipalooza` (upstream, shallow clone of main)
   and `/home/user/tatzelbrumm/sg13cmos5l_ocd_chipalooza` (Christoph's fork). The fork's branches for the slot project
   (fetch each with `git -C <clone> fetch --depth 1 origin <branch>` and read it with `git show` / `git ls-tree` or a
   worktree in your workspace): `custom-pad-test`, `claude/slot7-stage-a`, `claude/c6-submodule-pads`,
   `claude/c5-testplatform-test`, `delivery-test`, `tatzelbranch`, `ruth`, `gzippedgds`, `version_hell`, `main`.
   Look for 3.3 V logic cells, transmission gates, level shifters, analog switches, and any standard-cell-style rows with
   fill / decap / endcap / tap cells, in Magic (`.mag`) or GDS. The harness's IP repositories, if referenced as
   submodules or in docs, may be cloned read-only into your workspace (public GitHub, anonymous clone:
   `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 <url> <your workspace>/<name>`), e.g.
   `RTimothyEdwards/sg13cmos5l_ocd_ip__analog_switches` and the bias generator's repository.
3. **Already in our repository** (for comparison): `macros/ocd_analog_switches/` (KLayout copies of the harness's
   analog switches, xgate, sw_lvl_shift, with a README), `macros/ls_up_1v2_3v3`, `macros/ls_dn_3v3_1v2`,
   `macros/hv_logic` (sheets only), and `tatzelbrumm/sg13cmos5l_cm_ip__shared_levelshifters` (public; clone read-only
   into your workspace if you need it).

Do not open `tatzelbrumm/sg13cmos5l_cm_slot7`.

## Deliverables (in `$WS/out/`), then stop

- `survey.md` (under ~150 lines):
  - a table of every candidate cell with: name, source (repo, branch, commit, path), kind (fill / decap / endcap / tap /
    tie / logic / TG / switch / level shifter), voltage class (lv 1.2 V / hv 3.3 V, by the devices in it), size and
    row height, how it ties well / substrate, layout format, and the DRC / LVS status stated in its source;
  - what the PDK says about endcaps / taps / fill (documents and deck rules, cited by file and rule name);
  - options to close the guard around our switch row (e.g. hv endcap cells, a closed tie ring, tap cells, fill / decap
    in the row gaps), each with its source and what it would need; no recommendation beyond what the facts support.
- `previews/`: a PNG of each relevant candidate cell, rendered from its GDS with klayout's Python module (`klayout.db`)
  and matplotlib, device layers + metal, with its size.
- Mark measured facts [M] and statements taken from documents [D] with their citation; reasoning [R].

## Hard rules

- Read only. Never run the external repositories' scripts, Makefiles, xschemrc or Magic / KLayout macros; read their
  files as text and their GDS with `klayout.db` only. Never push anything, anywhere.
- Write only in `$WS` = `/tmp/claude-0/-home-user-sg13cmos5l-cm-ip--single2diff2single/f7165478-7787-531e-a1d8-6ec7206ebfcb/scratchpad/layout_rb/R`
  (`work/`, `out/`) and the report `../reports/R_report.md`. The fetches into the two harness clones above are allowed
  (they only add refs).
- No `mcp__*` tools, no web browsing beyond the git clones / fetches named here. Name yourself "Claude, agent R" in
  files, never a model name. American English. Kill processes by PID only. If an action is refused or blocked, stop
  that step and report it.
