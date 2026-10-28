"""Metal2 rework (option B) of sg13cmos5l_IOPadDiff2Single, 2026-10-28 (scratch builder, cloud workspace).

usage: python3 build_m2.py <pad_pcells_2026-10-28.klay.gds> <out.klay.gds>

Start: the pad cell on the SG13_cm_clamps PCells (drains unconnected, only the pad bar in Metal2).
What it does (all coordinates absolute, um, origin lower left of the 80 x 180 um cell):
  1. band above DCNDiode narrowed to DCNDiode's own guard ring (top-level Activ / Metal1 / NWell
     polygons clipped, crossbar contacts and the one duplicate contact removed from cell 'contacts')
  2. cap_cma, cap_cmb   : the Miller capacitors (hv PMOS in accumulation, as d2s_cma / d2s_cmb)
  3. m2_comb_n          : N-side pad lines + iovss straps (Via1, Via2 into the iovss rail), DCN side plates
  4. m2_comb_p          : P-side pad lines + iovdd straps (Via1, Via2 into the iovdd rail), DCP side plates
  5. m2_junction        : pad junction (Metal2, cut for dabn), its Via1 onto CMA's S/D frame,
                          iovss stubs on the DCPDiode guard ring (Via1 + Via2 into the iovss rail)
  6. replica_lines      : dabn (RN1 drain -> pin) and dabp (RP1 drain -> pin)
  7. gate_feeds         : gate bus feeds a / b at the frame ends, joins above the P frame, CMA gate, CMB well
The PCell instances and the rail cells (Metal3ViasUp, TopLayersTo4) are not touched.
"""
import os, sys, runpy
sys.dont_write_bytecode = True
W = '/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/pcw'
os.environ['PDKPATH'] = W + '/pdk/ihp-sg13cmos5l'
sys.path.insert(0, W + '/new/pcells')
runpy.run_path(W + '/new/pcells/load_clamp_pcells.py')          # registers SG13_cm_clamps (live PCells)
import klayout.db as db
import clamp_engine as E

SRC, OUT = sys.argv[1], sys.argv[2]
ly = db.Layout(); ly.read(SRC); top = ly.top_cell(); dbu = ly.dbu
L = lambda l, d: ly.find_layer(l, d) if ly.find_layer(l, d) is not None else ly.layer(l, d)
ACT, POLY, CONT, M1, M2, PSD, V1, V2, NW, TGO, HEAT = (L(1, 0), L(5, 0), L(6, 0), L(8, 0), L(10, 0), L(14, 0),
                                                       L(19, 0), L(29, 0), L(31, 0), L(44, 0), L(51, 0))
M1T, M2P, M2T = L(8, 25), L(10, 2), L(10, 25)
VIA = 0.19
um = lambda v: int(round(v / dbu))


def box(cell, layer, x0, y0, x1, y1):
    cell.shapes(layer).insert(db.Box(um(x0), um(y0), um(x1), um(y1)))


def label(cell, layer, text, x, y):
    cell.shapes(layer).insert(db.Text(text, db.Trans(um(x), um(y))))


def vias(cell, layer, pts):
    for x, y in pts:
        box(cell, layer, x, y, x + VIA, y + VIA)


def grid(x0, x1, y0, y1, px=0.41, py=0.41):
    """Lower-left corners of 0.19 um vias on a px / py grid, centred in [x0, x1] x [y0, y1] (5 nm grid)."""
    nx, ny = int((x1 - x0 - VIA) // px + 1e-9) + 1, int((y1 - y0 - VIA) // py + 1e-9) + 1
    if nx < 1 or ny < 1:
        return []
    sx = round(((x1 - x0) - (VIA + (nx - 1) * px)) / 2 / 0.005) * 0.005
    sy = round(((y1 - y0) - (VIA + (ny - 1) * py)) / 2 / 0.005) * 0.005
    return [(round(x0 + sx + i * px, 3), round(y0 + sy + j * py, 3)) for i in range(nx) for j in range(ny)]


def gap(p, q):
    """Euclidean distance between two via squares with lower-left corners p, q."""
    dx, dy = max(0.0, abs(p[0] - q[0]) - VIA), max(0.0, abs(p[1] - q[1]) - VIA)
    return (dx * dx + dy * dy) ** 0.5


def keep_apart(cands, placed, d):
    """Candidates that keep at least d from every placed via (d = 0: no overlap)."""
    out = []
    for p in cands:
        if all((gap(p, q) >= d - 1e-9) if d > 0 else (abs(p[0] - q[0]) >= VIA - 1e-9 or abs(p[1] - q[1]) >= VIA - 1e-9)
               for q in placed + out):
            out.append(p)
    return out


def new_cell(name):
    c = ly.cell(name)
    if c is not None:
        raise SystemExit('cell %s exists already: run on the start file' % name)
    c = ly.create_cell(name)
    top.insert(db.CellInstArray(c.cell_index(), db.Trans()))
    return c


# ------------------------------------------------------------------------------------------------
# geometry of the frames and diodes (engine, as placed by switch.py) -- checked against the layout
# ------------------------------------------------------------------------------------------------
x0N = (80000 - E.array_extent(35, 1000, 0)[1]) // 10 * 5
x0P = (80000 - E.array_extent(43, 600, 0)[1]) // 10 * 5
N_SRC, N_DRN = [v / 1000 for v in E.columns(35, 1000, x0N)[0]], [v / 1000 for v in E.columns(35, 1000, x0N)[1]]
P_SRC, P_DRN = [v / 1000 for v in E.columns(43, 600, x0P)[0]], [v / 1000 for v in E.columns(43, 600, x0P)[1]]
assert (N_SRC[0], N_DRN[0], N_DRN[8], P_SRC[0], P_DRN[0], P_DRN[10]) == (6.575, 8.485, 39.045, 7.535, 9.045, 39.245)
NY = (6.0, 15.56)                     # N frame origins (lower, upper)
PY = 65.0                             # P frame origin
fN, fP = E.FAMILY['N'], E.FAMILY['P']
n_drain_rows = lambda y0: [round(y0 + v / 1000, 3) for v in fN['drain_via1_rows'][0]]
p_drain_rows = [round(PY + v / 1000, 3) for r in fP['drain_via1_rows'] for v in r]
RN1_K, RP1_K = 8, 10                  # drain columns of RN1 (upper N frame) and RP1 / dummy (P frame)
three = lambda y0: [round(y0 + 0.125 + 0.41 * j, 3) for j in range(3)]   # 3 via rows on a 1.26 um bar / stripe
DCN_Y, DCP_Y = 27.12, 53.08           # DCNDiode / DCPDiode frame bottoms
DCN_BARS = [DCN_Y + a / 1000 for a, _ in E.DIODE_BARS]          # anode (iovss)
DCN_STRIPES = [DCN_Y + a / 1000 for a, _ in E.DIODE_STRIPES]    # cathode (pad)
DCP_BARS = [DCP_Y + a / 1000 for a, _ in E.DIODE_BARS]          # cathode (iovdd)
DCP_STRIPES = [DCP_Y + a / 1000 for a, _ in E.DIODE_STRIPES]    # anode (pad)
DCN_X = (3.56, 3.56 + 67.6 + 5.28)    # frame x extent (3.56 .. 76.44), side bars 1.26 wide
DCP_X = (4.46, 4.46 + 65.8 + 5.28)    # (4.46 .. 75.54)
IOVSS_RAIL = ((7.0, 32.5), (34.5, 60.0))
IOVDD_RAIL = (66.0, 91.5)
in_rail = lambda y, rails: any(a + 0.05 <= y and y + VIA <= b - 0.05 for a, b in rails)

# ------------------------------------------------------------------------------------------------
# 1. band above DCNDiode narrowed to DCNDiode's own guard ring (Activ / Metal1 top 39.04, NWell top 39.66)
# ------------------------------------------------------------------------------------------------
cut = {ACT: db.DBox(0.4, 39.04, 79.6, 42.56), M1: db.DBox(0.4, 39.04, 79.6, 42.56), NW: db.DBox(0.77, 39.66, 79.23, 43.18)}
for li, b in cut.items():
    shp = [s for s in top.shapes(li).each() if not s.is_text()]
    assert len(shp) == 1, (ly.get_info(li).to_s(), len(shp))
    r = db.Region(shp[0].polygon) - db.Region(b.to_itype(dbu))
    top.shapes(li).erase(shp[0])
    top.shapes(li).insert(r.merged())
cc = ly.cell('contacts')
act, m1 = db.Region(top.shapes(ACT)), db.Region(top.shapes(M1))
pcc = db.Region()                                                    # contacts of the PCells (and anything else)
for i in top.each_inst():
    if i.cell.name != 'contacts':
        pcc += db.Region(i.cell.begin_shapes_rec(CONT)).transformed(i.cplx_trans)
boxes = [s.box for s in cc.shapes(CONT).each()]
cc.shapes(CONT).clear()
seen, n0, gone_cut, gone_dup, gone_b1 = set(), len(boxes), 0, 0, 0
for b in boxes:
    key = (b.left, b.bottom, b.right, b.top)
    if key in seen:
        gone_dup += 1; continue
    seen.add(key)
    r = db.Region(b)
    if not (r.sized(70) - act).is_empty() or not (r - m1).is_empty():   # Cnt.c 0.07 in Activ, under Metal1
        gone_cut += 1; continue
    if not pcc.interacting(r.sized(195)).is_empty():                    # Cnt.b1: < 0.20 to DCNDiode's guard contacts
        gone_b1 += 1; continue
    cc.shapes(CONT).insert(b)
print('band: contacts %d -> %d (%d outside the narrowed band, %d duplicate, %d closer than 0.20 to a PCell contact)' % (
    n0, cc.shapes(CONT).size(), gone_cut, gone_dup, gone_b1))

# ------------------------------------------------------------------------------------------------
# 2. Miller capacitors (construction of d2s_cma / d2s_cmb, gate along x, W along y)
#    NWell 41.46 .. 50.66: NW.b1 1.80 to the DCN guard-ring NWell (top 39.66) and to DCPDiode's NWell (52.46)
#    p+ Activ 42.08 .. 50.04 (NW.c1 0.62), W = 7.96, L = 32.16 -> 256.0 um^2 each
# ------------------------------------------------------------------------------------------------
CAP_W, CAP_L = 7.96, 32.16
NWY = (41.46, 50.66)
AY = (NWY[0] + 0.62, NWY[1] - 0.62)           # 42.08 .. 50.04
HEAD = (AY[1] + 0.42, AY[1] + 0.78)           # poly head 50.46 .. 50.82 (as d2s_cma, 0.42 .. 0.78 above Activ)
assert abs(AY[1] - AY[0] - CAP_W) < 1e-9


def capacitor(name, wx0, gate_net, well_net, ubot):
    """NWell from x = wx0; ntap 0.36 | 0.30 | p+ S/D 0.34 | gate L | p+ S/D 0.34 | 0.30 | ntap 0.36, 0.62 to the well edge.
    Metal1: a U (both S/D columns, both ntap columns, a bottom strip from y = ubot) on the well net, and the
    gate-head strip on top. Returns the cell and a dict of the x positions."""
    c = ly.create_cell(name)
    top.insert(db.CellInstArray(c.cell_index(), db.Trans()))
    n0 = wx0 + 0.62; s0 = n0 + 0.36 + 0.30; g0 = s0 + 0.34; g1 = g0 + CAP_L; s1 = g1 + 0.34; n1 = s1 + 0.30; wx1 = n1 + 0.36 + 0.62
    for lay in (NW, TGO):
        box(c, lay, wx0, NWY[0], wx1, NWY[1])
    box(c, ACT, s0, AY[0], s1, AY[1])                                  # S/D + channel
    box(c, ACT, n0, AY[0], n0 + 0.36, AY[1]); box(c, ACT, n1, AY[0], n1 + 0.36, AY[1])   # ntaps
    box(c, PSD, s0 - 0.18, AY[0] - 0.40, s1 + 0.18, AY[1] + 0.40)       # pSD.c 0.18, pSD.i1 0.40
    box(c, POLY, g0, AY[0] - 0.18, g1, HEAD[1])                        # gate, end cap 0.18 below, head on top
    box(c, HEAT, g0, AY[0] - 0.18, g1, AY[1] + 0.18)                   # HeatTrans as in d2s_cma
    ys = [round(y / 1000, 3) for y in E._cont_row(round((AY[0] + 0.07) * 1000), round((AY[1] - 0.07) * 1000))]
    cols = (n0 + 0.10, s0 + 0.07, s1 - 0.07 - 0.16, n1 + 0.10)         # ntap, S/D (Cnt.f 0.11 to the gate), S/D, ntap
    for x in cols:
        for y in ys:
            box(c, CONT, x, y, x + 0.16, y + 0.16)
    hx = [round(x / 1000, 3) for x in E._cont_row(round((g0 + 0.07) * 1000), round((g1 - 0.07) * 1000))]
    hy = round((HEAD[0] + HEAD[1]) / 2 - 0.08, 3)
    for x in hx:
        box(c, CONT, x, hy, x + 0.16, hy + 0.16)
    top_m1 = ys[-1] + 0.16 + 0.05
    box(c, M1, cols[0] - 0.05, ubot, cols[1] + 0.21, top_m1)          # left end (ntap + S/D)
    box(c, M1, cols[2] - 0.05, ubot, cols[3] + 0.21, top_m1)          # right end
    box(c, M1, cols[0] - 0.05, ubot, cols[3] + 0.21, AY[0] - 0.23)    # bottom strip
    box(c, M1, hx[0] - 0.05, HEAD[0], hx[-1] + 0.21, HEAD[1])          # gate head
    label(c, M1T, well_net, (cols[0] + cols[3]) / 2, (ubot + AY[0] - 0.23) / 2)
    label(c, M1T, gate_net, (g0 + g1) / 2, (HEAD[0] + HEAD[1]) / 2)
    return c, dict(wx0=wx0, wx1=wx1, end_l=(cols[0] - 0.05, cols[1] + 0.21), end_r=(cols[2] - 0.05, cols[3] + 0.21),
                   head=(hx[0] - 0.05, hx[-1] + 0.21), bot=(ubot, AY[0] - 0.23), top_m1=top_m1)


JY = (39.3, 41.3)                                              # pad junction (Metal2)
cma, CA = capacitor('cap_cma', 2.57, 'a', 'pad', JY[0])        # S/D frame reaches down under the junction
cmb, CB = capacitor('cap_cmb', CA['wx1'] + 1.80, 'pad', 'b', 41.5)
assert abs(CA['wx0'] - (0.77 + 1.80)) < 1e-9 and CB['wx1'] <= 79.23 - 1.80
box(cma, M1, 3.0, HEAD[0], CA['head'][0] + 0.01, HEAD[1])     # CMA gate head extended left to the 'a' landing
print('CMA well x %.2f..%.2f, CMB well x %.2f..%.2f, W %.2f L %.2f (%.2f um^2 each)' % (
    CA['wx0'], CA['wx1'], CB['wx0'], CB['wx1'], CAP_W, CAP_L, CAP_W * CAP_L))

# ------------------------------------------------------------------------------------------------
# 3. N side: pad lines (0.61) on the N drains, iovss straps (0.2) on the N sources, DCN side plates
# ------------------------------------------------------------------------------------------------
cn = new_cell('m2_comb_n')
v1n, v2n = [], []
PAD_TOP_N, STRAP_N = JY[0] + 0.2, (6.2, 39.0)
for k, xd in enumerate(N_DRN):
    rows = n_drain_rows(NY[0]) + ([] if k == RN1_K else n_drain_rows(NY[1]) + [y for s in DCN_STRIPES for y in three(s)])
    top_y = 13.205 if k == RN1_K else PAD_TOP_N        # x 39.045: only the lower frame's ON drain is pad
    box(cn, M2, xd - 0.305, 2.8, xd + 0.305, top_y)
    v1n += [(round(xd + dx - 0.095, 3), y) for dx in (-0.205, 0.205) for y in rows]
for xs in N_SRC:
    box(cn, M2, xs - 0.1, STRAP_N[0], xs + 0.1, STRAP_N[1])
    rows = [y0 + 1.875 for y0 in NY] + [y0 + 7.835 for y0 in NY] + n_drain_rows(NY[0]) + n_drain_rows(NY[1]) + \
           [y for b in DCN_BARS for y in three(b)]
    mine = [(round(xs - 0.095, 3), round(y, 3)) for y in rows]
    v1n += mine
    c2 = [(round(xs - 0.095, 3), round(7.1 + 0.41 * m, 3)) for m in range(80)]
    v2n += keep_apart([p for p in c2 if in_rail(p[1], IOVSS_RAIL) and p[1] + VIA <= STRAP_N[1] - 0.05], mine, 0.0)
# DCN side plates (iovss): side bar + frame bars under the plate, Via1 on every bar of the net, Via2 into the rail
for px0, px1, sb in ((3.45, N_SRC[0] + 0.1, (DCN_X[0], DCN_X[0] + 1.26)), (N_DRN[-1] + 0.305 + 0.27, 76.55, (DCN_X[1] - 1.26, DCN_X[1]))):
    py0, py1 = DCN_Y - 0.17, DCN_Y + 10.26 + 0.17
    box(cn, M2, px0, py0, px1, py1)
    a, b = max(px0, DCN_X[0]) + 0.05, min(px1, DCN_X[1]) - 0.05
    c1 = grid(sb[0] + 0.05, sb[1] - 0.05, DCN_Y + 0.05, DCN_Y + 10.26 - 0.05)
    for yb in DCN_BARS:
        c1 += grid(a, b, yb + 0.05, yb + 1.26 - 0.05)
    new1 = keep_apart(c1, v1n, 0.22); v1n += new1
    c2 = []
    for ra, rb in IOVSS_RAIL:
        y0, y1 = max(py0, ra) + 0.05, min(py1, rb) - 0.05
        if y1 - y0 > VIA:
            c2 += grid(px0 + 0.05, px1 - 0.05, y0, y1, 0.41, 0.48)
    v2n += keep_apart(keep_apart(c2, v1n, 0.0), v2n, 0.29)
vias(cn, V1, v1n); vias(cn, V2, v2n)

# ------------------------------------------------------------------------------------------------
# 4. P side: pad lines on the P drains (k = 10 only a stub onto the DCP anode stripes: the RP1 drain is dabp),
#    iovdd straps on the P sources, DCP side plates (iovdd; no Via2 under the iovss rail, the right plate
#    reaches up into the iovdd rail)
# ------------------------------------------------------------------------------------------------
cp = new_cell('m2_comb_p')
v1p, v2p = [], []
STRAP_P = (53.0, 84.2)
for k, xd in enumerate(P_DRN):
    top_y = 61.6 if k == RP1_K else 81.45
    box(cp, M2, xd - 0.305, JY[1] - 0.2, xd + 0.305, top_y)
    rows = [y for s in DCP_STRIPES for y in three(s)] + ([] if k == RP1_K else p_drain_rows)
    if CB['head'][0] + 0.05 <= xd - 0.3 and xd + 0.3 <= CB['head'][1] - 0.05:
        rows.append(round((HEAD[0] + HEAD[1]) / 2 - 0.095, 3))          # CMB gate = pad: Via1 onto its gate head
    v1p += [(round(xd + dx - 0.095, 3), y) for dx in (-0.205, 0.205) for y in rows]
for xs in P_SRC:
    box(cp, M2, xs - 0.1, STRAP_P[0], xs + 0.1, STRAP_P[1])
    rows = [y for b in DCP_BARS for y in three(b)] + [PY + 1.875] + p_drain_rows + [PY + 17.195]
    mine = [(round(xs - 0.095, 3), round(y, 3)) for y in rows]
    v1p += mine
    c2 = [(round(xs - 0.095, 3), round(66.1 + 0.41 * m, 3)) for m in range(50)]
    v2p += keep_apart([p for p in c2 if in_rail(p[1], (IOVDD_RAIL,)) and p[1] + VIA <= STRAP_P[1] - 0.05], mine, 0.0)
for px0, px1, py1, sb in ((4.35, P_SRC[0] + 0.1, DCP_Y + 10.26 + 0.11, (DCP_X[0], DCP_X[0] + 1.26)),
                          (P_DRN[-1] + 0.305 + 0.28, 75.65, 68.0, (DCP_X[1] - 1.26, DCP_X[1]))):
    py0 = DCP_Y - 0.13
    box(cp, M2, px0, py0, px1, py1)
    a, b = max(px0, DCP_X[0]) + 0.05, min(px1, DCP_X[1]) - 0.05
    c1 = grid(sb[0] + 0.05, sb[1] - 0.05, DCP_Y + 0.05, DCP_Y + 10.26 - 0.05)
    for yb in DCP_BARS:
        c1 += grid(a, b, yb + 0.05, yb + 1.26 - 0.05)
    if py1 > 67.2:                                                   # P frame inner ring (iovdd), bottom side
        c1 += grid(px0 + 0.05, px1 - 0.05, PY + 1.8 + 0.05, PY + 2.14 - 0.05)
    new1 = keep_apart(c1, v1p, 0.22); v1p += new1
    if py1 > 67.2:
        c2 = grid(px0 + 0.05, px1 - 0.05, IOVDD_RAIL[0] + 0.05, py1 - 0.05, 0.41, 0.48)
        v2p += keep_apart(keep_apart(c2, v1p, 0.0), v2p, 0.29)
vias(cp, V1, v1p); vias(cp, V2, v2p)

# ------------------------------------------------------------------------------------------------
# 5. pad junction in Metal2 (cut for dabn), Via1 onto CMA's S/D frame (pad), iovss stubs on the DCP guard ring
# ------------------------------------------------------------------------------------------------
DABN = (38.15, 38.45)                                    # dabn track
cj = new_cell('m2_junction')
JL, JR = (3.0, DABN[0] - 0.27), (DABN[1] + 0.27, 74.0)
box(cj, M2, JL[0], JY[0], JL[1], JY[1]); box(cj, M2, JR[0], JY[0], JR[1], JY[1])
v1j = grid(CA['end_l'][0] + 0.05, CA['end_r'][1] - 0.05, JY[0] + 0.05, JY[1] - 0.05, 0.41, 0.48)
v2j = []
GY = DCP_Y - 1.66                                        # DCP guard ring bottom side, Activ / M1 51.42 .. 51.76
for k, xs in enumerate(P_SRC):
    sx0, sx1 = xs - 0.6, xs + 0.6
    if sx1 > DABN[0] - 0.27 and sx0 < DABN[1] + 0.27:
        sx1 = DABN[0] - 0.27
    box(cj, M2, sx0, 51.2, sx1, 52.2)
    xs_ = [x for x, _ in grid(sx0 + 0.05, sx1 - 0.05, 0, VIA)]
    v1j += [(x, round(GY + 0.075, 3)) for x in xs_]       # Via1 on the guard ring (iovss)
    v2j += [(x, 51.9) for x in xs_]                       # Via2 up into the iovss rail (34.5 .. 60)
vias(cj, V1, v1j); vias(cj, V2, v2j)

# ------------------------------------------------------------------------------------------------
# 6. replica lines: dabn from the RN1 drain (upper N frame, x 39.045) on the track x 38.15 .. 38.45;
#    dabp from the RP1 drain (x 39.245), a 0.61 line like the OP drains' pad lines. Pins 85 .. 86.
# ------------------------------------------------------------------------------------------------
cr = new_cell('replica_lines')
xd = N_DRN[RN1_K]
box(cr, M2, DABN[0], 18.255, xd + 0.305, 22.765)
box(cr, M2, DABN[0], 18.255, DABN[1], 86.0)
vias(cr, V1, [(round(xd + dx - 0.095, 3), y) for dx in (-0.205, 0.205) for y in n_drain_rows(NY[1])])
xd = P_DRN[RP1_K]
box(cr, M2, xd - 0.305, 67.805, xd + 0.305, 86.0)
vias(cr, V1, [(round(xd + dx - 0.095, 3), y) for dx in (-0.205, 0.205) for y in p_drain_rows])
for name, x0, x1 in (('dabn', DABN[0], DABN[1]), ('dabp', xd - 0.305, xd + 0.305)):
    box(cr, M2P, x0, 85.0, x1, 86.0); label(cr, M2T, name, round((x0 + x1) / 2, 3), 85.5)

# ------------------------------------------------------------------------------------------------
# 7. gate feeds: each bus segment from its own frame end (Metal1 extension + 0.8 x 0.8 landing, 2 x 2 Via1),
#    b down the cell edges x 0.5 .. 1.0 / 79.0 .. 79.5, a at x 3.2 .. 3.7 / 77.0 .. 77.5, joined above the
#    P frame (a 86.4 .. 87.0, b 87.4 .. 88.0); a to CMA's gate head, b to CMB's S/D / well frame.
# ------------------------------------------------------------------------------------------------
cg = new_cell('gate_feeds')
v1g = []
B_L, B_R, A_L, A_R = (0.5, 1.0), (79.0, 79.5), (3.2, 3.7), (77.0, 77.5)
AJ, BJ = (86.4, 87.0), (87.4, 88.0)


def feed(bus_y, x_end, side, lx, wire):
    """Metal1 from the bus end x_end out to a landing at lx (left edge), Via1 2 x 2, Metal2 landing + tab to wire."""
    by0, by1 = bus_y
    if side == 'L':
        box(cg, M1, lx + 0.4, by0, x_end + 0.1, by1)
    else:
        box(cg, M1, x_end - 0.1, by0, lx + 0.4, by1)
    box(cg, M1, lx, by1 - 0.8, lx + 0.8, by1)
    pts = [(round(lx + 0.065 + i * 0.48, 3), round(by1 - 0.8 + 0.065 + j * 0.48, 3)) for i in range(2) for j in range(2)]
    v1g.extend(pts)
    box(cg, M2, min(lx, wire[0]), by1 - 0.8, max(lx + 0.8, wire[1]), by1)


for y0 in NY:                                            # N frames: gate net b, buses at origin + 7.37 .. 7.53
    by = (y0 + fN['bus'][0] / 1000, y0 + fN['bus'][1] / 1000)
    feed(by, 6.975, 'L', 3.5, B_L)                       # strip[0] left edge 6.975
    feed(by, 72.755, 'R', 75.7, B_R)                     # strip[34] right edge 72.755
by = (PY + fP['bus'][0] / 1000, PY + fP['bus'][1] / 1000)  # P frame: gate net a
feed(by, 8.075, 'L', 5.0, A_L)                           # strip[0] left edge 8.075
feed(by, 71.655, 'R', 74.2, A_R)                         # strip[42] right edge 71.655
box(cg, M2, B_L[0], 13.53 - 0.8, B_L[1], BJ[1]); box(cg, M2, B_R[0], 13.53 - 0.8, B_R[1], BJ[1])
box(cg, M2, A_L[0], HEAD[0] + 0.03, A_L[1], AJ[1]); box(cg, M2, A_R[0], by[1] - 0.8, A_R[1], AJ[1])
box(cg, M2, A_L[0], AJ[0], A_R[1], AJ[1]); box(cg, M2, B_L[0], BJ[0], B_R[1], BJ[1])
# a onto CMA's gate head (extended to x 3.0): landing 3.1 .. 3.81, two Via1
box(cg, M2, 3.1, HEAD[0] + 0.03, 3.81, HEAD[1] - 0.03)
v1g += [(3.155, round(HEAD[0] + 0.085, 3)), (3.565, round(HEAD[0] + 0.085, 3))]
# b onto CMB's right S/D + ntap column (Metal2 over it, 2 Via1 columns), tab to b at the right edge
ex0, ex1 = CB['end_r']
box(cg, M2, ex0, 42.2, ex1, 49.8); box(cg, M2, ex0, 45.57, B_R[1], 46.34)
v1g += [(round(x, 3), y) for x in (ex0 + 0.05, ex1 - 0.05 - VIA) for _, y in grid(0, VIA, 42.25, 49.75, 0.41, 0.48)]
vias(cg, V1, v1g)
for name, x0, (y0, y1) in (('a', 35.5, AJ), ('b', 40.5, BJ)):
    box(cg, M2P, x0, y0, x0 + 2.0, y1); label(cg, M2T, name, x0 + 1.0, round((y0 + y1) / 2, 3))

for c in (cn, cp, cj, cr, cg, cma, cmb):
    print('%-14s' % c.name, ', '.join('%s %d' % (ly.get_info(li).to_s(), c.shapes(li).size()) for li in ly.layer_indexes() if c.shapes(li).size()))

lo = db.SaveLayoutOptions(); lo.format = "GDS2"; lo.write_context_info = True
lo.gds2_write_timestamps = False                  # byte-reproducible: rerun gives the same sha256
ly.write(OUT, lo)
print('written', OUT)
