# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""General version of the tp_en_ctrl router (stage B, 2026-11-06), for tp_en_ctrl_b and bias_tree_noab_pd.

tp_en_ctrl.py's build_tp_en_ctrl() is left exactly as it was (stage A's cell must stay as delivered); this module
reuses its helpers (mk_row, via, constants) and generalizes the band set-up:

    build_routed(name, bands, external)
      bands:    [[(row_name, kind, devs, tie), ...], ...]   top to bottom; rows of one band sit side by side
                devs: [(label, w, l, gate, source, drain)], all ng = 1
      external: nets that get a Metal4 column down to the cell's bottom edge with a Metal4 pin

Same scheme as tp_en_ctrl: gate bars on top of each row, tie at the bottom; per band a gate channel above and a drain
channel below with one Metal3 track per net; every terminal drops on Metal2 into its own channel; nets in more than
one channel and external nets get a Metal4 column left of the rows. Rows of one band are 3.62 um apart (separate
n-wells of different nets; NW.b1 1.8 um).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tp_en_ctrl as T                      # noqa: E402
from tp_en_ctrl import mk_row, via, PITCH, HW, TW   # noqa: E402
from pbc_row import ly, LI, box, g5         # noqa: E402
import pya                                  # noqa: E402


def build_routed(name, bands_spec, external):
    top = ly.create_cell(name)
    bands = []
    for band in bands_spec:
        placed, x = [], 0.0
        for (rname, kind, devs, tie) in band:
            c, _, terms = mk_row(rname, kind, devs, tie)
            placed.append((c, terms, g5(x)))
            x = g5(x + c.dbbox().right + 3.0 + 0.62)
        bands.append(placed)

    tracks, placed_all, y_cursor = {}, [], 0.0
    for bi, band in enumerate(bands):
        gnets, dnets = [], []
        for _, terms, _ in band:
            for t in terms:
                lst = gnets if t[0] == "gate" else dnets
                if t[1] not in lst:
                    lst.append(t[1])
        top_ext = max(c.dbbox().top for c, _, _ in band)
        bot_ext = min(c.dbbox().bottom for c, _, _ in band)
        for k, n in enumerate(gnets):
            tracks[(f"g{bi}", n)] = g5(y_cursor - PITCH * (len(gnets) - 1 - k))
        y_low_gate = y_cursor - PITCH * (len(gnets) - 1)
        dy = g5(y_low_gate - 0.6 - top_ext)
        for c, terms, dx in band:
            top.insert(pya.DCellInstArray(c.cell_index(), pya.DTrans(pya.DVector(g5(dx), dy))))
            placed_all.append((c, terms, dx, dy, bi))
        y0 = dy + bot_ext - 0.6
        for k, n in enumerate(dnets):
            tracks[(f"d{bi}", n)] = g5(y0 - PITCH * k)
        y_cursor = y0 - PITCH * (len(dnets) - 1) - 1.5

    xs_on_track = {}
    for c, terms, dx, dy, bi in placed_all:
        for kind, net, x, y, (yb0, yb1) in terms:
            X, Y = g5(dx + x), g5(dy + y)
            if kind == "tie":
                X = g5(dx - 0.9)
                # overlap the tap's own Metal1 by ~1 um (it starts 0.2 .. 0.4 um into the row, depending on the tie
                # length; ending the extension at dx + 0.2 left a 25 nm gap in tp_en_ctrl_b: M1.b)
                box(top, "M1", X - HW, dy + yb0, dx + 1.0, dy + yb1)
            ch = ("g" if kind == "gate" else "d") + str(bi)
            ty = tracks[(ch, net)]
            box(top, "M1", X - HW, Y - HW, X + HW, Y + HW)
            via(top, "Via1", X, Y)
            box(top, "M2", X - HW, min(Y, ty) - HW, X + HW, max(Y, ty) + HW)
            via(top, "Via2", X, ty)
            xs_on_track.setdefault((ch, net), []).append(X)

    chans_of = {}
    for (ch, n) in tracks:
        chans_of.setdefault(n, []).append(ch)
    col_nets = list(external) + sorted(n for n, chs in chans_of.items() if len(chs) > 1 and n not in external)
    for n in col_nets:
        assert n in chans_of, f"net {n} has no terminal"
    y_bottom = g5(min(tracks.values()) - 1.0)
    cols = {}
    for k, n in enumerate(col_nets):
        xc = g5(-2.0 - PITCH * k)
        cols[n] = xc
        ys = [tracks[(ch, n)] for ch in chans_of[n]]
        y_lo = y_bottom if n in external else min(ys)
        box(top, "M4", xc - TW, y_lo - TW, xc + TW, max(ys) + TW)
        for ch in chans_of[n]:
            xs_on_track[(ch, n)].append(xc)
            via(top, "Via3", xc, tracks[(ch, n)])
        if n in external:
            box(top, "M4pin", xc - TW, y_lo - TW, xc + TW, y_lo + 0.5)
            top.shapes(LI["M4txt"]).insert(pya.DText(n, xc, g5(y_lo + 0.2)))
    for (ch, n), xs in xs_on_track.items():
        y = tracks[(ch, n)]
        x0, x1 = min(xs) - 0.2, max(xs) + 0.2
        if x1 - x0 < 0.5:
            x1 = x0 + 0.5
        box(top, "M3", x0, y - TW, x1, y + TW)
    return top, cols, y_bottom


def tp_en_ctrl_b_spec(nch=9, per_band=3):
    bands = []
    for b0 in range(0, nch, per_band):
        ks = list(range(b0, min(nch, b0 + per_band)))
        d = [(f"PU{k}", 0.3, 20, "vss_3v3", "vdd_3v3", f"xb{k}") for k in ks]
        for k in ks:
            d += [(f"PA{k}", 1, 0.45, f"xb{k}", "vdd_3v3", f"en{k}"), (f"PB{k}", 1, 0.45, f"en{k}", "vdd_3v3", f"en{k}_b")]
        bands.append([(f"tpb_row_p{b0 // per_band}", "pmosHV", d, "vdd_3v3")])
    n = ([(f"NI{k}", 2, 0.45, f"en{k}_1v2", "ns1", f"xb{k}") for k in range(nch)]
         + [("NE", 2, 0.45, "enable", "ns2", "ns1"), ("NV", 2, 0.45, "vdd_1v2", "vss_3v3", "ns2")])
    for k in range(nch):
        n += [(f"NA{k}", 1, 0.45, f"xb{k}", "vss_3v3", f"en{k}"), (f"NB{k}", 1, 0.45, f"en{k}", "vss_3v3", f"en{k}_b")]
    bands.append([("tpb_row_n", "nmosHV", n, "vss_3v3")])
    ext = (["vdd_3v3", "vss_3v3", "vdd_1v2", "enable"] + [f"en{k}_1v2" for k in range(nch)]
           + [f"en{k}{s}" for k in range(nch) for s in ("", "_b")])
    return bands, ext


def tree_spec():
    """bias_tree_noab_pd (macros/bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice + bias_diodes)."""
    p = [("TGP", 1, 0.45, "en_3v3_b", "iref", "ni"),
         ("BP", 5, 6, "vbp", "vdd", "vbp"), ("PBN", 5, 6, "vbp", "vdd", "vbn"), ("PBNC", 2, 6, "vbp", "vdd", "vbnc"),
         ("MDBP", 2, 6, "vbp", "vdd", "vdd"), ("BPC", 1, 4, "vbpc", "vdd", "vbpc")]
    n = [("TDN", 1, 0.45, "en_3v3_b", "vss", "ni"), ("TGN", 1, 0.45, "en_3v3", "iref", "ni"),
         ("NI", 6, 6, "ni", "vss", "ni"), ("NBP", 6, 6, "ni", "vss", "vbp"), ("NBPC", 2.4, 6, "ni", "vss", "vbpc"),
         ("MDBN", 2.4, 6, "ni", "vss", "vss"), ("BN", 6, 6, "vbn", "vss", "vbn"), ("BNC", 1, 8, "vbnc", "vss", "vbnc")]
    bands = [[("tree_row_p", "pmosHV", p, "vdd")], [("tree_row_n", "nmosHV", n, "vss")]]
    ext = ["vdd", "vss", "iref", "vbp", "vbn", "vbpc", "vbnc", "en_3v3", "en_3v3_b"]
    return bands, ext


if __name__ == "__main__":
    which, out = sys.argv[1], sys.argv[2]
    bands, ext = tp_en_ctrl_b_spec() if which == "tp_en_ctrl_b" else tree_spec()
    cell, cols, yb = build_routed(which, bands, ext)
    for c in list(ly.top_cells()):
        if c.name != which:
            ly.delete_cell_rec(c.cell_index())
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    ly.write(out, opt)
    bb = cell.dbbox()
    print(f"wrote {out}: {which} {bb.width():.3f} x {bb.height():.3f} um, bbox {bb}, {len(cols)} columns")
