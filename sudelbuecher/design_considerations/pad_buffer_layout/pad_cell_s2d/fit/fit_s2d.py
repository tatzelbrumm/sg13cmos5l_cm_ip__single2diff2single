# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Tentative fit of the s2d buffer's blocks into the free region of the cleaned-out pad template (C3, 2026-11-03).

    python3 fit_s2d.py <template.gds> <out dir>

Placement only, no routing (as C2's stage A): bounding boxes of the drawn cells, bottom-left fill into the free region,
rotations 0 / 90 deg, several block orders, the order that places the most area wins. Three variants:
  A  drawn cells, 2 um between boxes (the library's own packing gap; no room for wiring)
  B  drawn cells, 4 um between boxes (a rough allowance for wiring channels; reasoning, not measured)
  C  boxes scaled by the compaction C2's reviewed rebuild measured on the d2s counterparts (budget.py), 4 um
Writes fit_<variant>.gds (template + placed cells, variants A, B; C is boxes only), fit.md (tables).
"""
import os, random, sys
import klayout.db as db

TPL, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, '../../klayout/pad_buffer_cells.gds')
N2 = os.path.join(HERE, '../../../../sg13cmos5l_IOPadDiff2Single_build/agents_c2/N2/out/d2s_n2_cells.gds')
# blocks: (name, cell, source, group, C2 compaction ratio for variant C)
BLOCKS = [('inputs', 's2d_inputs', LIB, 'xa', 1.08), ('tails', 's2d_tails', LIB, 'xa', 0.67),
          ('loads', 's2d_loads', LIB, 'xa', 0.79), ('casc_p', 's2d_casc_p', LIB, 'xa', 0.98),
          ('casc_n', 's2d_casc_n', LIB, 'xa', 1.17), ('sinks', 'sinks_6x6_s2d_c2', N2, 'xa', 1.0),
          ('sinks_cmfb', 's2d_sinks_cmfb', LIB, 'xa', 0.88), ('rhigh', 's2d_rhigh', LIB, 'xa', 0.92),
          ('pd_p', 's2d_pd_p', LIB, 'xa', 1.54), ('pd_n', 's2d_pd_n', LIB, 'xa', 2.73),
          ('cload', 's2d_cload', LIB, 'xa (cload)', 1.0),
          ('tree_n', 'bias_tree_n', LIB, 'xt', 0.85), ('tree_p', 'bias_tree_p', LIB, 'xt', 0.78),
          ('tree_sw', 'bias_tree_sw', LIB, 'xt', 1.0), ('tree_swp', 'bias_tree_swp', LIB, 'xt', 1.0)]
# free region of template version 4 (µm): the cell inside the edge strips, minus the protection and its wiring,
# each kept 1.5 µm away (the risers 0.5 µm: M2 only)
REGION = (1.8, 32.68, 78.2, 180.0)
OBST = [(0.0, 0.0, 39.45, 32.68),       # CN (NWell to 30.10), DN, the pad pin strap (to 31.18)
        (37.0, 0.0, 42.8, 38.20),       # RN / RP (EXTBlock to 36.68) and the CP gate line
        (40.3, 0.0, 80.0, 43.10),       # DP, CP, the iovdd bar (to 41.6)
        (42.1, 0.0, 45.7, 73.05),       # left iovdd riser (to 72.55)
        (75.0, 0.0, 80.0, 73.05)]       # right iovdd riser


def sizes():
    out = []
    for name, cell, src, grp, ratio in BLOCKS:
        ly = db.Layout()
        ly.read(src)
        b = ly.cell(cell).dbbox()
        out.append((name, cell, src, grp, ratio, b))
    return out


def overlap(a, b):
    return a[0] < b[2] - 1e-9 and b[0] < a[2] - 1e-9 and a[1] < b[3] - 1e-9 and b[1] < a[3] - 1e-9


def place(items, gap, order):
    placed, rest = [], []
    for i in order:
        name, w, h = items[i]
        best = None
        for rw, rh, rot in ((w, h, 0), (h, w, 90)):
            xs = {REGION[0]} | {r[2] for r in OBST} | {p[3] + gap for p in placed}
            ys = {REGION[1]} | {r[3] for r in OBST} | {p[4] + gap for p in placed}
            for y in sorted(ys):
                if best and y > best[1]:
                    break
                for x in sorted(xs):
                    r = (x, y, x + rw, y + rh)
                    if r[0] < REGION[0] - 1e-9 or r[1] < REGION[1] - 1e-9 or r[2] > REGION[2] + 1e-9 or r[3] > REGION[3] + 1e-9:
                        continue
                    if any(overlap(r, o) for o in OBST):
                        continue
                    if any(overlap(r, (p[1] - gap, p[2] - gap, p[3] + gap, p[4] + gap)) for p in placed):
                        continue
                    if not best or (y, x) < (best[1], best[0]):
                        best = (x, y, rot, rw, rh)
                    break
        if best:
            x, y, rot, rw, rh = best
            placed.append((i, x, y, x + rw, y + rh, rot))
        else:
            rest.append(i)
    return placed, rest


def best_fit(items, gap, tries=60):
    n = len(items)
    area = lambda i: items[i][1] * items[i][2]
    orders = [sorted(range(n), key=lambda i: -area(i)), sorted(range(n), key=lambda i: -max(items[i][1:])),
              sorted(range(n), key=lambda i: -items[i][2]), sorted(range(n), key=lambda i: -items[i][1])]
    rnd = random.Random(1)
    for _ in range(tries):
        o = orders[0][:]
        rnd.shuffle(o)
        orders.append(o)
    best = None
    for o in orders:
        placed, rest = place(items, gap, o)
        got = sum(area(p[0]) for p in placed)
        # xa first: an order that leaves an xa block out loses against one that leaves only xt / cload out
        key = (-sum(1 for i in rest if items[i][0] in XA), got)
        if not best or key > best[0]:
            best = (key, placed, rest)
    return best[1], best[2]


S = sizes()
XA = {s[0] for s in S if s[3] == 'xa'}
free = (REGION[2] - REGION[0]) * (REGION[3] - REGION[1])
free_reg = db.Region(db.DBox(*REGION).to_itype(0.001)) - db.Region([db.DBox(*o).to_itype(0.001) for o in OBST])
free = free_reg.area() * 1e-6
md = [f'# Tentative fit of the s2d blocks into template version 4\n',
      f'Free region: {free:.0f} µm² (x {REGION[0]}–{REGION[2]}, y {REGION[1]}–{REGION[3]}, minus the protection '
      'zone, the rppds and the iovdd risers with 1.5 / 0.5 µm keep-out). Placement only, no wiring.\n',
      '| block | cell | group | drawn w × h (µm) | area µm² |', '|---|---|---|---|---:|']
for name, cell, src, grp, ratio, b in S:
    md.append(f'| {name} | `{cell}` | {grp} | {b.width():.2f} × {b.height():.2f} | {b.width() * b.height():.0f} |')
for var, gap, scale in (('A', 2.0, False), ('B', 4.0, False), ('C', 4.0, True)):
    items = [(s[0], s[5].width() * (s[4] ** 0.5 if scale else 1), s[5].height() * (s[4] ** 0.5 if scale else 1)) for s in S]
    placed, rest = best_fit(items, gap)
    a = lambda i: items[i][1] * items[i][2]
    tot = {g: sum(a(i) for i, s in enumerate(S) if s[3] == g) for g in ('xa', 'xa (cload)', 'xt')}
    got = {g: sum(a(p[0]) for p in placed if S[p[0]][3] == g) for g in tot}
    md += [f'\n## Variant {var}: {"C2-compacted box estimates" if scale else "drawn cells"}, {gap:g} µm between boxes\n',
           f'- placed: {", ".join(items[p[0]][0] for p in placed)}',
           f'- left out: {", ".join(items[i][0] for i in rest) or "none"}',
           f'- cells placed {sum(got.values()):.0f} of {sum(tot.values()):.0f} µm² '
           f'(xa {got["xa"]:.0f} / {tot["xa"]:.0f}, cload {got["xa (cload)"]:.0f} / {tot["xa (cload)"]:.0f}, '
           f'xt {got["xt"]:.0f} / {tot["xt"]:.0f}); {sum(got.values()) / free:.0%} of the free region',
           f'- highest placed box top: y {max(p[4] for p in placed):.1f}']
    if scale:
        continue
    ly = db.Layout()
    ly.read(TPL)
    top = ly.top_cell()
    srcs = {}
    for p in placed:
        name, cell, src, grp, ratio, b = S[p[0]]
        if src not in srcs:
            srcs[src] = db.Layout()
            srcs[src].read(src)
        c = ly.cell(cell + '_fit') or ly.create_cell(cell + '_fit')
        if c.is_empty():
            c.copy_tree(srcs[src].cell(cell))
        x, y, rot = p[1], p[2], p[5]
        t = db.DCplxTrans(1, rot, False, 0, 0)
        bb = b.transformed(t)
        top.insert(db.DCellInstArray(c.cell_index(), db.DCplxTrans(1, rot, False, x - bb.left, y - bb.bottom)))
        top.shapes(ly.layer(63, 0)).insert(db.DText(f'FIT {name}', db.DTrans(x + 0.5, y + 0.5)))
    o = db.SaveLayoutOptions()
    o.gds2_write_timestamps = False
    ly.write(os.path.join(OUT, f'fit_{var}.gds'), o)
open(os.path.join(OUT, 'fit.md'), 'w').write('\n'.join(md) + '\n')
print('\n'.join(md))
