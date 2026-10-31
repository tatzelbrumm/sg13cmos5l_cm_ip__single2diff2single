# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Shared helpers for agent F's cells (C2, 2026-10-31): layer map, rule values from the PDK json, drawing helpers.
Rule values: /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json
(key named at each use). Layers: sg13cmos5l_maximal.drc layer definitions; pin convention of pad_buffer_cells.gds."""
import json
import klayout.db as db

PDK = "/foss/pdks/ihp-sg13cmos5l"
RULES = json.load(open(PDK + "/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json"))["drc_rules"]
LIB = "/home/user/c2/F/inputs/repo/macros/IOPad/layout/klayout/pad_buffer_cells.gds"
PAD = ("/home/user/c2/F/inputs/repo/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/"
       "sg13cmos5l_IOPadDiff2Single.klay.gds")
LAY = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25),
       "M2": (10, 0), "M2pin": (10, 2), "M2txt": (10, 25), "pSD": (14, 0), "Via1": (19, 0), "NWell": (31, 0),
       "TGO": (44, 0), "Via2": (29, 0), "M3": (30, 0), "M3pin": (30, 2), "M3txt": (30, 25), "Sub": (40, 0), "TEXT": (63, 0)}


def g5(v):
    """snap to the 5 nm grid (json 'grid' 0.005, geometry/3_1_offgrid.drc)"""
    return round(round(v / 0.005) * 0.005, 4)


class Drawer:
    def __init__(self, ly, cell):
        self.ly, self.c = ly, cell
        self.L = {k: ly.layer(*v) for k, v in LAY.items()}

    def box(self, lay, x0, y0, x1, y1):
        self.c.shapes(self.L[lay]).insert(db.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))

    def poly(self, lay, pts):
        self.c.shapes(self.L[lay]).insert(db.DPolygon([db.DPoint(g5(x), g5(y)) for x, y in pts]))

    def via1(self, x, y):           # V1_a 0.19
        a = RULES["V1_a"] / 2
        self.box("Via1", x - a, y - a, x + a, y + a)

    def via2(self, x, y):           # Vn_a 0.19
        a = RULES["Vn_a"] / 2
        self.box("Via2", x - a, y - a, x + a, y + a)

    def cont(self, x, y):           # Cnt_a 0.16
        a = RULES["Cnt_a"] / 2
        self.box("Cont", x - a, y - a, x + a, y + a)

    def pin(self, metal, net, x0, y0, x1, y1):
        self.box(metal + "pin", x0, y0, x1, y1)
        self.c.shapes(self.L[metal + "txt"]).insert(db.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))

    def note(self, text, x, y):
        self.c.shapes(self.L["TEXT"]).insert(db.DText(text, g5(x), g5(y)))

    def ptie(self, x0, y0, x1, y1, horizontal):
        """p+ substrate tie: Activ, pSD enclosure 0.03 (as the SG13_dev ptap1 cell), one contact row at Cnt_a + Cnt_b
        pitch with Cnt_c 0.07 enclosure, Metal1 over it. No Substrate 40/0 (tie extraction off, as A3)."""
        self.box("Activ", x0, y0, x1, y1)
        self.box("pSD", x0 - 0.03, y0 - 0.03, x1 + 0.03, y1 + 0.03)
        self.box("M1", x0, y0, x1, y1)
        self._contacts(x0, y0, x1, y1, horizontal)

    def ntie(self, x0, y0, x1, y1, horizontal, well_enc=0.24):
        """n+ tie in NWell (NW_e 0.24 outside ThickGateOx), contacts, Metal1."""
        self.box("Activ", x0, y0, x1, y1)
        self.box("NWell", x0 - well_enc, y0 - well_enc, x1 + well_enc, y1 + well_enc)
        self.box("M1", x0, y0, x1, y1)
        self._contacts(x0, y0, x1, y1, horizontal)

    def _contacts(self, x0, y0, x1, y1, horizontal):
        p = RULES["Cnt_a"] + RULES["Cnt_b"] + 0.02            # 0.36 pitch (Cnt_b 0.18, + margin)
        e = RULES["Cnt_c"] + RULES["Cnt_a"] / 2               # centre 0.15 from the Activ end
        if horizontal:
            n = int((x1 - x0 - 2 * e) / p) + 1
            s = x0 + (x1 - x0 - (n - 1) * p) / 2
            for k in range(n):
                self.cont(s + k * p, (y0 + y1) / 2)
        else:
            n = int((y1 - y0 - 2 * e) / p) + 1
            s = y0 + (y1 - y0 - (n - 1) * p) / 2
            for k in range(n):
                self.cont((x0 + x1) / 2, s + k * p)


def copy_cell(src_ly, name, dst_ly, rename=None):
    """deep copy of a cell (and its hierarchy) from src_ly into dst_ly; returns the new cell"""
    src = src_ly.cell(name)
    new = dst_ly.create_cell(rename or name)
    new.copy_tree(src)
    return new


def save(ly, path):
    opt = db.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    opt.write_context_info = False
    ly.write(path, opt)
