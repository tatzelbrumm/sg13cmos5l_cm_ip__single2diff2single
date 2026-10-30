# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""generator.py: assemble an analog block from layout primitives (process-agnostic, klayout.db >= 0.28).

    placement grammar (text) -> placed primitive instances -> tap stripes, merged wells
    -> two-metal grid router -> rails, edge pins -> GDS, report, latch-up check

Written 2026-10-28 by Claude (Opus 5.5). No process fact lives in this file: layer numbers, rule values, tap
construction and device derivations come from a process adapter module (e.g. process/ihp_sg13cmos5l.py) with
LAYERS, rules(), TAPS, derive(). No net or cell name lives here either: they are arguments (a config file).

Placement grammar: one node per line, children indented under their parent, '#' starts a comment.
    V  [gap=G] [align=left|right|center]     stack: children top -> bottom (voices, top voice first)
    H  [gap=G] [align=bottom|top|center]     sequence: children left -> right (time)
    cell <instance> [o=<orientation>]        a primitive instance (instance table: cell name, source, net map)
    rail <net> h=<height> [tap=n|p] [thick=1] [tap_x=x0,x1[;x0,x1]]
                                             lower-metal rail across the enclosing V; tap=: tie stripe under it
    space [w=<width>] [h=<height>]           reserved empty space (a routing channel)
    FREE                                     children placed absolutely: cell <instance> o=<o> at=<x>,<y>
  G: a number in um (negative = overlap, e.g. a ring shared with the rail), 'auto' (smallest gap >= 0 for which
  the two neighbours are DRC clean, latch-up excluded; needs the drc callback), or a comma list, one per seam.
  Orientations (KLayout codes, and the music aliases of the pattern notation):
    R0 = P (prime), M90 = MY = R (retrograde: x reversed), M0 = MX = I (inversion: y reversed),
    R180 = RI (retrograde inversion = point symmetry), R90, R270, M45, M135.

Router: two metals ("M1" = lower, "M2" = upper routing metal of the adapter), non-uniform grid = regular lines at
`pitch` + the centre lines of all pins, node squares `width` x `width`, A* with preferred directions, via and turn
costs, exact L1 distance-transform heuristic. Terminal of a pin = the cell's whole metal of that net (found by
connectivity inside the cell). Spacing is geometric: space / wide_space of the adapter next to the wide parts of
cell metal, space between router wires. After routing: same-net gaps < space are filled (closing), partial landings
get patches, same-net vias closer than via size + space are merged.
"""
import heapq
import importlib.util
import math
import re

import numpy as np
import klayout.db as db

ORIENT = {"R0": db.Trans.R0, "R90": db.Trans.R90, "R180": db.Trans.R180, "R270": db.Trans.R270,
          "M0": db.Trans.M0, "M45": db.Trans.M45, "M90": db.Trans.M90, "M135": db.Trans.M135,
          "MX": db.Trans.M0, "MY": db.Trans.M90, "P": db.Trans.R0, "R": db.Trans.M90, "I": db.Trans.M0,
          "RI": db.Trans.R180}
ROUTE_LAYERS = {"M1": "m1", "M1pin": "m1.pin", "M1txt": "m1.text", "V1": "via1", "M2": "m2", "M2pin": "m2.pin",
                "M2txt": "m2.text"}


def load_process(path):
    """Import a process adapter module from its file path."""
    spec = importlib.util.spec_from_file_location("process_adapter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------------------
# placement grammar
# ------------------------------------------------------------------------------------------------------------
class Node:
    def __init__(self, kind, args, attrs, line):
        self.kind, self.args, self.attrs, self.line = kind, args, attrs, line
        self.children, self.gaps = [], []
        self.w = self.h = 0.0

    def __repr__(self):
        return "%s(%s)" % (self.kind, " ".join(self.args))


def parse_floorplan(text):
    root, stack = None, []
    for ln, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        ind = len(line) - len(line.lstrip())
        tok = line.split()
        n = Node(tok[0], [t for t in tok[1:] if "=" not in t], dict(t.split("=", 1) for t in tok[1:] if "=" in t), ln)
        if n.kind not in ("V", "H", "cell", "rail", "space", "FREE"):
            raise ValueError("floorplan line %d: unknown node %r" % (ln, n.kind))
        while stack and stack[-1][0] >= ind:
            stack.pop()
        if stack:
            stack[-1][1].children.append(n)
        elif root is None:
            root = n
        else:
            raise ValueError("floorplan line %d: second root" % ln)
        stack.append((ind, n))
    return root


def _gaps(node, nseams):
    vals = node.attrs.get("gap", "0").split(",")
    if len(vals) == 1:
        vals = vals * nseams
    if len(vals) != nseams:
        raise ValueError("line %d: %d gaps for %d seams" % (node.line, len(vals), nseams))
    return [v if v == "auto" else float(v) for v in vals]


# ------------------------------------------------------------------------------------------------------------
# the block
# ------------------------------------------------------------------------------------------------------------
class Block:
    """name: top cell; sources: {key: gds}; instances: {inst: dict(cell=, o=, nets={cellpin: net})};
    floorplan: grammar text; proc: process adapter module; nets: block nets to route; ports: {net: (side, (lo, hi)
    or None)}; pin_overrides: {cell: [(metal "M1"/"M2", name, (x0, y0, x1, y1))]}; router: GridRouter options
    (+ keepout=[(metal, (x0, y0, x1, y1))]); drc: callable(layout, cellname) -> [(rule, count)];
    merge_wells: fill same-net well gaps < the well space rule (all wells of the block on one net)."""

    def __init__(self, name, sources, instances, floorplan, proc, nets, ports=None, pin_overrides=None,
                 router=None, drc=None, merge_wells=False, keep_cells=(), log=print):
        self.name, self.instances, self.proc, self.nets = name, instances, proc, list(nets)
        self.R = proc.rules()
        self.ports, self.pin_overrides, self.ropt = ports or {}, pin_overrides or {}, router or {}
        self.drc, self.merge_wells, self.log = drc, merge_wells, log
        self.ly = db.Layout()
        self.dbu = None
        self._load(sources, keep_cells)
        self.L = {k: self.ly.layer(*v) for k, v in proc.LAYERS.items() if isinstance(v, tuple)}
        self.LI = {k: self.L[v] for k, v in ROUTE_LAYERS.items()}
        self.top = self.ly.create_cell(name)
        self.tree = parse_floorplan(floorplan)
        self.leaves, self.rails, self.spaces, self.taps = {}, [], [], []
        self.port_pins, self.extra = {}, []

    # ---- loading -------------------------------------------------------------------------------------------
    def _load(self, sources, keep_cells):
        opt = db.LoadLayoutOptions()
        opt.cell_conflict_resolution = db.LoadLayoutOptions.RenameCell
        renamed = []
        for key, path in sources.items():
            tmp = db.Layout()
            tmp.read(path)
            if self.dbu is None:
                self.dbu = self.ly.dbu = tmp.dbu
            elif abs(tmp.dbu - self.dbu) > 1e-12:
                raise ValueError("dbu of %s differs" % path)
            before = {c.name for c in self.ly.each_cell()}
            own = {c.name for c in tmp.each_cell()}
            self.ly.read(path, opt)
            renamed += [c.name for c in self.ly.each_cell() if c.name not in before and c.name not in own]
        need = set()
        for spec in self.instances.values():
            c = self.ly.cell(spec["cell"])
            if c is None:
                raise ValueError("cell %s not found in the sources" % spec["cell"])
            need |= {c.cell_index()} | set(c.called_cells())
        for n in keep_cells:
            c = self.ly.cell(n)
            need |= {c.cell_index()} | set(c.called_cells())
        self._dedupe([n for n in renamed if self.ly.has_cell(n)])
        need = set()
        for spec in self.instances.values():
            c = self.ly.cell(spec["cell"])
            need |= {c.cell_index()} | set(c.called_cells())
        for ci in [c.cell_index() for c in self.ly.each_cell()]:
            if ci not in need:
                self.ly.delete_cell(ci)

    def _same(self, a, b):
        for li in self.ly.layer_indexes():
            if not (db.Region(a.begin_shapes_rec(li)) ^ db.Region(b.begin_shapes_rec(li))).is_empty():
                return False
            ta = sorted((s.text_string, s.text.x, s.text.y) for s in a.shapes(li).each() if s.is_text())
            tb = sorted((s.text_string, s.text.x, s.text.y) for s in b.shapes(li).each() if s.is_text())
            if ta != tb:
                return False
        return True

    def _dedupe(self, renamed):
        """Cells renamed on reading a later source (name$N) and identical to the first copy are replaced by it
        (e.g. the same unmodified PDK device cell in two primitive libraries)."""
        for name in renamed:
            c = self.ly.cell(name)
            m = re.match(r"^(.*)\$\d+$", c.name)
            if not m or not self.ly.has_cell(m.group(1)):
                continue
            o = self.ly.cell(m.group(1))
            if self._same(o, c):
                for pi in list(c.each_parent_inst()):
                    pi.child_inst().cell_index = o.cell_index()
                self.ly.delete_cell(c.cell_index())
            else:
                self.log("warning: %s and %s differ; both kept" % (o.name, c.name))

    # ---- helpers -------------------------------------------------------------------------------------------
    def u(self, v):
        return int(round(v / self.dbu))

    def g5(self, v):
        g = self.R["grid"]
        return round(round(v / g) * g, 6)

    def itrans(self, t):
        return db.CplxTrans(self.dbu).inverted() * db.DCplxTrans(t) * db.CplxTrans(self.dbu)

    def oriented_bbox(self, inst, o):
        c = self.ly.cell(self.instances[inst]["cell"])
        return c.dbbox().transformed(db.DTrans(ORIENT[o], db.DVector(0, 0)))

    def orient_of(self, node):
        return node.attrs.get("o", self.instances[node.args[0]].get("o", "R0"))

    def region(self, key, cell=None):
        li = self.L.get(key)
        cell = cell or self.top
        return db.Region(cell.begin_shapes_rec(li)).merged() if li is not None else db.Region()

    # ---- placement -----------------------------------------------------------------------------------------
    def _size(self, n):
        if n.kind == "cell":
            b = self.oriented_bbox(n.args[0], self.orient_of(n))
            n.w, n.h = b.width(), b.height()
        elif n.kind == "space":
            n.w, n.h = float(n.attrs.get("w", 0)), float(n.attrs.get("h", 0))
        elif n.kind == "rail":
            n.w, n.h = 0.0, float(n.attrs["h"])
        elif n.kind in ("H", "V"):
            for c in n.children:
                self._size(c)
            n.gaps = _gaps(n, len(n.children) - 1)
            for i, g in enumerate(n.gaps):
                if g == "auto":
                    n.gaps[i] = self._auto_gap(n, i)
            if n.kind == "H":
                n.w = sum(c.w for c in n.children) + sum(n.gaps)
                n.h = max(c.h for c in n.children)
            else:
                n.w = max(c.w for c in n.children)
                n.h = sum(c.h for c in n.children) + sum(n.gaps)
        elif n.kind == "FREE":
            bb = db.DBox()
            for c in n.children:
                x, y = (float(v) for v in c.attrs["at"].split(","))
                bb += self.oriented_bbox(c.args[0], self.orient_of(c)).moved(db.DVector(x, y))
            n.w, n.h, n.bb = bb.width(), bb.height(), bb

    def _place(self, n, x, y, w=None, out=None):
        out = self.leaves if out is None else out
        if n.kind == "cell":
            o = self.orient_of(n)
            b = self.oriented_bbox(n.args[0], o)
            out[n.args[0]] = db.DTrans(ORIENT[o], db.DVector(self.g5(x - b.left), self.g5(y - b.bottom)))
        elif n.kind == "rail":
            out[("rail", n.line)] = (n, db.DBox(x, y, x + (w if w is not None else n.w), y + n.h))
        elif n.kind == "space":
            out[("space", n.line)] = db.DBox(x, y, x + n.w, y + n.h)
        elif n.kind == "H":
            al = n.attrs.get("align", "bottom")
            cx = x
            for i, c in enumerate(n.children):
                dy = {"bottom": 0.0, "top": n.h - c.h, "center": (n.h - c.h) / 2}[al]
                self._place(c, cx, y + dy, None, out)
                cx += c.w + (n.gaps[i] if i < len(n.gaps) else 0)
        elif n.kind == "V":
            al = n.attrs.get("align", "left")
            cy = y + n.h
            for i, c in enumerate(n.children):
                cy -= c.h
                dx = {"left": 0.0, "right": n.w - c.w, "center": (n.w - c.w) / 2}[al]
                self._place(c, x + (0 if c.kind == "rail" else dx), cy, n.w if c.kind == "rail" else None, out)
                cy -= (n.gaps[i] if i < len(n.gaps) else 0)
        elif n.kind == "FREE":
            for c in n.children:
                cx, cy = (float(v) for v in c.attrs["at"].split(","))
                out[c.args[0]] = db.DTrans(ORIENT[self.orient_of(c)],
                                           db.DVector(cx - n.bb.left + x, cy - n.bb.bottom + y))

    def _materialize(self, placed, cell, interior_y=None):
        """Instances, then rails (+ tie stripes where the rail band is free) of a placement dict into `cell`."""
        rails = []
        for k, v in placed.items():
            if isinstance(k, str):
                cell.insert(db.DCellInstArray(self.ly.cell(self.instances[k]["cell"]).cell_index(), v))
        for k, v in placed.items():
            if isinstance(k, tuple) and k[0] == "rail":
                node, box = v
                cell.shapes(self.LI["M1"]).insert(box)
                rails.append((node.args[0], box, "M1"))
                if "tap" in node.attrs:
                    inward = -1 if interior_y is None or (box.top + box.bottom) / 2 > interior_y else 1
                    self._draw_tap(cell, node, box, inward)
        return rails

    def _draw_tap(self, cell, node, box, inward):
        """Tie stripe under a rail: diffusion + one contact row (the rail's lower metal covers it), well (n) or
        implant (p) per the adapter's TAPS; thick=1: inside the thick oxide (adapter THICK), merging with it.
        Only where the rail band is free: keeps the adapter's spacings to the diffusion, poly, contacts (and thick
        oxide for a thin tie, the well for a p tie) already in `cell`; the diffusion sits one enclosure from the
        rail's outer edge, so well / oxide stay inside the block."""
        R, kind = self.R, node.attrs["tap"]
        thick = node.attrs.get("thick", "0") == "1"
        T = self.proc.TAPS[kind]
        a = max(R["diff.width"], R["cont.size"] + 2 * R["cont.enc_diff"])
        enc = R[T["well_enc_thick"] if thick else T["well_enc"]] if kind == "n" else R[T["implant_enc"]]
        if thick:
            enc = max(enc, R[self.proc.THICK["enc"]])
        y0 = box.top - enc - a if inward < 0 else box.bottom + enc
        ranges = [(box.left, box.right)]
        if "tap_x" in node.attrs:
            ranges = [tuple(float(v) for v in r.split(",")) for r in node.attrs["tap_x"].split(";")]
        u = self.u
        reg = {k: self.region(k, cell) for k in ("diff", "poly", "cont", "thickox", "nwell", "pimp")}
        dv = self.proc.derive(reg)
        blk = (reg["diff"].sized(u(R["diff.space"])) + reg["poly"].sized(u(R["diff.space"])) +
               reg["cont"].sized(u(R["cont.space"])))
        if not thick:
            blk += reg["thickox"].sized(u(R["thickox.space_diff"]))
        if kind == "p":
            blk += reg["nwell"].sized(u(R["nwell.space_ptap"]))
            blk += dv["ndiff_dev"].sized(u(R["pimp.enc_pdiff"] + R["pimp.space_ndiff"]))
            blk += reg["pimp"].sized(u(R["pimp.space"] + enc))
        else:
            blk += dv["ndiff_dev"].sized(u(R["nwell.space_ndiff_thick"] + enc))
            blk += dv["ptap"].sized(u(R["nwell.space_ptap"] + enc))
            blk += dv["pdiff_dev"].sized(u(R["pimp.enc_pdiff"] + R["pimp.space_ndiff"]))
        for x0, x1 in ranges:
            x0, x1 = self.g5(max(x0, box.left) + enc), self.g5(min(x1, box.right) - enc)
            if x1 - x0 < a:
                continue
            stripe = db.Region(db.DBox(x0, self.g5(y0), x1, self.g5(y0) + a).to_itype(self.dbu))
            ha = u(a) // 2 - 1                      # opening across the stripe: drop everything thinner than a tie
            free = (stripe - blk).sized(0, -ha, 2).sized(0, ha, 2) & stripe
            for tz in free.merged().decompose_trapezoids_to_region(db.Polygon.TD_htrapezoids).each():
                pb = tz.bbox().to_dtype(self.dbu)
                if pb.height() < a - 1e-6:
                    continue
                self._tap_box(cell, kind, node.args[0], db.DBox(self.g5(pb.left), pb.bottom, self.g5(pb.right),
                                                                pb.top), enc, thick, metal=False,
                              well_to=(box.bottom if inward < 0 else box.top))

    def _tap_box(self, cell, kind, net, d, enc, thick, metal=True, well_to=None):
        """One tie: diffusion box d, a contact row along its long side, optional lower-metal cover, well (n) /
        implant (p) by enc, thick oxide by enc if thick; well_to: stretch the well to this y (to meet the cells)."""
        R = self.R
        s, sp, e = R["cont.size"], R["cont.space"], R["cont.enc_diff"]
        horiz = d.width() >= d.height()
        L = d.width() if horiz else d.height()
        n = int((L - 2 * e + sp) // (s + sp))
        if n < 1:
            return False
        cell.shapes(self.L["diff"]).insert(d)
        start = self.g5((d.left if horiz else d.bottom) + (L - (n * s + (n - 1) * sp)) / 2)
        for i in range(n):
            c0 = round(start + i * (s + sp), 6)                  # pitch s + sp is on grid: snap only the start
            if horiz:
                cy = self.g5((d.bottom + d.top - s) / 2)
                cell.shapes(self.L["cont"]).insert(db.DBox(c0, cy, c0 + s, cy + s))
            else:
                cx = self.g5((d.left + d.right - s) / 2)
                cell.shapes(self.L["cont"]).insert(db.DBox(cx, c0, cx + s, c0 + s))
        if metal:
            cell.shapes(self.LI["M1"]).insert(d)
        T = self.proc.TAPS[kind]
        if kind == "n":
            wb = d.enlarged(enc, enc)
            if well_to is not None:
                wb = db.DBox(wb.left, min(wb.bottom, well_to), wb.right, max(wb.top, well_to))
            cell.shapes(self.L[T["well"]]).insert(wb)
        else:
            cell.shapes(self.L[T["implant"]]).insert(d.enlarged(enc, enc))
        if thick:
            tb = d.enlarged(enc, enc)
            if well_to is not None:
                tb = db.DBox(tb.left, min(tb.bottom, well_to), tb.right, max(tb.top, well_to))
            cell.shapes(self.L[self.proc.THICK["layer"]]).insert(tb)
        if cell is self.top:
            self.taps.append((kind, net, d))
        return True

    def add_tap_segments(self, segs):
        """Explicit ties (e.g. where the primitive's designer says latch-up needs them): dict(inst, kind, net,
        box=(x0, y0, x1, y1) of the diffusion in the instance's cell coordinates, thick=bool, metal=bool)."""
        R = self.R
        for sgm in segs:
            t = self.leaves[sgm["inst"]]
            d = db.DBox(*sgm["box"]).transformed(t)
            kind, thick = sgm["kind"], sgm.get("thick", False)
            T = self.proc.TAPS[kind]
            enc = R[T["well_enc_thick"] if thick else T["well_enc"]] if kind == "n" else R[T["implant_enc"]]
            if thick:
                enc = max(enc, R[self.proc.THICK["enc"]])
            self._tap_box(self.top, kind, sgm["net"], d, enc, thick, metal=sgm.get("metal", True))

    def _well_fill(self, cell):
        """Gaps narrower than the space rule between shapes of a MERGE layer (adapter MERGE_LAYERS: e.g. the
        one-net well, the thick oxide) are filled (closing): one polygon whose outline follows the cells; no
        bounding rectangle. Returns the filled area region of the first layer (the well)."""
        first = None
        for key, rule in self.proc.MERGE_LAYERS:
            reg = self.region(key, cell)
            if reg.is_empty():
                continue
            d = self.u(self.R[rule] / 2) + self.u(self.R["grid"])
            fill = reg.sized(d).sized(-d) - reg
            if not fill.is_empty():
                cell.shapes(self.L[key]).insert(fill)
            if first is None:
                first = fill
        return first if first is not None else db.Region()

    def _auto_gap(self, n, i, lo=0.0, hi=6.0, coarse=0.25):
        if self.drc is None:
            raise ValueError("gap=auto needs a drc callback")
        a, b = n.children[i], n.children[i + 1]

        def trial(g):
            tmp = self.ly.create_cell("__gap_trial")
            pa = {}
            if n.kind == "H":
                h = max(a.h, b.h)
                al = n.attrs.get("align", "bottom")
                dy = lambda c: {"bottom": 0.0, "top": h - c.h, "center": (h - c.h) / 2}[al]
                self._place(a, 0, dy(a), max(a.w, b.w), pa)
                self._place(b, a.w + g, dy(b), max(a.w, b.w), pa)
                iy = h / 2
            else:
                w = max(a.w, b.w)
                al = n.attrs.get("align", "left")
                dx = lambda c: 0.0 if c.kind == "rail" else {"left": 0.0, "right": w - c.w, "center": (w - c.w) / 2}[al]
                self._place(a, dx(a), b.h + g, w, pa)
                self._place(b, dx(b), 0, w, pa)
                iy = (b.h + g + a.h) / 2 if a.kind != "rail" and b.kind != "rail" else (b.h if a.kind == "rail" else b.h + g)
            rails = self._materialize(pa, tmp, iy)
            if self.merge_wells:
                self._well_fill(tmp)
            res = self.drc(self.ly, tmp.name)
            nshort = self._label_shorts(tmp, rails)
            self.ly.delete_cell(tmp.cell_index())
            return sum(c for r, c in res if not r.startswith("LU")) + nshort

        g, last_bad = lo, None
        while g <= hi + 1e-9:
            if trial(g) == 0:
                break
            last_bad, g = g, g + coarse
        else:
            raise ValueError("line %d: no DRC-clean gap up to %g um" % (n.line, hi))
        if last_bad is not None:
            bad, good = last_bad, g
            while good - bad > self.R["grid"] * 1.5:
                mid = self.g5((bad + good) / 2)
                if mid in (bad, good):
                    break
                if trial(mid) == 0:
                    good = mid
                else:
                    bad = mid
            g = good
        self.log("auto gap line %d seam %d (%s | %s): %.3f um" % (n.line, i, a, b, g))
        return self.g5(g)

    def _label_shorts(self, cell, rails):
        """Merged lower / upper metal polygons that carry pin texts of two different nets (rails count with their
        net): touching metal of two nets merges silently, so the DRC alone does not see it."""
        n = 0
        for metal in ("M1", "M2"):
            texts = []
            it = cell.begin_shapes_rec(self.LI[metal + "txt"])
            while not it.at_end():
                s = it.shape()
                if s.is_text():
                    texts.append((s.text_string, s.text.transformed(it.trans()).position()))
                it.next()
            reg = db.Region(cell.begin_shapes_rec(self.LI[metal]))
            for net, box, m in rails:
                if m == metal:
                    texts.append((net, box.center().to_itype(self.dbu)))
            for poly in reg.merged().each():
                names = {t for t, p in texts if poly.inside(p)}
                if len(names) > 1:
                    n += 1
        return n

    def place(self):
        self._size(self.tree)
        placed = {}
        self._place(self.tree, 0.0, 0.0, self.tree.w, placed)
        self.rails = self._materialize(placed, self.top, self.tree.h / 2)
        self.leaves = {k: v for k, v in placed.items() if isinstance(k, str)}
        self.spaces = [v for k, v in placed.items() if isinstance(k, tuple) and k[0] == "space"]
        self.bbox = self.top.dbbox()
        self.log("placed %d instances, %d rails, %d tap stripes: %.3f x %.3f um"
                 % (len(self.leaves), len(self.rails), len(self.taps), self.bbox.width(), self.bbox.height()))
        return self.bbox

    # ---- pins ----------------------------------------------------------------------------------------------
    def cell_pins(self, cellname):
        """[(metal, name, DBox)] in cell coordinates: pin boxes with a text; a text alone takes the metal under it."""
        if cellname in self.pin_overrides:
            return [(m, n, db.DBox(*b)) for m, n, b in self.pin_overrides[cellname]]
        c = self.ly.cell(cellname)
        pins = []
        for metal in ("M1", "M2"):
            boxes = [s.dbbox() for s in c.shapes(self.LI[metal + "pin"]).each() if not s.is_text()]
            texts = [s.dtext for s in c.shapes(self.LI[metal + "txt"]).each() if s.is_text()]
            texts += [s.dtext for s in c.shapes(self.LI[metal + "pin"]).each() if s.is_text()]
            mreg = db.Region(c.begin_shapes_rec(self.LI[metal])).merged()
            for t in texts:
                p = db.DPoint(t.x, t.y)
                hit = [b for b in boxes if b.contains(p)]
                if hit:
                    pins.append((metal, t.string, min(hit, key=lambda b: b.area())))
                    continue
                under = [q for q in mreg.each() if q.inside(db.Point(self.u(p.x), self.u(p.y)))]
                if under:
                    pins.append((metal, t.string, under[0].bbox().to_dtype(self.dbu)))
                else:
                    self.log("warning: %s text %s at %s on no metal" % (cellname, t.string, p))
        return pins

    def _internal_clusters(self, cellname, pins):
        """Connectivity inside a cell (diffusion cut by poly, poly, contact, M1, via1, M2) on a flat copy: per pin
        the cluster id and the cell's whole metal of that net {"M1": Region, "M2": Region} (cell coordinates)."""
        fl = db.Layout()
        fl.dbu = self.dbu
        c = fl.create_cell(cellname)
        c.copy_tree(self.ly.cell(cellname))
        c.flatten(-1, True)
        l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(fl, c, []))
        g = {}
        for k in ("diff", "poly", "cont", "m1", "via1", "m2"):
            li = fl.find_layer(*self.proc.LAYERS[k])
            g[k] = l2n.make_layer(li, k) if li is not None else l2n.make_layer(k)
        sd = g["diff"] - g["poly"]
        l2n.register(sd, "sd")
        for r in (sd, g["poly"], g["m1"], g["m2"]):
            l2n.connect(r)
        for a, b in ((sd, g["cont"]), (g["poly"], g["cont"]), (g["cont"], g["m1"]), (g["m1"], g["via1"]),
                     (g["via1"], g["m2"])):
            l2n.connect(a, b)
        l2n.extract_netlist()
        out = []
        for metal, name, box in pins:
            li = fl.find_layer(*self.proc.LAYERS[ROUTE_LAYERS[metal]])
            reg = (db.Region(c.begin_shapes_rec(li)) if li is not None else db.Region()) & \
                db.Region(box.to_itype(self.dbu))
            pt = reg.bbox().center() if not reg.is_empty() else box.to_itype(self.dbu).center()
            net = l2n.probe_net(g["m1" if metal == "M1" else "m2"], pt.to_dtype(self.dbu))
            if net is None:
                out.append((None, {metal: db.Region(box.to_itype(self.dbu))}))
                continue
            out.append((net.cluster_id, {"M1": l2n.shapes_of_net(net, g["m1"], True).merged(),
                                         "M2": l2n.shapes_of_net(net, g["m2"], True).merged()}))
        return out

    def collect_pins(self):
        """Block pins: dict(net, metal, box (top DBox), terms {"M1": Region, "M2": Region} (top, dbu), inst,
        cellpin, group). Pins already connected (inside a cell, or touching on one metal) share a group."""
        self.pins, gid = [], 0
        for inst, t in self.leaves.items():
            spec = self.instances[inst]
            pins = self.cell_pins(spec["cell"])
            it = self.itrans(t)
            group_of = {}
            for (metal, name, box), (cl, geo) in zip(pins, self._internal_clusters(spec["cell"], pins)):
                net = spec.get("nets", {}).get(name, name)
                terms = {m: r.transformed(it) for m, r in geo.items()}
                terms[metal] = (terms.get(metal, db.Region()) + db.Region(box.to_itype(self.dbu)).transformed(it)).merged()
                key = (net, cl) if cl is not None else (net, "p%d" % gid)
                if key not in group_of:
                    group_of[key], gid = gid, gid + 1
                self.pins.append(dict(net=net, metal=metal, box=box.transformed(t), terms=terms, inst=inst,
                                      cellpin=name, group=group_of[key]))
        for net, box, metal in self.rails:
            self.pins.append(dict(net=net, metal=metal, box=box, terms={metal: db.Region(box.to_itype(self.dbu))},
                                  inst="rail", cellpin=net, group=gid))
            gid += 1
        parent = list(range(gid))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        for i, p in enumerate(self.pins):
            for q in self.pins[i + 1:]:
                for m in ("M1", "M2"):
                    if m in p["terms"] and m in q["terms"] and not (p["terms"][m] & q["terms"][m]).is_empty():
                        if p["net"] != q["net"]:
                            raise ValueError("short on %s: %s.%s (%s) touches %s.%s (%s)" % (
                                m, p["inst"], p["cellpin"], p["net"], q["inst"], q["cellpin"], q["net"]))
                        parent[find(p["group"])] = find(q["group"])
        for p in self.pins:
            p["group"] = find(p["group"])
        return self.pins

    # ---- routing -------------------------------------------------------------------------------------------
    def route(self, order=None):
        opts = dict(self.ropt)
        keepout = opts.pop("keepout", [])
        opts.pop("scarce", None)
        names = [None] + self.nets
        idx = {n: i for i, n in enumerate(names)}
        px = [p["box"].center().x / self.dbu for p in self.pins if p["net"] in idx and p["inst"] != "rail"]
        py = [p["box"].center().y / self.dbu for p in self.pins if p["net"] in idx and p["inst"] != "rail"]
        gr = GridRouter(self.bbox, self.R, self.dbu, nets=len(names), extra_x=px, extra_y=py, **opts)
        self.router = gr
        # obstacles: everything in the top cell (primitives, utility cells, rails), tagged by net where a polygon
        # touches the terminal of a routed net; vias block vias
        for metal in ("M1", "M2"):
            terms = [(p["net"], p["terms"][metal]) for p in self.pins if metal in p["terms"] and p["net"] in idx]
            for poly in db.Region(self.top.begin_shapes_rec(self.LI[metal])).merged().each():
                pr = db.Region(poly)
                tags = {n for n, t in terms if not (t & pr).is_empty()}
                if len(tags) > 1:
                    raise ValueError("short on %s between %s" % (metal, sorted(tags)))
                gr.add_obstacle(metal, pr, idx[tags.pop()] if tags else 0)
        gr.add_via_obstacle(db.Region(self.top.begin_shapes_rec(self.LI["V1"])))
        for ko in keepout:   # (metal, (x0, y0, x1, y1)) or dict(metal, inst, box in cell coords, nets allowed)
            if isinstance(ko, dict):
                b = db.DBox(*ko["box"]).transformed(self.leaves[ko["inst"]])
                metals = [ko["metal"]] if isinstance(ko["metal"], str) else ko["metal"]
                allow = ko.get("nets", {p["net"] for p in self.pins if p["inst"] == ko["inst"]})
            else:
                metals, b, allow = [ko[0]], db.DBox(*ko[1]), set()
            for metal in metals:
                gr.add_keepout(metal, db.Region(b.to_itype(self.dbu)), {idx[n] for n in allow if n in idx})
        groups = {}
        for p in self.pins:
            if p["net"] in idx:
                groups.setdefault(p["net"], {}).setdefault(p["group"], []).append(p)
        todo = []
        for net in self.nets:
            g = groups.get(net, {})
            if len(g) + (1 if net in self.ports else 0) >= 2:
                est = self._mst_estimate(g)
                if net in self.ports:                  # plus the way from the nearest terminal to the port edge
                    bbs = [r.bbox() for ps in g.values() for p in ps for r in p["terms"].values()]
                    B = self.bbox.to_itype(self.dbu)
                    d = {"top": min(B.top - b.top for b in bbs), "bottom": min(b.bottom - B.bottom for b in bbs),
                         "left": min(b.left - B.left for b in bbs), "right": min(B.right - b.right for b in bbs)}
                    est += d[self.ports[net][0]] * self.dbu
                todo.append((est, net))
        # nets whose scarcest terminal has few free access nodes go first (they lose them to earlier nets)
        scarce = {}
        for est, net in todo:
            k = idx[net]
            counts = []
            for ps in groups.get(net, {}).values():
                nodes = set()
                for p in ps:
                    for m, reg in p["terms"].items():
                        nodes |= gr.terminal_nodes(m, reg, k) | gr.via_access_nodes(m, reg, k)
                counts.append(len(nodes))
            scarce[net] = min(counts) if counts else 0
        lim = self.ropt.get("scarce", 12)
        todo = [(0 if scarce[n] <= lim else 1, scarce[n] if scarce[n] <= lim else e, n) for e, n in todo]
        todo.sort()
        todo = [(e, n) for _, e, n in todo]
        self.scarce = scarce
        if order:
            todo = [(0, n) for n in order if any(n == t[1] for t in todo)] + [t for t in todo if t[1] not in order]
        self.route_log, failed = [], []
        for _, net in todo:
            k = idx[net]
            tg = []
            for gid, ps in sorted(groups.get(net, {}).items()):
                nodes = set()
                for p in ps:
                    for m, reg in p["terms"].items():
                        nodes |= gr.terminal_nodes(m, reg, k) | gr.via_access_nodes(m, reg, k)
                tg.append(("%s.%s" % (ps[0]["inst"], ps[0]["cellpin"]), nodes))
            if net in self.ports:
                side, rng = self.ports[net]
                tg.append(("port:" + side, gr.edge_nodes(side, rng, k)))
            empty = [n for n, s in tg if not s]
            if empty:
                failed.append((net, "no free access node at " + ", ".join(empty)))
                continue
            ok, info = gr.route_net(k, [s for _, s in tg], alt_last=net in self.ports)
            self.route_log.append((net, ok, info))
            if not ok:
                failed.append((net, info))
        self.failed = failed
        return failed

    def _mst_estimate(self, g):
        """Length estimate of a net: minimum spanning tree over its terminal groups, bbox-to-bbox distance."""
        bbs = []
        for ps in g.values():
            b = db.Box()
            for p in ps:
                for r in p["terms"].values():
                    b += r.bbox()
            bbs.append(b)
        if len(bbs) < 2:
            return 0.0

        def dist(a, b):
            return (max(0, max(a.left, b.left) - min(a.right, b.right)) +
                    max(0, max(a.bottom, b.bottom) - min(a.top, b.top))) * self.dbu
        inside, total = {0}, 0.0
        while len(inside) < len(bbs):
            d, j = min((dist(bbs[i], bbs[j]), j) for i in inside for j in range(len(bbs)) if j not in inside)
            inside.add(j)
            total += d
        return total

    def emit(self):
        """Wires (with same-net gap fill and landing patches), vias, port pins and rail pins into the top cell."""
        gr, R = self.router, self.R
        names = [None] + self.nets
        own = {}
        for p in self.pins:
            for m, reg in p["terms"].items():
                own.setdefault((p["net"], m), db.Region()).insert(reg)
        sp = {"M1": self.u(R["m1.space"]), "M2": self.u(R["m2.space"])}
        spw = {"M1": self.u(R["m1.wide_space"]), "M2": self.u(R["m2.wide_space"])}   # a patch may make it wide
        self.fills, self.patches, self.via_merges = {}, {}, []
        wires = {}
        dmin = self.u(R["via1.size"] + R["via1.space"])
        for k, net in enumerate(names):
            if k == 0:
                continue
            keep, bridges = [], []
            for r in gr.vias.get(k, []):
                x, y = gr.xl[r // gr.NY], gr.yl[r % gr.NY]
                near = [q for q in keep if abs(q[0] - x) < dmin and abs(q[1] - y) < dmin]
                if near:
                    q, h = near[0], gr.h
                    bridges.append(db.Box(min(x, q[0]) - h, min(y, q[1]) - h, max(x, q[0]) + h, max(y, q[1]) + h))
                    self.via_merges.append((net, (x * self.dbu, y * self.dbu)))
                else:
                    keep.append((x, y))
            gr.vias[k] = [int(gr.xs.searchsorted(x)) * gr.NY + int(gr.ys.searchsorted(y)) for x, y in keep]
            for metal in ("M1", "M2"):
                r = gr.wire_region(metal, k)
                for b in bridges:
                    r.insert(b)
                r.merge()
                if not r.is_empty():
                    wires[(k, metal)] = r
        allm = {}
        for metal in ("M1", "M2"):
            a = db.Region(self.top.begin_shapes_rec(self.LI[metal]))
            for (k, m), r in wires.items():
                if m == metal:
                    a += r
            allm[metal] = a.merged()
        for (k, metal), r in list(wires.items()):
            net = names[k]
            c = own.get((net, metal), db.Region()).merged()
            if c.is_empty():
                continue
            mine = (r + c).merged()
            other = allm[metal] - mine
            L0 = 0 if metal == "M1" else 1
            add = db.Region()
            for path in gr.paths.get(k, []):
                for n in path:
                    L, b = gr.node_box(n)
                    if L != L0:
                        continue
                    sq = db.Region(b)
                    if (c & sq).is_empty() or (sq - c).is_empty():
                        continue
                    for ex, ey in ((gr.h, gr.h), (gr.h, 0), (0, gr.h)):     # full, along x, along y
                        pb = ((c & db.Region(b.enlarged(ex, ey))) + sq).bbox()
                        patch = db.Region(pb) - mine
                        if patch.is_empty():
                            break
                        if (patch.sized(spw[metal]) & other).is_empty():
                            add.insert(pb)
                            break
            if not add.is_empty():
                self.patches[(net, metal)] = add.count()
                wires[(k, metal)] = (r + add).merged()
        # same-net gaps < space rule (router wire / patch vs. own cell metal or own wire): fill them (closing);
        # no other net can sit in such a gap without violating its own spacing. After the patches, so that the
        # notches a patch leaves are filled too.
        for (k, metal), r in list(wires.items()):
            c = own.get((names[k], metal), db.Region())
            both = (r + c).merged()
            d = sp[metal] // 2 + self.u(R["grid"])
            fill = (both.sized(d).sized(-d) - both).interacting(r)
            if not fill.is_empty():
                self.fills[(names[k], metal)] = fill.area() * self.dbu ** 2
                wires[(k, metal)] = (r + fill).merged()
        # necks: a wire end that stops short of same-net cell metal by less than the space rule gets the gap filled
        # above, but where the two only overlap by a sliver (a pad corner) the fill is narrower than the width rule.
        # Widen every such neck to the width rule (a box centred on the neck), where the spacing to other nets allows.
        # (bg_core_pd 2026-10-28: a via pad 0.075 um beside a pnp emitter pad's corner left a 0.035 um neck.)
        self.necks = []
        gq = self.u(R["grid"])
        allm = {}
        for metal in ("M1", "M2"):
            a = db.Region(self.top.begin_shapes_rec(self.LI[metal]))
            for (k, m), r in wires.items():
                if m == metal:
                    a += r
            allm[metal] = a.merged()
        for (k, metal), r in list(wires.items()):
            c = own.get((names[k], metal), db.Region())
            both = (r + c).merged()
            wmin = self.u(R["m1.width" if metal == "M1" else "m2.width"])
            other = allm[metal] - both
            add = db.Region()
            for ep in both.width_check(wmin).each():
                b = ep.bbox()
                if (db.Region(b.enlarged(1, 1)) & r).is_empty():
                    continue                                    # a cell's own geometry, not a router neck
                w, h = max(b.width(), wmin), max(b.height(), wmin)
                cx, cy = (b.left + b.right) // 2, (b.bottom + b.top) // 2
                nb = db.Box((cx - w // 2) // gq * gq, (cy - h // 2) // gq * gq,
                            -(-(cx + w - w // 2) // gq) * gq, -(-(cy + h - h // 2) // gq) * gq)
                if (db.Region(nb).sized(sp[metal]) & other).is_empty():
                    add.insert(nb)
                    self.necks.append((names[k], metal, nb.to_dtype(self.dbu)))
            if not add.is_empty():
                wires[(k, metal)] = (r + add).merged()
        # minimum area (m1.area / m2.area): router pieces that touch no cell metal of their net and are too small
        # (e.g. an edge pin reached by a via) grow along their long side where the spacing allows
        amin = {"M1": R["m1.area"], "M2": R["m2.area"]}
        self.area_fixes = []
        for (k, metal), r in list(wires.items()):
            c = own.get((names[k], metal), db.Region())
            extra = r.dup()
            if (k in gr.ports) and metal == "M2":
                extra.insert(gr.ports[k][1])
            pieces = extra.merged()
            other = allm[metal] - (pieces + c).merged()
            add = db.Region()
            for poly in pieces.each():
                pr = db.Region(poly)
                if not (pr & c).is_empty() or poly.area() * self.dbu ** 2 >= amin[metal]:
                    continue
                b = poly.bbox()
                horiz = b.width() >= b.height()
                gq = self.u(R["grid"])
                need = self.u(amin[metal] / ((b.height() if horiz else b.width()) * self.dbu)) - \
                    (b.width() if horiz else b.height()) + gq
                need = -(-need // gq) * gq                                   # on the grid
                # the short side as well (bg_core_pd: a port pin boxed in between a wire and the block edge)
                need2 = self.u(amin[metal] / ((b.width() if horiz else b.height()) * self.dbu)) - \
                    (b.height() if horiz else b.width()) + gq
                need2 = -(-need2 // gq) * gq
                cands = (((need, 0, 0, 0), (0, 0, need, 0), (0, need2, 0, 0), (0, 0, 0, need2)) if horiz else
                         ((0, need, 0, 0), (0, 0, 0, need), (need2, 0, 0, 0), (0, 0, need2, 0)))
                for dx0, dy0, dx1, dy1 in cands:
                    nb = db.Box(b.left - dx0, b.bottom - dy0, b.right + dx1, b.top + dy1)
                    if nb.left < self.router.bb.left or nb.right > self.router.bb.right or \
                            nb.bottom < self.router.bb.bottom or nb.top > self.router.bb.top:
                        continue
                    if (db.Region(nb).sized(sp[metal]) & other).is_empty():
                        add.insert(nb)
                        self.area_fixes.append((names[k], metal, nb.to_dtype(self.dbu)))
                        break
            if not add.is_empty():
                wires[(k, metal)] = (r + add).merged()
        for (k, metal), r in wires.items():
            self.top.shapes(self.LI[metal]).insert(r)
        for k in range(1, len(names)):
            v = gr.via_region(k)
            if not v.is_empty():
                self.top.shapes(self.LI["V1"]).insert(v)
        for net, (side, rng) in self.ports.items():
            pb = gr.port_pin_box(names.index(net), side)
            if pb is None:
                continue
            for key in ("M2", "M2pin"):
                self.top.shapes(self.LI[key]).insert(pb)
            c = pb.center()
            self.top.shapes(self.LI["M2txt"]).insert(db.Text(net, c.x, c.y))
            self.port_pins[net] = pb.to_dtype(self.dbu)
        for net, box, metal in self.rails:
            self.top.shapes(self.LI[metal + "pin"]).insert(box)
            c = box.center()
            self.top.shapes(self.LI[metal + "txt"]).insert(db.DText(net, c.x, c.y))
        for key, reg in self.extra:
            self.top.shapes(self.L[key]).insert(reg)

    # ---- checks and utilities ------------------------------------------------------------------------------
    def latchup(self):
        """Device diffusion farther than the adapter's LU distances from a tie of its well / substrate, measured
        inside the well, grown in the adapter's LU_STEP steps (the way the process deck measures it).
        Returns {kind: (area um2, boxes)}."""
        reg = {k: self.region(k) for k in ("diff", "poly", "pimp", "nwell")}
        dv = self.proc.derive(reg)
        step = self.proc.LU_STEP
        chip = db.Region(self.top.bbox()).sized(self.u(max(self.R["lu.ntap_dist"], self.R["lu.ptap_dist"])))

        def uncovered(dev, ties, well, dist):
            reach = ties.dup()
            for _ in range(int(round(dist / step))):
                reach = (reach.sized(self.u(step)) & well) | reach
            return dev - reach
        out = {}
        for kind, dev, tie, well, dist in (("pmos/ntap", dv["pdiff_dev"], dv["ntap"], dv["nwell"], self.R["lu.ntap_dist"]),
                                           ("nmos/ptap", dv["ndiff_dev"], dv["ptap"], chip - dv["nwell"], self.R["lu.ptap_dist"])):
            u = uncovered(dev, tie, well, dist)
            out[kind] = (u.area() * self.dbu ** 2, [p.bbox().to_dtype(self.dbu) for p in u.each()][:6])
        return out

    def point_image(self, inst, layers, select, name):
        """Point image (R180 about the well / bbox centre of the instance's cell) of the cell's own shapes on
        `layers` (generic names) chosen by select(layer, DBox in cell coordinates); placed as a new cell `name`
        with the instance's transformation. Use: make a point-symmetric array's wiring point-symmetric too."""
        c = self.ly.cell(self.instances[inst]["cell"])
        cb = self.region("nwell", c).bbox()
        if cb.empty():
            cb = c.bbox()
        cx, cy = (cb.left + cb.right) // 2, (cb.bottom + cb.top) // 2
        img = self.ly.create_cell(name)
        T = db.Trans(db.Trans.R180, db.Vector(2 * cx, 2 * cy))
        for lk in layers:
            for s in c.shapes(self.L[lk]).each():
                if not s.is_text() and select(lk, s.dbbox()):
                    img.shapes(self.L[lk]).insert(s.polygon.transformed(T))
        self.top.insert(db.DCellInstArray(img.cell_index(), self.leaves[inst]))
        return img

    def stretch_rails(self):
        """Rails span the final block width (ties may have widened the block after placement); the block is then
        moved so that its lower left corner is the origin."""
        bb = self.top.dbbox()
        new = []
        for net, box, metal in self.rails:
            nb = db.DBox(bb.left, box.bottom, bb.right, box.top)
            if nb != box:
                self.top.shapes(self.LI[metal]).insert(nb)
            new.append((net, nb, metal))
        self.rails = new
        if abs(bb.left) > 1e-9 or abs(bb.bottom) > 1e-9:
            t = db.DTrans(db.DVector(-bb.left, -bb.bottom))
            self.top.transform(t)
            self.leaves = {k: t * v for k, v in self.leaves.items()}
            self.rails = [(n, b.transformed(t), m) for n, b, m in self.rails]
            self.taps = [(k, n, d.transformed(t)) for k, n, d in self.taps]

    def write(self, path):
        opt = db.SaveLayoutOptions()
        opt.gds2_write_timestamps = False
        self.ly.write(path, opt)

    def report(self):
        bb = self.top.dbbox()
        area = bb.width() * bb.height()
        A = lambda r: r.area() * self.dbu ** 2
        diff, poly = self.region("diff"), self.region("poly")
        gate = diff & poly
        mos = diff.interacting(gate)
        top_layers = sorted({"%d/%d" % (self.ly.get_info(li).layer, self.ly.get_info(li).datatype)
                             for li in self.ly.layer_indexes() if not self.top.shapes(li).is_empty()})
        wl = {}
        if hasattr(self, "router"):
            for k, net in enumerate(self.nets, 1):
                wl[net] = self.router.stats(k)
        return dict(bbox=(bb.left, bb.bottom, bb.right, bb.top), w=bb.width(), h=bb.height(), area=area,
                    gate_area=A(gate), mos_act_area=A(mos), util_gate=A(gate) / area, util_mos=A(mos) / area,
                    top_layers=top_layers, wires=wl, failed=getattr(self, "failed", None),
                    nwell_fill=A(getattr(self, "wellfill", db.Region())), taps=len(self.taps))


# ------------------------------------------------------------------------------------------------------------
# grid router
# ------------------------------------------------------------------------------------------------------------
class GridRouter:
    """Two-metal router (lower = 0, upper = 1) on a non-uniform grid: regular lines at `pitch` plus the centre lines
    of the pins (a node can sit exactly on a minimum-pitch track). Node squares are width x width; wires and pads
    are unions of node squares. A node is free for net k if its square keeps the spacing to every shape of another
    net: cell metal (space; wide_space next to the parts wider than wide_width), router wires (space)."""

    def __init__(self, bbox, rules, dbu, pitch=None, width=None, margin=None, pref=("H", "V"), nonpref=1.6,
                 via_cost=6.0, turn_cost=1.5, nets=64, extra_x=(), extra_y=()):
        self.R, self.dbu = rules, dbu
        u = lambda v: int(round(v / dbu))
        self.u = u
        up = lambda v: math.ceil(round(v / rules["grid"], 6)) * rules["grid"]
        s_max = max(rules["m1.space"], rules["m2.space"], rules["m1.wide_space"], rules["m2.wide_space"])
        if width is None:          # wire = via pad: via + end enclosure on both sides, at least the metal widths
            width = up(max(rules["m1.width"], rules["m2.width"], rules["via1.size"] + 2 * rules["via1.enc_end"]))
        if pitch is None:          # two pitches - one wire >= the widest space rule (merged same-net wires)
            pitch = up((width + s_max) / 2)
        if margin is None:         # half the widest space to the block edge (an abutting block does the same)
            margin = up(s_max / 2)
        self.P, self.W, self.h, self.margin = u(pitch), u(width), u(width / 2), u(margin)
        g = u(rules["grid"])
        bb = bbox.to_itype(dbu)
        self.bb = bb
        snap = lambda v: int(math.ceil(v / g) * g)
        lox, hix = snap(bb.left + self.margin + self.h), bb.right - self.margin - self.h
        loy, hiy = snap(bb.bottom + self.margin + self.h), bb.top - self.margin - self.h
        xs = set(range(lox, hix + 1, self.P)) | {int(round(x / g)) * g for x in extra_x if lox <= x <= hix}
        ys = set(range(loy, hiy + 1, self.P)) | {int(round(y / g)) * g for y in extra_y if loy <= y <= hiy}
        self.xs, self.ys = np.array(sorted(xs), dtype=np.int64), np.array(sorted(ys), dtype=np.int64)
        self.xl, self.yl = self.xs.tolist(), self.ys.tolist()
        self.NX, self.NY = len(self.xs), len(self.ys)
        self.N = self.NX * self.NY
        self.pref, self.nonpref, self.via_cost, self.turn_cost = pref, nonpref, via_cost, turn_cost
        self.mask = np.zeros((nets, 2, self.NX, self.NY), dtype=bool)   # mask[k]: nodes net k makes unusable
        self.viablk = np.zeros((self.NX, self.NY), dtype=bool)
        self.paths, self.vias, self.ports, self.va = {}, {}, {}, {}
        self.keepouts = []
        self.s_narrow = (u(rules["m1.space"]), u(rules["m2.space"]))
        self.s_wide = (u(rules["m1.wide_space"]), u(rules["m2.wide_space"]))
        self.w_wide = (u(rules["m1.wide_width"]), u(rules["m2.wide_width"]))
        self.min_ov = u(rules["via1.enc_end"])          # minimum landing overlap = the via end enclosure
        assert self.W >= u(max(rules["m1.width"], rules["m2.width"])), "wire narrower than the metal width rule"
        assert self.h - u(rules["via1.size"] / 2) >= u(rules["via1.enc_end"]), "pad too small for the via end enclosure"
        assert 2 * self.P - self.W >= max(self.s_narrow), "pitch too small for the metal space rule"

    def _rng(self, arr, lo, hi):
        return int(np.searchsorted(arr, lo, side="right")), int(np.searchsorted(arr, hi, side="left")) - 1

    def _raster_box(self, b, bloat, out):
        i0, i1 = self._rng(self.xs, b.left - bloat, b.right + bloat)
        j0, j1 = self._rng(self.ys, b.bottom - bloat, b.top + bloat)
        if i0 <= i1 and j0 <= j1:
            out[i0:i1 + 1, j0:j1 + 1] = True

    def _raster(self, reg, bloat, out):
        for poly in reg.each():
            for tz in poly.decompose_trapezoids(db.Polygon.TD_htrapezoids):
                self._raster_box(tz.bbox(), bloat, out)

    def add_obstacle(self, metal, reg, k):
        L = 0 if metal == "M1" else 1
        ww = self.w_wide[L]
        wide = reg.sized(-(ww // 2)).sized(ww // 2) & reg
        blk = np.zeros((self.NX, self.NY), dtype=bool)
        self._raster(reg, self.s_narrow[L] + self.h, blk)
        self._raster(wide, self.s_wide[L] + self.h, blk)
        self.mask[k, L] |= blk

    def add_keepout(self, metal, reg, allow):
        """Region closed to every net except the indices in `allow` (e.g. no foreign net over a matched array;
        the array's own nets may still reach their pins through it)."""
        L = 0 if metal == "M1" else 1
        blk = np.zeros((self.NX, self.NY), dtype=bool)
        self._raster(reg, self.h, blk)
        self.keepouts.append((L, blk, set(allow)))

    def add_via_obstacle(self, reg):
        self._raster(reg, self.u(self.R["via1.space"]) + self.u(self.R["via1.size"] / 2), self.viablk)

    def free(self, k):
        f = (self.mask.sum(axis=0) - self.mask[k]) == 0
        for L, blk, allow in self.keepouts:
            if k not in allow:
                f[L] &= ~blk
        return f

    def nid(self, L, i, j):
        return (L * self.NX + i) * self.NY + j

    def terminal_nodes(self, metal, term, k):
        L = 0 if metal == "M1" else 1
        hit = np.zeros((self.NX, self.NY), dtype=bool)
        self._raster(term, self.h - self.min_ov, hit)
        hit &= self.free(k)[L]
        ii, jj = np.nonzero(hit)
        return {self.nid(L, int(i), int(j)) for i, j in zip(ii, jj)}

    def via_access_nodes(self, metal, term, k):
        """Nodes on the OTHER metal where a via fits inside the cell metal `term` (enclosure via1.enc all round and
        via1.enc_end on two opposite sides from the cell metal itself): land there with a via and no pad on
        `metal` (narrow pins, e.g. a gate column narrower than the router pad)."""
        L = 1 if metal == "M1" else 0
        a = self.u(self.R["via1.size"] / 2)
        c, c1 = self.u(self.R["via1.enc"]), self.u(self.R["via1.enc_end"])
        free = self.free(k)[L] & ~self.viablk
        out = set()
        bb = term.bbox()
        i0, i1 = self._rng(self.xs, bb.left, bb.right)
        j0, j1 = self._rng(self.ys, bb.bottom, bb.top)
        for i in range(max(i0, 0), i1 + 1):
            for j in range(max(j0, 0), j1 + 1):
                if not free[i, j]:
                    continue
                x, y = self.xl[i], self.yl[j]
                ex = db.Region(db.Box(x - a - c1, y - a - c, x + a + c1, y + a + c))
                ey = db.Region(db.Box(x - a - c, y - a - c1, x + a + c, y + a + c1))
                if (ex - term).is_empty() or (ey - term).is_empty():
                    n = self.nid(L, i, j)
                    out.add(n)
                    self.va.setdefault(k, set()).add(n)
        return out

    def edge_nodes(self, side, rng, k):
        f = self.free(k)[1]
        out = set()
        if side in ("top", "bottom"):
            j = self.NY - 1 if side == "top" else 0
            for i in range(self.NX):
                if f[i, j] and (rng is None or rng[0] <= self.xl[i] * self.dbu <= rng[1]):
                    out.add(self.nid(1, i, j))
        else:
            i = self.NX - 1 if side == "right" else 0
            for j in range(self.NY):
                if f[i, j] and (rng is None or rng[0] <= self.yl[j] * self.dbu <= rng[1]):
                    out.add(self.nid(1, i, j))
        return out

    def route_net(self, k, groups, alt_last=False):
        """groups: node sets, one per terminal; alt_last: the last set holds alternatives (an edge port): only the
        node reached joins the tree."""
        alt = groups[-1] if alt_last else None
        fb = self.free(k).reshape(-1).tobytes()
        vb = (~self.viablk).reshape(-1).tobytes()
        tree = set(groups[0])
        rest = [g if g is alt else set(g) for g in groups[1:]]
        paths, vias = [], []
        while rest:
            path = self._astar(tree, set().union(*rest), fb, vb)
            if path is None:
                return False, "no path to %d of %d terminal groups" % (len(rest), len(groups) - 1)
            end = path[-1]
            for g in rest:
                if end in g:
                    rest.remove(g)
                    tree |= {end} if g is alt else g
                    break
            tree |= set(path)
            paths.append(path)
            vias += [a % self.N for a, b in zip(path[:-1], path[1:]) if a // self.N != b // self.N]
            vias += [n % self.N for n in {path[0], path[-1]} if n in self.va.get(k, ())]
        self.paths.setdefault(k, []).extend(paths)
        self.vias.setdefault(k, []).extend(vias)
        self._commit(k, paths, vias)
        return True, "%d branches, %d vias" % (len(paths), len(vias))

    def _astar(self, sources, targets, fb, vb):
        NX, NY, N, P = self.NX, self.NY, self.N, float(self.P)
        xl, yl = self.xl, self.yl
        INF = float("inf")
        D = np.full((NX, NY), np.inf)                    # exact L1 distance to the nearest target (admissible)
        for t in targets:
            rem = t % N
            D[rem // NY, rem % NY] = 0.0
        dx, dy = np.diff(self.xs).astype(float), np.diff(self.ys).astype(float)
        for i in range(1, NX):
            np.minimum(D[i], D[i - 1] + dx[i - 1], out=D[i])
        for i in range(NX - 2, -1, -1):
            np.minimum(D[i], D[i + 1] + dx[i], out=D[i])
        for j in range(1, NY):
            np.minimum(D[:, j], D[:, j - 1] + dy[j - 1], out=D[:, j])
        for j in range(NY - 2, -1, -1):
            np.minimum(D[:, j], D[:, j + 1] + dy[j], out=D[:, j])
        Hl = (D / P).reshape(-1).tolist()
        cost = {(L, d): (1.0 if self.pref[L] == d else self.nonpref) for L in (0, 1) for d in ("H", "V")}
        best, parent, heap = {}, {}, []
        for s in sources:
            if fb[s]:
                best[s * 5 + 4] = 0.0
                heapq.heappush(heap, (Hl[s % N], 0.0, s * 5 + 4))
        tc, vc = self.turn_cost, self.via_cost
        while heap:
            f, g, st = heapq.heappop(heap)
            if g > best.get(st, INF):
                continue
            node, d = divmod(st, 5)
            if node in targets:
                path = [node]
                while st in parent:
                    st = parent[st]
                    if st // 5 != path[-1]:
                        path.append(st // 5)
                path.reverse()
                return path
            L, rem = divmod(node, N)
            i, j = divmod(rem, NY)
            for nd, di, dj in ((0, 1, 0), (1, -1, 0), (2, 0, 1), (3, 0, -1)):
                ni, nj = i + di, j + dj
                if ni < 0 or nj < 0 or ni >= NX or nj >= NY:
                    continue
                nn = node + di * NY + dj
                if not fb[nn]:
                    continue
                c = (abs(xl[ni] - xl[i]) / P * cost[(L, "H")]) if nd < 2 else (abs(yl[nj] - yl[j]) / P * cost[(L, "V")])
                if d != 4 and d != nd:
                    c += tc
                ng, ns = g + c, nn * 5 + nd
                if ng < best.get(ns, INF):
                    best[ns], parent[ns] = ng, st
                    heapq.heappush(heap, (ng + Hl[nn % N], ng, ns))
            on = (1 - L) * N + rem
            if fb[on] and vb[rem]:
                ng, ns = g + vc, on * 5 + 4
                if ng < best.get(ns, INF):
                    best[ns], parent[ns] = ng, st
                    heapq.heappush(heap, (ng + Hl[rem], ng, ns))
        return None

    def _commit(self, k, paths, vias):
        for path in paths:
            for n in path:
                L, b = self.node_box(n)
                self._raster_box(b, self.s_narrow[L] + self.h, self.mask[k, L])
        a = self.u(self.R["via1.size"] / 2)
        for rem in vias:
            x, y = self.xl[rem // self.NY], self.yl[rem % self.NY]
            self._raster_box(db.Box(x - a, y - a, x + a, y + a), self.u(self.R["via1.space"]) + a, self.viablk)

    def node_box(self, n):
        L, rem = divmod(n, self.N)
        x, y = self.xl[rem // self.NY], self.yl[rem % self.NY]
        return L, db.Box(x - self.h, y - self.h, x + self.h, y + self.h)

    def wire_region(self, metal, k):
        L0 = 0 if metal == "M1" else 1
        r = db.Region()
        for path in self.paths.get(k, []):
            for n in path:
                L, b = self.node_box(n)
                if L == L0:
                    r.insert(b)
        if L0 == 1 and k in self.ports:
            r.insert(self.ports[k][1])
        return r.merged()

    def via_region(self, k):
        r = db.Region()
        a = self.u(self.R["via1.size"] / 2)
        for rem in self.vias.get(k, []):
            x, y = self.xl[rem // self.NY], self.yl[rem % self.NY]
            r.insert(db.Box(x - a, y - a, x + a, y + a))
        return r

    def port_pin_box(self, k, side):
        """The edge node net k reached: its square extended to the block edge (the pin box)."""
        for path in self.paths.get(k, []):
            for n in (path[0], path[-1]):
                L, rem = divmod(n, self.N)
                i, j = divmod(rem, self.NY)
                hit = ((side == "top" and j == self.NY - 1) or (side == "bottom" and j == 0) or
                       (side == "right" and i == self.NX - 1) or (side == "left" and i == 0))
                if L == 1 and hit:
                    x, y, b, h = self.xl[i], self.yl[j], self.bb, self.h
                    box = {"top": db.Box(x - h, y - h, x + h, b.top), "bottom": db.Box(x - h, b.bottom, x + h, y + h),
                           "right": db.Box(x - h, y - h, b.right, y + h), "left": db.Box(b.left, y - h, x + h, y + h)}[side]
                    self.ports[k] = ((i, j), box)
                    return box
        return None

    def stats(self, k):
        n = {0: 0, 1: 0}
        for path in self.paths.get(k, []):
            for a, b in zip(path[:-1], path[1:]):
                if a // self.N == b // self.N:
                    L, ba = self.node_box(a)
                    _, bb_ = self.node_box(b)
                    n[L] += abs(ba.left - bb_.left) + abs(ba.bottom - bb_.bottom)
        return dict(M1=round(n[0] * self.dbu, 2), M2=round(n[1] * self.dbu, 2), vias=len(self.vias.get(k, [])))


# ------------------------------------------------------------------------------------------------------------
# driver, self-test
# ------------------------------------------------------------------------------------------------------------
def build(cfg, out=None, log=print):
    """cfg: NAME, SOURCES, INSTANCES, FLOORPLAN, NETS, PROCESS (adapter path or module); optional PORTS,
    PIN_OVERRIDES, ROUTER, DRC, MERGE_WELLS, PRE_ROUTE / POST_ROUTE (callable(block)), ROUTE_ORDER."""
    proc = cfg["PROCESS"] if not isinstance(cfg["PROCESS"], str) else load_process(cfg["PROCESS"])
    blk = Block(cfg["NAME"], cfg["SOURCES"], cfg["INSTANCES"], cfg["FLOORPLAN"], proc, cfg["NETS"],
                cfg.get("PORTS"), cfg.get("PIN_OVERRIDES"), cfg.get("ROUTER"), cfg.get("DRC"),
                cfg.get("MERGE_WELLS", False), cfg.get("KEEP_CELLS", ()), log)
    blk.place()
    if cfg.get("TAP_SEGMENTS"):
        blk.add_tap_segments(cfg["TAP_SEGMENTS"])
    blk.wellfill = blk._well_fill(blk.top) if blk.merge_wells else db.Region()
    blk.stretch_rails()
    blk.bbox = blk.top.dbbox()
    ns = blk._label_shorts(blk.top, blk.rails)     # pairwise gap trials cannot see a cell bridging two seams
    if ns:
        raise ValueError("placement shorts %d metal polygon(s) carrying two nets (e.g. a cell touching both rails): "
                         "increase the gaps" % ns)
    if cfg.get("PRE_ROUTE"):
        cfg["PRE_ROUTE"](blk)
    blk.collect_pins()
    failed = blk.route(cfg.get("ROUTE_ORDER"))
    blk.emit()
    if cfg.get("POST_ROUTE"):
        cfg["POST_ROUTE"](blk)
    if out:
        blk.write(out)
    rep = blk.report()
    rep["latchup"] = blk.latchup()
    log("block %s: %.3f x %.3f um = %.1f um2; gate %.1f um2 (%.1f %%), MOS diffusion %.1f um2 (%.1f %%)"
        % (cfg["NAME"], rep["w"], rep["h"], rep["area"], rep["gate_area"], 100 * rep["util_gate"],
           rep["mos_act_area"], 100 * rep["util_mos"]))
    log("layers drawn in the top cell: " + " ".join(rep["top_layers"]) + "; well fill %.2f um2, tap stripes %d"
        % (rep["nwell_fill"], rep["taps"]))
    for kind, (a, boxes) in rep["latchup"].items():
        log("latch-up %s: %s" % (kind, "all device diffusion within reach" if a == 0 else
                                 "%.2f um2 out of reach, e.g. %s" % (a, boxes[:3])))
    for net, st in rep["wires"].items():
        if st["M1"] or st["M2"]:
            log("  %-10s M1 %6.2f um  M2 %6.2f um  vias %d" % (net, st["M1"], st["M2"], st["vias"]))
    for net, why in failed:
        log("  UNROUTED %s: %s" % (net, why))
    return blk, rep


def load_config(path):
    cfg = {"__file__": path, "__name__": "config"}
    exec(compile(open(path).read(), path, "exec"), cfg)
    return cfg


def selftest(proc, out, drc=None):
    """Porting self-test: two tiny pin cells, an obstacle between them, rails with n / p tie stripes over a well
    patch; routed and written to `out`. The new PDK's own DRC and LVS (two nets a, b plus vdd / vss) must pass."""
    R = proc.rules()
    tie = max(R["diff.width"], R["cont.size"] + 2 * R["cont.enc_diff"])
    enc = max(R[proc.TAPS["n"]["well_enc"]], R[proc.TAPS["p"]["implant_enc"]])
    rail_h = round(math.ceil((tie + 2 * enc + 4 * R["m1.space"]) / R["grid"]) * R["grid"], 6)
    ly = db.Layout()
    ly.dbu = 0.001
    L = {k: ly.layer(*v) for k, v in proc.LAYERS.items() if isinstance(v, tuple)}
    cells = {}
    for name, net in (("pinA", "a"), ("pinB", "a"), ("pinC", "b"), ("pinD", "b")):
        c = ly.create_cell(name)
        c.shapes(L["m1"]).insert(db.DBox(0, 0, 1.0, 1.0))
        c.shapes(L["m1.pin"]).insert(db.DBox(0, 0, 1.0, 1.0))
        c.shapes(L["m1.text"]).insert(db.DText(net, 0.5, 0.5))
        cells[name] = c
    wall = ly.create_cell("wall")
    wall.shapes(L["m1"]).insert(db.DBox(0, 0, 0.5, 6.0))
    tmp = out + ".src.gds"
    ly.write(tmp)
    cfg = dict(NAME="selftest", SOURCES={"s": tmp}, PROCESS=proc, NETS=["a", "b", "vdd", "vss"],
               INSTANCES={"A": dict(cell="pinA"), "B": dict(cell="pinB"), "C": dict(cell="pinC"),
                          "D": dict(cell="pinD"), "W": dict(cell="wall")},
               FLOORPLAN="V gap=%g\n  rail vdd h=%g tap=n\n  H gap=2,2,2,2 align=center\n    cell A\n    cell C\n"
                         "    cell W\n    cell B\n    cell D\n  rail vss h=%g tap=p\n" % (2 * R["m1.wide_space"], rail_h, rail_h),
               PORTS={"b": ("top", None)}, DRC=drc)
    return build(cfg, out)



TERMINALS = {"M": 4, "R": 2, "Q": 3, "C": 2, "D": 2}    # SPICE element letter -> node count (SPICE convention)


def compose_reference(name, ports, instances, cdl_files, ties=None, extra=()):
    """Reference netlist for LVS from the primitives' own netlists: every instance's subckt (found in
    cdl_files) is flattened in, its ports mapped through the instance's net map (default: same name), its
    internal nets prefixed with the instance name, nets in `ties` renamed (e.g. a tap-less cell's internal bulk
    {"nw": "vdd"} where the parent's merged well ties it). extra: further device lines. Returns CDL text.
    Element lines M (4 nodes), R (2), Q (3), C (2), D (2) are flattened (TERMINALS); anything else is an error.
    (bg_core_pd, 2026-10-28: R and Q lines added for the bandgap's rhigh array and pnp core.)"""
    ties = ties or {}
    subs = {}
    for f in cdl_files:
        cur = None
        for raw in open(f):
            line = raw.strip()
            if not line or line.startswith("*"):
                continue
            tok = line.split()
            if tok[0].upper() == ".SUBCKT":
                cur = tok[1]
                subs[cur] = (tok[2:], [])
            elif tok[0].upper() == ".ENDS":
                cur = None
            elif cur is not None:
                if line.startswith("+"):
                    subs[cur][1][-1] += " " + line[1:].strip()
                else:
                    subs[cur][1].append(line)
    out = [".SUBCKT %s %s" % (name, " ".join(ports))]
    for inst, spec in instances.items():
        cell = spec["cell"]
        if cell not in subs:
            raise ValueError("no subckt %s in %s" % (cell, cdl_files))
        pins, lines = subs[cell]
        nmap = spec.get("nets", {})
        out.append("* %s: %s" % (inst, cell))
        for line in lines:
            tok = line.split()
            letter = tok[0][0].upper()
            if letter not in TERMINALS:
                raise ValueError("element %s not flattened here (TERMINALS): %s" % (letter, line))
            nn = TERMINALS[letter]

            def net(n):
                if n in ties:
                    return ties[n]
                if n in pins:
                    return nmap.get(n, n)
                return "%s.%s" % (inst, n)
            out.append(" ".join(["%s%s_%s" % (letter, inst, tok[0][1:])] + [net(n) for n in tok[1:1 + nn]] +
                                tok[1 + nn:]))
    out += list(extra)
    out.append(".ENDS %s" % name)
    return "\n".join(out) + "\n"

if __name__ == "__main__":
    import sys
    blk, rep = build(load_config(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else None)
    sys.exit(1 if rep["failed"] else 0)
