"""render.py <gds> <cell> <png> [x1 y1 x2 y2] [w px]"""
import sys, klayout.lay as lay, klayout.db as db
gds, cell, png = sys.argv[1:4]
v = lay.LayoutView()
v.load_layout(gds, True)
v.load_layer_props("/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/sg13cmos5l.lyp")
v.select_cell(v.active_cellview().layout().cell(cell).cell_index(), 0)
v.max_hier()
w = int(sys.argv[9]) if len(sys.argv) > 9 else 1400
if len(sys.argv) > 8:
    v.zoom_box(db.DBox(*[float(a) for a in sys.argv[4:8]]))
else:
    v.zoom_fit()
b = v.box()
h = int(w * b.height() / b.width())
v.save_image_with_options(png, w, h, 0, 0, 0, db.DBox(), True)
