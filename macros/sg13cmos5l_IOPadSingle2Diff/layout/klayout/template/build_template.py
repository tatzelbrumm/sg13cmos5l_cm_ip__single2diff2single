# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Cleaned-out template of the sg13cmos5l_IOPadSingle2Diff pad cell (draft for review, 2026-11-03, version 2).

    PDKPATH=/foss/pdks/ihp-sg13cmos5l python3 build_template.py <C2 padctx dir> [out.gds]

<C2 padctx dir>: sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/padctx (notes branch), with C2's
edge_stubs.gds.

Frame: IHP's IOPadAnalog, of which only these stay: the ring rails M3 / M4 / TM1 with Via3 / TopVia1, the pad exit
(M2 bar x 5-75, y 0-3, and its Via2), the two narrow NWell legs at the edges (n+ iovdd, x 0-0.4 / 79.6-80,
y 6-61), prBoundary. Everything else of IOPadAnalog goes, its five protection instances included; the secondary
protection is left out for now (Christoph, 2026-11-03).

Protection, rebuilt from the SG13_cm_clamps PCells (scripts/pcells) in the region between the legs, y 5.38-39.02,
in two columns (left the n-type devices, right the p-type devices, each in IHP's vertical order and relative
position):
  CN Clamp_N_M1 ng 20, l 0.6u, frame fit   at (1.20, 6.00)    = IHP's Clamp_N20N0D array (20 x 4.4/0.6)
  DN DCNDiode l 27.78u                      at (2.67, 17.56)   = IHP's DCNDiode; guard ring abuts CN's outer ring
  CP Clamp_P_M1 ng 20, l 0.6u, frame fit   at (42.23, 6.00)   = IHP's Clamp_P20N0D array (20 x 2 x 6.66/0.6)
  DP DCPDiode l 27.78u                      at (43.70, 26.92)  = IHP's DCPDiode; guard ring abuts CP's outer ring
The gate tie-off of IHP's 0D clamps: rppd w 0.5u, l 3.54u (CN gate -> iovss) and l 12.9u (CP gate -> iovdd) from
SG13_dev, in the 4 um gap between the columns.
Wiring (all new, M2 with Via1 / Via2):
  - pad: one 0.62 um strap per clamp drain from the pad bar up over the diode stripes (10 per column, as IHP's
    0.61 um straps), Via1 onto drains and stripes; one strap of the left column goes on to y 40 as the core-side
    pad pin for the buffer.
  - iovss: Via1 / M2 / Via2 stubs from CN's inner ring, DN's anode frame, CP's outer ring and DP's guard ring into
    the M3 iovss rails (7-32.5, 34.5-60).
  - iovdd: CP's inner ring to DP's cathode frame (short M2 between the pad straps, and the right side), DP's frame
    up to M3 iovdd (66-91.5) by two 1.26 um straps on its side bars (IHP: 2.2 um over DCP); the n-side guard (CN's outer
    ring, DN's guard ring, the left leg) and the right leg each by an M2 line up to M3 iovdd.
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
P = {}
for key, name, lib, par, x, y in [
        ('CN', 'Clamp_N_M1', 'SG13_cm_clamps', {'ng': 20, 'l': '0.6u', 'frame': 'fit'}, 1.20, 6.00),
        ('DN', 'DCNDiode', 'SG13_cm_clamps', {'l': '27.78u'}, 2.67, 17.56),
        ('CP', 'Clamp_P_M1', 'SG13_cm_clamps', {'ng': 20, 'l': '0.6u', 'frame': 'fit'}, 42.23, 6.00),
        ('DP', 'DCPDiode', 'SG13_cm_clamps', {'l': '27.78u'}, 43.70, 26.92),
        ('RN', 'rppd', 'SG13_dev', {'w': '0.5u', 'l': '3.54u', 'Calculate': 'R'}, 38.80, 9.52),
        ('RP', 'rppd', 'SG13_dev', {'w': '0.5u', 'l': '12.9u', 'Calculate': 'R'}, 40.60, 22.93)]:
    c = ly.create_cell(name, lib, par)
    if c is None:
        raise SystemExit(f'PCell {lib}.{name} not available')
    top.insert(db.DCellInstArray(c.cell_index(), db.DTrans(x, y)))
    P[key] = (x, y)

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
CNx, CNy = P['CN']
CPx, CPy = P['CP']
DNx, DNy = P['DN']
DPx, DPy = P['DP']
dl = [CNx + 4.10 + PITCH * k for k in range(10)]   # left drain columns (x0), 0.62 wide
dr = [CPx + 4.10 + PITCH * k for k in range(10)]   # right drain columns
gaps = lambda d: [(d[k] + 0.62 + 0.30, d[k + 1] - 0.30) for k in range(9)]

# pad straps
for x in dl:
    B((10, 0), x, 2.80, x + 0.62, DNy + 8.01 + 0.23)
    column((19, 0), x + 0.31, CNy + 2.95, CNy + 6.95)                      # CN drains y 2.75-7.15 (cell)
    for ys in (2.25, 6.75):                                                # DN cathode stripes, 1.26 tall
        column((19, 0), x + 0.31, DNy + ys + 0.38, DNy + ys + 0.88)
for x in dr:
    B((10, 0), x, 2.80, x + 0.62, DPy + 8.01 + 0.23)
    column((19, 0), x + 0.31, CPy + 3.10, CPy + 16.10)                     # CP drains y 2.86-16.4 (cell)
    for ys in (2.25, 6.75):                                                # DP anode stripes
        column((19, 0), x + 0.31, DPy + ys + 0.38, DPy + ys + 0.88)
xpad = dl[5]                                                               # core-side pad pin for the buffer
B((10, 0), xpad, DNy + 8.0, xpad + 0.62, 40.0)
top.shapes(L(10, 2)).insert(um(xpad, 39.4, xpad + 0.62, 40.0))
top.shapes(L(10, 25)).insert(db.DText('pad', db.DTrans(xpad + 0.31, 39.7)).to_itype(ly.dbu))

# gate tie-offs: CN gate bus (cell y 7.15-7.53, x 3.44-32.56) -> RN -> CP's outer ring (iovss);
#                CP gate bus (cell y 16.4-16.89, x 3.44-32.56) -> RP -> DP's cathode frame (iovdd)
B((8, 0), CNx + 32.10, CNy + 7.22, CNx + 32.56, CNy + 7.57)              # landing on the 0.16 um bus end (y 7.37-7.53)
via((19, 0), CNx + 32.33, CNy + 7.40)
gy = P['RN'][1] + 3.82                                                     # RN top terminal (cell y 3.67-3.97)
B((10, 0), CNx + 32.18, gy - 0.15, P['RN'][0] + 0.40, CNy + 7.55)
via((19, 0), P['RN'][0] + 0.25, gy)
yb = P['RN'][1] - 0.28
B((8, 0), P['RN'][0] + 0.02, yb - 0.15, CPx + 0.34, yb + 0.15)             # RN bottom terminal -> CP outer ring
B((8, 0), CPx + 3.18, CPy + 16.60, CPx + 3.60, CPy + 16.94)              # landing on the bus end (y 16.73-16.89)
via((19, 0), CPx + 3.39, CPy + 16.77)
gy = P['RP'][1] - 0.28                                                     # RP bottom terminal (cell y -0.43..-0.13)
B((10, 0), P['RP'][0] + 0.10, gy - 0.15, CPx + 3.54, CPy + 16.92)
via((19, 0), P['RP'][0] + 0.25, gy)
yt = P['RP'][1] + 12.9 + 0.28
via((19, 0), P['RP'][0] + 0.25, yt)
B((10, 0), P['RP'][0] + 0.10, yt - 0.15, DPx + 0.85, yt + 0.15)         # joins the M2 strap on DP's left frame bar

# iovss
for x0, x1 in [(CNx + 1.80, dl[0] - 0.30)] + gaps(dl) + [(dl[9] + 0.92, CNx + 34.20)]:
    iovss_stub_h(x0, x1, CNy + 1.97)                                       # CN inner ring, bottom side
for x0, x1 in [(CNx + 1.80, dl[0] - 0.30)] + gaps(dl)[:8]:
    iovss_stub_h(x0, x1, CNy + 7.93)                                       # CN inner ring, top side
iovss_stub_v(CNx + 1.97, CNy + 2.40, CNy + 7.50)                           # left side
iovss_stub_v(CNx + 34.03, CNy + 2.40, CNy + 6.90)                          # right side (gate line above)
for yb_ in (0.63, 5.13, 9.63):                                             # DN anode frame bars
    for x0, x1 in [(DNx + 0.20, dl[0] - 0.30)] + gaps(dl) + [(dl[9] + 0.92, DNx + 32.86)]:
        if x0 < xpad < x1 or x0 < xpad + 0.62 < x1:
            continue
        iovss_stub_h(x0, x1, DNy + yb_)
iovss_stub_v(CPx + 0.17, CPy + 1.20, CPy + 16.20)                          # CP outer ring, left (gate line at 16.65)
iovss_stub_v(CPx + 35.83, CPy + 1.20, CPy + 18.90)                         # right
iovss_stub_v(DPx - 1.49, DPy + 0.30, DPy + 8.65)                           # DP guard ring, left (RP line at 13.18)
iovss_stub_v(DPx + 34.55, DPy + 0.30, DPy + 11.60)                         # right
top_ys = DPy + 11.75
xs_dd = [(DPx, DPx + 1.26), (DPx + 31.80, DPx + 33.06)]          # iovdd straps up: DP's two side bars
edges = [DPx - 1.66] + [v for a, b in xs_dd for v in (a, b)] + [DPx + 34.72]
for k in range(0, len(edges), 2):
    x0, x1 = edges[k] + (0.30 if k else 0.0), edges[k + 1] - (0.30 if k + 1 < len(edges) - 1 else 0.0)
    if x1 - x0 > 0.6:
        iovss_stub_h(x0, x1, top_ys)                                       # DP guard ring, top side

# iovdd
Y3 = 66.55                                                                 # Via2 row into M3 iovdd (66-91.5)
for x0, x1 in xs_dd:
    B((10, 0), x0, DPy + 0.10, x1, Y3 + 0.25)
    column((19, 0), x0 + 0.40, DPy + 0.35, DPy + 10.0)
    column((19, 0), x0 + 0.86, DPy + 0.35, DPy + 10.0)
    row((29, 0), Y3, x0 + 0.15, x1 - 0.15, p=0.45)
for x0, x1 in gaps(dr):                                                    # CP inner ring top -> DP frame bottom bar
    c = (x0 + x1) / 2
    B((10, 0), c - 0.30, CPy + 17.12 - 0.20, c + 0.30, DPy + 1.26 - 0.05)
    via((19, 0), c, CPy + 17.29)
    for yv in (DPy + 0.38, DPy + 0.88):
        via((19, 0), c, yv)
B((10, 0), CPx + 33.80, CPy + 1.80, CPx + 34.30, DPy + 0.80)               # CP inner ring right side -> DP right bar
column((19, 0), CPx + 34.03, CPy + 2.10, CPy + 17.20)
# n-side guard (CN outer ring, DN guard ring, left leg) and the right leg -> M3 iovdd
B((8, 0), 0.0, CNy, CNx + 0.34, CNy + 9.90)
B((8, 0), 0.0, CNy + 9.90, DNx - 1.32, DNy + 11.92)
B((10, 0), 1.02, CNy + 0.20, 1.52, Y3 + 0.25)
column((19, 0), CNx + 0.17, CNy + 0.40, CNy + 9.40)
column((19, 0), DNx - 1.49, DNy - 1.0, DNy + 11.40)
via((29, 0), 1.27, Y3)
B((8, 0), 78.95, 6.0, 80.0, 61.0)
B((10, 0), 79.00, 6.20, 79.45, Y3 + 0.25)
column((19, 0), 79.20, 6.50, 60.50)
via((29, 0), 79.20, Y3)

for c in [c for c in ly.top_cells() if c.name != TOP]:          # IOPadAnalog's protection cells, now unused
    ly.delete_cell_rec(c.cell_index())
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
opt.write_context_info = True                     # keep the PCell context (library, parameters)
ly.write(OUT, opt)
print('wrote', OUT, 'top', TOP, top.dbbox())
