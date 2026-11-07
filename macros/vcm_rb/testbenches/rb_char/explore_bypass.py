# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Extra bypass capacitors on vcm and vref of pad_ref_rb (Christoph, 2026-11-07: room at the bottom of slot 7; "if we
can afford the space, we should have nmos and pmos bypass capacitors in parallel"). Each variant adds 12u x 12u hv
MOS capacitors per node, on top of the drawn ones (CB on vcm, CB1 / CB2 on vref, NMOS to vss):

  now    nothing added
  nmos   + 2 NMOS, gate to the node, rest to vss
  pmos   + 2 PMOS, gate to the node, rest to the block's supply (= iovdd, the pads' unit rail)
  both   + 1 NMOS + 1 PMOS (the same added area as nmos / pmos)
  both2  + 2 NMOS + 2 PMOS (twice the area)
  ideal  (psrr only) the pads with ideal vref / vcm at the blocks' DC values: the pads' own supply rejection

Experiments (results/bypass_*.tsv):
  bypass_s2d   iovdd ripple (1 V AC on every 3.3 V source: pads, harness, blocks) -> S2D differential output referred
               to its input (/2), and |vref|, |vcm|, at 1 k / 100 k / 1 M / 10 MHz. The pad source is ground-referenced
               (as an external signal), so ripple on vref shows up as input.
  bypass_d2s   the same ripple -> D2S output (ground-referenced) and |vcm|; D2S input common mode = vcm, as in the chain.
  bypass_kick  S2D enable with the blocks (cl_s2d_en): the kick on vcm and vref.
  bypass_en    the references' own enable time (rb_en), sel 0.
usage: python3 -I explore_bypass.py bypass_s2d bypass_d2s bypass_kick bypass_en -j N
"""
import argparse
import itertools
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_rb as B  # noqa: E402

R = B.R
CAPS = ["now", "nmos", "pmos", "both", "both2"]


def cap_lines(cap):
    n = lambda k, node: f"XBX{k} 0 {node} 0 0 sg13_hv_nmos w=12u l=12u ng=1\n"
    p = lambda k, node, sup: f"XBX{k} {sup} {node} {sup} {sup} sg13_hv_pmos w=12u l=12u ng=1\n"
    return {"now": "",
            "nmos": n(1, "vcm") + n(2, "vcm") + n(3, "vref") + n(4, "vref"),
            "pmos": p(1, "vcm", "vddc") + p(2, "vcm", "vddc") + p(3, "vref", "vddr") + p(4, "vref", "vddr"),
            "both": n(1, "vcm") + p(2, "vcm", "vddc") + n(3, "vref") + p(4, "vref", "vddr"),
            "both2": n(1, "vcm") + n(2, "vcm") + p(3, "vcm", "vddc") + p(4, "vcm", "vddc")
            + n(5, "vref") + n(6, "vref") + p(7, "vref", "vddr") + p(8, "vref", "vddr")}[cap]


_blocks = B.blocks


def blocks(c, vdd_node="iovdd"):
    return _blocks(c, vdd_node) + cap_lines(c.get("cap", "now"))


B.blocks = blocks  # the decks of run_rb look blocks() up at call time

FREQS = ((1e3, "1k"), (1e5, "100k"), (1e6, "1M"), (1e7, "10M"))


def with_ac(deck, exprs):
    """replace the deck's analysis by op + AC with 1 V on every 3.3 V supply source; magnitudes at FREQS."""
    d = deck[:deck.index(".control")]
    for s in ("Vio", "Vbt", "Vbc", "Vbr"):
        d = re.sub(rf"^({s} \S+ 0 dc \S+)\s*$", r"\1 ac 1", d, flags=re.M)
    ctl, out = [".control", "op", "ac dec 20 1k 20meg"], []
    for nm, ex in exprs:
        ctl.append(f"let {nm} = {ex}")
        for f, tag in FREQS:
            ctl.append(f"meas ac {nm}_{tag} find {nm} at={f:g}")
            out.append(f"$&{nm}_{tag}")
    return d + "\n".join(ctl + ["echo RES " + " ".join(out), ".endc", ".end"]) + "\n"


def deck_s2d_ac(c):
    if c["cap"] == "ideal":
        d = R.deck_s2d_dc(dict(c, vref=c["vref_dc"], vcm=c["vcm_dc"]))
    else:
        d = B.deck_s2d_dc_rb(c).replace("Ein vsrc vref u 0 1", f"Vrefx vrefx 0 {c['vref_dc']}\nEin vsrc vrefx u 0 1")
    return with_ac(d, [("gin", "mag(v(outp) - v(outn))/2"), ("gvref", "mag(v(vref))"), ("gvcm", "mag(v(vcm))")])


def deck_d2s_ac(c):
    if c["cap"] == "ideal":
        d = R.deck_d2s_dc(dict(c, vref=c["vcm_dc"], vicm=c["vcm_dc"], vterm=c["vcm_dc"]))
        return with_ac(d, [("gout", "mag(v(pad))"), ("gvcm", "0*mag(v(pad))")])
    return with_ac(B.deck_d2s_dc_rb(c), [("gout", "mag(v(pad))"), ("gvcm", "mag(v(vcm))")])


def ac_conds():
    v = B.rb_values()
    for cap, vdd, m, t in itertools.product(["ideal"] + CAPS, [3.3], ["ss", "tt", "ff"], [27, 125]):
        vr, vc = v[(str(vdd), m, str(t), "0")]
        yield dict(cap=cap, vdd=vdd, corner_mos=m, temp=t, sel=0, vref_dc=vr, vcm_dc=vc)


def cols(names):
    return [f"{n}_{tag}" for n in names for _, tag in FREQS]


EXP = {
    "bypass_s2d": dict(what="iovdd ripple (1 V AC on every 3.3 V source) -> S2D input-referred differential output, "
                            "|vref|, |vcm|; extra bypass capacitors per variant (explore_bypass.py)", kind="dc",
                       deck=deck_s2d_ac, cols=cols(["gin", "gvref", "gvcm"]), conds=ac_conds),
    "bypass_d2s": dict(what="iovdd ripple -> D2S output (ground-referenced) and |vcm|; extra bypass capacitors per "
                            "variant", kind="dc", deck=deck_d2s_ac, cols=cols(["gout", "gvcm"]), conds=ac_conds),
    "bypass_kick": dict(what="S2D enable with the blocks (cl_s2d_en) per bypass variant", kind="dc",
                        deck=B.deck_s2d_en_rb, cols=B.EXP["cl_s2d_en"]["cols"],
                        conds=lambda: (dict(c, cap=cap) for cap in CAPS for c in B.en_conds())),
    "bypass_en": dict(what="enable of the references (rb_en, sel 0) per bypass variant", kind="dc",
                      deck=B.deck_rb_en, cols=B.EXP["rb_en"]["cols"],
                      conds=lambda: (dict(cap=cap, vdd=v, corner_mos=m, temp=27, sel=0)
                                     for cap, v, m in itertools.product(CAPS, [3.0, 3.6], ["ss", "tt", "ff"]))),
}

if __name__ == "__main__":
    R.EXPERIMENTS.update(EXP)
    ap = argparse.ArgumentParser()
    ap.add_argument("experiments", nargs="+")
    ap.add_argument("-j", type=int, default=2)
    a = ap.parse_args()
    sys.exit(1 if sum(R.experiment(e, a.j) for e in a.experiments) else 0)
