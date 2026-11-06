# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""tp_en_ctrl layout: the fail-safe enable cell (4 channels) of slot7_testplatform (netlist: ../../netlist/source/slot7_testplatform.spice).

Written 2026-11-06 (cloud session). Devices are IHP SG13_dev PCells placed in rows by pbc_row.row() (copied from
pad_buffer_cells.py). What this file adds is a small channel router:

  * every row has its gate bars on top and its tie at the bottom;  a gate channel above the row and a drain
    channel below it hold one Metal3 track per net;
  * each terminal (gate bar, S/D stripe, tie) drops on a Metal2 vertical (0.29 wide) into its own channel: gate
    bars go up, stripes and the tie go down.  So two verticals in one channel always come from the same side and
    never overlap (stripes are >= 0.83 um apart);
  * nets in more than one channel, and every external net, get a Metal4 column left of the rows, Via3 on each of
    its tracks;  external columns run down to the cell's bottom edge and carry a Metal4 pin there.
Rules (sg13cmos5l_tech_default.json): Mn 0.20 / 0.21, area 0.144;  Vn 0.19, enclosure 0.005 (0.05 endcap).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pbc_row as P                      # noqa: E402
from pbc_row import ly, LI, box, row, g5  # noqa: E402
import pya                               # noqa: E402

for k, v in {"M3": (30, 0), "M3pin": (30, 2), "M3txt": (30, 25), "Via2": (29, 0), "Via3": (49, 0),
             "M4": (50, 0), "M4pin": (50, 2), "M4txt": (50, 25)}.items():
    LI[k] = ly.layer(*v)

PITCH = 0.7          # Metal3 track pitch / Metal4 column pitch
HW = 0.145           # half width of Metal2 verticals and via landing pads
TW = 0.15            # half width of Metal3 tracks / Metal4 columns


def harvest(cell, gate_nets):
    """Pins of a pbc_row row cell -> terminals [(kind, net, x, y, (y0, y1))], then delete the pin/text shapes.
    kind: 'gate' (bar, via at the pin), 'sd' (stripe), 'tie'."""
    d = ly.dbu
    boxes = [s.dbbox() for s in cell.shapes(LI["M1pin"]).each()]
    terms = []
    for t in cell.shapes(LI["M1txt"]).each():
        p = t.dtext.trans.disp
        b = next(b for b in boxes if b.contains(pya.DPoint(p.x, p.y)))
        net = t.dtext.string
        if b.height() < 0.3 and b.width() <= 0.31 and net in gate_nets and b.bottom > 0:
            terms.append(("gate", net, b.center().x, b.center().y, (b.bottom, b.top)))
        elif b.width() >= 0.39:
            terms.append(("tie", net, b.center().x, b.center().y, (b.bottom, b.top)))
        else:
            terms.append(("sd", net.split("#")[0], b.center().x, b.center().y, (b.bottom, b.top)))
    for k in ("M1pin", "M1txt", "M2pin", "M2txt"):
        cell.shapes(LI[k]).clear()
    return terms


def mk_row(name, kind, devs, tie):
    """devs: [(label, w, l, gate, src, drn)]; stripe nets get unique aliases (no trunks inside the row)."""
    rd = []
    for i, (lab, w, l, g, s, dn) in enumerate(devs):
        sa = s if s == tie else f"{s}#{lab}s"
        da = dn if dn == tie else f"{dn}#{lab}d"
        rd.append((lab, w, l, 1, g, [sa, da]))
    c, info = row(name, kind, rd, tie)
    terms = harvest(c, {d[3] for d in devs})
    return c, info, terms


def via(c, lay, x, y):
    box(c, lay, x - 0.095, y - 0.095, x + 0.095, y + 0.095)


def build_tp_en_ctrl():
    top = ly.create_cell("tp_en_ctrl")
    # ---- rows -----------------------------------------------------------------------------------------------
    def pdevs(ks):
        d = [(f"PU{k}", 0.3, 20, "vss_3v3", "vdd_3v3", f"xb{k}") for k in ks]
        for k in ks:
            d += [(f"PA{k}", 1, 0.45, f"xb{k}", "vdd_3v3", f"en{k}"), (f"PB{k}", 1, 0.45, f"en{k}", "vdd_3v3", f"en{k}_b")]
        return d
    PR_DEVS = [(f"PR{k}", 1, 0.45, f"xb{k}", "vdd_1v2", f"rb{k}") for k in range(4)]
    N_DEVS = ([(f"NI{k}", 2, 0.45, f"en{k}_1v2", "ns1", f"xb{k}") for k in range(4)]
              + [("NE", 2, 0.45, "enable", "ns2", "ns1"), ("NV", 2, 0.45, "vdd_1v2", "vss_3v3", "ns2")]
              + [(f"NL{k}", 0.5, 0.45, "vdd_1v2", "vss_1v2", f"lo{k}") for k in range(4, 12)]
              + [("NRD", 0.3, 20, "vdd_3v3", "vss_3v3", "vdd_1v2")])
    for k in range(4):
        N_DEVS += [(f"NA{k}", 1, 0.45, f"xb{k}", "vss_3v3", f"en{k}"), (f"NR{k}", 1, 0.45, f"xb{k}", "vss_1v2", f"rb{k}"),
                   (f"NB{k}", 1, 0.45, f"en{k}", "vss_3v3", f"en{k}_b")]
    ra, _, ta = mk_row("tp_row_pa", "pmosHV", pdevs([0, 1]), "vdd_3v3")
    rb, _, tb = mk_row("tp_row_pb", "pmosHV", pdevs([2, 3]), "vdd_3v3")
    rr, _, tr = mk_row("tp_row_pr", "pmosHV", PR_DEVS, "vdd_1v2")
    rn, _, tn = mk_row("tp_row_n", "nmosHV", N_DEVS, "vss_3v3")
    # bands (top to bottom); each band: rows side by side [(cell, terms, dx)], gate channel above, drain channel below
    xr = g5(ra.dbbox().right + 3.0 + 0.62)          # read-back PMOS: own n-well (vdd_1v2), 3 um from band A's well
    bands = [[(ra, ta, 0.0), (rr, tr, xr)], [(rb, tb, 0.0)], [(rn, tn, 0.0)]]

    tracks = {}                                      # (channel, net) -> y
    placed = []                                      # (cell, terms, dx, dy, channel prefix)
    y_cursor = 0.0                                   # y of the next band's top gate track
    for bi, band in enumerate(bands):
        terms_all = [t for _, terms, _ in band for t in terms]
        gnets, dnets = [], []
        for t in terms_all:
            lst = gnets if t[0] == "gate" else dnets
            if t[1] not in lst:
                lst.append(t[1])
        top_ext = max(c.dbbox().top for c, _, _ in band)
        bot_ext = min(c.dbbox().bottom for c, _, _ in band)
        # gate tracks from y_cursor downward; the row's top sits 0.6 below the lowest gate track
        for k, n in enumerate(gnets):
            tracks[(f"g{bi}", n)] = g5(y_cursor - PITCH * (len(gnets) - 1 - k))
        y_low_gate = y_cursor - PITCH * (len(gnets) - 1)
        dy = g5(y_low_gate - 0.6 - top_ext)
        for c, terms, dx in band:
            top.insert(pya.DCellInstArray(c.cell_index(), pya.DTrans(pya.DVector(g5(dx), dy))))
            placed.append((c, terms, dx, dy, bi))
        y0 = dy + bot_ext - 0.6
        for k, n in enumerate(dnets):
            tracks[(f"d{bi}", n)] = g5(y0 - PITCH * k)
        y_cursor = y0 - PITCH * (len(dnets) - 1) - 1.5

    # ---- terminals -> Metal2 verticals -> Metal3 tracks ----------------------------------------------------------
    xs_on_track = {}
    for c, terms, dx, dy, bi in placed:
        for kind, net, x, y, (yb0, yb1) in terms:
            X, Y = g5(dx + x), g5(dy + y)
            if kind == "tie":
                X = g5(dx - 0.9)                     # tap point 0.9 um left of the row, on an M1 extension of the tie
                box(top, "M1", X - HW, dy + yb0, dx + 0.2, dy + yb1)
            ch = ("g" if kind == "gate" else "d") + str(bi)
            ty = tracks[(ch, net)]
            box(top, "M1", X - HW, Y - HW, X + HW, Y + HW)
            via(top, "Via1", X, Y)
            box(top, "M2", X - HW, min(Y, ty) - HW, X + HW, max(Y, ty) + HW)
            via(top, "Via2", X, ty)
            xs_on_track.setdefault((ch, net), []).append(X)

    # ---- Metal4 columns ---------------------------------------------------------------------------------------
    EXTERNAL = (["vdd_3v3", "vss_3v3", "vdd_1v2", "vss_1v2", "enable"] + [f"en{k}_1v2" for k in range(4)]
                + [f"en{k}{s}" for k in range(4) for s in ("", "_b")] + [f"rb{k}" for k in range(4)]
                + [f"lo{k}" for k in range(4, 12)])
    chans_of = {}
    for (ch, n) in tracks:
        chans_of.setdefault(n, []).append(ch)
    col_nets = EXTERNAL + sorted(n for n, chs in chans_of.items() if len(chs) > 1 and n not in EXTERNAL)
    for n in col_nets:
        assert n in chans_of, f"net {n} has no terminal"
    x_col0 = -2.0
    y_bottom = g5(min(tracks.values()) - 1.0)
    cols = {}
    for k, n in enumerate(col_nets):
        xc = g5(x_col0 - PITCH * k)
        cols[n] = xc
        ys = [tracks[(ch, n)] for ch in chans_of[n]]
        y_lo = y_bottom if n in EXTERNAL else min(ys)
        box(top, "M4", xc - TW, y_lo - TW, xc + TW, max(ys) + TW)
        for ch in chans_of[n]:
            xs_on_track[(ch, n)].append(xc)
            via(top, "Via3", xc, tracks[(ch, n)])
        if n in EXTERNAL:
            box(top, "M4pin", xc - TW, y_lo - TW, xc + TW, y_lo + 0.5)
            top.shapes(LI["M4txt"]).insert(pya.DText(n, xc, g5(y_lo + 0.2)))
    for (ch, n), xs in xs_on_track.items():
        y = tracks[(ch, n)]
        x0, x1 = min(xs) - 0.2, max(xs) + 0.2
        if x1 - x0 < 0.5:
            x1 = x0 + 0.5
        box(top, "M3", x0, y - TW, x1, y + TW)
    return top, cols, y_bottom


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "tp_en_ctrl.gds"
    top, cols, yb = build_tp_en_ctrl()
    # keep only tp_en_ctrl and its children
    for c in list(ly.top_cells()):
        if c.name != "tp_en_ctrl":
            ly.delete_cell_rec(c.cell_index())
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    ly.write(out, opt)
    bb = top.dbbox()
    print(f"wrote {out}: tp_en_ctrl {bb.width():.3f} x {bb.height():.3f} um, bbox {bb}")
    for n, x in cols.items():
        print(f"  column {n:10s} x={x:.3f}")
