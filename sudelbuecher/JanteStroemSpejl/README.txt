CACE-only files for JanteStroemSpejl
====================================

These files do NOT replace or modify:
  JanteStroemSpejl.sch
  JanteStroemSpejl.sym
The development testbench JanteStroemSpejl_tb_mismatch.sch is separate.
Its reference current is now  .param IREF=10u  (block PARAMS); the
.control section reads the same value through  .csparam irefval=IREF .
10u is the worst-case-safe choice: V(IREF) <= 1.11 V over
ss/tt/ff/sf/fs x -55/27/125 C (ss, 125 C is the worst case).

The dedicated CACE testbench is:
  cace/templates/JanteStroemSpejl_cace_mismatch.sch

It contains exactly one operating-point run. CACE performs the outer loop.
One template serves two datasheets:
  cace/JanteStroemSpejl.yaml    thin oxide,  sg13_lv_nmos (JanteStroemSpejl.sch)
  cace/JanteStroemSpejlHV.yaml  thick oxide, sg13_hv_nmos (JanteStroemSpejlHV.sch)
Each has two parameters, 500 iterations each:
  mirror_mismatch  iref = 3u, 10u; outputs at V(IREF)     -> pooled_mismatch.svg
  mirror_rout      iref = 3u; outputs at V(IREF)+dvds,
                   dvds = -0.3, 0, +0.3 V                 -> rout_shift.svg

Run, inside IIC-OSIC-TOOLS (about 10 minutes each with -j 8):
  cace cace/JanteStroemSpejl.yaml   --source schematic -j 8 --parallel-parameters 1
  cace cace/JanteStroemSpejlHV.yaml --source schematic -j 8 --parallel-parameters 1
--parallel-parameters 1: two xschem processes started at the same moment
crashed once in five runs (Tcl_AppInit, exit -11).
Results: runs/RUN_<date>/parameters/<parameter>/
Datasheet with figures: docs/JanteStroemSpejl[HV].md and
docs/JanteStroemSpejl[HV]_schematic.md (overwritten on every run).
Histograms with common bin edges, for comparing peak heights:
  python3 cace/scripts/replot_shared_bins.py runs/RUN_<date>
  -> runs/RUN_<date>/parameters/<parameter>/<parameter>_shared_bins.svg
Write-up with all numbers: REPORT.md (pictures in pix/, sources in ref/)


2026-10-15 fix (Claude Opus, after ChatGPT)
===========================================

Verified in the cloud with the image's pins (sudelbuecher/cloud_environment.md):
CACE 2.11.0, ngspice-47, xschem ddc7344, OpenVAF 5ed9e63, IHP dev c271a7e9.

Results (5000 samples per current):
  iref = 3u   V(IREF) = 0.59 V   mean -0.04 %   sigma 2.0 %   range -7.1 .. +7.4 %
  iref = 10u  V(IREF) = 0.90 V   mean -0.04 %   sigma 1.5 %   range -5.2 .. +5.9 %
Two reruns gave bit-identical .data files.

What was wrong, in the order CACE would have hit it
---------------------------------------------------

1. Unescaped placeholders (the actual blocker).
   For a .sch template CACE reads the schematic file itself, where braces
   inside attributes must be escaped. CACE 2.11.0 parameter.py,
   get_condition_names_used(..., escape=True), with cace_format 5.2:
       CACE\\\{([^ \}\t]+)\\\}
   so only  CACE\{iterations\}  is found; CACE{iterations} is invisible.
   That one cause produced both log lines of every failed run:
     "No conditions found in template ..."
     "Couldn't find condition "iterations" used for collating the results."
   Same convention as macros/inverter/verification/cace/templates/.

2. Result file name. CACE reads <template>_<N>.data, so the echo target must
   be  CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data , not ...CACE{filename}.data.

3. No DUT include. CACE turns JanteStroemSpejl.sym into a primitive for the
   testbench netlist, so the subcircuit must come from
   .include CACE\{DUT_path\} .

4. Operating point outside the device ratings (inherited from the
   development testbench JanteStroemSpejl_tb_mismatch.sch, which is now
   set to IREF = 10u as well).
   IREF = 100 uA from an ideal current source into the diode pair
   (2 x sg13_lv_nmos, W/L = 0.32u/5.12u) forced V(IREF) = 3.3 V. The
   ideal source ignores the 1.2 V VDD next to it. SG13CMOS5L process spec,
   2.1.1 NMOS: VGS <= 1.65 V (TDDB, 1 FIT in 10 years), BVDSS >= 2.0 V.
   About 2 % of the current never reached the drains, so every output read
   -2.0 % even with mismatch off (mos_tt). The repeated "dynamic gmin
   stepping" notes in ngspice.stderr were a symptom of the same thing.
   Systematic error with mos_tt, by IREF:
     100u: V(IREF) 3.32 V, -2.0 %    30u: 1.49 V, -0.10 %
     10u:  0.90 V, -0.018 %          3u:  0.59 V, -0.009 %
   iref is now a CACE condition (enumerate [3u, 10u]) and also the
   normalisation of e01..e10.

Where it went astray
--------------------

- It guessed placeholder syntax and repackaged ZIPs (zipslop/) instead of
  reading the one function that decides it. At the end it had found
  get_condition_names_used() but had not read it.
- Runs 16-33 and 16-37 tried a .spice template. CACE 2.11.0 does not support
  that: "TODO: Implement substitution for spice templates!".
- The VDUMMY rationale was wrong. CACE does not need the condition in a
  component value; CACE\{...\} anywhere in the file works, including inside
  code_shown blocks. VDUMMY is kept anyway, as a visible iteration marker.
  It is electrically isolated, so it is harmless.

Added: seeded runs
------------------

  .option SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
(same line as the inverter template). Each iteration is a distinct,
repeatable draw. Without it ngspice seeds from the process id: still
different per run, but not reproducible. Both currents use the same seeds,
so iteration k is the same "chip" at 3u and at 10u.

Known CACE 2.11.0 quirks
------------------------

Misleading histograms: every condition set gets its own ax.hist(...,
bins="auto"), so the bin width scales with each set's own sigma and the
peaks come out equally high. Don't compare peak heights in CACE's plots;
use cace/scripts/replot_shared_bins.py.

Cosmetic: with more than one condition set CACE draws a legend and saves
with bbox_extra_artists=[legend]. The tight bounding box then drops the
plot title, which is in the SVG but cropped.

Unused leftover: cace/templates/xschemrc. CACE netlists with the PDK
xschemrc, not this one.
