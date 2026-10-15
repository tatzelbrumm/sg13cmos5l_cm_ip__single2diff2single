<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# JanteStrømSpejl: a 2019 lecture slide becomes a CACE-characterised current mirror

2026-10-15. Written by Claude (Opus) about work done by ChatGPT and Claude for
Christoph Maier, in sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/JanteStroemSpejl/.

## 1. Where it started

On 11 March 2019 Christoph gave a test lecture for a faculty position at UiO,
"What's All This Analog IC Design Stuff, Anyhow? How to Think Like an Analog IC
Designer" (slides: bitbucket.org/cmucsd/analogdesignlecture). In the middle of the
talk, the "Matching design pattern" section explains why a current mirror works.
It *subtracts* two nearly equal threshold voltages, and the large die-to-die
variation cancels, leaving only the small local mismatch δV_T:
I₂ ≈ I₁ + g_m·δV_T.

The section "Analog Design Thought that Doesn't Fit a Pattern" then builds a
layout slide by slide. It is a 22-transistor, common-source current mirror: eleven
rows of two transistors, a shared source down the middle, a gate-metal cross, and
the diode-connected reference pair in the cross arm. Drawn in red poly, yellow
diffusion and blue metal, it is the Norwegian flag. Each of the ten output rows
carries one rule of the Jante Law ("Du skal ikke tro at du er noe."). The reference
row carries the eleventh: "Dere tror kanskje ikke at jeg vet noe om dere?"
The slide title is "Interdisciplinary design pattern: Matching".

The joke is exact. A current mirror is a circuit whose specification *is*
Janteloven: no output may be more than any other. The row that "knows something
about everybody" is the one that sets everybody's gate voltage.

## 2. What happened on 15 October 2026

**ChatGPT** session "Russische Etymologie Nemez", morning to 17:11
(Appendix B):

- **The joke.** It began with the etymology of немец, "German", originally "the
  mute one", the one who cannot speak our language. It ended with a LinkedIn image:
  the Danish-flag variant of the layout with Fleet Admiral Chester W. Nimitz,
  "Адмирал немец". It took several corrections before ChatGPT left the layout
  unmodified: "red is poly, yellow is diffusion, white is metal".
- **Layout to netlist.** Asked to turn the picture into a circuit, it read the
  artwork as layout and produced a correct 22-device netlist. Each row is two
  separate `sg13_lv_nmos` (W/L = 4λ/64λ, λ = 0.08 µm), with no `m`/`ng` arraying.
  Row 6 is diode-connected and the twenty other drains pair into ten outputs.
  It also produced an xschem schematic and a development testbench. With the
  user's corrections (one transistor having all the mismatch, a sign error) that
  testbench gave plausible mismatch data. That was real, useful work.
- **CACE.** Asked for a CACE histogram, it wrote a YAML, a template and a pooling
  script. Seven CACE runs (15:39 to 16:54) failed. Instead of reading the CACE source,
  it guessed placeholder syntax, tried a template type CACE does not support, and
  re-zipped unchanged files under new names (`zipslop/`). It ended by exporting
  the chat at the user's request.

**Claude** session, 17:22 to about 18:45 (this report):

- **Toolchain.** Rebuilt the pinned toolchain of the user's IIC-OSIC-TOOLS image,
  following `sudelbuecher/cloud_environment.md`.
- **Diagnosis.** Read the CACE 2.11.0 source and found three plumbing bugs
  (Appendix A): unescaped `CACE\{…\}` placeholders, the wrong result-file name and
  a missing DUT `.include`. ChatGPT's design is otherwise kept, including its
  VDUMMY iteration marker; a SEED line makes runs reproducible.
- **Bias.** The first working run showed every output 2 % low. The cause was the
  bias, inherited from the development testbench: 100 µA from an ideal current
  source forced V_GS = 3.3 V on 1.2 V thin-oxide devices. That is twice the
  process spec's V_GS limit of 1.65 V and above the 2.0 V minimum drain breakdown.
  Neither ChatGPT nor its user had noticed, because the ideal source ignores the
  1.2 V supply drawn next to it. The bias is now 3 µA and 10 µA.
- **Extensions.** Added two follow-up studies the user asked for: output-resistance
  vs. mismatch, and the same mirror in thick-oxide `sg13_hv_nmos`.

## 3. Results (500 seeded mismatch runs × 10 outputs per histogram)

| Device | IREF | V(IREF) | mean error | σ (pooled) |
|---|---|---|---|---|
| sg13_lv_nmos | 3 µA | 0.59 V | −0.04 % | 2.0 % |
| sg13_lv_nmos | 10 µA | 0.90 V | −0.04 % | 1.5 % |
| sg13_hv_nmos | 3 µA | 1.27 V | −0.03 % | 1.7 % |
| sg13_hv_nmos | 10 µA | 1.82 V | −0.02 % | 1.1 % |

**Output resistance vs. mismatch** (3 µA; outputs at V_DS = V_GS(ref) + ΔV):

| ΔV | LV mean | LV σ | HV mean | HV σ |
|---|---|---|---|---|
| −0.3 V | −6.1 % | 1.9 % | −0.82 % | 1.7 % |
| 0 | −0.04 % | 2.0 % | −0.03 % | 1.7 % |
| +0.3 V | +2.6 % | 2.1 % | +0.54 % | 1.7 % |

Moving the output voltage shifts the whole distribution and leaves its width
alone. Above saturation the shift is ≈ 8.5 %/V, an effective Early voltage of
about 12 V even at L = 5.12 µm. The −0.3 V point (V_DS = 0.29 V) is already
near the saturation knee. Over a ±0.3 V output swing the systematic spread,
8.7 %, is four times the random σ. At this bias, a cascode is worth more than
a bigger device.

**Thick oxide.** The same geometry in `sg13_hv_nmos`, at the same currents, has a
smaller spread: σ is 14 % smaller at 3 µA and 27 % smaller at 10 µA. That is
despite an A_VT almost twice as large, 7.0 vs. 3.9 mV·µm in the PDK's mismatch
model. At the same current, the thick-oxide device runs at a much larger
overdrive (V_GS = 1.27 V and 1.82 V), so g_m/I is lower and each millivolt of V_T
scatter costs less current. Its output resistance is also about four times higher.
The shift is ≈ 2.3 %/V (V_A ≈ 45 V), so over ±0.3 V the systematic spread
(1.4 %) stays below σ. "Same operating conditions" here means the same currents
and the same V_DS = V_GS bias; the voltages themselves differ. The HV mirror
needs more headroom: a 1.2 V supply would not fit it.

## 4. Perspective

The same picture went out again on 15 October 2026 as a LinkedIn post: "Hierdie
woordspeling val op dowe ore vir diegene wat nie Nederlands of Afrikaans praat nie."
The post is tagged "Doofe Ohren" and signed "Приветствие, Адмирал немец". It is a pun on
deaf ears: Dutch *doof* means deaf, German *doof* means dumb, немец means mute.
It follows a run of posts aimed, by Christoph's own account without echo, at
Eriksholm, Oticon's hearing research centre, which is "committed to making audiological
discoveries". Its "Partner with Eriksholm" page invites "recognized scientists"
to reach out:

- 11 Oct, "Hearing aid, reimagined": Christiane Nüsslein-Volhard ("Creativity is
  combining facts no one else has connected before") celebrating her retirement
  with a Quodlibet, answered with the Quodlibet section of Christoph's 2000 ETH
  dissertation, and Goethe's *licet quod decet* vs. *licet quod libet*.
- 12 Oct, Einstein on discovery (The Atlantic, Nov. 1945): "Only a free
  individual can make a discovery". A comment quotes Eriksholm's invitation
  verbatim.

The files next to this report show that the 2019 slide is a design artifact as
well as a joke. A language model can read it as a layout and turn it into a
netlist. An open PDK and CACE then turn the netlist into a calibrated statement:
a Jante mirror keeps its ten outputs within a few percent of one another, and no
closer. Getting from a plausible histogram to a correct one took two checks that
no tool volunteered: reading the CACE source when its error messages explained
nothing, and noticing that the bias source was running 1.2 V gates at 3.3 V.

## Appendix A: The CACE fix, line by line

Template `cace/templates/JanteStroemSpejl_cace_mismatch.sch`, against ChatGPT's last version:

| # | ChatGPT | now | why |
|---|---|---|---|
| 1 | `value=CACE{iterations}` | `value=CACE\{iterations\}` | CACE 2.11.0, `parameter.py`, `get_condition_names_used(escape=True)`: for `.sch` templates and cace_format 5.2 the regex is `CACE\\\{([^ \}\t]+)\\\}`. Unescaped placeholders are invisible, which is the source of "No conditions found" and "Couldn't find condition iterations". |
| 2 | `> CACE{simpath}/CACE{filename}.data` | `> CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data` | `parameter_ngspice.py` reads `<template>_<index><suffix>`. |
| 3 | (none) | `.include CACE\{DUT_path\}` | CACE rewrites the DUT symbol to `type=primitive` for the testbench, so the subcircuit must be included. |
| 4 | `IREFSRC value=100u`, `/100u` | `value=CACE\{iref\}`, `/CACE\{iref\}` | 100 µA gives V(IREF) = 3.3 V (Section 2). The conditions are 3u and 10u. |
| 5 | (none) | `.option SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]` | Reproducible draws; same line as `macros/inverter`. Without it ngspice seeds from the process id. |
| 6 | (none) | `.lib cornerMOShv.lib mos_tt_mismatch`, `C {CACE\{DUT_name\}.sym}`, `VDVDS DREF IREF CACE\{dvds=0\}` | One template serves the LV and the HV datasheet and the r_out sweep. With dvds = 0 the LV results are bit-identical to the version without these lines. |

Systematic error with typical models (no mismatch), by IREF, LV:
100 µA: V(IREF) 3.32 V, −2.0 %; 30 µA: 1.49 V, −0.10 %; 10 µA: 0.90 V, −0.018 %; 3 µA: 0.59 V, −0.009 %.

Where ChatGPT went astray, apart from the bugs:

- The VDUMMY rationale ("so CACE sees the iterations condition") was wrong.
  `CACE\{…\}` is found anywhere in the file, including `code_shown` blocks.
  VDUMMY is kept as a visible, electrically isolated iteration marker.
- Runs 16:33 and 16:37 tried a `.spice` template. CACE 2.11.0 answers
  "TODO: Implement substitution for spice templates!".
- At 16:51 and 16:54 it had located `get_condition_names_used()` in the user's
  pasted code but had not read it.
- `cace/templates/xschemrc` is unused. CACE netlists with the PDK's xschemrc.

CACE quirk, cosmetic: with more than one condition set, the plot gets a legend
and `savefig(bbox_extra_artists=[legend])` crops the title.

Environment quirk: in 1 of 5 runs, two xschem processes started by CACE for two
parameters at once crashed (`Tcl_AppInit`, exit −11). Use `--parallel-parameters 1`.

## Appendix B: ChatGPT session timeline

From the user's PDF print of chatgpt.com/c/6ad0a469-05d8-83eb-889f-0b6d945ad274
(53 pages, printed 17:11) and `JanteStroemSpejl_chat_export/`. Times are where the
log shows them. User turns are quoted in their original language.

1. "etymologie russisch für deutsche: nemez". немец comes from немой, "mute".
2. The user uploads `JanteStroemSpejl.svg` and asks for a mashup with "diesem
   'stummen' Großadmiral vor der dänischen Janteloven-Fahne … so, dass alle 10+1
   Gebote lesbar und nicht verdeckt sind".
3. ChatGPT alters the flag. The user: "Lass die Janteloven-Fahne unverändert und die
   Sprache auch. Den Witz mit dem Layout der Fahne verstehst du nicht und machst
   ihn kaputt." Then "Oder kannst du CMOS-Layouts lesen?" ChatGPT answers yes,
   within limits.
4. Layer correction by the user: "Rot ist Polysilizium, gelb ist Diffusion",
   "Weiss ist Metall". The mashup succeeds after the user has the canvas extended
   and Nimitz placed beside the circuit (`pix/JanteStroemSpejl_Nimitz.png`).
5. "Mach da mal eine Schaltung draus, skaliert auf lambda … als xschem-Schaltung
   für IHP sg13cmos5L". The first schematic has broken `m`/`ng`. The user asks for
   an ngspice netlist first, which becomes `JanteStroemSpejl_explicit22.spice` and
   `JanteStroemSpejl_contact_port_map.txt`, then the schematic and the mismatch
   testbench.
6. Iterations in the IIC-OSIC-TOOLS container: "BARF" (5 MB of ngspice output),
   the netlist location, "Can you do it or should I ask Claude?", nine outputs
   stuck at −1 (only one device had mismatch), the current sign fix. Result: a
   working five-run development testbench.
7. "Ok, can you use CACE to produce a nice histogram of the runs?" ChatGPT
   delivers YAML, template and script without running them.
8. Seven failed CACE runs. The user asks for the latest ZIP; the ZIPs carry
   13:40 timestamps; "You're giving me crap"; re-zipping; "you just touched the
   otherwise unmodified files and produced a shitload of administrative clutter".
   ChatGPT agrees.
9. ChatGPT asks for `get_condition_names_used()`. The user pastes the surrounding
   code, and the user requests a verbatim export of the chat.

## Appendix C: Reproduction

Inside IIC-OSIC-TOOLS (2026.09: CACE 2.11.0, ngspice-47, xschem 3.4.8RC
ddc7344, IHP dev c271a7e9), from this directory:

    cace cace/JanteStroemSpejl.yaml   --source schematic -j 8 --parallel-parameters 1
    cace cace/JanteStroemSpejlHV.yaml --source schematic -j 8 --parallel-parameters 1

Each takes about 10 minutes and writes
`runs/RUN_<date>/parameters/{mirror_mismatch,mirror_rout}/` with
`pooled_mismatch.svg`, `rout_shift.svg` and `simulation_summary.{md,csv}`.

The numbers above come from the same versions built in a cloud container, per
`sudelbuecher/cloud_environment.md`. Two reruns gave bit-identical `.data` files.

Files touched by Claude:

- `cace/JanteStroemSpejl.yaml`: fixed, `iref` and `mirror_rout` added.
- `cace/JanteStroemSpejlHV.yaml`: new; the same datasheet with name `JanteStroemSpejlHV`.
- `cace/templates/JanteStroemSpejl_cace_mismatch.sch`: Appendix A.
- `JanteStroemSpejlHV.sch` and `.sym`: new. `JanteStroemSpejl.sch` with
  `sg13_lv_nmos` → `sg13_hv_nmos`; same geometry, which is above the HV minimum of
  W 0.30 µm and L 0.45 µm.
- `README.txt`: fix log.
- `REPORT.md`: this file.

Unchanged: `JanteStroemSpejl.sch`/`.sym`, `JanteStroemSpejl_tb_mismatch.sch`
(still 100 µA), `cace/scripts/pool_mismatch.py`.

## Appendix D: Sources

- C. Maier, "What's All This Analog IC Design Stuff, Anyhow?", test lecture, UiO,
  11 March 2019. bitbucket.org/cmucsd/analogdesignlecture
- C. H. Maier, "Equivalent circuit models and interface circuits for CMOS
  microsensors", Diss. ETH No. 13532, 2000, "Quodlibet", p. 167.
  https://cmucsd.bitbucket.io/akademix/PhD.pdf#page=168
- LinkedIn posts by C. Maier, 6, 7, 11, 12 and 15 Oct 2026.
  The 15 Oct post: https://lnkd.in/p/ez5utx59
- A. Einstein, "Einstein on the Atomic Bomb", The Atlantic, Nov. 1945.
  https://www.theatlantic.com/magazine/archive/1945/11/einstein-on-the-atomic-bomb/656626/
- C. Maier, Flickr album "Quodlibet".
  https://www.flickr.com/photos/89067995@N00/albums/72177720303647432/
- Eriksholm Research Centre, "Partner with Eriksholm".
  https://eriksholm.com/partner-with-eriksholm/
- IHP, SG13CMOS5L process specification, §2.1.1 NMOS (V_GS ≤ 1.65 V, BV_DSS ≥ 2.0 V).
  IHP-Open-PDK `ihp-sg13cmos5l/libs.doc/doc/SG13CMOS5L_os_process_spec.pdf`
- IHP-Open-PDK `sg13g2_moslv_mismatch.lib` / `sg13g2_moshv_mismatch.lib`: A_VT
  (`delvto_mm`) 3.9 mV·µm (LV) and 7.0 mV·µm (HV).
- CACE 2.11.0, `cace/parameter/parameter.py`, `parameter_ngspice.py` (PyPI `cace`).
