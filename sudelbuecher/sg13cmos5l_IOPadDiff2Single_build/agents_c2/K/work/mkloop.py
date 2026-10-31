# writes deck 7 (loop gain, vd = 0 / +1.3 / -1.3 V) and deck 8 (closed-loop steps). One DUT per run: the variant is
# chosen by work/variant.inc (".subckt fix_sel ... fix_vN"), written by run78.sh; ngspice's op does not converge
# with several fixtures in one netlist (Transient op fallback, seen 2026-10-31).
hdr = """.lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.lib cornerPNP.lib typ
.include /home/user/c2/K/out/decks/dut_variants.spice
.include /home/user/c2/K/work/variant.inc
.include /home/user/c2/K/work/nodeset.inc
Vdd vdd 0 3.3
Vs0 s0 0 0
Vs1 s1 0 0
Vext vext 0 3.3
Iext xg 0 5e-06
XKEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XKEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
Vref vref 0 1.65
Vic vic 0 1.65
Ep vinp vic dp 0 0.5
En vinn vic dp 0 -0.5
RL vout vterm 1000
Vterm vterm 0 1.65
CL vout 0 1e-10
"""
opts = ".temp 27\n* no klu: KLU + the mosvar OSDI (S-Varicap) aborts with 'doAnalyses: out of memory'; rshunt 10 GOhm on every node\n* and source stepping are needed for a valid op with S-Varicaps (else Transient op into a latched state, pad 3.28 V)\n.options method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15\n.option warn=1 rshunt=1e10 itl1=500 gminsteps=50\n"
d = ["* K deck 7: loop gain T = -v(vout)/v(fb) of the fixture d2s_mpdda_pd_sel with a CMA / CMB variant (dut_variants.spice,",
     "* chosen by variant.inc). Sources, load (1 kOhm to 1.65 V || 100 pF) and measurement as the CACE template",
     "* d2s_mpdda_pd_sel_tb_loop.sch, plus a differential input vd (template: 0): vd = 0 / +1.3 / -1.3 V -> pad 1.65 / 2.3 / 1.0 V,", "* one vd per run ($vdv), op seeded by .nodeset from the present variant's op at the same vd (nodeset.inc; empty for v0).",
     hdr, "Vd dp 0 0", "x1 vdd 0 vdd 0 vinp vinn vref vout fb ibias vdd s0 s1 0 fix_sel",
     "Lb vout fb 1G", "Cb fb inj 1", "Vinj inj 0 dc 0 ac 1", opts, ".control",
     "set vdv = $vdv", "  alter Vd dc = $vdv", "  op", "  print all > /home/user/c2/K/work/op_$variant_$vdv.txt", "  let vo = v(vout)", "  let va = v(x1.xsel.net2)", "  let vb = v(x1.xsel.net3)",
     "  set svo = \"$&vo\"", "  set sva = \"$&va\"", "  set svb = \"$&vb\"", "  ac dec 50 1 1G",
     "  let T = -v(vout)/v(fb)", "  let Tdb = vdb(T)", "  let Tph = cph(T)*180/pi",
     "  meas ac T0 find Tdb at=10", "  meas ac fc when Tdb=0 fall=1", "  meas ac phc find Tph when Tdb=0 fall=1",
     "  let PM = 180 + phc", "  meas ac gmdb find Tdb when Tph=-180 cross=1", "  let GM = -gmdb",
          "  echo $variant $vdv $svo $sva $svb $&T0 $&fc $&PM $&GM >> /home/user/c2/K/out/logs/loop7.dat",
     ".endc", ".end", ""]
open('/home/user/c2/K/out/decks/loop7_variants.spice','w').write('\n'.join(d))
# deck 8: one stimulus, two steps: the CACE tb_tran step (vd -0.5 -> +0.5 -> -0.5, pad 1.4 / 1.9) at 1 / 5 us,
# then a step at the top of the linear range (vd 0.8 -> 1.3 -> 0.8, pad 2.05 / 2.3) at 13 / 17 us
d = ["* K deck 8: closed-loop step response (fixture with vfb = vout) of a CMA / CMB variant (variant.inc), 1 kOhm to 1.65 V || 100 pF.",
     "* step 1 = CACE tb_tran step vd -0.5 <-> +0.5 V (pad 1.4 <-> 1.9 V) at 1 / 5 us; step 2 vd 0.8 <-> 1.3 V (pad 2.05 <-> 2.3 V) at 13 / 17 us.",
     hdr.replace('reltol',''), "Vd dp 0 pwl(0 -0.5 1u -0.5 1.001u 0.5 5u 0.5 5.001u -0.5 9u -0.5 9.001u 0.8 13u 0.8 13.001u 1.3 17u 1.3 17.001u 0.8 21u 0.8)",
     "x1 vdd 0 vdd 0 vinp vinn vref vout vout ibias vdd s0 s1 0 fix_sel",
     opts.replace('abstol=1e-15 gmin=1e-15','abstol=1e-12 gmin=1e-12'), ".control", "save v(vout)", "tran 2n 21u",
     "wrdata /home/user/c2/K/out/logs/step8_$variant.dat v(vout)"]
for k,(t0,t1,t2) in enumerate(((1,5,9),(13,17,21))):
    d += [f"meas tran v0 find v(vout) at={t0-0.01}u", f"meas tran v1 find v(vout) at={t1-0.1}u", "let dv = v1 - v0",
          "let vn = (v(vout) - v0) / dv",
          f"meas tran t10r when vn=0.1 rise=1 from={t0}u to={t1}u", f"meas tran t90r when vn=0.9 rise=1 from={t0}u to={t1}u",
          f"meas tran t90f when vn=0.9 fall=1 from={t1}u to={t2}u", f"meas tran t10f when vn=0.1 fall=1 from={t1}u to={t2}u",
          f"meas tran vnmax max vn from={t0}u to={t1}u", f"meas tran vnmin min vn from={t1}u to={t2}u",
          "let er = abs(vn - 1)", "let ef = abs(vn)",
          f"meas tran tsr when er=0.01 cross=last from={t0}u to={t1}u", f"meas tran tsf when ef=0.01 cross=last from={t1}u to={t2}u",
          "let sr = 0.8*dv/(t90r - t10r)", "let sf = 0.8*dv/(t10f - t90f)", "let osr = vnmax - 1", "let osf = -vnmin",
          f"let tr = tsr - {t0}.001u", f"let tf = tsf - {t1}.001u",
          f"echo $variant step{k+1} $&v0 $&v1 $&sr $&sf $&osr $&osf $&tr $&tf >> /home/user/c2/K/out/logs/step8.dat"]
d += [".endc", ".end", ""]
open('/home/user/c2/K/out/decks/step8_variants.spice','w').write('\n'.join(d))
