# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""The bypass capacitors as drawn in a layout of pad_ref_rb, against the parametric bypass_rb of the source netlist
(Christoph, 2026-11-07: "The capacitor placement is pretty much ad lib (maintaining overall capacitance to the nodes and
avoiding long interconnects)"; agent F's pad_ref_rb v2 splits and reshapes them, e.g. 2 x 34.1u/16.9u on vref).
The decks of rb_z, rb_en and cl_s2d_en with pad_ref_rb.spice replaced by a copy whose bypass_rb is the drawn one.
usage: python3 -I explore_layout_caps.py <bypass_rb_drawn.spice> drawn_rb_z drawn_rb_en drawn_cl_s2d_en -j N
Results in results/drawn_*.tsv (compare with rb_z.tsv, rb_en.tsv, cl_s2d_en.tsv)."""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_rb as B  # noqa: E402

R = B.R
SRC = B.MAC / "pad_ref_rb/netlist/source/pad_ref_rb.spice"
VAR = HERE / "_runs" / "drawn_netlists"


def variant(drawn):
    """pad_ref_rb.spice with its bypass_rb subckt replaced by the one in <drawn>."""
    VAR.mkdir(parents=True, exist_ok=True)
    sub = re.search(r"^\.subckt bypass_rb .*?^\.ends bypass_rb\n", Path(drawn).read_text(), flags=re.M | re.S).group(0)
    src = SRC.read_text()
    out = re.sub(r"^\.subckt bypass_rb .*?^\.ends bypass_rb\n", lambda m: sub, src, count=1, flags=re.M | re.S)
    assert out != src
    p = VAR / "pad_ref_rb_drawn_caps.spice"
    p.write_text(out)
    return str(p)


def wrap(name, var):
    e = dict(B.EXP[name])
    deck = e["deck"]
    e["deck"] = lambda c: deck(c).replace(str(SRC), var)
    e["what"] = e["what"] + "; bypass_rb as drawn in the layout"
    return e


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("drawn")
    ap.add_argument("experiments", nargs="+")
    ap.add_argument("-j", type=int, default=2)
    a = ap.parse_args()
    var = variant(a.drawn)
    for n in ("rb_z", "rb_en", "cl_s2d_en"):
        R.EXPERIMENTS["drawn_" + n] = wrap(n, var)
    sys.exit(1 if sum(R.experiment(e, a.j) for e in a.experiments) else 0)
