<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C0: oa_core_pd PEX in a cloud session, report

2026-10-30, Claude Code cloud session, environment `sg13cmos5l`. Brief: `C0_oa_core_pd_pex.md`.
Design branch `claude/c0-oa-core-pd-pex` (from `toplevel` 1903407; outputs in 82a57ec), notes branch
`claude/c0-oa-core-pd-pex-sudel` (from `sudel_buecher` 3acf926). Container times below are UTC; the
MANIFEST rows are in CET (UTC+1), like the rest of that file.

**Result:** every target passes. DRC clean, LVS match (28 devices, 22 nets), all four PEX netlists with
all ports connected, each target under 1.1 s. The setup script had been cut off before its last lines;
running those lines by hand was the only environment change needed.

## Toolchain and setup

| tool | version |
|---|---|
| `klayout -b -v` | KLayout 0.30.12 (`/usr/bin/klayout`, the klayout.org .deb); PyPI `klayout` 0.30.12 |
| `magic -dnull -noconsole --version` | 8.3.685 |
| netgen | 1.5.324 |
| `xschem --version` | 3.4.8RC |
| `ngspice -v` | ngspice-47 |
| `kpex --version` | 0.6.8 |
| `/usr/local/bin/sak-*` | 18 scripts (chipart-install, chipart, clean, dffram-install, dffram, drc, gds-xor, layconv, lvs, open, pdk-script, pex, pin-reorder, render, sch2svg, spice-model-red, v2svg, vlint) |
| IHP-Open-PDK | `df4c5054ee8ca481c3eb873687274f28cdb50b1e` |

`/foss/setup.log`, seconds after the script's start (17:14:07): APT_OK 38, PIP_OK 73, SAK_OK 73,
PDK_OK 79, NETGEN_OK 83, MAGIC_OK 106, XSCHEM_OK 112, OPENVAF_OK 170, NGSPICE_OK 289. **No OSDI_OK and no
SETUP_DONE.** The log stops at 17:19:02 (about 295 s), right after `Finished building psp103.va`, which
is the first model of the OSDI compile. It shows no error and no process was left running, so the script
was stopped from outside, probably at a time limit, not by a failing command. The VM of this session
booted at 17:20:33 from that state. As a result, the lines after `wait` never ran, except the first
model of the OSDI compile:

- OSDI compile: only `psp103.osdi` exists in `libs.tech/ngspice/osdi`. I didn't finish it; no target here
  simulates.
- `chmod +x $F/tools/sak/*`: `sak-pin-reorder.py` had no exec bit (the other `sak-*` files did).
- kpex wrapper: `kpex` was still pip's original.
- symlinks into `/usr/local/bin`: magic, netgen, xschem, ngspice and `sak-*` weren't on PATH.
- `rm -rf $F/src`: the build trees are still in `/foss/src`.

## Environment adaptations

1. Before any target: ran the setup script's kpex-wrapper line and its symlink loop, verbatim.
2. After `magic-pex` failed (below): `chmod +x /foss/tools/sak/*`, the setup script's line.
3. Cloned `github.com/tatzelbrumm/sg13cmos5l_ocd_chipalooza` read-only (`--depth 1`, HEAD ac5ef9e,
   2026-10-20) to `/home/user/tatzelbrumm/` for the harness comparison. Nothing pushed there.

**Setup-script fix:** move the OSDI compile after the chmod, wrapper and symlink lines, or put it in the
background, so that what DRC/LVS/PEX need finishes well inside the time limit.

No schematic, GDS, Makefile or `scripts/` file was edited. `git status` after the runs showed only the
nine new outputs.

## Targets

All from `macros/oa_core_pd` after `source .designinit`, each with `SCRIPTS_DIR=../../scripts`, tee'd to
`sudelbuecher/logs/claude/c0-oa-core-pd-pex/`.

| target | result | wall time |
|---|---|---|
| `magic-drc` | clean | 0.58 s |
| `magic-lvs-netlist` | written | 0.42 s |
| `magic-lvs` | match (below) | 0.37 s |
| `magic-pex EXT_MODE=1`, 2, 3, first try | **exit 2**: `sak-pin-reorder.py: Permission denied` (environment, see above); logs `*.try1.*` | 0.25 / 0.25 / 0.38 s |
| `magic-pex EXT_MODE=1` | all ports connected | 0.34 s |
| `magic-pex EXT_MODE=2` | all ports connected | 0.43 s |
| `magic-pex EXT_MODE=3` | all ports connected | 0.59 s |
| `klayout-pex EXT_MODE=2` | all ports connected; deprecation warning for the missing subcommand, as expected | 1.08 s |

Nothing failed because of the design. Two messages in the logs come from the design:
- xschem, on every netlist run: `MCL`, `MCS` (sg13_hv_nmos, L = 30 µm) and `MS1_0..7` (sg13_hv_pmos,
  L = 12.5 µm): `length is too big, max l < 10.0u`. These are the PDK symbols' range warnings.
- magic, each extraction: `29 warnings`. All 29 are `device missing 1 terminal; connecting remainder to
  node vss` (20) or `vdd` (9), one for each of the 29 devices whose D = S is a rail, i.e. the dummies.

## LVS (netgen)

`Final result: Circuits match uniquely.` 28 devices on both sides (layout 53 → 10 sg13_hv_nmos and
58 → 18 sg13_hv_pmos after merging 83 parallel fingers) and 22 nets on both sides; the pin lists are
equivalent. `Property errors were found`, but all of them are `Property mm_ok in circuit2 has no
matching property in circuit1`: the schematic-only mismatch flag. W and L match on all 28 devices.

## PEX netlists

| netlist | ports (= `oa_core_pd_pex.sym` order) | devices | R | C | ΣC |
|---|---|---|---|---|---|
| `oa_core_pd_magic_pex_1.spice` | vdd vss iout en_3v3 en_3v3_b | 111 | 0 | 15 | 234.8 fF |
| `oa_core_pd_magic_pex_2.spice` | same | 111 | 0 | 102 | 277.6 fF |
| `oa_core_pd_magic_pex_3.spice` | same | 111 | 42 | 113 | 444.3 fF |
| `oa_core_pd_klayout_pex_2.spice` | same | 111 | 0 | 106 | 340.6 fF |

`check_pex_ports.py`: all ports connected in all four. `sak-pin-reorder.py`: name match, identity
mapping. The 111 devices are the unmerged fingers (53 sg13_hv_nmos, 58 sg13_hv_pmos). Mode 3 keeps
resistors on 2 of 22 nets: vss (24 R) and `oa_svpg_0.vpg` (18 R). A rerun of mode 3 in a scratch
directory gave 37 R, with the same 113 C and the same capacitance per net. That is the known spread of
full-RC (CLAUDE.md §5). Mode 2 reproduced its C list exactly.

bg_core_pd for comparison (Cowork session, 2026-10-29): 123 devices; C in modes 1/2/3 = 50/313/347,
R = 359, KLayout-PEX 317 C.

### Capacitance per port net, fF: to vss / coupling to all other nets

| net | magic 1 | magic 2 | magic 3 | KLayout-PEX 2 |
|---|---|---|---|---|
| iout | 9.94 / – | 1.31 / 7.70 | 1.36 / 7.70 | 0.28 / 7.70 |
| vdd | 56.96 / – | 0.62 / 107.81 | 47.37 / 107.81 | 0.00 / 107.81 |
| vss (total from all nets) | 234.83 | 52.81 | 155.41 | 115.74 |
| en_3v3 | 0 / – | 0.00 / 0.55 | 0.00 / 0.55 | 0.21 / 0.55 |
| en_3v3_b | 0 / – | 0.00 / 12.56 | 0.00 / 12.56 | 1.31 / 12.56 |

Subnodes of mode 3 (`vss.t4`, `vss.n1`, …) are summed into their net. Mode 1 (`extract no coupling`)
writes 15 caps, all to vss; en_3v3, en_3v3_b, vnc, vpc, vpg and vbr get none.

Largest internal nets (to vss / coupling, magic 2 vs. KLayout-PEX 2): `oa_svpg_0.vpg` 0 / 99.2 vs.
0.9 / 99.2; `oa_mcs_c_0.vres` 6.3 / 47.8 in both; `oa_n10_0.vnc` 0 / 46.3 vs. 45.6 / 46.3;
`a_724_2272#` 23.9 / 30.2 in both; `oa_mcs_c_0.vbr` 0 / 11.7 vs. 32.9 / 11.7. Largest pairs: vpg–vdd
83.2, vres–vnc 26.6, a_724_2272#–vres 19.7, c8–co 11.0, a_724_2272#–vnc 9.4, en_3v3_b–vdd 8.1.

**The coupling capacitors are identical in magic 2, magic 3 and KLayout-PEX 2. The capacitors to vss
differ.** KLayout-PEX writes 14 caps to vss marked `**FLOATING` (vnc 45.6 fF, vbr 32.9 fF, …; +62.9 fF
in total), which `sak-pex.sh` doesn't write. Both flatten and extract with the same magic options. The
difference is ext2spice's hierarchy option: `sak-pex.sh` runs `ext2spice lvs`, which turns
`hierarchy on`, and then the floating-substrate caps are dropped. kpex runs with hierarchy off and
keeps them. In a scratch directory, kpex's script with `ext2spice hierarchy on` reproduces magic 2
(102 C, 277.6 fF), and `sak-pex.sh`'s with `ext2spice hierarchy off` gives the 14 `**FLOATING` caps.

## Harness fit

The magic commands of `sak-pex.sh` (scripts rerun with `-d` in a scratch directory, since the Makefile
deletes them), compared with `magic/run_extract_user_project.sh` of `sg13cmos5l_ocd_chipalooza`:

1. **Same:** `magic -dnull -noconsole -rcfile $PDK_ROOT/$PDK/libs.tech/magic/ihp-sg13cmos5l.magicrc`
   (`$PDKPATH` is the same path); `select top cell`; `extract path`; `extract all`; `ext2spice lvs`.
2. **Input:** the harness does `source ../scripts/layout_setup.tcl` (`units microns`, `snap internal`,
   `addpath` for the dependencies' magic and paramcells directories, stdcell, io, sram) and
   `load openframe_user_project`, a .mag hierarchy. `sak-pex.sh` does `gds read <cell>.gds`, checks
   the top-cell name and runs `load <cell>`, with no `units`, `snap` or `addpath`.
3. **Flatten:** `sak-pex.sh` runs `flatten <cell>_flat`, deletes the original and renames the copy
   `<cell>_pex`. The harness extracts the hierarchy as is.
4. **Extract options:** the harness runs `extract no all` then `extract do unique`. In 8.3.685 that
   leaves only label check, aliases and unique, a connectivity extraction without parasitics.
   `sak-pex.sh` keeps magic's defaults (adjust, capacitance, coupling, length, lumped R, label check,
   aliases and unique on; resistance off). Mode 1 adds `extract no coupling`. Mode 3 adds
   `extresist threshold 10000`, `mindelay 1`, `minres 1000`, `extract do resistance`,
   `extract do unique` (already on) and `ext2spice extresist on`.
5. **ext2spice:** `sak-pex.sh` adds `ext2spice cthresh 0.01` (`lvs` sets it infinite). It issues
   `ext2spice lvs` before `extract all`, the harness after; both only set options for the final
   `ext2spice`.
6. **Housekeeping:** `sak-pex.sh` runs `crashbackups stop` and `drc off`; the harness runs neither.
   The harness keeps its `.ext` files in `extfiles/` (its `rm` is commented out). `sak-pex.sh` deletes
   them, adds a header line and names the subckt `<cell>_pex`, and the Makefile reorders pins to
   `_pex.sym`.
7. **No PEX in the harness:** its netlist feeds `validate/run_lvs_user_project.sh`, so modes 1–3 have
   no counterpart there. The nearer counterpart is `sak-lvs.sh`'s extraction: flatten,
   `extract no capacitance / coupling / resistance / length`, `ext2spice lvs`. That differs from the
   harness by the flatten and by leaving adjust and lumped R on, which are value options with no
   parasitics extracted. Both LVS runs use the same `$PDK_ROOT/$PDK/libs.tech/netgen/ihp-sg13cmos5l_setup.tcl`.
   The harness also reads the stdcell SPICE and housekeeping netlists into circuit 2 and sets
   `NETGEN_COLUMNS=75`.

## Delivered

- `claude/c0-oa-core-pd-pex`: `macros/oa_core_pd/` `netlist/schematic/oa_core_pd_magic.spice`,
  `netlist/layout/oa_core_pd_magic.ext.spc`, `netlist/pex/oa_core_pd_{magic_pex_1,2,3,klayout_pex_2}.spice`,
  `schematic/xschem/oa_core_pd_pex.sym`, `verification/drc/oa_core_pd.magic.drc/oa_core_pd.magic.drc.rpt`,
  `verification/lvs/oa_core_pd.magic.lvs/oa_core_pd.lvs.out`. The `.log` and `.tcl` files the targets
  also wrote are in `.gitignore`.
- `claude/c0-oa-core-pd-pex-sudel`: 20 logs in `sudelbuecher/logs/claude/c0-oa-core-pd-pex/`, one
  `MANIFEST.tsv` row each, and this report.
