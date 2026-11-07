# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): pad_ref_rb in the bottom-right corner of slot7 (slot files read only, unchanged), the custom-
pad pins on the slot's right edge (slot7_pins.md) and straight-line sketches of the connections.
    python3 context.py <slot.klay.gds> <slot7_pins.md> <pad_ref_rb.gds> <x0> <y0> <out.png>
(x0, y0): proposed position of pad_ref_rb's lower left corner in slot coordinates."""
import sys

import klayout.db as db
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402
from matplotlib.patches import Rectangle              # noqa: E402

slot, pins_md, cell, X0, Y0, png = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
win = (400.0, 0.0, 545.0, 273.0)
fig, (ax, az) = plt.subplots(1, 2, figsize=(15, 14), gridspec_kw=dict(width_ratios=[1.05, 1]))
u = 0.001


def draw(layout, cellname, t, layers):
    for a_ in (ax, az):
        _draw(a_, layout, cellname, t, layers)


def _draw(ax, layout, cellname, t, layers):
    c = layout.cell(cellname)
    clip = db.Region(db.DBox(*win).to_itype(u))
    for (l, d), col, a in layers:
        li = layout.find_layer(l, d)
        if li is None:
            continue
        r = (db.Region(c.begin_shapes_rec(li)).transformed(t) & clip).merged()
        ps = [[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in r.decompose_trapezoids_to_region().each()]
        ax.add_collection(PolyCollection(ps, facecolor=col, alpha=a, edgecolor='none'))


s = db.Layout()
s.read(slot)
draw(s, 'slot', db.Trans(), [((10, 0), '#8040c0', 0.6), ((30, 0), '#d08020', 0.6), ((10, 23), '#999999', 0.25)])
for a_ in (ax, az):
    a_.add_patch(Rectangle((0, 0), 537.15, 273, fill=False, ec='black', lw=1.2))
ax.text(534.15, 41.3, 'M2 vss_1v2\n(frame)', fontsize=7, ha='right', va='center', rotation=90)
ax.text(536.15, 20, 'edge keep-out', fontsize=7, rotation=90, ha='center', va='center')
c = db.Layout()
c.read(cell)
top = c.cell('pad_ref_rb')
t = db.Trans(db.Vector(int(round(X0 / u)), int(round(Y0 / u))))
draw(c, 'pad_ref_rb', t, [((31, 0), '#2e8b57', 0.25), ((1, 0), '#22aa22', 0.3), ((8, 0), '#3a8fd9', 0.3),
                          ((10, 0), '#8e7cc3', 0.35)])
bb = top.dbbox().moved(X0, Y0)
ax.add_patch(Rectangle((bb.left, bb.bottom), bb.width(), bb.height(), fill=False, ec='#b03030', lw=1.5))
ax.text(bb.center().x, bb.bottom + 20, 'pad_ref_rb\n%.2f x %.2f um\nat (%.2f, %.2f)' % (bb.width(), bb.height(), X0, Y0),
        ha='center', fontsize=9, color='#b03030', weight='bold', bbox=dict(fc='white', ec='none', alpha=0.8))
# the cell's ports
ports = {}
for li in (c.find_layer(10, 25),):
    for sh in top.shapes(li).each():
        if sh.is_text():
            ports[sh.text_string] = (sh.text.x * u + X0, sh.text.y * u + Y0)
# boundary pins
bp = {}
for line in open(pins_md):
    f = [x.strip() for x in line.split('|')]
    if len(f) > 9 and f[1].startswith('s7_an'):
        x0, x1, y0, y1 = (float(v) for v in f[6:10])
        bp[f[1]] = (x0, y0, x1, y1, f[3])
        for a_, fs in ((ax, 6.5), (az, 8)):
            a_.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, color='#d08020'))
            a_.text(x1 + 0.3, (y0 + y1) / 2, f[1].replace('s7_an_', 'an')[:20], fontsize=fs, va='center')
COL = {'vref': '#e377c2', 'vcm': '#9467bd', 'en_3v3': '#2ca02c', 'en_3v3_b': '#d62728', 'iref': '#1f77b4'}
for net, target in (('vref', 's7_an_0_vref'), ('vcm', 's7_an_0_vcm'), ('en_3v3', 's7_an_0_en_3v3'),
                    ('en_3v3_b', 's7_an_0_en_3v3_b'), ('iref', 's7_an_0_iref'), ('vcm', 's7_an_1_vref')):
    px, py = ports[net]
    x0, y0, x1, y1, _ = bp[target]
    for a_ in (ax, az):
        a_.plot([px, x0], [py, (y0 + y1) / 2], color=COL[net], lw=1.2, ls='--' if target == 's7_an_1_vref' else '-')
for net, (px, py) in ports.items():
    if net in COL:
        for a_ in (ax, az):
            a_.plot(px, py, 'o', ms=3, color=COL[net])
        az.text(px - 0.4, py, net, fontsize=8, ha='right', va='center', color=COL[net])
ax.text(402, 268, 'slot7 (537.15 x 273 um), bottom-right corner; orange: Metal3 custom-pad pins (slot7_pins.md);\n'
        'lines: straight sketches of the five connections (dashed: vcm also = D2S vref); vddh / vssh on the cell\'s '
        'left edge', fontsize=7, va='top')
ax.set_xlim(win[0], win[2])
ax.set_ylim(win[1], win[3])
ax.set_aspect('equal')
ax.set_xlabel('x (um, slot coordinates)')
ax.set_ylabel('y (um)')
ax.set_title('pad_ref_rb placed in slot7 (Claude, agent F, C4)', fontsize=10)
az.set_xlim(505, 540)
az.set_ylim(90, 165)
az.set_aspect('equal')
az.set_xlabel('x (um, slot coordinates)')
az.set_title('zoom: the cell\'s pins (1.08 um pitch) and the S2D pins', fontsize=10)
fig.tight_layout()
fig.savefig(png, dpi=130)
print('ports in slot coordinates:', {k: (round(v[0], 2), round(v[1], 2)) for k, v in ports.items()})
