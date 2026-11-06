# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Characterization of the replica bias blocks vcm_rb and vref_s2d_rb, alone and with the pads (closed loop).

Every block gets its reference from its own bias_gen_pd (same selection as the pads': 0 harness iDAC 5 uA, 1 Oguey-Aebischer
core, 2 bandgap core) and its own supply source (Vbc for vcm_rb, Vbr for vref_s2d_rb, both at iovdd), so its current
is measured; the 5 uA reference it takes from bias_gen_pd is measured in series (Vic / Vir).
Closed loop: the pad decks of ../pad_char/run_pad_char.py with the ideal Vref / Vcm replaced by the blocks.

usage (repo env): python3 -I run_rb.py <experiment> [-j 4]; results in results/<experiment>.tsv
"""
import argparse
import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "pad_char"))
import run_pad_char as R  # noqa: E402

R.RUNS = HERE / "_runs"
R.RES = HERE / "results"
MAC = R.MACROS
RB_INC = [str(MAC / "vcm_rb/netlist/source/vcm_rb.spice"), str(MAC / "vref_s2d_rb/netlist/source/vref_s2d_rb.spice")]
GEN_INC = ["hv_logic/netlist/source/hv_logic.spice", "ls_up_1v2_3v3/netlist/source/ls_up_1v2_3v3.spice",
           "en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice", "bias_tree_pd/netlist/source/bias_ref_pd.spice",
           "bias_gen_pd/netlist/source/bias_gen_pd.spice"]


def blocks(c, vdd_node="iovdd"):
    """vcm_rb and vref_s2d_rb with their own bias_gen_pd, on the harness controls of R.harness(c, 'b')."""
    return f"""{R.harness(c, 'b')}Iextc xgc 0 5u
XEdc xgc xgc vextb vextb sg13_hv_pmos w=5u l=6u
XEmc ibiasc xgc vextb vextb sg13_hv_pmos w=5u l=6u
Xgr iovdd 0 ibiasc irr en_3v3b sel0_3v3b sel1_3v3b bias_gen_pd
Vic irefb irc2 0
Vir irr irr2 0
Vbc vddc 0 dc {c['vdd']}
Vbr vddr 0 dc {c['vdd']}
Xvcm vddc 0 irc2 vcm en_3v3b en_3v3_bb vcm_rb
Xvrf vddr 0 irr2 vref en_3v3b en_3v3_bb vref_s2d_rb
"""


def gen_models_inc(c, extra=()):
    return R.models(c) + R.includes(GEN_INC + list(extra), RB_INC)


# ------------------------------------------------------------------ blocks alone
def deck_rb_dc(c):
    return f"""* replica blocks DC, {c}
{gen_models_inc(c)}Vio iovdd 0 dc {c['vdd']}
{blocks(c)}.temp {c['temp']}
{R.OPTS_S2D}.control
op
let ic = -i(vbc)
let ir = -i(vbr)
let irefc = i(vic)
let irefr = i(vir)
echo RES $&v(vcm) $&v(vref) $&ic $&ir $&irefc $&irefr $&v(xvcm.gh) $&v(xvcm.xp) $&v(xvcm.m)
.endc
.end
"""


def deck_rb_z(c):
    return f"""* replica blocks output impedance, {c}
{gen_models_inc(c)}Vio iovdd 0 dc {c['vdd']}
{blocks(c)}Izc 0 vcm dc 0 ac 1
Izr 0 vref dc 0 ac 0
.temp {c['temp']}
{R.OPTS_S2D}.control
ac dec 10 1 100meg
let z = mag(v(vcm))
meas ac zc1k find z at=1k
meas ac zc1m find z at=1meg
set s_zc1k = $&zc1k
set s_zc1m = $&zc1m
alter @izc[acmag] = 0
alter @izr[acmag] = 1
ac dec 10 1 100meg
let z = mag(v(vref))
meas ac zr1k find z at=1k
meas ac zr1m find z at=1meg
echo RES $s_zc1k $s_zc1m $&zr1k $&zr1m
.endc
.end
"""


def deck_rb_en(c):
    cc = dict(c, en="pwl(0 0 2u 0 2.001u 1.2 40u 1.2 40.001u 0)")
    return f"""* replica blocks enable at 2 us, disable at 40 us, {c}
{gen_models_inc(c)}Vio iovdd 0 dc {c['vdd']}
{blocks(cc)}.temp {c['temp']}
.options savecurrents method=gear reltol=1e-4 abstol=1e-12 gmin=1e-12
.control
save v(vcm) v(vref) i(vbc) i(vbr)
tran 20n 60u
meas tran vc_end find v(vcm) at=39.9u
meas tran vr_end find v(vref) at=39.9u
let ec = abs(v(vcm) - vc_end)
let er = abs(v(vref) - vr_end)
let bc = 0.01*vc_end
let br = 0.01*vr_end
meas tran tc when ec=bc cross=last from=2u to=39.9u
meas tran tr when er=br cross=last from=2u to=39.9u
let t_vcm = tc - 2u
let t_vref = tr - 2u
meas tran vc_max max v(vcm) from=2u to=39.9u
meas tran vr_max max v(vref) from=2u to=39.9u
meas tran vc_off find v(vcm) at=59.9u
meas tran vr_off find v(vref) at=59.9u
let icc = -i(vbc)
let irr = -i(vbr)
meas tran ic_off find icc at=59.9u
meas tran ir_off find irr at=59.9u
echo RES $&t_vcm $&t_vref $&vc_end $&vr_end $&vc_max $&vr_max $&vc_off $&vr_off $&ic_off $&ir_off
.endc
.end
"""


def deck_rb_up(c):
    """iovdd (and the blocks' supplies) ramp 0 -> vdd in 10 us; core 1.2 V and enable present from t = 0; every node
    starts at 0 V (uic: the operating point with iovdd = 0 does not converge at ss / -40 C, in the bandgap core's PNP)."""
    d = deck_rb_dc(c)
    d = d.replace(f"Vio iovdd 0 dc {c['vdd']}", f"Vio iovdd 0 pwl(0 0 10u {c['vdd']})")
    d = d.replace(f"Vbc vddc 0 dc {c['vdd']}", "Ebc vddc 0 iovdd 0 1").replace(f"Vbr vddr 0 dc {c['vdd']}",
                                                                              "Ebr vddr 0 iovdd 0 1")
    d = d.replace("Vs33b s33b 0 3.3", "Es33b s33b 0 iovdd 0 1")
    ctrl = d[d.index(".control"):]
    d = d.replace(ctrl, """.control
tran 20n 80u uic
meas tran vc_end find v(vcm) at=79.9u
meas tran vr_end find v(vref) at=79.9u
let ec = abs(v(vcm) - vc_end)
let er = abs(v(vref) - vr_end)
let bc = 0.01*vc_end
let br = 0.01*vr_end
meas tran tc when ec=bc cross=last from=0 to=79.9u
meas tran tr when er=br cross=last from=0 to=79.9u
echo RES $&tc $&tr $&vc_end $&vr_end
.endc
.end
""")
    return d.replace(R.OPTS_S2D, ".options method=gear reltol=1e-4 abstol=1e-12 gmin=1e-12\n")


def deck_rb_mm(c):
    cc = dict(c, corner_mos="tt_mismatch")
    return deck_rb_dc(cc).replace(R.OPTS_S2D, R.OPTS_S2D.replace("gmin=1e-15", f"gmin=1e-15 SEED={c['seed']}"))


# ------------------------------------------------------------------ closed loop: pads with the blocks
def deck_s2d_dc_rb(c):
    d = R.deck_s2d_dc(dict(c, vref=0, vcm=0))
    d = d.replace(R.includes(R.S2D_INC), R.includes(R.S2D_INC, RB_INC))
    d = d.replace("Vref vref 0 dc 0\n", "").replace("Vcm vcm 0 0\n", "")
    d = d.replace("Rsrc vsrc pad 50", "Rsrc vsrc pad 50\n" + blocks(c))
    d = d.replace("save v(outp) v(outn) v(vcm) v(u) i(vio) i(vcore)", "save v(outp) v(outn) v(vcm) v(vref) v(u) i(vio) i(vcore)")
    return d.replace("echo RES $&Gain $&Vos_in $&INL $&Vcm_err $&Iio",
                     "meas dc vrefo find v(vref) at=0\nmeas dc vcmo find v(vcm) at=0\n"
                     "echo RES $&Gain $&Vos_in $&INL $&Vcm_err $&Iio $&vrefo $&vcmo")


def deck_s2d_win_rb(c):
    """pad = a GROUND-referenced source swept 0 ... vref + 1 V (vref = the block's DC value, rb_dc), as an external
    signal would be; the S2D sees pad - vref(block). Output vd(pad) to a file for the window (linear to 1 mV)."""
    d = deck_s2d_dc_rb(c)
    d = d.replace("Ein vsrc vref u 0 1", f"Vrefx vrefx 0 {c['vref_dc']}\nEin vsrc vrefx u 0 1")
    ctrl = d[d.index(".control"):]
    return d.replace(ctrl, f""".control
save v(outp) v(outn) v(u) v(vref) v(pad)
dc Vu -{c['vref_dc']} 1.0 0.005
let vd = v(outp) - v(outn)
wrdata {R.RUNS}/win_{c['tag']}.dat v(pad) vd v(vref)
echo RES done
.endc
.end
""")


def win_conds():
    v = rb_values()
    for vdd, m, t in itertools.product(R.VDDS, ["ss", "tt", "ff"], R.TEMPS):
        yield dict(vdd=vdd, corner_mos=m, temp=t, sel=0, tag=f"{vdd}_{m}_{t}", vref_dc=v[(str(vdd), m, str(t), "0")][0])


def deck_d2s_dc_rb(c):
    """D2S with vref = vcm_rb's output and the input common mode at the same net (as in the chain), load to vref."""
    d = R.deck_d2s_dc(dict(c, vref=0, vicm=0, vterm=0))
    d = d.replace(R.includes(R.D2S_INC), R.includes(R.D2S_INC, RB_INC))
    d = d.replace("Vref vref 0 0\n", "").replace("Vic vic 0 dc 0\n", "Evic vic 0 vcm 0 1\n")
    d = d.replace("Vterm vterm 0 0", "Evt vterm 0 vcm 0 1")
    d = d.replace("X1 iovdd 0 vcore 0 pad vinp vinn vref ", "X1 iovdd 0 vcore 0 pad vinp vinn vcm ")
    d = d.replace("RL pad vterm", blocks(c) + "RL pad vterm")
    d = d.replace("save v(pad) v(vref)", "save v(pad) v(vcm)").replace("let vo = v(pad) - v(vref)",
                                                                       "let vo = v(pad) - v(vcm)")
    return d.replace("echo RES $&Gain $&Vos_out $&INL $&Iio $&IqP $&Imin",
                     "meas dc vcmo find v(vcm) at=0\necho RES $&Gain $&Vos_out $&INL $&Iio $&IqP $&Imin $&vcmo")


def deck_loop_rb(c):
    d = R.deck_loop(dict(c, vref_s2d=0, vcm=0))
    d = d.replace(R.includes(R.S2D_INC, R.D2S_INC), R.includes(R.S2D_INC + R.D2S_INC, RB_INC))
    d = d.replace("Vrefs vrefs 0 0\n", "").replace("Vcm vcm 0 0\n", "")
    d = d.replace("Ein vsrc vrefs u 0 1", "Ein vsrc vref u 0 1").replace("pin dp dn vcm vrefs", "pin dp dn vcm vref")
    return d.replace("Rsrc vsrc pin 50", "Rsrc vsrc pin 50\n" + blocks(c))


def deck_s2d_en_rb(c):
    """S2D enable (en_1v2 at 1 us, u = +0.25 V) with vref / vcm from the blocks; seq 'before': blocks on from t = 0,
    'together': the blocks' en_1v2 switches with the pad's."""
    d = R.deck_s2d_en_z(dict(c, vref=0, vcm=0, rs=1e-3, cb=0))
    d = d.replace(R.includes(R.S2D_INC), R.includes(R.S2D_INC, RB_INC))
    for s in ("Vref vref 0 dc 0\n", "Vcm vcm 0 0\n", "Rvref vref vrefi 0.001\n", "Rvcm vcm vcmi 0.001\n"):
        d = d.replace(s, "")
    d = d.replace("vcmi vrefi iref", "vcm vref iref").replace("Ein vsrc vref u 0 1", "Ein vsrc vrefx u 0 1")
    # the input source is referenced to the block's settled vref (sampled by an ideal source at its DC value)
    cb = dict(c, en="pwl(0 0 1u 0 1.001u 1.2)") if c.get("seq") == "together" else c
    d = d.replace("Rsrc vsrc pad 50", f"Vrefx vrefx 0 {c['vref_dc']}\nRsrc vsrc pad 50\n" + blocks(cb))
    d = d.replace("v(vcmi)", "v(vcm)").replace("v(vrefi)", "v(vref)")
    # pin deviations relative to the blocks' own settled values
    d = d.replace("let ec = v(vcm) - v(vcm)", f"let ec = v(vcm) - {c['vcm_dc']}")
    d = d.replace("let er = abs(v(vref) - v(vref))", f"let er = abs(v(vref) - {c['vref_dc']})")
    d = d.replace("let vc = (v(outp) + v(outn))/2 - v(vcm)", f"let vc = (v(outp) + v(outn))/2 - {c['vcm_dc']}")
    return d


def rb_values():
    rows = [l for l in open(R.RES / "rb_dc.tsv") if not l.startswith("#")]
    import csv as _csv
    return {(r["vdd"], r["corner_mos"], r["temp"], r["sel"]): (float(r["vref"]), float(r["vcm"]))
            for r in _csv.DictReader(rows, delimiter="\t")}


def en_conds():
    v = rb_values()
    for vdd, m, seq in itertools.product([3.0, 3.3], ["ss", "tt", "ff"], ["before", "together"]):
        vr, vc = v[(str(vdd), m, "27", "0")]
        yield dict(vdd=vdd, corner_mos=m, temp=27, sel=0, seq=seq, vref_dc=vr, vcm_dc=vc)


def loop_eq_conds():
    v = rb_values()
    for vdd, m, t in itertools.product(R.VDDS, R.CORNERS, R.TEMPS):
        vr, vc = v[(str(vdd), m, str(t), "0")]
        yield dict(vdd=vdd, corner_mos=m, temp=t, vref_s2d=vr, vcm=vc)


EXP = {
    "rb_dc": dict(what="blocks alone: vcm, vref, block supply currents (without / with the 5 uA reference), internal nodes",
                  kind="dc", deck=deck_rb_dc,
                  cols=["vcm", "vref", "I_vcm_rb", "I_vref_s2d_rb", "Iref_vcm_rb", "Iref_vref_s2d_rb", "gh", "xp", "m"],
                  conds=lambda: R.grid(vdd=R.VDDS, corner_mos=R.CORNERS, temp=R.TEMPS, sel=[0, 1, 2])),
    "rb_z": dict(what="output impedance |Z| at 1 kHz / 1 MHz (vcm_rb with its CB, vref_s2d_rb with CB1 / CB2)", kind="dc",
                 deck=deck_rb_z, cols=["Zvcm_1k", "Zvcm_1M", "Zvref_1k", "Zvref_1M"],
                 conds=lambda: R.grid(vdd=[3.0, 3.3, 3.6], corner_mos=["ss", "tt", "ff"], temp=R.TEMPS, sel=[0])),
    "rb_en": dict(what="enable (en_1v2 0 -> 1.2 V at 2 us) and disable (at 40 us): settling to 1 %, overshoot, off state",
                  kind="dc", deck=deck_rb_en,
                  cols=["t_vcm", "t_vref", "vcm", "vref", "vcm_max", "vref_max", "vcm_off", "vref_off", "I_vcm_rb_off",
                        "I_vref_s2d_rb_off"],
                  conds=lambda: R.grid(vdd=[3.0, 3.6], corner_mos=["ss", "tt", "ff"], temp=[-40, 27, 125],
                                       sel=[0, 1, 2])),
    "rb_up": dict(what="start-up: iovdd ramp 0 -> vdd in 10 us with the enable requested from t = 0", kind="dc",
                  deck=deck_rb_up, cols=["t_vcm", "t_vref", "vcm", "vref"],
                  conds=lambda: R.grid(vdd=[3.0, 3.6], corner_mos=["ss", "tt", "ff"], temp=[-40, 27, 125],
                                       sel=[0, 1, 2])),
    "rb_mm": dict(what="mismatch Monte Carlo of the blocks (mos tt_mismatch, mm_ok = 1 on every block device), tt 27 C",
                  kind="dc", deck=deck_rb_mm, cols=["vcm", "vref", "I_vcm_rb", "I_vref_s2d_rb", "Iref_vcm_rb",
                                                    "Iref_vref_s2d_rb", "gh", "xp", "m"],
                  conds=lambda: (dict(vdd=3.3, temp=27, sel=0, seed=s) for s in range(1, 101))),
    "cl_s2d_dc": dict(what="S2D DC (INL over u = +-0.5 V around the block's vref) with vref / vcm from the blocks",
                      kind="dc", deck=deck_s2d_dc_rb, cols=R.S2D_DC_COLS + ["vref", "vcm"],
                      conds=lambda: R.grid(vdd=R.VDDS, corner_mos=R.CORNERS, temp=R.TEMPS, sel=[0, 1, 2])),
    "cl_d2s_dc": dict(what="D2S DC (vd = +-1 V) with vref = vicm = vterm = vcm_rb's output", kind="dc",
                      deck=deck_d2s_dc_rb, cols=R.D2S_DC_COLS + ["vcm"],
                      conds=lambda: R.grid(vdd=R.VDDS, corner_mos=R.CORNERS, temp=R.TEMPS, sel=[0, 1, 2])),
    "cl_loop": dict(what="round trip S2D pad -> D2S pad with both blocks (out - vcm vs pad - vref)", kind="dc",
                    deck=deck_loop_rb, cols=R.LOOP_COLS,
                    conds=lambda: R.grid(vdd=R.VDDS, corner_mos=R.CORNERS, temp=R.TEMPS, sel=[0])),
    "cl_loop_eq": dict(what="round trip S2D pad -> D2S pad, vref_s2d / vcm = the blocks' DC outputs (rb_dc, sel 0) as "
                       "ideal sources (exact at DC; the deck with the blocks inside does not converge)", kind="dc",
                       deck=R.deck_loop, cols=R.LOOP_COLS, conds=loop_eq_conds),
    "cl_s2d_en": dict(what="S2D enable with the blocks (blocks on before / enabled together); pin deviations from the "
                           "blocks' settled values", kind="dc", deck=deck_s2d_en_rb,
                      cols=["t_on", "Vc_max", "Vc_min", "dvcm_max", "dvcm_min", "dvref", "vd_end"], conds=en_conds),
    "cl_s2d_win": dict(what="S2D pad swept with the block's vref; data files for the window (post-processing)",
                       kind="dc", deck=deck_s2d_win_rb, cols=["done"], conds=win_conds),
}

if __name__ == "__main__":
    R.EXPERIMENTS.update(EXP)
    ap = argparse.ArgumentParser()
    ap.add_argument("experiments", nargs="+")
    ap.add_argument("-j", type=int, default=4)
    ap.add_argument("--rerun-failed", action="store_true")
    a = ap.parse_args()
    f = R.rerun_failed if a.rerun_failed else R.experiment
    bad = sum(f(e, a.j) for e in a.experiments)
    sys.exit(1 if bad else 0)
