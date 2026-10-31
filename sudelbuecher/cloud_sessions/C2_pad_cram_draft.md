<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2 (draft): layout of the `sg13cmos5l_IOPadDiff2Single` pad cell, bottom-up with agents

Claude Code cloud session, environment `sg13cmos5l` with the setup script of
`github.com/tatzelbrumm/claude-cloud-config`, as C1. Same procedure as `oa_core_pd` and `bg_core_pd` on 2026-10-28:
compact primitives from agents, an assembly agent, and the lead session checks every delivery independently.
A capacitor agent K investigates and simulates alternatives for CMA / CMB in parallel from the start. Its results
inform the layout as they arrive; the layout never waits for them.
The result is the drawn pad cell. Its sheets and source netlists are backannotated to the layout, and IHP's DRC and
LVS are run on the drawn layout.

Runs in parallel with C1. It changes none of C1's files (`oa_core_pd`, `bg_core_pd`, `bias_sel_pd`, `bias_gen_pd`)
and none of the shared macros (rule 4 below).

**Models** (Christoph picks the lead's model when he starts the session; the agents' models are set here, and the
lead passes them when it starts each agent):

| role | model, effort | why |
|---|---|---|
| lead (this session) | Opus, high | partition, ESD, independent checks, integration, backannotation |
| agent F: floorplan and assembly | Opus, high | routing and fitting blocks around each other were the hard part of `oa_core_pd` |
| agents P and N: primitives | Sonnet, medium | rule-driven compaction with existing generators and rules; the lead's checks catch errors |
| agent K: capacitors for CMA / CMB, with ngspice | Opus, medium | device physics from the compact models, C(V) and loop simulations; mostly reading and small decks |

If a delivery fails the lead's check twice, the lead starts that role again one tier up: P / N on Opus, F on Fable.
No Haiku, and no effort above high.

## Read first

Read only what a step names, beyond this list:
- `CLAUDE.md`;
- this brief;
- `sudelbuecher/design_considerations/pad_buffer_layout/layout_primitives.md` §1–4, §6;
- `sudelbuecher/design_considerations/pad_buffer_layout/klayout/README.md`;
- `sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents/README.md` (the procedure, the roles, what survives a
  session) and the briefs there (`A2_oa_core_pd_layout/BRIEF*.md`, `A3…/BRIEF*.md`, `A4…/BRIEF*.md`) as templates;
- `scripts/pcells/README.md`;
- `sudelbuecher/esd_protection/ihp_sg13cmos5l_io_esd_notes.tex`, sections Summary and "Implications for resized clamp PCells".

## Rules

1. **Existing code first.**
   - `scripts/pcells` holds Christoph's PyCells in the PDK's own style:
     - `Clamp_N` / `Clamp_P` (identical to IHP's at the reference `ng`);
     - `Clamp_N_M1` / `Clamp_P_M1` (`ng`, `l`, `frame` fit / 80u, `wiring` internal / external);
     - `DCNDiode` / `DCPDiode`;
     - with their tests in `scripts/pcells/test_m1/` and `verify_clamp.py` / `lvs_clamp.py`.

     The pad cell uses them since 2026-10-28.
   - The replica option (RP1 / RN1 in the clamp frames) exists only as
     `sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/replica_prototype/clamp_engine.diff` and the mock-up
     `layout/klayout/replica_mockup/`; it is not in `scripts/pcells` yet.
   - Changes to clamps and diodes are changes to `scripts/pcells`, with its tests run again. No second generator for
     anything these cells cover.
   - The d2s primitives come from `pad_buffer_cells.py` / `.gds`. The compaction code and rules come from
     `agents/A3_oa_nmos_primitives/out*/` and `agents/A4_oa_pmos_primitives/out*/`, including
     `skill/generic/rules.md` and `skill/ihp_sg13cmos5l/rules.md`. The router comes from `generator.py` in
     `pad_buffer_layout/oa_core_pd_v2_2026-10-28/` and `bg_core_pd_2026-10-28/`. The scratch folders
     `agents/*/work*/` are examples; their scripts carry cloud paths of 2026-10-28.
   - Keep code small: no "just in case" options, no script piled on script (Christoph's rule).
2. **Primitives may be adapted.** The layout drives the design. Christoph's rules of 2026-10-28:
   - no substrate taps between rows of arrayed transistors;
   - one NWell per rail, not separate wells;
   - a tap ring is optional and needn't be rectangular;
   - NWell polygonal where the rules allow;
   - narrow dummies.

   Ratios that set the circuit stay as they are unless the report gives the reason: the I_Q ratio OP : RP1 = 82 : 2,
   the mirror ratios, the common-centroid maps of `layout_primitives.md` §5.
3. **Rule values only from the PDK's decks and documents**, each cited with file and rule name:
   - `libs.tech/klayout/tech/drc/rule_decks/*`;
   - `libs.doc/doc/SG13CMOS5L_os_layout_rules.pdf`;
   - `SG13CMOS5L_os_process_spec.pdf` §3.5.
4. **Shared macros stay unchanged**: `bias_tree_pd`, `bias_gen_pd`, `en_ctrl_3v3`, `ls_*`, `hv_logic`, the cores. A
   shared block laid out in the pad cell is drawn to its present sheet. If its layout implies a sheet change, the change
   goes into the report as a proposal, and Christoph applies it after C1.
5. Measured facts are stated as facts; reasoning and guesses are marked as such. Times are given as `TZ=Europe/Berlin date`.

## ESD, as far as IHP has published it

The open PDK states no ESD rating for the I/O library and has no TLP / HBM data. The only kV figures are the
`SG13_dev` ESD PCells (`diodevdd_2kv` …, `nmoscl_2/4`, layer `Recog.esd` 99/30). IHP's I/O cells don't use these and
don't carry `Recog.esd`. What IHP does publish, and what follows for this cell:

- **The scheme of `sg13cmos5l_io`:**
  - primary diodes `DCNDiode` / `DCPDiode` on every signal pad;
  - the drivers themselves as the large thick-oxide arrays on the pad;
  - an RC rail clamp in every supply pad;
  - a secondary stage (series rppd plus diodes) in front of every gate on the pad.

  Keep the finger cell of the output arrays as in IHP's cells: drain 1.18 µm as ballast, source 0.64 µm, end source
  0.47 µm. `scripts/pcells` keeps it. Change only finger counts and arrangement.
- **Gates on the pad.**
  - `XCMB b pad b b` has its gate on the pad: a thick-oxide gate directly on the pad, without the secondary stage
    IHP puts in front of every pad gate.
  - Options:
    - turn CMB around (source / drain / bulk on the pad, gate on `b`);
    - or keep it, and state the voltage the primary diodes leave across the oxide during a strike (the PDK gives no
      oxide breakdown figure).
  - Decide neither; give the case for each in the report. Until Christoph decides, lay CMB out as in the sheet.
  - Check the antenna rules of §7.1 for every gate on the pad net.
- **Latch-up, §7.2.1 / §7.2.2:**
  - a guard ring around every device tied to the pad. This includes CMA, whose NWell is the pad net; its missing ring
    is an open point of A1 on 2026-10-28.
  - double guard rings (NWell isolator and P+ isolator) between the n- and p-channel output devices, and between them
    and the circuitry;
  - LU.a / LU.b 20 µm, LU.c / LU.d 6 µm.

  Run DRC with `$latchUpRules` on: `sg13cmos5l_maximal.drc` implements LU.a, LU.c, LU.c1, LU.d and LU.d1, not LU.b.
- **Pad rules, §6.4:** Pad.jR (no devices under the pad), Pad.d1R (11.2 µm from the pad to Activ), Pad.eR / Pad.fR
  (metal exit at least 7 µm wide and 7 µm long). Check them against where the bond pad sits in IHP's ring convention.
- **Current paths:** process spec §3.5 gives electromigration limits (DC), not ESD limits. Make every path from the
  pad to diodes and clamps, and from them to the rails, at least as wide as in IHP's `IOPadAnalog`; measure those
  widths there.

## Phase 0, lead: tools

`/foss/setup.log` needs `APT_OK`, `PIP_OK`, `TOOLS_OK`, `PDK_OK` and `SETUP_DONE`, and no `KLAYOUT_DEB_FAILED`.
Record the versions as C0 did: klayout, magic, netgen, xschem, and `git -C /foss/pdks/IHP-Open-PDK rev-parse HEAD`.
PDK paths in this brief are relative to `/foss/pdks/ihp-sg13cmos5l/`, and IHP's I/O cells are in
`libs.ref/sg13cmos5l_io/gds/`. The OSDI models aren't needed, because nothing is simulated.

## Phase 1, lead: frame, partition, budget

1. **Abutment with IHP's pads and fillers:**
   - outline and boundary layer (`scripts/check_boundary.py`, prBoundary 189) against `IOPadAnalog`, `IOPadIOVdd`,
     `IOPadIOVss` and the `Filler*`;
   - per layer, the y intervals of the shapes touching each cell edge, as a table of differences;
   - the row `Filler1000 | IOPadAnalog | pad cell | Filler200 | IOPadIOVdd | pad cell | Filler1000`, with IHP's
     `sg13cmos5l_maximal.drc` (latch-up on). Report violations within 5 µm of an abutment line separately;
   - each ring rail and each band is one net through the row (klayout.db `LayoutToNetlist`).

   Expected bands from edge to edge:
   - NWell with n+, iovdd: y 6–61;
   - p+ ring, iovss: 65–84.4;
   - p+ plate with Substrate, iovss: 84.5–140;
   - n+ in NWell, iovdd: 148.35–148.65;
   - p+, vss: 156.85–157.15;
   - n+ in NWell, vdd: 166.85–167.15.

   A filler gets these potentials only by abutment, so every band reaches both edges of the cell and is tied there to
   its rail. The current pad cell is the first test; the final cell is checked the same way in phase 4.
2. **Partition** of the pad sheet `sg13cmos5l_IOPadDiff2Single.sch`:
   - **in the cell:** `Xd` (`d2s_mpdda_pd`); `Xfp` / `Xfn` (output stage in the clamp frames); `XCMA` / `XCMB`; `XDN` / `XDP`;
   - **if they fit:** `Xt` (`bias_tree_pd`), then `Xc` (`en_ctrl_3v3`, only if a layout or primitives of it exist);
   - **out, to the slot:** `Xg` (`bias_gen_pd`, which holds the two cores).

   Moving instances out of the cell changes the hierarchy: the cell gets new ports, for example `iref`. Propose the
   cell's sheet and ports in the report, and use them for LVS. The slot-level sheet is not changed in this task.
3. **Budget:** the compacted size of every block, estimated with rules 2 and 1, against y 84–178.
   - The packing so far, uncompacted: d2s front end 94.2 µm; with CMA / CMB 98.8 µm; free height 94 µm.
   - **CMA / CMB:** at least a part of each sits next to the output devices and clamps, in y 0–84 where the frames
     leave room. This has high priority. Each may be split into units of any shape. The total gate area stays as it is
     (7.96 × 32.16 µm = 256 µm² each). Record the changed series channel resistance (∝ L / W per unit, units in
     parallel) as a circuit effect.
   - **Routing:** M1 / M2 under the ring rails; M3 only at y 119–126 and 134–140; core-side pins on M2 at the top.

   **Stop condition:** if the d2s front end does not fit even compacted, stop after phase 1 and report what has to leave.
4. Write `report.md`, then commit and push.

## Agent K, from the start of phase 1, in parallel: capacitors for CMA / CMB

**The question** (Christoph, 2026-10-31 04:06, verbatim): "maybe spawn off an investigative agent whether CMA and CMB
can be replaced by different capacitor types ... do structures with mosfet-type gates exist, but that don't go into
inversion? then there are also metal capacitors, but they are probably incompatible with the power buses in the IHP
pads. Then, there's the question whether CMA and CMB should be split between different capacitor types, so that some
capacitance is left even if the output is close to the rails."

**Starting point.** A first local run (A5, 2026-10-31 04:10–04:16) was stopped before it reported. Its brief
`sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents/A5_cap_options/BRIEF.md` lists the questions; K takes them over.
That brief's paths and its no-simulator rule are of the earlier workspace and don't apply here. `inputs.md` there gives
the sha256 of the files A5 read, from Christoph's PDK checkout `6ac9bb9d`. Found so far:
- **The PDK's capacitor devices:**
  - PCells `moscap_n` / `moscap_p`, `SVaricap`, `cap_cmomf`, `cap_cmomi`;
  - models `sg13_moscap_n` (G SUB) and `sg13_moscap_p` (G NW);
  - `sg13_hv_svaricap` (G1 W G2 bn, mosvar Verilog-A);
  - `cap_cmomf` / `cap_cmomi` (OSDI, Metal1–Metal4). Their wrappers say "APPROXIMATE MODEL -- NOT YET VALIDATED ON
    ihp-sg13cmos5l SILICON".
  - No MIM device: the layout rules define the MIM layers 36/0 and 129/0, but there is no PCell and no model.
- **S-Varicap** (process spec §2.2.4, thick gate oxide): 23 / 35.3 / 39.5 fF/µm² at −3 / 0 / +3 V. Measured on a
  10 × (3.74 × 0.3) µm² structure at 15.8 GHz; Q 43–62.
- **Metal-to-metal area capacitance** (process spec §3.7): 68 aF/µm² for Metal1–Metal2, Metal2–Metal3 and
  Metal3–Metal4; Metal4–TopMetal1 "tbd". The MOM cells get more from fringe fields, per their models.
- **`Recog.mom` 99/39** marks MOM capacitors.
- **CMA / CMB now:** `XCMA pad a pad pad` and `XCMB b pad b b`, hv PMOS 7.96 × 32.16 µm, 256 µm² of gate each. CMB has
  its gate on the pad (rule ESD).

**Tasks:** A5's questions 1–5, plus simulation:
- C(V) of each candidate over −3.3 … +3.3 V.
- The voltage across CMA and CMB with the pad near iovss, at mid-rail and near iovdd, from a DC sweep of the pad. Use
  the pad's existing testbenches (`macros/sg13cmos5l_IOPadDiff2Single/testbenches/`, the CACE yaml) where they cover it.
- Phase margin and step response of the loop with the present caps and with the two or three best splits, at the
  same nominal capacitance.

At most 10 decks, no sweeps beyond a C(V) curve and the DC swing.

**Simulation setup:**
- PDK `/foss/pdks/ihp-sg13cmos5l` at the environment's `df4c5054`. First compare its capacitor model files with the
  sha256 in A5's `inputs.md` and note any difference.
- ngspice-47 and the prebuilt OSDI models (`OSDI_OK` in `/foss/setup.log`). Compile a missing model with the openvaf of
  claude-cloud-config's tools, and record it.

**Results in stages,** each added to `agents_c2/K/report.md` and announced to the lead:
1. inventory and voltage windows;
2. C(V);
3. splits with area and where they fit;
4. phase margin.

The lead passes each stage on to F.

**How the results are used:**
- F lays out CMA / CMB with K's latest stage when it gets to them.
- Without a result yet, F lays them out as in the sheet, as hv PMOS units, and keeps each capacitor in its own region,
  so that a later change of type stays local.
- The lead adopts a type change only if K's simulations show at least the present phase margin and capacitance over
  the swing, and records it as a decision for Christoph's review. The question of CMB's gate on the pad is part of
  that decision.

## Phase 2, agents P and N (in parallel): compact primitives

- **P (as A4):** the PMOS cells of d2s:
  - input tubs `d2s_inputs` / `tub_p20x1`;
  - tails `d2s_tails`;
  - loads `d2s_loads`;
  - PMOS cascodes `d2s_casc_p`;
  - class-AB P group `d2s_ab_p`;
  - `d2s_pd_p`.
- **N (as A3):**
  - sinks `sinks_6x6` (shared with s2d, so keep a variant for it);
  - NMOS cascodes `d2s_casc_n`;
  - class-AB N group `d2s_ab_n`;
  - `d2s_pd_n`.
- Each gets its own brief in the format of A3 / A4, with:
  - F's pin and aspect requests (relayed by the lead);
  - read-only inputs;
  - its own `work/` and `out/`;
  - no git, no repo writes.

  The deliverables per cell are the GDS, CDL, IHP DRC (latch-up on), LVS against the cell's reference netlist, a
  picture, and the netlist changes the cell implies.
- **The lead checks every delivery** with XOR against the agent's GDS, its own DRC and LVS runs, and a flat extraction
  of every device's W / L / nets. Only then does it pass the cell to F.

## Phase 3, agent F (as A2): floorplan and assembly

- **Also F's own cells:**
  - the `d2s_rhigh` R block (rhigh chains, as `bg_res_c`);
  - CMA / CMB units (MOS capacitors, `d2s_cma` / `d2s_cmb`), with agent K's latest result;
  - the guard rings and band ties of rule ESD / phase 1;
  - `bias_tree_pd` drawn to its present sheet, if the budget lets it in.
- **Assembly:** place P's and N's cells; route in M1 / M2, M3 in the gaps; pins.

  F may change copies of P's and N's cells if that makes the cell more compact (as A2 on 2026-10-28, 03:40). Every
  change is listed.
- **The lead checks the assembled block independently** (flat extraction, DRC, LVS) before integration.

## Phase 4, lead: integration, backannotation, DRC / LVS on the drawn layout

1. **The pad cell:** y 84–178 from F, CMA / CMB units in y 0–84, written into
   `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`. The cell as it was goes to
   `layout/klayout/backups/` first. Keep the boundary and the abutment of phase 1.
2. **Backannotation, as for `bg_core_pd`:** the sheets follow the layout.
   - Sheets: `sg13cmos5l_IOPadDiff2Single.sch` (as partitioned), `d2s_mpdda_pd.sch`, `d2s_out_p.sch` / `d2s_out_n.sch`.
   - Source netlists: `netlist/source/*.spice`.
   - Tools: the sheet edits of `bg_core_pd` (`pad_buffer_layout/bg_core_pd_2026-10-28/macro_install/bg_sheet_ba.py`)
     show the method, but its helper `schedit.py` is not in the repository. Write one small sheet editor of your own.
     Check the edited sheets with `scripts/xschem/sheet_equiv.py` (old root against new root).
   - Content:
     - finger counts and `ng` as drawn;
     - resistor chains as xschem vector instances;
     - every dummy as a device;
     - CMA / CMB as their units.
   - Checks:
     - sheet against source subckt (topology);
     - every sheet that uses these cells, flattened, before against after;
     - renders.
   - The files replaced go to a `macro_before/` folder of the notes.
3. **DRC and LVS on the drawn cell, against the backannotated sheet:**
   - the macro Makefile's `klayout-drc`, `klayout-lvs`, `magic-drc`, `magic-lvs-netlist` and `magic-lvs`, all with
     `SCRIPTS_DIR=../../scripts` (C0's report). These need `TOOLS_OK` in `/foss/setup.log` for `sak-*`.
   - `klayout-drc` runs `sak-drc.sh` at a `DRC_LEVEL` (precheck / macro / regular). Record which deck that level runs
     and whether it runs the latch-up rules. If it doesn't, add one run of `sg13cmos5l_maximal.drc` with
     `$latchUpRules` on.

   After that, phase 1's row checks on the final cell.
4. **The open points of 2026-10-28**, each either closed or still open:
   - the a / b joins above the P frame;
   - `guard` not tied inside the cell;
   - CMA's ring;
   - rules at exactly their limit;
   - the 63/0 GateDecode box.

## Cost rules

- At most four agents at a time (K throughout; P and N in phase 2; F in phase 3). Each brief is self-contained and gives
  the agent only the files it needs. No web searches.
- No sweeps. At most two floorplan variants. Each check runs once, and once more after each fix. A cell that is not
  clean after three rounds is reported and left; the work goes on with the others.
- The lead does not redo an agent's work; it checks it.
- `report.md` is updated after every phase, then committed and pushed.

## Git, for this task only (Christoph's permission)

- Design branch `claude/c2-pad-layout` from `toplevel`, for `macros/sg13cmos5l_IOPadDiff2Single/` and
  `scripts/pcells/` only.
- Notes branch `claude/c2-pad-layout-sudel` from `sudel_buecher`, as a worktree `../sudel`:

  `git fetch origin sudel_buecher && git worktree add -b claude/c2-pad-layout-sudel ../sudel origin/sudel_buecher`
- Commit on these two branches and push them. Never push `main`, `toplevel` or `sudel_buecher`; no tags, no force
  pushes, no merges.
- Notes outputs:
  - report, checks, before-copies: `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/`;
  - agents: `sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/<role>/`, each with brief, messages, report,
    and **its `out/` and `work/` folders**. These are copied before the session ends, because the agents' workspaces
    die with it.
  - command logs as in C0: `sudelbuecher/logs/claude/c2-pad-layout/`.
- No internal agent ids in any file; the agents are called P, N, F.
