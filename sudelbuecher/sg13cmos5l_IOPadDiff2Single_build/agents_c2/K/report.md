# K: capacitor types for the Miller capacitors CMA / CMB of sg13cmos5l_IOPadDiff2Single (ngspice)

Agent K, 2026-10-31 (Europe/Berlin). Brief: `BRIEF.md`; A5's questions 1–5 plus simulation. Workspace `/home/user/c2/K/`.
Labels: **[sim]** = simulated here (deck and log named), **[PDK]** / **[spec]** / **[rules]** = read from the PDK files or
the two PDFs (file and line or section; `spec` = `inputs/notes/SG13CMOS5L_os_process_spec.txt`, `rules` =
`inputs/notes/SG13CMOS5L_os_layout_rules.txt`, line numbers of those text files), **[est]** = my reasoning or estimate.

## Short answers to Christoph's three questions

See "Short answers (final)" at the end of the file (written after stage 4).

## Preliminaries

**Model files against A5's hashes [PDK].** All PDK files of `inputs/notes/A5_inputs.md` that exist here have the same
sha256 prefix and size as in Christoph's checkout `6ac9bb9d` (the environment PDK is `df4c5054`): the two PDFs,
`cap_cmomf.lib`, `cap_cmomi.lib`, `cornerCAP.lib`, `cornerMOSCAP.lib`, `sg13g2_moscap_mod.lib`, `sg13g2_moscap_parm.lib`,
`sg13g2_svaricaphv_mod.lib`, `cornerMOShv.lib`, `sg13g2_moshv_mod.lib`, `sg13g2_moshv_parm.lib`, both MOM `.va`, `mosvar.va`,
`mosvarpspMacros.va`, the five PCell `.py`, the six symbol / tcl files and `sg13cmos5l_maximal.drc`. The five macro files
(netlists, README, `.klay.gds`) also match. **No difference found.** One file could not be compared:
`ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/layers_def.drc` does not exist in this checkout (the cmos5l
`layers_def.drc` is a dangling link to it). The OSDI objects in `$PDK_ROOT/$PDK/libs.tech/ngspice/osdi/` exist, nothing was
compiled (`cap_cmomf.osdi` is byte-identical to the one in `/foss/tools/osdi/ihp-sg13cmos5l-df4c5054…/`).

**Templates run unchanged first [sim].** In a copy (`work/repo`), CACE 2.11.0, `-s schematic`:
- `d2s_mpdda_pd_sel.yaml -p loop_load_params` (6 runs, `out/logs/cace_loop_load_unchanged.log`): PM 72.55° / fc 1.371 MHz /
  T0 79.05 dB at 1 kΩ ∥ 100 pF (committed `results/d2s_mpdda_pd_sel/loop_load_params.csv`: 72.43° / 1.370 MHz / 78.91 dB;
  the 0.1° / 0.14 dB are the newer PDK checkout); worst case PM 42.2° at 300 pF unloaded (committed 41.96°).
- `sg13cmos5l_IOPadDiff2Single.yaml -p dc_params tran_params` (39 runs, `out/logs/cace_pad_dc_tran_unchanged.log`): gain
  0.500, I_Q 215.5 µA; tt 100 pF step ts 0.329 / 0.336 µs, overshoot 0 (committed 0.327 / 0.334 µs, 0).
- No `Transient op started`, no `Timestep too small` in any run; 10 runs had "Dynamic gmin stepping failed" followed by
  "True gmin stepping completed" (valid op). The `undriven node: vinn / vinp` lines in CACE's `error.log` come from
  xschem's netlister on the E sources, not from a simulation.

## Stage 1 — Inventory and voltage windows

### 1.1 Candidate structures

| structure | inversion? | terminals (well / substrate) | oxide, allowed V | C per µm² | series R | layers, metals | PCell parameters | model status |
|---|---|---|---|---|---|---|---|---|
| **hv PMOS** as now (`sg13_hv_pmos`, S/D/NW tied) | **yes**: the p+ S/D supply holes, so below V_GW ≈ −0.7 V C returns to C_ox [sim, deck 1] | gate; S/D/NW = **n-well** (on a signal node; NW–substrate diode not in the model) | thick: TGOX1NW 7.3 nm [spec l.705]; V_GS ≤ 3.3 V for L ≥ 0.5 µm [spec §2.1.5, l.376]; model toxo 6.945 nm [`sg13g2_moshv_parm.lib` l.357] | 1.6 … 4.7 fF/µm² of gate [sim]; C_ox(7.3 nm) = 4.73 [est] | accumulation / inversion layer across L = 32 µm, not in the quasi-static model (§2.3) | Activ, GatPoly, ThickGateOx, pSD, NWell, Cont, Metal1 | `pmosHV`: w, l, ng (registered in cmos5l) | PSP 103.6, IHP-characterised MOS with corners and mismatch [PDK] |
| **S-Varicap** `sg13_hv_svaricap` (G1 W G2 bn) | **no**: n+ poly over n-well, n+ contacts only (accumulation / depletion, no hole source) [model `type=-1`; DRC `SVaricap_gate_0 = NGate…NWell…ThickGateOx`, `sg13cmos5l_maximal.drc` l.1785] | G1, G2 gates; **W = n-well**; bn = substrate (well–sub diode `dsubw` and `rsubw` in the model) | thick (ThickGateOx replaces nBuLay in cmos5l, `__init__.py` l.51); model toxo 6.945 nm [`sg13g2_svaricaphv_mod.lib` l.48]; 3.3 V class [est: same oxide as hv MOS] | 1.8 … 5.1 fF/µm² of gate (9.74 / 0.8), 2.5 … 5.8 (3.74 / 0.3) [sim, deck 4]; spec 23 / 35.3 / 39.5 "fF/µm²" at −3 / 0 / +3 V [spec §2.2.4 l.505–511, note a] | well R `rww` ≈ 100 Ω for Nx = 6 [est from model l.31–33, l.62]; Q 43–62 at 15.8 GHz [spec] | Activ, GatPoly, ThickGateOx, NWell, pSD tie ring, Cont, **Metal1 only** | `SVaricap`: w ∈ {3.74, 9.74} µm, l ∈ {0.3, 0.8} µm, Nx 1…10, bn [`SVaricap_code.py` l.30–40]; model W 3.74–9.74, L 0.3–0.8, Ny = 1 | mosvar 1.3 (Verilog-A → `mosvar.osdi`), sg13g2 fit, corner factors in `cornerMOShv.lib` l.115–121 |
| **moscap_p** `sg13_moscap_p` (G NW) | yes (thin PMOS, S/D/B = NW) | G; **NW** | **thin**: model toxo 1.97 nm [`sg13g2_moscap_parm.lib` l.182]; lv V_GS ≤ 1.65 V at 125 °C [spec §2.1.2 l.269] | 2.4 … 15.5 fF/µm² [sim, deck 2] | — | Activ, GatPoly, pSD, NWell, Cont, Metal1 | **not available in cmos5l**: `moscap_p_code.py` is linked but not in `moduleNames` (`__init__.py` l.47–76), no `moscap_*` entries in `sg13cmos5l_tech.json`; KLayout's SG13_dev library lists no moscap [sim, `work/pcellbox.py`] | PSP, sg13g2 parameters |
| **moscap_n** `sg13_moscap_n` (G SUB) | yes (thin NMOS, S/D/B = SUB) | G; **SUB = p-substrate** (= iovss) | thin, toxo 2.24 nm [l.53]; ≤ 1.65 V | 1.6 … 14 fF/µm² [sim, deck 3] | — | Activ, GatPoly, pSD, Cont, Metal1 | not available (as moscap_p) | PSP, sg13g2 parameters |
| **cap_cmomf** (fringe MOM) | n/a, linear | PLUS, MINUS; no substrate node | none | **0.677** (M1–M2), 1.287 (M1–M4) fF/µm² of footprint [sim, deck 5] = 0.372 + 0.305·(mmax − mmin) [`cap_cmomf.lib` header] | none modelled | Metal1…Metal4 (mmin / mmax), vias, Recog 99/40, NoMetFiller | w, l, mmin, mmax, subblock | "LOW-FREQUENCY MODEL ONLY — NOT VALIDATED ON SILICON", density from the Magic generator recalibrated against OpenEMS; no corners, no mismatch [`cap_cmomf.lib`, `cornerCAP.lib`] |
| **cap_cmomi** (interdigitated MOM) | n/a, linear | PLUS, MINUS (SUB tied to 0 in the wrapper) | none | 0.528 (M1–M2, N = 2 extrapolated), 1.038 (M1–M4) fF/µm² [sim, deck 5] | RF R / L fit; SRF 30–47 GHz for large cells | Metal1…Metal4, Recog 99/39 | w, l, mmin, mmax, feed, subblock | "APPROXIMATE MODEL — NOT YET VALIDATED ON ihp-sg13cmos5l SILICON", sg13g2 coefficients transferred by layer count [`cap_cmomi.lib`] |
| MIM | — | — | — | — | — | MIM 36/0 and Vmim 129/0 are **forbidden** in cmos5l [rules §3.2, l.645, 655] | none | none |
| MVaricap | — | — | — | — | — | the DRC recognises it (`sg13cmos5l_maximal.drc` l.1801), the tech json names a model (l.588) | **no PCell, no ngspice model** | — |
| junctions (p+/NW, n+/p-sub) | — | one side is always a well or the substrate | — | 0.8–0.95 fF/µm² at 0 V [spec CJUNCTION*, l.255, 295, 362, 402], falls with reverse bias, conducts forward | — | — | `dpantenna`, `dantenna` | `diodes.lib`, reverse direction only |

Notes:
- (a) **S-Varicap spec units.** 39.5 fF/µm² is 8× the thick-oxide C_ox (4.73 fF/µm²), so the spec value cannot be per µm²
  of gate. The model gives 129 / 105 / 56 fF in total for the spec structure (10 × 3.74 × 0.3, two gates, 22.4 µm²) at
  +3 / 0 / −3 V [sim, deck 4]; the ratio C(−3 V) / C(+3 V) is 0.58 in the spec and 0.43 in the model. Open point: what the
  spec's unit refers to (and the spec measures at 15.8 GHz, the deck at 100 kHz).
- (b) Thin-oxide devices (moscap_p / _n) are out: CMA / CMB see up to 1.8 V in the linear range and 2.9 V with the output
  at the rail (stage 3); the lv oxide is rated 1.65 V. moscap_n is a capacitor to the substrate and cannot be a Miller
  capacitor at all. Neither PCell is available in cmos5l.
- (c) **"MOS-type gates that do not go into inversion" exist: the S-Varicap.** But not inverting is not what helps. The
  present hv PMOS loses capacitance in **depletion** (V_GW ≈ −0.6 … +1.2 V: p+ poly over n-well puts flatband near
  +1 V), and inversion actually *restores* its capacitance below −0.7 V. The S-Varicap's dip sits about 1 V lower (n+ poly,
  flatband near 0 V) and, without inversion, it stays depleted below that (1.8 fF/µm² at −3 V). What makes the S-Varicap
  useful here is the **position** of its window relative to the bias CMA / CMB see (stage 3), not the missing inversion.

### 1.2 DRC rules that concern the candidates

| candidate | rules |
|---|---|
| hv PMOS | NWell enclosure of P+Activ in ThickGateOx 0.62 µm (NW.c1, rules l.774); NW space to N+Activ in TGO 0.62 (NW.d1, l.776); TGO.a–f (l.971–978); pSD.i1 0.40 (l.1142). Wells on different nets ≥ 1.80 µm apart (NW.b1, l.772): CMA's well (pad) and CMB's well (b) are different nets. |
| S-Varicap | recognised by NGate inside NWell and ThickGateOx plus the `SVaricap` text (`sg13cmos5l_maximal.drc` l.1785–1850); excluded from the generic NWell / pSD / Cont device rules (`devExclud`, l.1874), its own pSD tie (`SVaricap_Tie`, l.1881). PCell guard ring options NONE or NWELL only (`SVaricap_code.py`, `validGuardRingTypes`). |
| MOM | no MOM-specific rules in `sg13cmos5l_maximal.drc` (Recog 99/39–40 are not referenced); Metal1–4 width / space / density and metal slits (§7.3; `sltc_M*` exempt only Recog 99/0 and pads, drc l.1698–1702); the PCell draws NoMetFiller. |
| all | antenna §7.1: Ant.b ≤ 200 × gate area of metal without a diode, Ant.e ≤ 20 000 with one (rules l.2223, 2228). |

### 1.3 ESD, latch-up and antenna per option

| option | gate on the pad? | well on the pad? | latch-up (rules §7.2) | antenna (§7.1) |
|---|---|---|---|---|
| CMA hv PMOS (gate a, S/D/NW pad), now | no | **yes**: NW–substrate diode on the pad, and p+ S/D in a pad-driven well = p+/NW/p-sub, a PNP injector when the pad undershoots | §7.2.1 item 3: guard rings (VSS / VDD ties) around devices tied directly to a pad; items 4–5: double rings toward the internal circuit (rules l.2326–2335); LU.a / LU.b ≤ 20 µm to a tie (l.2353 ff.). Keep it in the ESD zone inside the clamps' rings, as now (`layout_primitives.md` P9) | gate on a (a drain node, i.e. diffusion-protected): fine [est] |
| CMB hv PMOS (gate pad, S/D/NW b), now | **yes**: 7 nm oxide directly on the pad, no secondary stage (CDM stresses gates directly, `ihp_sg13cmos5l_io_esd_notes.tex` l.253–257) | no (well on b) | floating n-well (net b) near the output clamps: ring it | pad has the clamp drains: fine |
| CMB hv PMOS turned (gate b, S/D/NW pad) | no | yes (as CMA) | as CMA | fine |
| S-Varicap, orientations as now | CMB type: yes (gate on pad) | CMA type: yes (W on pad) | n+ only inside the well, **no p+ in the well**: a pad-driven S-Varicap well is a plain NW/p-sub diode with its own pSD tie ring, no PNP emitter: less latch-up exposure than a pad-driven hv PMOS well [est] | as hv PMOS |
| MOM | no oxide on the pad | no well | none | metal only; on a gate node it counts toward Ant.b (an 840 fF M1–M2 MOM is ≈ 1270 µm² × 2 layers, below 200 × 256 µm² = 51 200 µm²) [est] |
| thin-oxide moscap | — | — | — | excluded (oxide rating) |

IHP itself puts a ≈ 1200 µm² thick-oxide MOS capacitor into its rail clamps (`ihp_sg13cmos5l_io_esd_notes.tex` l.94):
thick-oxide MOS capacitors in a pad cell are established practice; a gate *on the pad* is what IHP's own cells avoid.

## Stage 2 — C(V)

Decks `out/decks/cv1_hvpmos.spice` … `cv5_mom.spice` (one per candidate type; logs and data `out/logs/cv*.log / .dat`).
Method: V(T1) − V(T2) swept −3.3 … +3.3 V in 50 mV steps (133 points), at each point an AC analysis at 100 kHz (the spec's
capacitance condition [A.k] / [A.aq], spec l.946 ff.), C = −Im(I)/(2πf), tt, 27 °C, normalised per µm² of gate (MOS) or of
drawn footprint w × l (MOM). No convergence warnings, no transient op in any C(V) log [sim].

Plots: `out/cv_candidates.png` (all), `out/cv_thick_oxide.png` (the two usable ones; CMA and CMB connection of the hv PMOS).

### 2.1 C(V) per µm², fF/µm² [sim]

V = V(gate) − V(well) for the MOS types (CMA: V(a) − V(pad); CMB: V(pad) − V(b)); the hv PMOS in CMB connection is the same
curve mirrored (column B in `cv1_hvpmos.dat`, checked: identical to 4 digits).

| V (V) | −3.3 | −2 | −1 | −0.7 | −0.5 | 0 | 0.5 | 1 | 1.5 | 2 | 3.3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hv PMOS 7.96 / 32.16 (CMA, CMB now) | 4.46 | 4.44 | 4.16 | 3.18 | 1.62 | 1.78 | 2.26 | 3.31 | 4.15 | 4.44 | 4.66 |
| hv PMOS 8 × 7.96 / 4.02 (same area) | 4.51 | 4.48 | 4.20 | 3.25 | 1.69 | 1.84 | 2.31 | 3.34 | 4.18 | 4.48 | 4.70 |
| hv PMOS, rfmode = 1 (NQS), read at 2 MHz | 4.62 | 4.60 | 4.30 | 3.28 | 1.68 | 1.85 | 2.34 | 3.43 | 4.29 | 4.60 | 4.83 |
| S-Varicap Nx 10, 9.74 / 0.8 | 1.76 | 1.77 | 2.18 | 2.47 | 2.77 | 3.98 | 4.63 | 4.86 | 4.97 | 5.03 | 5.11 |
| S-Varicap Nx 10, 3.74 / 0.3 (spec structure) | 2.48 | 2.49 | 2.90 | 3.18 | 3.47 | 4.66 | 5.30 | 5.53 | 5.64 | 5.70 | 5.78 |
| moscap_p 10 / 10 (thin; valid \|V\| ≤ 1.65) | 11.05 | 11.86 | 12.21 | 11.87 | 10.77 | 2.36 | 3.39 | 9.50 | 13.44 | 14.55 | 15.46 |
| moscap_n 10 / 10 (thin; to substrate) | 13.94 | 13.13 | 7.15 | 2.92 | 2.18 | 1.60 | 11.40 | 12.50 | 12.82 | 12.92 | 12.86 |
| cap_cmomf M1–M2 / M1–M4 (footprint) | 0.68 / 1.29 | … | … | … | … | … | … | … | … | … | 0.68 / 1.29 |
| cap_cmomi M1–M2 / M1–M4 (footprint) | 0.53 / 1.04 | … | … | … | … | … | … | … | … | … | 0.53 / 1.04 |

Per µm² of **layout** (PCell boxes from KLayout, `work/pcellbox.py` [sim]): hv PMOS 7.96 / 32.16 = 34.08 × 9.20 µm
(313.5 µm²; the drawn CMA / CMB n-wells are 35.4 × 9.2 = 326 µm²) for 256 µm² of gate, i.e. × 1.27; S-Varicap Nx 10
9.74 / 0.8 = 22.11 × 12.35 µm (273 µm²) for 155.8 µm² of model gate (× 1.75; 162 µm² GatPoly ∩ Activ); S-Varicap
3.74 / 0.3 Nx 10 = 12.11 × 6.35 µm (77 µm²) for 22.4 µm² (× 3.4); cap_cmomf 20 × 20 → 20.0 × 20.5 µm; cap_cmomi 20 × 20 →
21.1 × 20.2 µm. The S-Varicap PCell has 2.1 µm of width per column at l = 0.8 (1.1 at l = 0.3) and height w + 2.61 µm.

### 2.2 Reading

- **hv PMOS (now):** C_ox plateau 4.4–4.7 fF/µm² at |V| ≥ 1.5 V on either side; a **depletion dip of 1.6–2.3 fF/µm²
  between −0.6 and +0.6 V**, recovering only above +1.5 V (accumulation, flatband ≈ +1 V for p+ poly on n-well [est]) and
  below −0.8 V (inversion, holes from the p+ S/D). Its 50 %-point is at +0.75 V and −0.6 V. ccomp.spice's "0.4 … 0.8 of
  C_ox in use" (comment, `netlist/source/d2s_mpdda.spice`) is what this curve gives at V_GW = 0.15 … 1.15 V.
- **S-Varicap:** the same oxide, but the dip is shifted about −1 V: ≥ 4.6 fF/µm² (≥ 90 % of its maximum) for V ≥ +0.5 V,
  3.98 at 0 V, then falling to 1.8 at −2 V and staying there (no inversion). Over the V_GW window CMA / CMB see in the linear
  range (−0.2 … +1.8 V, stage 3) it varies 3.5 … 5.0 fF/µm² (factor 1.43) against 1.68 … 4.36 (factor 2.6) for the hv PMOS.
- **Thin-oxide moscaps:** 3× the density, but dip in the middle of their range and rated for 1.65 V only; excluded (§1.1 b).
- **MOM:** flat by construction; 0.68 fF/µm² (cmomf M1–M2), i.e. 6–7× less than either thick-oxide device at its plateau.
- **Frequency / NQS:** with rfmode = 1 (PSP NQS, `swnqs = 5`, `sg13g2_moshv_parm.lib` l.600) the model shows no difference
  between 100 kHz and 2 MHz (the ≈ 3 % offset is the rf card's other `cfrw`). My own estimate of the channel RC for the
  32 µm long device in inversion, τ ≈ (L/2)²/(µ·V_ov)·4/π² ≈ 35 ns (µ_p ≈ 100 cm²/Vs, V_ov 0.3 V), i.e. a corner near
  4–5 MHz, is not confirmed by the model [est]; splitting into 8 fingers of L = 4 µm costs +1 % C and makes it 64× faster
  — cheap insurance if the device is kept.

## Stage 3 — Voltage across CMA / CMB, depletion, splits, area and fit

### 3.1 DC swing of the pad and the bias of CMA / CMB [sim]

Deck `out/decks/dc6_swing.spice` (log `out/logs/dc6_swing.log`, data `dc6_swing.dat`): the pad's schematic netlist with the
sources of the CACE template `sg13cmos5l_IOPadDiff2Single_tb_dc.sch` unchanged (tt, 27 °C, sel 0, 5 µA harness bias), one
sweep vd = −3.3 … +3.3 V (template: ±1 V), two instances: x1 with the template load (1 kΩ to 1.65 V ∥ 100 pF), x2 unloaded.
Op: "Dynamic gmin stepping completed", no transient op. (a, b are `net2`, `net3` in the netlisted pad.)

| vd (V) | pad (V) | a = OP gate (V) | b = ON gate (V) | V_GW CMA = a − pad | V_GW CMB = pad − b | state |
|---|---|---|---|---|---|---|
| −3.3 | 0.901 | 2.677 | 0.839 | +1.78 | +0.06 | bottom limit: front-end input range, not the output stage |
| −1.3 | 1.006 | 2.677 | 0.821 | +1.67 | +0.19 | linear |
| 0 | 1.650 | 2.632 | 0.663 | +0.98 | +0.99 | linear, mid-rail |
| +1.3 | 2.306 | 2.467 | 0.619 | +0.17 | +1.69 | linear, top |
| +1.5 … +3.3 | 3.277 (3.300 unloaded) | 0.38–0.43 | 0.35–0.40 | −2.9 | +2.9 | **saturated**: loop open, OP fully on |

- **The pad does not reach the rails in linear operation.** It tracks vd/2 from 0.94 to 2.31 V (1 kΩ load) and then jumps
  to 3.28 V between vd = 1.3 and 1.5 V (the PMOS input pairs and the vref / vfb units leave their common-mode range, the
  loop opens, OP turns fully on); below vd ≈ −1.5 V it stops at 0.90 V (unloaded 0.896 V) for the same reason. README
  finding 6 reports 0.64–0.74 V low at vd = −3 V; the difference is the bias / PDK state, not investigated.
- **Where the present hv PMOS is depleted** (C < 50 % of its plateau, i.e. −0.6 < V_GW < +0.75 V, stage 2):
  **CMA from pad ≈ 1.9 V up to the top of the linear range** (V_GW 0.6 → 0.17; 2.3 → 1.9 fF/µm², 41 % of plateau at
  pad 2.3 V); **CMB from pad ≈ 1.4 V down to the bottom** (V_GW 0.6 → 0.06; 41 % at pad 0.9 V). At mid-rail both sit at
  V_GW ≈ 1 V, on the steep flank (3.3 fF/µm², 70 %). In saturation (pad 3.28 V) CMA is in inversion and CMB in accumulation
  (both ≈ 95 %).
- Side finding [sim]: the transient-op fallback of a failed op (deck 7 trial runs with S-Varicaps, `work/t1.dat`, `t3.dat`,
  `t4.dat`; and deck 9 v4, `out/logs/loop9_300p_v4_*.log`) lands in the saturated state (pad 3.28–3.30 V, a ≈ b ≈ 0.05 V) at vd = 0, i.e. the loop has a **second stable DC state** at the top rail. Whether the
  pad returns from it when vd goes back is not checked (no reverse sweep); open point for the driver, not for the caps.

### 3.2 Splits (each sized for the present C at mid-rail: CMA 837 fF, CMB 840 fF) [sim + est]

C along the swing from the C(V) curves (decks 1, 4, 5) at the V_GW of deck 6 (`work/splits.py`, `work/cmbcombo.py`,
`work/cmacombo.py`); flatness = max / min of C over the linear range (pad 0.95 … 2.31 V). "Turned" = gate and well swapped
(sees −V_GW). Area = layout footprint (present drawn NWell 326 µm² per 256 µm² gate; S-Varicap PCell box × 1.82 per µm² of
gate from Nx 6 + Nx 5; cmomf box 1.025 × w·l). Plot: `out/c_along_swing.png`.

**CMB** (V_GW 0.06 … 1.69 V linear, 2.92 V saturated):

| option | C at pad 0.90 / 1.00 / 1.65 / 2.30 / 3.28 (fF) | max / min (linear) | min / mid | gate µm² | area µm² | gate on pad | well on pad |
|---|---|---|---|---|---|---|---|
| present hv PMOS 7.96 / 32.16 | 466 / 487 / 840 / 1098 / 1185 | **2.31** | 0.57 | 256 | 326 | yes | no |
| hv PMOS turned (gate b, well pad), same C | 354 / 342 / 840 / 894 / 905 | 2.62 | 0.38 | 203 | 258 | no | yes |
| hv PMOS turned, same 256 µm² (loop variant v3) | 447 / 432 / 1060 / 1128 / 1142 | 2.77 | — | 256 | 326 | no | yes |
| anti-parallel hv PMOS 50 / 50 | 410 / 415 / 840 / 996 / 1045 | 2.42 | 0.49 | 229 | 292 | yes (half) | yes (half) |
| S-Varicap (gate pad, well b) | 708 / 740 / 840 / 863 / 881 | 1.19 | 0.86 | 173 | 315 | yes | no |
| S-Varicap turned (gate b, well pad) | 1471 / 1363 / 840 / 700 / 674 | 1.20 | 0.83 | 383 | 699 | no | yes |
| **S-Varicap 80 % ∥ S-Varicap turned 20 %** (v4: Nx 9 + Nx 5) | 874 / 878 / 853 / 843 / 852 | **1.04** | 0.99 | 218 | ≈ 400 (box 33.4 × 12.35 = 413) | yes (80 %) | yes (20 %) |
| S-Varicap 70 % ∥ turned 20 % ∥ hv PMOS 10 % | 829 … 854 (linear) | 1.03 | 0.99 | — | 393 | yes | yes |
| S-Varicap 90 % ∥ turned 10 % | 794 … 847 (linear) | 1.07 | 0.95 | — | 354 | yes | yes |
| S-Varicap 70 % ∥ hv PMOS 30 % (v2) | 651 / 680 / 858 / 952 / 991 | 1.43 | 0.77 | 201 | 318 | yes | no |
| only gate-off-pad parts: hv PMOS turned 50 % ∥ S-Varicap turned 50 % | 693 … 882 (linear) | 1.27 | 0.83 | — | 478 | **no** | yes |
| hv PMOS 50 % ∥ MOM M1–M2 50 % | 653 / 664 / 840 / 969 / 1012 | 1.48 | 0.78 | 128 | 798 | yes | no |
| S-Varicap 50 % ∥ MOM M1–M2 50 % | 774 / 790 / 840 / 851 / 860 | 1.10 | 0.93 | 86 | 793 | yes | no |
| **MOM cap_cmomf M1–M2 only** (passive reference) | 840 flat | 1.00 | 1.00 | 0 | **1271** (M1 + M2) | no | no |

**CMA** (V_GW 1.78 … 0.17 V linear, −2.90 V saturated): the mirror image, same numbers within 1 %: present 2.28,
S-Varicap 1.17 (734 … 861 fF, but 302 fF = 36 % in saturation, where V_GW = −2.9 V depletes it), S-Varicap 80 % ∥ turned
20 % 1.04 (390 µm², 75 % in saturation), S-Varicap 70 % ∥ turned 20 % ∥ hv PMOS 10 % 1.03 (391 µm², 85 % in saturation),
70 / 30 S-Varicap / hv PMOS 1.41, MOM 1.00 at 1267 µm². For CMA, "turned" puts the gate on the pad, so the 20 % turned part
of CMA would add a gate on the pad that CMA does not have now.

The complementary pair works because the two S-Varicap orientations have mirror-image C(V) around V_GW = 0 and CMB's
V_GW stays on the positive side: the main part rises with V_GW (4.0 → 5.0 fF/µm² from 0 to 1.7 V), the turned part falls
(4.0 → 1.9). The hv PMOS cannot be flattened the same way: its two orientations both dip at the same place (−0.6 … +0.75 V),
so an anti-parallel hv PMOS pair is *worse* (2.42) than one device. Thin moscaps would complement better in principle but
are excluded (oxide, not in the cmos5l PCell library).

### 3.3 Where it fits [sim: GDS measurement `work/gdsfree.py`, `work/slot.py` on the `.klay.gds`]

| zone of the 80 × 180 µm cell | free Metal1 / Metal2 (µm², minus min space) | free of devices + M1 + M2, pieces ≥ 5 × 5 µm |
|---|---|---|
| y 0–84 (clamps, diodes, CMA / CMB) | 2976 / 3643 in fragments | **none** (largest 3 µm pieces: 26 µm² at the corners) |
| y 84–119 | 2808 / 2668 (nothing drawn yet) | one 80 × 92 µm block above y 88 (amplifier not drawn yet; planned full, `layout_primitives.md` §4) |
| y 119–126, 134–140 (the only Metal3 gaps) | — | Metal3 free 535 / 454 µm² |
| Metal3 / Metal4 elsewhere | 965 / 965 below y 84 and 156 at y 84–119 in slivers | — |

- **MOM:** Metal3 / Metal4 / TopMetal1 carry the ring buses (Christoph's suspicion holds), so a MOM is limited to
  Metal1–Metal2 = 0.68 fF/µm² (cmomf). 840 fF needs **≈ 1270 µm² of M1 + M2**: nothing like that is free in the ESD zone,
  and in the amplifier zone it would take 45 % of the 2800 µm² PMOS band. A single-layer M2 MOM over the S-Varicaps (they use
  Metal1 only) would add ≈ 0.3 fF/µm² (cmomf base for mmin ≠ 1 [`cap_cmomf.lib`]) → ≈ 120 fF over 400 µm² [est], but the
  Metal2 over the cap slot is already used by the pad comb / straps (free M2 there after removing the caps: 64 µm²).
- **Present slots:** `cap_cma` 35.4 × 11.5 µm (x 2.6–38.0, y 39.3–50.8), `cap_cmb` 35.4 × 9.4 µm (x 39.8–75.2, y 41.5–50.8),
  between DCN and DCP; removing them frees only that box (the M1 / M2 around them belongs to other cells).
- **S-Varicap at equal C:** 9.74 / 0.8 µm is the dense choice (Nx 10: 22.1 × 12.35 µm). The 171 µm² variant (Nx 6 + Nx 5)
  is ≈ 26 × 12.35 µm: **9 µm shorter but 1–3 µm taller than the present slots.** The CMB 80 / 20 pair (Nx 9, well b, and
  Nx 5, well pad, ≥ 1.8 µm apart, NW.b1) is 20.0 + 1.8 + 11.6 = 33.4 × 12.35 µm: **it fits the slot's 35.4 µm width and
  needs 12.35 µm of height instead of 9.4 µm** — +3 µm in y between the diodes, or a slot elsewhere in the ESD zone. With
  w = 3.74 µm (6.35 µm high) the same C needs ≈ 2 × the area (the PCell's fixed overhead per column), so it does not help.
  Whether the band between DCN and DCP can give up 3 µm is for the layout agent.

## Stage 4 — Phase margin and step response

### 4.1 Setup [sim]

- Variants (`out/decks/dut_variants.spice`, generated by `work/mkvar.py` from the CACE netlist of the fixture
  `d2s_mpdda_pd_sel`, `out/decks/dut_fixture.spice`; CMA / CMB replaced, everything else unchanged):
  - **v0** present: 2 × hv PMOS 7.96 / 32.16 (256 µm² each);
  - **v1** S-Varicap for both, same orientations (CMA gate a / well pad, CMB gate pad / well b), each Nx 6 + Nx 5, 9.74 / 0.8
    (171 µm² gate, same mid-rail C as now);
  - **v2** both 70 % S-Varicap (Nx 8) ∥ 30 % hv PMOS (7.96 / 9.65);
  - **v3** CMA present, **CMB turned around** (hv PMOS 7.96 / 32.16, gate b, S/D/NW pad) — the same device, so 26 % more C at
    mid-rail;
  - **v4** CMA present, **CMB = S-Varicap Nx 9 (gate pad, well b) ∥ S-Varicap Nx 5 turned (gate b, well pad)**, the flattest
    pair of §3.2 (Christoph's 16:50 target).
- Deck 7 `loop7_variants.spice`: loop gain as the CACE template `d2s_mpdda_pd_sel_tb_loop.sch` (loop broken at vfb, 1 GH /
  1 F, T = −v(vout)/v(fb), same `meas`), 1 kΩ to 1.65 V ∥ 100 pF, plus a differential input vd = 0 / +1.3 / −1.3 V to put the
  pad at 1.65 / 2.29 / 0.99 V (three operating points, no sweep). Deck 9 `loop9_300p.spice` = deck 7 at the CACE worst-case
  load (unloaded ∥ 300 pF). Deck 8 `step8_variants.spice`: closed loop (vfb = vout), 1 kΩ ∥ 100 pF, the CACE `tb_tran`
  step vd −0.5 ↔ +0.5 V (pad 1.40 ↔ 1.90 V) and a step at the top of the linear range vd 0.8 ↔ 1.3 V (pad 2.05 ↔ 2.29 V),
  measurements as `tb_tran`. One DUT per run (`work/run78.sh` selects the variant and vd); logs `out/logs/loop7_variants_*`,
  `loop9_300p_*`, `step8_variants_*`; results `loop7.dat`, `loop9.dat`, `step8.dat`, plot `out/step_response.png`.
- **Simulator settings that had to change, and their cost [sim]:** with an S-Varicap in the netlist, ngspice-47 aborts with
  "doAnalyses: out of memory" under `klu` (the CACE templates use `.options klu`), and without klu the op fails (gmin and
  source stepping) and the transient-op fallback lands in the latched state (pad 3.28 V). Valid ops came only with
  `rshunt = 1e10` (10 GΩ from every node to ground), `itl1 = 500`, `gminsteps = 50`, sparse solver, and a `.nodeset` from v0's
  op at the same vd. I applied these to **all** variants including v0. Their effect on v0: PM 72.554° (CACE 72.553°),
  fc 1.3708 MHz (1.3708), T0 78.47 dB (79.05: the 10 GΩ shunts on the high-impedance nodes cost 0.6 dB), step 1 ts
  0.3285 / 0.3346 µs (CACE 0.3293 / 0.3355). Every log in the tables below: no `Transient op started`, no
  `Timestep too small`, op via "Source stepping completed", "spice3 gmin stepping completed" or direct convergence (v3).
  Exception: **v4 at 300 pF** — transient op in all three runs, results invalid and not reported.

### 4.2 Loop gain, 1 kΩ ∥ 100 pF (deck 7) [sim]

T0 (dB) / fc (MHz) / **PM (°)** / GM (dB); limits of the yaml (proposals): PM ≥ 60, GM ≥ 15, fc ≥ 1 (`loop_params`).

| variant | pad 0.99 V (vd −1.3) | pad 1.65 V (vd 0) | pad 2.29 V (vd +1.3) | fc max / min |
|---|---|---|---|---|
| v0 present | 81.7 / 1.552 / **78.4** / 22.6 | 78.5 / 1.371 / **72.6** / 23.1 | 90.0 / 1.790 / **75.4** / 16.8 | 1.31 |
| v1 S-Varicap both | 81.0 / 1.502 / **76.6** / 22.5 | 77.5 / 1.343 / **72.7** / 23.1 | 88.2 / 1.734 / **73.7** / 17.7 | 1.29 |
| v2 70 / 30 both | 81.2 / 1.483 / **77.4** / 22.8 | 77.8 / 1.324 / **73.1** / 23.3 | 88.9 / 1.710 / **74.6** / 17.7 | 1.29 |
| v3 CMB turned | 82.0 / 1.599 / **78.2** / 22.2 | 78.6 / 1.241 / **74.6** / 23.7 | 90.1 / 1.760 / **75.7** / 17.0 | 1.42 |
| v4 CMB S-Varicap pair | 81.1 / 1.260 / **79.6** / 24.7 | 78.0 / 1.344 / **72.8** / 23.2 | 89.9 / 2.023 / **71.3** / 16.1 | 1.61 |

### 4.3 Loop gain at the CACE worst case, unloaded ∥ 300 pF (deck 9) [sim]

| variant | pad 0.99 V | pad 1.65 V | pad 2.29 V |
|---|---|---|---|
| v0 present | 103.1 / 1.312 / **43.7** / 20.3 | 104.1 / 1.392 / **42.2** / 19.3 | 104.6 / 1.467 / **39.7** / 17.5 |
| v1 S-Varicap both | 102.7 / 1.295 / **43.3** / 19.7 | 103.7 / 1.369 / **42.4** / 19.3 | 104.3 / 1.446 / **39.3** / 17.2 |
| v3 CMB turned | 103.4 / 1.351 / **42.1** / 19.9 | 103.4 / 1.302 / **46.0** / 20.2 | 104.6 / 1.449 / **40.4** / 17.6 |
| v4 CMB S-Varicap pair | no valid op (see 4.1) | | |

### 4.4 Step response, 1 kΩ ∥ 100 pF (deck 8) [sim]

Slew rate rise / fall (V/µs), overshoot (%), settling to 1 % rise / fall (µs). (CACE prints SR in V/s under a "V/us" label.)

| variant | step 1: pad 1.40 ↔ 1.90 V | step 2: pad 2.05 ↔ 2.29 V |
|---|---|---|
| v0 present | 2.44 / 2.46, 0.00 %, 0.329 / 0.335 | 1.37 / 1.28, 0.00 %, 0.316 / 0.329 |
| v1 S-Varicap both | 2.36 / 2.36, 0.00 %, 0.340 / 0.345 | 1.36 / 1.25, 0.00 %, 0.304 / 0.327 |
| v2 70 / 30 both | 2.30 / 2.31, 0.00 %, 0.352 / 0.357 | 1.32 / 1.22, 0.00 %, 0.319 / 0.342 |
| v3 CMB turned | 2.12 / 2.12, 0.00 %, 0.388 / 0.380 | 1.31 / 1.22, 0.00 %, 0.327 / 0.352 |
| v4 CMB S-Varicap pair | 2.42 / 2.31, 0.01 %, 0.312 / 0.376 | 1.70 / 1.55, 0.03 %, 0.241 / 0.247 |

### 4.5 Reading

- **The depletion of the present caps costs no phase margin** over the linear swing: at 100 pF the present PM is lowest at
  mid-rail (72.6°) and *higher* at both ends (78.4° / 75.4°), where one of the two caps is at 41 % of its plateau. Every
  variant stays within 71–80°; no overshoot in any step. The loop's phase margin is set elsewhere (the output stage's gm
  and the load pole), not by the C(V) of CMA / CMB [sim; mechanism = est].
- **fc moves with the output stage, not with the caps:** v1 (both caps flat within ±9 %) still has fc 1.34 → 1.73 MHz from
  mid-rail to the top, as v0 (1.37 → 1.79). The present caps' C(V) even partly compensates it: flattening only CMB (v4)
  *widens* the fc spread (1.26 … 2.02 MHz) and lowers GM at the top to 16.1 dB (limit 15) [sim].
- **At 300 pF unloaded, the worst case is at the top of the swing**, not at mid-rail where CACE looks: PM 39.7° at pad 2.29 V
  for the present design, below the yaml's 40° proposal (`loop_load_params`), and the same within ±1° for v1 and v3. This
  is a driver finding, not a capacitor one; no capacitor variant fixes it.
- Turning CMB around (v3) gives the highest mid-rail PM (74.6° / 46.0°) because the same device then sits in inversion with
  26 % more C; its settling is 15 % slower (0.38 µs). At equal C (203 µm² instead of 256 µm²) it would land between v0 and
  v3 [est].

## Recommendation

**CMA: keep the hv PMOS as it is** (gate a; S/D/NW on the pad; 256 µm²). Over the linear swing it is the C(V) that matters
least for PM (§4.5), and in saturation (pad at 3.28 V, loop open) it keeps 95 % of its C through inversion, where an
S-Varicap CMA would keep 36 % (§3.2). Optional: draw it as 8 fingers of 7.96 / 4.02 µm (+1 % C, 64× shorter channel RC; a
guard against the channel-RC roll-off the model does not show, §2.2) if the slot allows.

**CMB: leave it as it is for now** (Christoph, 16:50), with three options for the discussion after task F, ranked:

| option | flatness max / min (linear) | PM 100 pF (pad 0.99 / 1.65 / 2.29) | PM 300 pF | area | gate on pad | well on pad | cost |
|---|---|---|---|---|---|---|---|
| keep (v0) | 2.31 | 78.4 / 72.6 / 75.4 | 43.7 / 42.2 / 39.7 | 326 µm², fits | **yes** | no | thick gate on the pad without secondary stage (CDM) |
| **turn around** (v3), or at equal C 203 µm² | 2.77 (2.62 at equal C) | 78.2 / 74.6 / 75.7 | 42.1 / 46.0 / 40.4 | 326 (258) µm², fits | **no** | yes (2nd) | a second pad-driven n-well with p+ inside (PNP injector): guard rings per §7.2.1, inside the ESD zone next to CMA |
| S-Varicap 80 % ∥ turned 20 % (v4) | **1.04** | 79.6 / 72.8 / 71.3 | not converged | ≈ 400 µm² (33.4 × 12.35), slot needs +3 µm in y | yes (80 %) | yes (20 %, no p+ in it) | the S-Varicap breaks the CACE setup (`klu` → out of memory; needs rshunt / nodeset to converge) — every pad template would need changing; mosvar is a sg13g2 fit; widens fc spread |
| MOM M1–M2, 840 fF | 1.00 | not simulated | — | 1271 µm² M1 + M2 | no | no | no room in the ESD zone; 45 % of the PMOS band; model not validated |

The case **for turning CMB** (gate on b; S/D/NW on the pad): the only option that removes the gate oxide from the pad, it
keeps the simulated PM (≥ 74.6° at 100 pF, ≥ 40.4° at 300 pF), costs no area (or saves 21 % at equal C), and fits the
present slot. **Against:** a second n-well on the pad with p+ diffusion in it (latch-up injector, LU rings, NW.b1 spacing to
CMA's well unless both share one pad well — they are the same net then, which a shared well and one guard ring would
exploit [est]); its C dips to 432 fF at the bottom of the swing (V_GW → −0.06 V, depletion), which the PM table shows to be
harmless; and in a pad-undershoot event the PNP is on the pad either way (CMA already has one). The case **for keeping the
gate on the pad**: no new pad-connected well; against: CDM stress on a 7 nm gate with no series resistor, which IHP's own
pads avoid (`ihp_sg13cmos5l_io_esd_notes.tex` l.51–57, 253–257).

The linear-ish split Christoph asked about exists (v4: S-Varicap ∥ turned S-Varicap, max/min 1.04 at ≈ 400 µm², a third of
a MOM's area), but this loop does not need it: the C variation of the present CMB costs no PM, and the flat CMB alone
increases the fc spread. Worth it only if CMB's C(V) is wanted flat for another reason (distortion at high frequency,
predictability across corners) — not evaluated here.

### Open points

1. **CDM / ESD of CMB's gate on the pad**: no ESD simulation here; decide with task F. *Corrected in stage 5:* the earlier
   estimate here, that IHP's secondary stage (series R) "cannot be inserted without breaking the Miller path", was wrong —
   a 587 Ω or 2 kΩ secondary stage in front of CMB's gate leaves the loop unchanged within 0.5° [sim, stage 5].
2. **Latch-up of pad-driven wells** (CMA now; CMB turned): guard-ring layout per §7.2.1 items 3–5; not checked (latch-up rules
   are off by default, §7.2).
3. **300 pF unloaded at pad 2.29 V: PM 39.7°** (present), below the 40° proposal; CACE only checks vd = 0. A driver issue.
4. **Second stable state** of the loop at the top rail (§3.1); whether the pad recovers when vd returns is unchecked.
5. **Corners / temperature** not run for the variants (tt, 27 °C only; brief limits). The S-Varicap's corner factors exist
   (`cornerMOShv.lib`), the MOM has none.
6. S-Varicap spec unit (§1.1 note a) and the mosvar fit's validity on cmos5l.
7. Channel / well RC of the 32 µm long hv PMOS at the 1–2 MHz crossover: the quasi-static PSP (also rfmode = 1) shows none;
   my estimate puts a corner at 4–5 MHz [est]. A finger split removes the question.
8. Slot height for any S-Varicap variant (+3 µm between DCN and DCP) — layout agent.

## Decks and runs (limit 10)

1 `cv1_hvpmos`, 2 `cv2_moscap_p`, 3 `cv3_moscap_n`, 4 `cv4_svaricap`, 5 `cv5_mom`, 6 `dc6_swing`, 7 `loop7_variants`,
8 `step8_variants`, 9 `loop9_300p` (in `out/decks/`; netlists `dut_pad.spice`, `dut_fixture.spice` from CACE,
`dut_variants.spice` generated). Decks 7–9 run once per variant (and per vd for 7 and 9) through `work/run78.sh`. Not decks
of their own, but listed for completeness: `work/t1…t7.spice`, convergence trials = deck 7 with changed options
(`klu`, gmin, rshunt), and `work/t2.spice`, a one-device op check of the S-Varicap's DC gate current (0 … 7 pA). CACE runs:
the three unchanged template groups of "Preliminaries". Scripts: `work/mkcv.py`, `mkvar.py`, `mkloop.py`, `run78.sh`,
`splits.py`, `cmbcombo.py`, `cmacombo.py`, `gdsfree.py`, `slot.py`, `pcellbox.py`, `plots.py`, `plotstep.py`.

## Short answers (final)

1. **MOS-type gates that do not go into inversion?** Yes: the S-Varicap (thick oxide, n+ poly on n-well; PCell and model in
   cmos5l). But inversion is not the problem: the hv PMOS loses C in *depletion* (−0.6 … +0.75 V, flatband ≈ +1 V), and
   inversion restores it below −0.7 V. The S-Varicap's dip sits ≈ 1 V lower, which suits CMA / CMB's bias (V_GW ≈ 0 … 1.8 V)
   better: ≥ 86 % of its mid-rail C over the linear swing, against 57 % for the hv PMOS. Thin-oxide moscaps are excluded
   (1.65 V oxide, PCells not registered in cmos5l).
2. **Metal capacitors vs the pad buses?** Confirmed: M3 / M4 / TopMetal1 carry the ring, so only M1–M2 MOM (cmomf
   0.68 fF/µm², model not validated on silicon): 1270 µm² per capacitor, 3.9× the present area, and no free M1 / M2 in the ESD
   zone. Not practical.
3. **Split between types so capacitance is left near the rails?** The pad never comes near the rails in linear operation
   (0.94 … 2.31 V), the present caps keep ≥ 41 % there, and the loop does not care: PM 72.6–78.4° (100 pF) for the present
   caps and 71–80° for every split. A linear-ish CMB exists — **S-Varicap 80 % ∥ S-Varicap turned 20 %, max/min 1.04 at
   ≈ 400 µm²** — but it is not needed for stability and costs CACE convergence. **Recommended: CMA as is; CMB as is for now,
   with "turn CMB around" (removes the gate from the pad, PM 74.6° at 100 pF mid-rail, ≥ 40.4° at 300 pF, 326 µm², fits) as
   the first option for the discussion after task F.**

## Stage 5 — series R in front of CMB (IHP's secondary stage), requested 18:20

### 5.1 Setup [sim]

CMB as now (gate side on the pad, S/D/NW on b), CMA unchanged, and between the pad and CMB's gate (new node `kcg`) the
full secondary stage of `sg13cmos5l_SecondaryProtection` (`libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl` l.473–479):
- **v5**: `XKRP6 vout kcg vss rppd w=1u l=2u b=0` (IHP's RR0), `XKDN6 vss kcg dantenna w=0.64u l=3.1u` (kcg → substrate),
  `XKDP6 kcg vddo dpantenna w=0.64u l=4.98u` (kcg → iovdd);
- **v6**: the same with the rppd scaled to 2 kΩ in length, `l=7.435u` (from 587 Ω = 260 Ω/□ × 2 + 67 Ω of heads).
The PDK's `rppd` model was used (not an ideal R); a check in deck 11 (1 V across separate copies, `rcheck` lines in
`out/logs/loop11.dat`) gives **587.0 Ω and 1991.6 Ω**. Diodes from `cornerDIO.lib dio_tt` (`diodes.lib`). All new devices
are named `XK…`, different from every template name by more than case. Decks: **11** `loop11_seriesR.spice` (= deck 7 with
the load as a parameter, run at 1 kΩ ∥ 100 pF and at unloaded ∥ 300 pF as deck 9) and **12** `step12_seriesR.spice`
(= deck 8), run through `work/run78.sh` with the same options and nodesets as v0 in decks 7 / 9. Logs
`out/logs/loop11_seriesR_*` (12) and `step12_seriesR_*` (2): no `Transient op started`, no `Timestep too small`, no
"failed" line; the ops converged directly. v0 values below are from decks 7 / 8 / 9 (identical settings).

### 5.2 Loop gain, 1 kΩ ∥ 100 pF — T0 (dB) / fc (MHz) / **PM (°)** / GM (dB) [sim]

| variant | pad 0.99 V | pad 1.65 V | pad 2.29 V |
|---|---|---|---|
| v0 present | 81.7 / 1.552 / **78.4** / 22.6 | 78.5 / 1.371 / **72.6** / 23.1 | 90.0 / 1.790 / **75.4** / 16.8 |
| v5 587 Ω + diodes | 81.7 / 1.552 / **78.4** / 22.7 | 78.5 / 1.371 / **72.6** / 23.2 | 90.0 / 1.791 / **75.6** / 16.8 |
| v6 2 kΩ + diodes | 81.7 / 1.552 / **78.5** / 23.1 | 78.5 / 1.371 / **72.9** / 23.5 | 90.0 / 1.796 / **76.1** / 16.6 |

### 5.3 Loop gain, unloaded ∥ 300 pF [sim]

| variant | pad 0.99 V | pad 1.65 V | pad 2.29 V |
|---|---|---|---|
| v0 present | 103.1 / 1.312 / **43.7** / 20.3 | 104.1 / 1.392 / **42.2** / 19.3 | 104.6 / 1.467 / **39.7** / 17.5 |
| v5 587 Ω + diodes | 103.1 / 1.312 / **43.7** / 20.3 | 104.1 / 1.392 / **42.3** / 19.4 | 104.6 / 1.468 / **39.8** / 17.6 |
| v6 2 kΩ + diodes | 103.1 / 1.313 / **43.8** / 20.4 | 104.1 / 1.393 / **42.4** / 19.6 | 104.6 / 1.470 / **40.1** / 17.9 |

### 5.4 Step response, 1 kΩ ∥ 100 pF — SR rise / fall (V/µs), overshoot, ts 1 % rise / fall (µs) [sim]

| variant | step 1: pad 1.40 ↔ 1.90 V | step 2: pad 2.05 ↔ 2.29 V |
|---|---|---|
| v0 present | 2.44 / 2.46, 0.00 %, 0.329 / 0.335 | 1.37 / 1.28, 0.00 %, 0.316 / 0.329 |
| v5 587 Ω | 2.44 / 2.45, 0.00 %, 0.330 / 0.336 | 1.36 / 1.27, 0.00 %, 0.318 / 0.332 |
| v6 2 kΩ | 2.43 / 2.43, 0.00 %, 0.335 / 0.339 | 1.34 / 1.26, 0.00 %, 0.323 / 0.338 |

### 5.5 RC time constant over the swing

R × C_CMB, with C_CMB from §3.2 (present hv PMOS at the deck-6 bias) [sim inputs, product est]; the two diodes add
≈ 5 fF at kcg (≈ 2 µm² dantenna + 3.2 µm² dpantenna at 0.8–0.95 fF/µm², spec l.255 / 295) [est], under 1 %.

| pad (V) | 0.90 | 1.00 | 1.65 | 2.30 | 3.28 (saturated) |
|---|---|---|---|---|---|
| C_CMB (fF) | 466 | 487 | 840 | 1098 | 1185 |
| τ at 587 Ω (ns) / pole (MHz) | 0.27 / 580 | 0.29 / 560 | 0.49 / 320 | 0.64 / 250 | 0.70 / 230 |
| τ at 1992 Ω (ns) / pole (MHz) | 0.93 / 170 | 0.97 / 160 | 1.67 / 95 | 2.19 / 73 | 2.36 / 67 |

### 5.6 Reading

- **The secondary stage does not change the loop** [sim]: PM within +0.0 … +0.7° of v0 at every operating point and both
  loads, fc within 0.3 %, GM within ±0.4 dB, step settling +0.3 % (587 Ω) and +2 % (2 kΩ), no overshoot.
- Why [est]: the RC pole of R with CMB lies at ≥ 67 MHz (2 kΩ, worst case) and ≥ 230 MHz (587 Ω), 40–300× above the
  1.2–1.8 MHz crossover; and a resistor in series with a Miller capacitor is the classic nulling resistor, which moves the
  feed-forward zero — hence the slight PM *increase*, not a decrease. A value up to several kΩ would still keep the pole
  well above fc; ≈ 20 kΩ would bring it to ≈ 7 MHz at the top of the swing [est].
- DC: no current flows into CMB's gate, so kcg follows the pad and both diodes stay reverse-biased over 0 … 3.3 V (the pad
  in saturation reaches 3.28–3.30 V, the dpantenna then sits at ≈ 0 V) [est from the op].
- **Consequence for the CMB discussion:** keeping CMB's gate on the pad *with* IHP's secondary stage in front of it costs
  nothing in loop terms and ≈ 6 µm² of devices plus a 1 × 2 µm (or 1 × 7.4 µm) rppd. Whether that makes the gate CDM-safe is
  an ESD question (task F), not answered here. Next to "turn CMB around" (§Recommendation) this is now a second way to get the
  gate oxide off the bare pad, without a second pad-connected n-well.

## Stage 6 — symmetry and pole–zero map over the swing (requested 18:25)

Christoph: "the small signal poles and zeros depend on output voltage, and the consequences may get overlooked by just
standard AC analysis at output voltage = output reference voltage."

### 6.1 Setup [sim]

- Variants (CMA / CMB orientation as now; `dut_variants.spice`): **v0** present; **v5 / v6** CMB-only secondary stage (stage 5,
  587 Ω / 1992 Ω rppd + dantenna + dpantenna at CMB's gate); **v7 / v8 symmetric**: v5 / v6 plus the same rppd between the
  pad and CMA's S/D/well (node `kca`, `XKRA8` / `XKRA9`), no diodes at CMA; **v7d** = v7 plus a dummy dantenna + dpantenna
  at `kca` (`XKEN10`, `XKEP10`).
- **Deck 13** `loop13_sweep.spice` (= deck 11 without the R check, plus `wrdata` of T(f)): the one pad sweep, vd = −1.4,
  −1.05, −0.7, −0.35, 0, 0.35, 0.7, 1.05, 1.3 V → pad 0.937 … 2.292 V (9 points), at 1 kΩ ∥ 100 pF and at unloaded ∥ 300 pF;
  6 variants × 9 × 2 = 108 runs (`work/run13.sh`), v0 first at each point, its op seeding the others' `.nodeset`.
  Logs `out/logs/loop13_sweep_*` (108): no `Transient op started`, no `Timestep too small`; v0's op via "Source stepping
  completed" (after "spice3 gmin stepping failed"), the others converged directly from the nodeset. Results
  `out/logs/loop13.dat`, T(f) in `work/T13/`.
- **Poles / zeros: fitted, not `.pz`.** A trial of ngspice's `pz` on this circuit (deck 13 at vd = 0, v0, 2.6 min) returned
  60 identical garbage roots (−7.6e-7 ± j1e8 rad/s): it does not converge here. The poles and zeros are therefore fitted
  from the loop-gain response T(jω), 1 Hz … 300 MHz, by vector fitting (Gustavsen & Semlyen, real formulation, relative
  weighting; `work/vfit.py`), order 6 (order 5–10 where 6 gave roots that do not classify), pole–zero doublets above 10 kHz
  within 5 % removed, roots below 1 Hz dropped (outside the band). Fit error 0.001–0.06 dB / 0.01–0.3° at 103 of 108
  points; one point needed order 8 (0.001 dB) and 5 points order 5, fitting to 0.11–1.7 dB / 0.8–5.5° (v0 300 pF mid-rail, v5
  100 pF mid-rail, v6 300 pF pad 1.48 V, v8 both loads at pad 0.94 V; low confidence, marked in `out/logs/stage6_table.txt`,
  columns "fit_err" and "order"). PM / fc / GM come from the AC data directly, not from the fit. The full
  table (T0, fc, PM, GM, p1, |p2| and its damping, |p3|, lowest LHP and RHP zero per point) is `out/logs/stage6_table.txt`;
  the summary `stage6_summary.txt`; plots `out/pm_fc_gm_vs_pad.png`, `out/pz_vs_pad.png`.

### 6.2 PM, fc, GM over the swing — v0 present [sim]

| pad (V) | 0.94 | 1.12 | 1.30 | 1.48 | 1.65 | 1.83 | 2.00 | 2.17 | 2.29 |
|---|---|---|---|---|---|---|---|---|---|
| 100 pF: PM (°) | 79.0 | 76.8 | 74.9 | 73.2 | **72.6** | 72.7 | 73.9 | 75.1 | 75.4 |
| 100 pF: fc (MHz) | 1.52 | 1.57 | 1.52 | 1.43 | 1.37 | 1.42 | 1.51 | 1.64 | 1.79 |
| 100 pF: GM (dB) | 22.5 | 22.8 | 23.3 | 23.7 | 23.1 | 21.4 | 19.7 | 18.1 | **16.8** |
| 300 pF: PM (°) | 44.2 | 43.0 | 42.4 | 42.1 | 42.2 | 42.1 | 42.2 | 41.6 | **39.7** |
| 300 pF: fc (MHz) | 1.29 | 1.35 | 1.38 | 1.39 | 1.39 | 1.40 | 1.39 | 1.42 | 1.47 |
| 300 pF: GM (dB) | 20.5 | 19.9 | 19.6 | 19.4 | 19.3 | 19.1 | 19.1 | 18.6 | **17.5** |

### 6.3 Poles and zeros over the swing — v0, 1 kΩ ∥ 100 pF [sim, fitted]

| pad (V) | 0.94 | 1.12 | 1.30 | 1.48 | 1.65 | 1.83 | 2.00 | 2.17 | 2.29 |
|---|---|---|---|---|---|---|---|---|---|
| p1 (Hz) | 124 | 137 | 152 | 166 | 168 | 145 | 105 | 70 | 56 |
| \|p2\| (MHz), damping | 10.4, 0.73 | 10.3, 0.80 | 10.2, 0.91 | 8.0, 0.98 | 6.0, real | 6.9, real | 9.3, real | 9.4, 0.95 | 11.0, 0.88 |
| lowest LHP zero (MHz) | 26 | 24 | 26 | 11 | 39 | 47 | 52 | **7.1** | **8.5** |
| lowest RHP zero (MHz) | 247 | 249 | 258 | 258 | 261 | 259 | 157 | **56** | **58** |

At unloaded ∥ 300 pF: p1 6.3–7.5 Hz (T0 103–105 dB), p2 = the output pole 1.45–1.51 MHz (real, nearly constant), LHP
zero 38–44 MHz, dropping to 22 MHz at pad 2.29 V; RHP zero 190–330 MHz.

### 6.4 Variants: worst-case PM and symmetry [sim]

Symmetry = |PM(+x) − PM(−x)| for mirrored vd (x = 0.35 / 0.7 / 1.05 V, and the ends vd = −1.4 / +1.3 V).

| variant | worst PM 100 pF (at pad) | worst PM 300 pF (at pad) | min GM 100 / 300 pF | \|ΔPM\| mirrored, 100 pF | \|ΔPM\| mirrored, 300 pF | fc max / min 100 / 300 pF |
|---|---|---|---|---|---|---|
| v0 present | 72.6 (1.65) | 39.7 (2.29) | 16.8 / 17.5 | 0.5 / 0.9 / 1.8 / 3.6 | 0.1 / 0.2 / 1.3 / 4.6 | 1.31 / 1.14 |
| v5 CMB 587 Ω | 72.6 (1.65) | 39.8 (2.29) | 16.8 / 17.6 | 0.5 / 0.9 / 1.6 / 3.5 | 0.0 / 0.1 / 1.3 / 4.5 | 1.31 / 1.14 |
| v6 CMB 2 kΩ | 72.9 (1.65) | 40.1 (2.29) | 16.6 / 17.9 | 0.4 / 0.7 / 1.4 / 3.1 | 0.0 / 0.0 / 1.1 / 4.2 | 1.31 / 1.14 |
| v7 sym 587 Ω | 72.7 (1.65) | 39.8 (2.29) | 16.8 / 17.7 | 0.5 / 0.9 / 1.8 / 3.6 | 0.1 / 0.2 / 1.3 / 4.6 | 1.31 / 1.14 |
| **v8 sym 2 kΩ** | **73.2** (1.65) | **40.2** (2.29) | 16.8 / **18.1** | 0.5 / 1.0 / 1.7 / 3.6 | 0.1 / 0.2 / 1.3 / 4.5 | 1.31 / 1.14 |
| v7d sym 587 Ω + dummy diodes | 72.7 (1.65) | 39.8 (2.29) | 16.8 / 17.7 | identical to v7 | identical to v7 | 1.31 / 1.14 |

### 6.5 Reading

- **What moves with the pad voltage** [sim, fitted]: the dominant pole p1 (×3 at 100 pF: 168 Hz at mid-rail, 56 Hz at the
  top, together with T0 rising from 78.5 to 90 dB — the gain-bandwidth stays near 1.4–1.8 MHz); the non-dominant pole
  (6 MHz real at mid-rail, 10–11 MHz and complex with damping 0.73–0.88 at both ends); and, **only on the sourcing half
  (pad ≥ 2.17 V)**, a zero pair: an LHP zero comes down to 7–9 MHz and the RHP zero from ≈ 250 MHz to 55–58 MHz. On the
  sinking half (pad ≤ 1.30 V) the zeros stay where they are at mid-rail (LHP 24–26 MHz, RHP ≈ 250 MHz). The output pole at
  300 pF (≈ 1.5 MHz) does not move.
- **The two halves are not symmetric**, and the asymmetry is the driver's, not the capacitors': at 100 pF PM rises toward
  both ends but more on the sinking side (79.0° at 0.94 V against 75.4° at 2.29 V), GM falls only on the sourcing side
  (23.7 → 16.8 dB, 1.8 dB above the 15 dB proposal); at 300 pF PM is flat at 42–44° on the sinking side and drops to 39.7°
  at 2.29 V. In the sourcing half the class-AB control pushes b (ON's gate) to 0.62–0.65 V, close to ON's threshold, so the
  b-side path (ON, CMB) loses gm; that is where the extra zero pair appears [mechanism est; numbers sim].
- **Christoph's point holds**: the mid-rail AC analysis that CACE runs shows the *lowest* PM at 100 pF (72.6°), but hides
  the worst GM (16.8 dB) and, at 300 pF, the worst PM (39.7°, below the 40° proposal), both at the top of the swing.
- **The series R, one-sided or symmetric, changes almost nothing** [sim]: PM within +0.6°, GM within +0.6 dB, fc within
  0.3 %, the same pole-zero pattern and the same asymmetry (|ΔPM| at the ends 3.1–3.6° at 100 pF, 4.2–4.6° at 300 pF for
  every variant). Making CMA's network a mirror of CMB's (v7 / v8) does not make the loop symmetric, because the loop's
  asymmetry does not come from the capacitor networks.
- **Best variant:** v8 (2 kΩ in front of both caps) has the highest worst-case PM over the whole swing (73.2° at 100 pF,
  40.2° at 300 pF) and the highest worst-case GM at 300 pF (18.1 dB); v6 (2 kΩ at CMB only) is the most symmetric by a
  small margin (end asymmetry 3.1° / 4.2°). The differences to v0 are 0.5° — within what a corner or layout parasitic
  would move. Neither is a reason to choose a variant; the choice of CMB's protection can be made on ESD grounds alone.
- **Dummy junction capacitance at CMA** (v7d against v7): identical to 0.1° and 0.1 dB everywhere [sim]; the ≈ 5 fF of the
  diodes [est] is nothing next to ≈ 0.5–1.2 pF of CMA. Matching it is not needed.
- Deck budget: deck 13 only (decks 14–15 unused); the `.pz` trial was deck 13 with an added `pz` line.
