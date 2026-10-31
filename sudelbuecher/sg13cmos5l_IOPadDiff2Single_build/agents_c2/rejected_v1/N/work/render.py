import sys, klayout.db as db
try:
    import klayout.lay as lay
except Exception as e:
    print("nolay", e); sys.exit(1)
gds, cell, png = sys.argv[1:4]
w = int(sys.argv[4]) if len(sys.argv)>4 else 1200
h = int(sys.argv[5]) if len(sys.argv)>5 else 1200
lv = lay.LayoutView()
lv.load_layout(gds, True)
lv.active_cellview().cell_name = cell
lv.load_layer_props("/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/sg13cmos5l.lyp")
lv.max_hier()
lv.zoom_fit()
lv.save_image(png, w, h)
