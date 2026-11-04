# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Cleaned-out template of the sg13cmos5l_IOPadSingle2Diff pad cell (draft for review, 2026-11-03, version 4).

    PDKPATH=/foss/pdks/ihp-sg13cmos5l python3 build_template.py <C2 padctx dir> [out.gds]

<C2 padctx dir>: sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/padctx (notes branch), with C2's
edge_stubs.gds.

Frame: IHP's IOPadAnalog, of which only these stay: the ring rails M3 / M4 / TM1 with Via3 / TopVia1, the pad exit
(M2 bar x 5-75, y 0-3, and its Via2), the two narrow NWell legs at the edges (iovdd, x -0.62-0.77 / 79.23-80.62,
y 5.38-61.62; their n+ taps redrawn), prBoundary. IHP's five protection instances go; the secondary protection is
left out for now (Christoph, 2026-11-03).

Protection from the SG13_cm_clamps PCells (scripts/pcells), y 5.38-38.84 between the legs (Christoph, 2026-11-03:
diodes side by side closest to the pad, clamps side by side, no long wires to the core, no needless distance):
  DN DCNDiode l 27.78u                        at (2.67, 7.66)    bottom row, left
  DP DCPDiode l 27.78u                        at (43.70, 7.66)   bottom row, right
  CN Clamp_N_M1 ng 20, l 0.6u, frame fit     at (1.20, 19.58)   on DN, rings abutting = IHP's Clamp_N20N0D array
  CP Clamp_P_M1 ng 20, l 0.6u, frame fit     at (42.23, 19.58)  on DP, rings abutting = IHP's Clamp_P20N0D array
  RN rppd w 0.5u l 3.54u (CN gate -> iovss), RP rppd w 0.5u l 12.9u (CP gate -> iovdd): IHP's 0D gate ties, in the
  gap between the columns.
Wiring (cell esd_wiring, M2 with Via1 / Via2):
  - pad: one 0.62 um strap per clamp drain (10 per column, as IHP's 0.61 um), from the pad bar over the diode
    stripes to the clamp drains; one left-column strap ends 1.7 um above CN as the core-side pad pin.
  - iovss: Via1 / M2 / Via2 stubs into the M3 iovss rails (7-32.5, 34.5-60) from DN's anode frame, DP's guard
    ring, CN's inner ring, CP's outer ring and RN's far end.
  - iovdd: M3 / M4 / TM1 over the whole zone are iovss rails, so iovdd has to climb on M2 to the M3 iovdd rail
    (66-91.5): 9 straps between the right column's pad straps plus one on DP's right side bar join DP's cathode
    frame and CP's inner ring into a 2.2 um M2 bar just above CP; two risers at the column's edges (x 42.6-45.2,
    75.5-78.4) take it up, so the band above the clamps stays free, and run 6 um under the rail with 13 x 5 and
    13 x 6 Via2 (IOPadAnalog: 495 Via2 into the same rail, its Clamp_P sits under it). The n-side guards (DN's guard ring, CN's outer
    ring) join the left leg in M1; each leg has a 6 um M2 tie into M3 iovdd at its top.
Edges: C2's edge_stubs above y 84 (the left iovdd n+ stub tied as the right one) and a p+ iovss stub at IHP's
interval y 65-84.26 at each edge, so the cell keeps IOPadAnalog's edge contract.
Rule values (sg13cmos5l_tech_default.json): Via1 / Via2 0.19 (V1_a, Vn_a), array pitch 0.50 >= 0.19 + V1_b1 / Vn_b1
0.29, enclosures >= 0.05 (V1_c1 / Vn_c1), metal spacings >= 0.21 (M1_b 0.18, Mn_b 0.21).
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(HERE, '../../../../../scripts/pcells/load_clamp_pcells.py'))   # SG13_cm_clamps
import sg13cmos5l_pycell_lib  # noqa: E402,F401  (registers SG13_dev: rppd)
import klayout.db as db  # noqa: E402

IO = '/foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds'
TOP = 'sg13cmos5l_IOPadSingle2Diff'
CTX = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, TOP + '_template.gds')

src = db.Layout()
src.read(IO)
ly = db.Layout()
ly.dbu = src.dbu
ly.technology_name = 'sg13cmos5l'
top = ly.create_cell(TOP)
top.copy_tree(src.cell('sg13cmos5l_IOPadAnalog'))
L = lambda l, d=0: ly.layer(l, d)
um = lambda x0, y0, x1, y1: db.DBox(x0, y0, x1, y1).to_itype(ly.dbu)
R = lambda *b: db.Region(um(*b))

# ---- strip IOPadAnalog to rails, pad exit and legs ----------------------------------------------------------------
for inst in list(top.each_inst()):
    inst.delete()
KEEP = {(30, 0), (30, 2), (50, 0), (50, 2), (126, 0), (126, 2), (49, 0), (125, 0), (189, 4)}
LEGS_NW = R(-0.62, 5, 0.77, 62) + R(79.23, 5, 80.62, 62)          # IHP's NWell legs (iovdd), kept
PADEXIT = R(-1, -1, 81, 3.0)
for li in ly.layer_indexes():
    info = (ly.get_info(li).layer, ly.get_info(li).datatype)
    sh = top.shapes(li)
    if info in KEEP:
        for s in list(sh.each()):                                  # core-side pad / padres pins at y 179.7-180
            if not s.is_text() and s.dbbox().bottom > 179:
                sh.erase(s)
        continue
    texts = [s.dtext for s in sh.each() if s.is_text()]
    poly = db.Region([s.polygon for s in sh.each() if not s.is_text()])
    sh.clear()
    if info in ((30, 25), (50, 25), (126, 25)):
        texts = [t for t in texts if not (t.y > 170 and t.string in ('pad', 'padres'))]
    elif info == (10, 25):
        texts = [t for t in texts if t.y < 3]
    else:
        texts = []
    for t in texts:
        sh.insert(t.to_itype(ly.dbu))
    if info == (31, 0):
        poly &= LEGS_NW
    elif info in ((10, 0), (10, 2)):
        poly &= PADEXIT
    elif info == (29, 0):
        poly = poly.inside(PADEXIT)
    else:
        poly = db.Region()
    sh.insert(poly)


# n+ taps in the legs at IHP's edge interval (Activ / M1 x 0-0.4, y 6-61), one contact column (LU.d: <= 6 um apart)
for x0 in (0.0, 79.6):
    top.shapes(L(1, 0)).insert(um(x0, 6.0, x0 + 0.4, 61.0))
    top.shapes(L(8, 0)).insert(um(x0, 6.0, x0 + 0.4, 61.0))
    for k in range(int((60.8 - 6.2) / 0.36) + 1):
        top.shapes(L(6, 0)).insert(um(x0 + 0.12, 6.12 + 0.36 * k, x0 + 0.28, 6.28 + 0.36 * k))


# ---- C2's edge stubs, the left iovdd n+ stub tied; p+ stubs 65-84.26 ----------------------------------------------
def import_cell(name):
    tmp = db.Layout()
    tmp.read(f'{CTX}/{name}.gds')
    c = ly.create_cell(name)
    c.copy_tree(tmp.cell(name))
    top.insert(db.DCellInstArray(c.cell_index(), db.DTrans()))
    return c


M2V = [(10, 0), (19, 0), (29, 0)]
stubs = import_cell('edge_stubs')
for lay in M2V:                                   # right iovdd n+ stub's M2 / Via1 / Via2 to M3, mirrored to x -> 80 - x
    r = db.Region(stubs.shapes(L(*lay))) & R(78.2, 118.3, 78.9, 149.0)
    stubs.shapes(L(*lay)).insert(r.transformed(db.Trans(db.Trans.M90, db.Vector(round(80.0 / ly.dbu), 0))))
low = ly.create_cell('edge_stubs_low')
top.insert(db.DCellInstArray(low.cell_index(), db.DTrans()))
for mx in (lambda x: x, lambda x: 80.0 - x):
    B = lambda lay, x0, y0, x1, y1: low.shapes(L(*lay)).insert(um(min(mx(x0), mx(x1)), y0, max(mx(x0), mx(x1)), y1))
    B((1, 0), 0, 65.0, 1.2, 84.26)                # IOPadAnalog's p+ interval at the edges (iovss), as C2's stub above
    B((40, 0), 0, 65.0, 1.2, 84.26)
    B((14, 0), -0.18, 64.82, 1.38, 84.44)
    B((8, 0), 0, 65.0, 1.2, 84.26)                # joins C2's stub M1 (84.0-140.17), tied there to M3 iovss
    for xc in (0.40, 0.80):
        for k in range(int((84.0 - 65.3) / 0.36) + 1):
            B((6, 0), xc - 0.08, 65.3 + 0.36 * k - 0.08, xc + 0.08, 65.3 + 0.36 * k + 0.08)

# ---- protection devices ---------------------------------------------------------------------------------------------
# bottom row (next to the pad exit): DN | DP; directly on them CN | CP, rings abutting as in IHP's cells
P = {}
for key, name, lib, par, tr in [
        ('DN', 'DCNDiode', 'SG13_cm_clamps', {'l': '27.78u'}, db.DTrans(2.67, 7.66)),
        ('DP', 'DCPDiode', 'SG13_cm_clamps', {'l': '27.78u'}, db.DTrans(43.70, 7.66)),
        ('CN', 'Clamp_N_M1', 'SG13_cm_clamps', {'ng': 20, 'l': '0.6u', 'frame': 'fit'}, db.DTrans(1.20, 19.58)),
        ('CP', 'Clamp_P_M1', 'SG13_cm_clamps', {'ng': 20, 'l': '0.6u', 'frame': 'fit'}, db.DTrans(42.23, 19.58)),
        ('RN', 'rppd', 'SG13_dev', {'w': '0.5u', 'l': '3.54u', 'Calculate': 'R'}, db.DTrans(38.80, 23.16)),
        ('RP', 'rppd', 'SG13_dev', {'w': '0.5u', 'l': '12.9u', 'Calculate': 'R'}, db.DTrans(40.60, 23.17))]:
    c = ly.create_cell(name, lib, par)
    if c is None:
        raise SystemExit(f'PCell {lib}.{name} not available')
    top.insert(db.DCellInstArray(c.cell_index(), tr))
    P[key] = (tr.disp.x, tr.disp.y)

w = ly.create_cell('esd_wiring')
top.insert(db.DCellInstArray(w.cell_index(), db.DTrans()))
B = lambda lay, x0, y0, x1, y1: w.shapes(L(*lay)).insert(um(x0, y0, x1, y1))


def via(lay, x, y):
    B(lay, x - 0.095, y - 0.095, x + 0.095, y + 0.095)


def column(lay, x, y0, y1, p=0.50):
    n = int((y1 - y0) / p + 1e-6) + 1
    for k in range(n):
        via(lay, x, y0 + k * p)


def row(lay, y, x0, x1, p=0.50):
    n = int((x1 - x0) / p + 1e-6) + 1
    s = (x1 - x0 - (n - 1) * p) / 2
    for k in range(n):
        via(lay, x0 + s + k * p, y)


IOVSS_M3 = [(7.0, 32.5), (34.5, 60.0)]                           # M3 iovss rails over the ESD zone


def via2_iovss(x, y):
    if any(a + 0.15 <= y <= b - 0.15 for a, b in IOVSS_M3):
        via((29, 0), x, y)


def iovss_stub_h(x0, x1, y_m1):
    """M2 piece over a horizontal 0.34 um (or wider) p+ ring / bar segment, Via1 + Via2 into the M3 iovss rail"""
    B((10, 0), x0, y_m1 - 0.21, x1, y_m1 + 0.21)
    row((19, 0), y_m1, x0 + 0.2, x1 - 0.2)
    n = int((x1 - x0 - 0.4) / 0.5 + 1e-6) + 1
    for k in range(n):
        via2_iovss(x0 + 0.2 + (x1 - x0 - 0.4 - (n - 1) * 0.5) / 2 + 0.5 * k, y_m1)


def iovss_stub_v(x_m1, y0, y1):
    B((10, 0), x_m1 - 0.25, y0, x_m1 + 0.25, y1)
    column((19, 0), x_m1, y0 + 0.2, y1 - 0.2)
    for k in range(int((y1 - y0 - 0.4) / 0.5 + 1e-6) + 1):
        via2_iovss(x_m1, y0 + 0.2 + 0.5 * k)


PITCH = 3.02
DNx, DNy = P['DN']
DPx, DPy = P['DP']
CNx, CNy = P['CN']
CPx, CPy = P['CP']
RNx, RNy = P['RN']
RPx, RPy = P['RP']
dl = [CNx + 4.10 + PITCH * k for k in range(10)]   # left drain columns (x0), 0.62 wide, over DN's stripes
dr = [CPx + 4.10 + PITCH * k for k in range(10)]   # right drain columns, over DP's stripes
gaps = lambda d: [(d[k] + 0.62 + 0.30, d[k + 1] - 0.30) for k in range(9)]
mid = lambda d: [(a + b) / 2 for a, b in gaps(d)]
YB = (39.40, 41.60)                                # iovdd bar above CP (2.2 um, IHP's iovdd width over DCP)

# pad: straps from the pad bar over the diode stripes to the clamp drains (cell y 2.75-7.15 / 2.86-16.4)
for x in dl:
    B((10, 0), x, 2.80, x + 0.62, CNy + 7.35)
    for ys in (2.25, 6.75):                                                # diode stripes, 1.26 tall
        column((19, 0), x + 0.31, DNy + ys + 0.38, DNy + ys + 0.88)
    column((19, 0), x + 0.31, CNy + 2.95, CNy + 6.95)
for x in dr:
    B((10, 0), x, 2.80, x + 0.62, CPy + 16.60)
    for ys in (2.25, 6.75):
        column((19, 0), x + 0.31, DPy + ys + 0.38, DPy + ys + 0.88)
    column((19, 0), x + 0.31, CPy + 3.10, CPy + 16.10)
xpad = dl[5]                                                               # pad pin for the buffer, just above CN
B((10, 0), xpad, CNy + 7.0, xpad + 0.62, CNy + 11.60)
top.shapes(L(10, 2)).insert(um(xpad, CNy + 11.0, xpad + 0.62, CNy + 11.60))
top.shapes(L(10, 25)).insert(db.DText('pad', db.DTrans(xpad + 0.31, CNy + 11.3)).to_itype(ly.dbu))

# gate ties: M1 landings on the 0.16 um gate bus ends (cell y 7.37-7.53 / 16.73-16.89), M2 to the rppds in the gap
B((8, 0), CNx + 32.10, CNy + 7.22, CNx + 32.56, CNy + 7.57)
gyn = CNy + 7.40
via((19, 0), CNx + 32.33, gyn)
B((10, 0), CNx + 32.18, gyn - 0.15, RNx + 0.40, gyn + 0.15)
via((19, 0), RNx + 0.25, RNy + 3.82)                                       # RN top terminal
for lay in ((19, 0), (29, 0)):                                             # RN bottom terminal -> M3 iovss
    via(lay, RNx + 0.25, RNy - 0.28)
B((10, 0), RNx + 0.04, RNy - 0.49, RNx + 0.46, RNy - 0.07)
B((8, 0), CPx + 3.18, CPy + 16.60, CPx + 3.60, CPy + 16.94)
gyp = CPy + 16.77
via((19, 0), CPx + 3.39, gyp)
B((10, 0), RPx + 0.10, gyp - 0.15, CPx + 3.54, gyp + 0.15)
via((19, 0), RPx + 0.25, RPy + 13.18)                                      # RP top terminal
yb = RPy - 0.28                                                            # RP bottom terminal -> DP's frame (iovdd)
via((19, 0), RPx + 0.25, yb)
B((10, 0), RPx + 0.10, DNy + 9.53, RPx + 0.40, yb + 0.15)
B((10, 0), RPx + 0.10, DNy + 9.53, DPx + 0.85, DNy + 9.83)
via((19, 0), DPx + 0.63, DNy + 9.68)                                       # DP frame, left side bar

# iovss
for yb_ in (0.63, 5.13, 9.63):                                             # DN anode frame bars -> M3 7-32.5
    for x0, x1 in [(DNx + 0.20, dl[0] - 0.30)] + gaps(dl) + [(dl[9] + 0.92, DNx + 32.86)]:
        iovss_stub_h(x0, x1, DNy + yb_)
iovss_stub_v(DPx - 1.49, DNy - 0.45, DNy + 9.25)                           # DP guard ring, left (RP line at 9.68)
iovss_stub_v(DPx + 34.55, DNy - 0.45, DNy + 11.70)                         # right
for x0, x1 in [(CNx + 1.80, dl[0] - 0.30)] + gaps(dl) + [(dl[9] + 0.92, CNx + 34.20)]:
    iovss_stub_h(x0, x1, CNy + 1.97)                                       # CN inner ring, lower side
for x0, x1 in [(CNx + 1.80, xpad - 0.30), (xpad + 0.92, CNx + 31.70)]:
    iovss_stub_h(x0, x1, CNy + 7.93)                                       # upper side (gate line right of 33.4)
iovss_stub_v(CNx + 1.97, CNy + 2.40, CNy + 7.50)                           # left side
iovss_stub_v(CNx + 34.03, CNy + 2.40, CNy + 6.90)                          # right side (gate line above)
iovss_stub_v(CPx + 0.17, CPy + 1.20, CPy + 16.30)                          # CP outer ring, left (gate line above)
iovss_stub_v(CPx + 35.83, CPy + 1.20, CPy + 18.90)                         # right

# iovdd: DP's cathode frame and CP's inner ring by 9 straps between the pad straps and one on DP's right side bar,
# into a 2.2 um M2 bar above CP; two risers at the column's edges take it into M3 iovdd (66-91.5)
Y3 = 66.30                                                                # first Via2 row in M3 iovdd (66-91.5)
Y3R = 72.30                                                               # risers' last row: 6 um under the rail
for cx in mid(dr):
    B((10, 0), cx - 0.30, DPy - 0.15, cx + 0.30, YB[0] + 0.10)
    for yb_ in (0.63, 5.13, 9.63):
        for dy in (-0.25, 0.25):
            via((19, 0), cx, DPy + yb_ + dy)
    via((19, 0), cx, CPy + 1.97)                                           # CP inner ring, lower side
    via((19, 0), cx, CPy + 17.29)                                          # upper side
x0 = DPx + 31.80                                                           # DP right side bar (cell x 31.8-33.06)
B((10, 0), x0, DPy + 0.10, x0 + 1.26, YB[0] + 0.10)
column((19, 0), x0 + 0.40, DPy + 0.35, DPy + 10.0)
column((19, 0), x0 + 0.86, DPy + 0.35, DPy + 10.0)
column((19, 0), CPx + 34.03, CPy + 2.10, CPy + 17.20)                      # CP inner ring right side (76.09-76.43)
B((10, 0), 42.60, YB[0], 78.40, YB[1])
for r0, r1 in ((42.60, 45.20), (75.50, 78.40)):
    B((10, 0), r0, YB[0], r1, Y3R + 0.25)
    for xv in [r0 + 0.25 + 0.50 * k for k in range(int((r1 - r0 - 0.40) / 0.50) + 1)]:   # pitch 0.50 >= 0.19 + Vn_b1 0.29
        column((29, 0), xv, Y3, Y3R)
# n-side guard (DN's guard ring, CN's outer ring) by M1 into the left leg; both legs by short M2 into M3 iovdd
B((8, 0), 0.0, DNy - 1.66, DNx - 1.32, DNy + 11.92)
B((8, 0), 0.0, CNy, CNx + 0.34, CNy + 9.90)
for xl, xm, xv in ((0.0, 1.60, 1.27), (78.95, 80.0, 79.20)):
    B((8, 0), xl, 60.20, xm, 61.00)
    via((19, 0), xv, 60.60)
    B((10, 0), xv - 0.23, 60.30, xv + 0.23, Y3 + 1.75)
    column((29, 0), xv, Y3, Y3 + 1.50)

for c in [c for c in ly.top_cells() if c.name != TOP]:          # IOPadAnalog's protection cells, now unused
    ly.delete_cell_rec(c.cell_index())
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
opt.write_context_info = True                     # keep the PCell context (library, parameters)
ly.write(OUT, opt)
print('wrote', OUT, 'top', TOP, top.dbbox())
