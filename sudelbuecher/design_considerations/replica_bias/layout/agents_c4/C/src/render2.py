# s7_ctrl.png: merged layers (flattened) + pin names (Claude, agent C, C4)
import klayout.db as db, sys, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
ly = db.Layout(); ly.read(sys.argv[1]); c = ly.cell('s7_ctrl')
LAY = [((31, 0), 'NWell', '#c8e6c9', 0.5), ((1, 0), 'Activ', '#2e7d32', 0.55), ((5, 0), 'GatPoly', '#d32f2f', 0.7),
       ((8, 0), 'Metal1', '#1565c0', 0.40), ((10, 0), 'Metal2', '#ef6c00', 0.45), ((19, 0), 'Via1', '#000000', 0.9)]
fig, ax = plt.subplots(figsize=(24, 14), dpi=100)
for (l, d), name, col, a in LAY:
    li = ly.find_layer(l, d)
    if li is None: continue
    r = db.Region(c.begin_shapes_rec(li)).merged()
    for p in r.each():
        pts = [(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()]
        ax.add_patch(Polygon(pts, closed=True, fc=col, ec='none', alpha=a))
    ax.plot([], [], 's', color=col, alpha=a, ms=12, label=name)
bb = c.dbbox(); ax.add_patch(Polygon([(bb.left, bb.bottom), (bb.right, bb.bottom), (bb.right, bb.top), (bb.left, bb.top)],
                                    closed=True, fc='none', ec='k', lw=1))
for line in open(sys.argv[3]):
    if line.startswith('#'): continue
    n, lay, x1, y1, x2, y2 = line.split(); x1, y1, x2, y2 = map(float, (x1, y1, x2, y2))
    ax.add_patch(Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], closed=True, fc='magenta', ec='magenta'))
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    if y2 >= bb.top - 0.01: ax.text(cx, bb.top + 0.3, n, rotation=90, ha='center', va='bottom', fontsize=11)
    elif y1 <= 0.01: ax.text(cx, -0.3, n, rotation=90, ha='center', va='top', fontsize=11)
    elif x1 <= 0.01: ax.text(-0.3, cy, n, ha='right', va='center', fontsize=12)
    else: ax.text(x2 + 0.3, cy, n, ha='left', va='center', fontsize=12)
ax.set_xlim(bb.left - 3, bb.right + 4); ax.set_ylim(bb.bottom - 3.5, bb.top + 4.5); ax.set_aspect('equal')
ax.set_title('s7_ctrl  %.2f x %.2f um  (7 ls_up_fs | channel | 13 nand2_hv, 12 inv_hv, 10 tg_hv | switch tracks; pins magenta)'
             % (bb.width(), bb.height()))
ax.set_xlabel('um'); ax.legend(loc='upper right', bbox_to_anchor=(1.0, 0.62), fontsize=11)
fig.tight_layout(); fig.savefig(sys.argv[2])
