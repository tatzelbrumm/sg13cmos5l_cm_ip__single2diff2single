# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Cleaned-out template of the sg13cmos5l_IOPadSingle2Diff pad cell: IHP's IOPadAnalog with the core-side plates
cleared for the s2d buffer, the way C2 cleared sg13cmos5l_IOPadDiff2Single (2026-11-03, draft for review).

    python3 build_template.py <C2 padctx dir> [out.gds]

<C2 padctx dir>: sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/padctx (notes branch), holding C2's
edge_stubs.gds and nw_isolator.gds.

Kept from IOPadAnalog, unchanged: the five protection instances (Clamp_N20N0D, DCNDiode, DCPDiode, Clamp_P20N0D,
SecondaryProtection), every own shape at y <= 84.44 (the iovdd / iovss plates of the ESD zone, the pad M2), the ring
rails M3 / M4 / TM1 with Via3 / TopVia1, prBoundary.
Cleared, above the Clamp_P frame (y > 84.44): the p+ plate on iovss (84.51-139.92), the three bands across the cell
(n+ iovdd 148.35, p+ vss 156.85, n+ vdd 166.85) with their ties, the pad M2 fingers to the core side and the core-side
pad / padres pins.
Added:
  - C2's nw_isolator (n+ in NWell on iovdd above the frame's outer p+ ring, Via1 / Via2 into M3 iovdd); its M2 stack at
    x 54.345 is left out (it would touch SP's pad finger), stacks at x 39.245 and 57.365 (C2's exclusions for its own
    lines) are put back.
  - C2's edge_stubs (IOPadAnalog's edge intervals at both edges, each tied to its rail), with the left iovdd n+ stub
    tied like the right one (M2 down to M3 iovdd): in C2 the d2s block tied it.
  - SecondaryProtection's ties, which it got from the cleared plate and band: IHP's pad finger (M2 x 53.17-54.01) kept
    up to SP's pad pin; an M1 / Via1 / M2 / Via2 stack from its p+ rings into M3 iovss (126-134); a Via1 / M2 / Via2
    line from its n+ ring into M3 iovdd (93.5-119); a padres M2 stub with a pin.
Rule values (sg13cmos5l_tech_default.json): Via1 / Via2 0.19 (V1_a, Vn_a), array pitch 0.50 >= 0.19 + V1_b1 / Vn_b1
0.29, enclosures >= 0.075 (V1_c1 / Vn_c1 0.05), metal spacings >= 0.27 (M1_b 0.18, Mn_b 0.21).
"""
import sys
import klayout.db as db

IO = '/foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds'
TOP = 'sg13cmos5l_IOPadSingle2Diff'
CTX = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else TOP + '_template.gds'
Y_FRAME = 84.44                       # top of Clamp_P20N0D (bbox) = top of the kept ESD zone
Y_PAD_M2 = 84.20                      # pad M2 fingers end here (C2: 0.25 below the isolator's M2 at 84.45)
FINGER = (53.17, 54.01)               # IHP's pad M2 finger into SecondaryProtection's pad pin (y 140.17)

src = db.Layout()
src.read(IO)
ly = db.Layout()
ly.dbu = src.dbu
top = ly.create_cell(TOP)
top.copy_tree(src.cell('sg13cmos5l_IOPadAnalog'))
L = lambda l, d=0: ly.layer(l, d)
um = lambda x0, y0, x1, y1: db.DBox(x0, y0, x1, y1).to_itype(ly.dbu)
ABOVE = db.Region(um(-5, Y_FRAME, 85, 190))

# ---- clear the core side: every own shape of these layers above the frame; M1 / pSD / M2 polygons are clipped ------
for lay in [(1, 0), (31, 0), (14, 0), (40, 0), (8, 0), (8, 2), (6, 0), (19, 0), (10, 0), (10, 2), (29, 0)]:
    sh = top.shapes(L(*lay))
    keep = db.Region()
    for s in list(sh.each()):
        if s.is_text():
            continue
        b = s.dbbox()
        if b.top > Y_FRAME + 1e-6:
            if b.bottom < Y_FRAME - 1e-6:          # straddles: keep the part in the ESD zone
                part = db.Region(s.polygon) - ABOVE
                if lay[0] == 8:                    # M1 plate: down to the top of the plate's Activ (84.26)
                    part -= db.Region(um(-5, 84.26, 85, 190))
                if lay == (10, 0):                 # pad M2 plate: fingers end at 84.2, IHP's SP finger goes on
                    part = (db.Region(s.polygon) - db.Region(um(-5, Y_PAD_M2, 85, 190))) + \
                           (db.Region(s.polygon) & db.Region(um(FINGER[0], Y_PAD_M2, FINGER[1], 140.17)))
                keep += part
            sh.erase(s)
    sh.insert(keep.merged())
# core-side pins on M3 (pad, padres at y 179.71-180) and the texts above the frame that name cleared shapes
for lay in [(30, 0), (30, 2)]:
    sh = top.shapes(L(*lay))
    for s in list(sh.each()):
        if not s.is_text() and s.dbbox().bottom > 179:
            sh.erase(s)
for lay in [(63, 0), (10, 25), (30, 25)]:
    sh = top.shapes(L(*lay))
    for s in list(sh.each()):
        if s.is_text() and s.dtext.y > Y_FRAME and (lay != (30, 25) or s.text.string in ('pad', 'padres')):
            sh.erase(s)


# ---- C2's cells --------------------------------------------------------------------------------------------------
def import_cell(name):
    tmp = db.Layout()
    tmp.read(f'{CTX}/{name}.gds')
    c = ly.create_cell(name)
    c.copy_tree(tmp.cell(name))
    top.insert(db.DCellInstArray(c.cell_index(), db.DTrans()))
    return c


def stack(c, x0, x1, y0, y1, over):
    """shapes of c in the box: returns {layer: Region}"""
    r = {}
    for lay in over:
        r[lay] = db.Region(c.shapes(L(*lay))) & db.Region(um(x0, y0, x1, y1))
    return r


iso = import_cell('nw_isolator')
M2V = [(10, 0), (19, 0), (29, 0)]
ref = stack(iso, 35.9, 36.55, 84.0, 86.5, M2V)                       # C2's stack at x 36.225
for x in (39.245, 57.365):
    for lay, r in ref.items():
        iso.shapes(L(*lay)).insert(r.moved(db.DVector(x - 36.225, 0).to_itype(ly.dbu)))
for lay in M2V:
    sh = iso.shapes(L(*lay))
    for s in list(sh.each()):
        if 53.8 < s.dbbox().center().x < 54.9:                       # the stack at 54.345, 0.035 from SP's finger
            sh.erase(s)

stubs = import_cell('edge_stubs')
right = stack(stubs, 78.2, 78.9, 118.3, 149.0, M2V)                 # right iovdd n+ stub's M2 / Via1 / Via2 to M3
for lay, r in right.items():
    stubs.shapes(L(*lay)).insert(r.transformed(db.Trans(db.Trans.M90, db.Vector(round(80.0 / ly.dbu), 0))))  # x -> 80 - x

# ---- SecondaryProtection's ties ----------------------------------------------------------------------------------
sp_tie = ly.create_cell('sp_ties')
top.insert(db.DCellInstArray(sp_tie.cell_index(), db.DTrans()))
B = lambda lay, *b: sp_tie.shapes(L(*lay)).insert(um(*b))


def vias(lay, xs, ys):
    for x in xs:
        for y in ys:
            B(lay, x - 0.095, y - 0.095, x + 0.095, y + 0.095)


grid = lambda a, b, p=0.50: [round(a + p * k, 3) for k in range(int((b - a) / p + 1e-6) + 1)]
# iovss: SP's two p+ rings (M1 bottom edges at y 140.17, x 52.15-55.03 and 56.49-58.77) -> M3 iovss (126-134)
B((8, 0), 52.15, 139.37, 58.77, 140.17)                              # joins both ring bottoms
B((8, 0), 55.20, 126.40, 58.60, 140.17)
B((10, 0), 55.20, 126.40, 58.60, 133.70)                             # 1.19 from SP's pad finger (x 54.01)
vias((19, 0), grid(55.55, 58.25), grid(126.75, 133.25))
vias((29, 0), grid(55.55, 58.25), grid(126.75, 133.25))
# iovdd: SP's n+ ring, right leg x 58.43-58.77 (M1) -> M2 x 59.6-60.2 -> M3 iovdd (93.5-119) at y 118.6
vias((19, 0), [58.60], [147.25, 147.75])
B((10, 0), 58.40, 147.00, 60.20, 148.00)                             # 0.52 from SP's core M2 (x 57.88)
B((10, 0), 59.60, 118.30, 60.20, 148.00)
vias((29, 0), [59.90], [118.55])
# padres: IHP's line (M2 x 57.355-57.855 from y 147.18) as a stub with a pin
B((10, 0), 57.355, 147.18, 57.855, 151.00)
# pin and text in the top cell: IHP's LVS names ports from top-cell texts only
top.shapes(L(10, 2)).insert(um(57.46, 150.00, 57.75, 151.00))
top.shapes(L(10, 25)).insert(db.DText('padres', db.DTrans(57.605, 150.5)).to_itype(ly.dbu))

opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(OUT, opt)
print('wrote', OUT, 'top', TOP, top.dbbox())
