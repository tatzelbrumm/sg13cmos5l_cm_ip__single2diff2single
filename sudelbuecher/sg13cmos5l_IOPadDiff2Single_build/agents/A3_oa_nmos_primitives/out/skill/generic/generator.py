# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Rotated-row MOS array generator (KLayout Python, klayout.db >= 0.28). Process-free: every rule value, layer and
device cell comes from a process adapter (one module per process, interface in adapter_template.py) through
semantic names (P.rule("finger_gap"), P.layer("metal1")). No net names inside: nets come with the score / voices.

Written 2026-10-28 by Claude (Opus 5.5) for rotated-row primitives (mirrors, sink rows, cascode rows, start-up
switches) of analog bias blocks.

The pattern ("score") -> cell, in short (patterns.md has the notation, SKILL_draft.md the procedure):
  * a row = a string of letters, one letter = one finger = one unmodified device cell, placed R270 (W along x,
    L along y, PCell texts upright) at P.rule("finger_gap"): the gate polys of a row merge into one strip; runs of
    the same cell become one AREF;
  * every row has two lines, B (bottom S/D stripes) and T (top). Each finger terminal gets a net; consecutive equal
    nets on a line become ONE Metal2 track drawn directly over the stripes; an M1 pad on the stripe holds up to
    three Via1. Rows are stacked at P.rule("active_space"): no band between rows. This needs every line to carry
    one net per contiguous run, i.e. rows that are pure in (S, D) -- interdigitate by rows, not inside a row;
  * vertical Metal1 at the row ends, from the array outwards: dummy strap (end dummies, D = S, tied to a net),
    gate bar (gate contacts of all rows that share a gate net), joiner(s) (one per net that has several tracks);
    a track gets Via1 wherever it crosses a vertical structure of its own net;
  * substrate / well ties: one-contact-row segments only where the latch-up distance needs them, no closed ring;
  * implant / thick-oxide outlines follow the devices as polygons (grown, then closed below the merge distance).
"""
import math
import klayout.db as db

EPS = 1e-6


def snap(v, g=0.005):
    return round(round(v / g) * g, 4)


class Ctx:
    """process adapter + layout + derived dimensions (each a formula of adapter rules)"""

    def __init__(self, P, ly):
        self.P, self.ly = P, ly
        self.g = P.rule("grid")

    def r(self, name):
        return self.P.rule(name)

    def L(self, name):
        return self.ly.layer(*self.P.layer(name))

    def s(self, v):
        return snap(v, self.g)

    # derived dimensions
    def track_w(self):      # M2 track over a via row: via + M2 endcap enclosure on both long sides
        return self.s(self.r("via1") + 2 * self.r("m2_via1_endcap"))

    def pad_h(self):        # M1 pad across a stripe: via + M1 enclosure both sides; the endcap runs along the pad
        return self.s(self.r("via1") + 2 * self.r("via1_m1_enc"))

    def via_pitch(self):
        return self.s(self.r("via1") + self.r("via1_space"))

    def pad_len(self, n):   # n vias in a row + M1 endcap at both ends
        return self.s(n * self.r("via1") + (n - 1) * self.r("via1_space") + 2 * self.r("via1_m1_endcap"))

    def cont_pitch(self):
        return self.s(self.r("cont") + self.r("cont_space"))

    def tap_h(self):        # one contact row
        return self.s(self.r("cont") + 2 * self.r("cont_in_active"))

    # drawing primitives
    def box(self, cell, lay, x0, y0, x1, y1):
        cell.shapes(self.L(lay)).insert(db.DBox(self.s(min(x0, x1)), self.s(min(y0, y1)), self.s(max(x0, x1)),
                                                self.s(max(y0, y1))))

    def hpath(self, cell, lay, x0, x1, y, w):
        cell.shapes(self.L(lay)).insert(db.DPath([db.DPoint(self.s(x0 + w / 2), self.s(y)),
                                                  db.DPoint(self.s(x1 - w / 2), self.s(y))], w, w / 2, w / 2))

    def vpath(self, cell, lay, x, y0, y1, w):
        cell.shapes(self.L(lay)).insert(db.DPath([db.DPoint(self.s(x), self.s(y0 + w / 2)),
                                                  db.DPoint(self.s(x), self.s(y1 - w / 2))], w, w / 2, w / 2))

    def text(self, cell, lay, s, x, y):
        cell.shapes(self.L(lay)).insert(db.DText(s, db.DTrans(self.s(x), self.s(y))))

    def vias(self, cell, xc, yc, n, vertical=False):
        a, p = self.r("via1"), self.via_pitch()
        for k in range(n):
            o = (k - (n - 1) / 2) * p
            x, y = (xc, yc + o) if vertical else (xc + o, yc)
            self.box(cell, "via1", x - a / 2, y - a / 2, x + a / 2, y + a / 2)

    def pin(self, cell, metal, net, x0, y0, x1, y1):
        """pin box + label at its centre (<metal>_pin + <metal>_label)"""
        m = "metal%d" % metal
        self.box(cell, m + "_pin", x0, y0, x1, y1)
        self.text(cell, m + "_label", net, (x0 + x1) / 2, (y0 + y1) / 2)


# ------------------------------------------------------------------ device cells
def copy_cell(src_ly, name, dst_ly, new_name=None):
    """Copy a flat leaf cell (an exported PCell variant) unchanged into dst_ly."""
    new_name = new_name or name
    if dst_ly.has_cell(new_name):
        return dst_ly.cell(new_name)
    src = src_ly.cell(name)
    dst = dst_ly.create_cell(new_name)
    for li in src_ly.layer_indexes():
        if src.shapes(li).is_empty():
            continue
        info = src_ly.get_info(li)
        dl = dst_ly.layer(info.layer, info.datatype)
        for s in src.shapes(li).each():
            dst.shapes(dl).insert(s)
    return dst


def derive_mos(cx, src_ly, cell_L, cell_W, new_name):
    """A W/L variant of a MOS PCell that the library lacks, built from two exported variants: cell_L has the wanted
    L, cell_W the wanted W. Valid only for a separable PCell (x depends on L only, y on W only, gate vertical);
    this is CHECKED: on every layer the result's distinct x-intervals must equal cell_L's and its y-intervals
    cell_W's, else ValueError. Texts are moved with the gate centre."""
    d = src_ly.dbu
    pl = src_ly.layer(*cx.P.layer("poly"))
    gW = db.Region(src_ly.cell(cell_W).shapes(pl)).bbox()
    gL = db.Region(src_ly.cell(cell_L).shapes(pl)).bbox()
    lw, ll, g0 = gW.width(), gL.width(), gW.left

    def mx(x):
        if x <= g0:
            return x
        if x >= g0 + lw:
            return x - lw + ll
        return g0 + round((x - g0) * ll / lw)
    src = src_ly.cell(cell_W)
    dst = cx.ly.create_cell(new_name)
    for li in src_ly.layer_indexes():
        info = src_ly.get_info(li)
        dl = cx.ly.layer(info.layer, info.datatype)
        for s in src.shapes(li).each():
            if s.is_box():
                b = s.box
                dst.shapes(dl).insert(db.DBox(mx(b.left) * d, b.bottom * d, mx(b.right) * d, b.top * d))
            elif s.is_text():
                dst.shapes(dl).insert(db.DText(s.text.string, db.DTrans(mx(s.text.x) * d, s.text.y * d)))
            else:
                raise ValueError("derive_mos: non-box shape in %s" % cell_W)

    def iv(ly, c, l, ax):
        out = set()
        for s in c.shapes(l).each():
            if s.is_text():
                continue
            b = s.bbox()
            out.add((b.left, b.right) if ax == "x" else (b.bottom, b.top))
        return sorted((round(a * ly.dbu, 4), round(b * ly.dbu, 4)) for a, b in out)
    for li in src_ly.layer_indexes():
        info = src_ly.get_info(li)
        dl = cx.ly.layer(info.layer, info.datatype)
        if iv(cx.ly, dst, dl, "x") != iv(src_ly, src_ly.cell(cell_L), li, "x"):
            raise ValueError("derive_mos: x-intervals differ from %s on %d/%d" % (cell_L, info.layer, info.datatype))
        if iv(cx.ly, dst, dl, "y") != iv(src_ly, src, li, "y"):
            raise ValueError("derive_mos: y-intervals differ from %s on %d/%d" % (cell_W, info.layer, info.datatype))
    return dst


class Mos:
    """Geometry of a device cell in its own frame (gate vertical: L along x, W along y), measured from the cell."""

    def __init__(self, cx, cell, model, name=None):
        self.cell, self.model = cell, model
        d = cx.ly.dbu
        a = db.Region(cell.shapes(cx.L("active"))).bbox().to_dtype(d)
        p = db.Region(cell.shapes(cx.L("poly"))).bbox().to_dtype(d)
        self.lact, self.W, self.L = snap(a.width()), snap(a.height()), snap(p.width())
        self.sd = snap(p.left - a.left)                  # S/D extension beyond the gate
        m1 = sorted((s.bbox().to_dtype(d) for s in cell.shapes(cx.L("metal1")).each()), key=lambda b: b.left)
        self.stripe_c = [snap(m1[0].center().x), snap(m1[-1].center().x)]


# ------------------------------------------------------------------ rows
class Finger:
    def __init__(self, **k):
        self.__dict__.update(k)


def place_row(cx, top, letters, devs, x0, y0):
    """Fingers R270 (W along x) left to right at the finger gap; returns [Finger] with the Activ box, the line
    centres yB / yT (bottom / top stripe) and the gate y-range g0..g1."""
    gap = cx.r("finger_gap")
    out, x, runs = [], x0, []
    for k, ch in enumerate(letters):
        m = devs[ch]
        out.append(Finger(letter=ch, idx=k, mos=m, x0=snap(x), x1=snap(x + m.W), y0=snap(y0), y1=snap(y0 + m.lact),
                          yB=snap(y0 + m.lact - m.stripe_c[1]), yT=snap(y0 + m.lact - m.stripe_c[0]),
                          g0=snap(y0 + m.sd), g1=snap(y0 + m.sd + m.L)))
        if runs and runs[-1][0] is m:
            runs[-1][2] += 1
        else:
            runs.append([m, x, 1])
        x += m.W + gap
    for m, xs, n in runs:
        t = db.DTrans(db.DTrans.R270, db.DVector(snap(xs), snap(y0 + m.lact)))
        if n == 1:
            top.insert(db.DCellInstArray(m.cell.cell_index(), t))
        else:
            top.insert(db.DCellInstArray(m.cell.cell_index(), t, db.DVector(snap(m.W + gap), 0), db.DVector(0, 0), n, 1))
    return out


def gate_contacts(cx, cell, row, side):
    """Poly tab + contact column beyond the end finger of a row (side 'L' / 'R') over the gate's y-range. The
    contact keeps max(m1_space, polycont_to_active) from the Activ end (the end finger's stripes end there).
    Returns ((bar_x0, bar_x1), (cont_y0, cont_y1)): the M1 bar x-range (via-ready) and the contacts' y-span."""
    f = row[0] if side == "L" else row[-1]
    gap = max(cx.r("m1_space"), cx.r("polycont_to_active"))
    c, cd = cx.r("cont"), cx.r("cont_in_poly")
    barw = max(c, cx.r("via1") + 2 * cx.r("via1_m1_enc"))
    if side == "L":
        cx0 = f.x0 - gap - c
        bar, tab = (snap(f.x0 - gap - barw), snap(f.x0 - gap)), (cx0 - cd, f.x0)
    else:
        cx0 = f.x1 + gap
        bar, tab = (snap(f.x1 + gap), snap(f.x1 + gap + barw)), (f.x1, cx0 + c + cd)
    cx.box(cell, "poly", tab[0], f.g0, tab[1], f.g1)
    p = cx.cont_pitch()
    n = int(math.floor((f.g1 - f.g0 - 2 * cd + cx.r("cont_space")) / p + EPS))
    span = n * c + (n - 1) * cx.r("cont_space")
    y0 = f.g0 + (f.g1 - f.g0 - span) / 2
    for k in range(n):
        y = snap(y0 + k * p)
        cx.box(cell, "contact", cx0, y, cx0 + c, y + c)
    return bar, (snap(y0), snap(y0 + span))


def stripe_pad(cx, cell, f, line, nmax=3):
    """M1 pad across a finger's stripe (centred) with up to nmax Via1; fewer on narrow fingers."""
    yc = f.yB if line == "B" else f.yT
    n = nmax
    while n > 1 and cx.pad_len(n) > f.x1 - f.x0:
        n -= 1
    ln, h, xc = cx.pad_len(n), cx.pad_h(), (f.x0 + f.x1) / 2
    cx.box(cell, "metal1", xc - ln / 2, yc - h / 2, xc + ln / 2, yc + h / 2)
    cx.vias(cell, xc, yc, n)
    return n


class Block:
    """Rows, over-stripe tracks and vertical M1 structures of one array cell; wire() adds the vias."""

    def __init__(self, cx, cell):
        self.cx, self.cell = cx, cell
        self.rows, self.tracks, self.verticals = [], [], []

    def add_row(self, name, letters, devs, x0, y0):
        f = place_row(self.cx, self.cell, letters, devs, x0, y0)
        self.rows.append((name, f))
        return f

    def line_tracks(self, fingers, line, nets, ext=None, pads=True):
        """nets: per finger the net on this line (None: no track, e.g. a strapped dummy). Consecutive equal nets
        form one segment, ext[net] = (x_left, x_right) overrides its ends. Different nets that would overlap on
        one line raise ValueError (a mixed row needs a second line: split the row instead)."""
        ext = ext or {}
        segs = []
        for f, n in zip(fingers, nets):
            if n is None:
                continue
            if segs and segs[-1]["net"] == n and segs[-1]["last"] == f.idx - 1:
                segs[-1].update(x1=f.x1, last=f.idx)
                segs[-1]["f"].append(f)
            else:
                segs.append(dict(net=n, x0=f.x0, x1=f.x1, last=f.idx, f=[f]))
        y = fingers[0].yB if line == "B" else fingers[0].yT
        sp = self.cx.r("m2_space")
        for s in segs:
            e = ext.get(s["net"], (None, None))
            x0 = s["x0"] if e[0] is None else e[0]
            x1 = s["x1"] if e[1] is None else e[1]
            for t in self.tracks:
                if abs(t["y"] - y) < EPS and t["net"] != s["net"] and x0 < t["x1"] + sp and t["x0"] < x1 + sp:
                    raise ValueError("track %s collides with %s at y=%.3f" % (s["net"], t["net"], y))
            self.tracks.append(dict(net=s["net"], x0=snap(x0), x1=snap(x1), y=y))
            if pads:
                for f in s["f"]:
                    stripe_pad(self.cx, self.cell, f, line)
        return segs

    def track(self, net, x0, x1, y):
        self.tracks.append(dict(net=net, x0=snap(x0), x1=snap(x1), y=snap(y)))

    def vertical(self, net, x0, x1, y0, y1, nvia=1, draw=True):
        v = dict(net=net, x0=snap(x0), x1=snap(x1), y0=snap(y0), y1=snap(y1), nvia=nvia)
        self.verticals.append(v)
        if draw:
            self.cx.box(self.cell, "metal1", x0, y0, x1, y1)
        return v

    def wire(self):
        cx, w = self.cx, self.cx.track_w()
        a, enc = cx.r("via1"), cx.r("via1_m1_enc")
        for t in self.tracks:
            cx.hpath(self.cell, "metal2", t["x0"], t["x1"], t["y"], w)
            for v in self.verticals:
                if v["net"] != t["net"] or not (v["x0"] < t["x1"] and t["x0"] < v["x1"]):
                    continue
                if not (v["y0"] - EPS <= t["y"] - a / 2 - enc and t["y"] + a / 2 + enc <= v["y1"] + EPS):
                    continue
                lo, hi = max(v["x0"], t["x0"]), min(v["x1"], t["x1"])
                n = v["nvia"]
                while n > 1 and n * a + (n - 1) * cx.r("via1_space") + 2 * enc > hi - lo + EPS:
                    n -= 1
                cx.vias(self.cell, (lo + hi) / 2, t["y"], n)


def strap(cx, cell, column, y0, y1):
    """Vertical M1 strap over a column of end dummies (one per row, same x): D = S of each, all joined.
    Width = a 3-via pad, centred on the dummy. Returns (x0, x1)."""
    f = column[0]
    w, xc = cx.pad_len(3), (f.x0 + f.x1) / 2
    cx.box(cell, "metal1", xc - w / 2, y0, xc + w / 2, y1)
    return snap(xc - w / 2), snap(xc + w / 2)


def tie(cx, cell, x0, x1, ya, grid_x, impl="pimp"):
    """Tie segment (substrate tie with impl='pimp'), one contact row, Activ [x0, x1] x [ya, ya + tap_h]. Contacts
    on the global grid grid_x + k * cont_pitch (two cells on the same grid can overlap their ties exactly).
    M1 = contacts + m1_cont_endcap all round (via-ready). Checks tie_cont_ext_max. Returns the M1 box."""
    h, c, cc, p = cx.tap_h(), cx.r("cont"), cx.r("cont_in_active"), cx.cont_pitch()
    cx.box(cell, "active", x0, ya, x1, ya + h)
    e = cx.r("tie_impl_enc")
    cx.box(cell, impl, x0 - e, ya - e, x1 + e, ya + h + e)
    k0 = math.ceil((x0 + cc - grid_x) / p - EPS)
    k1 = math.floor((x1 - cc - c - grid_x) / p + EPS)
    xs = [snap(grid_x + k * p) for k in range(k0, k1 + 1)]
    for x in xs:
        cx.box(cell, "contact", x, ya + cc, x + c, ya + cc + c)
    if xs[0] - x0 > cx.r("tie_cont_ext_max") or x1 - xs[-1] - c > cx.r("tie_cont_ext_max"):
        raise ValueError("tie Activ extends too far beyond its contacts")
    m = cx.r("m1_cont_endcap")
    mb = (snap(xs[0] - m), snap(ya + cc - m), snap(xs[-1] + c + m), snap(ya + cc + c + m))
    cx.box(cell, "metal1", *mb)
    return mb


def outline(cx, cell, lay, grow_from, close):
    """Polygon following the devices on layer `lay`: union of (layer region sized by its grow value) for each
    (layer name, grow) in grow_from, closed by close/2 (gaps and notches < close merge), drawn as polygons."""
    r = db.Region()
    d = cx.ly.dbu
    for src, gr in grow_from:
        li = cx.L(src)
        r += db.Region(cell.begin_shapes_rec(li)).sized(int(round(gr / d)))
    r = r.merged()
    h = int(round(close / 2 / d))
    r = r.sized(h).sized(-h).merged()
    for p in r.each():
        cell.shapes(cx.L(lay)).insert(p)
    return r


# ------------------------------------------------------------------ score and netlist
def parse_score(text):
    """Score syntax (one statement per line, '#' starts a comment; rows bottom first):
         row   <name> [flip] : <letter> <letter> ...   one letter = one finger, left to right; 'flip' = this row
                                                        has S on its top line (T), D on its bottom line (B)
         voice <letter> = <device> D=<net> G=<net> S=<net> [B=<net>]
         sym   <op> rows=<first>-<last> [letters=<l,l>]  op: mirror_y (retrogradation of the rows),
                                                          mirror_x (retrogradation inside each row),
                                                          point (retrograde inversion), translate_y=<k>,
                                                          mirror_y_orient (mirror_y, and mirrored rows have
                                                          opposite current direction: retrograde + inversion
                                                          of the S/D direction)
         cc    <l,l,...> rows=<first>-<last>             claim: these voices share one centroid
       Returns dict(rows=[(name, [letters])], flip={names}, voices={l: dict}, syms=[...], ccs=[...])."""
    rows, voices, syms, ccs, flip = [], {}, [], [], set()
    for ln in text.strip().splitlines():
        ln = ln.split("#")[0].strip()
        if not ln:
            continue
        kw = ln.split()[0]
        if kw == "row":
            head, body = ln.split(":", 1)
            hp = head.split()
            rows.append((hp[1], body.split()))
            if len(hp) > 2 and hp[2] == "flip":
                flip.add(hp[1])
        elif kw == "voice":
            head, body = ln[len("voice"):].split("=", 1)
            parts = body.split()
            v = dict(device=parts[0])
            for p in parts[1:]:
                k, n = p.split("=")
                v[k] = n
            voices[head.strip()] = v
        elif kw in ("sym", "cc"):
            parts = ln.split()
            kv = dict(p.split("=") for p in parts[2:])
            (syms if kw == "sym" else ccs).append(dict(op=parts[1], **kv))
        else:
            raise ValueError("score: " + ln)
    return dict(rows=rows, flip=flip, voices=voices, syms=syms, ccs=ccs)


def _rows_range(score, spec):
    names = [n for n, _ in score["rows"]]
    a, b = spec.split("-")
    return [l for n, l in score["rows"][names.index(a):names.index(b) + 1]]


def check_score(score):
    """Verify every 'sym' and 'cc' claim on the letter matrix; returns a list of (claim, ok, detail)."""
    out = []
    for s in score["syms"]:
        M = _rows_range(score, s["rows"])
        if s["op"] == "mirror_y":
            ok = M == M[::-1]
        elif s["op"] == "mirror_x":
            ok = all(r == r[::-1] for r in M)
        elif s["op"] == "point":
            ok = M == [r[::-1] for r in M[::-1]]
        elif s["op"] == "mirror_y_orient":
            names = [n for n, _ in score["rows"]]
            a, b = s["rows"].split("-")
            nm = names[names.index(a):names.index(b) + 1]
            fl = [n in score.get("flip", set()) for n in nm]
            ok = M == M[::-1] and all(fl[i] != fl[len(fl) - 1 - i] for i in range(len(fl)) if 2 * i + 1 != len(fl))
        elif s["op"].startswith("translate_y"):
            k = int(s["op"].split("=")[1])
            ok = all(M[i] == M[i + k] for i in range(len(M) - k))
        else:
            raise ValueError(s)
        out.append((s, ok, ""))
    for c in score["ccs"]:
        M = _rows_range(score, c["rows"])
        cents = {}
        for l in c["op"].split(","):
            pts = [(x, y) for y, r in enumerate(M) for x, ch in enumerate(r) if ch == l]
            cents[l] = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts), len(pts))
        vals = list(cents.values())
        ok = all(abs(v[0] - vals[0][0]) < 1e-9 and abs(v[1] - vals[0][1]) < 1e-9 for v in vals)
        out.append((c, ok, cents))
    return out


def write_cdl(fn, subckts, header=""):
    """subckts: [(name, ports, devices)], device = (name, d, g, s, b, model, w, l)"""
    with open(fn, "w") as f:
        f.write(header)
        for name, ports, devs in subckts:
            f.write(".SUBCKT %s %s\n" % (name, " ".join(ports)))
            for dv in devs:
                f.write("M%s %s %s %s %s %s w=%gu l=%gu ng=1 m=1\n" % dv)
            f.write(".ENDS %s\n\n" % name)


if __name__ == "__main__":
    # python3 generator.py <patterns.md>: parse every fenced score block and check its sym / cc claims
    import re
    import sys
    txt = open(sys.argv[1]).read()
    for k, blk in enumerate(re.findall(r"```\n(.*?)```", txt, re.S)):
        if not blk.lstrip().startswith("row ") or "<" in blk:          # skip the syntax block
            continue
        sc = parse_score(blk)
        res = check_score(sc)
        print("score %d: %d rows, voices %s, claims %s" % (k, len(sc["rows"]), "".join(sorted(sc["voices"])) or "-",
              ["%s %s" % (c[0]["op"], "ok" if c[1] else "FAILS") for c in res] or "-"))
