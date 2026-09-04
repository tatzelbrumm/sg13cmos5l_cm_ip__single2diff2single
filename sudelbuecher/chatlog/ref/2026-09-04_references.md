# References — 2026-09-04 session

Index only, per the rule in [`README.md`](README.md): no third-party documents
are copied into this repository. Fetch what you need at read time.

## External

| Ref | Source | Used for |
|---|---|---|
| R1 | H. J. Oguey and D. Aebischer, "CMOS current reference without resistance," *IEEE J. Solid-State Circuits*, vol. 32, no. 7, pp. 1132–1135, Jul. 1997 | The topology `OgueyAebischerBias.sch` implements; cited verbatim in the schematic's own title block |
| R2 | <https://www.semanticscholar.org/paper/Ultra-High-Input-Impedance%2C-Low-Noise-Integrated-Chi-Maier/ab83669efb5f29a94e19b8e2c3f4801ab50ba3ea/figure/10> | Cited in `s2d_d2s_pinbuffers.md` alongside the bias-generation note |
| R3 | <https://github.com/MastellaM/sky130_TAC3/pull/3> | Cited alongside R2 in `s2d_d2s_pinbuffers.md` |
| R4 | <https://github.com/RTimothyEdwards/sg13cmos5l_ocd_chipalooza> | `origin` of the connected `sg13cmos5l_ocd_chipalooza` folder; the Chipalooza Analog Harness this design will eventually embed into as a slot |
| R5 | `git@github.com:RTimothyEdwards/sg13cmos5l_ocd_ip__analog_switches`, `.../sg13cmos5l_ocd_ip__biasgen` | Git submodules of `sg13cmos5l_ocd_chipalooza` (`.gitmodules`), not opened this session |

## Local, outside this repository

| Ref | Path | Used for |
|---|---|---|
| L1 | `~/EDA/sg13cmos5l_ocd_chipalooza/README`, `config.txt` | The harness's own build instructions and the `s1`…`s16` slot/pad-type configuration format |
| L2 | `~/EDA/sg13cmos5l_ocd_chipalooza/librelane/housekeeping_top/README` | LibreLane build recipe for the harness's housekeeping/sequencer digital block |
| L3 | `~/EDA/chipalooza2024/sky130_cm_ip__biasgen/README.md` | Filled-in specification table (operating voltage/temp, output current range, power enabled/disabled, output current accuracy, temperature coefficient, PSRR, output noise, start-up time, output impedance, matching between sources) for the same Oguey-Aebischer core in sky130 — target numbers adapted into `reference.yaml` this session |
| L4 | `~/EDA/chipalooza2024/sky130_cm_ip__biasgen/cace/sky130_cm_ip__biasgen.txt`, `.draft` | Prior, incomplete CACE attempt for the same block (`cace_format: 4.0`, gm/Id device-sizing boilerplate only; `.draft` has an unmatched brace) — confirms the README's spec table was never turned into a working CACE deck there |
| L5 | `~/EDA/chipalooza2024/sky130_cm_ip__biasgen/xschem/OgueyAebischerBias.sch` | sky130 sibling of this design's schematic — same nets/instance names, sky130 device symbols instead of `sg13g2_pr`; confirmed orphaned (unused by any other schematic in that repo) same as here |
| L6 | `~/EDA/TinyTapeout/designs/tt10-analog-tatzelreference/xschem/OgueyAebischerBias.sch`, `ToBiasStartup.sch` | The direct origin of this repo's two schematics — identical topology, nets, instance names and paper citation |
| L7 | `~/EDA/TinyTapeout/designs/tt10-analog-tatzelreference/xschem/reference.sch`, `reference.sym` | The missing combined-macro precedent: instantiates `xbias` (OgueyAebischerBias) + `xstart` (ToBiasStartup) as one symbol exposing `vdd`/`vss`/`vbp`/`vbn`/`vbr`/`disable`. Ported into this repo this session as `macros/OgueyAebischerBias/schematic/xschem/reference.{sch,sym}` |
| L8 | `~/EDA/TinyTapeout/designs/tt10-analog-tatzelreference/xschem/test_reference.sch` | Testbench precedent for `reference.sym`: VDD PWL ramp, `disable` source, `.nodeset`-assisted op+tran sanity check. Informed (but was deliberately *not* copied verbatim into) `reference_tb_tran.sch` — see the file's own header comment on why the `.nodeset` shortcut was dropped for the CACE start-up spec |
| L9 | `~/EDA/TinyTapeout/designs/{tt10-analog-bandgap,tt10-analog-tatzeltapeout}` | Sibling TinyTapeout projects in the same connected folder; listed, not opened this session |

## In this repository

| Ref | Path | Used for |
|---|---|---|
| P1 | `sudelbuecher/description/s2d_d2s_pinbuffers.md` | The IP-block proposal this session's `README.md`/`submission.yaml` rewrites are based on |
| P2 | `macros/inverter/verification/cace/inverter.yaml` | CACE format/convention precedent — `pins`/`default_conditions`/`parameters` structure, the `ac_mc_params`/`ac_mm_params` Monte Carlo/mismatch pattern reused for `reference.yaml`'s `mm_params` group |
| P3 | `macros/inverter/verification/cace/templates/inverter_tb_ac.sch` | CACE testbench templating syntax precedent — `CACE\{condition\}` placeholders, `.include CACE\{DUT_path\}`, `.lib cornerMOShv.lib mos_CACE\{corner_mos\}`, the `echo ... > CACE\{simpath\}/...` result-file convention. Directly copied into `reference_tb_dc.sch`/`reference_tb_tran.sch` |
| P4 | `macros/inverter/verification/cace/templates/xschemrc` | Copied near-verbatim to `macros/OgueyAebischerBias/verification/cace/templates/xschemrc` |
| P5 | `macros/OgueyAebischerBias/testbenches/xschem/OgueyAebischerBias_tb.sch` | Pre-existing flat `xbias`+`xstart` testbench; its wiring is what first revealed the two schematics are complementary halves of one macro, not alternatives |
| P6 | `macros/OgueyAebischerBias/verification/cace/OgueyAebischer.yaml` | Pre-existing blank CACE scaffold (all `<placeholder>` tokens), superseded but not deleted by `reference.yaml` this session — flagged to the user as redundant |
| P7 | `CLAUDE.md` §5 | "Mismatch Monte Carlo is vacuous on an extracted netlist... Run mismatch on `-s schematic`" — the reasoning `reference.yaml`'s `mm_params` group description points back to |

## Files written or edited this session

| File | What changed |
|---|---|
| `README.md` | Intro rewritten to describe the actual pin-buffer/g_mC/scan-chain/bias circuit instead of the template; new "Chip Integration" section (comparison table, `sg13cmos5l_ocd_chipalooza` cross-reference); directory-tree and Recursive-Macro-Structure sections updated to flag `inverter`/`counter` as template placeholders and list `OgueyAebischerBias` |
| `submission.yaml` | New cross-reference comment near the top; `long-description` fully rewritten |
| `macros/OgueyAebischerBias/schematic/xschem/reference.sch`, `reference.sym` | New — ported from L7 |
| `macros/OgueyAebischerBias/verification/cace/templates/xschemrc` | New — copied from P4 |
| `macros/OgueyAebischerBias/verification/cace/templates/reference_tb_dc.sch` | New — authored this session, unverified |
| `macros/OgueyAebischerBias/verification/cace/templates/reference_tb_tran.sch` | New — authored this session, unverified |
| `macros/OgueyAebischerBias/verification/cace/reference.yaml` | New — full CACE deck, two groups wired to real templates, four groups spec'd but marked TODO. Later fixed: six SPICE-suffixed spec bounds (`200n`, `1u`, `20u`, `40u`, `10u`, `20n`, ...) converted to plain floats after `cace ... -p dc_params` crashed on `float('200n')` |
| `macros/OgueyAebischerBias/verification/cace/templates/reference_tb_tran.sch` | Fixed after first CACE run: `Vbp_final`/`Vbn_final`/`Vbr_final` were `let X = v(node)` (dumps the whole transient vector), changed to `.meas tran X find v(node) at=CACE\{tstop\}` (one scalar each), matching how `t_startup` was already written |
| `schematic/xschem/xschemrc` (top level) | Added the missing `source .../macros/OgueyAebischerBias/schematic/xschem/xschemrc` line, alongside the existing `inverter`/`counter` lines — this was why `reference.sym` and its siblings weren't resolving in a top-level Xschem session |
| `README.md` (second pass) | Xschem Configuration table (+3 rows) and chain diagram updated to include `OgueyAebischerBias` |
| `HANDOVER.md` (repo root) | New — seed context for a future Opus sizing session: state snapshot, the sizing flag (ported sky130 device sizes, never re-derived), unverified-testbench caveat, precedents, parallel-session coordination notes |

## Verified by actual CACE runs (2026-09-04, after the fixes above)

`dc_params`: 45 corner×vdd×temp points, all converged. `Vbp` 2.26–3.09V, `Vbn` 0.53–0.69V, `Vbr` 0.91–1.09V, core current 27–65nA. Overall **Fail** — `Ibias_val`'s 200nA minimum (borrowed from `sky130_cm_ip__biasgen`'s spec table) isn't met; the design proposal's own ~100nA ballpark is actually closer to what was measured, so the spec bound is the wrong number, not the sizing.

`tran_startup_params`: 15 corner×temp points, overall **Pass**. Start-up time 200–285ns in every corner (the kick circuit escapes the zero-current state reliably). `Vbp_final`/`Vbn_final`/`Vbr_final` cross-check against `dc_params`' steady-state values at matching conditions — they agree closely, which is real evidence the two testbenches and the `.meas` fix are correct, not just "didn't crash."
