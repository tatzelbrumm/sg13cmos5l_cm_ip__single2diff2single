v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Template Testbench for output-current noise - OgueyAebischerBias reference} 120 -890 0 0 0.5 0.5 {}
T {H. J. Oguey and D. Aebischer, “CMOS current reference without resistance,”
IEEE J. Solid-State Circuits, vol. 32, no. 7, pp. 1132-1135, Jul. 1997} 400 -140 0 0 0.3 0.3 {}
T {How the current noise is measured
---------------------------------
ngspice's .noise can only take a VOLTAGE as its output, so the mirrored
output current is converted to a voltage by a noiseless CCVS:

  XMREP   replica of the DUT's diode NMOS M11 (w=1u l=1u m=1), gated by
          vbn, so it carries the same current the real fan-out legs mirror
  VDS     holds the replica drain at a fixed Vds - it is an AC short, so
          ALL of XMREP's noise current flows in the sense branch
  Vsense  0 V ammeter in that branch
  HSENSE  CCVS, 1 V/A: v(nsense) is numerically the short-circuit output
          noise current, and HSENSE itself contributes no noise

Those four lines are netlist text in the code block rather than drawn
symbols on purpose: the sense network is measurement scaffolding, not
part of the DUT, and keeping it as text means the transresistance and the
replica sizing are visible in one place.

A plain resistor cannot be used instead of the CCVS: at ~50 nA the
device's own noise current is ~0.1 pA/rtHz, so any resistor small enough
not to disturb the drain node would swamp the measurement with its own
thermal noise.} 400 -430 0 0 0.3 0.3 {}
T {What is reported
----------------
Ibias_noise is the SPOT noise density at f_spot (default 1 Hz), in
nA/rtHz, which is what reference.yaml's unit asks for. Because the sweep
starts at f_spot, that value is vector index 0 - no interpolation, and no
index arithmetic to keep in sync with the sweep settings.

The yaml's description mentions a 0.1-10 Hz band, carried over from the
sky130_cm_ip__biasgen precedent. If you want the integrated RMS current
in a band instead, set f_spot/fn_stop to that band and swap the echoed
variable for the onoise_total line below.

ngspice reports onoise_spectrum as a density (A/rtHz here, given the
1 V/A CCVS). If your build returns a power density instead, the values
will look absurdly small - wrap the expression in sqrt().} 400 -730 0 0 0.3 0.3 {}
N 180 -140 180 -120 {lab=0}
N 420 -320 480 -320 {lab=vbp}
N 420 -300 480 -300 {lab=vbn}
N 420 -280 480 -280 {lab=vbr}
N 260 -280 300 -280 {lab=#net1}
N 360 -260 360 -140 {lab=0}
N 260 -140 360 -140 {lab=0}
N 180 -180 180 -140 {lab=0}
N 260 -180 260 -140 {lab=0}
N 180 -140 260 -140 {lab=0}
N 260 -280 260 -240 {lab=#net1}
N 360 -360 360 -340 {lab=#net2}
N 180 -360 360 -360 {lab=#net2}
N 180 -360 180 -240 {lab=#net2}
C {devices/code_shown.sym} 20 -670 0 0 {name=NGSPICE
simulator=ngspice
only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.nodeset v(vbp)=200m
*
* --- output-current sense network, see the note on the schematic ---
XMREP ndrep vbn 0 0 sg13_hv_nmos w=1u l=1u ng=1 m=1
VDS ndsup 0 CACE\{vds_rep=1.0\}
Vsense ndsup ndrep 0
HSENSE nsense 0 Vsense 1
*
.control
save all
op
noise v(nsense) VDD dec CACE\{noise_pts=10\} CACE\{f_spot=1\} CACE\{fn_stop=100k\}
setplot noise1
* sweep starts at f_spot, so index 0 IS the spot frequency
let Ibias_noise = 1e9 * onoise_spectrum[0]
* alternative: integrated RMS over the whole swept band, in nA
* setplot noise2
* let Ibias_noise = 1e9 * onoise_total
echo $&Ibias_noise > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {devices/code_shown.sym} 20 -780 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
"}
C {reference.sym} 360 -300 0 0 {name=x1}
C {devices/vsource.sym} 180 -210 0 1 {name=VDD value=CACE\{vdd\}}
C {devices/gnd.sym} 180 -120 0 0 {name=l1 lab=0}
C {devices/vsource.sym} 260 -210 0 1 {name=Voff value=0}
C {devices/lab_wire.sym} 480 -320 0 0 {name=l2 lab=vbp}
C {devices/lab_wire.sym} 480 -300 0 0 {name=l3 lab=vbn}
C {devices/lab_wire.sym} 480 -280 0 0 {name=l4 lab=vbr}
C {devices/title.sym} 160 -40 0 0 {name=l5 author="Christoph Maier"}
