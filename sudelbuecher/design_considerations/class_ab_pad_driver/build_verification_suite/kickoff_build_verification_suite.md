Task: testbenches and CACE skeletons to characterize (1) each real bias block alone
(d2s_bias_in, _out, _oa, _bg) and (2) bias + d2s_mpdda (the class-AB driver,
Miller compensated).

Where things are:
- Design folder: ~/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/
  design_considerations/class_ab_pad_driver/improvements/
  Read first: log.md (newest at the end), bias.md, xschem/README.md.
- Netlists: sim/d2s_mpdda.spice, sim/units.spice, sim/d2s_bias_ref.spice;
  decks sim/tb/*.spice; sim/run_bias.py (+ ../../run_d2s.py) reproduce every number in bias.md.
- Schematics: xschem/d2s_bias_*.sch are hand-edited and under review in another chat:
  read them, don't edit them. xschem/d2s_mpdda_biased.sch is the CACE fixture.
  check_xschem.py must stay at MISMATCHES: 0.
- Existing CACE setup of the original driver: main repo
  ~/mnt/sg13cmos5l_cm_ip__single2diff2single/verification/cace (also read that repo's CLAUDE.md).
  Follow its structure.

What to characterize for the bias blocks: the six bias currents into the diodes over PVT,
line sensitivity and PSRR per rail (vdd, vss, vddo, vsso), start-up from 0 V, mismatch,
supply current. For bias + driver: the specs of the existing CACE setup.

Rules:
- Don't write anything into DoNotLitter. No git commands without asking.
  Don't create or append chatlog/*.md. No new scripts unless asked; keep them minimal.
- Write to my computer only via device_commit_files from a new staged dir under
  /mnt/user-data/outputs/, with expectedMtimeMs guards on existing files; verify checksums after.
  Never overwrite my hand edits.
- Keep improvements/log.md going (rebuild log.tex/log.pdf; the LaTeX header is the first 53
  lines of log.tex). Another chat writes to it too: re-read it right before each commit.
- Index external sources, don't copy them. ODF/LibreOffice only, no Microsoft formats.

Cloud setup: IHP-Open-PDK dev branch, sparse checkout of ihp-sg13cmos5l (xschem, ngspice,
klayout dirs). xschem 3.4.4 from apt lacks the Tcl proc ev7 that pnpMPA.sym needs to
netlist: put a stand-in in a scratch xschemrc only, never ship it.
