import sys, klayout.lay as lay, klayout.db as db
gds, out = sys.argv[1], sys.argv[2]
v = lay.LayoutView(); v.load_layout(gds, True)
v.load_layer_props('/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/sg13cmos5l.lyp')
v.max_hier(); v.set_config('background-color', '#ffffff'); v.set_config('grid-visible', 'false')
hide = {(30,0),(50,0),(126,0),(49,0),(125,0),(189,4)}  # ring rails and their vias would hide everything below
it = v.begin_layers()
while not it.at_end():
    p = it.current()
    if p.source_layer in {l for l, _ in hide}: p.visible = False; v.set_layer_properties(it, p)
    it.next()
c = v.active_cellview().layout().top_cell()
v.zoom_box(db.DBox(-2, -2, 82, 182)); v.save_image(out, 840, 1890)
