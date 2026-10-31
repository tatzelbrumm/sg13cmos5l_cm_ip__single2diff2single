# Brief: capacitor types for the Miller capacitors CMA / CMB of the IOPadDiff2Single pad, 2026-10-31

Workspace (yours, nothing else): `/mnt/user-data/outputs/capagent/` with `work/` (scratch, scripts) and `out/`
(deliverables). Called `$A` below. Your report is `$A/out/report.md`.

## The question (Christoph, 04:06, verbatim)

"maybe spawn off an investigative agent whether CMA and CMB can be replaced by different capacitor types ... do
structures with mosfet-type gates exist, but that don't go into inversion? then there are also metal capacitors, but
they are probably incompatible with the power buses in the IHP pads. Then, there's the question whether CMA and CMB
should be split between different capacitor types, so that some capacitance is left even if the output is close to
the rails."

## Context

`sg13cmos5l_IOPadDiff2Single` is an analog output pad. A differential-to-single-ended amplifier (`d2s_mpdda_pd`)
drives a class-AB output stage:
- OP, a thick-oxide PMOS from iovdd (3.3 V) to the pad, gate on node `a`;
- ON, a thick-oxide NMOS from the pad to iovss, gate on node `b`.

OP and ON are the ESD clamp arrays of the pad cell. Two Miller capacitors compensate the loop:
- `XCMA pad a pad pad sg13_hv_pmos w=7.96u l=32.16u ng=1`: an hv PMOS with gate on `a`, and drain, source and
  NWell on the pad;
- `XCMB b pad b b sg13_hv_pmos w=7.96u l=32.16u ng=1`: gate on the pad, and drain, source and NWell on `b`.

Each has 256 µm² of gate area. A MOS capacitor like these loses capacitance in depletion, between accumulation and
inversion. Christoph wants to know whether other capacitor types, or a split between types, keep enough capacitance
over the whole output swing, including near the rails.

The pad cell is 80 × 180 µm:
- y 0–84: output devices, diodes and clamp frames. Some space may be left there.
- y 84–178: planned for the amplifier, which fills it almost completely.
- The IO ring's power buses run across the whole cell on Metal3 / Metal4 (y 0–178), and on TopMetal1 up to y 134.
  Metal3 is free only at y 119–126 and 134–140, so the circuitry routes on Metal1 / Metal2.

The details are in `layout_primitives.md` §4. A layout task for the pad cell is being prepared; your report feeds it.

## Inputs (read-only; use these paths, which are copies of Christoph's PDK checkout of 2026-10-26)

`/mnt/user-data/uploads/IHP-Open-PDK/` also holds older files from another copy. Read only the paths listed here.

| path under `/mnt/user-data/uploads/` | what |
|---|---|
| `IHP-Open-PDK/ihp-sg13cmos5l/libs.doc/doc/SG13CMOS5L_os_process_spec.pdf` | device data: §2.2.4 S-Varicap, §3.5 current densities, §3.7 parasitic capacitances, hv MOS gate data (`pdftotext -layout`) |
| `IHP-Open-PDK/ihp-sg13cmos5l/libs.doc/doc/SG13CMOS5L_os_layout_rules.pdf` | layout rules: MIM / MOM / varicap / moscap rules if any, §6.4 pads, §7.1 antenna, §7.2 latch-up |
| `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/ngspice/models/cap_cmomf.lib`, `cap_cmomi.lib`, `cornerCAP.lib` | MOM capacitors (fringe, interdigitated) on Metal1–Metal4: model wrappers, provenance notes |
| `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/verilog-a/cap_cmomf/cap_cmomf.va`, `cap_cmomi/cap_cmomi.va` | their compact models (coefficients) |
| `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSCAP.lib`, `sg13g2_moscap_mod.lib`, `sg13g2_moscap_parm.lib` | `sg13_moscap_n` (G SUB), `sg13_moscap_p` (G NW) |
| `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_svaricaphv_mod.lib` | `sg13_hv_svaricap` (G1 W G2 bn), mosvar model |
| `IHP-Open-PDK/ihp-sg13g2/libs.tech/verilog-a/mosvar/mosvar.va`, `mosvarpspMacros.va` | the varicap compact model |
| `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerMOShv.lib`, `sg13g2_moshv_mod.lib`, `sg13g2_moshv_parm.lib` | hv MOS (for the present CMA / CMB) |
| `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/cap_cmomf_code.py`, `cap_cmomi_code.py`, `SVaricap_code.py` | PCells (parameters, layers) |
| `IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python/sg13g2_pycell_lib/ihp/moscap_n_code.py`, `moscap_p_code.py` | PCells of the MOS capacitors (the cmos5l files are links to these) |
| `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/xschem/sg13cmos5l_pr/cap_cmomf.sym`, `cap_cmomi.sym`, `cap_cmomi.tcl`; `IHP-Open-PDK/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/moscap_n.sym`, `moscap_p.sym`, `sg13_svaricap.sym` | symbols (terminals, default parameters) |
| `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_maximal.drc`; `IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/layers_def.drc` | DRC rules that concern these devices |
| `sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/netlist/source/sg13cmos5l_IOPadDiff2Single.spice`, `d2s_out.spice`, `d2s_mpdda_pd.spice`, `README.md` | the circuit |
| `sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` | the pad cell as drawn so far (klayout.db is installed; `import klayout.db`) |
| `sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/pad_buffer_layout/layout_primitives.md` | floorplan, metal usage |
| `sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/esd_protection/ihp_sg13cmos5l_io_esd_notes.tex` | what IHP publishes about ESD |

## What to find out

1. **Capacitor types in this PDK** that could take CMA's or CMB's place. Candidates: the hv PMOS as now; `moscap_p`,
   `moscap_n`; the S-Varicap; `cap_cmomf`, `cap_cmomi`; anything else you find (junction capacitance, etc.). For each:
   - structure, and whether it can invert;
   - terminals, and which terminal is a well or the substrate;
   - oxide (lv or hv) and the voltage it may see;
   - capacitance per µm² and how it varies with voltage over −3.3 … +3.3 V;
   - series resistance;
   - layers, and which metals it occupies;
   - PCell parameters;
   - DRC rules;
   - how far the model is validated (the MOM wrappers say "approximate, not yet validated on ihp-sg13cmos5l silicon").
2. **Voltage across CMA and CMB** with the pad near iovss, mid-rail and near iovdd. Node `a` (OP's gate) and node
   `b` (ON's gate) follow from the circuit: estimate them from device thresholds and the class-AB biasing in the
   netlists, and mark them as estimates. Then say where the present hv PMOS capacitors are in depletion.
3. **Room for metal capacitors:** with the buses on Metal3 / Metal4 / TopMetal1, which MOM layer ranges are possible
   where in the cell? Measure free areas per metal from the GDS, and say what density you get.
4. **Splits:** combinations that keep a stated fraction of the capacitance over the whole swing. Examples:
   - MOS plus MOM;
   - two MOS capacitors in opposite orientations in parallel;
   - MOS plus S-Varicap.

   Give the area of each, for the same nominal capacitance as now, and where it would fit.
5. **ESD and latch-up of each option:**
   - gates on the pad (CMB today, and any reversed part);
   - wells on the pad (CMA's NWell is the pad net) and the guard rings that needs (layout rules §7.2.1);
   - antenna rules (§7.1).

   MOM capacitors put no oxide on the pad.

## Rules

- Work only in `$A`. Do not use any `mcp__remote-devices__*` tool, run no git command, do no web searches, and write
  nothing outside `$A`.
- There is no circuit simulator here: don't install one. Use the model equations and parameters and the process
  specification's numbers. Add a short simulation plan for a session that has ngspice and the OSDI models: at most 10
  decks, written out in `$A/out/sim_plan/`, with C(V) per candidate and the loop's phase margin for the two or three
  best splits.
- No sweeps beyond what a C(V) curve needs. Keep scripts few and short.
- Cite every number with file and section, table or line. Mark measured or published facts as facts, and reasoning
  and estimates as such.
- Times: `TZ=Europe/Berlin date`.

## Deliverables in `$A/out/`

- `report.md`: one table per question above, then a recommendation with its open points. Put the short answer to
  Christoph's three questions first.
- any small scripts you used, and `sim_plan/`.
