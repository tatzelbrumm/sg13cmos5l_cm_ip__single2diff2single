# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""generator.py: process-free generators for compact MOS layout primitives, 2026-10-28, Claude.

A pattern (score, see patterns.md) + a process adapter (one Python file per process: rules, layers, devices,
each with its source; e.g. ../ihp_sg13cmos5l/adapter.py) -> a KLayout cell and its reference-netlist lines. No rule value, layer number or device name in here:
every number comes from P.rule(<generic name>), every layer from P.layer(<generic name>), every device from
P.device(...) or a cell you pass in; the finger's own geometry (diffusion length, contact stripes, gate) is measured
from the device cell.

    import generator as G
    P = G.load_adapter("<path to adapter.py>")
    for s in G.parse_scores(open("patterns.md").read()):
        cell, devices, info = G.build(ly, P, s)

Generators
  mirror_stack  rows of R270 fingers; drains into Metal2 track bands between row pairs, sources on Metal1 plates,
                gate contact column along each row end, Metal2 staircase joining two bands; tap-less, one well
                polygon (device wells + well enclosure of the diffusion, 45-degree corners where the adapter allows,
                notches below the same-net well space filled)
  cascode_stack mirror rows + cascode rows of equal fingers (L short): each cascode row carries the letters of the
                mirror row it faces, so drain / source meet in one Metal1 joint across a diff_space gap; tracks run
                over each row's own channel; gate pads at both row ends; Metal1 lines at the sides join the rows
  series_row    n fingers R270 in one row, merged gate strip, Metal1 meander puts them in series
  switch_cell   one finger, gate contact beside the channel, pins on three edges
  tap_path      a one-contact-column well tap along any rectilinear path, for the PARENT's merged-well periphery
  cdl           .SUBCKT text from the device lists
Coordinates are integers in database units (1 nm).
"""
import importlib.util
import math
import re
import klayout.db as db

DBU = 0.001


def load_adapter(path):
    """import a process adapter file (module with rule(), src(), layer(), device(), model(), RULES, LAYERS)"""
    spec = importlib.util.spec_from_file_location("process_adapter", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def min_contact_width(P):
    """narrowest finger that still carries one S/D contact: 2 diff_encl_contact + contact_size"""
    return 2 * P.rule("diff_encl_contact") + P.rule("contact_size")


def U(v):
    return int(round(v / DBU))


class Ctx:
    """layout + adapter helpers"""
    def __init__(self, ly, P):
        self.ly, self.P = ly, P
        self.g = U(P.rule("grid"))

    def r(self, name):
        return U(self.P.rule(name))

    def li(self, name):
        return self.ly.layer(*self.P.layer(name))

    def box(self, cell, k, x1, y1, x2, y2):
        cell.shapes(self.li(k)).insert(db.Box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

    def text(self, cell, k, s, x, y):
        cell.shapes(self.li(k)).insert(db.Text(s, db.Trans(db.Point(x, y))))

    def pin(self, cell, metal, net, x1, y1, x2, y2):
        """<metal>_pin box + <metal>_text at its centre"""
        self.box(cell, metal + "_pin", x1, y1, x2, y2)
        self.text(cell, metal + "_text", net, (x1 + x2) // 2, (y1 + y2) // 2)

    def via1(self, cell, xc, yc):
        h = self.r("via1_size") // 2
        self.box(cell, "via1", xc - h, yc - h, xc + h, yc + h)

    def snap(self, v):
        return int(round(v / self.g)) * self.g


def finger_geom(C, dev):
    """measure a device cell (frame: x along L, y along W): diffusion length / width, the S/D Metal1 column next to the
    x = 0 end, the gate's x range"""
    own = lambda k: db.Region(dev.shapes(C.li(k))).merged()
    diff = own("diff").bbox()
    poly = (own("poly") & own("diff")).bbox()
    m1 = min((p.bbox() for p in own("m1").each()), key=lambda b: b.left)
    return dict(La=diff.width(), W=diff.height(), sd=(m1.left - diff.left, m1.right - diff.left),
                gate=(poly.left - diff.left, poly.right - diff.left))


def place_r270(cell, dev, fg, x, y, n=1, pitch=0):
    """R270 turns the finger's L axis vertical with upright PCell texts; (x, y) = lower left diffusion corner"""
    t = db.Trans(db.Trans.R270, db.Vector(x, y + fg["La"]))
    if n > 1:
        cell.insert(db.CellInstArray(dev.cell_index(), t, db.Vector(pitch, 0), db.Vector(0, 0), n, 1))
    else:
        cell.insert(db.CellInstArray(dev.cell_index(), t))


def well_polygon(C, cell, extra=()):
    """the cell's one well: device wells + well_encl_pdiff around all diffusion under the well (45-degree corners
    if P.WELL_45: KLayout sizing mode 1 puts the chamfer tangent at the enclosure distance; one grid added, then
    snapped), gaps / notches below well_space_same closed. Same polygon on hvox if P.HVOX_LIKE_WELL."""
    P = C.P
    rec = lambda k: db.Region(cell.begin_shapes_rec(C.li(k))).merged()
    w = rec("well")
    enc = C.r("well_encl_pdiff")
    diff_in = rec("diff") & w
    grown = diff_in.sized(enc, enc, 5)                         # straight edges exactly at the enclosure
    if getattr(P, "WELL_45", False):                           # corners: 45-degree chamfer, one grid outside
        grown &= diff_in.sized(enc + C.g, enc + C.g, 1)
    for x in extra:
        grown += x
    w = (w + grown).merged()
    h = (C.r("well_space_same") + 1) // 2
    w = w.sized(h, h, 5).sized(-h, -h, 5).merged()             # close gaps < well_space_same (same net)
    w = w.snapped(C.g, C.g)
    cell.shapes(C.li("well")).insert(w)
    if getattr(P, "HVOX_LIKE_WELL", False):
        cell.shapes(C.li("hvox")).insert(w)
    return w


# --------------------------------------------------------------------------------------------- patterns
def parse_scores(text):
    """read the ```score blocks of patterns.md -> list of dicts (notation: patterns.md)"""
    out = []
    for blk in re.findall(r"```score\n(.*?)```", text, re.S):
        s = None
        for raw in blk.splitlines():
            line = raw.split("#")[0].strip()
            if not line:
                continue
            w0 = line.split()[0]
            if w0 in ("stack", "cstack", "chain", "single"):
                s = dict(kind=w0, name=line.split()[1], rows=[], voices={}, sym=None)
                out.append(s)
            elif line.startswith("|"):
                s["rows"].append(line.strip("|").split())
            elif w0 == "voice":
                t = line.split()
                v = dict(name=t[2], kind=t[3], w=t[4] if t[4] == "min" else float(t[4]), l=float(t[5]), d=None)
                for kv in t[6:]:
                    k, val = kv.split("=")
                    v["d" if k == "drain" else k] = None if val == "rest" else val
                s["voices"][t[1]] = v
            elif w0 == "symmetry":
                t = line.split()
                s["sym"] = dict(op=t[1], swap=dict(zip(t[3::2], t[4::2])) if len(t) > 2 else {})
            elif w0 == "links":
                s["links"] = line.split()[1:]
            elif w0 == "end":
                s = None
            else:
                for part in line.split(";"):
                    t = part.split()
                    if t:
                        s[t[0]] = t[1:] if len(t) > 2 else (t[1] if len(t) == 2 else True)
    return out


def point_image(rows, swap=None):
    """retrograde inversion (R180) of a letter matrix; swap: letters exchanged by the image"""
    sw = dict(swap or {})
    sw.update({v: k for k, v in list(sw.items())})
    return [[sw.get(t, t) for t in reversed(r)] for r in reversed(rows)]


def build(ly, P, s, cells=None):
    """score dict -> (cell, devices, info). cells: optional {letter: existing device cell} (e.g. library PCells);
    other letters get P.device(ly, kind, w, l)."""
    cells = dict(cells or {})
    made = {}
    for v in s["voices"].values():
        if v["w"] == "min":                                    # 'min' = one S/D contact wide (the rest's width)
            v["w"] = round(min_contact_width(P), 6)
    for k, v in s["voices"].items():
        if k not in cells:
            key = (v["kind"], v["w"], v["l"])
            if key not in made:
                made[key] = P.device(ly, v["kind"], v["w"], v["l"])
            cells[k] = made[key]
    if s["kind"] == "stack":
        if s.get("sym"):
            assert point_image(s["rows"], s["sym"]["swap"]) == s["rows"], "score is not point-symmetric"
        letters = {k: dict(cell=cells[k], w=v["w"], l=v["l"], d=v["d"], name=v["name"], tag=v["name"], kind=v["kind"])
                   for k, v in s["voices"].items()}
        return mirror_stack(ly, P, s["name"], s["rows"], letters, s["src"], s["gate"], s["tracks"],
                            int(s.get("pin_band", -1)), bulk=s.get("bulk", s["src"]))
    if s["kind"] == "cstack":
        if s.get("sym"):
            assert point_image(s["rows"], s["sym"]["swap"]) == s["rows"], "score is not point-symmetric"
        letters = {k: dict(cell=cells[k], w=v["w"], l=v["l"], d=v["d"], cd=v.get("cdrain"), name=v["name"],
                           cname=v.get("cname", v["name"] + "C"), kind=v["kind"]) for k, v in s["voices"].items()}
        lst = lambda x: x if isinstance(x, list) else [x]
        pins = dict(p.split(":") for p in lst(s.get("pins", [])))
        return cascode_stack(ly, P, s["name"], s["rows"], letters, s["src"], s["gate"], s["cgate"], lst(s["mtracks"]),
                             lst(s["ctracks"]), lst(s.get("lines_left", [])), lst(s.get("lines_right", [])), pins,
                             bulk=s.get("bulk", s["src"]))
    (k, v), = s["voices"].items()
    if s["kind"] == "chain":
        return series_row(ly, P, s["name"], cells[k], len(s["rows"][0]), v["w"], v["l"], s["src"], s["end"],
                          s["gate"], s.get("inner", "n%d"), s.get("bulk", s["src"]), v["name"], P.model(v["kind"]),
                          gate_pin=s.get("gate_pin", "L"), end_pin=s.get("end_pin", "T"))
    return switch_cell(ly, P, s["name"], cells[k], v["w"], v["l"], s["s"], s["d"], s["g"], s.get("bulk", s["s"]),
                       v["name"], P.model(v["kind"]))


# --------------------------------------------------------------------------------------------- mirror stack
def mirror_stack(ly, P, name, rows, letters, src, gate, tracks, pin_band=-1, bulk=None):
    """Rows of R270 fingers, top row first. Rows pair up around Metal2 track bands (even row: drain at the bottom,
    odd row: drain at the top); pairs share source plates (diff_space apart). No well tap: one well polygon to the
    cell edge (well_polygon), the parent taps the merged well at its periphery (tap_path).
      letters: {letter: dict(cell, w, l, d=drain net or None (dummy: D = S, strapped in Metal1 on its contact
               column), name, tag, kind)}
      src: source net (plates, dummies); gate: gate net = the outermost track (the gate columns reach it)
      tracks: band nets from the block's centre line outwards (above the centre: bottom to top; below: top to
              bottom = the point image)
      pin_band: band whose tracks end on the right cell edge as Metal2 pins (-1 = lowest)
      bulk: netlist name of the well (internal net when tap-less)
    Supply path: outer plates (to the top / bottom cell edge) - straps over the end-column dummies - Metal1 through
    the bands in those columns - inner plates. Gate: one Metal1 column along each side, Via1 onto the gate track of
    every band. Two bands: Metal2 staircase on the left joins the non-gate tracks (outermost net = outermost line).
    Returns (cell, devices, info), devices = [(name, d, g, s, b, w, l, model)]."""
    C = Ctx(ly, P)
    bulk = bulk or src
    nr = len(rows)
    assert nr % 2 == 0, "rows pair up around bands"
    assert tracks[-1] == gate, "gate track outermost"
    r = C.r
    cs, m1b = r("contact_size"), r("m1_space")
    v1, v1b, v1c, v1c1 = r("via1_size"), r("via1_space"), r("m1_encl_via1"), r("m1_endcap_via1")
    m2c1 = r("m2_endcap_via1")
    tw = max(r("m2_width"), v1 + 2 * r("m2_encl_via1"))   # Metal2 track width
    tp = r("m2_width") + r("m2_space")                   # Metal2 track pitch
    gap = r("finger_gap")
    pgap = r("diff_space")
    nt = len(tracks)
    geo = {k: finger_geom(C, v["cell"]) for k, v in letters.items()}
    Las = set(g["La"] for g in geo.values())
    assert len(Las) == 1, "one finger length per stack"
    La = Las.pop()
    g0 = next(iter(geo.values()))
    sd_out, sd_in = g0["sd"]                             # S/D Metal1 stripe from the diffusion end
    gate_y0 = g0["gate"][0]                              # gate edge from the diffusion end
    tab_reach = v1 // 2 + v1c                            # tab end past the track centre (endcap along the tab)
    edge_c = m1b - sd_out + tab_reach                    # first / last track centre from the diffusion edges
    gband = 2 * edge_c + (nt - 1) * tp
    tabw = 2 * v1 + v1b + 2 * v1c1                       # two Via1 per tab
    gcol_in = m1b                                        # gate Metal1 column: m1_space from the finger's S/D Metal1
    gcol_w = v1 + 2 * v1c
    cnt_x = gcol_in + (gcol_w - cs) // 2
    assert cnt_x >= r("poly_contact_to_diff")
    tab_out = cnt_x + cs + r("poly_encl_contact")
    m1_end = sd_in + m1b                                 # gate column end from the diffusion end (plates)

    cols = [geo[t]["W"] for t in rows[0]]
    for row in rows:
        assert [geo[t]["W"] for t in row] == cols, "rows must have the same column widths"
    xs = [0]
    for wv in cols[:-1]:
        xs.append(xs[-1] + wv + gap)
    xend = xs[-1] + cols[-1]
    ybot = [0] * nr
    y = 0
    for i in range(nr - 1, -1, -1):
        ybot[i] = y
        y += La
        if i > 0:
            y += gband if (i % 2 == 1) else pgap
    ytop = [yb + La for yb in ybot]
    bands = [(i, i + 1, ytop[i + 1]) for i in range(0, nr, 2)]
    ctr_y = (ybot[nr - 1] + ytop[0]) // 2
    nw = max(r("well_encl_pdiff"), tab_out)
    xl, xr, yb, yt = -nw, xend + nw, ybot[nr - 1] - r("well_encl_pdiff"), ytop[0] + r("well_encl_pdiff")

    c = ly.create_cell(name)
    devices = []
    for i, row in enumerate(rows):                       # fingers: runs of one cell = one AREF (translation)
        j = 0
        while j < len(row):
            k = j
            while k + 1 < len(row) and letters[row[k + 1]]["cell"] is letters[row[j]]["cell"]:
                k += 1
            place_r270(c, letters[row[j]]["cell"], geo[row[j]], xs[j], ybot[i], k - j + 1, cols[j] + gap)
            j = k + 1
        for j, t in enumerate(row):
            lt = letters[t]
            C.text(c, "text", lt.get("tag", t), xs[j] + cols[j] // 2, (ybot[i] + ytop[i]) // 2)
            d = lt["d"] if lt["d"] is not None else src
            devices.append(("%s_r%d_%s_%d" % (name, i + 1, lt["name"], j), d, gate, src, bulk, lt["w"], lt["l"],
                            P.model(lt["kind"])))
    tr_y = {}
    for b, (iu, il, y0) in enumerate(bands):
        above = (y0 + gband // 2) > ctr_y
        order = list(tracks) if (above or len(bands) == 1) else list(reversed(tracks))
        for k, net in enumerate(order):
            tr_y[(b, net)] = y0 + edge_c + k * tp
    vias_x = {}
    for b, (iu, il, y0) in enumerate(bands):             # drain tabs: lower row left edge, upper row right edge
        for i, side in ((il, "lo"), (iu, "hi")):
            for j, t in enumerate(rows[i]):
                lt = letters[t]
                if lt["d"] is None:
                    continue
                assert cols[j] >= 2 * tabw + m1b, "finger too narrow for two tabs"
                yc = tr_y[(b, lt["d"])]
                if side == "lo":
                    x1 = xs[j]
                    C.box(c, "m1", x1, ytop[i] - sd_in, x1 + tabw, yc + tab_reach)
                else:
                    x1 = xs[j] + cols[j] - tabw
                    C.box(c, "m1", x1, yc - tab_reach, x1 + tabw, ybot[i] + sd_in)
                for vx in (x1 + v1c1 + v1 // 2, x1 + v1c1 + v1 + v1b + v1 // 2):
                    C.via1(c, vx, yc)
                    vias_x.setdefault((b, lt["d"]), []).append(vx)
    strap = {}                                           # dummies: D = S over the channel; end columns joined
    for i, row in enumerate(rows):
        for j, t in enumerate(row):
            if letters[t]["d"] is None:
                sw = min(cols[j], tabw)
                sx = xs[j] + (cols[j] - sw) // 2
                strap[(i, j)] = (sx, sx + sw)
                C.box(c, "m1", sx, ybot[i] + sd_out, sx + sw, ytop[i] - sd_out)
    for b, (iu, il, y0) in enumerate(bands):
        for j in range(len(cols)):
            if (iu, j) in strap and (il, j) in strap and strap[(iu, j)] == strap[(il, j)]:
                sx = strap[(iu, j)]
                C.box(c, "m1", sx[0], ytop[il] - sd_out, sx[1], ybot[iu] + sd_out)
    C.box(c, "m1", xl, yb, xr, ybot[nr - 1] + sd_in)     # source plates
    C.box(c, "m1", xl, ytop[0] - sd_in, xr, yt)
    for i in range(1, nr - 1, 2):
        C.box(c, "m1", 0, ybot[i] + sd_in, xend, ytop[i + 1] - sd_in)
    pitch_c = cs + r("contact_space")
    for side in (-1, 1):                                 # row ends: poly tab, contacts, one gate column per side
        ref = 0 if side < 0 else xend
        X = lambda a, b_: (min(ref + side * a, ref + side * b_), max(ref + side * a, ref + side * b_))
        for i in range(nr):
            px = X(0, tab_out)
            C.box(c, "poly", px[0], ybot[i] + gate_y0, px[1], ytop[i] - gate_y0)
            cy0, cy1 = ybot[i] + m1_end + r("m1_endcap_contact"), ytop[i] - m1_end - r("m1_endcap_contact")
            n = (cy1 - cy0 + r("contact_space")) // pitch_c
            y = C.snap(cy0 + ((cy1 - cy0) - (n * cs + (n - 1) * r("contact_space"))) // 2)
            cx = X(cnt_x, cnt_x + cs)
            for _ in range(n):
                C.box(c, "contact", cx[0], y, cx[1], y + cs)
                y += pitch_c
        gx = X(gcol_in, gcol_in + gcol_w)
        C.box(c, "m1", gx[0], ybot[nr - 1] + m1_end, gx[1], ytop[0] - m1_end)
        for b in range(len(bands)):
            vx = (gx[0] + gx[1]) // 2
            C.via1(c, vx, tr_y[(b, gate)])
            vias_x.setdefault((b, gate), []).append(vx)
    pb = pin_band % len(bands)                           # Metal2 tracks and staircase
    stair = [n_ for n_ in tracks if n_ != gate] if len(bands) > 1 else []
    line_x = {n_: xl + (len(stair) - 1 - k) * tp for k, n_ in enumerate(stair)}
    pin_len = 2 * r("m2_width")
    for b in range(len(bands)):
        for net in tracks:
            yc = tr_y[(b, net)]
            vx = vias_x.get((b, net), [])
            x_left = line_x[net] if net in line_x else min(vx) - v1 // 2 - m2c1
            x_right = xr if b == pb else max(vx) + v1 // 2 + m2c1
            C.box(c, "m2", x_left, yc - tw // 2, x_right, yc + tw // 2)
            if b == pb:
                C.pin(c, "m2", net, xr - pin_len, yc - tw // 2, xr, yc + tw // 2)
    if stair:
        assert len(bands) == 2, "staircase drawn for two bands"
        assert len(xs) < 2 or line_x[stair[0]] + tw + r("m2_space") <= xs[1] + 2 * r("m2_space")
        for net in stair:
            ys_ = sorted(tr_y[(b, net)] for b in range(2))
            C.box(c, "m2", line_x[net], ys_[0] - tw // 2, line_x[net] + tw, ys_[1] + tw // 2)
    C.pin(c, "m1", src, (xl + xr) // 2 - pin_len, yb, (xl + xr) // 2 + pin_len, yb + 2 * r("m1_width"))
    well = well_polygon(C, c, [db.Region(db.Box(xl, yb, xr, yt))])
    info = dict(xs=xs, cols=cols, ybot=ybot, ytop=ytop, xend=xend, bbox=(xl, yb, xr, yt), gband=gband,
                tracks=tr_y, lines=line_x, well=well, rowend=(gcol_in, gcol_w, cnt_x, tab_out))
    return c, devices, info


# --------------------------------------------------------------------------------------------- cascode stack
def cascode_stack(ly, P, name, mrows, letters, src, gate, cgate, mtracks, ctracks, lines_left, lines_right,
                  pins=None, bulk=None):
    """Mirror rows + cascode rows of R270 fingers, top mirror row first. Every two mirror rows (Ma, Mb) form a group
    [Ma, Ca, Cb, Mb]: the cascode row Ca (Cb) carries the letters of Ma (Mb), so a mirror drain and its cascode's
    source are the same net in every column and meet in one Metal1 joint across a diff_space gap. Ca / Cb face
    each other with their drains; Mb of one group and Ma of the next share a source plate. All row gaps are
    diff_space; outer source plates run to the top / bottom cell edge.
      letters: {letter: dict(cell, w, l, d = mirror drain net (None: rest), cd = cascode drain net, name, cname, kind)}
      mtracks / ctracks: Metal2 tracks over every mirror / cascode row's own channel, from its drain side; the
               row's gate net must be the one whose via fits the gate pad (checked)
      lines_left / lines_right: nets of the Metal1 lines along the sides, inner to outer; each joins that net's
               tracks of all rows (Via1)
      pins: {net: 'T' | 'B' | 'L' | 'R'}: line end on the top / bottom edge, or the outermost line at the side edge;
            src: top / bottom plate
    Every real finger gets the same 3-Via1 tab (centred, from its drain stripe to the far track; m1_wide_space to
    the opposite stripe); the via sits on its own net's track. Rests: D = S = src, strapped; their column is the
    src spine through all rows. Gate pads (poly tab + contacts + Metal1) at both ends of every row, Via1 onto the
    row's gate track. Tap-less; one well polygon to the cell edge.
    Returns (cell, devices, info), devices = [(name, d, g, s, b, w, l, model)]."""
    C = Ctx(ly, P)
    bulk = bulk or src
    pins = pins or {}
    assert len(mrows) % 2 == 0
    r = C.r
    cs, m1b = r("contact_size"), r("m1_space")
    v1, v1b, v1c, v1c1 = r("via1_size"), r("via1_space"), r("m1_encl_via1"), r("m1_endcap_via1")
    tw = max(r("m2_width"), v1 + 2 * r("m2_encl_via1"))
    tp = r("m2_width") + r("m2_space")
    gap, rgap = r("finger_gap"), r("diff_space")
    geo = {k: finger_geom(C, v["cell"]) for k, v in letters.items()}
    Las = set(g_["La"] for g_ in geo.values())
    assert len(Las) == 1, "one finger length per stack"
    La = Las.pop()
    g0 = next(iter(geo.values()))
    sd_out, sd_in = g0["sd"]
    gate_y0 = g0["gate"][0]
    tab_reach = v1 // 2 + v1c
    tab3 = 3 * v1 + 2 * v1b + 2 * v1c1
    wide = tab3 > r("m1_wide_width") and tab3 > r("m1_wide_run")
    clr = r("m1_wide_space") if wide else m1b                # the tab end to the opposite (plate) stripe
    nt = max(len(mtracks), len(ctracks))
    far = La - sd_in - clr - tab_reach                       # far track centre from the drain-side diffusion edge
    off = [far - (nt - 1 - k) * tp for k in range(nt)]
    assert off[0] - tab_reach >= sd_out, "tracks do not fit over the channel"
    gcol_in, gcol_w = m1b, v1 + 2 * v1c
    cnt_x = gcol_in + (gcol_w - cs) // 2
    assert cnt_x >= r("poly_contact_to_diff")
    tab_out = cnt_x + cs + r("poly_encl_contact")
    m1_end = sd_in + m1b
    vlo, vhi = m1_end + v1 // 2 + r("m1_endcap_via1"), La - m1_end - v1 // 2 - r("m1_endcap_via1")
    for trk, gn in ((mtracks, gate), (ctracks, cgate)):
        o = off[trk.index(gn)]
        assert vlo <= o <= vhi, "gate track %s must lie on the gate pad (%d..%d)" % (gn, vlo, vhi)
    lw = gcol_w
    lgap = max(m1b, v1b - 2 * v1c)                       # vias on neighbouring lines / pad may share a track
    line_x = lambda k: gcol_in + gcol_w + lgap + k * (lw + lgap)    # inner edge, outward from the end finger
    nl = max(len(lines_left), len(lines_right))
    side = max(r("well_encl_pdiff"), tab_out,
               (line_x(nl - 1) + lw // 2 + v1 // 2 + r("m2_endcap_via1")) if nl else 0)   # track endcap at the edge

    rows = []
    for gi in range(0, len(mrows), 2):
        ma, mb = mrows[gi], mrows[gi + 1]
        rows += [("M", ma, "bot"), ("C", ma, "bot"), ("C", mb, "top"), ("M", mb, "top")]
    nr = len(rows)
    cols = [geo[t]["W"] for t in rows[0][1]]
    for _, row, _ in rows:
        assert [geo[t]["W"] for t in row] == cols, "rows must have the same column widths"
    xs = [0]
    for wv in cols[:-1]:
        xs.append(xs[-1] + wv + gap)
    xend = xs[-1] + cols[-1]
    ybot, y = [0] * nr, 0
    for i in range(nr - 1, -1, -1):
        ybot[i] = y
        y += La + rgap
    ytop = [b_ + La for b_ in ybot]
    nw = r("well_encl_pdiff")
    xl, xr, yb, yt = -side, xend + side, ybot[-1] - nw, ytop[0] + nw

    c = ly.create_cell(name)
    devices = []
    for i, (kind, row, dside) in enumerate(rows):
        j = 0
        while j < len(row):
            k = j
            while k + 1 < len(row) and letters[row[k + 1]]["cell"] is letters[row[j]]["cell"]:
                k += 1
            place_r270(c, letters[row[j]]["cell"], geo[row[j]], xs[j], ybot[i], k - j + 1, cols[j] + gap)
            j = k + 1
        for j, t in enumerate(row):
            lt = letters[t]
            rest = lt["d"] is None
            tag = lt["name"] if (kind == "M" or rest) else lt["cname"]
            C.text(c, "text", tag, xs[j] + cols[j] // 2, (ybot[i] + ytop[i]) // 2)
            if kind == "M":
                dv = (lt["d"] if not rest else src, gate, src)
            else:
                dv = (lt["cd"] if not rest else src, cgate, lt["d"] if not rest else src)
            devices.append(("%s_r%d_%s_%d" % (name, i + 1, tag, j), dv[0], dv[1], dv[2], bulk, lt["w"], lt["l"],
                            P.model(lt["kind"])))
    # tracks (Metal2, full width) and their y per row
    ty = {}
    for i, (kind, row, dside) in enumerate(rows):
        trk = mtracks if kind == "M" else ctracks
        for k, net in enumerate(trk):
            yc = ybot[i] + off[k] if dside == "bot" else ytop[i] - off[k]
            ty[(i, net)] = yc
            C.box(c, "m2", xl, yc - tw // 2, xr, yc + tw // 2)
    # tabs: identical on every real finger, vias on its own net's track
    for i, (kind, row, dside) in enumerate(rows):
        for j, t in enumerate(row):
            lt = letters[t]
            if lt["d"] is None:
                continue
            net = lt["d"] if kind == "M" else lt["cd"]
            x1 = C.snap(xs[j] + (cols[j] - tab3) // 2)
            if dside == "bot":
                C.box(c, "m1", x1, ybot[i] + sd_out, x1 + tab3, ybot[i] + far + tab_reach)
            else:
                C.box(c, "m1", x1, ytop[i] - far - tab_reach, x1 + tab3, ytop[i] - sd_out)
            for q in range(3):
                C.via1(c, x1 + v1c1 + v1 // 2 + q * (v1 + v1b), ty[(i, net)])
    # joints (mirror drain = cascode source, full column width), rest straps and the rest spine
    for i in range(nr - 1):
        up, lo = rows[i], rows[i + 1]
        mc = (up[0] == "M" and lo[0] == "C") or (up[0] == "C" and lo[0] == "M")
        for j, t in enumerate(up[1]):
            rest = letters[t]["d"] is None
            if mc or (rest and letters[lo[1][j]]["d"] is None):
                C.box(c, "m1", xs[j], ytop[i + 1] - (sd_in if mc else sd_out), xs[j] + cols[j],
                      ybot[i] + (sd_in if mc else sd_out))
    for i, (kind, row, dside) in enumerate(rows):
        for j, t in enumerate(row):
            if letters[t]["d"] is None:
                C.box(c, "m1", xs[j], ybot[i] + sd_out, xs[j] + cols[j], ytop[i] - sd_out)
    # source plates: top / bottom to the cell edge, inner ones between Mb and the next Ma
    C.box(c, "m1", 0, ytop[0] - sd_in, xend, yt)
    C.box(c, "m1", 0, yb, xend, ybot[-1] + sd_in)
    for i in range(3, nr - 1, 4):
        C.box(c, "m1", 0, ytop[i + 1] - sd_in, xend, ybot[i] + sd_in)
    # row ends: poly tab, contacts, gate pad with Via1 onto the row's gate track; both ends of every row
    pc = cs + r("contact_space")
    for sgn in (-1, 1):
        ref = 0 if sgn < 0 else xend
        X = lambda a, b_: (min(ref + sgn * a, ref + sgn * b_), max(ref + sgn * a, ref + sgn * b_))
        for i, (kind, row, dside) in enumerate(rows):
            px = X(0, tab_out)
            C.box(c, "poly", px[0], ybot[i] + gate_y0, px[1], ytop[i] - gate_y0)
            cy0, cy1 = ybot[i] + m1_end + r("m1_endcap_contact"), ytop[i] - m1_end - r("m1_endcap_contact")
            n = (cy1 - cy0 + r("contact_space")) // pc
            yy = C.snap(cy0 + ((cy1 - cy0) - (n * cs + (n - 1) * r("contact_space"))) // 2)
            cx = X(cnt_x, cnt_x + cs)
            for _ in range(n):
                C.box(c, "contact", cx[0], yy, cx[1], yy + cs)
                yy += pc
            gx = X(gcol_in, gcol_in + gcol_w)
            C.box(c, "m1", gx[0], ybot[i] + m1_end, gx[1], ytop[i] - m1_end)
            C.via1(c, (gx[0] + gx[1]) // 2, ty[(i, gate if kind == "M" else cgate)])
        # side lines (Metal1, full height), Via1 from every row's track of that net
        for k, net in enumerate(lines_left if sgn < 0 else lines_right):
            lx = X(line_x(k), line_x(k) + lw)
            C.box(c, "m1", lx[0], yb, lx[1], yt)
            for (i, nn), yc in ty.items():
                if nn == net:
                    C.via1(c, (lx[0] + lx[1]) // 2, yc)
            e = pins.get(net)
            ph = 2 * r("m1_width")
            if e == "T":
                C.pin(c, "m1", net, lx[0], yt - ph, lx[1], yt)
            elif e == "B":
                C.pin(c, "m1", net, lx[0], yb, lx[1], yb + ph)
            elif e in ("L", "R"):
                assert k == len(lines_left if sgn < 0 else lines_right) - 1, "side pin needs the outermost line"
                ym = C.snap((yb + yt) // 2)
                ex = (xl, lx[1]) if sgn < 0 else (lx[0], xr)          # Metal1 out to the cell edge
                C.box(c, "m1", ex[0], ym - ph, ex[1], ym + ph)
                C.pin(c, "m1", net, ex[0], ym - ph, ex[1], ym + ph)
    ph = 2 * r("m1_width")
    if pins.get(src, "T") == "T":
        C.pin(c, "m1", src, xend // 2 - ph, yt - ph, xend // 2 + ph, yt)
    else:
        C.pin(c, "m1", src, xend // 2 - ph, yb, xend // 2 + ph, yb + ph)
    well = well_polygon(C, c, [db.Region(db.Box(xl, yb, xr, yt))])
    info = dict(xs=xs, cols=cols, ybot=ybot, ytop=ytop, xend=xend, bbox=(xl, yb, xr, yt), rows=rows, tracks=ty,
                off=off, well=well)
    return c, devices, info


# --------------------------------------------------------------------------------------------- series row
def series_row(ly, P, name, dev, n, w, l, start, end, gate, inner="n%d", bulk=None, label="S", model="",
               gate_pin="L", end_pin="T"):
    """n fingers R270 at pitch W + finger_gap (merged gate strip), in series by a Metal1 meander: start at finger 0
    top, links alternate bottom / top (hocket), end at finger n-1. Gate contact column at the left end. Tap-less.
    gate_pin: 'L' = pin on the left edge; 'B' = the gate column moves out to m1_space from finger 0's stripes and
    runs down to the bottom edge. end_pin: 'T' = on the top edge above finger n-1 (n even); 'B' = to the bottom
    edge (n odd: straight down; n even: along a Metal1 line m1_space right of finger n-1, inside the well margin)."""
    C = Ctx(ly, P)
    bulk = bulk or start
    r = C.r
    cs, m1b = r("contact_size"), r("m1_space")
    fg = finger_geom(C, dev)
    W, La = fg["W"], fg["La"]
    sd = fg["sd"]
    pitch = W + r("finger_gap")
    nw = r("well_encl_pdiff")
    c = ly.create_cell(name)
    place_r270(c, dev, fg, 0, 0, n, pitch)
    xend = (n - 1) * pitch + W
    nets = [start] + [inner % (k + 1) for k in range(n - 1)] + [end]
    devices = []
    for k in range(n):
        devices.append(("%s_%s_%d" % (name, label, k), nets[k + 1], gate, nets[k], bulk, w, l, model))
        C.text(c, "text", "%s_%d" % (label, k), k * pitch + W // 2, La // 2)
    for k in range(n - 1):
        x1, x2 = k * pitch, (k + 1) * pitch + W
        if k % 2 == 0:
            C.box(c, "m1", x1, sd[0], x2, sd[1])
        else:
            C.box(c, "m1", x1, La - sd[1], x2, La - sd[0])
    pin_h = 2 * r("m1_width")
    C.box(c, "m1", 0, La - sd[1], W, La + nw)
    C.pin(c, "m1", start, 0, La + nw - pin_h, W, La + nw)
    xe = (n - 1) * pitch
    lw = r("via1_size") + 2 * r("m1_encl_via1")
    if n % 2 == 0 and end_pin == "T":
        C.box(c, "m1", xe, La - sd[1], xe + W, La + nw)
        C.pin(c, "m1", end, xe, La + nw - pin_h, xe + W, La + nw)
    elif n % 2 == 0:                                      # top terminal of the last finger down the right side
        xl_ = xend + m1b
        assert xl_ + lw <= xend + nw, "end line does not fit the well margin"
        C.box(c, "m1", xe, La - sd[1], xl_ + lw, La - sd[0])
        C.box(c, "m1", xl_, -nw, xl_ + lw, La - sd[0])
        C.pin(c, "m1", end, xl_, -nw, xl_ + lw, -nw + pin_h)
    else:
        C.box(c, "m1", xe, -nw, xe + W, sd[1])
        C.pin(c, "m1", end, xe, -nw, xe + W, -nw + pin_h)
    gy0 = fg["gate"][0]
    cx1 = -r("poly_contact_to_diff") - cs
    if gate_pin == "B":                                   # column m1_space from finger 0's stripes, to the bottom
        gx1 = -m1b - lw
        cx1 = gx1 + (lw - cs) // 2
        C.box(c, "poly", cx1 - r("poly_encl_contact"), gy0, 0, La - gy0)
        y0, y1 = sd[1] + m1b + r("m1_endcap_contact"), La - sd[1] - m1b - r("m1_endcap_contact")
        pc = cs + r("contact_space")
        k = (y1 - y0 + r("contact_space")) // pc
        y = C.snap(y0 + ((y1 - y0) - (k * cs + (k - 1) * r("contact_space"))) // 2)
        for _ in range(k):
            C.box(c, "contact", cx1, y, cx1 + cs, y + cs)
            y += pc
        C.box(c, "m1", gx1, -nw, gx1 + lw, La - sd[1] - m1b)
        C.pin(c, "m1", gate, gx1, -nw, gx1 + lw, -nw + pin_h)
        assert cx1 - r("poly_encl_contact") >= -nw
        well = well_polygon(C, c)
        return c, devices, dict(bbox=(-nw, -nw, xend + nw, La + nw), xend=xend, La=La, well=well)
    C.box(c, "poly", cx1 - r("poly_encl_contact"), gy0, 0, La - gy0)
    dx = r("poly_contact_to_diff")
    dy = int(math.ceil(math.sqrt(max(0, m1b ** 2 - dx ** 2))))     # corner-to-corner m1_space to finger 0's stripes
    m1y0 = max(sd[1] + dy, gy0 + r("poly_encl_contact") - r("m1_endcap_contact"))
    m1y0 = C.snap(m1y0 + C.g // 2 + 1)
    y0, y1 = m1y0 + r("m1_endcap_contact"), La - m1y0 - r("m1_endcap_contact")
    pc = cs + r("contact_space")
    k = (y1 - y0 + r("contact_space")) // pc
    y = C.snap(y0 + ((y1 - y0) - (k * cs + (k - 1) * r("contact_space"))) // 2)
    for _ in range(k):
        C.box(c, "contact", cx1, y, cx1 + cs, y + cs)
        y += pc
    C.box(c, "m1", cx1, m1y0, cx1 + cs, La - m1y0)
    ym = C.snap(La // 2)
    C.box(c, "m1", -nw, ym - pin_h // 2, cx1 + cs, ym + pin_h // 2)
    C.pin(c, "m1", gate, -nw, ym - pin_h // 2, -nw + pin_h, ym + pin_h // 2)
    well = well_polygon(C, c)
    return c, devices, dict(bbox=(-nw, -nw, xend + nw, La + nw), xend=xend, La=La, well=well)


# --------------------------------------------------------------------------------------------- switch
def switch_cell(ly, P, name, dev, w, l, s, d, g, bulk=None, label="SW", model=""):
    """one finger R270: S at the top (pin on the top edge), D at the bottom (pin on the bottom edge), gate contact
    right of the channel (poly_contact_to_diff from the diffusion, m1_space from the S/D stripes), gate pin on the
    right edge. Tap-less."""
    C = Ctx(ly, P)
    bulk = bulk or s
    r = C.r
    cs, m1b = r("contact_size"), r("m1_space")
    fg = finger_geom(C, dev)
    W, La = fg["W"], fg["La"]
    sd = fg["sd"]
    nw = r("well_encl_pdiff")
    c = ly.create_cell(name)
    place_r270(c, dev, fg, 0, 0)
    gy0 = fg["gate"][0]
    gx0 = W + max(r("poly_contact_to_diff"), m1b)
    cy = C.snap(La // 2 - cs // 2)
    e = r("m1_endcap_contact")
    C.box(c, "poly", W, gy0, gx0 + cs + r("poly_encl_contact"), La - gy0)
    C.box(c, "contact", gx0, cy, gx0 + cs, cy + cs)
    C.box(c, "m1", gx0, cy - e, W + nw, cy + cs + e)
    pin_h = 2 * r("m1_width")
    C.pin(c, "m1", g, W + nw - pin_h, cy - e, W + nw, cy + cs + e)
    C.box(c, "m1", 0, La - sd[1], W, La + nw)
    C.pin(c, "m1", s, 0, La + nw - pin_h, W, La + nw)
    C.box(c, "m1", 0, -nw, W, sd[1])
    C.pin(c, "m1", d, 0, -nw, W, -nw + pin_h)
    C.text(c, "text", label, W // 2, La // 2)
    well = well_polygon(C, c)
    return c, [(name + "_" + label, d, g, s, bulk, w, l, model)], dict(bbox=(-nw, -nw, W + nw, La + nw), well=well)


# --------------------------------------------------------------------------------------------- taps
def tap_path(ly, P, name, points, net):
    """Well tap for the PARENT: one contact column along a rectilinear path (list of (x, y) um, the path's
    centre line). Diffusion 2 diff_encl_contact + contact_size wide, contacts at contact_size + contact_space,
    Metal1 over the contacts, well (and hvox) well_encl_tap around the diffusion. A segment only where the
    latch-up distance needs it; it follows the outline instead of enclosing empty area."""
    C = Ctx(ly, P)
    r = C.r
    cs, cao, cd = r("contact_size"), r("diff_encl_contact"), r("contact_space")
    wa = 2 * cao + cs
    pts = [db.Point(U(x), U(y)) for x, y in points]
    c = ly.create_cell(name)
    act = db.Region(db.Path(pts, wa, wa // 2, wa // 2).polygon())
    m1 = db.Region(db.Path(pts, cs, cs // 2, cs // 2).polygon()) & act
    c.shapes(C.li("diff")).insert(act)
    c.shapes(C.li("m1")).insert(m1.merged())
    for p1, p2 in zip(pts[:-1], pts[1:]):
        L_ = abs(p2.x - p1.x) + abs(p2.y - p1.y)
        n = max(1, (L_ + cd) // (cs + cd))
        off = (L_ - (n * cs + (n - 1) * cd)) // 2
        for k in range(n):
            t = C.snap(off + k * (cs + cd))
            if p1.y == p2.y:
                x = min(p1.x, p2.x) + t
                C.box(c, "contact", x, p1.y - cs // 2, x + cs, p1.y + cs // 2)
            else:
                y = min(p1.y, p2.y) + t
                C.box(c, "contact", p1.x - cs // 2, y, p1.x + cs // 2, y + cs)
    wl = act.sized(r("well_encl_tap"), r("well_encl_tap"), 5)
    c.shapes(C.li("well")).insert(wl)
    if getattr(P, "HVOX_LIKE_WELL", False):
        c.shapes(C.li("hvox")).insert(wl)
    q = pts[0]
    C.pin(c, "m1", net, q.x - cs // 2, q.y - cs // 2, q.x + cs // 2, q.y + cs // 2)
    return c


# --------------------------------------------------------------------------------------------- netlist
def cdl(name, pins, devices, comments=()):
    out = [".SUBCKT %s %s" % (name, " ".join(pins))]
    out += ["* " + x for x in comments]
    for (n, d, g, s, b, w, l, model) in devices:
        out.append("M%s %s %s %s %s %s w=%gu l=%gu ng=1 m=1" % (n, d, g, s, b, model, w, l))
    out.append(".ENDS %s" % name)
    return "\n".join(out) + "\n"
