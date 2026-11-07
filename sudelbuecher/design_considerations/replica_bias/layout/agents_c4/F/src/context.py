# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4), v2: pad_ref_rb at slot7's right edge between the S2D and D2S pin groups (slot files read
only, unchanged), the custom-pad pins (slot7_pins.md) and straight-line sketches of the outputs.
    python3 context.py <slot.klay.gds> <slot7_pins.md> <pad_ref_rb.gds> <x_right> <out.png>
Position: the cell's right edge at x_right; its vcm pin at the height of the D2S vref pin (straight out)."""
import sys

import klayout.db as db
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402
from matplotlib.patches import Rectangle              # noqa: E402

slot, pins_md, cell, XR, png = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
win = (400.0, 90.0, 545.0, 273.0)
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

c = db.Layout()
c.read(cell)
top = c.cell('pad_ref_rb')
loc = {sh.text_string: (sh.text.x * u, sh.text.y * u) for sh in top.shapes(c.find_layer(10, 25)).each() if sh.is_text()}
X0 = XR - top.dbbox().width()
Y0 = 223.34 - loc['vcm'][1]                          # D2S vref pin centre (slot7_pins.md: 223.195 .. 223.485)
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
# outputs: vcm straight out to the D2S vref; vcm and vref down the right side to the S2D pins (top-level routes)
for net, target, xt in (('vcm', 's7_an_1_vref', None), ('vcm', 's7_an_0_vcm', 534.2), ('vref', 's7_an_0_vref', 533.6)):
    px, py = ports[net]
    x0, y0, x1, y1, _ = bp[target]
    ym = (y0 + y1) / 2
    xs_, ys_ = ([px, x0], [py, ym]) if xt is None else ([px, xt, xt, x0], [py, py, ym, ym])
    for a_ in (ax, az):
        a_.plot(xs_, ys_, color=COL[net], lw=1.2, ls='-' if xt is None else '--')
# inputs and supplies leave on the left edge (toward the bias sources / bias_dist_pd; own enables)
for net in ('en_3v3', 'en_3v3_b', 'iref', 'vddh', 'vssh'):
    px, py = ports[net]
    for a_ in (ax, az):
        a_.annotate('', xy=(px - 12, py), xytext=(px, py), arrowprops=dict(arrowstyle='->', color=COL.get(net, '#555555'), lw=1))
    az.text(px - 12.5, py, net, fontsize=7, ha='right', va='center', color=COL.get(net, '#555555'))
for net, (px, py) in ports.items():
    if net in COL:
        for a_ in (ax, az):
            a_.plot(px, py, 'o', ms=3, color=COL[net])
        if net in ('vcm', 'vref'):
            az.text(px - 0.4, py, net, fontsize=8, ha='right', va='center', color=COL[net])
ax.text(402, 271, 'slot7 (537.15 x 273 um), right edge; orange: Metal3 custom-pad pins (slot7_pins.md);\n'
        'solid: vcm straight out to the D2S vref; dashed: vcm and vref down the right side to the S2D pins\n'
        '(top-level routes, sketched); arrows: inputs and supplies on the left edge', fontsize=7, va='top')
ax.set_xlim(win[0], win[2])
ax.set_ylim(win[1], win[3])
ax.set_aspect('equal')
ax.set_xlabel('x (um, slot coordinates)')
ax.set_ylabel('y (um)')
ax.set_title('pad_ref_rb placed in slot7 (Claude, agent F, C4)', fontsize=10)
az.set_xlim(440, 540)
az.set_ylim(100, 265)
az.set_aspect('equal')
az.set_xlabel('x (um, slot coordinates)')
az.set_title('zoom: the cell and the S2D / D2S pins', fontsize=10)
fig.tight_layout()
fig.savefig(png, dpi=130)
print('ports in slot coordinates:', {k: (round(v[0], 2), round(v[1], 2)) for k, v in ports.items()})
