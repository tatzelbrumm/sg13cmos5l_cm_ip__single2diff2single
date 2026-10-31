<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C1: PEX of oa_core_pd and bg_core_pd in the bias verification, report

2026-10-30, Claude Code cloud session, environment `sg13cmos5l` (prebuilt toolchain of `claude-cloud-config`). Brief:
`C1_core_pex_bias_verification.md`. Design branch `claude/c1-core-pex-verif` (from `toplevel` 36ca38d; results in
0ee4cc0 … 8a72dd8), notes branch `claude/c1-core-pex-verif-sudel` (from `sudel_buecher` 2832ef4). Changes and omissions
for review, one entry each: `C1_verification_changes.md`. Times are UTC; the MANIFEST rows are in CET, like the rest of
that file.

**Result.**
- **bg_core_pd:** DRC clean, LVS match (29 devices, 21 nets), PEX 1 / 2 / 3 and KLayout-PEX 2 with all ports connected;
  123 devices, C 50 / 313 / 353, R 216 (mode 3, not reproducible: 722–999 in reruns), KLayout 317 C. Every bg extraction
  has 41 nodes that only capacitors touch.
- **The cores' layouts don't move the dc bias currents** (PEX 2: 0.00 %, PEX 3: ≤ 0.02 %, bandgap at the R / pnp corners
  0.1 %). **They do raise the supply sensitivity at 100 kHz – 1 MHz** (vdd / vss, up to ×2.6 for the bandgap: 18 →
  48 %/V at 1 MHz; ×2 even with both cores off, through the shared tree input) and **slow the bandgap's settling by
  40–57 %** (0.7 → 1.1 µs). No limit of the existing groups is violated in any view.
- **Mismatch** (new, 100 runs × 6 per corner): the cores dominate (σ of vbp 4.9 % Oguey-Aebischer, 3.0 % bandgap, tree
  alone 1.1 %); with `mm_ok` restored on the extracted cores the spread is the same within the statistics. The worst
  cases (ss / −40 °C / R wcs / pnp bcs and ff / 125 °C / R bcs / pnp wcs, 3.0 and 3.6 V) pass the `pvt` limits (lowest
  vbp 2.39 µA against 2.2 µA); the typical corner fails the tight `supply_params` window (4.8–5.3 µA) in every view:
  the only violations, and a matter of the proposed limits. pnpMPA has no mismatch model.
- **To get there:** the DC / tran templates didn't run under ngspice-47 (name clash), the committed results predate
  the cores' layout redraw (sel 1 / 2 / 3 moved by up to 1 %), bg's capacitor-only nodes put ngspice on wrong operating
  points (+18 %) until tied, and PEX 3 needed looser Newton settings. All of it is in the verification files, listed
  for review in `C1_verification_changes.md`.

## Toolchain and setup

| tool | version |
|---|---|
| `klayout -b -v` | KLayout 0.30.12 (`/usr/bin/klayout`, the klayout.org .deb); PyPI `klayout` 0.30.12 |
| `magic -dnull -noconsole --version` | 8.3.685 (`bed8d4ff`) |
| netgen | 1.5.324 (`abe6117e`) |
| `xschem --version` | 3.4.8RC (`d76e6cc7`) |
| `ngspice -v` | ngspice-47 (KLU) |
| `kpex --version` | 0.6.8 (the setup script's wrapper for `ihp_sg13cmos5l`) |
| OpenVAF | `openvaf-r` dd05b5e (osdi_0.5_20260820-26) |
| `/usr/local/bin/sak-*` | 18 scripts, IIC-OSIC-TOOLS 2026.10 (68d3f07) |
| IHP-Open-PDK | `df4c5054ee8ca481c3eb873687274f28cdb50b1e`; OSDI: cap_cmomf, cap_cmomi, mosvar, psp103, psp103_nqs, r3_cmc |
| CACE | 2.11.0 (the 2026.10 pin), under Python 3.12.3; accepts `cace_format: 5.2` |
| Python | `python3` = 3.13.17 (alternatives); 3.12.3 for CACE |

`/foss/setup.log`: TOOLS_OK 5 s, PDK_OK 5 s, PIP_OK 24 s, APT_OK 26 s, OSDI_OK 26 s, **SETUP_DONE 26 s**: unlike C0, the
prebuilt archive ran to the end (kpex wrapper, symlinks, sak exec bits all in place). `/foss/tools/BUILDINFO` lists the
sources and commits of the prebuilt tools. Versions in `logs/.../env.versions.out`.

## Environment adaptations

1. `pip install --break-system-packages cace==2.11.0` stopped at `Cannot uninstall blinker 1.7.0, RECORD file not found`
   (Debian's package); rerun with `--ignore-installed blinker`. pip warned that conan 2.32.0 wants python-dateutil < 3.
2. `cace` then failed at import: `No module named 'tkinter'`. `python3` is 3.13 here, and Ubuntu has no Tk for it.
   Installed `python3-tk` (apt, for 3.12) and `cace==2.11.0` under `python3.12` (same `--ignore-installed blinker`), which
   rewrote `/usr/local/bin/cace` to `#!/usr/bin/python3.12`. Log: `env.cace-py312-install.out`. **Setup-script fix:**
   add `python3-tk` and install CACE with `python3.12 -m pip` (or have the image's `python3` be 3.12).
3. Nothing else: no tool rebuilt, no PDK file touched.

## Git (step 1)

- `git fetch origin claude/c0-oa-core-pd-pex claude/c1-core-pex-verif-sudel` as given.
- `git cherry-pick 82a57ec` was empty: `toplevel` already contains it (36ca38d's history has 82a57ec), so the branch
  already had C0's nine oa_core_pd outputs. I aborted the empty pick; nothing else to do.
- Worktree `../sudel` on a local `claude/c1-core-pex-verif-sudel` tracking the remote one (2832ef4 = `sudel_buecher`).
- Commits only on the two `claude/c1-core-pex-verif*` branches; pushed only those.

## bg_core_pd PEX (step 2)

From `macros/bg_core_pd` after `source .designinit`, each with `SCRIPTS_DIR=../../scripts`, tee'd to
`sudelbuecher/logs/claude/c1-core-pex-verif/bg_core_pd.<target>.{out,err}`. No environment fix was needed (C0 needed
three).

| target | result | wall time |
|---|---|---|
| `magic-drc` | clean (`COUNT: 0`) | 0.46 s |
| `magic-lvs-netlist` | written; xschem's range warnings for `MS1_0..7` (sg13_hv_pmos, L = 12.5 µm > 10 µm), as in C0 | 0.13 s |
| `magic-lvs` | `Circuits match uniquely`: 29 devices, 21 nets on both sides; property errors are `mm_ok` only (44) | 0.49 s |
| `magic-pex EXT_MODE=1` | all ports connected | 0.52 s |
| `magic-pex EXT_MODE=2` | all ports connected | 0.75 s |
| `magic-pex EXT_MODE=3` | all ports connected | 0.64 s |
| `klayout-pex EXT_MODE=2` | all ports connected; deprecation warning for the missing subcommand, as expected | 1.07 s |

LVS merged 58 parallel and 36 series devices in the layout (41 rhigh segments, the MOS fingers) and 2 parallel / 36
series in the schematic. magic reports 27 extraction warnings in every mode (C0's 29 for oa were the dummies' missing
terminal).

| netlist | ports (= `bg_core_pd_pex.sym`) | devices | R | C | ΣC |
|---|---|---|---|---|---|
| `bg_core_pd_magic_pex_1.spice` | vdd vss iout en_3v3 en_3v3_b | 123 | 0 | 50 | 287.7 fF |
| `bg_core_pd_magic_pex_2.spice` | same | 123 | 0 | 313 | 338.1 fF |
| `bg_core_pd_magic_pex_3.spice` | same | 123 | 216 | 353 | 343.8 fF |
| `bg_core_pd_klayout_pex_2.spice` | same | 123 | 0 | 317 | 364.8 fF |

123 devices = 57 sg13_hv_pmos + 16 sg13_hv_nmos + 41 rhigh + 9 pnpMPA, unmerged. **Against the Cowork run
(2026-10-29):** devices 123, C 50 / 313 (modes 1 / 2) and KLayout 317 C are the same; **mode 3 is not: 353 C and 216 R
here, 347 C and 359 R there.** Three reruns of mode 3 in a scratch folder gave 722 / 999 / 974 R and 349 / 369 / 372 C,
two reruns of mode 2 the identical C list (sorted). This is CLAUDE.md's "full-RC PEX is not reproducible". In bg the R
sits on vss (160 of 216 here, 679–931 in the reruns, 3.7–11.3 kΩ in sum) and on the two PMOS drain nets of the output
branch (`a_918_6928#`, `a_918_8440#`, about 25 R / 100–135 Ω each); in two reruns also on `bg_pmir_pcas_c_0.vpg`. The
committed mode-3 netlist, and so every PEX 3 result below, is one draw of that spread.

**41 capacitor-only nodes in every bg netlist** (magic 2 and 3, KLayout 2): `a_<x>_4084#`, one next to each rhigh
segment, at the pitch of the segments (0.50 fF to each neighbour, 0.027 fF to the segment's end `a_<x>_3998#`). No
device or resistor touches them, so LVS doesn't see them. (KLayout-PEX's 51 `**FLOATING` lines are something else:
capacitors to vss, as C0 found for oa.) oa_core_pd has none. In a simulation they make the op matrix singular (below). What they are in the layout (poly or implant beyond
the rhigh marker?) I didn't check: worth a look in KLayout.

### Capacitance per port net, fF: to vss / coupling to all other nets

| net | magic 1 | magic 2 | magic 3 | KLayout-PEX 2 |
|---|---|---|---|---|
| iout | 44.24 / – | 1.96 / 39.97 | 2.10 / 37.28 | 0.58 / 39.97 |
| vdd | 48.52 / – | 2.66 / 73.42 | 2.70 / 61.02 | 0.00 / 73.42 |
| vss (total from all nets) | 287.69 | 61.88 | 151.27 | 88.55 |
| en_3v3 | 0 / – | 0.00 / 5.28 | 0.00 / 4.02 | 1.68 / 5.28 |
| en_3v3_b | 0 / – | 0.00 / 11.98 | 0.00 / 11.75 | 1.62 / 11.98 |

Mode-3 subnodes of the ports are summed into the port. As in C0, magic 2 and KLayout-PEX 2 have the same coupling
capacitors and differ in the capacitors to vss. Largest internal nets (coupling, magic 2): `bg_n4_0.vpc` 86.8 fF,
`bg_pmir_pcas_c_0.vpg` 84.5, `bg_n4_0.g` 60.4 (KLayout: 87.3 coupling plus 27.0 to vss), `a_918_6928#` 53.0,
`a_918_8440#` 42.8.


## Core PEX in bias_sel_pd (step 3): how

**The views.** The DC, tran, PSRR and start-up templates include `templates/cores/<cores>.spice` just before the DUT
netlist; `cores` is a CACE condition (yaml default `schematic`). A view file includes the cores' extracted netlists
and defines `oa_core_pd` / `bg_core_pd` as wrappers around `oa_core_pd_pex` / `bg_core_pd_pex`. ngspice keeps the
first definition of a subckt and ignores later ones ("Warning: redefinition of .subckt oa_core_pd, ignored", checked in
the run logs), so the DUT netlist that CACE writes from the schematic is used as is: only the two cores change.
`make sim-cace CORES=<view>` runs a copy of the yaml whose `cores` defaults to the view and writes
`results/bias_sel_pd_cores_<view>/`. Without `CORES` everything is as before: schematic cores, the DUT netlist CACE
writes, `results/bias_sel_pd/`. Views: `schematic`, `magic_pex_2`, `magic_pex_3`, `magic_pex_2_mm_ok`.

**Capacitor-only nodes.** The first PEX 2 run gave sel 1 (Oguey-Aebischer, tt, 27 °C) vbp = 5.968 µA, +18 % on the
schematic, and I ibias = −0.21 µA. The ngspice log: `singular matrix: check node x1.xbg.xpex.a_3207_4084#`, gmin and
source stepping failed, transient op. That node is one of bg's 41 capacitor-only nodes; the transient op ended on a
wrong operating point. With `.option rshunt=1e15` the same deck gave 5.04434 µA against 5.04432 µA schematic, but at
ss, −40 °C the op still fell back to a transient op (sel 0: I vdd +10 %; sel 2: I vsso −9 %, I vabn +4.3 %; presumably
because 1e-15 S leaves the matrix ill-conditioned), and rshunt touches every node of the testbench. Tying only the 41
nodes to vss through 1 TΩ (copies of bg's netlists, `scripts/cace/pex_for_sim.py --tie`) converges directly and gives
the schematic's numbers to all printed digits (sel 2, ss, −40 °C: vbp 4.91515 µA in both). The superseded rshunt runs'
logs are in `superseded_rshunt/`; their results were deleted.

**PEX 3 needs looser Newton settings.** With the full-RC bg netlist 7 runs of the dc groups (sel 2 at tt, 27 °C among
them) still fell back to a transient op (`singular matrix` at a rhigh terminal in the first iteration, then the default
100 iterations ran out), and sel 2 came out at I vdd −21 %, I vsso −4.5 %, I vddo ≠ I vabp: not an operating point.
`.option itl1=5000` fixed that one (vbp 5.00975 µA against 5.01005 µA schematic) and 3 more (logs in
`superseded_pex3_itl1/`), but 3 runs at −40 °C still failed (sel 1, ff: vbp +33 %; sel 0, tt / ff: I vdd −29 / +31 %).
reltol 1e-3 fixes them (gmin 1e-12 too, but that adds pA-level currents that `pd_params` would see). The templates
set reltol 1e-4 after the view's include and the last `.options` wins, so `magic_pex_3.spice` sets it at run time in a
`.control` block of its own, which ngspice runs before the template's. The dc currents then agree with the schematic
to 0.02 %. For the transients 1e-3 is too loose (2 tran runs stopped, and settling to 1 % wasn't resolved), so the
tran and start-up templates set reltol back to 1e-4 right before `tran`; with the other views that is a no-op (checked:
the schematic tran and start-up groups and the PEX 2 start-up group, rerun with it, are byte-identical). Every PEX 3 group was rerun with the final files (intermediate logs in
`superseded_pex3_reltol/`, `superseded_tran_reltol/`).

**Left over in PEX 3** (not chased further; the brief asked PEX 3 for the dc groups, which are clean): in
`psrr_params` the op of sel 2, ff, −40 °C still falls back to a transient op (its values are ~10 % off a converged
reference with gmin 1e-12; that run sets none of the maxima). Tran and start-up run complete (18 / 18, 48 / 48).

**Start-up at −40 °C is fragile.** The bandgap's pnpMPA on the 1 µs ramp at −40 °C stops ngspice with "timestep too
small" for some settings: the schematic at sel 2, ff, 3.6 V with the default itl4 (fixed by `itl4=1000`); with
`vntol=1e-4` one PEX 3 run came back but two PEX 2 runs were lost, so it isn't used. The final template (itl4 1000,
reltol 1e-4 for the transient) runs all 48 runs in all three views (logs of the other tries in
`superseded_startup_vntol/`).

**Mismatch.** The PDK draws local mismatch in the `*_mismatch` model sections for instances with `mm_ok=1`: MOS (w, l,
vth, mobility) and rhigh (rsh, w, l). pnpMPA has no mismatch model (`cornerPNP.lib` has typ / stat / bcs / wcs only),
so the bandgap's Q1 / Q2 ratio (1 : 8) has no spread in any of these runs: the bg spread below is MOS and rhigh only.
The seed is `12345 + iteration`, so iteration k draws the same numbers for every sel and vdd of a group (paired). The
extracted netlists have no `mm_ok`, so a mismatch run on a plain PEX view draws only for the tree (schematic) and not
for the cores. **Restored:** `pex_for_sim.py --mm-ok` appends `mm_ok=1` to every X line of a MOS or rhigh model in
copies of the two magic PEX 2 netlists (111 devices in oa, 114 in bg; the 9 pnpMPA stay as they are), with bg's 41
nodes tied as above; view `magic_pex_2_mm_ok`. Each finger is a device of its own there (w per finger, ng = 1), so it
draws its own mismatch, and the sum over the fingers has the spread of the schematic's multi-finger device. The
dummies draw too, which doesn't matter. With the default solver settings 2 of the 600 `mm_params` runs of this view
fell back to a transient op, so it got PEX 3's settings (itl1 5000, reltol 1e-3 at run time) and all three groups were
rerun (first try's logs in `superseded_mm_ok_conv/`).

**Worst-case combinations.** From the committed / rerun `pvt_params`, `supply_params` and `rpnp_params` the extremes
are the same for both cores: lowest current at ss, −40 °C, rhigh wcs, pnpMPA bcs, 3.0 V; highest at ff, 125 °C, rhigh
bcs, pnpMPA wcs, 3.6 V (rhigh / pnpMPA only move bg). `pvt` never combined MOS and temperature corners with the R / pnp
corners; the mismatch groups do (`mm_lo_params`, `mm_hi_params`), and `mm_params` is the typical corner. Each group is
sel 1 / 2 / 3 × 3.0 / 3.6 V × 100 iterations = 600 runs.


## Results

### Baseline: does the schematic view reproduce the committed results?

- `make sim-cace` first stopped in every run: ngspice-47 rejects the DC and tran templates ("device already exists, bail
  out", `XRP1` / `XRp1`, change 1). The committed results are from 0d12e00 (2026-10-28 00:24), before the fixtures
  came into the templates; these templates had never run.
- With the rename: **sel 0 bit-identical** to the committed CSVs (`iref_params.csv` unchanged, the sel 0 rows of all
  other groups too). **sel 1 / 2 / 3 are not**: vbp at tt, 27 °C 5.04432 / 5.01005 / 10.0026 µA against 5.05187 /
  5.06139 / 10.0612 µA committed (−0.15 / −1.01 / −0.58 %). The cores' schematics were redrawn for their layouts on
  2026-10-28 (ba511f5 oa, 1903407 bg: rhigh in 9.94 µm segments, MS1 as eight L = 12.5 µm devices, dummies), after the
  committed results; the tree sheet changed too (61624e5, f5b333c),
  without moving sel 0. The change is the DUT's, not the testbench's: a control run with HEAD's DC template plus only
  the rename gave the same `sel_params` as the final templates, digit for digit.
- So `results/bias_sel_pd/` is rewritten (change 10); every limit still passes there.
- Convergence in the schematic view: some runs needed gmin stepping (pvt 5, pd 2, tran 10: "dynamic gmin stepping
  failed", then true gmin stepping succeeded, which is a valid op). One PSRR run (sel 0, ss, −40 °C) fell back to a
  transient op with the flat template's reltol 1e-6; with 1e-4 it converges directly and moves by 0.48 %, all other
  runs identical. The final schematic logs carry no warning.

### What the cores' layouts do (PEX 2 and PEX 3 against the schematic)

**DC currents: nothing that matters.** PEX 2 reproduces the schematic's bias currents to 0.00 % in every run of
`sel`, `pvt`, `supply`, `rpnp` and `iref` (capacitors don't move dc currents, and the PEX devices have the schematic's
W / L). Only leakage moves a little (`pd_params`, all disabled: I vdd +0.3 %, I ibias −0.5 % at the maximum; the
extracted junction areas and perimeters).

PEX 3 adds the wiring resistance and moves the bias currents by at most 0.02 % in `sel`, `pvt`, `supply` and `iref`; the only visible effect is in `rpnp_params`, the bandgap at the rhigh / pnpMPA corners: −0.10 % on the high
side (0.20 % in one run), from the resistance of bg's vss wiring (160 of its 216 R) in series with the resistors and
the pnps. Against every limit that is noise. (PEX 3 runs at reltol 1e-3, see above; at that tolerance PEX 3 and the
schematic agree to 0.02 % where no wiring R is involved.)

**Supply rejection: the coupling capacitors raise the sensitivity on vdd and vss at 100 kHz and 1 MHz** (maximum over
the six currents, %/V, maximum over ss / tt / ff × −40 / 27 / 125 °C; tt, 27 °C in brackets):

| sel | rail, f | schematic | PEX 2 | PEX 3 |
|---|---|---|---|---|
| 0 (harness, both cores off) | vdd 1 MHz | 4.91 (4.82) | 9.70 (9.51) | 9.28 (9.08) |
| 1 (Oguey-Aebischer) | vdd 100 kHz | 6.12 (4.30) | 9.63 (6.69) | 10.51 (7.30) |
| 1 | vdd 1 MHz | 8.61 (5.70) | 15.99 (10.29) | 12.92 (8.89) |
| 2 (bandgap) | vdd 100 kHz | 2.65 (2.40) | 6.88 (5.69) | 5.35 (4.54) |
| 2 | vdd 1 MHz | 18.46 (17.39) | 48.44 (46.48) | 39.88 (36.60) |

PEX 3 softens the 1 MHz coupling somewhat (wiring R in series with the coupling C) but keeps the picture. vss behaves
like vdd (2 (bandgap), 1 MHz: 19.10 → 49.34 / 40.55 %/V); vddo and vsso, which only feed the class-AB fixtures,
don't change (≤ 0.1 %); at 1 kHz nothing changes (≤ 3 %, mostly 0). Even with both cores off (sel 0) the 1 MHz
sensitivity doubles: the cores' outputs share the tree's input node, and their extracted coupling stays on it. In
bg_core_pd, `iout` couples 29.4 fF to the core's own cascode gate line `bg_n4_0.vpc` and 5.9 fF to `bg_n4_0.g`; in
oa_core_pd the largest is 0.9 fF (to `oa_n10_0.vpc`). That makes the bg output wiring the first suspect for the vdd /
vss feed-through; the per-node attribution wasn't simulated here. `psrr_params` is report only (no limits; the flat
copies' proposals were 3.2 / 8.4 / 8.5 %/V on vdd at 1 k / 100 k / 1 MHz for `bias_oa_pd`: sel 1 exceeds the 1 MHz
one already in the schematic view, 8.61, and with PEX 2 both, 9.63 and 15.99).

**Settling and start-up: the bandgap is slower, the Oguey-Aebischer core about the same.** `tran_params`, time to
1 % of the final vbp (ss / tt / ff, 27 °C):

| event | schematic | PEX 2 | PEX 3 |
|---|---|---|---|
| enable, sel 0 (harness) | 0.21–0.22 µs | 0.18 µs | 0.18 µs |
| enable, sel 1 (OA) | 25.5–30.4 µs | 26.6–28.7 µs | 26.5–28.6 µs |
| enable, sel 2 (bg) | 0.71–0.74 µs | 1.03–1.15 µs (+40…57 %) | 1.07–1.19 µs |
| sel 0 → 1 | 25.5–25.9 µs | 26.5–27.0 µs | 26.4–26.8 µs |
| sel 1 → 2 | 0.70–0.74 µs | 1.01–1.13 µs (+40…52 %) | 1.04–1.16 µs |
| sel 2 → 0 | 0.14 µs | 0.15 µs | 0.15 µs |

Start-up from a supply ramp (`startup_params`, time to 90 % of the final vbp from the start of the ramp; ranges over
ss / tt / ff × −40 / 125 °C × 3.0 / 3.6 V):

| sel, ramp | schematic | PEX 2 | PEX 3 |
|---|---|---|---|
| 1 (OA), 1 µs | 0.99–1.52 µs | 1.05–1.66 µs (≤ +9 %) | 1.05–1.66 µs (≤ +9 %) |
| 1 (OA), 100 µs | 73.3–96.6 µs | 72.8–97.3 µs | 72.3–96.8 µs |
| 2 (bg), 1 µs | 0.90–1.62 µs | 1.55–2.51 µs (up to +88 %) | 1.44–2.03 µs (up to +64 %) |
| 2 (bg), 100 µs | 47.2–88.3 µs | 47.1–88.3 µs | 47.1–88.3 µs |

With the 100 µs ramp the supply sets the pace (≤ 1.4 % change). All far inside the 130 µs limit; the final currents
are within 1e-6 of the dc point in every run of every view.


### Mismatch at typical and worst case (sel 1 / 2 / 3, 3.0 / 3.6 V, 100 runs each)

vbp current per group, sel and vdd, in the three views: the schematic (cores and tree draw), PEX 2 with `mm_ok`
restored (cores and tree draw), and plain PEX 2 (only the tree draws, since extraction drops `mm_ok`). Limits for
sel 1 / 2: `supply_params` for the typical group, `pvt_params` for the worst cases (sel 3 runs both cores, about twice
every current, and has none). "fails" lists the currents whose min or max leaves those limits.

| group | sel | vdd | view | vbp mean | σ | min .. max | limits | fails (min / max outside) |
|---|---|---|---|---:|---:|---:|---|---|
| mm_params | 1 | 3.0 | schematic | 5.015 | 4.89 % | 4.248 .. 5.717 | 4.8 .. 5.3 | Ibp, Ibn, Ibnc, Ibpc, Iabp, Iabn |
| mm_params | 1 | 3.0 | PEX 2 + mm_ok | 5.045 | 4.58 % | 4.570 .. 5.654 | 4.8 .. 5.3 | Ibp, Ibn, Ibnc, Ibpc, Iabp, Iabn |
| mm_params | 1 | 3.0 | PEX 2 (cores without mismatch) | 5.027 | 1.11 % | 4.872 .. 5.190 | 4.8 .. 5.3 | Ibn |
| mm_params | 1 | 3.6 | schematic | 5.036 | 4.88 % | 4.268 .. 5.741 | 4.8 .. 5.3 | Ibp, Ibn, Ibnc, Ibpc, Iabp, Iabn |
| mm_params | 1 | 3.6 | PEX 2 + mm_ok | 5.066 | 4.58 % | 4.591 .. 5.677 | 4.8 .. 5.3 | Ibp, Ibn, Ibnc, Ibpc, Iabp, Iabn |
| mm_params | 1 | 3.6 | PEX 2 (cores without mismatch) | 5.048 | 1.11 % | 4.892 .. 5.212 | 4.8 .. 5.3 | Ibn |
| mm_params | 2 | 3.0 | schematic | 4.971 | 3.02 % | 4.554 .. 5.346 | 4.8 .. 5.3 | Ibp, Ibn, Ibnc, Ibpc, Iabp, Iabn |
| mm_params | 2 | 3.0 | PEX 2 + mm_ok | 5.003 | 2.89 % | 4.638 .. 5.338 | 4.8 .. 5.3 | Ibp, Ibn, Ibpc, Iabp, Iabn |
| mm_params | 2 | 3.0 | PEX 2 (cores without mismatch) | 4.987 | 1.11 % | 4.832 .. 5.149 | 4.8 .. 5.3 | Ibn |
| mm_params | 2 | 3.6 | schematic | 5.003 | 3.00 % | 4.589 .. 5.381 | 4.8 .. 5.3 | Ibp, Ibn, Ibnc, Ibpc, Iabp, Iabn |
| mm_params | 2 | 3.6 | PEX 2 + mm_ok | 5.036 | 2.88 % | 4.673 .. 5.371 | 4.8 .. 5.3 | Ibp, Ibn, Ibnc, Iabp, Iabn |
| mm_params | 2 | 3.6 | PEX 2 (cores without mismatch) | 5.018 | 1.11 % | 4.864 .. 5.182 | 4.8 .. 5.3 | Ibn |
| mm_params | 3 | 3.0 | schematic | 9.934 | 2.87 % | 9.101 .. 10.853 | none (2x) | – |
| mm_params | 3 | 3.0 | PEX 2 + mm_ok | 9.996 | 2.84 % | 9.317 .. 10.708 | none (2x) | – |
| mm_params | 3 | 3.0 | PEX 2 (cores without mismatch) | 9.984 | 1.60 % | 9.730 .. 10.825 | none (2x) | – |
| mm_params | 3 | 3.6 | schematic | 9.987 | 2.86 % | 9.151 .. 10.911 | none (2x) | – |
| mm_params | 3 | 3.6 | PEX 2 + mm_ok | 10.050 | 2.83 % | 9.367 .. 10.764 | none (2x) | – |
| mm_params | 3 | 3.6 | PEX 2 (cores without mismatch) | 10.014 | 0.84 % | 9.782 .. 10.250 | none (2x) | – |
| mm_lo_params | 1 | 3.0 | schematic | 3.059 | 7.21 % | 2.387 .. 3.688 | 2.2 .. 9.3 | – |
| mm_lo_params | 1 | 3.0 | PEX 2 + mm_ok | 3.088 | 6.79 % | 2.667 .. 3.645 | 2.2 .. 9.3 | – |
| mm_lo_params | 1 | 3.0 | PEX 2 (cores without mismatch) | 3.069 | 1.46 % | 2.944 .. 3.205 | 2.2 .. 9.3 | – |
| mm_lo_params | 1 | 3.6 | schematic | 3.081 | 7.19 % | 2.406 .. 3.712 | 2.2 .. 9.3 | – |
| mm_lo_params | 1 | 3.6 | PEX 2 + mm_ok | 3.110 | 6.77 % | 2.687 .. 3.669 | 2.2 .. 9.3 | – |
| mm_lo_params | 1 | 3.6 | PEX 2 (cores without mismatch) | 3.091 | 1.46 % | 2.965 .. 3.227 | 2.2 .. 9.3 | – |
| mm_lo_params | 2 | 3.0 | schematic | 3.866 | 3.43 % | 3.487 .. 4.213 | 2.2 .. 9.3 | – |
| mm_lo_params | 2 | 3.0 | PEX 2 + mm_ok | 3.894 | 3.32 % | 3.571 .. 4.188 | 2.2 .. 9.3 | – |
| mm_lo_params | 2 | 3.0 | PEX 2 (cores without mismatch) | 3.879 | 1.38 % | 3.735 .. 4.035 | 2.2 .. 9.3 | – |
| mm_lo_params | 2 | 3.6 | schematic | 3.902 | 3.41 % | 3.529 .. 4.250 | 2.2 .. 9.3 | – |
| mm_lo_params | 2 | 3.6 | PEX 2 + mm_ok | 3.930 | 3.30 % | 3.611 .. 4.226 | 2.2 .. 9.3 | – |
| mm_lo_params | 2 | 3.6 | PEX 2 (cores without mismatch) | 3.916 | 1.33 % | 3.770 .. 4.072 | 2.2 .. 9.3 | – |
| mm_lo_params | 3 | 3.0 | schematic | 6.895 | 3.71 % | 6.148 .. 7.711 | none (2x) | – |
| mm_lo_params | 3 | 3.0 | PEX 2 + mm_ok | 6.951 | 3.67 % | 6.358 .. 7.604 | none (2x) | – |
| mm_lo_params | 3 | 3.0 | PEX 2 (cores without mismatch) | 6.918 | 1.07 % | 6.713 .. 7.133 | none (2x) | – |
| mm_lo_params | 3 | 3.6 | schematic | 6.945 | 3.69 % | 6.194 .. 7.765 | none (2x) | – |
| mm_lo_params | 3 | 3.6 | PEX 2 + mm_ok | 7.002 | 3.66 % | 6.406 .. 7.657 | none (2x) | – |
| mm_lo_params | 3 | 3.6 | PEX 2 (cores without mismatch) | 6.968 | 1.06 % | 6.762 .. 7.184 | none (2x) | – |
| mm_hi_params | 1 | 3.0 | schematic | 7.350 | 3.20 % | 6.612 .. 8.019 | 2.2 .. 9.3 | – |
| mm_hi_params | 1 | 3.0 | PEX 2 + mm_ok | 7.379 | 2.93 % | 6.902 .. 7.930 | 2.2 .. 9.3 | – |
| mm_hi_params | 1 | 3.0 | PEX 2 (cores without mismatch) | 7.365 | 0.86 % | 7.201 .. 7.534 | 2.2 .. 9.3 | – |
| mm_hi_params | 1 | 3.6 | schematic | 7.102 | 3.28 % | 6.378 .. 7.783 | 2.2 .. 9.3 | – |
| mm_hi_params | 1 | 3.6 | PEX 2 + mm_ok | 7.130 | 3.04 % | 6.678 .. 7.681 | 2.2 .. 9.3 | – |
| mm_hi_params | 1 | 3.6 | PEX 2 (cores without mismatch) | 7.114 | 0.82 % | 6.954 .. 7.278 | 2.2 .. 9.3 | – |
| mm_hi_params | 2 | 3.0 | schematic | 6.605 | 2.68 % | 6.114 .. 7.020 | 2.2 .. 9.3 | – |
| mm_hi_params | 2 | 3.0 | PEX 2 + mm_ok | 6.646 | 2.53 % | 6.207 .. 7.031 | 2.2 .. 9.3 | – |
| mm_hi_params | 2 | 3.0 | PEX 2 (cores without mismatch) | 6.626 | 0.91 % | 6.472 .. 6.786 | 2.2 .. 9.3 | – |
| mm_hi_params | 2 | 3.6 | schematic | 6.371 | 2.75 % | 5.885 .. 6.800 | 2.2 .. 9.3 | – |
| mm_hi_params | 2 | 3.6 | PEX 2 + mm_ok | 6.410 | 2.56 % | 5.979 .. 6.792 | 2.2 .. 9.3 | – |
| mm_hi_params | 2 | 3.6 | PEX 2 (cores without mismatch) | 6.389 | 0.86 % | 6.238 .. 6.544 | 2.2 .. 9.3 | – |
| mm_hi_params | 3 | 3.0 | schematic | 13.607 | 2.13 % | 12.818 .. 14.531 | none (2x) | – |
| mm_hi_params | 3 | 3.0 | PEX 2 + mm_ok | 13.675 | 2.09 % | 12.986 .. 14.391 | none (2x) | – |
| mm_hi_params | 3 | 3.0 | PEX 2 (cores without mismatch) | 13.640 | 0.65 % | 13.410 .. 13.867 | none (2x) | – |
| mm_hi_params | 3 | 3.6 | schematic | 13.406 | 2.15 % | 12.627 .. 14.349 | none (2x) | – |
| mm_hi_params | 3 | 3.6 | PEX 2 + mm_ok | 13.472 | 2.11 % | 12.773 .. 14.191 | none (2x) | – |
| mm_hi_params | 3 | 3.6 | PEX 2 (cores without mismatch) | 13.436 | 0.63 % | 13.207 .. 13.659 | none (2x) | – |

- **The cores dominate the spread.** With only the tree drawing (plain PEX 2), σ(vbp) is 1.1 % at typical, 0.8–1.5 %
  at the worst cases; with the cores drawing it is 4.6–4.9 % for the Oguey-Aebischer core and 2.9–3.0 % for the
  bandgap at typical, and 6.8–7.2 % / 3.3–3.4 % at the low corner. The Oguey-Aebischer core is the one to look at.
- **The layouts don't change the spread measurably.** PEX 2 with `mm_ok` against the schematic: σ 4.58 vs 4.89 %
  (OA) and 2.89 vs 3.02 % (bg) at typical, 6.8 vs 7.2 % and 3.3 vs 3.4 % at the low corner. With 100 runs σ has a
  relative standard error of about 7 %, so these are within noise; the means are 0.4–1 % higher in every PEX case
  (paired seeds, but the extracted fingers draw their own numbers, so the draws aren't the same devices' and this
  isn't a clean paired difference either). Without mismatch the PEX 2 and schematic dc points are identical.
- **Against the limits.** The worst cases pass every `pvt_params` limit in all three views; the tightest margin is the
  Oguey-Aebischer core at ss, −40 °C, 3.0 V: lowest vbp 2.39 µA (schematic) / 2.67 µA (PEX 2 + mm_ok) against 2.2 µA,
  lowest I vbpc 0.92 / 1.02 µA against 0.85 µA. The typical group fails `supply_params`' window (vbp 4.8–5.3 µA,
  vbnc 1.9–2.2 µA, vbpc 1.8–2.1 µA) for every bias current of sel 1 and 2 in the schematic and the `mm_ok` view: that
  window was set from nominal runs (−4 / +6 % around 5 µA), and ±3σ of mismatch is ±15 % (OA) / ±9 % (bg). Even the
  tree alone leaves it on I vbn (sel 1 / 2: down to 4.73 µA). These are the only limit violations of the session; the
  limits are proposals, and this says they need a mismatch allowance, not that the circuit changed.
- **pnpMPA has no mismatch model** in the PDK, so the bandgap's spread here is MOS and rhigh only; the real one is
  larger by the Q1 / Q2 mismatch.
- Convergence: the schematic and `mm_ok` views ran every iteration to a proper op. Plain PEX 2 (default solver
  settings) had 3 / 4 / 0 runs in `mm_params` / `mm_lo_params` / `mm_hi_params` that fell back to a transient op;
  those few points may be off, which doesn't change the tree-only σ of about 1 %.

### Limit violations

- Default groups (`sel`, `pvt`, `supply`, `rpnp`, `iref`, `pd`, `tran`, `psrr`, `startup`), all three views: **none**
  (`make spec-table CORES=…`: 168 pass, 183 report only, per view the same).
- `mm_params` (typical, against `supply_params`): sel 1 and sel 2 fail on every bias current in the schematic and the
  `mm_ok` view, and on I vbn in plain PEX 2 (table above). `mm_lo_params`, `mm_hi_params` (against `pvt_params`):
  none.
- CACE itself reports every group as passing: the mismatch groups carry no limits (`any`), the comparison is
  `make mc-table`'s.

### Per-parameter table: schematic / PEX 2 / PEX 3

Every quantity of every default group, min .. max over the group's runs in the display unit, the limits, the change of
min / max against the schematic in %, and the largest change of a single run (runs matched by their conditions).
Generated by `scripts/cace/compare_views.py`. No run of any view is outside a limit (a violation would be marked
**min** / **max**). The large "largest run" figures of `pvt` / `sel` I ibias are fA-level leakage; of `psrr` at 1 kHz in
PEX 3 they come from the one unconverged run (sel 2, ff, −40 °C).

| group | quantity | unit | limits | bias_sel_pd min .. max | bias_sel_pd_cores_magic_pex_2 min .. max (change %) | bias_sel_pd_cores_magic_pex_2 largest run change % | bias_sel_pd_cores_magic_pex_3 min .. max (change %) | bias_sel_pd_cores_magic_pex_3 largest run change % |
|---|---|---|---|---|---|---|---|---|
| sel_params | Ibp | uA | any | 5.01 .. 10 | 5.01 .. 10 (+0.00 / +0.00) | 0.00 | 5.01 .. 10 (-0.01 / +0.01) | 0.02 |
| sel_params | Ibn | uA | any | 5.02 .. 10.01 | 5.02 .. 10.01 (+0.00 / +0.00) | 0.00 | 5.019 .. 10.02 (-0.01 / +0.01) | 0.02 |
| sel_params | Ibnc | uA | any | 2.059 .. 4.107 | 2.059 .. 4.107 (+0.00 / +0.00) | 0.00 | 2.059 .. 4.108 (-0.01 / +0.01) | 0.02 |
| sel_params | Ibpc | uA | any | 1.925 .. 3.842 | 1.925 .. 3.842 (+0.00 / +0.00) | 0.00 | 1.924 .. 3.842 (-0.01 / +0.01) | 0.02 |
| sel_params | Iabp | uA | any | 4.992 .. 9.978 | 4.992 .. 9.978 (+0.00 / +0.00) | 0.00 | 4.991 .. 9.979 (-0.01 / +0.01) | 0.02 |
| sel_params | Iabn | uA | any | 5.014 .. 10 | 5.014 .. 10 (+0.00 / +0.00) | 0.00 | 5.014 .. 10 (-0.01 / +0.01) | 0.02 |
| sel_params | I_vdd | uA | any | 19.22 .. 56.56 | 19.22 .. 56.56 (+0.00 / +0.00) | 0.00 | 19.22 .. 56.56 (+0.00 / +0.01) | 0.02 |
| sel_params | I_vddo | uA | any | 4.992 .. 9.978 | 4.992 .. 9.978 (+0.00 / +0.00) | 0.00 | 4.991 .. 9.979 (-0.01 / +0.01) | 0.02 |
| sel_params | I_vsso | uA | any | 5.014 .. 10 | 5.014 .. 10 (+0.00 / +0.00) | 0.00 | 5.014 .. 10 (-0.01 / +0.01) | 0.02 |
| sel_params | I_ibias | uA | any | 7.453e-08 .. 5.009 | 7.454e-08 .. 5.009 (+0.02 / +0.00) | 0.03 | 7.454e-08 .. 5.009 (+0.01 / +0.00) | 0.05 |
| pvt_params | Ibp | uA | 2.2 .. 9.3 | 3.087 .. 7.111 | 3.087 .. 7.111 (+0.00 / +0.00) | 0.00 | 3.088 .. 7.112 (+0.02 / +0.02) | 0.02 |
| pvt_params | Ibn | uA | 2.2 .. 9.3 | 3.094 .. 7.124 | 3.094 .. 7.124 (+0.00 / +0.00) | 0.00 | 3.094 .. 7.126 (+0.02 / +0.02) | 0.02 |
| pvt_params | Ibnc | uA | 0.85 .. 3.8 | 1.278 .. 2.9 | 1.278 .. 2.9 (+0.00 / +0.00) | 0.00 | 1.279 .. 2.901 (+0.02 / +0.02) | 0.02 |
| pvt_params | Ibpc | uA | 0.85 .. 3.8 | 1.182 .. 2.739 | 1.182 .. 2.74 (+0.00 / +0.00) | 0.00 | 1.182 .. 2.74 (+0.02 / +0.02) | 0.02 |
| pvt_params | Iabp | uA | 2.2 .. 9.3 | 3.063 .. 7.108 | 3.063 .. 7.108 (+0.00 / +0.00) | 0.00 | 3.064 .. 7.109 (+0.02 / +0.02) | 0.02 |
| pvt_params | Iabn | uA | 2.2 .. 9.3 | 3.09 .. 7.118 | 3.09 .. 7.118 (+0.00 / +0.00) | 0.00 | 3.09 .. 7.119 (+0.02 / +0.02) | 0.02 |
| pvt_params | I_vdd | uA | - .. 50 | 16.98 .. 38.32 | 16.98 .. 38.32 (+0.00 / +0.00) | 0.00 | 16.98 .. 38.33 (+0.02 / +0.02) | 0.02 |
| pvt_params | I_vddo | uA | - .. 9.3 | 3.063 .. 7.108 | 3.063 .. 7.108 (+0.00 / +0.00) | 0.00 | 3.064 .. 7.109 (+0.02 / +0.02) | 0.02 |
| pvt_params | I_vsso | uA | - .. 9.3 | 3.09 .. 7.118 | 3.09 .. 7.118 (+0.00 / +0.00) | 0.00 | 3.09 .. 7.119 (+0.02 / +0.02) | 0.02 |
| pvt_params | I_ibias | uA | any | 3.577e-09 .. 5.011 | 3.562e-09 .. 5.011 (-0.42 / +0.00) | 0.81 | 3.56e-09 .. 5.011 (-0.48 / +0.00) | 0.65 |
| supply_params | Ibp | uA | 4.8 .. 5.3 | 4.996 .. 5.073 | 4.996 .. 5.073 (+0.00 / +0.00) | 0.00 | 4.996 .. 5.073 (-0.01 / +0.00) | 0.02 |
| supply_params | Ibn | uA | 4.8 .. 5.3 | 5.004 .. 5.085 | 5.004 .. 5.085 (+0.00 / +0.00) | 0.00 | 5.004 .. 5.085 (-0.01 / +0.00) | 0.02 |
| supply_params | Ibnc | uA | 1.9 .. 2.2 | 2.052 .. 2.085 | 2.052 .. 2.085 (+0.00 / +0.00) | 0.00 | 2.052 .. 2.085 (-0.01 / +0.00) | 0.02 |
| supply_params | Ibpc | uA | 1.8 .. 2.1 | 1.919 .. 1.949 | 1.919 .. 1.949 (+0.00 / +0.00) | 0.00 | 1.919 .. 1.949 (-0.01 / +0.00) | 0.02 |
| supply_params | Iabp | uA | 4.8 .. 5.3 | 4.975 .. 5.056 | 4.975 .. 5.056 (+0.00 / +0.00) | 0.00 | 4.975 .. 5.056 (-0.01 / +0.00) | 0.02 |
| supply_params | Iabn | uA | 4.8 .. 5.3 | 4.997 .. 5.08 | 4.997 .. 5.08 (+0.00 / +0.00) | 0.00 | 4.997 .. 5.08 (-0.01 / +0.00) | 0.02 |
| supply_params | I_vdd | uA | - .. 40 | 19.17 .. 29.6 | 19.17 .. 29.6 (+0.00 / +0.00) | 0.00 | 19.17 .. 29.6 (+0.00 / -0.01) | 0.02 |
| supply_params | I_vddo | uA | any | 4.975 .. 5.056 | 4.975 .. 5.056 (+0.00 / +0.00) | 0.00 | 4.975 .. 5.056 (-0.01 / +0.00) | 0.02 |
| supply_params | I_vsso | uA | any | 4.997 .. 5.08 | 4.997 .. 5.08 (+0.00 / +0.00) | 0.00 | 4.997 .. 5.08 (-0.01 / +0.00) | 0.02 |
| supply_params | I_ibias | uA | any | 6.513e-09 .. 5.009 | 6.512e-09 .. 5.009 (-0.02 / +0.00) | 0.04 | 6.517e-09 .. 5.009 (+0.05 / +0.00) | 0.10 |
| rpnp_params | Ibp | uA | 2.8 .. 8.5 | 3.968 .. 6.408 | 3.968 .. 6.408 (+0.00 / +0.00) | 0.00 | 3.968 .. 6.402 (-0.01 / -0.10) | 0.20 |
| rpnp_params | Ibn | uA | 2.8 .. 8.5 | 3.976 .. 6.419 | 3.976 .. 6.419 (+0.00 / +0.00) | 0.00 | 3.976 .. 6.412 (-0.00 / -0.10) | 0.20 |
| rpnp_params | Ibnc | uA | 1.1 .. 3.5 | 1.631 .. 2.632 | 1.631 .. 2.632 (+0.00 / +0.00) | 0.00 | 1.631 .. 2.63 (-0.00 / -0.10) | 0.20 |
| rpnp_params | Ibpc | uA | 1.1 .. 3.5 | 1.524 .. 2.462 | 1.524 .. 2.462 (+0.00 / +0.00) | 0.00 | 1.524 .. 2.459 (-0.01 / -0.10) | 0.20 |
| rpnp_params | Iabp | uA | 2.8 .. 8.5 | 3.952 .. 6.387 | 3.952 .. 6.387 (+0.00 / +0.00) | 0.00 | 3.951 .. 6.381 (-0.01 / -0.10) | 0.20 |
| rpnp_params | Iabn | uA | 2.8 .. 8.5 | 3.972 .. 6.411 | 3.972 .. 6.411 (+0.00 / +0.00) | 0.00 | 3.972 .. 6.405 (-0.01 / -0.10) | 0.19 |
| rpnp_params | I_vdd | uA | - .. 50 | 23.38 .. 37.51 | 23.38 .. 37.51 (+0.00 / +0.00) | 0.00 | 23.38 .. 37.47 (-0.00 / -0.10) | 0.19 |
| rpnp_params | I_vddo | uA | any | 3.952 .. 6.387 | 3.952 .. 6.387 (+0.00 / +0.00) | 0.00 | 3.951 .. 6.381 (-0.01 / -0.10) | 0.20 |
| rpnp_params | I_vsso | uA | any | 3.972 .. 6.411 | 3.972 .. 6.411 (+0.00 / +0.00) | 0.00 | 3.972 .. 6.405 (-0.01 / -0.10) | 0.19 |
| rpnp_params | I_ibias | uA | any | 7.555e-08 .. 7.647e-08 | 7.558e-08 .. 7.648e-08 (+0.04 / +0.00) | 0.05 | 7.558e-08 .. 7.649e-08 (+0.04 / +0.02) | 0.04 |
| iref_params | Ibp | uA | any | 2.547 .. 7.566 | 2.547 .. 7.566 (+0.00 / +0.00) | 0.00 | 2.547 .. 7.566 (+0.00 / +0.00) | 0.00 |
| iref_params | Ibn | uA | any | 2.553 .. 7.578 | 2.553 .. 7.578 (+0.00 / +0.00) | 0.00 | 2.553 .. 7.578 (+0.00 / +0.00) | 0.00 |
| iref_params | Ibnc | uA | any | 1.047 .. 3.108 | 1.047 .. 3.108 (+0.00 / +0.00) | 0.00 | 1.047 .. 3.108 (+0.00 / +0.00) | 0.00 |
| iref_params | Ibpc | uA | any | 0.9779 .. 2.906 | 0.9779 .. 2.906 (+0.00 / +0.00) | 0.00 | 0.9779 .. 2.906 (+0.00 / +0.00) | 0.00 |
| iref_params | Iabp | uA | any | 2.534 .. 7.544 | 2.534 .. 7.544 (+0.00 / +0.00) | 0.00 | 2.534 .. 7.544 (+0.00 / +0.00) | 0.00 |
| iref_params | Iabn | uA | any | 2.551 .. 7.568 | 2.551 .. 7.568 (+0.00 / +0.00) | 0.00 | 2.551 .. 7.568 (+0.00 / +0.00) | 0.00 |
| iref_params | I_vdd | uA | any | 9.676 .. 28.73 | 9.676 .. 28.73 (+0.00 / +0.00) | 0.00 | 9.676 .. 28.73 (+0.00 / +0.00) | 0.00 |
| iref_params | I_vddo | uA | any | 2.534 .. 7.544 | 2.534 .. 7.544 (+0.00 / +0.00) | 0.00 | 2.534 .. 7.544 (+0.00 / +0.00) | 0.00 |
| iref_params | I_vsso | uA | any | 2.551 .. 7.568 | 2.551 .. 7.568 (+0.00 / +0.00) | 0.00 | 2.551 .. 7.568 (+0.00 / +0.00) | 0.00 |
| iref_params | I_ibias | uA | any | 2.506 .. 7.511 | 2.506 .. 7.511 (+0.00 / +0.00) | 0.00 | 2.506 .. 7.511 (+0.00 / +0.00) | 0.00 |
| pd_params | Ibp | nA | - .. 0.2 | 4.885e-05 .. 0.04695 | 4.887e-05 .. 0.04695 (+0.06 / +0.00) | 0.12 | 4.89e-05 .. 0.04695 (+0.12 / -0.00) | 0.12 |
| pd_params | Ibn | nA | - .. 0.2 | 0.000577 .. 0.1377 | 0.000577 .. 0.1377 (+0.00 / +0.00) | 0.01 | 0.000577 .. 0.1377 (-0.00 / -0.00) | 0.00 |
| pd_params | Ibnc | nA | - .. 0.1 | 0.0002071 .. 0.05376 | 0.0002071 .. 0.05376 (+0.00 / +0.00) | 0.01 | 0.0002071 .. 0.05376 (+0.00 / +0.00) | 0.00 |
| pd_params | Ibpc | nA | - .. 0.1 | 2.089e-05 .. 0.01767 | 2.09e-05 .. 0.01767 (+0.05 / +0.00) | 0.09 | 2.09e-05 .. 0.01767 (+0.05 / +0.00) | 0.11 |
| pd_params | Iabp | nA | - .. 0.2 | 5.038e-05 .. 0.04713 | 5.037e-05 .. 0.04713 (-0.02 / +0.00) | 0.04 | 5.036e-05 .. 0.04713 (-0.04 / +0.00) | 0.05 |
| pd_params | Iabn | nA | - .. 0.2 | 0.000423 .. 0.1335 | 0.000423 .. 0.1335 (+0.00 / +0.00) | 0.00 | 0.000423 .. 0.1335 (+0.00 / +0.00) | 0.00 |
| pd_params | I_vdd | nA | - .. 6.5 | 0.0128 .. 4.867 | 0.01286 .. 4.882 (+0.42 / +0.29) | 0.71 | 0.01286 .. 4.882 (+0.40 / +0.29) | 0.71 |
| pd_params | I_vddo | nA | - .. 0.1 | 5.022e-05 .. 0.04604 | 5.02e-05 .. 0.04604 (-0.04 / +0.00) | 0.07 | 5.022e-05 .. 0.04604 (-0.00 / +0.00) | 0.05 |
| pd_params | I_vsso | nA | - .. 0.2 | 0.0004204 .. 0.1332 | 0.0004204 .. 0.1332 (+0.00 / +0.00) | 0.00 | 0.0004204 .. 0.1332 (+0.00 / +0.00) | 0.00 |
| pd_params | I_ibias | nA | - .. 0.05 | 1.824e-05 .. 0.02184 | 1.82e-05 .. 0.02174 (-0.21 / -0.48) | 1.04 | 1.804e-05 .. 0.02174 (-1.08 / -0.47) | 1.14 |
| tran_params | t_settle | us | any | 0.1385 .. 30.36 | 0.1458 .. 28.75 (+5.27 / -5.30) | 56.97 | 0.1455 .. 28.57 (+5.05 / -5.88) | 62.33 |
| tran_params | Ibp_end | uA | any | 4.746 .. 5.385 | 4.747 .. 5.385 (+0.01 / +0.01) | 0.01 | 4.747 .. 5.386 (+0.03 / +0.03) | 0.03 |
| psrr_params | P_vdd_1k | %/V | any | 0.8246 .. 1.679 | 0.8255 .. 1.68 (+0.11 / +0.04) | 3.43 | 0.8238 .. 1.679 (-0.10 / +0.00) | 8.22 |
| psrr_params | P_vdd_100k | %/V | any | 0.9652 .. 6.125 | 1.275 .. 9.63 (+32.15 / +57.23) | 160.26 | 1.077 .. 10.51 (+11.54 / +71.63) | 102.01 |
| psrr_params | P_vdd_1M | %/V | any | 4.054 .. 18.46 | 7.253 .. 48.44 (+78.90 / +162.37) | 170.37 | 6.136 .. 39.88 (+51.37 / +116.01) | 135.41 |
| psrr_params | P_vss_1k | %/V | any | 0.871 .. 1.773 | 0.8821 .. 1.774 (+1.27 / +0.04) | 3.08 | 0.8858 .. 1.773 (+1.71 / +0.00) | 11.20 |
| psrr_params | P_vss_100k | %/V | any | 1.098 .. 6.245 | 1.416 .. 9.765 (+28.99 / +56.37) | 158.80 | 1.216 .. 10.65 (+10.79 / +70.55) | 102.00 |
| psrr_params | P_vss_1M | %/V | any | 4.367 .. 19.1 | 7.624 .. 49.34 (+74.60 / +158.32) | 167.70 | 6.391 .. 40.55 (+46.37 / +112.31) | 132.39 |
| psrr_params | P_vddo_1k | %/V | any | 0.848 .. 1.717 | 0.848 .. 1.717 (-0.00 / +0.00) | 0.00 | 0.848 .. 1.717 (-0.00 / -0.00) | 2.05 |
| psrr_params | P_vddo_100k | %/V | any | 0.8715 .. 1.772 | 0.8715 .. 1.772 (+0.00 / +0.01) | 0.01 | 0.8715 .. 1.772 (-0.00 / +0.00) | 2.05 |
| psrr_params | P_vddo_1M | %/V | any | 2.179 .. 4.69 | 2.179 .. 4.691 (+0.02 / +0.03) | 0.11 | 2.179 .. 4.691 (+0.01 / +0.01) | 2.07 |
| psrr_params | P_vsso_1k | %/V | any | 0.2062 .. 0.2683 | 0.2062 .. 0.2683 (+0.00 / +0.00) | 0.00 | 0.2062 .. 0.2683 (-0.00 / +0.01) | 1.53 |
| psrr_params | P_vsso_100k | %/V | any | 0.2612 .. 0.3512 | 0.2612 .. 0.3512 (+0.00 / +0.00) | 0.00 | 0.2612 .. 0.3511 (+0.00 / -0.01) | 1.59 |
| psrr_params | P_vsso_1M | %/V | any | 1.247 .. 2.588 | 1.247 .. 2.588 (-0.00 / +0.00) | 0.00 | 1.246 .. 2.587 (-0.02 / -0.02) | 1.71 |
| startup_params | t_su90 | us | - .. 130 | 0.9009 .. 96.57 | 1.05 .. 97.25 (+16.50 / +0.71) | 87.54 | 1.055 .. 96.81 (+17.10 / +0.25) | 63.67 |
| startup_params | Rbp_end |  | 0.95 .. 1.05 | 1 .. 1 | 1 .. 1 (+0.00 / +0.00) | 0.00 | 1 .. 1 (-0.00 / +0.00) | 0.00 |
| startup_params | Rabn_end |  | 0.95 .. 1.05 | 1 .. 1 | 1 .. 1 (+0.00 / +0.00) | 0.00 | 1 .. 1 (-0.00 / +0.00) | 0.00 |

### Times per group (wall time, CACE_JOBS = 3 on 4 vCPU, final runs)

| group | runs | schematic | magic_pex_2 | magic_pex_3 | magic_pex_2_mm_ok |
|---|---:|---:|---:|---:|---:|
| sel_params | 4 | 4.5 s | 6.9 s | 16 s | – |
| pvt_params | 30 | 16 s | 27 s | 106 s | – |
| supply_params | 9 | 6.9 s | 13 s | 32 s | – |
| rpnp_params | 4 | 5.0 s | 5.4 s | 11 s | – |
| iref_params | 3 | 4.2 s | 4.3 s | 6.6 s | – |
| pd_params | 8 | 8.3 s | 9.6 s | 25 s | – |
| tran_params | 18 | 147 s | 318 s | 324 s | – |
| psrr_params | 27 | 31 s | 54 s | 396 s | – |
| startup_params | 48 | 192 s | 367 s | 515 s | – |
| mm_params | 600 | 293 s | 746 s | – | 1735 s |
| mm_lo_params | 600 | 300 s | 910 s | – | 2302 s |
| mm_hi_params | 600 | 329 s | 789 s | – | 2183 s |

Totals: 3.4 h of wall time for the committed final runs, 5.0 h with the superseded ones. Every group's
rc is 0. `_times.txt` has every run, including the superseded ones.


## Adequacy of the verification (step 4)

What the suite could not show, and what changed (details and undo in `C1_verification_changes.md`):

- **No way to put the layouts in.** The core view switch (condition `cores`, `CORES=` in the Makefile) and the
  `templates/cores/` files. Default unchanged.
- **The dc groups can't see parasitic C**, and a C-coupled extraction moves no dc current (confirmed: PEX 2 = schematic
  to 0.00 % in every dc quantity). Only `tran_params` could. Added `psrr_params` (supply rejection at 1 k / 100 k /
  1 MHz on all four rails) and `startup_params` (supply ramp from 0 V), the measurements of the flat copies' groups,
  now with the real cores and every view.
- **No mismatch in `bias_sel_pd`.** Added `mm_params`, `mm_lo_params`, `mm_hi_params` and `mc-table`.
- **Unseen convergence failures.** The run folders are deleted after each group, so an op that fell back to a transient
  op (which produced the +18 % above) left no trace in the results. `sim-cace` now warns per group.
- **Broken templates.** The `XRP1` / `XRp1` collision stopped ngspice-47 in the DC and tran templates; fixed in
  `bias_sel_pd`, not in the flat copies (omissions 1 and 2).

**Redundant checks.** With `psrr_params`, `startup_params` and the mismatch groups, `bias_sel_pd` with sel 1 / 2 covers
what `bias_oa_pd` and `bias_bg_pd` check, for the cores as they are now; the flat copies still hold the cores as they
were before 2026-10-28, and their psrr templates can't run under ngspice-47. I left them untouched rather than drop
them (omission 1); dropping their CACE is the obvious next step.

**Pad-level CACE (out of scope).** Both pads instantiate the cores through `bias_gen_pd` (`xg`). Their 17 CACE
templates default to `sel` = 0 (the harness current, cores off); only some groups select the cores (Diff2Single: 3 of
15 groups and its loop fixture, Single2Diff: 2 of 14). To show the cores' layouts there they would need: the same
`cores` include before `CACE{DUT_path}` in each template (the view files can be shared: they only define `oa_core_pd` /
`bg_core_pd`), the `cores` condition and the `CORES` logic in their yaml and Makefile, the convergence warning, and a
check for the same case-insensitive name collisions (my scan found none in the pad templates). Their mismatch group
(output offset) would need the `mm_ok` view as well. The pads' own wiring can't be extracted
yet: they have no layout (size mock-ups only).

## Delivered

- `claude/c1-core-pex-verif`:
  - 0ee4cc0: `macros/bg_core_pd/` `netlist/schematic/bg_core_pd_magic.spice`, `netlist/layout/bg_core_pd_magic.ext.spc`,
    `netlist/pex/bg_core_pd_{magic_pex_1,2,3,klayout_pex_2}.spice`, `schematic/xschem/bg_core_pd_pex.sym`,
    `verification/drc/bg_core_pd.magic.drc/bg_core_pd.magic.drc.rpt`, `verification/lvs/bg_core_pd.magic.lvs/bg_core_pd.lvs.out`
    (C0's list; `.log` / `.tcl` are in `.gitignore`). C0's oa_core_pd outputs were already on the branch (82a57ec).
  - 63f7fbb, e692d03, 69715c3, f3d3121, 40af37e, 30d458b, 3bc7e7a, be91b80, 5c1d18c, 8a72dd8: the verification changes (`C1_verification_changes.md`), `results/bias_sel_pd/`
    rerun plus `psrr` / `startup` / mismatch CSVs, `results/bias_sel_pd_cores_magic_pex_2/`, `_magic_pex_3/`,
    `_magic_pex_2_mm_ok/`. CSV, CACE summaries and the CACE plots.
- `claude/c1-core-pex-verif-sudel`: 172 files in `sudelbuecher/logs/claude/c1-core-pex-verif/` (logs of every
  target and CACE group, `_times.txt`, `env.*`, and the superseded runs in `superseded_*/`), one `MANIFEST.tsv` row each;
  this report; `C1_verification_changes.md`; the chatlog `sudelbuecher/chatlog/2026-10-30_opus_c1_core_pex_bias_verification.md`
  with its README entry.
