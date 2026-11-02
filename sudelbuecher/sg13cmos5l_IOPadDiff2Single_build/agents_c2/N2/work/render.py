"""render.py <gds> <cell> <png> [x0 y0 x1 y1] : PNG with the PDK layer properties"""
import sys
import klayout.lay as lay, klayout.db as db
gds, cell, png = sys.argv[1:4]
v = lay.LayoutView()
v.load_layout(gds, True)
v.load_layer_props("/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/sg13cmos5l.lyp")
ly = v.cellview(0).layout()
v.select_cell(ly.cell(cell).cell_index(), 0)
v.max_hier()
v.set_config("background-color", "#ffffff")
v.set_config("grid-visible", "false")
v.set_config("text-font", "3")
v.set_config("default-text-size", "0.3")
if len(sys.argv) > 4:
    x0, y0, x1, y1 = map(float, sys.argv[4:8])
    v.zoom_box(db.DBox(x0, y0, x1, y1))
else:
    v.zoom_fit()
b = v.box()
w = 1800
h = int(w * b.height() / b.width())
v.save_image(png, w, max(300, min(h, 3000)))
