Task: give the class-AB driver and its bias a digital enable. IHP sg13cmos5l only, for now.
- Disabled:
  - the bias variants and d2s_mpdda draw no supply current beyond leakage;
  - the output devices OP and ON are off, with their gates tied so that they work as ESD clamps.
- Enabled: everything works as it does today.

Where things are:
- Design folder: ~/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/
  design_considerations/class_ab_pad_driver/improvements/
  Read first: log.md (newest at the end), bias.md, xschem/README.md.
- Netlists:
  - sim/d2s_bias_ref.spice: the four bias variants, with start-up in _oa and _bg;
  - sim/d2s_bias_lp.spice;
  - sim/d2s_mpdda.spice with units.spice and ccomp.spice;
  - sim/d2s_lc2.spice;
  - ports `vdd vss vddo vsso ...`.
  run_bias.py and run_improvements.py reproduce results_bias.txt and results_improvements.txt.
- Other chats are working on improvements/ (schematics under review; testbenches and CACE). Don't
  edit it. Work in power_down/ (this folder): sim/, xschem/ and a log.md of its own. Christoph
  decides when to merge back.
- Prior art: main repo ~/mnt/sg13cmos5l_cm_ip__single2diff2single/macros/OgueyAebischerBias.
  - ToBiasStartup has an active-high `disable` that pulls vbr and vbn low.
  - Its CACE docs are in verification/cace/_docs/reference.md.
  - Also read that repo's CLAUDE.md.
- Slot boundary: main repo TOP_LEVEL_MODULE.md, sections 2 and 2.2.
  - `enable`, dig_in and dig_out are on the 1.2 V domain.
  - vdd_3v3 and vdd_1v2 are switched separately (power_3v3_ena, power_1v2_ena).
  - vssio is the ESD ground.
  - Level shifting is an open item there.
- ESD clamp practice: IHP's own IO cells, ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl
  (IHP-Open-PDK dev branch).
  - See how the Clamp_N*/Clamp_P* gates are tied, and how LevelUp and GateDecode work.
  - The project doc claude/sg13cmos5l_pad_cell_internals.md summarizes the library.
  - The output devices double as the pad's clamps in case (a), d2s_mpdda. In case (b), d2s_lc2,
    they sit in the slot (xschem/README.md).

Settle these with Christoph before designing; don't guess:
1. Which signal enables the block: the slot's `enable`, a dig_in bit, or a register? Also its
   polarity, name, and place in the port order (after `vdd vss vddo vsso`?).
2. Level shifting from 1.2 V to 3.3 V: inside the cell, or one shared shifter? Which state is
   required while vdd_1v2 is off and vdd_3v3 is on?
3. Unpowered slot: the clamp gates must still be held. Should the enable and the gate ties cover
   case (a) only, or case (b) too?
4. "Zero power" as a number: the leakage budget at 27 °C and at 125 °C.
5. Variants 1 and 2 take iref from outside. Who switches it off?
6. Wake-up time after enable, and what vout may do during enable and disable transitions.

Then show, with proof-of-concept subsets rather than exhaustive runs:
- supply current when disabled, over corners and temperature;
- start-up after enable over corners and ramps, including _oa and _bg, with no stuck state;
- the gate voltages of OP and ON when disabled and when unpowered;
- vout during enable and disable transitions;
- enabled performance unchanged against results_bias.txt and results_improvements.txt.

Rules:
- Don't write anything into DoNotLitter. No git commands without asking.
  Don't create or append chatlog/*.md.
- No new scripts unless asked; keep them minimal. Cloud-only helpers are not shipped.
- Write to my computer only via device_commit_files from a new staged dir under
  /mnt/user-data/outputs/, with expectedMtimeMs guards on existing files.
  - Verify checksums afterwards. PNG/SVG get a provenance stamp in transit, so verify those by pixel
    compare.
  - Never overwrite my hand edits.
- Schematics: use the xschem-analog-schematic skill. Round-trip check at MISMATCHES: 0.
- Index external sources; don't copy them. ODF/LibreOffice only, no Microsoft formats.
- Memory: never add inferences about my habits or views without asking first.

Cloud setup: follow sudelbuecher/cloud_environment.md. It pins the versions of my IIC-OSIC-TOOLS
image and builds them from GitHub: xschem 3.4.8RC, ngspice-47, OpenVAF, and the iic-jku IHP PDK fork.
No ev7 stand-in and no OSDI patch are needed any more. Add libs.ref/sg13cmos5l_io/cdl to the PDK
sparse checkout for the IO cells.
