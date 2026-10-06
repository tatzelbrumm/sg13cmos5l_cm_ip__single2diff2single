Task: port the real bias variants and their test/verification suite from IHP sg13cmos5l to
GF180MCU (gf180mcuD, as installed in IIC-OSIC-TOOLS). This is a side quest: the IHP design stays the
reference and is not changed.

Where things are:
- Source design: ~/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/
  design_considerations/class_ab_pad_driver/improvements/
  Read first: log.md (newest at the end), bias.md, xschem/README.md.
- Netlists (source of truth):
  - sim/d2s_bias_ref.spice: the diodes and the four variants.
  - sim/d2s_bias_lp.spice: the ideal fixture.
  - sim/d2s_mpdda.spice with units.spice and ccomp.spice: the driver the bias is sized for.
  - Ports are `vdd vss vddo vsso ...`. Keep the rail partition of bias.md.
- Suite as of today:
  - sim/run_bias.py produces every number in bias.md and sim/results_bias.txt.
  - Also sim/run_improvements.py and the decks sim/tb/*.spice.
  - xschem/check_xschem.py (round trip) and the sheets xschem/tb_*.sch.
  - The IHP numbers are in results_bias.txt and results_improvements.txt. Don't rerun IHP.
- Another chat is building testbenches and CACE skeletons for the bias blocks
  (../build_verification_suite/kickoff_build_verification_suite.md). Nothing of it is on disk yet.
  Port it once it is. Until then, port run_bias.py and the decks it needs.
- The existing CACE setup of the original driver is in ../verification/cace.
- Write everything into port_gf180/ (this folder): sim/, xschem/, figures/ and a log.md of its own.
  Read the IHP files; don't edit them.

Scope. These are defaults; confirm them with Christoph at the start:
- In: d2s_bias_diodes, the variants _in _out _oa _bg, d2s_bias_lp, and d2s_mpdda with its units and
  Miller capacitors. The vabp/vabn replicas are sized against OP/ABP/ON/ABN, and run_bias.py's
  driver sections need the driver.
- Out: d2s_lc2/_nc, the unit alternatives, gen_cells.py and gen_testbenches.py.
- Devices: nfet_03v3/pfet_03v3 at 3.3 V, the counterpart of sg13_hv. Use the 6 V devices only if
  Christoph says the target runs at 5 V.

Re-derive the sizes; don't transliterate them. The targets stay the same, the sizes are new:
- bias currents 5 / 5 / 2 / 2 / 5 / 5 µA;
- I_Q ≈ 212 µA;
- the loop and PSRR numbers in bias.md.

Cautionary example: macros/OgueyAebischerBias in the main repo is a 1:1 sky130 port that was
never re-sized. It gives 47 nA instead of 200 nA (bias.md, variant 3).

What does not carry over:
- bg: the bandgap relies on rhigh's TC (−0.22 %/K) nearly cancelling V_BE's.
  - gf180's high-R polys (ppolyf_u_1k/_2k/_3k) have their own TC.
  - Redo the PTAT/CTAT balance.
  - Redo the R1A/R1B asymmetry against the false operating point.
- pnpMPA becomes gf180's vertical PNPs (pnp_05p00x05p00, pnp_10p00x10p00, the 0p42 strips). Their
  geometry is fixed, so ratios come from m only.
- oa: the weak-inversion sizing follows from gf180's n, μ and V_T, so recompute it:
  - U_T ln 16 at M10's source;
  - the composite pair;
  - the MC10 cascode;
  - start-up MS1–MS3.
- Miller capacitors (hv PMOS in accumulation) become cap_pmos_03v3 / cap_nmos_03v3 (moscap
  models), or MIM. The image's gf180mcuD has the 2 fF/µm² MIM option (nodeinfo.json: MIM_2P0).
- The DDA degeneration resistor (rhigh) becomes a gf180 high-R poly.

PDK facts were checked on 2026-10-06 against fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_pr
(HEAD e11a8c9, 2026-09-04), which open_pdks copies into libs.tech/xschem and libs.tech/ngspice.
The image's build (open_pdks 1689ac3, see cloud_environment.md) is the reference, so re-check them
there.
- MOS symbols nfet_03v3 and pfet_03v3 (also _05v0 and _06v0):
  - format `@name @pinlist @model L=@L W=@W nf=@nf m=@m`;
  - no spiceprefix, so they are plain M devices (BSIM4);
  - pin order D G S B for both; the pfet has S on top.
- ppolyf_u_1k/_2k/_3k: format `@spiceprefix@name @pinlist @model r_width=@W r_length=@L m=@m`, pins
  M P B (the bulk is a pin).
- pnp_*: pins C B E, `m` only.
- Models:
  - `.include design.ngspice` sets sw_stat_global and sw_stat_mismatch.
  - `.lib sm141064.ngspice` sections:
    - MOS: typical, ff, ss, fs, sf;
    - resistors: res_typical, res_ss, res_ff;
    - BJTs: bjt_typical, bjt_ss, bjt_ff;
    - capacitors: moscap_*, mimcap_*;
    - mismatch: statistical.
  - The PDK's test sheets write `.lib $::180MCU_MODELS/sm141064.ngspice typical`.
- Read L_min and the bin limits from the model files; don't assume them.

Deliverables, in this order, each with a log.md entry:
1. sim/:
   - the gf180 netlists;
   - adapted copies of run_bias.py and the decks, kept diff-able against the IHP originals;
   - a results table in the layout of bias.md, with IHP and gf180 side by side.
2. xschem/:
   - the bias sheets, drawn from the gf180 netlists in the layout of the IHP sheets
     ([R] | vabp BPC BP | vabn BNC BN, iref from the left at mid-height; see xschem/README.md);
   - an adapted check_xschem.py at MISMATCHES: 0.
   Use the xschem-analog-schematic skill.
3. CACE, once the other chat's suite exists: proof-of-concept subsets only, no exhaustive runs.

Rules:
- Don't write anything into DoNotLitter. No git commands without asking.
  Don't create or append chatlog/*.md.
- No new scripts unless asked. Adapted copies of existing ones are the job; keep them minimal.
  Cloud-only helpers are not shipped.
- Write to my computer only via device_commit_files from a new staged dir under
  /mnt/user-data/outputs/, with expectedMtimeMs guards on existing files.
  - Verify checksums afterwards. PNG/SVG get a provenance stamp in transit, so verify those by pixel
    compare.
  - Never overwrite my hand edits.
- Index external sources; don't copy them. ODF/LibreOffice only, no Microsoft formats.
- Memory: never add inferences about my habits or views without asking first.

Cloud setup: follow sudelbuecher/cloud_environment.md. It pins the versions of my IIC-OSIC-TOOLS
image and builds them from GitHub: xschem 3.4.8RC, ngspice-47 and OpenVAF. It installs gf180mcuD
from the image's open_pdks build (ciel release asset), laid out as $PDK_ROOT/gf180mcuD like in the
image, so the sheets run unchanged there (`sak-pdk gf180mcuD`). The IHP PDK is needed only to
re-run IHP references; the IHP numbers are in the results files.
