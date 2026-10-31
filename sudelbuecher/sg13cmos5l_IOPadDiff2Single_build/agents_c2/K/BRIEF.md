# Brief K: capacitor types for the Miller capacitors CMA / CMB of the IOPadDiff2Single pad, with ngspice (C2, 2026-10-31)

Workspace (yours, nothing else): `/home/user/c2/K/` — `inputs/` read-only, `work/` scratch and scripts, `out/`
deliverables. Called `$K` below. Your report is `$K/out/report.md`.

## The question (Christoph, 2026-10-31 04:06, verbatim)

"maybe spawn off an investigative agent whether CMA and CMB can be replaced by different capacitor types ... do
structures with mosfet-type gates exist, but that don't go into inversion? then there are also metal capacitors, but
they are probably incompatible with the power buses in the IHP pads. Then, there's the question whether CMA and CMB
should be split between different capacitor types, so that some capacitance is left even if the output is close to
the rails."

## Starting point

A first run without a simulator (A5) was stopped before it reported. Its brief is `inputs/notes/A5_BRIEF.md`: read its
"Context" and "What to find out" (questions 1–5). You take those questions over. **Its paths, its workspace and its
no-simulator rule do not apply here.** `inputs/notes/A5_inputs.md` gives the sha256 of the files A5 read, from
Christoph's PDK checkout `6ac9bb9d`. The two PDK PDFs as text are in `inputs/notes/*.txt` (the same PDFs are in the PDK
below).

Found so far (facts, from the A5 preparation):
- PDK capacitor devices: PCells `moscap_n` / `moscap_p`, `SVaricap`, `cap_cmomf`, `cap_cmomi`; models `sg13_moscap_n`
  (G SUB) and `sg13_moscap_p` (G NW); `sg13_hv_svaricap` (G1 W G2 bn, mosvar Verilog-A); `cap_cmomf` / `cap_cmomi`
  (OSDI, Metal1–Metal4), whose wrappers say "APPROXIMATE MODEL -- NOT YET VALIDATED ON ihp-sg13cmos5l SILICON". No MIM
  device: the layout rules define the MIM layers 36/0 and 129/0, but there is no PCell and no model.
- S-Varicap (process spec §2.2.4, thick gate oxide): 23 / 35.3 / 39.5 fF/µm² at −3 / 0 / +3 V, measured on a
  10 × (3.74 × 0.3) µm² structure at 15.8 GHz; Q 43–62.
- Metal-to-metal area capacitance (process spec §3.7): 68 aF/µm² for M1–M2, M2–M3, M3–M4; M4–TopMetal1 "tbd". MOM
  cells get more from fringe fields, per their models. `Recog.mom` 99/39 marks MOM capacitors.
- CMA / CMB now: `XCMA pad a pad pad sg13_hv_pmos w=7.96u l=32.16u ng=1` and `XCMB b pad b b sg13_hv_pmos w=7.96u
  l=32.16u ng=1`, 256 µm² of gate each. CMB has its gate on the pad (an ESD concern: a thick-oxide gate directly on the
  pad without IHP's secondary stage).
- Cell context: 80 × 180 µm. y 0–84: output clamps OP / ON (frames), DCN / DCP diodes; y 84–178: the amplifier
  (nearly full). IO ring buses on Metal3 / Metal4 across the whole cell (y 0–178) and TopMetal1 up to y 134; Metal3 free
  only at y 119–126 and 134–140. Circuitry routes in Metal1 / Metal2 (`inputs/notes/layout_primitives.md` §4).

## Inputs (read-only)

- `inputs/repo/`: a snapshot of the design repository (branch `toplevel`, commit 8a72dd8). The pad macro is
  `inputs/repo/macros/sg13cmos5l_IOPadDiff2Single/`: `netlist/source/*.spice`, `schematic/xschem/*.sch`,
  `verification/cace/sg13cmos5l_IOPadDiff2Single.yaml` and `d2s_mpdda_pd_sel.yaml` (the loop group: phase margin),
  `verification/cace/templates/*.sch`, `verification/cace/results/` (committed results), `README.md`,
  `layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` (the cell as drawn so far; `import klayout.db`).
  The repo's `CLAUDE.md` is context; its traps section applies to CACE.
- The PDK, read-only: `/foss/pdks/ihp-sg13cmos5l/` (environment checkout `df4c5054`; `git -C /foss/pdks/IHP-Open-PDK
  rev-parse HEAD`). Models in `libs.tech/ngspice/models/`, Verilog-A in `libs.tech/verilog-a/`, PCells in
  `libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/`, symbols in `libs.tech/xschem/`, DRC decks in
  `libs.tech/klayout/tech/drc/rule_decks/`, documents in `libs.doc/doc/`. Some cmos5l paths are links into
  `/foss/pdks/IHP-Open-PDK/ihp-sg13g2/` (A5's list shows which).
- `inputs/notes/`: `layout_primitives.md` (floorplan), `ihp_sg13cmos5l_io_esd_notes.tex` (what IHP publishes about
  ESD), `C1_core_pex_bias_verification_report.md` (the checks below come from it).

Tools: ngspice-47, the prebuilt OSDI models (`/foss/tools/osdi/`, and wherever the PDK's `.spiceinit` points), CACE
2.11.0 (`cace --version`), xschem, `klayout.db`. Before any CACE / make run, in the repo copy: `export PDK_ROOT=/foss/pdks;
source .designinit`. If a model's OSDI file is missing, compile it with `/foss/tools/openvaf` and record that.

## Tasks

A5's questions 1–5, plus simulation:
1. **Inventory and voltage windows** (A5 questions 1, 2, 5): per candidate structure, inversion yes / no, terminals and
   which is a well / substrate, oxide and allowed voltage, C per µm², series resistance, layers and metals used, PCell
   parameters, DRC rules, model validation status; ESD / latch-up per option (gates on the pad, wells on the pad and the
   guard rings layout rules §7.2.1 asks for, antenna §7.1).
2. **C(V)** of each candidate over −3.3 … +3.3 V (one small-signal C(V) deck per candidate, normalised to µm²), including
   the present hv PMOS connections of CMA and CMB.
3. **Voltage across CMA and CMB** with the pad near iovss, at mid-rail and near iovdd, from a DC sweep of the pad (one
   sweep). Use the pad's existing testbenches / CACE templates where they cover it. Then say where the present hv PMOS
   capacitors are in depletion. Then **splits** (A5 questions 3, 4): combinations that keep a stated fraction of the
   capacitance over the whole swing (MOS + MOM, two MOS in opposite orientation in parallel, MOS + S-Varicap, …), the
   area of each at the same nominal capacitance, and where it would fit (free area per metal measured from the GDS).
   Each capacitor may be split into units of any shape; total gate area today 256 µm² each.
4. **Phase margin and step response** of the loop with the present caps and with the two or three best splits, at the
   same nominal capacitance.

Limits: at most 10 decks in all; no sweeps beyond a C(V) curve and the one DC swing.

## Simulation rules (from session C1; follow them)

- First compare the capacitor model files of the PDK here with the sha256 in `inputs/notes/A5_inputs.md`, and note any
  difference (file, both hashes).
- Grep every ngspice log for `Transient op started` and `Timestep too small`. A failed op that falls back to a transient
  op gives plausible, wrong numbers (+18 % in C1), and CACE still reports pass. "Dynamic gmin stepping failed" followed
  by a successful true gmin stepping is a valid op.
- SPICE names are case-insensitive: `XRP1` and `XRp1` are the same instance, and ngspice-47 stops ("device already
  exists"). Give every device you add a name that differs from the template's by more than case.
- Run every pad template you use once, unchanged, before trusting or extending it (in C1 two templates had not run since
  an edit). All 17 pad templates default to `sel` = 0 (harness current, cores off).
- CACE: always pass `-s schematic` explicitly. Run CACE in a copy: `cp -a $K/inputs/repo $K/work/repo` (do not write into
  `inputs/`). Background commands die after 2 h; keep each run short. Kill processes by PID, never `pkill -f`.

## Results in stages

Write `$K/out/report.md` in four stages, in this order, each as its own section, and after each stage append one line
to `$K/out/announcements.md`: `<TZ=Europe/Berlin date> stage <n> done: <one-line result>`. The lead reads these while
you work and passes them on to the layout agent.
1. inventory and voltage windows;
2. C(V) (with plots in `out/`);
3. splits with area and where they fit;
4. phase margin and step response.

## Hard rules

- Work only in `$K`. No git commands (not even read-only), no web searches, no writes outside `$K`, do not touch
  `inputs/`. No `mcp__*` tools.
- Cite every number with file and section / table / line. Mark measured or simulated facts as facts, reasoning and
  estimates as such.
- Times: `TZ=Europe/Berlin date`.
- Keep scripts few and short. Decks in `out/decks/`, logs in `out/logs/`, plots in `out/`.

## Deliverables in `$K/out/`

- `report.md`: the short answer to Christoph's three questions first, then the four stages (one table per question),
  then a recommendation with its open points: which type / split for CMA, which for CMB, and the case for and against
  turning CMB around (source / drain / bulk on the pad, gate on `b`) versus keeping its gate on the pad.
- `announcements.md`, `decks/`, `logs/`, plots, small scripts.

When done, reply with a summary of no more than 15 lines: the short answers, the recommended option with its area and
phase margin, and the open points.
